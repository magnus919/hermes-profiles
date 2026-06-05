# SRE Guiding Principles

> *"Site Reliability Engineering is what happens when you ask a software engineer to design an operations team."*
>
> — Benjamin Treynor Sloss, Google VP of Engineering, founder of SRE

This document captures the first principles and core philosophy of Site Reliability Engineering as
codified by Google's SRE team. Each principle includes the canonical statement from the SRE book,
an explanation of its reasoning, the practical implications for engineering teams, and guidance on
when to apply it.

---

## 1. Reliability Is a Feature (Not an Add-On)

> *"The primary motivation for having an SRE team is to build and run large-scale, highly available
> systems. But SREs don't just care about availability — they care about latency, performance,
> efficiency, change management, monitoring, emergency response, and capacity planning."*
>
> — *Site Reliability Engineering*, Chapter 1 (Introduction)

**Explanation.** Reliability is a product attribute in its own right, on par with user-facing
features. It cannot be bolted on after the fact like a performance optimization or a security
patch. A system's reliability profile is determined by the design decisions, dependencies, and
architectural tradeoffs baked in from day one — not by how many on-call rotations you run.

**Actionable Implication.** Reliability must be a first-class requirement in every design doc,
sprint planning session, and launch review. Teams should allocate engineering time to reliability
work just as they would to new feature development. If reliability isn't in the roadmap, it
will inevitably be sacrificed for feature velocity.

**When to Apply.** At project inception (architecture decisions), during sprint planning (work
prioritization), and at launch reviews (acceptance criteria). Any time a new dependency or
integration is introduced.

---

## 2. Error Budgets Resolve the Tension Between Velocity and Stability

> *"The error budget is the primary mechanism by which SRE teams decide how to balance the
> reliability of a service with the need to ship features."*
>
> — *Site Reliability Engineering*, Chapter 4 (Service Level Objectives)

> *"The error budget makes it clear that the SRE team is not responsible for maintaining 100%
> reliability. They are responsible for maintaining the agreed-upon level of reliability."*
>
> — *Site Reliability Engineering*, Chapter 4 (Service Level Objectives)

**Explanation.** An error budget is simply 1 minus the SLO. For a service targeting 99.9%
availability, the error budget is 0.1% of total possible uptime (roughly 43 minutes per month).
The product team and SRE team agree on an SLO; the error budget is the "budget of unreliability"
that can be spent by shipping risky changes. As long as the budget is not exhausted, features
ship freely. When the budget is depleted, releases halt until reliability is restored.

**Actionable Implication.** Error budgets turn a philosophical tension into a quantitative
control. Product managers see exactly how much risk they have left in the month. SRE teams get
a objective mechanism to push back on releases when budget is exhausted — it is not opinion,
it is math. Both sides have a shared language for the trade-off.

**When to Apply.** In any organization where product/SRE conflict over release velocity exists.
Essential for services with formal SLOs. Adopt before the tension becomes personal.

---

## 3. Embrace Risk (Don't Aim for 100% Reliability)

> *"100% is the wrong reliability target for basically everything. The cost of achieving 100%
> reliability is so high that it is almost never justified."*
>
> — *Site Reliability Engineering*, Chapter 3 (Embracing Risk)

> *"The marginal return on investment for reliability is not linear. Going from 99.9% to 99.99%
> is roughly 10x the cost, but the benefit depends entirely on the service's business context."*
>
> — *Site Reliability Engineering*, Chapter 3 (Embracing Risk)

**Explanation.** Reliability follows a logarithmic cost curve. Achieving four nines (99.99%)
requires redundant infrastructure in multiple geographic regions, sophisticated failover
mechanisms, and dramatically more engineering effort than three nines (99.9%). For most
services — internal dashboards, batch jobs, experimental features — the extra cost of four
nines provides negligible business value. SRE explicitly rejects the religious pursuit of
perfection in favor of cost-conscious risk management.

**Actionable Implication.** Define reliability targets by asking "what level of unreliability
can our users tolerate?" rather than "how reliable can we make this?" The error budget makes
this explicit: if the service has unused budget, it is *too* reliable and resources are being
wasted. Deploy less redundancy, ship features faster, or reallocate the excess budget elsewhere.

**When to Apply.** When defining SLOs for a new service. When a team reflexively says "we need
five nines." When evaluating architecture proposals that add complexity in the name of
reliability.

---

## 4. Toil Is a Tax on Engineering Creativity

> *"Toil is the kind of work tied to running a production service that tends to be manual,
> repetitive, automatable, tactical, devoid of enduring value, and that scales linearly as the
> service grows."*
>
> — *Site Reliability Engineering*, Chapter 5 (Toil Elimination)

> *"If a human operator needs to touch your system during normal operations, you have a bug."*
>
> — Carla Geisser, Google SRE (paraphrased in Chapter 5)

**Explanation.** Toil is work that (a) is manual, (b) is repetitive, (c) can be automated,
(d) is tactical (interrupt-driven) rather than strategic, (e) has no enduring value (fixing
the same alert every week creates no lasting improvement), and (f) grows linearly with the
scale of the service. Toil is insidious because it feels productive — you are doing things! —
but it displaces the engineering work that actually improves the system.

**Actionable Implication.** Track toil as a metric. If an SRE spends more than 50% of their
time on toil, the organization is over-investing in operations at the expense of engineering.
Dedicate sprint capacity to eliminating toil: automate the manual runbook, fix the flaky alert,
rewrite the fragile deployment script. Every hour spent on toil is an hour not spent making
the system better.

**When to Apply.** During sprint retrospectives (identify toil patterns), in on-call handoffs
(catalog toil), during incident postmortems (identify toil that contributed to the incident),
and at quarterly planning (allocate toil-reduction work).

---

## 5. Blameless Culture (You Can't Fix People, but You Can Fix Systems)

> *"Blameless postmortems are a tenet of SRE culture. The goal is to focus on identifying the
> contributing causes of the incident without indicting any individual. If a team is
> incentivized to hide or gloss over problems, systemic issues are never fixed."*
>
> — *Site Reliability Engineering*, Chapter 15 (Postmortem Culture)

> *"You can't fix people, but you can fix systems."*
>
> — *Site Reliability Engineering*, Chapter 15 (Postmortem Culture)

**Explanation.** Human error is a symptom of system design flaws, not a root cause. When a
pager goes off at 3 AM and an engineer misses a step in the runbook, the failure is in the
runbook design, the alert configuration, the monitoring coverage, or the fatigue induced by
the on-call rotation — not in the individual engineer. Blameless culture does not mean
"no accountability"; it means holding the *system* accountable for tolerating — or preventing —
human error.

**Actionable Implication.** Postmortems must never use the words "should have," "could have,"
or "would have." Replace "operator error" with "a gap in runbook coverage" or "insufficient
automation guardrails." Every postmortem action item must be a system change, not a training
requirement. When an incident involves human error, the question is "what in our system allowed
that error to cause harm?" not "why did that person make a mistake?"

**When to Apply.** Every incident postmortem, every root cause analysis, every time a team
is tempted to blame an individual for a production issue.

---

## 6. Measure Everything with SLOs and SLIs

> *"If you can't measure it, you can't manage it. An SLO-bounded error budget is what allows
> SRE teams to make data-driven decisions about the trade-off between reliability and feature
> velocity."*
>
> — *Site Reliability Engineering*, Chapter 4 (Service Level Objectives)

> *"The most important thing about an SLI is that it actually corresponds to user-facing
> reliability. A metric that doesn't reflect user experience is worse than no metric at all,
> because it gives a false sense of confidence."*
>
> — *Site Reliability Engineering*, Chapter 6 (Monitoring Distributed Systems)

**Explanation.** Service Level Indicators (SLIs) are the raw measurements — request latency,
error rate, throughput, availability. Service Level Objectives (SLOs) are the target thresholds
for those indicators. Together they provide an objective, quantitative definition of what
"reliable enough" means. Without SLIs and SLOs, reliability is a matter of opinion — the SRE
thinks the system is failing and the product manager thinks it is fine, and there is no shared
data to resolve the disagreement.

**Actionable Implication.** Every service must have at least one user-facing SLI and SLO before
it can be meaningfully operated. Start simple: latency at the 99th percentile and error rate
are usually sufficient. Do not create dashboards full of metrics without corresponding SLO
targets — measurement without targets is noise. SLIs should always measure from the user's
perspective (end-to-end), not from internal infrastructure metrics.

**When to Apply.** Before any service is deemed "production." During incident response to
verify the service is back within SLO. During capacity planning to understand whether
growth threatens SLO attainment. At quarterly reviews to track reliability trends.

---

## 7. Automation Over Manual Operations

> *"The SRE approach to operations is a simple tenet: we vastly prefer systems and automation
> over humans doing things manually. Automation is a force multiplier, not a job replacer."*
>
> — *Site Reliability Engineering*, Chapter 5 (Toil Elimination) & Chapter 33 (Automation)

> *"The best automation is the automation that never runs. If you can remove the need for a
> task entirely, that is superior to automating the task."*
>
> — *Site Reliability Engineering*, Chapter 33 (Automation)

**Explanation.** Automation serves three purposes at scale: consistency (machines follow the
same steps every time), speed (automated recovery happens in seconds, human recovery in
minutes or hours), and efficiency (a single engineer can manage orders of magnitude more
infrastructure through automation than through manual clicks). But the hierarchy matters:
before automating a painful manual process, ask whether the process can be eliminated
entirely. Automation of a bad process simply makes bad things happen faster.

**Actionable Implication.** Build automated runbooks for the most common operational actions
(restart, rollback, scale up/down). Use ChatOps or a bot to trigger them. Target a state where
a brand-new engineer with zero domain knowledge can, by typing a single command, perform any
routine operational task that would otherwise take a senior engineer 10 minutes of manual work.
Before automating anything, first ask: "can we make this failure case impossible by changing
the system design?"

**When to Apply.** Whenever a manual step is identified in a runbook. Whenever the same
operational task has been performed more than three times. Whenever an incident could have
been mitigated faster with an automated response.

---

## 8. Simplicity Is a Prerequisite for Reliability

> *"Reliability is inversely proportional to complexity. Every line of code, every dependency,
> every configuration knob is a potential failure mode. The most reliable systems are the
> simplest ones."*
>
> — *Site Reliability Engineering*, Chapter 20 (Load Balancing Layer) & Chapter 22 (Reliable Product Launches)

> *"A simple system that works reliably is infinitely better than a clever system that works
> most of the time."*
>
> — *Site Reliability Engineering*, Chapter 22 (Reliable Product Launches)

**Explanation.** Complexity is the primary enemy of reliability. Each moving part — each
service, database, queue, configuration flag, middleware layer — adds failure modes,
debugging surface area, and operational burden. The SRE philosophy favors straightforward,
well-understood solutions (even if they are less "elegant") over architecturally ambitious
designs. "Boring" infrastructure is reliable infrastructure.

**Actionable Implication.** Actively resist architectural complexity. Use the "cognitive load"
test: if understanding a single failure scenario requires holding more than a handful of
components in your head simultaneously, the system is too complex. Prefer monoliths over
microservices for teams that cannot justify the operational overhead. Remove unused code,
features, and configuration aggressively. Every deleted line of code is a prevented incident.

**When to Apply.** During architecture reviews (push back on unnecessary abstractions).
During incident postmortems (identify which complexity contributed). During code reviews
(reject over-engineered solutions). During quarterly architecture audits (dedicate time to
simplification).

---

## 9. Slow Is Smooth, Smooth Is Fast (Incident Response Discipline)

> *"In a time-critical incident, the most important thing is to remain calm and follow the
> process. Going fast by yourself will be slower than going together as a team."*
>
> — *Site Reliability Engineering*, Chapter 13 (Emergency Response)

> *"The difference between a good incident response and a bad one is not technical skill —
> it's discipline. The discipline to follow the process, the discipline to engage the right
> people, and the discipline to stop and think before acting."*
>
> — *Site Reliability Engineering*, Chapter 13 (Emergency Response)

**Explanation.** Incident response is an exercise in controlled urgency. The natural instinct
when a production incident occurs is to fix it as fast as possible — jump into the system,
try things, escalate laterally. This instinct is wrong. The fastest path to recovery is
almost always: (1) declare the incident formally, (2) assemble the response team with clear
roles (Incident Commander, Operations Lead, Comms Lead), (3) triage before acting, and
(4) act deliberately. "Slow is smooth, smooth is fast" means the initial overhead of process
is repaid many times over by avoiding mistakes, confusion, and wasted effort.

**Actionable Implication.** Adopt explicit incident command protocols (similar to firefighting
ICS/NIMS). Practice them in drills and tabletop exercises. The Incident Commander should
*not* be debugging — their job is to coordinate the response, keep time, and ensure roles
are filled. After every major incident, evaluate the *process* (not just the technical cause):
was the incident declared promptly? Were roles filled? Did communications stay on the
designated channel?

**When to Apply.** Every time a production incident is declared. During incident response
drills (practice the process, not the technology). When training new on-call engineers.
When a postmortem reveals that confusion, not technical failure, slowed recovery.

---

## 10. Production Is the Only Thing That Matters

> *"If you haven't run your service in production, you don't understand it. Production reveals
> failure modes that no amount of staging, testing, or simulation can uncover."*
>
> — *Site Reliability Engineering*, Chapter 29 (Software Engineering in SRE)

> *"The production environment is not a development environment, and it must be protected by
> mechanical sympathy, gradual rollout, and safe deployment practices."*
>
> — *Site Reliability Engineering*, Chapter 29 (Software Engineering in SRE)

**Explanation.** There is an unbridgeable gap between how a system behaves in staging and how
it behaves in production. Production has real user traffic, real data shapes, real network
conditions, real contention, and real failure modes that no test environment can faithfully
reproduce. SRE treats production as the authoritative environment. All engineering decisions —
deployment strategies, rollout speeds, configuration changes, capacity planning — are made
with production as the reference frame.

**Actionable Implication.** Invest in production telemetry and observability above all else.
Staging environments should be treated as validation tools, not as reliable proxies for
production behavior. Use canary deployments, gradual rollouts, and feature flags to safely
verify changes in the real environment. Production access is a privilege, not a right — it
requires training, tools, and safety mechanisms.

**When to Apply.** When designing deployment pipelines (always include canary/progressive
rollout). When evaluating monitoring (does it measure production behavior end-to-end?).
When deciding what to test (prioritize production-proxy tests over staging-only tests).
When training engineers (production safety and awareness is a mandatory competency).

---

## 11. The 50% Engineering Time Mandate

> *"SRE teams must spend no more than 50% of their time on operational work (toil and
> incident response). The remaining 50% is reserved for engineering projects that reduce
> toil, improve reliability, and increase service capacity."*
>
> — *Site Reliability Engineering*, Chapter 5 (Toil Elimination)

> *"If operational work regularly exceeds 50% of an SRE team's time, the team is too small
> for the service they are operating. The solution is not to work harder — it is to either
> reduce the operational load or grow the team."*
>
> — *Site Reliability Engineering*, Chapter 5 (Toil Elimination)

**Explanation.** The 50% cap on operational work is the defining operational constraint of SRE
as a discipline. It ensures that SRE teams are engineering teams that do operations, not
operations teams that occasionally write scripts. The cap forces hard decisions: if on-call
load, pager volume, and manual tasks consume more than 50% of the team's time, the team must
either automate the work, push back on accepting additional service ownership, or grow.

**Actionable Implication.** Time-track operational vs. engineering work explicitly. Use the
50% threshold as a forcing function: if you are above it, the team's OKRs must include
toil-reduction projects. Managers must protect the engineering allocation from being eroded
by operational firefighting. If the team sustains >50% operations for multiple quarters, the
situation requires organizational intervention (headcount, service transfer, or SLO relaxation).

**When to Apply.** During quarterly capacity planning. When evaluating whether to take on a
new service. During one-on-ones and team health assessments. When the team consistently feels
"too busy to improve things."

---

## 12. Sublinear Scaling as the Goal

> *"The goal of SRE is to build systems that scale sublinearly with service growth. If you
> double the size of the service, you should not need to double the size of the SRE team."*
>
> — *Site Reliability Engineering*, Chapter 1 (Introduction)

> *"A team of five SREs should be able to manage a fleet that is ten times larger than the
> fleet that required a team of five SREs a year ago."*
>
> — *Site Reliability Engineering*, Chapter 1 (Introduction)

**Explanation.** Linear scaling (double the machines, double the operators) is the default
state of manual operations — and it is unsustainable. The entire philosophy of SRE —
automation, simplification, toil elimination — is motivated by the goal of sublinear scaling.
If service growth requires proportional headcount growth, the team is doing operations work,
not engineering work. True SRE success means the team's span of control (the size and
complexity of the system they operate) grows faster than the team itself.

**Actionable Implication.** Track the ratio of team size to service footprint (servers, QPS,
services owned, data volume). This ratio is a leading indicator of SRE health. When the ratio
degrades (more resources per engineer owned), invest in automation and simplification before
asking for more headcount. A healthy SRE organization should be able to absorb 2x service
growth with no more than a marginal increase in team size.

**When to Apply.** When justifying headcount requests. When evaluating whether automation
investments are paying off. When a service is growing rapidly and the team feels the strain.
During architectural discussions about service boundaries and ownership.

---

## 13. The Hierarchy of Production Needs

> *"A service must meet its foundational requirements — monitoring, incident response, and
> capacity planning — before higher-order concerns like feature velocity or developer
> productivity can be addressed."*
>
> — *Site Reliability Engineering*, Chapter 6 (Monitoring Distributed Systems) & Chapter 17 (Testing for Reliability)

> *"You cannot deploy reliably if you don't know whether your service is healthy. You cannot
> know whether your service is healthy if you aren't monitoring it. Monitoring is the
> foundation on which all other SRE practices rest."*
>
> — *Site Reliability Engineering*, Chapter 6 (Monitoring Distributed Systems)

**Explanation.** Reliability has a dependency hierarchy, analogous to Maslow's hierarchy of
needs. At the base is monitoring and observability — without knowing your system's state,
nothing else is possible. Above that: incident response (the ability to react when monitoring
alerts). Above that: capacity planning (ensuring resources match demand). Above that:
deployment and change management (safely evolving the system). At the top: feature velocity
and developer productivity. Skipping lower levels makes higher levels impossible or dangerous.

**Actionable Implication.** When onboarding a new service onto an SRE team, audit the
hierarchy bottom-up. Is monitoring in place? Is there a documented incident response process?
Is there capacity planning? Is there a safe deployment pipeline? Do not accept a service
into production that has gaps in the lower tiers. Fix the foundation before building on it.

**When to Apply.** When accepting a new service for SRE support. When the team's reliability
problems feel overwhelming (fix the bottom of the hierarchy first). When planning reliability
improvements. When a service has frequent incidents that the team cannot explain.

---

## 14. The "Reliability Enough" Philosophy

> *"The goal is not to maximize reliability; it is to provide reliability that is sufficient
> for the service's business purpose, at a cost that is justified by the value."*
>
> — *Site Reliability Engineering*, Chapter 3 (Embracing Risk)

> *"A service that is 'too reliable' is wasting resources that could be spent on features,
> performance, or other services. The error budget is the mechanism for detecting and
> correcting over-investment in reliability."*
>
> — *Site Reliability Engineering*, Chapter 4 (Service Level Objectives)

**Explanation.** "Reliability enough" is the practical expression of SRE's risk-embracing
philosophy. It means explicitly choosing a reliability target that is "good enough" for the
business context — not the maximum achievable, not what competitors do, not what feels safe.
A development API that serves internal teams can run at 99% (8 hours of downtime per month)
without meaningful harm. A payment gateway needs 99.99% or higher. The choice is deliberate
and data-informed, not reactive or aspirational.

**Actionable Implication.** Every service should have regularly reviewed SLOs that reflect the
business value of that service to its users. Services with no direct user-facing impact should
have lower SLO targets. Review SLOs quarterly; if a service never exhausts its error budget,
raise the question: "are we over-investing in this service's reliability?" The answer may be
"no, it's just well-run," but the question must be asked explicitly.

**When to Apply.** During annual or quarterly SLO reviews. When a team wants to raise a
service's SLO target. When a team is evaluating new architecture for an existing service.
When the error budget is consistently under-consumed and the team is wondering why.

---

## Cross-Reference: Principle to SRE Book Chapter

| # | Principle | Primary Chapter(s) | Secondary Chapter(s) |
|---|-----------|--------------------|-----------------------|
| 1 | Reliability Is a Feature | Ch. 1 — Introduction | Ch. 29 — Software Engineering in SRE |
| 2 | Error Budgets | Ch. 4 — Service Level Objectives | Ch. 3 — Embracing Risk |
| 3 | Embrace Risk | Ch. 3 — Embracing Risk | Ch. 4 — SLOs |
| 4 | Toil Is a Tax | Ch. 5 — Toil Elimination | Ch. 6 — Monitoring |
| 5 | Blameless Culture | Ch. 15 — Postmortem Culture | Ch. 12 — Effective Troubleshooting |
| 6 | Measure Everything (SLOs/SLIs) | Ch. 4 — SLOs / Ch. 6 — Monitoring | Ch. 3 — Embracing Risk |
| 7 | Automation Over Manual Ops | Ch. 5 — Toil Elimination / Ch. 33 — Automation | Ch. 8 — Release Engineering |
| 8 | Simplicity | Ch. 20 — Load Balancing / Ch. 22 — Reliable Launches | Ch. 31 — Simplicity |
| 9 | Slow Is Smooth, Smooth Is Fast | Ch. 13 — Emergency Response | Ch. 14 — Incident Management |
| 10 | Production Is the Only Thing That Matters | Ch. 29 — Software Engineering in SRE | Ch. 8 — Release Engineering |
| 11 | 50% Engineering Time Mandate | Ch. 5 — Toil Elimination | Ch. 6 — Monitoring |
| 12 | Sublinear Scaling | Ch. 1 — Introduction | Ch. 33 — Automation |
| 13 | Hierarchy of Production Needs | Ch. 6 — Monitoring / Ch. 17 — Testing | Ch. 8 — Release Engineering |
| 14 | "Reliability Enough" Philosophy | Ch. 3 — Embracing Risk / Ch. 4 — SLOs | Ch. 2 — Production Environment |

---

## How to Use This Reference

1. **Onboarding.** New SRE team members should read through each principle as part of their
   orientation. The principles provide the conceptual vocabulary for all team decisions.

2. **Decision Making.** When facing a trade-off (e.g., "should we invest in more redundancy or
   ship this feature?"), reference the relevant principle. The principles encode decades of
   accumulated operational wisdom at Google scale.

3. **Postmortems and Reviews.** Use the principles as evaluation criteria. Did we violate
   "simplicity" in this design? Did "toil" play a role in this incident? Did we respect the
   "error budget" in our release cadence?

4. **Cultural Alignment.** The principles are not just technical guidelines — they are the
   cultural DNA of SRE. A team that lives these principles will naturally prioritize
   automation, embrace blameless learning, and resist the impulse to chase perfection at
   the expense of everything else.

---

> *"SRE is fundamentally about applying a software engineering mindset to operations problems.
> The principles above are the axioms that fall out of that mindset. Internalize them, and
> the operational decisions become obvious."*
>
> — *Site Reliability Engineering*, Chapter 1 (Introduction) — adapted
