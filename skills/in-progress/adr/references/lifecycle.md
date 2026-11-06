# Applying and revisiting decisions

Find the repository's ADR index and read records relevant to the area being changed, including linked replacements. Use status and scope to determine which decisions govern the work. A proposal is under discussion; it is not an accepted constraint.

If a requested change conflicts with an accepted ADR, identify the record and explain the conflict. Distinguish implementation drift from an intentional change of direction. Do not silently introduce a parallel pattern or rewrite the record to make current code appear compliant. Report the conflict within the task; create a replacement record only when requested.

Use the repository's lifecycle vocabulary. When none is established:

- **Proposed:** under discussion; the default for a new draft.
- **Accepted:** acceptance is established by the user or project evidence.
- **Rejected:** considered but not adopted; retain the reasoning.
- **Deprecated:** no longer applicable, with the reason recorded.
- **Superseded:** replaced by another accepted ADR, linked explicitly.

Preserve accepted decision text and rationale. Correcting a typo or broken link does not change the decision; changing its substance requires a new ADR. A proposed replacement leaves the existing decision active. When the replacement is accepted, mark the old record superseded, date the transition, and link both records through lifecycle metadata. Preserve unaffected decisions when a new ADR merely supplements them.

Keep the index's titles, links, and status labels consistent with the records. Do not infer acceptance from a filename, a merged implementation, or the act of writing the ADR.
