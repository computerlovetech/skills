---
name: pypi-cli-cicd
description: >
  Set up a tag-driven GitHub Actions CI/CD pipeline that publishes a Python CLI
  to PyPI — the computerlove.tech recipe used by agr and outcome-engineering.
  Configures a uv-managed package whose version is a single source of truth, a
  test workflow (ruff + ty + pytest on push/PR), and a publish workflow that, on
  a vX.Y.Z tag, runs quality checks, builds, publishes to PyPI via trusted
  publishing (OIDC — no API token), and cuts a GitHub Release from CHANGELOG.md.
  Use this whenever the user wants to add CI/CD or PyPI publishing to a Python
  CLI/package, set up tag-driven releases, configure trusted publishing, or
  "ship this to PyPI like agr" — e.g. "add a release pipeline", "publish my CLI
  to PyPI on a tag", "set up GitHub Actions for this package".
---

# PyPI CLI CI/CD Pipeline

This is the GitHub Actions release recipe behind `agr` and `outcome-engineering`:
a Python CLI that ships to PyPI the moment you push a `vX.Y.Z` tag, with no
stored secrets. This skill sets up (or retrofits) that pipeline.

> Companion skill: to give agents an in-repo *release playbook* and an operating
> manual for the CLI, use **`cli-skill-creator`** after this. This skill builds
> the pipeline; that one authors the agent skills that drive it.

## Two facts that drive the whole design

- **The version in `pyproject.toml` is the single source of truth.** Runtime
  code reads it back via `importlib.metadata`; the publish workflow refuses to
  build if it doesn't match the pushed tag. You bump it in exactly one place.
- **Releases are tag-driven.** Pushing a `vX.Y.Z` tag *is* the release. The
  pipeline runs quality → build → publish → GitHub Release. Nothing else
  triggers a publish. So shipping reduces to: green `main`, bumped version,
  correct changelog, push tag.

## What you set up

1. **Project skeleton** — `pyproject.toml` with a `[project.scripts]` entry
   point and the version as source of truth. See
   `references/pyproject-template.toml`.
2. **`test.yml`** — quality (`ruff check`, `ruff format --check`, `ty check`) +
   tests (`pytest`) [+ optional `mkdocs build --strict`] on every push/PR to
   `main`. See `references/test-workflow.yml`.
3. **`publish.yml`** — the tag-driven release pipeline. See
   `references/publish-workflow.yml`.
4. **`CHANGELOG.md`** — Keep a Changelog format; the pipeline parses it for
   release notes. See `references/changelog-template.md`.
5. **Trusted publishing** configured on PyPI (one-time, outside the repo).

## Steps

### 1. Project skeleton

Use `uv`. Copy `references/pyproject-template.toml` and fill in the placeholders.
The load-bearing parts:

- `[project] version = "0.1.0"` — the one place the version lives.
- `[project.scripts]` mapping `<tool> = "<package>.cli:app"` — what makes the
  command runnable after `pip install`.
- `[dependency-groups] dev` with `pytest`, `ruff`, `ty`.
- A build backend (`hatchling` or `uv_build`).

Wire the version into the runtime so `--version` can't drift:

```python
# <package>/__init__.py
from importlib.metadata import version
__version__ = version("<tool>")
```

Adopt the **`uv run` convention** for every command (`uv run pytest`,
`uv run ruff check .`, `uv run ty check`) and document it in `AGENTS.md`.

### 2. CI workflow — `test.yml`

Copy `references/test-workflow.yml` to `.github/workflows/test.yml`. It uses
`astral-sh/setup-uv`, runs on push/PR to `main`, and has three jobs: **quality**,
**test**, and an optional **docs** build. Mark slow/network/e2e tests and exclude
them in CI with `-m "not e2e and not network and not slow"`. Split jobs for
parallelism, or collapse to one job for a small project.

### 3. Release workflow — `publish.yml`

Copy `references/publish-workflow.yml` to `.github/workflows/publish.yml`. It
triggers on `push: tags: ['v*']` plus a `workflow_dispatch` with a `dry_run`
input (build path without publishing). Four sequential jobs:

1. **quality** — same checks as CI. Never publish from red.
2. **build** — `uv build`, then **verify `pyproject.toml` version == tag**
   (`v1.2.3` → `1.2.3`). Catches the most common release mistake. Uploads
   `dist/`.
3. **publish** — `pypa/gh-action-pypi-publish` via **trusted publishing**; needs
   `permissions: id-token: write` and a `pypi` environment. **No token stored.**
4. **release** — validates the tag format
   (`^v[0-9]+\.[0-9]+\.[0-9]+([ab][0-9]+)?$`), extracts the matching version
   section from `CHANGELOG.md` with `awk`, and creates the GitHub Release with
   `gh`. Only this job gets `contents: write`.

### 4. Changelog

Add `CHANGELOG.md` from `references/changelog-template.md`. Keep an
`## [Unreleased]` section at the top. The release job matches headings of the
form `## [X.Y.Z] - YYYY-MM-DD` exactly — the format is load-bearing, not
decoration.

### 5. Configure trusted publishing on PyPI (one-time)

This must happen outside the repo or the publish job fails with an auth error:

- On PyPI: project → **Settings → Publishing** → add the GitHub repo, the
  workflow filename (`publish.yml`), and environment name **`pypi`**.
- For a **brand-new package name**, use PyPI's **"pending publisher"** flow so
  the first tagged release can create the project.

### 6. First release

- Test the build path: run `publish.yml` via `workflow_dispatch` with
  `dry_run: true`.
- When green and the version/changelog are ready, tag and push:
  `git tag v0.1.0 && git push origin v0.1.0`.
- Watch it: `gh run watch $(gh run list --workflow=publish.yml --limit=1 --json databaseId -q '.[0].databaseId')`.

## Boundaries

- **Never publish from a red `main`.** Quality runs first in both workflows for a
  reason.
- **One version source.** Bump `pyproject.toml` only; read it at runtime via
  `importlib.metadata`. Don't hardcode it elsewhere.
- **Prefer trusted publishing over a stored token.** If the user insists on an
  API token, that's a deliberate deviation — flag it and use a repo secret
  scoped to the publish job.
- **The version-matches-tag guard stays.** It's the cheapest protection against a
  mismatched release.

## References

- [pyproject-template.toml](references/pyproject-template.toml) — package skeleton
- [test-workflow.yml](references/test-workflow.yml) — CI pipeline
- [publish-workflow.yml](references/publish-workflow.yml) — tag-driven release pipeline
- [changelog-template.md](references/changelog-template.md) — Keep a Changelog format the pipeline parses
