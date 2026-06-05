---
name: sdd-authoring
description: "Specification authoring for AI-native SDD — writes formal specifications in structured formats (Gherkin, user stories, acceptance criteria), enforces spec quality gates, and produces artifact-pyramid-compliant SPEC.md outputs. Trigger when specifications or requirements documents need to be authored from scratch or refined."
version: 1.0.0
author: Hermes Agent community
license: MIT
metadata:
  hermes:
    tags: [sdd, specifications, gherkin, requirements, bdd, acceptance-criteria]
    related_skills: [sdd-work-decomposition, sdd-verification, sdd-review]
---

# SDD Specification Authoring

Writing formal, machine-readable specifications that drive AI-assisted implementation. This skill owns the **Specify** phase of the SDD pipeline and its output is the prerequisite for all downstream SDD work.

## SDD Pipeline Position

```
INCEPTION → [SPECIFY] → PLAN → TASKS → IMPLEMENT → VERIFY
                ↑
          You are here
```

The specification is the single source of truth. Every downstream artifact — task plan, architecture, implementation, tests — derives from and traces back to this document. Ambiguity in the spec propagates as defects in every subsequent phase.

## Artifact-Pyramid Output: SPEC.md

The specification documents produced by this skill follow the artifact-pyramid structure:

| Layer | Content | File |
|-------|---------|------|
| L1 | Executive Summary — one-paragraph scope statement, key stakeholders, overall success criteria | `00-index.md` (entry point) |
| L2 | Per-dimension specification — user stories, Gherkin scenarios, edge cases, NFRs, out-of-scope, data contracts | Individual `*.spec.md` files |
| L3 | Detailed per-story dossiers — full acceptance criteria, interface definitions, data schemas, examples | `dossiers/` directory |
| SOURCES | Navigation index linking each L2 dimension to its L3 sources | Footer of each file |

## Loading Guidance

| Reference | When to load | File |
|-----------|-------------|------|
| Spec Quality Gates | Before delivering any SPEC.md — validates completeness against 7 quality dimensions | `references/spec-quality-gates.md` |
| Gherkin Patterns | Writing executable scenarios — Given/When/Then structure for specific patterns | `references/gherkin-patterns.md` |
| Acceptance Criteria Design | Crafting ACs that pass the "no-surprises" test — edge case enumeration, boundary conditions | `references/acceptance-criteria-design.md` |

| Template | When to use | File |
|----------|-------------|------|
| SPEC.md | Producing a specification document from scratch | `templates/SPEC.md` |

| Script | When to run | File |
|--------|-------------|------|
| `spec-quality-check.sh` | After authoring a SPEC.md — validates all required sections exist | `scripts/spec-quality-check.sh` |

## Trigger Conditions

Invoke this skill when:
- A new feature, component, or system needs a formal specification before implementation begins
- An existing specification needs refinement or gap analysis
- A vague requirement (ticket, conversation, email) needs to be translated into a structured SDD-ready spec
- The input is a research report, competitive analysis, or user interview transcript that needs distillation into engineering requirements

## Output Contract

Every SPEC.md MUST include:

1. **Problem statement** — what problem this solves and why it matters
2. **Scope boundary** — explicit in-scope and out-of-scope
3. **User stories** — prioritized, with links to acceptance criteria
4. **Acceptance criteria** — per-story, framed as Given/When/Then or bulleted pass/fail conditions
5. **Edge cases** — explicit enumeration of boundary conditions, error states, invalid inputs
6. **Non-functional requirements** — performance, security, observability, compliance, accessibility
7. **Data contracts / interfaces** — schemas, APIs, events (can be stubs that get refined in later phases)

The spec is NOT complete until a automated quality check passes (run `spec-quality-check.sh`).

## SDD Philosophy

Specifications in SDD serve a different purpose than traditional requirements documents. They are not communication artifacts for humans that happen to be read by an AI. They are **executable inputs to a code generation pipeline** that happen to be readable by humans.

This distinction drives everything about how specs are written:

- **Precision over clarity.** A spec that is technically precise but dense is better than a spec that reads well but leaves ambiguity. The AI cannot ask for clarification when it encounters a vague phrase — it implements one interpretation at random.
- **Completeness over brevity.** Every missing acceptance criterion is a missing feature, not a question the implementer will ask. The cost of specifying an edge case up front is minutes. The cost of discovering it in production is hours or days.
- **Testability over descriptiveness.** An acceptance criterion that cannot be verified (passed or failed) by a deterministic check is not an acceptance criterion — it is a hope. Every AC must produce a binary verdict.

## Framework Awareness

This skill is methodology-agnostic at the framework level but follows SDD principles common to all major frameworks:

- **GitHub Spec Kit** — Four-phase Specify→Plan→Tasks→Implement. The spec produced here fulfills Phase 1 (Specify).
- **GSD** — Uses PROJECT.md and REQUIREMENTS.md as spec layer. SPEC.md maps to these artifacts.
- **BMAD** — Role-based specification chain (BA → PRD → Architecture). SPEC.md here aligns with the PRD and Architecture layers.
- **Taskmaster AI** — PRD-driven. SPEC.md is the structured PRD that Taskmaster parses into task graphs.
- **Native Claude Code** — CLAUDE.md + spec files. SPEC.md is consumed alongside CLAUDE.md by the implementation agent.
