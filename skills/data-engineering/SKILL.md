---
name: data-engineering
description: "Data engineering methodology — database operations (vector, relational, graph, time-series), ETL/ELT pipeline design (dbt patterns, incremental loading), SQL analytical patterns, data quality monitoring, schema migration, and storage infrastructure management. Grounded in operational patterns for production data systems."
version: 1.1.0
author: Hermes Agent community
license: MIT
metadata:
  hermes:
    tags: [data-engineering, etl, dbt, sql, database, graph-db, time-series, vector-db, migration, data-quality, storage, influxdb, neo4j]
    related_skills: [data-architect, data-scientist, platform-engineering]
---

# Data Engineering Methodology

Data engineering is the operational backbone of data-driven systems. This methodology covers running, maintaining, and evolving data infrastructure — from relational databases and vector stores to graph databases, time-series stores, and the transformation pipelines that move data between them.

## The Data Engineer's Domain

| You own | You don't own |
|---------|--------------|
| Database operations — schema management, indexing, backup/recovery, migration across relational, vector, graph, and time-series stores | Data modeling and schema design — that's the data architect |
| Data transformation pipelines — dbt models, ETL/ELT patterns, incremental loading, incremental strategies | Statistical analysis and experiments — that's the data scientist |
| Analytical SQL — window functions, CTEs, query optimization, execution plan analysis, star schema queries | Training infrastructure and model deployment — that's the ML engineer |
| Graph database operations — Neo4j data modeling, Cypher queries, graph algorithms, import/export | Application-level data access patterns — that's the developer |
| Time-series database operations — InfluxDB schema design, downsampling, retention policies, Telegraf | Infrastructure provisioning — that's the platform engineer |
| Data quality monitoring — integrity checks, deduplication, anomaly detection, freshness validation | Visual dashboard design — that's the analyst or UX designer |
| Storage infrastructure — capacity planning, performance tuning, archival strategies | 

## Reference Files

| Reference | When to load |
|-----------|-------------|
| `references/sql-analytical-patterns.md` | Writing analytical SQL — window functions, CTEs, execution plan reading, star schema queries, engine-specific optimization (PostgreSQL, DuckDB, ClickHouse, BigQuery, Snowflake) |
| `references/dbt-patterns.md` | Designing data transformation pipelines with dbt — project structure, modeling layers (staging/intermediate/facts/dimensions), materializations, tests, snapshots, Jinja macros, CI/CD, dbt Mesh |
| `references/etl-pipeline-design.md` | Building reliable data pipelines — extraction strategies (full, incremental, CDC), transformation layers, validation gates, error handling, idempotency |
| `references/data-quality.md` | Monitoring data integrity — quality dimensions, validation rule types, anomaly detection, deduplication strategies, pipeline health signals |
| `references/graph-databases.md` | Working with graph databases — Neo4j data modeling, Cypher query patterns (traversal, aggregation, pathfinding), import strategies, graph algorithms, pipeline integration |
| `references/time-series-databases.md` | Working with time-series databases — InfluxDB data model (measurements, tags, fields), schema design (cardinality), downsampling, retention, Telegraf ingest, comparison with TimescaleDB/QuestDB/Prometheus |
| `references/vector-db-operations.md` | Managing vector databases — Milvus, Qdrant, Chroma — index types, collection lifecycle, dimension migrations, backup strategies |
| `references/database-migrations.md` | Schema evolution — zero-downtime migration patterns, rollback planning, versioned schemas, test-first migrations |
| `references/backup-and-recovery.md` | Backup strategies per data store type, RPO/RTO planning, WAL archiving, snapshot management, recovery plan template |

## Core Principles

**Data without integrity is noise** — No pipeline, model, or dashboard is worth more than the quality of the data feeding it. Validate at every boundary.

**Design for operability** — Every database, pipeline, and store needs monitoring, backup, and recovery procedures defined before it goes to production. If you can't detect failure, you can't recover from it.

**Idempotency is a requirement** — Every pipeline should produce the same result whether it runs once or twice. Duplicate handling is not optional.

**Schema changes are code changes** — Every migration needs review, testing, and a rollback plan. Schema drift is technical debt with compounding interest.

**Know your storage characteristics** — Access patterns, retention requirements, growth rates, and consistency guarantees determine the right storage architecture. Choose based on data, not familiarity.
