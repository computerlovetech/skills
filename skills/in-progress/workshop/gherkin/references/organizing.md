# Organizing features

Feature files are documentation first. Organize them so a reader can find what the system does, not how the tests are wired.

## Principles

- **One feature per capability.** Name files and features after business capabilities (`withdraw_cash.feature`), not after screens, tickets, or sprints.
- **Group by domain.** Use folders for business areas (`features/billing/`, `features/accounts/`).
- **Use `Rule` to structure a feature.** Each rule gets the examples that illustrate it, which makes gaps visible.
- **Keep `Background` short and essential.** Use it only for context every scenario in the scope needs and the reader must see. Hide setup the reader doesn't care about in step definitions or hooks. Keep it to a few `Given` steps.
- **Tag with purpose.** Use a small, agreed set of tags (`@smoke`, `@wip`, `@slow`, ticket IDs if useful). Don't tag every scenario with everything.
- **Describe the feature.** Use the free-text description under `Feature` for the why, the actors, and links to related material.

## Step definitions

- **Write steps, then glue.** Formulate the scenario in business language first, then write step definitions to fit it. Don't bend the language to reuse existing steps.
- **Keep glue thin.** Step definitions should translate to calls into the domain or an application driver, not hold test logic. Put UI or API mechanics in a separate layer (page objects, drivers, or the screenplay pattern).
- **Organize steps by domain concept, not by feature.** `account_steps` rather than `withdrawal_feature_steps`, so steps can be shared without coupling features.
- **Use expressions, not regex soup.** Cucumber expressions with parameter types (`{int}`, custom `{account}`) keep steps readable and convert values in one place.
- **Share state through a world or context object,** not globals.

## Check

- Can someone new find the behaviour they're looking for from the folder and file names?
- Does each `Rule` have examples, and does each scenario sit under the rule it illustrates?
- Does every `Background` step matter to every scenario under it?
- Do step definitions read like translations, with no logic or assertions buried in helpers?
