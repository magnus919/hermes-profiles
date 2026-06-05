# dbt (Data Build Tool) — Comprehensive Reference Guide

> A methodology reference for data-engineering teams adopting dbt as the transformation layer in the modern data stack.

---

## Table of Contents

1. [What Is dbt and What Problem Does It Solve?](#1-what-is-dbt-and-what-problem-does-it-solve)
2. [dbt Core vs dbt Cloud](#2-dbt-core-vs-dbt-cloud)
3. [dbt Project Structure](#3-dbt-project-structure)
4. [dbt Modeling Concepts (Kimball Star Schema)](#4-dbt-modeling-concepts-kimball-star-schema)
5. [dbt Materializations](#5-dbt-materializations)
6. [dbt Tests](#6-dbt-tests)
7. [dbt Sources and Source Freshness](#7-dbt-sources-and-source-freshness)
8. [dbt Snapshots (Slowly Changing Dimensions)](#8-dbt-snapshots-slowly-changing-dimensions)
9. [dbt Documentation Generation](#9-dbt-documentation-generation)
10. [dbt Jinja/SQL Templating and Macros](#10-dbt-jinjasql-templating-and-macros)
11. [dbt Packages (dbt_utils, dbt_expectations)](#11-dbt-packages)
12. [dbt CI/CD Integration Patterns](#12-dbt-cicd-integration-patterns)
13. [dbt Mesh / Multi-Project Deployments](#13-dbt-mesh--multi-project-deployments)

---

## 1. What Is dbt and What Problem Does It Solve?

**dbt (data build tool)** is an open-source command-line tool and platform that enables analytics engineers and data analysts to transform data in their warehouse using SQL `SELECT` statements. It applies software-engineering best practices — version control, modularity, testing, CI/CD, documentation — to the data transformation layer.

### The Core Problem

Before dbt, the typical data workflow looked like:

1. Raw data lands in a warehouse via EL(E) tools (Fivetran, Airbyte, Stitch).
2. Transformations are written as arbitrary Python scripts, stored procedures, or tangled SQL in BI tools.
3. There is no lineage tracking, no testing, no documentation, and no repeatable deployment process.
4. Collaboration is hard because transformations are ad-hoc, not modular.

**dbt solves this by:**

- Moving the **T** (transform) from ETL to ELT — transformations happen *inside* the warehouse after data is loaded.
- Providing a **declarative, modular** framework: you write SQL `SELECT` statements, and dbt handles DDL (`CREATE TABLE`, `CREATE VIEW`, `INSERT`, `MERGE`) automatically.
- **Inferring a DAG** (directed acyclic graph) from `ref()` calls between models, enabling automatic dependency resolution and execution ordering.
- Bringing **software engineering to data**: version control (git), testing, documentation, CI/CD, package management.

### Key Concepts

| Concept | Description |
|---|---|
| **Models** | SQL files that `SELECT` from sources or other models; dbt materializes them as views/tables/incremental builds |
| **Tests** | Assertions on data quality — uniqueness, not-null, referential integrity, custom logic |
| **Sources** | Declarations of raw database tables loaded by EL tools; enables lineage, freshness checks |
| **Snapshots** | Type-2 slowly changing dimension (SCD) recording |
| **Seeds** | CSV files loaded into the warehouse as tables (for small reference/lookup data) |
| **Exposures** | Declarations of downstream consumers (dashboards, apps, ML models) |
| **Metrics** | Business metric definitions used by the dbt Semantic Layer |

> dbt is *not* an EL tool — it does not extract or load data. It assumes data already exists in a data warehouse (Snowflake, BigQuery, Redshift, Databricks, Postgres, etc.).

---

## 2. dbt Core vs dbt Cloud

### dbt Core

- **Free and open-source** (Apache 2.0 license).
- Command-line tool: `pip install dbt-core` + adapter for your warehouse (`dbt-snowflake`, `dbt-bigquery`, etc.).
- Requires you to manage your own orchestration (Airflow, Dagster, cron, GitHub Actions, etc.).
- No web UI — all development happens in a code editor + CLI.
- Community-driven; no official scheduling, logging, or collaboration features.

### dbt Cloud

- **Managed SaaS platform** by dbt Labs.
- Includes a web-based IDE, job scheduler, run history, and alerting.
- Built-in CI/CD via "Compare Changes" and environment promotion.
- **dbt Semantic Layer** with GraphQL and JDBC APIs for BI tool integration.
- **dbt Mesh** support for cross-project collaboration (multi-project `ref`).
- Role-based access control (RBAC), audit logs, SSO (Enterprise).
- **Pricing** is usage-based (by model runs/credits); free Developer tier available.

### Decision Matrix

| Criteria | dbt Core | dbt Cloud |
|---|---|---|
| Cost | Free | Paid (metered) |
| Orchestration | External (Airflow, Dagster, etc.) | Built-in scheduler |
| UI | CLI only | Web IDE + CLI |
| CI/CD | Manual setup (CI runner) | Built-in (Compare Changes) |
| Semantic Layer | Not available | Included (all paid tiers) |
| dbt Mesh | Limited (dbt-loom, manual) | Native support |
| Multi-user Dev | Git-based only | Managed environments + RBAC |
| Support | Community | Vendor support tiers |

**Typical pattern:** Teams using dbt Core locally for development and dbt Cloud (or a self-hosted orchestration tool) for production execution. Some teams use Core exclusively with Airflow/Dagster.

---

## 3. dbt Project Structure

A standard dbt project created via `dbt init <project_name>` has this layout:

```
my_dbt_project/
  ├── .gitignore
  ├── README.md
  ├── dbt_project.yml          # Project config (name, profile, model paths, etc.)
  ├── profiles.yml             # (outside project dir, ~/.dbt/) — DB connection config
  │
  ├── models/                  # SQL models (the core of the project)
  │   ├── staging/             # Raw → cleaned, one-to-one with source tables
  │   │   ├── _stg__models.yml # schema/docs for staging models
  │   │   ├── stg_customers.sql
  │   │   └── stg_orders.sql
  │   ├── intermediate/        # Business-logic transformations between staging and marts
  │   │   ├── int_order_items.sql
  │   │   └── ...
  │   └── marts/               # Business-facing models (facts + dimensions)
  │       ├── marketing/
  │       ├── finance/
  │       └── ...
  │
  ├── tests/                   # Singular tests (ad-hoc SQL assertions)
  │   ├── assert_total_revenue_positive.sql
  │   └── ...
  │
  ├── macros/                  # Jinja macros for reusable SQL logic
  │   ├── generate_schema_name.sql
  │   └── ...
  │
  ├── snapshots/               # Type-2 SCD snapshots
  │   ├── scd_customers.sql
  │   └── ...
  │
  ├── seeds/                   # CSV files loaded as tables
  │   ├── country_codes.csv
  │   └── ...
  │
  ├── analyses/                # Ad-hoc queries (not materialized)
  │   └── ...
  │
  └── data/                    # (deprecated in favor of seeds/)
```

### Key Files

**`dbt_project.yml`** — The project manifest:

```yaml
name: my_project
version: "1.0.0"
config-version: 2
profile: my_project_profile  # references profiles.yml

model-paths: ["models"]
seed-paths: ["seeds"]
test-paths: ["tests"]
macro-paths: ["macros"]
snapshot-paths: ["snapshots"]

clean-targets:
  - "target"
  - "dbt_packages"

models:
  my_project:
    staging:
      +materialized: view
    intermediate:
      +materialized: view
    marts:
      +materialized: table
```

### Node Types in Detail

| Node Type | Directory | Description |
|---|---|---|
| **Models** | `models/` | SQL `SELECT` statements materialized as views/tables |
| **Sources** | Defined in YAML (inside `models/`) | Declare upstream raw tables for lineage and freshness |
| **Tests** | `tests/` (singular) + YAML `tests:` blocks (generic) | Data quality assertions |
| **Snapshots** | `snapshots/` | SCD Type-2 tracking |
| **Seeds** | `seeds/` | Small CSV lookup tables |
| **Exposures** | Defined in YAML | Declare downstream consumers (dashboard URLs, etc.) |
| **Metrics** | Defined in YAML | Business metric definitions for the Semantic Layer |
| **Analyses** | `analyses/` | SQL that is *not* materialized (ad-hoc exploration) |

---

## 4. dbt Modeling Concepts (Kimball Star Schema)

The gold standard for dbt projects is the **Kimball dimensional modeling** approach organized into a **layered architecture**:

```
┌─────────────────────────────────────────────────┐
│  Raw Data (EL layer — Fivetran, Airbyte, etc.)  │
│  Tables in warehouse: order_db.orders, etc.     │
└────────────────────┬────────────────────────────┘
                     │ source()
                     ▼
┌─────────────────────────────────────────────────┐
│  Staging Layer   (stg_*)                        │
│  - One model per source table                   │
│  - Light cleaning: rename, cast, deduplicate    │
│  - No joins — 1:1 with source                   │
│  - Materialized as VIEW                         │
└────────────────────┬────────────────────────────┘
                     │ ref()
                     ▼
┌─────────────────────────────────────────────────┐
│  Intermediate Layer  (int_*)                    │
│  - Business-logic transformations               │
│  - Joins across staging models                  │
│  - Pivot/unpivot, aggregations, filtering       │
│  - Usually VIEW (or ephemeral CTE)              │
└────────────────────┬────────────────────────────┘
                     │ ref()
                     ▼
┌─────────────────────────────────────────────────┐
│  Mart Layer  (fct_*, dim_*)                     │
│  - Facts: measures, foreign keys, grain-defining │
│  - Dimensions: descriptive attributes, conformed │
│  - Materialized as TABLE or INCREMENTAL          │
└────────────────────┬────────────────────────────┘
                     │
                     ▼
              Dashboards / Exposures
```

### Staging Models (`stg_*`)

Purpose: clean, type, and rename raw data. Always 1:1 with a source table.

```sql
-- models/staging/stg_orders.sql
WITH source AS (
    SELECT * FROM {{ source('source_name', 'orders') }}
),
renamed AS (
    SELECT
        id              AS order_id,
        customer_id     AS customer_id,
        order_date      AS order_date,
        status          AS order_status,
        amount          AS order_amount,
        -- standard timestamp
        _loaded_at      AS loaded_at
    FROM source
    WHERE id IS NOT NULL
)
SELECT * FROM renamed
```

### Intermediate Models (`int_*`)

Purpose: bridge staging → marts. Common patterns:
- **Pivots**: `int_orders_pivoted` — pivot order statuses into columns
- **Aggregations**: `int_customer_orders` — aggregate orders per customer
- **Joins**: `int_order_items_joined` — join orders to line items

```sql
-- models/intermediate/int_customer_orders.sql
SELECT
    customer_id,
    MIN(order_date)                 AS first_order_date,
    MAX(order_date)                 AS most_recent_order_date,
    COUNT(order_id)                 AS number_of_orders,
    SUM(order_amount)               AS lifetime_value
FROM {{ ref('stg_orders') }}
GROUP BY customer_id
```

### Fact Models (`fct_*`)

- Represent business processes/events (sales, orders, clicks, shipments).
- Contain measures (numeric, additive) and foreign keys to dimensions.
- Grain must be explicitly stated in YAML documentation.

```sql
-- models/marts/fct_orders.sql
SELECT
    order_id,
    customer_id,
    order_date,
    order_amount,
    order_status
FROM {{ ref('stg_orders') }}
```

### Dimension Models (`dim_*`)

- Represent business entities (customer, product, date, store).
- Contain descriptive attributes.
- Are *conformed* (same attributes mean the same thing across facts).

```sql
-- models/marts/dim_customers.sql
SELECT
    customer_id,
    first_name || ' ' || last_name   AS customer_name,
    email,
    city,
    country,
    first_order_date,
    most_recent_order_date,
    number_of_orders,
    lifetime_value
FROM {{ ref('int_customer_orders') }}
```

### Best Practice: Directory Layout Inside `marts/`

```
models/
  marts/
    marketing/
      dim_customers.sql
      fct_customer_attribution.sql
    finance/
      fct_orders.sql
      dim_products.sql
    product/
      fct_sessions.sql
      dim_products.sql     # shared (conformed)
```

Each mart subdirectory gets its own `_models.yml` file for schema/documentation.

---

## 5. dbt Materializations

Materializations determine *how* a model is physically built in the warehouse.

### View (default)

```sql
{{ config(materialized='view') }}
SELECT ...
```

- Creates a `CREATE VIEW AS ...`.
- **Pros**: always up-to-date, no storage cost, fast to create.
- **Cons**: slower to query (especially with nested views), can't add indexes/partitions.
- **Use for**: staging and intermediate models.

### Table

```sql
{{ config(materialized='table') }}
SELECT ...
```

- Creates `CREATE TABLE AS SELECT` (full refresh every run).
- **Pros**: fast queries, can be indexed/clustered.
- **Cons**: expensive to rebuild fully each run, requires storage.
- **Use for**: small-to-medium marts, dimensions.

### Incremental

```sql
{{ config(
    materialized='incremental',
    unique_key='order_id',
    incremental_strategy='merge'  -- or 'insert_overwrite', 'delete+insert'
) }}
SELECT ...
{% if is_incremental() %}
  WHERE updated_at > (SELECT MAX(updated_at) FROM {{ this }})
{% endif %}
```

- Only processes new/changed rows since the last run.
- Strategies: `merge` (Snowflake, Databricks, BigQuery), `insert_overwrite` (BigQuery partitions), `delete+insert` (Redshift, Postgres).
- **Pros**: efficient for large-volume append or upsert workloads.
- **Cons**: more complex, risk of data drift if `unique_key` is wrong or source data is mutated outside incremental window.
- **Use for**: large fact tables, event logs, transaction tables.

### Ephemeral

```sql
{{ config(materialized='ephemeral') }}
SELECT ...
```

- Not materialized at all — becomes a CTE (common table expression) wherever it's `ref()`'d.
- **Pros**: no storage, zero maintenance.
- **Cons**: can't be directly queried, can cause deeply nested CTEs.
- **Use for**: lightweight intermediate transformations that are only used once.

### Comparison

| Materialization | DDL | Storage | Query Speed | Refresh |
|---|---|---|---|---|
| **view** | `CREATE VIEW` | None | Slow | Always live |
| **table** | `CREATE TABLE AS` | Full | Fast | Full refresh |
| **incremental** | `MERGE` / `INSERT` | Full | Fast | Incremental |
| **ephemeral** | None | None | Depends | N/A (CTE) |

---

## 6. dbt Tests

dbt provides a testing framework to assert data quality. Tests are run via `dbt test`.

### Generic Tests (schema tests)

Defined in YAML — reusable assertions against columns:

```yaml
# models/marts/_models.yml
models:
  - name: dim_customers
    columns:
      - name: customer_id
        tests:
          - unique
          - not_null
      - name: email
        tests:
          - unique
          - not_null
      - name: country
        tests:
          - accepted_values:
              values: ['US', 'UK', 'DE', 'FR', 'CA']
  - name: fct_orders
    columns:
      - name: customer_id
        tests:
          - not_null
          - relationships:
              to: ref('dim_customers')
              field: customer_id
```

**Built-in generic tests:**
- `unique` — no duplicate values in column
- `not_null` — no NULL values
- `accepted_values` — column values come from a defined list
- `relationships` — referential integrity (foreign key check)
- Custom ones from packages: `dbt_utils.expression_is_true`, `dbt_expectations.expect_column_values_to_match_regex`, etc.

### Singular Tests (data tests)

Standalone SQL files in `tests/` that return failing rows. Any returned row == test failure.

```sql
-- tests/assert_positive_revenue.sql
SELECT
    order_id,
    order_amount
FROM {{ ref('fct_orders') }}
WHERE order_amount < 0
```

### Custom Generic Tests (test macros)

Create reusable test macros in `macros/tests/`:

```sql
{% test assert_positive(model, column_name) %}
SELECT *
FROM {{ model }}
WHERE {{ column_name }} < 0
{% endtest %}
```

Then use it in YAML:

```yaml
tests:
  - assert_positive
```

### Running Tests

```bash
dbt test                          # run all tests
dbt test --select dim_customers   # test a single model
dbt test --select tag:nightly     # tests tagged 'nightly'
```

**Store test failures:**

```bash
dbt test --store-failures         # persists failures as tables for review
```

### Test Severity (dbt v1.5+)

```yaml
tests:
  - not_null:
      severity: warn   # non-blocking; reported but doesn't fail the run
```

---

## 7. dbt Sources and Source Freshness

### Declaring Sources

Sources define which raw database tables your pipeline starts from.

```yaml
# models/staging/_sources.yml
version: 2

sources:
  - name: jaffle_shop      # logical name
    database: raw_db
    schema: public
    tables:
      - name: orders
        description: "Raw orders from the jaffle_shop transactional system"
        loaded_at_field: _etl_loaded_at
        freshness:
          warn_after: { count: 12, period: hour }
          error_after: { count: 24, period: hour }
        columns:
          - name: id
            description: Primary key
            tests:
              - unique
              - not_null
      - name: customers
        loaded_at_field: _etl_loaded_at
        freshness:
          warn_after: { count: 24, period: hour }
```

### Using Sources in Models

```sql
-- models/staging/stg_orders.sql
SELECT *
FROM {{ source('jaffle_shop', 'orders') }}
```

Using `source()` instead of raw table names gives you:
- **Lineage**: dbt tracks dependencies from models back to source tables.
- **Freshness**: `dbt source freshness` runs timestamp-based checks to detect stale data.

### Source Freshness Command

```bash
dbt source freshness
```

Output: a JSON file `target/sources.json` with per-source freshness results. This can be integrated into monitoring/alerting pipelines. Failures can be flagged as warnings or errors.

### Snapshotting Source Config

In `dbt_project.yml` you can set a blanket source freshness policy:

```yaml
sources:
  jaffle_shop:
    freshness:
      warn_after: { count: 6, period: hour }
    loaded_at_field: _loaded_at
```

---

## 8. dbt Snapshots (Slowly Changing Dimensions)

Snapshots implement **Type 2 Slowly Changing Dimensions (SCD)** — they track historical changes to dimension attributes.

### How Snapshots Work

1. You define a snapshot SQL file in `snapshots/` that `SELECT`s the source data.
2. dbt compares the current source data against the existing snapshot table.
3. If any tracked column changed, dbt **closes** the old row (sets `dbt_valid_to`) and **inserts** a new row (sets `dbt_valid_from`).

### Snapshot Configuration

```sql
-- snapshots/scd_customers.sql
{% snapshot scd_customers %}

{{
    config(
        target_schema='snapshots',
        unique_key='customer_id',
        strategy='check',
        check_cols='all'  -- or ['email', 'city', 'country']
    )
}}

SELECT * FROM {{ source('jaffle_shop', 'customers') }}

{% endsnapshot %}
```

### Snapshot Strategies

| Strategy | Description |
|---|---|
| **`timestamp`** | Uses a `updated_at` column to detect changes (more efficient). Requires `updated_at` column. |
| **`check`** | Compares specified columns (or all columns) for changes. No timestamp needed. |

**Timestamp strategy (preferred when possible):**

```sql
{{
    config(
        target_schema='snapshots',
        unique_key='customer_id',
        strategy='timestamp',
        updated_at='updated_at',
        invalidate_hard_deletes=True
    )
}}
```

### Snapshot Metadata Columns

Every snapshot row gets these columns automatically:

| Column | Meaning |
|---|---|
| `dbt_scd_id` | Surrogate key for the SCD record |
| `dbt_updated_at` | When the row was updated (the `updated_at` value or snapshot run time) |
| `dbt_valid_from` | Start date/time of this version |
| `dbt_valid_to` | End date/time (NULL = current version) |
| `dbt_is_contaminated` | Flag if multiple changes happened between snapshot runs (unusual) |

### Querying Snapshot Tables

```sql
-- Get current customers
SELECT * FROM snapshots.scd_customers WHERE dbt_valid_to IS NULL

-- Get customers as of a specific date
SELECT * FROM snapshots.scd_customers
WHERE '2024-06-01' BETWEEN dbt_valid_from AND COALESCE(dbt_valid_to, '9999-12-31')

-- Full history for a specific customer
SELECT * FROM snapshots.scd_customers
WHERE customer_id = 42
ORDER BY dbt_valid_from
```

---

## 9. dbt Documentation Generation

dbt can auto-generate a static documentation site from your project using `dbt docs generate`.

### What Gets Generated

- **Model lineage** (DAG visualization) via `dbt docs serve` (interactive web UI).
- **Schema/datatype info** from the warehouse (via `dbt docs generate` which runs `dbt run` + `dbt test` + catalog collection).
- **Descriptions** from YAML schema files.
- **Test results** and sources information.

### Adding Documentation

```yaml
# models/marts/_models.yml
version: 2

models:
  - name: dim_customers
    description: >
      Customer dimension table. One row per customer with current attributes
      and aggregated lifetime metrics.
    columns:
      - name: customer_id
        description: "Primary key from the source CRM system"
        tests:
          - unique
          - not_null
      - name: lifetime_value
        description: "Total revenue from this customer (all orders)"
```

### Docs Blocks (reusable markdown)

```sql
-- models/docs.md
{% docs dim_customers_description %}
The **customer dimension** contains one row per customer.
It includes:
- Demographics (name, email, location)
- Behavioral metrics (first/last order date, lifetime value)
{% enddocs %}
```

Referenced in YAML:

```yaml
models:
  - name: dim_customers
    description: "{{ doc('dim_customers_description') }}"
```

### Generating and Serving

```bash
dbt docs generate          # produces target/catalog.json + target/manifest.json
dbt docs serve             # serves docs at http://localhost:8080
dbt docs serve --port 8081
```

### CI Integration

Many teams upload the generated docs to a static hosting service (S3, Netlify, GitHub Pages) as part of CI/CD, so the documentation is always up-to-date with production.

---

## 10. dbt Jinja/SQL Templating and Macros

dbt uses **Jinja** (Python templating engine) to make SQL programmable.

### Basic Jinja in dbt

```sql
SELECT
    order_id,
    {% if include_customer_name %}
        customer_name,
    {% endif %}
    order_amount * {{ multiplier }} AS adjusted_amount
FROM {{ ref('fct_orders') }}
```

### Built-in Jinja Functions

| Function | Purpose |
|---|---|
| `{{ ref('model_name') }}` | Reference another model (creates DAG edge) |
| `{{ source('source_name', 'table') }}` | Reference a declared source |
| `{{ config(...) }}` | Set model-level configuration |
| `{{ this }}` | Current model's database object reference |
| `{{ is_incremental() }}` | Returns `True` if the model is doing an incremental run |
| `{{ var('variable_name') }}` | Access user-defined variables |
| `{{ env_var('ENV_NAME') }}` | Access environment variables |

### Macros

Macros are reusable Jinja-SQL snippets, stored in `macros/`. They are like functions.

**Creating a macro:**

```sql
{# macros/cents_to_dollars.sql #}
{% macro cents_to_dollars(column_name, precision=2) -%}
    ({{ column_name }} / 100.0)::numeric(16, {{ precision }})
{%- endmacro %}
```

**Using a macro:**

```sql
SELECT
    {{ cents_to_dollars('order_amount_cents') }} AS order_amount_dollars
FROM {{ ref('stg_orders') }}
```

### Control Flow

```sql
{% if target.name == 'prod' %}
    -- only run in production
    AND status IN ('shipped', 'delivered')
{% elif target.name == 'dev' %}
    -- sample for development
    LIMIT 1000
{% endif %}
```

### Loops

```sql
{% for column in var('payment_methods') %}
    SUM(CASE WHEN payment_method = '{{ column }}' THEN amount ELSE 0 END) AS {{ column }}_amount
    {%- if not loop.last %},{% endif %}
{% endfor %}
```

### DBT_UTILS Macro Example

```sql
{% set payment_methods = dbt_utils.get_column_values(
    table=ref('stg_payments'),
    column='payment_method'
) %}
```

### Materialized Macro (Advanced)

dbt also provides *dispatcher macros* for adapter-specific SQL:

```sql
{% macro my_custom_merge() %}
  {% if target.type == 'snowflake' %}
    -- Snowflake MERGE syntax
  {% elif target.type == 'bigquery' %}
    -- BigQuery MERGE syntax
  {% endif %}
{% endmacro %}
```

### Best Practices for Macros

- Keep macros in `macros/`, organized by domain (`macros/pricing/`, `macros/logging/`).
- Prefix macros with a package name when distributing (`my_package::macro_name`).
- Document macro arguments with `{% docs %}` blocks.
- Avoid excessive Jinja complexity — it makes SQL harder to read and debug.

---

## 11. dbt Packages

dbt packages are reusable libraries of models, macros, and tests. They are managed via a `packages.yml` file.

### Installing Packages

```yaml
# packages.yml
packages:
  - package: dbt-labs/dbt_utils
    version: 1.1.1
  - package: calogica/dbt_expectations
    version: 0.9.0
  - package: dbt-labs/spark_utils
    version: 0.3.0
  - git: "https://github.com/dbt-labs/dbt-utils.git"
    revision: 0.9.2   # optional
```

Install with:

```bash
dbt deps
```

Packages are installed into the `dbt_packages/` directory.

### dbt_utils (dbt-labs/dbt_utils)

The most widely used dbt package. Key capabilities:

**Cross-database macros:**

| Macro | Purpose |
|---|---|
| `dbt_utils.surrogate_key('col1', 'col2')` | Create a hash-based surrogate key |
| `dbt_utils.datediff('start', 'end', 'day')` | Cross-database date difference |
| `dbt_utils.date_trunc('month', 'date_col')` | Cross-database date truncation |
| `dbt_utils.hash('col')` | Cross-database hash function |
| `dbt_utils.concat(['col1', 'col2'])` | Cross-database concatenation |

**Testing macros:**

| Test | Purpose |
|---|---|
| `dbt_utils.expression_is_true` | Assert that an expression is true |
| `dbt_utils.unique_combination_of_columns` | Composite uniqueness |
| `dbt_utils.mutually_exclusive_ranges` | No overlapping ranges |
| `dbt_utils.cardinality_equality` | Two sources have same set of values |
| `dbt_utils.recency` | Max timestamp is recent enough |

**Schema/table utilities:**

| Macro | Purpose |
|---|---|
| `dbt_utils.get_column_values()` | Return list of column values |
| `dbt_utils.get_tables_by_pattern()` | Find tables matching a pattern |
| `dbt_utils.get_query_results_as_dict()` | Run any SQL return results |

**Schema tests (YAML):**

```yaml
tests:
  - dbt_utils.expression_is_true:
      expression: "order_amount >= 0"
  - dbt_utils.unique_combination_of_columns:
      combination_of_columns:
        - order_id
        - line_item_id
```

### dbt_expectations (calogica/dbt_expectations)

Inspired by the Python `great_expectations` library. Provides dozens of data-quality tests.

**Common tests:**

| Test | Purpose |
|---|---|
| `expect_column_values_to_match_regex` | Regex validation |
| `expect_column_values_to_be_between` | Range check |
| `expect_column_values_to_be_in_set` | Set membership |
| `expect_column_distinct_count_to_equal` | Exact distinct count |
| `expect_column_values_to_not_be_null` | Not-null (adds threshold support) |
| `expect_table_row_count_to_be_between` | Row count range |
| `expect_column_pair_values_A_to_be_greater_than_B` | Cross-column comparison |
| `expect_queried_row_count_to_be_between` | Dynamic SQL row count |
| `expect_queried_column_value_frequency_to_be_between` | Value frequency checks |
| `expect_table_columns_to_match_ordered_list` | Schema validation |

### Other Notable Packages

| Package | Purpose |
|---|---|
| `dbt-labs/audit_helper` | Compare row counts and values between two inputs |
| `dbt-labs/dbt-artifacts` | Parse dbt artifacts into warehouse tables |
| `dbt-labs/date_spine` | Generate date spines for calendar dimensions |
| `dbt-labs/codegen` | Auto-generate base models and YAML from source tables |
| `elementary-data/elementary` | Data monitoring, alerting, and observability |
| `re-data/re_data` | Data reliability and anomaly detection |
| `infinitelambda/dbt_ml` | ML preprocessing utilities in dbt |

---

## 12. dbt CI/CD Integration Patterns

### Pattern 1: dbt Cloud CI

1. Create a **Merge Request / Pull Request** on GitHub/GitLab.
2. dbt Cloud's CI job fires automatically.
3. It creates a **temporary schema** with the PR's changes.
4. Runs `dbt build --select state:modified+` to run only changed models and their downstream tests.
5. Reports results back as a PR check.

**Key commands:**

```bash
# Compare against production manifest
dbt build --select state:modified+ --defer --state target-prod/
```

Where `--defer` means "use production tables for unmodified models" and `state:modified+` selects changed models plus everything downstream.

### Pattern 2: dbt Core + GitHub Actions

```yaml
# .github/workflows/dbt-ci.yml
name: dbt CI
on:
  pull_request:
    branches: [main]

jobs:
  dbt-ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Install dependencies
        run: |
          pip install dbt-snowflake dbt-utils
          dbt deps
      - name: dbt build (CI)
        env:
          DBT_USER: ${{ vars.DBT_USER }}
          DBT_PASSWORD: ${{ secrets.DBT_PASSWORD }}
        run: |
          dbt build --target ci --select state:modified+ --defer
```

### Pattern 3: dbt + Airflow

Use the `Cosmos` library (by Astronomer) to run dbt inside Airflow DAGs:

```python
from cosmos import DbtDag, ProjectConfig, ProfileConfig
from pendulum import datetime

dbt_dag = DbtDag(
    project_config=ProjectConfig("/path/to/dbt_project"),
    profile_config=ProfileConfig(
        profile_name="my_project",
        target_name="prod",
        profiles_yml_filepath="/path/to/profiles.yml",
    ),
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    default_args={"retries": 2},
    tags=["dbt"],
)
```

### Pattern 4: Slim CI (state-based)

```bash
# In production: upload manifest.json as an artifact
dbt run                          # full run
dbt docs generate
cp target/manifest.json target-prod/manifest.json

# In CI: download production manifest, run slim CI
dbt build --select state:modified+ --defer --state target-prod/
```

### Environment Strategy

```yaml
# dbt_project.yml
models:
  +post-hook:
    - "GRANT SELECT ON {{ this }} TO ROLE ANALYST_ROLE"   # only in prod
    - "{{ 'GRANT SELECT ON {{ this }} TO ROLE DEV_ROLE' if target.name == 'dev' else '' }}"
```

**Recommended targets:**

| Target | Purpose | Schema Suffix |
|---|---|---|
| `dev` | Individual developer | `_dev_<username>` |
| `ci` | PR validation | `_pr_<number>` |
| `staging` | Pre-production | `_staging` |
| `prod` | Production | (none) |

---

## 13. dbt Mesh / Multi-Project Deployments

dbt Mesh is dbt Labs' solution for scaling dbt across multiple teams and domains, enabling **decentralized ownership with centralized governance**.

### The Problem dbt Mesh Solves

- A single monolithic dbt project becomes unwieldy at scale (1000+ models, 10+ teams).
- Teams need to own their data independently but depend on models from other teams.
- No cross-project visibility or contracts between teams.

### Key Concepts

| Concept | Description |
|---|---|
| **Multi-project collaboration** | Different teams maintain separate dbt repos/projects |
| **Cross-project `ref`** | Use `ref('model_name')` across projects via `dependencies.yml` |
| **Model contracts** | Enforced column names, types, and constraints on public models |
| **Access control** | `public` / `protected` / `private` model access modifiers |
| **Versioning** | Semantic versioning for model contracts |
| **Discovery API** | Query metadata across all projects |

### Setting Up dbt Mesh

**Producer (upstream) project:**

```yaml
# models/_models.yml
models:
  - name: dim_customers
    access: public             # can be used by other projects
    config:
      contract:
        enforced: true
    columns:
      - name: customer_id
        data_type: int
        constraints: [not_null, unique]
      - name: customer_name
        data_type: varchar(256)
      - name: email
        data_type: varchar(256)
```

**Consumer (downstream) project:**

```yaml
# dependencies.yml
packages:
  - name: upstream_core
    version: 1.0.0
    # For dbt Cloud:
    #   (handled via Project Dependencies UI)
    # For dbt Core (with dbt-loom or similar):
    git: "https://github.com/team-a/dbt-core-project.git"
```

```sql
-- models/marts/fct_orders.sql
SELECT *
FROM {{ ref('upstream_core', 'dim_customers') }}  -- cross-project ref
```

### Model Contracts

Contracts enforce a "schema on write" for downstream consumers:

```yaml
models:
  - name: dim_customers
    config:
      contract:
        enforced: true  # dbt will fail if the model's SQL doesn't match the declared columns
    columns:
      - name: customer_id
        data_type: int
        constraints:
          - type: not_null
          - type: primary_key
      - name: email
        data_type: varchar(256)
```

### Benefits

- **Team autonomy**: Each team manages their own dbt project, CI/CD, and deployments.
- **Governance**: Model contracts prevent breaking changes across teams.
- **Scalability**: Reduced DAG complexity per project, faster CI, independent deploy cycles.
- **Reusability**: Shared domain models (e.g., `dim_customers`, `dim_dates`) are versioned and consumed by many projects.

### Tools for Multi-Project Without dbt Cloud

| Tool | Description |
|---|---|
| **dbt-loom** | Open-source CLI tool for cross-project `ref()` resolution in dbt Core |
| **dbt-meshify** | CLI by dbt Labs to assist splitting monolithic projects |
| **Custom scripts** | `git submodule` or multi-repo CI strategies |

---

## Appendix A: Essential dbt Commands

```bash
dbt init <project_name>       # Create a new dbt project
dbt deps                      # Install packages from packages.yml
dbt debug                     # Verify warehouse connection
dbt seed                      # Load CSV files (seeds)
dbt run                       # Execute all models
dbt run --select +model_name  # Run a model + its upstream dependencies
dbt run --select model_name+  # Run a model + its downstream dependents
dbt run --exclude tag:stale   # Run everything except models tagged 'stale'
dbt test                      # Run all tests
dbt test --select model_name  # Run tests only for a specific model
dbt build                     # seed + run + test (in one command, DAG-ordered)
dbt snapshot                  # Execute snapshots
dbt source freshness           # Check source table freshness
dbt docs generate             # Build documentation
dbt docs serve                # Serve documentation locally
dbt ls                        # List all resources (models, tests, etc.)
dbt compile                   # Compile SQL without executing
dbt parse                     # Validate project without running anything
```

## Appendix B: YAML Schema File Pattern

Organize YAML files alongside models. Naming convention:

| File | Contains |
|---|---|
| `_sources.yml` | Source declarations |
| `_models.yml` | Model descriptions, column docs, tests |
| `_metrics.yml` | Metric definitions |
| `_exposures.yml` | Exposure declarations |
| `_macros.yml` | Macro documentation |

## Appendix C: Key Resources

- [Official dbt Documentation](https://docs.getdbt.com/)
- [dbt GitHub (dbt-core)](https://github.com/dbt-labs/dbt-core)
- [dbt_utils Package](https://github.com/dbt-labs/dbt-utils)
- [dbt_expectations Package](https://github.com/calogica/dbt-expectations)
- [dbt Discourse Community](https://discourse.getdbt.com/)
- [dbt Best Practices Guide](https://docs.getdbt.com/best-practices)
- [dbt Mesh Docs](https://docs.getdbt.com/docs/mesh)

---

*Document produced for data-engineering methodology skill reference. June 2026.*
