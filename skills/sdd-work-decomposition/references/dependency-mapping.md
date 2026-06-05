# Dependency Mapping

Identifying real, spec-derived dependencies between tasks.

## Real vs Apparent Dependencies

A dependency is **real** when task B requires task A's output — a function, a schema, a data structure, a file — that B cannot independently stub or mock.

A dependency is **apparent** (not real) when B only needs to know A's interface contract. If the spec defines the interface, B can implement against the contract and test with a stub while A is still being implemented.

**Rule:** If the spec is complete enough to define the contract between A and B, the dependency is NOT real. Both tasks can proceed in parallel against the spec's contract definition.

## Dependency Types

| Type | Real? | Example |
|------|-------|---------|
| Interface dependency | No, if contract is spec'd | B needs A's function signature — but the spec defines it |
| Data dependency | Yes | B needs A's output data (file, database record) |
| State dependency | Conditional | B needs the system to be in a state that A creates — may be satisfiable by seeding test data |
| Knowledge dependency | No | B needs information that A discovered — the spec should contain it |
| Infrastructure dependency | Yes | B needs the database to exist, which A sets up |

## The Stub Test

To test whether a dependency is real:
1. Can B implement against a hardcoded mock of A's output?
2. If yes: the dependency is not real. The contract is sufficient.
3. If no: the dependency is real. B must wait for A.

## Dependency Graph Notation

```
T-001 → T-002: T-002 needs the schema defined in T-001
T-001 → T-003: T-003 needs the schema defined in T-001
T-002 ─ T-003: No dependency (parallel execution possible)
T-004 → T-005: T-005 needs T-004's database migration
```

The critical path is the longest chain of real dependencies. Tasks not on the critical path have scheduling flexibility — they can be delayed without affecting the overall timeline.
