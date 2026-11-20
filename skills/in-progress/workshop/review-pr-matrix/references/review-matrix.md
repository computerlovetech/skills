# Review matrix reference

Rows are **Change types**. The **Present?** column records whether the diff contains each type. The remaining columns are **Review criteria**.

Classify from the diff and relevant surrounding code. A change can match several rows. Mark both API rows when a change breaks the existing client contract. Treat schema and data migrations as migrations, SQL and ORM query behavior changes as query changes, and behavior-preserving restructuring as refactoring, even when bundled with a feature.

| Change type | Covered by regression tests? | Necessary for the user story? | Failure modes and edge cases handled? | Safe to roll out and roll back? |
|---|---|---|---|---|
| Database migration | Do tests cover upgrades from the existing schema with representative data? | Which acceptance criterion needs the schema or data change? | What happens after a partial failure or retry? | Can app versions coexist during rollout, and is there a safe recovery path? |
| Database query changes | Do tests verify the changed results or behavior on representative data? | Which required behavior or performance target needs the query change? | Are empty results, timeouts, and concurrency handled where relevant? | Can the old query be restored, and are required schema or indexes available first? |
| UI changes | Do tests cover the affected user flows? | Which user task or acceptance criterion does the change support? | Are loading, empty, error, and accessibility states handled where relevant? | Can the previous UI work with the deployed API and data? |
| API changes | Do contract or integration tests cover changed requests, responses, and errors? | Which consumer need or acceptance criterion requires the change? | Are invalid inputs, permissions, and error responses handled? | Can callers and servers be deployed and rolled back safely? |
| Breaking client API changes | Do tests cover the intended behavior of existing and migrated clients? | Why does the story require breaking the contract? | What happens when an older client encounters the changed contract? | Is there a versioning or migration plan with a recovery path? |
| Refactoring | Do existing or new tests verify that behavior is preserved? | What part of the story does the refactor enable? | Are existing error paths and side effects preserved? | Can the previous implementation be restored safely if the refactor causes a regression? |
