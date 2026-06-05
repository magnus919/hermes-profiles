# Bootstrapping ADR Conventions in a New Project

A repeatable workflow for establishing Architecture Decision Records in a codebase that doesn't have them yet.

## Quick Checklist

- [ ] Choose a template (default: MADR)
- [ ] Decide directory location (default: `docs/adr/`)
- [ ] Write a README index (`docs/adr/README.md`)
- [ ] Document conventions in `CONTRIBUTING.md`
- [ ] Document ADR location in `AGENTS.md` (AI agents need to know where to look)
- [ ] Add `.hermes/` to `.gitignore` if it doesn't exist
- [ ] Create initial batch of ADRs for the design decisions already made
- [ ] File as a single PR: issue → branch → ADRs + docs → PR

## Step-by-Step

### 1. Choose a Template

| When | Template | Sections |
|------|----------|----------|
| Quick decision, single rationale | **Nygard** | Status, Context, Decision, Consequences |
| Multi-option trade-off analysis | **MADR** (default) | Status, Deciders, Date, Context, Decision Drivers, Considered Options, Outcome, Links |
| High-stakes / regulatory | **Tyree & Akerman** | 12 sections (Issue, Positions, Argument, Implications, etc.) |
| Vendor / procurement | **Business Case** | Evaluation criteria, cost/SWOT analysis |
| QA / NFR focused | **Planguage** | Tag, Gist, Priority, Stakeholders, Risks |

### 2. Set Directory Convention

```text
docs/
└── adr/
    ├── README.md          # Index table with statuses + links
    ├── 0001-title.md      # First ADR
    ├── 0002-title.md
    └── ...
```

**Naming convention:**
- `NNNN-title-with-dashes.md` — sequential zero-padded numbers, imperative verb phrase
- Status lives in the document header (`Status: accepted`), never in the filename
- Extension: `.md` for easy rendering

**Directory naming note:** Some teams prefer `decisions/` over `adr/` for plain-language accessibility. The ADR template format works identically with either name.

### 3. Write the README Index

The index serves as the entry point for anyone (including AI agents) exploring the decision log. Include:

- Brief explanation of what ADRs are and the convention
- Full table: ADR number, title, status
- Link back to `CONTRIBUTING.md` for the ADR workflow

See `docs/adr/README.md` in the GroktoCrawl repo (`groktopus/groktocrawl`) for a worked example.

### 4. Document in CONTRIBUTING.md

Add a section covering:

- **Convention:** file naming, statuses, immutability
- **When to write an ADR:** new integration/service, changing existing pattern, choosing between significant alternatives, decisions a future contributor would want the "why" on
- **Workflow:** create ADR with next number → include in PR → on acceptance update the index

### 5. Document in AGENTS.md

AI agents need a single sentence pointing them to the ADR directory:

```markdown
Architecture Decision Records (ADRs) live in `docs/adr/` and capture the context
and rationale behind significant design choices. Always check the ADR index at
`docs/adr/README.md` before making architectural changes — existing ADRs may
document constraints or rejected alternatives that inform your approach.
```

### 6. Issue-First PR Workflow

1. File an issue documenting the adapter/architecture design (L1 summary + L2 key decisions)
2. Branch from main with a descriptive name (`feat/adapter-architecture`)
3. Create ADR files using the MADR template
4. Document convention in `CONTRIBUTING.md`
5. Add agent reference in `AGENTS.md`
6. Add `.hermes/` to `.gitignore` if missing (local dev artifacts should not be committed)
7. Commit with `Signed-off-by` (DCO) and `Refs: #NNN` in the commit body
8. Push and open PR referencing the issue (`Closes #NNN`)

## ADR Lifecycle (for ongoing use)

```text
proposed → accepted → [deprecated | superseded by ADR-NNNN | rejected]
```

- **Immutable rule:** Existing ADRs are never edited after acceptance. To change a decision, write a new ADR and update the old one's status.
- **Linking:** Every ADR's Links section should reference related ADRs with semantic link types: `Refined by`, `Supersedes`, `Defined by`, `Contradicts`.
- **Retired numbers:** Never reuse an ADR number — if rejected, leave the number retired in the index with status `rejected`.

## Worked Example

The GroktoCrawl adapter architecture PR at `groktopus/groktocrawl#89` demonstrates this full workflow:
- 9 ADRs using the MADR template covering the adapter registry pattern
- README index with status table
- CONTRIBUTING.md update with ADR convention section
- AGENTS.md update with ADR reference
