# Forty-seven things nobody wrote down, and two are the ones you found

Research topic: feature coverage. The commission is [BRIEF.md](./BRIEF.md). The
full merged checklist, with each item's lenses and its place in the plan, is
[DELIVERY.md](./DELIVERY.md) beside this file, in a form that can become the
per-stage list in `ROADMAP.md`.

## The count

Four lenses produced **179 expected features**. Against the plan, meaning
`ROADMAP.md`, `canon.md`, `DECISIONS.md`, the 111-row systems inventory and the
69 research files:

- **90 are in the plan.** Written down with a place, whether or not anything is
  built. An inventory row typed absent counts here: it is written down.
- **42 are partly in the plan.** Named only inside a coarser row, or only in a
  research delivery that has no home in the roadmap or the inventory.
- **47 are absent.** Nothing in 73 files names them.
- **65 of those 89** would be noticed by a player inside the first thirty
  minutes.

## The sentence worth taking away

The two things you found by accident are still not in the plan.

Neither `head turn` nor `positional sound` nor `look`, `gaze`, `spatial` or
`bump` appears in the name of any of the 111 systems, or in `ROADMAP.md`, or in
`canon.md`, or in `DECISIONS.md`. Both exist in exactly one place: the
baseline-features delivery, and that is on a branch which has not been merged.
The audit that found them has not yet put them anywhere a future session would
read. Until it lands, the same accident can happen again.

## Why a 111-row inventory missed them

Because its rows are tiles and a tile is not a checklist. `menus` is one row.
`accessibility` is one row. `sound in the Unreal build` is one row. A tile is a
place to put a colour. Every one of the 42 partly rows is a feature that a tile
swallowed: the quit confirmation inside `menus`, the subtitle's speaker name
inside `subtitles`, the head turn inside `bodies and faces`, positional sound
inside `sound in the Unreal build`.

## What a player meets soonest, of the 89

1. **No sound that comes from where it is**, and none that falls off with
   distance. Nought and one minute.
2. **Nothing before the game starts.** No logo or legal screen, no content or
   photosensitivity warning, no first-run detection, no version anywhere.
3. **A shimmering image.** Nothing in the plan asks for a stable one, on a wet
   street at night, which is exactly where it shows.
4. **No body and no shadow** for the player in third person.
5. **Display settings the plan does not name**: resolution, window mode,
   vertical sync, a frame cap. Two sliders and a render scale is what is
   written down.
6. **Nobody gives way** as you walk, and nothing says they should.
7. **A menu a gamepad cannot drive**, and no button prompt that matches whatever
   is in the player's hands.
8. **The head turn**, two minutes in.
9. **No birds.** In a port town. No animal of any kind appears in the plan.
10. **No prompt** telling you that you can do anything at all.
11. **Not knowing what to do next.** The word `objective` appears **zero times**
    in all 73 files. I did not believe that and checked it separately.
12. **People who ignore the weather.** Rain changes what they can see and hear,
    which is perception. Nothing says it changes what they DO.
13. **Subtitles with no speaker name**, in a game whose whole subject is who
    said what.
14. **No privacy notice**, while decision 4 keeps the text model on a paid
    online service that the player's typed words reach.

## Which lens found what the others missed

**Lens 4, what the industry already checks.** It found 15 items no other lens
found. Ten of the fifteen are absent from the plan and one is in it. No other
lens comes near that ratio. Its subjects are the ones a studio with no publisher
and no compliance department never meets: what happens when a pad is unplugged,
whether a sound you cannot see has a visual form, whether anything requires a
fast repeated press, whether a menu can be read aloud, whether the screen may
flash.

And the awkward half of that: **lens 4 is also the one whose sources this
environment refused.** The Xbox Accessibility Guidelines and the Game
Accessibility Guidelines are both blocked here, as is every platform
certification site. I built that lens from the structure of the problem rather
than from a checklist, and it still out-found the other three. Anybody with an
unblocked browser can fetch the ESA's 24 accessibility labelling tags in ten
minutes and would probably double it.

**Lens 1, who builds it, confirmed rather than discovered.** Thirteen items
found alone, ten of them already in the plan: casting, motion capture, music,
clearance, art direction, writing at volume, QA, build engineering, playtesting.
That is a studio recognising itself. Its sources were also refused, so it is a
reconstruction from award categories and a discipline list rather than from the
credits rolls you asked for.

**Lens 3 produced the clock.** Every ranking above is its ordering. **Lens 2 was
narrow and deep**, and it is the only one that reported from the engine's own
mouth: Unreal ships 1,869 modules, 246 of them runtime, and three of them are
called `SubtitlesAndClosedCaptions`, `ScreenReader` and `TextToSpeech`. What is
missing above is not missing from the engine.

## Three things in the brief that turned out differently

1. **D24 rules nothing out.** You offered it as a verdict for features that do
   not belong in this game. It rules out zero of the 179. Its own words make it
   a spend rule and not a ban, so every absent item in the delivery carries a
   stage instead.
2. **Around two hundred systems is 111**, in five areas: 30 exists, 41 partial,
   36 absent, 4 ruled-out.
3. **The inventory's phase numbers do not mean ROADMAP's stages.** They point at
   the old roadmap-v2, now in the archive. I re-mapped every item onto the six
   stages you ruled on 14 September.

## Where the missing work lands

Of the 89 items not properly held, **45 belong to stage 4, the player's shell**,
and 17 to ship preparation past the sixth stage. Twenty belong to stage 2. That
is the useful shape of this: half of what a player expects and the plan does not
hold is the shell you already named as a stage, and it is currently one line
long.
