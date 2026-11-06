---
name: maintain-docs
description: Run one unattended maintenance pass over a repository's Markdown documentation — sync docs with recent code changes, fix broken links and references, cut bloat and duplication, resolve contradictions, and improve discoverability — then open a single reviewable pull request. Use for scheduled or on-demand docs upkeep in any repository.
---

# Maintain docs

One run of this skill is one maintenance pass. It is designed to run unattended, for example nightly, and to produce at most one small, reviewable pull request. If nothing needs changing, it changes nothing.

## 1. Start from the latest default branch

Before reading or checking anything, make sure the checkout matches the remote's latest default branch. Every later step analyzes this state, so a stale checkout means stale results.

- Identify the default branch (for example `main`), fetch it from the remote, check it out, and fast-forward it to the remote: `git fetch origin <default>`, `git checkout <default>`, `git pull --ff-only origin <default>`.
- If the working tree has uncommitted changes, or the local default branch has diverged from the remote, stop and report it. Never stash, reset, or discard someone else's work to get a clean state.

## 2. Orient

Learn the repository before touching it.

- Read its agent and contributor entry points: `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `README.md`, and the root of any `docs/` directory.
- Adopt any documentation conventions they state — where docs live, how they are indexed, naming, tone. The repository's own conventions override the defaults in this skill.
- Identify the files in scope: tracked Markdown files the repository owns.
- Exclude anything vendored, generated, or read-only: paths ignored by Git, dependency directories (`node_modules/`, `vendor/`, `.venv/`), build output, generated API docs, changelogs written by release tooling, and anything the repository marks as reference-only or external.
- Check for an open pull request from a previous run of this skill. If one exists, update that branch instead of opening a second one, or stop if it is awaiting review and you have nothing new.

## 3. Find what to look at

Prefer a focused pass over re-reading everything.

- List commits on the default branch since the last run. Use the previous maintenance pull request's date if there is one; otherwise use the last 24 hours. If there is no usable history, sample the docs most likely to drift: setup, commands, architecture, and configuration.
- Map changed code to the docs that describe it: docs in or near the changed directories, docs that mention changed file paths, commands, scripts, environment variables, or identifiers.
- Run the repository-wide mechanical checks (links, references, reachability) on every in-scope file. They are cheap and exact.

## 4. Checks

### Correctness

- **Out of sync with code.** Compare what docs claim against the current code, configuration, and scripts: commands, flags, file paths, environment variables, ports, default values, directory layout, and described behavior. Update the doc to match the code. Never change code to match a doc.
- **Broken links.** Relative links and anchors must resolve. Fix moved targets; remove links to targets that no longer exist.
- **Broken references.** File paths, script names, and commands mentioned in inline code must exist — check against the tree and against task runners and manifests such as `package.json`, `Makefile`, `justfile`, or `pyproject.toml`.
- **Contradictions.** When two documents give conflicting guidance on the same subject, determine which matches the code and reconcile the other to it.
- **Stale content.** Remove or rewrite sections about removed apps, packages, features, or workflows. Resolve leftover `TODO`, `TBD`, `FIXME`, and placeholder text when the answer is clear from the code; otherwise report it.

### Bloat

- **Duplication.** Keep each fact in one authoritative document and link to it from elsewhere.
- **Restated code.** Replace copied configuration, full flag lists, or code walkthroughs that the source already expresses with a short explanation and a link to the source. Keep explanations of purpose, rationale, constraints, and non-obvious operational knowledge — those are what docs are for.
- **Padding.** Tighten verbose prose, filler introductions, and repeated caveats. Do not rewrite text that is already clear just to change its style.

### Discoverability

- **Reachability.** Every persistent document should be reachable from an entry point — the root `README.md` or `AGENTS.md`, then a docs index, then a `README.md` in each docs subdirectory. Link orphaned documents from the most relevant index.
- **Indexes.** Each documentation directory should have a `README.md` that introduces its subject and links its documents. Keep existing indexes in sync with the files they list.
- **Naming.** Titles, headings, and filenames should use the terms the code and the team use, so a reader searching for a task finds the right page.
- **Link labels.** Use descriptive labels that say what the target covers, not "here" or bare URLs.
- **Gaps.** Note significant code areas — a new app, package, or service — that have no documentation entry point. Report them; do not invent documentation for behavior you cannot verify.

## 5. Make changes

- Work on a new branch created from the default branch updated in step 1. Never commit to the default branch.
- Change only what a check justifies. Keep the diff small enough to review in a few minutes; if there is more to do, do the most valuable part and leave the rest for the next run.
- Every factual change must be verifiable from the code at the current commit. When you cannot tell whether the code or the doc is wrong, do not guess — report it.
- Preserve the author's structure and voice. Don't reorganize documentation wholesale in an unattended run; propose large restructurings in the report instead.
- When moving, renaming, or deleting a document, update every link that points to it.
- Group commits by theme, such as "sync docs with code", "fix links", and "remove duplication".

## 6. Report

Open one pull request, or update the existing one. Its description lists:

- **Changes**, grouped by theme, each with the file and a one-line reason — for sync changes, the code it now matches.
- **Needs a human**: code-versus-doc conflicts you could not resolve, unresolved `TODO`s, undocumented areas, and suggested restructurings.

If there are no changes but there are items that need a human, report them without a pull request — for example as an issue — or in the run's output, whichever the repository or the caller prefers. If there is nothing at all, end the run without opening anything.
