# Composite Pyramid Synthesis

When multiple parallel subagents each produce their own artifact pyramid (one per research dimension), the orchestrator synthesizes them into a single **composite pyramid** organized by **opportunity/entity** rather than by **source agent**.

## When to Use This Pattern

Any parallel research pipeline where 2+ subagents investigate independent dimensions and their findings need to be merged into a unified view. Examples:
- Jobs Finder: 4 researchers (ATS, exec search, aggregators, company pages) → 1 consolidated opportunity pyramid
- Competitive analysis: market sizing + technical feasibility + competitive landscape → 1 merged pyramid
- Due diligence: financial + technical + legal + operational → 1 deal pyramid

## The Problem With Leaving Sub-Pyramids In Place

Each subagent pyramid is organized by what that agent discovered. When a downstream orchestrator or scoring agent needs to evaluate, say, "Komodo Health," it must:
1. Read R1's pyramid to see the Greenhouse listing
2. Read R3's pyramid to see if Built In also found it
3. Cross-reference mentally whether both sources refer to the same opportunity

This defeats the purpose of progressive disclosure. The composite pyramid reorganizes the data so one `02-analysis/komodo-health.md` file contains everything from all sources.

## Synthesis Protocol

### Step 1: Cross-Reference All Candidates

Read the L1 summary from each sub-pyramid. Build a master list of every unique candidate identified as `company|role`. Note which sub-pyramids found each one.

### Step 2: Build the Composite Pyramid

```
<project-root>/
├── 00-index.md              ← Entry point with cross-dedup summary
├── 01-summary/
│   └── findings.md          ← L1: merged findings with triage
├── 02-analysis/             ← L2: one file per OPPORTUNITY
│   ├── komodo-health.md
│   ├── picnichealth.md
│   ├── mie-cto.md
│   └── ...
└── 03-dossiers/
    ├── dedup-log.md          ← Cross-result dedup audit trail
    └── sub-pyramids-archive.md  ← What was absorbed and from where
```

The critical difference from a single-agent pyramid: L2 files are named after **opportunities** (companies + roles), not after **research dimensions**. A downstream agent reads `02-analysis/komodo-health.md` and gets everything — regardless of whether R1 or R3 found it.

### Step 3: Cross-Result Dedup

For each candidate, check whether it appeared in multiple sub-pyramids. If the same `company|role` was found by R1 (Greenhouse) and R4 (career page), collapse to a single entry. Document the collision in `03-dossiers/dedup-log.md`:

```markdown
| Company | Role | Found By | Also Found By | Verdict |
|---------|------|----------|---------------|---------|
| Veeva Systems | VP Engineering | R3 (Built In) | R4 (career page) | Already in dedup set — no collision |
| Komodo Health | VP AI Engineering | R1 (Greenhouse) | — | Unique to R1 |
```

### Step 4: Remove Sub-Pyramids

After the composite pyramid is verified complete:
1. Confirm all candidates from all sub-pyramids are represented in the composite
2. Delete the individual sub-pyramid directories
3. Update the `03-dossiers/sub-pyramids-archive.md` to document what was removed
4. Fix all SOURCES sections in the composite that referenced the old sub-pyramid paths

### Step 5: Fix SOURCES Navigation

After removal, update every SOURCES section that pointed to a deleted sub-pyramid. Replace researcher-specific `../researcher-1/00-index.md` references with a pointer to `03-dossiers/sub-pyramids-archive.md`.

## Worked Example

See the June 1 2026 jobs-finder session (companion-session-summary.md), where this pattern was developed and applied across 4 researcher pyramids producing 11 consolidated opportunities.
