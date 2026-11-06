# Decisions and rationale

Record a choice whose reasoning future contributors need: a costly commitment, a boundary that several parts of the system must respect, a surprising trade-off, or a constraint invisible in code. Routine implementation details usually belong in code or module documentation. A request to document a decision is sufficient reason to help; do not impose a rigid eligibility test.

Keep one consequential decision per record. Aim for one page, at most two; link detailed designs, operational instructions, and supporting evidence instead of embedding them. Keep constraints needed to understand the decision in the record itself.

Lead with what is decided and where it applies. Explain the problem and constraints, then why the choice fits them. Record the benefits and drawbacks of serious alternatives actually considered, including keeping the current approach when relevant. State the costs and obligations the chosen approach creates, not just its advantages.

Distinguish evidence, assumptions, and expected outcomes. Never invent alternatives, dates, owners, advice, confidence, or acceptance. For a historical decision with missing rationale, say what was not recorded. When a missing fact prevents a useful draft, ask a focused question; otherwise make the uncertainty visible in the draft.

Confidence should have a basis: experiments, operational experience, or unresolved assumptions. Name observable conditions that would justify reevaluation, such as a workload exceeding a tested limit or a new requirement breaking a boundary. Do not add a confidence score without evidence.

Review for these failures:

- A topic or aspiration in place of a concrete choice.
- An implementation plan that obscures the enduring decision.
- Alternatives invented to make the chosen option look inevitable.
- Benefits without costs, limitations, or ongoing obligations.
- A proposed approach presented as accepted, or accepted architecture presented as fully implemented.
- General claims such as "more scalable" without the relevant constraint or evidence.
