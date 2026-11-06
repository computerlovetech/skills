# ADR record

Read repository instructions, the existing index, and related ADRs before drafting. Reuse local conventions. If none exist, use:

```text
docs/adr/
└── ADR-001-short-decision-title.md
```

Create the directory with the first requested record. Use the highest existing number plus one, preserving the local prefix and padding. Do not fill gaps or renumber historical records. If identifiers are already duplicated, use full titles and paths to disambiguate references and report the collision.

Use the [ADR template](templates/adr.md) as a starting point. Remove inapplicable optional metadata and sections; keep the decision, rationale, and consequences understandable. Label unknown historical facts instead of supplying today's date or invented reasoning. A new draft starts as Proposed unless acceptance is already established.

Update the existing architecture decisions index. If there is none, add a concise index to the repository's agent instructions or link a dedicated ADR index from them. Each record should have one entry with its number, title, relative link, status when not accepted, and a short "read when" cue. Preserve existing reading guidance and include proposed and retired records so their status is visible.

Before finishing, check that the identifier is unique, local links resolve, the index matches the records, and lifecycle transitions are supported by evidence. Report changed paths and any unresolved questions.
