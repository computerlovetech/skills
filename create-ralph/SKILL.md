---
name: create-ralph
description: >
  Author a new ralph — a directory containing a RALPH.md file that defines an
  autonomous agent loop for the ralphify runtime. Use when the user wants to
  create, draft, design, or scaffold a ralph for a repeatable autonomous task
  (test coverage, bug hunting, migrations, research, TODO execution, docs
  improvement, etc.). Asks a thorough set of questions up front, explores the
  target project for real test/lint/type commands, drafts RALPH.md from scratch
  using the canonical 5-section body shape, bundles helper scripts when commands
  need shell features, presents the draft for review, and writes the files only
  after sign-off.
---

# Create Ralph

Draft a high-quality `RALPH.md` for the [ralphify](https://github.com/computerlovetech/ralphify) runtime. A ralph is a directory containing a `RALPH.md` (YAML frontmatter + markdown prompt body) that defines an autonomous agent loop. Each iteration the runtime runs the frontmatter commands, fills the prompt template with their output, pipes the assembled prompt to the agent, and repeats.

## Initial Setup

Respond with:

```
I'll help you create a ralph. Before I draft anything, I need to understand the loop you want to build. I'll ask a few questions, then explore your project to find the real test/lint/type commands to wire in.
```

Then immediately begin **Phase 1: Thorough Q&A**. Do not wait for the user to prompt you further.

## Workflow

### Phase 1: Thorough Q&A

Ask the user the questions in the **Q&A Checklist** section below. Batch related questions into 2-3 `AskUserQuestion` rounds rather than asking one at a time. Do not start drafting until every non-optional slot has an answer (the user is free to say "default" or "skip" — treat that as an answer).

### Phase 2: Explore the project

Only explore enough to find the commands the loop actually needs (per the Q&A answers). If the ralph will record progress via git commits, also check the project's commit-message convention. Don't gather every possible command "just in case" — unused commands clutter the ralph.

Useful places to look, if relevant:

- `pyproject.toml`, `uv.lock`, `requirements*.txt` (Python)
- `package.json`, `pnpm-lock.yaml`, `yarn.lock` (JS/TS)
- `Cargo.toml` (Rust)
- `go.mod`, `Makefile`
- `justfile`, `Taskfile.yml`
- `.github/workflows/*.yml` (what CI runs is often the best source of truth)
- `CLAUDE.md`, `AGENTS.md`, `README.md` (documented commands)

Extract **only** the commands the user's Q&A answers said the loop needs (often 0-2 of: test, lint, type-check, build, format, coverage). If the ralph will commit to git, check `git log --oneline -20` for the project's commit-message convention. If the user named a file or directory the loop drives off (`TODO.md`, `PLAN.md`, a workspace dir, a state file), verify it exists or note it will need to be created.

Reconcile discovered commands against the Q&A answers — prefer commands that actually exist in the project over generic defaults.

### Phase 3: Draft from scratch

Compose a new `RALPH.md` using the **Canonical 5-Section Template** below. Do **not** clone an archetype — draft each section fresh, using `references/snippets.md` as a source of phrasings you can adapt. Apply every relevant principle from **Drafting Principles** as you write.

### Phase 4: Draft helper scripts (if needed)

If any `run:` string requires shell features (pipes `|`, redirects `>` `2>&1`, chaining `&&` `||`, variable expansion `$VAR`, subshells), the command will **silently fail** in ralphify — it parses `run:` with `shlex` and executes directly, not through a shell.

For every such case, write a helper script as a sibling of `RALPH.md` and reference it with the `./` prefix so it executes from the ralph directory:

```yaml
commands:
  - name: filtered-tests
    run: ./filter-tests.sh
```

```bash
#!/usr/bin/env bash
# my-ralph/filter-tests.sh
set -euo pipefail
uv run pytest --tb=line -q 2>&1 | tail -50
```

Mark scripts as executable when you write them (`chmod +x`).

### Phase 5: Present the draft

Show the full draft in chat — the `RALPH.md`, any helper scripts, and a short rationale explaining which commands you chose and why, which rules you baked in, and which args you exposed. **Do not write any files yet.** Use the **Review Handoff Message** below.

### Phase 6: Iterate

Incorporate the user's feedback into the draft. Loop Phase 5 → Phase 6 until the user signs off with "looks good", "ship it", or equivalent.

### Phase 7: Pre-flight validation

Silently run the draft through `references/anti-patterns.md`. Fix any violations. Do not mention the checklist to the user unless a violation requires a substantive change that warrants another review round.

### Phase 8: Write the files

Write `RALPH.md` and any helper scripts to the target directory. Make helper scripts executable. Report the paths written.

## Q&A Checklist

Every slot below must have an answer before drafting. Batch into 2-3 `AskUserQuestion` rounds — group related questions (e.g., task + directory + agent in round 1, rules + args + progress-recording convention in round 2, slow/complex commands in round 3).

| # | Slot | Question | Default if skipped |
|---|---|---|---|
| 1 | **Task** | What autonomous work should this loop do? Describe the goal in a sentence. | — (required) |
| 2 | **Ralph name** | What should the ralph directory be called? (kebab-case, e.g. `test-coverage`, `bug-hunter`) | Derive from task |
| 3 | **Target directory** | Where should the ralph live? | `<project-root>/<ralph-name>/` |
| 4 | **Agent command** | Which agent CLI? | `claude -p --dangerously-skip-permissions` |
| 5 | **Per-iteration boundary** | What is "one unit of work" per iteration? (one module, one bug, one file, one test, …) | Ask — do not guess; this becomes the most important rule |
| 6 | **State location** | Does the loop have persistent state outside the prompt, and if so where does it live? — informs the identity paragraph. Do not prescribe a mechanism; let the user describe whatever fits their task. | None — skip the state sentence in the identity paragraph |
| 7 | **Feedback needed** | What (if anything) does the agent need to **see** each iteration to decide its next action? (test output, lint output, a count of remaining items, a review, a diff, nothing at all) Be minimal — only list signals the agent can actually act on. Each answer becomes one command. | Zero commands — start minimal |
| 8 | **Focus knob** | Should the loop expose an `args.focus` (or similar) so the user can steer it at runtime without editing the file? If yes, which args? | No args |
| 9 | **Anti-patterns** | Anything the agent must NOT do? ("don't delete failing tests", "don't add `# pragma: no cover`", "don't touch the migrations directory", etc.) | None — but prompt with examples |
| 10 | **Progress-recording convention** | How should the agent record each iteration's progress, and in what format? Ralphify records nothing automatically — the prompt has to tell the agent. If the loop uses git, ask for the commit-message format. Otherwise ask for whatever the equivalent is (an append format for a log file, a schema for a state record, a checklist update convention, etc.). | Ask — do not guess; depends on how the ralph persists progress |
| 11 | **Credit trailer** | Keep the default `Co-authored-by: Ralphify <noreply@ralphify.co>` trailer, or set `credit: false`? | `credit: true` (default, omit the field) |
| 12 | **Slow commands** | Any command expected to exceed 60s that needs a `timeout:` override? (only relevant if you declared commands) | None |
| 13 | **Complex commands** | Any command needing pipes/redirects/chaining? (triggers helper-script bundling in Phase 4) | None |

## Format Cheatsheet

Use this for reference while drafting. Never invoke `ralph` or check the ralphify source from inside the skill — the cheatsheet below is the contract.

### Frontmatter fields

| Field | Type | Required | Notes |
|---|---|---|---|
| `agent` | string | **yes** | Full agent CLI command. Piped via stdin. Binary must exist on PATH. |
| `commands` | list of `{name, run, timeout?}` | no | Each `name` unique. `run` parsed with `shlex` — **no shell features**. `timeout` in seconds, default 60, must be positive. |
| `args` | list of strings | no | Positional user-argument names. Each unique. |
| `credit` | bool | no | Default `true`. Appends a co-author trailer instruction to the prompt. |

### Name regex

`[a-zA-Z0-9_-]+` — letters, digits, hyphens, underscores only. Command names, arg names. **Prefer kebab-case** (`git-log`, `remaining-files`) to match the ralphify examples.

### Placeholder syntax

- `{{ commands.<name> }}` — replaced with the command's stdout + stderr (regardless of exit code). Must be `commands` (plural). Unreferenced commands still run every iteration but their output is excluded.
- `{{ args.<name> }}` — replaced with the CLI value for `--<name>`. Missing → empty string.
- `{{ ralph.name }}`, `{{ ralph.iteration }}`, `{{ ralph.max_iterations }}` — auto-populated metadata.
- HTML comments `<!-- … -->` are stripped from the prompt body before it reaches the agent — safe to use as author notes.

### Command execution rules

- Commands starting with `./` run from the **ralph directory** — use for bundled helper scripts.
- Bare commands run from the **project root** (the directory `ralph run` was invoked from).
- `run` is parsed with `shlex` — **no pipes, redirects, chaining, or variable expansion**. Bundle in a `./script.sh` instead.
- Command output is captured regardless of exit code. A failing test command is often exactly what you want.
- Default timeout: **60 seconds**. Truncated output is annotated.

### Live-reload semantics

- **Prompt body** is re-read from disk every iteration — the user can edit it mid-loop to steer behavior.
- **Frontmatter** (agent, commands, args, credit) is parsed once at startup — changing it requires restarting the loop.

## Drafting Principles

Apply these when composing each section of the body. They are the good-practice principles distilled from the ralphify example ralphs and the runtime's validation rules.

1. **Open with an identity paragraph.** Every good ralph begins with something like: *"You are an autonomous \<role\> agent running in a loop. Each iteration starts with a fresh context."* This orients a fresh-context agent to the loop's nature — there is no conversation history, only what the prompt tells it. **If (and only if) the ralph has state living somewhere specific outside the prompt** — a workspace directory, a TODO.md file, a particular set of notes files — tell the agent where to look. State location is a **per-ralph design decision**, not a universal truth. Do not reflexively add a boilerplate "your progress lives in the code and git" line; many ralphs keep state elsewhere, and some keep no persistent state at all.
2. **Don't overuse commands.** Commands are powerful but every command runs every iteration whether its output is useful or not. A minimal ralph with zero commands and a clear prompt is often better than one padded with four commands the agent skims past. **Only add a command if the agent needs its output to decide what to do next.** Start with the smallest set that actually informs behavior — usually one or two signals, sometimes zero. Add more incrementally only when you discover a specific gap the current feedback doesn't fill.
3. **Lead with feedback, then state the task.** *When* you do include commands, paste their output near the top of the body via `{{ commands.x }}` placeholders, immediately followed by an instruction like "Fix any failing tests above before starting new work." Self-healing loops happen because the agent sees its last iteration's damage — but only surface signals the agent can act on.
4. **Only reference commands you surface.** An unreferenced command still runs every iteration — wasted time with no benefit. Either put it in a `{{ commands.x }}` placeholder or delete it.
5. **Bound per-iteration scope with an explicit rule.** Every strong ralph has a "One X per iteration" rule. Without it, the agent over-reaches and produces sprawling, hard-to-review iterations.
6. **Rules encode specific anti-patterns.** "Do not delete failing tests." "Do not add `# pragma: no cover`." "Do not invent hypothetical bugs." Each rule should prevent a failure mode you can actually picture. Generic rules ("write good code") are dead weight.
7. **Prescribe a consistent format for the ralph's progress record.** Whatever the loop produces each iteration — a commit, an appended log line, a row in a state file, a checked item in a TODO list — it needs a consistent format so the trail is legible. For git-committing ralphs that means a commit-message convention (`fix: …`, `test: add coverage for <module>`). For other ralphs it means whatever convention fits the mechanism. Pick one and enforce it.
8. **Always tell the agent to record progress.** Ralphify does **not** persist anything on the agent's behalf — no commits, no file writes, no state updates. Whatever mechanism the ralph uses to record per-iteration progress, the prompt must explicitly tell the agent to do it every iteration. If the prompt is silent, the agent may skip it and the loop produces no visible trail. For a git-committing ralph this is the "commit your work" step; for other ralphs it's the equivalent in that mechanism.
9. **Write the process as numbered steps.** A strong ralph has an explicit 3-5 step `## Process` section: 1. read, 2. hypothesize, 3. change, 4. verify, 5. record progress. Numbered steps constrain behavior.
10. **Parameterize with `args` for reusability.** Expose an `args.focus` (or `args.target`, `args.dir`) as an optional steering knob. Embed it in the task paragraph: *"Increase test coverage. {{ args.focus }}"*. Users can bias the loop with `ralph run my-ralph --focus "the api module"` without editing the file.
11. **Name commands in kebab-case.** Match the ralphify examples: `git-log`, `remaining-files`, `count-remaining`. Use underscores only if the user explicitly prefers them.
12. **Set `timeout:` on slow commands.** Anything expected to exceed 60s (large test suites, slow builds) needs an explicit `timeout: 300` or similar. Truncated output confuses the agent.
13. **Leave `credit` at the default unless the user asks otherwise.** The `Co-authored-by: Ralphify` trailer is on by default — omit the `credit` field entirely unless the user specifically wants it off.
14. **HTML comments for author notes.** `<!-- TODO: revisit this rule once tests are passing -->` is stripped from the agent's view — use it for your own scratchpad.
15. **Minimum viable ralph is still useful.** A ralph with just `agent:` + a good prompt is a valid ralph. Don't over-engineer a loop that only needs two commands.

## Canonical 5-Section Template

The body of every drafted `RALPH.md` follows this shape. Adapt the wording per task, but keep the section order and purpose.

The template below shows the **shape**, not a minimum command set. Most ralphs need fewer commands than this — some need zero. Only wire in commands the agent actually needs to see.

```markdown
---
agent: claude -p --dangerously-skip-permissions
# commands: are OPTIONAL. Add only the ones whose output the agent
# needs to see to decide what to do next. Start minimal — often 0-2.
# Example (remove or shrink based on the actual loop):
# commands:
#   - name: tests
#     run: <discovered test command, e.g. uv run pytest -x>
args:
  - focus
---

# <Task Title>

You are an autonomous <role> agent running in a loop. Each iteration
starts with a fresh context.
<!-- If the ralph has state in a specific location, add a sentence here
naming it: e.g. "Your notes live in workspace/notes/." or "Read TODO.md
for the current task list." Skip this line entirely if there is no
persistent state outside the prompt itself. -->

<!-- Feedback sections — one per command you declared, in the order
the agent should read them. Omit this entire block if you have no
commands. -->

## <Feedback header>

{{ commands.<name> }}

<One-line "fix this first" instruction if the feedback can indicate damage.>

## Task

<One-paragraph goal that states what the loop should accomplish>.
{{ args.focus }}

## Process

Each iteration:

1. <read / orient>
2. <make one small change>
3. <verify>
4. <record progress using the ralph's chosen mechanism and format>

## Rules

- <per-iteration boundary, e.g. "One module per iteration">
- <anti-pattern prevention, e.g. "Do not delete failing tests">
- <quality gate, e.g. "All existing tests must still pass">
- <scope limit, e.g. "Do not change unrelated code">
- <progress-recording convention — whatever the ralph uses; for a git-committing ralph this is the commit-message format>
```

### Section purposes

1. **Identity paragraph** *(required)* — tells a fresh-context agent what loop it's in. Optionally names the location of persistent state if one exists.
2. **Feedback sections** *(optional, one per command)* — heading + `{{ commands.x }}` placeholder. Skip entirely if the ralph has no commands.
3. **Task paragraph** *(required)* — the explicit goal, parameterized with `{{ args.focus }}` if an args knob was exposed.
4. **Process steps** *(required)* — a numbered list the agent follows for a single iteration. Concrete actions, not strategy.
5. **Rules** *(required)* — bulleted, concrete constraints. Include at least: the per-iteration boundary and the progress-recording convention (commit-message format, log-append format, state-file schema, or whatever the ralph uses).

## Review Handoff Message

After drafting, present the full file(s) and use this message to hand off for review:

```
Here's the draft.

Commands chosen: <short justification — "real pyproject.toml commands, plus git-log for context">
Rules baked in: <count> (<short summary, e.g. "one module/iteration, no pragma, record progress as `test:` commits">)
Args exposed: <list or "none">
Helper scripts: <list or "none">

Before I write it, please review:

- Correct — wrong commands, misidentified patterns, or assumptions I got wrong
- Add — rules I missed, anti-patterns specific to your project, args I should expose
- Align — does this match how you want the loop to actually behave?

Say "looks good" and I'll write the files. Otherwise tell me what to change.
```

Wait for the user's response. Iterate on the draft until they sign off, then proceed to pre-flight validation (Phase 7) and write the files (Phase 8).

## References

- `references/snippets.md` — section-level snippet library. Load while drafting to find phrasings for identity paragraphs, feedback headers, task statements, process blocks, rules, and helper scripts.
- `references/anti-patterns.md` — pre-flight validation checklist. Run through this in Phase 7 before writing any files.
