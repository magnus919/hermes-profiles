# Test Strategy Design

## Test Pyramid

```
        ╱╲
       ╱ E2E ╲         Few — critical user journeys
      ╱────────╲
     ╱          ╲
    ╱ Integration ╲     Some — contract tests, API tests, service boundaries
   ╱────────────────╲
  ╱                  ╲
 ╱   Unit / Component ╲    Many — isolated, fast, deterministic
╱────────────────────────╲
```

| Level | Speed | Cost to maintain | What it catches |
|-------|-------|-----------------|-----------------|
| Unit | ms | Low | Logic errors, edge cases, invariants |
| Integration | seconds | Medium | Contract mismatches, data flow errors |
| E2E | minutes | High | System behavior, user-visible regressions |

## Risk-Based Prioritization

| Risk Level | Test Coverage Required | Example |
|------------|----------------------|---------|
| Critical (P0) | 100% — every path, every edge case | Payment processing, auth, data integrity |
| High (P1) | 90%+ — all happy paths, known failure modes | Core business logic, API contracts |
| Medium (P2) | 70%+ — happy paths, common failure modes | Secondary features, non-critical APIs |
| Low (P3) | Smoke test only | UI polish, optional features, debug tooling |

## Test Selection by Project Type

| Project Type | Recommended Test Mix |
|-------------|---------------------|
| Library / SDK | 80% unit, 15% integration, 5% E2E |
| Web API | 40% unit, 40% integration, 20% E2E |
| Web application | 30% unit, 40% integration, 30% E2E |
| CLI tool | 60% unit, 30% integration (output comparison), 10% E2E |
| Data pipeline | 50% unit, 40% integration (data flow), 10% E2E |
