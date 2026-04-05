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

### [docs-audit](./docs-audit/)

| Skill | Description |
|-------|-------------|
| `/docs-audit` | Audit a CLI tool's documentation quality across the full user journey (A-F grading with actionable recommendations) |

### [setup-agent-workspace](./setup-agent-workspace/)

| Skill | Description |
|-------|-------------|
| `/setup-agent-workspace` | Set up a persistent `workspace/` directory for AI agents to store artifacts, reports, and notes across sessions |

### [oss-growth-advisor](./oss-growth-advisor/)

| Skill | Description |
|-------|-------------|
| `/oss-growth-advisor` | Analyze an open source repo's positioning, market context, and adoption signals, then produce blunt, execution-oriented growth advice for a solo creator (snapshot, scorecard, top actions, 30-day plan) |

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
agr add computerlovetech/docs-audit
agr add computerlovetech/setup-agent-workspace
agr add computerlovetech/oss-growth-advisor
```

agr detects your tool (Claude Code, Cursor, Copilot, etc.) and places the skills in the right directory automatically. Run `agr sync` on a new machine to install everything tracked in `agr.toml`.

## License

MIT
