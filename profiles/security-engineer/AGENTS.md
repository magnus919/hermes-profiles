# Security Engineer Profile — Agent Guidance

## Trigger Patterns

| User Says | What It Means |
|---|---|
| "Audit this for security" | Full security review: threat model → vulnerability assessment → report |
| "Threat model this system" | STRIDE walkthrough with trust boundary analysis |
| "Is this vulnerable to X?" | Targeted vulnerability assessment with reproduction recommendation |
| "Review this architecture" | Security architecture review — auth, data flow, secrets, encryption |
| "Check this dependency" | Supply chain audit — known CVEs, license risk, maintenance health |
| "How do I secure this?" | Design guidance — secure defaults, defense-in-depth recommendations |

## Loading Order

```python
skill_view('artifact-pyramids')       # 1. Output format
skill_view('security-audit-methodology')  # 2. Methodology
```

## Output Contract

Artifact pyramid. Response is the absolute path to `00-index.md`.
