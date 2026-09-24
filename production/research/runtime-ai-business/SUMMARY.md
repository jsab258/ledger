# How live talk can pay for itself: sell the game once, cap what one copy can cost, and let design decide the bill

The research topic on the business of live AI. The sources are in DELIVERY.md,
the full records in `notes/`, and the numbers you can change are in
`runtime-ai-business-model.xlsx`. Written 24 September.

## The short answer

**Charge once for the game. Include a generous amount of live talk with every
copy, counted on our own server. When a player uses it up, the street carries
on with written lines and the brush-off you already ruled for a dropped
connection.** Offer an optional mode where enthusiasts plug in their own key
for unlimited talk. Later, add a mode where capable cards run the talk
themselves.

That is the one shape that puts a ceiling on what any player can cost us. At
the placeholder cost of 14 cents an hour, a 40-hour allowance costs at most
$5.60 per copy, out of the $17.49 we keep from a $24.99 sale.

## What the research found

**Nobody publishes what live AI costs them per hour of play.** The only hard
numbers are totals. AI Dungeon spent about $200,000 a month at its peak, "about
the same as payroll", and halved it by moving to cheaper models. So our own
measurement from the slice will be the best evidence anyone has.

**Every game that offered unlimited live talk for one price either had a rich
backer or moved to cheaper or local models.**
- Suck Up! capped play at about 40 to 50 hours per purchase, then dropped the
  cap at release, and players say the AI got much worse.
- Vaudeville, a detective game like ours, moved to a model on the player's own
  PC because of the bills and the outages.
- Charging extra per conversation on top of the price didn't survive anywhere
  it was tried.
- Monthly subscriptions work for AI chat products, not for games. Steam
  itself calls them "not a fully supported feature".

**The price of our model isn't falling.** A given level of capability gets 5
to 13 times cheaper a year, but only by switching to whichever company is
cheapest that month. Anthropic's small model went from 25 cents to $1 for the
same amount of reading in about two years. So the safe plan is today's price, and a
saving only arrives if we can switch models.

**The stores mostly add requirements rather than forbid things.**
- Steam: tell players the game uses live AI, describe the safeguards, and let
  players report bad output.
- Anything sold inside the game goes through Steam's own payment system.
- Ads are banned.
- Microsoft has the same kind of rules. Sony and Nintendo publish nothing.
- EU law has required telling players they're talking to an AI since August.

**The server between the game and the model is cheap:** $5 to $100 a month
even at 200,000 players. What needs care is Anthropic's monthly spending cap.
At the cap, every character goes silent until the next month, so our server
needs its own stop well before it.

**Heavy players drive the bill.** The average player plays three to four
times as long as the typical one. With no cap, a player who plays 120 hours at
36 cents an hour costs us $26 more than they paid.

## What money should decide

These choices set the bill, in order of how much they move it:

1. **How much of the talk is written ahead.** Every share of talk that becomes
   written barks, remarks and stock replies comes straight off the bill. It is
   also what keeps the street alive after the allowance runs out.
2. **Whether line-writing can run on the player's card.** Writing the line is
   about 70% of the cost. That is the blind test already queued on the
   checklist.
3. **The cost of each call.** How long the character briefings are, whether
   the unchanged part of each request is billed at the cheaper reused rate,
   and how many calls an hour. The slice's measurement settles this.
4. **Being able to switch models**, so future price drops reach us.
5. **The size of the allowance**, set once the measured cost is known.

## The spreadsheet

Change the blue numbers on the Inputs sheet. The cost per hour is a yellow
placeholder, 14 cents, until the slice measures ours. The Models sheet shows
what each business model earns or loses on a typical, a heavy and an average
player. The Grid sheet shows where selling once, with no allowance, breaks.

## Required whatever we choose

- A way for players to report bad output.
- The notice that they're talking to an AI.
- The safeguards description for Steam.
- Our content rule enforced on what characters say live.
- The server's own spending stop.
