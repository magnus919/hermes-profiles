# Chief of Staff Profile — Agent Guidance

This document is for AI agents that interact with or consume outputs from the
Chief of Staff Hermes profile.

## Trigger Patterns

Load this profile when the user asks for any of the following:

| User Says | What It Means |
|-----------|---------------|
| "I need a Chief of Staff" or "Design a CoS function for me" | Full engagement — capacity audit, triage design, briefing templates, memory systems |
| "Help me manage my calendar / meetings" | Calendar audit — meeting classification, time allocation analysis, triage framework |
| "I'm overwhelmed with information / decisions" | Gatekeeping design — triage stack, escalation paths, decision pipeline |
| "I need better briefs / decision memos" | Briefing design — memo templates, morning brief format, decision memo structure |
| "I need to know what's really happening in the org" | Organizational sensing — sensing mechanisms, signal detection, honest broker protocol |
| "I keep losing context / forgetting past decisions" | Institutional memory — decision log, commitment tracker, memory transfer |
| "I need to coordinate across teams / departments" | Cross-functional coordination — dependency mapping, handoff protocols, decision rights |
| "Prepare me for a board meeting / investor meeting" | Board prep — deck structure, Q&A preparation, stakeholder briefing |
| "I need to delegate better" | Delegation design — decision rights, escalation paths, proxy protocols |

## Loading Order

When starting a CoS engagement, load skills in this sequence:

```python
skill_view('artifact-pyramids')                       # 1. Output format specification
skill_view('executive-methodology')                    # 2. Executive frameworks (decision frameworks, stakeholder communication)
skill_view('chief-of-staff-methodology')               # 3. CoS-specific methodology index
# Then load specific references based on the engagement type:
skill_view('chief-of-staff-methodology', file_path='references/gatekeeping-and-triage.md')
skill_view('chief-of-staff-methodology', file_path='references/executive-briefing.md')
skill_view('chief-of-staff-methodology', file_path='references/force-multiplication.md')
skill_view('chief-of-staff-methodology', file_path='references/organizational-sensing.md')
skill_view('chief-of-staff-methodology', file_path='references/institutional-memory.md')
skill_view('chief-of-staff-methodology', file_path='references/meeting-and-calendar-triage.md')
```

## Output Contract

The profile produces CoS artifacts as an artifact pyramid. The response to the
caller is always the **absolute path to `00-index.md`** at the pyramid root.
Not a summary. Not a natural-language handoff.

### Expected Structure

```
<engagement>/
├── 00-index.md                        ← Navigation index with SOURCES
├── 01-summary/
│   ├── capacity-assessment.md        ← Leader effectiveness audit and recommendations
│   └── cos-system-design.md          ← Overall CoS function architecture
├── 02-analysis/
│   ├── gatekeeping-and-triage.md    ← Triage stack, escalation paths, filter design
│   ├── calendar-audit.md            ← Time allocation analysis, meeting classification
│   ├── briefing-templates.md        ← Decision memo, morning brief, weekly brief templates
│   ├── organizational-sensing.md    ← Sensing mechanisms, signal definitions
│   └── institutional-memory.md      ← Memory systems, decision logs, transfer protocols
└── 03-dossiers/
    ├── frameworks/                   ← Decision frameworks, RAPID/DACI templates
    ├── templates/                    ← Briefing templates, memo formats
    └── reference-materials.md       ← Supporting research, examples, edge cases
```

### Cross-Reference Rules

1. **Every recommendation in L1 is grounded in analysis from L2** — summary decisions link to detailed frameworks
2. **Gatekeeping designs include escalation rules** with clear criteria for each tier
3. **Calendar audits include time allocation targets** with current vs. desired state
4. **Organizational sensing mechanisms include signal definitions** — what to look for, what it means, what to do
5. **Institutional memory systems include transfer protocols** — how memory survives when the CoS or leader changes
6. **SOURCES sections at every layer** — absolute paths with descriptions

## Handoff Protocol

1. **The pyramid IS the handoff.** Close with the path. Do not summarize.
2. **Triage designs include escalation rules** — clear criteria for what reaches the leader, what gets routed, what gets resolved.
3. **Briefing templates are ready to use** — formats are filled with examples, not left as blanks.
4. **Output feeds into operational-design and org-design** profiles for implementation.

## Related Profiles

- **CEO** — primary stakeholder; receives triaged information and strategic support
- **CTO** — coordinates on technology decisions affecting the broader organization
- **CFO** — coordinates on resource allocation and budget decisions
- **COO** — coordinates on operational execution and cross-functional workflows
- **CHRO** — coordinates on organizational health and talent decisions
- **product-manager** — receives product context for leadership alignment
- **orchestrator** — partners on multi-agent coordination
