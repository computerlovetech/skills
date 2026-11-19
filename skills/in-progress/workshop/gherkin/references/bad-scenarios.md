# Bad scenarios

Use this as a checklist when reviewing feature files.

## Traps

- **Test scripts in Gherkin.** Steps describe clicks, fields, and URLs instead of behaviour. They break on every UI change and hide the rule.
- **Incidental details.** Values and steps that don't affect the outcome, such as a full address in a scenario about discounts.
- **Several behaviours in one scenario.** Multiple `When`/`Then` pairs, or a long journey testing everything at once.
- **Conjunction steps.** One step doing two things ("Given I have an account and I am logged in"), which makes reuse and reading harder.
- **Abstract data.** "user1", "product X", "a valid amount". Readers can't check the example against reality.
- **`Then` checks internals.** Asserting on database rows, logs, or method calls instead of what an actor could observe.
- **`Given` performs the action under test.** Context set up through the same UI flow the scenario is about.
- **Bloated `Background`.** Long setup that only some scenarios need, or that readers must scroll back to understand.
- **Giant outlines.** Dozens of rows, or columns that change which behaviour is tested. These belong in unit tests or separate scenarios.
- **Vague names.** "Scenario 1", "Happy path", or names that repeat the steps.
- **Dependent scenarios.** One scenario relies on state left by another, or on running in a set order.
- **Developer-only language.** Words like `null`, `HTTP 404`, `flag`, or table names in a spec meant for the business.
- **Written after the fact.** Scenarios generated from existing code or tests, with no discovery conversation, describe what was built, not what was wanted.
- **Everything as Gherkin.** Using Cucumber for checks no business person will read. Plain unit tests are cheaper there.

## Review questions

1. Would a business expert read this and agree it is right?
2. Does each scenario illustrate a single rule, named after what makes it distinct?
3. Is every step declarative and free of UI mechanics?
4. Is every value real and essential?
5. Does each `Then` describe something observable?
6. Can each scenario run alone?
7. Would this be better as a unit test?
