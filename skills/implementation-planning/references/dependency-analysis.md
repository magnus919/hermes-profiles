# Dependency Analysis

## Types of Dependencies

| Type | Description | Example |
|------|-------------|---------|
| **Structural** | Inherent in the architecture. Cannot be eliminated. | API must exist before clients can call it |
| **Discretionary** | A preference or convenience. Can be changed. | Team A wants to finish before Team B starts |
| **Integration** | Shared interfaces between components. | Both teams need the same contract defined |
| **Resource** | Constrained by people or tools. | One person is needed on two critical path tasks |

## The Critical Path

The critical path is the longest sequence of dependent tasks that determines the project's minimum duration. Any delay on the critical path delays the entire project.

**To find the critical path:**
1. Map all tasks and their dependencies
2. Calculate the earliest start and earliest finish for each task
3. Calculate the latest start and latest finish (working backward from the deadline)
4. Tasks where earliest finish equals latest finish are on the critical path

**Warning signs:**
- Multiple critical paths (no slack anywhere — any delay is catastrophic)
- A single person on multiple critical path tasks (bus factor of 1)
- Integration tasks on the critical path (shared interfaces are always risky)
