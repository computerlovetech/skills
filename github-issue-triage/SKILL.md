---
name: github-issue-triage
description: >
  Triage all open issues in a GitHub repository: fetch them via the gh CLI,
  classify each by type, priority, and quality, flag likely duplicates and
  stale/low-quality reports, suggest labels, and produce a prioritized triage
  report. Read-only by default — recommends writes (labels, comments, closes)
  but never applies them without explicit human approval, one batch at a time.
  Use this skill when the user wants to triage their GitHub issues, clean up
  their backlog, label untriaged issues, find duplicate issues, identify stale
  bugs, prioritize what to work on next, or asks things like "help me triage
  my issues", "what should I work on from my backlog", or "which of my open
  issues are duplicates".
---

# GitHub Issue Triage

Fetch all open issues from a GitHub repository, classify and prioritize them,
and produce a triage report the user can act on. Optionally, after the report,
apply recommended changes — but only with explicit human approval per batch.

## Philosophy

- Read first, recommend second, write only with approval.
- Every recommended write is reviewable before it happens. No bulk auto-apply.
- Be specific: say *which* issue, *which* label, *why*.
- A backlog isn't a to-do list — it's a signal. Triage surfaces the signal
  (what's urgent, what's dead, what's duplicated) instead of just shuffling items.
- Prefer existing labels in the repo over inventing new ones.
- Short, useful output beats exhaustive reports nobody reads.

## Prerequisites

- `gh` CLI installed and authenticated (`gh auth status` should succeed).
- The user has at least read access to the target repo.
- If `gh` is missing or unauthenticated, stop and tell the user how to fix it
  before continuing.

## Inputs

### Required
- **Repository**, as `owner/repo` or a GitHub URL. If the user didn't specify
  one, ask. Don't guess from the current working directory unless they confirm.

### Optional
- A workspace directory to save the report. Default to
  `workspace/issue-triage/` at the repo root if a `workspace/` exists,
  otherwise save to the current directory as `ISSUE_TRIAGE.md`.
- A project-specific priority rubric (what counts as critical for *this* repo).
  If absent, use the default rubric in this skill.
- A cap on issues to fetch (default: all open issues).

## Workflow

### Step 1: Verify access and fetch

Run:

```bash
gh auth status
gh label list --repo <owner/repo> --limit 200 --json name,description,color
gh issue list --repo <owner/repo> --state open --limit 1000 \
  --json number,title,body,labels,author,assignees,createdAt,updatedAt,comments,url,state
```

Record the full label set — you'll only recommend labels that already exist
unless the user explicitly wants new ones proposed.

If the repo has more than 1000 open issues, warn the user and ask whether to
continue, sample, or filter further.

### Step 2: Classify each issue

For every issue, determine:

**Type** — one of:
- `bug` — something broken or behaving incorrectly
- `feature` — new capability or enhancement request
- `question` — a support/usage question, not actionable work
- `docs` — documentation gap or error
- `chore` — refactor, test, build, CI, dependency
- `discussion` — design/meta/roadmap with no clear action
- `unclear` — can't tell from the body; needs more info

**Priority** — one of:
- `critical` — data loss, security, broken core flow, affects many users
- `high` — affects a common workflow or blocks real users
- `medium` — real issue but workaround exists or narrow impact
- `low` — nice-to-have, cosmetic, rare edge case
- `unknown` — not enough info to judge

**Quality** — one of:
- `good` — has repro steps / clear ask / enough context
- `thin` — missing repro or context, author can likely clarify
- `needs-info` — unusable as-is; comment asking for specifics is the next step
- `noise` — spam, off-topic, clearly wrong repo

**Activity state** — one of:
- `fresh` — updated in the last 14 days
- `warm` — updated in the last 90 days
- `stale` — no activity in 90+ days
- `cold` — no activity in 180+ days (candidate for close-with-comment)

**Suggested labels** — labels from the existing repo label set that the issue
should carry, based on type, priority, and any area/component hints in the body.

**Duplicate candidates** — other issue numbers from the same batch this issue
likely duplicates. Use title overlap, shared error messages, shared stack
traces, and semantic similarity. Err on the side of flagging as *candidate*,
not confirmed — the user confirms.

### Step 3: Cluster duplicates

Group candidate duplicates into clusters. For each cluster, pick the best
"canonical" issue (usually the oldest with the most activity / clearest repro)
and list the others as likely duplicates of it.

### Step 4: Build the priority queue

Order issues into a "top N to look at next" list using this logic:
1. `critical` priority, any type, `good` or `thin` quality
2. `high` priority bugs with `good` quality
3. `high` priority bugs with `thin` quality (needs-info candidates)
4. `high` priority features with traction (comments, reactions)
5. Everything else by priority, then recency

Cap the priority queue at 15 items. The rest live in the full table.

### Step 5: Write the report

Save to the chosen output path using the template below. Then show the user:
- the overall counts
- the top 5 priority items
- the recommended-writes summary
- where the full report lives

### Step 6 (optional): Propose writes

After presenting the report, ask whether the user wants to apply any of the
recommended writes. If yes, work through them in **small reviewable batches**,
grouped by action type:

1. **Label additions** — show a table of `#N → labels to add`. User confirms
   the whole batch, or edits it, before applying with `gh issue edit`.
2. **Needs-info comments** — show each proposed comment in full. User approves
   each one individually; no bulk approval for comments.
3. **Duplicate closes** — show each cluster. For each, show the canonical
   issue, the duplicates, and the proposed close-comment. User approves each
   close individually.
4. **Stale closes** — show the list and the proposed close-comment. User
   approves the list (can remove items) before applying.

Never batch-apply across action types. Never apply any write without an
explicit "yes, apply these" from the user for that specific batch. If the user
edits the batch, re-show it and re-confirm before applying.

When applying:
- Labels: `gh issue edit <N> --repo <owner/repo> --add-label "<label>"`
- Comment: `gh issue comment <N> --repo <owner/repo> --body "<body>"`
- Close as duplicate: `gh issue close <N> --repo <owner/repo> --reason "not planned" --comment "Duplicate of #<canonical>. Closing — please continue the discussion there."`
- Close as stale: `gh issue close <N> --repo <owner/repo> --reason "not planned" --comment "<stale message>"`

After each batch, report what was actually applied (with issue numbers) so the
user can audit.

## Default priority rubric

Adjust to the project when the user provides one. Otherwise:

- **critical**: crashes on startup, data loss or corruption, security
  vulnerability, auth bypass, broken install, broken release, regression in
  the primary use case.
- **high**: a main workflow is broken for many users, a documented feature
  doesn't work, performance regression users notice, breaks a common
  integration.
- **medium**: narrow bug with a workaround, UX friction, inconsistency,
  edge-case failure, missing useful feature with clear demand.
- **low**: cosmetic, typo, rare edge case, nice-to-have, refactor with no
  user-visible impact.
- **unknown**: body doesn't give enough to judge impact.

## Duplicate detection heuristics

Flag as duplicate candidate when two issues share any of:
- near-identical titles (after normalizing case, punctuation, version numbers)
- the same error message or stack trace signature
- the same reproduction steps
- the same feature request phrased differently but with the same outcome
- cross-references in comments ("see also #123", "same as #456")

Do not auto-close. Duplicates are *candidates* until the user confirms.

## Needs-info comment template

When proposing a comment on a `needs-info` issue, draft something like:

> Thanks for the report! To help us investigate, could you share:
> - the exact version of `<tool>` you're running (`<tool> --version`)
> - your OS and version
> - a minimal reproduction (commands, config, or repo link)
> - the full error output
>
> Without these we can't reliably reproduce this — happy to reopen once we
> have more detail.

Tailor the specifics to the project. Never post a generic "please provide more
information" — always ask for the *specific* things this repo needs.

## Stale close comment template

> This issue has had no activity in over 180 days. Closing to keep the backlog
> focused — please reopen or comment if it's still relevant and we'll take
> another look.

## Report template

Save as `ISSUE_TRIAGE.md` (or in the workspace path). Use:

```markdown
# Issue Triage — <owner/repo>

**Triaged:** <date>
**Open issues:** <N>
**Stale (>180 days):** <N>
**Likely duplicate clusters:** <N>

## Summary

| Type | Count |
|------|-------|
| bug | |
| feature | |
| question | |
| docs | |
| chore | |
| discussion | |
| unclear | |

| Priority | Count |
|----------|-------|
| critical | |
| high | |
| medium | |
| low | |
| unknown | |

## Top priorities (next to look at)

1. **#<N>** — <title> — <priority> <type>
   - Why: <one line>
   - Recommended: <action>
2. ...

## Likely duplicate clusters

### Cluster 1 — canonical: #<N>
- **#<N>** <title> (canonical — oldest, most activity)
- #<N> <title> — same <reason>
- #<N> <title> — same <reason>
- Recommended: close duplicates with link to #<N>.

## Needs-info

Issues that can't be acted on without more detail from the author.

- **#<N>** <title> — missing: <what>
  - Proposed comment: <draft>

## Stale (>180 days, no activity)

- **#<N>** <title> — last update <date>
- ...
- Recommended: close with stale comment, or label `stale` for a grace period.

## Label recommendations

| Issue | Current labels | Recommended additions |
|-------|----------------|-----------------------|
| #<N> | <labels> | <labels> |

## Full triage table

| # | Title | Type | Priority | Quality | Activity | Suggested labels | Notes |
|---|-------|------|----------|---------|----------|------------------|-------|
| | | | | | | | |
```

## What not to do

- Don't apply any write (label, comment, close) without explicit per-batch
  human approval.
- Don't invent labels the repo doesn't have unless the user asks for label
  suggestions.
- Don't confidently mark duplicates as confirmed — they're always candidates.
- Don't post generic "please provide more info" comments. Always list the
  specific things this project needs.
- Don't close issues just because they're old. Cold + no engagement + resolved
  elsewhere is different from cold + still valid.
- Don't dump a 500-row report without a priority queue on top. The point of
  triage is surfacing *what to do next*, not cataloging.
- Don't silently skip issues you couldn't classify — list them under `unclear`
  so the user knows they weren't processed.
