# Worked Example: Cashew Sleep Cycle Refactor

A real PR that demonstrates the backward-compat shell-and-pipeline pattern,
issued to upstream ([#66](https://github.com/rajkripal/cashew/pull/66)).

## Context

**Source:** Upstream thought-graph memory library.
**Goal:** Port proven improvements from a fork upstream without breaking existing callers.

## The Pattern Used

### 1. Cross-repo comparison (10 improvements identified)

| Improvement | Upstream (old) | Fork (new) |
|---|---|---|
| Scaling strategy | Full O(N²) every cycle | Work-capped at 2000 nodes |
| DB writes | One SELECT+INSERT+commit per pair | Batched executemany, 500/commit |
| Architecture | Stateful class with implicit connections | Pure functions with explicit conn |
| Vector validation | None — NaN/inf crash sklearn silently | Filter before matrix computation |
| Dedup algorithm | Bron-Kerbosch maximal cliques (O(3^(n/3))) | BFS connected components (O(N)) |
| Cross-source noise | No filter — links same-source pairs | Skip pairs sharing source_file |
| Edge cap | None — unlimited growth | Hard cap at 100K edges/cycle |
| Async LLM | Blocks caller for ~60s dream generation | Daemon thread |
| Orphan detection | Not checked | Auto-embed missing nodes |
| WAL mode | DELETE journal | Explicit WAL enable |

### 2. Shell-and-pipeline architecture

```
SleepProtocol.run_sleep_cycle()                # ← old interface (class)
  │
  ├─ conn = self._get_connection()
  ├─ has_embeddings = check table exists
  │
  ├─ if NOT has_embeddings:
  │     └─ _run_sleep_cycle_legacy()           # ← old code path
  │        # calls individual class methods
  │        # (find_cross_link_candidates, cross_link_nodes, ...)
  │        # text-based Jaccard fallback
  │
  └─ if has_embeddings:
        └─ run_sleep_cycle()                    # ← new pipeline (free fn)
           # Phase 1: _find_pairs()
           # Phase 2: _batch_cross_links()
           # Phase 3: _run_dedup()
           # Phase 4: _compute_metrics()
           # Phase 5: _garbage_collect()
           # Phase 6: _evaluate_permanence()
           # Phase 7: _promote_core_memories()
           # Phase 8: _generate_dream()
           # Phase 9: _embed_orphans()
```

### 3. Dispatch check code pattern

```python
# Inside SleepProtocol.run_sleep_cycle():
def run_sleep_cycle(self, model_fn=None, **kwargs):
    conn = self._get_connection()
    has_embeddings = conn.execute(
        "SELECT name FROM sqlite_master "
        "WHERE type='table' AND name='embeddings'"
    ).fetchone() is not None
    conn.close()

    if not has_embeddings:
        # Old path: per-method calls, text-based fallback
        return self._run_sleep_cycle_legacy(model_fn=model_fn)

    # New path: vectorized pipeline
    return run_sleep_cycle(
        db_path=self.db_path,
        limit=kwargs.get("limit", 2000),
        model_fn=model_fn,
        background_dream=kwargs.get("background_dream", False),
        ...
    )
```

### 4. Preserved all existing tests + added new ones

| Test file | Tests | Status |
|---|---|---|
| `tests/test_sleep.py` | 38 (original) | All pass unchanged |
| `tests/test_sleep_refactor.py` | 23 (new) | All pass |
| **Total** | **61** | **Green** |

### 5. Documentation delta

| Doc | What changed |
|---|---|
| `CLAUDE.md` | Sleep Cycle section replaced with 9-phase pipeline description |
| `DESIGN.md` | §4.5 updated from 5-step to 9-step pipeline |

## Key Implementation Decisions

### Why the legacy fallback exists

The tests created temporary databases without an `embeddings` table — and the
old code path handled this by catching sklearn exceptions and falling back to
text Jaccard. Rather than modifying every test fixture, the legacy fallback
preserves the exact old behavior. The new pipeline only activates when the
embeddings table is present.

### Why each phase is a free function

Each phase is independently testable, can be run in isolation, and has explicit
dependency injection (the `conn` parameter). No hidden state. This makes it
trivial to:
- Test a single phase with a synthetic database
- Reorder phases without touching class state
- Skip phases when their preconditions aren't met

### Why Bron-Kerbosch was preserved

The existing `find_merge_clusters()` method uses Bron-Kerbosch maximal clique
enumeration because one test explicitly verifies that a chain A-B-C-D does NOT
produce a single 4-node cluster (connected components would merge all of them).
The new pipeline uses connected-components BFS for dedup, which is correct for
the dedup case (you DO want transitive merging). Both algorithms coexist.
