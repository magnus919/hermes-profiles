# Release Engineering for Infrastructure Artifacts

Release engineering for infrastructure artifacts differs from open source releases. Infrastructure artifacts — container images, Helm charts, Terraform modules, Compose stacks — have different publication patterns, versioning strategies, and verification requirements.

## Artifact Types and Publication Targets

| Artifact Type | Publication Target | Versioning | Verification |
|--------------|-------------------|------------|--------------|
| Container image | Container registry (GHCR, Docker Hub, ECR) | Git SHA + semver tags | Image scan, size check, smoke test |
| Helm chart | OCI registry, chart repo | Chart.yaml version, semver | `helm template` dry-run, install test |
| Terraform module | Git tag, registry | Semver tag | `terraform validate`, `tflint` |
| Docker Compose stack | Git tag | Semver or date tag | `docker compose config`, smoke test |
| Internal package | Private registry (PyPI, npm) | Semver + pre-release label | Build, install, import test |

## Container Image Lifecycle

```
Build → Tag → Scan → Sign → Push → Verify → Deploy
```

| Step | Tooling | Success Criteria |
|------|---------|-----------------|
| Build | `docker build`, `buildkit`, `ko` | Exit code 0, image ID captured |
| Tag | `docker tag` with SHA + semver + "latest" | Tags applied to build image |
| Scan | Trivy, Grype, Snyk | No critical/high CVEs, or exceptions documented |
| Sign | cosign | Signature attached to image |
| Push | `docker push`, `crane` | Registry confirms digest |
| Verify | `cosign verify`, digest comparison | Signature valid, digest matches |
| Deploy | Helm upgrade, kubectl apply, compose up | Pods healthy, endpoint responds |

## Versioning Strategies

| Strategy | When to Use | Example |
|----------|-------------|---------|
| Git SHA only | Development, CI-only artifacts | `sha-a1b2c3d` |
| Semver tags | Public-facing releases, API consumers | `v1.2.3` |
| Date-based | Internal rollups without consumer compatibility | `2026-06-01` |
| Semver + pre-release | Release candidates, staging deployments | `v1.2.3-rc.1` |
| Git SHA + semver | Production — both for traceability and semantics | `v1.2.3-sha-a1b2c3d` |

## Release Gate Checklist

Before promoting any artifact to production:

- [ ] All tests pass (unit, integration, E2E)
- [ ] Security scan passes with no unexcepted critical/high CVEs
- [ ] Image is signed (for containerized deployments)
- [ ] Changelog entry exists for the release
- [ ] Rollback plan documented (previous version, restore command)
- [ ] Smoke test passes against staging
- [ ] Release notes drafted for communication
