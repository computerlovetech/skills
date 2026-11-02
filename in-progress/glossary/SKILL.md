---
name: glossary
description: Keep and use a project's GLOSSARY.md — its shared language. Use when starting work in a project that has a GLOSSARY.md, when naming domain concepts in code, specs, issues or tests, when terms are fuzzy, overloaded or conflicting, or when a term is agreed and should be written down.
---

# Glossary

A project's `GLOSSARY.md` holds its shared language: one word per concept, used the same way by people, agents, specs, code and tests.

## Where it lives

- **Single context** (most projects): one `GLOSSARY.md` at the project root.
- **Several contexts**: a root `GLOSSARY-MAP.md` lists each context's `GLOSSARY.md` and how the contexts relate. Pick the glossary the topic belongs to; ask if unclear.
- **None yet**: create it when the first term is agreed, never upfront.

## Use it

- Read the relevant glossary before exploring or changing an area.
- Name things with glossary terms in discussion, specs, issues, code and tests. Never use a word listed under _Avoid_.
- A concept with no term is a signal: either you are inventing language the project doesn't use (reconsider), or there is a real gap (propose a term).

## Sharpen it

- **Challenge conflicts at once:** "The glossary defines a Loan as X, but you seem to mean Y. Which is it?"
- **Resolve fuzzy words:** when a word is vague or overloaded, propose one precise term.
- **Test with scenarios:** invent edge cases that force the boundary between two concepts.
- **Check the code:** if the code contradicts a stated meaning, say so.

Update `GLOSSARY.md` as soon as a term is agreed. Don't save terms up for later.

## File format

`GLOSSARY.md` has exactly this structure:

1. `# {Context name}`: one H1, the name of the context.
2. An intro of one or two sentences: what the context is and why it exists.
3. `## Language`: the only H2.
4. Entries, optionally grouped under `### {Group}` subheadings once clusters emerge. Without groups, entries sit directly under `## Language`.

Each entry is three lines, followed by a blank line:

```md
**{Term}**:
{Definition: one or two sentences saying what it is, not what it does.}
_Avoid_: {synonym}, {synonym}
```

- **Term**: bold, singular, capitalised as in prose, followed by a colon outside the bold.
- **Definition**: plain text on the next line. It may name other glossary terms, capitalised.
- **Avoid**: optional. A comma-separated list of rejected synonyms. Omit the line when there are none.
- Order entries so a term is defined before other definitions lean on it; otherwise alphabetically.

### Example

```md
# Lending

Lending covers how members borrow, return and reserve physical items from the library.

## Language

### Members

**Member**:
A person registered with the library who may borrow Items.
_Avoid_: User, customer, patron

### Borrowing

**Item**:
A single physical copy that can be lent out.
_Avoid_: Book, copy, title

**Loan**:
A Member's possession of an Item from checkout until return.
_Avoid_: Rental, borrowing

**Reservation**:
A Member's claim on the next available Item of a title.
_Avoid_: Hold, booking
```

### Multi-context map

`GLOSSARY-MAP.md` lists contexts, then relationships:

```md
# Glossary map

## Contexts

- [Lending](./lending/GLOSSARY.md): borrowing, returning and reserving items
- [Catalogue](./catalogue/GLOSSARY.md): describing and finding titles

## Relationships

- **Catalogue → Lending**: a Lending Item is one physical copy of a Catalogue Title.
```

## What belongs

- **Domain terms only.** No general programming concepts (timeouts, retries, caches), even if the project uses them heavily.
- **No implementation.** No table names, endpoints, specs, decisions or notes. A glossary is not a scratch pad.
- **Be opinionated.** Pick one word per concept and list the rest under _Avoid_.

## Credits

Adapted from the `domain-modeling` skill in Matt Pocock's [mattpocock/skills](https://github.com/mattpocock/skills), MIT License, Copyright (c) 2026 Matt Pocock. This version covers only the glossary, separate from decision records and issue-tracker setup.
