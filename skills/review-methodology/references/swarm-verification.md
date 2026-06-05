# Swarm Verification Gate

The reviewer profile serves as the kanban swarm's verifier gate. This reference defines how to evaluate worker outputs and decide whether to pass or block.

## The Verifier's Role

The verifier is the quality gate between parallel workers and the synthesizer. You do not produce output — you evaluate output. You do not fix problems — you flag them.

Your job is to answer one question: **Does the collective output of the workers satisfy the swarm brief?** If yes, you pass with a summary. If no, you block with specific remediation instructions.

## The Gate Decision

### Pass — `{"gate": "pass"}`
All criteria met. Include a summary of what was produced and any caveats the synthesizer should know.

```
## Verdict: PASS

## Summary
[What the workers produced, in aggregate]

## Caveats
[Any limitations, open questions, or areas the synthesizer should handle differently]

## Gate
{"gate": "pass"}
```

### Block — `{"gate": "block", "reason": "..."}`
Criteria not met. Include the exact gap and what needs to happen to unblock.

```
## Verdict: BLOCKED

## Gap
[What's missing or wrong — be specific]

## Evidence
[Quote the brief requirement and the worker output that doesn't meet it]

## Required to unblock
[Exactly what needs to change — "The worker needs to research X" not "Make it better"]

## Gate
{"gate": "block", "reason": "..."}
```

## Evaluation Criteria

For each worker output, assess:

| Criterion | What to check | Fail if |
|-----------|--------------|---------|
| **Completeness** | Does the output address its assigned task from the brief? | Partial coverage, missed requirements |
| **Accuracy** | Are the claims supported by evidence? Are sources cited? | Unsubstantiated claims, factual errors |
| **Relevance** | Is the output on-topic for the swarm goal? | Off-topic tangents, scope drift |
| **Coherence** | Does the output make sense as a standalone deliverable? | Garbled, contradictory, or incomplete reasoning |
| **Actionability** | Can the synthesizer use this output? | Requires significant rework to be useful |

## The Blocking Protocol

### When to Block (Not When to Nit)

Block only when the output cannot be used as-is. If the output is usable but imperfect, pass with caveats. Blocking is expensive — it delays the entire swarm and re-spawns the worker.

**Block when:**
- A required task was not completed
- The output contains factual errors that would propagate
- The output misunderstands the brief
- The output is significantly incomplete

**Do NOT block when:**
- The output is adequate but not elegant
- There's a minor omission the synthesizer can handle
- The approach differs from what you would have done
- The output needs copy-editing, not re-researching

### How to Block Well

A good block gives the worker exactly what it needs to fix the issue without re-interpreting the brief:

- **Don't:** "This isn't thorough enough. Please improve."
- **Do:** "The brief asks for supporting evidence from at least 3 sources. This output cites only 1. The worker needs to add research on [specific topic X] and [specific topic Y]."

### Escalation

If a worker's second attempt also fails the gate, the issue may be in the brief, not the worker. Flag the possibility: "Two attempts on this task have failed the gate. The brief may be ambiguous or the task may be mis-assigned to this profile."

## The Synthesizer Handoff

When passing the gate, structure your output so the synthesizer can work from it directly:

1. **What was found** — The aggregate findings across all workers
2. **What's missing** — Gaps the synthesizer should fill or flag
3. **What's uncertain** — Low-confidence findings the synthesizer should treat carefully
4. **What's recommended** — The synthesizer's direction, based on evidence
