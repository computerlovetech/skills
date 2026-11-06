# Types of changes

Group entries under these headings, in this order, and include only the ones that apply to a version.

| Type | For | Example |
|---|---|---|
| **Added** | New features. | Added a `--json` output flag. |
| **Changed** | Changes in existing functionality. | Default timeout is now 30 seconds instead of 10. |
| **Deprecated** | Soon-to-be removed features. | `--legacy` flag is deprecated and will be removed in 3.0. |
| **Removed** | Now removed features. | Removed support for Python 3.8. |
| **Fixed** | Bug fixes. | Fixed a crash when the config file is empty. |
| **Security** | In case of vulnerabilities. | Fixed path traversal in file uploads (CVE-2026-1234). |

## Choosing a type

- **Changed vs. Fixed.** If the old behaviour was intended and is now different, it's Changed. If it was a bug, it's Fixed.
- **Deprecated before Removed.** Deprecate first, ideally for at least one release, so users can prepare. Then list it under Removed when it is gone.
- **Security over Fixed.** Vulnerability fixes go under Security so users can find them quickly.
- **Breaking changes.** There is no separate type. List them under Changed or Removed and mark them clearly, for example with **BREAKING** at the start of the entry, and say what users must do. Under Semantic Versioning they require a major version bump.
