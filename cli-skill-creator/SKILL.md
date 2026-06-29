---
name: cli-skill-creator
description: >
  Create the agent skills that make a CLI "agent-native" — the computerlove.tech
  pattern used by agr and outcome-engineering, where a repo ships a "<tool>-cli"
  operating manual (teaches an agent how to drive the CLI) and a "<tool>-release"
  playbook (drives the release), both bundled under skills/ and registered in
  agr.toml. Use this whenever the user wants to onboard agents onto a CLI, give a
  CLI an in-repo skill / operating manual, add a release playbook skill, make a
  tool "agent-native", or "give this CLI a skill like agr has" — e.g. "write a
  skill so agents know how to use my CLI", "add a release skill", "create the
  -cli and -release skills".
---

# CLI Skill Creator

Two CLIs in this org — `agr` and `outcome-engineering` — ship agent skills *in
the repo* so any agent that lands there can operate the tool correctly and cut a
release without spelunking the source. This skill creates those skills for a new
CLI.

The pattern is a pair:

- **`<tool>-cli`** — the **operating manual**. Mental model + workflows +
  boundaries for driving the CLI.
- **`<tool>-release`** — the **release playbook**. Steps to cut a release that
  passes the publish pipeline on the first try.

> Companion skill: to set up the actual PyPI release pipeline these skills
> assume (`test.yml` / `publish.yml`, trusted publishing, tag-driven release),
> use **`pypi-cli-cicd`**. This skill authors the agent-facing manuals; that one
> builds the machinery.

## When to use

- The user wants agents to know how to use their CLI without reading the code.
- The user wants an in-repo release playbook for a tag-driven PyPI CLI.
- The user is replicating the agr / outcome-engineering "agent-native" setup.

Do NOT use this for: building the CI/CD pipeline itself (→ `pypi-cli-cicd`), or
authoring a general-purpose skill unrelated to a CLI (→ a generic skill-creator
such as `anthropics/skills/skill-creator`).

## What makes a good CLI operating-manual skill

The single most important quality: the `<tool>-cli` skill must let an agent use
the CLI **correctly from the skill alone**, without reading the source. That
means it leads with a **mental model** (the core nouns, the files the CLI
reads/writes, the local-vs-global / manifest-vs-lockfile distinctions, the "X
only does Y, use Z for W" gotchas), then gives **task-oriented workflows** (one
per command or job, with exact commands and the flags that matter), then
**boundaries** (never-do / confirm-before, with reasons).

It must also stay **honest**: the command list has to match `<tool> --help`. A
stale operating manual is worse than none. Bake this expectation into the skill
and into the repo's `AGENTS.md`.

## Steps

### 1. Learn the CLI surface

Read `<tool> --help` (and each subcommand's `--help`), the CLI source
(`<package>/cli.py` or `main.py`), and any config-file format the tool reads.
List the commands, the core nouns, the files it touches, and the gotchas. You
can't write an honest operating manual without this.

### 2. Write `skills/<tool>-cli/SKILL.md`

Start from `references/cli-skill-template.md`. Fill in:

- **Frontmatter** — `name` must equal the folder name. The `description` is the
  trigger; pack it with the verbs and nouns a user would say ("install", "sync",
  the tool name, its config filenames). This is what makes the skill fire.
- **Mental model** — the read-first facts.
- **Workflows** — one section per task, exact commands.
- **Boundaries** — including "don't push or `git tag`; leave releases to
  `<tool>-release`."
- **Keeping it honest** — note that the command list tracks `<tool> --help`.

If the CLI ships from PyPI and you want the skill available to users who just
`pip install` it (not only repo contributors), bundle a second copy inside the
package (e.g. `src/<package>/skills/<tool>-cli/SKILL.md`) and install it via a
`<tool> install --skills` command. If you do, document in `AGENTS.md` that
**both copies must change together** — this is the one maintenance trap of the
pattern.

### 3. Write `skills/<tool>-release/SKILL.md`

Start from `references/release-skill-template.md`. It mirrors the publish
pipeline from the operator's side: preconditions → inspect changes → local
checks (the *exact* CI commands) → docs check → bump version in `pyproject.toml`
→ update `CHANGELOG.md` (heading format the pipeline parses) → commit/tag/**wait
for confirmation**/push → monitor `gh run watch` → verify → recovery. Adjust the
local-check commands to match what this project's CI actually runs.

### 4. Register the skills in `agr.toml`

Add both as local `path` deps so they travel with the repo and need no network:

```toml
dependencies = [
    {path = "skills/<tool>-cli", type = "skill"},
    {path = "skills/<tool>-release", type = "skill"},
]
```

Full manifest (tools list, default owner/repo, source) in
`references/agr-toml-template.toml`. Then run `agr sync` to fan the skills out to
each configured tool, and commit `agr.toml` + `agr.lock`.

### 5. Verify the skills fire and read well

- Confirm the frontmatter `name` matches each folder name.
- Sanity-check the `description` triggers — read them as a user request and ask
  "would this fire?"
- Walk the `<tool>-cli` workflows against `<tool> --help` to confirm accuracy.
- Optionally test discovery/iteration with `agrx` or `agr run`.

## Boundaries

- **Keep `<tool>-cli` in sync with `<tool> --help`.** Update the skill in the
  same PR as any CLI surface change. If a bundled package copy exists, change
  both.
- **The `<tool>-release` skill must wait for user confirmation before pushing a
  tag**, and treat tag deletion as destructive.
- **`name` must equal the folder name** for every skill (registry convention).
- This skill authors the agent skills; it does not build the CI/CD pipeline
  (→ `pypi-cli-cicd`) or write the CLI's business logic.

## References

- [cli-skill-template.md](references/cli-skill-template.md) — `<tool>-cli` operating-manual skeleton
- [release-skill-template.md](references/release-skill-template.md) — `<tool>-release` playbook skeleton
- [agr-toml-template.toml](references/agr-toml-template.toml) — registering skills with agr
