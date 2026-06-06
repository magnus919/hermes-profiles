# CMO — Chief Marketing Officer — Hermes Profile

Go-to-market leadership specialization for Hermes Agent. Owns brand strategy, customer acquisition, positioning and messaging, growth channel management, and market entry planning.

## What This Profile Provides

- **Go-to-market strategy** — positioning, segmentation, channel strategy, timing, competitive posture
- **Brand architecture** — brand hierarchy, visual identity governance, tonal coherence, brand equity measurement
- **Acquisition strategy** — channel portfolio management, CAC optimization, growth modeling
- **Positioning and messaging** — differentiation strategy, value proposition development, messaging hierarchy
- **Market entry planning** — timing analysis, launch sequencing, resource allocation
- **Marketing measurement** — attribution modeling, LTV:CAC frameworks, leading/lagging indicator dashboards

## Prerequisites

- Hermes Agent installed and configured
- The following skills must exist in `~/hermes-profiles/skills/`:
  - `artifact-pyramids`
  - `executive-methodology`
  - `go-to-market`

## Installation

```bash
git clone https://github.com/magnus919/hermes-profiles.git ~/hermes-profiles
ln -s ~/hermes-profiles/profiles/cmo ~/.hermes/profiles/
hermes --profile cmo
```

## Trigger Patterns

| Trigger | What It Activates |
|---|---|
| "Define the GTM strategy for..." | Full GTM engagement: positioning → segmentation → channels → budget → measurement |
| "How should we position X against Y?" | Positioning engagement: differentiation analysis → value proposition → messaging |
| "What's our brand architecture?" | Brand audit: hierarchy → coherence assessment → governance recommendations |
| "Model our acquisition channels..." | Channel analysis: portfolio assessment → efficiency modeling → rebalancing |
| "Plan the market entry for..." | Entry strategy: timing → sequencing → resource allocation → risk assessment |

## Skill Dependencies

| Skill | Provides | Load Command |
|---|---|---|
| `artifact-pyramids` | Three-layer progressive disclosure output format | `skill_view('artifact-pyramids')` |
| `executive-methodology` | Strategic thinking, decision frameworks, governance, stakeholder communication | `skill_view('executive-methodology')` |
| `go-to-market` | Positioning, acquisition strategy, growth modeling, customer acquisition frameworks | `skill_view('go-to-market')` |

## Output Format

All go-to-market artifacts follow the artifact pyramid convention. The response to any caller is the absolute path to `00-index.md`.

## Verification

- [ ] Accepts a GTM prompt and produces an artifact pyramid
- [ ] Pyramid contains strategic frame, execution plan, and measurement framework
- [ ] Response is the absolute path to `00-index.md`, not a summary
- [ ] Channel recommendations include expected ROI, payback period, and downside scenarios
