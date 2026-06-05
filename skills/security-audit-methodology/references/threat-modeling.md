# Threat Modeling

## STRIDE Per Component

For each component in the system, evaluate:

| Threat | What to ask | Example finding |
|--------|-------------|-----------------|
| **S**poofing | Can an actor claim an identity they don't own? | No client certificate validation on mTLS endpoint |
| **T**ampering | Can data be modified in transit or at rest? | Logs written world-writable before ingestion |
| **R**epudiation | Can an actor deny an action they performed? | No audit trail on privilege escalation |
| **I**nformation Disclosure | Can an unauthorized party read protected data? | Stack traces in production error responses |
| **D**enial of Service | Can the system be rendered unavailable? | No rate limiting on token generation endpoint |
| **E**levation of Privilege | Can a limited actor gain unauthorized capabilities? | IDOR in user-to-admin role upgrade path |

## Trust Boundaries

Every data flow crossing a trust boundary is a risk surface. Map:

1. **External → Internal** — user input, webhooks, third-party API calls
2. **Internal → Internal** — service-to-service, pod-to-database, cache-to-application
3. **Internal → External** — outbound webhooks, telemetry export, log shipping

Each boundary crossing needs: authentication, authorization, input validation, output encoding, and rate limiting at minimum.

## Attack Trees

Structure potential attacks as decision trees:

```
Compromise API Key
├── Extract from source code (hardcoded credential)
│   ├── In repo history (git leak)
│   └── In config file (unencrypted config)
├── Intercept in transit (plaintext HTTP, no TLS)
├── Social engineering (developer phishing)
└── Brute force (weak key entropy, no rate limit)
```

Leaf nodes are actionable findings. Internal nodes are preconditions.
