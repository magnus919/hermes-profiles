---
title: "Site Reliability Engineering — Methodology"
type: skill
subjects:
  - SRE
  - Reliability Engineering
  - Incident Management
  - Observability
  - Platform Engineering
---

# Site Reliability Engineering

A comprehensive methodology for designing, operating, and improving reliable production systems. Rooted in Google SRE principles and extended with modern practices for incident command, observability engineering, error budget governance, and operational excellence.

## When to Load This Skill

| Trigger | What It Means |
|---|---|
| "Design reliability into this system" | SLO/SLI framework, error budget policy, resilience architecture |
| "Run an incident postmortem" | Blameless postmortem with timeline, 5 Whys, action tracking |
| "Improve our on-call" | Rotation design, alert tuning, toil reduction, escalation policy |
| "Build observability" | The Four Golden Signals, dashboard design, alert rule patterns |
| "Do a reliability review" | Architecture review against SRE principles, risk assessment |
| "I need an incident commander" | Incident command framework, role cards, communication templates |
| "Automate this operational task" | Toil assessment, automation decision tree, runbook pattern |

## Loading Order

1. `skill_view('site-reliability-engineering')` — this file, methodology index
2. Load references on demand by topic (see below)

## Reference Files

| Topic | File | When to Load |
|---|---|---|
| SRE Book Chapter Summaries | `references/sre-book-chapters.md` | Design engagement, first principles review |
| SLO/SLI Framework | `references/slo-sli-framework.md` | Defining reliability targets |
| Error Budget Governance | `references/error-budget-governance.md` | Policy design, burn rate alerts |
| Incident Command System | `references/incident-command-system.md` | During/after incident, training |
| Blameless Postmortems | `references/postmortem-culture.md` | After incident, process design |
| Monitoring & Alerting | `references/monitoring-alerting.md` | Observability design, alert rules |
| On-Call Best Practices | `references/oncall-best-practices.md` | Rotation design, team sizing |
| Toil Elimination | `references/toil-elimination.md` | Automation prioritization, ops review |
| Release Engineering | `references/release-engineering.md` | Deployment pipeline design |
| Effective Troubleshooting | `references/troubleshooting.md` | Debugging methodology |
| Senior SRE Role Blueprint | `references/senior-sre-blueprint.md` | Role definition, KPI framework |
| SRE Communication Guide | `references/sre-communication-guide.md` | Stakeholder updates, incident communication |
| Guiding Principles | `references/guiding-principles.md` | First principles, philosophy |
| Product-Focused Reliability | `references/product-focused-reliability.md` | Product-centric SRE, CUJ-based SLOs, JTBD model |
| Twenty Years of Lessons | `references/twenty-years-lessons.md` | Incident-derived tactical lessons, Prodverbs |
| SRE Ecosystem Guide | `references/sre-ecosystem-guide.md` | Curated guide to all SRE resources (Workbook, Secure Systems, Classroom, Prodcast, STPA, Video Gallery, Mobaa, fundamentals, AI ops) |

## Templates

| Template | File | Purpose |
|---|---|---|
| Incident Commander Checklist | `templates/incident-command-checklist.md` | Step-by-step IC response |
| Postmortem Template | `templates/postmortem-template.md` | Blameless postmortem document |
| Runbook Template | `templates/runbook-template.md` | Operational runbook standard |
| SLO Declaration Template | `templates/slo-declaration-template.md` | Service-level objective specification |
| Error Budget Policy | `templates/error-budget-policy.md` | Team-level error budget governance |
| On-Call Rotation Template | `templates/oncall-rotation.md` | Rotation schedule and escalation |
| Service Review Checklist | `templates/service-review-checklist.md` | Pre-launch reliability review |
| Incident Communication Template | `templates/incident-communication.md` | Status updates during incidents |

## Scripts

| Script | Purpose |
|---|---|
| `scripts/slo-burn-rate.py` | Calculate error budget burn rate from SLI data |
| `scripts/postmortem-summary.py` | Generate a postmortem summary from structured data |

## Output Contract

All output follows the artifact pyramid convention (three-layer progressive disclosure). The response to any caller is the absolute path to `00-index.md`. Not a summary. Not a conversation. A path.

## Related Profiles

This skill is primarily used by the **site-reliability-engineer** profile. It works alongside:

- **technical-architect** — receives reliability constraints, provides architecture context
- **data-architect** — coordinates on observability pipeline and data durability
- **orchestrator** — routes incident response tasks and reliability initiatives
- **implementation-planner** — consumes reliability requirements for build plans
