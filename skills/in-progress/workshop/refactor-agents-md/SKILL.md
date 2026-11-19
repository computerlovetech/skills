---
name: refactor-agents-md
description: Refactor an AGENTS.md longer than 100 lines.
---

Keep repo-wide instructions in AGENTS.md. Create wiki/ if missing. Move detailed guidance into Markdown pages grouped by domain, preserving each instruction’s meaning. In AGENTS.md, link once to wiki/index.md and say when to consult it.

Give every wiki folder an index.md listing only its own Markdown pages and its immediate child indexes. Follow the relevant links one level at a time.

```text
AGENTS.md
wiki/
├── index.md
├── guidelines.md
└── billing/
    ├── index.md
    ├── invoicing.md
    └── refunds/
        ├── index.md
        └── eligibility.md
```

`wiki/index.md`

```markdown
- [Guidelines](guidelines.md)
- [Billing](billing/index.md)
```

`wiki/billing/index.md`

```markdown
- [Invoicing](invoicing.md)
- [Refunds](refunds/index.md)
```
