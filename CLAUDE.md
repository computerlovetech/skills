# Project Instructions

## What this is

A registry of open-source agent skills published by computerlove.tech. Each top-level folder is one skill (or a tightly related collection) containing a `SKILL.md` that defines a repeatable workflow an agent can follow. Skills follow the [Agent Skills open standard](https://agentskills.io) and are distributed via [agr](https://github.com/computerlovetech/agr).

## Layout

- `<skill-name>/SKILL.md` — the skill definition. Frontmatter `name:` must match the directory name.
- `README.md` — the public landing page. It explains what the repo is and how to install skills with `agr`, but intentionally does **not** enumerate individual skills, so it doesn't need updating when skills are added, removed, or renamed.

## README.md

The README is deliberately generic — people discover skills by browsing the folders and reading each `SKILL.md`. Don't add a per-skill list or table back to it; that's what went stale before. Only touch the README when the repo's purpose or install instructions actually change.
