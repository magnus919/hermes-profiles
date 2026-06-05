# Graph Databases for Data Engineering: Neo4j & Cypher Reference

> A practical reference for data engineers working with Neo4j, the Cypher query language,
> and graph data modeling patterns in production pipelines.

---

## Table of Contents

1. [Graph Data Modeling Principles](#1-graph-data-modeling-principles)
2. [Neo4j Deployment Models](#2-neo4j-deployment-models)
3. [Cypher Query Language Fundamentals](#3-cypher-query-language-fundamentals)
4. [Graph Data Modeling Patterns by Domain](#4-graph-data-modeling-patterns-by-domain)
5. [Cypher Aggregation & Graph Traversal](#5-cypher-aggregation--graph-traversal)
6. [Importing Data into Neo4j](#6-importing-data-into-neo4j)
7. [Indexing & Performance Optimization](#7-indexing--performance-optimization)
8. [Graph Algorithms Library (GDS)](#8-graph-algorithms-library-gds)
9. [Integrating Neo4j into Data Pipelines](#9-integrating-neo4j-into-data-pipelines)
10. [Graph vs. Relational: When to Use Which](#10-graph-vs-relational-when-to-use-which)

---

## 1. Graph Data Modeling Principles

### 1.1 The Property Graph Model

Neo4j uses the **labeled property graph** model. A graph is composed of:

| Element | Description | Example |
|---------|-------------|---------|
| **Node** | A discrete entity/object | `(:Person {name: "Alice"})` |
| **Relationship** | A directed connection between two nodes | `(Alice)-[:KNOWS]->(Bob)` |
| **Label** | A node category/type (a node can have many) | `:Person`, `:Company`, `:Customer` |
| **Property** | A key-value pair on a node or relationship | `{name: "Alice", age: 30}` |
| **Relationship Type** | The semantic category of a relationship | `:KNOWS`, `:WORKS_FOR`, `:PURCHASED` |

**Key distinction from relational**: Relationships are first-class citizens, not foreign-key joins computed at query time. In Neo4j, a relationship is a physically stored pointer — traversal is O(1) per hop regardless of graph size.

### 1.2 Core Modeling Principles

**1. Model the Domain, Not the Schema**
- In a relational DB you design tables first, then JOIN them.
- In a graph you ask "what are the real-world entities and how do they connect?"
- A node label groups entities by role; a relationship type captures the verb.

**2. Favor Relationships Over Join Tables**
- A join table in SQL (e.g., `user_roles`) becomes a relationship in Neo4j.
- If the relationship itself has data (e.g., `since` date on an employment relationship), put properties on the relationship.

```cypher
-- Relational: JOIN table with data columns
-- user_id, role_id, assigned_date

-- Graph: relationship carries the data
(:User)-[:HAS_ROLE {assigned_date: "2024-01-15"}]->(:Role)
```

**3. Nodes for Nouns, Relationships for Verbs**
- `:Invoice`, `:Product`, `:Customer` → nodes
- `:PURCHASED`, `:SHIPPED_TO`, `:CONTAINS` → relationships
- If you find yourself creating `:Transaction` as a node connecting two other nodes, first ask whether you need properties on the connection itself.

**4. Avoid "Meta-Relationships"** (relationships that should be nodes)
- If a relationship has enough data to be an entity itself (especially if it connects more than two nodes), promote it to a node.

```
BAD:  (User)-[:TRANSACTION {amount, date}]->(Product)
BETTER: (User)-[:MADE]->(Transaction {amount, date})-[:FOR]->(Product)
```

**5. Use Labels as Index Categories**
- Every query starts with a label match: `MATCH (p:Person)`.
- Labels separate entity types. A node can have multiple labels: `(:Person:Customer:Premium)`.

### 1.3 Common Anti-Patterns

| Anti-Pattern | Why It's Wrong | Fix |
|---|---|---|
| One giant "Thing" label for everything | Every query scans everything | Use specific labels `:Person`, `:Invoice` |
| Properties on relationship that belong on the target node | Bloated traversals | Put the property on the destination node |
| Creating a node for a simple scalar value | Unnecessary overhead | Keep it as a property |
| Over-labeling (10+ labels on one node) | Index overhead, confusion | Consolidate; use at most 3-4 per node |
| Chaining relationships where a direct one suffices | Slower queries | Shortest path wins; add direct relationships for frequent patterns |

---

## 2. Neo4j Deployment Models

### 2.1 Comparison Matrix

| Feature | Self-Hosted (Community) | Self-Hosted (Enterprise) | AuraDB Free | AuraDB Professional | AuraDB Enterprise |
|---------|------------------------|-------------------------|-------------|--------------------|--------------------|
| Cost | Free | License fee | Free (limited) | Consumption-based | Consumption-based |
| Scaling | Single instance | Clustering (primary-replica) | Auto-scaled | Auto-scaled | Auto-scaled |
| HA/DR | None | Full clustering, backups | Built-in | Built-in | Multi-region |
| Cypher | Full | Full with fabric | Full | Full | Full |
| GDS Library | Manual install | Included | Via plugin | Via plugin | Via plugin |
| APOC | Manual install | Included | Via plugin | Via plugin | Via plugin |
| Backup | Manual/`neo4j-admin` | Online, incremental | Automated | Automated | Automated |
| SLA | None | Optional | 99.9% | 99.95% | 99.995% |
| Max DB size | Limited by hardware | Limited by cluster | 200K nodes | Pay-as-you-grow | Pay-as-you-grow |

### 2.2 When to Choose Each

**Self-Hosted (Community)**
- Development, prototyping, small internal tools
- Air-gapped environments
- Cost-sensitive projects with under ~50M nodes
- You already manage your own infrastructure

**Self-Hosted (Enterprise)**
- Regulatory requirements (data residency, SOC2 on your own infra)
- Need full clustering (up to 200+ core servers + read replicas)
- Custom security policies (LDAP, Kerberos, custom plugins)
- You have a DBRE team

**AuraDB**
- "I just want a graph database, not a server to manage"
- Serverless scaling without capacity planning
- Graph apps in production that need HA out of the box
- CI/CD and dev/staging/prod environments you spin up/down
- Small team without DBA headcount

### 2.3 Deployment Infrastructure Quickstart

**Docker (local dev):**
```bash
docker run \
  --name neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/strongpassword \
  -e NEO4J_PLUGINS='["apoc","graph-data-science"]' \
  neo4j:enterprise
```

**Kubernetes (production):**
- Use the Neo4j Helm chart: `helm repo add neo4j https://helm.neo4j.com`
- Supports Core/Read-replica topology
- PersistentVolumeClaims for data durability

**AuraDB (managed):**
- Sign up at https://neo4j.com/cloud/aura-free/
- Download `.env` with credentials
- Connect via `neo4j+s://<instance-id>.databases.neo4j.io`

---

## 3. Cypher Query Language Fundamentals

Cypher is a declarative, pattern-matching query language inspired by ASCII-art syntax for graph patterns.

### 3.1 Core Clauses

#### `MATCH` — Find Patterns in the Graph

```cypher
-- Simple node match
MATCH (p:Person)
RETURN p.name

-- Pattern match (relationship)
MATCH (a:Person)-[:KNOWS]->(b:Person)
RETURN a.name, b.name

-- Property filter
MATCH (p:Person {name: "Alice"})
RETURN p.email

-- WHERE clause (equivalent — use for complex predicates)
MATCH (p:Person)
WHERE p.name STARTS WITH "A" AND p.age > 25
RETURN p

-- Variable-length traversal
MATCH (a:Person)-[:KNOWS]->{1..3}(b:Person)
RETURN DISTINCT b.name
```

#### `CREATE` — Add Nodes and Relationships

```cypher
-- Create a node
CREATE (p:Person {name: "Charlie", age: 35})

-- Create a relationship between existing nodes
MATCH (a:Person {name: "Alice"})
MATCH (b:Person {name: "Bob"})
CREATE (a)-[:KNOWS {since: 2020}]->(b)

-- Create both (avoid for large imports to prevent OOM)
CREATE (a:Person {name: "Dave"})-[:WORKS_FOR]->(:Company {name: "Acme"})
```

#### `MERGE` — Find or Create (Upsert)

```cypher
-- Find a node by ID, create if missing
MERGE (p:Person {id: "alice-001"})
ON CREATE SET p.name = "Alice", p.createdAt = datetime()
ON MATCH  SET p.lastSeen = datetime()

-- MERGE a relationship (only creates if not exists)
MATCH (a:Person {id: $id1})
MATCH (b:Person {id: $id2})
MERGE (a)-[:KNOWS]->(b)
```

**MERGE pitfall**: `MERGE (a)-[:R]->(b)` without MATCHing a and b first will create duplicate nodes. Always MATCH both endpoints first.

#### `RETURN` — Shape Query Output

```cypher
-- Return specific properties (for LLM/API consumption)
MATCH (p:Person)
RETURN p.name AS name, p.email AS email

-- Map projection (concise)
MATCH (p:Person)
RETURN p { .name, .email, .age }

-- Return entire node (for visualization tools)
MATCH path = (a:Person)-[:KNOWS*1..3]->(:Person)
RETURN path
```

#### `WHERE` — Filter Results

```cypher
-- Comparisons
WHERE p.age >= 18 AND p.age <= 65

-- String patterns
WHERE p.name STARTS WITH "A"
WHERE p.name ENDS WITH "son"
WHERE p.name CONTAINS "li"

-- List membership
WHERE p.name IN ["Alice", "Bob", "Charlie"]

-- Existence
WHERE exists { (p)-[:KNOWS]->() }

-- Negation
WHERE NOT (p)-[:KNOWS]->()
```

### 3.2 Essential Patterns (Cypher 25+)

Cypher 25 introduced cleaner syntax. Avoid deprecated patterns.

| Old (Deprecated) | New (Preferred) |
|---|---|
| `shortestPath((a)-[*]-(b))` | `SHORTEST 1 (a)-[*]-(b)` |
| `()-[*1..5]-()` | `()-[]{1,5}-()` |
| `WITH collect(x)` | `COLLECT { MATCH ... RETURN ... }` |
| `WITH count(*)` | `COUNT { MATCH ... }` |
| `RETURN exists((n)-[:R]->())` | `RETURN exists { (n)-[:R]->() }` |

### 3.3 Parameterization

**Always use `$parameters` — never string-interpolate.**

```python
# BAD: string interpolation (SQL injection risk)
query = f"MATCH (p:Person {{name: '{user_input}'}}) RETURN p"

# GOOD: parameterized
records, _, _ = driver.execute_query(
    "MATCH (p:Person {name: $name}) RETURN p.email",
    name=user_input
)
```

```cypher
// Cypher-side (parameters passed by driver)
MATCH (p:Person {name: $name})
RETURN p
```

### 3.4 Subqueries and Chaining

```cypher
-- COUNT subquery (Cypher 25)
MATCH (p:Person)
RETURN p.name, COUNT { (p)-[:KNOWS]->() } AS friend_count

-- COLLECT subquery
MATCH (p:Person)
RETURN p.name, COLLECT {
    MATCH (p)-[:KNOWS]->(friend)
    RETURN friend.name
} AS friends

-- WITH for pipeline chaining
MATCH (p:Person)-[:PURCHASED]->(item:Product)
WITH p, count(item) AS purchase_count
WHERE purchase_count > 5
RETURN p.name, purchase_count
```

---

## 4. Graph Data Modeling Patterns by Domain

### 4.1 Knowledge Graph

**Pattern**: Entities connected by typed, often hierarchical relationships.

```cypher
-- Schema: documents, concepts, entities with semantic relationships
(:Document {id, title, published_date})
  -[:CONTAINS]->(:Chunk {id, text, embedding})
    -[:MENTIONS]->(:Entity {id, name, type})

(:Entity)-[:RELATED_TO {weight, relationship_type}]->(:Entity)
(:Entity)-[:SUBCLASS_OF]->(:Entity)  -- taxonomy hierarchy
```

**Common queries**:
```cypher
-- Multi-hop: find concepts reachable from a document
MATCH (d:Document {id: $doc_id})-[:CONTAINS]->(:Chunk)-[:MENTIONS]->(e:Entity)
RETURN DISTINCT e.name, e.type

-- Graph traversal for GraphRAG: entities connected to a seed through 2 hops
MATCH (e:Entity {name: $seed})-[]->{1,2}(related:Entity)
RETURN related.name, related.type
```

**When it wins vs. relational**: Multi-hop queries (`book → author → institution → location`) that would require 4+ JOINs in SQL are a single variable-length pattern match in Cypher.

### 4.2 Recommendation Engine

**Pattern**: Users, items, and interactions as relationships carrying weight/timestamp.

```cypher
-- Schema
(:User {id, preferences, embeddding})
  -[:RATED {score, timestamp}]->(:Item {id, category, tags})
  -[:BELONGS_TO]->(:Category {name})
  -[:SIMILAR_TO {score}]->(:Category)

(:User)-[:FRIENDS_WITH]->(:User)
(:User)-[:VIEWED]->(:Item)
(:Item)-[:CO_OCCURS {count}]->(:Item)  -- "bought together"
```

**Common queries**:
```cypher
-- Collaborative filtering: "users like you also liked"
MATCH (me:User {id: $user_id})-[:RATED]->(item:Item)
WHERE item.rating >= 4
MATCH (other:User)-[:RATED]->(item)
WHERE other.id <> $user_id
MATCH (other)-[:RATED]->(rec:Item)
WHERE NOT exists { (me)-[:RATED]->(rec) }
RETURN rec.id, avg(other.rating) AS predicted_rating
ORDER BY predicted_rating DESC
LIMIT 20

-- Content-based: "similar to items you liked"
MATCH (me:User {id: $user_id})-[:RATED {score: 5}]->(liked:Item)
MATCH (liked)-[:BELONGS_TO]->(cat:Category)
MATCH (rec:Item)-[:BELONGS_TO]->(cat)
WHERE NOT exists { (me)-[:RATED]->(rec) }
RETURN rec.id, count(*) AS matches
ORDER BY matches DESC
LIMIT 10
```

**When it wins vs. relational**: The `other-[:RATED]->item` join pattern (users-to-items-to-users) avoids a three-table self-join. Variable-length traversal replaces recursive CTEs for path-based similarity.

### 4.3 Network/Mesh (Infrastructure & Topology)

**Pattern**: Physical or logical nodes connected by directed/undirected links, often with layered abstraction.

```cypher
-- Schema: cloud infrastructure
(:Server {id, hostname, ip, region, provider})
  -[:HOSTS]->(:Container {id, image, status})
  -[:RUNS]->(:Service {name, version, port})

(:Server)-[:CONNECTS_TO {bandwidth, latency_ms}]->(:Server)
(:Service)-[:DEPENDS_ON]->(:Service)
(:Service)-[:EXPOSES]->(:Endpoint {path, method})
(:Subnet {cidr})-[r:CONTAINS]->(:Server)
```

**Common queries**:
```cypher
-- Blast radius: all services reachable from a failing server
MATCH (s:Server {id: $server_id})-[:HOSTS]->(:Container)-[:RUNS]->(svc:Service)
RETURN svc.name

-- Dependency chain: find all transitive dependencies
MATCH (svc:Service {name: $svc_name})-[:DEPENDS_ON]->{1..10}(dependency:Service)
RETURN DISTINCT dependency.name, length(path) AS depth

-- Shortest network path between two servers
MATCH SHORTEST 1 (a:Server {ip: $ip1})-[:CONNECTS_TO*]-(b:Server {ip: $ip2})
RETURN [x IN nodes(path) | x.hostname] AS route
```

**When it wins vs. relational**: Blast-radius analysis and transitive dependency resolution are O(1)-per-hop tree traversals in a graph vs. recursive CTEs (which hit recursive query limits and degrade with depth).

### 4.4 Access Control (RBAC / ReBAC)

**Pattern**: Users, roles, permissions, and resources as nodes; grants and assignments as relationships.

```cypher
-- Schema: Relationship-Based Access Control (ReBAC)
(:User {id, email})
  -[:HAS_ROLE]->(:Role {name, level})
  -[:GRANTS]->(:Permission {action, resource_type})

(:User)-[:MEMBER_OF]->(:Group {name})
(:Group)-[:HAS_ROLE]->(:Role)

(:Permission)-[:ON]->(:Resource {id, type, owner_id})

-- Direct access via ownership
(:User)-[:OWNS]->(:Resource)

-- Organization hierarchy
(:OrgUnit)-[:CONTAINS]->(:OrgUnit)
(:User)-[:BELONGS_TO]->(:OrgUnit)
```

**Common queries**:
```cypher
-- Is user authorized to perform action on resource?
MATCH (u:User {id: $user_id})
MATCH (r:Resource {id: $resource_id})
CALL {
    WITH u
    // Direct role assignment
    MATCH (u)-[:HAS_ROLE]->(role:Role)-[:GRANTS]->(perm:Permission)
    WHERE perm.action = $action
    RETURN perm
    UNION
    // Group membership
    MATCH (u)-[:MEMBER_OF]->(:Group)-[:HAS_ROLE]->(role:Role)-[:GRANTS]->(perm:Permission)
    WHERE perm.action = $action
    RETURN perm
    UNION
    // Ownership
    MATCH (u)-[:OWNS]->(r)
    RETURN null AS perm
}
RETURN count(*) > 0 AS is_authorized

-- Compute effective permissions for a user
MATCH (u:User {id: $user_id})
OPTIONAL MATCH path = (u)-[:MEMBER_OF|HAS_ROLE|GRANTS*]->(p:Permission)
RETURN p.action, p.resource_type, min(length(path)) AS shortest_path
```

**When it wins vs. relational**: ReBAC requires modeling nested group membership and inheritance chains. In SQL this is a many-many join across 5+ tables with recursive CTEs. In Cypher it's a variable-length traversal with union.

---

## 5. Cypher Aggregation & Graph Traversal

### 5.1 Aggregation Functions

| Function | Purpose | Example |
|----------|---------|---------|
| `count()` | Count rows or distinct values | `RETURN count(*)` |
| `collect()` | Aggregate into a list | `RETURN p.name, collect(friend.name)` |
| `avg()` | Average of numeric values | `RETURN avg(r.rating)` |
| `sum()` | Sum of values | `RETURN sum(o.total)` |
| `min()` / `max()` | Min/max | `RETURN max(p.salary)` |
| `stDev()` / `stDevP()` | Sample/population stddev | `RETURN stDev(p.age)` |

**GROUP BY is implicit**: any non-aggregated column in `RETURN` is a grouping key.

```cypher
MATCH (o:Order)-[:CONTAINS]->(p:Product)
RETURN p.category, count(o) AS order_count, avg(o.total) AS avg_order_value
ORDER BY order_count DESC
```

### 5.2 Graph Traversal Patterns

**Variable-length path traversal:**
```cypher
-- Depth 1 to 3
MATCH (a:Person)-[:KNOWS]->{1,3}(b:Person)
RETURN a.name, collect(DISTINCT b.name) AS network

-- Exactly 3 hops
MATCH (a:Person)-[:KNOWS]->{3}(b:Person)
```

**Shortest/fastest paths (Cypher 25):**
```cypher
-- Single shortest path
MATCH SHORTEST 1 (a:Airport {code: "LAX"})-[:ROUTE*]-(b:Airport {code: "JFK"})
RETURN [x IN nodes(path) | x.code] AS route

-- All shortest paths
MATCH ALL SHORTEST (a)-[:KNOWS*]-(b)
RETURN count(path) AS path_count

-- Cost-based (using relationship property as weight)
MATCH SHORTEST 1 (a:City {name: "NYC"})-[:ROAD*]-(b:City {name: "SF"})
WHERE reduce(cost = 0, r IN relationships(path) | cost + r.distance) < 5000
RETURN path, reduce(cost = 0, r IN relationships(path) | cost + r.distance) AS total_distance
```

**Quantified path patterns (Cypher 25):**
```cypher
-- Named quantified path: each hop can be any of several relationship types
MATCH (a:Person) ((:Person)-[:KNOWS|:FRIENDS_WITH]->(:Person)){1,3} (b:Person)
RETURN a.name, b.name
```

### 5.3 Path Projections and Analysis

```cypher
-- Extract node names from a path
MATCH p = (a:Person)-[:KNOWS*1..3]->(b:Person)
RETURN [n IN nodes(p) | n.name] AS name_chain,
       length(p) AS depth

-- Sum relationship properties along a path
MATCH p = (a:User)-[:TRANSFERRED*]-(b:User)
RETURN reduce(total = 0, r IN relationships(p) | total + r.amount) AS total_transferred

-- Find paths where a condition holds at each step
MATCH p = (a:Car {status: "active"})-[:BELONGS_TO*]-(org:Org)
WHERE all(n IN nodes(p) WHERE n.active = true)
RETURN p
```

---

## 6. Importing Data into Neo4j

### 6.1 `LOAD CSV` — Online, Incremental

Best for small to medium datasets (up to ~10M rows). Runs as a Cypher query.

```cypher
// Simple import
LOAD CSV WITH HEADERS FROM 'file:///users.csv' AS row
CREATE (:User {
    id: row.id,
    name: row.name,
    email: row.email,
    created_at: datetime(row.created_at)
})

// With MERGE and relationships
LOAD CSV WITH HEADERS FROM 'https://s3.amazonaws.com/bucket/orders.csv' AS row
MATCH (u:User {id: row.user_id})
MATCH (p:Product {id: row.product_id})
MERGE (u)-[:PURCHASED {amount: toFloat(row.amount), date: date(row.date)}]->(p)

// Periodic commit (for large files, though Cypher 25 handles streaming better)
:auto USING PERIODIC COMMIT 5000
LOAD CSV WITH HEADERS FROM 'file:///large.csv' AS row
CREATE (:Event {id: row.id})
```

**Performance tips for `LOAD CSV`:**
- Always use `WITH HEADERS` for readability
- Create indexes/lookup constraints on `id` fields before loading relationships
- Pre-`MATCH` / `MERGE` by indexed property, not label scan
- Limit to 10M rows per `LOAD CSV` call for practical performance
- For larger datasets, batch with `UNWIND` and `IN TRANSACTIONS`

```cypher
// Batched import via UNWIND (Cypher 25)
UNWIND $batch_of_rows AS row
CALL (row) {
    MERGE (u:User {id: row.user_id})
    SET u.name = row.name, u.email = row.email
} IN TRANSACTIONS OF 5000 ROWS
```

### 6.2 APOC Load (`apoc.load.*`)

The APOC library provides more powerful import capabilities.

```cypher
// Load from JSON API
CALL apoc.load.json("https://api.example.com/users")
YIELD value
MERGE (u:User {id: value.id})
SET u.name = value.name, u.email = value.email

// Load from CSV with more control
CALL apoc.load.csv("data.csv", {header: true, sep: "|"})
YIELD map AS row
CREATE (:Record {id: row.id, value: row.val})

// Load from Parquet / ORC (via apoc.nlp or custom plugins)
CALL apoc.load.parquet("s3://bucket/data.parquet")
YIELD row
MERGE (p:Product {sku: row.sku})
SET p.price = row.price

// Conditional import
CALL apoc.periodic.iterate(
    "LOAD CSV WITH HEADERS FROM 'file:///data.csv' AS row RETURN row",
    "MATCH (c:Customer {id: row.id})
     CREATE (c)-[:PURCHASED]->(:Order {id: row.order_id, total: toFloat(row.total)})",
    {batchSize: 1000, parallel: true}
)
```

### 6.3 `neo4j-admin database import` — Bulk Offline Import

Best for initial bulk loads (hundreds of millions to billions of nodes). Requires the database to be offline.

```bash
# Stop Neo4j first, then:
neo4j-admin database import full \
  --nodes=import/users_header.csv,import/users.csv \
  --nodes=import/products_header.csv,import/products.csv \
  --relationships=import/purchases_header.csv,import/purchases.csv \
  --delimiter="," \
  --verbose

# With a single header file per entity type
# users_header.csv:  id:ID, name, email:STRING, age:INT, :LABEL
# purchases_header.csv: :START_ID, :END_ID, amount:FLOAT, date:DATE, :TYPE
```

**Performance:**
- 1-2 billion nodes per hour on reasonable hardware
- Creates the database from scratch (no merge logic)
- Best for initial data loads, then use CDC/incremental for updates

### 6.4 Import Strategy Decision

| Data Volume | Approach | Latency | Complexity |
|-------------|----------|---------|------------|
| < 100K rows | `LOAD CSV` | Minutes | Low |
| 100K – 10M | `apoc.periodic.iterate` | Minutes | Medium |
| 10M – 100M | `LOAD CSV` + `IN TRANSACTIONS` | Hours | Medium |
| 100M – 1B+ | `neo4j-admin database import` | Minutes (offline) | High |
| Streaming / real-time | CDC + `MERGE` | Sub-second | High |
| Incremental updates | `apoc.periodic.iterate` / CDC | Variable | Medium |

---

## 7. Indexing & Performance Optimization

### 7.1 Index Types

| Index Type | Syntax | Use Case |
|---|---|---|
| **BTREE** (default) | `CREATE INDEX FOR (p:Person) ON (p.name)` | Equality, range, prefix queries |
| **RANGE** (Cypher 25) | `CREATE RANGE INDEX FOR (p:Person) ON (p.name)` | Same as BTREE; preferred syntax |
| **TEXT** | `CREATE TEXT INDEX FOR (p:Person) ON (p.name)` | Full-text `CONTAINS`, `STARTS WITH` |
| **POINT** | `CREATE POINT INDEX FOR (l:Location) ON (l.coords)` | Spatial queries (`distance()`, `point.withinBBox()`) |
| **VECTOR** | `CREATE VECTOR INDEX FOR (c:Chunk) ON (c.embedding)` | ANN similarity search for embeddings |
| **FULLTEXT** | `CREATE FULLTEXT INDEX names FOR (p:Person) ON EACH [p.name]` | Language-aware full-text search |

### 7.2 Constraints (Which Also Create Indexes)

```cypher
-- Unique constraint (creates a backing index)
CREATE CONSTRAINT FOR (p:Person) REQUIRE p.id IS UNIQUE

-- Node key constraint (composite uniqueness)
CREATE CONSTRAINT FOR (p:Person) REQUIRE (p.first_name, p.last_name) IS NODE KEY

-- Existence constraint
CREATE CONSTRAINT FOR (p:Person) REQUIRE p.email IS NOT NULL
```

**Rule of thumb**: Every property you filter on in `WHERE` should have an index. Every property used for `MERGE` should have a uniqueness constraint.

### 7.3 Query Performance Rules

1. **Use labels always**: `MATCH (n)` scans everything → always write `MATCH (n:Label)`.
2. **Index lookup before traversal**: Put selective filters first.
   ```cypher
   -- Fast: narrows to one user first, then traverses
   MATCH (u:User {id: $id})-[:PURCHASED]->(o:Order)
   RETURN o

   -- Slow: might scan all orders first
   MATCH (o:Order)<-[:PURCHASED]-(u:User {id: $id})
   RETURN o
   ```
3. **Use `PROFILE` and `EXPLAIN`**:
   ```cypher
   PROFILE MATCH (u:User {id: $id})-[:PURCHASED]->(o:Order) RETURN o
   ```
   Look for `NodeByLabelScan` (bad) vs `NodeUniqueIndexSeek` (good).
4. **Always `LIMIT` unbounded traversals** in user-facing queries.
5. **Avoid `RETURN n`** for large result sets — project specific properties.
6. **Use `WHERE n.property = $param`** over `{property: $param}` when the filter is a precondition.

### 7.4 Caching Strategy

Neo4j uses a page cache (mmap-based). Everything that fits in cache runs at memory speed.

```ini
# neo4j.conf
# Set page cache to 50-70% of available RAM for graph workloads
server.memory.pagecache.size=8G
# Heap for query execution and transactions
server.memory.heap.max_size=4G
# Off-heap for GDS algorithms
server.memory.off_heap.max_size=2G
```

**Cache hit ratio monitoring:**
```cypher
CALL dbms.listConfig() YIELD name, value
WHERE name STARTS WITH "server.memory"
RETURN name, value
```

---

## 8. Graph Algorithms Library (GDS)

The Neo4j Graph Data Science library provides in-database parallel graph algorithms. Algorithms operate on an **in-memory graph projection**, not the stored graph directly.

### 8.1 Workflow

```
Stored Graph → Project → In-Memory Graph → Run Algorithm → Stream/Write Results
```

```cypher
-- 1. Project a graph into memory
CALL gds.graph.project(
    'myGraph',
    ['Person', 'Company'],
    ['KNOWS', 'WORKS_FOR']
)

-- 2. Run an algorithm
CALL gds.pageRank.stream('myGraph')
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).name AS name, score
ORDER BY score DESC
LIMIT 10

-- 3. Write results back to stored graph
CALL gds.pageRank.write('myGraph', {writeProperty: 'pagerank'})

-- 4. Drop the in-memory graph when done
CALL gds.graph.drop('myGraph')
```

### 8.2 Algorithm Categories

#### Pathfinding

| Algorithm | Use Case | Syntax Hint |
|---|---|---|
| **Shortest Path (Dijkstra)** | Weighted shortest route | `gds.shortestPath.dijkstra.stream()` |
| **A\*** | Geospatial routing (with coordinates) | `gds.shortestPath.astar.stream()` |
| **All Pairs / Single Source** | Distance matrix computation | `gds.allPairsShortestPath.stream()` |
| **Yen's K-Shortest Paths** | Top-N alternative routes | `gds.shortestPath.yens.stream()` |

```cypher
-- Weighted shortest path
MATCH (a:Airport {code: "LAX"}), (b:Airport {code: "JFK"})
CALL gds.shortestPath.dijkstra.stream('flightGraph', {
    sourceNode: a,
    targetNode: b,
    relationshipWeightProperty: 'distance'
})
YIELD nodeIds, totalCost
RETURN [id IN nodeIds | gds.util.asNode(id).code] AS route, totalCost
```

#### Centrality (Node Importance)

| Algorithm | What It Measures | Use Case |
|---|---|---|
| **PageRank** | Inbound link importance | Influence ranking, recommendation |
| **Betweenness Centrality** | Node bridge/connector importance | Identifying chokepoints, fraud rings |
| **Closeness Centrality** | Average distance to all other nodes | Information propagation speed |
| **Degree Centrality** | Number of connections | Hub identification |
| **Eigenvector Centrality** | Influence of connected nodes | Authority ranking |
| **ArticleRank** | PageRank variant for co-citation | Academic citation analysis |

```cypher
-- PageRank for influencer detection
CALL gds.pageRank.stream('socialGraph', {
    maxIterations: 20,
    dampingFactor: 0.85
})
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).name AS influencer, score
ORDER BY score DESC
LIMIT 50

-- Betweenness for bridge detection (identify fraud mules)
CALL gds.betweenness.stream('transactionGraph')
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).id AS account_id, score
ORDER BY score DESC
```

#### Community Detection

| Algorithm | Type | Use Case |
|---|---|---|
| **Louvain** | Hierarchical clustering | General community detection, org structure |
| **Label Propagation** | Fast, near-linear | Large-scale community assignment |
| **Weakly Connected Components** | Connectivity check | Isolated subgraph detection |
| **Strongly Connected Components** | Directed connectivity | Dependency cycles |
| **Triangle Count / Clustering Coefficient** | Local connectivity density | Fraud rings, highly clustered groups |
| **K-1 Coloring** | Graph coloring | Resource allocation, scheduling |
| **Modularity Optimization** | Quality measure for communities | Evaluating cluster quality |

```cypher
-- Louvain community detection
CALL gds.louvain.stream('interactionGraph')
YIELD nodeId, communityId, intermediateCommunityIds
RETURN gds.util.asNode(nodeId).name AS name, communityId
ORDER BY communityId

-- Label Propagation (for billion-node graphs)
CALL gds.labelPropagation.stream('hugeGraph', {maxIterations: 10})
YIELD nodeId, communityId
RETURN communityId, count(*) AS member_count
ORDER BY member_count DESC

-- Triangle count (fraud detection: dense subgraphs)
CALL gds.triangleCount.stream('transactionGraph')
YIELD nodeId, triangleCount
WHERE triangleCount > 10
RETURN gds.util.asNode(nodeId).id AS account, triangleCount
ORDER BY triangleCount DESC
```

#### Node Embedding (Graph ML)

| Algorithm | Description |
|---|---|
| **FastRP** | Fast random-projection embeddings |
| **Node2Vec** | Random-walk based embeddings |
| **GraphSAGE** | GNN-based inductive embeddings |
| **HashGNN** | Scalable GNN embeddings |

### 8.3 GDS Production Tips

- **Mutate mode** (`{mutateProperty: '...'}`) — stores results in the in-memory graph without writing to the stored graph. Useful for chaining: run Louvain, use communities as features for Node2Vec.
- **Write mode** (`{writeProperty: '...'}`) — persists to the stored graph for dashboard queries.
- **Tiered projections**: Create progressively smaller projections for iterative algorithm chaining.
- **Memory estimation**: Always call `gds.<algo>.estimate()` before running on large graphs to avoid OOM.

---

## 9. Integrating Neo4j into Data Pipelines

### 9.1 Change Data Capture (CDC)

Neo4j CDC (GA since 2024) streams transaction log changes to Kafka or directly to consumers.

```bash
# Enable CDC on the database
ALTER DATABASE neo4j SET cdc ENABLED;
```

```python
# Python CDC consumer (via Neo4j Kafka Connector or direct capture)
from neo4j import GraphDatabase

def watch_changes(driver):
    # Poll the CDC stream
    with driver.session() as session:
        result = session.run("""
            CALL cdc.current()
            YIELD eventId, operation, metadata, change
            RETURN eventId, operation, metadata, change
            ORDER BY eventId
            LIMIT 100
        """)
        for record in result:
            handle_change(record)
```

**Neo4j Connector for Apache Kafka:**
```
Source: Neo4j → CDC → Kafka topic → Sink (downstream systems)
```

CDC captures every `CREATE`, `UPDATE`, `DELETE` on nodes and relationships with before/after snapshots.

### 9.2 Querying Neo4j from Applications

**Python (neo4j driver):**
```python
from neo4j import GraphDatabase

class Neo4jConnection:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def find_person_network(self, name):
        with self.driver.session(database="neo4j") as session:
            result = session.run("""
                MATCH (p:Person {name: $name})-[:KNOWS]->{1,3}(contacts)
                RETURN contacts.name AS name,
                       labels(contacts) AS labels
                LIMIT 100
            """, name=name)
            return [record.data() for record in result]

# Singleton pattern — one driver per process
conn = Neo4jConnection("neo4j+s://myinstance.databases.neo4j.io", "neo4j", os.getenv("PASSWORD"))
network = conn.find_person_network("Alice")
conn.close()
```

**HTTP Query API (driverless — useful for serverless/lambda):**
```bash
curl -X POST https://<instance>.databases.neo4j.io/db/neo4j/query/v2 \
  -u neo4j:$PASSWORD \
  -H "Content-Type: application/json" \
  -d '{
    "statement": "MATCH (p:Person {name: $name}) RETURN p.email",
    "parameters": {"name": "Alice"}
  }'
```

**Airflow integration (custom hook or operator):**
```python
from airflow.providers.common.sql.hooks import SqlHook

# Use a custom Neo4j hook or the generic DB API hook
# Alternatively, use the PythonOperator with the neo4j driver directly
def pull_graph_data(**context):
    driver = GraphDatabase.driver(...)
    with driver.session() as session:
        result = session.run("MATCH ... RETURN ...")
        return [r.data() for r in result]
```

### 9.3 Pipeline Architecture Patterns

**Batch ETL (Daily/Weekly):**
```
Source DB → (CSV/Parquet) → S3/GCS → LOAD CSV / apoc.load → Neo4j
```

**Streaming / Micro-batch:**
```
Source DB → Debezium → Kafka → Neo4j Connector (CDC sink) → Neo4j
```

**Dual-write / Transactional:**
```
App → (Write to Postgres + Neo4j in same transaction) → Both databases consistent
```

**Graph as enrichment layer:**
```
Data Lake → Spark (featurization using GDS) → ML model training
                           ↓
                     Neo4j (graph features joined back)
```

### 9.4 Neo4j + Spark Integration

The Neo4j Spark Connector supports reading/writing via DataFrames:

```python
# Read from Neo4j into Spark
df = spark.read \
    .format("org.neo4j.spark.DataSource") \
    .option("url", "neo4j+s://...") \
    .option("query", "MATCH (p:Person)-[:KNOWS]->(f:Person) RETURN p.name, collect(f.name) AS friends") \
    .load()

# Write from Spark to Neo4j
df.write \
    .format("org.neo4j.spark.DataSource") \
    .option("url", "neo4j+s://...") \
    .option("labels", ":Person") \
    .mode("Overwrite") \
    .save()
```

### 9.5 Neo4j + GraphQL

Neo4j GraphQL Library auto-generates a GraphQL API from the graph model:

```javascript
const { Neo4jGraphQL } = require("@neo4j/graphql");
const { Neo4jDriver } = require("neo4j-driver");

const typeDefs = `
  type Person {
    name: String!
    knows: [Person!]! @relationship(type: "KNOWS", direction: OUT)
  }
`;

const neoSchema = new Neo4jGraphQL({ typeDefs, driver });
const schema = await neoSchema.getSchema();
// Expose as Apollo Server, Express, etc.
```

---

## 10. Graph vs. Relational: When to Use Which

### 10.1 Decision Matrix

| Criteria | Choose Graph (Neo4j) | Choose Relational (Postgres, etc.) |
|---|---|---|
| **Connection depth** | Deep traversals (3+ hops) frequent | Shallow joins (1-2 tables) |
| **Relationship cardinality** | Many-to-many, recursive, hierarchical | One-to-many, simple FK lookups |
| **Schema evolution** | Frequent, ad-hoc, per-instance | Stable, predefined migrations |
| **Query pattern** | "Who/what is connected to X through Y?" | "What are the attributes of X?" |
| **Write volume** | Moderate (OLTP) or batch (analytics) | High-velocity OLTP |
| **Data volume** | Hundreds of millions of relationships | Trillions of rows (columnar) |
| **Team expertise** | Data scientists, ML engineers | DBAs, backend engineers |
| **Reporting** | Graph-based analytics (GDS) | SQL BI, OLAP cubes |

### 10.2 When SQL JOINs Become Painful

**Query**: "Find all products purchased by people who bought the same product as Alice and live in the same city as Bob"

```sql
-- SQL (6 JOINs, deeply nested)
SELECT DISTINCT p2.name
FROM users alice
JOIN orders o1 ON alice.id = o1.user_id
JOIN order_items oi1 ON o1.id = oi1.order_id
JOIN products p1 ON oi1.product_id = p1.id
JOIN order_items oi2 ON p1.id = oi2.product_id
JOIN orders o2 ON oi2.order_id = o2.id
JOIN users u2 ON o2.user_id = u2.id
JOIN users bob ON bob.name = 'Bob'
WHERE alice.name = 'Alice'
  AND u2.city = bob.city
  AND u2.id != alice.id;
```

```cypher
-- Cypher (natural pattern match)
MATCH (alice:User {name: "Alice"})-[:PURCHASED]->(:Product)<-[:PURCHASED]-(other:User),
      (bob:User {name: "Bob"})
WHERE other.city = bob.city AND other <> alice
MATCH (other)-[:PURCHASED]->(rec:Product)
WHERE NOT (alice)-[:PURCHASED]->(rec)
RETURN DISTINCT rec.name
```

### 10.3 Hybrid Approaches

Many production systems use both:
- **Postgres** for transactional data (orders, users, inventory)
- **Neo4j** for recommendations, fraud detection, and relationship analytics
- **Elasticsearch** for full-text search
- Sync via CDC (Debezium → Kafka → Neo4j connector)

```python
# Dual database pattern
def get_recommendations(user_id):
    # 1. Get user profile from Postgres (OLTP)
    user = pg_client.query("SELECT * FROM users WHERE id = %s", user_id)

    # 2. Get recommendations from Neo4j (graph traversal)
    with neo4j_driver.session() as session:
        result = session.run("""
            MATCH (me:User {id: $uid})-[:PURCHASED]->(:Product)
                <-[:PURCHASED]-(other:User)
            MATCH (other)-[:PURCHASED]->(rec:Product)
            WHERE NOT (me)-[:PURCHASED]->(rec)
            RETURN rec.id, count(*) AS score
            ORDER BY score DESC LIMIT 10
        """, uid=user_id)
        return [record["rec.id"] for record in result]
```

### 10.4 Cost & Operational Comparison

| Factor | Relational (RDS Postgres) | Graph (Neo4j Aura) |
|--------|--------------------------|-------------------|
| **Query time** (3-hop join) | 500ms – 5s (depending on indexes) | 5ms – 50ms |
| **Query time** (10-hop recursive) | Minutes or timeout | 100ms – 500ms |
| **Schema migration** | ALTER TABLE (locking) | Add label/relationship at runtime |
| **Backup size** | Larger (normalized with indexes) | More compact (pointer-based) |
| **Learning curve** | Widely known | Specialized (Cypher, GDS) |
| **Tool ecosystem** | Mature (every BI tool) | Growing (Bloom, Neodash, GraphQL) |

### 10.5 Rule of Thumb

> **Use a graph database when the relationships between your entities are as important as, or more important than, the entities themselves.**

If your primary query pattern is "find me X by its attributes" with occasional FK lookups → use relational.

If your primary query pattern is "find me everything connected to X through N degrees of separation" → use a graph.

If you need both → use both (polyglot persistence).

---

## Appendix A: Quick Reference — Cypher by Analogy to SQL

| SQL | Cypher |
|-----|--------|
| `SELECT col FROM table` | `RETURN n.prop` |
| `FROM table AS t` | `MATCH (t:Label)` |
| `WHERE t.col = val` | `WHERE t.prop = val` or `MATCH (t {prop: val})` |
| `JOIN t1 ON t1.id = t2.fk` | `(a)-[:REL]->(b)` |
| `LEFT JOIN` | `OPTIONAL MATCH` |
| `GROUP BY col` | Implicit in `RETURN` with aggregation |
| `ORDER BY col LIMIT n` | `ORDER BY col LIMIT n` |
| `INSERT INTO` | `CREATE` or `MERGE` |
| `UPDATE` | `SET n.prop = val` |
| `DELETE` | `DETACH DELETE n` |
| `UNION` | `UNION` |
| `WITH (CTE)` | `WITH` (pipeline) |
| Recursive CTE | Variable-length `[]->{1..n}` |
| `ROW_NUMBER() OVER (PARTITION BY ...)` | Reduce to pattern match + collect |

## Appendix B: Essential CLI Tools

```bash
# neo4j-admin — backup, restore, import
neo4j-admin database dump neo4j --to-backup=/backups/
neo4j-admin database load neo4j --from-backup=/backups/

# cypher-shell — direct Cypher execution
echo "MATCH (n) RETURN count(n)" | cypher-shell -u neo4j -p password

# neo4j-cli — unified agent-friendly CLI
neo4j-cli aura create myinstance --region us-east-1 --type professional
neo4j-cli cypher "MATCH (n) RETURN count(n)"
neo4j-cli schema describe

# Install neo4j-cli
curl -sSfL https://neo4j.sh/install.sh | bash
```

---

*Generated: 2025-06-05 | Based on Neo4j 5.x / Cypher 25 / GDS 2.x*
