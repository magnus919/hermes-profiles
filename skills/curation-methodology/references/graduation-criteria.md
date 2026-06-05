# Graduation Criteria

Notes and topics evolve through stages. This reference defines when to promote a note from one stage to the next.

## The Note Lifecycle

```
Ghost note → Stub → Active note → Mature note → (MoC or Archive)
```

### Ghost Note → Stub

A ghost note is a wikilink to a note that doesn't exist yet. Ghost notes are intentional — they signal future investment areas without creating empty files.

**Graduate to stub when:** The concept appears in 3+ independent sources or a molecule needs it as a `derived_from:` target.

A stub is a minimal note with frontmatter and a 1-2 sentence definition/summary. It exists so wikilinks resolve and the graph is complete. Stubs live in their natural folder (atoms, people, etc.) from creation.

### Stub → Active Note

**Graduate to active when:** There's enough content to write a substantive body — at least 3 claims that can be made about the concept, or a clear narrative.

An active note has:
- Complete frontmatter with all required fields
- A body with developed paragraphs, not just a definition
- 3+ outgoing wikilinks to related concepts
- At least 1 incoming backlink from a non-self note

### Active → Mature

**Graduate to mature when:**
- The note has 10+ incoming backlinks from notes beyond its immediate cluster
- The body has been revised at least once since creation
- Its claims have survived cross-referencing with new sources
- It's referenced in at least one alloy

## Topic → Map of Content (MoC)

Topics are a flat index in the topic tree. A MoC is a curated narrative that guides reading.

**Graduate to MoC when the topic has:**
- 10+ backlinks from notes across at least 3 different folders
- At least 2 molecules that substantially cover the topic
- A natural narrative structure emerges (these subtopics group into these themes)
- Someone reading the topic would benefit from a guided path rather than a flat list

### MoC Quality Standards

A good MoC:
- Opens with a paragraph explaining what this MoC covers and why it exists
- Organizes links into thematic groups with headings, not a flat list
- Highlights the most important/current notes at the top
- Includes a "Sources" section if there are foundational external references
- Is publishable (will be `publish: true`)

## When to Deprecate

Sometimes a note outlives its usefulness. Deprecation is different from deletion.

| Signal | Action |
|--------|--------|
| The note's claims have been superseded by newer research | Add a deprecation notice at the top: "This note may be outdated. See [[Newer Note]] for current findings." |
| The note was speculative and the speculation didn't pan out | Same treatment — deprecation notice, don't delete (the speculation path is still data) |
| The note is a duplicate | Merge into the canonical note, then redirect the duplicate with a wikilink-only stub |
| The note is factually wrong | Correct the error, don't delete. The original error + correction is valuable data |

## Never Delete

| Don't delete | Instead |
|-------------|---------|
| Notes with incoming backlinks | Update or deprecate, but preserve the reference chain |
| Notes that are part of a published article | Deprecate with notice — the published article still links here |
| Notes representing a person's stated position | Even if the position changed — the record of the original position is historical data |
| Notes documenting a process or decision | The decision context may be valuable later, even if the decision was wrong |
