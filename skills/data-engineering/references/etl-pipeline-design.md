# ETL/ELT Pipeline Design

## ETL vs ELT

| Approach | Transform location | When to use | Tools |
|----------|-------------------|-------------|-------|
| ETL (Extract, Transform, Load) | Staging server before load | Strict schema enforcement, legacy systems | Custom scripts, Spark, Python |
| ELT (Extract, Load, Transform) | Target database after load | Cloud data warehouses, modern stacks | dbt, BigQuery, Snowflake |

Modern data engineering overwhelmingly favors ELT. The data warehouse is the transformation engine — load raw data first, then transform with SQL.

## Pipeline Architecture Patterns

| Pattern | Latency | Complexity | Best for |
|---------|---------|------------|----------|
| Batch (scheduled) | Hours/days | Low | Reporting, BI, historical analysis |
| Micro-batch (frequent) | Minutes | Medium | Near-real-time dashboards, ML features |
| Streaming (continuous) | Seconds | High | Real-time alerts, fraud detection, monitoring |
| Lambda (batch + streaming) | Mixed | High | Systems needing both real-time and historical |
| Delta (unified batch/stream) | Mixed | Medium | Lakehouse architectures (Delta Lake, Iceberg) |

## Extraction Strategies

| Strategy | Mechanism | Freshness | Load on source |
|----------|-----------|-----------|----------------|
| Full refresh | `SELECT * FROM source` | Per schedule | High — reads everything |
| Incremental (watermark) | `WHERE updated_at > last_max` | Minutes | Low — only new/changed rows |
| CDC (change data capture) | Binlog/WAL replication | Real-time | Minimal — reads transaction log |
| Snapshot diff | Compare periodic snapshots | Hours | Medium — stores full snapshots |
| API polling | Paginated API calls | Configurable | Varies — respects rate limits |

## Transformation Layers (dbt-style)

```
Raw (source) → Staging → Intermediate → Marts (facts/dimensions)
```

| Layer | Purpose | Materialization | Idempotent |
|-------|---------|-----------------|------------|
| **Staging** | Clean, type, rename, deduplicate source data | View or ephemeral | Yes — always full-refresh safe |
| **Intermediate** | Business logic, joins, aggregations, pivots | Ephemeral or table | Yes — recomputable from staging |
| **Facts** | Measurable business events | Table or incremental | Yes — idempotent merge/upsert |
| **Dimensions** | Descriptive business entities | Table or slowly-changing | Yes — SCD Type 2 tracked |

## Incremental Load Patterns

### Watermark Pattern
```sql
-- Pseudocode pattern
SELECT * FROM source_table
WHERE updated_at > (
    SELECT MAX(updated_at) FROM target_table
);
```

### Merge/Upsert Pattern
```sql
-- PostgreSQL
INSERT INTO target (id, value, updated_at)
SELECT id, value, updated_at FROM source
ON CONFLICT (id) DO UPDATE
SET value = EXCLUDED.value,
    updated_at = EXCLUDED.updated_at;
```

### Snapshot Pattern (Full Replace)
```sql
-- For small dimensions: truncate and reload
TRUNCATE TABLE dim_small;
INSERT INTO dim_small SELECT * FROM source;
```

## Validation Gates

Every pipeline stage should validate:

| Gate | What it catches | Implementation |
|------|-----------------|----------------|
| Schema validation | Column count, type mismatch | Compare source schema to expected |
| Null check | Required field missing | `HAVING COUNT(*) = SUM(CASE WHEN col IS NULL THEN 1 ELSE 0 END)` |
| Row count | Missing data, truncation | Compare source row count to target row count |
| Uniqueness | Duplicate records | `COUNT(*) vs COUNT(DISTINCT pk)` |
| Freshness | Stale data pipeline | Timestamp threshold check |
| Distribution | Data quality drift | Min/max/avg comparison to historical |

## Error Handling

| Error type | Strategy | Example |
|------------|----------|---------|
| Transient (network, timeout) | Retry with exponential backoff | 3 retries, 30s/60s/120s intervals |
| Data quality (null key, type error) | Reject to dead letter queue, alert | Log bad rows, continue pipeline |
| Schema drift (new column) | Alert, optionally adapt | Detect, log, notify, proceed with null |
| Catastrophic (source down) | Halt pipeline, alert, wait for manual recovery | Preserve pipeline state for resume |
