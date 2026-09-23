# You are an invisible man walking in silence down an empty street

Research topic: baseline features. The full checklist, feature by feature, in a
form that can become a per-stage list, is [DELIVERY.md](./DELIVERY.md) beside
this file.

## The answer is not a list of missing features

You asked which ordinary things we are missing, expecting nearly everything to
be in. It is the other way round, and the reason is better news than it sounds.

The Unreal side of this project is not a game build with gaps in it. It is a
street photography rig and a walk test: 57 files that spawn 593 street pieces
and four lights, put a capsule with a camera in the middle, and take pictures.
Its own code says so. The character file states in plain words that it carries
no visible mesh and has "no jump, no crouch, no interact".

Measured this session, not assumed. Files in the Unreal build that mention
animation: none. Skeletal meshes: none. AI controllers: none. Navigation: none.
Any interface widget: none. Particles: none. Time of day: none. And anything
that plays a sound, of any kind: none.

So both things you found by accident have the same cause. Nobody turns their
head to look at you because there is nobody in the street and no character
animation. Sound does not come from where its source is because nothing plays
sound at all.

**The floor is not missing pieces. On that side, the floor has not been laid.**

## The one sentence worth taking away

We already model sound in detail, and we make none.

The hearing model is ported into the Unreal build and locked by a golden test:
how loud a thing is, how far that carries, and that a wall takes twenty-two
decibels off it. The game can work out who heard a shout through a wall. It just
cannot let you hear anything. That is a gap between simulating a world and
presenting one, and it is the shape of most of this audit.

## What a player notices, in order, in the first ten minutes

1. **Silence.** Nothing plays. Noticed before you have taken a step.
2. **The street is empty.** No people at all.
3. **You have no body.** Third person on an invisible capsule.
4. **No footsteps**, and none that change on cobbles or wet stone.
5. **No ambience.** No traffic, no gulls, no distant town.
6. **Nobody moves out of your way**, because there is nobody.
7. **No pause, no interface, nothing to press.**
8. **No head turns toward you**, the thing that started this.
9. **No prompts and no subtitles.**
10. **Feet not planted** on the stairs and slopes when characters exist.

## The cheap ones, because Unreal gives them

I checked Epic's documentation rather than trusting memory, and three pages are
confirmed to exist: spatialisation, Control Rig, and Nanite. So positional sound
with distance falloff, head-turn and foot planting through Control Rig, and
detail that appears without popping through Nanite are all engine features we
would be switching on and wiring rather than inventing.

That covers items 1, 4, 8 and 10 on the list above, plus muffling through walls
and room reverb later. On the current evidence the expensive ones are the ones
that are ours anyway: people in the street with behaviour, and what the world
does with time and weather.

I should be straight about the limit here. I confirmed those three pages exist
with their titles; Epic's site did not give up the page bodies, and every other
"Unreal gives you this" line in the long version is my general knowledge, marked
as such. None of it should be used to size work without a check.

## Two things you should know I got wrong or could not do

**The stage names do not exist.** You asked for the stage of ROADMAP.md,
presentable or the playable slice. There is no ROADMAP.md, and neither phrase
appears anywhere in the repository. The live plan is roadmap-v2 and it runs
phases R and 0 to 6. I mapped presentable to Phase 2, the street at the visual
bar, and the slice to Phase 3, the town, and said so in the long version so you
can reject the mapping.

**One row I nearly shipped on weak evidence.** I had marked the camera passing
through walls as partial, on the strength of the right component being present.
I then opened the file: the collision test is switched on deliberately, with a
comment saying so. The camera is fine. What is actually missing there is
smoothing, which is not set at all.

Finally, a caution about the method rather than the findings: my first sweep of
the build used a broken search pattern and reported that seven whole categories
were absent. They were not; the pattern was. A control search against terms I
knew were present caught it, and everything above comes from the corrected
sweep. The numbers here are only as good as that second pass.
