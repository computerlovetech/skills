# Pre-flight Validation Checklist

Run the draft through this checklist in Phase 7 before writing any files. Every item traces to a real ralphify validation error, a documented anti-pattern, or a pattern observed across the best ralphify example ralphs.

Walk the checklist top to bottom. If you find a violation, fix it silently unless the fix requires a substantive change the user would want to see — in that case, loop back to Phase 5 (present the draft) and surface the change.

---

## 1. Frontmatter validity

These are validated by ralphify at startup. A single violation causes `ralph run` to exit with status 1 before any iteration starts.

- [ ] `agent` field is present and non-empty (e.g., `claude -p --dangerously-skip-permissions`)
- [ ] `agent` value has no unclosed quotes (`shlex`-parsed; unclosed quotes raise "Malformed 'agent' field")
- [ ] `commands` (if present) is a **list**, not a scalar or mapping
- [ ] Every command has both `name` and `run`, and both are non-empty strings
- [ ] Every command `timeout` (if set) is a positive number
- [ ] `args` (if present) is a **list of strings** (not a bare string, not integers, not booleans)
- [ ] `credit` (if present) is a bare YAML boolean (`true` / `false`, not `"yes"`, not `1`)

## 2. Name regex

- [ ] Every command `name` matches `[a-zA-Z0-9_-]+` (no dots, spaces, or other punctuation)
- [ ] Every arg name matches `[a-zA-Z0-9_-]+`
- [ ] No duplicate command names
- [ ] No duplicate arg names
- [ ] Names use kebab-case where sensible (`git-log`, `remaining-files`) to match ralphify example conventions

## 3. Placeholder resolution

Unmatched placeholders silently resolve to empty string — they fail quietly. Catch them here.

- [ ] Every `{{ commands.<name> }}` in the body references a command actually declared in frontmatter
- [ ] Every `{{ args.<name> }}` in the body references an arg actually declared in frontmatter (unless you intentionally want it optional — then this is OK, but confirm)
- [ ] Every `{{ args.<name> }}` used inside a command `run:` string references a declared arg
- [ ] Placeholder keyword is **`commands`** (plural), not `command`
- [ ] Placeholder keyword is **`args`** (plural), not `arg`
- [ ] `{{ ralph.<name> }}` uses only `name`, `iteration`, or `max_iterations` — no other metadata keys exist

## 4. Shell-feature escape hatch

Commands are parsed with `shlex` and executed **directly** — not through a shell. Shell features silently fail or produce unexpected output.

- [ ] No `|` (pipe) in any `run:` string
- [ ] No `>`, `>>`, `2>&1` (redirect) in any `run:` string
- [ ] No `&&`, `||`, `;` (chaining) in any `run:` string
- [ ] No `$VAR`, `${VAR}`, `$(…)`, or backticks in any `run:` string
- [ ] Any command that needs these features is bundled as a `./helper.sh` sibling of `RALPH.md`, referenced via `run: ./helper.sh`
- [ ] All bundled helper scripts have the execute bit set (write with `chmod +x` or equivalent)

## 5. Command hygiene

- [ ] **Every command earns its place.** Its output must actually influence the agent's next action. If the agent would read it and move on without changing behavior, cut it. Zero commands is a valid answer.
- [ ] Every command in `commands:` is referenced by a `{{ commands.x }}` placeholder in the body (unreferenced commands still run every iteration — pure waste)
- [ ] No "just in case" commands — don't reflexively add the common four (`tests`/`lint`/`types`/`git-log`); include only the ones this specific loop needs
- [ ] Any command expected to exceed 60 seconds has an explicit `timeout:` override (2-3× typical runtime)
- [ ] Commands without a `./` prefix are expected to be found on PATH from the project root — verify the binaries exist (e.g., `uv`, `pytest`, `ruff`, `ty`)
- [ ] No hardcoded secrets, API keys, tokens, or credentials in any `run:` string

## 6. Body structure

- [ ] **Identity paragraph** present near the top. Minimum form: "You are an autonomous \<role\> agent running in a loop. Each iteration starts with a fresh context."
- [ ] **State-location sentence** — if (and only if) the loop has persistent state outside the prompt, the identity paragraph names where it lives (a workspace dir, a TODO.md file, "the code and git" for coding loops that commit, etc.). **Do not include a boilerplate state sentence if no such state exists.** State location is a per-ralph design choice.
- [ ] **Feedback sections** *(only if commands were declared)* — each declared command has its own `## <Header>` followed by the `{{ commands.x }}` placeholder. If the ralph has no commands, there are no feedback sections — that is valid.
- [ ] **"Fix this first" instruction** *(only if feedback commands can indicate damage)* — if a command like `tests` or `lint` is declared, the body includes an instruction telling the agent to fix failing tests/lint before starting new work. Skip if the feedback is informational-only.
- [ ] **Task section** present (`## Task`, `## Your mission`, `## Migration spec`, or equivalent) with an explicit one-paragraph goal
- [ ] **Process section** present with numbered steps (3-5 steps, concrete actions)
- [ ] **Rules section** present with bulleted constraints

## 7. Rules content

- [ ] At least one rule bounds per-iteration scope (e.g., "One module per iteration", "Migrate 1-3 files per iteration")
- [ ] At least one rule prescribes the ralph's progress-recording convention — the format of whatever record each iteration produces. For a git ralph this is the commit-message format (e.g., "Commit with `fix: resolve <description>`"). For a ralph recording progress differently (log append, state-file update, TODO tick, etc.), the rule must be phrased for that mechanism instead.
- [ ] Rules are concrete, not generic — each one should prevent a specific failure mode
- [ ] No vague rules like "write good code" or "follow best practices"
- [ ] If the task touches tests/types/lint, there's an anti-cheating rule (e.g., "Do not delete failing tests", "Do not add `# pragma: no cover`")

## 8. Progress-recording instruction

Ralphify persists **nothing** on the agent's behalf — no commits, no file writes, no state updates. Whatever mechanism the ralph uses to record per-iteration progress, the prompt must explicitly tell the agent to do it every iteration. If the prompt is silent, the loop can run forever without producing a visible trail. (For git-committing ralphs this is the familiar "always tell the agent to commit" rule; it's the same requirement generalized.)

- [ ] The process block ends with (or otherwise includes) an explicit step that records the iteration's progress via the ralph's chosen mechanism (commit, log append, state-file update, TODO tick, etc.)
- [ ] The rules section prescribes a format/convention for those records

## 9. Args hygiene

- [ ] If an `args.focus` (or similar steering knob) is exposed, it appears in the task paragraph where users would expect it to steer behavior
- [ ] If args are declared but never referenced in the body or in command `run:` strings, either reference them or remove them
- [ ] If args are declared for positional use, they appear in the order the user will pass them

## 10. Secrets and safety

- [ ] No secrets in `run:` strings (API keys, tokens, passwords, database URLs with credentials)
- [ ] No secrets in the prompt body
- [ ] No secrets in helper scripts — if the script needs credentials, read them from environment variables inside the script, not from the `run:` field

## 11. File write targets

- [ ] Target directory path is valid and doesn't collide with an existing file (ralph directory must be a directory, not a file)
- [ ] `RALPH.md` filename is exactly `RALPH.md` (case-sensitive) — `ralph.md`, `Ralph.md`, or `readme.md` will not be detected
- [ ] Any bundled helper scripts are placed inside the same directory as `RALPH.md`

---

## When a violation requires user review

Fix these silently:
- Name regex violations (rename to kebab-case)
- Missing `./` prefix on bundled scripts
- Missing execute bit on helper scripts
- Placeholder typos (`command.x` → `commands.x`)
- Missing progress-recording step in process block (append one using the ralph's already-declared mechanism)

Loop back to Phase 5 (present the draft) for these:
- Adding or removing a command
- Adding or removing a rule
- Changing the task statement
- Changing which args are exposed
- Any change that alters the loop's behavior

The rule of thumb: **mechanical fixes happen silently, semantic changes require re-review**.
