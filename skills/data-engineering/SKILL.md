---
name: data-engineering
description: "Data engineering methodology — database operations (vector, relational, graph), ETL pipeline design, schema migration patterns, data quality monitoring, and storage infrastructure management. Grounded in operational patterns for production data systems."
version: 1.0.0
author: Hermes Agent community
license: MIT
metadata:
  hermes:
    tags: [data-engineering, etl, database, vector-db, migration, data-quality, storage]
    related_skills: [data-architect, data-scientist, platform-engineering]
---

# Data Engineering Methodology

Data engineering is the operational backbone of data-driven systems. This methodology covers running, maintaining, and evolving data infrastructure — from vector databases and relational stores to ETL pipelines and quality monitoring.

## The Data Engineer's Domain

| You own | You don't own |
|---------|--------------|
| Database operations — schema management, indexing, backup/recovery, migration | Data modeling and schema design — that's the data architect |
| Vector database operations — collection lifecycle, index tuning, dimension migration | Statistical analysis and experiments — that's the data scientist |
| ETL/ELT pipeline design and maintenance — ingestion, transformation, validation, export | Training infrastructure and model deployment — that's the ML engineer |
| Data quality monitoring — integrity checks, deduplication, corruption detection | Application-level data access patterns — that's the developer |
| Storage infrastructure — capacity planning, performance tuning, archival strategies | Infrastructure provisioning — that's the platform engineer |

## Reference Files

| Reference | When to load |
|-----------|-------------|
| `references/vector-db-operations.md` | Managing vector databases — Milvus, Qdrant, Chroma — index types, collection lifecycle, dimension migrations, backup strategies |
| `references/database-migrations.md` | Schema evolution — zero-downtime migration patterns, rollback planning, versioned schemas, test-first migrations |
| `references/etl-pipeline-design.md` | Building reliable data pipelines — extraction strategies, transformation patterns, validation gates, error handling, idempotency |
| `references/data-quality.md` | Monitoring data integrity — validation rules, anomaly detection, deduplication strategies, corruption recovery |
| `references/backup-and-recovery.md` | Backup strategies, point-in-time recovery, disaster recovery planning, restoration testing |

## Core Principles

**Data without integrity is noise** — No pipeline, model, or dashboard is worth more than the quality of the data feeding it. Validate at every boundary.

**Design for operability** — Every database, pipeline, and store needs monitoring, backup, and recovery procedures defined before it goes to production. If you can't detect failure, you can't recover from it.

**Idempotency is a requirement** — Every pipeline should produce the same result whether it runs once or twice. Duplicate handling is not optional.

**Schema changes are code changes** — Every migration needs review, testing, and a rollback plan. Schema drift is technical debt with compounding interest.

**Know your storage characteristics** — Access patterns, retention requirements, growth rates, and consistency guarantees determine the right storage architecture. Choose based on data, not familiarity.
