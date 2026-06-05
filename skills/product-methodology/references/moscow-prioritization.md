# MoSCoW Prioritization

A method for aligning a team on scope for a specific time-boxed delivery. Every item is classified into one of four buckets.

## The Four Categories

### Must Have
Non-negotiable. Without these, the release has no value. If a Must Have slips, the date slips.

**Test:** "If we ship without this, would we regret delaying the whole release?"

**Examples:** Authentication for a login-required product. Payment processing for an e-commerce launch.

**Rules:**
- Must Haves should consume no more than 60% of total capacity
- If everything is Must Have, nothing is Must Have — push back
- Must Haves are the first thing built and the last thing cut

### Should Have
Important but not vital. These deliver significant value and should be included if possible, but the release is viable without them.

**Test:** "If we ship without this, will users notice? (Yes, but they won't leave.)"

**Examples:** Secondary sort options on a search results page. Email notifications for account changes.

**Rules:**
- Should Haves are the first to get descoped when Must Haves overrun
- They should have a clear workaround or fallback
- A Should Have that survives 2+ consecutive releases without being built is probably a Could Have

### Could Have
Nice-to-have. These are the first to cut when time runs short. Including them is a bonus, not an expectation.

**Test:** "If we ship without this, would anyone actively complain?"

**Examples:** Custom themes. Advanced filtering. Keyboard shortcuts.

**Rules:**
- Could Haves are where you put your stretch goals
- Zero shame in cutting every Could Have
- If a Could Have generates repeated stakeholder pressure, it's probably misclassified

### Won't Have (This Time)
Explicitly out of scope. The most important category — it makes the other three meaningful by establishing a boundary.

**Test:** "Are we confident we won't build this even if we finish early?" (If yes, it's a Won't Have. If no, it's a Could Have.)

**Examples:** Cross-platform sync in v1. Admin dashboard for a v1 consumer product.

**Rules:**
- Won't Haves get a reason and a potential timeline ("v2 if we hear demand")
- They protect the team from scope creep by making the boundary explicit
- Revisit every quarter — some Won't Haves become Must Haves as context changes

## The Ratio Rule

| Category | Target capacity |
|----------|----------------|
| Must Have | 60% |
| Should Have | 20% |
| Could Have | 20% |
| Won't Have | (not allocated) |

If your Must Haves exceed 60% of estimated capacity, you have two options:
1. **Cut scope** — move some to Should Have or Won't Have
2. **Extend timeline** — but be explicit that this is the tradeoff

## When to Use MoSCoW vs RICE

| Use MoSCoW When | Use RICE When |
|----------------|---------------|
| Scope is fixed (deadline-driven release) | Effort is fixed (you can build anything, within capacity) |
| You need crisp boundaries for a team | You need defensible priorities for stakeholders |
| Items are all in the same problem space | Items span unrelated domains |
| The team needs a shared understanding of scope | You need a numerical comparison to settle disagreements |

## The Anti-Pattern

**Everything is a Must Have.** This is the most common failure mode. It means nobody trusts that Should Haves will actually get built, so everyone pads their requirements. The fix is to demonstrate that Should Haves really do get built — which means actually cutting something on the Must Have list first.

If a stakeholder insists everything is Must Have, write them all down, show the team's capacity, and ask: "Given we can only deliver 60% of this list, which 40% do you want to cut?" The question reframes the constraint from abstract to concrete.
