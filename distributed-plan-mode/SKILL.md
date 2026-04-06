---
name: distributed-plan-mode
description: >
  Drive a Claude-Code-style plan-mode interview for ambitious work and emit a
  set of small, self-contained plan files that a ralph (or any fresh-context
  agent) can execute independently. Use when the user wants to plan something
  too big for a single plan file — multi-subsystem refactors, migrations, new
  features touching unrelated areas, or any work they intend to run through
  the execute-plans ralph. Runs an iterative interview → explore → decompose
  → draft → review → write loop. Each emitted plan file follows Claude Code's
  plan format (Context, recommended approach, critical files, existing code
  to reuse, verification) — not the research-plan-implement/create-plan
  framework. Read-only until the user signs off, then writes numbered plan
  files to ./plans/ or ./plans/groups/<name>/ in the project repo.
---

# Distributed Plan Mode

A cross-tool planning skill that encodes the hard-earned lessons of Claude Code's plan mode and adapts them to produce **many** small plan files instead of one monolithic one. The goal is that an ambitious user request ends with a set of atomic, fresh-context-executable plan files in `./plans/` that a ralph (like `execute-plans`) or a human driving an agent can pick up and ship one at a time.

## When to Use

Use this skill for ambitious work that naturally splits into multiple independent pieces:

- Multi-subsystem refactors or migrations
- New features that touch unrelated areas of the codebase
- Staged rollouts with ordered steps (schema first, then backend, then UI)
- Any work the user plans to execute via the `execute-plans` ralph
- Work that would blow out a single plan file past ~100 lines

**Skip** this skill for tasks that fit in a single plan file — use Claude Code's built-in plan mode (or the host tool's single-plan equivalent) for those. A 3-file bug fix does not need a distributed plan.

## Initial Setup

Respond with:

```
I'll help you plan <task>. I work the way Claude Code's plan mode does —
explore a bit, write to a plan skeleton, ask you questions, refine. The
goal is a set of small self-contained plan files that a fresh-context
agent can execute independently. Let me start by understanding the scope.
```

Then immediately begin **Phase 0**. Do not wait for further prompting.

## Workflow

### Phase 0: Check for existing plans

Look for `./plans/` at the repo root. If plan files already exist there, read them before asking anything else. Then ask the user whether this is:

- **A new task** — move existing plans aside or overwrite them (ask which)
- **A continuation** — extend the existing set with new plans
- **Unrelated** — use a group directory (`./plans/groups/<name>/`) to keep this stream separate

This mirrors Claude Code's `plan_mode_reentry` behavior: you always read the existing plan file before assuming anything.

If `./plans/` does not exist, proceed directly to Phase 1.

### Phase 1: Interview — first round

One or two batched question rounds (use `AskUserQuestion` or the host tool's equivalent — in raw-API contexts, end the turn with the batched questions). Establish:

- **Task goal** in one sentence
- **Concrete acceptance criteria** ("done when X")
- **Known constraints** — libraries to use or avoid, files to leave alone, deadlines, performance budgets
- **Parallelism intent** — does the user want a group directory so this stream runs in parallel with other work? (Default: no, ungrouped.)

Scale depth to the task. A vague ambitious request may need several rounds spread across later phases; a well-scoped one may need just this.

**Never** ask things you could find out by reading code. Never ask one question at a time.

### Phase 2: Lightweight exploration

Read a few key files — just enough to form an initial mental model. Use direct read/search tools (`Read`, `Glob`, `Grep` in Claude Code; equivalents elsewhere).

Launch parallel exploration **only** when scope is genuinely uncertain or multiple unrelated areas are involved. Quality over quantity — usually one pass is right. This mirrors Claude Code's guidance: up to 3 Explore agents, "but usually just 1".

Do **not** explore exhaustively before engaging the user again. Get a shape, then interview.

### Phase 3: Write skeleton plan files

Draft rough `NN-slug.md` plan files **in memory only**. One file per atomic unit of work. Use the **Plan File Template** below. At this point each file is sparse — title, rough context sketch, target files, a handful of notes. Fill-in happens in Phase 4.

How to decide the split:

- **One unit of work per file.** If you can describe a file's change in one coherent paragraph, it's probably one plan. If you find yourself writing "and then separately…" you have two plans.
- **Split on dependencies, not just size.** A plan that must finish before another can start is a separate plan. A plan that can happen concurrently is a separate plan.
- **Don't over-decompose.** A 3-file fix in one concern is one plan, not three. Aim for 2-7 plans per ambitious task. If you have 15, you're splitting too fine.

### Phase 4: Interview — subsequent rounds

Loop until the plans are concrete:

1. **Read more code** to fill specific gaps — exact file paths, line numbers for existing functions to reuse, verification commands that actually exist in the project.
2. **Update skeleton plans in memory** — after each discovery, immediately refine the relevant plan. Don't let findings pile up.
3. **Ask the user** when you hit a decision only they can make (preference, priority, tradeoff). Batch related questions into a single round.

Stop when every plan has:

- A concrete Context paragraph
- A recommended Approach (not alternatives)
- Exact file paths under Critical files
- At least one `file:line` reference under Existing code to reuse (or a justified "nothing reusable found")
- A runnable Verification description

### Phase 5: Present the plan set for review

Show the full set in chat, one fenced block per plan file. Include:

- The ordered list of filenames at the top
- Full body of each plan file inline
- A short rationale: why this decomposition, what the ordering is, and what is explicitly out of scope

Do **not** write any files yet. Use the **Review Handoff Message** below.

### Phase 6: Iterate

Incorporate user feedback into the in-memory drafts. Loop Phase 5 → 6 until the user signs off with "looks good", "ship it", or equivalent.

### Phase 7: Write the files

Write each plan to `./plans/NN-slug.md` (or `./plans/groups/<name>/NN-slug.md` if a group was requested). Report the paths written, one per line. Done.

## Plan File Template

Each emitted plan file follows the Claude Code plan format from `src/utils/messages.ts:3156-3163` (the 5-phase workflow's Phase 4 shape, `PLAN_PHASE4_CONTROL` constant). Prose and bullets. Concise enough to scan, detailed enough to execute. **No** Phase-1/Phase-2 scaffolding, **no** Automated-vs-Manual split, **no** Testing Strategy / Rollback Strategy boilerplate. That is a different framework.

```markdown
# Plan NN — <title>

**Status:** Ready to execute
**Depends on:** <prior plan filenames, or "nothing">
**Followed by:** <next plan filenames, or "nothing">

## Context

<One or two short paragraphs: why this change is being made — the problem
it addresses, what prompted it, the intended outcome. This is the "why",
not the "what".>

## Approach

<The recommended approach only — not alternatives. Prose describing what
will change and roughly how. Concrete enough that a fresh-context agent
understands the shape without guessing, but not so long it becomes a
line-by-line spec. If the approach has 2-4 natural steps, list them as
a short numbered list or bullets.>

## Critical files

- `path/to/file.ext` — <one line on what changes here>
- `path/to/other.ext` — <one line>

## Existing code to reuse

- `functionName()` at `path/to/file.ext:LINE` — <what it does, why relevant>
- `OtherThing` at `path/to/thing.ext:LINE` — <short justification>

## Verification

<How to test the change end-to-end. Be specific and runnable where
possible: exact test commands, exact behaviors to check, how to know
it worked. Not a checklist — a short description a human or a
fresh-context agent can follow.>
```

## Plan File Rules (apply to every file you emit)

- **Only the recommended approach.** Never list alternatives "for consideration". The planning conversation considered them; the plan file commits to one.
- **Concise enough to scan, detailed enough to execute.** If a plan file is longer than ~100 lines, it is probably multiple plans in a trench coat.
- **Every critical file path is exact** — verified by actually reading the file during planning. No guesses.
- **Every "existing code to reuse" reference has a `file:line`.** If you can't give a line, either you didn't read it or it doesn't exist.
- **Verification is actionable.** "Make sure it works" is not verification. Name commands, name observable behaviors. If a check must be manual, say so plainly.
- **No cross-plan references.** Never write "as planned in 01" or "building on plan 02". A plan reader may have executed sibling plans days ago in a completely different context. Restate anything needed.
- **Stand-alone test:** before finalizing each file, read it as if you have never seen this conversation. Does it make sense? If not, add what's missing.

## Guidelines — hard-earned rules from Claude Code's plan mode

- **Never ask what you can find by reading code.** If grep can tell you, grep.
- **Batch questions.** One `AskUserQuestion` call with 2-4 related questions beats four rounds.
- **First turn: engage early.** Scan a few key files, draft skeletons, then ask. Don't explore exhaustively before engaging.
- **End turns with a question or a concrete handoff — never "does this look ok?".** The Review Handoff Message asks for specific feedback kinds, not vague approval.
- **Read-only until Phase 7.** Do not write any file to disk until after the user signs off. The planning session mirrors plan mode's own read-only constraint.
- **One unit of work per plan file.** If a plan has more than ~5 distinct file changes across unrelated concerns, split it.
- **Each plan stands alone.** A fresh-context agent reads only that one file.
- **Filename is the ordering mechanism.** `01-`, `02-`, `03-` — two-digit minimum. `execute-plans` picks the lowest filename first.

## Review Handoff Message (used in Phase 5)

After presenting the full plan set, end your turn with:

```
Here's the proposed decomposition.

Plan count: <N>
Order: <01-foo → 02-bar → 03-baz>
Out of scope: <short list>

Before I write the files, please review:
- Correct — wrong files, misread existing code, bad assumptions
- Split — plans that should be merged or further split
- Order — dependencies I got backwards
- Complete — anything missing

Write "looks good" and I'll create the plan files. Otherwise tell me
what to change.
```

## Cross-tool notes

Use abstract verbs (read, search, ask the user) rather than tool-specific calls. In Claude Code this maps to `Read` / `Glob` / `Grep` / `AskUserQuestion`. In Cursor, Codex, Copilot, or other hosts, use their equivalents. In raw-API contexts, "ask the user" means ending the turn with the question so the calling application can relay it.

Artifact locations (`./plans/`, `./plans/groups/<name>/`) are project-relative and tool-agnostic. Never write to `.claude/` or `.cursor/` or any other tool-specific directory — the output is meant to feed the `execute-plans` ralph or any other consumer that reads from `./plans/`.

## References

- Claude Code plan mode source (the source of truth this skill mirrors):
  - `src/utils/messages.ts:3207` — `getPlanModeV2Instructions` (the 5-phase workflow)
  - `src/utils/messages.ts:3156` — `PLAN_PHASE4_CONTROL` (the exact plan file shape this template emits)
  - `src/utils/messages.ts:3323` — `getPlanModeInterviewInstructions` (the iterative interview loop this workflow mirrors)
  - `src/tools/EnterPlanModeTool/prompt.ts` — when plan mode is appropriate
  - `src/tools/ExitPlanModeTool/prompt.ts` — exit / approval semantics
- `ralphs/execute-plans/RALPH.md` — the executor this skill targets; reads `./plans/*.md` (or `./plans/groups/<group>/*.md`) in lexical filename order
- `ralphify/plans/01-structured-activity-peek.md` — the `**Status:** / **Depends on:** / **Followed by:**` header triple this template borrows for distributed ordering metadata
