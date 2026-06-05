# Stakeholder Communication

Different audiences need different information in different containers. The skill of a PM is not just knowing what to say — it's knowing what to say to whom.

## To Executives

### The Format

```
RECOMMENDATION: [one sentence]
WHY: [2-3 sentences]
WHAT WE NEED: [specific ask, with deadline]
BAD NEWS: [if any, surfaced early]
```

### The Rules

**Lead with the recommendation.** Executives don't need to walk through your analysis to get to your conclusion. Give them the answer first. If they want the methodology, they'll ask.

**Surface bad news early.** Before it becomes a crisis. An exec who hears about a slip from a customer before hearing it from you has already lost trust. The format:

> We're going to miss the [date] launch for [feature]. We caught this [when]. The root cause is [specific — no blame]. Here's what we're doing: [plan]. We'll know more by [date].

**No decisions hidden in status reports.** If you need a decision, make it a separate request. Don't bury "by the way, should we..." in a weekly update.

**Include the counterargument.** If you're recommending option A, briefly say why someone might pick option B and why you chose A anyway. It pre-empts the question and shows you considered alternatives.

### Anti-patterns

- **Deck-first thinking.** You don't need slides to communicate. A well-structured paragraph is faster to read and harder to misinterpret.
- **The twenty-slide tour.** You explored options A, B, C, and D. Tell them you chose A and why. Don't walk them through each option.
- **Optimism bias.** "We might make up the time" is not a plan. Give them the current forecast, not the hope.

## To Engineers

### The Format

A spec document (see `references/spec-template.md`). But the living communication — day to day — follows different rules.

### The Rules

**Be specific and be honest.** Flag what you know, what you don't know, and which decisions are deferred. Engineers have been burned by PMs who pretend to have answers they don't have.

**Explain the "why" behind priority changes.** Not just "leadership decided" — the actual reasoning and tradeoffs that were considered. Engineers who understand the business context make better technical decisions.

**Don't make commitments on their behalf.** "Engineering said this would take two weeks" is fine. "I told stakeholders it would take two weeks" is a commitment you made without their input.

**Bring constraints early.** Technical, business, timeline — inform engineering before they start designing, not after they've built the wrong thing.

**Flag the open questions.** Every spec should have a section called "Open Questions." Engineers will find them anyway — listing them upfront builds trust.

### Anti-patterns

- **Ticket-taker mode.** "Here's the spec, build it." The best engineering work comes from engaging them in the problem, not just the solution.
- **Scope surprise.** Adding requirements after the estimate is done. If scope changes, re-estimate.
- **No response.** An engineer asks a question about the spec. If you don't answer within 24 hours, you've created a blocker. Answer even if it's "I need to check."

## To Designers

### The Format

Outcome descriptions, not pixel specs.

### The Rules

**Be specific about outcomes, flexible about implementation.** Describe what success looks like in measurable terms without dictating the UI. "Users need to understand which team members are available right now" is a good brief. "We need a green dot next to each avatar" is a bad one.

**Bring constraints early.** Technical, business, timeline. Give designers the constraints before they start exploring, so their work isn't rejected later for reasons outside their control.

**Review as a partner, not an approver.** Frame feedback in terms of user behavior, not personal preference. "This interaction doesn't handle the case where the user hasn't completed onboarding" is useful. "I don't like this shade of blue" is not.

**Protect exploration time.** The same way you protect engineering flow. A designer who has to defend every hour of exploration will stop exploring.

### Anti-patterns

- **"Make it pop."** If you can't describe what's wrong, you probably can't describe what's right either.
- **Skipping the problem space.** Bringing designers in only after requirements are locked wastes their best skill — solving problems in ambiguity.
- **Death by feedback round.** Three rounds of feedback on a design usually means you didn't give clear enough constraints upfront.

## To Customers

### The Format

Listening mode. Ask about the last time. Watch without guiding. Pay attention to hesitation, frustration, workarounds.

### The Rules

**Ask about behavior, not opinions.** "Tell me about the last time you tried to do X" produces truth. "Would you use Y if we built it?" produces politeness.

**Don't defend your product.** If a customer struggles, that's data. If you jump in to show them the "right way," you've lost the signal.

**Promises are debt.** "We'll fix that" is a commitment. "That's interesting — tell me more" is learning. Don't confuse the two.

**Close the loop.** If a customer gave you time for an interview, tell them what came of it. Even if the answer is "we learned it wasn't the right problem to solve." It builds trust for the next conversation.

### Anti-patterns

- **Sales mode.** Your product has flaws. A customer pointing them out is not an attack — it's research data.
- **Solution fishing.** "Would you pay for X?" No one knows until they're asked to actually pay. Ask about their current costs instead.

## To Everyone

| Principle | Why |
|-----------|-----|
| Surface bad news early | Bad news doesn't get better with time |
| Say "I don't know" when you don't | Pretending wastes everyone's time |
| Explain the reasoning, not just the decision | Understanding builds trust |
| Write it down | Verbal agreements have half-lives |
| Follow up with a timestamp | "I'll check" means nothing without a follow-up |
