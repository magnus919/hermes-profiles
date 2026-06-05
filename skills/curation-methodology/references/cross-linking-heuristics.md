# Cross-Linking Heuristics

A note's value is what it connects to. But not every potential connection is worth making. This reference helps decide when to link, what kind of link to use, and when not to link.

## The Three Link Types

| Link type | Where | What it means | Strength |
|-----------|-------|---------------|----------|
| **Wikilink in body** | Prose of any note | "These two concepts are related in a specific, explainable way" | Strong — the author explicitly connected them |
| **Related:** (frontmatter) | Frontmatter of any note | "Someone reading this note would also want to read this other note" | Medium — contextual recommendation |
| **Atoms:** (frontmatter) | Molecule frontmatter | "This molecule is composed of these atomic claims" | Compositional — defines the graph's structure |
| **Molecules:** (frontmatter) | Alloy frontmatter | "This alloy synthesizes across these molecules" | Compositional — multi-domain synthesis |
| **Derived_from:** (frontmatter) | Atom frontmatter | "This atom was extracted from this source" | Provenance — links claim to evidence |

## When to Link in Body Text

**Default: link.** The graph value of a note comes from its connections; missed wikilinks are missed connections forever. When in doubt, link it.

**Always link:**
- Researchers, executives, authors, public figures on first mention
- Companies, institutions, universities
- Central technical concepts — the subject of the sentence
- Named events, conferences, protocols
- Products, frameworks, languages
- Books, papers, named studies when referenced as sources
- Geographic places when their identity matters to the context

**Skip linking:**
- Generic terms used in their generic sense ("software," "the company")
- Pronouns and referential phrases ("this approach," "their findings")
- Concepts so abstract they have no plausible note ("the idea," "reality")
- Second and subsequent mentions of the same link in the same note

## The Two-Hop Rule

A wikilink should never require more than two hops to reach foundational evidence. If a reader follows a link from a MoC to a molecule, then to an atom, the atom should contain the claim itself — not another wikilink to a clipping.

```
MoC → Molecule → Atom → Claim ✓
MoC → Molecule → Atom → Clipping → Claim ✗ (three hops to evidence)
```

When you find three-hop chains, the middle note needs to incorporate the claim, not just reference it.

## When NOT to Link

| Don't link | Because |
|------------|---------|
| Every instance of the same term | First mention only. Subsequent mentions are noise. |
| Concepts that everyone already understands | "The network layer" in a networking article doesn't need a link to [[Network Layer]] |
| A link to a note that doesn't add information | If the target note says nothing the source doesn't already imply, the link adds noise, not signal |
| Circular links | Atom A links to Atom B which links to Atom A. Break the cycle — one direction only. |

## The Density Sweet Spot

A healthy note has between 3 and 12 outgoing wikilinks in its body.

| Density | Signal |
|---------|--------|
| 0 links | Dead end — the note goes nowhere. Probably incomplete. |
| 1-2 links | Thin — the note connects to almost nothing |
| 3-12 links | Healthy — well-connected to the graph |
| 12+ links | Dense — may be trying to do too much. Consider splitting. |
| 30+ links | Wiki page, not a note. Should be a MoC or broken into molecules. |

## Topics as NEAR-Connections

The `topics:` frontmatter field creates implicit NEAR-clustering. Two notes that share a topic are in the same semantic neighborhood even if they don't directly link. This is weaker than a direct wikilink but wider — it tells the graph traversal that these notes are related by domain.

**When to add a topic link:** Every note should have 2-5 topics. These are pulled from the topic tree (`8 - Topics/_Topic Tree.md`). Topics should be canonical — use the exact topic name from the tree.
