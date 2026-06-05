# Postmortem: [Incident Title]

> **Blameless Culture Reminder:** This postmortem is a blameless analysis of what happened, why it happened, and how we prevent it from happening again. The goal is to learn and improve our systems and processes — not to assign blame or punishment. All participants are expected to contribute honestly and constructively.

---

## Header Metadata

| Field          | Value |
|----------------|-------|
| **Date**       | [YYYY-MM-DD] |
| **Title**      | [Short, descriptive title of the incident] |
| **Severity**   | [SEV1 / SEV2 / SEV3 / SEV4] |
| **Duration**   | [Start time] – [End time] ([Total duration in minutes/hours]) |
| **Date(s)**    | [Date range of the incident] |
| **Reported by**| [Name / Team] |
| **Participants** | [Name / Team], [Name / Team], [Name / Team] |

### Severity Definitions

| Severity | Description |
|----------|-------------|
| **SEV1** | Complete service outage or critical data loss affecting all users |
| **SEV2** | Major feature degradation or partial outage affecting a significant subset of users |
| **SEV3** | Minor degradation, non-critical feature impact, or single-user issue |
| **SEV4** | Cosmetic issue, internal tooling problem, or question/inquiry |

---

## Incident Summary

[1-2 paragraphs providing a high-level overview of the incident. Describe what happened, which systems were involved, the overall impact on users and business, and how the incident was ultimately resolved. This section should be understandable by someone outside the immediate team — executives, customer support, other engineering teams.]

**Example:** "On [DATE] between [START TIME] and [END TIME] UTC, the [SERVICE NAME] experienced a [DESCRIPTION OF FAILURE]. This caused [IMPACT] for [NUMBER] users. Root cause was [BRIEF ROOT CAUSE]. The incident was resolved by [RESOLUTION ACTION]. Total time to resolve was [DURATION]."

---

## Timeline

All times in [UTC / LOCAL TZ].

| Timestamp (UTC) | Event | Who |
|-----------------|-------|-----|
| [YYYY-MM-DD HH:MM] | [Incident begins — first failure symptom observed] | [System / Person] |
| [YYYY-MM-DD HH:MM] | [Alert triggered / page sent] | [Monitoring system] |
| [YYYY-MM-DD HH:MM] | [First responder acknowledged] | [Name] |
| [YYYY-MM-DD HH:MM] | [Initial investigation — what was checked] | [Name] |
| [YYYY-MM-DD HH:MM] | [Escalation to additional team members] | [Name] |
| [YYYY-MM-DD HH:MM] | [Root cause identified] | [Name] |
| [YYYY-MM-DD HH:MM] | [Mitigation action taken] | [Name] |
| [YYYY-MM-DD HH:MM] | [Service restored / incident resolved] | [Name] |
| [YYYY-MM-DD HH:MM] | [Monitoring confirmed healthy / all-clear] | [System / Person] |
| [YYYY-MM-DD HH:MM] | [Postmortem meeting scheduled] | [Name] |

### Key Duration Metrics

| Metric | Duration |
|--------|----------|
| Time to detection (TTD) | [MM minutes] |
| Time to response (TTR) | [MM minutes] |
| Time to mitigation (TTM) | [MM minutes] |
| Time to resolution (TTR) | [MM minutes] |
| Total incident duration | [HH:MM] |

---

## Impact

### Affected Services

- [Service name] — [Description of how it was affected]
- [Service name] — [Description of how it was affected]
- [Service name] — [Description of how it was affected]

### User Impact

- **[Number]** users were affected
- **[Number]** requests failed / timed out ( **[X]%** error rate )
- **[Number]** support tickets filed related to this incident
- **[Description of user-facing symptoms]**

### Business Impact

- **[Amount]** in estimated revenue loss
- **[Number]** failed transactions / orders
- **[Description of SLA/SLO breach, if applicable]**
- **[Other business metrics affected]**

### Metrics at Time of Incident

| Metric | Baseline | During Incident | Post-Recovery |
|--------|----------|-----------------|---------------|
| Error rate | [X]% | [X]% | [X]% |
| Latency p50 | [X]ms | [X]ms | [X]ms |
| Latency p99 | [X]ms | [X]ms | [X]ms |
| CPU utilization | [X]% | [X]% | [X]% |
| Memory usage | [X]% | [X]% | [X]% |
| [Other metric] | [Value] | [Value] | [Value] |

---

## Root Cause

### Summary

[1-2 sentences describing the root cause at a high level.]

### 5 Whys Analysis

| Why? | Answer |
|------|--------|
| **1.** Why did [symptom] happen? | [Answer] |
| **2.** Why did [cause from #1] happen? | [Answer] |
| **3.** Why did [cause from #2] happen? | [Answer] |
| **4.** Why did [cause from #3] happen? | [Answer] |
| **5.** Why did [cause from #4] happen? | **[Root cause — the fundamental system or process issue]** |

### Root Cause Diagram

```
[SYMPTOM]
    |
    v
[Why #1]
    |
    v
[Why #2]
    |
    v
[Why #3]
    |
    v
[Why #4]
    |
    v
[ROOT CAUSE]
```

---

## Contributing Factors

List factors that contributed to the incident's severity, duration, or impact beyond the root cause.

| Factor | Description | Category |
|--------|-------------|----------|
| [Factor 1] | [Description of how this factor contributed] | [Process / People / Technology / External] |
| [Factor 2] | [Description of how this factor contributed] | [Process / People / Technology / External] |
| [Factor 3] | [Description of how this factor contributed] | [Process / People / Technology / External] |

---

## Detection

- **How was the incident first detected?** [Alert / Customer report / Manual observation / Scheduled health check / Other]
- **Time to detection:** [Time between first symptom and first alert/notification]
- **Detection mechanism:** [Describe the monitoring, alert, or human process that surfaced the issue]
- **Did existing monitoring cover the failure mode?** [Yes / No / Partially]
- **If no, what monitoring gap existed?** [Description of gap]
- **Was there a faster way this could have been detected?** [Yes / No — explain]

---

## Response

- **Time to respond:** [Time between first alert and first person taking action]
- **Who responded?** [Names / Teams]
- **What worked well during the response?**
  - [Thing that worked well and why]
  - [Thing that worked well and why]
- **What didn't work well during the response?**
  - [Thing that didn't work well and why]
  - [Thing that didn't work well and why]
- **Were runbooks available and accurate?** [Yes / No — describe]
- **Were the right people reachable?** [Yes / No — describe]
- **Communication channels used:** [Slack / PagerDuty / Zoom / Email / Other]
- **Communication effectiveness:** [Rating 1-5 with comments on clarity, speed, audience]

### Response Timeline Gaps

| Gap | Description | Improvement |
|-----|-------------|-------------|
| [Gap 1] | [What went wrong] | [How to fix] |
| [Gap 2] | [What went wrong] | [How to fix] |

---

## Action Items

Action items derived from this postmortem. Each item has a reference ID that can be linked from epics or tickets.

| ID | Description | Owner | Deadline | Type | Epic/Ticket |
|----|-------------|-------|----------|------|-------------|
| ACT-[001] | [Detailed description of the action to take] | [Name] | [YYYY-MM-DD] | [Prevent / Detect / Mitigate / Process] | [LINK-001] |
| ACT-[002] | [Detailed description of the action to take] | [Name] | [YYYY-MM-DD] | [Prevent / Detect / Mitigate / Process] | [LINK-002] |
| ACT-[003] | [Detailed description of the action to take] | [Name] | [YYYY-MM-DD] | [Prevent / Detect / Mitigate / Process] | [LINK-003] |
| ACT-[004] | [Detailed description of the action to take] | [Name] | [YYYY-MM-DD] | [Prevent / Detect / Mitigate / Process] | [LINK-004] |
| ACT-[005] | [Detailed description of the action to take] | [Name] | [YYYY-MM-DD] | [Prevent / Detect / Mitigate / Process] | [LINK-005] |

### Action Type Definitions

| Type | Description |
|------|-------------|
| **Prevent** | Changes that prevent the incident from recurring |
| **Detect** | Improvements to monitoring, alerting, and observability |
| **Mitigate** | Changes that reduce blast radius or speed recovery if it happens again |
| **Process** | Changes to runbooks, documentation, communication, or training |

### Epic / Ticket References

**LINK-001:** [Epic/Ticket system and ID, e.g., JIRA SRE-1234] — [Brief title]
**LINK-002:** [Epic/Ticket system and ID, e.g., JIRA SRE-1235] — [Brief title]
**LINK-003:** [Epic/Ticket system and ID, e.g., JIRA SRE-1236] — [Brief title]
**LINK-004:** [Epic/Ticket system and ID, e.g., JIRA SRE-1237] — [Brief title]
**LINK-005:** [Epic/Ticket system and ID, e.g., JIRA SRE-1238] — [Brief title]

---

## Lessons Learned

### What Went Well

- [Specific positive observation]
- [Specific positive observation]
- [Specific positive observation]

### What Went Wrong

- [Specific negative observation]
- [Specific negative observation]
- [Specific negative observation]

### What We Were Lucky About

- [Factor outside our control that worked in our favor]
- [Near-miss that could have made things worse]

### Surprises

- [Unexpected behavior or outcome encountered during the incident]
- [Something that was thought to be in place but was not]

---

## Follow-Up Plan

### Immediate Actions (Next 7 Days)

- [ ] [Action item] — Owner: [Name]
- [ ] [Action item] — Owner: [Name]

### Short-Term Actions (Next 30 Days)

- [ ] [Action item] — Owner: [Name]
- [ ] [Action item] — Owner: [Name]

### Long-Term Actions (Next 90 Days)

- [ ] [Action item] — Owner: [Name]
- [ ] [Action item] — Owner: [Name]

### Review Schedule

| Review | Date | Participants |
|--------|------|-------------|
| Action item check-in #1 | [YYYY-MM-DD] | [Names] |
| Action item check-in #2 | [YYYY-MM-DD] | [Names] |
| Follow-up postmortem review | [YYYY-MM-DD] | [Names] |

---

## Appendix

### Supporting Data

- [Link to dashboard / Grafana / Datadog screenshots]
- [Link to relevant logs (Splunk / ELK / CloudWatch)]
- [Link to chat transcript / incident Slack channel]
- [Link to incident ticket / PagerDuty timeline]
- [Link to zoom recording / meeting notes]

### Related Postmortems

- [Link to related postmortem #1]
- [Link to related postmortem #2]

### Changes Since Last Review

[List any relevant changes made to systems/processes since the last postmortem review that are pertinent to this incident.]

---

## Sign-Off

| Role | Name | Date |
|------|------|------|
| Incident Commander | [Name] | [YYYY-MM-DD] |
| Technical Lead | [Name] | [YYYY-MM-DD] |
| SRE Lead | [Name] | [YYYY-MM-DD] |
| Engineering Manager | [Name] | [YYYY-MM-DD] |
| Product Manager (if applicable) | [Name] | [YYYY-MM-DD] |

---

*This postmortem was created on [YYYY-MM-DD] and last updated on [YYYY-MM-DD]. Template version 1.0.*
