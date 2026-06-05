---
name: implementation-planning
description: "Implementation planning methodology — work breakdown, dependency analysis, critical path identification, risk assessment, and rollback planning."
version: 1.0.0
author: Hermes Agent community
license: MIT
metadata:
  hermes:
    tags: [implementation, planning, work-breakdown, critical-path, risk, rollback]
---

# Implementation Planning Methodology

Translating architecture into an executable sequence of work with explicit dependencies, risks, and buffers.

## The Planning Lifecycle

```
DECOMPOSE → SEQUENCE → RISK → BUFFER → VERIFY
```

## Reference Files

| Reference | When to load |
|-----------|-------------|
| `references/work-breakdown.md` | You need to decompose architecture into estimable work units |
| `references/dependency-analysis.md` | You need to identify dependency chains and the critical path |
| `references/risk-assessment.md` | You need to score risks with probability, impact, mitigations |
| `references/rollback-planning.md` | You need to ensure every deployable phase has a rollback strategy |
