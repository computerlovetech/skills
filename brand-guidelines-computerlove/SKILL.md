---
name: brand-guidelines-computerlove
description: Applies Computer Love's official brand colors and typography to any sort of artifact that may benefit from having Computer Love's look-and-feel. Use it when brand colors or style guidelines, visual formatting, or company design standards apply.
---

# Computer Love Brand Styling

## Overview

To access Computer Love's official brand identity and style resources, use this skill.

**Keywords**: branding, corporate identity, visual identity, post-processing, styling, brand colors, typography, Computer Love brand, visual formatting, visual design, AI engineering, agentic coding

## Brand Guidelines

### Colors

**Background Colors (Dark Theme):**

- Deep: `#0c0c10` - Primary dark background
- Surface: `#141418` - Card and section backgrounds
- Elevated: `#1c1c22` - Elevated surfaces and hover states
- Card: `#222228` - Card backgrounds

**Accent Colors:**

- Primary (Coral): `#e85a42` - Primary accent, CTAs, highlights
- Secondary (Gold): `#f0c060` - Secondary accent, credentials, stats
- Tertiary (Teal): `#4bc0a0` - Success states, feature icons
- Cool (Teal): `#4bb8b0` - Alternative teal accent

**Text Colors:**

- Primary: `#f0f0f2` - Main text on dark backgrounds
- Secondary: `#9898a8` - Supporting text, descriptions
- Muted: `#606070` - Subtle text, labels

**Semantic Colors:**

- Success: `#4bc0a0` - Positive states, checkmarks
- Warning: `#f0c060` - Warnings, attention
- Error: `#e85a42` - Errors, required indicators

### Typography

- **Headings/Display**: Syne (with system sans-serif fallback)
- **Body/Monospace**: Space Mono (with system monospace fallback)
- **Note**: Fonts should be pre-installed in your environment for best results

## Features

### Smart Font Application

- Applies Syne font to headings and display text (24pt and larger)
- Applies Space Mono font to body text and code
- Automatically falls back to system fonts if custom fonts unavailable
- Preserves readability across all systems

### Text Styling

- Headings (24pt+): Syne font, bold weight
- Body text: Space Mono font
- Smart color selection based on background
- Preserves text hierarchy and formatting

### Shape and Accent Colors

- Non-text shapes use accent colors
- Cycles through coral, gold, and teal accents
- Maintains visual interest while staying on-brand

## Technical Details

### Font Management

- Uses system-installed Syne and Space Mono fonts when available
- Provides automatic fallback to system sans-serif (headings) and monospace (body)
- No font installation required - works with existing system fonts
- For best results, pre-install Syne and Space Mono fonts in your environment

### Color Application

- Uses RGB color values for precise brand matching
- Applied via python-pptx's RGBColor class
- Maintains color fidelity across different systems

### CSS Variables Reference

```css
--bg-deep: #0c0c10;
--bg-surface: #141418;
--bg-elevated: #1c1c22;
--bg-card: #222228;
--accent-primary: #e85a42;
--accent-secondary: #f0c060;
--accent-tertiary: #4bc0a0;
--text-primary: #f0f0f2;
--text-secondary: #9898a8;
--text-muted: #606070;
--font-display: 'Syne', sans-serif;
--font-mono: 'Space Mono', monospace;
```
