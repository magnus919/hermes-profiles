# Site Reliability Engineer — Hermes Profile

SRE specialization for Hermes Agent. Designs, operates, and improves production system reliability through SLO-driven operations, incident command, observability engineering, automation, and operational excellence — all delivered as artifact pyramids.

## What This Profile Provides

- **SLO/SLI Framework** — define, measure, and govern reliability targets aligned to user journeys
- **Error Budget Governance** — data-driven release gating, burn rate alerting, budget policy
- **Incident Command** — structured incident management with roles, checklists, and communication templates
- **Blameless Postmortems** — systematic root cause analysis with 5 Whys, action tracking, follow-up
- **Observability Design** — The Four Golden Signals, symptom-based alerting, dashboard architecture
- **Operational Excellence** — toil elimination, automation prioritization, runbook design
- **Reliability Reviews** — pre-launch reviews, architecture assessments, risk analysis

## Prerequisites

- [Hermes Agent](https://hermes-agent.nousresearch.com/) installed and configured

## Installation

```bash
# Clone the profiles repo
git clone https://github.com/magnus919/hermes-profiles.git ~/hermes-profiles

# Symlink the profile into ~/.hermes/profiles/
ln -s ~/hermes-profiles/profiles/site-reliability-engineer ~/.hermes/profiles/

# Switch to profile (skills are bundled — no separate install needed)
hermes --profile site-reliability-engineer
```

## Quick Start

Once the profile is loaded, give it a reliability prompt:

> "Design a reliability framework for our payment processing API. Define SLOs, error budget policy, and alerting rules."

The profile will:

1. Identify user journeys and tier the service
2. Define SLIs and set SLO targets with error budgets
3. Design burn rate alerting and release gating rules
4. Produce an artifact pyramid at `/tmp/sre-workflow/<project>/00-index.md`

## Skill Dependencies

| Skill | Provides | Load Command |
|---|---|---|
| `artifact-pyramids` | Three-layer progressive disclosure specification | `skill_view('artifact-pyramids')` |
| `site-reliability-engineering` | Full SRE methodology, references, templates, scripts | `skill_view('site-reliability-engineering')` |

### Supporting References

The skill bundles extensive reference material accessible via `skill_view()`:

- **SRE Book Chapters** — complete summaries of the Google SRE book (`site-reliability-engineering` skill, `references/sre-book-chapters.md`)
- **SLO/SLI Framework** — SLI patterns, SLO setting methodology, burn rate formulas (`references/slo-sli-framework.md`)
- **Error Budget Governance** — budget mechanics, consumption thresholds, release gating (`references/error-budget-governance.md`)
- **Incident Command System** — roles, hierarchy, handoff protocols, severity classification (`references/incident-command-system.md`)
- **Blameless Postmortems** — culture, structure, 5 Whys, language transformation (`references/postmortem-culture.md`)
- **Monitoring & Alerting** — Four Golden Signals, alert design, PromQL examples (`references/monitoring-alerting.md`)
- **On-Call Best Practices** — rotation design, workload caps, cognitive load management (`references/oncall-best-practices.md`)
- **Toil Elimination** — toil assessment rubric, automation decision tree, prioritization (`references/toil-elimination.md`)
- **Release Engineering** — hermetic builds, progressive delivery, deployment patterns (`references/release-engineering.md`)
- **Effective Troubleshooting** — hypothetico-deductive method, diagnostic techniques (`references/troubleshooting.md`)
- **Senior SRE Blueprint** — role definition, KPI framework, career progression (`references/senior-sre-blueprint.md`)
- **SRE Communication Guide** — incident communication, influencing without authority, stakeholder updates (`references/sre-communication-guide.md`)
- **Guiding Principles** — first principles, philosophy, cross-reference to SRE book chapters (`references/guiding-principles.md`)

### Templates

| Template | Purpose |
|---|---|
| `templates/incident-command-checklist.md` | Step-by-step IC response during active incidents |
| `templates/postmortem-template.md` | Blameless postmortem document with 5 Whys |
| `templates/runbook-template.md` | Operational runbook with 10 failure mode patterns |
| `templates/slo-declaration-template.md` | Formal SLO specification document |
| `templates/error-budget-policy.md` | Team-level error budget governance policy |
| `templates/oncall-rotation.md` | Rotation schedule and escalation protocol |
| `templates/service-review-checklist.md` | Pre-launch reliability review (~80 checks) |
| `templates/incident-communication.md` | 6 communication templates per incident phase |

### Scripts

| Script | Purpose |
|---|---|
| `scripts/slo-burn-rate.py` | Calculate error budget burn rate from SLI data |

## Output Format

All output follows the artifact pyramid convention:

```
<output>/
├── 00-index.md              ← Navigation + SOURCES
├── 01-summary/              ← Reliability posture, SLO attainment, key findings
├── 02-analysis/             ← Per-journey analysis, trade-off evaluation
└── 03-dossiers/             ← Raw SLI data, runbooks, configurations
```

The response to any caller is the absolute path to `00-index.md`. Not a summary. Not a conversation. A path.

## Verification

A deployed site-reliability-engineer agent should pass these checks:

- [ ] Accepts a reliability design prompt and produces an artifact pyramid
- [ ] Can define SLOs and error budgets for a service given constraints
- [ ] Can run an incident postmortem from a timeline
- [ ] Can produce a service review checklist assessment
- [ ] Response is the absolute path to `00-index.md`, not a summary
- [ ] Can calculate burn rate from SLI data using bundled script
