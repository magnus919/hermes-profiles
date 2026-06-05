# Blameless Postmortem Culture & Methodology

> **Reference for Site Reliability Engineering teams**  
> How to build, run, and sustain a learning-oriented incident review practice

---

## Table of Contents

1. [The Blameless Postmortem Philosophy](#1-the-blameless-postmortem-philosophy)
2. [Postmortem Triggers and Criteria](#2-postmortem-triggers-and-criteria)
3. [Postmortem Structure](#3-postmortem-structure)
4. [The 5 Whys Methodology](#4-the-5-whys-methodology)
5. [Systemic Fixes vs. Human Fixes](#5-systemic-fixes-vs-human-fixes)
6. [Avoiding Blame Language](#6-avoiding-blame-language)
7. [Postmortem Review Process](#7-postmortem-review-process)
8. [Sharing and Knowledge Management](#8-sharing-and-knowledge-management)
9. [Measuring Postmortem Effectiveness](#9-measuring-postmortem-effectiveness)
10. [Common Pitfalls](#10-common-pitfalls)
11. [Cultural Integration](#11-cultural-integration)
12. [The Cost of Failure as Education](#12-the-cost-of-failure-as-education)
13. [Language Transformation Table](#13-language-transformation-table)

---

## 1. The Blameless Postmortem Philosophy

### What Is a Blameless Postmortem?

A blameless postmortem is a structured process conducted after an incident to understand what happened, why it happened, and how to prevent it from happening again. The defining characteristic — the "blameless" part — is that the analysis focuses entirely on systemic causes, process failures, and environmental conditions, never on individual actions, mistakes, or character.

The core axiom of blameless postmortems is:

> **Every person was doing their best with the information and tools available to them at the time.**

This is not naivete or an excuse to avoid accountability. It is a pragmatic recognition that blame is a failure-analysis dead end. When an engineer makes a mistake, the question is never "Who should be held responsible?" but rather "What conditions made that mistake possible, and how do we change those conditions?"

### Why Blameless?

The rationale is grounded in two domains:

**Psychological safety.** In his landmark research on high-performing teams, Google's Project Aristotle identified psychological safety as the single most important predictor of team effectiveness. Blameless postmortems create safety by guaranteeing that honest participation carries no career risk. Without this guarantee, incidents go uninvestigated, root causes remain hidden, and the same failures recur.

**Systems thinking.** Complex socio-technical systems fail in characteristic ways that are almost never reducible to individual error. Reason's "Swiss Cheese Model" of accident causation shows that most failures require multiple latent conditions (holes in the cheese) to align before a catastrophe occurs. Blaming the person at the sharp end — the operator who pressed the wrong button — ignores the dozen other holes that were already present: unclear documentation, missing alerts, poorly designed UI, insufficient testing, breakneck deadlines.

### The Safety-I vs. Safety-II Paradigm

Traditional incident analysis (Safety-I) asks: "What went wrong?" and seeks to eliminate errors. Modern SRE practice increasingly adopts Safety-II thinking, which asks: "Why did things go right most of the time?" and treats incidents as valuable data points about how the system actually behaves under stress. Blameless postmortems bridge both paradigms — they study failures to strengthen the system's ability to succeed.

---

## 2. Postmortem Triggers and Criteria

Not every bug, page, or degraded response merits a full postmortem. Organizations define explicit criteria to ensure postmortem effort is proportionate to incident impact and learning value.

### Recommended Trigger Criteria

A postmortem should be conducted when any of the following occurs:

| Severity | Criterion | Example |
|----------|-----------|---------|
| **High** | User-visible outage lasting > N minutes | 5+ minutes of 5xx errors for a customer-facing service |
| **High** | Data loss or corruption | Permanent loss of customer records |
| **High** | Security breach or intrusion | Unauthorized access to production data |
| **High** | Financial impact above threshold | >$10K in direct costs |
| **Medium** | Degraded experience exceeding SLO | P99 latency exceeds 2x target for 10+ minutes |
| **Medium** | On-call escalation requiring >2 people | Incident requiring coordination across teams |
| **Medium** | Manual intervention to restore service | Any incident where a person had to SSH into a box or edit a config to fix it |
| **Low** | Recurring same-class failure | Third occurrence of the same root-cause pattern |
| **Any** | Novel failure mode | Something never seen before that teaches a new lesson |

### Optional but Recommended Triggers

- Any incident that consumed an on-call shift entirely (burnout risk signal)
- Any incident that required a rollback
- Any incident involving a change that bypassed normal review
- Near-misses with high potential impact
- Customer-reported issues that revealed systemic gaps

### Setting the Bar

The threshold should be calibrated to the team's capacity. A good heuristic: **if you're going to tell someone about the incident, write a postmortem.** The formal barrier should be low enough that the 80th-percentile incident gets documented, not just the catastrophic ones.

---

## 3. Postmortem Structure

A good postmortem is organized, consistent, and actionable. Below is the canonical structure used by leading SRE organizations.

### 3.1 Metadata Header

```
Incident ID:        INC-2025-06-05-001
Title:              [Brief, descriptive title]
Date:               2025-06-05 14:32 UTC
Duration:           47 minutes
Severity:           Critical
Services Affected:  [list of services]
Trigger:            [what initiated the incident]
Postmortem Owner:   [name]
Reviewer:           [name]
```

### 3.2 Executive Summary

A 3-5 sentence overview accessible to non-technical stakeholders. State what happened, the impact, and the highest-priority action items.

### 3.3 Timeline

A chronological, time-stamped account of the incident. This is the most important section for learning. Include:

- **Before:** The state of the system prior to the trigger event (deployments, config changes, traffic shifts)
- **Trigger:** The specific event that initiated the incident
- **Detection:** When and how the team learned something was wrong (alert, user report, dashboard)
- **Response:** Every action taken, including false starts and dead ends
- **Resolution:** The action that restored service
- **After:** Remediation steps already taken during or immediately after the incident

Timeline entries should be precise UTC timestamps. Include relevant logs, metrics, and command output. Do not editorialize — just state what happened and when.

### 3.4 Root Cause

A single paragraph describing the fundamental underlying failure. The root cause should be **systemic** — a statement about process, design, or environment, not about a person.

**Good root cause statement:** "A race condition between the deploy pipeline's health-check timeout (30s) and the new service's JVM warmup period (45s) caused the load balancer to mark all instances as unhealthy, blackholing traffic."

**Bad root cause statement:** "Alice deployed during peak hours without checking the warmup time."

### 3.5 Contributing Factors

All the conditions that made the root cause possible or worsened the impact. This is where most of the learning lives. Common categories:

| Category | Examples |
|----------|----------|
| **System design** | Single point of failure, missing redundancy, tight coupling |
| **Process** | Missing change review, insufficient test coverage, gaps in runbook |
| **Tooling** | Poor observability, confusing dashboards, slow deployment tooling |
| **Organizational** | Team knowledge silos, inadequate on-call training, time pressure |
| **Environmental** | Dependency failure (DNS, cloud provider, third-party API), capacity exhaustion |

Aim for 3-8 contributing factors per postmortem.

### 3.6 Action Items

Specific, tracked, and owner-assigned tasks to prevent recurrence. Each action item should follow the SMART criteria.

| Field | Description |
|-------|-------------|
| **Description** | What specifically will be done? |
| **Type** | Preventative (reduces likelihood) / Mitigating (reduces impact) / Detectability (improves discovery) / Process (improves response) |
| **Owner** | Single responsible person |
| **Tracker URL** | Link to Jira/Asana/GitHub issue |
| **Due Date** | Realistic deadline |
| **Status** | Open / In Progress / Done / Won't Do |

Good action items are concrete: "Add a canary deployment stage that runs the health-check with a 60-second grace period" — not "Improve deployment safety."

### 3.7 Lessons Learned

What the team learned collectively:

- What went well (so it can be reinforced)
- What went poorly (the gaps identified)
- What surprised the team
- Where the team was lucky

### 3.8 Appendix

Supporting evidence: dashboard screenshots, log excerpts, config files, chat transcripts, monitoring graphs.

---

## 4. The 5 Whys Methodology

The 5 Whys is a root-cause analysis technique that iteratively asks "Why?" to peel back layers of symptoms until the fundamental systemic cause is exposed. It was developed by Sakichi Toyoda and is a core component of the Toyota Production System and Lean methodology.

### How It Works

Start with the incident description, then ask "Why did this happen?" For each answer, ask "Why?" again. Repeat until the answer points to a process, design, or organizational issue — not a person's action.

### Worked Example

**Incident:** Production database was dropped at 03:14 UTC on June 5.

1. **Why was the database dropped?**
   Because a `DROP DATABASE` command was executed against the production cluster.

2. **Why was the DROP DATABASE command executed?**
   Because an engineer ran a migration script against the wrong cluster.

3. **Why did the engineer run against the wrong cluster?**
   Because the production cluster and the staging cluster had nearly identical connection strings in the config file.

4. **Why did the config file have nearly identical connection strings?**
   Because the naming convention for clusters was `db-prod-1` and `db-staging-1` — only the environment segment differs, making it hard to distinguish at a glance.

5. **Why was the naming convention chosen?**
   Because there was no documented standard for cluster naming, and the original team followed a pattern from a deprecated infrastructure template.

**Root cause:** Inconsistent cluster naming conventions and a lack of visual differentiation in connection strings made cross-environment mistakes possible. The staging migration process lacked guardrails to prevent targeting production.

### When 5 Whys Works Best

- Single-cause, relatively simple incidents
- Incidents where the causal chain is well-understood
- Time-constrained situations (5 Whys can be done in 15 minutes)

### Limitations

- Complex incidents with multiple interacting failures may need more sophisticated analysis (e.g., causal trees, STAMP)
- The technique tends to produce a single linear narrative, which can miss parallel contributing factors
- The fifth "why" is often arbitrary; stop when you hit a systemic cause, not when you hit five

---

## 5. Systemic Fixes vs. Human Fixes

The central discipline of blameless postmortem culture is distinguishing between fixes that address the system and fixes that address the person.

### Systemic Fixes (Preferred)

Systemic fixes change the environment, process, or technology to make errors impossible or harmless.

| Type | Example |
|------|---------|
| **Automation** | Add a pre-commit hook that warns when a migration targets production |
| **Guardrails** | Implement a "production confirmation" step that requires a second approval |
| **Design change** | Use different color schemes for prod/staging database connection strings |
| **Process change** | Require runbook review as part of the deploy checklist |
| **Tooling** | Create a CLI wrapper that prevents dangerous commands across environments |
| **Observability** | Add an alert for `DROP DATABASE` statements on production |
| **Isolation** | Remove direct database access entirely; route all mutations through an API |

### Human Fixes (Avoid)

Human fixes attempt to prevent recurrence through individual effort, training, discipline, or accountability.

| Type | Why It Fails |
|------|-------------|
| **Retraining** | Assumes the engineer didn't know better; usually they did, but the system made error easy |
| **Reviewer added** | Adds a human bottleneck; humans are inconsistent at catching errors in repetitive reviews |
| **Policy change** | "Be more careful" is not an action item; policies without tooling are ignored under pressure |
| **Blame / disciplinary action** | Destroys psychological safety, discourages future reporting, and doesn't fix the root cause |
| **Process checklist** | Checklists are effective only when the failure mode is known and the checklist is enforceable |

### The Golden Rule

> **If a fix can be automated, it should be automated. If a guardrail can be built, it should be built. A human fix is the failure of engineering, and a second failure to fix the right thing.**

### Exceptions

There is a small category of genuinely individual failures: intentional malice, gross negligence, or repeated violation of clearly documented safety-critical procedures after the system was corrected. These are vanishingly rare and should be handled through management processes, not postmortem action items.

---

## 6. Avoiding Blame Language

Language shapes culture. The words used in a postmortem determine whether the document is a tool for learning or a weapon for blame.

### Principles of Blameless Language

1. **Describe actions, not people.** Say "the deployment pipeline removed healthy instances" not "the engineer unhealthy instances."
2. **Use passive or systemic voice.** Say "the alert was not configured" not "you forgot to configure the alert."
3. **State facts neutrally.** "The change was deployed during peak traffic" not "someone deployed at a stupid time."
4. **Attribute decisions to context, not character.** "The engineer chose the fastest option under time pressure" not "the engineer was lazy."
5. **Focus on conditions, not choices.** "The console showed identical hostnames for prod and staging" not "the engineer didn't check which host they were on."

### Blame Language Detection

Scan postmortem drafts for these red-flag words and phrases:

| Flag | Blame Implication |
|------|-------------------|
| "should have" | Hindsight bias — implies the person should have known the outcome |
| "failed to" | Focuses on omission rather than surrounding conditions |
| "neglected" | Suggests carelessness or laziness |
| "didn't" | Blames the absence of an action without asking why |
| "careless," "sloppy" | Character judgments that shut down analysis |
| "obvious" | Retrospective clarity; nothing was obvious in the moment |
| "common sense" | Assumes shared knowledge that may not have existed |

---

## 7. Postmortem Review Process

The review process ensures quality, consistency, and real learning. It should not be a rubber stamp.

### Step 1: Draft (Within 48 Hours)

The incident responder or designated postmortem owner writes the initial draft. Focus on the timeline while memory is fresh. Do not wait for perfection — publish an incomplete draft early.

### Step 2: Peer Review (Within 1 Week)

The postmortem is reviewed by:

- **The incident responder(s)** — verify timeline accuracy
- **A subject matter expert** — validate technical analysis
- **An SRE lead or manager** — check for blameless language and systemic action items
- **A peer from another team** — bring fresh eyes and challenge assumptions

Review criteria:
- Is the timeline accurate and complete?
- Is the root cause truly systemic?
- Are contributing factors explored, not just the trigger?
- Is every action item SMART and owned?
- Does the document pass the "blameless language" test?

### Step 3: Action Item Assignment

Each action item is assigned an owner and entered into the team's tracking system. The postmortem itself is not "closed" until all action items are resolved.

### Step 4: Broad Review (Weekly or Monthly)

A recurring meeting (e.g., a weekly "Postmortem Review" slot) where the team walks through new postmortems. This is not a punishment round — it is a collective learning session. Key outcomes:

- Shared understanding of failure modes
- Cross-team pattern recognition ("We saw this same issue in the payments service last month")
- Prioritization of systemic fixes that affect multiple services

### Step 5: Closure (After 30-90 Days)

- All action items have been completed or explicitly deprioritized
- The postmortem is archived in a searchable knowledge base
- A brief follow-up note is appended documenting what changed

---

## 8. Sharing and Knowledge Management

A postmortem that sits in a private Google Doc is worthless. Sharing is the mechanism through which one team's failure becomes every team's learning.

### Internal Sharing Practices

- **Postmortem email list / Slack channel.** A low-traffic, opt-in distribution for all completed postmortems.
- **Searchable archive.** Index all postmortems in a tool that supports full-text search. Tools like GitHub, Confluence, or dedicated platforms.
- **Incident database.** Maintain a lightweight registry (spreadsheet, wiki, or database) tracking: incident ID, date, service, severity, root cause category, action items.
- **Quarterly incident review.** A broader retrospective looking at patterns across multiple incidents.

### External Sharing

When the incident affected customers or had industry relevance, consider sharing publicly. Site Reliability Engineering pioneered the model of publishing postmortems to learn from each other across organizational boundaries:

- [Amazon AWS Postmortems](https://aws.amazon.com/message/)
- [Google Cloud Status Dashboard](https://status.cloud.google.com/)
- [GitHub Engineering Blog](https://github.blog/category/engineering/)
- [Cloudflare Blog](https://blog.cloudflare.com/tag/outage/)

### Anonymization

For shared postmortems, strip identifying information (engineer names, specific customer data, internal systems whose names leak architecture). The goal is to share the *lesson*, not the *story* behind it.

---

## 9. Measuring Postmortem Effectiveness

If you don't measure it, you don't know if it's working. Track these metrics to gauge postmortem program health.

### Process Metrics

| Metric | Target | What It Measures |
|--------|--------|------------------|
| **Time-to-postmortem** | <48 hours from incident | Freshness of analysis; delays reduce accuracy |
| **Postmortem coverage** | >90% of qualifying incidents | Are we writing postmortems consistently? |
| **Time-to-review** | <7 days from draft | Is the review process a bottleneck? |
| **Action item completion rate** | >80% within 90 days | Are we following through? |

### Outcome Metrics

| Metric | Target | What It Measures |
|--------|--------|------------------|
| **Repeat incident rate** | Declining trend | Are we learning? Same-class incidents should decrease |
| **Mean time to resolve (MTTR)** | Stable or declining | Are postmortem findings improving response? |
| **Incident severity distribution** | Shift toward lower severities | Are preventative measures working? |
| **Action items per postmortem** | 3-5 (sweet spot) | Too few = shallow analysis; too many = scope creep |

### Cultural Metrics

Harder to quantify but equally important:

- **Postmortem participation rate.** Are on-call engineers contributing, or just the SRE lead?
- **Psychological safety surveys.** Do team members feel safe reporting incidents and mistakes?
- **Blame-language audit.** What fraction of postmortem language is blame-free? Trend this over time.

---

## 10. Common Pitfalls

Even well-intentioned postmortem programs fall into predictable traps.

### Superficial Analysis

The postmortem stops at the first apparent cause rather than digging deeper.

**Signs:** Action items are trivial or obvious. Root cause is a single sentence that blames a person or a "config error." Contributing factors section is empty.

**Fix:** Use the 5 Whys. Ask "What made that possible?" for every finding. Insist on at least three contributing factors.

### Too Many Action Items

A postmortem produces 15+ action items, most of which are never completed. This creates a false sense of progress and erodes trust in the process.

**Signs:** Action item list is a brain dump. Many items are vague ("improve testing"). No owner assigned. Completion rate is below 50%.

**Fix:** Limit action items to 3-5 per postmortem. Force prioritization. If something is important but not a top-5 priority, create a separate initiative. Track completion aggressively.

### No Follow-Through

Postmortems are written, action items are created, and then nothing happens. This is the most damaging pitfall because it teaches the organization that postmortems are theater.

**Signs:** Action items stay "Open" for months. The same root cause appears in multiple postmortems. Engineers stop participating because they don't see change.

**Fix:** Assign a postmortem program owner with authority to escalate. Review action item completion in every sprint planning. Close postmortems only when action items are resolved.

### Blame Creep

Despite professed blameless culture, postmortems contain subtle blame language. Senior engineers publicly say "no blame" but privately harbor resentment.

**Signs:** Postmortem drafting is avoided. Engineers deflect ownership. Language audits find blaming phrases.

**Fix:** Train reviewers on blameless language. Conduct periodic audits. Model vulnerability from leadership — managers should present their own postmortems first.

### Survivorship Bias

Only major incidents get postmortems; the small ones and near-misses are ignored. This means the high-frequency, low-severity failure modes never get fixed.

**Fix:** Lower the postmortem threshold. Create a lightweight "mini-postmortem" format (just timeline + root cause + 1 action item) for smaller incidents.

---

## 11. Cultural Integration

Postmortem culture is not created by writing a policy document. It is created through rituals, habits, and visible leadership behavior.

### Postmortem of the Month

A monthly session where the team reviews the most interesting postmortem — either internal or from another company. The presenter walks through the timeline and lessons. This:

- Normalizes failure as a topic of conversation
- Builds shared mental models of failure modes
- Creates a rhythm of continuous learning
- Makes postmortems a source of interest, not dread

### Reading Clubs

Organize a book club or reading group around SRE and incident analysis texts:

- *Site Reliability Engineering* (Beyer et al., O'Reilly)
- *The Field Guide to Understanding Human Error* (Dekker)
- *Drift into Failure* (Dekker)
- *The Art of Capacity Planning* (Allspaw)
- *Incident Management for Operations* (Limoncelli et al.)

Rotate facilitation. Encourage members to bring parallels to their own incidents.

### Wheel of Misfortune

A popular training exercise developed at Google. A team is given a simulated incident scenario and must respond in real time, making decisions, communicating, and debugging under pressure. After the simulation, the group conducts a mini-postmortem.

**Benefits:**
- Builds muscle memory for incident response
- Reveals gaps in runbooks, tooling, and team coordination
- Normalizes failure in a safe environment
- Identifies who thrives under pressure (not to "grade" but to assign incident roles)

**Format suggestions:**
- Run quarterly, rotating scenario types
- Include participants from multiple teams
- Invite observers who are not participating
- Treat outcome as data, not evaluation

### Incident Commander Rotation

Ensure every engineer takes a turn as incident commander. This builds empathy for the on-call experience, breaks down the "operator vs. developer" divide, and ensures postmortem recommendations reflect real operational pain.

### Leadership Modeling

The most powerful cultural signal is a senior leader presenting their own postmortem — admitting a mistake their team made, showing vulnerability, and modeling the blameless analysis approach. When the VP of Engineering says "Here's a failure I own and here's what I learned," the entire organization internalizes that postmortems are safe.

---

## 12. The Cost of Failure as Education

### The Tuition Model

Every failure is tuition paid for organizational learning. The question is whether the lesson is actually learned. An incident that costs $50K in downtime and produces a postmortem with actionable, implemented fixes is $50K well spent. The same incident that produces no learning is pure waste.

### Calculating the Return

Organizations that invest in postmortem culture see measurable returns:

- **Reduced incident frequency.** Each failure prevented saves the direct cost of downtime plus the opportunity cost of engineers' time spent fighting fires.
- **Faster incident resolution.** Teams that practice postmortems develop shared mental models that accelerate diagnosis during the next incident.
- **Lower turnover.** Psychological safety is one of the strongest predictors of retention. Engineers leave organizations where they fear blame.
- **Customer trust.** Fewer and shorter outages directly affect customer retention and brand equity.

### The Cost of Not Doing Postmortems

The alternative to blameless postmortems is not "no postmortems" — it's secret blame, finger-pointing, and unrepeated lessons. The cost of blameless culture is a small investment in writing and reviewing documents. The cost of *not* having blameless culture is the same incidents recurring indefinitely, accompanied by attrition of the very people who understand the system best.

### Messaging to Leadership

When pitching postmortem culture to skeptical leadership:

> "We can pay for failure once and learn from it, or we can pay for it over and over. A blameless postmortem is the mechanism that converts incident cost into institutional knowledge. Without it, we're just paying tuition and skipping class."

---

## 13. Language Transformation Table

A quick-reference guide for converting blame-laden language into blameless, systemic language.

| Blame Language (Avoid) | Blameless Language (Use) |
|------------------------|--------------------------|
| "Alice failed to check the config before deploying." | "The deploy process did not include a pre-flight config validation step." |
| "Bob should have noticed the alert earlier." | "The alert was routed to a channel that Bob had notifications muted on." |
| "The team was careless with the migration." | "The migration script lacked a dry-run mode, making it impossible to test without risk." |
| "No one thought to monitor the database connection pool." | "Connection pool metrics were not surfaced in the standard service dashboard." |
| "The developer didn't read the documentation." | "The documentation for this feature was stored in a separate wiki that was not linked from the deployment guide." |
| "Someone pushed a bad change." | "Change X introduced a regression in the user-auth module. The change passed code review but lacked test coverage for the edge case encountered." |
| "The operator panicked and made it worse." | "During the incident, the operator's actions were taken under time pressure without a defined escalation path. The runbook for this scenario did not exist." |
| "It was a human error." | "The UI presented the 'Delete' and 'Archive' buttons adjacent to each other with identical styling, making misclicks predictable under pressure." |
| "Why didn't anyone catch this in QA?" | "The test environment did not replicate production traffic patterns, so the race condition did not manifest during testing." |
| "The SRE on call was sleeping and missed the page." | "The paging system uses a single notification channel that can be silenced by Do Not Disturb mode. The escalation policy does not include a secondary on-call." |
| "Common sense should have prevented this." | "The safety mechanism for this operation was entirely manual and relied on individual vigilance, which is unreliable under fatigue or time pressure." |
| "This engineer has made this mistake before." | "This is the second incident involving this failure pattern, indicating that the previous action items (retraining, docs update) were insufficient. A systemic fix is needed." |
| "The rollout was reckless." | "The rollout was performed during peak traffic because the release calendar left no off-peak window. The deployment pipeline did not enforce a canary strategy." |
| "They should have rolled back immediately." | "The rollback procedure was documented in a separate, infrequently accessed runbook and required credentials not available to the incident commander." |

---

## Appendix: Sample Mini-Postmortem Template

For low-severity incidents where a full postmortem is disproportionate:

```
## Mini-Postmortem: [Title]

**Incident ID:** INC-YYYY-MM-DD-NNN  
**Date:** YYYY-MM-DD HH:MM UTC  
**Duration:** N minutes  
**Impact:** [Brief description]

### What Happened
[2-3 sentences]

### Root Cause
[1 sentence, systemic]

### One Action Item
- [ ] [Concrete, owned, tracked] — Owner, Due

### What We Learned
[Optional: 1-2 sentences about the takeaway]
```

---

## Further Reading

| Resource | Author(s) | Why |
|----------|-----------|-----|
| *Site Reliability Engineering* | Beyer, Jones, Petoff, Murphy | The canonical text on SRE practice, including postmortem chapters |
| *The Field Guide to Understanding Human Error* | Sidney Dekker | The definitive argument for the "new view" of human error |
| *Drift into Failure* | Sidney Dekker | How complex systems gradually move toward failure |
| *Incident Management for Operations* | Limoncelli, Kerth | Practical incident response and postmortem facilitation |
| *Learning from Incidents in Software* | Allspaw (blog) | Seminal essays on blameless analysis from Etsy's CTO |
| *Postmortem Action Items: How Google SRE Reduces Incident Recurrence* | Google SRE (white paper) | Data-driven look at what makes action items effective |
| *Project Aristotle* | Google re:Work | Research on psychological safety in high-performing teams |

---

> **Last updated:** 2025-06-05  
> **Maintainer:** SRE Skill Profile / Hermes Agent  
> **License:** This reference is part of the Hermes Agent SRE profile. Use freely, adapt locally.
