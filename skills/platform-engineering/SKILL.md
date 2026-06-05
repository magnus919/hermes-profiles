---
name: platform-engineering
description: "Infrastructure as code, CI/CD, container orchestration, service networking — methodology and reference patterns for building and operating internal developer platforms."
author: Hermes Profiles
license: MIT
---

# Platform Engineering

Core methodology and reference library for platform engineering work. This skill does not execute operations itself — it provides the frameworks, patterns, and reference material that a platform-engineer profile loads on demand.

## When to Load

Load this skill when the task involves:

| Trigger | What's Needed |
|---------|---------------|
| Design a CI/CD pipeline | Pipeline structure, GitOps sync strategies, release automation |
| Infrastructure as code plan | Terraform/OpenTofu module patterns, state management, Pulumi/Ansible patterns |
| Container orchestration design | K8s pod lifecycle, Helm chart conventions, Kustomize overlays, Docker Compose |
| Service networking / mesh | Traefik/nginx/Caddy config, Tailscale/Headscale ACL, WireGuard, service mesh |
| Observability strategy | Prometheus rules, Grafana dashboards-as-code, Loki logging, tracing |
| Secret management design | Vault, SOPS, External Secrets Operator patterns |
| Cloud architecture assessment | Multi-cloud patterns, provider foundations, cost governance |
| Deployment pipeline review | End-to-end delivery pipeline audit, release engineering patterns |

## Loading Order

```
skill_view('platform-engineering')          # This — methodology index
skill_view('artifact-pyramids')              # Output contract
skill_view('docker-management')              # Container lifecycle (if needed)
skill_view('traefik')                        # Reverse proxy (if needed)
skill_view('tailscale')                      # Mesh networking (if needed)
skill_view('implementation-planning')        # Work breakdown (if needed)
```

Then load domain-specific references from this skill:

```
skill_view('platform-engineering', file_path='references/ci-cd-pipelines.md')
skill_view('platform-engineering', file_path='references/infrastructure-as-code.md')
# ... etc per domain
```

## Reference Files

| Reference | Purpose |
|-----------|---------|
| `references/ci-cd-pipelines.md` | GitHub Actions, GitLab CI, Forgejo CI, Jenkins, CircleCI; GitOps with ArgoCD/Flux; release automation |
| `references/container-orchestration.md` | K8s/k3s, Helm chart conventions, Kustomize overlays, RBAC patterns, Docker Compose production patterns |
| `references/infrastructure-as-code.md` | Terraform/OpenTofu module design, state backends, Pulumi project structure, Ansible roles, CloudFormation/CDK |
| `references/service-networking.md` | Reverse proxy config (Traefik, nginx, Caddy), Tailscale/Headscale ACL, WireGuard topology, service mesh (Istio, Cilium) |
| `references/observability.md` | Prometheus recording rules/alerting, Grafana dashboards-as-code, Loki log aggregation, OpenTelemetry tracing |
| `references/secret-management.md` | HashiCorp Vault auth/policies, SOPS/age encryption in Git, External Secrets Operator, Sealed Secrets |
| `references/cloud-platforms.md` | AWS/GCP/Azure foundational services, multi-cloud design, cost governance, provider abstraction |
| `references/automation-languages.md` | Go CLI patterns, Python SDK integration, Bash bootstrap/conventions for platform tooling |

## Output Contract

The profile using this skill produces artifact pyramids. The response to any caller is the absolute path to `00-index.md`. See `artifact-pyramids` skill for the specification.

## Design Principles

1. **The platform is a product.** Internal developers are your customers. Their productivity, satisfaction, and cognitive load are the primary metrics.
2. **Golden paths, not golden cages.** Provide paved roads for common workflows but allow escape hatches. Make the right thing easy, not the wrong thing impossible.
3. **Reduce cognitive load.** Abstract infrastructure complexity. Developers should not need to understand Kubernetes internals or Terraform state management to deploy their service.
4. **Everything as code.** Infrastructure, configuration, pipelines, and policies are version-controlled, reviewed, and reproducible. Git is the single source of truth.
5. **Self-service over tickets.** Every manual handoff between teams is a bottleneck. If a developer needs another team to deploy, the platform is incomplete.
6. **Automation is the default.** If a process can be automated, it must be. Manual operations are toil — tax on the organization.
7. **Observability is infrastructure.** Logs, metrics, traces, and dashboards are platform contract, not optional extras. Every service gets them by default.
8. **Security is built in, not bolted on.** Supply chain security, secret management, vulnerability scanning, and policy enforcement are platform responsibilities.
9. **API-first design.** Everything the platform does should be accessible via API — enabling automation, self-service portals, and CLI tools.

## Related Skills

- `artifact-pyramids` — output contract specification
- `docker-management` — container lifecycle and Compose
- `traefik` — reverse proxy and ingress configuration
- `tailscale` — mesh networking and ACL policies
- `implementation-planning` — work breakdown and dependency ordering
- `mermaid-diagrams` — architecture diagram generation
- `site-reliability-engineering` — sister domain (post-deployment reliability)
