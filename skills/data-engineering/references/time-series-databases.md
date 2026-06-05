# Time-Series Database Patterns for Data Engineering

> A thorough reference on time-series databases with a focus on InfluxDB, written for the data engineering methodology skill.

---

## Table of Contents

1. [When to Choose a Time-Series DB Over a Relational DB](#1-when-to-choose-a-time-series-db-over-a-relational-db)
2. [InfluxDB Data Model](#2-influxdb-data-model)
3. [Schema Design for Time-Series](#3-schema-design-for-time-series)
4. [Flux Query Language Fundamentals](#4-flux-query-language-fundamentals)
5. [InfluxQL vs Flux vs SQL](#5-influxql-vs-flux-vs-sql)
6. [Downsampling and Continuous Queries / Tasks](#6-downsampling-and-continuous-queries--tasks)
7. [Data Lifecycle Management](#7-data-lifecycle-management)
8. [Ingest Patterns](#8-ingest-patterns)
9. [Integration with Data Engineering Pipelines](#9-integration-with-data-engineering-pipelines)
10. [Comparison: InfluxDB vs TimescaleDB vs Prometheus vs QuestDB](#10-comparison-influxdb-vs-timescaledb-vs-prometheus-vs-questdb)

---

## 1. When to Choose a Time-Series DB Over a Relational DB

### Time-Series Data Characteristics

Not all timestamped data is time-series data. True time-series data has these properties:

- **Append-heavy**: New data points arrive continuously; updates/upserts are rare.
- **Time-ordered**: Write order closely follows the timestamp order (recent data is hot).
- **Time-centric queries**: Analysts almost always filter, aggregate, and slice by time ranges.
- **Downsampling pattern**: Old data is routinely summarized into lower-resolution rollups.
- **Immutable by nature**: Historical records are almost never modified.

### Decision Matrix

| Factor | Choose Relational (PostgreSQL/MySQL) | Choose Time-Series DB (InfluxDB/TimescaleDB) |
|---|---|---|
| Write pattern | Mixed read-write, UPDATE-heavy | Append-only streaming writes |
| Data volume | Millions of rows | Billions to trillions of data points |
| Query pattern | OLTP: single-row lookups, JOINs, transactions | Time-bucket aggregates, range scans |
| Retention | Keep everything indefinitely, DELETE rare | Auto-expire raw data after N days |
| Schema | Frequently evolving, normalized | Stable, denormalized per measurement |
| Consistency | ACID strongly required | Eventual or tunable consistency acceptable |
| Cardinality | Low (user IDs, order IDs) | Can range from low to very high (device IDs, container IDs) |

### When to Use a General-Purpose TSDB (like InfluxDB)

- **Metrics infrastructure**: Server/container CPU, memory, disk, network (DevOps/SRE).
- **IoT/IIoT sensor data**: Temperature, pressure, vibration readings at high frequency.
- **Application telemetry**: Request latencies, error rates, user counts.
- **Industrial/historian workloads**: Replacing PI System, OSIsoft, or other historians.
- **Financial tick data**: Stock trades, order book snapshots (though QuestDB may be better here).

### When to Stick with a Relational DB + Time-Series Extension

- You already have a PostgreSQL ecosystem and want to avoid another infrastructure stack.
- Your time-series data has complex relational joins (e.g., sensor metadata normalized across 5 tables).
- You need full SQL with window functions, CTEs, and transactional guarantees.
- *Solution: TimescaleDB hypertables on PostgreSQL.*

### When to Use an Analytical Columnar DB (ClickHouse) Instead

- You run large ad-hoc analytical queries on time-series data (OLAP-style).
- You need sub-second aggregation over billions of rows across many dimensions.
- Your query patterns are more "GROUP BY time, dimension" than "latest value per series."

---

## 2. InfluxDB Data Model

InfluxDB v1 and v2 share a four-component data model. InfluxDB 3 (the current recommended version) retains compatibility with this model but adds SQL-on-Parquet support.

### The Four Components

```
Measurement   ->  Logical table name (e.g., "cpu", "sensor_temp")
Tag set       ->  Indexed metadata key=value pairs (e.g., host=server01, region=us-east)
Field set     ->  Actual data values (e.g., temperature=98.6, cpu_usage=0.85)
Timestamp     ->  Nanosecond-precision Unix timestamp
```

### Line Protocol Format

This is the canonical way to write data into InfluxDB (all versions):

```
<measurement>[,<tag_key>=<tag_value>[,<tag_key>=<tag_value>...]] <field_key>=<field_value>[,<field_key>=<field_value>...] [<timestamp>]
```

**Concrete example:**

```
sensor_temp,host=server01,region=us-east temperature=98.6,humidity=0.45 1717610400000000000
```

Or in InfluxDB 3 SQL terms, the CREATE TABLE equivalent would be:

```sql
-- InfluxDB 3 uses SQL for schema management
CREATE TABLE sensor_temp (
    time TIMESTAMP,
    host STRING,      -- tag
    region STRING,    -- tag
    temperature DOUBLE,  -- field
    humidity DOUBLE      -- field
);
```

### How InfluxDB Stores Data

- **Tags are indexed** — they form the *series key*. Every unique combination of measurement + tag set defines a **time series**.
- **Fields are not indexed** — querying by field values requires a full scan.
- **Timestamp** is the primary sort key within each series.
- In InfluxDB 3 (IOx engine), data is stored in **Parquet files** on object storage, with an in-memory catalog for indexing.
- In InfluxDB 1.x/2.x (TSM engine), data is stored in **TSM (Time-Structured Merge Tree)** files with an in-memory index.

### Series Cardinality

```
series cardinality = number of unique (measurement, tag set) combinations
```

**Example:** If you have measurement `cpu` with tags `host` (1000 values) and `region` (5 values), you have up to 5,000 series.

**High cardinality is the #1 performance killer in InfluxDB v1/v2 (TSM engine).** InfluxDB 3 (IOx) largely solves this by using a columnar storage engine, but high cardinality still affects memory for the catalog.

**Values that cause high cardinality and should NEVER be tags:**
- Request IDs
- Session IDs
- User IDs (if unique per user and high volume)
- Timestamps as strings
- Email addresses
- Any value with millions of unique values

---

## 3. Schema Design for Time-Series

### Measurement Design

**Rule of thumb:** One measurement per logical data source type.

```
GOOD:  measurement="cpu"     fields={usage_user, usage_system, usage_idle}
GOOD:  measurement="memory"  fields={used_bytes, free_bytes, total_bytes}
BAD:   measurement="metrics" fields={cpu_user, cpu_system, mem_used, mem_free, disk_read, disk_write}
```

### Tag vs Field Decision Guide

| Put in TAGS if... | Put in FIELDS if... |
|---|---|
| Low to moderate cardinality (< 100K unique values) | The actual measured numeric value |
| You filter or GROUP BY this attribute | High cardinality (request IDs, UUIDs) |
| It's static/reusable metadata (host, region, data_center) | It's the payload/metric value itself |
| You need fast indexed lookups | It changes on every data point |

### Tag Cardinality Management

**For InfluxDB v1/v2 (TSM):**
- Keep total series cardinality under 10 million per node (hard limit ~10-20M).
- Keep per-measurement cardinality under 1 million for good performance.
- Use TSI (Time Series Index) for higher cardinality in v1.7+ but expect memory pressure.

**For InfluxDB 3 (IOx/columnar):**
- Catalog memory scales with number of unique tag values, not combinations.
- Can handle 100M+ unique series; watch catalog memory (~2-4 GB per 100M series).

**Anti-patterns to avoid:**
- Putting timestamps, dates, or high-entropy strings as tags.
- Using tags for values that change on every write.
- Over-tagging (10+ tags per measurement when 3-4 would suffice).
- Tag values that grow unboundedly (e.g., container IDs in Kubernetes).

### Retention Policies (v1) vs Buckets (v2)

**InfluxDB v1 — Retention Policies (RPs):**
```sql
-- Create a retention policy: keep data for 30 days, 1 replica
CREATE RETENTION POLICY "thirty_days" ON "mydb" DURATION 30d REPLICATION 1 DEFAULT;
```

**InfluxDB v2 — Buckets:**
```bash
# A bucket combines a database + retention policy from v1
influx bucket create --name "sensor_data_30d" --retention 30d
```

**InfluxDB 3 — Retention at Database Level:**
```bash
# InfluxDB 3 Core: retention set at database level
# Core OSS enforces a 72-hour default; Cloud Dedicated and Enterprise allow custom retention
influxdb3 create database iot_sensors_prod --retention-period 90d
```

**Best practices:**
- Use separate buckets for different retention durations.
- For long-term storage, downsample raw data into a separate measurement with longer retention.
- In InfluxDB 3, the retention period is set per database and defines how long data is kept before automatic deletion.

---

## 4. Flux Query Language Fundamentals

> **Note:** Flux was introduced with InfluxDB v2.x. InfluxDB 3 now recommends **SQL** as the primary query language. Flux is still supported in InfluxDB 2.x and for backward compatibility, but new development on InfluxDB 3 should favor SQL. This section is retained for teams maintaining v2.x workloads.

### Basic Structure

Flux is a **functional, piped-data language**. Every query is a chain of transformations with data flowing left-to-right through pipes (`|>`).

```
data_source
    |> transformation_1()
    |> transformation_2()
    |> transformation_3()
```

### Core Functions

```flux
// 1. Define the data source and time range
from(bucket: "sensor_data")
    |> range(start: -1h)                    // last hour of data
    |> filter(fn: (r) => r._measurement == "cpu")
    |> filter(fn: (r) => r._field == "usage_user")
    |> filter(fn: (r) => r.host == "server01")
    |> yield(name: "cpu_usage")
```

### Common Flux Patterns

**Aggregation with windowing (downsampling):**
```flux
from(bucket: "sensor_data")
    |> range(start: -7d)
    |> filter(fn: (r) => r._measurement == "sensor_temp")
    |> aggregateWindow(every: 1h, fn: mean)
    |> yield(name: "hourly_mean")
```

**Multiple aggregations in one query:**
```flux
from(bucket: "sensor_data")
    |> range(start: -24h)
    |> filter(fn: (r) => r._measurement == "cpu" and r._field == "usage_user")
    |> aggregateWindow(every: 15m, fn: mean)
    |> duplicate(column: "_stop", as: "_time")
    |> drop(columns: ["_start", "_stop"])
    |> set(key: "_field", value: "usage_user_mean")
    |> to(bucket: "downsampled_cpu")
```

**Pivoting to wide format (useful for Grafana):**
```flux
from(bucket: "sensor_data")
    |> range(start: -1h)
    |> filter(fn: (r) => r._measurement == "cpu")
    |> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")
    |> yield(name: "wide")
```

**Joining data streams:**
```flux
cpu = from(bucket: "sensor_data")
    |> range(start: -1h)
    |> filter(fn: (r) => r._measurement == "cpu" and r._field == "usage_user")

mem = from(bucket: "sensor_data")
    |> range(start: -1h)
    |> filter(fn: (r) => r._measurement == "mem" and r._field == "used_percent")

join(tables: {cpu: cpu, mem: mem}, on: ["_time", "host"])
    |> yield(name: "joined")
```

### Flux Task (recurring script)

```flux
// Run every hour
option task = {
    name: "downsample_cpu_hourly",
    every: 1h,
    offset: 5m
}

from(bucket: "raw_sensor_data")
    |> range(start: -2h)
    |> filter(fn: (r) => r._measurement == "cpu")
    |> aggregateWindow(every: 1h, fn: mean)
    |> to(bucket: "downsampled_cpu")
```

---

## 5. InfluxQL vs Flux vs SQL

### Overview

| Feature | InfluxQL | Flux | SQL (InfluxDB 3) |
|---|---|---|---|
| Era | InfluxDB 1.x | InfluxDB 2.x | InfluxDB 3 (current) |
| Style | SQL-like | Functional / piped | Standard SQL |
| Complexity | Low | Medium-High | Low |
| Learning curve | Easy (if you know SQL) | Steep | Easy (if you know SQL) |
| Multi-bucket queries | No | Yes | Yes |
| Joins | Limited (subqueries only) | Native | Full SQL JOINs |
| Scripting | No | Yes (variables, conditionals, functions) | Via SQL functions |
| Window functions | Limited | Native | Yes |
| Performance | Good | Medium (interpreted) | Best (compiled) |
| Status in InfluxDB 3 | Read-only compatibility | Supported for compatibility | **Recommended** |

### When to Use Which

```
Use SQL  (InfluxDB 3):  Default for ALL new projects on InfluxDB 3.
Use Flux (v2.x only):   Existing v2.x deployments, complex transformation pipelines.
Use InfluxQL (v1.x):    Existing v1.x deployments, minimal migration path.
```

### InfluxQL vs Flux: Equivalent Queries

**InfluxQL:**
```sql
SELECT mean("usage_user")
FROM "cpu"
WHERE time > now() - 1h
AND "host" = 'server01'
GROUP BY time(15m)
```

**Flux:**
```flux
from(bucket: "mydb/autogen")
    |> range(start: -1h)
    |> filter(fn: (r) => r._measurement == "cpu" and r._field == "usage_user" and r.host == "server01")
    |> aggregateWindow(every: 15m, fn: mean)
```

**SQL (InfluxDB 3):**
```sql
SELECT DATE_BIN(INTERVAL '15 minutes', time) AS bucket,
       AVG(usage_user) AS avg_usage
FROM cpu
WHERE time > now() - INTERVAL '1 hour'
  AND host = 'server01'
GROUP BY bucket
ORDER BY bucket;
```

### Key Migration Notes

- InfluxQL `GROUP BY time(interval)` → Flux `aggregateWindow(every: interval, fn: ...)`
- InfluxQL `INTO` (downsample+write) → Flux `... |> to(bucket: "...")`
- Continuous Queries (InfluxQL) → Tasks (Flux)
- InfluxDB 3: Rewrite InfluxQL CQs as SQL scheduled queries or use external orchestrators.

---

## 6. Downsampling and Continuous Queries / Tasks

### The Downsampling Pattern

Downsampling is the most critical data engineering pattern for time-series:

```
RAW DATA (1-second resolution, keep 30 days)
    |
    v  [downsample every hour]
HOURLY ROLLUPS (1-minute aggregates, keep 1 year)
    |
    v  [downsample every day]
DAILY ROLLUPS (1-hour aggregates, keep 5 years)
```

Each tier provides exponentially smaller storage footprint while preserving analytical value.

### InfluxDB 1.x: Continuous Queries (CQs)

```sql
CREATE CONTINUOUS QUERY "cq_cpu_hourly" ON "mydb"
BEGIN
  SELECT mean("usage_user") AS "mean_usage"
  INTO "mydb"."downsampled"."cpu_hourly"
  FROM "cpu"
  GROUP BY time(1h), "host"
END;
```

CQs run automatically at the end of each time window. They are simple but limited: only one aggregation function per CQ, no chaining.

### InfluxDB 2.x: Tasks (Flux-based)

```flux
// downsample_cpu_hourly
option task = {
    name: "downsample_cpu_hourly",
    every: 1h,
    offset: 10m
}

from(bucket: "raw_data")
    |> range(start: -task.every)
    |> filter(fn: (r) => r._measurement == "cpu")
    |> aggregateWindow(every: 1h, fn: mean)
    |> set(key: "_measurement", value: "cpu_hourly")
    |> to(bucket: "downsampled_data")
```

**Chained (hierarchical) downsampling with tasks:**
```
Task 1: raw_1s -> hourly (runs every hour)
Task 2: hourly -> daily   (runs every day, queries the hourly bucket)
Task 3: daily -> monthly  (runs monthly, queries the daily bucket)
```

### InfluxDB 3: Scheduled Queries / External Orchestration

InfluxDB 3 Core does not have built-in continuous aggregates. Recommended approaches:

1. **External scheduler** (Airflow, cron, Prefect):
   ```sql
   -- Run hourly via Airflow
   INSERT INTO cpu_hourly
   SELECT DATE_BIN(INTERVAL '1 hour', time) AS bucket,
          host,
          AVG(usage_user) AS avg_usage,
          MIN(usage_user) AS min_usage,
          MAX(usage_user) AS max_usage,
          COUNT(*) AS sample_count
   FROM cpu
   WHERE time > now() - INTERVAL '2 hours'
   GROUP BY bucket, host;
   ```

2. **InfluxDB 3 processing engine plugins** for real-time transformations on write.

3. **Write-time processing** via Telegraf aggregator plugins:
   ```toml
   [[processors.aggregate]]
   period = "60s"

   [[processors.aggregate.config]]
   measurement = "cpu"
   columns = ["usage_user", "usage_system"]
   functions = ["mean", "max", "min"]
   ```

### Downsampling Best Practices

- Store raw data at full resolution for the shortest practical window.
- Always include `COUNT(*)` in aggregates to track sample density.
- Use hierarchical aggregation (aggregate hourly data into daily, not raw into daily).
- Align your downsampling schedule with your retention policies.
- Consider **two-phase downsampling**: real-time via Telegraf aggregators for the first 1-5 minutes, then batch tasks for correction/backfill.

---

## 7. Data Lifecycle Management

### Storage Engine Architecture

**InfluxDB 1.x / 2.x (TSM Engine):**
- Data organized into **shards** by time range (typically 7 days).
- Each shard is a set of TSM files + Write-Ahead Log (WAL).
- **Compaction** merges smaller TSM files into larger ones, removing deleted/overwritten data.
- **Shard management**: Default 7-day shard duration; configurable.
- Memory index (in-memory) maps series keys to TSM file locations.

**InfluxDB 3 (IOx Engine):**
- Data stored as **Parquet files** in object storage (S3, local FS).
- Catalog (SQLite or PostgreSQL) tracks table/column metadata.
- **Compaction** merges Parquet files for read efficiency.
- No shards per se — data is partitioned by time but managed at the file level.

### Retention Lifecycle Strategy

```
Example: 3-tier retention for IoT sensor data

Tier 1: Raw (1-second resolution)   -> 30 days   -> bucket "raw_30d"
Tier 2: Hourly aggregates           -> 1 year    -> bucket "hourly_1y"
Tier 3: Daily aggregates            -> 5 years   -> bucket "daily_5y"
```

**InfluxDB v2/v3 implementation:**
1. Create three buckets with different retention periods.
2. Run downsampling tasks from raw -> hourly -> daily.
3. InfluxDB automatically deletes data older than each bucket's retention period.

### Compaction

**TSM compaction stages:**
- **Level 1** (snapshot): WAL -> TSM file (when WAL reaches threshold).
- **Level 2** (merge): 2-4 small TSM files -> 1 larger TSM file.
- **Level 3** (full): Multiple TSM files -> 1 optimized TSM file (deduplicates, removes tombstones).
- Compaction runs automatically; tune `cache-snapshot-write-cold-duration` and `compact-full-write-cold-duration` for write-heavy workloads.

**IOx/Parquet compaction:**
- Merges small Parquet files (< 100 MB) into larger ones (~100-500 MB).
- Runs automatically but can be triggered manually via API.
- Compaction also applies retention deletion.

### Shard Management (InfluxDB v1/v2)

```
Command:             Effect:
ALTER RETENTION      Change shard duration (default 7d)
  POLICY ... DURATION
DROP SHARD           Force-delete a specific shard and all its data
SHOW SHARDS          List all shards with durations, sizes, status
influx_inspect       Low-level TSM inspection and recovery tools
```

**Choosing shard duration:**
- Short shard duration (1-7d): More granular retention, easier to drop old data, more overhead.
- Long shard duration (1-4w): Less overhead, faster range queries, slower retention enforcement.
- Rule: shard duration should be ≤ 1/2 of your retention period for efficient expiry.

### Cold / Tiered Storage

- **InfluxDB Cloud Serverless**: Automatically tiers data to object storage.
- **InfluxDB Cloud Dedicated**: Configurable cold storage with Parquet.
- **TimescaleDB**: Native tiering to S3 via `tiering` policies.
- **InfluxDB OSS**: No built-in tiering; manage via external scripts or data migration.

---

## 8. Ingest Patterns

### Line Protocol

The core ingestion format for all InfluxDB versions.

**Format:**
```
measurement,tag1=val1,tag2=val2 field1=val1,field2=val2 timestamp
```

**Data types:**
- Tags: strings only (no quoting needed if no special chars).
- Fields: floats (default), integers (trailing `i`), strings (`"quoted"`), booleans (`t`/`f`/`true`/`false`).
- Timestamp: nanosecond epoch (default); configurable precision (s, ms, us, ns).

**Examples:**
```ini
# Float fields (default)
weather,location=us-midwest temperature=82.0 1465839830100400200

# Integer field (trailing i)
weather,location=us-midwest wind_speed=15i 1465839830100400200

# String field (double-quoted)
weather,location=us-midwest conditions="partly cloudy" 1465839830100400200

# Boolean field
weather,location=us-midwest is_raining=t 1465839830100400200

# Multiple fields
weather,location=us-midwest temperature=82.0,humidity=71.2 1465839830100400200
```

**Write via HTTP API:**
```bash
curl -X POST \
  "http://localhost:8086/write?db=mydb&precision=s" \
  --data-raw "weather,location=us-midwest temperature=82.0 1465839830"
```

### Batch vs Streaming Writes

| Factor | Batch | Streaming |
|---|---|---|
| Frequency | Every N seconds or N points | Every point as it arrives |
| Overhead | Low (HTTP overhead amortized) | High (per-request overhead) |
| Throughput | High (10K-100K points/s per node) | Low (1K-10K points/s per node) |
| Latency | Seconds to minutes | Sub-second |
| Use case | Backfill, batch ETL | Real-time monitoring, Telegraf |

**Best practice:** Always batch writes — send 1,000-10,000 points per HTTP request. Never send single points.

### Telegraf Agent

Telegraf is InfluxData's plugin-driven collection agent.

**Architecture:**
```
Input Plugins  ->  Aggregator/Processor Plugins  ->  Output Plugins
    |                       |                           |
  (CPU, disk,             (aggregate,                  (InfluxDB,
   MQTT, Kafka,            transform,                   Prometheus,
   Prometheus,              enrich,                      file, Kafka,
   syslog, SNMP,            filter)                      CloudWatch)
   Docker, k8s...)
```

**Example Telegraf config (`telegraf.conf`):**
```toml
# Global settings
[agent]
  interval = "10s"
  flush_interval = "10s"
  metric_batch_size = 5000

# Input: CPU metrics
[[inputs.cpu]]
  percpu = true
  totalcpu = true

# Input: MQTT subscriber
[[inputs.mqtt_consumer]]
  servers = ["tcp://broker.local:1883"]
  topics = ["sensors/#"]
  data_format = "json"
  json_time_key = "timestamp"
  json_time_format = "unix_ms"
  tag_keys = ["device_id", "location"]

# Processor: apply transformation
[[processors.enum]]
  [[processors.enum.mapping]]
    tag = "status"
    value_mappings = {online = 1, offline = 0}

# Aggregator: downsample in real-time
[[processors.aggregate]]
  period = "60s"
  [[processors.aggregate.config]]
    measurement = "cpu"
    columns = ["usage_idle", "usage_user"]
    functions = ["mean", "min", "max"]

# Output: InfluxDB v2
[[outputs.influxdb_v2]]
  urls = ["http://localhost:8086"]
  token = "${INFLUX_TOKEN}"
  organization = "myorg"
  bucket = "sensor_data"

# Output: backup to file (for audit trail)
[[outputs.file]]
  files = ["/var/log/telegraf_audit.log"]
  data_format = "json"
```

**Telegraf best practices:**
- Use `metric_batch_size` (5,000-10,000) and `flush_interval` (5-10s) for efficient batching.
- Tag inputs with consistent metadata (data center, region, environment).
- Use processor and aggregator plugins rather than sending raw data and downsampling later.
- Set `fieldpass`/`fielddrop` on inputs to avoid collecting unused metrics.
- File-based logging output for auditability and data recovery.

### Ingest Performance Tuning

| Parameter | InfluxDB v1/v2 (TSM) | InfluxDB 3 (IOx) |
|---|---|---|
| Write batch size | 5,000-10,000 points | 10,000-50,000 points |
| HTTP workers | 8-16 | 16-64 |
| WAL flush interval | 1-10s (lower = safer) | N/A (no WAL) |
| Max points per second (single node) | 500K-1M | 3M-10M |
| Bottleneck | CPU (index updates) | Network I/O (Parquet writes) |

### Kafka Integration

**Telegraf as Kafka consumer:**
```toml
[[inputs.kafka_consumer]]
  brokers = ["kafka:9092"]
  topics = ["sensor_events"]
  group_id = "telegraf_ingest"
  data_format = "json"
  consumer_fetch_min = "100KB"
  consumer_fetch_default = "1MB"
  max_undelivered_messages = 10000
```

**Telegraf as Kafka producer:**
```toml
[[outputs.kafka]]
  brokers = ["kafka:9092"]
  topic = "aggregated_metrics"
  data_format = "json"
  compression_codec = 2  # snappy
  required_acks = -1      # all
```

---

## 9. Integration with Data Engineering Pipelines

### Apache Airflow DAG Example

```python
from airflow import DAG
from airflow.providers.http.operators.http import HttpOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data_engineering',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'influxdb_downsample_hourly',
    schedule='0 * * * *',   # Every hour
    start_date=datetime(2025, 1, 1),
    catchup=False,
)

def generate_line_protocol(**context):
    """Generate downsampled data from raw and write hourly rollup."""
    import requests
    import json

    # Query raw hourly aggregates via SQL (InfluxDB 3)
    raw_data = requests.get(
        f"{INFLUX_HOST}/api/v3/query",
        params={"db": "sensor_raw"},
        headers={"Authorization": f"Bearer {INFLUX_TOKEN}"},
        data={
            "query": """
                SELECT DATE_BIN(INTERVAL '1 hour', time) AS bucket,
                       host, region, AVG(temperature) AS avg_temp,
                       MIN(temperature) AS min_temp, MAX(temperature) AS max_temp,
                       COUNT(*) AS sample_count
                FROM sensor_readings
                WHERE time >= now() - INTERVAL '2 hours'
                  AND time < now() - INTERVAL '1 hour'
                GROUP BY bucket, host, region
            """
        }
    )

    # Convert to line protocol and write to hourly bucket
    points = []
    for row in raw_data.json():
        lp = (
            f"sensor_hourly,host={row['host']},region={row['region']} "
            f"avg_temp={row['avg_temp']},min_temp={row['min_temp']},"
            f"max_temp={row['max_temp']},sample_count={row['sample_count']}i "
            f"{row['bucket']}"
        )
        points.append(lp)

    # Batch write
    requests.post(
        f"{INFLUX_HOST}/api/v2/write",
        params={"bucket": "sensor_hourly", "precision": "ms"},
        headers={"Authorization": f"Bearer {INFLUX_TOKEN}"},
        data="\n".join(points),
    )
```

### Apache Spark / PySpark Integration

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("influxdb_etl").getOrCreate()

# Read from InfluxDB v3 using JDBC (PostgreSQL-compatible driver)
df = spark.read \
    .format("jdbc") \
    .option("url", f"jdbc:postgresql://{INFLUX_HOST}:5432/mydb") \
    .option("query", """
        SELECT time, host, region, temperature
        FROM sensor_readings
        WHERE time >= now() - INTERVAL '24 hours'
    """) \
    .option("user", INFLUX_USER) \
    .option("password", INFLUX_PASS) \
    .option("driver", "org.postgresql.Driver") \
    .load()

# Transform
hourly_agg = df.groupBy(
    F.window("time", "1 hour").alias("bucket"),
    "host", "region"
).agg(
    F.avg("temperature").alias("avg_temp"),
    F.min("temperature").alias("min_temp"),
    F.max("temperature").alias("max_temp"),
    F.count("*").alias("sample_count")
)

# Write back to InfluxDB
hourly_agg.write \
    .format("jdbc") \
    .option("url", f"jdbc:postgresql://{INFLUX_HOST}:5432/downsampled_db") \
    .option("dbtable", "sensor_hourly") \
    .option("user", INFLUX_USER) \
    .option("password", INFLUX_PASS) \
    .mode("append") \
    .save()
```

### Grafana Integration

Grafana is the most common visualization layer for InfluxDB:

```
Grafana Data Source:
  Type: InfluxDB
  URL: http://influxdb:8086
  Database: mydb     (v1) / Organization: myorg, Bucket: sensor_data (v2/v3)
  Min time interval: 10s (matches collection interval)
  Version: InfluxQL (v1) / Flux (v2) / SQL (v3)
```

### ETL Pipeline Patterns

```
Pattern 1: Telegraf -> InfluxDB -> Grafana
  (simplest, real-time monitoring)

Pattern 2: Sensors -> MQTT/Kafka -> Telegraf -> InfluxDB -> Grafana
  (Kafka for buffering, backpressure handling)

Pattern 3: Sensors -> Kafka -> Flink/Spark -> InfluxDB -> Airflow (downsample) -> InfluxDB
  (heavy stream processing + scheduled downsampling)

Pattern 4: Application -> InfluxDB -> Airflow/Spark -> Parquet -> S3/Data Lake
  (time-series data lake architecture)
```

---

## 10. Comparison: InfluxDB vs TimescaleDB vs Prometheus vs QuestDB

### At a Glance

| Feature | InfluxDB 3 | TimescaleDB | Prometheus | QuestDB |
|---|---|---|---|---|
| **Type** | Purpose-built TSDB | PostgreSQL extension | Monitoring + TSDB | Purpose-built TSDB |
| **Engine** | Columnar (Parquet/IOx) | Hybrid row-columnar (Hypercore) | Custom TSDB engine | Columnar (custom) |
| **Query Language** | SQL + Flux + InfluxQL | Full SQL + PG extensions | PromQL | SQL |
| **Ingest Protocol** | Line Protocol, SQL, InfluxDB v2 API | PostgreSQL INSERT, COPY | Push via remote write | Line Protocol, InfluxDB, PostgreSQL wire |
| **Storage** | Parquet files on object storage | PostgreSQL on local/cloud disk | Local TSDB blocks | Memory-mapped files + disk |
| **Compression** | Good (Parquet) | Excellent (up to 95%) | Good (snappy) | Good |
| **High Availability** | Enterprise / Cloud (multi-node) | Streaming replication (PG built-in) | Sidecar (Thanos/Cortex) | Enterprise (pending) |
| **Clustering** | Enterprise only | PG-based | Built-in with Thanos | Enterprise |
| **Retention** | Per-database config | Per-hypertable via policies | Configurable (local) | Partition-based |
| **Continuous Aggregation** | External only (Core) | Built-in (continuous aggregates) | Recording rules | Materialized views |
| **Downsampling** | Tasks / external orchestration | Continuous aggregates | Recording rules + federation | SAMPLE BY + scheduled queries |
| **Real-time performance** | Excellent (3M+ points/s per node) | Very good (1M+ points/s) | Good (1M samples/s) | Excellent (5M+ points/s) |
| **SQL compatibility** | High (PostgreSQL-like) | **Complete (PostgreSQL)** | None (PromQL only) | High (custom SQL) |
| **Data lake export** | Native Parquet output | Via PG tools | Remote write / Thanos | Native Parquet output |
| **Best for...** | General TSDB, IoT, app metrics, edge | Teams already on PostgreSQL, need full SQL | Kubernetes monitoring, site reliability | **Lowest-latency**, financial tick data, HFT |

### Detailed Comparison

#### InfluxDB 3
- **Strengths:** Mature ecosystem (Telegraf, 300+ plugins), multiple deployment options (edge to cloud), native line protocol (de facto standard), good for heterogeneous data sources.
- **Weaknesses:** Flux deprecation path creates migration friction; Core OSS has 72h retention limit; no built-in continuous aggregates in Core; clustering only in Enterprise.
- **Best fit:** General-purpose time-series, DevOps/SRE monitoring, IoT/IIoT, replacing legacy historians.

#### TimescaleDB (Tiger Data)
- **Strengths:** Full PostgreSQL compatibility (all SQL, all PG extensions, all tools), continuous aggregates with incremental refresh, hierarchical aggregation, excellent compression (up to 95%), hypertables with automatic partitioning, mature replication/PITR/HA from PostgreSQL.
- **Weaknesses:** Slightly lower raw ingest throughput than InfluxDB 3 or QuestDB; requires PostgreSQL knowledge; not as lightweight for edge deployments; parent company rebranded to Tiger Data (some confusion).
- **Best fit:** Data teams already on PostgreSQL; workloads needing complex JOINs, transactions, or full SQL analytics; long-term historical storage.

#### Prometheus
- **Strengths:** Cloud-native standard for Kubernetes monitoring, simple operational model (single binary), PromQL is excellent for alerting and service-level metrics, pull-based model works well for dynamic infra.
- **Weaknesses:** Not a general-purpose TSDB (no SQL, no complex aggregations), limited retention (default 15d), single-node, no native HA (requires Thanos/Cortex), poor for IoT or high-cardinality label sets.
- **Best fit:** Kubernetes and container monitoring, service-level dashboards, alerting (PagerDuty/AlertManager), infra metrics.

#### QuestDB
- **Strengths:** **Highest raw ingest throughput** (claimed 5M+ points/s on single node), lowest query latency for time-bucket aggregations, designed for capital markets/finance, native InfluxDB line protocol and PostgreSQL wire protocol support, SQL-compatible, non-blocking ingestion (immutable append), parallelized and vectorized query execution.
- **Weaknesses:** Smaller ecosystem (fewer integrations, fewer client libraries), newer project (less mature), clustering is Enterprise-only, less tooling for alerting/monitoring out of the box.
- **Best fit:** Financial tick data, high-frequency trading, real-time dashboards demanding microsecond query latency, capital markets infrastructure.

### Decision Flowchart

```
Q: What infrastructure are you already running?
  |
  +-- PostgreSQL everywhere?
  |     |--> TimescaleDB (stay in PG ecosystem)
  |
  +-- Kubernetes / containers?
  |     |--> Prometheus for infra monitoring
  |     +--> InfluxDB for app metrics and IoT
  |
  +-- Need lowest possible latency (< 1ms queries)?
  |     |--> QuestDB (financial, HFT)
  |
  +-- Heterogeneous environment, edge devices, IoT?
        |--> InfluxDB (Telegraf ecosystem, multiple deployment options)

Q: What query language do you need?
  |--> Full SQL with JOINs, CTEs, window functions?    -> TimescaleDB or InfluxDB 3
  |--> Time-series specific: PromQL?                   -> Prometheus
  |--> Time-series specific: Flux?                     -> InfluxDB 2.x
  |--> DevOps dashboards: Grafana + search?            -> Any (Grafana supports all)

Q: How much data are you ingesting?
  |--> < 100K points/s                                 -> Any
  |--> 100K-1M points/s                                -> InfluxDB or TimescaleDB
  |--> > 1M points/s                                   -> QuestDB or InfluxDB 3
  |--> > 5M points/s                                   -> QuestDB (benchmark leader)
```

### Version Guidance (InfluxDB Specific)

| Deployment | Best For | Query Language |
|---|---|---|
| InfluxDB 3 Cloud Serverless | Rapid prototyping, variable workloads | **SQL** (recommended) |
| InfluxDB 3 Cloud Dedicated | Predictable production workloads | **SQL** (recommended) |
| InfluxDB 3 Enterprise | Self-managed HA production | **SQL** (recommended) |
| InfluxDB 3 Core | Edge, dev, prototypes | **SQL** (recommended) |
| InfluxDB OSS v2 | Existing v2.x deployments | Flux (migrate to SQL when moving to v3) |
| InfluxDB OSS v1 | Legacy, no migration budget yet | InfluxQL (migrate to SQL when possible) |

---

## Appendix: Quick Reference

### Line Protocol Cheatsheet

```
# Measurement name
weather
# Tags (comma-separated after measurement, space before fields)
weather,location=us-midwest,station=A
# Fields (comma-separated, space before timestamp)
weather temperature=82.0,humidity=71.2
# Timestamp (nanoseconds since epoch; space after fields)
weather temperature=82.0 1465839830100400200

# Data type suffixes:
#   Integer:    value=42i
#   Float:      value=3.14   (default)
#   String:     value="hello world"
#   Boolean:    value=t   (t/true/True/TRUE)
#               value=f   (f/false/False/FALSE)
#   Timestamp:  value=1465839830100400200   (nanosecond)

# Escaping:
#   Commas in tag values:    tag=hello\,world
#   Spaces in tag values:    tag=hello\ world
#   Equals in tag values:    tag=hello\=world
#   Double-quotes in string fields: field="say \"hello\""
#   Backslashes:             tag=path\\to\\dir
```

### Key InfluxDB v2/v3 CLI Commands

```bash
# InfluxDB v2
influx bucket create --name my_bucket --retention 30d
influx task create --file downsample.flux
influx query --file my_query.flux

# InfluxDB 3 Core
influxdb3 create database my_db --retention-period 90d
influxdb3 write --db my_db --file data.lp
influxdb3 query --db my_db "SELECT * FROM cpu WHERE time > now() - INTERVAL '1 hour'"
```

### Key TimescaleDB SQL Commands

```sql
-- Create hypertable
SELECT create_hypertable('sensor_readings', 'time');

-- Add compression
ALTER TABLE sensor_readings SET (
  timescaledb.compress,
  timescaledb.compress_segmentby = 'sensor_id'
);
SELECT add_compression_policy('sensor_readings', INTERVAL '7 days');

-- Continuous aggregate
CREATE MATERIALIZED VIEW sensor_hourly
WITH (timescaledb.continuous) AS
SELECT time_bucket('1 hour', time) AS bucket,
       sensor_id,
       AVG(value) AS avg_value
FROM sensor_readings
GROUP BY bucket, sensor_id;
```

---

*Generated: 2025-06-05 | InfluxDB 3 (IOx/columnar engine) is the current recommended version. Flux is supported for v2.x compatibility; new projects should prefer SQL.*
