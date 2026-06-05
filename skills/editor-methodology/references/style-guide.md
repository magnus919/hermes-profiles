# Style Guide — Author Voice Rules

The single source of truth for voice rules across all editorial passes. Every skill (humanize, voice-check, copy-edit, engagement-review) enforces these. If there's a conflict between this file and a skill, this file wins — it's the canonical reference.

## Universal Voice Rules

These apply to every draft regardless of site:

1. **No emdashes.** Use semicolons, commas, colons, or sentence breaks instead. The emdash is a crutch that AI drafts reach for constantly. Every emdash is a violation in narrative prose.

   **Exceptions:**
   - HTML card data displays use emdashes as visual separators between labels and values (e.g., "Companion — no relay"). These are in `<span>` or `<div>` elements and are left alone.
   - Image caption `<p>` elements with inline styling use emdashes as visual rhythm markers. Check for `style="text-align:center"` to distinguish from prose.
   - Parenthetical emdashes in closing passages (final ~3 paragraphs) that carry essential dramatic emphasis. Read aloud — if a comma flattens the rhythm, restore the emdash.

2. **Oxford commas always.** In every series of three or more items. No exceptions.

3. **US English spellings.** "Neighbors" not "neighbours", "behavior" not "behaviour", "color" not "colour", "organize" not "organise".

4. **Contractions in narrative prose.** "Don't" not "do not" in ordinary sentences. Full-form negatives are only acceptable when doing deliberate rhetorical work: parallel structure, italics emphasis, or thesis-level assertions.

5. **No AI-giveaway phrases.** Flag and replace:
   - "Delve", "dive in", "unpack", "explore" (when not literal)
   - "Furthermore", "Moreover", "In addition", "Additionally"
   - "It should be noted that", "What is interesting is that", "It's worth noting that"
   - "In today's world", "In conclusion", "To summarize"
   - "Game-changer", "paradigm shift", "cutting-edge", "state-of-the-art" (in non-technical contexts)
   - "Thought leader", "industry veteran", "hardworking father of three" (lazy characterization)

6. **No fabricated anecdotes.** If an anecdote would strengthen a section, ask the author for real material. Never draft a hypothetical anecdote with a named character and invented biography.

7. **No internal agent infrastructure references.** No mention of councils, multi-agent debates, subagents, kanban pipelines, or any AI orchestration mechanics in published content.

8. **Lead with problem, not evidence.** The argument comes first. Data and experiments are supporting evidence, not the hook. Don't bury the lede.

## Emdash Replacement Patterns

When replacing an emdash, context determines the replacement:

| Context | Replacement | Example |
|---------|------------|---------|
| Dependent clause | Period or colon | "the reviewer approves — all with a full audit trail" → "the reviewer approves. All with a full audit trail" |
| Parenthetical pair | Commas on both sides | "the system — which was new — handled it" → "the system, which was new, handled it" |
| Explanation | Colon | "the only automatic transition — every other requires a call" → "the only automatic transition: every other requires a call" |
| Conjunction continuation | Remove emdash, keep conjunction | "I decided to do it properly — and write it down" → "I decided to do it properly and write it down" |
| Emphasis break | Period or comma | "no external service — just the database" → "no external service. Just the database" |

**Never blindly replace** `—` with `;` across the whole file. The replacement must be grammatical. Read the sentence aloud after replacement. If the punctuation forces an unnatural pause, it's wrong.

## Site-Specific Voice Profiles

### magnus919.com — Personal-Reflective

**Tone:** Warm, conversational, self-aware. Dry humor. Comfortable with vulnerability.
**Register:** Casual-to-reflective. Contractions throughout. "I" used freely.
**Humor:** Dry wit, self-deprecating when appropriate. Not goofy.
**Transitions:** Conversational. "So what does that mean?" "Here's where it gets weird." "And yet."
**Structure:** Bold lead-ins as topic markers within sections. Short paragraphs. One-sentence paragraphs allowed when they land.
**Visual:** Amber CRT terminal aesthetic. Captions in amber italic beneath images. Info callout boxes via Hugo shortcode.

### groktop.us — Analyst-Sharp

**Tone:** Imperative, statistic-heavy, critical. "Signal" framing for industry moves.
**Register:** Professional but not corporate. Analytical, not academic. Direct commands: "Here's what this means for your org."
**Humor:** Sardonic. Never cozy.
**Transitions:** Assertive. "That's the problem." "Here's the signal." "The math doesn't work."
**Structure:** Case-study based. Data leads the narrative. Bold claims supported by specific numbers.
**Visual:** Vintage steel engraving aesthetic. Parchment/maroon/navy palette.

### rdumesh.org — Community-Technical

**Tone:** Hopeful, edgy, countercultural. DIY zine energy.
**Register:** Community-technical. Accessible to hobbyists and newcomers. Not gatekeepy.
**Humor:** Playful, irreverent toward corporate polish.
**Transitions:** Energetic. "Here's the thing." "And that's where it gets interesting."
**Structure:** FAQ-friendly. Practical. Hardware recommendations with reasoning.
**Visual:** Clean Ghost theme. Inter sans-serif. Light background. No terminal aesthetic.

### southeastme.sh — Minimal

**Tone:** Sparse. Landing page + about only. Not an active content site.
**Register:** Conversational but brief.
**Structure:** Minimal paragraphs. No long-form content.

## Voice Drift Patterns to Watch For

These are the specific, predictable ways voice gets destroyed:

1. **Research-heavy sections drift academic.** Citations pile up, language becomes hedged, the author disappears behind "the literature suggests."
2. **Conclusions turn formal.** The piece has been conversational throughout, then suddenly "In conclusion, this article has demonstrated..." — the whole register shift signals a different author.
3. **Personal anecdotes get smoothed.** A specific memory becomes a generic example. "The time I was stuck in Denver traffic" becomes "when professionals face logistical challenges."
4. **Technical sections lose the reader.** The author writes for peers instead of the blog audience. Jargon increases, examples decrease, the reader is left behind.
5. **Analogies change flavor.** One section uses cooking metaphors, the next uses sports metaphors. The reader's mental model keeps resetting.
6. **Confidence level oscillates.** Declarative claim, then three paragraphs of hedging, then another declaration. The reader can't tell what the author actually believes.

## Verification Command

After any pass that should enforce voice rules, run:

```bash
# Emdash count (should be 0 in prose; only HTML cards/captions exempt)
grep -c '—' <path>

# Full-form negatives in narrative prose
grep -nE '\b(is not|are not|was not|were not|do not|does not|did not|cannot|have not|has not|had not|will not|would not)\b' <path>

# AI-giveaway phrases
grep -niE '\b(furthermore|moreover|in addition|additionally|delve|paradigm shift|cutting-edge|in conclusion|in today.s world)\b' <path>
```
