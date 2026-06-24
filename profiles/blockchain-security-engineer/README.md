# Blockchain Security Engineer - Hermes Profile

Blockchain security specialization for Hermes Agent. Reviews smart contracts, wallet flows, protocol architecture, tokenomics, and deployment plans with an adversarial mindset.

## Installation

```bash
git clone https://github.com/magnus919/hermes-profiles.git ~/hermes-profiles
ln -s ~/hermes-profiles/profiles/blockchain-security-engineer ~/.hermes/profiles/
hermes --profile blockchain-security-engineer
```

## Skill Dependencies

| Skill | Provides |
|---|---|
| `artifact-pyramids` | Progressive disclosure output format |
| `security-audit-methodology` | Threat modeling, vulnerability assessment, security architecture review |
| `review-methodology` | Structured review process and evidence handling |

## Good Prompts

```text
Threat model this smart contract system before testnet deployment. Focus on admin powers, oracle assumptions, upgradeability, accounting invariants, and incident response.
```

```text
Review this Octra wallet workflow for private-key handling, local server exposure, RPC assumptions, and unsafe support instructions.
```

## Related Work

For a standalone installable Hermes profile focused specifically on blockchain engineering, see [ChainForge](https://github.com/codegraphtheory/chainforge).

## Output Format

Artifact pyramid. Response is the absolute path to `00-index.md`.
