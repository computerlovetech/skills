---
name: setup-instructions
description: Set up the project instruction file (CLAUDE.md / AGENTS.md). Use when starting work on a new project that doesn't have an instruction file yet. Explores the codebase, drafts the instruction file, and asks the user to review and refine it.
---

# Set Up Instruction File

Creates a concise, high-signal instruction file for the project.

## Initial Setup

Respond with:

```
I'll set up an instruction file for this project. First, let me explore the codebase to understand what's here.
```

Then immediately begin the workflow — do not wait for user input.

## Workflow

1. **Explore the codebase** — read project root files (package.json, pyproject.toml, Makefile, Cargo.toml, etc.), scan key directories, identify the tech stack, build/test/lint commands, and project structure
2. **Draft the instruction file** using the template below — fill in every section based on what you found
3. **Present the draft to the user in chat** — do NOT write the file yet. Show the full draft and ask:

```
Here's my draft. Before I write it, please review:

- **Correct** any misunderstandings — wrong commands, misidentified patterns, incorrect assumptions
- **Add** anything I missed — boundaries, team conventions, things you know that aren't in the code
- **Align** the file with how your team actually works — does this match your mental model of the project?

The goal is 15–30 lines of genuinely useful context. What should I change?
```

4. **Iterate** — incorporate the user's feedback. If they say it looks good, proceed.
5. **Determine filename** — check which skills directory exists (`.claude/`, `.cursor/`, `.github/`, `.codex/`) to infer the tool. Use `CLAUDE.md` for Claude Code, `AGENTS.md` for everything else. Confirm with the user before writing.
6. **Write the file** to the project root

## Guidelines

- **Think of this file as a contract between the team and the agent.** It defines how the agent should work in this project — what to do, what not to touch, what patterns to follow.
- Including key patterns and conventions the agent *could* discover by reading code is fine — it saves tokens and avoids the agent re-discovering them in every new session.
- Do NOT include framework documentation the agent already knows or code style rules a linter enforces.
- DO include: build/test/lint commands, architectural boundaries, established patterns, conventions, and things to avoid.
- State rules positively ("Use X") except in the Boundaries section

## Template

```markdown
# [CLAUDE.md or AGENTS.md]

## Project
<!-- 1-3 sentences: What is this? What does it do? Tech stack? -->

## Commands
<!-- The commands useful for working with this codebase. Adapt to the stack — e.g. build, test, lint, run, type-check, etc. -->


## Architecture
<!-- Key directories and what they contain. Only non-obvious ones. -->

## Conventions
<!-- Only rules a linter CANNOT enforce. -->

## Boundaries
<!-- What the agent must NOT do. Be specific about why. -->

## Testing
<!-- How tests work in this project. What pattern to follow. -->
```
