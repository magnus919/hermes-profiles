# Data Engineering SQL & Relational Database Reference

**Purpose:** A thorough reference for data engineers covering analytical SQL patterns,
ETL/ELT patterns, query performance, data modeling, testing, and engine comparisons.
This is methodology-level guidance — not a tutorial, but a field manual.

---

## Table of Contents

1. [Analytical SQL Patterns](#1-analytical-sql-patterns)
2. [ETL/ELT SQL Patterns](#2-etlelt-sql-patterns)
3. [Query Performance Patterns](#3-query-performance-patterns)
4. [Data Modeling for Analytics](#4-data-modeling-for-analytics)
5. [SQL Testing & Validation Patterns](#5-sql-testing--validation-patterns)
6. [Analytical SQL Engine Comparison](#6-analytical-sql-engine-comparison)

---

## 1. Analytical SQL Patterns

### 1.1 Window Functions

Window functions perform calculations across a set of rows related to the current
row, without collapsing rows into a single output (unlike GROUP BY).

**Syntax anatomy:**
```sql
<function>() OVER (
  [PARTITION BY col1, col2, ...]
  [ORDER BY col1 [ASC|DESC], ...]
  [frame_spec]
)
```

**Frame specifications (critical for correctness):**
| Clause | Behavior |
|---|---|
| `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` | Physical — counts actual rows regardless of value ties |
| `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` | Logical — includes peers (rows with same ORDER BY value) |
| `ROWS BETWEEN n PRECEDING AND n FOLLOWING` | Sliding physical window of 2n+1 rows |
| `RANGE BETWEEN INTERVAL '7' DAY PRECEDING AND CURRENT ROW` | Time-based frame (Date/Time ORDER BY) |
| `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING` | Entire partition (like SUM with no frame) |

**Window function families:**

| Family | Functions | Use Case |
|---|---|---|
| **Ranking** | `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`, `NTILE(n)` | Dedup, pagination, top-N-per-group |
| **Value** | `LAG(col, n)`, `LEAD(col, n)`, `FIRST_VALUE()`, `LAST_VALUE()`, `NTH_VALUE()` | Time-series shifts, YoY comparison, filling gaps |
| **Aggregate** | `SUM()`, `AVG()`, `COUNT()`, `MIN()`, `MAX()` over window | Running totals, moving averages, cumulative stats |
| **Distribution** | `PERCENT_RANK()`, `CUME_DIST()`, `PERCENTILE_CONT()`, `PERCENTILE_DISC()` | Statistical distributions, median calculation |

**Running total (cumulative sum):**
```sql
SELECT
  order_date,
  amount,
  SUM(amount) OVER (ORDER BY order_date
                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total
FROM orders;
```

**Moving average (7-day):**
```sql
SELECT
  date,
  revenue,
  AVG(revenue) OVER (ORDER BY date
                     ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS ma_7d
FROM daily_revenue;
```

**First value in partition (fill-forward):**
```sql
SELECT
  user_id,
  login_date,
  FIRST_VALUE(login_date) OVER (PARTITION BY user_id
                                 ORDER BY login_date
                                 ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS first_login
FROM user_logins;
```

**Deduplication with ROW_NUMBER:**
```sql
WITH ranked AS (
  SELECT *,
    ROW_NUMBER() OVER (PARTITION BY id ORDER BY updated_at DESC) AS rn
  FROM raw_table
)
SELECT * FROM ranked WHERE rn = 1;
```

---

### 1.2 Common Table Expressions (CTEs)

CTEs improve query readability, enable recursion, and allow stepwise logic.

**Non-recursive CTE:**
```sql
WITH monthly_sales AS (
  SELECT
    DATE_TRUNC('month', order_date) AS month,
    SUM(amount) AS total
  FROM orders
  WHERE order_date >= '2024-01-01'
  GROUP BY 1
),
ranked_months AS (
  SELECT *,
    RANK() OVER (ORDER BY total DESC) AS rank
  FROM monthly_sales
)
SELECT * FROM ranked_months WHERE rank <= 5;
```

**Recursive CTE (hierarchy traversal — org chart, bill of materials):**
```sql
WITH RECURSIVE org_tree AS (
  -- Anchor: top-level
  SELECT id, name, manager_id, 1 AS level
  FROM employees
  WHERE manager_id IS NULL

  UNION ALL

  -- Recursive step
  SELECT e.id, e.name, e.manager_id, t.level + 1
  FROM employees e
  JOIN org_tree t ON e.manager_id = t.id
)
SELECT * FROM org_tree;
```

**CTE vs subquery guidance:**
- Use CTEs for readability when the same subquery is referenced multiple times.
- CTEs are **optimization fences** in some engines (PostgreSQL materializes them by
  default; BigQuery inlines them). Test performance with real data.
- In Snowflake and DuckDB, CTEs are usually inlined unless forced with materialization hints.

---

### 1.3 Pivot / Unpivot

**Pivot (rows to columns):**

Most engines provide a `PIVOT` or `CROSSTAB` function. The fallback is conditional aggregation.

*Explicit PIVOT (Snowflake, BigQuery, SQL Server):*
```sql
SELECT *
FROM sales
PIVOT (
  SUM(amount)
  FOR category IN ('Electronics', 'Clothing', 'Food')
) AS p;
```

*Conditional aggregation fallback (works everywhere):*
```sql
SELECT
  region,
  SUM(CASE WHEN category = 'Electronics' THEN amount ELSE 0 END) AS electronics,
  SUM(CASE WHEN category = 'Clothing'    THEN amount ELSE 0 END) AS clothing,
  SUM(CASE WHEN category = 'Food'        THEN amount ELSE 0 END) AS food
FROM sales
GROUP BY region;
```

**Unpivot (columns to rows):**

*Explicit UNPIVOT (Snowflake, BigQuery, SQL Server):*
```sql
SELECT region, category, amount
FROM regional_sales
UNPIVOT (
  amount FOR category IN (electronics, clothing, food)
);
```

*CROSS JOIN LATERAL / UNION ALL fallback:*
```sql
SELECT region, 'electronics' AS category, electronics AS amount FROM regional_sales
UNION ALL
SELECT region, 'clothing'    AS category, clothing    AS amount FROM regional_sales
UNION ALL
SELECT region, 'food'        AS category, food        AS amount FROM regional_sales;
```

---

### 1.4 Rolling Aggregates

Rolling aggregates extend window functions for time-series analytics.

**Year-over-year comparison:**
```sql
SELECT
  month,
  revenue,
  LAG(revenue, 12) OVER (ORDER BY month) AS revenue_12m_ago,
  (revenue - LAG(revenue, 12) OVER (ORDER BY month))
    / NULLIF(LAG(revenue, 12) OVER (ORDER BY month), 0) * 100 AS yoy_pct
FROM monthly_revenue;
```

**Rolling 30-day sum (period-to-date-style):**
```sql
SELECT
  date,
  amount,
  SUM(amount) OVER (ORDER BY date
                    RANGE BETWEEN INTERVAL '29' DAY PRECEDING AND CURRENT ROW) AS rolling_30d
FROM daily_data;
```

**Sessionized aggregates (reset per partition):**
```sql
SELECT
  user_id,
  event_time,
  SUM(value) OVER (PARTITION BY user_id
                   ORDER BY event_time
                   ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS session_running_total
FROM user_events;
```

---

### 1.5 Date/Time Bucketing

Bucketing dates into intervals is essential for rollups and time-series.

**DATE_TRUNC (standard in PostgreSQL, DuckDB, Snowflake, BigQuery):**
```sql
-- Bucket to hour, day, week, month, quarter, year
SELECT
  DATE_TRUNC('month', event_timestamp) AS bucket,
  COUNT(*) AS events
FROM events
GROUP BY 1
ORDER BY 1;
```

**Custom bucket sizes (DuckDB: `date_bin`):**
```sql
SELECT
  date_bin(INTERVAL '15 minutes', event_timestamp, TIMESTAMP '2024-01-01') AS bucket_15min,
  COUNT(*) AS events
FROM events
GROUP BY 1;
```

**ISO week and year extraction:**
```sql
SELECT
  EXTRACT(YEAR FROM order_date) AS yr,
  EXTRACT(WEEK FROM order_date) AS wk,
  SUM(amount) AS total
FROM orders
GROUP BY yr, wk;
```

**Fiscal calendar bucketing (when standard months don't fit):**
```sql
SELECT
  CASE
    WHEN EXTRACT(MONTH FROM order_date) >= 2 THEN EXTRACT(YEAR FROM order_date)
    ELSE EXTRACT(YEAR FROM order_date) - 1
  END AS fiscal_year,
  SUM(amount) AS total
FROM orders
GROUP BY fiscal_year;
```

**Period-over-period difference using DATE_TRUNC and LAG:**
```sql
WITH weekly AS (
  SELECT
    DATE_TRUNC('week', order_date) AS week,
    SUM(amount) AS revenue
  FROM orders
  GROUP BY 1
)
SELECT
  week,
  revenue,
  LAG(revenue) OVER (ORDER BY week) AS prev_week_rev,
  revenue - LAG(revenue) OVER (ORDER BY week) AS wow_change
FROM weekly;
```

---

## 2. ETL/ELT SQL Patterns

### 2.1 Incremental Loading

**Watermark / High-Water Mark pattern:**

Use a monotonically increasing column (timestamp, auto-increment ID) to track what
has already been loaded.

```sql
-- Extract: pull rows newer than the last watermark
INSERT INTO target_table (id, col1, col2, loaded_at)
SELECT id, col1, col2, CURRENT_TIMESTAMP
FROM source_table
WHERE updated_at > (SELECT MAX(loaded_at) FROM target_table);
```

**Last-modified pattern with checksum for changed detection:**
```sql
WITH source AS (
  SELECT id, MD5(col1 || col2) AS row_hash, updated_at
  FROM source_table
  WHERE updated_at > (SELECT MAX(watermark_ts) FROM load_watermarks WHERE table_name = 'target')
)
SELECT s.*
FROM source s
LEFT JOIN target_table t ON s.id = t.id
WHERE t.id IS NULL OR s.row_hash != t.row_hash;
```

**Best practices:**
- Store watermarks in a control table (`table_name`, `watermark_ts`, `row_count`, `run_id`).
- Use `BEGIN`/`COMMIT` to make extract-and-update-watermark atomic.
- Prefer timestamp columns that are indexed in the source.
- For append-only sources (event logs), use an auto-increment ID as the watermark.

---

### 2.2 Merge / Upsert (MERGE / INSERT ON CONFLICT)

**PostgreSQL (`INSERT ... ON CONFLICT DO UPDATE`):**
```sql
INSERT INTO target (id, col1, col2, updated_at)
VALUES (1, 'val1', 'val2', NOW())
ON CONFLICT (id) DO UPDATE SET
  col1 = EXCLUDED.col1,
  col2 = EXCLUDED.col2,
  updated_at = EXCLUDED.updated_at;
```

**Standard SQL MERGE (Snowflake, BigQuery, SQL Server, DuckDB):**
```sql
MERGE INTO target AS t
USING source AS s
  ON t.id = s.id
WHEN MATCHED AND (
  t.col1 != s.col1 OR t.col2 != s.col2 OR (t.col1 IS NULL AND s.col1 IS NOT NULL)
) THEN UPDATE SET
  col1 = s.col1,
  col2 = s.col2,
  updated_at = CURRENT_TIMESTAMP
WHEN NOT MATCHED THEN
  INSERT (id, col1, col2, created_at, updated_at)
  VALUES (s.id, s.col1, s.col2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
```

**BigQuery MERGE (with DML):**
```sql
MERGE INTO `project.dataset.target` AS t
USING `project.dataset.source` AS s
ON t.id = s.id
WHEN MATCHED THEN
  UPDATE SET col1 = s.col1, col2 = s.col2
WHEN NOT MATCHED THEN
  INSERT (id, col1, col2) VALUES (id, col1, col2);
```

**DuckDB MERGE (note: single UPDATE/DELETE per WHEN MATCHED):**
```sql
MERGE INTO target AS t
USING source AS s
ON t.id = s.id
WHEN MATCHED AND s._is_deleted THEN DELETE
WHEN MATCHED THEN UPDATE SET col1 = s.col1, col2 = s.col2
WHEN NOT MATCHED THEN INSERT (id, col1, col2) VALUES (s.id, s.col1, s.col2);
```

**Engine-specific notes:**
| Engine | Upsert Method | Notes |
|---|---|---|
| PostgreSQL | `INSERT ... ON CONFLICT DO UPDATE` | Also supports `DO NOTHING`; requires unique index |
| Snowflake | `MERGE` | Also supports `INSERT OVERWRITE` for tables |
| BigQuery | `MERGE` | Charges for all bytes processed, even if no rows change |
| DuckDB | `INSERT OR REPLACE` or `MERGE` | DuckDB v1.3+: `MERGE` with single action per clause |
| Redshift | `MERGE` (via `UPDATE`/`INSERT` or `MERGE` since RA3) | Older versions: separate UPDATE then INSERT |
| ClickHouse | `ReplacingMergeTree` engine or `ALTER TABLE DELETE` | ClickHouse is append-optimized; upserts are not idiomatic |

---

### 2.3 Change Data Capture (CDC) Patterns

**1. Debezium-style (log-based CDC):**
- Source database captures changes via transaction log (PostgreSQL WAL, MySQL binlog).
- Events streamed to Kafka -> consumed and written to staging tables.
- Target SQL: merge staged changes into the final table.

```sql
-- Staging table holds INSERT, UPDATE, DELETE events
WITH latest_changes AS (
  SELECT DISTINCT ON (id) id, col1, col2, op, change_ts
  FROM cdc_staging
  ORDER BY id, change_ts DESC
)
MERGE INTO target t
USING latest_changes s ON t.id = s.id
WHEN MATCHED AND s.op = 'DELETE' THEN DELETE
WHEN MATCHED AND s.op IN ('INSERT', 'UPDATE') THEN UPDATE SET col1 = s.col1, col2 = s.col2
WHEN NOT MATCHED AND s.op IN ('INSERT', 'UPDATE') THEN INSERT (id, col1, col2)
  VALUES (s.id, s.col1, s.col2);
```

**2. Audit-column CDC (watermark + last-modified):**
- Source table has `updated_at` and optionally a version column.
- Periodic poll queries `WHERE updated_at > last_watermark`.
- Works for sources that cannot stream logs.

**3. Trigger-based CDC (SQL Server, PostgreSQL):**
- Database triggers write changes to a change-tracking table.
- Downstream reads the change table and clears processed rows.

```sql
-- PostgreSQL trigger-captured changes
CREATE TABLE _audit_accounts (
  audit_id   BIGSERIAL PRIMARY KEY,
  op         TEXT,       -- 'INSERT', 'UPDATE', 'DELETE'
  old_row    JSONB,
  new_row    JSONB,
  changed_at TIMESTAMPTZ DEFAULT NOW()
);
```

**4. Snapshot-diff CDC:**
- Periodically snapshot the entire source table.
- Compare the new snapshot with the previous snapshot to find changes.
- Works for small reference tables; wasteful for large fact tables.

---

### 2.4 Full Refresh vs Incremental Decision Matrix

| Scenario | Strategy |
|---|---|
| Small dimension tables (< 10K rows) | Full refresh (simpler, idempotent) |
| Large fact tables (millions of rows) | Incremental with watermark |
| Append-only event streams | Incremental by ID or timestamp |
| Slow-changing reference data | Full refresh on schedule |
| Source has no reliable watermark column | Full refresh or snapshot-diff CDC |
| Source supports CDC (logical replication) | Stream-based CDC (lowest latency) |

---

## 3. Query Performance Patterns

### 3.1 Execution Plan Analysis

**Reading EXPLAIN output:**

Every plan is a tree of *nodes*. Each node has cost estimates and actuals (with ANALYZE).

```
Seq Scan on orders  (cost=0.00..1234.56 rows=56789 width=32)
  Filter: (amount > 100)
```

| Component | Meaning |
|---|---|
| `cost=0.00..1234.56` | Startup cost .. total cost (arbitrary units) |
| `rows=56789` | Estimated rows produced by this node |
| `width=32` | Average row width in bytes |
| `actual time=12.3..45.6` | (With EXPLAIN ANALYZE) actual timing in ms |

**Node types you'll see (PostgreSQL):**

| Node | Meaning | Usually okay? |
|---|---|---|
| `Seq Scan` | Full table scan | Yes for small tables, bad for large filtered queries |
| `Index Scan` | Single index lookup | Good for point queries |
| `Index Only Scan` | All needed data in index | Excellent (avoids heap fetch) |
| `Bitmap Heap Scan` + `Bitmap Index Scan` | Reads index, builds bitmap, then fetches pages | Good for medium-selectivity queries |
| `Nested Loop` | For each outer row, probe inner index | Good with small outer set |
| `Hash Join` | Build hash table on one side, probe with other | Good for medium-large joins |
| `Merge Join` | Sort both sides, merge | Good for pre-sorted data |
| `Sort` / `Incremental Sort` | Ordering operation | Expensive; avoid if possible |
| `Aggregate` (Hash/GroupAgg) | GROUP BY or aggregation | HashAgg is faster; GroupAgg requires sorted input |

**Red flags in execution plans:**
- Sequential scans on large tables (>1M rows) with selective filters (<1% of rows)
- Nested Loop joins where the outer input is large (tens of thousands+)
- Sort operations on unindexed columns driving GROUP BY or ORDER BY
- `rows` estimates far off from `actual rows` (sign of stale statistics)
- Spilling to disk (temp files) for sort/hash operations

**EXPLAIN ANALYZE checklist:**
```sql
-- 1. Check estimated vs actual row counts (accuracy)
-- 2. Check actual time (where is the most time spent?)
-- 3. Check for sequential scans on large tables
-- 4. Check for sorts that could use indexes
-- 5. Check for loops in Nested Loop (high loop count = bad)
EXPLAIN (ANALYZE, BUFFERS, TIMING) SELECT ...
```

---

### 3.2 Index Strategies for Analytical Queries

**Type comparison:**

| Index Type | Best For | Avoid When |
|---|---|---|
| **B-Tree** | Equality + range queries, primary keys, foreign keys | High-cardinality columns with wide values (text blobs) |
| **BRIN** (Block Range Index) | Large, append-only, naturally ordered tables (time-series, logs) | Randomly distributed data, high-update tables |
| **Hash Index** | Exact-equality lookups only | Anything with range/order |
| **GIN** (Generalized Inverted Index) | Array columns, full-text search, JSONB | Simple = lookups on scalar columns |
| **GiST** | Geometric/geospatial data, range overlap, full-text | General-purpose analytical queries |
| **Z-ordering** (Delta/BigQuery) | Multi-dimensional range queries on several columns | Single-column queries (use simple sort instead) |

**Analytical index patterns:**

*Covering index (index-only scans):*
```sql
-- Avoid heap fetches by including all needed columns
CREATE INDEX idx_sales_date_amount ON sales (sale_date) INCLUDE (amount, product_id);
```

*Partial index (filtered):*
```sql
-- Only index active records
CREATE INDEX idx_orders_active ON orders (order_date) WHERE status = 'active';
```

*Composite B-Tree for analytical filter patterns:*
```sql
-- Order columns by: equality -> range -> group/order
CREATE INDEX idx_sales_region_date ON sales (region, sale_date);
-- Supports: WHERE region = 'US' AND sale_date BETWEEN '2024-01-01' AND '2024-06-30'
```

*BRIN for time-series (low maintenance, tiny index):*
```sql
-- 10x smaller than B-Tree on ordered timestamps
CREATE INDEX idx_events_ts_brin ON events USING brin(created_at)
  WITH (pages_per_range = 32);
```

**Indexing anti-patterns for analytics:**
- Don't index every column — write throughput suffers.
- Don't index low-cardinality columns alone (e.g., `gender`) — full scan is faster.
- Don't use B-Tree on timestamp columns in append-only tables — use BRIN.
- Don't forget `VACUUM`/`ANALYZE` after bulk loads — stale stats cause bad plans.

---

### 3.3 Partitioning

**When to partition:**
- Table > 100 GB or > 100M rows
- Queries always filter by a partition key (e.g., `order_date`)
- Old data can be dropped by dropping partitions (time-series retention)
- Maintenance operations (VACUUM, index rebuild) can target individual partitions

**Partition strategies:**

| Strategy | Key | Use Case |
|---|---|---|
| **Range** | Date, timestamp | Time-series data, event logs |
| **List** | Region, status, category | Discrete value partitions |
| **Hash** | ID, customer_id | Even data distribution, parallelism |

**PostgreSQL range partitioning:**
```sql
CREATE TABLE orders (
  id BIGSERIAL,
  order_date DATE NOT NULL,
  amount NUMERIC
) PARTITION BY RANGE (order_date);

CREATE TABLE orders_2024_q1 PARTITION OF orders
  FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');
CREATE TABLE orders_2024_q2 PARTITION OF orders
  FOR VALUES FROM ('2024-04-01') TO ('2024-07-01');
```

**BigQuery partitioning (table creation):**
```sql
CREATE TABLE `project.dataset.orders`
PARTITION BY DATE(order_timestamp)
CLUSTER BY region, product_id
OPTIONS(require_partition_filter=true);
```

**Snowflake clustering (automatic):**
```sql
ALTER TABLE orders CLUSTER BY (order_date, region);
```

**Partition pruning verification:**
```sql
-- PostgreSQL: check for "Append" node showing only relevant partitions
EXPLAIN SELECT * FROM orders WHERE order_date = '2024-02-15';
```

**Key rules:**
- Aim for 100-500 partitions (too few = no benefit; too many = metadata overhead).
- Always filter queries by the partition key.
- Use partition pruning verification after implementation.
- Consider declarative partitioning over manual table inheritance.

---

### 3.4 Clustering (within-partition ordering)

Clustering physically co-locates rows with similar cluster-key values. This reduces
the amount of data scanned by filter/aggregation queries.

| Engine | Feature | Notes |
|---|---|---|
| BigQuery | `CLUSTER BY` | Automatic re-clustering; no maintenance |
| Snowflake | `CLUSTER BY` | Automatic, but reclustering costs credits |
| Redshift | `SORTKEY` compound/interleaved | Manual; re-sort with `VACUUM SORT ONLY` |
| DuckDB | `ORDER BY` within `CREATE TABLE AS` | Manual; use WITH clause or ordering |
| PostgreSQL | CLUSTER command | One-time reorder; not maintained automatically |

**Strategy:**
```sql
-- BigQuery
CREATE TABLE `project.dataset.orders`
PARTITION BY DATE(order_date)
CLUSTER BY customer_id, region;
```

```sql
-- Redshift
CREATE TABLE orders (
  id BIGINT,
  order_date DATE,
  customer_id BIGINT,
  region VARCHAR(50)
) SORTKEY (customer_id, order_date);
```

**Cluster key ordering rules:**
- High-cardinality filter columns first.
- Equality filter columns before range filter columns.
- Columns frequently used in GROUP BY or ORDER BY.
- Avoid columns that are monotonically increasing (like timestamps) as the
  *first* cluster key if the table is also partitioned by time — it adds no extra benefit.

---

### 3.5 Materialized Views

Materialized views pre-compute and store query results. They trade storage for
query speed.

**PostgreSQL materialized view:**
```sql
CREATE MATERIALIZED VIEW mv_monthly_sales AS
SELECT
  DATE_TRUNC('month', order_date) AS month,
  region,
  SUM(amount) AS total_sales,
  COUNT(*) AS order_count
FROM orders
GROUP BY 1, 2;

-- Refresh (blocking — table locked during refresh)
REFRESH MATERIALIZED VIEW mv_monthly_sales;

-- Concurrent refresh (non-blocking, requires unique index)
CREATE UNIQUE INDEX idx_mv_monthly_sales_key ON mv_monthly_sales (month, region);
REFRESH MATERIALIZED VIEW CONCURRENTLY mv_monthly_sales;
```

**BigQuery materialized views (auto-refreshed):**
```sql
CREATE MATERIALIZED VIEW `project.dataset.monthly_sales`
AS
SELECT
  DATE_TRUNC(order_date, MONTH) AS month,
  region,
  SUM(amount) AS total_sales
FROM `project.dataset.orders`
GROUP BY 1, 2;
```

**Snowflake materialized views (auto-maintained, credits incurred):**
```sql
CREATE MATERIALIZED VIEW mv_monthly_sales AS
SELECT
  DATE_TRUNC('month', order_date) AS month,
  region,
  SUM(amount) AS total_sales
FROM orders
GROUP BY 1, 2;
```

**When to use materialized views:**
- Slow-running aggregations that are queried frequently.
- Dashboard/report queries with known filter patterns.
- Pre-joined dimension+fact denormalizations.
- Data that changes infrequently (or you can tolerate stale data).

**When NOT to use materialized views:**
- Highly volatile data (refresh cost exceeds query savings).
- Ad-hoc query workloads with unpredictable filter patterns.
- Tables under 50M rows (incremental query is often fast enough).
- When the view depends on tables with complex streaming updates.

---

### 3.6 Sorting within Analytical Engines

| Engine | Default Physical Sort | Notes |
|---|---|---|
| PostgreSQL | Heap-organized (CTID = physical order of insertion) | CLUSTER reorders once |
| DuckDB | Row-group columnar layout | `ORDER BY` in `COPY` or `CREATE TABLE AS` optimizes scan |
| ClickHouse | ORDER BY columns specified in table engine | Primary key determines sort |
| BigQuery | Capacitor columnar format, no physical sort guarantee | `CLUSTER BY` controls block layout |
| Snowflake | Micro-partition metadata tracks column min/max | Automatic via clustering |
| Redshift | SORTKEY determines block order | Compound vs interleaved |

---

## 4. Data Modeling for Analytics

### 4.1 Star Schema

**Structure:** One central *fact table* surrounded by *dimension tables*.

```
                     +--------------+
                     | Date (Dim)   |
                     | date_key     |<-------+
                     +--------------+        |
                                              |
+----------------+                  +------------------+
| Product (Dim)  |                  | Sales (Fact)     |
| product_key    |<-----------------| product_key (FK) |
| product_name   |                  | customer_key (FK)|
| category       |                  | date_key (FK)    |
+----------------+                  | store_key (FK)   |
                                    | quantity         |
+----------------+                  | unit_price       |
| Store (Dim)    |                  | discount         |
| store_key      |<-----------------+------------------+
| store_name     |
| region         |                  +------------------+
+----------------+                  | Customer (Dim)   |
                                    | customer_key (FK)|
                                    +------------------+
```

**Fact table design rules:**
- Grain: explicitly define what one row represents (e.g., one row per product per store per day).
- Foreign keys: reference dimension surrogate keys, not natural keys.
- Measures: additive (quantity, amount), semi-additive (balance), non-additive (ratio).
- Avoid storing NULLs in numeric measure columns — use 0 if meaningful.

**Dimension table design rules:**
- Surrogate key (auto-increment or UUID) as primary key.
- Natural key stored as a separate attribute (business key).
- Split hierarchical attributes into role-playing dimensions where appropriate.
- Include descriptive text, codes, and categorization columns.

---

### 4.2 Snowflake Schema

**Structure:** Dimensions are normalized into multiple related tables.

```
+----------------+    +------------------+    +------------------+
| Category       |    | Subcategory      |    | Product          |
| category_id    |<---| category_id (FK) |<---| subcategory_id   |
| category_name  |    | subcategory_id   |    | product_key      |
+----------------+    | subcategory_name |    | product_name     |
                      +------------------+    +------------------+
```

**Star vs Snowflake decision:**

| Factor | Star | Snowflake |
|---|---|---|
| Query simplicity | Simple (fewer joins) | Complex (more joins) |
| Storage | Redundant (denormalized) space | Normalized (less space) |
| ETL complexity | Simple (single table) | Complex (multiple related tables) |
| BI tool performance | Fast (fewer joins) | Slower (more joins) |
| Maintenance | Update all rows in denormalized table | Update one row in normalized table |
| Dimensional hierarchy | Flattened into one table | Separate tables per level |

**Rule of thumb:** Start with star schema. Only normalize to snowflake when:
- Dimension has more than 5 hierarchical levels.
- Dimension rows are shared across multiple fact tables.
- Storage cost savings from normalization are significant.
- The ETL/maintenance overhead of snowflake is acceptable.

---

### 4.3 Dimensional Modeling (Kimball)

Kimball's four-step dimensional design process:

1. **Select the business process** (e.g., sales, inventory, customer orders).
2. **Declare the grain** (e.g., one row per product per store per day).
3. **Identify the dimensions** (who, what, where, when, why).
4. **Identify the facts** (measures: how many, how much).

**Conformed dimensions:** Dimensions that are shared across multiple fact tables
with the same keys, attributes, and meanings. This enables cross-process analysis
(e.g., compare sales to inventory by product).

**Degenerate dimensions:** Dimension attributes stored in the fact table because
they have no separate dimension table (e.g., order number for a line-item fact).

**Junk dimensions:** A single dimension table combining multiple low-cardinality
flags and indicators (e.g., `is_new_customer`, `is_express_shipping`, `is_promo`)
into one table to keep the fact table lean.

**Fact table types:**

| Type | Description | Example |
|---|---|---|
| **Transactional** | One row per event | Line-item sales, web clicks |
| **Periodic Snapshot** | One row per period | Daily account balance, monthly inventory |
| **Accumulating Snapshot** | One row per process lifecycle | Order fulfillment (order -> ship -> deliver) |

---

### 4.4 Slowly Changing Dimensions (SCD)

**SCD Type 0 — Retain original:**
- Dimension attributes never change once written.
- Use for immutable reference data (date of birth, timestamp).

**SCD Type 1 — Overwrite:**
- No history; current value overwrites the old value.
```sql
UPDATE customer_dim
SET email = 'new@email.com'
WHERE customer_id = 123;
```

**SCD Type 2 — Add new row (most common for analytics):**
- Each change creates a new row with effective dates.
```sql
UPDATE customer_dim
SET end_date = CURRENT_DATE - 1
WHERE customer_id = 123 AND end_date IS NULL;  -- expire old

INSERT INTO customer_dim (customer_id, name, email, start_date, end_date)
VALUES (123, 'John', 'new@email.com', CURRENT_DATE, NULL);  -- add new
```

*Additional columns for Type 2:*
- `start_date`, `end_date` — effective date range
- `is_current` — boolean flag for active row
- `version_number` — incrementing version

**SCD Type 3 — Add new column:**
- Track limited history by adding a "previous value" column.
```sql
ALTER TABLE customer_dim ADD COLUMN previous_email VARCHAR(255);
UPDATE customer_dim
SET previous_email = email, email = 'new@email.com'
WHERE customer_id = 123;
```

**SCD Type 4 — Mini-dimension:**
- Rapidly changing attributes are split into a separate dimension table.
- The main dimension stores the current value; the mini-dimension tracks changes.
- Useful when attributes change faster than the dimension can accommodate Type 2.

**SCD Type 6 (Hybrid 1+2+3):**
- Combines Type 1 (current value), Type 2 (history via rows), and Type 3 (previous value column).
- Useful for "as-is" and "as-was" reporting in the same table.

**Decision table:**

| SCD Type | Use When |
|---|---|
| 0 | Attribute never changes (birth date, original SKU) |
| 1 | History not needed, audit not required (email, phone) |
| 2 | Full history required (address, department) |
| 3 | Quick access to previous value only (territory assignment) |
| 4 | Attributes change very frequently (credit score, loyalty tier) |
| 6 | Need both current and historical in same query (compliance) |

---

### 4.5 Fact Table Design — Advanced

**Additive vs Semi-Additive vs Non-Additive:**

| Measure Type | Add Across All Dims | Add Across Time | Example |
|---|---|---|---|
| Additive | Yes | Yes | Sales amount, quantity |
| Semi-additive | Yes | No | Account balance, inventory level |
| Non-additive | No | No | Ratio, percentage, unit price |

*Semi-additive handling:* Use `SUM()` across other dimensions, but `AVG()` or
`LAST_VALUE()` across time.

**Null handling in facts:**
- Numeric facts: use 0 for additive nulls (quantity, amount). Use NULL for
  non-applicable values (e.g., discount on non-promotional sale).
- Foreign keys: avoid NULLs — use a "Unknown" dimension row (key = -1).

**Factless fact tables:**
- A fact table with only foreign keys and no measures.
- Records an event or relationship (e.g., product-to-campaign assignment, student attendance).

**Transaction header + line-item fact modeling:**
- Grain = line item.
- Header-level attributes (order date, customer, store) are degenerate dimensions.
- Headers with multiple grains may split into separate fact tables.

---

## 5. SQL Testing & Validation Patterns

### 5.1 Data Quality Testing with SQL

**Category: Uniqueness / Primary Key**
```sql
-- EXPECT: 0 rows (all IDs are unique)
SELECT id, COUNT(*)
FROM target_table
GROUP BY id
HAVING COUNT(*) > 1;
```

**Category: Not Null**
```sql
-- EXPECT: 0 rows (no nulls in required columns)
SELECT COUNT(*) AS null_count
FROM target_table
WHERE required_column IS NULL;
```

**Category: Referential Integrity**
```sql
-- EXPECT: 0 rows (all foreign keys exist in parent)
SELECT DISTINCT ft.fk_column
FROM fact_table ft
LEFT JOIN dim_table dt ON ft.fk_column = dt.pk
WHERE dt.pk IS NULL;
```

**Category: Accepted Values (enum/dimension)**
```sql
-- EXPECT: 0 rows (all values in allowed set)
SELECT DISTINCT status
FROM target_table
WHERE status NOT IN ('active', 'inactive', 'pending', 'cancelled');
```

**Category: Freshness (data recency)**
```sql
-- EXPECT: max date within acceptable lag
SELECT MAX(loaded_at) AS last_load
FROM target_table;
-- Alert if last_load < CURRENT_TIMESTAMP - INTERVAL '24 hours'
```

**Category: Row Count Consistency**
```sql
-- EXPECT: row counts match (within tolerance)
SELECT 'source' AS source, COUNT(*) AS cnt FROM source_table
UNION ALL
SELECT 'target', COUNT(*) FROM target_table;
```

**Category: Distribution / Outlier Detection**
```sql
-- EXPECT: no rows outside 3 standard deviations
WITH stats AS (
  SELECT
    AVG(amount) AS avg,
    STDDEV(amount) AS std
  FROM orders
)
SELECT *
FROM orders, stats
WHERE ABS(orders.amount - stats.avg) > 3 * stats.std;
```

**Category: Duplicate Detection (multi-column)**
```sql
-- EXPECT: 0 rows
SELECT natural_key_1, natural_key_2, COUNT(*)
FROM target_table
GROUP BY natural_key_1, natural_key_2
HAVING COUNT(*) > 1;
```

---

### 5.2 dbt Test Patterns

dbt provides four built-in generic tests:

```yaml
# schema.yml
version: 2
models:
  - name: orders
    columns:
      - name: order_id
        tests:
          - unique
          - not_null
      - name: status
        tests:
          - accepted_values:
              values: ['placed', 'shipped', 'completed', 'cancelled']
      - name: customer_id
        tests:
          - not_null
          - relationships:
              to: ref('customers')
              field: customer_id
```

**Custom singular tests (dbt):**
```sql
-- tests/custom/positive_revenue.sql
-- EXPECT: 0 rows returned
SELECT order_id, revenue
FROM {{ ref('orders') }}
WHERE revenue < 0;
```

**Custom generic tests (dbt):**
```sql
-- tests/generic/test_is_positive.sql
{% test is_positive(model, column_name) %}
SELECT *
FROM {{ model }}
WHERE {{ column_name }} < 0
{% endtest %}
```

---

### 5.3 Testing Pipeline Patterns

**Unit testing (transformation logic):**

```sql
-- Given: a known input
WITH test_data AS (
  SELECT 'US' AS country, 100 AS amount, DATE '2024-01-15' AS order_date
  UNION ALL
  SELECT 'UK', 200, DATE '2024-02-20'
)
-- When: apply transformation
, transformed AS (
  SELECT
    country,
    amount,
    CASE WHEN country = 'US' THEN amount * 1.0 ELSE amount * 1.2 END AS amount_usd
  FROM test_data
)
-- Then: assert expected output
SELECT *
FROM transformed
WHERE (country = 'US' AND amount_usd != 100)
   OR (country = 'UK' AND amount_usd != 240);
```

**Regression testing (compare output across versions):**

- Store known-good output as a reference table or CSV.
- Run the new version of the query.
- EXPECT: row-perfect match (or within delta for floating-point).

**Schema drift detection:**
```sql
-- Compare column schemas between source and target
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'source'
EXCEPT
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'target';
```

**Reconciliation (cross-system):**

```sql
SELECT
  COALESCE(a.order_id, b.order_id) AS order_id,
  a.total AS source_total,
  b.total AS target_total,
  COALESCE(a.total, 0) - COALESCE(b.total, 0) AS diff
FROM source_system.orders a
FULL OUTER JOIN target_system.orders b
  ON a.order_id = b.order_id
WHERE a.total IS DISTINCT FROM b.total;
```

---

## 6. Analytical SQL Engine Comparison

### 6.1 Engine Overview

| Feature | PostgreSQL | DuckDB | ClickHouse | BigQuery | Snowflake | Redshift |
|---|---|---|---|---|---|---|
| **Architecture** | Row-store, monolithic | Columnar, embedded | Columnar, MPP | Serverless, columnar | Virtual warehouses, columnar | Columnar, MPP |
| **Deployment** | Self-hosted / managed | Embedded / MotherDuck cloud | Self-hosted / ClickHouse Cloud | GCP only | AWS / Azure / GCP | AWS only |
| **SQL dialect** | SQL:2011 | SQL:2011 + extensions | Custom SQL (MySQL-like) | GoogleSQL | SnowflakeSQL | PostgreSQL-like |
| **ACID** | Full | Full | Per-table | Row-level (recent) | Snapshot isolation | Serial isolation |
| **Concurrency model** | Connection-based | Single-user (per process) | High-concurrency reads | Massive concurrency | Virtual warehouse scale | WLM queues |

### 6.2 Performance Characteristics

| Metric | PostgreSQL | DuckDB | ClickHouse | BigQuery | Snowflake | Redshift |
|---|---|---|---|---|---|---|
| **Scan speed (single node)** | ~50 MB/s | ~500 MB/s | ~2-5 GB/s | ~GB/s (distributed) | ~MB/s per node | ~GB/s per slice |
| **Aggregation throughput** | Moderate | Very high | Extremely high | Very high | High | High |
| **JOIN performance** | Excellent (indexed) | Good (hash join) | Good (need careful schema) | Excellent | Excellent | Good |
| **Sub-second queries** | Yes (small data) | Yes (in-memory) | Yes (columnar) | Yes (with cached) | Yes (with cached) | Yes (with SORTKEY) |
| **Full table scan** | Slow | Fast | Very fast | Fast | Moderate | Fast |
| **Concurrent queries** | Good (configurable) | Limited (single process) | Excellent | Excellent | Good (per warehouse) | Good (per WLM queue) |

### 6.3 When Each Engine Makes Sense

**PostgreSQL — The transactional foundation:**
- Source of record for OLTP systems.
- Small-to-medium analytical workloads (< 50 GB).
- When you need full ACID and complex joins.
- Data engineering: staging area, metadata store, Airflow backend.
- NOT for: multi-TB datasets, high-cardinality aggregations on billions of rows.

**DuckDB — The embedded analyst:**
- Local data exploration on Parquet/CSV files.
- Single-machine analytical workloads (up to ~100 GB comfortably in memory).
- Data engineering: dbt development, local testing, transform-in-place.
- Embedded analytics (in-process OLAP).
- NOT for: multi-user production APIs, concurrent write workloads.

**ClickHouse — The real-time powerhouse:**
- Real-time dashboards and observability.
- High-ingestion-rate event data (logs, metrics, clickstreams).
- Sub-second aggregations on billions of rows.
- Data engineering: time-series analytics, real-time monitoring, product analytics.
- NOT for: point-lookup queries, frequent small updates/deletes, complex joins.

**BigQuery — The serverless warehouse:**
- When you don't want to manage infrastructure.
- Petabyte-scale analytics with auto-scaling.
- Integration with Google Cloud ecosystem (Dataflow, Looker, Vertex AI).
- Data engineering: ELT-heavy workflows, ad-hoc analysis at scale.
- NOT for: transactional workloads, predictable monthly spend (cost can be spiky).

**Snowflake — The enterprise data cloud:**
- When multi-cloud or multi-region is required.
- Data sharing across organizations (Snowflake Marketplace).
- Separation of compute and storage with automatic scaling.
- Data engineering: production data warehouses, data sharing, BI backends.
- NOT for: real-time streaming (ingest latency is seconds), budget-constrained workloads.

**Redshift — The AWS-native warehouse:**
- Heavily invested in the AWS ecosystem.
- Predictable performance for well-defined workloads.
- Integration with S3, Glue, Spectrum, QuickSight.
- Data engineering: large-scale batch processing on AWS, BI workloads.
- NOT for: ad-hoc multi-user queries without careful WLM tuning, multi-cloud.

### 6.4 Key Feature Differences

| Feature | PostgreSQL | DuckDB | ClickHouse | BigQuery | Snowflake | Redshift |
|---|---|---|---|---|---|---|
| **Materialized views** | Manual REFRESH | Not built-in (use dbt) | Materialized views | Auto-refresh | Auto-refresh, cost credits | Late-binding views |
| **MERGE support** | `INSERT ON CONFLICT` | `MERGE` (v1.3+) | `ALTER TABLE .. DELETE` + INSERT | `MERGE` | `MERGE` | `MERGE` (RA3+) |
| **External tables** | FDW (postgres_fdw) | `read_parquet`, `read_csv` | `CREATE TABLE .. ENGINE=Kafka/MySQL` | External tables | External tables | Spectrum |
| **Window functions** | Full support | Full support | Full support | Full support | Full support | Full support |
| **Recursive CTEs** | Yes | Yes | No (non-recursive only) | Yes | Yes | Yes |
| **PIVOT** | `crosstab()` extension | `PIVOT` | No (use `GROUP BY` + arrays) | `PIVOT` | `PIVOT` | No (use CASE) |
| **Semi-structured** | JSONB | JSON, Struct, Array | JSON, Array, Tuple, Nested | REPEATED, RECORD | VARIANT | SUPER (JSON-like) |
| **Time travel** | pg_rewind (limited) | Not built-in | Not built-in (use snapshot) | Query any point in 7 days | `AT (TIMESTAMP)` up to 90 days | `RESTORE TABLE` |
| **Cost model** | Licensing + hardware | Free / MotherDuck consumption | Open source / Cloud credits | Pay per byte scanned | Pay per compute credit | Pay per node-hour |

### 6.5 Pricing and Cost Considerations

| Engine | Cost Character | Best Cost Profile | Worst Cost Profile |
|---|---|---|---|
| PostgreSQL | Fixed (HW/license) | Predictable, moderate volume | Very large datasets (no auto-scale) |
| DuckDB | Free / MotherDuck usage | Sub-TB workloads, OLAP queries | Multi-user concurrent access |
| ClickHouse | HW/cloud credits | High-volume, high-throughput real-time | Small workloads (overhead of cluster) |
| BigQuery | Per-byte scanned | Ad-hoc, infrequent large queries | Repeated full scans of large tables |
| Snowflake | Per-credit (compute) | Variable workloads with auto-suspend | Always-on large warehouse |
| Redshift | Per-node-hour (fixed) | Steady-state batch workloads | Idle clusters (pay for what you allocate) |

### 6.6 Engine Selection Matrix

| Workload Profile | Recommended Engine | Runner-Up |
|---|---|---|
| Small team, local analysis | DuckDB | PostgreSQL |
| Cloud-native analytics, GCP shop | BigQuery | Snowflake |
| Enterprise data warehouse, multi-cloud | Snowflake | BigQuery |
| AWS ecosystem, steady workloads | Redshift | Snowflake |
| Real-time observability, logs | ClickHouse | BigQuery (streaming) |
| Embedded analytics (SaaS product) | DuckDB | ClickHouse |
| Transactional + reporting (single system) | PostgreSQL | -- |
| Petabyte-scale ad-hoc | BigQuery | Snowflake |
| Budget-constrained, large batch | ClickHouse (self-hosted) | DuckDB (MotherDuck) |

---

## Appendix: Quick Reference SQL Snippets

**Common analytical queries:**

```sql
-- Top-N per group
SELECT * FROM (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY category ORDER BY revenue DESC) AS rn
  FROM sales
) WHERE rn <= 10;

-- Running total
SELECT date, SUM(amount) OVER (ORDER BY date ROWS UNBOUNDED PRECEDING) AS running_total
FROM daily;

-- Month-over-month change
WITH monthly AS (
  SELECT DATE_TRUNC('month', date) AS month, SUM(val) AS val
  FROM data GROUP BY 1
)
SELECT month, val,
  LAG(val) OVER (ORDER BY month) AS prev,
  (val - LAG(val) OVER (ORDER BY month)) / NULLIF(LAG(val) OVER (ORDER BY month), 0) * 100 AS mom_pct
FROM monthly;

-- Rolling 7-day average
SELECT date, AVG(amount) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS ma_7
FROM daily_revenue;

-- Deduplication (keep latest)
WITH deduped AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY business_key ORDER BY updated_at DESC) AS rn
  FROM raw
)
SELECT * FROM deduped WHERE rn = 1;

-- Fill forward (last non-null value)
SELECT
  date,
  amount,
  LAST_VALUE(amount IGNORE NULLS) OVER (ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS filled
FROM sparse_data;
```

---

*End of reference document.*
