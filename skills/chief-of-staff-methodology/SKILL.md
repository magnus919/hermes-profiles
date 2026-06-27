---
name: chief-of-staff-methodology
description: >-
  The craft of being a Chief of Staff — gatekeeping, force multiplication,
  executive briefing, organizational sensing, institutional memory, and
  meeting/calendar triage. Provides the frameworks and templates that make an
  executive more effective by managing their capacity, information flow, and
  decision surface.
version: 0.1.0
author: Hermes Agent community
license: MIT
metadata:
  hermes:
    tags:
      [executive, chief-of-staff, gatekeeping, coordination, leadership]
---

# Chief of Staff Methodology

The Chief of Staff is an amplifier. They don't own a domain — they own the leader's
capacity to operate across all domains. This skill provides the operational craft:
how to triage, brief, coordinate, sense, and remember so the leader can lead.

## When to Load

Load this skill when the task involves:

- Triaging information flow to an executive — what reaches them, in what form, at what latency
- Preparing executive briefs, decision memos, or board materials
- Managing an executive's calendar, meeting load, and attention allocation
- Coordinating across multiple teams or departments on behalf of a leader
- Building and maintaining institutional memory across turnover or discontinuity
- Sensing organizational mood, political dynamics, and team health
- Designing the systems that make the leader more effective (capacity multiplication)
- Creating or auditing escalation paths, decision rights, and delegation rules

## Loading Order

```
skill_view('artifact-pyramids')                          # Output contract
skill_view('chief-of-staff-methodology')                 # This — methodology index
skill_view('executive-methodology')                      # Decision frameworks, stakeholder communication
skill_view('chief-of-staff-methodology', file_path='references/gatekeeping-and-triage.md')
skill_view('chief-of-staff-methodology', file_path='references/executive-briefing.md')
skill_view('chief-of-staff-methodology', file_path='references/force-multiplication.md')
skill_view('chief-of-staff-methodology', file_path='references/organizational-sensing.md')
skill_view('chief-of-staff-methodology', file_path='references/institutional-memory.md')
skill_view('chief-of-staff-methodology', file_path='references/meeting-and-calendar-triage.md')
```

## Reference Files

| Reference | Load When | File |
|-----------|-----------|------|
| Gatekeeping & Triage | You need to manage what reaches the leader — filtering, prioritization, escalation rules | `references/gatekeeping-and-triage.md` |
| Executive Briefing | You're preparing a memo, brief, or board deck for an executive | `references/executive-briefing.md` |
| Force Multiplication | You're designing systems that make the leader more effective | `references/force-multiplication.md` |
| Organizational Sensing | You need to read organizational mood, team health, and political dynamics | `references/organizational-sensing.md` |
| Institutional Memory | You're building continuity across leadership transitions or session boundaries | `references/institutional-memory.md` |
| Meeting & Calendar Triage | You're managing an executive's calendar, prepping for meetings, or auditing how time is spent | `references/meeting-and-calendar-triage.md` |

## Design Principles

1. **Visibility without ego.** The CoS sees everything and claims nothing. If the CoS is getting credit, something went wrong.
2. **The truth at the speed of trust.** The CoS costs the leader nothing in honesty and everything in filtering. Bad news must travel faster than good news.
3. **Capacity is the fundamental metric.** Not "did the CoS do good work" but "did the leader do better work because the CoS was there?"
4. **Proactive before reactive.** A great CoS surfaces what needs attention before it becomes a fire. The leader should rarely be surprised.
5. **Write in the leader's voice.** The CoS is a translation layer between the leader's intent and the organization's language. Every brief, memo, or email should sound like it came from the leader.
6. **The gate swings both ways.** Gatekeeping that creates organizational friction is failure. The CoS should make it easier for the right things to reach the leader, not harder for everything.
7. **Institutional memory is a designed system, not a natural side effect.** What the CoS remembers must survive across sessions, leaders, and reorganizations.

## Related Skills

- `executive-methodology` — shared decision frameworks, stakeholder communication, governance
- `artifact-pyramids` — output contract specification
- `orchestration-methodology` — coordination across multiple agents or teams
- `org-design` — organizational structure, team topology, decision rights
- `operational-design` — process design, workflows, scale patterns
