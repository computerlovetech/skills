# Snippet Library

Section-level snippets drawn from real ralphify example ralphs. Skim these while drafting — adapt phrasings to fit the current task, don't clone them whole. Each snippet is cited so you can audit the source.

---

## 1. Identity paragraphs

The opening paragraph of the prompt body. Every strong ralph has one. Its job is to orient a fresh-context agent to the loop: **what role it plays, and that it's in a loop with no conversation history**. Optionally — *only if it applies* — where persistent state lives for this specific ralph.

### Minimum form

The irreducible minimum is two sentences — role and loop-awareness:

> You are an autonomous \<role\> agent running in a loop. Each iteration starts with a fresh context.

That's enough for any ralph. Everything else is optional and per-ralph.

### Adding a state-location sentence (only when applicable)

If the ralph actually has persistent state living somewhere specific — and the agent needs to know where to look — add a third sentence that names the location. **Do not add a boilerplate state sentence reflexively**; where state lives is a per-ralph design choice.

Examples of legitimate state-location sentences:

- *"Read TODO.md for the current task list."* — when the loop drives off a file
- *"Your notes live in `workspace/notes/`. Read `workspace/CONVENTIONS.md` for the structure."* — when the loop writes to a workspace directory
- *"Your progress lives in the code and git."* — when the loop's output is commits and file changes (valid for some coding loops, but don't copy-paste it into every ralph — only use it when it's actually true and load-bearing)
- *(nothing)* — when the ralph has no persistent state outside the prompt itself

### Full examples from ralphify examples

Note: some of these use the "progress lives in the code and git" phrasing — that's fine for those specific ralphs because git actually *is* their state. For a ralph whose state lives elsewhere (or nowhere), drop or replace that line.

#### 1a. Generic coding loop (from `examples/python-dev`)

> You are an autonomous coding agent running in a loop. Each iteration starts with a fresh context. Your progress lives in the code and git.

#### 1b. Bug hunter (from `examples/bug-hunter`)

> You are an autonomous bug-hunting agent running in a loop. Each iteration starts with a fresh context. Your progress lives in the code and git.

#### 1c. Research (from `examples/research`)

> You are an autonomous research agent running in a loop. Each iteration starts with a fresh context. Your progress lives in files and git history.

#### 1d. Test coverage (from `examples/test-coverage`)

> You are an autonomous testing agent running in a loop. Each iteration starts with a fresh context. Your progress lives in the code and git.

### Pattern

```
You are an autonomous <role> agent running in a loop. Each iteration
starts with a fresh context.
[Optional: one sentence naming where persistent state lives, ONLY
 if the ralph has state outside the prompt that the agent must read.]
```

- `<role>` — coding, bug-hunting, testing, research, documentation, security, migration, refactoring, etc.
- The state sentence is **optional**. Add it only when there's a concrete location the agent needs to read from or write to. Skip it entirely for loops where the prompt itself is sufficient context.

**Why this matters:** The agent has no conversation history between iterations. Without the identity paragraph it acts like a one-shot — not an iterator. The state sentence, when included, tells it where to look for the work so far — but only if there is such a place.

---

## 2. Feedback-section headers

Every feedback section is a heading + a single `{{ commands.x }}` placeholder. **But first, decide whether you need feedback commands at all.** Commands are not mandatory. A ralph with zero commands and a sharp prompt is valid and often ideal. Only declare commands whose output the agent needs to see to decide what to do next — every command runs every iteration whether the agent reads it or not.

When you do include feedback sections, group them near the top of the body, followed by a brief "fix this first" instruction if the feedback can indicate damage.

### 2a. The common four (from `examples/bug-hunter`, `examples/python-dev`)

```markdown
## Recent commits

{{ commands.git-log }}

## Test results

{{ commands.tests }}

## Type checking

{{ commands.types }}

## Lint

{{ commands.lint }}
```

### 2b. With "fix first" instruction (from `examples/bug-hunter`)

```markdown
If tests, types, or lint are failing, fix that before hunting for new bugs.
```

### 2c. Domain-specific: coverage (from `examples/test-coverage`)

```markdown
## Current coverage

{{ commands.coverage }}
```

### 2d. Domain-specific: remaining files (from `examples/migrate`)

```markdown
## Remaining files

{{ commands.remaining }}
```

Backed by a helper script — see section 8.

### 2e. Domain-specific: editorial review (from `examples/research`)

```markdown
### Editorial review

{{ commands.review }}

Pay close attention to the review above. It's written by an editor
who can see your full body of work. Follow its guidance on where to
focus and what to improve.
```

### 2f. Domain-specific: last diff (from `examples/research`)

```markdown
### What changed last iteration

{{ commands.last-diff }}
```

### Pattern

1. **Consider whether you need commands at all.** Zero is a valid answer. Many effective ralphs have no commands — just a sharp prompt.
2. **Pick the minimum set.** One or two commands is often enough. Only add a command if the agent would actually make a different decision based on its output. If the agent would just skim the output and move on, cut it.
3. **Watch out for reflex-adding the common four.** `tests` / `lint` / `types` / `git-log` is a common shape in ralphify coding-loop examples, but it's not a default template. Drop any you don't need for this specific loop.
4. **Only add domain-specific signals when they inform the next action.** A `coverage` command earns its place in a coverage loop; a `lines-of-code` command does not earn its place anywhere.
5. **End the feedback block with one explicit "fix this first" instruction** if the feedback can indicate damage — this is what makes the loop self-healing. Skip it if there's nothing to "fix first".

---

## 3. Task statements

One-paragraph statements of the loop's goal, often parameterized with `{{ args.focus }}`.

### 3a. Bug hunter (from `examples/bug-hunter`)

```markdown
## Task

Find and fix a real bug in this codebase.
{{ args.focus }}
```

### 3b. Test coverage (from `examples/test-coverage`)

```markdown
## Task

Increase test coverage for this project.
{{ args.target }}

Pick the module with the most missing lines from the coverage report
above. Read the source code, understand what it does, and write
meaningful tests that exercise the uncovered paths.
```

### 3c. Migration (from `examples/migrate`)

```markdown
## Migration spec

Migrate all usages of `{{ args.old_pattern }}` to `{{ args.new_pattern }}`.
```

### 3d. Research (from `examples/research`)

```markdown
## Your mission

{{ args.focus }}

Conduct structured, iterative research on this topic. Go deep.
Discover angles and insights that aren't obvious from the surface.
```

### 3e. TODO-driven (from `examples/python-dev`)

```markdown
Read TODO.md for the current task list. Pick the top uncompleted task,
implement it fully, then mark it done.
```

### Pattern

- One short paragraph stating the goal.
- If you have an args knob, drop it bare on its own line: `{{ args.focus }}`. Empty args resolve to empty string so this is safe.
- If the task depends on reading a specific file, say so explicitly: "Read TODO.md…", "Read the coverage report above…".

---

## 4. Process blocks

Numbered step-by-step instructions for a single iteration. 3-5 steps, concrete actions.

### 4a. Bug hunter (from `examples/bug-hunter`)

```markdown
Each iteration:

1. **Read code** — pick a module and read it carefully. Look for
   edge cases, off-by-one errors, missing validation, incorrect
   error handling, race conditions, or logic errors.
2. **Write a failing test** — prove the bug exists with a test that
   fails on the current code.
3. **Fix the bug** — make the test pass with a minimal fix.
4. **Verify** — all existing tests must still pass.
```

### 4b. Research (from `examples/research`)

```markdown
## Each iteration

1. **Orient** — read the state above. Read the editorial review.
   Understand where you left off.
2. **Decide: research or refine?** Roughly every 3-4 iterations,
   skip research and instead tighten prose, merge overlapping
   sections, and sharpen insights. Less but better content wins.
3. **Research** — pick ONE question or area. Go deep.
4. **Capture** — update notes files with questions, insights, sources.
5. **Write** — findings go into the appropriate chapter.
6. **Commit and push** — stage all changes, commit, push.
```

### Pattern

- **Numbered list**, not bullets — order matters.
- **Start each step with a verb** (Read, Write, Fix, Verify, Commit, Orient, Pick, Record, Append).
- **Bold the verb** for scanability: `1. **Read code** — …`.
- **End with a progress-recording step.** Whatever mechanism the ralph uses to persist progress — git commit, log append, state-file update, TODO tick — the last step must explicitly tell the agent to do it. Ralphify persists nothing on its own; if the prompt is silent, the trail goes missing. For a git ralph this is "commit (and push)"; for other ralphs it's the equivalent.
- **Keep it concrete.** "Pick the module with the most missing lines" is better than "work on the area that needs attention".

---

## 5. Rules menu

Rules are the most important part of a ralph. Each one should encode a specific failure mode. Pick from these categories when drafting — every ralph should have at least one rule from each of the first four categories.

### 5a. Per-iteration boundaries (required)

> - One task per iteration  *(from python-dev)*
> - One bug per iteration  *(from bug-hunter)*
> - One module per iteration  *(from test-coverage)*
> - Migrate 1-3 files per iteration — small batches that stay green  *(from migrate)*
> - ONE focused thread per iteration. Depth over breadth.  *(from research)*

### 5b. Reality constraints (prevent hallucination / laziness)

> - The bug must be real — do not invent hypothetical issues  *(from bug-hunter)*
> - No placeholder code — full, working implementations only  *(from python-dev)*
> - Write tests that verify behavior, not just hit lines — assert return values, side effects, and error cases  *(from test-coverage)*
> - Do not fabricate sources. When you find contradictions, note both sides.  *(from research)*

### 5c. Quality gates

> - All existing tests must still pass after your changes  *(from test-coverage)*
> - Always write a regression test before fixing  *(from bug-hunter)*
> - Run tests after each change to catch breakage early  *(from migrate)*
> - Run tests before committing  *(from python-dev)*

### 5d. Scope limits

> - Do not change unrelated code  *(from bug-hunter)*
> - Do not change behavior — only update the pattern  *(from migrate)*
> - Do not mock things unnecessarily — prefer real objects when feasible  *(from test-coverage)*
> - If a file needs more than a mechanical replacement, note it in MIGRATION_NOTES.md and skip it  *(from migrate)*

### 5e. Anti-cheating (prevent silencing the feedback loop)

> - Do not add `# pragma: no cover` comments  *(from test-coverage)*
> - Do not add `# type: ignore` or `# noqa` comments  *(from python-dev)*
> - Do not delete failing tests — fix the underlying code instead

### 5f. Progress-recording conventions (required)

Every ralph needs a rule prescribing the format of its per-iteration progress record, whatever mechanism it uses. Git commit messages are the most common instance; appended log lines, state-file rows, TODO updates, and the like are equally valid — pick what fits the ralph and mandate a consistent format.

Git commit-message examples (from the ralphify examples, which are all commit-based):

> - Commit with `fix: resolve <description>`  *(from bug-hunter)*
> - Commit with `test: add coverage for <module>`  *(from test-coverage)*
> - Commit with `refactor: migrate <file> from old_pattern to new_pattern`  *(from migrate)*
> - Commit with a descriptive message like `feat: add X` or `fix: resolve Y`  *(from python-dev)*

For non-git ralphs, write the equivalent rule in the ralph's own vocabulary (an append format, a schema, a checklist-update convention). Do not reach for a git example when git isn't the mechanism.

### 5g. Progress-tracking rules (when loop drives off a file)

> - Mark the completed task in TODO.md  *(from python-dev)*
> - The research question tree (`notes/questions.md`) must grow every research iteration  *(from research)*
> - Every web source gets logged in `notes/sources.md` with URL, author, one-line summary, and relevance rating  *(from research)*

### Pattern

- Every ralph needs rules from 5a (per-iteration boundary) and 5f (progress-recording convention) — these two are non-negotiable.
- Add rules from 5b-5e based on the task's failure modes.
- Concrete > generic. "Don't add `# pragma: no cover`" is worth 100 "write good tests" rules.
- Prefer bullets over paragraphs. Keep each rule to one line if possible.

---

## 6. Args usage

Args are the loop's runtime knobs. Declared in frontmatter, referenced with `{{ args.<name> }}` in the body or in command `run` strings.

### 6a. Single focus knob (from `examples/bug-hunter`)

```yaml
args:
  - focus
```

```markdown
## Task

Find and fix a real bug in this codebase.
{{ args.focus }}
```

```bash
ralph run bug-hunter --focus "the auth module"
```

### 6b. Two positional args (from `examples/migrate`)

```yaml
args:
  - old_pattern
  - new_pattern
```

```markdown
Migrate all usages of `{{ args.old_pattern }}` to `{{ args.new_pattern }}`.
```

```bash
ralph run migrate "requests.get" "httpx.get"
# or: ralph run migrate --old_pattern "requests.get" --new_pattern "httpx.get"
```

### 6c. Args inside command run strings (from `examples/migrate`)

```yaml
commands:
  - name: remaining
    run: ./count-remaining.sh {{ args.old_pattern }}
```

Args work inside `run:` strings too — the script gets the resolved value as an argument.

### 6d. Args for workspace location (from `examples/research`)

```yaml
args:
  - workspace
  - focus
```

```markdown
You work within `{{ args.workspace }}/`. Read
`{{ args.workspace }}/CONVENTIONS.md` for the full workspace structure.
```

### Pattern

- **Expose an args knob whenever the loop could be reused across projects or focus areas.** Even a single `args.focus` adds huge steering power for zero cost.
- **Empty args resolve to empty string** — safe to put `{{ args.focus }}` bare on its own line; if not provided, it just disappears.
- **Args names follow the same regex as command names**: `[a-zA-Z0-9_-]+`. Use snake_case or kebab-case consistently.

---

## 7. Timeout overrides

Default command timeout is 60 seconds. Timed-out output is truncated and the agent sees a "[Command timed out]" notice. Override for slow commands.

### 7a. Slow review command (from `examples/research`)

```yaml
commands:
  - name: review
    run: ./review.sh
    timeout: 120
```

### 7b. Slow test suite (conventional)

```yaml
commands:
  - name: tests
    run: uv run pytest
    timeout: 300  # 5 minutes
```

### Pattern

- Set `timeout:` to a positive integer (seconds).
- Estimate 2-3× the command's typical runtime to leave headroom.
- If you're not sure, **run the command manually once** and time it before setting the override.
- Don't over-engineer — only override when a command actually exceeds 60s.

---

## 8. Helper script pattern

When a command needs shell features (pipes, redirects, `&&`, `$VAR`), ralphify's `shlex`-based parser cannot handle it. Bundle the logic in a helper script next to `RALPH.md` and reference it with the `./` prefix — the `./` makes it execute from the ralph directory (not the project root).

### 8a. Counting remaining files (from `examples/migrate/count-remaining.sh`)

```yaml
commands:
  - name: remaining
    run: ./count-remaining.sh {{ args.old_pattern }}
```

```bash
#!/bin/bash
# my-ralph/count-remaining.sh
pattern="$1"
files=$(grep -rl "$pattern" src/ 2>/dev/null)
count=$(echo "$files" | grep -c . 2>/dev/null || echo 0)
echo "$count files remaining"
echo "$files" | head -20
```

### 8b. Filtered test output (for truncating long pytest output)

```yaml
commands:
  - name: tests
    run: ./filter-tests.sh
```

```bash
#!/usr/bin/env bash
# my-ralph/filter-tests.sh
set -euo pipefail
uv run pytest --tb=line -q 2>&1 | tail -50
```

### 8c. Multi-step "show state" helper (inspired by `examples/research`)

Research uses helpers like `./show-focus.sh`, `./show-questions.sh`, `./show-outline.sh`. Each is a small script that prints one slice of the workspace state.

```bash
#!/usr/bin/env bash
# my-ralph/show-focus.sh
tail -30 "$WORKSPACE/notes/scratchpad.md" 2>/dev/null || echo "(no scratchpad yet)"
```

### Pattern

1. **When to bundle a script:** any command that needs `|`, `>`, `2>&1`, `&&`, `||`, `$VAR`, subshells, or multi-step logic.
2. **Where to put it:** as a sibling of `RALPH.md`, inside the ralph directory.
3. **How to reference it:** `run: ./script.sh` — the `./` prefix makes ralphify execute it from the ralph directory.
4. **Make it executable:** `chmod +x` when you write it. Without the execute bit, ralphify's binary-exists check fails at startup.
5. **Use `set -euo pipefail`** in bash scripts — fail fast if a subcommand errors.
6. **Args pass through:** `run: ./script.sh {{ args.pattern }}` resolves the placeholder first, then passes the resolved value as `$1` to the script.

---

## 9. Whole-file shape reference

A compact reference for the 5-section shape, drawn from `examples/bug-hunter/RALPH.md`. **This is a structural reference, not a starting template.** The bug-hunter ralph happens to use four commands because a bug-hunting loop genuinely benefits from seeing test/type/lint state and recent commits. Your ralph will probably use fewer. Look at the *shape* (identity → feedback → fix-first → task → process → rules), not the *count*.

```markdown
---
agent: claude -p --dangerously-skip-permissions
commands:
  - name: tests
    run: uv run pytest -x
  - name: types
    run: uv run ty check
  - name: lint
    run: uv run ruff check .
  - name: git-log
    run: git log --oneline -10
args:
  - focus
---

# Bug Hunter

You are an autonomous bug-hunting agent running in a loop. Each
iteration starts with a fresh context. Your progress lives in the
code and git.

## Test results

{{ commands.tests }}

## Type checking

{{ commands.types }}

## Lint

{{ commands.lint }}

## Recent commits

{{ commands.git-log }}

If tests, types, or lint are failing, fix that before hunting for new bugs.

## Task

Find and fix a real bug in this codebase.
{{ args.focus }}

Each iteration:

1. **Read code** — pick a module and read it carefully.
2. **Write a failing test** — prove the bug exists.
3. **Fix the bug** — make the test pass with a minimal fix.
4. **Verify** — all existing tests must still pass.

## Rules

- One bug per iteration
- The bug must be real — do not invent hypothetical issues
- Always write a regression test before fixing
- Do not change unrelated code
- Commit with `fix: resolve <description>`
```

That's a complete, production-ready ralph in ~40 lines of body. Use it as a structural reference — not a template to clone. Your ralph will likely differ in at least three ways:

1. **Probably fewer commands.** Bug-hunter has four because each one actually influences what it does next. Most ralphs need fewer. Some need zero.
2. **The state sentence may differ or disappear.** Bug-hunter's "Your progress lives in the code and git" is accurate *for bug-hunter* because git commits are its output. For a ralph that writes notes to a workspace, say so. For a ralph with no persistent state, drop the sentence entirely.
3. **The progress-recording rule may not be a commit rule.** Bug-hunter ends with `Commit with 'fix: resolve <description>'` because it's a git-committing ralph. A ralph that records progress differently needs a rule phrased for its own mechanism — not a commit rule bolted on. The *shape* "end with a progress-recording rule" is universal; the *content* is per-ralph.

Adapt the identity, feedback, task, process, and rules to the user's actual goal.
