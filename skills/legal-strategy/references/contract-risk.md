# Contract Risk Assessment

## Key Contract Provisions

### Indemnification

The indemnification clause determines who bears the cost of a third-party claim arising from the contract.

| Type | What it covers | Who bears risk |
|------|----------------|----------------|
| **Mutual indemnification** | Each party indemnifies for claims arising from their own breach/negligence | Balanced |
| **One-way indemnification** | Only one party indemnifies the other | Unbalanced — typically favors the provider |
| **IP indemnification** | Claims that the product infringes third-party IP | Provider bears infringement risk |
| **Data breach indemnification** | Claims from a security incident involving customer data | Party responsible for the breach |

**Negotiation tips:**
- Push for mutual indemnification whenever possible
- IP indemnification should be capped at the same amount as general liability
- Exclude claims arising from customer's modifications, misuse, or combination with third-party products
- Ensure coverage for settlement amounts, not just judgment

### Liability Caps

| Term | Typical range | Strategy |
|------|---------------|----------|
| **Liability cap** | 1x to 12x monthly or annual fees | Customer: push for multiple of fees. Provider: push for single digit multiple |
| **Uncapped exceptions** | IP infringement, breach of confidentiality, death/injury, fraud | Never cap these |
| **Mutual vs one-sided** | Some caps apply only to one party | Push for mutual caps with same exceptions |

### The Liability Cap Tiers

| Tier | Multiplier | Context |
|------|------------|---------|
| Enterprise deal, strong negotiating position | 12x annual fees | Customer-side enterprise procurement |
| Mid-market | 6x annual fees | Balanced negotiation |
| SMB / standard terms | 1x-3x annual fees | Provider's standard terms |
| Uncapped | N/A | Only for IP, confidentiality, fraud |

### Force Majeure

| Element | Description | Key issue |
|---------|-------------|-----------|
| **Events** | Acts of god, war, terrorism, pandemic, government action, labor strike | Is pandemic explicitly included? (Post-COVID: yes) |
| **Effect** | Performance becomes impossible, illegal, or impracticable | "Impossible" is narrower than "impracticable" |
| **Duration** | How long until termination rights arise | 30-90 days is typical |
| **Obligation** | Notice requirement, mitigation duty | Must notify within X days of triggering event |
| **Exclusions** | What is NOT force majeure | Economic hardship, market changes, supplier failure (unless force majeure) |

**Post-COVID update:** Force majeure clauses are now reviewed carefully. Ensure pandemics are explicitly included (many pre-2020 contracts excluded them). Some contracts now have a separate "business continuity" or "pandemic" clause.

### Limitation of Liability

The limitation of liability clause excludes certain types of damages:

| Excluded damages | Typical scope | Negotiation strategy |
|-----------------|---------------|---------------------|
| **Consequential damages** | Indirect, incidental, special, punitive | Never exclude damages for breach of confidentiality, IP infringement, or data breach |
| **Lost profits** | Revenue the customer expected to generate | Exclude for everyone — too speculative |
| **Lost data** | Cost of recreating or recovering data | Provider should exclude; customer should carve out if provider destroys customer data |

### Data Protection / Privacy Addendum

Must include:

1. **Data Processing Agreement (DPA)** — Required under GDPR Art. 28
2. **Data Security Schedule** — Specific security measures, encryption standards, breach notification timeline
3. **Data Transfer Mechanism** — SCCs or adequacy decision for cross-border transfers
4. **Data Retention and Deletion** — Timeframes for deletion after contract termination
5. **Sub-processor List** — Approved sub-processors, change notification, objection rights
6. **Audit Rights** — Customer's right to audit provider's security practices

## Contract Lifecycle

### Pre-Signature Checklist

- [ ] Scope of work clearly defined (SOW or exhibit)
- [ ] Pricing and payment terms unambiguous
- [ ] Term, renewal, and termination provisions clear
- [ ] Liability cap (mutual, with appropriate exceptions)
- [ ] Indemnification scope matches risk allocation
- [ ] DPA/data protection addendum attached (if processing personal data)
- [ ] Governing law and dispute resolution specified
- [ ] Confidentiality obligations mutual
- [ ] IP ownership: each party retains its pre-existing IP; deliverables IP assigned to customer
- [ ] SLA (if applicable) with service credits

### Post-Signature Management

| Phase | Action | Owner |
|-------|--------|-------|
| **Day 1** | File signed contract in repository, assign to contract manager, set renewal reminder | Legal ops |
| **Ongoing** | Track obligations (reporting, compliance, renewal deadlines) | Contract manager |
| **At renewal** | Review performance against SLA, negotiate improvements, update terms | Legal + Business |
| **At termination** | Confirm data deletion, final payment, close-out obligations | Legal ops |

## Contract Risk Scoring

| Risk level | Characteristics | Review requirement |
|------------|----------------|--------------------|
| **Low** | Standard terms on provider's paper, minimal data processing, low value | Fast-track, no redlines |
| **Medium** | Custom terms, moderate data processing, some redlines expected | Counsel review, key terms only |
| **High** | Customer's paper, aggressive redlines, high-value, significant data processing | Full counsel review, exec approval |
| **Critical** | Uncapped liability, one-way indemnification, unusual data handling | External counsel, board approval |
