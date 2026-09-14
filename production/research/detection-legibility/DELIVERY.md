# Topic 12: detection as a legible system

STATUS: SPEC (research delivery). Branch `research/detection-legibility`, from
commit `074f85b`. Written 2026-09-14 by the research lane.

NOTHING IN THIS FILE IS AN INSTRUCTION. No queue item filed, no tile proposed,
no decision record written.

## 0. How to read this file

Claim labels are CITED, DERIVED, ASSUMED and HOLE. Sourcing limit unchanged.
Repository claims name their file and line.

This topic resolves a question I have now raised twice, in the Hitman coverage
audit and again, corrected, in the RDR2 one. Section 1 is the resolution.

## 1. The principle, and it is one sentence

The Hitman audit asked whether the player should be shown, live, who can see
through them and how close they are to being noticed, and flagged a tension with
D12's rule that "NPC minds are never shown as ground truth" and that there is "no
free omniscient read". The RDR2 audit narrowed it, because `Core/Observation.cs`
had already ruled the unaware case: `Awareness.NeitherKnows` is documented as
"THE QUIET HORROR CASE, and the design deliberately gives the player nothing
here, no ghost, no warning."

Thief's light gem answers the rest, and the answer is in its own justification.

CITED (search summary of Sneaky Bastards' "Deep in the Shadows: Thief Design
Analysis Part 1" and the Thief Wiki's Light Gem entry): **"The lightgem serves as
a helper to give players information that they cannot experience themselves,
because they cannot see their own body in a first-person view."**

DERIVED, and it is the line D12 needs: **a readout is legitimate when it restores
information the PLAYER CHARACTER has and the camera denies. It is illegitimate
when it adds information the character does not have.**

Garrett knows whether he is standing in a pool of light. The player, looking out
through Garrett's eyes, does not. The gem gives back what the camera took. It is
not a window into the guard's mind, and Thief's guards are famously opaque:
CITED (search summary of Game Developer's "Building the original Thief's
revolutionary stealth system"), during development "you got confused signals, you
didn't necessarily know what the guard was thinking, or how well you were
hiding", and the gem fixed the SECOND of those two and deliberately not the
first.

That distinction is clean, it is D12-compatible without amendment, and it is the
principle I could not state in either earlier delivery.

## 2. And it does not transfer to us straight, because we are third person

The inventory's tile "camera" (exists): "One camera, third person, spring rig in
Core and the wiring in the controller."

DERIVED: the light gem's own justification is a first-person justification. In
third person the player CAN see whether Tom is standing under a lamp, whether his
coat is dark, whether he is crouched. A gem would be restoring information the
camera has not taken away, and by the principle in section 1 it would be
illegitimate.

**So what DOES the third-person camera deny?** This is the useful question and it
has a short answer:

- **What the player character can feel and the camera cannot show.** Being
  watched from behind is the obvious one. Tom would feel a stare; the camera
  shows him a back.
- **What the player character knows and the player has forgotten.** Who in this
  room knows him well enough that a change of coat will not help. That is the
  Hitman white-dot question, and by section 1's principle it is legitimate,
  because it is Tom's own knowledge, which D12 explicitly surfaces in full.
- **What is on his own person.** Blood on the back of a coat is exactly the case
  the gem was invented for: a fact about your own body you cannot see. The
  coverage audit's most-repeated recommendation, appearance as a perception
  input, therefore arrives with its readout question already answered.

And what it does NOT deny, and so should not be given: whether any specific
person is currently suspicious of him. That is a mind.

## 3. The legibility rules, which are more prescriptive than I expected

CITED (search summaries of gamedesignskills' stealth design guide, Game
Developer's "Stealth Game Design", Christopher Smith's "Stealth Design Part 2:
AI States", and the DiVA thesis "Examining the Essentials of Stealth Game
Design"):

- **Three states, universally.** "Guards typically have three AI-states: Idle
  (unaware, patrolling), Searching (investigating sounds or distractions), and
  Alert (actively hunting)", and "enemies first becoming suspicious before fully
  alerted" exists "to give players the chance to get away, keeping the player in
  control".
- **State changes must be instant to read.** "State changes must be identifiable
  the moment they happen; if players spend too long identifying what's happening,
  they get frustrated or perform incorrect actions."
- **And the rule with the sharpest edge: "Feedback for each state must be clear
  and instantly show what's happening, subtle doesn't work."**
- **Teach through behaviour, not text.** "Reactive animations teach players the
  detection system's rules through observable character behaviour rather than
  tutorial text", with alertness shown in "relaxed stances, cocked ears, or
  running".

DERIVED, against our model: our `Awareness` enum has four states and they are a
different axis. `NeitherKnows`, `YouKnow`, `TheyKnow`, `Standoff` describe MUTUAL
knowledge, which is a more interesting thing than an alert level and is not a
substitute for one. `Core/Suspicion.cs` exists and the tile "suspicion and heat"
(partial) records that suspicion does move, 0.060 to 0.176 across 90 caught lies.

So we have a suspicion number and a mutual-awareness state and no alert LADDER of
the idle-searching-alert kind. Whether we need one is a design question; what the
literature establishes is that every stealth game that works has one, and that
its states are read from BEHAVIOUR rather than from a bar.

That last part is the cheap half and it lands on the coverage audit's finding
from KCD2 and RDR2: a person who changes what they are doing is the readout.
Someone stopping, turning, and looking at you for two seconds is an alert state
rendered diegetically, and it needs no HUD at all.

## 4. The warning, and it is the second sighting of a finding from topic 7

CITED (search summaries of the FRVR and Lemmy write-ups): **a Splinter Cell
designer says "one of the difficulties with modern stealth games" is realistic
lighting, as environments are now so much "harder to read".**

DERIVED: topic 7 found that photorealism costs apophenia, the room a player's
imagination needs to build a story. This is the same cost in the spatial
dimension. Stylised lighting can make a shadow obviously a HIDING PLACE.
Photoreal lighting makes a shadow a shadow, and the player has to work out
whether it is dark enough, which is the guessing game the light gem was invented
to end.

**LEDGER has this problem in its most acute possible form**, and this is worth
stating plainly:

- D8 sets the bar as "photoreal wet overcast grimy Britain".
- `Core/Perception.cs` scales every identification rung by `LightFactor`, so the
  light level is not atmosphere, it is the mechanic.
- `LightFactor(0.25)` is about 0.34, so at a sodium-lit street our rung 3 shrinks
  from 8 metres to 2.7. That is an enormous mechanical difference driven by a
  value the player has to read off a photoreal frame.
- And the tile "street lighting at night" is typed absent, while the tile "the
  street you walk" records that the last landed probe run "wrote a street with no
  sky".

DERIVED: we are building a game where light level is a primary mechanical input,
in a lighting style that the industry says is hard to read, with the night
lighting not yet built. That is not a criticism of D8, which is decided. It is
the third independent arrival at the same conclusion in this research lane:
**photorealism raises the legibility bar, and every system that depends on the
player reading the frame pays for it.**

## 5. Findings

1. **A readout is legitimate when it restores what the camera took from the
   character, and illegitimate when it adds what the character lacks** (1). This
   resolves the question from the Hitman and RDR2 audits and needs no change to
   D12.
2. **A light gem is not ours to take**, because we are third person and the
   camera does not take the light away (2).
3. **Three things the third-person camera DOES deny**, and all three are already
   recommended elsewhere in this lane: being watched from behind, who in the room
   knows you, and what is on your own coat (2).
4. **Every working stealth game has a three-state alert ladder read from
   behaviour**, and "subtle doesn't work" (3). We have a suspicion number and a
   mutual-awareness model and no such ladder.
5. **Realistic lighting is harder to read, by the admission of the people who
   make stealth games**, and our design makes light level a primary mechanical
   input (4).

## 6. What could not be established

1. **How Thief's guards actually signal state**, in detail. The sources say the
   gem deliberately did not tell you what the guard was thinking; they do not say
   what did.
2. **Any measurement of how badly realistic lighting hurts readability** (4). One
   designer's statement, relayed.
3. **Whether Splinter Cell's in-fiction justification for its meter matters.**
   Its meter is diegetic, "one of Sam's in-universe gadgets connected to dozens of
   light sensors sewn into his stealth suit". Tom Novak has no such gadget and
   1990 has no such technology, so the diegetic route is closed to us, which is
   worth knowing before anybody proposes one.
4. **What our `Suspicion` model's states are**, as opposed to its number. I read
   the tile and not the file, and section 3's claim that we have no alert ladder
   is bounded to that.
5. **Not covered:** sound as a detection channel, which Thief treats as
   co-equal with light (distinct footstep surfaces) and which we have as
   `Core/Acoustics.cs`; and the whole question of level design for stealth, which
   is topic 3's.

## 7. Sources

Search channel summaries, retrieved 2026-09-14; none read in full.

- Game Developer, "Building the original Thief's revolutionary stealth system", https://www.gamedeveloper.com/design/building-the-original-i-thief-s-i-revolutionary-stealth-system (EGRESS BLOCKED)
- Sneaky Bastards, "Deep in the Shadows: Thief Design Analysis Part 1, Light, Sound, and Stealth Systems", https://sneakybastards.net/stealthreview/thief-design-analysis-part-1/
- Thief Wiki, "Light Gem", https://thief.fandom.com/wiki/Light_Gem
- Splinter Cell Wiki, "Stealth Meter", https://splintercell.fandom.com/wiki/Stealth_Meter
- TV Tropes, "Visibility Meter", https://tvtropes.org/pmwiki/pmwiki.php/Main/VisibilityMeter
- FRVR, "Splinter Cell designer says one of the difficulties with modern stealth games is realistic lighting", https://frvr.com/blog/news/splinter-cell-designer-says-one-of-the-difficulties-with-modern-stealth-games-is-realistic-lighting/
- gamedesignskills, "Stealth Game Design (Principles, Mechanics, Template)", https://gamedesignskills.com/game-design/stealth/
- Game Developer, "Stealth Game Design", https://www.gamedeveloper.com/design/stealth-game-design (EGRESS BLOCKED)
- Christopher Smith, "Stealth Design Part 2: AI States", https://www.gamedesigndiary.co.uk/post/design-stealth-part-2-ai-behaviours
- DiVA, Youssef Khatib, "Examining the Essentials of Stealth Game Design", https://www.diva-portal.org/smash/get/diva2:624222/FULLTEXT01.pdf
- MoCap Online, "Stealth Game Animation Design: Sneaking, Cover and Detection", https://mocaponline.com/blogs/mocap-news/stealth-game-animation-design
- The Nocturnal Rambler, "Looking Back at Thief: The Dark Project", http://thenocturnalrambler.blogspot.com/2015/11/thief-dark-project-review.html

Repository sources, read this session at commit `074f85b`:
`ledger/Assets/Scripts/Core/Observation.cs` (the `Awareness` enum),
`Core/Perception.cs` (`LightFactor`, the rung constants),
`production/systems-inventory.json` (the camera, suspicion and heat, street
lighting at night, and the street you walk tiles),
`ledger-v2/respec/decision-register/D8-visual-bar.md` and
`D12-information-surfaces.md`.
