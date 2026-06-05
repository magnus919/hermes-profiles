# Container Orchestration — Reference

## Kubernetes and k3s

- **Core objects:** Pod, Service, Deployment, StatefulSet, DaemonSet, Ingress, ConfigMap, Secret, PersistentVolume/PVC, Namespace, RBAC (Role/ClusterRole/RoleBinding/ClusterRoleBinding), NetworkPolicy
- **Lifecycle:** Rolling updates, recreate, canary via flags, blue-green via Services; readiness/liveness/startup probes, preStop hooks, pod disruption budgets
- **Scheduling:** nodeSelector, node affinity/anti-affinity, pod affinity/anti-affinity, taints and tolerations, topology spread constraints, resource limits/requests, QoS classes (Guaranteed/Burstable/BestEffort)
- **k3s specifics:** Lightweight Kubernetes (single binary), embedded etcd (or SQLite), Traefik as default ingress, servicelb, HelmController, local-path-provisioner, useful for edge/IoT/development

## Helm

- **Chart structure:** `Chart.yaml`, `values.yaml`, `templates/`, `charts/` (dependencies), `crds/`, `templates/NOTES.txt`, `templates/tests/`
- **Conventions:** helper templates (helpers.tpl), named templates, required values with `required`, global values for cross-chart values, conditionally-enabled subcharts
- **Lifecycle:** `helm create`, `helm lint`, `helm template`, `helm install --values`, `helm upgrade --install`, `helm rollback`, `helm uninstall`, `helm dependency update`
- **Repos:** ChartMuseum, OCI registries (GHCR, ECR, ACR), `helm repo add/update`
- **Best practices:** Pin dependency versions, set resource limits, use release namespace, separate env values files, enable/disable subcharts via `tags` or `condition`

## Kustomize

- **Core model:** Base + overlays — base sets common config, overlays apply env-specific patches
- **Key directives:** `resources`, `patchesStrategicMerge`, `patchesJson6902`, `configMapGenerator`, `secretGenerator`, `namePrefix`, `namespace`, `commonLabels`, `images`, `replicas`, `vars`
- **Patterns:** Multi-environment (dev/staging/prod), multi-cluster, component-based composition, in-line vs file-sourced patches
- **Integration:** `kustomize build` as input to kubectl or ArgoCD, `kustomize edit` for interactive modification

## Docker Compose (Production Patterns)

- **Production concerns:** Health checks (`healthcheck:`), restart policies (`unless-stopped/always`), resource limits (`deploy.resources.limits`), logging drivers, network isolation (custom networks), volume management (named volumes, bind mounts, tmpfs)
- **Multi-service patterns:** Depends-on with health check wait, init containers, sidecar containers (nginx reverse proxy, log shipper), environment file separation (`.env`, multiple `--env-file`)
- **Orchestration compatibility:** Compose file can be used directly (single host), converted to K8s via `kompose`, or used as a local dev environment matching production topology
