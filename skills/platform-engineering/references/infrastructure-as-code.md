# Infrastructure as Code — Reference

## Terraform / OpenTofu

- **Core concepts:** Resources, data sources, providers, state (local, remote backends), modules, variables, outputs, lifecycle rules (`create_before_destroy`, `prevent_destroy`)
- **State management:** Remote backends (S3 + DynamoDB, GCS, Azure Storage, Terraform Cloud), state locking, state migration, workspaces for env separation, `terraform state` subcommands (mv, rm, pull, push)
- **Module design:** Composition (call smaller modules), version pinning, registry conventions (hashicorp/terraform-google-modules), output minimal surface area, internal vs published modules
- **Advanced patterns:** `for_each`/`count` for dynamic resources, `templatefile` for config injection, file/external data sources for bridge to external systems, provisioners as last resort (remote-exec/local-exec)
- **OpenTofu specifics:** Drop-in Terraform replacement, same HCL syntax, OSS license (no BSL change), `tofu` CLI, supports encryption at rest in state natively, enhanced provider signing

## Pulumi

- **Core model:** Infrastructure as real code — Go, Python, TypeScript, .NET, Java, YAML
- **Key concepts:** Programs (stack definitions), stacks (env instances), resources, components (custom abstractions), providers (Pulumi-native, TF bridge), outputs, config/secret management
- **State:** Pulumi Cloud (managed), self-managed backends (S3, GCS, Azure Blob S3-compatible), state encryption
- **Automation API:** Embed Pulumi in applications (CI/CD, self-service platforms), inline updates, preview + deploy in code
- **Bridge to Terraform:** TF bridge adapter wraps existing TF providers as native Pulumi providers — convenient but adds a layer

## Ansible

- **Core model:** Agentless — SSH/WinRM transport, push-based, YAML playbooks, Jinja2 templating
- **Key concepts:** Inventory (static, dynamic from cloud APIs), modules (idempotent operations), roles (reusable content packages), playbooks (execution order), variables and facts, handlers (notify-based triggers)
- **Best practices:** Role-based layout, vault for secrets, molecule for testing, ansible-lint, `--check --diff` for dry-run, `--limit` for targeted execution
- **Use case in platform engineering:** Day-2 configuration (post-provisioning), OS hardening, agent installation, but generally less suited than Terraform for cloud resource provisioning

## CloudFormation / CDK

- **CloudFormation:** Native AWS IaC — JSON/YAML templates, stacks, nested stacks, change sets, drift detection, stack sets (multi-account, multi-region)
- **CDK (Cloud Development Kit):** CloudFormation as real code (TypeScript, Python, Go, Java, C#) — constructs (L1/L2/L3 abstraction), `cdk synth` → CloudFormation template, `cdk deploy` / `cdk diff`, context, aspects, permissions boundaries
- **CDKTF (CDK for Terraform):** Bridge for Terraform providers in CDK languages — cross-platform between AWS and non-AWS providers
