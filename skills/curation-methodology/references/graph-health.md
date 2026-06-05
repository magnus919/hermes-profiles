# Graph Health

Diagnostics and maintenance for the knowledge graph. Run these checks periodically to prevent decay.

## The Four Vital Signs

### 1. Orphan Rate — Notes with zero incoming backlinks

Every note should have at least one incoming backlink (from a note other than itself). Orphans are disconnected from the graph.

| Orphan rate | Health |
|-------------|--------|
| < 5% of all notes | Healthy — mostly connected |
| 5-15% | Warning — some pockets of disconnected notes |
| > 15% | Action needed — a significant portion of the vault is isolated |

**Common orphan causes:**
- Recently created notes that haven't been linked yet (transient — resolve in the same session)
- Clippings without molecules extracting from them (expected — clippings are the exception)
- Stubs that never attracted connections (check if they're still needed)
- Notes whose synonyms created alternate names for the same concept (merge or redirect)

**Fix:** For each orphan, determine whether it needs:
- A wikilink from a related note (most common fix)
- A topic assignment (if it's untopiced, it won't appear in topic-based navigation)
- A merge into a canonical note (if it's a duplicate)
- Deprecation (if it's obsolete)

### 2. Dead-End Rate — Notes with zero outgoing links

A dead-end note goes nowhere. It's a terminal node.

| Dead-end rate | Health |
|---------------|--------|
| < 10% | Healthy |
| 10-20% | Moderate — many notes are self-contained |
| > 20% | Action needed — too many notes don't connect forward |

**Common dead-end causes:**
- Note was created as a stub and never developed
- Note makes claims without linking to the concepts in those claims
- Note references external sources by URL instead of linking to vault notes

**Fix:** For each dead end, add outgoing wikilinks to the key concepts, people, and technologies mentioned in the body.

### 3. Cluster Density

The vault should form clusters around topics, not one giant undifferentiated mass or thousands of isolated islands.

| Pattern | Health |
|---------|--------|
| Clear clusters around major topics with cross-cluster bridges | Healthy |
| One giant cluster (everything links to everything) | Noise — too many weak links |
| Many small disconnected clusters | Fragmentation — knowledge domains aren't integrating |
| Star clusters (one central note with many satellites that don't link to each other) | The central note is a bottleneck — satellites should also link among themselves |

**Fix for star clusters:** Add cross-edges between satellite notes. If they're all connected to [[Machine Learning]], they should also link to each other where relevant.

### 4. Freshness

Older notes should still be accurate. Stale notes are worse than missing notes — they actively mislead.

| Age | Action |
|-----|--------|
| < 6 months | Current — no action needed |
| 6-12 months | Review for accuracy on a sample basis |
| 12-24 months | Check if the domain has changed significantly; add a "last reviewed" date |
| > 24 months | Flag for full review, especially in fast-moving domains |

## The Maintenance Cycle

### Daily (passive)
- Notes created in the current session get a quick link check: do they connect to the graph?

### Weekly (active)
- Run orphan check on this week's new notes
- Run dead-end check on this week's new notes
- Fix any issues found

### Monthly (deep)
- Full orphan scan across the entire vault
- Full dead-end scan
- Check for topic density — any ghost notes that have reached graduation threshold?
- Check for cluster anomalies — any isolated groups forming?

### Quarterly (strategic)
- Full graph health audit (all four vital signs)
- Topic tree review — any new topics needed? Any topics that should merge?
- MoC graduation review — which topics have reached 10+ backlinks?
- Deprecation sweep — which notes need freshness updates?
- Alloy gap analysis — which molecule pairs would benefit from a cross-domain alloy?

## Diagnostics Script

```
assets/graph-diagnostics.sh
```
