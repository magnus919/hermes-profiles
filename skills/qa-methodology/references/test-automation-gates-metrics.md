# QA Methodology Reference: Test Automation, Quality Gates & Quality Metrics

> A comprehensive reference for QA engineers, covering test automation patterns, quality gate design, and quality metrics. Researched June 2026.

---

## Table of Contents

1. [Test Framework Selection](#1-test-framework-selection)
2. [CI Integration: Parallel Execution, Sharding & Test Splitting](#2-ci-integration-parallel-execution-sharding--test-splitting)
3. [Flaky Test Management](#3-flaky-test-management)
4. [Quality Gates](#4-quality-gates)
5. [Quality Metrics](#5-quality-metrics)

---

## 1. Test Framework Selection

### 1.1 Framework Decision Matrix

| Criteria | pytest | Playwright | Vitest | Cypress |
|---|---|---|---|---|
| **Language** | Python | JS/TS, Python, .NET, Java | JS/TS (Vite-based) | JS/TS (bundled) |
| **Primary Domain** | Unit, integration, API | E2E browser, mobile (WebKit) | Unit, component, E2E | E2E browser, component |
| **Browser Support** | N/A | Chromium, Firefox, WebKit, Edge | Via Playwright/WDIO browser mode | Chromium, Firefox, Edge, WebKit |
| **Parallelism** | pytest-xdist | Built-in workers + sharding | Built-in worker pool + sharding | Dashboard parallelization (paid) |
| **Auto-wait** | N/A | Yes (built-in) | N/A (VDOM assertions) | Yes (built-in, retry-ability) |
| **Network Mocking** | responses / pytest-httpx | route() API | vi.mock / msw | cy.intercept() |
| **Debugging** | pdb / --pdb | Trace viewer, screenshots, video | Browser DevTools | Time-travel, snapshots |
| **CI-first?** | Yes | Yes (blob reports, sharding) | Yes (sharding, pool) | Dashboard-based |
| **Community** | Mature, 10k+ plugins | Rapidly growing, MS-backed | Growing, Vite ecosystem | Large, mature |
| **Best For** | Python projects, data/API testing | Multi-browser E2E, cross-platform | Vite/React/Vue component & unit | Dev-integrated E2E, component testing |

### 1.2 When to Use Which Framework

**pytest**
- Python projects of any size
- API/integration testing against backends
- Data pipeline validation, DB testing
- Parameterized testing at scale (built-in)
- When you need 500+ plugins (django, mock, cov, xdist, splinter)
- Architecture: `conftest.py` hierarchy with scoped fixtures

**Playwright**
- Cross-browser E2E (Chromium + Firefox + WebKit)
- Mobile Web testing (emulation)
- Network interception and mocking
- When CI speed matters (native sharding + workers)
- Trace viewer for debugging flaky tests
- API testing alongside browser tests (request context)

```typescript
// Playwright sharding in CI
// npx playwright test --shard=1/4
// npx playwright test --shard=2/4
```

**Vitest**
- Vite-based projects (React, Vue, Svelte)
- Component tests with HMR (instant feedback during dev)
- Unit tests needing ES module support
- When you want Jest-compatible API but faster
- Browser mode (experimental) for limited E2E

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config'
export default defineConfig({
  test: {
    globals: true,
    pool: 'forks', // or 'threads'
    poolOptions: { threads: { singleThread: true } },
  },
})
```

**Cypress**
- Developer-focused E2E where debugging UX matters
- Teams already in the JS ecosystem
- Component tests for React/Vue (experimental)
- When time-travel debugging is essential
- Note: limited cross-browser (no Safari) without paid plan

### 1.3 Framework Selection Decision Flow

```
Is the project Python?
   |-- YES --> Use pytest (with xdist for speed)
   |-- NO  --> Is it a Vite-based JS/TS project?
                 |-- YES --> Unit/component: Vitest
                 |          E2E: Playwright or Cypress
                 |-- NO  --> JS/TS non-Vite: Playwright (E2E) + Jest/Vitest (unit)
```

---

## 2. CI Integration: Parallel Execution, Sharding & Test Splitting

### 2.1 Three Levels of Parallelism

| Level | What It Does | Tooling |
|---|---|---|
| **Within a job (multi-worker)** | Multiple tests run on the same machine in parallel | `pytest -n auto` (xdist), Playwright workers, Vitest pool |
| **Across jobs (sharding)** | Test suite split into N groups, each on its own CI runner | `--shard=x/y`, matrix strategy |
| **Across suites** | Different test types (unit, integration, E2E) run in separate CI jobs | CI matrix, workflow orchestration |

### 2.2 Pytest Parallelism

**pytest-xdist (within node)**
```bash
# Auto-detect CPU count
pytest -n auto

# Fixed number of workers
pytest -n 4

# Distribute by scope: each worker gets a subset of tests
pytest -n 4 --dist loadscope   # tests in same module stay together
pytest -n 4 --dist loadfile    # tests in same file stay together
pytest -n 4 --dist worksteal   # dynamic rebalancing (pytest-xdist 3.x+)
```

**pytest-split (across CI jobs)**
```bash
# Job 1
pytest --splits 4 --group 1

# Job 2
pytest --splits 4 --group 2

# Uses timing data from --store-durations to balance groups
```

```yaml
# GitHub Actions: pytest-split with matrix
jobs:
  test:
    strategy:
      matrix:
        group: [1, 2, 3, 4]
    steps:
      - uses: actions/checkout@v4
      - run: pip install pytest pytest-split
      - run: pytest --splits 4 --group ${{ matrix.group }}
```

### 2.3 Playwright Sharding

```yaml
# playwright.config.ts
export default defineConfig({
  fullyParallel: true, // split at test level, not file level
  workers: process.env.CI ? 2 : undefined,
  reporter: process.env.CI ? 'blob' : 'html',
})

# GitHub Actions with matrix
# npx playwright test --shard=${{ matrix.shardIndex }}/${{ matrix.shardTotal }}
jobs:
  test:
    strategy:
      matrix:
        shardIndex: [1, 2, 3, 4]
        shardTotal: [4]
    steps:
      - run: npx playwright test --shard=${{ matrix.shardIndex }}/${{ matrix.shardTotal }}
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: blob-report-${{ matrix.shardIndex }}
          path: blob-report

  merge-reports:
    if: always()
    needs: [test]
    steps:
      - uses: actions/download-artifact@v4
      - run: npx playwright merge-reports --reporter html ./all-blob-reports
```

**Shard Balancing Tips**
- `fullyParallel: true` splits at the individual test level for even distribution
- Without `fullyParallel`, shards split at the file level (files with many tests can unbalance)
- Use `blob` reporter in CI to capture results across shards
- Merge reports into a single HTML for aggregate viewing

### 2.4 Vitest Sharding

```bash
# CLI sharding
vitest --shard=1/4
vitest --shard=2/4

# GitHub Actions with matrix
jobs:
  test:
    strategy:
      matrix:
        shard: [1, 2, 3, 4]
    steps:
      - run: npx vitest --reporter=junit --shard=${{ matrix.shard }}/4
```

**Vitest Pool Options**
| Pool | Description | Best For |
|---|---|---|
| `threads` (default) | Uses worker_threads, fastest | Pure unit tests |
| `forks` | Uses child_process, better isolation | Tests with side effects |
| `vmThreads` | Uses vm module within threads | Tests needing module sandboxing |

```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    pool: 'forks',
    poolOptions: {
      forks: {
        singleFork: false,
        maxForks: 4,
        minForks: 1,
      },
    },
  },
})
```

### 2.5 Cypress Parallelization

Cypress requires the **Dashboard** service (paid) for native parallelization:

```bash
# Autoscales across available CI machines
cypress run --record --parallel
```

Alternatively, use **cypress-split** (open source) for manual splitting:
```bash
# Job 1
cypress run --env split=1,of=4

# Job 2
cypress run --env split=2,of=4
```

### 2.6 Best Practices for CI Test Distribution

1. **Log historical timing data** — tools like pytest-split use previous run durations to balance groups. Run `--store-durations` on a baseline first.
2. **Set job-level timeouts** — prevent hung workers from blocking the pipeline.
3. **Fail fast on critical failures** — separate critical (blocking) tests from advisory tests so critical failures halt early.
4. **Use dependency caching** — cache node_modules, .cache, and pip packages between shards.
5. **Shard by timing, not alphabetically** — alphabetically splitting tests creates unbalanced groups.

---

## 3. Flaky Test Management

### 3.1 Definition & Impact

> A flaky (or flakey) test is an automated test that produces inconsistent outcomes — green one run, red the next — with no changes to code or test environment.

**Impact Summary**
- **Delayed PRs** — developers rerun jobs or request overrides
- **Higher CI costs** — repeated runs consume compute
- **Loss of trust** — teams bypass automation for manual checks
- **Customer risk** — real defects masked by noise
- **Quantifiable**: 5% flakiness on 10,000 daily tests = 500 false failures/day (~40+ hours lost/week)

### 3.2 Root Causes

| Category | Examples | Fix Pattern |
|---|---|---|
| **Async / Race Conditions** | Click before element ready, DOM not updated | Explicit waits, auto-waiting frameworks |
| **External Dependencies** | API latency, DB connection flakiness | Mock/stub external services |
| **Uncontrolled Test Data** | Random data, data collisions | Seeded randomness, idempotent setup |
| **Environment Issues** | CI resource contention, clock skew | Increase resources, isolate test environments |
| **State Leakage** | Shared mutable state, bad teardown | Isolated state per test, fixture cleanup |
| **Test Interdependence** | Test B depends on Test A's state | Fully independent tests, random execution order |

### 3.3 Detection Strategies

```bash
# Repeat test to reproduce flakiness
pytest --repeat 20 test_flaky.py
npx playwright test --repeat-each=20
npx vitest --repeats 10
```

**Automated Detection**
1. **Retry analysis** — track which tests fail on first attempt but pass on retry
2. **Cross-environment comparison** — compare pass/fail across branches and CI runners
3. **Statistical trending** — track flakiness rate per test over time (failures / total runs)
4. **Burn-in** — run new tests 100+ times in CI before allowing into the main suite

### 3.4 Management Framework

```
Detection --> Measurement --> Prioritization --> Resolution --> Prevention
```

| Phase | Actions |
|---|---|
| **Detection** | Retries (2-3x), repeat-each runs, cross-branch analysis |
| **Measurement** | Flakiness Rate = failures / runs; set threshold (<1-2%) |
| **Prioritization** | Fix core workflow / critical-path tests first; quarantine non-critical |
| **Resolution** | Reproduce locally, inspect traces/logs/videos, stabilize waits/selectors |
| **Prevention** | Ownership assignment, flakiness budgets, dashboards + alerts |

### 3.5 Auto-Retry vs Quarantine

| Strategy | How It Works | When to Use |
|---|---|---|
| **Auto-retry** | Test that fails on first attempt is retried 1-3x before reporting failure | Smoke tests, CI where 1-2% flakiness is tolerated |
| **Quarantine** | Flaky test moved to separate suite; runs but doesn't block pipeline | Tests > 5% flaky, or blocking PRs |
| **Blocking** | Test must pass every time without retry | Critical-path tests, security, payment flows |

```yaml
# Playwright: auto-retry with limits
# playwright.config.ts
export default defineConfig({
  retries: process.env.CI ? 2 : 0,
})
```

### 3.6 Stabilization Patterns

**Stable selectors and waits (Playwright)**
```typescript
// BAD: blind sleep
await page.waitForTimeout(3000)

// GOOD: await observable state
await expect(page.locator('[data-testid="submit"]')).toBeVisible({ timeout: 5000 })
await page.waitForLoadState('networkidle')
await page.waitForResponse(resp => resp.url().includes('/api/login') && resp.status() === 200)
```

**Controlled test data (pytest)**
```python
import uuid

def test_create_user(db_session):
    unique_email = f"test-{uuid.uuid4()}@example.com"
    # use unique_email to prevent collision
```

**Isolated fixtures (pytest)**
```python
@pytest.fixture(autouse=True)
def clean_state(db_session):
    yield
    db_session.rollback()  # never leak state between tests
```

**Mocking external services**
```python
# pytest with responses library
import responses

@responses.activate
def test_api_call():
    responses.get("https://api.example.com/data", json={"key": "value"})
    # test now has 0 flakiness from network
```

### 3.7 Burn-in Protocol

New tests should prove their reliability before entering the main suite:

1. **Commit test** → run in PR pipeline
2. **Burn-in period** → run 100+ times in CI (bg job or nightly)
3. **Stability check** → if flakiness rate > threshold, quarantine until fixed
4. **Promotion** → move to main test suite once proven stable

---

## 4. Quality Gates

### 4.1 Definition & Core Principles

> A quality gate is an enforced measure built into your pipeline that must be satisfied before the software can proceed to the next stage or be released.

**Core Principles**

| Principle | Description |
|---|---|
| **Shift left** | Catch issues as early as possible — static analysis before unit tests, unit tests before integration |
| **Automate by default** | Prefer automated gates; only use manual approvals where regulatory compliance requires them |
| **Fast feedback** | Quick gates run first (linting, unit tests); slower gates (E2E, performance) run later |
| **Make pass/fail unambiguous** | Criteria must be binary — no "mostly passes" |
| **Allow manual override** | Emergency bypass must exist with accountability (multi-party approval, audit trail) |
| **Evolve over time** | Gate thresholds should tighten as the project matures |

### 4.2 Gate Types: Blocking vs Advisory

| Type | Behavior | CI Signal | Example |
|---|---|---|---|
| **Blocking** | Pipeline stops. Artifact is not promoted. Release is blocked. | ❌ Red | Unit test failure, security vulnerability |
| **Advisory** | Pipeline continues. Warning is logged. Team notified. | ⚠️ Warn-only | Code coverage dropped under threshold, linting warnings |
| **Informational** | No pipeline impact. Metric recorded for dashboard. | ℹ️ Info | Test execution time trend, flakiness rate |

**Mixing blocking and advisory gates by stage:**

```
Commit --> [Lint (advisory)] --> [Unit tests (blocking)]
  --> [Build (blocking)] --> [Static analysis (advisory)]
    --> [Integration tests (blocking)] --> [E2E tests (blocking)]
      --> [Performance/load (advisory)] --> [Security scan (blocking)]
        --> [Manual approval (blocking)] --> Release
```

### 4.3 Common Quality Gates by Pipeline Stage

| Stage | Gate | Type | Threshold |
|---|---|---|---|
| **Code commit** | Linting / formatting | Advisory | 0 errors; formatting warnings logged |
| **Build** | Compilation | Blocking | 0 compile errors |
| **Unit tests** | Pass rate | Blocking | 100% pass (known fails = 0) |
| **Code coverage** | Coverage threshold | Advisory → Blocking | Unit ≥ 80%, Integration ≥ 60% |
| **Static analysis** | Bugs / smells | Blocking | 0 critical/blocker bugs |
| **Security** | SAST / dependency check | Blocking | 0 known CVEs above threshold |
| **Integration tests** | Pass rate | Blocking | 100% pass |
| **E2E tests** | Pass rate | Blocking | 100% pass (with flake retry budget) |
| **Performance** | Response time / throughput | Advisory | p95 < 500ms, no regression > 10% |
| **Flaky tests** | Quarantine count | Advisory | < N flaky tests in suite |

### 4.4 Implementing Quality Gates in CI

**GitHub Actions example — staged gates**

```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - run: npm run lint
        continue-on-error: true  # advisory: warn but continue

  unit-tests:
    needs: [lint]
    runs-on: ubuntu-latest
    steps:
      - run: npm test -- --coverage
      - run: |
          # Advisory: coverage check (warns but doesn't fail)
          npx istanbul check-coverage --statement=80

  integration:
    needs: [unit-tests]
    runs-on: ubuntu-latest
    steps:
      - run: npm run test:integration
        # Blocking: integration tests must all pass

  e2e:
    needs: [integration]
    runs-on: ubuntu-latest
    steps:
      - run: npx playwright test
        # Blocking: E2E must pass

  security-scan:
    needs: [unit-tests]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - run: npm audit --audit-level=high
```

**Jenkins Pipeline — declarative gates**

```groovy
stage('Quality Gates') {
    steps {
        // Blocking: test pass
        sh 'pytest tests/unit --junitxml=unit-results.xml'

        // Advisory: coverage
        sh '''
            coverage=$(python -c "import json; d=json.load(open('coverage.json')); print(d['totals']['percent_covered'])")
            if (( $(echo "$coverage < 80" | bc -l) )); then
                echo "WARNING: Coverage ${coverage}% below 80% threshold"
                # Don't fail the build
            fi
        '''

        // Blocking: SonarQube quality gate
        withSonarQubeEnv('SonarQube') {
            sh 'mvn sonar:sonar'
        }
        timeout(time: 5, unit: 'MINUTES') {
            waitForQualityGate abortPipeline: true
        }
    }
}
```

### 4.5 Security Gates

| Check | Tooling | Gate Behavior |
|---|---|---|
| **SAST** | SonarQube, Semgrep, CodeQL | Block on critical/high findings |
| **SCA (dependency vulns)** | Dependabot, Snyk, OWASP DC | Block on CVSS ≥ 7.0 |
| **Secrets detection** | GitLeaks, TruffleHog | Block on any hardcoded secret |
| **Container scanning** | Trivy, Grype | Block on critical OS-level CVEs |
| **License compliance** | FOSSA, LicenseFinder | Block on GPL/AFL in commercial project |

### 4.6 Quality Gate Evolution

Gates should tighten as the project and team mature:

```
Phase 1 (Starting out):
  - Blocking: tests must compile and pass
  - Advisory: coverage > 50%

Phase 2 (Growing):
  - Blocking: unit tests pass, coverage > 70%, 0 critical SonarQube issues
  - Advisory: coverage > 80%, security scan clean

Phase 3 (Maturing):
  - Blocking: all tests pass, coverage > 80%, 0 blocker/critical SonarQube, 0 high CVEs
  - Advisory: coverage > 85%, flakiness < 2%

Phase 4 (High performance):
  - Blocking: all tests pass, coverage > 85%, 0 SonarQube bugs, 0 CVEs above threshold
  - Advisory: coverage > 90%, performance regression < 5%, flakiness < 1%
```

**Gate review cadence:** Re-evaluate gate thresholds quarterly. If a gate never fires (all PRs pass trivially), consider tightening it. If a gate fires too frequently (50%+ of PRs blocked), loosen it temporarily while the team improves code quality.

### 4.7 Common Anti-Patterns

| Anti-pattern | Problem | Fix |
|---|---|---|
| **Too many blocking gates** | Developers bypass or game the pipeline | Keep blocking gates to critical checks; use advisory for everything else |
| **Gates that never change** | Thresholds become irrelevant as project evolves | Review quarterly, tighten gradually |
| **Measuring coverage without quality** | 90% coverage of untested logic is misleading | Combine coverage with mutation testing or code review |
| **Single flaky test blocks the entire pipeline** | Loss of trust in CI | Quarantine flaky tests automatically; separate blocking vs advisory suites |
| **Manual gates for everything** | Pipeline becomes the bottleneck | Automate everything that can be scripted; keep manual for regulatory sign-offs only |

---

## 5. Quality Metrics

### 5.1 The 5-10 Rule

Track only **5-10 core metrics** that directly inform decisions. Fewer than 5 misses signals; more than 10 causes analysis paralysis and actionability drops.

### 5.2 Metric Taxonomy

| Type | Definition | Examples |
|---|---|---|
| **Absolute** | Raw counts | Tests run, bugs found, lines of code |
| **Derived** | Ratios / percentages | Coverage %, pass rate %, defect density |
| **Leading** | Predicts future quality | Test coverage, execution status, code complexity |
| **Lagging** | Validates past outcomes | Production escapes, customer complaints, MTTR |
| **Effectiveness** | Does testing catch bugs? | Defect detection percentage, test effectiveness ratio |
| **Efficiency** | How fast is testing? | Test execution time, time to test bug fix |

### 5.3 Core Metrics — Formulas & Guidance

#### 5.3.1 Test Coverage

```text
Line Coverage = (Lines executed / Total lines) × 100
Branch Coverage = (Branches executed / Total branches) × 100
Function Coverage = (Functions called / Total functions) × 100
```

**Practical guidance:**
- 100% coverage is a trap — diminishing returns after ~80%
- Focus coverage on high-risk areas: payment flows, auth, data transformations
- Combine **line coverage** + **branch coverage** (line only misses `if` branches)
- Mutation testing (pitest, mutmut) validates coverage quality — high line coverage but low mutation score means tests don't actually assert behavior

```bash
# pytest coverage
pytest --cov=src --cov-report=term-missing --cov-fail-under=80

# vitest coverage
npx vitest --coverage --coverage.thresholds.lines 80
```

#### 5.3.2 Defect Density

```text
Defect Density = Total confirmed defects / Software size (LOC or function points)
```

**Interpretation:**
- Lower is better, but context matters (complex modules naturally have higher density)
- **Stratify by severity**: critical: 0.5/KLOC, minor: 2/KLOC → same density, different risk profiles
- **Stratify by module**: find modules with abnormally high density for targeted refactoring
- **Combine with coverage**: high defect density + low coverage = urgent improvement needed

**Common pitfalls:**
- Comparing defect density across projects of different types (libraries vs applications)
- Including duplicate/won't-fix bugs in the count
- Not normalizing for code complexity (a simple CRUD module vs complex algorithm)

#### 5.3.3 Test Effectiveness

```text
Test Effectiveness = (Defects found by testing / Total defects found) × 100

Or more practically:
DDP (Defect Detection Percentage) = (Bugs found before release / (Bugs found before + after release)) × 100
```

**Goal:** DDP > 95% means fewer than 5% of bugs reach production.

**Measuring what tests catch:**
- Track which tests actually find bugs (linked in bug tracker)
- Identify tests that never fail → candidates for removal or rewriting
- **Regression test effectiveness**: of bugs fixed, how many had a regression test added? Target > 80%.

#### 5.3.4 MTTD (Mean Time to Detect)

```text
MTTD = Sum of (Detection time - Introduction time) / Total defects found
```

Where detection time = when the bug was first observed (not when reported).

| Scenario | Typical MTTD | Interpretation |
|---|---|---|
| Automated test catches bug in PR | Minutes | Excellent — shift-left detection |
| Caught in staging CI | Hours | Good |
| Caught in QA period | Days | Needs faster feedback |
| Caught in production by monitoring | Hours–days | Acceptable for edge cases |
| Caught in production by customer report | Days–weeks | Poor — invest in monitoring |

**Reducing MTTD:**
- Expand automated test coverage
- Improve production monitoring (APM, error tracking)
- Feature flags for gradual rollouts
- Real user monitoring (RUM) and session replay

#### 5.3.5 MTTR (Mean Time to Resolve / Repair)

```text
MTTR = Sum of (Resolution time - Detection time) / Total defects fixed
```

MTTR includes: triage → debug → fix → test → deploy

**Targets by severity:**
| Severity | Target MTTR |
|---|---|
| Critical (P0) | < 1 hour |
| High (P1) | < 4 hours |
| Medium (P2) | < 24 hours |
| Low (P3) | < 1 week |

**Reducing MTTR:**
- Automated rollback (fast revert)
- Feature flags to disable problematic code without redeploy
- Structured debugging tools (Playwright traces, log correlation)
- Post-incident reviews to eliminate process bottlenecks

#### 5.3.6 Defect Escape Rate

```text
Defect Escape Rate = Production defects / (Pre-production defects + Production defects) × 100
```

**Interpretation:**
- < 5%: Strong QA process
- 5-15%: Average — room for improvement
- > 15%: Significant escape pattern — invest in shift-left testing

### 5.4 Visualizing Metrics

**Recommended dashboard structure:**

```
╔══════════════════════════════════════╗
║  Quality Dashboard — Sprint 24      ║
╠══════════════════════════════════════╣
║  PASS RATE  │  COVERAGE  │ DEFECTS  ║
║  98.5% ✓    │  83% ⚠️    │  12 (3 P1)║
╠══════════════════════════════════════╣
║  DDP        │  MTTD      │  MTTR    ║
║  94% ✓      │  2.1h ✓    │  4.5h ⚠️ ║
╠══════════════════════════════════════╣
║  FLAKINESS  │  SUITE DUR │  BUDGET  ║
║  1.2% ✓     │  14m ✓     │  62% ▓██ ║
╚══════════════════════════════════════╝
```

### 5.5 Metric Selection Per Methodology

| Methodology | Priority Metrics |
|---|---|
| **Agile / Scrum** | Sprint pass rate, defect escape rate, test execution status, velocity-adjusted coverage |
| **Kanban** | Lead time to test, cycle time per fix, flow efficiency, WIP limits |
| **CI/CD** | Build stability, deployment frequency, change failure rate, MTTD, MTTR |
| **Waterfall** | Requirements coverage, phase-wise defect density, test case effectiveness |

### 5.6 Data-Driven Quality Culture

**Implementation principles:**
1. **Can you act on it?** — If a metric changes, do you know what to do next? If not, don't track it.
2. **Can you update it regularly?** — Match refresh frequency to decision cadence (daily for CI, sprintly for coverage, monthly for trends).
3. **Align with goals** — Faster releases = track speed + quality together (change failure rate).
4. **Avoid vanity metrics** — "Tests executed" is activity; "Tests that caught a real bug" is value.
5. **Share broadly** — Developers, PMs, and executives all get relevant slices of the same data.

---

## Quick Reference Summary

### Test Framework Cheatsheet

| Need | Pick |
|---|---|
| Python API/unit tests | pytest + xdist + pytest-cov |
| Multi-browser E2E | Playwright (sharding, trace viewer) |
| Vite/React component tests | Vitest (HMR, browser mode) |
| Dev-focused E2E debugging | Cypress (time-travel, retry-ability) |

### CI Parallelism Cheatsheet

| Tool | Within Node | Across CI Jobs | Timing Balance |
|---|---|---|---|
| pytest | `-n auto` (xdist) | pytest-split (`--splits N --group X`) | `--store-durations` |
| Playwright | `workers: N` | `--shard=x/y` | `fullyParallel: true` |
| Vitest | `poolOptions.forks.maxForks` | `--shard=x/y` | Pool-level balancing |
| Cypress | Auto (Dashboard) | `--parallel` (Dashboard) or cypress-split | Dashboard-managed |

### Quality Gates Cheatsheet

| Gate | Stage | Type | Threshold |
|---|---|---|---|
| Pass unit tests | Build → Integration | Blocking | 100% |
| Coverage ≥ 80% | After unit tests | Advisory → Blocking | Line + branch |
| No critical SonarQube | Static analysis | Blocking | 0 blocker + critical |
| No high CVEs | Security scan | Blocking | CVSS ≥ 7.0 |
| E2E tests pass | Pre-deployment | Blocking | 100% (retry budget) |
| Performance < 10% regression | Load test | Advisory | p95, throughput |

### Quality Metrics Cheatsheet

| Metric | Target | Formula |
|---|---|---|
| Defect Detection Percentage | > 95% | pre-release / (pre + post) × 100 |
| Defect Density | < 1/KLOC (critical), < 5/KLOC (all) | defects / LOC × 1000 |
| Line Coverage | > 80% | executed lines / total lines × 100 |
| MTTD | < 2 hours | sum(detection time) / defects |
| MTTR (critical) | < 1 hour | sum(resolution time) / fixes |
| Flakiness Rate | < 2% | flaky failures / total runs × 100 |
| Defect Escape Rate | < 5% | production defects / total defects × 100 |

---

*Document produced June 2026. Sources include Playwright docs, Vitest docs, SonarSource, TestRail, Currents, Information Week, MinimumCD Practice Guide, and industry patterns from leading QA teams.*
