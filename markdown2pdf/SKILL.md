---
name: markdown2pdf
description: Convert a Markdown file to a styled PDF and iterate on the design visually. Use when the user asks to render markdown as a PDF, style a PDF, produce a printable handout, or tune the look of a generated PDF. Ships a neutral default theme; pairs with any styling skill that provides a CSS file.
license: MIT
compatibility: Requires Python 3.10+ and `uv` on PATH. Rasterize step requires `poppler` (`pdftoppm`) — install with `brew install poppler` (macOS) or `apt-get install poppler-utils` (Debian/Ubuntu).
---

# markdown2pdf

Render a Markdown file to a styled PDF, then iterate on the design by reading the rasterized pages as images.

## When to use

Use this skill whenever the user asks to:
- Turn a Markdown file into a PDF
- Style or redesign a generated PDF
- Produce a printable handout, worksheet, or report from Markdown
- Review and refine the visual layout of a rendered document

## What this skill does and does not do

**Does:** Markdown → HTML (via `markdown-it-py`) → PDF (via WeasyPrint) with a single CSS file controlling all styling. Rasterizes the result so the agent can visually inspect pages.

**Does not:** Dictate visual design. Styling is fully decoupled — this skill ships a neutral default CSS and lets any styling skill, project config, or explicit flag override it.

## Styling contract

Styling is a single CSS file. Resolution order (first match wins):

1. `--css <path>` passed to `scripts/render`
2. `./.markdown2pdf/style.css` relative to the current working directory
3. `assets/default.css` bundled with this skill (neutral fallback)

Any other skill can plug in by producing or pointing at a CSS file. Brand skills should expose a path like `<their-skill>/assets/pdf.css` and instruct the user to pass it via `--css`.

## The loop

Run these steps. Do not skip the visual inspection — page breaks, code-block overflow, and callout styling often look wrong in the PDF even when the Markdown source looks fine.

1. **Render** the Markdown to PDF:
   ```
   scripts/render <file>.md [--css <path>] [-o <out.pdf>]
   ```
   Output: `<file>.pdf` (or the `-o` target) plus a printed `PDF:` / `CSS:` summary.

2. **Rasterize** the PDF to PNG pages:
   ```
   scripts/rasterize <file>.pdf
   ```
   Output: one PNG per page under `/tmp/pdf-preview/`. Each page's absolute path is printed on its own line.

3. **Read** every PNG with the Read tool and inspect the actual rendered layout. Check:
   - Page breaks land in sensible places (no orphaned headings, split code blocks, broken tables)
   - Long lines in code blocks wrap or fit the page width
   - Callouts, tables, and images are styled correctly
   - Headings, spacing, and hierarchy read clearly

4. **Iterate.** Edit either the Markdown (content/structure) or the CSS (visual design), then repeat from step 1. Keep iterating until the user approves.

## Quick reference

| What to change           | Where to edit                          |
| ------------------------ | -------------------------------------- |
| Content, order, wording  | The Markdown file                      |
| Fonts, colors, spacing   | The CSS file (`--css` or project-local)|
| Page size, margins       | `@page { size: ...; margin: ...; }` in CSS |
| Page breaks              | `page-break-before/after/inside` in CSS, or `<div style="page-break-before: always"></div>` in Markdown |

See `references/css-cookbook.md` for common print-CSS recipes (page breaks, avoiding splits, headers/footers, code-block overflow).

## Examples

Render with the default theme:
```
scripts/render report.md
```

Render with an explicit brand stylesheet from another skill:
```
scripts/render report.md --css ~/.claude/skills/brand-acme/assets/pdf.css
```

Render with a project-local override (automatic, no flag needed):
```
# project has ./.markdown2pdf/style.css committed
scripts/render report.md
```

Debug by dumping the intermediate HTML:
```
scripts/render report.md --dump-html
```
