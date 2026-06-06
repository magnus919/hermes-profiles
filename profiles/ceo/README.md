# CEO — Hermes Profile

CEO specialization for Hermes Agent. Translates vision into strategy, decomposes high-level objectives into domain-specific mandates, and makes final calls on strategic trade-offs.

## What This Profile Provides

- **Vision decomposition** — translates high-level direction into binding mandates for CTO, CFO, COO
- **Strategic analysis** — competitive positioning, market assessment, strategic option evaluation
- **Capital allocation** — investment prioritization, resource allocation, opportunity cost analysis
- **Talent strategy** — organizational design, hiring philosophy, talent density assessment
- **Board communication** — strategic narrative framing, board reporting, investor updates
- **Decision documentation** — strategic decision records with rationale, assumptions, and expected outcomes

## Installation

```bash
git clone https://github.com/magnus919/hermes-profiles.git ~/hermes-profiles
ln -s ~/hermes-profiles/profiles/ceo ~/.hermes/profiles/
hermes --profile ceo
```

## Quick Start

Once the profile is loaded, give it a strategic prompt:

> "We're a B2B SaaS company at $5M ARR growing 15% QoQ. Our main competitor just raised a $50M Series B and is expanding into our segment. Evaluate our strategic response options and decompose mandates for the leadership team."

The profile will:
1. Analyze the competitive threat and market dynamics
2. Develop strategic response options with trade-off analysis
3. Decompose mandates into domain-specific directives for CTO, CFO, COO
4. Produce an artifact pyramid at the output path

## Skill Dependencies

| Skill | Provides | Load Command |
|---|---|---|
| `artifact-pyramids` | Three-layer progressive disclosure output format | `skill_view('artifact-pyramids')` |
| `executive-methodology` | Strategic thinking frameworks, governance, decision frameworks, stakeholder communication | `skill_view('executive-methodology')` |
| `strategy-frameworks` | Strategic planning, competitive analysis, resource allocation, growth strategy | `skill_view('strategy-frameworks')` |
| `mermaid-diagrams` (recommended) | Strategic mapping, org charts, decision trees | `skill_view('mermaid-diagrams')` |

### Supporting References

| Reference | File |
|---|---|
| Strategic thinking | `skill_view('executive-methodology', 'references/strategic-thinking.md')` |
| Decision frameworks | `skill_view('executive-methodology', 'references/decision-frameworks.md')` |
| Governance | `skill_view('executive-methodology', 'references/governance.md')` |
| Stakeholder communication | `skill_view('executive-methodology', 'references/stakeholder-communication.md')` |
| Strategic planning | `skill_view('strategy-frameworks', 'references/strategic-planning.md')` |
| Competitive analysis | `skill_view('strategy-frameworks', 'references/competitive-analysis.md')` |
| Resource allocation | `skill_view('strategy-frameworks', 'references/resource-allocation.md')` |
| Growth strategy | `skill_view('strategy-frameworks', 'references/growth-strategy.md')` |

## Output Format

All output follows the artifact pyramid convention. The response to any caller is the absolute path to `00-index.md`.

## Verification

- [ ] Accepts a strategic prompt and produces an artifact pyramid
- [ ] Pyramid contains strategic recommendation, mandate decomposition, and supporting analysis
- [ ] Response is the absolute path to `00-index.md`, not a summary
- [ ] Mandates are decomposable into domain-specific directives for CTO, CFO, COO
