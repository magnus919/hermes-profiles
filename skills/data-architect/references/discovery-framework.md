# Architecture Discovery Framework

A structured approach to understanding a client's context before making recommendations. Use this when starting an architecture consulting session.

## Phase 1: Problem & Context

Establish what we're actually solving:

**Business:**
- What business problem are you solving? What's the measurable outcome?
- Who is asking for this? What's their pain point?
- What happens if we do nothing?
- What does success look like in 3 months, 12 months?

**Organizational:**
- Who are the stakeholders? Who has decision authority?
- What's the team structure — who builds, who operates, who consumes?
- What's the current team capability (size, seniority, key skills)?
- Is there executive sponsorship for cross-team changes?

**Temporal:**
- What's the timeline? What's driving the urgency?
- What's frozen (can't change) vs flexible?
- Are there existing commitments (vendor contracts, hiring freezes, compliance deadlines)?

## Phase 2: Current State

Understand what exists today:

**Data Profile:**
- What data sources exist? (Count, types, systems of record)
- Current data volume, velocity, variety — and projected 18-month growth
- Where is data quality acceptable vs problematic?
- What's the schema evolution frequency of source systems?

**Architecture:**
- Diagram the current data flow — source to consumption
- What's the current stack? (warehouse, pipeline tooling, BI layer, catalog)
- What's working well (don't fix what isn't broken)?
- What's the biggest operational pain point?

**Consumption:**
- Who consumes data and how? (analysts, data scientists, operational apps, ML models)
- What are their actual latency, freshness, and accuracy requirements?
- What do they complain about most?

**Governance:**
- What data governance exists currently? (ownership, quality, lineage, access control)
- What compliance/regulatory frameworks apply? (GDPR, HIPAA, SOX, CCPA, BCBS 239)
- Are there existing data sharing agreements or contractual constraints?

**Cost:**
- Current data infrastructure spend (compute, storage, tools, people)
- Where is cost growing fastest?
- Are there wasteful patterns (orphaned tables, unused pipelines, over-provisioned compute)?

## Phase 3: Constraints

Identify the hard boundaries:

**Non-negotiable:**
- Regulatory requirements
- Budget ceilings
- Hiring timeline
- Existing vendor contracts

**Tradeable:**
- Time-to-market vs robustness
- Feature scope vs timeline
- Central control vs team autonomy
- Managed service premium vs operational flexibility

**Unknowns to validate:**
- What assumptions are we making that should be tested?
- What POCs should we run before committing to an architecture?

## Phase 4: Recommendation Structure

Present findings as:

**Quick wins (this month)**
High impact, low effort — do these immediately regardless of long-term direction.
*(e.g., add data quality checks at ingestion, document current lineage, consolidate redundant pipelines)*

**Foundation (next quarter)**
Medium-term investments that enable future phases.
*(e.g., implement data catalog, establish governance board, standardize naming conventions)*

**Transformation (next 12 months)**
Major architectural shifts that require sequence and dependency management.
*(e.g., migrate from on-prem EDW to cloud, adopt Data Mesh, implement streaming platform)*

**Deferred / Not Yet**
Things that were requested but don't make sense given the current context.
*(e.g., "we should add real-time streaming" when batch is meeting all SLAs)*

## Phase 5: Risk Register

Flag these for every engagement:

- **Single point of failure** — one person who knows how X works
- **Vendor lock-in trajectory** — growing dependence on a platform without migration plan
- **Technical debt that compounds** — shortcuts taken now that make future changes harder
- **Skills gap** — architecture assumes capabilities the team doesn't have
- **Organizational dependency** — project requires another team's cooperation without their buy-in
- **Compliance cliff** — approaching regulatory deadline that current architecture can't meet

## Consulting Session Flow

```
1. "Tell me about the problem" → listen, don't prescribe
2. "What have you tried?" → understand the history
3. "What's the actual scale?" → quantify before designing
4. "Draw me your current flow" → visualize the as-is
5. "What hurts most?" → identify leverage points
6. "What's the simplest thing that could work?" → avoid over-engineering
7. "Here's what I recommend, and here's why..." → tradeoffs explicit
8. "What did I miss?" → invite challenge
```
