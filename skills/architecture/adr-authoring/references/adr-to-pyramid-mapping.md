# ADR-to-Pyramid Mapping

## Mapping Table

| ADR State | Pyramid Layer | What Lives There | Consumer |
|-----------|--------------|------------------|----------|
| Navigation index | **L1** (01-summary/) | List of all ADRs with status, link to each | Orchestrator needing to find a decision |
| Active ADRs | **L2** (02-analysis/) | Full decision record: context, options, rationale, consequences | Engineers, reviewers |
| Superseded ADRs | **L3** (03-dossiers/) | Historical decisions that have been replaced | Historians, anyone challenging a current decision |

## Why ADRs Need Three Layers

ADRs are modular by nature — each decision is a single document. But they still benefit from progressive disclosure:

- **L1:** A navigation index helps an agent find the right ADR without reading all of them
- **L2:** Active ADRs provide the decision rationale alongside the C4 views they relate to
- **L3:** Superseded ADRs preserve decision history without cluttering active analysis

## Relationship to C4

Every ADR in L2 should reference the C4 Container or Component it affects. Every C4 Container/Component diagram should reference the ADRs that shaped it.
