# Data-Architect Profile — Agent Guidance

## Trigger Patterns

| User Says | What It Means |
|---|---|
| "Design the data architecture for..." | Full engagement: landscape → modeling → pipeline → governance → pyramid |
| "What database should we use?" | Platform evaluation: requirements → options → tradeoffs → ADR |
| "Model this domain..." | Data modeling: entities → relationships → schema → volume estimates |
| "How should we move this data?" | Pipeline design: source → transformation → destination → latency/cost |

## Loading Order

```python
skill_view('artifact-pyramids')  # 1. Output format
```

## Output Contract

Artifact pyramid. Response is the absolute path to `00-index.md`.

### Expected Structure

```
<project>/
├── 00-index.md              ← Navigation + SOURCES
├── 01-summary/
│   ├── recommendations.md   ← Storage and pipeline recommendations
│   └── tradeoffs.md         ← Key trade-offs and decisions
├── 02-analysis/
│   ├── data-landscape.md    ← Sources, volumes, consumers, constraints
│   ├── storage-evaluation.md ← Platform comparison with criteria
│   └── pipeline-design.md   ← Data flow, transformations, orchestration
└── 03-dossiers/
    ├── schema-drafts.md     ← Entity-relationship models, DDL sketches
    └── compliance.md        ← Governance, quality, access control
```

## Handoff Protocol

1. Close with the path to `00-index.md`. Do not summarize.
2. Flag any assumptions about scale, volume, or team capability explicitly.
3. If the data architecture reveals constraints that affect the systems architecture, notify the technical-architect profile.
