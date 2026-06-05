# SRE Communication Guide

> A comprehensive reference for Site Reliability Engineering communication patterns, templates, and best practices.
> Target audience: SREs, incident commanders, reliability engineers, and engineering leaders.

---

## Table of Contents

1. [Foundations of SRE Communication](#1-foundations-of-sre-communication)
2. [Incident Communication](#2-incident-communication)
3. [Postmortem Communication](#3-postmortem-communication)
4. [Influencing Without Authority](#4-influencing-without-authority)
5. [On-Call Handoff Protocol](#5-on-call-handoff-protocol)
6. [Cross-Team Coordination](#6-cross-team-coordination)
7. [Escalation Communication](#7-escalation-communication)
8. [Metrics-Based Reporting to Leadership](#8-metrics-based-reporting-to-leadership)
9. [Writing Style Guide](#9-writing-style-guide)
10. [Templates](#10-templates)

---

## 1. Foundations of SRE Communication

SRE communication differs from general engineering communication in several critical ways. SREs operate in high-stakes, time-sensitive environments where clarity, brevity, and precision are paramount. Every message — whether an incident update, a postmortem, or a reliability proposal — carries operational weight.

### 1.1 Core Principles

| Principle | Description | Why It Matters |
|-----------|-------------|----------------|
| **Clarity over completeness** | Prioritize clear, unambiguous statements over exhaustive detail. | During incidents, ambiguity costs time. Teams act on what they understand. |
| **Evidence-based claims** | Every assertion about system behavior must trace back to observable data. | Prevents speculation-driven decisions that compound outages. |
| **Bias for action** | Communicate what is being done and what is needed, not just what is wrong. | Stakeholders need to know the response plan, not just the problem description. |
| **No-blame framing** | Describe system behavior in terms of conditions and events, not people or teams. | Psychological safety enables blameless postmortems and honest reporting. |
| **Audience awareness** | Tailor depth, frequency, and format to the consumer of the information. | Executives need impact and ETA; engineers need root cause and reproduction steps. |
| **Timeliness** | Communicate proactively at defined intervals, never let stakeholders wonder. | Silence erodes trust faster than bad news delivered promptly. |

### 1.2 Communication Channels by Urgency

| Urgency | Channel | Format | Examples |
|---------|---------|--------|----------|
| P0/P1 (Critical) | Pager/Phone + Incident Channel | Real-time updates | Outage in progress, data loss detected |
| P2 (High) | Chat + Ticketing | Structured thread | Degraded performance, partial failure |
| P3 (Medium) | Ticketing + Email | Detailed report | Non-critical bug, minor latency regression |
| P4 (Low) | Email / Documentation | Asynchronous write-up | Technical debt tracking, minor improvements |

---

## 2. Incident Communication

Incident communication is the most time-sensitive form of SRE communication. The goal is to keep stakeholders informed without distracting the responders actively troubleshooting.

### 2.1 Incident Status Updates

Status updates follow a predictable rhythm and structure. Updates should be posted:

- **Initial notification**: Within 5 minutes of declaration
- **Regular cadence**: Every 30 minutes for P0, every 60 minutes for P1
- **On any significant change**: Mitigation started, root cause identified, service restored
- **Resolution**: When the incident is declared resolved
- **Follow-up**: When the postmortem is scheduled and shared

**Structure of a Status Update:**

```
[INCIDENT-ID] Status Update [#N]

Severity: [P0/P1/P2]
Service:  [Affected service(s)]
Duration: [Elapsed time since declaration]

Current Status: [Investigating / Mitigating / Monitoring / Resolved]

Impact:
- [Metric] affected: [X]% of users / [Y] requests lost
- [Observable symptom]

Actions Taken:
- [What has been done so far]

Next Steps:
- [What is being attempted next]

ETA / Confidence:
- [Estimated time to resolution or "Unknown"]
- [Low / Medium / High confidence in ETA]

Handoff / Needs:
- [Is a handoff coming?]
- [Does anyone need to be paged?]

Posted by: [Name]
```

### 2.2 Executive Summaries

Executive summaries are concise, non-technical overviews aimed at leadership who need to understand business impact, timeline, and follow-up — not technical details.

**Structure of an Executive Summary:**

```
INCIDENT EXECUTIVE SUMMARY

Incident: [Brief one-line title, e.g., "Payment Processing Outage"]
Date:     [YYYY-MM-DD]
Duration: [Total time from declaration to resolution]
Severity: [P0/P1]

What Happened:
[3-4 sentences describing the user-facing impact and the technical
root cause at a business-readable level. Avoid jargon.]

Business Impact:
- Users affected: [X] (approximately [Y]%)
- Revenue impact: [Estimated $ amount or "None"]
- SLA impact: [Met / Missed — by how much]
- Customer-facing symptoms: [e.g., "Users could not complete purchases"]

Timeline (key events):
- [HH:MM UTC] Incident declared
- [HH:MM UTC] Mitigation started
- [HH:MM UTC] Service restored
- [HH:MM UTC] Incident declared resolved

Root Cause (one sentence):
[A single sentence explaining the technical root cause.]

Remediation Actions:
- Short-term: [What was done to restore service]
- Long-term: [What will prevent recurrence]

Prepared by: [Name]
Date: [YYYY-MM-DD]
```

### 2.3 Timeline Reconstruction

An accurate incident timeline is the backbone of any postmortem and is critical for understanding what happened, when, and why. During the incident, the incident commander (IC) or a dedicated scribe logs key events.

**Timeline Log Format:**

| Time (UTC) | Event | Source | Evidence |
|------------|-------|--------|----------|
| 14:02:15 | Alert fired: p99 latency > 500ms on `payment-service` | Datadog Monitor | Alert ID #8421 |
| 14:02:45 | On-call SRE acknowledged page | PagerDuty | Ack by @jsmith |
| 14:04:30 | Incident declared (P1) | Slack #incidents | Declaration message |
| 14:07:00 | Initial stakeholder notification sent | Slack #leadership-alerts | Message link |
| 14:12:00 | Mitigation: rolled back deploy v2.3.1 → v2.3.0 | Kubernetes | Rollout log |
| 14:18:00 | p99 latency returning to baseline | Datadog Dashboard | Graph link |
| 14:22:00 | Incident declared resolved | Slack #incidents | Resolution message |

**Timeline Best Practices:**

- Log timestamps in **UTC only** to avoid timezone confusion.
- Record events as they happen, not from memory after the fact.
- Include **negative signals** too ("14:10:00 — Rollback not yet complete, no change in error rates").
- Link to dashboards, alert IDs, deploy logs, and commit SHAs as evidence.
- Distinguish between **observations** ("alert fired"), **actions** ("rolled back deploy"), and **decisions** ("escalated to database team").

### 2.4 Incident Communication Roles

| Role | Communication Responsibilities |
|------|-------------------------------|
| **Incident Commander (IC)** | Owns all external communication; decides severity, cadence, and escalation. The single source of truth. |
| **Scribe / Deputy IC** | Logs timeline events; drafts status updates for IC approval; tracks action items. |
| **Subject Matter Expert (SME)** | Provides technical status to IC only; does NOT communicate externally. |
| **Stakeholder Liaison** | (If designated) Handles executive/support communication to keep IC focused on mitigation. |

---

## 3. Postmortem Communication

Postmortems are the primary vehicle for organizational learning from incidents. The quality of the postmortem directly determines whether the lessons are absorbed and acted upon.

### 3.1 Writing Clearly

**Postmortem Structure:**

```
# Postmortem: [INCIDENT-ID] — [Descriptive Title]

## Summary
[3-5 sentences: what happened, impact, how long, root cause category]

## Impact
| Metric | Value |
|--------|-------|
| Severity | [P0/P1/P2] |
| Duration | [X minutes/hours] |
| Users Affected | [X] (approximate) |
| Error Rate | [X]% |
| SLO Impact | [Met / Missed] |
| Revenue Impact | [$X or N/A] |

## Timeline
| Time (UTC) | Event |
|------------|-------|
| [T-0] | [First signal (alert, user report, etc.)] |
| [T+X] | [Key events in chronological order] |
| [T+Y] | [Mitigation started] |
| [T+Z] | [Service restored] |

## Root Cause Analysis
- **Trigger**: The specific condition that initiated the failure
- **Contributing Factors**: Conditions that amplified the impact or delayed detection
- **Why it wasn't caught earlier**: Gaps in monitoring, testing, or processes

## Detection
- How was the incident first detected? (Alert / User report / Proactive)
- Time from first failure to first notification:
- Could detection have been faster? [Yes/No — if yes, how?]

## Response
- Time to acknowledge:
- Time to mitigation:
- What went well in the response:
- What could have gone better:

## Action Items
| # | Action | Owner | Ticket | Due |
|---|--------|-------|--------|-----|
| 1 | Add alert for metric X | [Owner] | [Link] | [Date] |
| 2 | Add runbook for scenario Y | [Owner] | [Link] | [Date] |
| 3 | [Etc.] | | | |

## Prevention
- What specific changes prevent this exact failure from recurring?
- What systemic improvements reduce the class of failures this belongs to?

## Lessons Learned
- What did we learn about our system?
- What did we learn about our processes?
- What surprised us?

## Blameless Statement
*"The goal of this postmortem is to learn and improve our systems and processes.
No individual or team is blamed. We all operate within the constraints and information
available to us at the time."*
```

### 3.2 Action Items Ownership

Action items from postmortems must be treated as seriously as feature work. Each action item should be:

| Criterion | Description |
|-----------|-------------|
| **S.M.A.R.T.** | Specific, Measurable, Achievable, Relevant, Time-bound |
| **Assigned** | A named owner, not a team |
| **Tracked** | Linked to a ticket in the tracking system |
| **Classified** | Marked as "mitigation" (immediate) or "prevention" (systemic) |
| **Prioritized** | Labeled P0-P4 based on risk reduction |
| **Followed up** | Reviewed at regular reliability retrospectives |

### 3.3 Sharing Failures Constructively

The psychological safety of the team depends on how failures are shared and discussed.

**Do:**
- Start postmortem reviews with the blameless statement
- Discuss system conditions, not individual decisions
- Frame gaps as process opportunities, not personal failings
- Celebrate what was caught and what went well
- Share postmortems broadly (within reason) so other teams learn

**Don't:**
- Assign blame or use blame-implying language ("should have", "failed to", "mistake")
- Skip the "what went well" section — this is not just about failures
- Let action items languish without follow-up
- Use postmortems as performance review input

### 3.4 Postmortem Readability Guidelines

- Write for an audience that includes engineers who were not on-call
- Define acronyms on first use
- Use active voice ("The deploy caused X" not "X was caused by the deploy")
- Keep the summary to 3-5 sentences — busy engineers read this first
- Use concrete numbers, not ranges or estimates
- Link to supporting evidence (graphs, logs, commits)

---

## 4. Influencing Without Authority

SREs frequently need to drive reliability improvements across teams they do not manage. This requires influence grounded in data, respect, and relationship-building.

### 4.1 Data-Driven Proposals

When proposing reliability work to a product or feature team, data is your strongest tool.

**Anatomy of a Reliability Proposal:**

```
# Reliability Proposal: [Title]

## Problem Statement
[One paragraph describing the reliability risk, backed by data.]

## Evidence
- [Metric] over [timeframe]: [current value] vs [target] — [X]% deviation
- Incidents caused by this issue in last [N] months: [count]
- User-facing impact: [description with numbers]

## Proposed Solution
[What you propose to build or change, in engineering terms.]

## Expected Impact
- Reduction in p99 latency: [N]% (estimated)
- Incidents prevented per quarter: [N] (estimated)
- Engineering time saved per month: [N] hours

## Cost
- Engineering effort: [N] engineer-weeks
- Migration/rollout complexity: [Low / Medium / High]
- Risk of change: [Low / Medium / High]

## Alternatives Considered
| Option | Pros | Cons |
|--------|------|------|
| [Option A — proposed] | [List] | [List] |
| [Option B] | [List] | [List] |
| [Option C — do nothing] | [List] | [List] |

## Recommendation
[Clear recommendation with rationale. Frame in terms the team cares about:
faster feature velocity, fewer pages, better user experience, lower cost.]

Prepared by: [Name]
Date: [YYYY-MM-DD]
```

### 4.2 Building Buy-In

Influence without authority requires deliberate relationship-building:

| Strategy | Tactics |
|----------|---------|
| **Find shared goals** | Connect reliability work to the team's stated priorities (e.g., "This will reduce the number of pages that interrupt your sprint") |
| **Start small** | Propose a low-effort, high-impact change first to demonstrate value. You earn credibility from wins. |
| **Make it easy** | Provide code, configs, dashboards, and runbooks — don't just identify the problem. |
| **Speak their language** | Use the metrics the team already tracks. If they care about feature velocity, frame reliability work in terms of reducing rework and interruptions. |
| **Create visibility** | Build dashboards and reports that make the team's reliability transparent to *their* stakeholders. |
| **Credit generously** | Attribute wins to the team, not to SRE. Trust is built on shared success. |
| **Be persistent but patient** | Reliability improvements often compete with feature work. A proposal may need 3-5 touches before it's adopted. |

### 4.3 Reliability Culture Leadership

Building a reliability culture means embedding reliability thinking into how every team operates, not just the SRE team.

- **Champion error budgets**: Help teams understand their error budget and make data-driven decisions about when to release vs. when to invest in reliability.
- **Run reliability office hours**: Regular slots where teams can bring reliability questions, review dashboards, or get help with SLO design.
- **Share metrics broadly**: Make reliability data visible in places where teams already look — sprint reviews, all-hands, team dashboards.
- **Celebrate reliability wins**: Call out teams that improved their SLOs, reduced incident frequency, or shipped reliability improvements.
- **Lead by example**: The SRE team's own systems should be exemplars of reliability practices.

### 4.4 Handling Resistance

| Objection | Response |
|-----------|----------|
| "We don't have time for reliability work." | "Let's look at how much time incidents cost your team. Even a small investment in prevention can save multiples in firefighting." |
| "Our system is different — it doesn't need the same reliability." | "Let's define what 'good enough' looks like for your system and only invest to that bar." |
| "We'll fix it when it breaks." | "That's a valid approach for low-criticality systems. Let's classify this system's tier and set expectations accordingly." |
| "SRE is just saying we're doing it wrong." | "Our goal is to give you tools and data to make your own reliability decisions. The choice is yours." |

---

## 5. On-Call Handoff Protocol

Structured on-call handoffs prevent critical information from being lost between shifts and ensure continuity of incident response.

### 5.1 Standard Handoff Format

Handoffs should take no more than 10 minutes and cover a structured checklist:

```
# On-Call Handoff: [Date]

## Shift Context
- Shift starting: [Name] — [Date/Time]
- Shift ending:  [Name] — [Date/Time]

## Active Incidents
[Incident ID / None]
- Status: [Open / Monitoring / Resolved / Postmortem pending]
- Summary: [One-sentence status]
- Handoff notes: [What the incoming person needs to know]

## Ongoing Issues
- [Known non-incident issues, expected to degrade/require attention]
- [Bugs or flakiness being tracked]

## Scheduled Changes
| Change | Time | Owner | Risk | Rollback Plan |
|--------|------|-------|------|---------------|
| [Deploy X] | [UTC] | [Name] | [Low/Med/High] | [Yes/No — describe] |
| [Maintenance Y] | [UTC] | [Name] | [Low/Med/High] | [Yes/No] |

## Recent Deployments
- [Service] deployed [version] at [time] — [healthy / monitoring]
- [Service] rolled back [version] → [version] at [time] — reason: [X]

## Known Vulnerabilities / Risks
- [e.g., "Database master is at 80% disk — fill rate ~2%/day. Alert threshold at 85%. No action needed this shift unless rate accelerates."]
- [e.g., "Redis cluster has one failed node — repair scheduled for tomorrow. No data loss expected."]

## Runbook Updates
- [Any new or modified runbooks since last handoff]
- [Any common troubleshooting tips discovered this shift]

## Dashboard Links
- Primary monitoring dashboard: [link]
- Service health dashboard: [link]
- Recent incident dashboards: [links]

## Pages / Alerts This Shift
| Alert | Times Fired | Actions Taken |
|-------|-------------|---------------|
| [Alert name] | [N] | [Summary] |
| [Alert name] | [N] | [Summary] |

## Communication
- [Any ongoing stakeholder communication threads]
- [Any executive attention on specific issues]

## Checklist
- [ ] Handoff doc shared in on-call channel
- [ ] PagerDuty schedules verified for next shift
- [ ] Escalation path reviewed (if new to rotation)
- [ ] Critical runbooks reviewed
- [ ] Known-good rollback versions noted

Handoff completed by: [Outgoing SRE]
Handoff received by:  [Incoming SRE]
```

### 5.2 What to Communicate (and What Not To)

| Communicate | Do NOT Communicate |
|-------------|-------------------|
| Active incidents and their status | Exhaustive details of every non-critical alert |
| Ongoing known issues with workarounds | Long-standing technical debt with no active impact |
| Scheduled changes during the next shift | Changes that have already been completed safely |
| Alert patterns observed during the shift | Every single alert that fired (summarize instead) |
| Full-disk, near-capacity, or degraded resources | "Normal" operational state (assume baseline) |
| Stakeholder expectations or active comms threads | Personal opinions about team members or decisions |

### 5.3 Shadowing and Ramp-Up

When an SRE is new to the rotation, the handoff should include:

1. **First shift as shadow**: New SRE shadows the outgoing SRE for the full shift.
2. **First solo shift with backup**: New SRE takes the pager but the experienced SRE remains available for questions.
3. **Sign-off**: The experienced SRE confirms the new SRE is ready for independent rotation.

---

## 6. Cross-Team Coordination

SREs regularly coordinate with product, engineering, security, and support teams. Each relationship requires a tailored communication approach.

### 6.1 With Product Teams

| Situation | Communication Approach |
|-----------|----------------------|
| Reliability proposal | Frame in terms of user experience and feature velocity. Use error budgets to create shared vocabulary. |
| SLO negotiation | Present data on current performance, cost of improvement, and trade-offs. Let the product team decide the risk tolerance. |
| Incident affecting a feature | Communicate impact in user-facing terms. Provide ETA updates in product-relevant intervals. |
| Feature launch readiness | Run pre-launch reviews and present findings as a scorecard with clear pass/fail criteria. |

**Pre-Launch Readiness Scorecard:**

| Criterion | Status | Notes |
|-----------|--------|-------|
| SLO defined | ✅ / ❌ | Target values and measurement method agreed |
| Dashboards built | ✅ / ❌ | At least one dashboard covering the golden signals |
| Alerts configured | ✅ / ❌ | Pager-worthy alerts with runbooks |
| Load testing completed | ✅ / ❌ | Results within acceptable range |
| Error budget allocated | ✅ / ❌ | Error budget policy defined |
| Runbooks written | ✅ / ❌ | At minimum, incident response and rollback procedures |
| Rollback tested | ✅ / ❌ | Procedure confirmed working |
| Dependency map documented | ✅ / ❌ | All upstream/downstream dependencies identified |

### 6.2 With Engineering Teams

| Situation | Communication Approach |
|-----------|----------------------|
| Code review (reliability) | Focus on failure modes, retry logic, circuit breakers, and observability. Use concrete examples of past failures. |
| Architecture review | Ask "what happens when this fails?" for every component. Document failure modes and mitigations. |
| Incident retrospectives | Joint posture: "We all own the outcome." Share data before opinions. |
| Reliability training | Offer lunch & learns, dojo sessions, or paired incident response drills. |

### 6.3 With Security Teams

| Situation | Communication Approach |
|-----------|----------------------|
| Security incident coordination | SRE owns availability; Security owns confidentiality/integrity. Establish clear incident command boundaries. |
| Vulnerability disclosure | Provide blast radius analysis. Security communicates the vulnerability; SRE communicates the mitigation plan and timeline. |
| Disaster recovery testing | Coordinate with Security on access controls, key rotation, and credential management in DR scenarios. |
| Shared infrastructure | Establish clear escalation paths for when a reliability issue has security implications (and vice versa). |

**SRE-Security Coordination During Incidents:**

| Phase | SRE Leads On | Security Leads On |
|-------|-------------|-------------------|
| **Detection** | Monitoring/reliability signals | Security monitoring signals |
| **Triage** | Is this a reliability or security incident? | Is this an active threat or compliance issue? |
| **Response** | Service restoration, user communication | Containment, forensics, legal notification |
| **Recovery** | Service health verification | Post-incident security sweep |
| **Postmortem** | Timeline, impact, reliability fixes | Analysis of vulnerabilities, new controls |

### 6.4 With Customer Support / Triage Teams

- **Provide status templates**: Give the support team pre-approved incident communication templates they can use when customers ask.
- **One-way communication during incidents**: A designated person (or a status page) feeds information to support; support does not request updates during active response.
- **Post-incident follow-up**: Send a customer-facing summary (less technical than the internal postmortem) after every P0/P1 incident.

---

## 7. Escalation Communication

Escalation is not a failure — it is a structured process for getting the right resources and attention to a problem.

### 7.1 When to Escalate

| Condition | Escalate To | Method |
|-----------|-------------|--------|
| Incident exceeds 30 minutes without mitigation | IC escalates to SRE manager | Phone / Pager |
| Cross-team coordination needed | IC escalates to stakeholder liaison | Phone |
| Business-critical impact not communicated to executives | IC escalates to director+ | Phone then email |
| No clear mitigation path after 60 minutes | IC escalates to senior engineering | Phone / In-person |
| Multiple simultaneous incidents | IC escalates for additional IC support | Chat / Phone |

### 7.2 Escalation Message Template

```
# ESCALATION REQUEST

Incident: [INCIDENT-ID] — [Title]
Severity: [P0 / P1]
Elapsed Time: [X] minutes

Current Status: [Investigating / Mitigating / Stuck]

Issue:
[What is blocking resolution or why escalation is needed]
- We need [specific help / decision / resource]

Impact If Not Resolved:
- [X] additional minutes of downtime expected
- [Y] users affected
- [Z]% of error budget consumed

What We've Tried:
- [Action 1]
- [Action 2]

Requested:
- [Specific ask: e.g., "Authorization to fall back to degraded mode",
  "Database team to investigate replication lag"]

Requested by: [Name]
Time: [UTC]
```

### 7.3 Escalation Best Practices

- **Escalate early, not late**: It is better to escalate and then de-escalate than to wait until the situation is critical. A rule of thumb: if you're wondering whether to escalate, escalate.
- **Be specific about what you need**: "We need a DBA to review the query plan on the `orders` table" is actionable. "We need help" is not.
- **Stay in the loop**: After escalating, keep the escalator informed of progress. Do not hand off and disappear.
- **Respect the escalation path**: Follow the chain unless there is a reason to skip a level (document why).

---

## 8. Metrics-Based Reporting to Leadership

Leadership does not have time to dig through dashboards. Effective reporting distills complex operational data into actionable signals.

### 8.1 What Leadership Cares About

| Theme | Questions Leadership Asks | Metrics to Report |
|-------|--------------------------|-------------------|
| **Availability** | Are we meeting our commitments? | SLO attainment, uptime %, error budget remaining |
| **Velocity** | Is reliability blocking feature work? | Incident count, time spent responding vs. preventing |
| **Trend** | Are we getting better or worse? | Month-over-month trends in MTTR, MTBF, incident count |
| **Risk** | What could go wrong next? | Largest error budget consumers, known risks, overdue action items |
| **Cost** | Are we spending wisely? | Infrastructure cost per transaction, cost of reliability initiatives |

### 8.2 Weekly Reliability Summary

The weekly summary is the primary recurring report for engineering leadership.

```
# Weekly Reliability Summary: [YYYY-MM-DD] to [YYYY-MM-DD]

## At a Glance
| Metric | This Week | Previous Week | Trend | Target |
|--------|-----------|---------------|-------|--------|
| P0/P1 Incidents | [N] | [N] | ↑ ↓ → | [N] |
| MTTR (P0) | [X min] | [X min] | ↑ ↓ → | [X min] |
| MTBF | [X days] | [X days] | ↑ ↓ → | [X days] |
| Error Budget Burn Rate | [X]%/week | [X]%/week | ↑ ↓ → | [X]%/week |
| SLO Attainment (30d) | [X]% | [X]% | ↑ ↓ → | [X]% |

## Notable Incidents
- [INCIDENT-ID]: [Title] — [Duration], [Impact], [Root cause category]
  Action items: [N] open, [N] closed
- [INCIDENT-ID]: [Title] — [Duration], [Impact], [Root cause category]
  Action items: [N] open, [N] closed

## Reliability Wins
- [Team] improved [SLO/MTTR/etc] by [X]% through [initiative]
- [Capability] was rolled out: [description]
- [Improvement] prevented [N] potential incidents

## Risk Watchlist
| Risk | Likelihood | Impact | Owner | Status |
|------|------------|--------|-------|--------|
| [Description] | High/Med/Low | High/Med/Low | [Name] | Being addressed / Not yet started |
| [Description] | High/Med/Low | High/Med/Low | [Name] | Being addressed / Not yet started |

## Postmortem Action Items Summary
- Total open action items: [N]
- Overdue: [N] (list key ones)
- Completed this week: [N]

## Recommendation
[One or two specific, data-backed recommendations for leadership action.
E.g., "We recommend approving the database migration plan for Service X before
the holiday traffic peak. Current error budget burn rate will exhaust the quarter's
budget by [date] if not addressed."]
```

### 8.3 Monthly / Quarterly Business Review

For higher-level presentations, focus on narrative and trends:

- **The big story**: What one or two reliability trends defined this period?
- **Incident decomposition**: Group incidents by cause category (code change, configuration, infrastructure, external dependency, capacity, etc.)
- **Error budget report**: For each critical service, show remaining error budget and projected exhaustion date
- **ROI of reliability**: Show how investments in reliability (tooling, improvements, refactors) correlate with reduced incident count or duration
- **Ask**: What one or two decisions or resources does leadership need to provide to maintain or improve reliability

---

## 9. Writing Style Guide

Clear writing is a force multiplier in SRE. A status update, postmortem, or proposal that can be read and understood in 30 seconds saves time for every person who reads it.

### 9.1 General Principles

| Principle | Guideline | Bad Example | Good Example |
|-----------|-----------|-------------|--------------|
| **Be concise** | Use the fewest words that convey the needed information. | "At this point in time, we are currently in the process of investigating the issue which appears to be related to what seems like a database connection problem." | "Investigating a database connection pool exhaustion issue." |
| **Use active voice** | Subject performs the action. Avoid passive constructions. | "The deploy was rolled back by the on-call engineer after elevated error rates were observed." | "The on-call engineer rolled back the deploy after observing elevated error rates." |
| **Be specific** | Use concrete numbers and facts, not approximations or opinions. | "There were a lot of errors and most users were affected." | "Error rate peaked at 12.3% at 14:05 UTC; approximately 4,200 users (6.7%) encountered failures." |
| **Use plain language** | Avoid jargon, acronyms without definitions, and unnecessarily technical terms for non-technical audiences. | "The Envoy sidecar experienced a connection pool drain timeout due to excessive COW page faults from the kernel memory reclamation path." | "The proxy service ran out of available connections because the kernel was reclaiming memory used by connection buffers." |
| **Structure for scannability** | Use headings, bullet points, and tables. Put the most important information first. | A dense paragraph with key information buried in the middle. | An inverted pyramid: conclusion first, then supporting details, then background. |
| **One thought per sentence** | Short sentences are easier to parse under time pressure. | "We rolled back the deploy to version 2.3.0 and confirmed that error rates dropped from 8% to 0.2% within 3 minutes, though we're still monitoring latency to make sure it continues to trend down." | "We rolled back the deploy to version 2.3.0. Error rates dropped from 8% to 0.2% within 3 minutes. Latency is still returning to baseline — continuing to monitor." |

### 9.2 No-Blame Language Guide

| Instead of This | Use This |
|-----------------|----------|
| "The engineer failed to check the config before deploying." | "The configuration validation step did not catch the invalid parameter." |
| "The team should have caught this in code review." | "The code review checklist did not include this failure mode." |
| "Someone accidentally ran the wrong command." | "The runbook did not sufficiently distinguish between the production and staging commands." |
| "The developer made a mistake in the retry logic." | "The retry logic did not account for the case where the upstream returns a 429 status code." |
| "The alert was ignored." | "The alert was not actionable and was tuned out due to frequent false positives." |

### 9.3 Acronym and Abbreviation Rules

- **Define on first use**: "Mean Time to Repair (MTTR) improved by 20%."
- **Use consistently**: Once defined, use the acronym throughout the document.
- **Avoid unnecessary acronyms**: If you only use it once, spell it out.
- **Know your audience**: A postmortem for other SREs can use "SLO", "MTTR", "p99"; an executive summary should spell out or explain these.

### 9.4 Tense and Perspective

| Element | Recommendation |
|---------|---------------|
| **Postmortems** | Past tense (describing what happened) |
| **Incident updates** | Present tense / future tense (what is happening, what will happen) |
| **Proposals** | Present tense (problem exists) + future tense (proposed solution) |
| **Runbooks** | Imperative mood ("Run this command", "Check this metric") |
| **Status reports** | Present perfect ("We have mitigated") + present ("We are monitoring") |
| **First person** | Use "we" (organizational ownership), avoid "I" in incident updates unless attribution is needed |

---

## 10. Templates

### 10.1 Incident Status Update Template

```
INCIDENT STATUS UPDATE

===============================================================================
INCIDENT: [INCIDENT-ID]
SEVERITY: [P0 / P1 / P2]
SERVICE:  [Affected service names]
UPDATE #: [N]
===============================================================================

CURRENT STATUS: [Investigating / Mitigating / Monitoring / Resolved]

--- IMPACT ---

User-facing symptoms:
[2-3 sentences describing what users experienced]

Scope:
- [Metric] affected: [X]%
- Estimated users affected: [X]
- Error budget consumed: [X]%
- Revenue impact (estimated): [$X or N/A]

--- WHAT WE KNOW ---

Root cause (preliminary):
[One sentence if known, or "Under investigation"]

Trigger:
[The event that initiated the incident, if known]

--- ACTIONS TAKEN ---

1. [Action — timestamp UTC]
2. [Action — timestamp UTC]
3. [Action — timestamp UTC]

--- NEXT STEPS ---

1. [Next action — owner]
2. [Next action — owner]
3. [Next action — owner]

--- ETA ---

Estimated time to resolution: [Time or "Unknown"]
Confidence level: [Low / Medium / High]

--- COMMUNICATION ---

Next update: [Time or "On significant change"]
Channel: [#incident-channel]

Posted by: [Name]
Time: [UTC]
```

### 10.2 Reliability Review Proposal Template

```
RELIABILITY REVIEW PROPOSAL
===============================================================================
TO:      [Team or person being proposed to]
FROM:    [Your name / SRE Team]
DATE:    [YYYY-MM-DD]
SUBJECT: [Clear, specific title — e.g., "Proposed: Rate Limiting for Payment API"]
===============================================================================

1. PROBLEM STATEMENT
   ---------------------------------------------------------------------------
   [One paragraph describing the reliability risk or opportunity. Include:
   - What specific scenario or condition is causing concern
   - Who or what is affected
   - Why now is the right time to address it]

2. EVIDENCE
   ---------------------------------------------------------------------------
   Metric            | Current Value | Target Value | Deviation
   ------------------|---------------|--------------|----------
   [Metric name]     | [Value]       | [Value]      | [X]%
   [Metric name]     | [Value]       | [Value]      | [X]%

   Incidents in last 90 days related to this issue: [N]
   - [INCIDENT-ID]: [Brief description — 1 line]
   - [INCIDENT-ID]: [Brief description — 1 line]

   Error budget consumed by these incidents: [X]%

3. PROPOSED SOLUTION
   ---------------------------------------------------------------------------
   [Detailed description of what you propose to build, change, or implement.
   Include architecture components, configuration changes, or process changes.]

4. EXPECTED OUTCOMES
   ---------------------------------------------------------------------------
   Outcome                        | Metric                  | Estimated Impact
   ------------------------------|-------------------------|-----------------
   Fewer incidents               | Incident count/quarter  | [N] reduction
   Faster recovery               | MTTR                    | [N]% improvement
   Better user experience        | p99 latency             | [N]ms reduction
   Reduced operational burden    | On-call pages/month     | [N] reduction

5. COST AND EFFORT
   ---------------------------------------------------------------------------
   Engineering effort:    [N] engineer-weeks
   Calendar duration:     [N] weeks
   Dependencies:          [List of teams, systems, or decisions needed]
   Risk of change:        [Low / Medium / High]
   Rollback complexity:   [Low / Medium / High]

6. ALTERNATIVES EVALUATED
   ---------------------------------------------------------------------------
   Option | Upside | Downside | Recommendation
   -------|--------|----------|---------------
   [Proposed solution] | [Key benefit] | [Key drawback] | RECOMMENDED
   [Alternative A]     | [Key benefit] | [Key drawback] | Not recommended
   [Do nothing]        | Zero effort   | Risk of [X] incidents/quarter | Fallback

7. RECOMMENDATION
   ---------------------------------------------------------------------------
   [2-3 sentence recommendation. State clearly what you want the team to do,
   by when, and why it benefits the team's own priorities.]

8. NEXT STEPS
   ---------------------------------------------------------------------------
   [ ] Review and discuss this proposal
   [ ] Schedule architecture review (suggested: [date])
   [ ] Identify owner(s) for implementation
   [ ] Define success criteria and acceptance tests

===============================================================================
```

### 10.3 Weekly Reliability Summary Template

```
WEEKLY RELIABILITY SUMMARY
===============================================================================
PERIOD:   [YYYY-MM-DD] — [YYYY-MM-DD]
PREPARED: [Name]
===============================================================================

1. OVERVIEW
   ---------------------------------------------------------------------------
   | Metric                  | This Week | Last Week | Trend | Target |
   |-------------------------|-----------|-----------|-------|--------|
   | P0/P1 Incidents         | [N]       | [N]       | ↑↓→   | [N]    |
   | P2/P3 Incidents         | [N]       | [N]       | ↑↓→   | [N]    |
   | Mean Time to Acknowledge| [X] min   | [X] min   | ↑↓→   | [X]    |
   | Mean Time to Mitigate   | [X] min   | [X] min   | ↑↓→   | [X]    |
   | Mean Time to Resolve    | [X] min   | [X] min   | ↑↓→   | [X]    |
   | Error Budget Remaining  | [X]%      | [X]%      | ↑↓→   | [X]%   |
   | On-Call Pages          | [N]       | [N]       | ↑↓→   | [N]    |

2. INCIDENT SUMMARY
   ---------------------------------------------------------------------------

   INCIDENT #1: [INCIDENT-ID]
   - Severity:  [P0/P1]
   - Duration:  [X] minutes
   - Impact:    [X]% error rate, [X] users affected
   - Root cause: [One line]
   - Status:    [Resolved / Mitigated / Monitoring]
   - Action items: [N] open / [N] closed

   INCIDENT #2: [INCIDENT-ID]
   - Severity:  [P0/P1]
   - Duration:  [X] minutes
   - Impact:    [X]% error rate, [X] users affected
   - Root cause: [One line]
   - Status:    [Resolved / Mitigated / Monitoring]
   - Action items: [N] open / [N] closed

3. INCIDENT CAUSES BREAKDOWN (YTD)
   ---------------------------------------------------------------------------
   Cause Category        | This Week | Quarter to Date
   ----------------------|-----------|-----------------
   Code change           | [N]       | [N]
   Configuration change  | [N]       | [N]
   Infrastructure failure| [N]       | [N]
   External dependency   | [N]       | [N]
   Capacity exhaustion   | [N]       | [N]
   Human error           | [N]       | [N]

4. SERVICE HEALTH
   ---------------------------------------------------------------------------
   Service       | SLO Target | 30d Attainment | Error Budget Remaining
   -------------|------------|---------------|-----------------------
   [Service A]  | [X]%       | [X]%          | [X]%
   [Service B]  | [X]%       | [X]%          | [X]%
   [Service C]  | [X]%       | [X]%          | [X]%

5. RELIABILITY WINS
   ---------------------------------------------------------------------------
   - [Description of win — what was done, by whom, what impact it had]
   - [Description of win]
   - [Description of win]

6. ACTION ITEMS
   ---------------------------------------------------------------------------
   | #  | Action                                  | Owner | Due        | Status |
   |----|-----------------------------------------|-------|------------|--------|
   | 1  | [Description of action]                 | [Name]| [YYYY-MM-DD] | [Open/Closed] |
   | 2  | [Description of action]                 | [Name]| [YYYY-MM-DD] | [Open/Closed] |
   | 3  | [Description of action]                 | [Name]| [YYYY-MM-DD] | [Open/Closed] |

   Overdue items: [N]
   Items due this week: [N]

7. RISK WATCHLIST
   ---------------------------------------------------------------------------
   Risk                              | Likelihood | Impact | Action Plan
   ---------------------------------|------------|--------|-------------
   [Description of risk]            | H/M/L      | H/M/L  | [One sentence]
   [Description of risk]            | H/M/L      | H/M/L  | [One sentence]
   [Description of risk]            | H/M/L      | H/M/L  | [One sentence]

8. RECOMMENDATIONS
   ---------------------------------------------------------------------------
   [1-3 specific, actionable recommendations for leadership. Each should
   include the evidence supporting it and the expected impact.]

===============================================================================
```

### 10.4 Executive Incident Summary Template

```
CONFIDENTIAL — INCIDENT EXECUTIVE SUMMARY
===============================================================================
INCIDENT: [Brief descriptive title — e.g., "Payment Processing Outage"]
DATE:     [YYYY-MM-DD]
SEVERITY: [P0 / P1]
DURATION: [Total time — e.g., "47 minutes"]
===============================================================================

1. EXECUTIVE SUMMARY
   ---------------------------------------------------------------------------
   [3-5 sentences covering:
   - What happened (business-readable)
   - When it happened
   - How long it lasted
   - What the root cause was (high-level)
   - Current status (resolved, monitoring, etc.)]

2. BUSINESS IMPACT
   ---------------------------------------------------------------------------
   Impact Area          | Details
   ---------------------|--------------------------------------------------
   Users Affected       | [X] (approximately [Y]% of active users)
   Downtime Duration    | [X] minutes of total outage
   Degraded Duration    | [X] minutes of partial degradation
   Revenue Impact       | [Estimated $ amount, or "No measurable impact"]
   SLA Impact           | [SLA met / SLA missed by X min]
   Customer Escalations | [N] support tickets escalated
   Regulatory Impact    | [None / Description of any compliance considerations]

3. KEY EVENTS (TIMELINE)
   ---------------------------------------------------------------------------
   Time (UTC)        | Event
   ------------------|--------------------------------------------------
   [HH:MM]           | [First symptom detected — e.g., "Alert fired for error rate spike"]
   [HH:MM]           | [Incident declared / Responders engaged]
   [HH:MM]           | [Mitigation started — e.g., "Rollback initiated"]
   [HH:MM]           | [Service restoration — traffic fully restored]
   [HH:MM]           | [Incident declared resolved]
   [HH:MM]           | [Postmortem scheduled]

4. ROOT CAUSE
   ---------------------------------------------------------------------------
   [One paragraph, business-readable. Avoid excessive technical depth.]

   Category: [Code change / Config change / Infrastructure / External / Capacity]

5. RESOLUTION
   ---------------------------------------------------------------------------
   [Description of the actions taken to restore service. Include who
   responded and how quickly.]

   Key metrics:
   - Time to acknowledge: [X] minutes
   - Time to mitigate:    [X] minutes
   - Time to resolve:     [X] minutes

6. REMEDIATION PLAN
   ---------------------------------------------------------------------------
   Immediate Actions (completed or in progress):
   - [Action]: [Owner — status]
   - [Action]: [Owner — status]

   Long-term Prevention:
   - [Action]: [Owner — target date]
   - [Action]: [Owner — target date]
   - [Action]: [Owner — target date]

7. LESSONS LEARNED
   ---------------------------------------------------------------------------
   What went well:
   - [Observation]
   - [Observation]

   What could be improved:
   - [Observation]
   - [Observation]

8. ATTACHMENTS / REFERENCES
   ---------------------------------------------------------------------------
   - Full postmortem: [link]
   - Incident timeline (detailed): [link]
   - Related dashboards: [links]
   - Related change logs: [links]

===============================================================================
Prepared by: [Name]
Date: [YYYY-MM-DD]
Distribution: [Executive team / VP Engineering / Stakeholders]
===============================================================================
```

---

## Appendix A: Quick Reference Cards

### A.1 Communication Decision Matrix

| Situation | Who to Tell | How | When | Template |
|-----------|-------------|-----|------|----------|
| Incident declared | On-call team + stakeholders | Chat + Status page | Immediately | Section 10.1 |
| Incident status change | All incident subscribers | Chat (incident channel) | Every 30-60 min | Section 10.1 |
| Business-critical impact | Executives | Phone + Email | Within 15 min | Section 10.4 |
| Incident resolved | All subscribers + Support | Chat + Status page | Immediately | Section 10.1 |
| Postmortem complete | Engineering org | Email / Wiki | Within 5 business days | Section 3.1 |
| Reliability proposal | Target team + their manager | Doc + Review meeting | Scheduled | Section 10.2 |
| Weekly reliability | Engineering leadership | Email / Slack digest | Weekly | Section 10.3 |
| Risk identified | On-call + team lead | Chat + Ticketing | Within shift | None required |

### A.2 Common Mistakes and Fixes

| Mistake | Why It Hurts | Fix |
|---------|-------------|-----|
| Using passive voice during incidents | Makes it unclear who is doing what | Start sentences with the person/team performing the action |
| Speculating about root cause without evidence | Misleads stakeholders and creates confusion | Say "Under investigation" with confidence; share only confirmed facts |
| Overpromising on ETA | Erodes trust when the ETA is missed | Give a range, state confidence level, and update proactively |
| Including too much technical detail in executive updates | Leadership cannot act on information they don't understand | Write the "headline" first; offer to share technical details separately |
| Not documenting timeline during the incident | Makes postmortem reconstruction unreliable and harder | Assign a scribe for every P0/P1 incident |
| Letting action items expire | Wastes the learning from the incident | Track in the team's existing workflow, review weekly |
| Using blame language | Discourages honest reporting in future incidents | Review every postmortem draft for blame language before publishing |
| Writing runbooks in different formats | Slows down incident response when every runbook looks different | Use a standardized runbook template for all services |

### A.3 Recommended Reading

- *Site Reliability Engineering* (Beyer et al., O'Reilly) — Chapters on incident response and postmortems
- *The Field Guide to Understanding Human Error* (Dekker) — Foundations of blameless analysis
- *Influence Without Authority* (Cohen & Bradford) — Classic text on cross-team influence
- *Writing on Incident Response* by Google SRE — Published incident postmortems as examples of clear communication
- *Incident Management Best Practices* by PagerDuty — Operational communication patterns

---

> **Document Maintainer**: SRE Team
> **Last Updated**: [YYYY-MM-DD]
> **Version**: 1.0
> **Review Cadence**: Quarterly
