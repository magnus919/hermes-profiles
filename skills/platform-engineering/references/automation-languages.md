# Automation Languages — Reference

## Go

- **Use in platform engineering:** CLI tools (Cobra/Viper), Kubernetes operators (controller-runtime), Terraform providers (terraform-plugin-framework), ingress controllers, service mesh sidecars, infrastructure agents
- **Key patterns:** `os/exec` for running system commands, `os/signal` for graceful shutdown, `net/http` for API clients, `cobra.Command` for CLI structure, `viper` for config loading, `retry` patterns via backoff
- **Best practices:** Single binary deployment, cross-compilation (`GOOS=linux GOARCH=arm64`), no runtime dependencies, `go vet` + `staticcheck` in CI, readability over cleverness

## Python

- **Use in platform engineering:** Automation scripts, cloud SDK clients (boto3, google-cloud, azure-mgmt), CI/CD pipeline scripts, configuration validation, integration testing, internal tools
- **Key patterns:** `argparse`/`click` for CLI, `httpx`/`requests` for API calls, `pydantic` for config validation, `pyyaml` for config parsing, `rich`/`click` for CLI output formatting, `pathlib` for file operations
- **Best practices:** Type hints everywhere (mypy strict), `if __name__ == "__main__":` entry point, installable via `pip install` (entry_points in setup.cfg/pyproject.toml), dependency pinning for reproducibility, `--dry-run` flag on all mutating operations

## Bash / POSIX Shell

- **Use in platform engineering:** Bootstrap scripts, CI/CD glue, Dockerfile commands, container entrypoints, developer tool wrappers, provisioning one-shots
- **Key patterns:** `set -euo pipefail` for safety, argument parsing with `getopts` or `while case`, `mktemp` for temp files, `trap cleanup EXIT` for teardown, `${var:-default}` and `${var:?required}` patterns
- **Best practices:** ShellCheck in CI, prefer `[[ ]]` over `[ ]` in Bash, quote all variable expansions, use `printf` over `echo`, keep scripts short (beyond ~100 lines → Python or Go), `set -x` for debugging in development only
