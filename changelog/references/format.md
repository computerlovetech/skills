# Format

## File

- Name it `CHANGELOG.md`, in the project root. Some projects use `HISTORY`, `NEWS`, or `RELEASES`, but `CHANGELOG.md` is the convention.
- Write it in Markdown.
- Keep it in the repository rather than only in GitHub Releases, which are non-portable and less discoverable. Releases can mirror the changelog.

## Structure

1. A title and short header stating that notable changes are documented here, that the format follows Keep a Changelog, and whether the project follows Semantic Versioning.
2. An `## [Unreleased]` section at the top.
3. One `## [version] - YYYY-MM-DD` section per release, newest first.
4. Within each version, `### <Type>` subsections, using only the [types](types-of-changes.md) that apply.
5. Link references at the bottom: each version links to a comparison with the previous version, and `[unreleased]` compares the latest tag with `HEAD`.

## Dates

Use ISO 8601: `YYYY-MM-DD`, for example `2017-07-17`. It is unambiguous across regions and sorts correctly. Avoid regional formats like `07/17/2017` or `17.07.2017`.

## Template

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Export results as CSV.

## [1.1.0] - 2026-10-14

### Added

- `--json` flag to print results as JSON.

### Fixed

- Crash when the config file contains an empty value.

## [1.0.0] - 2026-09-01

### Added

- Initial release.

[unreleased]: https://github.com/owner/repo/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/owner/repo/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/owner/repo/releases/tag/v1.0.0
```
