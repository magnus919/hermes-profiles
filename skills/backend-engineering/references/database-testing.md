# Backend Engineering Methodology Reference

> Database access patterns & service-level testing — a comprehensive reference for backend engineering teams.
> Compiled: 2026-06-05

---

## Table of Contents

1. [Connection Pooling Configuration & Sizing](#1-connection-pooling-configuration--sizing)
2. [Query Optimization — Index Usage, Query Plans, EXPLAIN](#2-query-optimization--index-usage-query-plans-explain)
3. [N+1 Detection & Mitigation](#3-n1-detection--mitigation)
4. [Pagination Strategies — Cursor vs Offset vs Keyset](#4-pagination-strategies--cursor-vs-offset-vs-keyset)
5. [Transaction Boundary Design](#5-transaction-boundary-design)
6. [Read/Write Splitting](#6-readwrite-splitting)
7. [Replication Lag Handling](#7-replication-lag-handling)
8. [Service-Level Testing Overview](#8-service-level-testing-overview)
9. [Unit Testing Business Logic](#9-unit-testing-business-logic)
10. [Integration Testing — API Contracts, Testcontainers, WireMock](#10-integration-testing--api-contracts-testcontainers-wiremock)
11. [Contract Testing — Pact](#11-contract-testing--pact)
12. [Test Fixtures](#12-test-fixtures)
13. [CI Integration](#13-ci-integration)

---

## 1. Connection Pooling Configuration & Sizing

### The Problem

Creating a new TCP connection per request does not scale. At 10K+ RPS, the database is overwhelmed. PostgreSQL defaults to 100 simultaneous connections; exceeding that produces "sorry, too many clients already." Each new connection setup adds 20-50 ms of latency.

### The Solution

Connection pooling pre-establishes a fixed set of connections at application startup. Threads borrow a connection, execute queries, and return it to the pool.

```
┌──────────────┐     borrow     ┌──────────────────┐
│  App Thread  │ ─────────────→ │   Connection     │
│  (request)   │                │     Pool         │
│              │ ←───────────── │  (HikariCP/      │
│              │    return      │   pgBouncer)     │
└──────────────┘                └────────┬─────────┘
                                        │
                              ┌─────────▼─────────┐
                              │  Database Server   │
                              │  (PostgreSQL/MySQL)│
                              └───────────────────┘
```

### Pool Sizing Formula

The most commonly cited rule of thumb: **pool size = 2x (number of CPU cores)**.

However, the correct approach is empirical:

1. **Start small** — 20-30 connections for most services.
2. **Run load tests** with real traffic patterns. Monitor DB CPU, memory, connection wait times, and query latency.
3. **Add a 15-20% buffer** above measured peak usage.
4. **Consider multiple pools** for distinct workload patterns (e.g., small pool for admin queries, larger for user-facing traffic).

### Key Configuration Parameters

| Parameter | Description | Common Default |
|-----------|-------------|---------------|
| `maximumPoolSize` | Max connections in the pool | 10-30 |
| `minimumIdle` | Min idle connections to maintain | same as maxPoolSize |
| `connectionTimeout` | Max wait time for a connection (ms) | 30000 |
| `idleTimeout` | Max time a connection stays idle (ms) | 600000 (10 min) |
| `maxLifetime` | Max lifetime of a connection in pool (ms) | 1800000 (30 min) |

### Recommended Libraries

| Language | Library | Notes |
|----------|---------|-------|
| Java/Kotlin | **HikariCP** | Industry standard — fastest, lightest |
| Python | **psycopg2.pool / SQLAlchemy pool** | Built-in; tune pool_size and max_overflow |
| Node.js | **pg-pool** | Default pool for node-postgres |
| Go | **pgxpool** (/jackc/pgx) | High-performance Postgres driver |
| Ruby | **connection_pool** | Used by ActiveRecord internally |
| Rust | **deadpool-postgres** | Async pool for tokio-postgres |
| .NET | **Npgsql pooling (built-in)** | Connection pooling enabled by default |

### Proxy-Based Pooling (pgBouncer / PgCat)

For microservices or serverless, use a database proxy instead of app-level pooling:

```ini
[databases]
mydb = host=localhost port=5432 dbname=mydb

[pgbouncer]
listen_addr = 127.0.0.1
listen_port = 6432
pool_mode = transaction    # transaction-level pooling
max_client_conn = 100
default_pool_size = 20
```

- **Transaction pooling** — connections are returned to pool after each transaction (most common).
- **Session pooling** — connection held for entire session (useful for prepared statements).
- **Statement pooling** — connection returned after each statement (rarest).

### Serverless Considerations

Serverless functions are short-lived and cannot maintain persistent pools. Use proxy-based solutions:

- **AWS RDS Proxy** (managed, IAM auth)
- **Cloudflare Hyperdrive**
- **Supabase Supavisor**
- **PgCat** (open-source proxy)

---

## 2. Query Optimization — Index Usage, Query Plans, EXPLAIN

### Index Types (PostgreSQL-focused)

| Index Type | Best For | Considerations |
|------------|----------|---------------|
| **B-Tree** (default) | Equality & range queries, ORDER BY, foreign keys | General-purpose; works for most cases |
| **Hash** | Equality lookups only | Single-column; not WAL-logged in older versions |
| **GIN** (Generalized Inverted Index) | Full-text search, arrays, JSONB containment | Larger than B-tree; slower to build |
| **GiST** (Generalized Search Tree) | Geometric data, full-text search (ranking) | Lossy; supports nearest-neighbor |
| **BRIN** (Block Range INdex) | Very large tables with naturally ordered data (time-series, logs) | Extremely compact; only good for correlated data |
| **SP-GiST** | Space-partitioned data (maps, network trees) | Niche; for clustered data |
| **Covering Index** (`INCLUDE` columns) | Index-only scans | Adds payload columns without affecting key sort order |

### Composite Index Guidelines

- **Order matters**: column(s) for equality first, then range/ORDER BY columns.
- **Leftmost prefix rule**: a query must use the leftmost columns in the index to benefit from it.
- Example: `CREATE INDEX idx_users_org_status ON users (organization_id, status, created_at);`
  - Helps `WHERE org_id = ? AND status = ? ORDER BY created_at`
  - Does NOT help `WHERE status = ?` alone.

### EXPLAIN Fundamentals

```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) SELECT * FROM orders WHERE user_id = 42;
```

**Key plan node types:**

| Node | Meaning |
|------|---------|
| **Seq Scan** | Full table scan — expensive on large tables |
| **Index Scan** | Index lookup + heap fetch |
| **Index Only Scan** | All needed columns in the index itself (fastest) |
| **Bitmap Heap Scan** | Multiple index matches combined into a bitmap |
| **Nested Loop** | For each row in outer, scan inner (good for small joins) |
| **Hash Join** | Build hash table on one side, probe with other |
| **Merge Join** | Sort both sides, merge (good for large sorted sets) |

### What to Look For in a Query Plan

1. **Sequential scans on large tables** — missing index.
2. **High `rows` vs `actual rows` discrepancy** — planner has stale statistics; run `ANALYZE`.
3. **`Sort` nodes with large memory** — consider pre-sorted index or increased `work_mem`.
4. **`Nested Loop` joining large row sets** — might need a different join strategy.
5. **`Bitmap Heap Scan` with many row versions** — vacuum might be needed.
6. **`Filter` after index scan** — index is missing a column used in WHERE.

### Index Maintenance

```sql
-- Check index usage
SELECT schemaname, tablename, indexname, idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes
WHERE idx_scan = 0;  -- unused indexes (candidates for removal)

-- Rebuild bloated indexes
REINDEX INDEX CONCURRENTLY idx_name;   -- non-blocking in PG 12+
```

### Common Anti-Patterns

- Indexing low-cardinality columns (e.g., boolean) alone — not selective enough.
- Over-indexing — each index adds write overhead (INSERT/UPDATE/DELETE slower).
- Missing composite indexes for common query patterns.
- `SELECT *` pulling columns not covered by the index, forcing heap lookups.
- Function calls on indexed columns (`WHERE LOWER(email) = 'x'`) unless using a functional index.

---

## 3. N+1 Detection & Mitigation

### What Is N+1?

The N+1 selects problem occurs when an application issues 1 query to fetch N parent rows, then issues N additional queries to fetch related data for each parent — N+1 total queries instead of a single efficient query.

### Example (ORM-level Pseudocode)

```python
# N+1: 1 query for users + N queries for orders
users = User.query.all()              # 1 query → 100 users
for user in users:
    orders = user.orders               # 100 queries!
    ...
```

```sql
-- Queries generated:
SELECT * FROM users;                                       -- 1
SELECT * FROM orders WHERE user_id = 1;                    -- 2
SELECT * FROM orders WHERE user_id = 2;                    -- ...
SELECT * FROM orders WHERE user_id = 100;                  -- 101
```

### Detection Techniques

1. **ORM query logging** — enable SQL logging and watch for repeated similar queries.
2. **APM tools** — Scout, New Relic, Datadog highlight N+1 patterns automatically.
3. **Manual EXPLAIN** — detect many identical queries in a short window.
4. **Static analysis** — Rails' `bullet` gem, Django's `nplusone`, Java's `jpa-nplusone`.
5. **Database-side analysis** — `pg_stat_statements` showing high call counts.

### Mitigation Strategies

| Strategy | ORM | How |
|----------|-----|-----|
| **Eager loading (JOIN)** | Django `select_related` / Rails `includes` / Hibernate `JOIN FETCH` | Single query with JOIN |
| **Batch loading** | Django `prefetch_related` / Rails `preload` / Hibernate `@BatchSize` | Separate query per table, batched with `WHERE IN` |
| **GraphQL DataLoader** | Any GraphQL stack | Per-request batching & deduplication |
| **Lazy + batch** | Common in ORMs | Delay execution until accessed, then batch |

```python
# Fix with eager loading (Django)
users = User.objects.select_related('profile').prefetch_related('orders').all()

# Fix with DataLoader (GraphQL)
from promise import Promise
from promise.dataloader import DataLoader

class OrderLoader(DataLoader):
    def batch_load_fn(self, user_ids):
        orders = Order.objects.filter(user_id__in=user_ids)
        return Promise.resolve([list(orders.filter(user_id=uid)) for uid in user_ids])
```

### When N+1 Is Acceptable

- Small, fixed N (e.g., < 10 related items).
- Admin panels or reports where latency is not critical.
- Cached results with low cache-miss volume.

---

## 4. Pagination Strategies — Cursor vs Offset vs Keyset

### Offset/Limit (Most Common, Least Scalable)

```sql
SELECT * FROM orders ORDER BY created_at DESC LIMIT 20 OFFSET 0;
SELECT * FROM orders ORDER BY created_at DESC LIMIT 20 OFFSET 20;
```

**Pros:**
- Simple to implement.
- Supports arbitrary page jumps (page 1, page 5, page 100).
- Intuitive for developers.

**Cons:**
- **Performance degrades with page depth** — OFFSET 100000 must scan/skip 100K rows.
- **Phantom reads / missing rows** — if rows are inserted/deleted between requests, items may appear on multiple pages or be skipped entirely.
- **Inconsistent under write load** — `OFFSET` changes meaning as data shifts.

### Cursor-Based Pagination (Most Scalable, API-First)

```sql
-- First page: no cursor
SELECT * FROM orders ORDER BY created_at DESC LIMIT 20;

-- Next page: use the last item's cursor value
SELECT * FROM orders
WHERE created_at < '2026-06-04T12:00:00Z'  -- cursor value
ORDER BY created_at DESC LIMIT 20;
```

```json
// API response shape
{
  "data": [...],
  "pagination": {
    "next_cursor": "eyJpZCI6MTIzNDUsImNyZWF0ZWRfYXQiOiIyMDI2LTA2LTA0VDEyOjAwOjAwWiJ9",
    "has_more": true
  }
}
```

**Pros:**
- **O(1) performance at any depth** — uses index seek, not scan+skip.
- **Consistent** — no phantom reads or missed rows; cursor marks a fixed position.
- **Resilient to write load** — insertion/deletion doesn't shift cursor position.

**Cons:**
- No arbitrary page jumping (only next/prev).
- Requires a unique, sortable column (usually an ID or timestamp).
- Cursor encoding/decoding overhead (base64, opaque tokens).

### Keyset Pagination (Seek Method)

```sql
-- Composite pagination on (created_at, id)
SELECT * FROM orders
WHERE (created_at, id) < ('2026-06-04T12:00:00Z', 12345)
ORDER BY created_at DESC, id DESC
LIMIT 20;
```

- Uses a composite index on `(created_at, id)`.
- Similar performance to cursor-based — index seek on the tuple.
- Requires a compound comparison and a multi-column index.

### Comparison Table

| Aspect | Offset/Limit | Cursor | Keyset |
|--------|-------------|--------|--------|
| **Performance at depth** | O(n) — degrades | O(1) — constant | O(1) — constant |
| **Random page access** | Yes | No | No |
| **Phantom reads** | Yes | No | No |
| **Consistency** | Unstable | Stable | Stable |
| **Implementation complexity** | Trivial | Medium | Low-Medium |
| **Requires sortable unique column** | No | Yes | Yes |
| **Write-aware** | No | Yes | Yes |

### Recommendation

| Use Case | Strategy |
|----------|----------|
| **Admin panels, small datasets** | Offset/Limit (fine for < 10K rows) |
| **Public APIs, infinite scroll** | Cursor (REST/GraphQL best practice) |
| **Time-series, logs, audit trails** | Cursor or Keyset on timestamp + ID |
| **Internal tools with DB pagination** | Keyset (lowest complexity, no cursor encoding) |

---

## 5. Transaction Boundary Design

### ACID Properties

| Property | Meaning |
|----------|---------|
| **Atomicity** | All or nothing — transaction either completes fully or has no effect |
| **Consistency** | Transaction leaves DB in a valid state (constraints preserved) |
| **Isolation** | Concurrent transactions do not interfere with each other |
| **Durability** | Committed changes persist through failures |

### Isolation Levels

| Level | Dirty Read | Non-Repeatable Read | Phantom Read | Serialization Anomaly |
|-------|-----------|--------------------|-------------|---------------------|
| **Read Uncommitted** | Possible | Possible | Possible | Possible |
| **Read Committed** (default in PostgreSQL, SQL Server, Oracle) | Safe | Possible | Possible | Possible |
| **Repeatable Read** | Safe | Safe | Possible (PG: safe) | Possible |
| **Serializable** | Safe | Safe | Safe | Safe |

**PostgreSQL specifics:**
- Default is **Read Committed**.
- Repeatable Read also prevents phantom reads (uses snapshot isolation).
- Serializable uses Serializable Snapshot Isolation (SSI) — detects serialization conflicts and aborts.

### Choosing an Isolation Level

```sql
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
-- or for the session:
SET default_transaction_isolation = 'repeatable read';
```

| Level | When to Use |
|-------|------------|
| **Read Committed** | Default for most workloads. Good balance of consistency and performance. |
| **Repeatable Read** | Financial calculations, reporting — when you need consistent snapshots. |
| **Serializable** | Critical data integrity (ledgers, inventory allocation). Higher abort rate. |

### Transaction Retry Patterns

**Optimistic retry (for Serializable / Repeatable Read conflicts):**

```
RETRY_COUNT = 0
MAX_RETRIES = 3
BACKOFF = [50ms, 150ms, 500ms]

WHILE RETRY_COUNT <= MAX_RETRIES:
    BEGIN TRANSACTION
    TRY:
        -- business logic
        COMMIT
        BREAK
    CATCH serialization_failure:
        ROLLBACK
        SLEEP(BACKOFF[RETRY_COUNT])
        RETRY_COUNT += 1
    CATCH deadlock:
        ROLLBACK
        SLEEP(random 0-100ms)
        RETRY_COUNT += 1

IF RETRY_COUNT > MAX_RETRIES:
    RAISE "Transaction failed after retries"
```

**Best practices:**
- Use **exponential backoff** with jitter to avoid thundering herd.
- Keep transactions **short** — minimize lock duration.
- **Read before write** — detect conflicts early inside the transaction.
- Use **optimistic locking** (version column) for entity-level concurrency instead of pessimistic locks when possible.

### Distributed Transactions

| Pattern | Description | When to Use |
|---------|-------------|------------|
| **Two-Phase Commit (2PC)** | Coordinator prepares all participants, then commits | Within a single database system only |
| **Saga (Choreography)** | Each service publishes events; compensating actions roll back | Microservices, async boundaries |
| **Saga (Orchestration)** | Central orchestrator sends commands and handles compensation | Complex multi-service workflows |
| **Outbox Pattern** | Write events to an outbox table in the same DB transaction, then async publish | Event-driven architecture with exactly-once guarantees |
| **Idempotency Keys** | Unique key per operation prevents duplicate processing | Payment handling, any external API call |

### Transaction Anti-Patterns

- **Long-running transactions** that hold locks — split into smaller units.
- **Nested transactions** across service boundaries — use Sagas instead.
- **Transaction inside a loop** — batch the work into a single transaction.
- **Mixing heavy I/O inside a transaction** — external API calls should happen before or after.
- **Not handling retries** for serialization failures — every Serializable workload needs retry logic.

---

## 6. Read/Write Splitting

### Architecture

```
                    ┌─────────────────┐
                    │   Application    │
                    │  (ORM / Client)  │
                    └────┬────────┬───┘
                         │        │
                    Writes     Reads
                         │        │
                    ┌────▼──┐ ┌──▼────┐
                    │Primary│ │Replica│ ──→ (more replicas)
                    │(Write)│ │(Read) │
                    └───────┘ └───────┘
                        │          ↑
                        │  Async   │
                        │  Repl.   │
                        └──────────┘
```

### Implementation Approaches

| Approach | Mechanism | Pros | Cons |
|----------|-----------|------|------|
| **ORM-level** (`read_from=replica`) | Config in ORM (Django `DATABASES`, Rails `config`) | Simple; no infra change | Every service must configure manually |
| **Database Proxy** (ProxySQL, PgBouncer, PgCat) | Route based on query type | Centralized; no app changes | Extra hop; proxy becomes SPOF |
| **Middleware** (e.g., Spring `@Transactional(readOnly=true)`) | Annotation-driven routing | Fine-grained control; declarative | Framework-specific |
| **Client-side** (multi-DB driver config) | Connection string per role | Minimal infra | Deploy-time configuration |

### Query Routing Rules

```
Writes → Primary:
  - INSERT, UPDATE, DELETE, MERGE
  - DDL (CREATE TABLE, ALTER)
  - SELECT ... FOR UPDATE (needs primary)
  - SELECT inside a read-write transaction

Reads → Replica:
  - SELECT (no locking)
  - Read-only transactions (@Transactional(readOnly=true))
  - Reporting queries, analytics
```

### When NOT to Read from Replicas

- **Read-after-write** queries — data may not have replicated yet.
- **Strong consistency** requirements (ledgers, inventory).
- **Tightly coupled** workflows where the next read depends on the previous write.

### Spring Boot Example (ReadWriteSplit Routing)

```java
@Transactional(readOnly = true)
public OrderDTO getOrder(Long id) { ... }  // routed to replica

@Transactional
public OrderDTO createOrder(OrderDTO dto) { ... }  // routed to primary
```

Configure `AbstractRoutingDataSource` with a `@ReadOnlyRepository` annotation or AOP advice to switch between primary and replica `DataSource`.

---

## 7. Replication Lag Handling

### The Problem

Asynchronously replicated databases always have some lag between write on the primary and visibility on replicas. This causes:

- **Read-after-write inconsistency** — user creates a resource, then immediately gets a 404 reading from a stale replica.
- **Monotonic read violation** — user sees a newer version of data, then an older version (from a different replica).
- **Causality violations** — entity A's state depends on entity B, but B's update hasn't arrived yet.

### Handling Strategies

| Strategy | Description | Complexity |
|----------|-------------|------------|
| **Read-your-writes (RYW)** | Route reads for recently-written data to the primary | Low |
| **Monotonic reads** | Route a session's reads to the same replica | Low |
| **Bounded staleness** | Reject reads from replicas lagging beyond a threshold | Medium |
| **Causal consistency (GTID)** | Track which transaction IDs the client has seen; ensure replica applies those before serving reads | Medium |
| **Wait-for-replication** | After write, wait for replica to catch up before serving reads | Medium |
| **Synchronous replication** | Primary waits for N replicas before committing | High (latency cost) |

### Read-Your-Writes (RYW) Pattern

```python
class DatabaseRouter:
    def __init__(self):
        self.recent_writes = {}  # user_id → timestamp

    def execute_write(self, user_id, query, params):
        result = primary.execute(query, params)
        self.recent_writes[user_id] = time.now()
        return result

    def execute_read(self, user_id, query, params):
        last_write = self.recent_writes.get(user_id, 0)
        if time.now() - last_write < 5:  # 5-second window
            return primary.execute(query, params)  # use primary
        else:
            return replica.execute(query, params)  # use replica
```

### Monotonic Read Consistency (Shopify Pattern)

Route all related reads to the **same replica** using a hash-based sticky selection:

```sql
/* consistent_read_id:user_42 */ SELECT * FROM orders WHERE user_id = 42;
```

```
Hash("user_42") % NUM_REPLICAS = replica_index → always hits the same server
```

**Trade-off:** Simple and low-overhead; occasional inconsistency if that replica goes down.

### Wait-for-Replication

```python
def write_and_wait(data):
    primary.execute("INSERT INTO ...", data)
    # Wait for the write to arrive on at least one replica
    primary.execute("SELECT pg_current_wal_lsn()")  # Postgres
    # or use pg_stat_replication

def read_with_consistency(key):
    # Check that replica has caught up to a known LSN
    replica_lsn = replica.execute("SELECT pg_last_wal_replay_lsn()")
    if replica_lsn >= required_lsn:
        return replica.read(key)
    else:
        return primary.read(key)  # fallback to primary
```

### Strategies by Use Case

| Use Case | Recommended Strategy |
|----------|---------------------|
| **User-facing web app after form submit** | Read-your-writes (route to primary for 5-30s) |
| **Social feed, timeline** | Monotonic reads (sessions stick to one replica) |
| **Analytics, reporting** | Bounded staleness acceptable; lag of minutes is fine |
| **Inventory, financial ledger** | Always read from primary (strong consistency) |
| **Notifications** | Accept eventual consistency; timestamp-driven dedup |

---

## 8. Service-Level Testing Overview

```
                     Coverage ▲
                              │
                    ┌─────────┤
                    │  E2E    │   Few, slow, expensive
                ┌───┤  Tests  │
                │   └─────────┤
            ┌───┤            │
            │   │   Service  │   Medium count, medium speed
        ┌───┤   │  (Integ.) │
        │   │   └───────────┤
    ┌───┤   │              │
    │   │   │    Unit      │   Many, fast, cheap
    │   │   │    Tests     │
    └───┴───┴──────────────┘
```

The **Test Pyramid** recommends:
- **Unit tests**: ~70% — fast, deterministic, test business logic in isolation.
- **Integration tests**: ~20% — test boundaries (DB, external APIs).
- **Contract tests**: ~5% — verify API agreements between services.
- **E2E tests**: ~5% — happy-path critical flows.

---

## 9. Unit Testing Business Logic

### Principles

- **Test in isolation** — mock/stub all collaborators (DB, file system, network).
- **Focus on logic** — test business rules, transformations, validations, and state changes.
- **Deterministic** — no flaky tests. No external dependencies.
- **Fast** — individual tests complete in milliseconds.

### What to Unit Test

```python
# GOOD: Pure business logic — test this
class OrderService:
    def calculate_discount(self, order_total, customer_tier):
        if customer_tier == 'vip':
            return order_total * 0.20
        elif order_total > 1000:
            return order_total * 0.10
        else:
            return 0

# BAD: Impure — involves I/O, mock the boundary instead
class OrderController:
    def create_order(self, request):
        order = Order(...)
        db.save(order)          # this is an integration concern
        notification.send(order) # mock this in unit tests
        return order
```

### Repository/Data Layer Abstraction

Use the **Repository Pattern** to make business logic testable:

```java
// Business logic — unit testable with mock repository
public class OrderFulfillmentService {
    private final OrderRepository orderRepo;
    private final InventoryClient inventoryClient;

    public FulfillmentResult fulfillOrder(String orderId) {
        Order order = orderRepo.findById(orderId);
        if (order == null) return FulfillmentResult.notFound();

        boolean inStock = inventoryClient.checkStock(order.getSku(), order.getQuantity());
        if (!inStock) return FulfillmentResult.outOfStock();

        order.setStatus(OrderStatus.FULFILLED);
        orderRepo.save(order);
        return FulfillmentResult.success();
    }
}
// Unit test: Mock orderRepo and inventoryClient, test all branches
```

### Testing Patterns

| Pattern | Description |
|---------|-------------|
| **Given-When-Then** | Arrange → Act → Assert structure |
| **Parameterized tests** | Test many input combinations with one test method |
| **Property-based testing** | Generate random inputs, assert invariants hold |
| **State-based vs Interaction-based** | Prefer state assertions over verifying mock interactions |

---

## 10. Integration Testing — API Contracts, Testcontainers, WireMock

### Testcontainers

**What:** Library that provides lightweight, disposable containers for testing (PostgreSQL, Redis, Kafka, etc.) as JUnit `@Rule` / `@Container`.

**Why real containers instead of in-memory:**

| Approach | Issues |
|----------|--------|
| **H2 (in-memory)** | Different SQL dialect, missing features, different behavior under load |
| **SQLite** | No JSONB, no PostGIS, no full-text search, different type coercion |
| **Testcontainers** | Real PostgreSQL/MySQL — 100% behavior match |

**Example (Java / Spring Boot + Testcontainers):**

```java
@SpringBootTest
@Testcontainers
class UserRepositoryIntegrationTest {

    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16")
        .withDatabaseName("testdb")
        .withUsername("test")
        .withPassword("test");

    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
    }

    @Autowired
    private UserRepository userRepository;

    @Test
    void shouldPersistAndRetrieveUser() {
        User user = new User("alice@example.com", "Alice");
        User saved = userRepository.save(user);

        Optional<User> found = userRepository.findByEmail("alice@example.com");
        assertThat(found).isPresent();
        assertThat(found.get().getName()).isEqualTo("Alice");
    }
}
```

**Testcontainers in other languages:**

| Language | Library |
|----------|---------|
| Python | `testcontainers` (pip) |
| Node.js | `testcontainers` (npm) |
| Go | `testcontainers-go` |
| .NET | `Testcontainers for .NET` |
| Rust | `testcontainers` (crate) |

### WireMock

**What:** HTTP-based API mock server. Stub external HTTP services during integration tests.

```java
@SpringBootTest
@WireMockTest(httpPort = 8089)
class PaymentServiceIntegrationTest {

    @Test
    void shouldProcessPaymentWhenGatewayRespondsSuccess() {
        // Arrange: stub the external payment gateway
        stubFor(post(urlEqualTo("/gateway/charge"))
            .willReturn(aResponse()
                .withStatus(200)
                .withHeader("Content-Type", "application/json")
                .withBody("""
                    { "status": "success", "transaction_id": "txn_123" }
                """)));

        // Act
        PaymentResult result = paymentService.charge(new Payment("user_1", 50.00));

        // Assert
        assertThat(result.isSuccess()).isTrue();
        assertThat(result.getTransactionId()).isEqualTo("txn_123");
    }

    @Test
    void shouldHandleGatewayTimeoutGracefully() {
        stubFor(post(urlEqualTo("/gateway/charge"))
            .willReturn(aResponse()
                .withStatus(504)));

        assertThrows(PaymentGatewayTimeoutException.class, () -> {
            paymentService.charge(new Payment("user_1", 50.00));
        });
    }
}
```

**WireMock capabilities:**
- Stub based on URL, HTTP method, headers, body.
- Simulate delays, timeouts, and network failures.
- Record/playback (proxying real APIs during development).
- Verify requests were made (assert on expected interactions).
- Fault injection (malformed responses, connection resets).

### Integration Test Best Practices

1. **Test the boundary** — Repository tests with Testcontainers, external API tests with WireMock.
2. **Keep tests independent** — each test gets its own transaction or container state.
3. **Clean up between tests** — truncate tables or use transactional rollback.
4. **Use realistic data** — edge cases that trigger unique constraints, nulls, long strings.
5. **Don't test the framework** — you don't need to test that Hibernate/JPA/ActiveRecord works.
6. **Name tests by behavior** — `shouldRejectOrderWhenInventoryExhausted()`, never `testOrder1()`.

---

## 11. Contract Testing — Pact

### What Is Contract Testing?

Contract testing verifies that two services (consumer and provider) can communicate correctly by testing each side independently against a shared contract — without deploying both services.

### Pact Workflow

```
1. Consumer writes expectations (Pact file)
   ┌──────────┐                 ┌──────────┐
   │ Consumer │ ── generates ──→│ Pact     │
   │  Tests   │                 │ File     │
   └──────────┘                 └────┬─────┘
                                     │
2. Provider verifies against Pact   │
   ┌──────────┐                      │
   │ Provider │ ←── verifies ────────│
   │  Tests   │                      │
   └──────────┘                      │
                                     │
3. Pact Broker stores & diff         │
   ┌──────────────┐                  │
   │ Pact Broker  │ ←── stores ──────│
   │ (versioned)  │                  │
   └──────┬───────┘                  │
          │                          │
4. Can-I-Deploy checks versions      │
   ┌──────────┐                      │
   │ CI/CD    │ ←── compatibility ───│
   └──────────┘                      │
```

### Consumer-Side Test (Pact)

```java
@ExtendWith(PactConsumerTestExt.class)
@PactTestFor(providerName = "PaymentProvider", port = "8080")
class OrderServiceConsumerPactTest {

    @Pact(consumer = "OrderService")
    public V4Pact createPact(PactDslWithProvider builder) {
        return builder
            .given("a payment method exists with ID 'pm_1'")
            .uponReceiving("a request to charge a payment")
                .path("/gateway/charge")
                .method("POST")
                .headers("Content-Type", "application/json")
                .body(new PactDslJsonBody()
                    .stringType("payment_method_id", "pm_1")
                    .decimalType("amount", 49.99)
                )
            .willRespondWith()
                .status(200)
                .headers("Content-Type", "application/json")
                .body(new PactDslJsonBody()
                    .stringType("status", "success")
                    .stringType("transaction_id", "txn_abc123")
                )
            .toPact();
    }

    @Test
    @PactTestFor(pactMethod = "createPact")
    void shouldChargePaymentSuccessfully(MockServer mockServer) {
        PaymentClient client = new PaymentClient(mockServer.getUrl());
        PaymentResponse response = client.charge("pm_1", 49.99);
        assertThat(response.getStatus()).isEqualTo("success");
    }
}
```

### Provider-Side Verification

```java
@Provider("PaymentProvider")
@PactBroker(url = "${pactbroker.url}")
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class PaymentProviderPactVerificationTest {

    @LocalServerPort
    int port;

    @BeforeEach
    void setup(PactVerificationContext context) {
        context.setTarget(new HttpTestTarget("localhost", port));
    }

    @TestTemplate
    @ExtendWith(PactVerificationInvocationContextProvider.class)
    void pactVerificationTestTemplate(PactVerificationContext context) {
        context.verifyInteraction();
    }

    @State("a payment method exists with ID 'pm_1'")
    void setupPaymentMethod() {
        // Set up test data — this runs before the provider is called
        paymentMethodRepository.save(new PaymentMethod("pm_1", ...));
    }
}
```

### Pact Best Practices

- **Version both consumer and provider** — Pact Broker tracks compatibility matrix.
- **Use `can-i-deploy`** — the `pact-broker can-i-deploy` command checks if two versions are compatible before deploying.
- **Don't over-specify** — use matchers (`stringType`, `decimalType`) instead of exact values for most fields. Exact values should only be for fields where the value matters (e.g., status enums).
- **Tag pacts by environment** — tag pact versions with "prod", "staging" to gate deployments.
- **Run provider verification in CI** — not just locally. Break the build if a provider change breaks a consumer contract.

---

## 12. Test Fixtures

### What Are Test Fixtures?

Test fixtures are predefined data setups that provide a known baseline state before tests run. They reduce duplication and make tests readable.

### Fixture Strategies

| Strategy | Description | Best For |
|----------|-------------|----------|
| **Inline (test-local)** | Create data directly in the test method | Simple, focused tests |
| **Factory methods** | Helper functions that create objects with sensible defaults | Most cases — flexible, composable |
| **Factory Boy / build()** | Use a library to generate test objects | Complex object graphs |
| **Seed SQL files** | Pre-populated SQL inserts loaded before test suite | Integration + E2E tests |
| **JSON/YAML snapshots** | Load test data from fixture files | When data is complex and nested |

### Example: Factory Pattern (Python)

```python
# factories.py
class UserFactory:
    @staticmethod
    def create(
        email="test@example.com",
        name="Test User",
        tier="standard",
        balance=Decimal("100.00")
    ):
        return User(
            email=email,
            name=name,
            tier=tier,
            balance=balance
        )

# test_discount.py
def test_vip_discount():
    vip = UserFactory.create(tier="vip", balance=Decimal("500.00"))
    result = discount_service.calculate(vip, 200)
    assert result == Decimal("40.00")  # 20% VIP discount
```

### Factory Boy (Python) / Builders (Java)

```python
import factory

class OrderFactory(factory.Factory):
    class Meta:
        model = Order

    id = factory.Sequence(lambda n: n)
    user = factory.SubFactory(UserFactory)
    total = Decimal("100.00")
    status = OrderStatus.PENDING
    created_at = factory.Faker("date_time_this_year")

# Usage — only override what matters
order = OrderFactory.create(status=OrderStatus.FULFILLED)
assert order.user.email == "test@example.com"  # default from UserFactory
```

### Fixture Anti-Patterns

- **Shared mutable fixtures** — tests that mutate shared state cause flaky ordering dependencies.
- **Too much data** — loading 1000 rows for every test is slow; use the minimum needed.
- **Copy-paste fixtures** — leads to drift; use factories with default values.
- **Magic numbers** — use named constants: `UNIT_PRICE = Decimal("10.00")` instead of bare `10.00`.

---

## 13. CI Integration

### Test Execution in CI

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌──────────────┐
│   Lint &    │     │   Unit      │     │ Integration │     │   Contract   │
│   Static    │ ──→ │   Tests     │ ──→ │   Tests     │ ──→ │   Tests /    │
│   Analysis  │     │ (fast, par) │     │ (slower)    │     │   E2E Tests  │
└─────────────┘     └─────────────┘     └─────────────┘     └──────────────┘
     < 2 min           < 5 min            < 15 min            < 30 min
```

### Parallelization

- **Unit tests** — run in parallel across CPU cores (pytest-xdist, JUnit parallel).
- **Integration tests** — parallel by service/module; isolate with Testcontainers per test class.
- **Contract tests** — consumer tests in parallel; provider tests sequentially per pact file.

### CI Pipeline Example (GitHub Actions)

```yaml
name: CI
on: [push, pull_request]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with: { java-version: '21', distribution: 'temurin' }
      - run: ./gradlew test --parallel     # unit tests only

  integration-tests:
    needs: unit-tests
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - run: ./gradlew integrationTest --tests *IntegrationTest
    # Alternatively, use Testcontainers which starts containers in-test

  contract-tests:
    needs: unit-tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: ./gradlew pactVerify          # provider-side verification
      - run: ./gradlew pactPublish         # publish to Pact Broker

  pact-can-i-deploy:
    needs: contract-tests
    runs-on: ubuntu-latest
    steps:
      - run: pact-broker can-i-deploy
          --pacticipant OrderService
          --version $(cat version.txt)
          --to-environment production

  e2e-tests:
    needs: [integration-tests, pact-can-i-deploy]
    runs-on: ubuntu-latest
    steps:
      - run: docker compose -f docker-compose.e2e.yml up --abort-on-container-exit
```

### CI Best Practices

| Practice | Rationale |
|----------|-----------|
| **Fail fast** | Run fastest tests first (unit → integration → E2E). |
| **Cache dependencies** | Maven/Gradle/npm/pip caches speed up repeat builds. |
| **Cache Docker layers** | Testcontainers pulls — pre-warm image caches. |
| **Isolate flaky tests** | Quarantine flaky tests; don't let them block the pipeline. |
| **Test against production-like databases** | Use Testcontainers with the same DB version as production. |
| **Run pact verification as a required check** | Never deploy a provider that breaks a consumer contract. |
| **Use test reports as artifacts** | Publish JUnit XML / HTML reports for debugging. |

### Test Run Optimization

- **Selective test execution** — only run tests for changed modules (gradle `--changed-latest`, `pytest --last-failed`).
- **Test splitting** — split integration tests across multiple CI runners (`--shard` flags).
- **Docker layer reuse** — Dockerfile changes cause full rebuilds; keep rarely-changed layers early.
- **Database migrations in CI** — run migrations once, snapshot the DB, restore for each test runner.

---

## References & Further Reading

- **PostgreSQL Documentation** — [EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html), [Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html)
- **HikariCP** — [GitHub](https://github.com/brettwooldridge/HikariCP) (connection pool sizing)
- **PgBouncer** — [Official docs](https://www.pgbouncer.org/) (transaction pooling)
- **Pact** — [Documentation](https://docs.pact.io/) (contract testing)
- **Testcontainers** — [Official site](https://testcontainers.com/) (integration testing)
- **WireMock** — [Official site](https://wiremock.org/) (API mocking)
- **Shopify Engineering** — [Read Consistency with Database Replicas](https://shopify.engineering/read-consistency-database-replicas)
- **Crunchy Data** — [Postgres Indexes for Newbies](https://www.crunchydata.com/blog/postgres-indexes-for-newbies)
- **Scout APM** — [Understanding N+1 Database Queries](https://www.scoutapm.com/blog/understanding-n1-database-queries)
- **AWS** — [RDS Proxy](https://aws.amazon.com/rds/proxy/) (serverless connection pooling)
