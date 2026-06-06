# CHRO — Chief Human Resources Officer — Hermes Profile

Organizational design and talent strategy specialization for Hermes Agent. Owns organizational capability, talent acquisition and development, compensation architecture, culture building, and organizational health.

## What This Profile Provides

- **Organizational design** — structure assessment, team topology, decision-rights mapping, span-of-control analysis
- **Talent strategy** — workforce planning, skill gap analysis, succession planning, leadership pipeline design
- **Compensation architecture** — philosophy design, benchmarking, incentive structure modeling, equity planning
- **Hiring pipeline management** — role definition, sourcing strategy, interview process design, offer framework
- **Organizational health assessment** — engagement surveys, culture audits, retention analysis, burnout risk evaluation
- **Performance management** — framework design, calibration process, feedback systems, growth planning

## Prerequisites

- Hermes Agent installed and configured
- The following skills must exist in `~/hermes-profiles/skills/`:
  - `artifact-pyramids`
  - `executive-methodology`
  - `org-design`

## Installation

```bash
git clone https://github.com/magnus919/hermes-profiles.git ~/hermes-profiles
ln -s ~/hermes-profiles/profiles/chro ~/.hermes/profiles/
hermes --profile chro
```

## Trigger Patterns

| Trigger | What It Activates |
|---|---|
| "Design the org structure for..." | Org design: team topology → decision rights → coordination mechanisms → implementation |
| "Build a talent strategy for..." | Talent strategy: workforce planning → skill gaps → hiring plan → development roadmap |
| "Design a compensation framework..." | Compensation: philosophy → benchmarking → incentive design → implementation plan |
| "Assess organizational health..." | Health assessment: engagement → culture → retention → burnout → recommendations |
| "Plan the hiring pipeline for..." | Hiring plan: role definition → sourcing → process → capacity → timeline |

## Skill Dependencies

| Skill | Provides | Load Command |
|---|---|---|
| `artifact-pyramids` | Three-layer progressive disclosure output format | `skill_view('artifact-pyramids')` |
| `executive-methodology` | Strategic thinking, decision frameworks, governance, stakeholder communication | `skill_view('executive-methodology')` |
| `org-design` | Organizational design, talent strategy, compensation frameworks, culture architecture | `skill_view('org-design')` |

## Output Format

All organizational artifacts follow the artifact pyramid convention. The response to any caller is the absolute path to `00-index.md`.

## Verification

- [ ] Accepts an org design prompt and produces an artifact pyramid
- [ ] Pyramid contains assessment, analysis, and recommendation layers
- [ ] Response is the absolute path to `00-index.md`, not a summary
- [ ] Recommendations include capability assessment, gap analysis, and implementation roadmap
