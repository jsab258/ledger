# LEDGER: prototype scope (draft)

Review applied, 17 Nov 2026: all 15 fixes from production/lane/reviews/REVIEW-PROTOTYPE-SCOPE-DRAFT-2026-11-17.md, with the browser figures from the fixed SIM-IN-BROWSER-2026-11-17.md and the gun list from the fixed COMBAT-END-STATE-OPTIONS-2026-11-17 note (July's five guns, game-design/weapons-spec.md).

Draft, 17 November 2026, written by a lane helper for Jafar. Not ruled. canon.md outranks everything here; where his rulings settle a point, this draft follows them. Sizes are rough and marked so. Anything not checked is marked "unverified".

His decision of 17 Nov: the browser loop prototype (built by Fable, published on its own page) becomes the whole game in rough, playable form, and the spec of record the Unreal game builds from. Art quality, animation detail, performance, voices, clothes and faces stay out. That decision is not yet in RULINGS.md; it should land there the same day.

## 1. Summary in five lines

1. The prototype already plays one week on Quay Street with seeing, naming, gossip, the Ledger, live talk, fares, the tin, three night jobs, a fight ladder, police statements and Sheila's Friday question.
2. To be the whole game, within his ruled map (the Hook plus the docks), it needs the ruled warehouse fire, Acts II and III with the ruled two or three endings, the three rivals, the crew and empire firsts, carried weapons, then July's five guns, the camcorder and CCTV, and traffic.
3. It should move into the repository as a source project (prototype/) that builds one HTML file, with Node tests per system, published to the same page.
4. One simulation, not two: the real C# Core in the browser through WebAssembly (15 to 27 cloud hours, built on a GitHub build machine); if that fails, JavaScript rules must pass the same 102,960 golden answers.
5. Three decisions at the end: one simulation and its licence line, the endings count, and the prototype's budget.

## 2. What the prototype has today (from its own notes)

Read from the published page itself (its Design notes, How the town watches, Credits and run report code), 17 Nov. One 1.21 MB game code file (three.js), fifteen published files, about 5.5 MB in all (total unverified).

- Scope: the Hook around Quay Street, plus a slice of Copper Row over the bridge (bank, video shop, market hall, station forecourt). The Parade left out ("a nightlife strip without drink read thin"). The Widow's fish dock is spoken of, not built.
- Time: Monday 15 to Friday 19 October 1990; one game hour is 45 real seconds; hold Z to wait; beds skip to evening, last ferry or morning; clock stops in talk.
- Seeing: sight range 4 m plus 44 m scaled by light, cut by rain and mist; field of view about 120 degrees; a baked lamp light field feeds both the picture and the rule. Noise radius by action (walk 5 m, run 12, cab up to 30, fight 26), scaled by hour and rain. Nothing over heads by default; watchers show it with their bodies. A testing switch brings the meters back.
- Naming: face score is familiarity times closeness; coat at night times 0.4, cab 0.1 to 0.6; above 0.36 named, above 0.2 "the new owner", below that a man, a coat or a cab. A stranger can join the dots later.
- What they call him: knowing score; the new owner 0.2, Nowak 0.5, Tom 0.8, Tommy 1.05; the street's name is the highest one 40% of locals reach; liking never gates it; Sheila says "new management" to the end.
- Gossip: people on their routines pass their hottest story; certainty down 20% a telling; "heat" halves in about 20 game hours unless fed; one forced telling on Tuesday so day 2 always has a line back.
- The Ledger: only what Tom believes; by person, by event, what's open; gains an entry only from things he noticed or was told.
- Talk: live talk in two calls (the AI names the intent, the game decides, the AI voices the decided outcome from the card and known facts only); written fallback; content filter; suggested lines (three at most, Tab to open); decisions always the game's own yes and no lines.
- Money: starts at 23.50; fares 80p plus distance; the tin is dirty money; Sheila puts it through the fare book up to 10 pounds plus 80% of fares driven; rent 18 pounds Friday; Ron and Darren sell what they saw and heard.
- Night work (invented by the prototype): Monday holdall, Tuesday parcel, Wednesday collecting Iveson's 80 pounds against Ada's tea.
- The fire (invented by the prototype): No. 4 burned five weeks before. This differs from his ruled fire (see section 3).
- Fighting: ladder stare, square up, threaten, shove, strike, weapon out; giving way is nerve against the rung plus reputation; a killing needs a weapon, a man down and a separate key. The prototype also has Tom refuse to hit a woman, anyone 60 or over, or the priest: invented by the prototype, in neither canon nor combat-design.md, and not to reach the Unreal spec unruled.
- Hurt: no health bar by default; stoop, limp; beaten down, he wakes at Grace's kitchen, costs money and half the tin.
- Police: nightly statements from willing witnesses; constable at nine or Ellis for violence; 4 to 7 hours and 25 to 40 pounds; Ellis walks the street Thursday and Friday if loudness is over 2.2.
- Ending: Friday, Sheila's question (wind it down, take it on, or say nothing); end screen shows truth beside the Ledger, who told whom, the week in numbers, and six playtest questions; a copyable run report.
- Saving: to his Claude account through the page and to the browser; on sleep, after each beat, from pause.
- Its own "Not built" list: voices aloud, guns, a minimap, a second drivable car, interiors beyond Ada's, the Parade, Tom's past.
- People added for the prototype (PC Ibbotson, shopkeepers, Cammack's lads) are minor; Agar, the Widow, Cammack and Garbutt are names only.
- Its own shortfalls: the live follow-up line never heard live by its maker; frame time measured only at two views.

Where the page and the Core differ (the Core is the home of every rule, so these are faults to close in wave 1):
- Clock: the page runs 45 real seconds a game hour; the Core's rumour note (rumour-reach-2026-09-23.md) runs 2 game minutes a real second, 30 seconds a game hour.
- Gossip fading: the page's "heat" (how eagerly a story is passed on) halves in about 20 game hours; the Core halves a rumour's certainty every 96 game hours. These are different quantities, so neither number maps straight onto the other (unverified whether the page's certainty fades with time at all).
- Both feed the same question, "does the town know within thirty minutes", so a change to either changes the answer.

## 3. The systems

For each: in or out; the design question; what it hands the real game; its automatic checks; its wave (1 to 4, see section 4); its rough size in cloud hours (rough).

### Wave 1: one simulation, and what exists made right

**The real Core in the browser**
- In. Today: no; the page has its own JavaScript rules.
- Question: can the page run the game's own simulation, so the prototype and the Unreal game never disagree?
- Hands over: one simulation; every rule's home stays the Core.
- Checks: the 102,960 golden answers identical in the browser build; one town day timed.
- Size: 15 to 27 h (rough, from SIM-IN-BROWSER-2026-11-17.md). Download about 2 to 4 MB (not measured). Built on a GitHub build machine, so no cloud network setting is needed; his PC at most 2 hours. Needs one licence line from him.

**The warehouse fire, as ruled**
- In. Today: the prototype's invented "No. 4, five weeks before".
- Question: none for him; ruled 30 Sep ("the warehouse fire as drafted": the street's version is a street fact, the truth never the street's).
- Hands over: the fire of warehouse-fire-2026-09-29.md (the night watchman's lie, the scrap dealer's fittings, the page in Mickey's real book), as Act I's founding rumour.
- Checks: no line states the truth as a street fact; every fact traces to the draft.
- Size: 3 to 6 h (rough).
- The prototype's invented night jobs are story drafts the session may replace within canon (RULINGS 8 Nov), recorded in DECISIONS.md; no question for him.

**Witnesses and perception (seven slots, five rungs)**
- In. Today: yes, simplified.
- Question: can the player read who saw him without meters, and does light and noise feel fair?
- Hands over: sight, noise and naming numbers as one table; the seven slots per act.
- Checks: PerceptionGolden's 102,960 answers; a scripted lamp walk and dark doorway walk.
- Size: 8 to 15 h (rough), mostly joining to the Core.

**Gossip and memory**
- In. Today: yes.
- Question: does the town visibly know within thirty minutes, and is being talked about fun or noise?
- Hands over: telling rules, fading, reach per day, the forced Tuesday line or its replacement.
- Checks: Soak reach counts per seed; every telling has a meeting; no story without a witness; nothing ever wiped from a person's memory (canon's moat).
- Size: 6 to 10 h (rough).

**The Ledger (Tom's belief)**
- In. Today: yes, three parts.
- Question: is a book of beliefs, sometimes wrong, readable and worth opening?
- Hands over: entry triggers, wording rules (about 22 words a line), the truth against belief screen.
- Checks: every entry traces to a noticed event or a telling; never shows a fact he could not know.
- Size: 4 to 8 h (rough).

**Talk (live and written)**
- In. Today: yes. Voices aloud: out.
- Question: does free talk stay in character and never decide anything by itself?
- Hands over: the intent list, the two-call pattern, the yes/no/keep pattern, the line filters (twelve words, unknown names, content rule).
- Checks: the claim check and content gate over written lines; a stand-in model with planted bad replies, each dropped by name.
- Size: 10 to 20 h (rough); new scenes counted under story.

**Standing and names (the new owner to Tommy; Sheila's exception)**
- In. Today: yes.
- Question: does Tom feel his position rise without numbers?
- Hands over: knowing score thresholds; Sheila's trust rule (sheila-trust note, still open).
- Checks: a seeded week reaches each rung on a planned route; Sheila never names him before trust.
- Size: 3 to 6 h (rough).

**Day and night routines (including June Suddaby and Father Walsh)**
- In. Today: yes; routines carry gossip (caff breakfast, rank, fish queue, chapel).
- Question: are routines legible enough that the player can plan around them?
- Hands over: each regular's day as data, canon's day-life ring included.
- Checks: nobody vanishes in view; every person has a place each hour; weather changes attendance; the chapel is part of life, never a mechanic (canon: religion never a mechanic).
- Size: 6 to 12 h (rough).

**Street life (crowd, windows, barks)**
- In. Today: yes, rough.
- Question: does the street feel watched and alive at 0, 5, 10 and 20 visible people?
- Hands over: bark rules (say it once while it is news), window watchers.
- Checks: crowd generation passes the content rule (no children); every visible person has a simulation identity.
- Size: 4 to 8 h (rough).

**Weather and light**
- In. Today: drizzle and rain, night.
- Question: is rain cover the player uses?
- Hands over: one wetness value, its effect on sight, noise and attendance.
- Checks: dry, drizzle, rain runs change attendance but witnesses stay consistent.
- Size: 3 to 6 h (rough).

**Saving**
- In. Today: yes, page and browser.
- Question: does a save carry every memory exactly?
- Hands over: the save format (the Core's SaveCodec and TownSave once the Core runs in the page).
- Checks: SaveChaos-style reload at random moments gives the same next hour; every person's memories identical after reload.
- Size: 4 to 8 h (rough).

### Wave 2: the night and its costs

**Money and debts (fare book, the tin, laundering, Mickey's debt book, purses)**
- In. Today: fares, tin, laundering cap, rent, the debt book (collect or strike out).
- Question: does the clean and dirty split make the books a lie Tom must manage, without becoming an economy game (D24)?
- Hands over: fare and wash numbers, finite counterparty purses (counterparty-purses spec), the book state Act III's audit reads.
- Checks: no money from nowhere (sum of flows); laundering over cap is always noticed; many-seed balance runs.
- Size: 10 to 18 h (rough).

**The crime verbs (carry, collect, threaten, break in, fence, pay off)**
- In. Today: carry, collect, threaten, bribe.
- Question: which verbs make the night pull against the day?
- Hands over: a verb list with what each exposes in the seven slots; buying, selling and fencing, no crafting (ruled 23 Sep). Drugs never a verb (canon).
- Checks: every verb produces a perceivable event; content rule check on verb names.
- Size: 15 to 25 h (rough).

**Police and suspicion (statements, Ellis asking, arrest, custody, the file)**
- In. Today: statements, constable or Ellis, custody hours, Ellis asking on days 4 and 5.
- Question: is the police a pressure Tom can read and answer, never a game over?
- Hands over: statement rule, custody costs from the 1990 research, police asking (people remember being asked), the case joining crimes to the fire.
- Checks: no arrest without a statement; a refused or paid witness never states; asked people remember.
- Size: 10 to 18 h (rough).

**Combat, fists and street weapons**
- In. Settled by his rulings: 12 Oct (combat-design.md is the design; must look and feel AAA; guns only after melee works), 28 Oct (fists, improvised and carried weapons, rare guns), 30 Oct (fists knock out and never kill alone; a fall against a kerb, wall or step can kill, rarely, and the town treats it as a killing). Today: ladder to "weapon out", fists, block, step back.
- Question: does a fist fight feel weighty and readable in rough form, and does a weapon on Tom change how he is seen?
- Hands over: combat-design.md's ladder in numbers; improvised weapons (the street as weapon); carried weapons (cosh, knuckleduster, utility knife, flick knife, bat), with their rule: seen on you, found in a search, must be got rid of. Order inside the wave: the three gaps ordered in D56 first (outnumbered, running away, police arriving during a fight).
- Checks: fists never kill alone; a kill enters every witness's memory and the homicide chain (Core Homicide.cs); Tom never dies; a carried weapon is found in a search when on him. The prototype's "who Tom will not hit" rule gets no check until he rules on it.
- Size: 20 to 35 h (rough). AAA feel stays the Unreal game's job.

**The cab office (fares, radio, rank, yard)**
- In. Today: fares by car, Pauline calls them, the fare book; the radio is spoken of.
- Question: is the office the information room canon says (the radio nobody can help overhearing)?
- Hands over: fare rules, what the radio leaks and to whom, the yard's two escapes.
- Checks: every fare in the book; anything said near the radio becomes a telling.
- Size: 6 to 12 h (rough).

**Getting hurt and recovery**
- In. Today: yes (Grace's kitchen).
- Question: does losing cost hours and money, never the game?
- Hands over: the hurt states and their costs.
- Checks: Tom never dies; the recovery is seen by someone.
- Size: 2 to 4 h (rough).

### Wave 3: the squeeze

**Guns (July's five, rare and consequential)**
- In, last, after fists pass his playtest (12 Oct ruling). Today: none.
- Question: does a gun feel like a town event, not a mode?
- Hands over: July's five from weapons-spec.md, as reconciled in the combat note: sawn-off double-barrelled shotgun, old .38 revolver, .22 target pistol, heavy self-loading pistol, silenced .22 (whether to keep the last is that note's open question for him). All makes fictional. Armed police only when a gun is involved. Guns come from people, never random loot.
- Checks: one shot is a town-wide event; every shot is heard and reported by someone walking to a phone; a gun on Tom is noticed.
- Size: 10 to 20 h (rough, on box figures; the combat note's 6 to 10 agent weeks is for AAA feel in Unreal, not this).

**Jobs, crew and the empire firsts (first business, first recruit, first racket)**
- In. Today: Ron and Darren sell information; no crew on orders, no business beyond the office.
- Question: does a crew that acts on orders, and can be poached, plus a first business and a first racket, make Tom's rise felt?
- Hands over: open-city-spec.md section 2's four firsts (the fourth, a reacting rival, is under rivals); crew orders and loyalty; the job template (small state graph, 2 to 6 town-hour window, failure as kept state).
- Checks: each job's failure leaves a state the town can talk about; no job without a giver met on foot.
- Size: 25 to 40 h (rough).

**The three rivals (Agar, the Widow, Cammack) and the Fixer**
- In. Today: names only.
- Question: does each rival attack a different ledger (people, clean money, cover) and notice Tom only through its own people?
- Hands over: Act II's squeeze rules; the escalation ladder; Garbutt's true reads and one truce. The Widow works from the docks.
- Checks: a rival never acts on what none of its people saw; each rival reachable to a sit-down.
- Size: 25 to 40 h (rough).

**Love interests (Alison Sedman, Philip Danby)**
- In. Today: Alison as the reporter; Philip not present.
- Question: does someone worth being honest for pull against the night?
- Hands over: trust and friendship rules feeding the endings ("one friendship holds"). No sexual content (canon).
- Checks: the collision evening is always reachable; content gate on all lines.
- Size: 10 to 18 h (rough); Philip needs his card written (story is his to rule).

**The camcorder and CCTV witnesses**
- In. Today: a camera prop by the bus stop only, no rule behind it; no camcorder. Not in the C# Core either (no match by name).
- Question: does a witness that cannot be talked to, threatened or made to forget change how Tom plans?
- Hands over: a rule for tape (the bank's camera; tape recycled weekly; the second site is his to name, and the bank stands alone until he does) and the one camcorder (who holds it, where it goes).
- Checks: tape evidence expires on the weekly cycle; the camcorder's owner remembers like any person.
- Size: 6 to 12 h (rough).

**Story beats and endings (Acts I to III)**
- In. Today: Act I week only, ends at Sheila's question.
- Question: does the week become the on-ramp to a campaign, and is every ending's cost visible before it decides (D33, D58)?
- Hands over: the beat graph; the ending signs; the endings at the ruled count (28 Oct: "one main story with two or three endings"). The older outline and ActThree.cs have five (Quiet, Both, the Kingdom, the Straight Life, Burn Both); decision 2 settles how five become two or three.
- Checks: every ending reachable by a scripted route; no cost Tom could not see.
- Size: 35 to 60 h (rough; Act II in wave 3, Act III and the endings in wave 4).

### Wave 4: the place, filled out

**The Hook and the docks**
- In, as ruled 28 Oct: the Hook plus the docks; more districts in updates after release; if time runs short, the docks are cut first. Deep before wide (5 and 6 Nov). Today: the Hook and a slice of Copper Row.
- Question: do two districts, dense, hold the loop?
- Hands over: which routines, rivals and jobs live in each (the Widow's fish dock in the docks).
- Checks: every place has a reason in the loop (D24 spend rule).
- Size: 10 to 20 h (rough). The prototype's Copper Row slice stays as it is or is cut; the other five districts are after release. A pub stays a place without drink, which is a design task, not a subtraction (canon); the Parade waits for that design.

**Traffic behaviour**
- In, rough. Today: a bus and cars, keep left; behaviour unverified.
- Question: does traffic make the street real without becoming a driving game, and is the cab a witness and a cover?
- Hands over: traffic rules (keep left, stops, rank), 1990 kerbside rules (lane research note), what a car sees and is seen as.
- Checks: no car through a person or a wall; cabs always described by witnesses.
- Size: 8 to 15 h (rough).

**Shops and trade**
- In, small. Today: shops are small sets; a few purchases.
- Question: only what feeds perception or memory (D24): who sells to him, who refuses, what a shopkeeper saw.
- Hands over: a shop list and what each one knows.
- Checks: no alcohol or gambling goods; prices in 1990 pounds.
- Size: 4 to 8 h (rough).

**Side stories**
- In, three to five samples. Today: none as such.
- Question: do stories found on foot, no markers, keep the town dense?
- Hands over: three to five of the 32 drafts as playable samples (nothing multiplied before his approval).
- Checks: each ends in something the town knows; window at least 2 town hours.
- Size: 9 to 25 h (rough; 3 to 5 h each).

**Out of the prototype:** art quality, animation detail, performance targets, voices aloud, clothes, faces (his decision of 17 Nov). Also out: AAA driving (a rough cab stays), minigames, Tom's life before the Hook (canon), the five districts beyond the Hook and the docks.

**Total, all waves: about 270 to 500 cloud hours (rough, not measured).** Wave 1: 66 to 126. Wave 2: 63 to 112. Wave 3: 111 to 190. Wave 4: 31 to 68.

## 4. How it is built from here

- **Its place first.** RULINGS 29 Sep: no new system before its place in PLAN.md. The prototype stage gets its PLAN.md place, and wave 1 enters through the next Monday order, each item costed, as the week's rules require.
- **A source project in the repository.** A folder such as prototype/: the game split into files by system, a build step that outputs one HTML file (plus its pictures), and tests run by Node. Published to the same page, so his link never changes. Today the page's game code is one 1.21 MB file with no source in the repository (unverified whether Fable kept a source elsewhere); the first step is to bring it in as it is, then split it.
- **Who builds it.** The cloud session, within the week's production share, as Monday orders place it. Fable as his rulings stand: 10 Nov, only after two failed tries on code or tool faults; 16 to 23 Nov, up to 20% for the hardest code. Any wider role, such as Fable for big jumps in his own chat or a fixed share of the week, is new budget; decision 3 asks. Every change comes back into the repository source, never only onto the page.
- **One simulation, not two.** Preferred: the real C# Core compiled to WebAssembly and run in a background thread of the page (production/research/lane/SIM-IN-BROWSER-2026-11-17.md): the Core built cleanly and its 102,960 golden answers matched on a normal build; the two files with parts a browser cannot use (starting a helper program, the AI server's network handler) stay in the build and are never called in the browser; download about 2 to 4 MB (not measured); 15 to 27 cloud hours; built on a GitHub build machine, which can reach Microsoft's download sites, so no network setting is needed; his PC at most 2 hours; one licence line from him. The browser step itself is not yet proved. Fallback: JavaScript rules checked against the same golden answers exported as JSON (proved for three perception rules, 30 of 30 rows). Either way, a rule that differs between the page and the Core is a fault, and the Core is the home of the rule.
- **How it is judged.** Automatic checks per system (listed above), run on every build, failing the build. Plus his short playtests: 15 to 30 minutes, the page's own six playtest questions, the copied run report kept with the build. A wave is done when its checks pass and he has played it once.

## 5. The recipe side

Per RULINGS 9 Nov, these lines land first in NOTEBOOK.md; RECIPE.md is rewritten from it at the phase's end. The recipe map (RULINGS 16 Nov, the artifact the builder keeps) gains the new stage when RECIPE.md does. Confidence: low until LEDGER proves them.

- **New stage: a playable skeleton before production.** The whole game, rough, playable in a browser, before assets are multiplied. Changes chapter 0 ("in every chapter") and the plan's phase order: the skeleton answers design questions cheaply; Unreal builds from it. Confidence: low.
- **Feel studies before big systems.** A rough feel test (fight, cab, being watched) played by him before a system is built in Unreal. Adds to chapter 1 (research and targets) and chapter 8 (motion). Confidence: low.
- **The skeleton as spec of record.** Chapter 10 (simulation and its port) gains a third party: Core, port and prototype answer the same golden rows. Confidence: medium, since the rows already work for the Core and the port.
- **Testing.** Chapter 12 gains a browser walk: a scripted week run headless each night, its run report kept. Confidence: low.
- **Review gates.** Chapter 13: a system enters Unreal only after its prototype version passed its checks and his playtest. Confidence: low.

What would count as proof: (a) one system (for example fists and street weapons) built in Unreal from the prototype's numbers needs fewer tries than recent Unreal-first systems, by the time log; (b) his playtest verdict on the prototype predicts his verdict on the Unreal version; (c) zero rule differences between the page and the Core over a month of builds; (d) a design question settled in the browser that would otherwise have cost an Unreal build.

## 6. Decisions for Jafar

1. One simulation: the real Core runs in the browser, its numbers win where the page differs (clock, gossip fading), and the .NET runtime gets its licence line? Recommended: yes.
2. Endings: your ruling says two or three, the built story has five. Proposal: three, the Kingdom (with Quiet and Both as ways it can turn out), the Straight Life, and Burn Both? Recommended: yes, three as proposed.
3. Budget: build the prototype within the week's production share and the Fable rules as they stand, or add a share for it (Fable in your chat for big jumps)? Recommended: within the rules as they stand, until wave 1 has been played.
