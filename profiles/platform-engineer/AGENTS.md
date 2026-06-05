# Platform-Engineer Profile — Agent Guidance

This document is for AI agents that interact with or consume outputs from the platform-engineer Hermes profile.

## Trigger Patterns

Load this profile when the user asks for any of the following:

| User Says | What It Means |
|---|---|
| "Design a CI/CD pipeline for..." | Full engagement: workflow design → GitOps sync → release strategy → pyramid |
| "Cut a release for this service" | Full release lifecycle: version bump → build → scan → tag → push → deploy → verify |
| "Promote this image to production" | Image promotion: security gate → registry promotion → deploy → smoke test |
| "Design IaC modules for..." | Module architecture, state strategy, provider selection, cross-env patterns |
| "Architect a Kubernetes cluster for..." | Cluster topology, node sizing, Helm/Kustomize layout, RBAC, networking |
| "Design a service networking strategy" | Mesh topology, ingress/egress, TLS, mTLS, ACLs, zero-trust segments |
| "Design an observability stack" | Metric/trace/log strategy, storage sizing, retention, alert routing |
| "Set up secret management for..." | Vault architecture, auth methods, SOPS workflow, External Secrets patterns |
| "Review our deployment pipeline" | Pipeline audit: security, reliability, speed, governance gaps |
| "Design a platform self-service capability" | API-first design, golden paths, developer onboarding, portal integration |
| "Help me choose a CI/CD / IaC / orchestrator" | Decision framework: team size, cloud, K8s maturity, migration path |

## Loading Order

When starting an engagement, load the core skills:

```python
skill_view('platform-engineering')            # Methodology index and references
skill_view('artifact-pyramids')               # Output contract specification
```

Then load reference files on demand based on the specific engagement:

| Engagement Type | References to Load |
|----------------|-------------------|
| CI/CD Design | `references/ci-cd-pipelines.md` |
| Container Orchestration | `references/container-orchestration.md` |
| IaC Module Design | `references/infrastructure-as-code.md` |
| Service Networking | `references/service-networking.md` |
| Observability Stack | `references/observability.md` |
| Secret Management | `references/secret-management.md` |
| Cloud Architecture | `references/cloud-platforms.md` |
| Automation Scripting | `references/automation-languages.md` |

If the engagement involves specific tools, also load their dedicated skills:

```python
skill_view('docker-management')               # Container lifecycle (Compose, Dockerfiles)
skill_view('traefik')                          # Reverse proxy and ingress (if Traefik)
skill_view('tailscale')                        # Mesh networking (if Tailscale/Headscale)
skill_view('implementation-planning')          # Work breakdown (if building from plan)
skill_view('mermaid-diagrams')                 # Architecture diagrams (for documentation)
```

## Output Contract

The profile produces platform engineering documentation as an artifact pyramid. The response to the caller is always the **absolute path to `00-index.md`** at the pyramid root.

### Expected Structure

```
<output>/
├── 00-index.md              ← Navigation index with SOURCES
├── 01-summary/
│   ├── architecture-overview.md  ← Design choice, pipeline structure, topology
│   ├── trade-off-summary.md      ← Key trade-offs and decisions
│   └── recommendations.md        ← Key findings and next actions
├── 02-analysis/
│   ├── per-domain-analysis.md    ← Domain-by-domain evaluation
│   ├── comparison-matrix.md      ← Tool/approach/cloud comparison
│   └── security-review.md        ← Supply chain, secrets, network security
└── 03-dossiers/
    ├── pipeline-configs.md       ← CI/CD workflow definitions
    ├── infrastructure-modules.md ← IaC module patterns
    ├── helm-charts.md            ← Chart templates and patterns
    ├── network-configs.md        ← Traefik/nginx/Caddy configurations
    ├── acl-policies.md           ← Tailscale ACLs, network policies
    └── monitoring-configs.md     ← Prometheus rules, dashboard definitions
```

### Cross-Reference Rules

1. **Pipeline designs must reference developer workflows** — every stage ties to a specific team need
2. **Infrastructure designs must reference trade-offs** — every choice documents why this approach over alternatives
3. **Security recommendations must reference vendor docs** — every claim about a vulnerability or mitigation has a source
4. **SOURCES sections at every layer** — absolute path references with descriptions
5. **All examples use synthetic data** — no real hostnames, domains, IPs, or credentials

## Handoff Protocol

1. **The pyramid IS the handoff.** Close with the path. Do not summarize.
2. If the engagement is multi-phase, each phase produces its own pyramid. The L3 dossiers of phase N serve as context for phase N+1.
3. Partial pyramids are acceptable. If only CI/CD design is requested, produce only the pipeline layers.

## Supporting References

| Reference | File |
|-----------|------|
| CI/CD Pipelines | `references/ci-cd-pipelines.md` |
| Container Orchestration | `references/container-orchestration.md` |
| Infrastructure as Code | `references/infrastructure-as-code.md` |
| Service Networking | `references/service-networking.md` |
| Observability | `references/observability.md` |
| Secret Management | `references/secret-management.md` |
| Cloud Platforms | `references/cloud-platforms.md` |
| Automation Languages | `references/automation-languages.md` |

Load these with `skill_view('platform-engineering', file_path=<path>)` when depth is needed.

## Related Profiles

The platform-engineer profile is designed to work alongside:

- **site-reliability-engineer** — sister profile. Handoff: platform engineer produces pipeline design and deployment infrastructure; SRE owns post-deployment reliability (SLOs, error budgets, incident response). The pipeline artifact pyramid from platform-engineer serves as context for SRE's reliability assessment.
- **technical-architect** — receives infrastructure constraints from platform designs. Provides architecture context (system boundaries, integration patterns). Handoff: pyramid path.
- **implementation-planner** — consumes pipeline specs, infrastructure module designs, and deployment strategies for build plans and work breakdown.
- **security-engineer** — coordinates on secret management architecture, supply chain security, vulnerability scanning integration into pipelines, and network policy enforcement.
- **product-manager** — translates business priorities into platform investment decisions. The platform engineer explains platform capability trade-offs and developer productivity data.
- **orchestrator** — routes platform engineering tasks during multi-agent workflows.
