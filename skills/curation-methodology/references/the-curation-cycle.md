# The Curation Cycle

Regular maintenance rhythms for the vault. The curator doesn't just react to new content — it proactively maintains the health of the knowledge graph.

## The Rhythms

### Per-Session — Before Starting New Work

1. **Load context.** Read the Molecular Notes MoC if you haven't this session. Orient to the philosophy.
2. **Check recent orphans.** Run `obsidian orphans` and check last 5 entries. Any that look like oversight, fix before creating new notes.
3. **Review the brief.** What are you curating today? New extractions? Cross-linking existing molecules? A maintenance cycle?

### Per-Session — After Creating New Notes

1. **Link check.** Every new note needs 3+ outgoing wikilinks. If it has fewer, add them.
2. **Backlink check.** Every new structural note (atom, molecule, alloy, person, company) needs at least one incoming backlink. If it has none, add a link from a related note.
3. **Topic check.** Every new note needs 2-5 topics from the topic tree. Verify they exist and are canonical.
4. **QA gate.** Run the post-creation QA checks from vault-note.

### Weekly

1. **Orphan sweep.** `grep -rL "\\[\\["` on new notes — find notes with zero outgoing wikilinks
2. **Ghost note census.** Which ghost notes appear most frequently? The top 3-5 are candidates for graduation to stub status.
3. **Freshness flag.** Check creation dates on notes referenced in this week's molecules. Anything > 12 months old should be noted.

### Monthly

1. **Full orphan scan.** Run across the entire Atoms, Molecules, and People directories. Document orphans by type (recent vs chronic).
2. **Topic density check.** For each topic with 10+ backlinks, assess whether it should graduate to a MoC.
3. **Cluster health.** Identify any star clusters (one central note with satellites that don't interlink). Add cross-edges.
4. **Alloy opportunity scan.** Cross-reference recently created molecules with existing molecules in different domains. Any cross-domain patterns that warrant an alloy?

### Quarterly

1. **Full graph health audit.** Load `references/graph-health.md` and run all four vital signs.
2. **Topic tree review.** Add new topics that have emerged. Merge topics that overlap. Deprecate unused ones.
3. **MoC graduation.** Promote topics that have reached the threshold.
4. **Deprecation sweep.** Flag notes > 18 months in fast-moving domains for review.
5. **Alloy gap analysis.** Which existing molecule pairs WOULD reveal a pattern if connected, but haven't been? This is the most valuable and most commonly skipped step.

## The Negative Space

The most important curation work is recognizing what's missing:

- **What topics have many atoms but no molecule?** The atoms are there, waiting to be synthesized.
- **What molecules cross domains but have no alloy?** A synthetic connection was spotted but never written.
- **What ghost notes keep appearing but never get created?** The graph is telling you what to write about.
- **What clusters are entirely disconnected from the rest of the vault?** A knowledge silo no one has bridged.

Document the negative space. Not every gap needs filling today, but undiscovered gaps can't be filled tomorrow.
