# Agent Skills by computerlove.tech

A registry of open-source agent skills published by [computerlove.tech](https://computerlove.tech).

Skills are portable workflow definitions that coding agents can follow. Each skill is a folder containing a `SKILL.md` file that encodes a repeatable workflow — the agent reads the markdown and executes the steps. Skills follow the [Agent Skills open standard](https://agentskills.io).

## Browse the skills

Every top-level folder in this repo is a skill. Open its `SKILL.md` to see what it does — the frontmatter `name` and `description` explain the workflow and when to use it.

## Installation

The easiest way to install skills is with [agr](https://github.com/computerlovetech/agr), a package manager for agent skills.

```bash
# Install agr
uv tool install agr

# Add a skill (use the name of any folder in this repo)
agr add computerlovetech/<skill-name>
```

Since this repo is named `skills`, the shorthand `computerlovetech/<skill-name>` works in place of `computerlovetech/skills/<skill-name>`.

agr detects your tool (Claude Code, Cursor, Copilot, etc.) and places the skill in the right directory automatically. Run `agr sync` on a new machine to install everything tracked in `agr.toml`.

## License

MIT
