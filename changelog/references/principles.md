# Guiding principles

Keep a Changelog rests on a few principles.

- **Changelogs are for humans, not machines.** Write for the people who use or contribute to the project.
- **There should be an entry for every single version.**
- **Group the same types of changes.** Use the [types of changes](types-of-changes.md).
- **Versions and sections should be linkable.** Use Markdown headings and link references; see [Format](format.md).
- **The latest version comes first.** Reverse chronological order.
- **The release date of each version is displayed.** In ISO 8601 format, `YYYY-MM-DD`.
- **Mention whether you follow Semantic Versioning.**

## What counts as notable

A changelog lists changes that matter to its readers, not everything that happened.

| Include | Leave out |
|---|---|
| New features and options. | Merge commits. |
| Behaviour changes users will notice. | Refactors with no visible effect. |
| Deprecations, removals, and breaking changes. | Documentation typo fixes. |
| Bug fixes users might have hit. | Internal tooling and CI changes. |
| Security fixes. | Commit-by-commit detail. |

## Writing entries

- Describe the change from the reader's point of view: what they can now do, or what behaves differently.
- One change per bullet, short and specific.
- Call out breaking changes clearly, and say what users need to do.
- Link to issues or pull requests where useful, but the entry must make sense on its own.

| Commit-style | Changelog-style |
|---|---|
| `fix: handle null in parseConfig` | Fixed a crash when the config file contains an empty value. |
| `refactor auth middleware, bump deps` | *(omit unless users notice a difference)* |
| `feat: add --json flag` | Added a `--json` flag to print results as JSON. |
