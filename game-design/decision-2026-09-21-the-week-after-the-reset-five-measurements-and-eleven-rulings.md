# Jafar's order, 2026-09-21: the week after the reset, five measurements, eleven rulings

STATUS: LOG, 2026-09-21. NOT CURRENT once the D-records, queue items and
file edits it lists have landed: from then the decision register and the queue
are the reading copies and this is the record of what he said and when. His
message of Monday 2026-09-21, arriving between
11:19Z and 12:10Z with the reading total 0, Fable 0, ceiling 85 standing.
Written by the resident as dictated text, which is the one category of
authoring the resident may hand-apply, and kept VERBATIM below because a
paraphrase of a ruling is not a ruling. This is the source; the D-records,
queue items and file edits that carry each piece are derived from it and are
listed under "Where each piece went", which is a reading at the instant of
each commit and says so.

The budget row is `production/budget.md`, row 2026-09-21. With the same
message the session model was switched to the Fable tier, so the resident's
own turns spend the Fable meter from here.

## Where each piece went, a reading at each commit and not a promise

Filled in as things land. A line reading "not yet" is the truth at the
newest commit touching this file, not a plan.

- The reading: `production/budget.md` row 2026-09-21. Landed with this file.
- The order of the week and what is moving: `production/NOW.md`, top section.
  Landed with this file.
- Slice 1, D18 in the animation library: queue 388. Not yet at the first commit.
- Slice 2, the exposure fault and the night determinism check: queue 384,
  status changed to STARTED, plus the night extension written into it.
- Slice 3, the first authored facade as the measured batch: queue 389, behind
  queue 370's column and the throughput ledger's unit.
- The small-model test: queue 390.
- The MESH station: queue 391.
- The scale soak: queue 351 (with 116 folded in), status changed to STARTED.
- The frame instrument: queue 392, riding the slice's dispatches.
- The art lane, six character concept sheets: queue 393.
- The eleven rulings: D47 to D57 under `ledger-v2/respec/decision-register/`,
  indexed in `rulings-log.md`.
- The research corpus cleanup: queue 394. The v1 sweep: queue 395. The three
  conventions: `ledger-v2/studio-v2/operations.md` and queue 396 for the link
  sweep. The map's second board: queue 397, extending D38.
- The two cards: `production/decision-queue.md`, written by the Producer.
- The one check, the wake system against a usage limit: answered in the
  brief and recorded in `production/wakes/README.md` or queue 398.
- Queue 250 stays as filed and is taken if budget remains.

## His message, verbatim

Budget after the reset: total 0, Fable 0. Ceiling 85 on the higher meter, standing.

Research is finished. What remains unknown is six things, and every one of them is a measurement nobody can look up: what a unit of content costs, whether the simulation runs at three hundred residents rather than seven, whether a small model can hold a character, whether 3D generation runs on my card, what a frame costs in Unreal, and whether a person plays it without bouncing off. This week takes the first five. The sixth needs the smallest crime loop, which comes after the slice, and its runbook is already on disk. From here, a question a measurement can answer is not commissioned as research. One design audit is running in the research lane now and is covered under the rulings below.

How the week is ordered, so nothing below has to be reconciled with anything else:
- The visual slice is the spine and has the runner first.
- The measurements run in parallel with it and queue behind it on the runner.
- The art lane queues behind both.
- The rulings are recorded as you go; they are cheap and they are not the week's work.
- The cleanups, the two cards and the one check are studio work, taken at checkpoints inside the studio's third.
- Then, if budget remains, queue 250.
- Then the filed audit and red-team items.
This is more than one week at the ceiling will cover. When the budget forces a choice, cut from the bottom of that list, never from the slice. The slice, the measurements, the art lane and queue 250 are the game's two thirds; the rest is the studio's third, and the Sunday page shows the split.

THE VISUAL SLICE, in this order.

1. Fifteen minutes, first: D18 is violated in the animation library right now. A drinking clip is live and matched to a slot called drink, the bartending clip fills the counter-work slot, and the smoking clip, which D18 keeps, is the one that got dropped. Nobody caught it because all five content gates read text. Remove the clips, fix the slot names, and extend one gate to walk the animation library by clip name.

2. The exposure fault. It is item 1 of D28's own list, opened on 14 September and never closed. Run 54's controls disagree with their own second take in ten of twelve cases and run 53's in eight, so no night still from last week is comparable to another and the figure was judged against a moving target. The fault stayed invisible for a week because the rig's determinism check photographs only a day frame. Fix the fault and extend the determinism check to the night shots in the same batch, or the blind spot survives the fix. Then the figure.

3. The first authored building facade, as the week's measured batch. The Hook comparison showed the gap is no longer lighting: the reference is a street of buildings with faces, and ours is a corridor of blank walls with fog covering the absence of anything beyond thirty metres. D28's deferral of geometry is lifted, as recorded in Amendment A1. No building facade has ever been authored here, and the nearest four things to a building are a cornice, a bracket and two chimney pots, so the first one is the measurement. Before the window opens: queue 370's column is in place, and the throughput ledger takes a batch as its unit and counts rejected attempts, since the industry research found nobody measures rework and ours would be the instrument that does. Read both meters before and after. The facade is authored under the grime rule recorded below. It replaces the resident as the first measured batch because buildings are where the gap is; the resident follows when stage 2 opens.

THE MEASUREMENTS, in parallel with the slice.

The small-model test. The conversation ruling below withdraws a pillar's reasoning, and this is what replaces it. Caching on, the cost per hour printed, then a small model behind the existing conversation interface, run against a set of cases and scored on a bar that counts a well-formed wrong answer as a failure rather than a pass. If the model has to run locally, dispatch it to the PC like any other machine job. It gates the hardware floor, and the hardware floor gates who can run this game, which is a scope decision I cannot make without the number.

The MESH station, which has never run. It is wired to the original TRELLIS; the allowlist permits TRELLIS 2 as well, and nobody has chosen between them. The README's NVIDIA-only line is not the whole truth: a ROCm fork of TRELLIS has run end to end on a 16 GB AMD card, Hunyuan3D 2.1 runs on AMD via ROCm on Windows, and a DirectML port routes the CUDA calls through Microsoft's own path. The real limit is memory, around ten gigabytes for shape alone, which is exactly my card. Pick whichever route has the best chance, TRELLIS 2 included, install it through a dispatched job, and put one image through it. Texture generation is expected to fail and does not matter, because CLEAN and the material pipeline do that half. Report the route, what it needed, and the memory it used or where it ran out. If it runs, the 3D line is complete for the first time; if not, I have a hardware decision rather than an assumption.

The scale soak, queue 116, reopened. Pillar 1 claims three to five hundred residents who all remember, and its only evidence is a seven-agent soak. Run it at fifty, then two hundred, and report what holds and what falls over. It measures the Core rather than changing it, and it runs in the container.

The frame instrument. Nothing in the Unreal build measures a frame: the file called FrameStats measures screenshot brightness, and the only frame instrument was in the Unity build D16 retired. Phase 1's gate names a frame budget and cannot exist until something reads one. Add the readout to the slice's own dispatches rather than as a separate job, so it costs no extra runner time.

THE ART LANE, behind the slice and the measurements.

Character concept sheets, commissioned by stage 2, by the same three-pass method as the district sheets. We have thirty-five written cast cards and seventeen voices cast, and not one picture of a person in Meridian. Draw the archetypes before anyone builds a resident: a docker, a market trader, an office clerk, a copper, a cab controller, a young man about town. Full figure, working clothes, 1990, wet weather, from the town form bible and the period research rather than a generic idea of the era. They are what the clothing and animation lines will aim at.

RULINGS, recorded as you go. Number them from the register's next free number after checking it. They are corrections to decisions, not new work.

On the conversation pillar.

The pillar's reasoning about the conversation model is withdrawn, not the pillar. It said the model only classifies and picks from closed sets, so it can be small. The constraint-tax paper, read in full, measures the opposite for small models: constraining output to a closed set takes schema validity to one hundred percent and answer accuracy from 19.7 down to 11, with wrong-but-valid answers at 88.9 percent. A small model would confidently return well-formed wrong choices, which is the one failure the deterministic core cannot catch, since it checks that an output is in the set and not that it is the right member. The pillar stands: the model never adjudicates. What falls is the inference that it can therefore be small. Its size is the measurement ordered above, and no hardware floor is written before that number exists.

No resident speaks through a worse model than another because of who they are. The research recommends running the crowd on a small local model and the named cast on a better one. That is ruled out, because a consistent quality difference would tell the player who matters before the game does, which is the opposite of what this game is about. If tiering is needed, it follows the interaction rather than the person, so a passing remark runs cheap for anyone and a real conversation runs well for anyone; or everyone runs the better model. Choose between those only when the small-model test and the cost per hour exist.

Live content screening is built, and it is a pillar dependency rather than a ship task. Steam's January 2026 rules put us in the live-generation category twice over, because our characters both write and speak their lines as the game runs, and that category requires guardrails that stop illegal or offensive material reaching the player as a condition of being on the store. Today the validator checks length and staying in character, and the content rule is called only from crowd body generation, so nothing screens what a character says or what the voice speaks. It does not need to be sophisticated to start, because the deterministic core already licenses what a character may say and this is a last gate rather than the whole defence. It goes on the ladder as the conversation pillar's first rung.

The voice watermark is kept. The allowlist says keep it, the August stub was right and said the shipped game would have to decide, and that decision was never made, so the game speaks unmarked audio today. Ask the engineering question first, which nobody has asked: whether the watermark can be reapplied after the game decodes the audio. With the EU AI Act fully applicable since 2 August 2026, unmarked generated speech is not a risk worth carrying.

On speech and hardware.

The speech engine's upgrade path is not the upgrade path. The turbo model drops the exaggeration control the 28 July decision was made on; its own code defaults it to zero and ignores it. Chatterbox-Nano at 110 million parameters exists, clones from the same reference-clip interface, and neither earlier topic knew of it. It goes on the evaluation list ahead of turbo, and the 28 July record gets a note that its premise no longer holds for the successor.

The hardware floor paper says close to the opposite of what was taken from it. The sub-gigabyte figure is a stock small model scoring sixteen percent on factuality, which its own authors do not recommend for dialogue; their recommendation is the seven-billion model. Nobody writes a hardware floor from that paper. What transfers is its modular memory measurement, swaps and retrieval in tens of milliseconds at a thousand entries, which supports our memory design rather than our model choice.

On the look.

Grime is the strategy, per canon, against the light period look that the shader's art-direction line quotes. The two disagree and it has never been recorded. Record it as a rule with a number in it, a stated floor for how much wear a surface carries, so it is not re-litigated on every render. The facade is the first thing authored under it.

On bodies and movement, both for stage 2.

There is no MetaHuman wardrobe. It ships one unnamed outfit, so the question I was told to answer by opening MetaHuman Creator does not exist. Epic's own documentation says clothing does not need skinning at all, which removes the first named break in the clothing line. The route is: fourteen of eighteen bodies already wear separate garment meshes on one shared skeleton, Blender's weight transfer is on the PC, the clean script destroys clothing in four lines, and the checker cannot tell a working coat from a ruined one. Build the checker, then move a jacket between bodies. Nothing is bought. It waits for stage 2.

The animation route is not closed, and the earlier finding answered a question I did not ask. The mocap topic was briefed on whether markerless capture is viable, so it answered about licences and failure modes. My question is whether an animation assembly line can exist the way the image line does: a spec goes in, generation happens, an artifact comes out, it is imported and verified, and nobody hand-animates anything. The pieces exist: the image lane works, video models generate motion, MediaPipe and MMPose are Apache 2.0 so our own or generated footage through an estimator is unencumbered end to end, and Blender retargeting is scriptable and already on the PC. The soft physics and sliding feet the research flagged in generated video are a quality problem with known fixes, not a wall. The caveat is that this would be a third generative line while the second is unproven. So the route is recorded as open and commissioned at stage 2, after the 3D line has produced something.

On the crime layer, owed rather than built.

The half of the game where Tom is a boss rather than a witness has far fewer designed verbs than the half where the town watches him. Asked whether I could order a crew member to kill a rival, the answer was that nothing had been designed, and the coverage audit could not have found it, because none of its five reference games is a crime-empire game. Record it as owed, the way the narrative was recorded under D30. It covers ordering and delegating violence with the exposure that comes back to me; the information verbs only this game can have, such as seeding a rumour on purpose, buying an alibi, framing someone, and silencing a witness who cannot be made to forget; crew betrayal, including a crew member turning supergrass; the docks and business side; doing time while the town changes; and how the game ends, including a route to going straight, since the red team found no route back once the town turns. Combat is owed with it as its own layer, not only as violence through the moat: fists, scarce weapons, injury, being outnumbered, running, fighting dirty, and what a street of witnesses does during a fight. Put it in the stages document under stage 3 and in the Sunday page's list of things owed, so it surfaces without me asking. The research lane is running a crime and combat coverage audit now. When it lands, send me its summary and act on nothing in it until I rule; it goes on the consolidation page with the rest.

On tools.

Graphify is declined. The evaluation found six reasons, and two of them are facts about us rather than the tool, both addressed by the cleanups below. It retires nothing, which the standing rule on new instruments requires, and what it replaces is grep.

THE CLEANUPS, at checkpoints.

The research corpus. Every research delivery sits on its own branch and none of them is in this checkout: filing the playtest runbook on Friday, you could not cite the delivery it rests on, because a grep over the whole tree found zero hits. Copy every SUMMARY.md, RECHECK.md and BRIEF.md onto main under one folder, keeping the overturn markers the lane added. Write one page above them: every recommendation sorted into four columns, ruled by me with the record named, mine to rule with the question phrased for a one-line answer, a correction the studio applies under D43 with its queue item, and a fact to check with what would check it. The ladder references that page, and queue 387's note about the missing evidence is closed. Delete or merge each research branch once its files are on main.

The v1 material that should not have made the migration. The archive sweep of 10 September ran before the move, so everything it put in legacy/ was carried into this repository wholesale. The old repository still holds every commit, so anything here purely as history does not need to be here. Go through legacy/ and the v1 remnants and rule, for each, whether it is live, referenced by something live, or only history: the Unity character bodies and game scripts D16 retired, the fifteen probe projects, game-design/ with its seventy decision files, the voice-selection folders, the two thousand generated clips, and game-design/PLAYTEST-RUNBOOK.md, marked LIVE and verified 15 August, a Unity-on-macOS build guide superseded by production/playtest/RUNBOOK.md. What is only history is removed from main and the removal names the commit in wc26-picks where it still lives. What stays, stays with a reason. The C# Core stays; it is the source of truth the port is checked against.

Three conventions, because the last cleanup did not hold and rules are cheaper than sweeps. A research or art branch is merged to main or deleted, never left standing. A document that supersedes another marks the old one in the same commit. And anything that names a file links to it: we carry 2,135 backticked paths against 16 markdown links across 861 files, so nothing here can be traversed, by a tool or by a person.

The map's second board, from the asset audit's eighty-four categories, same five areas and three colours, so a missing content category is a tile rather than a conversation. Extend the standing rule: anything that produces a new kind of asset gets a tile before the work starts.

TWO CARDS I want, each with a recommendation.

Where the conversation pillar's rungs sit. The ladder is otherwise entirely visual, and screening, the model's size and the watermark are all conversation dependencies. Screening is now that pillar's first rung; propose where its rungs sit relative to the visual stages.

Whether to replace our single reviewing director with the gate six other studios have converged on independently: four directors in parallel, each returning ready, concerns or not-ready, strictest verdict wins, with three intensity modes set in a file, full, lean and solo. The same research found we are ahead of all of them on budget discipline and overnight autonomy, and nobody has published how those fail, so we find out ourselves.

ONE CHECK. Project threads on the new Claude Code projects feature wait out a usage limit and resume on their own when it resets. Say whether the wake system can do the same, so a limit no longer needs my reading to restart work.

IF BUDGET REMAINS: queue 250, the gossip mill passing what NPCs know through walls while my own hearing runs through the acoustics model. It is a change to the Core and keeps its full review.

Everything else holds: one brief a day with the frame in it, the reading asked as its first line, and beyond the two cards above, cards only when you cannot decide. Work until the ceiling or a limit; arm the resume on either.
