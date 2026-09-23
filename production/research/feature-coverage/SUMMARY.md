# Four hundred and sixty-two things neither of us had written down

The other model's list is five times finer than mine and it exposed 462 blind
spots. The full comparison and the merged master checklist of 957 features are
in [DELIVERY.md](./DELIVERY.md) beside this file; the list itself is
[astra-list.md](./astra-list.md).

## The count

Of its 923 expectations:

- **172** were in my checklist and in the plan.
- **116** were in my checklist and not in the plan.
- **99** were IN THE PLAN and not in my checklist.
- **74** are ruled out for this game by our own decisions, 25 of them
  multiplayer.
- **462 were in neither.** Half the list.

## The uncomfortable part

My delivery last week diagnosed exactly this failure. It said the head turn and
positional sound went missing because they were swallowed by headings: `bodies
and faces`, `sound in the Unreal build`. Then it produced 179 rows at the same
altitude as the headings it was complaining about. `Interaction prompts` is one
row of mine and twenty-four of theirs. The title screen is one row of mine and
twenty of theirs. `Positional sound` is one row of mine and fifteen of theirs,
ten of which are still nowhere.

So the audit that found the problem repeated it. That is worth more than the
462 numbers, because it says the fault is not carelessness. It is that a list
written by asking "what features does a game have" always comes out at the
altitude of the question.

## The worst of them

1. **The game needs the internet and has no plan for losing it.** Decision 4
   keeps the text model on a paid online service. Nothing anywhere says what a
   player sees when the connection drops, what happens to a conversation in
   progress, or whether there is anything to play offline. Two items, and the
   most dangerous two on the list for us.
2. **Nothing covers the silence while a character thinks.** A live model with a
   four-second budget will produce gaps and lines that arrive late, and there is
   no line anywhere about what fills the gap, or about subtitles matching a
   sentence that is generated rather than written.
3. **The town's reaction in the minute AFTER something happens.** We have the
   memory of the event, permanent and per person, and the plan does have a body
   being found, `the gap between the act and the discovery`. It has nothing for
   panic resolving, or for people not cheerfully chatting beside an ongoing
   emergency. The moat is the remembering; this is the minute afterwards, and
   it is the part a player watches.
4. **The head turn family, again.** Eight of fourteen items about looking,
   expression and orientation are still in neither list. Including people
   turning toward a shared disturbance, which for a game about who saw what is
   closer to the moat than to polish.
5. **Ten of the fifteen spatial-sound items.** One of the two accidents that
   started all this, audited, and still four fifths absent.
6. **Nothing says the simulation must not change speed with the frame rate.** A
   deterministic Core is a pillar. On a slow machine, nothing written down
   protects it.
7. **The basics that make a build feel amateur in ten seconds**: movement that
   does not stop when you release the key, a stuck input after closing a menu,
   an attack fired by the same click that dismissed a window. Cheap, invisible
   in a feature list, fatal to feel.
8. **Rocco and Lena.** Twelve of fourteen companion items are blind. No lens of
   mine ever asked who walks beside the player.
9. **Driving.** Nineteen of twenty-four vehicle items are blind, in a game where
   you inherit a minicab office. D24 caps the spend on driving; it does not make
   the cab office stop being a cab office.
10. **A mute player cannot play a game whose pillar is talking**, unless typed
    input is guaranteed. Nothing guarantees it.

## The reverse finding, which I did not expect

Ninety-nine of their items are things THE PLAN already holds and MY list
missed: thirteen about stealth and the law, ten about world layout, six about
enemy awareness, six about lighting. My four lenses were built from credits,
engine modules, a generic first session and compliance checklists, so they
produced a generic game and under-read the parts that are this game's actual
subject. The plan has been writing those down for weeks and my instrument
could not see them.

## What this says about how we find features in future

**Two independent lists, then a diff.** This is the cheapest instrument the
project has found. One list is one model's blind spots. Two lists made without
sight of each other, compared item by item, found 462 things that one of them
alone did not. It cost one commission. Do this for anything that has to be
complete: the crime verbs, the content rule's enforcement sites, the cast.

**A checklist row is only a row if it can fail.** `Interaction prompts` cannot
fail; `a prompt attached to the object you are looking at rather than the one
behind it` can. The grain test is whether a builder can tell you it is done and
a tester can tell you it is broken. Anything coarser is a heading pretending to
be a checklist, and this project now has two audits proving headings hide
things.

**Ask for the failure, not the feature.** Their list is mostly phrased as what
goes wrong: doors that trap you, saves that collide, sounds that double-trigger.
Mine is phrased as what exists. The first phrasing finds four times as much.

**A blocked source is a lane problem, not a fact about the world.** Their list
cites the Xbox accessibility guidelines and Steam's controller documentation,
both refused by this environment. My accessibility and platform sections are
where my blind count is highest. When a lane cannot reach a source, the answer
is to get it from a lane that can, not to reconstruct it.

## Where the work lands

Of the 883 features that are not ruled out: **291 are stage 4, the player's
shell**, 230 stage 2, 139 stage 3, 82 stage 6, 70 ship-prep, 47 stage 1 and 24
stage 5. The shell is a third of everything a player expects from this game and
it is currently one line of ROADMAP.md.
