# Cloud Platforms — Reference

## AWS

- **Core services:** VPC (subnets, route tables, NAT, security groups, NACLs, VPC peering, Transit Gateway), EC2 (instances, AMIs, auto-scaling, launch templates, spot), EKS (managed K8s, node groups, Fargate, IRSA), S3 (buckets, versioning, lifecycle, replication, presigned URLs), IAM (users, roles, policies, instance profiles, OIDC), Route53 (DNS, alias records, health checks, routing policies)
- **Common patterns:** Shared VPC (central networking team), multi-account (Control Tower, Organization, SCPs), IRSA for EKS pod IAM, S3 backend for Terraform state (bucket + DynamoDB lock), CodeBuild/CodePipeline for CI, CloudFront for CDN

## GCP

- **Core services:** VPC (subnets, firewall rules, Cloud NAT, VPC peering, Shared VPC), GKE (K8s, node auto-repair/auto-upgrade, Workload Identity for pod IAM), Cloud Storage (buckets, nearline/archive, object lifecycle), IAM (roles, custom roles, service accounts, Workload Identity Federation), Cloud DNS (managed zones, DNS forwarding, policy-based routing)
- **Common patterns:** Shared VPC (host project + service projects), workload identity federation (no static keys), Artifact Registry, Cloud Build CI, Terraform state via Cloud Storage

## Azure

- **Core services:** VNet (subnets, NSGs, Azure Bastion, VPN Gateway, VNet peering), AKS (K8s, node pools, managed identity, Azure AD integration), Blob Storage (containers, tiers, lifecycle, Azure Files), RBAC (roles, custom roles, managed identities, service principals), DNS (public/private zones, alias records, Azure DNS Private Resolver)
- **Common patterns:** Hub-and-spoke networking (central firewall), managed identity for pod IAM (AKS with aad-pod-identity), Terraform state via Azure Storage, Azure DevOps pipelines

## Multi-Cloud and Abstraction

- **Abstraction layers:** Terraform/OpenTofu providers — write once, target any cloud (with provider-specific variance). Pulumi similarly abstracts. Crossplane for K8s-native cloud resource provisioning
- **Governance cost:** State isolation per cloud, IAM duplication per provider, network egress charges (Free Tier per cloud but real cost at scale), skills distribution across cloud teams
- **When multi-cloud is worth it:** Regulatory (data residency), avoiding single-vendor lock-in for critical few services (object storage, K8s), acquisition integration. It is NOT a cost-savings strategy.
- **Cost governance:** Budget alerts (each cloud), tagging policies (`CostCenter`, `Environment`, `Owner`), right-sizing, reserved instances/committed use discounts, spot/preemptible for batch, storage tier policies
