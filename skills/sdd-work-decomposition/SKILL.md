---
name: sdd-work-decomposition
description: "SDD work decomposition — translates formal specifications into dependency-aware task plans with per-task acceptance criteria. Owns the mapping from specification to executable work units, producing artifact-pyramid-compliant TASK-PLAN.md outputs. Trigger when a reviewed specification needs to be broken into implementable tasks."
version: 1.0.0
author: Hermes Agent community
license: MIT
metadata:
  hermes:
    tags: [sdd, work-decomposition, task-planning, dependency-analysis, sdd-pipeline]
    related_skills: [sdd-authoring, sdd-verification, sdd-review]
---

# SDD Work Decomposition

Translating a reviewed, approved specification into an executable sequence of tasks with explicit dependencies, per-task acceptance criteria, and integration directives for the implementation agent.

## SDD Pipeline Position

```
SPECIFY → [PLAN] → TASKS → IMPLEMENT → VERIFY
              ↑
        You are here
```

This skill bridges the gap between *what* to build (the spec) and *how* to build it in independent, verifiable units. It produces both the human-readable task plan and the CLAUDE.md / AGENTS.md content that drives the implementation agent.

## Core Principle: Spec Is the Plan

This skill does not invent a plan from scratch. It **extracts** the plan from the specification. The spec already defines the behavior the system must exhibit — each behavior maps to a task. Every task traces to a specific section of SPEC.md. There is no work in the plan that is not required by the spec, and no requirement in the spec that is not addressed by at least one task.

This is what distinguishes SDD decomposition from general-purpose project planning. The planner does not ask "what work needs to happen?" — the spec already answered that. The planner asks "how do we sequence and package this work for safe execution?"

## Artifact-Pyramid Output: TASK-PLAN.md

The task plan follows the artifact-pyramid structure:

| Layer | Content | File |
|-------|---------|------|
| L1 | Phase overview — total task count, critical path estimate, key dependencies, recommended execution order | `00-index.md` (entry point) |
| L2 | Task groups by phase or feature area — dependency graph, per-group acceptance criteria derived from spec sections | Individual `*.phase.md` files |
| L3 | Individual task cards — each with spec-derived ACs, estimated complexity, preconditions, CLAUDE.md directives | `tasks/` directory |
| SOURCES | Cross-reference from each task to the SPEC.md section it implements | Footer of each file |

## Loading Guidance

| Reference | When to load | File |
|-----------|-------------|------|
| Task Decomposition Methodology | Before writing any task plan — patterns for spec-to-task extraction, sizing, atomicity | `references/task-decomposition-methodology.md` |
| Dependency Mapping | Sequencing tasks with real constraints — spec-derived dependency chains, not guesswork | `references/dependency-mapping.md` |
| CLAUDE.md as Spec Layer | After producing the task plan — generating CLAUDE.md directives for the implementation agent | `references/claude-dot-md-as-spec-layer.md` |

| Template | When to use | File |
|----------|-------------|------|
| TASK-PLAN.md | Producing the full task plan from a reviewed specification | `templates/TASK-PLAN.md` |

| Script | When to run | File |
|--------|-------------|------|
| `spec-to-tasks.sh` | After authoring a TASK-PLAN.md — validates every spec requirement has a covering task | `scripts/spec-to-tasks.sh` |

## Trigger Conditions

Invoke this skill when:
- A reviewed, approved specification needs to be broken into executable tasks
- An existing task plan needs restructuring because discovered dependencies invalidated the original sequencing
- Multiple specifications exist for a coordinated release and need cross-spec dependency resolution
- An implementation agent needs a CLAUDE.md or AGENTS.md generated from the spec and task plan

## Decomposition Rules

### Atomicity
Each task must be independently implementable and verifiable. The test: if a task is completed but its acceptance criteria can't be checked until another task also completes, the tasks are not atomic — merge them or redefine their boundaries.

### Spec Traceability
Every task body MUST include a `Spec: -- section X` reference back to the SPEC.md section that defines its requirements. This is not optional metadata — it is the mechanism that prevents scope drift during implementation.

### Task Size
No task should exceed one session of implementation work (typically 30-120 minutes for an AI coding agent, depending on complexity). Tasks larger than this signal that the spec section is too coarse and needs refinement. Decompose the spec section further before decomposing the task.

### Dependency Honesty
Record only real, spec-derived dependencies. A dependency is real when: task B requires task A's output (a function signature, a data structure, a schema, a module interface) that B cannot stub or mock. Dependencies that can be satisfied by a contract or interface definition are NOT real dependencies — define the contract in the spec instead.

### The CLAUDE.md Handoff
After the task plan is complete, this skill generates the CLAUDE.md directives that the implementation agent reads. These directives include:
- Which SPEC.md sections and task plan files to load
- The execution order and dependency constraints
- The acceptance criteria format expected by verification
- The escalation protocol for spec ambiguities
