# Interface Extraction — Worked Example

This reference demonstrates the Phase 3b interface extraction pattern using the [cashew thought-graph library](https://github.com/rajkripal/cashew) (MIT license) as the target codebase. The goal was to extract the implicit storage contract to design a provider-agnostic DAO interface enabling swappable backends (sqlite-vec, KuzuDB, DuckDB+vss, etc.).

This is a teaching example — the methodology, not the specific project, is what generalizes.

## The Five Steps

### Step 1 — Philosophy First

Read PHILOSOPHY.md, DESIGN.md, and README.md before touching code. The cashew repo's philosophy revealed a critical constraint: **"dumb graph, smart reasoning layer"** — edges carry no type labels, node types are descriptive hints for the LLM only, not load-bearing for graph engine operations. This constraint must be baked into the contract. The `Edge` dataclass has no `type` or `label` field.

### Step 2 — Catalog Every Storage Operation

Read all core modules and extracted every distinct database operation:

| Module | Operations | Current Implementation |
|--------|-----------|-----------------------|
| db.py | Node CRUD, connection mgmt, schema migration | Thin sqlite3 wrappers, schema in constants |
| embeddings.py | KNN search, dual-write, dim-mismatch, novelty check | vec0 fast path + numpy O(N) fallback + text Jaccard fallback |
| sleep.py | Cross-link candidates, dedup clusters, GC, core promotion | sklearn pairwise matrix, Bron-Kerbosch, random sampling via SQL |
| retrieval.py | Embedding search → BFS walk → hybrid score | vec0 query + recursive CTEs + manual scoring |
| traversal.py | Trace derivation paths, audit | Recursive CTEs, UNION BFS, DFS in Python |
| session.py | Context assembly, access tracking, node creation | db.py primitives + timestamp bumps |
| graph_utils.py | Load embeddings for batch operations | Full embeddings table → numpy array |

### Step 3 — Identify Boundary Leaks (Workarounds)

Four workarounds signaled the boundary was in the wrong place:

1. **Dual-write vector storage** — every embed writes to two tables (embeddings BLOB + vec_embeddings virtual table), with dim-mismatch detection and a three-layer fallback chain (vec0 → numpy → Jaccard). This is the cost of sqlite-vec not supporting native HNSW.

2. **O(N²) pairwise matrix in application memory** — the sleep cycle loads all embeddings into sklearn for cosine similarity, hitting ~160GB for 200K 1024-dim nodes. A native HNSW provider would do this incrementally.

3. **Recursive CTEs in Python strings** — graph traversal is hand-rolled via raw SQL recursive CTEs that a native graph DB would do with a single `MATCH` clause.

4. **Full-table load into numpy** — cross-link candidate discovery loads the entire embeddings table into memory instead of incremental approximate queries.

**Key lesson:** These are not bugs. They are signals telling you where the architectural boundary is currently leaking. Each one is a candidate to push behind the contract.

### Step 4 — Design the Contract

Produce a Python ABC (Abstract Base Class) with ~30 methods across 8 domains:

- `StorageProvider` base class with `initialize()`/`close()` lifecycle
- Node CRUD: `create_node`, `get_node`, `update_node`, `delete_node`, `scan_nodes`, `count_nodes`
- Edge CRUD (dumb graph — no edge types): `create_edge`, `get_neighbors`, `delete_incident_edges`, `redirect_edges`
- Vector KNN: `set_embedding`, `get_embedding`, `find_similar`, `find_similar_by_id`, `scan_embeddings`
- Graph traversal: `bfs`, `shortest_path`, `trace_derivation`
- Batch/maintenance: `find_cross_link_candidates`, `find_near_duplicates`, `random_sample`, `get_graph_metrics`
- Transactions and introspection

**Key decisions:**
- `find_cross_link_candidates` returns candidate pairs but does not specify *how* — sqlite-vec does O(N²) internally, HNSW providers query incrementally
- `find_near_duplicates` (Bron-Kerbosch algorithm) stays in application code as business logic, not storage
- `random_sample` is a provider operation — native sampling is far more efficient than loading everything to Python
- No edge type/label field anywhere — the dumb-graph constraint is enforced at the data-model level

### Step 5 — Two-Provider Proof Concept

Design two provider implementations to validate the contract:

- **Provider A (sqlite-vec):** wraps the existing dual-write, sklearn matrix, recursive CTEs, dim-mismatch detection into the contract. All the workarounds become *this provider's internal complexity*, not application core's.

- **Provider B (KuzuDB):** second implementation proving the contract is complete. Native HNSW means `set_embedding` is a column write, `find_similar` is `QUERY_VECTOR_INDEX`, `shortest_path` is `MATCH`. No fallback chains — the provider is simpler because the substrate handles it.

Both providers pass the same test suite, proving the abstraction is sound.

## Key Takeaways

1. **The philosophy is the constraint.** Read it before touching code — it tells you what the interface must respect.

2. **Workarounds are signals.** Dual-write, fallback chains, full-table loads, hand-rolled graph traversals in SQL — each one tells you where the boundary is leaking.

3. **Design against what the codebase *needs*, not what the current substrate *does*.** The interface represents the application's requirements, not the current provider's capabilities.

4. **The two-provider proof catches leaks.** If you can't implement a second provider against the same interface, the contract has holes.

5. **Expensive operations define the performance profile.** `find_similar`, `find_cross_link_candidates`, and `bfs` are the operations that determine whether the system is fast or slow. The contract must make them implementable efficiently on a native substrate.
