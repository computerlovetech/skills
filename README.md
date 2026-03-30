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

### [setup-instruction-file](./setup-instruction-file/)

| Skill | Description |
|-------|-------------|
| `/setup-instruction-file` | Bootstrap a project instruction file (CLAUDE.md / AGENTS.md) by exploring the codebase and drafting a high-signal onboarding doc for the agent |

## Installation

Copy the skill directories you want into your tool's skills folder:

| Tool | Skills directory |
|------|-----------------|
| Claude Code | `.claude/skills/` |
| Cursor | `.cursor/skills/` |
| GitHub Copilot | `.github/skills/` |
| Codex | `.codex/skills/` |

Then invoke a skill by typing `/skill-name` in your agent's chat.

## License

MIT
