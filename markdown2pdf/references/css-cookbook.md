# Print CSS cookbook

Small recipes for the WeasyPrint rendering pipeline used by `markdown2pdf`. Apply these in your override CSS (`--css` or `./.markdown2pdf/style.css`).

## Page size and margins

```css
@page {
  size: A4;              /* or: Letter, A5, "210mm 297mm" */
  margin: 22mm 20mm;     /* top/bottom  left/right */
}
```

Different first page:

```css
@page :first {
  margin-top: 40mm;      /* big title margin */
  @top-center { content: ""; }
}
```

## Page numbers and running header/footer

```css
@page {
  @bottom-right { content: counter(page) " / " counter(pages); }
  @top-left    { content: string(doc-title); font-size: 8pt; color: #888; }
}

/* Capture H1 text into the header */
h1 { string-set: doc-title content(); }
```

## Force and avoid page breaks

```css
h1, h2 { page-break-before: always; break-before: page; }  /* chapter-style */
h2, h3 { page-break-after: avoid;  break-after: avoid;  }  /* keep heading with next */
pre, table, figure, blockquote {
  page-break-inside: avoid;
  break-inside: avoid;
}
```

Force a break from Markdown:

```html
<div style="page-break-before: always"></div>
```

## Code blocks that don't overflow

```css
pre {
  white-space: pre-wrap;      /* wrap instead of overflow */
  word-wrap: break-word;
  overflow-wrap: anywhere;    /* break mid-token if needed */
  font-size: 9pt;             /* shrink if long shell lines are common */
}
```

Horizontal scroll is not an option in print — always wrap.

## Callouts / admonitions

`markdown-it-py` renders `> blockquote` as `<blockquote>`. Style it:

```css
blockquote {
  border-left: 3pt solid #e85a42;
  background: #faf6f4;
  padding: 0.6em 0.9em;
  font-style: italic;
}
```

For multi-type callouts (note/warning/tip), use class-tagged blockquotes in Markdown:

```markdown
<div class="callout warning">

**Warning.** Running this drops the table.

</div>
```

```css
.callout { padding: 0.7em 1em; border-radius: 4px; margin: 1em 0; }
.callout.warning { background: #fff7e0; border-left: 3pt solid #e0a000; }
.callout.note    { background: #eef4ff; border-left: 3pt solid #4070e0; }
```

## Tables that don't break ugly

```css
table { page-break-inside: avoid; break-inside: avoid; }
thead { display: table-header-group; }   /* repeat headers on each page */
tr    { page-break-inside: avoid; }
```

If a table is genuinely longer than a page, drop `page-break-inside: avoid` and keep `thead { display: table-header-group; }` so headers repeat.

## Fonts

Bundle `.ttf`/`.otf` files next to your CSS and register them:

```css
@font-face {
  font-family: "Inter";
  src: url("fonts/Inter-Regular.ttf") format("truetype");
  font-weight: 400;
}
@font-face {
  font-family: "Inter";
  src: url("fonts/Inter-Bold.ttf") format("truetype");
  font-weight: 700;
}

html { font-family: "Inter", sans-serif; }
```

Paths in the CSS are resolved relative to the CSS file.

## Colors and print considerations

- WeasyPrint honors full CSS color; no need to worry about CMYK for on-screen/web-print PDFs.
- If the user will physically print, use darker text (`#1a1a1e` or darker) and avoid light-gray body text — it washes out.
- `color-adjust: exact;` or `print-color-adjust: exact;` tells renderers to preserve backgrounds (e.g. code-block shading).

## Images

```css
img {
  max-width: 100%;
  height: auto;
  page-break-inside: avoid;
}
figure figcaption { font-size: 9pt; color: #666; margin-top: 0.3em; }
```

Image paths in Markdown are resolved relative to the Markdown file (WeasyPrint uses the file's dir as `base_url`).

## Debugging tips

- Run `scripts/render foo.md --dump-html` to inspect the intermediate HTML.
- Open the HTML in a browser and use devtools' print-preview (Cmd-P) — most WeasyPrint issues reproduce there.
- If something looks unstyled, check that your `@page` rules aren't being overridden by a later rule in the same CSS.
