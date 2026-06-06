# CPO — Chief Product Officer — Hermes Profile

Strategic product leadership specialization for Hermes Agent. Owns product strategy, market fit, competitive positioning, and the translation of business goals into product direction. Complements the product-manager profile at the strategic level.

## What This Profile Provides

- **Product strategy** — market thesis, competitive stance, prioritization principles, product vision
- **Market-fit analysis** — cohort-based fit measurement, segment targeting, willingness-to-pare assessment
- **Competitive positioning** — landscape evaluation, differentiation strategy, moat analysis
- **Strategic roadmapping** — hypothesis-driven planning, bet portfolio management, 90-day outcome tracking
- **Executive communication** — board-ready strategy narratives, trade-off presentations, investment framing
- **Product decision frameworks** — falsifiable hypothesis design, go/kill criteria, opportunity sizing

## Prerequisites

- Hermes Agent installed and configured
- The following skills must exist in `~/hermes-profiles/skills/`:
  - `artifact-pyramids`
  - `executive-methodology`
  - `product-strategy`

## Installation

```bash
git clone https://github.com/magnus919/hermes-profiles.git ~/hermes-profiles
ln -s ~/hermes-profiles/profiles/cpo ~/.hermes/profiles/
hermes --profile cpo
```

## Trigger Patterns

Load this profile for strategic product questions. See AGENTS.md for a full trigger table.

| Trigger | What It Activates |
|---|---|
| "Define product strategy for..." | Strategic frame: market thesis → competitive stance → bet portfolio → success criteria |
| "Evaluate product-market fit for..." | Fit analysis: cohort metrics → segment evaluation → gap assessment |
| "Where should we place our product bets?" | Bet portfolio: opportunity sizing → risk assessment → resource allocation |
| "How do we differentiate against X?" | Competitive positioning: landscape → positioning → moat analysis |
| "What should our product principles be?" | Product philosophy: strategic axioms → decision guardrails → culture |

## Skill Dependencies

| Skill | Provides | Load Command |
|---|---|---|
| `artifact-pyramids` | Three-layer progressive disclosure output format | `skill_view('artifact-pyramids')` |
| `executive-methodology` | Strategic thinking, decision frameworks, governance, stakeholder communication | `skill_view('executive-methodology')` |
| `product-strategy` | Market analysis, competitive positioning, product strategy frameworks | `skill_view('product-strategy')` |

### Recommended Additions

| Skill | Load Command |
|---|---|
| `product-methodology` (RICE, MoSCoW, specs) | `skill_view('product-methodology')` |
| `mermaid-diagrams` (strategy visuals) | `skill_view('mermaid-diagrams')` |

## Output Format

All strategic artifacts follow the artifact pyramid convention. The response to any caller is the absolute path to `00-index.md`.

## Verification

- [ ] Accepts a product strategy prompt and produces an artifact pyramid
- [ ] Pyramid contains strategic recommendation, analysis dimensions, supporting evidence
- [ ] Response is the absolute path to `00-index.md`, not a summary
- [ ] Skills load correctly and references are independently accessible
