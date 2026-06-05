# ADR Format & Authoring Guide

Complete catalog of Architecture Decision Record formats from the community ADR repository (https://github.com/architecture-decision-record/architecture-decision-record), with selection guidance by decision type and worked examples.

## Template Selection Guide

| Decision Type | Recommended Template | Why |
|---|---|---|
| Routine technology choice (library, framework) | **Nygard** | Lightweight: Status, Context, Decision, Consequences |
| Multi-option trade-off with explicit comparison | **MADR** | Decision Drivers + Considered Options with pros/cons |
| High-stakes / regulatory / compliance | **Tyree & Akerman** | 12 sections covering Issue, Assumptions, Constraints, Positions, Argument, Implications, Related decisions/requirements/artifacts/principles |
| Vendor / procurement / build-vs-buy | **Business Case** | Evaluation criteria, cost analysis, SWOT, opinions/recommendations |
| QA-contract / SLAs / non-functional requirements | **Planguage** | Tag, Gist, Priority, Stakeholders, Risks, Defined terms |
| Quick internal consensus, no formal review | **Alexandrian** | Context-specific, minimal structure |
| C-suite / executive review | **ITD (Important Technical Decisions)** | Decision-first, optimized for fast executive scanning |

---

## Template Catalog

### 1. Michael Nygard (Simple & Popular)

**Origin:** http://thinkrelevance.com/blog/2011/11/15/documenting-architecture-decisions

**When to use:** Everyday decisions where the rationale is straightforward and options are few. The default choice unless you need more structure.

```
# Title (present tense imperative verb phrase)

## Status

proposed | accepted | rejected | deprecated | superseded by ADR-NNN

## Context

What is the issue that we're seeing that motivates this decision or change?

## Decision

What is the change we're proposing and/or doing?

## Consequences

What becomes easier or more difficult to do because of this change?
```

**Section guidance:**
- **Title:** Short imperative phrase like "Use PostgreSQL for transaction storage" or "Adopt event-driven messaging between services"
- **Status:** Single value. Use lifecycle stages for more precision.
- **Context:** The forces at play — business need, technical constraint, team capability, timeline pressure. Include why this decision is being made *now*.
- **Decision:** The outcome. Concrete and unambiguous. "We will use X" not "We considered using X."
- **Consequences:** Both positive and negative. What trade-offs are being accepted? What follow-up decisions does this create?

**Pitfalls:**
- Too terse for multi-stakeholder decisions where options need explicit comparison
- No natural place for decision driver documentation
- Temptation to skip "Consequences" when they're the most important section

---

### 2. MADR — Markdown Any Decision Records (Structured)

**Origin:** https://adr.github.io/madr/

**When to use:** Most decisions that involve multiple options with explicit trade-off comparison. The best default for most engineering teams.

```
# [short title of solved problem and solution]

* Status: proposed | rejected | accepted | deprecated | superseded by ADR-NNN
* Deciders: [list everyone involved in the decision]
* Date: YYYY-MM-DD

Technical Story: [description | ticket/issue URL]

## Context and Problem Statement

[Describe the context and problem statement. You may want to articulate the
 problem in form of a question.]

## Decision Drivers

* [driver 1, e.g., a force, facing concern]
* [driver 2]
* ...

## Considered Options

* [option 1]
* [option 2]
* [option 3]

## Decision Outcome

Chosen option: "[option 1]", because [justification].

### Positive Consequences

* [e.g., improvement of quality attribute satisfaction]
* ...

### Negative Consequences

* [e.g., compromising quality attribute]
* ...

## Pros and Cons of the Options

### [option 1]

* Good, because [argument a]
* Good, because [argument b]
* Bad, because [argument c]

### [option 2]

* Good, because [argument a]
* Bad, because [argument b]

## Links

* Refined by [ADR-0005](0005-example.md)
* Supersedes [ADR-0002](0002-example.md)
```

**Section guidance:**
- **Decision Drivers:** The non-negotiable constraints that any solution must satisfy. These are your selection criteria. If the decision doesn't need explicit criteria, consider using Nygard instead.
- **Considered Options:** Exhaustive enough that no reviewer asks "Did you think about X?" but not so exhaustive it becomes noise. 3-5 options is typical.
- **Pros and Cons:** Each option gets its own subsection with bullet-point pros and cons. Be specific — "Good, because reduces latency by 40% under peak load" not "Good, because faster."
- **Links:** Bidirectional links to related ADRs. Use semantic link types: supersedes, refines, contradicts, extends.

**Pitfalls:**
- "Considered Options" sections can balloon. Cap at 5 options; group similar alternatives.
- Decision Drivers are often just listed not ranked. Prioritize them (Must-have vs Nice-to-have).

---

### 3. Jeff Tyree & Art Akerman (Heavyweight / Enterprise)

**Origin:** https://www.utdallas.edu/~chung/SA/zz-Impreso-architecture_decisions-tyree-05.pdf

**When to use:** High-stakes decisions with regulatory, compliance, or cross-team implications. Decisions that will be audited or referenced for years.

| Section | Purpose |
|---|---|
| **Issue** | The architectural design issue being addressed, with clear rationale for why *now* |
| **Decision** | The architecture's direction — the position selected |
| **Status** | pending, decided, approved |
| **Group** | Ontology grouping: integration, presentation, data, event, calendar, location |
| **Assumptions** | Underlying environmental assumptions (cost, schedule, technology, accepted standards) |
| **Constraints** | Additional constraints the chosen alternative imposes |
| **Positions** | Viable options considered. Include models, diagrams. This prevents "Did you think about X?" in review |
| **Argument** | Why you selected the position: implementation cost, TCO, time-to-market, resource availability. As important as the decision itself |
| **Implications** | Follow-on effects: new required decisions, new/modified requirements, additional constraints, scope/ schedule changes, training needs |
| **Related decisions** | Traceability matrix, decision trees, or metamodels. Links to related AD decisions |
| **Related requirements** | Direct mapping to business objectives. If a decision doesn't contribute to a requirement, don't make it |
| **Related artifacts** | Architecture, design, or scope documents this decision impacts |
| **Related principles** | Enterprise principles this decision is consistent with. Ensures cross-system alignment |
| **Notes** | Running notes from the socialization process |

**When to skip:** Routine choices, single-developer decisions, temporary workarounds.

---

### 4. Business Case (Procurement / Vendor)

**When to use:** Build-vs-buy, vendor selection, technology procurement — decisions where cost and organizational impact are primary drivers.

**Top-level structure:**
- Title
- Status
- Evaluation criteria
- Candidates to consider
- Research and analysis of each candidate
  - Does/doesn't meet criteria
  - Cost analysis (licensing, training, operating, metering)
  - SWOT analysis (Strengths, Weaknesses, Opportunities, Threats)
  - Internal and external opinions/feedback
- Recommendation

**Cost analysis dimensions:**
- **Licensing:** contract agreements, legal commitments, vendor lock-in risk
- **Training:** upskilling, change management, ramp time
- **Operating:** support, maintenance, incident response
- **Metering:** bandwidth, CPU, API calls, data egress

**Pitfalls:**
- External opinions can be biased toward whatever the vendor recommends. Cross-reference.
- Cost estimates age fast — include date stamps on all pricing references.

---

### 5. Planguage (QA / NFR Focused)

**Origin:** Tom Gilb, https://www.iaria.org/conferences2012/filesICCGI12/Tutorial%20Specifying%20Effective%20Non-func.pdf

**When to use:** Decisions driven by quality attributes, SLAs, or non-functional requirements where precision and measurability matter.

| Keyword | Purpose |
|---|---|
| **Tag** | Unique, persistent identifier |
| **Gist** | Brief summary of the requirement or area |
| **Requirement** | The requirement text |
| **Rationale** | Reasoning justifying the requirement |
| **Priority** | Statement of priority and claim on resources |
| **Stakeholders** | Parties materially affected |
| **Status** | Draft, reviewed, committed |
| **Owner** | Person responsible for implementing |
| **Author** | Person who wrote it |
| **Revision** | Version number |
| **Date** | Most recent revision date |
| **Assumptions** | Things that could cause problems if untrue |
| **Risks** | Things that could cause malfunction or delay |
| **Defined** | Glossary terms |

---

### 6. Alexandrian Pattern (Context-First)

**When to use:** Decisions where the context is the main driver and the solution space is tightly constrained.

```
## [Title]

## Context

[The forces at play — when does this pattern apply?]

## Problem

[The specific problem this decision addresses]

## Solution

[The decision, stated as the resolution of the forces]

## Consequences

[What follows from applying this solution]
```

---

### 7. Important Technical Decisions — ITD (Executive)

**Origin:** Ignacio Larrañaga

**When to use:** Decisions that need executive sign-off. Lean and decision-first — optimized for fast scanning, not detailed deliberation.

```
# [Decision title]

## Decision

[One-line statement of what was decided]

## Why

[Brief rationale — why this decision, why now]

## Impact

[What changes as a result — one paragraph]
```

---

### 8. arc42 ADR Template (Full Documentation Structure)

**Origin:** https://arc42.org/overview — License: CC-BY-SA 4.0

**When to use:** Decisions that need to be documented within the full arc42 architecture documentation framework. This is the ADR-specific template by the arc42 team, distinct from the arc42 full documentation template (used by the `arc42-context` skill for system context/constraint documentation).

**Sections:**

| arc42 Section | Purpose |
|---|---|
| **1. Introduction & Goals** | Requirements, driving forces, quality goals, stakeholders |
| **2. Constraints** | Anything constraining design/implementation freedom |
| **3. Context & Scope** | System boundary, external interfaces, business/technical context |
| **4. Solution Strategy** | Fundamental decisions shaping the architecture |
| **5. Building Block View** | Static decomposition — modules, components, layers |
| **6. Runtime View** | Behavior via scenarios — use cases, errors, operations |
| **7. Deployment View** | Infrastructure, environments, mapping of building blocks |
| **8. Crosscutting Concepts** | Patterns, rules, regulations spanning multiple building blocks |
| **9. Architectural Decisions** | Important decisions including rationale (this is the ADR proper) |
| **10. Quality Requirements** | Quality scenarios, quality tree |
| **11. Risks & Technical Debt** | Known risks, debt; ordered by priority |

**Relationship to arc42-context skill:** Our arc42-context skill uses the full arc42 template for documenting system constraints at the project level. This ADR template is a *lightweight version* focused on a single decision within that framework. Use this when documenting a decision inside existing arc42 documentation.

---

### 9. EdgeX Template (Platform / IoT)

**Origin:** https://docs.edgexfoundry.org/2.3/design/adr/template/

**When to use:** Decisions involving platform components, service boundaries, or API changes — especially IoT/edge contexts where multiple services are impacted.

```
# [Title]

## Submitters

- Name (Organization)

## Change Log

- [Status](URL of PR) YYYY-MM-DD
  Status: pending, approved, amended, deprecated.

## Referenced Use Case(s)

- [Use Case Name](URL)

## Context

- How the design is architecturally significant
- High-level design approach

## Proposed Design

Details without implementation:

- Services/modules impacted (changed)
- New services/modules to be added
- Model and DTO impact (additions/removals)
- API impact (additions/removals)
- Configuration impact
- DevOps impact

## Considerations

Alternatives, concerns, issues from debate. Resolution status.

## Decision

Caveats, future considerations, remaining or deferred issues.
Requirements not satisfied by the proposed design.

## Other Related ADRs

- [ADR Title](URL) — Relevance

## References
```

**Distinctive features:** Change Log with state/date/PR URL; Referenced Use Case(s); unusually detailed Proposed Design (model/DTO/API/config/devops). Good for when the ADR serves as both decision record AND preliminary design document.

---

### 10. Gareth Morgan Template (Summary-Driven)

**Origin:** Gareth Morgan

**When to use:** Decisions needing an executive summary first, followed by structured option analysis. Summary → Drivers → Options → Analysis → Recommendation structure mirrors modern product decision-making.

```
# [Title]

**Status:** Proposed | Under Review | Accepted | Rejected | Superseded | Deprecated
**Updated:** YYYY-MM-DD

## Summary

Executive summary / elevator pitch. 2-4 sentences stating the core problem
and a hint at the decision. Think abstract of a technical paper.

## Drivers

Why this decision is being made now:

- {We are developing a new feature that needs...}
- {We need to improve performance, accessibility...}
- {The current approach imposes limitations...}

## Options

List of options with facts, links:

### {Option 1}
Description

### {Option n}
...

## Options Analysis

### {Option 1 Assessment}
- Pro: {Specific advantage}
- Con: {Specific disadvantage, risk, or cost}
- Other: {Relevant point}

### {Option n Assessment}
...

## Recommendation

Clear statement of the final decision and why it best addresses the Drivers.

### Consequences

- Pro: {Positive outcome}
- Con: {Accepted downside or risk}
- Other: {Matter-of-fact consequence}

### Confirmation

- How implementation will be verified (reviews, tests, demos)
- How compliance will be maintained (automated checks, audits)
- Metrics/indicators showing intended outcomes
- Responsible owner

## More Information

Supplementary info, links, re-evaluation timeframe.
```

**Distinctive features:** Summary-first (elevator pitch before detail); explicit Drivers section (why *now*); Consequences classified as Pro/Con/Other; **Confirmation section** — a verification plan with compliance monitoring, metrics, and ownership. Rare in ADR templates and essential for high-stakes decisions.

---

### 11. GIG Cymru NHS Wales Template (Governance-Focused)

**Origin:** NHS Wales / GIG Cymru

**When to use:** Regulated environments (healthcare, finance, infrastructure) where compliance monitoring, governance, and visual options analysis are required.

```
# [Title]

**Status:** DRAFT | ACTIVE | DEPRECATED by [000] | SUPERSEDES [000]

## Context

Problem(s) this ADR addresses and why they exist.

## Decided Approach

Architecturally significant decision and how it solves the problem.

## Consequences

Impact on architecture characteristics and functional requirements.

## Governance

How will outcomes be monitored? How will compliance be ensured?

## Options Analysis

Trade-off analysis with traffic-light comparison tables.

### Key

Green = good fit  Amber = moderate  Red = poor fit
+ = positive comment  - = negative comment

### High-Level Overview

| Summary | Option 1 | Option 2 | Option 3 |
|---|---|---|---|
| Ease of Implementation | + Quick (green) | - Tricky (amber) | - Complex (red) |
| Timescales | + Fast (green) | - Slow (amber) | - Very slow (red) |
| Strategic Value | - Tactical (red) | + Improves (amber) | + Ideal (green) |

### Functional Requirements

| Scenario | Option 1 | Option 2 | Option 3 |
|---|---|---|---|
| Scenario 1 | | | |

### Non-Functional Requirements

| Characteristic | Option 1 | Option 2 | Option 3 |
|---|---|---|---|
| Scalability | | | |
| Performance | | | |
| Availability | | | |
```

**Distinctive features:** **Governance section** — unique among templates, asks explicitly about compliance monitoring. **Traffic-light comparison tables** — color-coded visual evaluation across summary, functional, and NFR dimensions. Designed for audited environments where decisions must be enforced, not just recorded.

---

### Template Selection Decision Tree

```
Is the decision quick, single-rationale?
  → YES → Nygard
  → NO → Multiple options being compared?
    → YES → Regulatory/governance requirement?
      → YES → Compliance monitoring needed?
        → YES → NHS Wales (governance + traffic-light tables)
        → NO → Cost a primary driver?
          → YES → Business Case (cost/SWOT)
          → NO → Platform/service boundary change?
            → YES → EdgeX (Change Log + Proposed Design)
            → NO → MADR (structured option comparison)
      → NO → MADR (default for multi-option)
    → NO → QA/NFR-driven? → Planguage
    → NO → C-suite consumption? → ITD
    → NO → Context-first? → Alexandrian
```

---

### Examples Reference

The community ADR repository includes ~50+ worked examples across multiple domains for learning and inspiration:

| Domain | Example Topics |
|---|---|
| **Frameworks** | CSS framework, React, Svelte, Vue, Rails, SvelteKit, Tailwind CSS |
| **Databases** | MySQL, PostgreSQL, Database technology choice |
| **Languages** | Go, Rust, Java, Python |
| **Infrastructure** | Docker Swarm, Kubernetes, AWS, GCP, Azure, CI, Secrets storage |
| **APIs & Protocols** | JSON vs gRPC, snake_case vs camelCase, Timestamp format |
| **Team & Process** | 4-day work week, Agile, High-trust teamwork, Work from home |
| **Cross-cutting** | Monorepo vs multirepo, Environment variable config, Metrics |

Browse the full collection at: https://github.com/architecture-decision-record/architecture-decision-record/tree/main/locales/en/examples/

Study 2-3 examples from your domain before writing a first ADR to internalize the conventions.

---

## Worked Example: MADR Format

```
# Use PostgreSQL for Service Transaction Storage

* Status: accepted
* Deciders: Magnus Hedemark, Sarah Chen, DevOps Team
* Date: 2026-06-05

Technical Story: Service requires durable, ACID-compliant storage for
customer transaction records across geographic regions.

## Context and Problem Statement

The service needs to store customer transaction data with strong consistency
guarantees. The current prototype uses in-memory storage which is unacceptable
for production. We need a database that supports ACID transactions, replication
across regions, and has a proven operational track record.

## Decision Drivers

* Must support ACID transactions (non-negotiable — regulatory requirement)
* Must support active-passive replication across 2 regions
* Team has existing PostgreSQL expertise (3 senior DBAs)
* Must fit within existing $500/mo infrastructure budget

## Considered Options

* PostgreSQL — relational, ACID, mature replication (pglogical / Patroni)
* MySQL — relational, ACID, Group Replication
* CockroachDB — distributed SQL, natively multi-region
* DynamoDB + transactions — managed NoSQL with limited ACID

## Decision Outcome

Chosen option: "PostgreSQL", because it satisfies all decision drivers,
eliminates team learning curve, and has the lowest operational cost for our
scale.

### Positive Consequences

* ACID compliance guaranteed within existing team expertise
* Active-passive replication via Patroni (deploy this week)
* No licensing costs; fits within infrastructure budget

### Negative Consequences

* Manual sharding may be needed above 5TB (unlikely in year 1)
* Single-writer limitation in active-passive mode

## Pros and Cons of the Options

### PostgreSQL

* Good, because full ACID with serializable isolation
* Good, because existing team expertise eliminates ramp time
* Good, because mature replication tooling (Patroni, repmgr)
* Bad, because single-writer topology limits write throughput

### MySQL

* Good, because ACID with InnoDB
* Good, because Group Replication supports multi-writer
* Bad, because less team expertise (1 DBA vs 3 for Postgres)
* Bad, because Group Replication has known stability issues in async mode

### CockroachDB

* Good, because natively multi-region with strong consistency
* Bad, because 2x infrastructure cost for equivalent hardware
* Bad, because operational complexity requires dedicated SRE support

### DynamoDB + Transactions

* Good, because zero operations overhead
* Bad, because transaction API has 25-item / 4MB limits
* Bad, because vendor lock-in to AWS
* Bad, because $0.50/hr per replica is over budget at scale

## Links

* Refined by [ADR-0010](0010-patroni-cluster-configuration.md)
* Supersedes [ADR-0003](0003-in-memory-storage-poc.md)
```

---

## Architecture Decision Log (ADL) Conventions

### File Naming

```
NNN-short-present-tense-phrase.md
```

Rules:
- **Number:** Zero-padded sequence (001, 002, ... 010). Avoid gaps; renumber on conflict.
- **Phrase:** Present tense imperative verb phrase — like a good commit message.
  - Good: `012-use-postgresql-for-transaction-storage.md`
  - Bad: `012-postgresql.md` (no verb), `012-decided-to-use-postgresql.md` (past tense)
- **Case:** Lowercase with hyphens (kebab-case).
- **Extension:** `.md` for easy rendering.

### Directory Naming

Consider naming the directory `decisions/` instead of `adr/` — some teams respond better to plain language. The template is content-neutral; you can document vendor decisions, planning decisions, and scheduling decisions in the same format.

### Numbering Scheme

- Sequential across the entire project (not per-category)
- Never reuse a number — if an ADR is rejected, leave the number retired
- Consider prefix for multi-project orgs: `PLAT-012-use-postgresql.md`
