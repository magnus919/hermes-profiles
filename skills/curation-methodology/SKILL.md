---
name: curation-methodology
description: "Knowledge curation methodology for the knowledge vault — atomic note principles, cross-linking heuristics, split/merge decisions, graph health diagnostics, and the curation cycle. Grounded in Zettelkasten and Molecular Notes philosophy."
version: 1.0.0
author: Hermes Agent community
license: MIT
metadata:
  hermes:
    tags: [curation, knowledge-management, vault, zettelkasten, molecular-notes, graph-health]
    related_skills: [vault-note, vault-consistency, vault-synthesis, alloy-scribe, knowledge-graph-query]
---

# Curation Methodology

The curator is the vault's gardener. You don't extract from sources — the researcher does that. You don't produce content — the writer does that. You maintain the health of the knowledge graph: connections, structure, emergence, and decay.

Load the Molecular Notes topic MoC (`[[Molecular Notes]]`) before any curation session for philosophical grounding.

## The Curator's Domain

| You own | You don't own |
|---------|--------------|
| Graph structure — connections, topology, cluster health | Source extraction — that's the researcher |
| Note lifecycle — creation, promotion, deprecation | First draft content — that's the writer |
| Cross-linking — finding and making connections | Original analysis — that's the alloy |
| Topic evolution — ghost notes to MoCs | Factual claims — those belong to the source |
| Graph diagnostics — orphans, dead ends, density | |

## Reference Files

| Reference | When to load |
|-----------|-------------|
| `references/atomic-note-principles.md` | You need to decide what deserves its own atom, or whether a note is too broad or too narrow |
| `references/cross-linking-heuristics.md` | You need to decide whether two notes should be linked — and which link type to use |
| `references/split-merge-decisions.md` | A note has grown too large, or two notes overlap too much — when to split, when to merge |
| `references/graduation-criteria.md` | A ghost note has accumulated enough backlinks — is it time to promote it? A topic is getting dense — is it time for a MoC? |
| `references/graph-health.md` | You're running a maintenance cycle — diagnostics, orphans, dead ends, stale notes |
| `references/the-curation-cycle.md` | Regular maintenance patterns — daily, weekly, quarterly rhythms |

## Assets

| Asset | What it produces |
|-------|-----------------|
| `assets/graph-diagnostics.sh` | Run diagnostics on the vault to identify orphans, dead ends, and cluster health |

## The First Principle

A note's value is not what it says — it's what it connects to. An isolated atom, however brilliant, is a dead node. A mediocre atom linked into a dense cluster of related ideas is more valuable than a brilliant one sitting alone. The curator's job is to maximize connections without creating noise.
