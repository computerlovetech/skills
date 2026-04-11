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

### [setup-agent-workspace](./setup-agent-workspace/)

| Skill | Description |
|-------|-------------|
| `/setup-agent-workspace` | Set up a persistent `workspace/` directory for AI agents to store artifacts, reports, and notes across sessions |

### [create-ralph](./create-ralph/)

| Skill | Description |
|-------|-------------|
| `/create-ralph` | Draft a high-quality `RALPH.md` for the [ralphify](https://github.com/computerlovetech/ralphify) autonomous-agent-loop runtime: asks scoping questions, explores the project for real test/lint/type commands, drafts from scratch using the canonical 5-section body shape, bundles helper scripts when commands need shell features, and presents for review before writing |

### [distributed-plan-mode](./distributed-plan-mode/)

| Skill | Description |
|-------|-------------|
| `/distributed-plan-mode` | Drive a Claude-Code-style plan-mode interview for ambitious work and emit a set of small, self-contained plan files (one unit of work each, ordered by filename) that a fresh-context agent or the `execute-plans` ralph can ship independently. Uses Claude Code's own plan file format — Context, recommended approach, critical files, existing code to reuse, verification — rather than a heavier framework |

### [brand-guidelines-computerlove](./brand-guidelines-computerlove/)

| Skill | Description |
|-------|-------------|
| `/brand-guidelines-computerlove` | Apply Computer Love's official brand colors and typography to any artifact that may benefit from the company look-and-feel. Use when brand colors, style guidelines, visual formatting, or company design standards apply |

### [making-presentations](./making-presentations/)

| Skill | Description |
|-------|-------------|
| `/making-presentations` | Create or extend static HTML slide decks under `presentations/` using the shared iframe shell, `slides.js` manifest, and per-slide HTML. Designed for repos that follow the `PRESENTATION_GUIDE.md` architecture |

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
agr add computerlovetech/setup-agent-workspace
agr add computerlovetech/create-ralph
agr add computerlovetech/distributed-plan-mode
agr add computerlovetech/brand-guidelines-computerlove
agr add computerlovetech/making-presentations
```

agr detects your tool (Claude Code, Cursor, Copilot, etc.) and places the skills in the right directory automatically. Run `agr sync` on a new machine to install everything tracked in `agr.toml`.

## License

MIT
