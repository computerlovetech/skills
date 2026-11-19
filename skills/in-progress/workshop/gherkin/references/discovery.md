# Discovery

Good Gherkin comes from good conversations. Before formulating, the team finds the rules and concrete examples together. The usual group is the **three amigos**: someone for the business (product owner or analyst), a developer, and a tester. Each brings a different view of what could go wrong.

## Example mapping

Matt Wynne's example mapping is a short, timeboxed session (about 25 minutes per story) using four colours of cards:

- **Yellow: the story.** The thing being discussed.
- **Blue: rules.** Acceptance criteria or business rules the story must satisfy.
- **Green: examples.** Concrete cases illustrating a rule, placed under it. Phrase them as short "the one where…" titles, not full Gherkin.
- **Red: questions.** Unknowns nobody in the room can answer. Park them instead of debating.

Read the map:

- **Many red cards:** the story isn't ready. Answer the questions first.
- **Many blue cards:** the story is too big. Split it, often along rules.
- **A rule with many examples:** the rule may be several rules.
- **A rule with no examples:** it isn't understood yet.

## From map to Gherkin

- Each blue card becomes a `Rule`.
- Each green card becomes a `Scenario`, named after its example.
- Each red card becomes a follow-up, not a scenario.

Formulate soon after discovery, ideally with the business reviewing the result, so the Gherkin stays true to what was agreed.

## Principles

- **Examples before abstractions.** Ask "can you give me an example?" whenever a rule feels vague.
- **Look for edges.** Ask for the one where it fails, the one at the boundary, and the one nobody thought of.
- **Discover before you automate.** Gherkin written without conversation tends to be a test script in disguise.

## Check

- Does every rule have at least one example?
- Are open questions recorded instead of guessed?
- Could the story be delivered without answering the remaining red cards?
