# What decides the week's end, and the sign Tom sees for each (30 September 2026)

Item i of the town list (U4 of Jafar's list of 30 September): every cost that
decides the ending readable before it decides, as Tom's own reading, never a
number and never another mind (D58, D33). Two attempts were set aside
(production/research/ending-reading/NOTE-2026-09-28.md). This is the design for
the third. Code waits on Jafar's scope call on the town's second page of 30
September; the page says why.

## The method (production/research/ending-reading/METHOD-2026-09-30.md)

- Each factor becomes a few named states. The ending's rule and every sign read
  that one state, so a sign cannot say "quiet" while its line is crossed.
- Where Tom already has a sign he trusts, the line moves onto the sign.
- No factor jumps a state he cannot see.
- Tom's reading of his week says "quiet" only when every factor's state is
  quiet, and its reasons are the signs he was given.

## Where it stands (read from the code, 30 September)

- **Where the endings are decided.** In the Core (ActThree.Eligible, in the
  order Quiet, Both, StraightLife, Kingdom, else BurnBoth), resolved once at
  the week's end by the old Unity layer.
- **The Unreal game has no endings yet.** Nothing that decides them is ported.
- **No factor has a sign that moves at its line.** The nearest are the police
  stage and the successor's offer, and those only in the old Unity layer.
- **Two of the old signs are meters by another name,** and are not to be
  ported: the evening's books word and the status bar's "The street:".

## The seven factors

**1. The books as the inspection would see them.**
- Decides Kingdom and Both. The line: 0.62.
- States: they stand, then they would not stand.
- The sign: the inspector's manner on the morning they stop standing ("I'll want
  the other book, Mr Nowak"). Today his word reads a different number.
- What each state is made of stays unsaid: his cooperation, a conviction,
  Ellis's case, the books moved. Only the state shows.

**2. The books as they are.**
- Decides Both. The line: 0.62.
- States: straight enough, then not.
- The sign: Sheila, in her own words, when they cross, whatever her loyalty,
  and once each way.
- Today she speaks only if loyal, and her band edges fall at 0.45 and 0.7.

**3. Keeping Mickey's business.**
- Decides Kingdom, Both and StraightLife.
- Already readable: it is his own act, answered at the week's end.

**4. A friend who would stand by him.**
- Decides Both and StraightLife. The line: 0.55.
- Three states:
  - known: calls him Tom, from 0.45;
  - warm;
  - would stand by him: 0.55.
- The sign for "would stand by him": an act asked of nobody, such as a warning
  in private, a door held, or an errand done. Today that warning comes at 0.6
  in the Unity layer; it moves to 0.55.
- Being called Tom stays the sign of being known, not of loyalty (decided
  within canon: the name is how the street learns him, PlayerIdentity).

**5. The street's talk.**
- Decides Both. The line: 0.5.
- States: quiet, then talked about.
- The sign: once the day circle holds it, he overhears a telling about him
  said as fact, not as doubt, and a remark stops as he passes.
- The status bar's word goes.

**6. Ellis's case.**
- Decides Both, and bears on Kingdom. The line: 0.5, or deflected.
- States: answerable, then not.
- The sign: Ellis's own manner. She asks while it is answerable and tells
  once it is not ("We both know where you were").
- Today his list of what people know about him shows only what he learned,
  when he learned it.

**7. The police.**
- Decides Quiet.
- States: nothing, then asking round, then investigating, then a manhunt.
- The sign for each: the detective's name in the street's talk; an officer at
  his door asking questions; a car on the street and his description.
- A killing with a sure witness passes through "investigating" for at least a
  day before a manhunt. Today it jumps from nothing to a manhunt unseen.
- This changes when an ending can shut, so it is his call. It is on the page
  with the scope question.

**Successor and handover** (decides Quiet): ready, then not.
- The sign: the successor's offer.
- If readiness lapses before he hands over, the successor says so ("I can't
  take it on now"). Today it is said only the first time.

**Witnesses' nerve** reaches the ending only through loyalty (factor 4). A
witness whose nerve holds meets his eye; one whose nerve goes looks away.

## Tom's reading

- Built only from the signs above: a line in his own ledger, in his own words.
  For example: "The inspector wants the other book. Ron would still stand by
  me. The police have been at the door."
- It says "quiet" only when every factor is quiet.

## The checks

- Each sign and Eligible() call the same state function; a Core test for each
  factor fails if they ever disagree.
- The balance lab sweeps the whole range: no ending shuts while the reading
  says quiet, and nothing reads shut while a move he has left could reopen it.
- The AI tester is asked at the evening checkpoints "how does this week end,
  and why?", and its answer is compared with the ending the state predicts.

## Who builds what

- **The town (Core):**
  - the named states;
  - the signs' words;
  - the reading;
  - the tests and the sweep.
- **The builder (Unreal):**
  - the endings themselves (ActThree and the police's stages, first);
  - then each sign in the street: the inspector, Sheila, a friend's act, the
    overheard telling, Ellis, the officer at the door, the successor.
