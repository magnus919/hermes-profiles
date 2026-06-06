# CLO — Chief Legal Officer / General Counsel — Hermes Profile

Legal strategy and risk management specialization for Hermes Agent. Owns regulatory risk assessment, IP protection, contract review, open-source license compatibility, and compliance frameworks.

## What This Profile Provides

- **Regulatory risk assessment** — exposure identification, probability quantification, mitigation planning
- **IP protection strategy** — patent/trademark/copyright analysis, defensibility assessment, enforcement planning
- **Contract review** — liability analysis, risk allocation, negotiation guidance, standard clause libraries
- **Open-source license compliance** — license compatibility analysis, dependency review, copyleft risk evaluation
- **Compliance framework design** — regulatory mapping, audit preparedness, policy architecture
- **Strategic legal guidance** — M&A due diligence, fundraising structure, market entry legal barriers

## Prerequisites

- Hermes Agent installed and configured
- The following skills must exist in `~/hermes-profiles/skills/`:
  - `artifact-pyramids`
  - `executive-methodology`
  - `legal-strategy`

## Installation

```bash
git clone https://github.com/magnus919/hermes-profiles.git ~/hermes-profiles
ln -s ~/hermes-profiles/profiles/clo ~/.hermes/profiles/
hermes --profile clo
```

## Trigger Patterns

| Trigger | What It Activates |
|---|---|
| "Review this contract for..." | Contract analysis: liability → risk allocation → negotiation recommendations |
| "What's the regulatory exposure for..." | Regulatory assessment: applicable frameworks → exposure analysis → compliance roadmap |
| "Assess our IP position on..." | IP analysis: portfolio → defensibility → gap assessment → filing recommendations |
| "Check license compatibility for..." | Open-source audit: dependency analysis → license compatibility → risk mitigation |
| "Design a compliance framework for..." | Compliance design: regulatory mapping → process architecture → audit protocol |

## Skill Dependencies

| Skill | Provides | Load Command |
|---|---|---|
| `artifact-pyramids` | Three-layer progressive disclosure output format | `skill_view('artifact-pyramids')` |
| `executive-methodology` | Strategic thinking, decision frameworks, governance, stakeholder communication | `skill_view('executive-methodology')` |
| `legal-strategy` | Contract risk, IP strategy, regulatory analysis, data privacy | `skill_view('legal-strategy')` |

## Output Format

All legal artifacts follow the artifact pyramid convention. The response to any caller is the absolute path to `00-index.md`.

## Verification

- [ ] Accepts a legal review prompt and produces an artifact pyramid
- [ ] Pyramid contains risk assessment, analysis, and supporting dossiers
- [ ] Response is the absolute path to `00-index.md`, not a summary
- [ ] Risk assessments include quantified probability and financial exposure
