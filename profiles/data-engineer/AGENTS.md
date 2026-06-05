# Data Engineer Profile — Agent Guidance

## Trigger Patterns

| User Says | What It Means |
|---|---|
| "Design a migration from X to Y" | Migration plan: source analysis → target schema → dual-write → cutover → verification |
| "This database is slow" | Performance investigation: query patterns, index analysis, resource utilization |
| "Set up a pipeline for X" | ETL pipeline design: source discovery → transformation → loading → monitoring |
| "Check data quality" | Data quality audit: integrity checks, deduplication, anomaly detection |
| "Back up this database" | Backup strategy: RPO/RTO definition, backup method selection, restoration testing |
| "Migrate this schema" | Schema migration: change analysis, migration script, rollback plan, test |

## Loading Order

```python
skill_view('artifact-pyramids')    # 1. Output format
skill_view('data-engineering')     # 2. Methodology
```

## Output Contract

Artifact pyramid. Response is the absolute path to `00-index.md`.
