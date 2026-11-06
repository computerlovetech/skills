---
name: adr
description: Record and respect architecture decision records (ADRs) in docs/adr/. Use when a hard-to-reverse, surprising trade-off is made, when work touches an area with recorded decisions, or when a proposal contradicts an existing ADR.
---

# ADR

An architecture decision record (ADR) explains a decision a future reader would otherwise question. It records *that* a decision was made and *why*.

## Where they live

- `docs/adr/` at the project root, numbered `0001-{slug}.md`, `0002-{slug}.md`, …
- In a project with several contexts, context-specific decisions may live in `{context}/docs/adr/`; system-wide ones stay at the root.
- Create `docs/adr/` when the first ADR is needed, never upfront.

## Use them

- Before changing an area, read the ADRs that touch it.
- If your proposal contradicts an ADR, say so explicitly rather than silently overriding it: _"Contradicts ADR 0003 (manual SQL), but worth reopening because…"_
- When an ADR is overturned, write a new ADR and mark the old one `superseded by ADR NNNN`. Never rewrite history.

## When to write one

Offer an ADR only when all three hold:

1. **Hard to reverse**: changing course later is costly.
2. **Surprising without context**: a reader would ask "why did they do it this way?"
3. **A real trade-off**: there were genuine alternatives, chosen between for specific reasons.

If any is missing, skip it. Easy-to-reverse decisions get reversed; obvious ones need no explanation.

Typical qualifiers:

- **Architectural shape**: monorepo, event-sourced write model, SPA with a separate API.
- **Integration between contexts**: events versus synchronous calls.
- **Technology with lock-in**: database, auth provider, deployment target. Not ordinary libraries.
- **Boundaries and scope**, including explicit "we won't".
- **Deliberate deviations** from the obvious path, so nobody "fixes" them.
- **Constraints invisible in code**: compliance, partner contracts, latency budgets.
- **Non-obvious rejected alternatives**, so they aren't re-proposed every six months.

## File format

File name: `docs/adr/{NNNN}-{slug}.md`. `NNNN` is the highest existing number plus one, zero-padded to four digits. `slug` is the title in lowercase kebab-case.

The minimum ADR is a title and one paragraph:

```md
# {Decision, phrased as what we do}

{One to three sentences: the context, what we decided, and why.}
```

Add these only when they earn their place, in this order:

- **Status** as frontmatter: `proposed`, `accepted`, `deprecated` or `superseded by ADR NNNN`. Useful once decisions get revisited.
- `## Considered options`: when the rejected alternatives are worth remembering.
- `## Consequences`: when downstream effects are non-obvious.

### Example

```md
---
status: accepted
---

# Use manual SQL instead of an ORM

Reporting queries rely on window functions and CTEs that our ORM expresses poorly and slowly. We write SQL by hand behind repository interfaces, so the domain never sees it.

## Considered options

- **ORM with raw-SQL escape hatches**: rejected; two query styles made reviews harder.

## Consequences

- Schema changes need matching SQL updates; repository tests run against a real database.
```

## Credits

Adapted from the `domain-modeling` skill and its ADR format in Matt Pocock's [mattpocock/skills](https://github.com/mattpocock/skills), MIT License, Copyright (c) 2026 Matt Pocock. This version covers only decision records, separate from the glossary and issue-tracker setup.
