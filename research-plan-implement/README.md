# Research-Plan-Implement

A three-skill workflow that separates understanding from planning from doing — with context resets between each stage. Designed for ambitious coding tasks on real codebases where you can't hold the entire architecture in your head.

## The Framework

The core idea: **quality outputs depend entirely on input quality**. Instead of dumping a vague task into an agent and hoping for the best, you guide it through three distinct phases, each producing a structured artifact that carries context forward while the conversation history resets.

### 1. Research (`/research-codebase`)

The agent explores the codebase systematically to understand the area you'll be changing. It documents what exists — components, integration points, patterns, file paths with line numbers — without suggesting changes.

**Output**: `tasks/YYYY-MM-DD-description/research.md`

### 2. Plan (`/create-plan`)

Starting from the research document, the agent creates a phased implementation plan with concrete file paths, line numbers, and verifiable success criteria for each phase. No vague hand-waving — the plan should be detailed enough to execute mechanically.

**Output**: `tasks/YYYY-MM-DD-description/plan.md`

### 3. Implement (`/implement-plan`)

The agent executes the plan phase by phase, updating checkboxes as it goes. It stops at the end of each phase for your review. If you start a new session, it picks up from the first unchecked item.

**Output**: Updated `plan.md` with `[x]` checkmarks and a summary of changes per phase.

## Why Reset Context Between Stages?

Each phase compresses its findings into a structured document, then you start a fresh session. This keeps the agent's context window clean (40-60% utilization) rather than letting it bloat with stale exploration history. The documents carry the signal forward; the noise stays behind.

## Installation

Copy the three skill directories into your tool's skills folder:

```
your-project/
├── .claude/skills/          # or .cursor/skills/, .github/skills/, .codex/skills/
│   ├── research-codebase/
│   │   └── SKILL.md
│   ├── create-plan/
│   │   └── SKILL.md
│   └── implement-plan/
│       └── SKILL.md
```

## Usage

```
# Phase 1: Research
/research-codebase
> "I need to add real-time notifications to the dashboard"

# Review research.md, then start a new session

# Phase 2: Plan
/create-plan
> "tasks/2026-03-30-realtime-notifications/research.md"

# Review plan.md, then start a new session

# Phase 3: Implement
/implement-plan
> "tasks/2026-03-30-realtime-notifications/plan.md"

# Review each phase, start new sessions between phases
```

## Credits

This workflow is a modified version of the Research-Plan-Implement framework introduced by [Dexter Horthy](https://github.com/dexhorthy) from [HumanLayer](https://humanlayer.dev). Dexter's original work on [Advanced Context Engineering for Coding Agents](https://github.com/humanlayer/advanced-context-engineering-for-coding-agents/blob/main/ace-fca.md) laid the foundation — the key insight that frequent intentional compaction of context into structured artifacts is what makes AI coding agents effective on large, real-world codebases.

These skills are packaged following the [Agent Skills open standard](https://agentskills.io) and published by [computerlove.tech](https://computerlove.tech).
