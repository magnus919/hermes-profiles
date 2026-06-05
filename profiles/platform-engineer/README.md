# Platform Engineer — Hermes Profile

Platform engineering specialization for Hermes Agent. Builds and operates the internal developer platform — CI/CD pipelines, infrastructure as code, container orchestration, service networking, observability, and deployment infrastructure — all delivered as artifact pyramids.

## What This Profile Provides

- **CI/CD & GitOps** — pipeline design for GitHub Actions, GitLab CI, Forgejo CI, Jenkins, CircleCI; GitOps with ArgoCD and Flux; release automation and artifact provenance
- **Infrastructure as Code** — Terraform/OpenTofu module architecture, Pulumi project structure, Ansible role patterns, CloudFormation/CDK design
- **Container Orchestration** — Kubernetes/k3s cluster design, Helm chart conventions, Kustomize overlays, Docker Compose production patterns
- **Service Networking** — Traefik, nginx, and Caddy reverse proxy configuration; Tailscale/Headscale mesh networking; WireGuard topology; service mesh with Istio and Cilium
- **Observability Infrastructure** — Prometheus metric collection and alerting, Grafana dashboards-as-code, Loki log aggregation, OpenTelemetry tracing
- **Secret Management** — HashiCorp Vault architecture, SOPS/age encryption in Git, External Secrets Operator patterns, Sealed Secrets
- **Cloud Foundations** — AWS, GCP, and Azure service architecture; multi-cloud design patterns; cost governance

## Prerequisites

- [Hermes Agent](https://hermes-agent.nousresearch.com/) installed and configured

## Installation

```bash
# Clone the profiles repo
git clone https://github.com/magnus919/hermes-profiles.git ~/hermes-profiles

# Symlink the profile into ~/.hermes/profiles/
ln -s ~/hermes-profiles/profiles/platform-engineer ~/.hermes/profiles/

# Switch to profile (skills are bundled — no separate install needed)
hermes --profile platform-engineer
```

## Quick Start

Once the profile is loaded, give it a platform engineering prompt:

> "Design a CI/CD pipeline for our microservices platform. Include GitHub Actions workflow structure, deployment environments, and GitOps sync strategy for Kubernetes."

The profile will:

1. Identify developer workflows and deployment requirements
2. Design pipeline architecture with environment promotion gates
3. Define GitOps sync strategy and release automation
4. Produce an artifact pyramid at `/tmp/platform-engineering/<project>/00-index.md`

Other example prompts:

- "Design the IaC module architecture for our AWS multi-account setup"
- "Architect a Kubernetes cluster for a multi-service deployment with Helm"
- "Design a service networking strategy for our microservices mesh"
- "Design an observability stack for our container platform"
- "Review our deployment pipeline for reliability and security gaps"

## Skill Dependencies

| Skill | Provides | Load Command |
|-------|----------|-------------|
| `artifact-pyramids` | Three-layer progressive disclosure specification | `skill_view('artifact-pyramids')` |
| `platform-engineering` | Full platform engineering methodology, references, patterns | `skill_view('platform-engineering')` |
| `docker-management` | Container lifecycle, Dockerfiles, Compose stacks, registries | `skill_view('docker-management')` |

### Supporting References

The `platform-engineering` skill bundles extensive reference material:

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

### Recommended Skills

| Skill | When to Use |
|-------|------------|
| `traefik` | Setting up reverse proxy / ingress with Traefik specifically |
| `tailscale` | Designing mesh networking or managing a Tailscale/Headscale tailnet |
| `implementation-planning` | Breaking platform designs into build plans with work breakdown |
| `mermaid-diagrams` | Generating architecture and topology diagrams for documentation |

## Output Format

All output follows the artifact pyramid convention:

```
<output>/
├── 00-index.md              ← Navigation index with SOURCES
├── 01-summary/              ← Architecture decision, pipeline design summary
├── 02-analysis/             ← Trade-off analysis, per-domain evaluation
└── 03-dossiers/             ← Configs, templates, manifests, reference data
```

The response to any caller is the absolute path to `00-index.md`. Not a summary. Not a conversation. A path.

## Verification

A deployed platform-engineer agent should pass these checks:

- [ ] Accepts a platform engineering prompt and produces an artifact pyramid
- [ ] Can design a CI/CD pipeline with environment gates given service constraints
- [ ] Can produce an IaC module architecture assessment
- [ ] Can design a container orchestration deployment strategy
- [ ] Can produce a service networking architecture review
- [ ] Response is the absolute path to `00-index.md`, not a summary
