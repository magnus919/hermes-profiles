---
name: executive-methodology
description: >-
  Shared decision-making and governance methodology for all C-suite profiles.
  Covers decision frameworks (RAPID, DACI, decision matrices, pre-mortems,
  red-teaming), strategic thinking patterns (inversion, first principles,
  second-order effects), stakeholder communication (executive summaries, board
  decks, strategy memos), and governance frameworks (risk appetite, delegation
  levels, escalation paths).
version: 1.0.0
author: Hermes Agent community
license: MIT
metadata:
  hermes:
    tags:
      [
        executive,
        decision-making,
        governance,
        strategic-thinking,
        stakeholder-communication,
      ]
---

# Executive Methodology

Shared methodology layer consumed by CEO, CFO, CTO, and COO profiles. Provides the foundational frameworks for decision-making, strategic reasoning, stakeholder communication, and governance — used across all C-suite engagements.

## Domain Model

Executive work decomposes into four interconnected domains:

| Domain | Covers | Consumed By |
|--------|--------|-------------|
| **Decision Frameworks** | RAPID, DACI, decision matrices, pre-mortems, red-teaming | All profiles |
| **Strategic Thinking** | Inversion, first principles, second-order effects, probabilistic reasoning | CEO, CTO |
| **Stakeholder Communication** | Executive summaries, board decks, strategy memos, crisis communication | All profiles |
| **Governance** | Risk appetite, delegation levels, escalation paths, decision rights | All profiles |

## When to Load

Load this skill when the task involves:

- Choosing a decision-making framework for a specific problem
- Structuring an executive summary or board-level communication
- Applying strategic thinking patterns to a complex problem
- Designing or auditing governance structures
- Escalating a decision through the appropriate channel
- Running a pre-mortem or red-team on a strategic plan
- Preparing stakeholder communication at the C-suite level

## Loading Order

```
skill_view('executive-methodology')                 # This — methodology index
skill_view('artifact-pyramids')                      # Output contract
skill_view('executive-methodology', file_path='references/decision-frameworks.md')
skill_view('executive-methodology', file_path='references/strategic-thinking.md')
skill_view('executive-methodology', file_path='references/stakeholder-communication.md')
skill_view('executive-methodology', file_path='references/governance.md')
```

## Reference Files

| Reference | Load When | File |
|-----------|-----------|------|
| Decision Frameworks | You need to choose and apply a decision-making framework (RAPID, DACI, decision matrix, pre-mortem) | `references/decision-frameworks.md` |
| Strategic Thinking | You need to apply inversion, first principles, second-order effects, or probabilistic reasoning to a problem | `references/strategic-thinking.md` |
| Stakeholder Communication | You're preparing an executive summary, board deck, or strategy memo | `references/stakeholder-communication.md` |
| Governance | You're designing delegation rules, escalation paths, risk appetite, or decision rights | `references/governance.md` |

## Design Principles

1. **Output is the artifact.** Every engagement produces a structured deliverable at an absolute path. The artifact pyramid pattern from `artifact-pyramids` skill applies.
2. **Know which framework fits.** RAPID is for decisions with one accountable person. DACI is for group decisions with a driver. Decision matrices are for comparing options. Pre-mortems are for stress-testing plans. Choose deliberately.
3. **Surface assumptions before conclusions.** Every strategic analysis should expose its axioms. An inversion exercise is only as valuable as the assumptions it challenges.
4. **Level-appropriate communication.** Board decks are not strategy memos which are not daily standup updates. The format must match the audience's time, context, and decision authority.
5. **Governance is a force multiplier.** Clear decision rights prevent bottlenecks and empower execution. Every escalation path that is unclear will be tested in a crisis.

## Related Skills

- `artifact-pyramids` — output contract specification
- `strategy-frameworks` — CEO-specific strategic planning (OKRs, competitive analysis, growth)
- `technology-radar` — CTO-specific technology evaluation and architecture governance
- `financial-modeling` — CFO-specific unit economics, modeling, and SaaS metrics
- `operational-design` — COO-specific process design, scaling, and vendor management
