# Methodology-to-Pyramid Mapping — Specialist Profile Convention

## The Pattern

Specialist profiles (researcher, technical-architect, data-architect, product-manager) each own a set of domain-specific methodologies. When consuming a task, they produce their domain's natural artifacts — but they structure those artifacts as an Artifact Pyramid at a known filesystem path and hand off ONLY the path to 00-index.md.

The pyramid structure is universal. The methodology mapping is domain-specific.

## Existing Mappings

### Researcher Profile

| Domain Artifact | Methodology | Pyramid Layer |
|----------------|-------------|--------------|
| Research question + key findings | Mission interpolation | L1 Summary |
| Per-dimension analysis (market, technical, competitive) | Systematic gathering + gap evaluation | L2 Analysis Collection |
| Source excerpts, transcripts, raw data | Source capture | L3 Dossiers |
| Path: `/tmp/researcher-workflow/<slug>/00-index.md` |

### Technical-Architect Profile

| Domain Artifact | Methodology | Pyramid Layer |
|----------------|-------------|--------------|
| C4 Level 1 (System Context) + arc42 Canvas + Decision dashboard | C4 Model, arc42 | L1 Summary |
| C4 Level 2 (Container), C4 Level 3 (Component), Active ADRs, arc42 sections 1-4, Quality attributes, Failure mode analysis | C4 + ADRs + arc42 | L2 Analysis Collection |
| C4 Level 4 (by exception), Superseded ADRs, Spike results, API contracts | C4 + ADRs | L3 Dossiers |
| Path: `/tmp/architect-workflow/<slug>/00-index.md` |

## Dimension Boundary Rules

When multiple methodologies overlap (e.g., C4 says "PostgreSQL 16" and arc42 says "must use RDS" and an ADR says "why PostgreSQL over MongoDB"), use these rules to decide where the fact lives:

| Claim Type | Goes In | Because |
|-----------|---------|---------|
| Structural choice (what) | C4-level file (L2) | Structural view shows the choice |
| Rationale (why) | ADR (L2) | ADRs capture reasoning |
| Constraint (must) | arc42 context file (L2) | Constraints are external forces |
| Quantified target (how good) | Quality attributes file (L2) | Scenarios, not decisions |
| Degradation (when it breaks) | Failure mode file (L2) | Different analytical dimension |
| Historical (was, but no longer) | L3 dossier | Reference only, not governing |

## Creating a New Profile Mapping

1. **Identify the profile's core methodologies.** What does a human in this role produce? (e.g., product manager produces PRDs, OKRs, competitive analyses)
2. **Map each artifact to a pyramid layer.** The summary document goes in L1. The per-dimension analysis goes in L2 (one file per dimension). The supporting reference materials go in L3.
3. **Define the output path.** Convention: `/tmp/<profile-role>-workflow/<slug>/00-index.md`
4. **Document the handoff.** The profile responds with ONLY the path to 00-index.md. Same convention as every other specialist profile.
5. **Define dimension boundaries.** If two methodologies would both claim the same fact, document which one owns it.

## Why This Matters

Without explicit methodology-to-pyramid mapping, each profile invents its own convention. With it, downstream orchestrators can route agents to any profile and know the handoff format is identical — only the content methodology changes. This makes specialist profiles plug-compatible.
