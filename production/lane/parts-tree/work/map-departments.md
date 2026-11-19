# Departments from five games' credits, mapped to the parts tree

Task (c). Read 19 November 2026. Part ids are from production/lane/parts-tree/SKELETON.txt. Outside-only rule kept: public pages only, no game files, no videos.

Key for the "credited by" column: K = Kingdom Come: Deliverance II, M = Mafia: Definitive Edition, S = Sleeping Dogs, G = GTA V, R = Red Dead Redemption 2. A letter appears only where a reached source shows that department. A game missing from a row means "not seen in what was reachable", not "absent". G and R lists are PARTIAL (see below).

## Sources used

| Game | Source | Date read | Completeness |
|---|---|---|---|
| K | production/research/aaa-reference/CREDITS-MAP.md in this repo (its source S1, the KCD wiki credits copy, read 13 October 2026; reused, not re-read) | 19 Nov 2026 (file), 13 Oct 2026 (web source) | Full roll as transcribed by the fan wiki; counts in that file |
| M | https://2k.com/mafia/game-credits (official; page header says "Mafia II" but the content is the 2020 Definitive Edition roll, with the 2002 original credited to Illusion Softworks) | 19 Nov 2026 | Department headings and one sample role each; treated as the whole list of headings |
| S | https://www.mobygames.com/game/sleeping-dogs-definitive-edition/credits (MobyGames; holds the Definitive Edition blocks and the original game's blocks) | 19 Nov 2026 | Full headings and roles as returned |
| G | https://www.imdb.de/title/tt2103188 pages as returned by search: https://m.imdb.com/title/tt2103188/fullcredits/animation_department (page returned the department headings of the whole credits list plus animation role titles) | 19 Nov 2026 | PARTIAL: headings, animation roles only |
| G | https://gta.wiki/w/Grand_Theft_Auto_Online/Credits (its "Thank You (GTA V)" section: first 100,000 of 486,302 characters read) | 19 Nov 2026 | PARTIAL: Take-Two, Dundee and Rockstar Games thanks only |
| G | https://www.wikiwand.com/en/articles/Development_of_Grand_Theft_Auto_V (a copy of Wikipedia's article) | 19 Nov 2026 | Not credits: team sizes (over 1,000 people, core North team 360), names of music producers, mocap use |
| R | https://m.imdb.com/title/tt6161168/fullcredits/sound_department (returned headings and role titles of the whole list, with some lists cut off) | 19 Nov 2026 | PARTIAL: some lists cut off |

## Unreachable or refused

- English Wikipedia (en.wikipedia.org): the permission request for Development of GTA V, Development of RDR2 and the RDR2 article was not answered in time. Not read there (the GTA V article was read through the Wikiwand copy above).
- IMDb German host full credits for GTA V (https://www.imdb.de/title/tt2103188/fullcredits): fetch denied by the session. Not retried.
- No full credit roll for GTA V or RDR2 was reached. The searches returned no Rockstar-hosted credits page, and MobyGames' RDR2 results were licensing pages, not credits. So G and R are PARTIAL and every G or R mark below rests only on the headings and role titles listed above.
- For Mafia: Definitive Edition, MobyGames and IMDb pages appeared in search but were not fetched; the official 2K page was enough for headings. Per-department headcounts are not reached for M, G or R.
- Earlier refusals (MobyGames 403 for KCD2 and Old Country, IMDb 202 robot check, Fandom pages) are in CREDITS-MAP.md under "Not reached".

## Table

Motion capture: LEDGER has no money for it (CREDITS-MAP gap 1; RULINGS says no hiring). Every capture-linked row is noted.

| Department | Credited by | Output | Part ids | GAP proposal |
|---|---|---|---|---|
| Direction, studio leadership | K M S G R | decisions, sequence, taste | 9.7 (Jafar decides) | none |
| Production, project management, coordination | K M S G R | schedule, order of work, handovers | 9.7, 9.5 | none |
| Open world / world layout, technical level design | K M(Mission Art, Environment Art) S(world art) | the map as placed data, set pieces in place | 4.1, 4.1.1, 4.1.2, 4.2, 4.3 | none |
| Mission and quest design, quest scripting | K M S G(lead mission designer named in Wikipedia copy) | authored jobs, steps that decide acts | 3.5, 3.5.1 to 3.5.5, 3.1.2, 7.4 | none |
| Gameplay and systems design | K M S G(Director of Design in thanks) | rules, verbs, tuning | 1 and children, 2 and children, 9.6, 7.10 | none |
| Metagame, progression, economy design | S | money, rank, unlocks | 2.7, 2.12, 7.7 | none |
| Technical design / scripting tooling | K S(scripting tech lead) | scripts that place and trigger content | 9.4, 9.3 | none |
| Narrative, story writing | K M S G R(Writers heading) | story, acts, endings, character cards | 3.1 and children, 3.2 and children, 3.3 | none |
| Dialogue and street-line writing, extra dialogue | K(English writers, editors) S(Dialogue, Additional Dialogue) | lines, shared lines, crowd lines | 3.6, 3.6.3, 3.6.4, 3.6.5 | none |
| Cinematics, cutscenes, cinematics producer | K M S G(lead cutscene animator, cinematic camera) R(cinematic animation, cinematic camera) | authored scenes | 5.8.2 | none (CREDITS-MAP gap 2 says nobody does it yet; the part exists) |
| Gameplay and dialogue cameras, camera programming | K(dialogue cameras and gestures) S(camera programmer) R(camera programmer) | camera rig by state, follow, chase | 1.1.2, 1.2.2, 5.8.1, 3.6.1 | none |
| Combat design, combat choreography, stunts | K(combat designers, fencers) G(Stunts heading) R(stunts) | blows, reactions, fight feel | 1.3 and children, 5.2.2, 5.5.6 | none |
| Vehicle handling and vehicle physics | S(physics programmers, lead vehicle artist) | car feel, damage, grip | 1.2.1, 1.2.4, 1.2.5, 9.9 | none (no handling credit title seen anywhere) |
| Vehicle art | M S | cars, vans, police cars (fictional) | 4.6 | none |
| AI programming, gameplay AI | S(Gameplay/AI) G(Dundee lead AI/gameplay programmer, thanks) | people deciding, chasing, giving up | 1.5.4, 2.1, 2.5, 2.6, 2.10, 2.11, 4.5 | none |
| Crowd and ambient life | R(Ambient World Animation) | unnamed people living by the clock | 2.1.2, 3.2.4, 5.1.5, 5.2.5 | none |
| Traffic | none titled in any reached list | cars driven by AI, braking for people | 4.5, 1.2.5 | none |
| Programming, engine and gameplay | K M S G R(audio and camera programmers) | the code | 9.3, 9.4, 8.1, 8.2 | none |
| Rendering and platform engineering, performance | M(Render, Platform, Engine) S(Rendering, Platform) | frame rate on target machine | 8.1, 8.3, 5.4.3 | none |
| Tools, pipeline, TechOps, DevOps | K(TechOps) M(Build System Engineering) S(Tools and Build, Build Systems) | scripts, importers, nightly build | 9.1, 9.2, 9.3, 9.5, 9.7 | none |
| Build, release, mastering, platform submissions | K(publisher release managers) M(2K QA and Submissions) S(Mastering Manager, compliance) | packaged build, store submission | 10.1, 10.2, 10.5, 8.5 | none |
| Online services, web | K(Software and Online) S(online programmers, web) G(Online Group, thanks) | server side and web | 8.6 (live talk service only; no multiplayer) | none |
| Animation, gameplay and in-game | K M S G(ingame animator, senior animator) R(Senior Gameplay Animator) | movement clips and blends | 5.2.1, 5.2.2, 5.2.3, 5.2.5, 5.2.6 | none |
| Cinematic animation | K S(Cinematic Animators) G(lead cutscene animator) R(Principal Lead Animator: Cinematic Animation) | animation for authored scenes | 5.8.2, 5.2.3 | none |
| Facial animation, lip sync | K(Facial Animation 4) R(facial art director, principal facial animator) M(Cubic Motion named among outsourcers; role not stated) | mouths, expression, glances | 5.2.4, 5.1.1, 5.6.3 | none |
| Animation programming, character rigging, technical animation | K(technical animators) S(Lead Animation Programmer) G(animation programmer, senior character rigging) R(Technical Director: Animation and Cinematography) | rigs, blending, retargeting | 5.1.2, 5.2.1, 9.2 | none |
| Motion capture, performance capture, capture editing (no money: note) | K M(Performance Capture; 2K Motion Capture) G(mocap used, Wikipedia copy) R(mocap actor, performance capture director, additional motion capture) | raw and cleaned body and face clips | none that names clip sourcing | GAP: "Clip sourcing and cleanup" (library clips from the allowlist, retarget, foot-slide fix; markerless capture only if Jafar rules it), parent 5.2 |
| Stunt and fight performers | K G R | reference for fight and fall motion | 5.2.2 | covered by the GAP above for sourcing |
| Character art | K M S G(Art Department) R(Art Department) | people's bodies, faces, outfits as models | 5.1, 5.1.1, 5.1.2 | none |
| Hair and costume, wardrobe | G(Costume Department heading) K(character artists) | hair, clothes | 5.1.3, 5.1.4, 9.1 | none |
| Face scanning, photogrammetry | K(3D scanners, More.is.More, 3D.sk) | scanned faces and surfaces (LEDGER: MetaHuman presets, no scans, no money) | 5.1.1, 9.2 | none |
| Casting and voice casting | K(Casting) G(Casting Department) S(Voice Talent) | who plays whom, voice chosen | 5.6.1, 3.2.1 | none |
| Environment art, level art, interiors | K M S G(Principal Artist Interiors, thanks) R(structure, general) | buildings, ground, rooms | 5.3, 5.3.1, 4.1, 4.3 | none |
| Props and street furniture | R(prop artist) G(Art Department) | phone boxes, bins, railings, furniture | 4.4, 4.9 | none |
| Terrain and vegetation | R(lead terrain artist) K(Vegetation and Biome Designer) | ground form and planting | 4.1.1, 4.1.4, 5.3 | none |
| Concept art, art direction, look reference | K M S G(Art Directors) R(Art Directors, interior and technical art directors) | the look bible, reference sheets | 5.3 and 5.4 loosely (no part holds the look itself) | GAP: "Art direction and look reference" (Hook sheet, grade targets, reference photos, per-kind floors), parent 5 |
| Lighting | K(Weather and Lighting) M S(Lead Lighting Artist) R(lighting director, lighting technician) | light for day, night, rooms | 5.4.1, 5.4.2, 1.4.2 | none |
| Visual effects | K M S(FX) G(Visual Effects heading) R(Visual Effects heading) | rain, smoke, blood, glass | 5.9, 5.3.3 | none |
| Compositing, post, motion design | R(lead compositor, motion design director) | grade, grain, composite | 5.4.3 | none |
| Technical art, shaders, materials | K M S R(technical art director) | materials, wear, wet, procedural kits | 5.3.2, 5.3.3, 9.2 | none |
| Weather | K(Weather and Lighting Artists) | rain, wetness, overcast, effect on crowd | 4.8, 2.1.4, 5.3.3, 5.5.4 | none |
| UI and UX design, UI art and programming | K M S(Lead UI Artist, UI programmers) R(UI Designer) | screens, notebook, prompts, menus | 6 and children, 6.6, 8.3 | none |
| User research, usability, playtest, analytics | K(GamesLab) S(Playtest and Research, Usability Testing, Playtest Observers) M(2K Global Analytics and Insights) | what players do and where they stall | 9.5, 9.9, 10.3, 7.12 | none |
| Sound design, audio direction | K M S G R(audio designer, director) | the street, doors, cars, fights | 5.5 and children | none |
| Foley | R(foley artist, mixer, recordist) | footsteps and cloth, surface sounds | 5.5.1, 5.5.2 | none |
| Audio programming, mix, middleware | S(Audio Programmers, Ogg Vorbis middleware) R(audio programmer, audio engineer) | mix rules, voice priority | 5.5.7, 8.1 | none |
| Music, composition, score recording | K M S G(Music Department; five music producers in Wikipedia copy) R(Music Department) | score, front-end music | 5.7 | none (LEDGER rules silence commonest; CREDITS-MAP gap 3 says nobody yet) |
| Licensed songs and radio production | S(Music Sourcing and Licensing; Radio Production, DJ scripting) G(Soundtrack Supervisor, thanks) | in-world radio programmes, period songs, rights | 5.7 (silence), 1.6.8 (radio as object) | GAP: "Radio programmes and period songs" (what the radio plays, rights check; free or CC0 only), parent 5.7 |
| Dialogue recording, voice direction, dialogue editing | K M S G(Cast) R(dialogue editor; additional performance direction) | spoken lines | 5.6.1, 5.6.2, 5.6.3 | none (LEDGER voices are synthetic) |
| Localisation and localisation QA | K M S | other-language text and speech | 8.9 (English only) | none |
| QA, compatibility, compliance, certification | K M S G(VP of QA, thanks) | faults found, builds cleared | 9.5, 10.5, 8.2 | none |
| Physics, ragdoll, destruction | S(Physics Programmers) | bodies and props reacting, glass and doors breaking | 1.2.4 (damage), 1.3.7 (fall rule), 5.2.2 (falls), 5.9 (glass), 5.5.2 (forced door) | GAP: "Physics and ragdoll" (collisions, bodies, props, cars together, one place for the settings), parent 8 |
| Accessibility | none titled in any reached list | text, hearing, motor, cognition options | 8.4, 6.1.2 | none |
| Photo mode | none titled in any reached list | a free camera for stills | none | GAP (scope question, probably no): "Photo mode", parent 6.4 |
| Research, history and culture, dialect advisors, location scouting | K(History Advisors, dialect and culture consultants) G(Location Management heading) | period facts, accents, places photographed | 4.9, 2.1.2, 5.6.1, 4.1.3 | none |
| Marketing, trailers, key art, store assets, PR | K M S(Marketing, Brand, Senior Marketing Artist) | trailer, capsule art, text | 10.2 (store page only) | GAP: "Trailer, key art and store capsule", parent 10 |
| Community and player support | K(Community Manager, Customer Service) M(2K Customer Service) S(Community Manager) | answers, forum, patch notes | 10.6 (patches only) | GAP: "Player support and community", parent 10.6 |
| Age rating, legal, finance, HR, IT (company support) | K M(Take-Two Legal, Finance, HR, IT) S(Rating Advisor, Legal, Finance) G(Take-Two legal, thanks) | rating forms, name clearance, licences, company admin | 10.2 (age rating, disclosure), 10.4 (notices) | GAP: "Legal clearances and company admin" (name search, licence checks, tax and company set-up), parent 10 |
| Sales, partnerships, regional publishing | K M S | deals, distribution | none | none (not an output the game needs; CREDITS-MAP gap 6 and 7 cover the choice) |
| Interns, additional help, outsourced co-development | K M S | extra hands | none (an arrangement, not an output) | none |
| Thanks lists (babies, forums, special thanks) | K M S | not jobs | 10.4 | none |

## Gaps

1. Clip sourcing and cleanup, parent 5.2. Capture has no part today; library clips, retargeting and the foot-slide fix are the output LEDGER can make. No mocap money.
2. Art direction and look reference, parent 5. The look (Hook sheet, grade targets, floors) has no part of its own.
3. Radio programmes and period songs, parent 5.7. Music exists as "silence commonest"; radio content and rights do not.
4. Physics and ragdoll, parent 8. Bodies, props, cars and doors reacting are spread across five parts with no owner.
5. Trailer, key art and store capsule, parent 10. Part 10.2 holds the store page and rating, not the pictures.
6. Player support and community, parent 10.6.
7. Legal clearances and company admin, parent 10 (name search, licences, tax).
8. Photo mode, parent 6.4. Scope question for Jafar; no game credited it in the lists reached, so probably not wanted.

Not gaps, checked: traffic (4.5), weather (4.8), accessibility (8.4), localisation (8.9), analytics and playtest (9.5, 9.9, 10.3), online services (8.6). No reached list names traffic, accessibility, destruction or photo mode as a credited department, so no game's evidence is cited for them.
