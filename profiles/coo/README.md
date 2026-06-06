# COO — Hermes Profile

COO specialization for Hermes Agent. Owns operational design and execution infrastructure, designs workflows and handoffs between teams, defines KPIs and operational metrics, ensures compliance, and scales processes.

## What This Profile Provides

- **Process design** — workflow mapping, handoff protocols, process documentation, SOP creation
- **Operational metrics** — KPI definition, lead/lag measures, dashboard design, reporting cadence
- **Scalability analysis** — bottleneck identification, capacity planning, scale-readiness assessment
- **Compliance framework** — regulatory requirements embedding, audit trail design, policy enforcement
- **Vendor management** — vendor evaluation, SLA definition, business review cadence, relationship governance
- **Operational assessments** — current-state analysis, friction point identification, improvement prioritization

## Installation

```bash
git clone https://github.com/magnus919/hermes-profiles.git ~/hermes-profiles
ln -s ~/hermes-profiles/profiles/coo ~/.hermes/profiles/
hermes --profile coo
```

## Quick Start

Once the profile is loaded, give it an operational design prompt:

> "We're scaling from 50 to 200 employees over the next year. Design the operational infrastructure — workflows, metrics, handoffs, and compliance processes — to support this growth without breaking."

The profile will:
1. Assess current operational state and identify scaling constraints
2. Design scalable workflows with explicit handoff protocols
3. Define KPIs and measurement frameworks for each operational domain
4. Embed compliance requirements into process design
5. Output an artifact pyramid at the engagement path

## Skill Dependencies

| Skill | Provides | Load Command |
|---|---|---|
| `artifact-pyramids` | Three-layer progressive disclosure output format | `skill_view('artifact-pyramids')` |
| `executive-methodology` | Strategic thinking, decision frameworks, governance, stakeholder communication | `skill_view('executive-methodology')` |
| `operational-design` | Process design, operational metrics, scaling frameworks, compliance, vendor management | `skill_view('operational-design')` |

### Supporting References

| Reference | File |
|---|---|
| Process design | `skill_view('operational-design', 'references/process-design.md')` |
| Operational metrics | `skill_view('operational-design', 'references/operational-metrics.md')` |
| Scaling frameworks | `skill_view('operational-design', 'references/scaling-frameworks.md')` |
| Compliance | `skill_view('operational-design', 'references/compliance.md')` |
| Vendor management | `skill_view('operational-design', 'references/vendor-management.md')` |
| Decision frameworks | `skill_view('executive-methodology', 'references/decision-frameworks.md')` |

## Output Format

All output follows the artifact pyramid convention. The response to any caller is the absolute path to `00-index.md`.

## Verification

- [ ] Accepts an operational design prompt and produces an artifact pyramid
- [ ] Pyramid contains process designs with measurement hooks and handoff protocols
- [ ] KPIs defined for each operational domain with lead and lag measures
- [ ] Compliance requirements are embedded in process documentation
- [ ] Response is the absolute path to `00-index.md`, not a summary
