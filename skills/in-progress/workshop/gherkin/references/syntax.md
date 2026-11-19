# Syntax

A Gherkin file has the `.feature` extension and holds one `Feature`. Most lines start with a keyword. Indentation is free, but two spaces per level is conventional.

```gherkin
# language: en
@billing
Feature: Account withdrawal
  Customers can take cash out of their account.

  Background:
    Given Alice has a current account

  Rule: Withdrawals cannot exceed the balance

    Scenario: Withdraw less than the balance
      Given her balance is £100
      When she withdraws £30
      Then her balance should be £70

    Scenario Outline: Withdraw more than the balance
      Given her balance is £<balance>
      When she withdraws £<amount>
      Then the withdrawal should be refused

      Examples:
        | balance | amount |
        | 0       | 1      |
        | 100     | 101    |
```

## Keywords

| Keyword | Purpose |
|---|---|
| `Feature` | Names the capability. Free-text description lines may follow. One per file. |
| `Rule` | Groups the scenarios that illustrate one business rule (Gherkin 6+). |
| `Scenario` / `Example` | One concrete example of behaviour. The two words are synonyms. |
| `Background` | Steps run before every scenario in its `Feature` or `Rule`. At most one per level. |
| `Scenario Outline` / `Scenario Template` | A scenario run once per row of its `Examples`. |
| `Examples` / `Scenarios` | The table of values for an outline. An outline may have several, each with its own tags and name. |
| `Given` | Context: the state of the world before the action. |
| `When` | The event or action. |
| `Then` | The expected, observable outcome. |
| `And` / `But` | Continue the previous step type. |
| `*` | A step with no type, for bullet-like lists. |

Step keywords are for readers. Cucumber ignores them when matching a step to code, so `Given there is £5` and `Then there is £5` match the same step definition.

## Step arguments

**Data table**: pipe-delimited rows directly under a step. Escape `|` as `\|`, a newline as `\n`, and a backslash as `\\`.

```gherkin
Given the following users exist:
  | name  | role  |
  | Alice | admin |
  | Bob   | guest |
```

**Doc string**: a block of text between `"""` or ```` ``` ````. An optional content type can follow the opening delimiter. Indentation is relative to the delimiter.

```gherkin
When the API receives:
  """json
  { "amount": 30 }
  """
```

## Outlines

`<name>` placeholders in an outline's steps are replaced by the matching column in each `Examples` row. Placeholders also work in the scenario name and in step arguments.

## Tags

`@tag` lines go above `Feature`, `Rule`, `Scenario`, `Scenario Outline`, or `Examples`. Tags are inherited downward. Use them to filter runs (`--tags "@smoke and not @wip"`) and to attach hooks.

## Comments and descriptions

A line starting with `#` is a comment. Free-text lines after `Feature`, `Rule`, `Background`, `Scenario`, or `Examples` are a description. They are kept as documentation but not executed.

## Localization

A `# language: <code>` comment on the first line switches the keywords to that language, such as `# language: da` for Danish (`Egenskab`, `Scenarie`, `Givet`, `Når`, `Så`). Gherkin supports more than 70 languages.

## Check

- Does each file have exactly one `Feature`?
- Does every outline have at least one `Examples` table whose columns match its placeholders?
- Is there at most one `Background` per `Feature` or `Rule`?
