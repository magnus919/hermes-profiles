# Chief of Staff — Hermes Profile

Chief of Staff specialization for Hermes Agent. Amplifies a leader's capacity by
managing information flow, calendar, decision pipeline, and cross-functional
coordination. The CoS doesn't own a domain — they own the leader's effectiveness
across all domains.

## What This Profile Provides

- **Gatekeeping & Triage** — filters what reaches the leader, routes decisions to the right level, resolves what doesn't need leader attention
- **Executive Briefing** — one-page decision memos, morning briefs, weekly summaries, board prep materials
- **Meeting & Calendar Triage** — strategic calendar design, meeting audit and classification, preparation standards
- **Force Multiplication** — attention leverage, decision velocity, organizational glue, strategic horizon management
- **Organizational Sensing** — mood tracking, political dynamics detection, team health monitoring, honest broker function
- **Institutional Memory** — decision logs, commitment tracking, relationship maps, knowledge archives, memory transfer protocols

## Installation

```bash
git clone https://github.com/magnus919/hermes-profiles.git ~/hermes-profiles
ln -s ~/hermes-profiles/profiles/chief-of-staff ~/.hermes/profiles/
hermes --profile chief-of-staff
```

## Quick Start

Once the profile is loaded, give it a task:

> "I'm the CEO of a 200-person company. I'm drowning in meetings, decisions are
> piling up, and I can't tell whether the organization is healthy or just quiet.
> Help me design a CoS function that would make me more effective."

The profile will:
1. Audit the current state of the leader's capacity, calendar, and information flow
2. Design a triage system for what reaches the leader
3. Create briefing templates (decision memo, morning brief, weekly brief)
4. Design organizational sensing mechanisms
5. Build an institutional memory system
6. Output an artifact pyramid at the engagement path

## Skill Dependencies

| Skill | Provides | Load Command |
|-------|----------|--------------|
| `artifact-pyramids` | Three-layer progressive disclosure output format | `skill_view('artifact-pyramids')` |
| `executive-methodology` | Decision frameworks, stakeholder communication, governance | `skill_view('executive-methodology')` |
| `chief-of-staff-methodology` | Gatekeeping, briefing, force multiplication, sensing, memory, calendar triage | `skill_view('chief-of-staff-methodology')` |
| `orchestration-methodology` (recommended) | Multi-agent coordination patterns | `skill_view('orchestration-methodology')` |
| `org-design` (recommended) | Organizational structure, team topology, decision rights | `skill_view('org-design')` |
| `operational-design` (recommended) | Process design, workflows, scale patterns | `skill_view('operational-design')` |

### Supporting References

| Reference | File |
|-----------|------|
| Gatekeeping & Triage | `skill_view('chief-of-staff-methodology', 'references/gatekeeping-and-triage.md')` |
| Executive Briefing | `skill_view('chief-of-staff-methodology', 'references/executive-briefing.md')` |
| Force Multiplication | `skill_view('chief-of-staff-methodology', 'references/force-multiplication.md')` |
| Organizational Sensing | `skill_view('chief-of-staff-methodology', 'references/organizational-sensing.md')` |
| Institutional Memory | `skill_view('chief-of-staff-methodology', 'references/institutional-memory.md')` |
| Meeting & Calendar Triage | `skill_view('chief-of-staff-methodology', 'references/meeting-and-calendar-triage.md')` |
| Decision Frameworks | `skill_view('executive-methodology', 'references/decision-frameworks.md')` |
| Stakeholder Communication | `skill_view('executive-methodology', 'references/stakeholder-communication.md')` |
| Governance | `skill_view('executive-methodology', 'references/governance.md')` |

## Output Format

All output follows the artifact pyramid convention. The response to any caller is the
absolute path to `00-index.md`.

## Verification

- [ ] Accepts a capacity management or organizational design prompt and produces an artifact pyramid
- [ ] Pyramid contains gatekeeping/triage design, briefing templates, and coordination frameworks
- [ ] Organizational sensing mechanisms are documented with signals, meanings, and actions
- [ ] Institutional memory systems include decision logs, commitment trackers, and transfer protocols
- [ ] Response is the absolute path to `00-index.md`, not a summary
