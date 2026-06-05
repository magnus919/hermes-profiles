---
name: qa-methodology
description: "Quality assurance methodology — test strategy design, test automation patterns, regression testing, CI quality gates, test data management, and quality metrics. Grounded in practical patterns for teams that want confident shipping."
version: 1.1.0
author: Hermes Agent community
license: MIT
metadata:
  hermes:
    tags: [qa, testing, quality-assurance, test-automation, regression, CI, quality-gates, flaky-tests, quality-metrics]
    related_skills: [verification-methodology, review-methodology, systematic-debugging, implementation-planning]
---

# QA Methodology

Quality assurance is the practice of making confident shipping routine. This methodology covers test strategy, automation, regression management, and quality metrics that scale with a project's complexity.

## The QA Engineer's Domain

| You own | You don't own |
|---------|--------------|
| Test strategy — what to test, at what level, with what priority | Code review — that's the reviewer |
| Test automation — framework selection, test harness setup, CI integration | Root cause analysis of bugs — that's the debugger |
| Regression testing — suites that catch regressions without becoming brittle | Feature implementation — that's the developer |
| Quality gates — CI integration, pass/fail criteria, blocking vs non-blocking | Kanban workflow design — that's the kanban strategist |
| Test data management — fixtures, factories, synthetic data | Production monitoring — that's SRE |
| Quality metrics — coverage analysis, defect density, MTD | Verdict on completion — that's the verifier |

## Reference Files

| Reference | When to load |
|-----------|-------------|
| `references/test-strategy.md` | Designing a test strategy for a new project or feature — test levels, risk analysis, prioritization, automation targets |
| `references/test-automation-gates-metrics.md` | Test automation framework selection, CI integration (parallel execution, sharding, flaky management), quality gate design (pass/fail criteria, blocking vs advisory, evolution), and quality metrics (coverage, defect density, MTTD/MTTR) |
| `references/regression-testing.md` | Building and maintaining regression suites — selection criteria, prioritization, suite evolution, false positive management |

## Core Principles

**If it isn't tested, it's broken** — Untested code is not working code; it's code whose failure mode hasn't been discovered yet.

**Quality is a property of the process, not the artifact** — Testing at the end doesn't create quality. Quality is designed in through test strategy, automation, and gating throughout the development cycle.

**Test behavior, not implementation** — Tests coupled to implementation details break on refactoring. Tests coupled to behavior survive it. Prefer testing what the system does, not how it does it.

**Fast feedback wins** — A test that takes 30 seconds to run gets run more often than a test that takes 30 minutes. Invest in test speed proportional to feedback frequency.

**Flaky tests are worse than no tests** — A test that fails nondeterministically trains teams to ignore failures. Fix or remove flaky tests on detection.
