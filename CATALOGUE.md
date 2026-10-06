# CATALOGUE: what exists, and where each fact lives

Phase 0, item 0.4 (PLAN.md; his edit 9). Search this, canon, the research library and every branch before making anything new (CLAUDE.md). tools/catalogue.py fails the build when a folder of production/art or production/research has no line here. Method: production/research/catalogue-and-homes/NOTE.md. Branches, old repositories and drive folders: production/audits/sweep-2026-10-05/SWEEP.md.

## One home for each kind of fact

| Fact | Its home | Derived from it, and what checks them |
|---|---|---|
| Premise, period, names, content rule | canon.md (outranks all) | everything; tools/canon-gate.py, tools/content-gate.py |
| His rulings; how the work runs | RULINGS.md; CLAUDE.md | tools/doc-caps.py |
| His page answers | production/approvals/answers/ | DECISIONS lines; tools/page_answers.py |
| The town's map and districts | production/art/atlas-01/data/atlas.json (adopted 5 October, updated to the built street 6 October; canon.md's seven districts) | the built street's place; district art. Checked: production/art/atlas-01/scripts/check.py (the street's length, climb and bend read from the built street) |
| Quay Street as built | production/specs/vignette-scene.json | vignette-pieces.json and feet (CoreTests fails on drift), the Unreal street (tools/spec-test-check.sh) |
| Trades and shop names | RULINGS.md (trades line) | shop-interiors.json, signs, content/brands (tools/brand-verify.py) |
| The cast | production/casting/CASTING.md and each SHEET.md | talk cards, the Unreal cast, street lines. No automatic check yet (cast-vs-sheets.md, 5 October, by hand) |
| Faces and voices in use | RULINGS.md (faces frozen, voices); production/casting/voice-key.json | the game's MetaHumans and voices; tools/approvals.py |
| The simulation's rules | the C# Core (ledger/Assets/Scripts/Core) and its golden tables | the Unreal port; tools/port-golden-check.sh, PerceptionGolden |
| The street's people | the simulation's residents (the Core) | production/specs/street-people.json. Checked: tools/homes_check.py (every figure on the street stands for a resident or is ruled scenery) |
| The look | production/specs/unreal-look.json, judged against production/reference/hook-sheet.png | the Unreal materials and grade |
| The story | game-design/story-outline-2026-09-28.md and first-hour-2026-09-29.md (approved) | talk facts and lines; canon-gate |
| Sources and licences | THIRD-PARTY.md; ledger-v2/research/license-allowlist.md | tools/attribution-check.py |
| The friends' build's requirements | production/friends-build/MAP.md (every ruling and the twenty basics, each with owner and proof) | PLAN.md's phases 3 and 4 |
| The plan and the current item | PLAN.md, then NOW.md | the overview's morning line (tools/morning_pictures.py) |
| Time spent | production/time-log.jsonl | tools/timelog.py week |

## Where two versions disagree today

1. **The built street against the atlas.** Agree: 6 m road, 2 m pavements, 6 m bays, Mickey's at the quay end of the east side (8 m deep), the fish shop next, the yard gap at 21 to 24 m. Disagree: the street is 48 m with the chandler's at 40 to 46 m, the atlas 42 m with no chandler's; the atlas puts the Old Basin and the Harbour Board at the quay end, the built street shows plain brick walls and an outsized tree there (the morning reverse view); the atlas marks Mickey's as a pub, the Ironside works' club and the Gullwing arcade, against the content rule and canon's cab office.
2. **The C# simulation against the Unreal port** (port-vs-core.md): the golden check passes, 57,913 checks over 57,876 rows, but skips 7 (the player's claims, unported) and silently drops one (the police order); random scripts run through both found no difference in 650,000 runs. 21 disagreements: 5 rules live only in the C++ (the two highest: who sees the window by hour, light and distance, and familiarity rising from meetings, which decides recognition, the report and the arrest), 8 C# rules are not ported, 6 are wired differently, and 11 of 30 planted one-line breaks in the port fail no test. Those five C++-only rules have no home in the Core.
3. **The game's cast against the casting sheets** (cast-vs-sheets.md): 32 disagreements, 3 high: the three principals wear the white base layer (Sheila and Darren barefoot) where their sheets give a cardigan and skirt, a donkey jacket and a shell suit, which RULINGS allows only meanwhile; Sheila's frozen face has short dark hair and no spectacles against her sheet's greying set and spectacles on a chain; Martha, Kate and Leonard have no sheet at all. The game has spoken with Nano since 24 September, chosen against two other engines but never re-tested against the one he preferred 7 to 2 on 23 September. Mickey's past differs only between CASTING.md and canon; the game never says it.
4. **The street's walkers against the residents** (walkers-vs-residents.md): of 13 figures on the street, 6 have a resident behind them and only Ron, Sheila and Darren perceive and remember; no ruling makes any of them scenery. Three placeholder figures stand where the window's witnesses should be (Martha before Rita's pane, Leonard on Ada's step, Kate across the road) and file nothing. 38 of the simulation's 41 residents are never drawn, six of last night's eight witnesses among them.
5. **Approvals.** 26 approval files, 24 current; eight things are in the game without a current approval (tools/approvals.py): the three principals as dressed now, the window's witness lines, the street's light and grade, pieces and sound, the four window interiors.
6. **Answers given by message only**: Thursday's four looks and three keys (q-ending-signs, regulars, ron-street-lines) have no stored answer (page-answers-check.md).

## Maps and district plans

- **The September atlas** (branch art/atlas-01, 22 September; to him on Monday's Sweep page): the map of Meridian's seven districts with routes, landmarks and contours (data/atlas.json), a plan of Quay Street, seven district plans, "how the town talks", a town form bible, Mickey's plans (as a pub: out), research references with their rights. An older copy, 9 September, in the old wc26-picks repository.
- **production/art/atlas-01**: the first review of the atlas and street frames of September. **production/art/atlas-02**: the atlas's second research batch (clothing by occupation, hillside housing, household contents, transport timetables, and a small pub's plan, out under the content rule).
- **canon.md**: the seven districts and Quay Street's three sides, in words.

## Concept images and references

- **The Hook sheet** (production/reference/hook-sheet.png): the bar for mood, palette and composition; the retired sheet of 9 September beside it; photographs.md lists the dated photographs. Other games' frames live on F: only (F:\LedgerTools\reference-other-games).
- **District concepts**: concept-copper-row-2026-09-10 and concept-fairview-2026-09-10 (production/art); the atlas's eight AI sheets (on its branch; bars and beer in the Hook's and the Parade's).
- **Casting concepts**: each character's folder under production/casting, with candidates of 25 to 29 September.

## Approved

Beside what they approve (*.approval.json; tools/approvals.py): the story outline, the first hour, the warehouse fire; twelve casting sheets (Ada, Alison Sedman, Carol Ellis, Danny Cammack, Father Emil, Geoffrey Agar, June, Maureen Jensen, Philip Danby, the fixer, Tom Nowak, the regulars) and Ron's street lines; Ron's face P2 and Sheila's S4; Ron's and Darren's game voices of 25 September; two thinking sounds, Ron's threat take B, the talk light, Sheila's little look; Steam's AI disclosure. Faces frozen by RULINGS: Ron P2, Sheila S4, Darren S6.

## Art (production/art)

- atlas-01, atlas-02: above.
- clothing: garment tests, the clothes rubric (RUBRIC.md), jacket and suit films, footwear and Sheila's pieces.
- clutter-2026-09-29: ten pieces of 1990 street clutter.
- compare: side-by-side frames of the street against references.
- concept-copper-row-2026-09-10, concept-fairview-2026-09-10: district concepts.
- facades: facade drawings and tries.
- fascia-01: Mickey's fascia package to a real mesh.
- hair-2026-09-29: a hair study.
- interiors-2026-09-23: the four window interiors (no current approval).
- lighting: the talk light and evening light tests.
- mickeys-cars: the cars considered for Mickey's (cars are off until convincing).
- shop-rooms: each shop's room plans and pictures. Its pawnbroker-goods-sources.md: every model in Rita's window and its licence (tools/art-recipes/verify_display_sources.py).
- mickeys-props: Mickey's office's hero props, modelled by script in Blender (tools/art-recipes/mickeys-props/; the meshes on F:/LedgerTools/game-inputs), 6 October.
- ui: the interface's screens.

## Research (production/research), by subject

- **The street and its look**: aaa-street, asset-plan, asset-coverage, asset-packs, photoreal-on-a-budget, 1990-on-film-stock, evening-light-1990, broken-window-look, chimney-smoke, shop-glass-reflections, shop-window-interiors, interior-blockout, cab-office-interior-1990, street-clutter-1990, period-vehicles-and-props, unreal-frame-budget, unreal-cache-cap, hardware-floor, third-person-camera-interiors, footsteps, atlas-01 (the atlas's evidence).
- **The town and its people**: rumour-propagation, small-town-networks, small-town-meetings, eyewitness-testimony, gaze-and-knowing, group-standing-without-a-score, precomputed-day, game-clock, waiting, players-and-a-world-that-remembers, holding-information, detection-legibility, emergent-story-legibility, ending-reading, authored-stories-in-simulation, crime-and-combat-coverage, failure-after-arrest, police-response-1990, british-policing-1988-1992, crime-scene-1990, threats-1990, shop-hours-1990, cab-office-1990, british-crime-fiction-tone, casting, cast-cards, hitman-density.
- **Talk and voices**: voice-off-card, grounded-dialogue-selection, grounded-replies, invented-claims, conversation-model-capability, local-models, local-writers, llm-inference-economics, prompt-caching, live-speech-architecture, talk-helper, ambient-lines, street-lines-1990, holding-a-large-script, voice-alternatives-2026-09-24, voice-direction, voice-in-the-game, voice-latency, nano-listening-test, tts-licensing-and-consent, runtime-ai-business, ai-npc-demos-hollow, steam-ai-disclosure, player-data-notice.
- **People on screen**: sit-and-turn, character-pipeline, metahuman-audio-driven-animation, lip-sync, talking-face-faults, natural-idles, townspeople-animation, markerless-mocap, clothing-pipeline, clothing-assembly-line, game-clothing-pipeline, plain-1990-clothes, free-garments, wardrobe-at-scale.
- **Play, testing and players**: baseline-features, feature-coverage, brief-coverage, coverage-audit, coverage-audit-disco-elysium, coverage-audit-hitman, coverage-audit-kcd2, coverage-audit-rdr2, coverage-audit-shadows-of-doubt, teaching-in-thirty-minutes, meridian-test-administration, packaged-game-testing, shipping-build, engine-notices, ai-tester, ui-design, ethics-and-reception.
- **How the work is done**: pre-production, agentic-studio-attempts, small-team-shipping, systemic-game-postmortems, content-mass-and-judgement, self-audit, checklist-sweep-2026-09-28, checklist-sweep-2026-09-29, claude-code-goal, blender-mcp, graphify-evaluation, egress-allowlist, terms-2026-10-03, catalogue-and-homes, git-history-clean-2026-10-04.md, README.md.

Older research outside these folders: ledger-v2/research (the licence allowlist, feasibility, the waste lessons) and legacy/studio-v2.
