# Product Manager — Hermes Profile

Product management specialization for Hermes Agent. Writes specs, manages roadmaps, aligns teams, and translates customer needs into prioritized deliverables.

## What This Profile Provides

- **Spec writing** — structured requirements documents engineers, designers, and stakeholders can all work from
- **Prioritization** — RICE scoring, MoSCoW, Opportunity Solution Trees for trade-off decisions
- **Stakeholder communication** — audience-appropriate messaging for engineers, designers, executives, and customers
- **Customer discovery** — interview guides, problem validation, outcome-based requirements
- **Decision logging** — lightweight format for tracking trade-offs, rationale, and expected outcomes

## Installation

```bash
git clone https://github.com/magnus919/hermes-profiles.git ~/hermes-profiles
ln -s ~/hermes-profiles/profiles/product-manager ~/.hermes/profiles/
hermes --profile product-manager
```

## Quick Start

Once the profile is loaded, give it a product prompt:

> "Write a spec for a notification preferences UI. Users want to control which notifications they receive and how they receive them (email, push, in-app)."

The profile will:
1. Define the problem and user segments
2. Produce user stories and acceptance criteria
3. Prioritize scope using the appropriate framework
4. Document open questions and trade-offs
5. Output an artifact pyramid at `/tmp/pm-workflow/<project>/00-index.md`

## Skill Dependencies

| Skill | Provides | Load Command |
|---|---|---|
| `artifact-pyramids` | Three-layer progressive disclosure output format | `skill_view('artifact-pyramids')` |
| `product-methodology` | RICE, MoSCoW, Opportunity Solution Trees, spec template, customer interviews, stakeholder communication, decision log | `skill_view('product-methodology')` |

### Supporting References

| Reference | File |
|---|---|
| RICE prioritization | `skill_view('product-methodology', 'references/rice-framework.md')` |
| MoSCoW prioritization | `skill_view('product-methodology', 'references/moscow-prioritization.md')` |
| Opportunity Solution Trees | `skill_view('product-methodology', 'references/opportunity-solution-trees.md')` |
| Customer interview guide | `skill_view('product-methodology', 'references/customer-interview-guide.md')` |
| Spec template | `skill_view('product-methodology', 'references/spec-template.md')` |
| Stakeholder communication | `skill_view('product-methodology', 'references/stakeholder-communication.md')` |
| Decision log | `skill_view('product-methodology', 'references/decision-log.md')` |
| Artifact pyramid mapping | `skill_view('product-methodology', 'references/artifact-pyramid-mapping.md')` |

## Output Format

All output follows the artifact pyramid convention. The response to any caller is the absolute path to `00-index.md`.

## Verification

- [ ] Accepts a product prompt and produces an artifact pyramid
- [ ] Pyramid contains problem definition, user stories, prioritization, and success criteria
- [ ] Response is the absolute path to `00-index.md`, not a summary
- [ ] Each methodology reference is independently loadable via skill_view()
