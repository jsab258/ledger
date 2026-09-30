# How a town's people are made to move

Research, 30 September 2026, by a separate research helper.

(The helper returned its text; the session that asked for it saved it here after checking its reading of the game's walking code: the street's walkers move at 1.2 metres a second unless the street file says otherwise, and the walk blends in and out over about half a second.)

## How studios do it, in order

1. **A list of moves for each kind of person** comes first. The trade calls it a "dance card". It covers standing, a few idles, walking at two or three speeds, starting, stopping, turning, looking, talking, what people do at a spot (smoke, lean, wait, sit) and reactions. GTA's street people pick from a list of "scenarios" tied to places. The Witcher 3 kept about 35 idles per body type, sorted by mood and standing.
2. **A source for each move**: the studio's own capture, a bought library or a free one.
3. **Retargeting**: the moves are carried onto the game's bodies, then checked for sliding feet.
4. **Layers at runtime.** From the bottom up: walking and standing; whole-body actions such as reactions and sitting; an upper-body layer for gestures and the cigarette; small added movements such as breathing and flinching; feet held on the ground; head and eyes turned by a look-at; and the face on its own layer. Big studios drive the walking with "motion matching". Smaller ones blend an idle and a walk and use tricks that stop the feet sliding.
5. **Marked spots** in the street tell people where they may lean, wait or sit.
6. **Cost-saving at a distance**: people further away are animated less often and use simpler models, with their hair and cloth turned off.
7. **Judged in the game**, through the game's own camera.

## What Epic gives free

- **Epic's animation sample**: more than 500 animations at launch in 2024 and 400 more in the 5.7 update. It includes motion matching and people sitting on benches, and 5.8 adds a new look-at and moves involving two characters. Epic shows a MetaHuman using it.
- **Lyra and City Sample.** City Sample's crowds wear 2020s clothes, so only its method is useful to us.
- **The licence.** All three are free for commercial games but only inside Unreal. For Lyra I read this on a copy of its readme; for the others it comes from search summaries. This "Unreal only" licence is not on our allowlist.

**Decision for you: may we use Epic's own free Unreal-only animations inside the game?**
- **(A) Yes, only inside the game. Recommended.**
- (B) No; Mixamo only.
- (C) Buy packs instead.

## What else can be used

- **Mixamo**: free, commercial and already allowed. Uneven quality; its starts, stops and turns rarely match its walks (my judgement).
- **Fab packs** (on our list): idles that include smoking, and conversation gestures. The paid ones would come to you as a money question.
- **Carnegie Mellon's library**: commercial games allowed, reselling the data not. Search summary only; the recordings are old and noisy.
- **Bandai Namco's set**: non-commercial. Never.
- **Our own capture**: Unreal 5.8 can now turn one phone or webcam video into body animation (experimental). It is still a lot of work, so not now.

## Getting them onto MetaHumans

MetaHumans share the mannequins' skeleton layout, so Epic's moves fit after retargeting. The body proportions differ, and Epic's own sample still retargets for each body type. Unreal 5.8's retargeting tool has a new "foot definition" and can pin feet that should be still.

**Our street walkers probably slide today.** They move at a fixed 1.2 metres a second, whatever speed the walk's feet actually travel. That is the first fix.

## What twenty people cost on your card

Nobody publishes a cost per person for MetaHumans. What is published:
- Epic's default animation budget is 1 millisecond a frame.
- A full-quality MetaHuman averages 1 to 2 GB of memory; the game version is under 100 MB. On a 10 GB card everyone must be the game version.
- Card hair for 50 people took about 800 MB on an 8 GB card.

My estimate for twenty people is about 1 to 3 milliseconds of processor time, 2 to 5 of graphics-card time, and 2 to 3 GB of graphics memory. None of it is measured yet.

## What to do, in order

1. **Measure** 0, 5, 10 and 20 people in the packaged game.
2. **Fix the walking feet**: match the body's speed to the walk, and check automatically for sliding.
3. **Your licence decision** above.
4. **One person first, with the full set of moves**, layered in our own animation code: stand, idle, walk, turn, look, talk, smoke a cigarette, react to a smash. You approve it in the game before it is copied to twenty.
5. **Then** the spots in the street, variety, and the cost-saving settings.

While the playable route is broken, only the moves that route needs come first.

## What could not be verified

Most outside sites were blocked, so these rest on search summaries: Epic's licence text, Adobe's Mixamo terms, Carnegie Mellon's and Rokoko's terms, and the conference talks. I found no published cost for a MetaHuman's face rig or its cloth.
