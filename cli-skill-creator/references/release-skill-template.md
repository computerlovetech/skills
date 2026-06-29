---
name: <tool>-release
description: >
  Release process for the <tool> package. Handles version bumping
  (major/minor/patch/beta), changelog updates, pre-release quality checks, git
  tagging, and monitoring the GitHub Actions publish pipeline. Use whenever the
  user wants to cut a release, bump the version, publish to PyPI, or asks about
  the release process — even if they just say "let's ship it" or "time for a new
  version".
---

# <Tool> Release Process

Releases are tag-driven: pushing a `vX.Y.Z` tag triggers the GitHub Actions
publish pipeline that runs quality checks, builds, publishes to PyPI via trusted
publishing, and creates a GitHub Release. Your job is to prepare everything so
the pipeline succeeds on the first try.

## Preconditions

Verify before editing anything. If any fail, stop and tell the user.

1. Clean working tree — `git status --short`
2. On `main` — `git branch --show-current`
3. Up to date with remote — `git fetch origin` and compare with `origin/main`

If the user hasn't said, ask what kind of release this is:
- **patch** (0.1.0 → 0.1.1) — bug fixes
- **minor** (0.1.0 → 0.2.0) — backwards-compatible features
- **major** (0.1.0 → 1.0.0) — breaking changes
- **beta** (0.1.1b1) — pre-release testing

## Step 1 — Inspect what changed

```bash
git log $(git describe --tags --abbrev=0)..HEAD --oneline
```

Cross-check against the `## [Unreleased]` section in `CHANGELOG.md`; add any
missing user-facing changes under Added / Changed / Fixed / Removed / Docs.

## Step 2 — Run local checks (mirror CI exactly)

```bash
uv run ruff check .
uv run ruff format --check .
uv run ty check
uv run pytest -m "not e2e and not network and not slow"
uv build
```

Fix any failure before continuing. Don't tag from a failing local state.

## Step 3 — Docs check

Update docs/README only if user-facing behavior changed (a command/flag changed,
public API changed, examples no longer match). Skip for internal refactors. <If
a CLI skill is bundled in two places, remind to update both copies here.>

## Step 4 — Bump the version

Edit `pyproject.toml` `version = "X.Y.Z"` — the single source of truth. Beta:
`0.1.0` → `0.1.1b1` → `0.1.1b2` → `0.1.1` (promote to stable).

## Step 5 — Update the changelog

In `CHANGELOG.md`: rename `## [Unreleased]` to `## [X.Y.Z] - YYYY-MM-DD`, ensure
all changes are listed, and add a fresh empty `## [Unreleased]` at the top. The
heading format is what the pipeline's `awk` extracts — keep it exact.

## Step 6 — Commit, tag, push

```bash
git add pyproject.toml CHANGELOG.md   # plus any docs you changed
git commit -m "release: vX.Y.Z"
git tag vX.Y.Z
```

**Show the user a summary (version, changelog section, files changed, tag) and
wait for explicit confirmation before pushing.**

```bash
git push origin main
git push origin vX.Y.Z
```

## Step 7 — Monitor the pipeline

```bash
gh run list --workflow=publish.yml --limit=1
gh run watch $(gh run list --workflow=publish.yml --limit=1 --json databaseId -q '.[0].databaseId')
```

Stages: Quality → Build (+ version-matches-tag) → Publish to PyPI → Create
GitHub Release. On failure: `gh run view <run-id> --log-failed`. Common causes:
quality slipped past local checks, version already on PyPI, malformed changelog
heading.

## Step 8 — Verify

```bash
pip index versions <tool>
gh release view vX.Y.Z
```

Report the PyPI and GitHub Release links.

## Recovery (destructive — confirm first)

If a pushed tag must be retried: fix the issue, then (after user confirmation)
`git tag -d vX.Y.Z && git push origin :refs/tags/vX.Y.Z`, amend or add a fix
commit, and re-tag.
