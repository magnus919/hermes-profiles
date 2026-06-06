# Data Privacy Framework

## Privacy-by-Design (PbD)

The seven foundational principles, as articulated by Dr. Ann Cavoukian and codified in GDPR Article 25:

### 1. Proactive Not Reactive; Preventative Not Remedial

| Traditional approach | PbD approach |
|---------------------|--------------|
| Respond to breaches after they happen | Anticipate and prevent privacy-invasive events |
| Privacy is a compliance checkbox | Privacy is a design requirement |
| Privacy reviewed at launch | Privacy considered from the first spec |

### 2. Privacy as the Default Setting

Data is automatically protected without the user having to take action:

- **Data minimization**: Collect the minimum data needed
- **Purpose limitation**: Process data only for specified purposes
- **Limited accessibility**: Only authorized personnel can access
- **Limited retention**: Automatically delete data when no longer needed
- **Privacy-preserving defaults**: Opt-in, not opt-out

### 3. Privacy Embedded into Design

Privacy is not bolted on after the fact — it's an integral part of the system:

- Architecture diagrams include data flows and privacy controls
- User stories include privacy acceptance criteria
- Code reviews check for privacy compliance
- Testing includes privacy scenarios

### 4. Full Functionality — Positive-Sum, Not Zero-Sum

Reject the false tradeoff between privacy and functionality. Design for both:

- **Privacy + Security** — Encryption is both a privacy and security measure
- **Privacy + Analytics** — Differential privacy allows aggregate analytics without individual identification
- **Privacy + Personalization** — On-device processing enables personalization without data collection

### 5. End-to-End Security

Privacy depends on security. Full lifecycle protection:

| Stage | Security measure |
|-------|------------------|
| **In transit** | TLS 1.3, mutual TLS, VPN |
| **At rest** | Encryption (AES-256), key rotation, HSM |
| **In use** | Confidential computing, differential privacy |
| **Processing** | Access controls, audit logging, anomaly detection |
| **Deletion** | Cryptographic erasure, secure wipe verification |

### 6. Visibility and Transparency

All stakeholders operate with the knowledge that the system is privacy-assuring:

- **Privacy notice** — Clear, specific, accessible
- **Data flow map** — Where data goes, who touches it, how it's protected
- **Processing records** — Article 30 RoPA (Record of Processing Activities)
- **Incident reporting** — Breach notification process
- **Audit trail** — Log of who accessed what and when

### 7. Respect for User Privacy

User-centric design — keep the individual's interests paramount:

- **Granular consent** — Separate consents for separate purposes
- **Easy exercise of rights** — Access, rectification, erasure, portability
- **Usable privacy controls** — Settings are easy to find and understand
- **User education** — Clear explanations of data practices

## Data Protection Impact Assessment (DPIA)

### When a DPIA is Required (GDPR Art. 35)

A DPIA is mandatory when processing is likely to result in high risk to individuals' rights and freedoms, specifically:

1. Systematic and extensive profiling with significant effects
2. Large-scale processing of special categories of data (health, biometric, genetic)
3. Systematic monitoring of a publicly accessible area on a large scale (CCTV)
4. Other high-risk processing as identified by the supervisory authority

### DPIA Process

```
Step 1: Identify need ──────────────────────────────┐
    │                                                │
    v                                                │
Step 2: Describe processing                         │
    │  (nature, scope, context, purposes)            │
    v                                                │
Step 3: Assess necessity & proportionality           │
    │  (is this the least privacy-invasive way?)      │
    v                                                │
Step 4: Identify and assess risks ───────────────────┤
    │  (likelihood × severity for each risk)          │
    v                                                │
Step 5: Identify mitigations ────────────────────────┤
    │  (reduce risk to acceptable level)              │
    v                                                │
Step 6: Document, sign off, integrate                │
    │  (record decision, obtain approval, implement)  │
    v                                                │
Step 7: Review                                        │
    (periodic review — update if processing changes) │
```

### DPIA Risk Matrix

| Likelihood \ Severity | Low | Medium | High |
|-----------------------|-----|--------|------|
| **High** | Medium risk | High risk | Critical |
| **Medium** | Low risk | Medium risk | High risk |
| **Low** | Low risk | Low risk | Medium risk |

**Response by risk level:**
- **Critical** — Processing cannot proceed as described. Redesign or abandon.
- **High** — Implement additional mitigations. Consult DPO/supervisory authority if mitigations cannot reduce to acceptable level.
- **Medium** — Mitigate; standard controls are sufficient.
- **Low** — Document and proceed.

## Data Mapping (Record of Processing Activities — RoPA)

### Required Under GDPR Article 30

| Field | Description |
|-------|-------------|
| **Controller/Processor** | Name and contact details of each |
| **Purposes of processing** | Why this data is processed |
| **Categories of data subjects** | Whose data (employees, customers, website visitors) |
| **Categories of personal data** | What data (name, email, health data, location) |
| **Categories of recipients** | Who receives it (processors, third parties, authorities) |
| **Transfers to third countries** | Any cross-border data flows and safeguard mechanism |
| **Retention periods** | How long data is kept |
| **Technical/organizational measures** | Security measures applied |

### Data Mapping Methodology

1. **Inventory data collection points** — Every system, form, API, integration, and manual process
2. **Map data flows** — From collection through processing, storage, sharing, to deletion
3. **Identify data elements** — What specific personal data is involved
4. **Classify by sensitivity** — Regular vs special category vs sensitive
5. **Assess legal basis** — What lawful basis applies to each processing purpose
6. **Document retention** — How long each data element is retained
7. **Review periodically** — Annual or on significant process change

## Breach Response

### The 72-Hour Notification Clock (GDPR Art. 33)

```
Breach detected
    │
    v
T+0 hours: Contain and assess
    ├── Isolate affected systems
    ├── Preserve evidence / logs
    ├── Determine scope (what data, who is affected)
    └── Assign breach response lead
    │
    v
T+24 hours: Notify internal stakeholders
    ├── Legal counsel
    ├── Security team
    ├── DPO
    ├── Comms / PR
    └── Executive team
    │
    v
T+48 hours: File (if required) – draft notification
    ├── Likelihood of risk to individuals?
    ├── Categories and approximate number of data subjects
    ├── Categories and approximate number of records
    ├── Likely consequences of the breach
    └── Measures taken or proposed to address the breach
    │
    v
T+72 hours: Submit notification to supervisory authority
    ├── Notify affected individuals (if high risk)
    └── Begin post-mortem
```

**Not required to notify if:**
- Data was encrypted (and key was not compromised)
- Breach is unlikely to result in risk to rights and freedoms
- Affected data was pseudonymized and cannot be re-associated

### Breach Notification Contents (GDPR Art. 33(3))

1. Description of the nature of the breach
2. Categories and approximate number of data subjects concerned
3. Categories and approximate number of personal data records concerned
4. Name and contact details of the DPO or other contact point
5. Likely consequences of the breach
6. Measures taken or proposed to address the breach

## Vendor Privacy Assessment

### Pre-Engagement Checklist

- [ ] Does vendor process personal data on our behalf?
- [ ] Is a DPA/Data Processing Agreement in place?
- [ ] Does vendor have ISO 27001, SOC 2 Type II certification?
- [ ] Is vendor's sub-processor list current and acceptable?
- [ ] What is vendor's breach notification timeline? (GDPR requires 72h — the same requirement flows down)
- [ ] Where is data physically stored? (Jurisdiction matters for transfers)
- [ ] Does vendor have a published data retention and deletion policy?
- [ ] Is vendor's liability cap sufficient for the data risk?
- [ ] What audit rights do we have?
- [ ] Does the contract survive a change-of-control at the vendor?
