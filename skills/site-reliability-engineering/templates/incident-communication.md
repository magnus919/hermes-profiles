# Incident Communication Templates

Copy-paste ready message templates for communicating during every phase of an incident. Replace `[bracket]` placeholders with actual information.

---

## 1. Incident Detected — Initial Notification

Use when an incident is first confirmed. Send to the incident response channel and on-call contacts.

```
[SUMMARY]: [BRIEF SUMMARY OF INCIDENT]

Severity: [SEV1 / SEV2 / SEV3 / SEV4]
Status: DETECTED — Investigating
Affected Services: [service-a, service-b, service-c]
Impact Description: [Describe what is broken or degraded and who is affected]
Time Started: [YYYY-MM-DD HH:MM UTC]
Last Updated: [YYYY-MM-DD HH:MM UTC]
Timeline Doc: [link to timeline doc]

Actions Taken:
  - [action taken so far]
  - [action taken so far]

Next Steps:
  - [next step]
  - [next step]

Responder(s): [@oncall-person]
```

---

## 2. Investigating — Status Update

Use when the team is actively investigating but has not yet identified the root cause or started mitigation.

```
[SEVERITY UPDATE / NO CHANGE]

Severity: [SEV1 / SEV2 / SEV3 / SEV4]
Status: INVESTIGATING
Affected Services: [service-a, service-b, service-c]
Impact Description: [current description of impact]
Time Started: [YYYY-MM-DD HH:MM UTC]
Last Updated: [YYYY-MM-DD HH:MM UTC]
Timeline Doc: [link to timeline doc]

Current Findings:
  - [finding — e.g. elevated error rate on endpoint X]
  - [finding — e.g. correlation with deployment Y at Z time]

Actions Taken:
  - [action]
  - [action]

Next Steps:
  - [next step]
  - [next step]

ETA: [if known, otherwise "TBD — still investigating"]
```

---

## 3. Mitigation In Progress

Use when a fix or workaround is being deployed. Richer detail than the initial notification.

```
[SUMMARY]: [BRIEF SUMMARY]

Severity: [SEV1 / SEV2 / SEV3 / SEV4]
Status: MITIGATING
Affected Services: [service-a, service-b, service-c]
Impact Description: [current state of impact — may be improving]
Time Started: [YYYY-MM-DD HH:MM UTC]
Last Updated: [YYYY-MM-DD HH:MM UTC]
Timeline Doc: [link to timeline doc]

Root Cause (if known): [root cause summary or "still under investigation"]

Mitigation Actions Taken:
  - [rollback of deployment X]
  - [scaled up resource Y]
  - [disabled feature flag Z]
  - [other action]

Expected Outcome: [what the mitigation should achieve — e.g. "error rate should drop below 1% within 5 min"]

Risks / Trade-offs: [any known side effects of mitigation]

Next Steps:
  - Monitor metrics for [N] minutes
  - Prepare roll-forward fix
  - Stakeholder comms at [time of next update]

ETA to Full Resolution: [time or "TBD"]
```

---

## 4. Resolved

Use when the incident is over — services are healthy and monitoring confirms steady state.

```
[SUMMARY]: [INCIDENT RESOLVED]

Severity: [SEV1 / SEV2 / SEV3 / SEV4]
Status: RESOLVED
Affected Services: [service-a, service-b, service-c]
Impact Description: [summary of what happened and what was impacted]
Time Started: [YYYY-MM-DD HH:MM UTC]
Time Resolved: [YYYY-MM-DD HH:MM UTC]
Duration: [X hours Y minutes]
Timeline Doc: [link to timeline doc]

Root Cause: [root cause summary — e.g. "memory leak in service-b triggered by payload spike"]

Resolution Actions:
  - [action that fixed the issue]
  - [follow-up action taken]

Verification: [how we confirmed the fix — e.g. "error rate at 0% for 15 min, P95 latency back to baseline"]

Post-Incident Items Opened:
  - [link to Jira/Asana bug or task]
  - [link to Jira/Asana bug or task]
```

---

## 5. Post-Incident Summary

Use after the post-mortem has been completed (usually 24-72 hours after resolution).

```
[INCIDENT SUMMARY]

Title: [incident title]
Severity: [SEV1 / SEV2 / SEV3 / SEV4]
Date: [YYYY-MM-DD]
Duration: [X hours Y minutes]

What Happened:
[3-5 sentence narrative of the incident timeline]

Business Impact:
  - [metric affected and value — e.g. "5 min of complete checkout downtime"]
  - [revenue / user / SLA impact]
  - [number of affected customers or requests]

Root Cause:
[1-2 sentence root cause description]

Trigger:
[what caused the incident to start — e.g. deployment, config change, external dependency failure]

Detection:
[How was it detected — monitoring alert, customer report, manual observation? Time to detect.]

Timeline (Key Events):
  - [HH:MM UTC] — [event]
  - [HH:MM UTC] — [event]
  - [HH:MM UTC] — [event]
  - [HH:MM UTC] — [event]

Action Items (from post-mortem):
| # | Action Item | Owner | Priority | Due Date | Tracking Link |
|---|-------------|-------|----------|----------|---------------|
| 1 | [action]    | [name]| [P0/P1]  | [date]   | [link]        |
| 2 | [action]    | [name]| [P0/P1]  | [date]   | [link]        |
| 3 | [action]    | [name]| [P0/P1]  | [date]   | [link]        |

Lessons Learned:
  - What went well: [observation]
  - What went wrong: [observation]
  - What to improve: [observation]

Timeline Doc: [link to timeline doc]
Post-Mortem Doc: [link to post-mortem doc]
```

---

## 6. Executive Summary Template

Use for C-level / VP communication during or immediately after an incident.

```
[EXECUTIVE SUMMARY — INCIDENT]

Subject: [SEV X] Incident Summary — [service / area]

Brief Summary:
[2-3 sentence summary of what happened, in business terms]

Business Impact:
  - Duration of impact: [X hours Y minutes]
  - Customers affected: [number or percentage]
  - Revenue impact: [estimate or "none"]
  - SLA implications: [yes/no + details]
  - Reputation / trust considerations: [if any]

Timeline (Executive View):
  - [HH:MM UTC] — Incident detected
  - [HH:MM UTC] — Mitigation started
  - [HH:MM UTC] — Partial recovery
  - [HH:MM UTC] — Full resolution

Root Cause (if known): [1-2 sentence root cause, in business-readable language — e.g. "A recent configuration change caused our payment gateway to reject valid transactions."]

Current Status: [Resolved / Monitoring / Mitigating]

Key Action Items:
  - [short-term fix deployed or planned]
  - [preventative measure being implemented]
  - [post-mortem scheduled for: date/time]

Communications:
  - Internal: [channel / who was notified]
  - External (if applicable): [customer-facing comms status]

Next Update: [time or "post-mortem report will follow within 48h"]

Point of Contact for Questions: [name / title / contact info]
```

---

## Quick Reference Card

| Phase               | When to Use                                       | Key Fields                                       |
|---------------------|---------------------------------------------------|--------------------------------------------------|
| DETECTED            | Incident first confirmed                          | Severity, affected services, impact, time started |
| INVESTIGATING       | Active diagnosis, no mitigation yet               | Findings, actions taken, ETA (or TBD)            |
| MITIGATING          | Deploying a fix or workaround                     | Mitigation actions, expected outcome, risks      |
| RESOLVED            | Monitored stable — incident over                  | Root cause, resolution, verification             |
| POST-INCIDENT       | After post-mortem (24-72h later)                  | Full timeline, action items, lessons learned     |
| EXECUTIVE SUMMARY   | C-level / VP comms during or right after incident | Business impact, SLA, revenue, clear language    |
