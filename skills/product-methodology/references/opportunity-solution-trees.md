# Opportunity Solution Trees

Teresa Torres's framework for connecting desired outcomes to the things you build — without jumping to solutions.

## The Structure

```
Desired Outcome
  └─ Opportunity 1 (customer need, pain point, or desire)
       ├─ Solution A
       │    └─ Experiment 1
       │    └─ Experiment 2
       └─ Solution B
            └─ Experiment 1
  └─ Opportunity 2
       ├─ Solution C
       │    └─ Experiment 1
       └─ Solution D
```

**Top level:** The desired outcome — something you want to be true ("increase trial-to-paid conversion from 12% to 18%").

**Middle level:** Opportunities — customer needs, pain points, or desires that, if addressed, would move the outcome. NOT solutions. "Customers don't understand the pricing page" is an opportunity. "Redesign the pricing page" is a solution.

**Bottom level:** Solutions — things you could build. Each solution is a hypothesis. Below each solution are the experiments you'd run to validate it.

## The Core Practice

### 1. Start with the outcome

Write down the measurable outcome you're trying to move. Be specific. "Improve onboarding" is too vague. "Increase the percentage of users who complete onboarding from 40% to 65%" is specific.

### 2. Discover opportunities

Talk to customers. Analyze usage data. Look for where users get stuck, where they develop workarounds, where they express frustration. Each distinct need is an opportunity node.

**Good opportunity statements:**
- "New users don't understand what value they'll get before signing up"
- "Users can't easily share their work with colleagues"
- "Power users need to automate repetitive tasks"

**Bad opportunity statements (they're actually solutions):**
- "We need a video on the landing page" → solution, not opportunity
- "Users need bulk editing" → solution, not opportunity (the opportunity is "users manage too many items one at a time")

### 3. Generate solutions for each opportunity

For each opportunity, brainstorm 3-5 possible solutions. Include non-technical solutions (process changes, content, partnerships). The best solution may not be code.

### 4. Test the riskiest assumption first

For each solution, identify the assumption that is both most critical and least certain. Design the smallest experiment that tests that assumption.

| Riskiest Assumption | Smallest Test |
|--------------------|---------------|
| Users want this | Landing page with "Notify me" button |
| Technically feasible | Quick prototype |
| Users will understand it | Usability test with 5 people |
| It's better than current workaround | Side-by-side comparison test |

### 5. Update the tree as you learn

Experiments produce evidence. Update each node with what you learned. Prune branches that don't survive contact with reality. Add new opportunities that emerge from learning.

## When to Use

Opportunity Solution Trees are the right tool when:
- The problem space is messy and you're not sure what to build
- Stakeholders are jumping to solutions without validating the problem
- You've built several features that didn't move the outcome
- You need a shared map of the territory to align the team

## The Anti-Pattern: Solutioning too early

The most common failure: someone names an opportunity and the room immediately jumps to "let's build X." The tree structure makes this visible — if your tree has one opportunity and six solutions under it, you skipped discovery. Go back and find more opportunities before evaluating solutions.

## Relationship to Other Frameworks

| Framework | Role |
|-----------|------|
| RICE | Prioritizes which opportunities/solutions to pursue next |
| MoSCoW | Scopes a specific tree branch for a release |
| Customer interviews | Feeds opportunities into the tree |
| Spec template | Documents the selected solution for implementation |
