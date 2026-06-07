# Wonderer

A lateral exploration profile for Hermes Agent. Given a seed topic, the wonderer explores its periphery — adjacent domains, overlooked angles, unexpected connections — and returns suggestions worth looking into.

Inspired by *Uncommon Genius* by Denise Shekerjian: the creative process cannot be collapsed into method. Breakthroughs come from staying loose, remaining in the divergent phase long enough to let the real shape of a problem reveal itself.

## When to Use

- You're brainstorming a topic and want to know what's adjacent to it
- You have a question but suspect there are angles you haven't considered
- You want to check for unexpected connections between domains
- You need raw material for a synthesis — things worth looking into, not things worth concluding
- You want to stay in the divergent phase before committing to a direction

## When NOT to Use

- You need a deep answer to a specific question (→ use the **researcher** profile)
- You need systematic evidence gathering and source triangulation (→ researcher)
- You need something critiqued or stress-tested (→ **debugger**)
- You're ready to converge and make a decision (→ **product-manager**)

## Installation

```bash
cd ~/.hermes/profiles
ln -s /path/to/hermes-profiles/profiles/wonderer wonderer
```

## Quick Start

```
Tell the wonderer to explore the periphery of [topic].
```

Or more concretely:

```
/wonderer What's adjacent to the concept of "nano SaaS" that I might be overlooking?
```

## Skills

| Skill | Purpose |
|---|---|
| `artifact-pyramids` | Standard output contract — progressive disclosure |
| `wonderer-methodology` | Conditions and patterns for lateral exploration |

## Related Profiles

| Profile | Relationship |
|---|---|
| **researcher** | Goes deep where wonderer goes wide |
| **debugger** | Converges on defects where wonderer expands possibility space |
| **editor** | Sharpen and focus what wonderer found |
| **writer** | Turn wonderer's leads into finished drafts |

## Credits

Inspired by a conversation with sovthpaw on the Nous Research Discord, who described the need for an agent that "wonders about things related to things that you talk about and goes out and randomly searches around those just to expand its suggestions while staying anchored."
