# Executive Briefing

The Chief of Staff is the translation layer between raw organizational data and
the leader's decision-ready understanding. A well-crafted brief compresses
complexity without losing signal, respects the leader's time, and makes decisions
obvious.

## The Golden Rule of Briefing

> A brief is not a document. It is a **decision enabler**. If the leader finishes
> reading and doesn't know what to do, the brief failed.

## The One-Page Decision Memo

The default format for Tier 2 items. It fits on one page, front only. If it
runs to two pages, the CoS hasn't done enough work.

| Section | Content | Target Length |
|---------|---------|---------------|
| **Subject** | Clear, specific, decision-focused | One line |
| **Situation** | What happened / what changed / what is being proposed | 2-3 sentences |
| **Context** | Relevant background the leader needs to evaluate the decision | 2-3 sentences |
| **Options** | 2-3 viable paths, each with pros, cons, and risk assessment | 1-2 sentences each |
| **Recommendation** | Which option and why — this is where the CoS adds value | 1-2 sentences |
| **Resource Impact** | Cost, headcount, time, dependencies | 1 sentence |
| **Decision Required** | Exactly what the leader needs to decide — yes/no, choose A/B/C, approve/reject | 1 clear sentence |
| **Next Steps** | What happens after the decision, who does it | 1-2 sentences |

### Example

> **Subject:** Approve AWS Reserved Instance commitment — $240K annual savings
>
> **Situation:** Our current on-demand EC2 spend is forecast at $1.2M for FY26. By
> committing to a 1-year reserved instance for our baseline compute (60% of total),
> we can reduce that by $240K.
>
> **Context:** Engineering validated that our baseline workload — 120 instances across
> production and staging — has been stable for 12 months. The reserved instance
> requires a 1-year commitment with no early termination. If we need to scale down,
> we can sell unused capacity on the AWS marketplace.
>
> **Options:**
> - **A:** 1-year reserved — $960K ($240K savings), lowest risk for stable workload
> - **B:** 3-year reserved — $840K ($360K savings), higher risk, better savings
> - **C:** Stay on-demand — $1.2M, maximum flexibility, minimum savings
>
> **Recommendation:** Option A — the 12-month stability track record gives us confidence
> in the commitment, and the savings ($240K) is material without over-committing.
>
> **Resource Impact:** $960K upfront (recouped in 12 months vs. on-demand). Finance
> confirmed budget availability.
>
> **Decision Required:** Approve option A (1-year reserved instance commitment).
>
> **Next Steps:** If approved, procurement will execute the commitment within 48 hours.

## The Morning Brief

A daily Tier 1 format. The leader's first-read of the day. Everything they need to
know but don't need to decide on (yet).

| Section | Content | Length |
|---------|---------|--------|
| Overnight | Anything that happened since end of day yesterday | 3-5 bullets |
| Today's agenda | Key meetings, decisions expected, who's presenting | 5-8 bullets |
| Watch list | Issues trending toward needing attention | 2-3 bullets |
| FYI | Information the leader should be aware of | 2-3 bullets |

The morning brief is **informational**. If it needs a decision, it's a memo, not a brief.

## The Weekly Brief

A broader view. What happened this week, what's coming next week, and what needs
attention in the medium term.

| Section | Content |
|---------|---------|
| Executive Summary | The 3-5 things the leader must know from this week |
| Decisions Made | What the leader decided and what happened as a result |
| Decisions Pending | What's waiting for the leader's attention (with links to memos) |
| Metrics Dashboard | Key operational metrics — green/yellow/red status |
| Team Pulse | Quick temperature check on each direct report's area |
| Next Week Preview | Major meetings, deadlines, decisions expected |
| Strategic Items | Longer-term issues the leader should start thinking about |

## Writing in the Leader's Voice

The CoS briefs are read as if the leader wrote them. This means:

- **The same vocabulary.** If the leader says "surface" not "raise," the brief says "surface."
- **The same level of formality.** If the leader is direct, the brief is direct. If the leader prefers context, the brief provides context.
- **The same priorities.** What the leader cares about gets more space. What the leader doesn't care about gets less (or doesn't appear).
- **No CoS-isms.** The brief doesn't say "I think" or "I recommend" — it says "The recommendation is" or says nothing and lets the options speak.

## Bad News Protocol

Bad news travels faster than good news. The CoS delivers bad news immediately,
completely, and without softening.

**Format for bad news:**
1. **What happened** — directly, no preamble
2. **What has been done** — the immediate response, containment, investigation
3. **What is needed** — decision, resources, communication, escalation
4. **What caused it** — root cause analysis (later, after the immediate response)

**Never lead with:**
- "I have some news..."
- "Before I tell you this..."
- "Let me give you some context first..."

**Lead with:**
- "We lost the [customer] deal."
- "[Service] is down. Here's what we've done so far..."
- "[Team member] has resigned effective immediately."

## Common Briefing Mistakes

| Mistake | Signal | Fix |
|---------|--------|-----|
| Buried lede | The key decision is at the bottom of a long memo | Lead with the decision. Context comes after. |
| False options | One option is clearly right, two are clearly wrong | Do more work. If there's only one real option, say so. |
| Analysis paralysis | The memo explains everything but recommends nothing | The recommendation IS the CoS's job. Make the call. |
| Defensive framing | Options are presented to avoid blame if the decision goes wrong | Own the recommendation. If it's wrong, fix it. |
| Missing context | The leader has to ask "what about X?" | Anticipate the 3 most likely questions and answer them before they're asked. |
