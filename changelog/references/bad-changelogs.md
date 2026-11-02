# Bad changelogs

Use this as a checklist when reviewing a changelog.

## Bad practices

- **Commit log diffs.** Dumping `git log` into the changelog. Commit logs are full of noise: merge commits, obscure titles, documentation changes. A commit records a step in the source code; a changelog entry documents a noteworthy difference for users.
- **Ignoring deprecations.** Users who upgrade should be able to see what will break. List deprecations, removals, and breaking changes.
- **Confusing dates.** Regional formats like `06/02/2026` are ambiguous. Use ISO 8601: `2026-06-02`.
- **Inconsistent changes.** Mentioning only some of the changes can be as dangerous as no changelog at all. Record all notable changes, every release.

## Other traps

- **No Unreleased section.** Entries are reconstructed from memory at release time, and things get missed.
- **Missing versions.** Releases with no entry.
- **Oldest first.** Readers have to scroll to find the latest release.
- **No links.** Versions don't link to the diff, so readers can't see the detail.
- **Vague entries.** "Various bug fixes and improvements" tells users nothing.
- **Deleted yanked releases.** Remove the release and users can't tell why a version disappeared. Mark it `[YANKED]` instead.
- **Only in GitHub Releases.** Not portable and harder to find than a file in the repo.

## Review questions

1. Is there an Unreleased section at the top?
2. Does every version have an entry, newest first, with an ISO 8601 date?
3. Are entries grouped under the standard types?
4. Is each entry written for users rather than copied from commits?
5. Are deprecations, removals, and breaking changes called out?
6. Do version headings link to comparisons?
7. Does the header say whether the project follows Semantic Versioning?
