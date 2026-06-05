# Data Architect — Hermes Profile

Data modeling, pipeline architecture, storage strategy, and schema design for teams building data-intensive systems.

## What This Profile Provides

- **Data modeling** — entity-relationship, dimensional modeling, schema design
- **Platform selection** — storage technology evaluation with tradeoff analysis
- **Pipeline architecture** — streaming vs batch, ETL vs ELT, data flow design
- **Governance** — data quality, lineage, access control patterns
- **Cost analysis** — storage and compute cost modeling at scale

## Installation

```bash
git clone https://github.com/magnus919/hermes-profiles.git ~/hermes-profiles
ln -s ~/hermes-profiles/profiles/data-architect ~/.hermes/profiles/
hermes --profile data-architect
```

## Quick Start

> "Design the data architecture for a payment processing system handling 10K transactions per minute with PCI-DSS compliance."

The profile will:
1. Understand the data landscape — sources, volume, velocity, consumers
2. Evaluate storage and pipeline options with explicit tradeoffs
3. Document data flow, quality checks, and governance requirements
4. Output an artifact pyramid at `/tmp/data-workflow/<project>/00-index.md`

## Skill Dependencies

| Skill | Provides |
|---|---|
| `artifact-pyramids` | Progressive disclosure output format |

## Related Profiles

- **technical-architect** — provides the systems context data architecture runs within
- **implementation-planner** — consumes data architecture for build sequencing

## Output Format

Artifact pyramid. Response is the absolute path to `00-index.md`.
