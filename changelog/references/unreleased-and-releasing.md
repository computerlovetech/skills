# Unreleased and releasing

## The Unreleased section

Keep an `## [Unreleased]` section at the top to track upcoming changes.

- People can see what changes they can expect in upcoming releases.
- At release time, the Unreleased section becomes the new version's section, so there is nothing to reconstruct.
- Add an entry in the same change (commit or pull request) that makes the notable change, while the details are fresh.

## Cutting a release

1. Decide the version number. Under Semantic Versioning: major for breaking changes, minor for new features, patch for fixes only.
2. Rename `## [Unreleased]` to `## [x.y.z] - YYYY-MM-DD` with today's date.
3. Add a new, empty `## [Unreleased]` section above it.
4. Update the link references at the bottom:
   - `[unreleased]` now compares the new tag with `HEAD`.
   - Add `[x.y.z]` comparing the previous tag with the new one.
5. Tag the release in version control with the same version.

## Yanked releases

A yanked release is a version pulled because of a serious bug or security issue. Don't delete it from the changelog. Keep it and mark it:

```markdown
## [0.0.5] - 2014-12-13 [YANKED]
```

The `[YANKED]` tag is in square brackets so it stands out and is easy to parse.

## Correcting the changelog

A changelog can be improved after the fact. If a release forgot to mention a breaking change or another important change, add it to that version's section.
