# CTO — Hermes Profile

CTO specialization for Hermes Agent. Owns technology strategy and architecture governance, evaluates build-vs-buy at the company level, sets engineering standards, and maintains a technology radar.

## What This Profile Provides

- **Architecture governance** — architecture decision records, system design reviews, technology stack evaluation
- **Build-vs-buy analysis** — total cost of ownership modeling, build vs. buy vs. partner evaluation
- **Technology radar** — technology adoption governance with Adopt/Trial/Assess/Hold rings
- **Engineering standards** — coding conventions, CI/CD standards, observability requirements, security patterns
- **Technical strategy** — technology investment recommendations, platform strategy, infrastructure architecture
- **Architecture Decision Records (ADRs)** — structured documentation of architectural decisions with context, decision, and consequences

## Installation

```bash
git clone https://github.com/magnus919/hermes-profiles.git ~/hermes-profiles
ln -s ~/hermes-profiles/profiles/cto ~/.hermes/profiles/
hermes --profile cto
```

## Quick Start

Once the profile is loaded, give it a technology strategy prompt:

> "We're building a real-time collaboration platform targeting 10M users. Evaluate our technology stack options, make build-vs-buy recommendations for core capabilities, and produce an architecture decision record for the critical path."

The profile will:
1. Analyze technical requirements and constraints
2. Evaluate technology options against strategic criteria
3. Produce build-vs-buy recommendations with TCO analysis
4. Document architecture decisions as ADRs
5. Output an artifact pyramid at the engagement path

## Skill Dependencies

| Skill | Provides | Load Command |
|---|---|---|
| `artifact-pyramids` | Three-layer progressive disclosure output format | `skill_view('artifact-pyramids')` |
| `executive-methodology` | Strategic thinking, decision frameworks, stakeholder communication | `skill_view('executive-methodology')` |
| `technology-radar` | Technology adoption governance, build-vs-buy framework, engineering metrics, architecture governance | `skill_view('technology-radar')` |
| `architecture` (recommended) | System architecture patterns, design reviews, reference architectures | `skill_view('architecture')` |
| `mermaid-diagrams` (recommended) | Architecture diagrams, system maps, decision trees | `skill_view('mermaid-diagrams')` |

### Supporting References

| Reference | File |
|---|---|
| Technology radar | `skill_view('technology-radar', 'references/technology-radar.md')` |
| Build-vs-buy | `skill_view('technology-radar', 'references/build-vs-buy.md')` |
| Architecture governance | `skill_view('technology-radar', 'references/architecture-governance.md')` |
| Engineering metrics | `skill_view('technology-radar', 'references/engineering-metrics.md')` |
| Decision frameworks | `skill_view('executive-methodology', 'references/decision-frameworks.md')` |

## Output Format

All output follows the artifact pyramid convention. The response to any caller is the absolute path to `00-index.md`.

## Verification

- [ ] Accepts a technology strategy prompt and produces an artifact pyramid
- [ ] Pyramid contains architecture decisions documented as ADRs
- [ ] Build-vs-buy recommendations include TCO analysis and strategic rationale
- [ ] Technology radar entries are categorized with clear adoption guidance
- [ ] Response is the absolute path to `00-index.md`, not a summary
