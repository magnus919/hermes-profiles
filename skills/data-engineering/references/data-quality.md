# Data Quality Monitoring

## Quality Dimensions

| Dimension | What it measures | Example violation |
|-----------|-----------------|-------------------|
| **Completeness** | Are all required values present? | Null in a required field |
| **Uniqueness** | Are there duplicate records? | Same primary key appearing twice |
| **Consistency** | Are values coherent across systems? | Customer name differs between CRM and billing |
| **Accuracy** | Do values reflect reality? | Wrong currency code, stale address |
| **Timeliness** | Is data current enough? | Batch pipeline 4 hours behind schedule |
| **Validity** | Do values conform to expected format? | Email address missing `@` |
| **Integrity** | Are referential relationships intact? | Order references a deleted customer |

## Validation Rule Types

| Rule type | What it does | SQL example |
|-----------|-------------|-------------|
| Not null | Field must have a value | `COUNT(*) WHERE email IS NULL` |
| Uniqueness | No duplicate values | `COUNT(*) vs COUNT(DISTINCT id)` |
| Referential integrity | Foreign key exists | `LEFT JOIN WHERE fk IS NULL` |
| Accepted values | Field in allowed set | `WHERE status NOT IN ('active','inactive','pending')` |
| Range check | Value within bounds | `WHERE age < 0 OR age > 150` |
| Freshness | Data is recent enough | `WHERE MAX(updated_at) < NOW() - INTERVAL '1 day'` |
| Row count | Volume in expected range | `ABS(COUNT(*) - historical_avg) / historical_avg > threshold` |
| Distribution | Value distribution hasn't drifted | Compare histogram to historical baseline |

## Anomaly Detection Strategies

| Strategy | What it detects | Best for |
|----------|----------------|----------|
| Fixed threshold | Values outside absolute bounds | Age, price, quantity ranges |
| Statistical (z-score) | Values far from mean | Transaction amounts, latencies |
| Moving average | Trends over time | Daily active users, revenue |
| Seasonality-adjusted | Expected patterns by time | Hourly traffic, weekly sales |
| ML-based | Complex multi-dimensional anomalies | Fraud detection, system health |

## Deduplication Strategies

| Strategy | When to use | SQL pattern |
|----------|-------------|-------------|
| Exact dedup | Exact row duplicates | `DELETE USING ... WHERE ctid < (SELECT MAX(ctid) FROM ...)` |
| Key-based dedup | Same natural key, keep latest | `ROW_NUMBER() OVER (PARTITION BY id ORDER BY updated_at DESC) = 1` |
| Fuzzy dedup | Similar but not identical records | `pg_trgm` similarity, Levenshtein distance, ML matching |
| Merge/consolidate | Multiple records for same entity | Survive best values per field, create golden record |

## Pipeline Health Monitoring

| Signal | What to check | Action on failure |
|--------|---------------|-------------------|
| Pipeline freshness | Last successful run time | Alert if > expected interval * 2 |
| Row counts | Source vs target volume | Investigate if delta > 10% |
| Null rates | % null in critical fields | Alert if above threshold (configurable per field) |
| Duplicate rates | % duplicate keys | Investigate if > 0% on unique fields |
| Latency | Time from source event to target | Alert if exceeds SLA |
| Schema drift | Column count/type changes | Log and alert for review |
