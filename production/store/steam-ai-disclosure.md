# Steam's AI disclosure: the draft

For the store page and Valve's content survey (ROADMAP, the thirty-minute
build; checklist AI07). Research: production/research/steam-ai-disclosure/NOTE-2026-09-29.md.
Drafted by the town, 29 September. Some answers lock once Valve approves the
game, so this is Jafar's to approve before the first public build. It names
only what the game does today (the Core's AiNotice, ContentRule, SafetyRule,
ClaimCheck and RealWorld, and the relay's limits).

## The public text (the store page's AI block)

> The people of LEDGER's town talk with you live: each reply is written as you
> play by an AI model, Anthropic's Claude, and spoken by a voice made on your
> own computer. Each character is told only what they have seen, heard and
> believe, and every line is checked before you hear it. You can report any
> line in the game.

(62 words.)

## Live-Generated: what is made while the game runs

- **Text:** each character's replies, written by Anthropic's Claude (Haiku 4.5,
  Sonnet 5), through LEDGER's own server. The player's key is never needed, and
  no payment is taken outside Steam.
- **Audio:** those replies spoken by a text-to-speech model on the player's own
  computer, in the cast's voices.

## The guardrails (Valve's field)

Every line a character says live is checked before the player hears it:

1. **The world's content rule.** The game's world holds:
   - no alcohol, no gambling and no children;
   - no prostitution or sexual content;
   - no drugs, no slurs and no cruelty the rule names.

   A line breaking it is never said. (ContentRule, ContentWords)
2. **A safety rule.** No line urging the player towards harming or killing
   themselves is ever said. (SafetyRule)
3. **Only what the simulation knows.** Each character is given only what they
   have seen, heard and believe. A second model checks every specific in a line
   against that. A line claiming what they do not know is written again, and
   failing that, replaced by the character's own "that's all I know". (ClaimCheck)
4. **No real world.** No real make, brand, shop, club, paper, programme or
   public figure, and nothing later than 1992. (RealWorld)
5. **The provider's own rules.** Anthropic's usage policies apply on top of
   ours.
6. **A report button on every reply.** It keeps that line, what the player said
   before it and their note, for the developers. Steam's own overlay report
   button works too, as long as the packaged game keeps the overlay (the
   builder's).
7. **Limits.** Every copy has a daily and monthly allowance of live talk. The
   server stops all calls well below its monthly budget. When talk is paused,
   characters answer in a few fixed words of their own.
8. **Told first.** Before the first conversation, the player is told the town
   talks through an AI model, where their words go (through our server to
   Anthropic), and that Anthropic deletes them within 30 days and does not
   train on them.

## Pre-Generated: what shipped was made with AI help

To be completed by the builder before release, since it covers art and voices:
- any AI-made images or textures;
- the crowd voices and fixed lines recorded with text-to-speech;
- the text of the cast's cards and fixed lines, written with Claude's help and
  approved by Jafar.

## Mature content (the content description)

> Characters answer what you type, and what you say can steer the tone. They
> can be rude, threaten, and talk about crime and violence, as the story does.
> Filters block sexual content, drink, gambling, drugs, slurs, anything
> urging self-harm, and real people or brands.

## For the builder

- Keep the Steam overlay working in the packaged game, so Valve's own report
  button works.
- Never ask a player for their own AI key, or for payment outside Steam.
