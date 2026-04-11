---
name: making-presentations
description: >-
  Creates or extends static HTML slide decks under presentations/ using the
  shared iframe shell, slides.js manifest, and per-slide HTML. Use when the user
  asks to make, create, build, or add presentations, slide decks, slides, or
  HTML decks in this repository, or when they mention PRESENTATION_GUIDE or
  presentations/supply-chain-security as a template.
---

# Making HTML presentation decks

## First step

Read [presentations/PRESENTATION_GUIDE.md](../../../presentations/PRESENTATION_GUIDE.md) from the repository root. It defines architecture (shell + iframe + bridge), PDF export rules, CSS tokens, and when to inline scripts versus shared assets. Follow it for contracts and troubleshooting.

## Where things live

- **Shared (all decks):** `presentations/shared/styles.css`, `presentations/shared/deck.js`, `presentations/shared/slide-nav-bridge.js`
- **Deck-specific:** `presentations/<deck-id>/` — one folder per presentation topic
- **Export tooling:** `presentations/scripts/export-deck-pdf.mjs`, `presentations/package.json`

## Starting a new deck

1. Pick a **`<deck-id>`** (kebab-case folder name, e.g. `threat-modeling-101`).
2. Create `presentations/<deck-id>/`.
3. **Shell:** Add `index.html` by copying [presentations/supply-chain-security/index.html](../../../presentations/supply-chain-security/index.html). Keep paths `../shared/styles.css`, `../shared/deck.js`, co-located `slides.js`, and `<iframe id="slide-frame" src="slide-01.html" ...>`. Customize title, brand line, and keyboard hint text only as needed.
4. **Manifest:** Add `slides.js` that sets `window.DECK_SLIDES` to an ordered array of slide filenames **before** `deck.js` loads (see guide). Script order in `index.html`: `slides.js` then `../shared/deck.js`.
5. **Top bar indicator:** Match the number of `.dot` elements and the `1 / N` counter in `index.html` to the slide count (fullscreen dots are automatic; the bar is manual).
6. **Slides:** Add `slide-01.html`, `slide-02.html`, … with two-digit padding. Each file is a full HTML page: `<link href="../shared/styles.css">`, body contains `<div class="slide accent-cyan|red|lime|amber">` (required for layout and PDF capture), then `<script src="../shared/slide-nav-bridge.js"></script>` last.
7. **Optional:** Speaker notes or research notes as `NOTES.md` (or similar) inside `<deck-id>/`; data files or scripts in `<deck-id>/data/` or `<deck-id>/scripts/` as needed. Add `export:pdf:<deck-id>` to `presentations/package.json` if the user wants a one-command PDF.

## Organizing content

- **Outline first:** Decide slide order; filenames must match `^slide-\d+\.html$` for PDF export and should stay aligned with `DECK_SLIDES`.
- **Reuse layout:** Prefer existing classes from `shared/styles.css` (`.slide-label`, headings, `.subtitle`, `.card` / `.card-grid`, `.slide-list`, `.stat-row`, `.chart-card`, `.slide-footer`) instead of inventing new layout for every slide.
- **Scripts:** Put slide-specific chart or DOM logic inline or in a sibling `.js` next to that slide; keep `slide-nav-bridge.js` last. Promote to `shared/` only when the same logic is reused across slides or decks (see guide table).
- **Preview:** Serve the `presentations/` root with a static server so `../shared/` resolves; avoid relying on `file://` for the shell.

## Reference implementation

Use [presentations/supply-chain-security/](../../../presentations/supply-chain-security/) as the working template: `index.html`, `slides.js`, and representative `slide-01.html` through `slide-08.html` (including optional inline chart scripts on later slides).
