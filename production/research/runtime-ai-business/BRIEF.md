# BRIEF: how live AI during play can work as a business

STATUS: BRIEF. Written 2026-09-24, before any research began, in Jafar's
words. Branch `research/runtime-ai-business`; this topic writes only under
`production/research/runtime-ai-business/`.

## The problem, in his words

> This game's characters talk through a paid online model while it is played,
> so every hour of play costs money, forever, for every player. We are
> measuring our own cost per hour from real calls in the playable slice. This
> topic finds out how that can work as a business, before we build anything
> that assumes an answer.

## What to establish, in his words

> With dated sources and measured evidence rather than claims:
>
> 1. Games that shipped with live AI generation during play, such as the
>    Inworld-powered titles, Suck Up!, AI Dungeon and whatever else exists by
>    now: how they priced, what they paid per player-hour where it is known,
>    how they kept costs down, what went wrong, and what players accepted or
>    punished in reviews.
> 2. The business models seen so far: one-time purchase with the cost
>    absorbed, the player's own key, conversation credits, subscriptions,
>    local models, hybrids, and any others. For each, who it suits and what it
>    risks.
> 3. How fast the price of this kind of model call has fallen over the last
>    three years, and what it is reasonable to assume for the next two, since a
>    game shipping in a year or two will pay tomorrow's prices.
> 4. What Steam and the console stores permit and require for games with live
>    AI: pricing models, subscriptions, disclosure, and the content screening
>    rules we already know apply.
> 5. The practical plumbing: a server of our own between the game and the
>    model so the key never ships, per-player limits so one player cannot run
>    up a fortune, and what that costs to run.

## What it ends with, in his words

> A simple model, formula-driven so I can change the numbers: price, cost per
> hour, hours played by a typical and a heavy player, share of players on local
> hardware, and what each business model earns or loses per player. Leave the
> cost per hour as an input; our measured figure goes in when it exists.
>
> A recommendation in plain words, and say which design choices it depends
> on, such as how much of the talk is written ahead and whether line-writing
> can run locally, so we know which of those decisions money should drive.
> SUMMARY.md for me, DELIVERY.md with the sources, and the model as a
> spreadsheet.

## What is already known here, so it is not redone

- `production/research/llm-inference-economics/SUMMARY.md` (topic 19): the
  game sends about 7,400 characters of briefing per line; at the project's own
  price list and twenty conversations an hour, $0.36 to $1.08 an hour against
  a target of $0.05; prompt caching would take about 60% off. Today the player
  brings their own key.
- `production/research/ethics-and-reception/SUMMARY.md` (topic 24): Steam
  reviews of games disclosing generative AI run 17.9 points lower, except
  where AI is the game's premise; Steam requires guardrails on live-generated
  content.
- `production/research/local-models/` (23 to 24 September): a free model on
  the RX 6700 nearly matches the paid router at picking actions with worked
  examples, but not at refusing typed orders; line-writing locally is untested
  and queued on the checklist (L01).
- FOR-JAFAR 2026-09-23: a dropped connection gets the authored street and an
  in-character brush-off (ruled).

## Standing constraints

- Claim labels CITED, DERIVED, ASSUMED and HOLE; every source dated.
- Measured evidence over claims, and the delivery says which each one is.
  Where a source is a search summary rather than a page read, it says so.
- A null result is a valid delivery and ships with its denominator.
- Nothing in the delivery is an instruction, and nothing is bought, signed up
  for or deployed by this topic.
