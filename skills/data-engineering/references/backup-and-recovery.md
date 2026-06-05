# Backup and Recovery

## RPO and RTO

| Term | Definition | How to set |
|------|------------|------------|
| **RPO** (Recovery Point Objective) | Maximum acceptable data loss in time | How much data can you afford to lose? 1 hour? 1 day? 1 week? |
| **RTO** (Recovery Time Objective) | Maximum acceptable downtime | How long can the system be unavailable? 5 minutes? 1 hour? 1 day? |

## Backup Strategies by Data Store Type

### Relational Databases (PostgreSQL, MySQL)

| Method | RPO | RTO | Storage | Best for |
|--------|-----|-----|---------|----------|
| Logical dump (pg_dump) | Point-in-time | Slow for large DBs | Large (SQL text) | Small DBs, schema-only backups |
| Physical backup (pg_basebackup) | Point-in-time if WAL archived | Fast | Moderate + WAL | Production deployments |
| WAL archiving + PITR | Continuous (every WAL segment) | Fast (base + replay WAL) | Moderate + continuous WAL | Maximum data protection |
| Replica-based (standby) | Zero (async) or near-zero (sync) | Minutes (promote replica) | Full replica storage | HA + backup combined |

### Vector Databases (Milvus, Qdrant, Chroma)

| Method | Considerations |
|--------|---------------|
| Milvus backup | `milvus-backup` tool for collection-level backup. Backup index + data separately. Restore requires matching index type. |
| Qdrant snapshot | Built-in `POST /collections/{name}/snapshots`. Snapshot full collection. Restore creates new collection. |
| Chroma | `chroma export` for collection export. File-based storage can use filesystem snapshots. |
| General vector DB | Backup embedding dimension must match target. Index rebuild required after restore. Always verify row count and sample queries. |

### Graph Databases (Neo4j)

| Method | Command | Frequency |
|--------|---------|-----------|
| Online backup (Enterprise) | `neo4j-admin backup` | Daily |
| Dump (Cypher-based) | `neo4j-admin dump --database=neo4j --to=backup.dump` | Daily/weekly |
| Causal cluster | Built-in replication across cluster members | Continuous |
| Offline copy | Stop DB → copy data directory → restart | Maintenance windows only |

### Time-Series Databases (InfluxDB)

| Method | Notes |
|--------|-------|
| InfluxDB backup | `influx backup` CLI for bucket-level backup. Includes data + metadata. |
| Downsample + retain | For time-series, consider downsampled archives vs raw data retention. Raw data may not need point-in-time recovery if derivable from sources. |

### Embedded / File-Based (SQLite, DuckDB)

| Method | Best practice |
|--------|---------------|
| WAL mode | Enable WAL journaling for crash recovery |
| File copy (with checkpoint) | `PRAGMA wal_checkpoint(TRUNCATE);` then copy file |
| `.backup` command | `sqlite3 db.sqlite '.backup /backup/db.sqlite'` |
| Replication (SQLite) | Litestream, rqlite for continuous backup |

## Backup Testing Cadence

| Type | Frequency | What to verify |
|------|-----------|----------------|
| Automated restore test | Weekly | Restore from latest backup, run integrity checks |
| Full DR drill | Quarterly | Complete recovery from scratch, measure RTO |
| RPO validation | Monthly | Verify WAL/snapshot frequency meets RPO targets |
| Corruption check | Daily | `pg_amcheck`, `sqlite3 db.sqlite 'PRAGMA integrity_check'` |

## Recovery Plan Template

```
1. **Assess** — What failed? Data loss? Schema corruption? Infrastructure failure?
2. **Select backup** — Which backup to restore from (latest clean, T+1, T-1)?
3. **Restore** — Restore data to recovery environment
4. **Verify** — Run integrity checks, sample queries, row count validation
5. **Replay** — Apply WAL/logs to reach target point-in-time
6. **Cut over** — Point applications to restored instance
7. **Validate** — Application smoke test, data freshness check
8. **Communicate** — RTO met? Data loss within RPO? Root cause?
```
