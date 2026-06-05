---
name: adr-authoring
description: "Architecture Decision Records — decision capture, rationale documentation, alternatives analysis, and consequence tracking. Maps ADRs to Artifact Pyramid layers (navigation index→L1, active ADRs→L2, superseded ADRs→L3). Use when the technical-architect profile needs to document architectural decisions."
---

# ADR Authoring

Architecture Decision Records for capturing design rationale. ADRs supply the temporal dimension — decisions over time — that structure-only views (C4) miss.

## ADR-to-Pyramid Mapping

| ADR State | Pyramid Layer | Path |
|-----------|--------------|------|
| Navigation index | L1 (Summary) | 01-summary/adr-index.md |
| Active ADRs | L2 (Analysis) | 02-analysis/architecture-decisions/ADR-NNN.md |
| Superseded ADRs | L3 (Dossiers) | 03-dossiers/adr-superseded.md |

Without ADRs, an agent sees a snapshot of the structure but cannot reconstruct the path that led to it. Active ADRs in L2 provide the decision rationale. Superseded ADRs in L3 preserve the history of rejected alternatives.

## ADR Lifecycle

ADRs progress through six stages, each with a gate criterion:

```
Initiating → Researching → Evaluating → Implementing → Maintaining → Sunsetting
```

| Stage | Status | Pyramid Layer | Consumer |
|-------|--------|--------------|----------|
| Initiating | `proposed` | L2 (02-analysis/) | Engineers evaluating |
| Researching | `proposed` | L2 (02-analysis/) | Engineers evaluating |
| Evaluating | `proposed` | L2 (02-analysis/) | Engineers deciding |
| Implementing | `accepted` | L2 (02-analysis/) | Implementers, reviewers |
| Maintaining | `accepted` | L2 (02-analysis/) | New team members, auditors |
| Sunsetting | `deprecated`/`superseded` | L3 (03-dossiers/) | Historians |

All live ADRs (proposed + accepted) stay in L2. Only superseded/deprecated ADRs move to L3. Proposed ADRs that are rejected should be moved to L3 with status `rejected` and a note on why.

### Alternative Lifecycle: AWS ADR Process

AWS Prescriptive Guidance defines a complementary lifecycle with a structured review process for teams that prefer formal immutability over living documents.

**States:** `proposed → accepted | rejected | superseded`

**Key difference:** AWS treats ADRs as strictly immutable once accepted. Changing a decision requires a new ADR that supersedes the old one. The community ADR repo's teamwork advice prefers mutable living documents with date-stamped updates. Choose the model that fits your team's culture.

**AWS Review Process:**

1. **Proposal** — any team member creates an ADR in `proposed` state. The author is the ADR owner.
2. **Review meeting** — dedicated time slot with structured format:
   - **10-15 minutes silent reading** — each member reads the ADR and adds comments
   - **Comment read-out** — the owner reads each comment aloud; team discusses
   - **Action points** — identified issues get an assignee; tracked to resolution
3. **Decision** — three outcomes:
   - **Accepted** → owner adds timestamp, version, stakeholder list. State → `accepted`. Immutable.
   - **Rework** → state stays `proposed`. Owner resolves action points and re-schedules review.
   - **Rejected** → owner documents rejection reason (prevents future re-litigation). State → `rejected`. File moves to L3.
4. **Superseding** — new decision invalidates an accepted ADR? Create a new ADR. On acceptance, update old ADR status to `superseded` and move it to L3.

```
[Identify need] → [Draft (proposed)] → [10-15m silent read] → [Discuss]
                      ↓                     ↓                     ↓
                 [Rework/review] ← [Needs rework]          [Accepted] → [Immutable]
                                                           [Rejected] → [L3]
```

## Template Selection

| When | Template | Sections |
|------|----------|----------|
| Quick decision, single rationale | **Nygard** | Status, Context, Decision, Consequences |
| Multi-option trade-off analysis | **MADR** | Decision Drivers, Considered Options, Pros/Cons, Links |
| High-stakes, regulatory, compliance | **Tyree & Akerman** | 12 sections: Issue, Positions, Argument, Implications, etc. |
| Vendor/procurement decision | **Business Case** | Evaluation criteria, Cost/SWOT, Recommendations |
| QA/contract-driven environment | **Planguage** | Tag, Gist, Priority, Stakeholders, Risks |

Full catalog with section-by-section guidance in `references/adr-format.md`.

## File Naming Conventions

Use present tense imperative verb phrases, lowercase-dashes, `.md` extension:

```
001-choose-database.md
002-format-timestamps.md
003-manage-secrets.md
```

Status lives in the document header, not the filename — status changes shouldn't require renames.

## Teamwork & Governance

- **Who can create:** Any team member who has read the ADR process docs
- **What justifies:** Decisions affecting future "why", cross-team coordination, long-term maintainability, external interfaces
- **What does NOT:** Limited scope/time/risk, already covered by standards, temporary workarounds/POCs
- **Roles per ADR:** Primary contact, secondary contact, accountable team
- **Living documents preferred:** Insert new info with date stamps rather than superseding ADRs for every update. Immutability is ideal in theory; mutability works better in practice.

See `references/adr-format.md` for the full governance model and teamwork questions.

## Contents

- `references/adr-format.md` — template catalog (11 formats: Nygard, MADR, Tyree & Akerman, Business Case, Planguage, Alexandrian, ITD, arc42, EdgeX, Gareth Morgan, NHS Wales), template selection decision tree, lifecycle stages, file naming, team governance, examples reference
- `references/adr-to-pyramid-mapping.md` — active→L2, superseded→L3, consumer routing
- `references/fitness-functions.md` — decisions as code: ArchUnit, ArchUnitTS, AI-assisted fitness functions, pyramid mapping (fitness functions → L3)
- `references/decision-sustainability.md` — 5 sustainability criteria + 8 guidelines for evaluating ADR quality before acceptance
- `references/project-setup-guide.md` — bootstrapping ADRs in a new project: directory setup, README index, CONTRIBUTING.md/AGENTS.md docs, issue-first PR workflow with worked example

## Canonical Reference

- Architecture Decision Record community repo — https://github.com/architecture-decision-record/architecture-decision-record
- Michael Nygard, "Documenting Architecture Decisions" — https://thinkrelevance.com/blog/2011/11/15/documenting-architecture-decisions
- Magnus Hedemark, "Clanker Technical Architect: First on the Scene with Progressive Disclosure" — https://magnus919.com/2026/05/clanker-technical-architect-first-on-the-scene-with-progressive-disclosure/
