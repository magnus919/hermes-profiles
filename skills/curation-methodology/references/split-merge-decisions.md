# Split vs. Merge Decisions

Notes drift over time. An atom that was perfectly narrow at creation may accumulate scope. Two molecules may overlap. This reference provides the decision framework for when to restructure.

## When to Split a Note

| Signal | Action |
|--------|--------|
| Atom summary contains "and" | Split into two atoms, each making one claim |
| Molecule passes 15KB without a clear structural reason | Sub-topics may want their own molecules with wikilinks from the parent |
| Topic MoC passes 5KB and covers distinct subtopics | Consider sub-MoCs or separate topic notes |
| Note has 30+ outgoing wikilinks | It's trying to be a directory. Create an index or split |
| Note covers two domains that don't share primary sources | Split — the connection between them may be weak |

### The Split Procedure

1. Create new note(s) with the narrower scope
2. Move relevant content from the original
3. Add wikilinks from the original to each new note
4. If the original was referenced by other notes, verify those references still make sense
5. Update the original's summary to reflect its new scope

## When to Merge Notes

| Signal | Action |
|--------|--------|
| Two atoms make the same claim with different phrasing | Merge into one, keep both sources in `derived_from:` |
| Molecule restates what its atoms already say without synthesis | Merge key claims into a stronger synthesis or delete the molecule if it adds nothing |
| Two atoms have overlapping claims that can't be separated | Merge — the boundary between them was artificial |
| A person has two notes under different names | Merge into the canonical name, redirect with a stub |
| A topic MoC and its topic note say the same thing | Merge into the MoC (it's the richer form) |

### The Merge Procedure

1. Determine canonical note — the one with more backlinks, more complete information, or better structure
2. Move all unique content from the retiring note into the canonical one
3. Update `derived_from:` to include both sources if applicable
4. Search for wikilinks to the retiring note and update them to point to the canonical note
5. Archive or delete the retiring note only after all references are updated

## What Never to Merge

| Don't merge | Because |
|-------------|---------|
| Atoms from different sources claiming the same thing | They may say the same thing for different reasons — that's a molecule, not a merge |
| A person and their company | These are different entities, even if closely associated |
| A mechanism and an application of it | The mechanism is an atom; the application is a molecule that references it |
| A primary source and a secondary analysis of it | Preserve the distinction between evidence and interpretation |

## What Never to Split

| Don't split | Because |
|-------------|---------|
| A note that's small but well-linked | Size doesn't warrant splitting if the scope is already narrow |
| A note that's part of a dense cluster | The cluster is doing the work — splitting removes context |
| A note that's intentionally synthetic | Some molecules are meant to cover a broad domain by design |
