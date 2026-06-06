---
name: technology-radar
description: >-
  CTO methodology for technology evaluation, architecture governance,
  build-vs-buy decisions, engineering metrics, technical debt quantification,
  and innovation pipeline management. Covers technology radar framework
  (Adopt/Trial/Assess/Hold), TCO analysis, architecture review boards,
  RFC processes, DORA/SPACE/DevEx metrics, debt interest calculation, and
  POC-to-production readiness criteria.
version: 1.0.0
author: Hermes Agent community
license: MIT
metadata:
  hermes:
    tags:
      [
        cto,
        technology-radar,
        architecture,
        engineering-metrics,
        technical-debt,
        build-vs-buy,
      ]
---

# Technology Radar

CTO methodology for making technology decisions, governing architecture, measuring engineering effectiveness, managing technical debt, and operating an innovation pipeline. These frameworks help a CTO balance short-term delivery velocity with long-term platform health.

## Domain Model

| Domain | Covers | Artifact |
|--------|--------|----------|
| **Technology Radar** | Adopt/Trial/Assess/Hold quadrants, tool selection criteria, deprecation policy | Technology radar document |
| **Build vs Buy** | TCO analysis, decision matrices, vendor evaluation, integration cost | Build-vs-buy recommendation |
| **Architecture Governance** | Standards, review boards, RFC process, design reviews | ADRs, RFC documents, governance charter |
| **Engineering Metrics** | DORA (deploy frequency, lead time, MTTR, change failure rate), SPACE, DevEx | Engineering dashboard, health report |
| **Technical Debt** | Interest calculation, remediation prioritization, principal estimation | Technical debt register |
| **Innovation Pipeline** | Horizon scanning, POC criteria, production readiness gates | Innovation funnel, POC report |

## When to Load

Load this skill when the task involves:

- Evaluating a new technology or tool for adoption
- Making a build-vs-buy decision with TCO analysis
- Designing or auditing architecture governance processes
- Setting up engineering metrics dashboards (DORA, SPACE)
- Quantifying and prioritizing technical debt remediation
- Running an innovation pipeline with POC-to-production gates
- Deprecating or retiring legacy technology
- Conducting an architecture review board session

## Loading Order

```
skill_view('technology-radar')                      # This — methodology index
skill_view('executive-methodology')                  # Shared decision frameworks
skill_view('artifact-pyramids')                      # Output contract
skill_view('technology-radar', file_path='references/technology-radar.md')
skill_view('technology-radar', file_path='references/build-vs-buy.md')
skill_view('technology-radar', file_path='references/architecture-governance.md')
skill_view('technology-radar', file_path='references/engineering-metrics.md')
```

## Reference Files

| Reference | Load When | File |
|-----------|-----------|------|
| Technology Radar | You need to evaluate and categorize a technology or tool for adoption, trial, assessment, or hold | `references/technology-radar.md` |
| Build vs Buy | You're comparing build vs buy options with TCO analysis and decision criteria | `references/build-vs-buy.md` |
| Architecture Governance | You're designing RFC processes, review boards, or architecture standards | `references/architecture-governance.md` |
| Engineering Metrics | You need to measure engineering effectiveness with DORA, SPACE, or DevEx frameworks | `references/engineering-metrics.md` |

## Design Principles

1. **Technology is a means, not an end.** Every technology decision must trace back to a business outcome. "Because it's new" is not a reason to adopt. "Because it solves X faster/safer/cheaper" is.
2. **Radar is a living document.** A technology radar updated once a year is a museum. Update it quarterly, or every time a significant adoption/hold/promote/promote-to-trial decision is made.
3. **Build vs buy is never just cost.** Total Cost of Ownership includes maintenance, hiring, training, integration, migration, and opportunity cost. A cheaper build today may be vastly more expensive over 3 years.
4. **Engineering metrics measure the system, not the people.** DORA metrics measure the delivery capability of the org. SPACE measures developer satisfaction. Neither is a performance review tool for individuals.
5. **Technical debt has a principal and an interest payment.** The principal is the cost to fix it properly. The interest is the recurring drag on velocity. Prioritize debt where interest/principal ratio is highest.
6. **Production readiness gates exist to prevent crisis.** Every gate that is skipped in the name of speed will be paid for in incident response time later.

## Related Skills

- `executive-methodology` — shared decision frameworks and governance
- `operational-design` — COO-side process design and scaling
- `artifact-pyramids` — output contract specification
- `platform-engineering` — infrastructure and CI/CD implementation patterns
