# Agent Skills by computerlove.tech

A registry of open-source agent skills published by [computerlove.tech](https://computerlove.tech).

Skills are portable workflow definitions that coding agents can follow. Each skill is a folder containing a `SKILL.md` file that encodes a repeatable workflow — the agent reads the markdown and executes the steps. Skills follow the [Agent Skills open standard](https://agentskills.io).

## Available Skill Collections

### [research-plan-implement](./research-plan-implement/)

A collection of three skills that work together as a pipeline for tackling ambitious coding tasks: research the codebase, create a concrete plan, then implement phase by phase.

| Skill | Description |
|-------|-------------|
| `/research-codebase` | Explore and document a codebase area before making changes |
| `/create-plan` | Create a phased implementation plan from research findings |
| `/implement-plan` | Execute a plan phase by phase with progress tracking |

### [setup-instructions](./setup-instructions/)

| Skill | Description |
|-------|-------------|
| `/setup-instructions` | Bootstrap a project instruction file (CLAUDE.md / AGENTS.md) by exploring the codebase and drafting a high-signal onboarding doc for the agent |

## Installation

The easiest way to install skills is with [agr](https://github.com/computerlovetech/agr), a package manager for agent skills.

### Install agr

```bash
uv tool install agr
```

### Add skills

Since this repo is named `skills`, you can use the shorthand `computerlovetech/<skill-name>` instead of `computerlovetech/skills/<skill-name>`:

```bash
# Install individual skills
agr add computerlovetech/setup-instructions
agr add computerlovetech/research-codebase
agr add computerlovetech/create-plan
agr add computerlovetech/implement-plan
```

agr detects your tool (Claude Code, Cursor, Copilot, etc.) and places the skills in the right directory automatically. Run `agr sync` on a new machine to install everything tracked in `agr.toml`.

## License

MIT
