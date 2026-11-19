# Writing scenarios

A scenario is one concrete example of one rule. It should read as a short story a business expert agrees with: some context, one thing happens, and an observable result. Rose and Nagy's *Formulation* sums up good scenarios as **BRIEF**.

## BRIEF

- **Business language.** Use words the business uses, not words from the UI, database, or code. Keep this vocabulary consistent across features (the ubiquitous language).
- **Real data.** Use concrete, realistic values ("Alice", "£30", "2 days late") instead of "user1" or "X". Real data exposes misunderstandings that abstract data hides.
- **Intention revealing.** Describe *what* the actor wants to achieve, not *how* they click through the system.
- **Essential.** Leave out any detail that doesn't affect the outcome. If removing a step or value doesn't change the meaning, remove it.
- **Focused.** Each scenario illustrates a single rule.
- **Brief.** Aim for five steps or fewer. Long scenarios are hard to read and usually hide more than one behaviour.

## Principles

- **Declarative over imperative.** Write "When Alice buys the book" rather than "When she clicks 'Add to basket'" and "And she clicks 'Checkout'". Declarative steps survive UI changes and say why, not how.
- **Given is state, When is one action, Then is an outcome.** Write `Given` in the past or present tense ("Alice has ordered", "the basket contains"). Use one `When` per scenario. `Then` asserts something an actor could observe, not internal state.
- **One behaviour per scenario.** More than one `When`/`Then` pair usually means two scenarios.
- **Name the scenario after what makes it different.** The name should say how this example differs from its siblings, for example "Refund refused after 30 days" rather than "Refund test 2".
- **Use a consistent actor.** A named persona ("Alice, a premium customer") carries context so steps don't have to.
- **Use outlines only when examples differ only in data.** If the rows need different explanations, write separate scenarios with descriptive names.
- **Keep scenarios independent.** Each one sets up its own context and can run alone and in any order.

## Imperative vs declarative

```gherkin
# Imperative: describes the UI
Scenario: Login
  Given I am on "/login"
  When I fill in "email" with "alice@example.com"
  And I fill in "password" with "secret"
  And I press "Log in"
  Then I should see "Welcome"

# Declarative: describes the behaviour
Scenario: Registered user signs in
  Given Alice has registered
  When she signs in with her credentials
  Then she should see her dashboard
```

## Check

- Would a business expert understand and agree with every line?
- Does the scenario name tell you which rule it illustrates and how it differs from the others?
- Is there exactly one `When`?
- Can any step or value be removed without changing the meaning?
- Would the scenario still be true if the UI were redesigned?
