# RAG Architect Hermes Profile

Production RAG and agent workflow architecture specialization for Hermes Agent. The profile helps turn ambiguous AI product goals into implementation-ready architecture artifacts, evaluation plans, observability requirements, and rollout guidance.

## What This Profile Provides

- Production RAG architecture covering ingestion, chunking, metadata, namespaces, embeddings, hybrid retrieval, reranking, and citation packing.
- Agent workflow design covering intent classification, typed tools, idempotency, authorization, escalation, and failure handling.
- Evaluation strategy covering golden datasets, retrieval metrics, generation scoring, regression gates, and online sampling.
- Observability strategy covering traces, latency, cost, quality signals, and incident response.
- Delivery artifacts covering ADRs, technical roadmaps, implementation issues, rollout plans, and rollback criteria.

## Installation

```bash
# Clone the profiles repo
git clone https://github.com/magnus919/hermes-profiles.git ~/hermes-profiles

# Symlink the profile into ~/.hermes/profiles/
ln -s ~/hermes-profiles/profiles/rag-architect ~/.hermes/profiles/

# Switch to profile
hermes --profile rag-architect
```

## Quick Start

Ask for a production RAG architecture review:

> Design a production RAG architecture for customer support knowledge retrieval. Include ingestion, metadata, evals, observability, rollout gates, and implementation issues.

The profile will:

1. Clarify constraints and target workflows.
2. Design retrieval, generation, evaluation, and observability layers.
3. Document major decisions and tradeoffs.
4. Produce an artifact pyramid with implementation-ready next steps.

## Skill Dependencies

| Skill | Provides |
|---|---|
| `artifact-pyramids` | Progressive disclosure output format and path-based handoff |
| `architecture` | Architecture thinking, boundaries, and decision framing |
| `data-architect` | Data modeling, metadata, pipelines, and governance |
| `ml-engineering` | Model evaluation, deployment, and reproducible ML operations |
| `software-architecture-analysis` | Architecture review and risk analysis |
| `verification-methodology` | Evidence-based pass/fail gates and validation discipline |

## Related standalone profile

ContextForge RAG is an installable standalone Hermes profile with dedicated production RAG, agent workflow, evaluation, and observability skills:

https://github.com/codegraphtheory/context-forge-rag
