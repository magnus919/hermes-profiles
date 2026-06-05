# Site-Reliability-Engineer Profile — Agent Guidance

This document is for AI agents that interact with or consume outputs from the site-reliability-engineer Hermes profile.

## Trigger Patterns

Load this profile when the user asks for any of the following:

| User Says | What It Means |
|---|---|
| "Design a reliability framework for..." | Full engagement: SLOs → error budget → alerting → pyramid |
| "Run a postmortem for this incident" | Incident postmortem with timeline, 5 Whys, action items |
| "Review this service for reliability" | Pre-launch checklist, architecture review, risk assessment |
| "Define SLOs for this service" | SLI specification, SLO target setting, error budget |
| "Improve our on-call / incident response" | Rotation design, IC framework, runbook gaps |
| "Build observability for..." | Four Golden Signals, dashboard design, alert rules |
| "Help me troubleshoot this issue" | Hypothetico-deductive methodology, diagnostic approach |
| "Automate this operational task" | Toil assessment, automation decision tree, ROI analysis |

## Loading Order

When starting an engagement, load the core skill:

```python
skill_view('site-reliability-engineering')     # Methodology index and references
skill_view('artifact-pyramids')                # Output contract specification
```

Then load reference files on demand based on the specific engagement:

| Engagement Type | References to Load |
|---|---|
| SLO/SLI Design | `references/slo-sli-framework.md`, `references/error-budget-governance.md`, `references/guiding-principles.md` |
| Incident Response | `references/incident-command-system.md`, `templates/incident-command-checklist.md`, `templates/incident-communication.md` |
| Postmortem | `references/postmortem-culture.md`, `templates/postmortem-template.md`, `references/troubleshooting.md` |
| Reliability Review | `templates/service-review-checklist.md`, `references/senior-sre-blueprint.md` |
| On-Call Redesign | `references/oncall-best-practices.md`, `templates/oncall-rotation.md` |
| Toil Reduction | `references/toil-elimination.md`, `references/sre-communication-guide.md` |
| Observability | `references/monitoring-alerting.md`, `references/slo-sli-framework.md` |
| Release Engineering | `references/release-engineering.md` |

## Output Contract

The profile produces reliability documentation as an artifact pyramid. The response to the caller is always the **absolute path to `00-index.md`** at the pyramid root.

### Expected Structure

```
<output>/
├── 00-index.md              ← Navigation index with SOURCES
├── 01-summary/
│   ├── reliability-posture.md  ← SLO attainment, error budget status
│   ├── incident-summary.md     ← For postmortem engagements
│   └── recommendations.md      ← Key findings and next actions
├── 02-analysis/
│   ├── per-journey-slos.md     ← User-journey-level SLO analysis
│   ├── burn-rate-analysis.md   ← Error budget consumption
│   ├── failure-modes.md        ← Risk and contributing factors
│   └── trade-offs.md           ← Reliability vs velocity/cost
└── 03-dossiers/
    ├── sli-data.md             ← Raw SLI data and calculations
    ├── runbooks.md             ← Generated runbook drafts
    ├── incident-timeline.md    ← Full incident timeline
    └── action-items.md         ← Tracked action items with owners
```

### Cross-Reference Rules

1. **SLO declarations must reference user journeys** — every SLO ties to a specific user experience
2. **Incident analyses must reference SLOs** — every incident describes which SLOs were affected and by how much
3. **Action items must reference root causes** — every action links back to the contributing factor it addresses
4. **SOURCES sections at every layer** — absolute path references with descriptions
5. **Error budget status references SLO attainment** — budget consumption is meaningless without the SLO it measures against

## Handoff Protocol

1. **The pyramid IS the handoff.** Close with the path. Do not summarize.
2. If the engagement is multi-phase, each phase produces its own pyramid. The L3 dossiers of phase N serve as context for phase N+1.
3. Partial pyramids are acceptable. If only SLO design is requested, produce only the SLO layers.

## Supporting References

| Reference | File |
|---|---|
| Google SRE Book Chapter Summaries | `references/sre-book-chapters.md` |
| SLO/SLI Framework | `references/slo-sli-framework.md` |
| Error Budget Governance | `references/error-budget-governance.md` |
| Incident Command System | `references/incident-command-system.md` |
| Blameless Postmortems | `references/postmortem-culture.md` |
| Monitoring & Alerting | `references/monitoring-alerting.md` |
| On-Call Best Practices | `references/oncall-best-practices.md` |
| Toil Elimination | `references/toil-elimination.md` |
| Release Engineering | `references/release-engineering.md` |
| Effective Troubleshooting | `references/troubleshooting.md` |
| Senior SRE Blueprint | `references/senior-sre-blueprint.md` |
| SRE Communication Guide | `references/sre-communication-guide.md` |
| Guiding Principles | `references/guiding-principles.md` |

Load these with `skill_view('site-reliability-engineering', file_path=<path>)` when depth is needed.

## Related Profiles

The site-reliability-engineer profile is designed to work alongside:

- **technical-architect** — receives reliability constraints. Handoff: pyramid path. The SRE's SLO targets and failure mode analysis feed the architecture.
- **product-manager** — translates business priorities into reliability trade-offs. Receives SLO impact analysis. Provides product constraints for error budget policy.
- **implementation-planner** — consumes runbook requirements, automation plans, and operational readiness items for build plans.
- **orchestrator** — routes incident response tasks and reliability initiative tasks during multi-agent workflows.
