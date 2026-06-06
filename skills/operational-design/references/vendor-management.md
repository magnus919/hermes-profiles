# Vendor Management

Vendors are partners, not transactions. A well-managed vendor relationship reduces risk, improves service quality, and creates leverage for cost negotiations.

## RFP Process

Request for Proposal (RFP) is a structured process for evaluating vendor options. Use RFPs for significant investments where comparison across multiple vendors is needed.

### RFP Lifecycle

1. **Requirements Definition** — What must the vendor do? What's nice-to-have?
2. **Vendor Shortlist** — 3-5 vendors who can meet requirements
3. **RFP Issuance** — Formal document sent to shortlisted vendors
4. **Vendor Q&A** — Clarify questions, ensure all vendors have same information
5. **Proposal Evaluation** — Score proposals against weighted criteria
6. **Vendor Demos / POCs** — Shortlisted vendors demonstrate capability
7. **Reference Calls** — Check with existing customers
8. **Negotiation & Selection** — Final terms and selection

### RFP Template

```
1. Executive Summary
   - Project overview, timeline, budget range

2. Company Background
   - About us, our needs, current state

3. Scope of Work
   - Detailed requirements (must-have, should-have, nice-to-have)
   - Deliverables, milestones, success criteria

4. Vendor Qualification Requirements
   - Company size, experience, certifications
   - Security and compliance (SOC 2, ISO 27001, GDPR)
   - References required

5. Commercial Terms
   - Pricing model requested (per seat, flat, usage-based)
   - Contract term, SLA requirements
   - Payment terms

6. Submission Requirements
   - Format, deadline, point of contact
   - Questions for vendor to answer

7. Evaluation Criteria
   - How proposals will be scored
   - Weight for each dimension
```

### RFP Evaluation Matrix

| Criterion | Weight | Vendor A | Vendor B | Vendor C |
|-----------|--------|----------|----------|----------|
| Functional fit | 25% | | | |
| Technical architecture | 15% | | | |
| Security & compliance | 15% | | | |
| Total cost (3-year TCO) | 20% | | | |
| Support & service | 10% | | | |
| Company stability | 10% | | | |
| References | 5% | | | |
| **Total** | **100%** | | | |

### RFP Anti-Patterns

- **RFPs for commodity purchases.** An RFP for a $500/month email tool wastes everyone's time. Use RFPs for significant, strategic decisions.
- **Too many vendors.** Evaluating 10 vendors comprehensively is unrealistic. Limit to 3-5.
- **Unequal information.** One vendor gets a question answered, others don't. Share Q&A with all vendors equally.
- **Death by requirements.** A 200-item requirements list buries the important ones. Distinguish must-have from nice-to-have.

---

## SLA Design

Service Level Agreements define what the vendor guarantees and what happens if they fail.

### SLA Components

| Component | Definition | Example |
|-----------|-----------|---------|
| **Service Definition** | What exactly is covered | "Core platform API availability" |
| **Uptime Commitment** | % of time service is available | 99.9% uptime (excluding planned maintenance) |
| **Measurement Period** | How availability is calculated | Monthly average, quarterly true-up |
| **Exclusions** | What's not covered | Scheduled maintenance, force majeure, customer-side issues |
| **Credits** | Penalty for missed SLA | 5% credit per 0.1% below target, max 25% |

### Credit Structure

| Uptime % | Credit (Typical) |
|----------|------------------|
| 99.9-100% | No credit |
| 99.0-99.9% | 5% of monthly fee |
| 95.0-99.0% | 10% of monthly fee |
| < 95.0% | 25% of monthly fee + termination rights |

### Beyond Uptime: Multi-Dimensional SLAs

| Dimension | Definition | Typical Target |
|-----------|-----------|---------------|
| **Availability** | Service is accessible | 99.9% (standard), 99.99% (critical) |
| **Performance** | Response times within threshold | P95 < 500ms |
| **Support response** | Time to first response | Critical: < 1hr, High: < 4hrs, Normal: < 24hrs |
| **Support resolution** | Time to resolution | Critical: < 4hrs, High: < 8hrs, Normal: < 5 days |

### SLA Pitfalls

- **Measuring what's easy, not what matters.** Dashboard uptime is easy to measure. API latency at P95, data freshness, and error rates matter more.
- **No measurement transparency.** If you can't independently verify uptime, the SLA is unenforceable. Require a status page and monthly reports.
- **Credits that don't hurt.** A 5% credit on a $1K/month contract is $50. That's not enough to incentivize performance.
- **Ignoring the exit.** If SLA violations accumulate, there should be a termination-for-cause clause with a data migration assistance obligation.

---

## Vendor Scorecards

Scorecards provide ongoing evaluation of vendor performance. They should be reviewed quarterly and factored into renewal decisions.

### Scorecard Template

| Category | Weight | Metric | Target | Actual | Score |
|----------|--------|--------|--------|--------|-------|
| **Service Quality** | 25% | Uptime SLA | 99.9% | | |
| | | Response time (P95) | < 500ms | | |
| **Support** | 20% | P1 response time | < 1hr | | |
| | | Ticket satisfaction | > 4.0/5.0 | | |
| **Security** | 15% | SOC 2 valid | Yes | | |
| | | Pen test results | No critical findings | | |
| **Value** | 20% | Cost variance vs budget | < 5% | | |
| | | Feature delivery vs roadmap | On track | | |
| **Relationship** | 10% | Executive engagement | Quarterly | | |
| | | Escalation responsiveness | < 24hrs | | |

### Vendor Tiering

| Tier | Criticality | Management Cadence | Exit Plan |
|------|-------------|-------------------|-----------|
| **Tier 1: Strategic** | Core to business operations | Monthly review, quarterly business review, annual contract | Maintained, updated semi-annually |
| **Tier 2: Important** | Significant but replaceable | Quarterly performance review | Maintained, reviewed annually |
| **Tier 3: Operational** | Useful but non-critical | Annual review | Documented, not maintained as active plan |
| **Tier 4: Commodity** | Easily replaceable | Monitor via SOW | No formal exit plan needed |

### Vendor Scorecard Pitfalls

- **No consequence for poor scores.** If a vendor consistently scores low but keeps the contract, the scorecard is theater. Tie scorecards to renewal decisions.
- **Annual review cadence for everyone.** Annual review is too infrequent for critical vendors and too frequent for commodity vendors. Match cadence to criticality.
- **Scoring without conversation.** Don't just send the scorecard. Review it with the vendor. Their response to the data is as informative as the data itself.

---

## Vendor Management Heuristics

| Heuristic | Why |
|-----------|-----|
| **Never be a vendor's only customer.** | If they go under, you're stranded. |
| **Always have an exit plan.** | The cost of switching is highest when you can't switch. Know the exit cost before you sign. |
| **Data portability is non-negotiable.** | Ensure you can export your data in a standard format at any time. |
| **Negotiate the renewal before signing.** | Know the renewal process and escalation structure. A vendor that's helpful during sales may be adversarial during renewal. |
| **Vendor concentration is risk.** | If one vendor accounts for > 30% of a capability, you have concentration risk. Identify alternatives. |
| **The cheapest option is rarely the cheapest.** | Hidden costs (integration, training, workarounds) make cheap vendors expensive. Calculate real TCO. |
| **Multi-year contracts need price protection.** | Lock in pricing or maximum annual increases. Without protection, you're at the vendor's pricing mercy. |
