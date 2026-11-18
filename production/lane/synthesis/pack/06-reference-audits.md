# 06. Reference audits digest

What this file is: a faithful digest of LEDGER's reference teardowns and coverage audits, for the synthesis pack. Nothing here is a new idea or an instruction; every line carries its source. Written 2026-11-18 from local files only.

How to read the numbers. No number in these sources was read from a game's own files, so the "(lead, from game files)" mark does not occur. External figures are developer or press statements (teardown) or search-channel summaries of named pages (coverage audits); CROSS-CUTTING.md section 7 item 2 says every quantity relayed in the five audits "is a direction, not a measurement". Figures about LEDGER's own code and runs are the audits' measurements of this repository.

Short names used below:
- TEARDOWN = ledger-v2/research/kcd2-rdr2-summary.md
- TEARDOWN-FULL = ledger-v2/research/full/kcd2-rdr2-teardown-FULL.md
- GTA = ledger-v2/research/gta6-triage.md
- WASTE = ledger-v2/research/waste-lessons.md
- FEAS = ledger-v2/research/ai-gamedev-feasibility-summary.md
- CC = production/research/coverage-audit/CROSS-CUTTING.md
- KCD2-S, KCD2-D = production/research/coverage-audit-kcd2/SUMMARY.md and DELIVERY.md (same pattern for HIT, RDR2, DE, SOD)

## 1. KCD2 and RDR2: what makes each immersive

Headline finding: what made both worlds alive splits into transferable systems logic (cheap) and non-transferable content mass (the arbitrage). (TEARDOWN, opening line)

### 1.1 Production numbers (developer-stated, not audited)

- RDR2: 500,000 recorded lines; 1,200 actors, 700 speaking; 2,200 motion-capture days; about 300,000 animations; some ambient NPCs with 80-page scripts. (TEARDOWN, THE NUMBERS)
- RDR2: 60-hour main story, main-story script about 2,000 pages, facial reference from about 60 to 70 cameras; actors cast for unrecognised voices. (TEARDOWN-FULL, B1)
- KCD2: 2.2 million-word script (about 25 novels, 11,000 screenplay pages); lead actor 508 booth hours across 127 sessions; about 250 staff; 40 to 45 million USD; five and a half years; about five hours of cutscenes. (TEARDOWN, THE NUMBERS; TEARDOWN-FULL, A4 and A5)
- Both used zero generative AI. Most of the spend bought dialogue variety and reactive lines; the spend that cannot be arbitraged is animation and physics fidelity. (TEARDOWN, THE NUMBERS)

### 1.2 KCD2, system by system

- NPC simulation: nearly 2,400 NPCs over two maps (2,048 m and 4,096 m square), about half in Kuttenberg, at a 60 fps target, by AI level of detail: full simulation only near the player, coarse schedule ticks elsewhere; limits set early. (TEARDOWN, Adopt from KCD2 1; TEARDOWN-FULL, A1)
- Behaviour architecture: goal-oriented action planning plus modular behaviour trees; per-NPC daily schedules; NPCs keep routines and react after the player leaves; the "two horses" discipline (a supported feature must be fully supported; only two NPCs own a horse). (TEARDOWN-FULL, A1; TEARDOWN, Adopt 7)
- Crime: witness-and-deduction; a resident near the scene suffices; an unwitnessed murder can go unpunished. (TEARDOWN, Adopt 2)
- Identification: "conspicuousness", the mean of worn items' values on a 0 to 100 scale; bright, expensive, bloodied or stolen clothing raises it, as do running and drawn weapons. (TEARDOWN-FULL, A2 item 2)
- Witness choice: report the player or blackmail him for silence. (TEARDOWN, Adopt 3)
- Punishment ladder: fine, jail, stocks or caning, branding, execution; the brand halves reputation gains and changes who will deal with you. (TEARDOWN, Adopt 4; TEARDOWN-FULL, A2 item 4)
- Reputation per settlement and per community, remediable by indulgences or pilgrimage. (TEARDOWN-FULL, A2 item 5)
- Needs and friction: food (spoils), sleep, bathing, dirt, blood, clothing as status, gear degradation; speech checks read appearance and prior actions. (TEARDOWN, Adopt 5; TEARDOWN-FULL, A3)
- Smell: a body-odour debuff broadcasts a detection circle around a dirty Henry. (TEARDOWN-FULL, A2)
- Saving: Saviour Schnapps manual save, plus Save and Exit and autosaves after dialogue and fights; community split. (TEARDOWN-FULL, A3)
- Quests: time-sensitive and self-resolving; the world proceeds without the player ("The Jaunt"). (TEARDOWN, Adopt 6; TEARDOWN-FULL, A4)

### 1.3 RDR2, system by system

- Witnesses: a witness runs to report; the player can intercept, threaten, bribe or kill; killing can mint a new witness (chains). LEDGER's era version: the run is to a phone box or the station, a built-in timer. (TEARDOWN, Adopt from RDR2 1; TEARDOWN-FULL, B3)
- Identification: binary, "Unknown Suspect" or named; mask, clothes or hair can prevent it for non-violent crimes; same clothes, horse and hair can get the player recognised even masked; lawmen who see directly identify through any disguise. Bounties cap at 1,500 dollars and are paid off at a post office. (TEARDOWN-FULL, B3)
- Camp as social hub: morale and contribution counters plus proximity chatter about recent events; higher morale means more donations and longer talk. (TEARDOWN, Adopt 2; TEARDOWN-FULL, B4)
- Greet and antagonise nearly anyone; shopkeeper memory is a scripted flag, not general memory; ambient lines repeat. (TEARDOWN-FULL, B1)
- Random-encounter skeletons with trigger conditions. (TEARDOWN, Adopt 3)
- Moving world furniture on schedules (their trains; LEDGER's buses, milk floats, brewery drays). (TEARDOWN, Adopt 4)
- Newspapers reporting player deeds. (TEARDOWN, Adopt 5)
- Honour: a single scalar, -8 to +8, gating discounts (10, 25, 50 percent), loot and the ending; self-corrects and is farmable. (TEARDOWN-FULL, B2)
- Animation: about 300,000 animations and Euphoria physics; seams show (insta-skin on slopes). (TEARDOWN-FULL, B5)
- World texture: weather, mud and snow accumulate on characters; shops open and close on schedules. (TEARDOWN-FULL, B6)

### 1.4 Shared conclusions

- Both games fake persistence: KCD2 deletes known felonies when punishment is accepted and wanted status expires in days; RDR2 witnesses live in short-lived bubbles. Permanent per-NPC memory plus gossip is what neither attempted. (TEARDOWN, Both games fake persistence)
- Reject: an honour-style global morality scalar; Euphoria-class physics and animation parity; forced save friction as default. (TEARDOWN, Reject)
- Failure modes: psychic guards (antidote: the what-they-know HUD); hollow generated people (Watch Dogs Legion); overpromised simulation (STALKER 2 A-Life); the repetition tell over long play, measured by the Phase 3 blind test. (TEARDOWN, Failure modes)
- Threshold rule: if performance forces a choice between more people and real memory, cut the people. (TEARDOWN, Threshold rule)

## 2. GTA VI triage (August), one line each

Source: GTA (Extended Look 2026-08-27 plus IGN 99-details transcript). Systems only. Pattern: GTA VI's most-praised systems are shallow global versions of the perception engine with excellent player-facing surfaces; the steals are mostly surfaces and verbs. (GTA, opening line)

Steal (GTA, STEAL):
1. What-they-know HUD (CCTV, clothes known, face seen, vehicle known, seen as couple, weapon; white-to-red stars; hollow stars) as the surface of the seven slots and the ladder.
2. Pre-crime prep verbs: masks, disguise slots, concealment, clean getaway vehicle, route choice.
3. Small shop robberies as a repeatable systemic petty-crime set.
4. Civilians who act: a courage value on witnesses; have-a-go heroes.
5. Eavesdropping that NPCs notice.
6. Contextual verbs on anyone (greet, intimidate, rob, mock) under typed or spoken input.
7. Cash on person versus bank, physically distinct; bankers' hours; the pub till launders.
8. Brand and media bible: recurring fictional brands, bands, adverts, TV, teams, pirate radio, pun shopfronts.
9. Barber as gossip hub; hair and stubble grow.
10. Non-lethal options surfaced in combat UI.
11. Era car theft: coat hanger, hotwire, or smash (loud); method sets the noise event.
12. Out-of-area vehicles implying a wider world.
13. Dogs: pet them; they bark at strangers and sneaks.
14. The town reacts to itself: breakdowns, deliveries, bin day, a funeral, with responders.

Adapt (GTA, ADAPT):
1. Criminal profile only as reputation derived from the belief network, never a stored meter.
2. Filming becomes gawker witnesses, the paper's photographer, and one camcorder in town.
3. Metabolism becomes appearance as information that NPCs pass on.
4. Public affection feeds the seen-as-couple slot.
5. Small period activities, each an information venue.
6. Legible escalation tiers on the existing law chain.
7. One postcard view per district within frame budget.

Skip (GTA, SKIP): modern social media; map scale and 80-hour breadth; destructibility; slow-motion focus meter; character switching; licensed soundtrack.

Era corrections (GTA, ERA CORRECTIONS): CCTV rare (bank, off-licence, weekly tape recycling, stealable tapes); pagers with phone-box callbacks; ram-raiding and joyriding; pirate radio and period fictional bands; VHS rental, arcade, teletext, pub satellite dish; match-day culture.

Note: Rockstar states no generative AI and no runtime AI characters in GTA VI; "the moat is uncontested". (GTA, NOTE)

## 3. Waste lessons and feasibility, one line each

### 3.1 Waste lessons (WASTE, numbered list; each is an operating rule in studio-v2/operations.md)

1. Turn ceilings too tight (four agents, about 398k tokens, nothing delivered): generous ceilings, resumable state, one deliverable per brief.
2. Standing constraints retyped into every brief: put them in agent definitions.
3. Multi-deliverable briefs gave partial delivery counted as none: one brief, one deliverable.
4. Shared scratch filenames collided and corrupted output: per-agent namespaced scratch.
5. A single-writer commit gate fought multi-agent work: branch per agent, an integrator merges.
6. Giant stale roadmap rows re-read at top-model prices: 80-word row cap, verified dates, doc-decay gate, history file.
7. Top-model use for mechanical work: routing law plus token ledger.
8. Decisions living only in session memory: canon.md and decision records, written the same day.
9. Lessons 1 and 3 relearned on 2026-09-16 (eight agents, about 1.3M tokens): budgets were declared (11 of 15 definitions) and never read at dispatch; a stop condition must be countable, have two exits, and each definition states its budget; first dispatch under that form delivered at call 26 of 30.
10. Checked negative: no bespoke world streaming at Phase B scale (Jafar, 2026-09-16; World Partition covers it); residents outside the streamed slice must still perceive, remember and gossip, which is a measurement, not research. (WASTE, Checked negatives)

### 3.2 Feasibility (FEAS, numbered list; scoped at a GTA-like, kept what survives the pivot)

1. Architecture: text data plus generator scripts are the source of truth; engine scenes are build products.
2. Density by agent-drivable techniques: modular kits, trim sheets, decals, rule-based scatter, fake-interior windows, HLOD and impostors.
3. Geodata: OSM or Overture footprints and road graph as skeleton, fictionalised; never ship Google 3D tiles.
4. Asset stack: headless Blender as processing hub; local TRELLIS for props; paid generators only when convenient; buy hero assets; local SDXL or Flux for PBR sets.
5. Faces and voice: Audio2Face-3D batch; hundreds of local voices; precompute fixed lines, runtime generation only for live talk.
6. Precompute doctrine: build-time generation gives a static library at zero per-player cost; runtime LLM and renderer share one GPU, budgets measured (once 38 tokens per second against 25 needed).
7. Honest limits: art coherence needs an enforced bible and calibrated judges; feel is hand-tuned; performance budgets from day one; no netcode.
8. Platform and legal: purely AI assets carry no US copyright; Steam requires disclosure of player-facing generative content; roughly a fifth of 2025 Steam releases disclosed AI.

## 4. Coverage audits

Method common to all five: each game's systems enumerated from one session's search channel and mapped against the 91 tiles of production/systems-inventory.json, as COVERED, PARTIAL, ABSENT or RULED OUT; absent items recommended IN, OUT, ASK or BENCHMARK. Not a census; combat was not enumerated in any. (CC, section 1 and section 7 item 7)

### 4.1 Kingdom Come Deliverance 2 (game 1)

Counts: 71 systems; 18 covered, 11 partial, 35 absent, 7 ruled out; of the absent 9 IN, 21 OUT, 5 ASK, plus a sixth ASK on save scarcity; five distinct things to build. (KCD2-D, section 1)

Conclusions:
- Already built but on no tile: blood on the player (noticed against distance and light, aged to a floor, washed in 25 minutes with water and privacy), object provenance across five origins, disguise ("buys doubt about the face; none about the car"), and the coat as a four-rung concealment limit. The inventory is incomplete about what it has. (KCD2-D, section 2; KCD2-S, One thing to know first)
- Built is not running: no verdict key or played build was found for these. (KCD2-D, section 2, HOLE)

What LEDGER lacks or must deliver (KCD2-S, Five things to take; costs from KCD2-D, section 5):
1. Appearance as something people see (dirty, torn, a different coat, another man's watch); small in code, moderate in art.
2. Carried things traced back to the act: the screen telling the player the watch is dangerous; small.
3. Sleeping and ending a day, with the town moving overnight; moderate.
4. Leaning on people as a system reading memory, appearance and who can hear, not stats; moderate, mostly writing.
5. The town changing behaviour after a crime (staying in, carrying something, asking for patrols); moderate. The audit cites LEDGER's own measurement that recognition talk landed below speaking level 1,944 times of 1,944.

Questions for Jafar: per-town or per-group opinion versus individuals only; what stops reloading to un-see a witness (lean: autosave at the moment of being seen); map, no map, or both; whether the built systems get tiles. (KCD2-S, Four questions)

Said no to: stats, 275 perks, use-based skills, crafting, hunger, illness, carry weight, horses, fast travel, a sentence wiping the record, next-town fencing, unexplained opening. (KCD2-S, What I said no to)

### 4.2 Hitman, World of Assassination (game 2)

Counts: 32 systems; 6 covered, 5 partial, 20 absent, 1 ruled out; of the absent 10 IN, 8 OUT, 2 ASK; five distinct things. High IN rate defended: Hitman's whole list is perception, disguise and evidence. (HIT-D, section 1)

Conclusion: a fifth built-but-untiled system, the four-rung concealment model in Core/Arsenal.cs (Innocent, Concealable, Damning, Impossible), which nothing in the game ever tests. (HIT-D, section 2)

What LEDGER lacks or must deliver (HIT-S, Five things to take):
1. Enforcers as a named system: who sees through a disguise is who knows you; small.
2. Blend-in: behaviour that needs no explaining for what you appear to be; moderate, mostly writing.
3. Bodies found at a time by a person, with hiding a body; moderate.
4. The camera and the tape: a witness with a one-week clock (canon already specifies it); small.
5. Finding a person from a description: the identification ladder run backwards; small model, needs a screen.
Smaller: a doorman pat-down; ringing a phone box to move someone. (HIT-S)

Questions: how much the player sees of being watched live (narrowed by RDR2-D section 3); whether anything ever tells the player who saw what. (HIT-S, Two questions)

Said no to: the reset structure (replay loop, mastery, Mission Stories), lookouts who see through anything, instinct mode. The audit warns LEDGER will meet Hitman's "players lost" problem and must solve it from the simulation. (HIT-S, What I said no to)

### 4.3 Red Dead Redemption 2 (game 3)

Counts: 36 systems; 6 covered, 8 partial, 20 absent, 2 ruled out; of the absent 5 IN, 14 OUT, 1 ASK, plus three INs in the partial column. (RDR2-D, section 1)

Conclusions:
- Clothing as identity is now in all three games so far; Core/Perception.cs rung-1 text ("a man, big, long coat") has nothing supplying it. (RDR2-D, section 2)
- RDR2's people despawn when the player leaves; LEDGER's headless run did seventeen days unwatched, logging 346 sightings and 508 sounds, an axis where LEDGER is already ahead. (RDR2-S, One result worth knowing)
- Correction to game 2: the unaware case (NeitherKnows, "the quiet horror case") is already decided in code to show nothing; only aware cases remain open. (RDR2-D, section 3)

What LEDGER lacks or must deliver (RDR2-S, Five things to take):
1. The town remembers the coat, not the face, so a new coat works until it is the remembered one; small.
2. The minute between being seen and being reported: pressure counts any living witness instantly, with no travel; one term in one function, moderate to make playable.
3. Nod or needle on every person, remembered; small, the cheapest in the audit.
4. Weather as an event that moves people (a downpour empties the street); small.
5. Personal habits on routines (the evening smoke) that make people predictable; small.

Question: town opinion versus people only, now raised three times. (RDR2-S, One question)

Said no to: survival layer, hunting, animals, horses, fishing, trains, fast travel, random encounters, honour; and two errors: lawmen seeing through any disguise, and the on-screen WITNESS banner. (RDR2-S, What I said no to)

### 4.4 Disco Elysium (game 4)

Counts: 26 systems; 5 covered, 1 partial, 15 absent, 5 ruled out (all by the no-player-progression ruling); of the absent 2 IN, 7 OUT, 2 ASK, 4 BENCHMARK. (DE-D, section 1)

Conclusion: D12 asks for a surface the project already builds for itself; the only public Why methods (PressureWhy, ProbeWhy) print which term moved, for debugging, never for the player; the gap is a caller and a screen. (DE-D, section 2)

What LEDGER lacks or must deliver (DE-S, Two things to take):
1. Show the working: the memory behind a belief or doubt surfaced before or after an attempt; small.
2. Failure that gives content: across 90 caught lies no spoken line differed, and truth ended at the same suspicion as silence; moderate, nearly all writing.

Question: does the game warn when a moment is permanent; to be answered with the save question. (DE-S, Two questions)

Benchmarks: about a million words, fourteen months, three voice directors and dozens of actors to voice it; one narrator eight months; Articy slowed and froze under the volume. (DE-S, Two numbers)

Said no to: the inner skill chorus, Thought Cabinet, skill points, stat clothing, dice, and an action-driven clock, which would delete the gossip mechanism. (DE-S, What I said no to)

### 4.5 Shadows of Doubt (game 5)

Counts: 23 systems; 6 covered, 1 partial, 16 absent, 0 ruled out; of the absent 7 IN, 5 OUT, 2 ASK, 2 BENCHMARK; two distinct new things. (SOD-D, section 2)

Conclusion, a warning: its generated cities, cases and documents read as repetitive to reviewers, and after a couple of cases only names and a fingerprint matter, a dominant strategy. Pillar 4 (no procedural filler without an authoring pass) is load-bearing; the tile "the cast" ("supplies names, not people") is the first three feet of the same road. (SOD-D, section 3; SOD-S, The warning first)

What LEDGER lacks or must deliver (SOD-S, Two things to take):
1. The man in the lit window as a witness: Core/Occupancy.cs lights windows but nobody looks out; small.
2. What is left at a scene: a print, a heel mark, a dropped object; in 1990 Britain fingerprints are the one mature forensic tool; moderate.

Question: a notebook journal or a corkboard with string. (SOD-S, One question)

For the studio: it precomputes each day (10 to 15 seconds) rather than simulating live; LEDGER runs live and has never stated the joint machine budget for street, local language model and voice model. (SOD-S, One thing for the studio)

Said no to: generated cases and documents, evidence that fades in hours, the player as arresting detective; the missing piece on LEDGER's side is being arrested. (SOD-S, What I said no to)

### 4.6 Cross-cutting (all five)

Totals: 188 systems; 41 covered (22 percent), 26 partial (14), 106 absent (56), 15 ruled out (8); of the absent 33 IN, 55 OUT, 12 ASK, 6 BENCHMARK; OUT is 52 percent of absent. (CC, section 1)

Conclusions:
- The only five-of-five gap: every game tells the player where they stand with the world; LEDGER has no such surface. (CC, section 2)
- This does not overturn D12 (what NPCs know stays unshown); the question is whether the player is shown his own position and why the game decided. (CC, section 2.1)
- Near misses: appearance as identity 4 of 5; gap between act and discovery 4 of 5; evidence at a place 3 of 5; group or district standing 2 of 5. (CC, section 2)
- Twenty distinct recommendations; five are half built (appearance, discovery gap, traceable objects, frisking, lit window) and should not be priced like the others. (CC, section 3)
- The inventory cannot see five systems it owns, and built is not running. (CC, section 5.1)
- The project already owns the Why idiom D12 asks for. (CC, section 5.2)
- Pillar 4 now has an empirical case (Shadows of Doubt). (CC, section 5.3)
- No system in 188 contradicts a pillar or decision record; the 15 ruled out fall to D11, D17 or D18. (CC, section 8)

What LEDGER lacks or must deliver, the twenty in order of agreement (CC, section 3):
1. Appearance as a perception input (three or more games).
2. The gap between the act and its discovery (three games).
3. The camera and the tape.
4. Sleep and crossing a day.
5. Objects traceable to what you did.
6. Enforcers: who sees through a disguise is who knows you.
7. Blend-in behaviour.
8. Frisking at a threshold, exercising the four concealment rungs.
9. Finding a person from a description.
10. The phone box as a distraction verb (small, conditional).
11. Town behaviour changing after a crime.
12. Persuasion and intimidation resolved from memory, not stats.
13. A codex entry on first contact with a system (rider on the first-hour tile).
14. Nod or needle on every person.
15. Weather as an event moving people indoors.
16. Personal habits making people predictable.
17. Show the working for social judgements.
18. Failure producing content.
19. The lit window as a witness.
20. Scene evidence: prints, heel mark, dropped object.

Seven questions for Jafar (CC, section 4): town opinion versus people; reloading to un-see a witness; map or walking and asking; how much being watched is shown live; whether anything tells who saw what; notebook or corkboard; tiles for built systems. Questions 4 and 5 go together, and so do 2 and 5.

Research topics not in the queue (CC, section 6): new, tooling to hold a large branching script; new, whether the simulation should run live at all; new, teaching a social system in thirty minutes; extension to topic 6, what a 1990 scene yields; extension to topic 11, group standing computed from individual records without a stored score.

Limits (CC, section 7): D24 does not exist in this checkout; no page was read in full (egress blocked; search summaries only); the key Hitman and Shadows of Doubt primary sources are blocked; two GDC talks paywalled; a Disco Elysium words-or-lines discrepancy unresolved; two silent search failures discarded; 188 is not a census; built is not running.
