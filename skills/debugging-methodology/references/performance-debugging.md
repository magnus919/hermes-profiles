# Performance Debugging

## Approach

1. **Define the baseline.** What's the expected performance? (p99 latency, throughput, memory usage)
2. **Profile before optimizing.** Measure first, then optimize. Without measurement, you're guessing.
3. **One change at a time.** Isolate which change produced the improvement.

## Common Performance Patterns

| Symptom | Likely Cause | Investigation |
|---------|-------------|---------------|
| High latency | Blocking I/O, serialization, slow dependency | Trace request flow, measure each step |
| High CPU | Tight loop, excessive GC, inefficient algorithm | CPU profile, identify hot spots |
| High memory | Leak, cache bloat, large object allocations | Heap dump, allocation tracking |
| Low throughput | Contention, connection pool exhaustion, serial bottlenecks | Check locks, pool sizes, queue depths |
