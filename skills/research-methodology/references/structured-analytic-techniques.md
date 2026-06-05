# Structured Analytic Techniques

Techniques adapted from intelligence analysis to systematically evaluate evidence, challenge assumptions, and avoid cognitive bias.

## Analysis of Competing Hypotheses (ACH)

Use when you have multiple possible explanations for the same evidence and need to decide which is most credible.

### Step-by-Step

1. **Identify all hypotheses.** Brainstorm every plausible explanation for what you're seeing. Include the null hypothesis (nothing unusual is happening). Do NOT pick a favorite yet.

2. **List evidence and assumptions.** For each hypothesis, note what would support it, what would contradict it, and what assumptions it requires.

3. **Build a matrix.** Rows = evidence items. Columns = hypotheses. For each cell, mark:
   - **CC** (consistent): This evidence supports this hypothesis
   - **IC** (inconsistent): This evidence contradicts this hypothesis
   - **N/A** (not applicable): This evidence doesn't bear on this hypothesis

4. **Work across, not down.** The most important step. For each piece of evidence, evaluate it against ALL hypotheses before moving to the next piece. This prevents confirmation bias toward a single hypothesis.

5. **Count inconsistencies.** The hypothesis with the FEWEST inconsistencies is the most likely — NOT the one with the most supporting evidence. ACH is a refutation tool, not a confirmation tool.

6. **Test sensitivity.** What if a key piece of evidence is wrong? If removing it changes your conclusion, that evidence is a linchpin — verify it.

7. **Report.** Present the conclusion, the rejected alternatives, and the linchpin evidence that drove the decision.

### When to Use ACH

| Good for | Not good for |
|----------|-------------|
| Competing technical explanations | Single-hypothesis verification |
| Evaluating competing vendor claims | Exploratory research |
| Root cause analysis | Routine fact-gathering |
| Contradictory evidence sets | Simple yes/no questions |

## Driving Forces Analysis

Use to understand what's shaping a trend, market, or technology trajectory.

1. **List driving forces.** What factors are pushing in one direction? (Technology advances, regulation, market demand, cost curves)
2. **List restraining forces.** What's holding back change? (Incumbent lock-in, technical limitations, talent gaps, infrastructure debt)
3. **Which forces are accelerating?** Are drivers getting stronger or weaker?
4. **What would change the balance?** What event or discovery would shift the equilibrium?
5. **Two scenarios.** If drivers win → what happens? If restrainers hold → what happens?

## Pre-Mortem Analysis

Use before committing to a research conclusion to identify what could be wrong.

1. **Assume the conclusion is wrong.** Imagine it's six months from now and your research finding turned out to be completely incorrect.
2. **Write the failure story.** What happened? What evidence misled you? What assumptions were wrong? What did you miss?
3. **Identify failure modes.** Which specific evidence items, assumptions, or reasoning steps are most vulnerable?
4. **Harden the analysis.** For each failure mode: what additional evidence would rule it out? What alternative explanation would cover it?

## Indicator / Validator Framework

Use to track whether an ongoing development is trending toward or away from a predicted outcome.

1. **Define observable indicators.** What would you see if the prediction is correct? What would you see if it's wrong?
2. **Assign diagnostic value.** Some indicators are stronger than others. An indicator that would exist ONLY under one scenario is highly diagnostic.
3. **Track over time.** Indicators don't fire all at once. Track which are appearing, which haven't, and which are contradictory.
4. **Update confidence.** As evidence accumulates, adjust your confidence in each scenario.

## Linchpin Analysis

Use to identify which single element your entire conclusion rests on.

1. **Trace the reasoning chain.** Conclusion → supporting evidence → foundational assumptions.
2. **Find the linchpin.** Which assumption or evidence item, if wrong, would collapse the entire conclusion?
3. **Test that specific element.** Don't test random alternatives. Test the linchpin.
4. **Report linchpin confidence separately.** "I'm confident in the conclusion IF [linchpin] holds. Here's what would change if it doesn't."
