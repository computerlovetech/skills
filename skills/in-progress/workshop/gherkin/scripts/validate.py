#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["gherkin-official>=42,<43"]
# ///
"""Validate Gherkin .feature files.

Parses each file with the official Cucumber Gherkin parser (syntax errors) and
lints it against the guidance in this skill (warnings).

Usage:
    uv run validate.py [PATH ...] [--strict] [--json] [--ignore RULE,...] [--max-steps N]

PATH may be a file or a directory (searched recursively for *.feature).
Defaults to the current directory.

Exit codes: 0 = no errors (and no warnings with --strict), 1 = problems found,
2 = no .feature files found.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from gherkin.errors import CompositeParserException, ParserError
from gherkin.parser import Parser
from gherkin.token_scanner import TokenScanner

RULES = {
    "syntax": "File is not valid Gherkin.",
    "no-feature": "File has no Feature.",
    "empty-feature": "Feature or Rule has no scenarios.",
    "missing-name": "Feature, Rule, or Scenario has no name.",
    "duplicate-name": "Two scenarios in a feature share a name.",
    "missing-when": "Scenario has no When step.",
    "missing-then": "Scenario has no Then step.",
    "multiple-when": "Scenario has more than one When; it likely tests several behaviours.",
    "step-order": "Steps are out of Given -> When -> Then order.",
    "too-many-steps": "Scenario is longer than the step limit.",
    "background-not-given": "Background contains When or Then steps.",
    "long-background": "Background has more than 4 steps.",
    "outline-no-examples": "Scenario Outline has no Examples, or Examples have no rows.",
    "undefined-placeholder": "Placeholder has no matching Examples column.",
    "unused-column": "Examples column is not used by any placeholder.",
    "imperative-step": "Step describes UI mechanics instead of behaviour.",
    "abstract-data": "Step uses placeholder-like data instead of real data.",
}

IMPERATIVE = re.compile(
    r"\b(click(s|ed)?|press(es|ed)?|tap(s|ped)?|fill(s|ed)? in|type(s|d)? .+ into|"
    r"select(s|ed)? .+ from|scroll(s|ed)?|navigate(s|d)? to|button|checkbox|"
    r"dropdown|text ?field|input field|xpath|css selector)\b",
    re.IGNORECASE,
)
ABSTRACT = re.compile(
    r"\b((user|customer|product|item|account|test)[ _-]?\d+|foo|bar|baz|"
    r"lorem ipsum|some value|valid \w+|invalid \w+)\b",
    re.IGNORECASE,
)
PLACEHOLDER = re.compile(r"<([^<>]+)>")
OUTLINE_WORDS = ("outline", "template")


@dataclass
class Problem:
    path: str
    line: int
    column: int
    severity: str
    rule: str
    message: str

    def __str__(self) -> str:
        return f"{self.path}:{self.line}:{self.column}: {self.severity} [{self.rule}] {self.message}"


class Linter:
    def __init__(self, path: str, ignore: set[str], max_steps: int):
        self.path = path
        self.ignore = ignore
        self.max_steps = max_steps
        self.problems: list[Problem] = []

    def add(self, node: dict, severity: str, rule: str, message: str) -> None:
        if rule in self.ignore:
            return
        loc = node.get("location", {})
        self.problems.append(
            Problem(self.path, loc.get("line", 1), loc.get("column", 1), severity, rule, message)
        )

    def lint(self, document: dict) -> None:
        feature = document.get("feature")
        if not feature:
            self.add({}, "error", "no-feature", RULES["no-feature"])
            return
        if not feature["name"].strip():
            self.add(feature, "warning", "missing-name", "Feature has no name.")
        scenarios = self.container(feature, "Feature")
        seen: dict[str, dict] = {}
        for sc in scenarios:
            name = sc["name"].strip()
            if name in seen:
                first = seen[name]["location"]["line"]
                self.add(sc, "warning", "duplicate-name", f"Scenario name '{name}' also used on line {first}.")
            elif name:
                seen[name] = sc

    def container(self, node: dict, kind: str) -> list[dict]:
        """Lint a Feature or Rule and return all scenarios within it."""
        scenarios: list[dict] = []
        for child in node.get("children", []):
            if "background" in child:
                self.background(child["background"])
            elif "scenario" in child:
                self.scenario(child["scenario"])
                scenarios.append(child["scenario"])
            elif "rule" in child:
                rule = child["rule"]
                if not rule["name"].strip():
                    self.add(rule, "warning", "missing-name", "Rule has no name.")
                scenarios += self.container(rule, "Rule")
        if not scenarios:
            self.add(node, "warning", "empty-feature", f"{kind} has no scenarios.")
        return scenarios

    def background(self, bg: dict) -> None:
        for step in bg["steps"]:
            if step["keywordType"] in ("Action", "Outcome"):
                self.add(step, "warning", "background-not-given", "Background should only set context (Given).")
        if len(bg["steps"]) > 4:
            self.add(bg, "warning", "long-background", f"Background has {len(bg['steps'])} steps; keep it to a few essential Givens.")
        self.step_text(bg["steps"])

    def scenario(self, sc: dict) -> None:
        steps = sc["steps"]
        if not sc["name"].strip():
            self.add(sc, "warning", "missing-name", "Scenario has no name.")
        types = self.resolve_types(steps)
        if "Action" not in types:
            self.add(sc, "warning", "missing-when", RULES["missing-when"])
        if "Outcome" not in types:
            self.add(sc, "warning", "missing-then", RULES["missing-then"])
        whens = [s for s in steps if s["keywordType"] == "Action"]
        if len(whens) > 1:
            self.add(whens[1], "warning", "multiple-when", RULES["multiple-when"])
        order = {"Context": 0, "Action": 1, "Outcome": 2}
        highest = 0
        for step, t in zip(steps, types):
            rank = order.get(t)
            if rank is None:
                continue
            if rank < highest and step["keywordType"] != "Conjunction":
                self.add(step, "warning", "step-order", f"'{step['keyword'].strip()}' step after a later step type.")
            highest = max(highest, rank)
        if len(steps) > self.max_steps:
            self.add(sc, "warning", "too-many-steps", f"Scenario has {len(steps)} steps (limit {self.max_steps}).")
        self.step_text(steps)
        self.outline(sc)

    @staticmethod
    def resolve_types(steps: list[dict]) -> list[str]:
        """Give And/But steps the type of the step they continue."""
        types, last = [], "Unknown"
        for step in steps:
            t = step["keywordType"]
            if t not in ("Conjunction", "Unknown"):
                last = t
            types.append(last if t in ("Conjunction", "Unknown") else t)
        return types

    def step_text(self, steps: list[dict]) -> None:
        for step in steps:
            if m := IMPERATIVE.search(step["text"]):
                self.add(step, "warning", "imperative-step", f"'{m.group(0)}' describes UI mechanics; state the intent instead.")
            if m := ABSTRACT.search(step["text"]):
                self.add(step, "warning", "abstract-data", f"'{m.group(0)}' looks like placeholder data; use a real, concrete value.")

    def outline(self, sc: dict) -> None:
        examples = sc.get("examples", [])
        is_outline = bool(examples) or any(w in sc["keyword"].lower() for w in OUTLINE_WORDS)
        if not is_outline:
            return
        if not examples or not any(ex.get("tableBody") for ex in examples):
            self.add(sc, "error", "outline-no-examples", RULES["outline-no-examples"])
            return
        used = set(PLACEHOLDER.findall(sc["name"]))
        for step in sc["steps"]:
            used |= set(PLACEHOLDER.findall(step["text"]))
            if ds := step.get("docString"):
                used |= set(PLACEHOLDER.findall(ds["content"]))
            if dt := step.get("dataTable"):
                for row in dt["rows"]:
                    for cell in row["cells"]:
                        used |= set(PLACEHOLDER.findall(cell["value"]))
        for ex in examples:
            header = ex.get("tableHeader")
            if not header:
                self.add(ex, "error", "outline-no-examples", "Examples table has no header row.")
                continue
            columns = {c["value"] for c in header["cells"]}
            for name in sorted(used - columns):
                self.add(ex, "error", "undefined-placeholder", f"Placeholder <{name}> has no column in these Examples.")
            for cell in header["cells"]:
                if cell["value"] not in used:
                    self.add(cell, "warning", "unused-column", f"Column '{cell['value']}' is not used in the outline.")


def find_files(paths: list[str]) -> list[Path]:
    files: list[Path] = []
    for p in map(Path, paths):
        if p.is_dir():
            files += sorted(f for f in p.rglob("*.feature") if f.is_file())
        elif p.is_file():
            files.append(p)
        else:
            print(f"{p}: not found", file=sys.stderr)
    return files


def validate(path: Path, ignore: set[str], max_steps: int) -> list[Problem]:
    linter = Linter(str(path), ignore, max_steps)
    try:
        document = Parser().parse(TokenScanner(path.read_text(encoding="utf-8")))
    except (CompositeParserException, ParserError) as exc:
        for err in getattr(exc, "errors", [exc]):
            loc = getattr(err, "location", None) or {"line": 1, "column": 1}
            msg = re.sub(r"^\(\d+:\d+\):\s*", "", str(err))
            linter.add({"location": loc}, "error", "syntax", msg)
        return linter.problems
    linter.lint(document)
    return sorted(linter.problems, key=lambda p: (p.line, p.column))


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate Gherkin .feature files.")
    ap.add_argument("paths", nargs="*", default=["."], help="Files or directories (default: .)")
    ap.add_argument("--strict", action="store_true", help="Exit non-zero on warnings too.")
    ap.add_argument("--json", action="store_true", help="Print problems as JSON.")
    ap.add_argument("--ignore", default="", help="Comma-separated rule IDs to skip.")
    ap.add_argument("--max-steps", type=int, default=5, help="Step limit per scenario (default: 5).")
    ap.add_argument("--list-rules", action="store_true", help="List rule IDs and exit.")
    args = ap.parse_args()

    if args.list_rules:
        for rule, desc in RULES.items():
            print(f"{rule:22} {desc}")
        return 0

    files = find_files(args.paths)
    if not files:
        print("No .feature files found.", file=sys.stderr)
        return 2

    ignore = {r.strip() for r in args.ignore.split(",") if r.strip()}
    problems = [p for f in files for p in validate(f, ignore, args.max_steps)]
    errors = sum(p.severity == "error" for p in problems)
    warnings = len(problems) - errors

    if args.json:
        print(json.dumps({"files": len(files), "errors": errors, "warnings": warnings,
                          "problems": [asdict(p) for p in problems]}, indent=2))
    else:
        for p in problems:
            print(p)
        print(f"{len(files)} file(s), {errors} error(s), {warnings} warning(s)")

    return 1 if errors or (args.strict and warnings) else 0


if __name__ == "__main__":
    sys.exit(main())
