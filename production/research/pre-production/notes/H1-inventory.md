> **Helper evidence note** for the pre-production review of 3 October 2026, kept as written by a read-only helper. Corrections found on checking are listed in ../SOURCES.md, "Corrections to the helper notes"; where they differ, the numbered sections govern.

# H1: LEDGER's pre-production inventory

Repository read at `main` 79cf8db (3 October 2026, 10:46 UTC). The checkout is shallow, so git dates are unreliable (most files show 1 October); every date below is the one written inside the file. Read only. Nothing in the repository was changed.

Verdicts: HAS = present, current and usable as a studio would expect; PARTLY = pieces exist but are scattered, stale, unadopted or incomplete; NOT = nothing serving the purpose.

| # | Item | Verdict |
|---|---|---|
| 1 | Vision, pillars, GDD, core loop, 30-minute scope | PARTLY |
| 2 | Art bible / visual target | PARTLY |
| 3 | Asset list with counts for the 30-minute build | PARTLY |
| 4 | Production method per asset family | PARTLY |
| 5 | Technical design | PARTLY |
| 6 | Performance budget, and measured | PARTLY |
| 7 | Pipeline and tools | PARTLY (tooling works, documentation scattered) |
| 8 | Legal and licensing | PARTLY |
| 9 | Money budget | PARTLY |
| 10 | Schedule with dates | NOT |
| 11 | Risk register | NOT |
| 12a | Vertical slice definition | PARTLY |
| 12b | Narrative bible and story | HAS (with gaps) |
| 12c | Audio direction | PARTLY |
| 12d | UI/UX style guide | HAS |
| 12e | QA / test plan | PARTLY |
| 12f | Build, release, distribution (friends' build) | PARTLY |
| 12g | Accessibility | PARTLY |
| 12h | Who does what | HAS (one inconsistency) |
| 12i | Approval process | HAS |

---

## 1. Vision, pillars and game design document

**Verdict: PARTLY.** The vision lives in canon and CLAUDE.md. The approved story and first hour are design documents. There is no current GDD. The only full design document and the only written pillars are archived and pre-date the Unreal switch.

- `canon.md` (approved 2026-08-31, edited since): the "Game" section ("open-town crime sim and social RPG. Single player, PC first"; third-person; Windows; one town of seven districts; the built street is Quay Street). "Tone" sets "grounded noir" and the visual target. "The moat (unchangeable)" works as pillars: seven perceivable slots, a five-rung identification ladder, permanent memory, gossip through schedules, live LLM talk, and a deterministic Core in which "LLMs classify, never adjudicate". "What LEDGER is not (D24)" is a scope fence: not open-world, not a shooter, not a driving game. The content rule (D18) is there too.
- `CLAUDE.md` "The one list" (Jafar, 3 October) sets the goal: "a thirty-minute build of Quay Street his friends play on this PC, which passes the Meridian Test". `NOW.md` repeats it with the builder's five items.
- `legacy/studio-v2/respec/vision-pillars-v2.md` (2026-08-31, 493 words, archived): the goal, the four Meridian Test conditions, six pillars, and "Worse at, and at peace with it". It says "small budget, no deadline". No current file links it; the only reference outside legacy is a research note citing it at its old path `ledger-v2/respec/`.
- `legacy/design-doc.md` (8,449 words, Unity era, marked "SUPERSEDED 2026-08-31"): the only full GDD. It has the premise ("two lives"), claims, pillars P1 to P5 and the core loop. It still has Mickey's as a pub and Unity 6.
- Core loop for the 30 minutes: `game-design/first-hour-2026-09-29.md`, approved by Jafar on 28/29 September (its `.approval.json`). Four steps: "He moves. He is seen ... It is written down ... It comes back". It also lays out the first hour minute by minute. Its own list says much is "Not built": the outfit's asks, Ada's tea, Ellis, the Ledger's screen, hints and the clock.
- The scope of the 30-minute build is spread over:
  - `NOW.md` items 2 to 5;
  - `production/research/checklist-sweep-2026-09-29/BUILDER.md` ("the twenty a friend would notice");
  - DECISIONS lines of 1 October (the friends' build on his PC, "nothing a friend sees unfinished");
  - `production/drafts/rulings-2026-10-03/RULINGS.md`, a consolidation of binding rulings marked as a draft "for the builder to apply".
- The archived decisions (`production/archive/DECISIONS-to-2026-09-24.md`, section "The genre", 23 September) rule G0 to G12 in or out: no jump, no multiplayer, English only, and so on.
- Stale design files still marked LIVE or SPEC: `game-design/how-to-play.md` ("LIVE, verified 2026-08-04": "your uncle Mickey's pub on Hook Street"), `game-design/agency-model.md` (July) and `ledger/README.md` (Unity M0).
- Missing compared with a studio:
  - one current GDD or one-page vision that names the pillars in force;
  - a single statement of what the 30-minute build contains: which first-hour beats, which characters and which systems are in it. DECISIONS line 111 refers to "the pillars" without saying which document holds them.

## 2. Art bible / visual target

**Verdict: PARTLY.** There is a strong bar: one approved image, two KCD2 frames and a rule for which source wins. There is no art bible with palette values, materials, texel or lighting standards in force, or a night reference.

- `production/reference/README.md`. The only approved concept image is `hook-sheet.png`, "from 22 September", 2048 x 1088, one street view generated by Z-Image-Turbo and approved by Jafar. Two things on it may not be cited (the second MICKEY'S sign and the third car).
- The KCD2 frames `kcd2-town-arcades.jpg` and `kcd2-town-fountain.jpg` (supplied 23 September) are both daytime.
- The rule (22 September): "THE SHEET GOVERNS MOOD, PALETTE AND COMPOSITION; THE PHOTOGRAPHS GOVERN WHAT THINGS ACTUALLY LOOKED LIKE".
- `production/reference/photographs.md`: links only, about seven period photographs (mostly Peter Marshall, Hull, all rights reserved). None is a file in the repository.
- `production/reference/hook-sheet-audit.md` checks the sheet against the research and canon: what it gets right, what it invented, and what may not be cited.
- `game-design/research/GOVERNS.md` ("verified 2026-09-21") routes 17 street asset families to a sheet panel and a research line. It warns that its rows were measured off the retired sheet: "treat every 'crop-verified' claim below as unverified".
- `game-design/research/art-direction.md` ("SPEC, 2026-08-25") gives numeric palette, saturation and texel-density rules. They were derived from five GTA V frames, and canon says "GTA V PS3 is retired as a reference bar".
- Rulings that act as art rules (archived DECISIONS):
  - D53 "grime is the strategy";
  - D40 "the sky is a photograph";
  - D28 "presentation is built early" (grain, grade and depth of field; ROADMAP says they are owed and not built);
  - the night ruling of 1 October ("pools of lamp light with darkness between").
- `production/specs/unreal-look.json`: the engine's look settings (gains, fog, wet film). These are tuning values, not targets.
- `production/research/aaa-street/SUMMARY.md` and `3-LIGHT-AND-GRADE.md` (1 October) recommend exposure, wetness, sodium-night and grade values. They are research, not adopted standards.
- Clothes have their own bar: `production/art/clothing/RUBRIC.md` (2 October). People's looks are set by `production/casting/*/SHEET.md`.
- Missing:
  - one art bible that pulls these together;
  - approved palette or values;
  - material, wear and texel standards for Unreal;
  - an approved night reference;
  - references for any view other than the hook camera. The other seven district sheets are "not re-approved".

## 3. Asset list for the 30-minute build, by family, with counts

**Verdict: PARTLY.** The newest plan counts variety per family, mostly for the whole town, with some Quay Street figures. No list says "the friends' build needs exactly these assets".

- `production/research/asset-plan/SUMMARY.md` (3 October; ruled binding the same day, DECISIONS "THE ASSET PLAN") covers 13 families. Examples of its counts:
  - building styles: "Quay Street needs four", 15 to 17 town-wide, 350 to 500 modules, six brick sets;
  - interiors: 12 shop rooms on Quay Street and about 20 mapped rooms;
  - cars: proof view 1 platform and 3 cars, street-wide 4 platforms and about 12 looks (none in the street until a proof passes, ruling of 2 October);
  - street furniture: about 25 kinds and 30 models;
  - containers: about 12;
  - signage: 12 fascias on Quay Street, about 300 cards and tickets, about 40 fly-posters;
  - wear: about 18 kinds;
  - vegetation: about 24 weed variants and 16 trees;
  - people: 14 principals, about 30 regulars, 30 to 40 passers-by;
  - clothes: about 40 base garments "for the first street".
- It is research ("Every effort figure is an estimate", "Nothing was seen in Unreal") and does not separate what the 30-minute build needs from what the street-wide pass and later stages need.
- `production/specs/vignette-bill-of-materials.md` and `.json` (2026-09-01): 77 lines with a route per item. It covers the D1b Unity-era vignette only and states "It is not the town". The asset plan found its G7 graffiti row still "HELD".
- `production/research/aaa-street/5-PROOF-FRAME.md` (1 October): a ranked work list of 13 items for one view. These are tasks, not assets.
- `production/research/asset-coverage/SUMMARY.md`: 84 kinds of material, "11 exist, 47 are part-done, 26 are absent". It is an older stocktake.
- Missing: one current asset list for the friends' build, per family, with counts, owner, source and state.

## 4. How each asset family is made

**Verdict: PARTLY.** The asset plan gives each family a source, a kit method, a reference and a first proof. Few of those methods are proven, and none is written as step-by-step tool instructions.

- `production/research/asset-plan/SUMMARY.md` (3 October) gives each family: professional practice, what is free, "We make" (for example: buildings extend `terrace-front.py` with three trim sheets and "our own brick-bond material"; cars use "a loft generator per body type"), the reference, and "the proof" with builder-day estimates.
- Proven pipelines in the repository:
  - shop rooms: `tools/art-recipes/shop-room.py`, "the method of Rita's window";
  - terrace fronts: `tools/art-recipes/terrace-front.py`, spec `production/specs/terrace-fronts.md`, 2026-09-21;
  - MetaHuman faces by script: `tools/ue/make_cast_metahumans.py`; faces are frozen;
  - accessories: `tools/meshgen/blender/model_accessory.py`; four passed blind review;
  - voices: `tools/voice-live/`.
- The clothing method is set out in `CLOTHES.md` and `production/research/clothing-pipeline/` (30 files). Tailoring is a "blocked capability", and the 3 October handover says "tailoring waits".
- The plan's own "What could not be verified": "Not tested in 5.8 here: shape grammar facades, Packed Level Actors, PCG clutter, the Crowd plugin, interior mapping on the RX 6700".
- Some current docs still name sources now removed: `ledger-v2/research/license-allowlist.md` entry 8 still admits the Game Animation Sample, and `aaa-street/SUMMARY.md` recommends Megascans. Both are out under the NoAI ruling of 3 October.
- Missing: a per-family production sheet (tool, version, steps, outputs, naming, checks), and a proven method for cars, the hill, crowd clothes, posters and the brick kit.

## 5. Technical design

**Verdict: PARTLY.** The architecture is real, partly specified and partly tested, but no technical design document describes it. It has to be pieced together from specs, decisions, config comments and code.

- Engine and rendering:
  - UE 5.8 (`production/d1-probe/ue-machine.txt`);
  - DX12 SM6, software Lumen GI and reflections, hardware ray tracing off, mesh distance fields on (`ue-probe/Config/DefaultEngine.ini`, with reasons in comments);
  - Nanite off at import; the simulation steps on a fixed clock of 0.1 s; 60 fps "met by drawing smaller and upscaling" (archived DECISIONS, 23 and 24 September).
- Game code: one Unreal module, `ue-probe/Source/LedgerProbe`, with 18 .cpp files and 57 headers. `CrimeProbe.cpp` has 9,394 lines and `VignetteShot.cpp` 9,121. The shipping game is the "probe" project.
- Simulation: the C# Core (`ledger/Assets/Scripts/Core`, 134 files) is the source of truth. A C++ port lives in the headers (Gossip.h, Perception.h, TownSave.h and others) and is checked against golden tables (`tools/port-golden-check.sh`, `ue-probe/tests/`).
- Talk: `production/specs/talk-protocol.md` (current) defines JSON lines on stdin and stdout between the game and `LedgerTalk.exe` (`ledger/TalkHelper`, C#). Its flags include `--early`, `--pending`, `--relay` and `--fake`.
- Voice: `tools/voice-live/voice-server.py`, a Python process beside the game with "one JSON line each way". Chatterbox Nano runs on the card through DirectML; the vocoder runs on the processor. Engine choice per character is in `production/specs/voice-engines.json`.
- Relay: `ledger/Relay`, ASP.NET (DECISIONS 2026-09-28). It is not hosted and is not used for the friends' build (DECISIONS 2026-10-01).
- `production/handovers/ROUTE.md` sets the hourly order of town calls the game must make, with acceptance rows.
- Data formats:
  - `production/specs/hook-cast.json` (40 people, places, ties);
  - `vignette-scene.json`, which generates `vignette-pieces.json`;
  - `garments.json`;
  - `production/specs/asset-interface.md` (GLB contract);
  - the save format through `SaveCodec.h` and `TownSave.h`.
- `ledger/README.md` is stale: "Unity 6 ... Current milestone: M0 tech spike".
- Missing: a current architecture document (processes, threads, data flow from game to talk to voice, failure modes, save schema, port status per system). The independent reviews of 30 September and 1 October found most faults in "the game's own wiring, which no test reaches".

## 6. Performance budget, and whether it is measured

**Verdict: PARTLY.** A whole-frame target exists and one fixed view is measured on every build-machine run. There are no per-asset, memory, draw-call or texture budgets, and play is not measured.

- The target (archived DECISIONS, Jafar, 23 September): "60 frames a second at Jafar's monitor's resolution on this card (the RX 6700), never below 30, with the voice running". On 24 September: "met by drawing smaller and upscaling". ROADMAP repeats it under stage 2.
- Measured: `production/d1-probe/ue-perf-verdict.txt`, written by `.github/workflows/ledger-probe-unreal.yml` on every run and read by `tools/slice-perf.py`. The latest (3 October, 12:35): `medianMs=13.32 p95Ms=15.05 ... fps=75.1 gpuMedianMs=11.43 ... gpuMemMB=3681`, at 3440x1440 with 50% screen percentage, the Nano voice on the card, and the slice standing still. The workflow says "This step reports and never turns the run red".
- `ROADMAP.md` says "the last measurement is from 24 September, before the MetaHumans, the shop rooms and the cloth", and asks for frames logged "by the route walk or the AI tester on every build". `tools/route_walk.py` and `tools/ai-tester/play.py` log no frame time. ROADMAP and the per-run file disagree.
- Per-asset: `production/specs/asset-interface.md` gives "Verts 56 to 2362 (median about 800) ... no LODs", measured from the existing props. It describes, it does not budget. `art-direction.md` R-C5 proposes a texel band of 384 to 1024 px/m but says to set it only after measuring, and it was never adopted.
- Research:
  - `game-design/research/performance-budget.md` (2026-08-25, Unity);
  - `production/research/unreal-frame-budget/SUMMARY.md` ("It is not a budget"; people simulated about 0.07 ms each);
  - `production/research/hardware-floor/SUMMARY.md` (minimum 12 GB of graphics memory, recommended 16 GB);
  - `aaa-street/3-LIGHT-AND-GRADE.md` (recommended 60 fps settings).
- No minimum spec has been adopted. The friends' build runs only on his PC (ruling of 1 October), but the sweep's basic #4 asks for "quality presets, so a weaker card than his still plays smoothly".

## 7. Pipeline and tools

**Verdict: PARTLY.** The tooling is extensive and much of it runs automatically. No current pipeline document ties the DCC tools, import, naming and validation together, and several tool READMEs are stale.

- DCC and engine:
  - Blender 4.5 headless, through recipes in `tools/art-recipes/` (terrace-front.py, shop-room.py, car-model.py and others) and `tools/meshgen/blender/`;
  - Unreal Python import and make scripts in `tools/ue/` (about 50: import_street.py, import_prop_meshes.py, make_cast_metahumans.py, make_wet_material.py and others);
  - image generation in `tools/imagegen` (stable-diffusion.cpp with Z-Image-Turbo);
  - voice tools in `tools/voice-live`, `voice-gen` and `voice-fetch`.
- The archived DECISIONS rule "Blender is for shapes and layout only; all look-development happens in Unreal" (23 September).
- Import, export and naming: `production/specs/asset-interface.md` sets GLB in metres, +Y up, file name = asset id, `SM_<id>` in Unreal, one material slot. It covers props only. Its "one material slot, unlit, untextured" rule may not fit the scanned and PBR work now planned (not checked against current imports).
- Validation and gates:
  - `tools/canon-gate.py`, `content-gate.py`, `names-gate.py`, `brand-verify.py`;
  - `attribution-check.py`, `git-size-guard.py` (pre-commit through `tools/hooks/pre-commit`);
  - `approvals.py`, `talk-protocol-check.py`, `retention.py` with `production/retention.json`.
- Build and CI: `.github/workflows/`, 11 files.
  - `ledger-core-tests.yml` runs on ubuntu.
  - `ledger-probe-unreal.yml` and `ledger-build-windows.yml` run on the self-hosted `ledger-pc` (his PC).
  - Some workflows are Unity-era: `ledger-build-mac.yml`, `citypack-*`.
- The sessions' workflow: `CLAUDE.md` (research first, the two-tries rule, the gate, one list); `NOW.md`, `TOWN.md` and `CLOTHES.md` for each lane; handovers in NOW.md.
- Stale READMEs:
  - `tools/meshgen/README.md` ("LIVE. Verified 2026-09-01", TRELLIS "Never yet run");
  - `ledger/README.md` (Unity);
  - FINDINGS notes the old launchers "still name the deleted wc26-picks".

## 8. Legal and licensing

**Verdict: PARTLY.** The licence allowlist, the NoAI ruling, an attribution file with a gate, the AI notice and an approved Steam AI disclosure all exist. Privacy, age rating, trade mark and the runtime model's terms are research only or absent, and the allowlist and THIRD-PARTY.md contradict newer rulings in places.

- `ledger-v2/research/license-allowlist.md` ("law"): ship-safe, never-ship and process lists. Entry 8 still admits "the Game Animation Sample and Lyra", which the NoAI ruling of 3 October removes. The file has no NoAI clause.
- The NoAI rule is in `CLAUDE.md` (lines 22 and 23) and DECISIONS (2026-10-03, lines 250, 252 and 262). The evidence is `production/specs/fab-noai-check-2026-10-03.md` (42 of 42 listings "No").
- `THIRD-PARTY.md` covers:
  - VCTK voices (CC BY 4.0, with the required credit text, "No credits screen shows it yet");
  - the Unreal EULA ("royalties apply only above its revenue threshold" and the credit notice);
  - MetaHuman;
  - Mixamo;
  - OFL fonts;
  - Poly Haven, ambientCG, Kenney and The Base Mesh (CC0);
  - MakeHuman (CC0);
  - the KCD2 and GTA screenshots as references only.
- Gaps in THIRD-PARTY.md:
  - no row for the live voice engine's weights (Chatterbox Nano);
  - no row for the Anthropic terms the live talk runs under;
  - "What this project made itself" is Unity-era ("All geometry procedural", "Music procedural layer, M13");
  - a heading "Textures, props, vehicles — NOTHING YET" is kept as a log.
- Voice consent: VCTK consent is "taken as covering cloned characters, as a stated risk" (DECISIONS 2026-09-24). Evidence: `production/research/tts-licensing-and-consent/VOICE-PERMISSIONS-2026-09-24.md`. The voice watermark is kept (D50).
- AI disclosure:
  - the in-game AI notice and the report button are in the Core (DECISIONS 2026-09-28, `AiNotice.cs`), with on-screen handover to the builder;
  - `production/store/steam-ai-disclosure.md`, approved 2026-09-30;
  - `production/research/steam-ai-disclosure/NOTE-2026-09-29.md`.
- Privacy: `production/research/player-data-notice/NOTE-2026-09-28.md` (GDPR, UK GDPR, Swiss FADP Art. 19, AI Act Art. 50). It says the notice's wording is "slightly off" and becomes true only once the relay is hosted. There is no privacy policy.
- Real names, brands and trade marks:
  - canon "Brands and law" (everything fictional) plus the gates;
  - the brand bible `content/brands/brand-bible-v1.json` still says "MICKEY'S IS A PUB" (asset-plan fault 3);
  - the trade mark check on "LEDGER" was researched (`production/research/ui-design/BRANDING.md`) and deferred "before any Steam page".
- Age rating: only checklist row T4 "Age rating submission", marked "later". Nothing else.
- Engine EULA: the THIRD-PARTY row above. MetaHuman's AI clause and the Fab EULA are known from search summaries only ("UNREACHED", asset-plan 0-SOURCES).

## 9. Money budget

**Verdict: PARTLY.** There are caps and rules on spending, but no budget: no total, no statement of what has been spent, and no monthly figure in force.

- `CLAUDE.md`: "he pays for Max, not for API calls on top". There are no API calls in development.
- DECISIONS 2026-10-03: LEDGER's key may spend "at most one dollar a day in total across sessions", each run logged in `production/playtest/talk-runs.jsonl`.
- `TOWN.md`: "The key's cap is enforced in code".
- Per copy, `ledger/Relay` defaults to $0.50 a day and $5 a month, and "stops every call at 80% of our month's budget". The month's budget is unset: "Where it runs, and the budget, are Jafar's" (DECISIONS 2026-09-28 and 09-29).
- Measured cost of talk: `production/playtest/talk-cost-2026-09-30-after.md` gives "an hour of steady talk at 120 turns: US$2.14".
- Purchases: "nothing bought without his yes, none for the street or cars" (RULINGS draft), no paid voice service (29 September), and the relay goes on his existing Hetzner server (28 September).
- Marvelous Designer at $39 was approved on 25 September and its trial was later cancelled. The 3 October clothes summary in FOR-JAFAR.md still asks him to buy a $39.99 jacket, while the 3 October ruling says "no purchases or commissions".
- The only spend plan is D6 (`legacy/studio-v2/respec/decision-register/D6-spend.md`, 2026-08-31): "roughly 50 to 150 per month average, 300 to 700 one-off in year one", with no currency stated. The archived DECISIONS say D6 is "DELIBERATELY ABSENT" from the binding decisions because it concerns the studio.
- Missing: monthly and total figures, what has been spent to date, the subscriptions he pays for (Max tier, Dropbox, Hetzner), and the relay's month budget.

## 10. Schedule

**Verdict: NOT.** Milestones exist in order. None has a date.

- `ROADMAP.md`: "Now" (the integrated encounter, passed 24 September), "Next" (a 10 to 15 minute slice; its status paragraph is from 24 September), "Then" (the friends' build) and six stages. Each stage says how it is judged, with no dates.
- `NOW.md`: items 1 to 5 in order. The weekly GOAL runs "until Sunday 4 October 20:00". The only time estimate on the list is item 3, "about two days".
- Effort estimates appear only in research: the proof view takes "about six to ten weeks of builder work" or "30 to 50 builder-days" (`aaa-street/SUMMARY.md`), and each asset-plan family proof is given in builder-days.
- `vision-pillars-v2.md` (archived): "no deadline".
- Missing: target dates for the proof view, the street-wide pass and the friends' build, and any tracking of estimates against actual time.

## 11. Risk register

**Verdict: NOT.**

- No file lists risks with likelihood, consequence, mitigation and an owner. Searches for "risk register", "likelihood" and "risks:" outside legacy found none.
- `FINDINGS.md` is "Unresolved faults only, at most twenty". It is a list of known faults (talk delay 5.4 s, invented details 7%, underlit faces, Mickey's past contradicting itself and others). Each fault is a problem already present, not a risk scored for likelihood.
- Risk-like items are scattered:
  - "stated risk" for VCTK consent and SLR83 ShareAlike (DECISIONS 24 September);
  - audits naming "the biggest risk" (`production/audits/2026-09-24-local-replacement-audit.md`);
  - "the coat being the risk" (asset plan);
  - blocked capabilities in "Needs you" (CLAUDE.md).

## 12. Other items

### a. Vertical slice definition: PARTLY

- `ROADMAP.md` defines the encounter (seven tests, passed) and the 10 to 15 minute slice ("Walk the street, talk to two or three people ... at 60 frames a second").
- The goal and the Meridian Test are in CLAUDE.md and NOW.md. The proof view is defined (NOW 2.1 to 2.13, `aaa-street/5-PROOF-FRAME.md`).
- "Nothing is multiplied until one complete sample has been approved" is in CLAUDE.md.
- Missing:
  - one definition of what the friends' 30-minute slice contains: which first-hour beats are in (the first hour lists many as "Not built") and which characters can talk;
  - ROADMAP's slice status, which is dated 24 September;
  - ROADMAP's "Then", which requires a relay, while DECISIONS of 1 October say "no relay" for friends.

### b. Narrative bible and story: HAS (with gaps)

- `canon.md`: world facts, cast, premise and the content rule.
- `game-design/story-outline-2026-09-28.md`, approved 28 September (`.approval.json`): the spine, three acts and five endings.
- `game-design/first-hour-2026-09-29.md`, approved.
- Nine first-week designs approved "as written" (RULINGS draft, 29 September): `game-design/*-2026-09-29.md`.
- Character sheets with approvals: `production/casting/<name>/SHEET.md` for 14 principals and `regulars/REGULARS.md`. `production/casting/CASTING.md` gives the census and three tiers. `production/specs/hook-cast.json` holds 40 people and their ties.
- Gaps:
  - Act II and III exist only in outline;
  - the outline marks Philip Danby's thread "still to write";
  - the brand bible still owes names (the paper, the club, radio, car makers, the council), which the town session is to mint on Monday;
  - FINDINGS: Mickey's past contradicts itself;
  - `production/cast/cards/` holds only three cards (lena, rocco, sam).

### c. Audio direction: PARTLY

- D26 (`legacy/.../D26-sound-is-a-lane.md`, 14 September): sound is a lane, CC0 libraries and the engine only, "NO NEW TOOLING".
- D42 (15 September): "SOUND HAS NO SUCH SHEET ... the test is my ear at the end".
- Voices: `game-design/voice-casting.md`, `production/research/voice-direction/` (30 September; recommends about −23 LUFS, research only), and voices chosen per the RULINGS draft.
- `production/specs/street-sounds.json` (ambience, cues; FINDINGS says the five crowd lines are out of use), and `production/research/footsteps/`.
- Missing: an audio style guide or reference bed, mix and loudness targets adopted, music direction (the allowlist names MusicGen; THIRD-PARTY's "Music procedural layer, M13" is Unity-era), and the radio.

### d. UI/UX style guide: HAS

- `production/design/ui/STYLE-GUIDE.md` (2,452 words): "The evening paper", picked by Jafar on 1 October. It covers principles, layout units and safe region, type, colour with measured contrast, parts and states, and notes for Unreal.
- `production/design/ui/README.md` records his answers, with a kit and screens in `step2/`.
- Research: `production/research/ui-design/`.
- Open: "The finish" (scanned paper and similar) waits; branding is deferred.

### e. QA / test plan: PARTLY

- Automated:
  - Core suites (CoreTests, Soak, SaveChaos, PerceptionGolden, StrangerTest, named in CLAUDE.md);
  - port goldens;
  - the build machine's probe verdicts (`production/d1-probe/*-verdict.txt`);
  - the AI tester's nightly walk (`tools/ai-tester/play.py`, `production/playtest/ai-tester/`), whose new "does the town know Tom" report is to start on 4 October;
  - independent reviews (`production/audits/review-2026-09-30`, `review-2026-10-01`).
- Human: `production/playtest/RUNBOOK.md` (the friends' protocol: shut up and watch, four things to write down) and `production/research/meridian-test-administration/` (19 September).
- `game-design/qa-matrix.md` ("LIVE, verified 2026-08-04") and `game-design/testing-system.md` are Unity-era.
- Missing: a current test plan for the Unreal game naming coverage per system, since the reviews say no test reaches "the game's own wiring". Nothing gates frame time. There is no acceptance checklist for the friends' build beyond the twenty basics.

### f. Build, release and distribution: PARTLY

- Friends' build: on his PC, "a shortcut in a fresh Windows account, no relay; the twenty basics; nothing a friend sees unfinished; Sheila's face whole when she talks; no debug text" (DECISIONS 2026-10-01, RULINGS draft).
- The voice stopgap is packed into the game's folder (`tools/voice-live/make_portable.py`, DECISIONS 2026-09-30). The played copy is at `F:\LedgerTools\played-game`, and retention keeps the latest two builds (CLAUDE.md).
- Beyond friends:
  - ROADMAP "Then" lists the relay, AI notice, reporting, Steam's safeguards and the content rule;
  - the business direction is "provisional: sold once, an allowance of live talk per copy";
  - the Steam AI disclosure is approved;
  - store page, pricing, patching, DRM and age rating are open checklist rows (T1, T4, T6, marked "later").
- Missing: a release plan, a build-versioning and sign-off checklist for a release candidate, and a distribution plan past his PC.

### g. Accessibility: PARTLY

- The archived DECISIONS (23 September) count "all settings, all accessibility" as FLOOR. G11: "Difficulty exists only as accessibility assists".
- `production/research/ui-design/PIPELINE-AND-STANDARDS.md` lists the settings to offer (subtitles in four sizes, remapping, hold or toggle, motion, colour).
- The game has subtitles on/off and size, invert look, sensitivity, presets and volume (`ue-probe/Source/LedgerProbe/Private/LedgerSettings.cpp`).
- The friends' build sweep marks fuller accessibility "later" (`checklist-sweep-2026-09-29/BUILDER.md`, rows A01.10, A42.08, A43.03, A43.07).
- No adopted accessibility spec.

### h. Who does what: HAS (one inconsistency)

- `CLAUDE.md` "Three sessions, one repository":
  - the builder: main, Unreal, art, faces, voices, the graphics card;
  - the town: worktree on branch town, simulation, talk, documents;
  - clothing: Blender only.
- Each lane has its own file (`TOWN.md`, `CLOTHES.md`), and handovers go in NOW.md.
- Jafar answers canon, scope and money on pages, approves people, voices, clothes and whole frames, and is the only purchaser.
- Gaps:
  - CLAUDE.md's first line still says "Two sessions ... (see 'Two sessions, one repository')";
  - the cloud session (it wrote the rulings drafts and asset-plan research), the build machine, the AI tester and the fresh reviewers act in practice but are not given roles in that section.

### i. Approval process: HAS

- CLAUDE.md "How to work":
  - "THE GATE": own check against references, then a fresh reviewer;
  - what reaches his page;
  - every page fits one phone screen;
  - pictures shown at 2560 x 1440;
  - "NOTHING REACHES HIS PAGE WITH A VISIBLE FAULT";
  - "READ HIS PAGES' PICKS".
- `tools/approvals.py`: an approval sits beside what it approves and lapses when its sources change. `production/specs/in-game.json` lists 8 placed items.
- Pages are built by `tools/candidate_page.py` and `tools/page_pictures.py`. Records are in `production/approvals/`, with 26 dated folders up to 2026-10-02.
- Big items need an independent review before "done".

---

## Could not determine

- What the measured performance view contains: whether `-LedgerSlice` standing still includes the MetaHumans, shop rooms and cloth, so whether ROADMAP's "last measurement 24 September" or the per-run file is the right reading. Frame time in actual play was not found anywhere.
- Actual money spent to date, the Claude Max tier now paid (D6 said Max 5x; a legacy note says Max 20x), and the Dropbox and Hetzner costs.
- The contents of Jafar's claude.ai pages and their stored verdicts. They were not read, so approvals given only on pages and not yet copied into the repository are not counted here.
- Anything on his PC outside git: F:\LedgerTools (bodies, garments, approvals, builds) and the build machine's state.
- Whether the rulings drafts (`production/drafts/rulings-2026-10-03/`) have been applied. Their NOTES say "Nothing live is replaced until the builder applies them".
- Whether he has switched off "Help improve Claude" (Needs you item 3).
- The exact current wording of the Fab EULA and the MetaHuman AI clause (unreached by the research; search summaries only).
- Whether `asset-interface.md`'s one-slot, unlit material contract still governs the props now being made.
