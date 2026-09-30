# The six named characters' own street lines: set aside after three reviews (30 September 2026)

Jafar's list of 30 September evening, item 2: "With Ron's tone approved, the
street's lines for the other named characters, in their own voices as their
casting sheets describe, within the approved story. Through the gate."

Darren, Sheila, Alison, Ada, Father Walsh and June were written three times
(about 600 lines each time) and failed a fresh blind reviewer each time on
obvious faults, so by the two-tries rule the work is set aside. The street
keeps the shared lines (StreetVoice.cs) for these six, as before; Ron keeps his
approved own lines. six-voices-v3.py is the third version, written bank by
bank for all six side by side (the method note's advice), kept only as the
record.

## Why the method failed (the third review's findings, and what they say about the method)

1. **Every line to Tom is said unprompted as he walks past** (GossipDirector.cs,
   within 7 m). A bank named "refuses" still plays with nothing asked, so five
   of six sets refused a request he never made. The banks were written from
   their names, not from the moment that plays them.
2. **These six meet each other, not strangers.** On weekdays at noon Darren,
   Sheila, Ada and Alison are all at the fish market front; Walsh and Ada share
   Ada's step every day from one to two. Their everyday openers and replies are
   heard against each other, so an opener no reply can follow ("Where are you
   off to?"), or a reply that only follows "How are you?" ("Grand, thanks"), is
   heard at once.
3. **Six sets written for one taxonomy converge.** Even side by side, whole
   banks said the same thing four to six times (the nephew in "faint", "it's
   over" when Mickey's arrangement ends, "just the cabs", "get that looked at").
   Sheila and Ada, two different women, came out as one.
4. **Some banks never play for some people**: night lines for people whose day
   ends by six; Sheila's week-end lines, which the design never shows.
5. **What a person may know** (Alison and "after ten", from Ron's terms to Tom;
   what the street says of Mickey, which Jafar kept from Alison and June) was
   checked by hand, and missed.

## What a next attempt would do differently

- Write only the banks that play for that person, at the places and hours their
  routine puts them (production/specs/hook-cast.json), for the people they
  actually meet there.
- Write the lines as exchanges between the people who meet (Ada and Walsh at
  the step; the four at the fish market), not as separate openers and replies.
- Give each person a handful of situations they would really remark on unprompted,
  rather than every bank the street has, and let the shared lines cover the rest.
- A machine check before the reviewer: the same idea in three mouths in one bank,
  a question with no reply that answers it, a line naming what the person does
  not hold (StreetFacts.Held).
