# Study 8: Sound (28 October 2026)

How a street is made to sound alive, from the files of Mafia: The Old Country (Unreal 5.4, Wwise) and Kingdom Come: Deliverance II (CryEngine, FMOD). Metadata only (event and table exports, sample names from bank headers, the package index); no sound was extracted or heard. Raw counts on F:/LedgerTools/aaa-study/mafia/study-8/ and F:/LedgerTools/aaa-study/kcd2/study-8/. Read 28 October 2026. Tags: **M** measured, **R** read in a file or interview, **I** inferred, **N** a name only.

**The short answer.** Both games build a street from three parts: a few quiet looping beds per zone; short sounds spawned around the listener, capped by zone and hour; and placed sources (windows, doors, bells, water), each heard within a set distance. Mafia's quiet street spawns at most 3 distant conversations and 3 small activity sounds by day, none at night. No loudness target is in either game's readable data; Mafia mixed to its quietest lead voice. LEDGER's built Quay Street sound (cloud unit 10) has the beds; it lacks the spawned layer, the echo zones and the hours between day and night.

## The numbers

| | Mafia | Kingdom Come II | LEDGER now |
|---|---|---|---|
| Effect and music files | 25,600 (M) | 6,243 in the two main banks; music 202 cutscene files, 278 sequences (M) | in game: 1 traffic bed, 16 steps; built, not in game: 97 (unit 10) |
| Sound events | 15,406, 12,558 of them dialogue (M) | 2,164 triggers, plus 11,097 for cutscenes (M) | |
| Ambience zones | 19 kinds painted on the land, 5 of them town (R) | Kuttenberg level: 956 areas, 365 with a bed, 583 setting the echo (M) | one bed, one point |
| Time of day | dawn 05:00, morning 06:30, day 08:00, evening 18:00, night 21:00 (R) | a daytime parameter (N); beds named by recording hour (M) | day, night (built) |
| Spawned voices at once (dawn/morning/day/evening/night) | quiet street 0/1/3/2/0; crowded 4/12/18/10/6; market 4/14/25/12/6 (R) | timed calls every 22 to 97 s (R) | a line every 18 to 40 s, within 16 m |
| Weather | no rain system found; a wind bed above intensity 2.9 (N, R) | rain, wind, lightning; rain, wind, cloud, puddle parameters (R) | rain in 3 places, one strength (built) |
| Footstep surfaces | 53 physical, 37 step sounds; 5 shod kinds share one set, barefoot apart (R, M) | 15; shoes or barefoot (R) | Tom's trainers on paving; built: 5 |
| Takes per set | walk 8 (cobbles) to 30 (rough road); 4 gaits; puddles 10 or 20 plus a splash layer of 14 or 26; heard to 30 m (M, R) | stone 13, wood 15, mud 14, water 52 (M, I); others' steps to 15 to 20 m (R) | 8 walk, 8 run (paving); built: 8 a surface |
| Echo | 18 reverb sends on 9 impulse responses; the 3 outdoor ones share one (R) | 128 settings on 34 reverbs: 20 indoor, 12 outdoor (M) | none |
| Zone edges | Palermo level: 43 rooms, 75 doorways, 7 shut at start (M) | beds fade over a median 10 m (p75 15); echo switches over 1 m (M) | |
| Music | 818 score files in 15 chapter folders; restarts after 25 s calm (M, R) | 287 states by priority; silence the most-used confirmed playlist, 31 of 299 (M) | none (P18 open) |
| Mix and loudness | 396 mix-state events, 314 per story beat; 3 mastering presets, settings unread (M, R) | 3 volume groups; 10 mix setups, one for dialogue (R) | day bed 13.5 LU under −23 LUFS (EBU R128, brief) |

## Ambience: layers, hour and weather

- **Mafia (R, M).** Every town zone plays the same three loops (a town night bed, a calm background, distant conversation). A spawner (76 rows) places short sounds 20 to 70 m off (quiet street 50 to 70), capped by zone and hour: conversations, street activity (32 kinds), birds (about 17 species; 2 at once in a street by day, none at night); water lapping, up to 14 at once within 25 m. Placed emitters: activity through windows (40 m), talk through windows (20 m), cooking and work (30 to 60 m), groups talking (35 m), church bells (150 m), gulls (57 call files, 150 m), a harbour's ropes and creaks (20 to 50 m). Placed ambience is heard to a median 30 m (p25 15, p75 60). A town street carries about 3 beds, 3 spawned kinds and a few emitters (I). Rain appears only in mission-named sounds (N, I).
- **Kingdom Come II (M, R).** Ambience areas are drawn shapes with a bed and a fade; areas without a bed set the echo. The city has 323 areas, 88 with a bed: a town-wide bed, street (6 shapes), market (3), square (2). Along Tarmark's 49 stations the town bed covers all, a street bed 3, and another bed lies within fade at 10. Global wind and rain, bells (13), point sources (22 in the city: streams, troughs, mills) and timed calls (a butcher every 48 to 64 s) complete it. Beds are long recordings named by hour; 60 one-shots are cut from them to scatter. Rain has an intensity, with drops on fabric, plate and wood (13, 11, 8 takes).

## Footsteps

- **Mafia (M).** One walk-run event switches surface, shoe and a clothing rustle (4 kinds). Cobbles, concrete and stone share one gritty set: 8 walk, 10 run, 10 sprint, 10 sneak. Smooth concrete has 27 walk takes, wood 20. 1,775 step files in all.
- **Kingdom Come II (R).** Each surface has walk-run, quiet and jump, for the player and others, plus a set marked d (meaning not found). Wet is a surface (mud-water, water), not a state.

## Spaces: echo and muffling

- **Mafia (R, M).** Convolution reverb by space (rooms small to big, halls, barn, cave, church), one exterior response for all outdoors, one shared game-defined send for all world sounds (interview). Wwise rooms and doorways; 4 reverb volumes at once, 3 room sends a sound. The listener sits halfway from camera to player; a sector value marks outdoor 0, forest 0.2, urban 0.3, indoor 1.
- **Kingdom Come II (M).** Its outdoor reverbs are the half-open places (arcade, gate small to big, pergola, yard); indoor ones by size; an indoor group mutes outdoor beds (I).

## Objects

- **Doors (Mafia, M):** six kinds (wood-and-glass, solid, rickety, gate, iron gate, fortified), each open, close-creak and close-hit, built from layers (creak, hit, detail; 3 to 5 takes each) plus a shared grit layer (7); heard to 30 m; knocks 6 takes, 10 m. Kingdom Come II: a wood or metal switch, 115 door samples (M).
- **Bells:** church bells in both; no shop bell in either. **Phone boxes:** none (period). **Cars:** not studied (no cars unless P9).

## Music and mix

- **Mafia (M, R):** one music event holds the score: per chapter, explore, stealth, combat and chase loops, intros, outros, stingers; states from the alert level and story; after 25 s calm, gameplay music restarts. Music in the world (gramophones, street musicians, bands) is heard 15 to 65 m off. Dialogue is the centre of the mix, the range wide, little compression; silence is used on purpose (interview). Mix states cover story beats, cinematics (with or without music), reading an item, and mutes with 2 or 3 s fades; home cinema, TV and night presets.
- **Kingdom Come II (M):** each music state overrides or blends by priority: time of day 11 to 13, weather 22 to 23, crime and trespass 31 to 37, combat 150, cutscene 502; dialogue has its own playlist; 14 states hold 2 to 15 s after they end; place keywords pick the music.

## For LEDGER

For phase 2's Quay Street and proof P13 (his ear decides), under the 5 October weather ruling and D26 (CC0 only). Unit 10 (production/cloud-week/sound) still waits for his ear (q-sound-listening).

1. **Adopt the three-part street** (P13; FEASIBILITY row 28, "near-silent"): unit 10's beds, spawned one-shots capped by hour, placed sources with set distances.
2. **Adopt four states of the hour,** crossfaded: dawn, day, evening, night, mixed from unit 10's day and night loops (I).
3. **Adapt weather** (5 October ruling): one rain parameter, dry through drizzle to rain, fades the rain layers, road hiss and gulls; rain halves spawned voices and activity (I).
4. **Adopt for footsteps** (the twenty basics, 18): 8 walk and 8 run per surface (unit 10 has 8 a surface, one gait); wet as a splash layer over the dry step; two shoe sets, soft (Tom's trainers) and hard; others' steps heard to 20 m.
5. **Adopt echo zones** with Unreal's own audio volumes, checked against 5.8 before building: street, shop doorways (Kingdom Come II's gate and arcade kinds), a small shop room, Mickey's office; the echo changes across about 1 m at a doorway, beds fade over about 10 m; an open door lets the street in, a shut one muffles it. Listener halfway between camera and Tom.
6. **Adopt layered doors** (phase 2's shopfronts): creak, hit and latch, 3 to 5 takes each, plus a shared grit layer; heard to 30 m, knocks to 10 m.
7. **Adapt the mix** (P13; phase 1's talk): the quietest lead voice is the reference; a talk state lowers the beds (by how much is in neither game's readable data: by ear); a full, TV or night range choice when the settings are next touched.
8. **Music, only if P18 rules it in:** priority states, silence the commonest; a 2 to 15 s hold; never combat music (12 October).
9. **Ignore:** Wwise or FMOD (outside the allowlist; any licence is his call), six shoe kinds, per-story mix states, vehicles (P9), animals beyond gulls, a cat and a far dog.

**Quay Street ambience plan (P13).** Bed and one-shot levels are unit 10's (BRIEF.md section 5: EBU R128, −23 LUFS programme, −1 dBTP), kept; counts and distances come from this study.

| Layer | Day / night / rain | Heard within | Unit 10 | From |
|---|---|---|---|---|
| Distant traffic (bed) | −40 / −45 / −42 LUFS | everywhere | has | brief |
| Harbour water (bed) | −41 / −43 / −43 | everywhere | has | brief |
| Wind (bed, gusts by parameter) | −46 / −47 / −43 | everywhere | has | Mafia |
| Gulls (bed plus 0 to 2 spawned calls) | −48 / −56 / −54 | 150 m | loop only | Mafia |
| Distant voices, no words (spawned) | at most 3 / 0 / 1; dawn 0, evening 2 | 15 to 40 m off (I; Mafia's quiet street 50 to 70) | lacks | Mafia |
| Street activity: crate, bin lid, pan, a door indoors, a cat, a far dog (spawned; ≥30 takes in ≥8 kinds, I) | at most 3 / 0 / 1 | 15 to 40 m off (I) | lacks | Mafia |
| Water lapping at the quay (spawned) | up to 14 by day, 6 at night | 25 m | in the bed | Mafia |
| Voices through a window (point) | −50 / −53 / −55 | 20 m | has, as a loop | Mafia |
| Radio through a window (point) | −52 / −54 / −54 | 20 to 30 m (I) | has, as a loop | brief |
| Work or cooking through a window (point) | by ear, near the window voices (I) | 30 to 40 m | lacks | Mafia |
| Rain on pavement, awning, gutter (one parameter) | −37, −42, −47 | near | has, one strength | brief, Kingdom Come II |
| Shop door and bell, house door, knock | −23 to −29 LUFS-M | 30 m; knock 10 m | has, no knock | Mafia |
| Phone box | −23 to −31 LUFS-M | 30 m (I) | stand-in ring | brief |
| Others' footsteps | −27 LUFS-M | 20 m | lacks | Kingdom Come II |

Bed mixes stay −36.5 (day), −39.5 (night), −33.5 (rain) LUFS. Spawned sounds are made at the brief's one-shot levels and placed by distance, so they land under the bed (I). Checks: spawned counts per hour, a minimum gap before a take repeats, each source's distance, the bed mixes within 1.5 LU.

## Coverage map

To tick in REFERENCE.md: sound and ambience (both games, data side; bank internals not read); doors' sound side under doors and world interaction.

## Open blind spots

- **Inside the banks and as played:** bus volumes, falloff curves, reverb and mastering settings, random and sequence rules, music transitions (binaries not parsed); no recordings (25 October). So the relative loudness of ambience, voices, effects and music is unmeasured in both.
- Kingdom Come II: how beds change by daytime and rain inside each event; the d footstep set; the puddle parameter's use.
- Mafia: emitters placed beyond the Palermo opera level; systemic rain (none found by name).

## Sources (read 28 October 2026)

- **Mafia:** FModel property exports of Nero/Audio (zones, spawners, settings, surfaces, listener, game states, music data), the reverb sends and twelve event folders (1,060 events); the package and pak name index; DefaultGame.ini (Wwise settings); Palermo level actors exported 25 October.
- **Kingdom Come II:** Libs/GameAudio; Libs/Tables/music; Scripts/Entities/Sound; footstep material effects; Kuttenberg's level objects and layers; sample names in the two main FMOD banks' headers (read in memory); the Sounds and Music pak indexes.
- **Public:** Jennifer Walden, interview on Mafia: The Old Country's audio, A Sound Effect, 19 November 2025 (page modified 21 October 2026), https://www.asoundeffect.com/mafia-the-old-country-game-audio/; seen only through a fetch tool's summary of the full page, not read in full.
- **LEDGER:** production/specs/street-sounds.json; production/cloud-week/sound/BRIEF.md, NOTES.md; PLAN.md, pre-production/3-PROOFS.md (P13); RULINGS.md.

## Review

A fresh reviewer (28 October) re-measured 52 numbers from the exports and files: 44 matched. Fixed here: pak counts made unique (25,600 files), mix states counted as events, bird species, street-activity kinds, Kingdom Come II's fade distances, the loudness and interview wording, tags on rain and material sets, unit 10's footsteps, the window-work level, Wwise's status; cut to length. Cost, from the clock: 12:50 to 13:35 (exports, measures, synthesis, review, fixes).
