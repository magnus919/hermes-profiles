# Product-Focused Reliability for SRE

## Synthesized Analysis

> **Source Article:** "Product-Focused Reliability for SRE" by Carl Crous, Parker Roth, and Victoria Hurd (Google)
> **URL:** https://sre.google/resources/practices-and-processes/product-focused-reliability-for-sre/
> **Analysis Date:** June 2026

---

## Overview

This article, published by Google SRE practitioners Carl Crous, Parker Roth, and Victoria Hurd, represents a significant evolution in Site Reliability Engineering thinking. It proposes a fundamental shift away from the traditional *service-centric* SRE model — where SRE teams own and operate specific infrastructure services — toward a *product-centric* model where SRE accountability is organized around what users actually care about: product functionality and end-user outcomes.

This is not a minor tweak to existing SRE practice. It reframes the unit of ownership, the stakeholders SRE partners with, the way SLOs are defined and measured, and even what triggers a pager. For practitioners, it offers a compelling path out of the scalability trap that service-based SRE inevitably hits as organizations grow.

---

## 1. Why Service-Centric SRE Falls Short

Traditional SRE organizes around *services* — databases, load balancers, authentication backends, API gateways. A team owns a set of services and is responsible for their availability, latency, and capacity. This model has been enormously successful but carries fundamental limitations.

> *"Service availability doesn't always result in user happiness with a product."*

### The Five Limitations

| Limitation | Description | Impact |
|---|---|---|
| **Services are partial proxies for user needs** | A user doesn't care about "database write availability at 99.99%." They care about "can I save my draft?" High service-level availability can mask broken user journeys. | SREs optimize what they can measure (service metrics) rather than what matters (user outcomes). |
| **Complex UIs create coverage gaps** | Modern web and mobile applications involve client-side logic, caching layers, retry logic, async RPCs, and service meshes. A service-level SLO cannot capture failures that happen entirely in the client or across multiple service hops. | The symptom a user sees (a blank page, a stuck spinner) is invisible to server-side monitoring. |
| **Service growth outpaces engineering** | The number of servers and microservices has grown exponentially (driven by public cloud). The number of software engineers grows linearly. SRE teams cannot scale by adding more services to their portfolio. | SRE teams become bottlenecks. They support more services with the same headcount, but each service gets thinner coverage. |
| **Service support optimizes a narrow slice** | If an SRE team owns a set of services, their incentives align with maximizing those services' metrics — not with the end-to-end product experience. They may ship infrastructure improvements that don't move the needle on user satisfaction. | Effort is misallocated. The SRE team works hard but the product doesn't get more reliable from the user's perspective. |
| **Async flows can't be measured by a single service** | A user request may trigger a chain: UI → enqueue → background worker → third-party API → callback. If any link in this chain fails silently, no single service's SLO catches it. | The user sees a failure. The SRE team sees green dashboards everywhere. The disconnect erodes trust in SRE. |

### Practitioner Takeaway

If your team has ever said "all our SLOs are green but users are complaining," you have experienced this problem. The service-centric model is not *wrong* — it is *insufficient*. It gives SREs a false sense of coverage and misdirects engineering effort toward infrastructure metrics that don't correlate cleanly with user happiness.

---

## 2. The Product Support Model

The article's central thesis: shift the unit of accountability from *services* to *products*. An SRE team doesn't ask "which services do we own?" but rather "which product functionality are we responsible for making reliable?"

> *"Rather than accepting accountability for service reliability, SRE teams can accept accountability for the product itself."*

### Key Characteristics

- **Accountability shifts upward.** The team is responsible for whether a user can complete a specific task (e.g., "send an email"), not for whether a particular microservice is healthy.
- **Scope broadens.** Product accountability naturally encompasses multiple services, client-side code, and third-party dependencies. The SRE team must care about the entire path.
- **Language changes.** Instead of talking about RPC latency percentiles, the team talks about "how long does it take to load the inbox?" — the same language product managers and UX researchers use.
- **Priorities get sharper.** When a pager fires, the question becomes "which user objective is affected and how severely?" rather than "which service is down?"

### What This Is Not

The product support model does **not** eliminate service ownership. Infrastructure must still run. The shift is one of *primary focus*: the team's north star is product reliability, and service reliability is a means to that end, not an end in itself.

---

## 3. Product Engagement

For product-focused SRE to work, SREs must step outside their traditional engineering silo and engage with disciplines they rarely partnered with before.

### New Stakeholder Relationships

| Stakeholder | What They Bring | Why SRE Needs Them |
|---|---|---|
| **Product Managers (PMs)** | User objectives, feature priorities, KPI definitions, roadmap | Defines *what* reliability means for the product, sets severity guidelines |
| **UX Researchers** | User behavior data, friction points, Jobs to be Done analysis | Grounds reliability work in real user behavior, not assumptions |
| **Engineering Teams** | Service architecture, implementation details, operational knowledge | Technical partner for instrumentation and incident response |
| **Support/Customer Success** | Escalation patterns, common user complaints | Early warning system for reliability gaps |

### Frameworks SRE Must Learn

The article highlights two frameworks that PMs and UX teams already use:

**Jobs to be Done (JTBD):** Models user objectives as "jobs" — the progress a user is trying to make in a particular circumstance. A user doesn't "use Gmail"; they "communicate with colleagues" or "archive promotional emails."

**Critical User Journeys (CUJs):** Google's internal framework that identifies the most important end-to-end paths a user takes through a product. CUJs map directly to what SRE should measure.

> *"Using this information, SRE can identify what is important to the product and its users, and they can define reliability in the same language used to define the product."*

### Practitioner Takeaway

This is perhaps the hardest cultural shift for SRE teams. SREs are trained to think in terms of systems, binaries, and infrastructure — not user behavior, product features, and business KPIs. Learning to speak the same language as PMs requires deliberate effort. The payoff is that SRE work becomes visible and valued at the product level, not just the infrastructure level.

---

## 4. Bootstrapping Workflow

The article provides a concrete 4-step workflow for adopting the product support model. This is not abstract theory — it is a practical sequence with intermediate deliverables.

### Step 1: Engage Stakeholders

| Action | Deliverable |
|---|---|
| Identify all relevant stakeholders using a RACI matrix | RACI chart |
| Meet with PMs, UX, engineering, support | Documented roles and responsibilities |
| Establish communication cadence | Meeting schedule, escalation paths |

The stakeholder set is *broader* than service-based SRE. A service engagement might only involve the service owner's engineering team. A product engagement includes PM (who defines what success looks like), UX (who understands user behavior), engineering (who builds and maintains), and support (who fields user complaints).

### Step 2: Model the Product

| Action | Deliverable |
|---|---|
| Identify user objectives (what users want to achieve) | List of user objectives |
| Break each objective into steps (individual user actions) | Step breakdown per objective |
| Register in a product registry | Maintained product model |

> *"People use a product to achieve a real-world objective... The user's intent is also a powerful reliability tool that SREs can leverage."*

### Step 3: Measure Performance

| Action | Deliverable |
|---|---|
| Define SLOs across three categories (service, client, E2E) | SLO definitions |
| Annotate SLOs with user objective/step information | Product-level SLOs |
| Set targets with user context | SLO targets aligned to product criticality |

### Step 4: Manage Reliability

| Action | Deliverable |
|---|---|
| Onboard a single objective/step | Initial SRE support scope |
| Iterate: improve metrics, expand objectives, address gaps | Expanded coverage |
| Periodically offboard obsolete SLOs | Focused, current support scope |

---

## 5. User Objectives and Steps

The decomposition of a product into user objectives and steps is the foundational modeling technique in the product support model.

### Definitions

- **User Objective:** A user's intent — what they want to achieve. High-level and stable. Example: "Communicate with people."
- **Step:** An individual action the user takes to accomplish the objective. Isolated, measurable, independent units of work. Example: "Compose and send a new email."

### Worked Example: Mail Service

| User Objective | Steps | Description |
|---|---|---|
| **Communicate with people** | Compose mail | Create and format a new email message |
| | Send mail | Submit the composed message for delivery |
| | Read incoming mail | View received messages in the inbox |
| | Search mail | Find specific messages by keyword or filter |
| | Manage mail | Delete, archive, label, or move messages |
| | Manage contacts | Add, edit, or delete address book entries |
| **Prevent unwanted communication** | Filter spam | Automatically classify and divert unwanted messages |
| | Block senders | Manually block specific email addresses |
| **Organize communication** | Create labels/folders | Build a personal organizational structure |
| | Apply rules/filters | Automate message triage |

### Why This Decomposition Matters

| Aspect | Service-Centric View | Product-Centric View |
|---|---|---|
| What we measure | RPC latency to the mail-store service | Time to render inbox with unread messages |
| What we alert on | Error rate on compose-save endpoint | Failure rate of "save draft" step |
| What we prioritize | Database replication lag | "Send mail" step latency during peak hours |
| Language used | "The compose validator service is p99=500ms" | "Composing mail is slower than users tolerate" |

### Practitioner Takeaway

If your product does not have clearly defined user objectives (owned by PM, not SRE), you will have to develop them yourself — at significant engineering cost, and with the risk that only SRE is invested in maintaining them. **The article is clear: PMs should own the user objectives.** SRE should partner, not own.

---

## 6. Product Criticality and Prioritization

Not all user objectives are equally important. Product criticality defines which objectives matter most.

### Severity Guidelines

Severity guidelines map outage impact to user experience. Examples from the article:

| Severity | Mail Service Example | Impact |
|---|---|---|
| **S1 (Critical)** | Cannot read or send email | Core functionality broken |
| **S2 (High)** | Emails delayed by > 5 minutes | Significant degradation |
| **S3 (Medium)** | Spell check, auto-complete not working | Auxiliary features degraded |
| **S4 (Low)** | UI cosmetic issue, non-critical feature broken | Minimal user impact |

### Product Criticality Matrix

Using severity guidelines, user objectives and steps are assigned criticality:

| User Objective | Steps | Criticality | Rationale |
|---|---|---|---|
| **Communicate with people** | Compose mail | Critical | Core functionality |
| | Send mail | Critical | Core functionality |
| | Read incoming mail | Critical | Core functionality |
| | Search mail | High | Important but not blocking |
| | Filter spam | Medium | Value-add |
| **Prevent unwanted communication** | Filter spam | Medium | Nice-to-have |
| **Organize communication** | Create labels | Low | Power user feature |

> *"The critical definition is modeled around the user's objectives (like composing and sending email) rather than how the system was implemented to address these needs."*

### Prioritization Principles

The article offers practical guidance for aligning SRE work with product KPIs:

1. **Base coverage first:** Ensure good base coverage across the entire infrastructure before investing in targeted improvements.
2. **Follow the KPIs:** Use product-level severity guidelines to prioritize. If revenue is the KPI, reliability work that protects revenue comes first.
3. **Avoid the one-size trap:** Don't apply the same methodology everywhere. Batch traffic doesn't need the same SLOs as interactive traffic.
4. **Invest proportionally:** Spend more on critical objectives, less on auxiliary ones. Not everything needs an end-to-end SLO.

### Practitioner Takeaway

> *"If an SRE knows an issue is severe, they will react and escalate more quickly, resulting in a faster resolution."*

Product criticality informs not just SLO design but incident response. When a page comes in annotated with "Critical User Objective: Compose Mail," the responder knows this is a customer-facing issue affecting core functionality, not an internal infrastructure hiccup.

---

## 7. Three SLO Categories

The article identifies three categories of SLOs with distinct trade-offs. Practitioners should use all three strategically.

| Dimension | Service SLOs | Client-Side Instrumentation | End-to-End SLOs |
|---|---|---|---|
| **Cost** | Low | Moderate | Very high |
| **Confidence** | High | Low | High |
| **Latency** | Low | Moderate | High |
| **Coverage** | Narrow | Broad | Narrow |
| **Where measured** | Server logs, load balancers | Browser, mobile app telemetry | Joined data across multiple sources |
| **What it catches** | Server-side failures | UI failures, client-side bugs, network issues | Async failures, multi-step workflows |
| **Data reliability** | High | Low (some data loss expected) | High (per-interaction measurement) |
| **Engineering effort** | Minimal | Moderate | Significant |

### Service SLOs

The familiar kind — measured from application servers, load balancers, or monitoring probes. Cheap, reliable, but myopic. They cannot see client-side failures, async failures, or issues that span multiple services.

*Good for:* Infrastructure health, baseline coverage, non-critical paths.

### Client-Side Instrumentation

Telemetry collected from web browsers or mobile apps. Captures what users actually experience — rendering time, network latency, client-side errors. Data is less reliable (batched, subject to loss on app close or network disconnect) but provides uniquely valuable insight.

> *"Complexities in how the interface behaves — caching, retries, and asynchronous RPC requests — are transparent when you can measure start and end conditions from the user interface."*

*Good for:* UI performance, mobile reliability, measuring what users actually experience.

### End-to-End SLOs

The most expensive and most accurate category. Joins data from multiple sources to measure a complete user interaction. For async workflows (e.g., "user requested a report → report was generated → report was delivered"), end-to-end SLOs are the only way to know if the workflow actually completed.

*Requirements:* Must identify and correlate events across systems, handle time synchronization, and manage data pipelines.

*Good for:* Critical user journeys, async workflows, business-critical features.

### Practitioner Takeaway

> *"There are classes of issues that cannot be measured from a single server, for example, issues that occur within a web or mobile application, or through an asynchronous action."*

The art is choosing the right SLO category for each user objective. Critical objectives get end-to-end SLOs. Important objectives get client-side or service SLOs. Everything else gets basic service SLOs or nothing at all. **Do not over-instrument.**

---

## 8. Product SLOs

A product-level SLO is any SLO that has been annotated with user objective and step information. It bridges the gap between infrastructure metrics and user experience.

### Annotation Process

1. Take an existing SLO (service, client-side, or end-to-end).
2. Annotate it with: which user objective it serves, which step it supports, the criticality level.
3. Set the target with user context, not infrastructure context.

### Before and After

| Aspect | Service-Framed SLO | Product-Framed SLO |
|---|---|---|
| **Question** | "How reliable should the AddressLookup service be?" | "How many errors can users tolerate when looking up email addresses?" |
| **Target** | 99.9% availability | 99.5% of "look up address" steps succeed within 200ms |
| **Context** | Infrastructure concern | User concern |
| **Validation** | Service properties | Product criticality guidelines |

> *"Setting the objective target or latency thresholds is notoriously challenging when the SLOs are framed around services and infrastructure. But when the SLOs have the additional context of the user's objectives, what is being measured becomes much clearer."*

### Why This Matters

- **Prevents over-engineering:** If a step is non-critical, you can justify a looser SLO. Without product context, SREs default to "as reliable as possible" — which is expensive.
- **Justifies spending:** "We need to invest in the 'send mail' E2E SLO because it's critical" is a much stronger case than "we need to improve the mail-sender service's p99."
- **Enables trade-offs:** When capacity is limited, you know which steps to degrade first.

---

## 9. Telemetry and Annotation

To turn product-level SLOs from theory into practice, SREs must instrument requests with product context.

### Client-Side Annotation

The user interface (web or mobile app) annotates each request with the user objective and step it serves. This happens at the source — the closest point to the user. The annotation propagates through the infrastructure stack.

### Server-Side Annotation

The server that handles the initial request infers the user objective from the request endpoint, parameters, or headers. This requires less client-side instrumentation but may be less accurate.

### Propagation Benefits

Once requests are annotated, the annotation propagates through the entire infrastructure stack, enabling:

| Use Case | Benefit |
|---|---|
| **Monitoring** | Dashboards show reliability per user objective, not per service |
| **Alerting** | Pages include "Critical: Compose Mail step failing" context |
| **Incident Response** | Responders know immediately which user functionality is affected |
| **Traffic Routing** | Low-priority steps can be shed before they harm critical steps |
| **Load Shedding** | During overload, shed non-critical steps first |
| **SLO Tracking** | Burn rates are tracked per user objective |

> *"This request-level information can also be used in traffic routing and load shedding policies to ensure that lower priority functionality doesn't harm more mission critical features."*

### Practical Guidance

The article advises against trying to annotate everything. Use product criticality to decide: annotate only the most critical user objectives, at least initially. The cost of annotation (engineering time, propagation complexity, data storage) must be justified by the value.

---

## 10. Onboarding, Iteration, Offboarding

Managing product reliability is an ongoing process, not a one-time project.

### Onboarding

Start small. Do not try to support every user objective at once.

1. Pick **one** user objective and a subset of its steps.
2. Ensure the team understands the objective thoroughly.
3. Define SLOs (start with service-level, add client-side and E2E as justified).
4. Establish the monitoring and alerting infrastructure.
5. Confirm incident response procedures cover this objective.

### Three Investment Areas

| Area | Description | Risk of Underinvesting |
|---|---|---|
| **Improve metrics** | Better instrumentation, more accurate SLIs, reduced data loss | Team misses root causes, can't validate improvements |
| **Expand objectives** | Add more user objectives and steps to SRE coverage | Important functionality remains unprotected |
| **Address gaps** | Fix the reliability issues the metrics reveal | Team measures problems but doesn't fix them |

> *"Not investing sufficiently in areas #1 and #2 can cause your team to miss targeting the most impactful issues in area #3. Investing only in areas #1 and #2 won't result in any improvements that help the user."*

### Offboarding

Periodically re-evaluate supported objectives and SLOs. Some become less important over time. Some become obsolete. The article recommends:

- Maintain a prioritized list of all supported objectives, steps, and SLOs.
- Regularly validate that the team's effort matches the current priority order.
- Offboard items that are no longer critical, freeing capacity for more important work.

> *"Every SLO carries an ongoing cost to maintain its underlying data and respond to SLO misses."*

---

## 11. Server Support and Baseline

A common objection to product-focused SRE is: "If we're focused on products, who keeps the servers running?" The article addresses this directly.

### Baseline Support

The concept of *baseline support* predates the product support model at Google. It's a set of standards and best practices that ensure any server can be run reliably without deep understanding of its specific purpose.

| Baseline Element | Purpose |
|---|---|
| Common libraries and frameworks | Consistent load balancing, RPC, monitoring |
| Platform-level reliability | Infrastructure SLOs owned by platform team |
| Minimum operational standards | Logging, monitoring, deployment, rollback |
| Development team ownership | The team that builds the service handles basic operations |

> *"The platform rather than the SREs provide baseline reliability support, which frees SREs to focus on more impactful reliability improvements."*

### When Do SREs Get Paged?

This is one of the most operationally consequential shifts in the model:

| Scenario | Service-Centric | Product-Centric |
|---|---|---|
| Database replica lag spikes | SRE paged | No page (unless it fails a product SLO) |
| Canary deployment fails | SRE paged | No page (unless it affects a critical objective) |
| Batch job fails silently | SRE paged | No page (batch is non-critical) |
| Inbox fails to load for 1% of users | No page (load balancer shows 99.9% uptime) | **SRE paged** (critical objective failing) |
| Async report generation fails | No page (enqueue succeeded) | **SRE paged** (end-to-end SLO breached) |

> *"Failures at the infrastructure level that do not impact the product SLOs will not alert SREs and can be handled by the development team that owns the service."*

### Practitioner Takeaway

This is liberating but requires organizational maturity. The development team must be capable of handling their own service issues. The platform must provide sufficient baseline support. Without these preconditions, the product focus will collapse because the infrastructure will rot.

---

## 12. When It's a Good Fit

The product support model is not universally applicable. The article is refreshingly honest about the prerequisites.

### Requirements Checklist

| Requirement | Why It's Needed |
|---|---|
| **Clear roles and responsibilities** | Without RACI clarity, the broader stakeholder set creates ambiguity, not alignment |
| **User objective definitions** | Must be owned by PMs, not retrofitted by SRE alone |
| **Easily maintainable servers** | If SREs spend all their time keeping servers alive, they can't focus on product |
| **Clear connection to user-facing functionality** | Infrastructure services with low-level APIs may not map cleanly to user objectives |

### Three Options for Infrastructure Services

The article acknowledges that some services (like data storage or message queues) don't have a direct user-facing component. Three approaches:

| Option | Description | Best For |
|---|---|---|
| **Map indirectly** | Find the upstream consumer that makes the service relevant to user objectives | Services close to the user-facing stack |
| **Treat as platform** | Apply baseline support only; don't invest in product-level SLOs | Generic infrastructure (KV stores, queues) |
| **Skip the model** | Some services don't benefit from product focus; use traditional SRE | Internal tooling, non-user-facing services |

### Organizational Readiness

The model works best when:

- The organization has mature product management with clear user objective definitions.
- Engineering teams can maintain their own services (DevOps maturity).
- Platform/infrastructure teams provide baseline reliability.
- SRE has executive support to prioritize product outcomes over service metrics.
- Incident severity guidelines already exist and are product-aligned.

---

## 13. Synthesis: What This Means for SRE Practice

This final section synthesizes the article's implications for the SRE profession.

### On-Call Changes

| Aspect | Service-Centric | Product-Centric |
|---|---|---|
| **What triggers a page** | Service error budget burn | Product SLO burn (per user objective) |
| **First question** | "Which service is down?" | "Which user objective is affected?" |
| **Runbook structure** | Per-service recovery | Per-objective recovery (may span services) |
| **Escalation** | Escalate to service owner | Escalate to product team (PM + eng + UX) |
| **Page reduction** | Harder to reduce (all service issues trigger) | Easier to reduce (infra failures that don't hit product SLOs are filtered) |

### Alerting Philosophy

Product-focused alerting means:

- Alerts carry user context: "Critical objective 'send mail' is experiencing 5% errors."
- Alerts for infrastructure degradation that doesn't affect product SLOs are routed to the owning development team, not SRE.
- Alert fatigue decreases because the team only pages on product-relevant failures.
- False negatives (the user sees a failure but no alert fires) decrease because client-side and E2E SLOs catch what service SLOs miss.

### Team Structure

| Model | Structure | Career Path |
|---|---|---|
| **Service SRE** | Teams organized by service (DB SRE, Networking SRE, Storage SRE) | Deep specialist → Senior infrastructure SRE |
| **Product SRE** | Teams organized by product (Gmail SRE, Drive SRE, Calendar SRE) | Broad generalist → Product reliability lead → SRE Manager |

The product SRE model creates a different career trajectory. Product SREs need broader knowledge (frontend, backend, mobile, APIs) rather than deep infrastructure specialization. They must be comfortable with product language, stakeholder management, and cross-team coordination.

### Organizational Model: Product SRE vs Service SRE

It is not necessarily an either/or choice. The article implies a hybrid model may work best:

1. **Platform SRE teams** handle baseline infrastructure (compute, networking, storage). They use traditional service SRE models.
2. **Product SRE teams** focus on user objectives. They partner with PMs and own product-level SLOs.
3. **Service SRE teams** (if needed) support critical internal services that don't map directly to user objectives.

> *"The product support model lets the SRE team focus on the user to ensure that the product meets the end user's real-world needs."*

### Key Insights for Practitioners

1. **Start small.** Pick one user objective, one step, one SLO. Prove the model works before expanding.

2. **Language is strategy.** If you're still talking about "services" and "RPC latency," you haven't made the shift. Product-level language ("compose mail," "send mail") drives alignment.

3. **The stakeholder set is wider.** PMs and UX are now essential partners. SREs must invest in cross-functional relationships.

4. **Not everything needs a product SLO.** Baseline support handles commodity infrastructure. Criticality guides where to invest.

5. **Offboarding is as important as onboarding.** SLOs have ongoing costs. Regularly prune obsolete ones.

6. **Annotation is the technical linchpin.** Without the ability to tag requests with user objective context, product SLOs remain theoretical.

7. **This model is a forcing function for platform maturity.** If your infrastructure requires constant SRE attention, you cannot shift to product focus. Invest in platform reliability first.

---

## Appendix: How This Changes Common SRE Practices

| Practice | Traditional SRE | Product-Focused SRE |
|---|---|---|
| **Error budgets** | Per service | Per user objective, aggregated across services |
| **Capacity planning** | Service-level utilization | Per-objective traffic patterns |
| **Load shedding** | By service priority | By user objective criticality |
| **Release engineering** | Rolling out new service versions | Canarying new features by user objective |
| **Incident management** | Service-centric IR (e.g., "DB incident") | Product-centric IR (e.g., "send mail incident") |
| **Postmortems** | Focus on service failure modes | Focus on user impact and journey gaps |
| **SLO reviews** | Quarterly service SLO review | Quarterly per-objective SLO review with PM |
| **Onboarding** | Service onboarding checklist | Objective/step onboarding with product team |
| **Team metrics** | Service availability, latency p99 | Objective reliability, step success rate |

---

## References

The article cites the following sources:

1. Ulwick, A.W. and Osterwalder, A. (2016). *Jobs to be Done: Theory to Practice.* Idea Bite Press.
2. Chang, A. (2017). "What To Do If Your Product Isn't Growing." Initialized Capital.
3. Beyer, B., Jones, C., Petoff, J. and Murphy, N. (2016). *Site Reliability Engineering: How Google Runs Production Systems.* O'Reilly Media.
4. Beyer, B., Murphy, N., Rensin, D.K., Kawahara, K. and Thorne, S. (2018). *The Site Reliability Workbook.* O'Reilly Media.
5. Kalbach, J. (2020). *The Jobs to be Done Playbook.* Two Waves Books.
6. Google Cloud. "Incidents and the Google Cloud Service Health Dashboard." https://cloud.google.com/support/docs/dashboard
7. Wikipedia. "Responsibility Assignment Matrix." https://en.wikipedia.org/wiki/Responsibility_assignment_matrix

---

*This document is a synthesized analysis of the Google SRE article "Product-Focused Reliability for SRE" by Carl Crous, Parker Roth, and Victoria Hurd. It is not a verbatim reproduction. The analysis adds practitioner interpretation, synthesized tables, and organizational guidance beyond what appears in the original article, while staying faithful to its core concepts.*
