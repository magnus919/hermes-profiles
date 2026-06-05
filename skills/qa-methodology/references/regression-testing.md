# Regression Testing

## What Belongs in a Regression Suite

| Include | Exclude |
|---------|---------|
| Every fixed bug (as a test) | Tests that haven't failed in 6+ months (archive) |
| Critical user paths | Tests for deprecated features |
| Known failure patterns | Tests that overlap with lower-level coverage |
| API contract checks | Visual regression tests for work-in-progress UI |
| Data integrity assertions | Performance tests (separate suite) |

## Suite Hygiene

| Condition | Action |
|-----------|--------|
| Test hasn't failed in 6 months | Consider archiving — it may not be testing anything meaningful |
| Test flakes > 1% over 10 runs | Investigate and fix or remove immediately |
| Test takes > 5s (unit) / > 30s (integration) | Optimize or promote to slower tier |
| Test depends on another test's state | Fix isolation — tests must be independent |
| Test runs against production data | Switch to synthetic fixtures |

## Change-Based Test Selection

Not every change needs the full regression suite. For targeted changes:

| Change Type | Required Tests |
|-------------|---------------|
| Bug fix | Test that reproduces the bug + related unit tests |
| Feature addition | New feature tests + smoke tests on adjacent areas |
| Refactoring | Full unit suite + integration smoke tests |
| Configuration change | Smoke tests on affected components |
| Dependency update | Full regression suite |
| Infrastructure change | Integration + E2E suite |
