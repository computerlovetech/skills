# Project Instructions

## What this is

A registry of open-source agent skills published by computerlove.tech. Each top-level folder is one skill (or a tightly related collection) containing a `SKILL.md` that defines a repeatable workflow an agent can follow. Skills follow the [Agent Skills open standard](https://agentskills.io) and are distributed via [agr](https://github.com/computerlovetech/agr).

## Layout

- `<skill-name>/SKILL.md` — the skill definition. Frontmatter `name:` must match the directory name.
- `README.md` — the public index of skills in this repo. Used by people browsing on GitHub and by anyone discovering what's installable via `agr add computerlovetech/<skill-name>`.

## Keep README.md up to date

**When you add, remove, or rename a skill, update `README.md` in the same change.** The README lists every skill with a description and shows the `agr add` command for each one — it goes stale fast if skill changes land without touching it. Check before committing that every skill folder has a corresponding README entry and every README entry points to a folder that still exists.
