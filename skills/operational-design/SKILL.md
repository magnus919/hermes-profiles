---
name: operational-design
description: >-
  COO methodology for process design, organizational scaling, operational
  metrics, compliance and audit, vendor management, and team topology. Covers
  value stream mapping, BPMN, bottleneck analysis, scaling from 10 to 100 to
  1000 people, KPI design, balanced scorecard, SOC 2, ISO 27001, GDPR
  readiness, RFP processes, SLA design, vendor scorecards, team topologies,
  Conway's Law, and Dunbar's Number.
version: 1.0.0
author: Hermes Agent community
license: MIT
metadata:
  hermes:
    tags:
      [
        coo,
        operations,
        process-design,
        scaling,
        compliance,
        vendor-management,
        team-topologies,
      ]
---

# Operational Design

COO methodology for designing and scaling operations, managing compliance, selecting and managing vendors, and measuring operational health. These frameworks help a COO build the systems and processes that enable the organization to execute reliably at scale.

## Domain Model

| Domain | Covers | Artifact |
|--------|--------|----------|
| **Process Design** | Value stream mapping, BPMN, bottleneck analysis, workflow optimization | Process maps, VSM current/future state |
| **Scaling Frameworks** | 10-to-100-to-1000 transitions, organizational design, delegation patterns | Scaling plan, org design |
| **Operational Metrics** | KPI design, balanced scorecard, leading vs lagging indicators | Operations dashboard |
| **Compliance & Audit** | SOC 2, ISO 27001, GDPR readiness, audit preparation | Compliance roadmap, control matrix |
| **Vendor Management** | RFP process, SLA design, vendor scorecards, relationship tiers | Vendor management framework |
| **Organizational Patterns** | Team topologies, Conway's Law, Dunbar's number, span of control | Team design, communication model |

## When to Load

Load this skill when the task involves:

- Mapping and optimizing a business process (value stream, BPMN)
- Planning organizational scaling through growth phases
- Designing operational KPIs and a balanced scorecard
- Preparing for SOC 2, ISO 27001, or GDPR compliance
- Running an RFP or vendor selection process
- Designing SLAs and vendor scorecards
- Restructuring teams using team topologies
- Analyzing bottlenecks and throughput constraints
- Designing delegation and span-of-control models

## Loading Order

```
skill_view('operational-design')                    # This — methodology index
skill_view('executive-methodology')                  # Shared decision frameworks
skill_view('artifact-pyramids')                      # Output contract
skill_view('operational-design', file_path='references/process-design.md')
skill_view('operational-design', file_path='references/scaling-frameworks.md')
skill_view('operational-design', file_path='references/operational-metrics.md')
skill_view('operational-design', file_path='references/compliance.md')
skill_view('operational-design', file_path='references/vendor-management.md')
```

## Reference Files

| Reference | Load When | File |
|-----------|-----------|------|
| Process Design | You need to map, analyze, or optimize a business process | `references/process-design.md` |
| Scaling Frameworks | You're planning organizational growth or restructuring | `references/scaling-frameworks.md` |
| Operational Metrics | You're designing KPIs, dashboards, or a balanced scorecard | `references/operational-metrics.md` |
| Compliance & Audit | You're preparing for SOC 2, ISO 27001, or GDPR compliance | `references/compliance.md` |
| Vendor Management | You're running an RFP, designing SLAs, or evaluating vendors | `references/vendor-management.md` |

## Design Principles

1. **Process before automation.** Automating a bad process makes bad output faster. Map and optimize the workflow before selecting tools.
2. **Scale is a discontinuous function.** An organization that works at 10 people will break at 50, 200, and 1,000 — each requires a different operating model. Design for the next phase, not the current one.
3. **Lead with leading indicators.** Lagging indicators tell you what already happened. Leading indicators tell you what will happen. A good operations dashboard has a balanced mix of both.
4. **Compliance is a system, not a project.** SOC 2 certification is not a one-time effort. Compliance requires embedded controls, continuous monitoring, and periodic testing.
5. **Vendors are partners, not passengers.** The cheapest vendor is usually the most expensive in total cost. Invest in vendor relationships proportional to business criticality.
6. **Structure follows strategy.** Team topology should be driven by the communication patterns the work requires (Conway's Law), not by reporting lines that are convenient for management.

## Related Skills

- `executive-methodology` — shared decision frameworks and governance
- `strategy-frameworks` — CEO-side strategic direction and competitive analysis
- `technology-radar` — CTO-side technology evaluation and architecture governance
- `financial-modeling` — CFO-side unit economics and SaaS metrics
- `artifact-pyramids` — output contract specification
