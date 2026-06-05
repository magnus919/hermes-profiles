# Flat Output to Artifact-Pyramid Migration

When converting existing flat-file outputs to artifact-pyramid format, follow this pattern. It has been applied to baseline caches (SkillOpt PR #23) and validation results (PR #29), with the same structure reused across both.

## The Pattern

Given an existing flat output directory like:

```
outputs/
├── item-1.json            ← item-level result
├── item-2.json
└── item-3.json
```

Convert to:

```
output-pyramid/epoch-<N>/
├── 00-index.md                    ← navigation + provenance only (no findings)
├── 01-summary/findings.md         ← L1: YAML frontmatter (aggregate metrics) + human summary
├── 02-analysis/
│   ├── category-a.md              ← L2: one file per meaningful category of items
│   └── category-b.md              ← L2: each with SOURCES linking to L3
└── 03-dossiers/
    ├── item-1.json                ← L3: original JSON files, schema unchanged
    ├── item-2.json
    └── item-3.json
```

## Rules

### L1 YAML Frontmatter
Machine-parseable via `json.loads()`. Contains aggregate metrics that downstream consumers need at a glance (counts, rates, averages). No nested objects that require recursive parsing — flat key-value pairs and lists of IDs only.

### L2 Analysis Files
One file per meaningful category of items (accepted vs rejected, success vs failure, by type). Each file:
- Lists every item in its category with a one-line summary per item
- Ends with a `## SOURCES (LAYER 3 NAVIGATION)` section that maps to individual L3 dossiers
- Paths in SOURCES are **relative** (e.g., `03-dossiers/item-1.json`) for portability

### L3 Dossiers
The original flat JSON files, schema unchanged. Copied (not symlinked) so the pyramid is self-contained. Copy via `shutil.copy2` to preserve metadata.

### 00-index.md
Navigation + provenance only. No findings, no verdicts, no scores. Per the output-classification-framework reference: "00-index.md exists only to get the consumer to the right layer file."

## Downstream Consumer Changes

When a downstream process previously read the flat files, add a pyramid-aware read path:

```python
# Try pyramid first, fall back to flat glob
pyramid_index = os.path.join(state_dir, "output-pyramid", f"epoch-{epoch}", "00-index.md")
if os.path.exists(pyramid_index):
    summary_path = os.path.join(os.path.dirname(pyramid_index), "01-summary", "findings.md")
    meta = json.loads(open(summary_path).read().split("---", 2)[1])
    item_ids = [e["id"] for e in meta.get("items", [])]
    dossier_dir = os.path.join(os.path.dirname(pyramid_index), "03-dossiers")
    result_files = sorted(os.path.join(dossier_dir, f"{eid}.json") for eid in item_ids)
else:
    result_files = sorted(glob.glob(os.path.join(flat_dir, "*.json")))
```

## When to Use

- You have existing flat JSON outputs that are consumed by downstream processes
- The items naturally fall into categories (accepted/rejected, pass/fail, by type)
- A human or agent needs to scan aggregate results without loading every item
- You want backward compatibility during the transition (flat files still written, pyramid is additive)
