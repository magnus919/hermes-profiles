# Data Engineer Profile — Agent Guidance

## Trigger Patterns

| User Says | What It Means |
|---|---|
| "Design a migration from X to Y" | Migration plan: source analysis → target schema → dual-write → cutover → verification |
| "This database is slow" | Performance investigation: query patterns, index analysis, resource utilization |
| "Set up a pipeline for X" | ETL/ELT pipeline design: source discovery → transformation (dbt recommended) → loading → monitoring |
| "Build a dbt project" | dBT project scaffold: model layers (staging/intermediate/facts/dimensions), sources, tests, documentation, CI/CD |
| "Model this with dbt" | dBT model design: materialization selection, incremental strategy, Jinja macros, package usage |
| "Design a Neo4j graph model" | Graph data modeling: node/relationship design, Cypher queries, import strategy |
| "Query this graph with Cypher" | Cypher optimization: traversal patterns, index usage, execution plan |
| "Set up InfluxDB for X" | Time-series architecture: measurement schema, tag design, retention, Telegraf config |
| "Write analytical SQL for X" | SQL pattern: window functions, CTEs, star schema queries, optimization |
| "Check data quality" | Data quality audit: integrity checks, deduplication, anomaly detection, freshness |
| "Back up this database" | Backup strategy: RPO/RTO definition, per-store method selection, restoration testing |
| "Migrate this schema" | Schema migration: change analysis, migration script, rollback plan, test |

## Loading Order

```python
skill_view('artifact-pyramids')    # 1. Output format
skill_view('data-engineering')     # 2. Methodology
```

## Output Contract

Artifact pyramid. Response is the absolute path to `00-index.md`.
