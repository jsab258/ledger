# Asset coverage audit: what a finished game of this shape is made of, and what we hold

STATUS: SPEC (research delivery). Branch `research/asset-coverage`, from commit
`766a210`. Written 2026-09-18 by the research lane.

NOTHING IN THIS FILE IS AN INSTRUCTION. It proposes no tile, files no queue
item, edits no inventory and adds nothing to the register. Every recommendation
is a recommendation and the decisions are Jafar's.

The companion one-page version for Jafar is `SUMMARY.md` beside this file.

## 0. The host check, first, because the brief asked for it

**All five newly allowlisted hosts are still refused at the gateway. None
opened.** Each was tested directly this session with curl through the proxy,
the proxy's own failure log agrees on all five, and one was retried through the
harness fetch as a second channel.

| Host | curl through the proxy | harness WebFetch |
|---|---|---|
| dev.epicgames.com | CONNECT tunnel failed, 403 | not tried (curl settled it) |
| docs.blender.org | CONNECT tunnel failed, 403 | `EGRESS_BLOCKED` |
| huggingface.co | CONNECT tunnel failed, 403 | not tried |
| arxiv.org | CONNECT tunnel failed, 403 | not tried |
| datashare.ed.ac.uk | CONNECT tunnel failed, 403 | not tried |

The proxy's own status endpoint (`$HTTPS_PROXY/__agentproxy/status`) lists each
of the five under `recentRelayFailures` with
`kind: connect_rejected, detail: gateway answered 403 to CONNECT (policy denial
or upstream failure)`, timestamped 2026-09-18T21:10:39 to 21:10:40Z. That is the
same failure mode the previous lane recorded. `en.wikipedia.org` was fetched as
a control and answered `EGRESS_BLOCKED` too.

WHAT THIS COSTS THIS DELIVERY, named at the two places it bites:

1. **NVIDIA's Audio2Face-3D model card cannot be read** (`huggingface.co`
   blocked), and section 7.3 turns on a licence distinction that the model card
   is the primary source for. The finding there is flagged as unverified, not
   asserted.
2. **The Audio2Face-3D paper (arXiv 2508.16401) cannot be read**, so nothing
   here quotes its method or its numbers.

WebSearch works. Every external citation below is therefore the search
channel's SUMMARY of a named page, exactly as in the prior research
deliveries, and is a direction rather than a measurement. Every internal claim
is the opposite: measured in this checkout, this session, with the command that
measured it recoverable from the evidence column.

## 1. What this audit is, and the denominators

The brief: the content equivalent of the systems coverage audit. Systems were
enumerated by working backwards from five finished games because the inventory
had the studio's blind spots built into it. Nobody has done that for assets.

**The enumeration: 84 asset categories in eight groups.** Where the list comes
from is section 2. Each is typed `exists`, `partial` or `absent` against this
checkout, using the same three words `production/systems-inventory.json` uses,
so the two documents can be read side by side.

WHAT THE 84 IS A COUNT OF: distinct kinds of authored or fetched material that
a finished game of LEDGER's shape must physically contain, at the grain where
one kind is made by one pipeline and one skill. It is not a bill of materials
and it is not a census of any of the five games. Splitting differently would
give a different number, and section 2.3 names the four places I split by
judgement.

**The totals**, recounted from the tables in section 3 by a script rather than
tallied by hand, because a total typed from memory is the thing this project
keeps catching.

| Typed | Count | Share |
|---|---|---|
| exists | 11 | 13% |
| partial | 47 | 56% |
| absent | 26 | 31% |
| **Total** | **84** | |

THESE ARE THE SECOND NUMBERS. The first pass typed 31 absent and was wrong by
five, all of them in sound, because it counted files instead of reading the
code that makes the sound. The correction is kept in the open at the head of
group D rather than silently fixed, because the failure mode (a measurement
that is true carrying a conclusion that is false) is the one this project
writes casebooks about.

**And the call, which is the brief's prediction confirmed:** of the 26 absent,
**22 IN, 0 OUT, 4 ASK**. Nothing is recommended OUT. The systems audit found a
52 percent OUT rate among absent systems; here it is zero, because a game
cannot omit its own materials. The four ASKs are not doubts about whether the
category is needed. They are questions about which of two routes to take, and
every one of them is Jafar's kind of question rather than the studio's.

So, exactly as the brief predicted, the in-or-out call carries no information
and **the interesting output is section 5: what each absent category costs.**

## 2. Where the category list comes from

### 2.1 The five games, the same five

| Game | Branch of the systems audit | What it contributes to the enumeration |
|---|---|---|
| Kingdom Come Deliverance 2 | `research/coverage-audit-kcd2` | layered garments as separate assets; wear and dirt as states of a garment |
| Hitman (World of Assassination) | `research/coverage-audit-hitman` | outfits as identity; crowd bodies at a second fidelity tier |
| Red Dead Redemption 2 | `research/coverage-audit-rdr2` | the animation and voice corpus as the dominant content cost |
| Disco Elysium | `research/coverage-audit-disco-elysium` | portraits, inventory icons and painted backgrounds as first-class categories |
| Shadows of Doubt | `research/coverage-audit-shadows-of-doubt` | interiors, furniture and per-room palettes as generated content |

Five specific contributions, dated and sourced:

- **KCD2 ships clothing as layered items, 16 slots, up to four garments stacked
  on the chest, and clothing that gets progressively more worn, dirty or
  bloody through use.** That is a garment category and a garment-state
  category, and they are separate lines here for that reason.
  ([inara.cz KCD2 armours](https://inara.cz/kingdom-come-2/armors/);
  [KCD wiki](https://kingdom-come-deliverance.fandom.com/wiki/Warhorse_armour/KCD2))
- **Warhorse published a 300-page art book of KCD2 concept work covering 2019
  to release**, announced by the studio itself. A concept corpus of that size
  for one game is why concept art is enumerated per subject here rather than as
  one line. The announcement's own date is not in the search summary and I have
  not read the post, so no date is claimed for it.
  ([Warhorse Studios announcement](https://x.com/WarhorseStudios/status/1864613767662764501?lang=en))
- **Disco Elysium contains 105 character portrait files and 193 squares of 4K
  environment texture, and the team spent about a year deciding the level of
  detail for inventory icons.** Icons are a category that took a year at a
  studio that had no 3D character art at all.
  ([MCV/Develop, The Art of Disco Elysium](https://mcvuk.com/business-news/we-knew-immediately-that-we-needed-to-make-a-game-with-a-striking-and-unique-look-to-accompany-the-writing-a-look-that-would-balance-the-mundane-with-the-unfamiliar-and-strange-the-art/))
- **RDR2 ran about 2,200 days of motion capture and recording, 1,200 actors,
  700 of them voicing 500,000 lines, and about ten times GTA V's animation
  volume.** Animation and voice are enumerated here as several categories
  each, because at this scale they are several pipelines.
  ([Development of Red Dead Redemption 2](https://en.wikipedia.org/wiki/Development_of_Red_Dead_Redemption_2);
  [ScreenRant, 25 things](https://screenrant.com/red-dead-redemption-2-making-of-details/))
- **Shadows of Doubt builds interiors from hand-made floorplan grids
  subdivided procedurally into rooms, and colours furniture from a five-colour
  palette generated per room.** Interior shells, interior fittings and interior
  clutter are three lines here because that game treats them as three problems.
  ([ColePowered DevBlog 13](https://colepowered.com/shadows-of-doubt-devblog-13-creating-procedural-interiors/);
  [ColePowered DevBlog 21](https://colepowered.com/shadows-of-doubt-devblog-21-how-voxels-saved-the-project/))

### 2.2 The two sources I argue for adding

The brief invites others. I add two, and neither is a game.

**The art department's own division of labour.** Working backwards from five
games finds what those games contain; it does not find what a game contains
that no reviewer or wiki ever describes. The discipline literature does:
concept art, character art, environment art, props, animation, VFX, UI/UX art
and technical art are the standing divisions, and each names material a player
never thinks of as an asset.
([Pixune, game art pipeline](https://pixune.com/blog/game-art-pipeline/);
[Beyond Extent, environment art specialisations](https://www.beyondextent.com/articles/environment-art-specialisations);
[8bitplay, game art roles](https://8bitplay.com/blog/game-art-jobs-and-roles-explained-a-recruiter-guide/))
Three categories here exist only because of this source: technical art and the
material library (A22), lighting keys and the colour script (G8), and UI sound
(D8).

**The sound department's division of labour**, for the same reason and more
sharply. Game audio is conventionally four pillars, sound effects and foley,
music and interactive score, dialogue and voice, and spatial sound, with
ambience, room tone, foley, one-shots, loops, UI and notification sound as
named sub-kinds.
([A Sound Effect, game audio explained](https://www.asoundeffect.com/gameaudioexplained/);
[Side, game sound design](https://side.inc/services/audio-production/sound-design);
[Bluezone, guide to game sound effects](https://www.bluezone-corporation.com/blog/the-ultimate-guide-to-video-game-sound-effects-for-indie-developers))
Nine audio categories here come from that division, and they are the reason
group D is nine lines rather than one.

This matters more than it looks. **D26 already names the sound contents in
Jafar's own words:** footsteps by surface, doors, cloth, breath, rain, room
tone, the harbour bed. The enumeration did not discover the sound gap. It
discovered that the gap is nine categories wide rather than one, and that seven
of the nine have no recorded file of any kind behind them: only the two voice
categories do.

### 2.3 Where I split by judgement, named so the count can be argued with

1. **Concept art is one line per subject** (environment, character, costume,
   prop, vehicle, interior, graphic, colour key), not one line. The brief's own
   phrasing, "concept art for each of those", asks for this, and the two known
   failures it names are both character-side, which a single line would hide.
2. **Animation is six lines** (locomotion, interaction, conversation, body
   language, reaction, vehicle), because Mixamo supplies some of those and
   supplies none of the others, and one line would average that away.
3. **Audio is nine lines**, per 2.2.
4. **Interiors are three lines** (shell, fittings, clutter), per Shadows of
   Doubt's own three problems.

Collapse all four and the enumeration is about 65 categories. The absent column
does not change; only its granularity does.

## 3. The mapping

Typed against this checkout at `766a210` on 2026-09-18. `exists` means the
material is here and something places it; `partial` means part of the category
is here, or the model is here and the material is not; `absent` means nothing
measured, with the search that found nothing named.

Every count in the evidence column was measured this session. Where a count
came from a file rather than from a walk of the disk, the file is named.

Column `call` is IN, OUT or ASK and applies to the absent rows only; a row that
already exists needs no call. The argument for every absent row is section 5.

### Group A. The world shell (24 categories)

| id | category | typed | evidence | call |
|---|---|---|---|---|
| A1 | building carcass and massing | partial | `production/specs/vignette-pieces.json` C1_terrace_carcass 16 pieces; 107 fbx across four Kenney city kits (`ledger/Assets/Props/city-kit-*`, CC0, `Props/THIRD-PARTY.md`); `Game/WorldBuilder.cs` | |
| A2 | facade detail: sills, lintels, cornices, consoles | partial | same file, C13_sills_lintels 72, C15_fascia_cornice_console 17; two in-house glb (`fascia_cornice_01.glb`, `fascia_console_01.glb`) authored by `production/art/fascia-01/author/make_fascia_mouldings.py` | |
| A3 | roofs, chimneys, aerials, gutters, downpipes | partial | D2_chimney_stack 5, D3_chimney_pots 5, D4_tv_aerial 24, D5_downpipe 27, D6_gutter_run 2, D7_parapet_coping 4; `Game/WorldBuilder.cs:1179` makes a roof from a box on `AssetLibrary.Roof` | |
| A4 | windows and glazing | partial | D8_upper_windows 36, C7_shop_glazing 12; `window.jpg/_n/_r` in `StreamingAssets/CityPack/textures`; `Core/Occupancy.cs` lit windows; `window_practicals` block in the pieces file | |
| A5 | doors | partial | C8_door_shop 18, C9_door_side 30. No door opens into a place, because A14 is absent | |
| A6 | shopfronts and fascias | partial | C5_shopfront_assembly 36, C6_fascia_lettering 4; `production/art/fascia-01/`; four `fascia_*.png` in `StreamingAssets/Decals/generated` | |
| A7 | ground surfaces: road, pavement, kerbs, gullies | exists | A0_ground_planes 9, B1_kerbstone_run 84, B2_dropped_kerb 5, B3_gully_recess 4, A7_gully_grate 1, A8_manhole 2; asphalt, sidewalk and kerb surfaces in CityPack | |
| A8 | street furniture | exists | E1 lighting column 20, E3 telephone kiosk 11, E4 pillar box 4, E5 bollards 2, E6 public bins 2, E8 guard railing 25, E11 cones 3, E13 dustbin 4; bollards, benches and bins among the 39 glb in `ledger/Assets/Props/base-mesh` (37 CC0 from The Base Mesh) | |
| A9 | signage, lettering and notices | partial | 45 generated png in `StreamingAssets/Decals/generated`, counted by prefix: 15 `sign_`, 11 `notice_`, 8 `poster_`, 4 `fascia_`, 3 `interior_`, 2 `wall_`, 2 probe; `Game/WorldText.cs` and `Game/Billboard.cs`; the inventory records 153 pieces of world text placed and depth tested | |
| A10 | vegetation | absent | Nothing measured. The bill of materials says in terms "No tree is on this list", and lists street trees among the American tells it refuses. The only planting object is the Kenney suburban `planter` placed by `Game/StreetDressing.cs:255`. A word-boundary grep for foliage, vegetation, shrub and hedge over 192 scripts returns 0; the 22 hits for "tree" are all `blend tree` | IN |
| A11 | water: harbour, tidal edge, puddles | absent | Nothing measured. No water surface, renderer or asset exists. `Game/WorldBuilder.cs:4225` defines a water LINE at the ground slab's south edge and forbids building across it, and `Game/GullHost.cs:27` says "where the map implies water". Two of the eight vignette decals (`gutter_water.png`, `puddle_mask.png`) are the whole of the wet-ground material. `game-design/research/water.md` is research from 2026-08-25 and names itself as such | IN |
| A12 | sky and weather visuals | partial | four Poly Haven CC0 HDRI in `ledger/Assets/Resources/Sky/polyhaven` plus two png previews; `LedgerSky.shader`; D40 rules the sky a photograph. The inventory records that the last landed Unreal probe run wrote a street with no sky | |
| A13 | terrain, landform and coastline | absent | Nothing measured. One street exists. The seven district plans on `origin/art/atlas-01` (`previews/district-*-plan.svg`) are drawings, not terrain | IN |
| A14 | interiors: rooms you can enter | absent | Inventory tile "interiors you can enter" is typed absent with the note "no room a player walks into exists in this checkout". C11_lit_interior_card is 3 cards behind glass. D14 rules every interior a designed layout | IN |
| A15 | interior fittings and furniture | absent | Nothing measured. `production/art/concept-fairview-2026-09-10/fairview-furniture-2026-09-10.json` is a spec; `production/art/atlas-02/research/household-contents-and-upstairs.md` is written research. No furniture geometry is held except the outdoor Kenney bench and planter | IN |
| A16 | interior clutter and set dressing | absent | Nothing measured, same denominator as A15. Three `interior_*.png` cards (`interior_bar_back`, `interior_shop_shelves`, `interior_stair_landing`) are pictures of clutter, not clutter | IN |
| A17 | decals, grime, wear and stains | exists | 45 generated png plus 16 ambientCG CC0 sets under `StreamingAssets/Decals/ambientcg`; G1 leak stains 3, G2 asphalt damage 2, G4 moss 2, G5 stickers 1, G6 fly posters 3; `Game/DecalLayer.cs` | |
| A18 | litter and loose debris | partial | G8_litter 34 and G9_chewing_gum 60 pieces in the vignette. Both are placed primitives and decals rather than modelled rubbish | |
| A19 | vehicles that move | partial | `Core/Traffic.cs`, `Game/TrafficHost.cs`: 28 vehicles of seven kinds, built from primitives with a kit-mesh path at `TrafficHost.cs:569`. 50 Kenney car-kit fbx and 34 OGA vehicle fbx held. Canon forbids real car models and the held kits are stylised | |
| A20 | parked vehicles as dressing | absent | Inventory tile typed absent, named by Jafar's ruling of 2026-09-10, with his own note: "an empty kerb reads as a film set, and period cars parked badly are the cheapest density in the project" | IN |
| A21 | boats, cranes and harbour plant | partial | `Game/WorldBuilder.cs:4362` builds a skyline of cranes, gasholders, stacks and tanks from primitives, and says at `:4387` that "No kit on disk contains a crane, a gasholder, a" one. No boat exists; the only hit is a gate named "the boat repair yard" in `Game/AccessSetup.cs:81` | |
| A22 | material and surface library | exists | 17 surfaces at three maps each, 51 jpg in `StreamingAssets/CityPack/textures`, all ambientCG CC0 with per-file provenance in `CityPack/ATTRIBUTION.json` | |
| A23 | lighting fixtures and practicals | partial | E1 column 20 and E2 sodium lantern head 4; `lantern` and `window_practicals` colour and intensity blocks in the pieces file; 4 emissive pieces of 610. The inventory's own tile "street lighting at night" is absent: the street has never been rendered at night in a landed run | |
| A24 | particles and VFX | partial | one `ParticleSystem` in the whole codebase, `Game/WorldBuilder.cs:2611`, capped at 6 particles; `LedgerSmoke.shader`; rain in `Game/Weather.cs` | |

### Group B. People (15 categories)

| id | category | typed | evidence | call |
|---|---|---|---|---|
| B1 | body meshes | partial | 18 Mixamo fbx in `ledger/Assets/Characters`. `Game/RealBody.cs` instantiates ONE, on the player only, and says why: "A Mixamo body is a skinned mesh of several thousand triangles; `Mannequin` is thirteen boxes." The crowd is `Game/Mannequin.cs`, ten boxes and a sphere, 67 of them | |
| B2 | faces and heads | partial | the stock Mixamo head, kept with the artist's own texture (`RealBody.cs:802`). No authored face, no face variation beyond a skin tint | |
| B3 | facial rig, blendshapes and lip sync | absent | Nothing measured, and this is the sharpest zero in the audit. Over 192 scripts under `ledger/Assets/Scripts`: `viseme` 0, `lipsync` 0, `lip-sync` 0, `facial` 0, `blink` 2 (both false friends, a fading speech bubble and people blinking in and out of a population). D2 approved the direction on 2026-08-31 and named the driver | IN |
| B4 | hair and headwear | partial | the stock mesh's own hair on the player; on the crowd, `Game/Mannequin.cs:241` builds one box whose height comes from `Shape.Headwear`, plus a peak above 0.72 that reads as a cap | |
| B5 | skin, physique and age variation | partial | `Core/Physique.cs` and `Core/BodyParts.cs`; 92 rigs at heights 1.58 to 1.91 per the inventory. `RealBody.cs:181` names the goal: "the town stops being sixty people wearing one face" | |
| B6 | garments as geometry | absent | Nothing measured. `Core/Wardrobe.cs` is a colour model: eight authored hue bands applied as an albedo tint to whatever the mesh already wears. The prior lane established that nothing in the toolchain touches a skinned mesh and the Unreal importer imports static meshes only (`research/clothing-pipeline`) | IN |
| B7 | garment wear states: dirt, blood, tears | partial | `Core/Traces.cs` models blood on a person with noticing, ageing and washing, and `Wardrobe.Wash` darkens the colour. It is a number and a tint, not a texture or a mesh state | |
| B8 | carried items and accessories | absent | Nothing measured. `Core/Arsenal.cs` models four rungs of concealment and `Characters/B/carry_bag__Walking With Shopping Bag` is an animation for carrying, with nothing to carry. No bag, hat, glasses, umbrella or watch geometry exists | IN |
| B9 | locomotion animation | exists | 24 fbx in `ledger/Assets/Characters/B`: walk, female walk, start walking, jog, back away, turns left and right, stairs up, carrying. Driven by the blend tree in `Game/CharacterRig.cs`, with `Game/FootIk.cs` solving feet | |
| B10 | interaction and prop-handling animation | partial | 12 fbx in `Characters/D`: lift, rummage, point, pat pockets, talk on phone, shake hands, wave, yell, laugh, think, sit, sit and talk. Three more sit rejected (`.fbx.rejected`), two of them drinking, which D17 and D18 forbid | |
| B11 | conversation and gesture animation, and staging | partial | the talk, sit-talk, greet, wave and head-shake clips exist. The inventory's tile "dialogue staging" is absent, and states the risk plainly: an unstaged conversation is the clearest slop tell in a game claiming real spoken dialogue | |
| B12 | body language as a moat surface | absent | Nothing measured, and the ruling that ordered it is not in the map. D29 (2026-09-14) ordered the inventory's "bodies and faces" tile split into three, Faces, Body animation, and Body language. `production/systems-inventory.json` was typed 2026-09-15 and still carries one tile; the string "body language" appears 0 times in the file | IN |
| B13 | reaction and combat animation | partial | 21 fbx in `Characters/A` and the tier-A picks in `Characters/_picks.json`: fight idle, enter and exit fight idle, block start, hold, end, block broken. `game-design/combat-spec.md` exists; D4 puts combat before driving | |
| B14 | vehicle entry, exit and driving animation | absent | Nothing measured. `Game/TrafficHost.cs:1456` is the whole of getting into a car, and `:1468` shows what the player sees: a toast reading "You get in." No clip, no transition | IN |
| B15 | crowd bodies at a second fidelity tier | partial | `Game/Mannequin.cs`, which is honest about itself: "It will not be mistaken for a person. It will be unmistakably A PERSON WALKING." Its own note records that both tiers are live at once and will be for a long time | |

### Group C. Objects the player uses (5 categories)

| id | category | typed | evidence | call |
|---|---|---|---|---|
| C1 | handheld props | absent | Nothing measured. No held object geometry exists; the pat-pockets and rummage clips handle nothing | IN |
| C2 | readable documents: letters, papers, the book of fares | absent | Inventory tile "letters and newspapers the player can read" is typed absent, with the grep that found nothing recorded on the tile and the reason stated: LATE-ANALOG means paper is the information channel, so this is pillar work and not dressing | IN |
| C3 | period technology props | partial | E3 telephone kiosk, 11 pieces, is the one that exists. Over 192 scripts: `camcorder` 0, despite canon minting exactly one camcorder in town as a rare witness type; `answering machine` 1; `pager` 1. The inventory's "radio and TV" tile is absent | |
| C4 | weapons and tools | partial | `Core/Arsenal.cs` with concealment fits. No weapon geometry is held | |
| C5 | searchable containers and their contents | absent | Inventory tile "searching a room, a container or a body" typed absent | IN |

### Group D. Sound (9 categories)

**THIS GROUP IS THE AUDIT'S LARGEST CORRECTION TO ITS OWN FIRST READING, and
the correction is recorded rather than quietly absorbed.** My first pass typed
five of these nine absent on one measurement: the repository contains 2,111
audio files and every single one is a voice clip or a voice candidate. That
measurement is true and is restated below. The conclusion drawn from it was
false, and reading `Game/Audio.cs` rather than counting files is what caught it.

**THE MEASUREMENT.** 2,027 wav, of which 2,010 are the six crowd pool voices at
335 clips each under `StreamingAssets/Audio/Voice/crowd_*`, 13 under
`game-design/voice-live` and 4 under `game-design/picked-clips`; plus 84 mp3, 65
of them candidate auditions under `voice-candidates/` and 19 picked clips. Zero
ogg, zero flac, zero aiff anywhere. There is no recorded non-voice audio file in
this project.

**WHAT THAT DOES NOT MEAN.** The game is not silent. `Game/Audio.cs` SYNTHESISES
its non-voice audio at runtime, in DSP, and the inventory's SFX tile says so in
one line I had read and not understood: "Every sound is synthesised at runtime
unless a pack is dropped under StreamingAssets/Audio." Cloth, keys, footsteps,
rain at two layers, a day bed and a night bed crossfaded equal-power, four
material impacts, five interface cues and a four-stem adaptive score are all
generated from noise and sine sums, and every one of them has a live caller.

**SO THE HONEST TYPING IS `partial` FOR ALL OF THEM**, and the absent thing is
not sound but RECORDED MATERIAL. That is a different finding and a better one,
because it is the finding D26 already acts on: Jafar ruled sound a lane with CC0
libraries and the engine's own audio, which is a ruling that synthesised
placeholder audio is not the bar. And it is sharper in the engine that ships:
the inventory's tile "sound in the Unreal build" is absent, and all of the above
lives in the C# Game layer.

`Core/Mixing.cs:29` declares six buses: Voice, Foley, Impact, Ambience, Music,
Ui. All six have something to play, and five of them are playing something
nobody recorded.

| id | category | typed | evidence | call |
|---|---|---|---|---|
| D1 | cast voice recordings | partial | The casting is DONE and the recording is not. `Core/VoiceBank.cs:59` declares 17 cast voice ids; `tools/voice-cast-check.py` run this session reports all 7 tier-1 principals reaching a voice, two through aliases (sera to kest, halvard to hal); `game-design/picked-clips/` holds one picked reference clip per voice, 17 cast plus 6 crowd; `voice-candidates/` holds 13 directories of unused auditions. What is absent is the rendered bank: `StreamingAssets/Audio/Voice` contains the six crowd pools and no cast directory at all. `game-design/production-plan-audio-art.md:723` sizes that bank at 49,476 clips across 19 voices | |
| D2 | crowd and bark voices | exists | 2,010 rendered wav across six pool voices, with `rendered.json` and `barks-manifest.json` beside them; `game-design/barks.json` holds 2,604 distinct bark lines | |
| D3 | foley | partial | `Game/Audio.cs:830` `Foley(kind, volume)` synthesises cloth long, cloth short and keys, called from `Game/DialogueUI.cs:1546` on the coat verb; footsteps at `Audio.cs:818`. Zero recorded files. D26 names what is owed: footsteps BY SURFACE, doors, cloth, breath | |
| D4 | exterior ambience beds | partial | `Game/Audio.cs:179` makes a looping Ambience source; `:408` and `:439` set synthesised `ambience_day` and `ambience_night` clips crossfaded equal-power at `:451`; `RainBed` at `:349` builds two rain layers from shaped noise. Zero recorded files, and no harbour bed of any kind | |
| D5 | room tone | partial | `Game/RoomTone.cs` holds a room-tone authority and `Game/Audio.cs:335` gains the bed through `Core.Acoustics.OutsideBleed`, so a door does muffle the outside. Zero recorded interior tones | |
| D6 | spot and one-shot effects | partial | `Game/Audio.cs` `Impact(material, force)` synthesises metal, glass, wood and soft hits, called from `Game/DoorHost.cs:161` and `:162` and `Game/PlayerController.cs:554`. Zero recorded files | |
| D7 | music | partial | `Core/MusicModel.cs` with 4 layers; `Game/Audio.cs` plays four sample-aligned stems faded independently, driven from `Game/GameController.cs:3322`. No authored score. NOTE: the inventory's music tile still describes "a synthesised day and night pair", which the code's own comment calls the thing the stems replaced. MusicGen and Stable Audio Open are already on the licence allowlist | |
| D8 | UI sound | partial | `Game/Audio.cs:872` `Ui(kind)` synthesises page, coin, door, dread and tick, called from `Game/DialogueUI.cs` and `Game/GossipDirector.cs:596`. Zero recorded files | |
| D9 | reverb and impulse responses | partial | `Core/Acoustics.cs` with 10 reverb references across the scripts. No impulse response file is held | |

### Group E. The screen (10 categories)

| id | category | typed | evidence | call |
|---|---|---|---|---|
| E1 | typeface | exists | `ledger/Assets/Resources/LedgerSans.ttf`, 442,960 bytes, PT Sans under the SIL Open Font License 1.1, with `LedgerSans.LICENCE.txt` beside it. NOTE: `Game/UiTheme.cs:87` still says "Empty until M17.9 lands one". That comment is decayed; the file is on disk | |
| E2 | icon set | absent | Nothing measured. Two hits for `icon` across 192 scripts, both structural. The only icon art is `Resources/AppIcon`, eight png of one mark at eight sizes. Disco Elysium spent about a year settling the detail level of inventory icons | IN |
| E3 | UI panel and frame art | partial | `Game/UiTheme.cs` and `Core/Typography`: an approved visual language expressed entirely as colour constants and a type scale, drawn procedurally. No panel texture, frame, rule or ornament exists as art | |
| E4 | HUD elements | partial | inventory tile "HUD" is typed exists: clock, money and slot on one line plus a toast channel. It is text, and the what-they-know HUD is a separate absent tile | |
| E5 | title screen and menu art | partial | `Game/MainMenu.cs` and `Game/OptionsScreen.cs` exist as screens. No art. The inventory's "visual identity in the Unreal build" tile is absent, with the note that the probe carries no title, no typography, no menu and no graphic identity | |
| E6 | loading and transition screens | absent | Nothing measured. `LoadingScreen` returns 0 across the scripts. `Game/ScreenCurtain.cs` is a fade to black for the Fall, not a loading screen, and says so | IN |
| E7 | in-game map art | absent | Nothing measured. D20 rules no minimap for phase A and D36 says a map's design follows the world's size, so this is a decided-later rather than an oversight. `map.html` at the repository root is a studio page, not game art | ASK |
| E8 | subtitles and caption presentation | exists | 106 references across the scripts; `Game/SpeechBubble.cs` stages the line, fading the last stretch so lines leave rather than blink out | |
| E9 | cursor | partial | 25 references. No cursor art is held | |
| E10 | build and product identity | partial | eight `AppIcon` png for the Unity build. The Unreal side has none, per the "visual identity in the Unreal build" tile | |

### Group F. Fiction as material (7 categories)

| id | category | typed | evidence | call |
|---|---|---|---|---|
| F1 | brand marks and identities | partial | `content/brands/brand-bible-v1.json` and `production/specs/brand-bible-v1.md`. Canon names four minted (Mickey's, the Tivoli, Meridian Harbour Board, Meridian Ferry) and six still owed: the football club, the local paper, the pirate radio station, the regional TV channel, the telephone operator's mark and the postal cypher | |
| F2 | world text corpus | exists | `Game/WorldText.cs`; the inventory records 153 pieces of world text placed and depth tested in the Unity street with none refused | |
| F3 | dialogue banks and barks | partial | `content/dialogue/crime-witness-v1.json`, `content/dialogue/pub-regular-v1.json`, `ledger/BarkGen`, `game-design/barks.json` at 2,604 distinct lines | |
| F4 | cast cards and character notes | partial | `game-design/cast-tier1-batch2.md` with 35 headed entries; `ledger/Assets/StreamingAssets/tier2-batch-1.json` with 60 entries; `game-design/cast-noor-draft.md`. The inventory's own note: the population generator supplies names, not people | |
| F5 | newspapers and printed matter copy | absent | same tile as C2. Absent as words as well as absent as objects | IN |
| F6 | radio and TV copy | absent | inventory tile "radio and TV" typed absent, with its own measurement: zero hits for radio across the Core and Game scripts walked, and one comment about the UHF band | IN |
| F7 | graffiti | absent | Nothing measured. Canon minted five tags on 2026-09-02 (TANNER, SNIDE, GULL, QUAY FIRM, PARADE RATS). A grep for `graffiti` over 192 scripts returns 0, and no decal in the 45 generated images is named for one | IN |

### Group G. Concept and reference (10 categories)

| id | category | typed | evidence | call |
|---|---|---|---|---|
| G1 | environment concept art | exists | eight images on `origin/art/atlas-01` at `production/art/atlas-01/concepts/` (copper, exchange, fairview, gullwing, hook, ironside, mickeys, parade) with four prompt-set json beside them; five sheets plus a comparison in `production/art/concept-fairview-2026-09-10/sheets/` | |
| G2 | character concept art | absent | **Nothing measured, and the zero is exact.** A search for concept, portrait, character sheet, turnaround, costume, wardrobe, face reference and cast sheet across `HEAD`, `origin/main` and `origin/art/atlas-01` returns not one character image. The only human figure in any reference folder is `production/art/atlas-01/references/kasbah-character-09.png`, which is somebody else's art held as reference under `references/RIGHTS.md` | IN |
| G3 | costume and wardrobe design sheets | absent | Nothing measured as art. `production/art/atlas-02/research/adult-clothing-by-occupation.md` is written research and is the nearest thing that exists | IN |
| G4 | prop concept art | partial | seven png in `production/art/mickeys-cars/drawings/`; the fascia package spec and verify folders in `production/art/fascia-01/` | |
| G5 | vehicle concept art | partial | the same `mickeys-cars` drawings, which are the minicab plans and elevations | |
| G6 | interior concept art | partial | `production/art/atlas-01/MICKEYS.md` and the `previews/target-a01_pub_*` set (screen, table, till, notice paper) on that branch; `fairview-furniture-2026-09-10.json` | |
| G7 | signage and graphic design sheets | partial | the 45 generated images; the svg layout proofs in `production/art/atlas-01/artwork/` (fascia layout, hours, pump clip, returns) | |
| G8 | colour script and lighting keys | partial | `game-design/research/art-direction.md` carries a palette discipline with measured instruments (`hueArcAt`, `hueArc60`, `satP50`, `satP99`) rather than painted keys. No lighting key frame exists per time of day | |
| G9 | photographic reference boards | partial | `production/art/atlas-01/references/` on that branch: hull map, a 1981 Hull west dock photograph, a street evidence contact sheet, with `RIGHTS.md` beside them | |
| G10 | town atlas, district plans and maps | exists | `production/art/atlas-01/DISTRICTS.md`, `TOWN-FORM-BIBLE.md`, `PRODUCTION-CATALOGUE.md` and seven district plan svg with png beside them | |

### Group H. Presentation and shipping (4 categories)

| id | category | typed | evidence | call |
|---|---|---|---|---|
| H1 | key art | absent | Nothing measured | ASK |
| H2 | store page, screenshots and trailer material | absent | Nothing measured | ASK |
| H3 | credits | absent | Nothing measured. Two hits for `credits` across the scripts. `Game/UiTheme.cs` names the consequence of not having a font, "the credits cannot name a typeface, because there isn't one", which is now stale on the font and still true on the credits | ASK |
| H4 | accessibility presentation assets | partial | `UiTheme.SetColourblind` swaps the only hue-coded pair in the game to blue and orange; a text scale runs through every `MakeText`. No high-contrast or large-text asset set exists | |

## 4. The two checks the brief named specifically

### 4.1 Character concept art, against nineteen cast voices and written cast notes

**There is no character concept art in this project. Not one image.** The zero
is measured across three refs (`HEAD`, `origin/main`, `origin/art/atlas-01`)
with a search covering concept, portrait, character sheet, cast sheet,
turnaround, costume, wardrobe and face reference. The one human figure in any
art folder, `production/art/atlas-01/references/kasbah-character-09.png`, is
somebody else's work held as reference under a rights file.

**What stands beside that zero, measured:**

| The cast as words and sound | Count |
|---|---|
| tier-1 cast entries with written cards | 35 headed entries in `game-design/cast-tier1-batch2.md` |
| tier-2 generated residents | 60 in `ledger/Assets/StreamingAssets/tier2-batch-1.json` |
| cast voice ids declared and wired | 17, in `Core/VoiceBank.cs:59` |
| tier-1 principals reaching a voice | 7 of 7, measured by `tools/voice-cast-check.py` this session |
| picked reference clips on disk | 23 in `game-design/picked-clips/`, one per cast voice plus six crowd |
| cast voices planned for the full bank | 19, per `game-design/production-plan-audio-art.md:723` |
| environment concept images | 8 districts and places, plus 5 Fairview sheets |
| character concept images | 0 |

A NOTE ON THE BRIEF'S FIGURE, because the number moved twice while I checked it.
The brief says nineteen cast voices. Nineteen is the size of the PLANNED clip
bank. Seventeen voices are actually declared and wired in `VoiceBank.Cast`, and
every one of the seven tier-1 principals reaches one. I first wrote thirteen
here, from counting audition directories, and the project's own
`tools/voice-cast-check.py` corrected me.

So the comparison is sharper than the brief's, not softer: **seventeen of these
people have been cast and have a chosen clip on disk, thirty-five have written
cards saying how they think, and not one of them has ever been drawn.**

**Why this is the failure mode the audit exists to catch, rather than a
scheduling accident.** The environment had a commission structure, two atlas
deliveries, a five-station line and a review document. The cast had a voice
pipeline, a consent rule and an audition corpus. Neither of those structures
has a drawing station in it, so nobody was ever late. The category was not
deferred; it was never named, and it is not named in the inventory either: the
one tile that could hold it, "concept art and the town atlas", cites the atlas
and the district sheets and nothing else.

### 4.2 Bodies and clothing, against a photoreal bar

The brief's framing is right and the measured position is worse than it, in one
specific way that matters more than the clothes.

**What is actually on screen.** `Game/RealBody.cs` instantiates ONE Mixamo body,
on the player only, and states the reason in its own header: a Mixamo body is a
skinned mesh of several thousand triangles and `Mannequin` is thirteen boxes, on
a runner with no GPU. **The crowd is `Game/Mannequin.cs`: ten boxes and a
sphere, with one more box on top for hair or a cap.** (The two files disagree on
the part count, thirteen boxes against ten and a sphere, and `Mannequin.cs` is
the one that builds them. The crowd size, sixty-seven, is `Mannequin.cs`'s own
figure; the inventory's "bodies and faces" tile says 92 rigs, which counts a
different thing. Neither number is load-bearing here.) So against the
photoreal bar the 18 contemporary-dress bodies are not the front line. The front
line is that everybody except the player is a box figure, and the code says both
tiers will be live together for a long time.

I read the frames rather than the gate. `game-design/sim-shots/figure_run53_camA_before_after.png`
is the current Unreal evidence for a person in the street, and its own caption
line reads `box=x605.675/y315.393 projH=77.63 461 of 5460 px differ by >2/255`.
A figure that changes 461 pixels is the whole of the human presence in that
frame. `game-design/sim-shots/brief_2026-09-16_hook_day_run51.png` is the day
street: brick, roofs, awnings, railings, bollards, a skip, lamp columns, cobbles,
and no person, no vehicle, no vegetation, no shopfront glazing and no signage
in shot.

**On clothing specifically, the route is already decided and the prior lane
settled it.** `research/clothing-pipeline` establishes that D2 names MetaHuman
as the rig source, D16 made the engine Unreal on 2026-09-10, MetaHuman is on the
licence allowlist and free under a million in revenue, its clothing arrives
fitted and rigged, and nothing in our toolchain touches a skinned mesh at all
(the Unreal importer imports static meshes only). That delivery also names the
one hard case to test a route with: the donkey jacket, which hangs straight from
the shoulders past the hip and therefore does not follow the body.

**So the clothing gap is not a decision gap.** The decision was taken eight days
before this audit. It is that the decided route has not been exercised once, and
that `Core/Wardrobe.cs`, the file everyone points at when clothing comes up, is
a palette. It picks one of eight authored hue bands and tints whatever the
bought mesh is already wearing. Its own header says what it is for and never
claims to be a garment.

## 5. What the absent column costs

D24's operative half is the spend rule: anything that does not feed perception,
memory, gossip or consequence gets the smallest budget that keeps it from
looking wrong. That cuts both ways, and this section uses it both ways. For each
absent category: the argument, then THE SMALLEST VERSION, which is what D24
actually licenses.

Ordered by what it costs to leave the category absent, not by size.

### 5.1 The three that break a pillar, not the dressing

**B3, facial rig and lip sync (IN).** Pillar 2 is real spoken conversation and
the most-viewed surface in this game is a face at conversational distance. D2
said this on 2026-08-31 and named the driver. The measured position is that
`viseme`, `lipsync` and `facial` return zero across 192 scripts. A talking head
with a still mouth is not a smaller version of a talking head; it is the one
thing that makes a photoreal face read as a corpse, and it undoes pillar 2 in
the first conversation of the thirty minutes the Meridian Test allows.
SMALLEST VERSION: jaw-and-mouth blendshapes on cast heads only, driven offline
over the rendered clip corpus, crowd faces static at distance. That is exactly
what D2 already approved, batch first and streamed later.

**B12, body language as a moat surface (IN).** D29 ruled on 2026-09-14 that this
is moat, not polish, with the reason stated: the five-rung identification ladder
is invisible except in dialogue, and body language is how a player reads it
without being told. Condition 2 of the Meridian Test is that the world visibly
knows you at least once inside thirty minutes; a posture is the cheapest way
that happens without a line of dialogue.
SMALLEST VERSION: three idle variants and two approach variants, selected by
identification rung. Five clips. Mixamo holds them already, and the catalogue on
disk (`ledger/Assets/Characters/_catalogue.txt`, 2,846 clip names) is the proof
the fetch works.

**C2 and F5, readable paper (IN, together).** LATE-ANALOG is not a period
setting, it is the information architecture: with no internet and no mobiles,
paper and the telephone are how information moves, which is pillar 1's supply
line. The inventory's own tile says it: this is pillar work and not dressing.
SMALLEST VERSION: one readable object type (a sheet of paper on screen with
authored text), four kinds of content (a letter, a page of the local paper, a
page of the book of fares, a notice), and the existing image generator for the
paper itself. The 45 generated decals prove that pipeline runs.

NOTE ON WHAT MOVED OUT OF THIS SECTION. Foley and ambience were in this list
until group D was corrected. They are typed partial, so they are not absent
categories and do not belong in a costed absent column. They remain the second
of my three recommendations in section 6, because a partial whose entire
material half is synthesised placeholder is a different thing from a partial
that is half finished, and D26 already ruled on it.

### 5.2 The eight where absence makes the frame read as a film set

These do not touch the moat. Under D24 they get the smallest budget that keeps
them from looking wrong, and the argument for each is what "wrong" means.

**A20, parked vehicles (IN).** Jafar's own note on the tile is the argument: an
empty kerb reads as a film set, and period cars parked badly are the cheapest
density in the project. SMALLEST VERSION: three or four fictional period
silhouettes, parked, never driven, never entered. Canon forbids real car models,
so a generic shape is not a compromise here, it is the requirement.

**A10, vegetation (IN).** A British port town with no weed in a gutter, no moss
on a wall and no tree anywhere reads as a set rather than a place. The bill of
materials already refuses street trees as an American tell, which is a period
judgement about AVENUES and not an argument against planting.
SMALLEST VERSION: weeds at wall bases, moss in shade, and one or two scrubby
things in yards. Two of these are decals and `Moss001` is already on disk in the
ambientCG set.

**A11, water (IN).** It is a port town. The map already has a water line at the
south edge that buildings may not cross, and gulls fly over it. A port with no
water in any frame is the single largest departure from canon in the visual
build. SMALLEST VERSION: a flat tidal plane with the sky reflected in it, seen
from the quay and never entered, plus wet gutters where the existing
`gutter_water.png` and `puddle_mask.png` decals already sit. `game-design/research/water.md`
sized this in August and is the place to start rather than a new search.

**A14, A15 and A16, interiors, fittings and clutter (IN).** D14 already rules every
interior a designed layout. Mickey's is the player's own office and the
information room is the business, per D19. An interior you cannot enter makes
the one place the game is about a facade. SMALLEST VERSION, and it is genuinely
small: ONE room, Mickey's, with the fittings D19 names (the book of fares, the
radio, the desk, the rank outside the window). Shadows of Doubt's method is the
cheap one for later: hand-made floorplan grids subdivided by rule, furniture
coloured from a per-room palette.

**E6, loading and transition screens (IN).** This is the first thing a player
sees and the only asset guaranteed to be looked at with full attention. An
engine default here is the cheapest possible damage to condition 1 of the
Meridian Test. SMALLEST VERSION: one full-bleed image from the environment
concept set that already exists, the shipped typeface, and the town's name.
Close to free.

**F6, radio and TV (IN).** A town with no radio in 1990 is not a quiet town, it
is a town with the era removed. Canon owes a pirate radio station and a regional
TV channel among its six unminted brands, the phone box and the answering
machine already exist as systems, and D19 made Mickey's information room a radio
nobody can help overhearing. That makes radio a pillar-1 carrier rather than
dressing: it is a way information reaches people who were not there.
SMALLEST VERSION: a handful of written bulletins and a shipping forecast read by
one of the existing voices, played from the radio in Mickey's and from one shop
front. Words and the voice pipeline, no new capability.

**F7, graffiti (IN).** Canon minted five tags on 2026-09-02 and the code has
never heard of them. This is the cheapest district-legibility asset there is: a
wall tells you which part of town you are in before any sign does.
SMALLEST VERSION: five decals, one per tag, placed by district. The generated
decal pipeline that made 45 images makes these.

**A13, terrain and coastline (IN).** Meridian is seven districts on a coast with
hills at Fairview. Absent is correct TODAY because only one street exists, and
becomes wrong the moment a second district does. SMALLEST VERSION: a ground form
carrying the hill and the water edge, no detail, at the point the second
district starts. This is the one absent row whose cost is zero right now.

### 5.3 The six where absence is invisible today and expensive later

**B6, garments as geometry (IN).** Covered at 4.2: decided, unexercised.
SMALLEST VERSION: three garments on the MetaHuman path, and the prior lane
already named which three and which one is the test.

**B8, carried items (IN).** `Core/Arsenal.Concealment` has four rungs nothing
exercises, and the shopping-bag walk cycle carries nothing.
SMALLEST VERSION: a bag, a coat with pockets, and one concealable object.

**B14, vehicle entry and exit (IN).** Today the player reads "You get in." as a
toast. D24 says driving may exist and must not look broken; a teleport into a
car is the definition of looking broken. SMALLEST VERSION: two clips, in and
out, from the Mixamo catalogue, with a fade if the alignment is poor.

**C1, handheld props (IN)** and **C5, searchable containers (IN).** A game where
what people know about you is the mechanic needs things to be found on you and
taken from places. SMALLEST VERSION: five or six objects at the fidelity of the
existing base-mesh props, and one container interaction.

**E2, icon set (IN).** Disco Elysium spent about a year on icon detail level and
has no 3D art at all, which is evidence that this is a real category rather than
a finishing task. SMALLEST VERSION: one drawn family covering the verbs the game
actually has.

**G2 and G3, character and costume concept art (IN).** The measured position is
section 4.1. The argument is that concept art is not a picture of the game, it
is the decision about what the game looks like, taken once and cheaply instead
of nineteen times and expensively in the model. Warhorse published 300 pages of
it for KCD2; Disco Elysium's 105 portraits ARE its characters. Skipping it does
not save the work, it moves the work into the expensive medium and guarantees
that nineteen people designed by nineteen prompts do not look like one town.
SMALLEST VERSION: one sheet, the nine or ten people a player meets in the first
thirty minutes, at the fidelity of the existing Fairview sheets, plus one
costume page per social band (dock, market, office, law) rather than per person.
The pipeline that made the eight district concepts and the five Fairview sheets
makes these, so this is a brief and a run rather than a capability.

### 5.4 The four ASKs

Every one of these is genuinely Jafar's, and none is a doubt about need.

**E7, in-game map (ASK).** D20 rules no minimap for phase A and D36 says a map's
design follows the world's size. The systems audit already raised the question
in its section 4 as "does Meridian have a map, or do you learn it by walking and
asking", and it is unanswered. THE ASK: whether a map is an asset category at
all in this game, or a thing the player builds by asking people.

**H1, key art, H2, store and trailer material, H3, credits (ASK).** Success is
defined as clearing the Meridian Test, not shipping or selling, so the case for
these is not automatic and should not be assumed by a studio that enjoys making
things. THE ASK: whether LEDGER is ever presented to anyone beyond Jafar. If the
answer is no, all three stay absent for ever and that is a clean result. If it
is yes, H3 is a legal and courtesy obligation rather than a choice, because the
licence allowlist carries attribution duties for CC0 and OFL material that only
a credits screen or an about page discharges in a shipped build.

## 6. The three I would act on first, and why these three

The brief asks for three. These are chosen on one test: which absent category
does the most damage to the Meridian Test per unit of work, given what the
project can already do.

**FIRST: character and costume concept art (G2, G3).** It is the cheapest of the
three, it is the one whose pipeline already exists and has run, it is a blocker
on the other two rather than a parallel task, and every day it stays absent the
studio makes more cast decisions in words that will have to be re-decided in
pictures. Nine or ten faces and four costume pages. This is the one where
inaction is actively accruing cost.

**SECOND: recorded sound material (D3 to D8, the material half).** Not an absent
category after the correction at group D, and still second, because the whole
non-voice soundtrack of this game is DSP synthesised from noise and sine sums
against a photoreal bar, and because it moves condition 3 of the Meridian Test
(alive without being prompted) more per hour than anything else on the board.
Everything needed is already decided: D26 made sound a lane with a standing
daily deliverable, named the contents (footsteps by surface, doors, cloth,
breath, rain, room tone, the harbour bed) and set the constraint (CC0 libraries
and the engine's own audio, no new tooling). D26 gates it on the street's light
being right, which is a real gate and Jafar's to judge, so the recommendation is
narrow: that it starts the day that gate opens, and not behind anything else.
The one thing that IS absent here is the Unreal side, which is silent, and that
is where the material has to land anyway.

**THIRD: the face that moves (B3).** It is the largest of the three and the only
one that touches a pillar directly. Pillar 2 is the reason this project exists in
the form it does, and thirty minutes of a photoreal face talking with a still
mouth loses condition 1 and condition 3 together. D2 approved it in August, the
driver is named, and nothing has been built. The honest note is that this one is
weeks rather than days, which is exactly why it should start before it is
urgent.

WHAT I DELIBERATELY DID NOT PUT IN THE THREE, with the reason, because a choice
without its rejects is not a choice:

- **Interiors (A14 to A16).** Bigger than all three combined, and D14 and the
  visual ladder already order it after the street. Leaving it out of the three is
  an ordering call, not a judgement that it matters less.
- **Water (A11).** The strongest single argument in the audit (it is a port town
  with no water) and it is nonetheless gated behind the sky, which the inventory
  says the last Unreal run rendered as nothing at all. A reflective plane under
  no sky is not an improvement.
- **Parked vehicles (A20).** The best cost-to-density ratio in the whole absent
  column and it very nearly made the three. It loses to concept art only because
  a car is not on the critical path of anything and a cast sheet is.

## 7. What this audit found about the project's own maps

Four findings about the instruments rather than the content, the last of them
three separate tile notes. Each is a fact about a file, measured here, and none
of them is a proposal.

### 7.1 Where the inventory can and cannot see an asset category

`production/systems-inventory.json` holds 111 systems in five areas, and the
`content` area holds 11 tiles. That is not a criticism: it is a map of SYSTEMS,
typed by a director under a ruling, and it says so in its own header. But it is
the only enumeration this project has that comes near content, and a reader
looking there for the material the game is made of would find 11 content tiles
where this audit finds 84 categories.

The useful measurement is not that gap, though, because tiles outside the
content area carry asset categories too (the water tile is in `world`, the map
tile is in `player-facing`). The useful measurement is per absent category, and
here it is, checked one by one against all 111 tile names:

| How the inventory sees it | Count | Which |
|---|---|---|
| a tile of its own, correctly typed absent | 10 | A11 water (tile 77), A14 interiors (22), A20 parked vehicles (79), C2 and F5 readable paper (80), C5 searchable containers (75), E6 loading screens (inside tile 49, whose note says so), E7 map (42), F6 radio and TV (62), H3 credits screen (inside tile 53, whose note says so) |
| inside a broader tile that does not distinguish it | 2 | B3 facial rig and lip sync, inside "bodies and faces" (24); G2 character concept art, inside "concept art and the town atlas" (60) |
| **not present in the file in any form** | **14** | A10 vegetation, A13 terrain, A15 interior fittings, A16 interior clutter, B6 garments as geometry, B8 carried items, B12 body language, B14 vehicle entry, C1 handheld props, E2 icon set, F7 graffiti, G3 costume sheets, H1 key art, H2 store material |

**So more than half of what this audit found absent is invisible from inside the
project's own map, and the two known examples that prompted this brief are both
in the invisible column or the undistinguished one.** That is the systems
audit's finding about its own instrument (section 5.1 of CROSS-CUTTING: the
inventory is a good map of what the studio has CONSIDERED and an incomplete map
of what it HAS) pointed at content instead of code, and it comes out the same
way.

DENOMINATOR, because a count like this needs one: 26 absent categories examined
against all 111 tiles, read by name, one at a time. Nothing was sampled.

### 7.2 D29's inventory change has not landed, and the inventory was typed after it

D29 was ruled on 2026-09-14 and ordered the "bodies and faces" tile split into
three: Faces, Body animation, and Body language as a moat surface. The record
states what is missing in its own words: "The register decides faces in D2 and
NOTHING decides bodies."

`production/systems-inventory.json` carries `typedOn: 2026-09-15`, one day after
that ruling, and still holds one tile named "bodies and faces". The string "body
language" appears 0 times in the file.

This is filed as a finding and nothing more. Under CLAUDE.md rule 11 an audit
finding does not generate its own follow-on work, and the research lane touches
no inventory in any case.

### 7.3 A licence distinction on the face route that I could not verify

`ledger-v2/research/license-allowlist.md` reads, under SHIP-SAFE: "Faces:
Audio2Face-3D (MIT)." D2 says the same, "open-sourced 2025-09-24, MIT".

The search channel says the picture may be two-part: NVIDIA published
Audio2Face code, models and training stacks in September 2025 under an MIT
licence for the SDK and repositories, while the MODEL WEIGHTS on Hugging Face
(`nvidia/Audio2Face-3D-v3.0`) are governed by the NVIDIA Open Model License
rather than MIT.
([VideoCardz](https://videocardz.com/newz/nvidia-releases-audio2face-as-open-source-for-game-developers);
[Open Source For You](https://www.opensourceforu.com/2025/09/nvidia-moves-audio2face-technology-to-open-source/);
[nvidia/Audio2Face-3D-v3.0 model card](https://huggingface.co/nvidia/Audio2Face-3D-v3.0))

**I could not verify this, and I am not asserting it.** `huggingface.co` is one
of the five hosts that were added to the allowlist and still answer 403 at the
gateway, so the model card, which is the primary source and the only thing that
settles it, cannot be read from here.

WHY IT IS WORTH A LINE ANYWAY: the allowlist's own title is "verify weights
license, not code license", and this is precisely the shape of thing that
warning exists for. If the search summary is right, the allowlist's own rule has
been applied to the wrong half of a two-part release. If it is wrong, one page
read settles it. Either way it is a ten-minute check that only needs a machine
that can reach the host, and B3 is one of the three recommendations above.

### 7.4 Three tile notes that the code beside them falsifies

All three found while checking my own typing, and all three are the same shape:
a tile whose TYPING is right and whose stated REASON or DESCRIPTION is not.

**The ambient beds tile.** Tile 91, "ambient beds and room tone", is typed
partial with this reason: "Typed partial because the tokens ambientBed,
ambientLoop and BackgroundLoop return zero in 218 files: outdoors there is no
bed." Outdoors there is a bed. `Game/Audio.cs:179` creates a looping source
named Ambience, `:408` and `:439` give it synthesised `ambience_day` and
`ambience_night` clips, and `:451` crossfades them equal-power with a comment
explaining why linear would dip at dusk. Three token names that the code does
not happen to use were read as the absence of the thing. The right reason for
partial is the one in this delivery: the bed exists and nobody recorded it.

**The music tile.** Tile 46 says "A music bus plays a synthesised day and night
pair and the adaptive layer model exists in Core." `Game/Audio.cs` now plays
four sample-aligned stems faded independently through `Core/MusicModel` (4
layers), driven every frame from `Game/GameController.cs:3322`, and the code's
own comment says what happened: "The fixed day/night pair was wallpaper; this is
the score doing the one job nothing else can." The tile describes the thing that
was replaced. The typing, partial, is still right, because there is still no
authored score.

**The voices tile.** Tile 61 says "no voice is picked for any character in the
files committed here". Every cast voice is picked. `Core/VoiceBank.cs:59` names
17, `game-design/picked-clips/` holds a chosen clip for each of them plus the
six crowd pools, and `tools/voice-cast-check.py`, which is in this project's own
verify suite and ran green this session, prints all seven tier-1 principals
reaching a voice, two of them through aliases the tool exists to catch. The
typing, partial, is right for a third time, because the rendered bank is what is
missing: `StreamingAssets/Audio/Voice` holds the six crowd pools and no cast
directory.

None of the three is filed as work. All three are recorded because I made the
same class of mistake myself in this document, twice, from the same habit of
trusting a count over the file: I typed five sound categories absent from a file
census, and I wrote thirteen cast voices from a directory count until this
project's own tool said seventeen. A finding that only names other people's
instances of a fault the author just committed is not an honest finding.

## 8. Sources

External, all through the search channel, none read as a page. Dated where the
page carries a date.

1. [Development of Red Dead Redemption 2, Wikipedia](https://en.wikipedia.org/wiki/Development_of_Red_Dead_Redemption_2) and [ScreenRant, 25 things only true fans know](https://screenrant.com/red-dead-redemption-2-making-of-details/): about 1,600 developers, about 2,200 days of motion capture and recording, 1,200 actors, 700 voicing 500,000 lines, about ten times GTA V's animation volume.
2. [MCV/Develop, The Art of Disco Elysium](https://mcvuk.com/business-news/we-knew-immediately-that-we-needed-to-make-a-game-with-a-striking-and-unique-look-to-accompany-the-writing-a-look-that-would-balance-the-mundane-with-the-unfamiliar-and-strange-the-art/): 105 character portrait files, 193 squares of 4K environment texture, about a year spent settling inventory icon detail, the character pipeline rebuilt three or four times.
3. [ColePowered DevBlog 13, Creating Procedural Interiors](https://colepowered.com/shadows-of-doubt-devblog-13-creating-procedural-interiors/) and [DevBlog 21, How Voxels Saved the Project](https://colepowered.com/shadows-of-doubt-devblog-21-how-voxels-saved-the-project/): buildings split into floors, addresses and rooms; hand-made floorplan grids about 15 by 15 subdivided by prioritised rules; voxels instead of meshes; furniture keyed by texture map and coloured from a five-colour per-room palette.
4. [inara.cz, all armour and clothing, KCD2](https://inara.cz/kingdom-come-2/armors/) and [Kingdom Come Deliverance wiki](https://kingdom-come-deliverance.fandom.com/wiki/Warhorse_armour/KCD2): 16 item slots, layering up to four garments on the chest, clothing that becomes worn, dirty and bloody through use.
5. [Warhorse Studios announcement](https://x.com/WarhorseStudios/status/1864613767662764501?lang=en), date not established because the post was not read: a 300-page KCD2 art book of concepts and art direction covering 2019 to release.
6. [Game Developer, The AI of Hitman (2016)](https://www.gamedeveloper.com/design/the-ai-of-hitman-2016-) and [Hitman wiki, NPC](https://hitman.fandom.com/wiki/NPC): NPC, crowd and animation architecture built for Absolution and extended; crowd NPCs as a distinct minimal-AI class. The Game Developer page itself is blocked here, as the previous lane also recorded.
7. [A Sound Effect, game audio explained](https://www.asoundeffect.com/gameaudioexplained/), [Side, game sound design](https://side.inc/services/audio-production/sound-design), [Bluezone, guide to game sound effects](https://www.bluezone-corporation.com/blog/the-ultimate-guide-to-video-game-sound-effects-for-indie-developers): the four-pillar division of game audio and the named sub-kinds, ambience and room tone, foley, one-shots and loops, UI and notification sound.
8. [Pixune, game art pipeline](https://pixune.com/blog/game-art-pipeline/), [Beyond Extent, environment art specialisations](https://www.beyondextent.com/articles/environment-art-specialisations), [8bitplay, game art roles](https://8bitplay.com/blog/game-art-jobs-and-roles-explained-a-recruiter-guide/): the standing division into concept, character, environment, props, animation, VFX, UI/UX and technical art.
9. [NVIDIA Audio2Face-3D on GitHub](https://github.com/NVIDIA/Audio2Face-3D), [VideoCardz](https://videocardz.com/newz/nvidia-releases-audio2face-as-open-source-for-game-developers), [Open Source For You](https://www.opensourceforu.com/2025/09/nvidia-moves-audio2face-technology-to-open-source/), [nvidia/Audio2Face-3D-v3.0 model card](https://huggingface.co/nvidia/Audio2Face-3D-v3.0): the September 2025 open-source release, 52 ARKit blendshape outputs, Maya and Unreal Engine 5 plugins, and the code-versus-weights licence question at 7.3.

Internal, and these are the load-bearing ones. All read in this checkout at
`766a210` except where a branch is named.

- `ledger-v2/respec/vision-pillars-v2.md`, `canon.md` (including D24 in full), `production/systems-inventory.json`, and `production/research/coverage-audit/CROSS-CUTTING.md` on `origin/research/coverage-audit`.
- Decision records D2 (faces), D14 (authored interiors), D20 (no minimap for phase A), D24 (what LEDGER is not), D26 (sound is a lane), D29 (body language is a moat surface), D36 (a map's design follows the world's size), D40 (the sky is a photograph), D46 (Mixamo bodies are in).
- `ledger-v2/research/license-allowlist.md`.
- `production/specs/vignette-bill-of-materials.json` and `.md`, `production/specs/vignette-pieces.json`.
- Prior research lane deliveries: `research/asset-packs`, `research/clothing-pipeline`, `research/clothing-assembly-line`, `research/markerless-mocap`, `research/photoreal-on-a-budget`.
- `game-design/production-plan-audio-art.md`, `game-design/research/art-direction.md`, `game-design/research/water.md`.
- `tools/voice-cast-check.py`, run this session, which corrected a count of mine.
- The stills at `game-design/sim-shots/`, opened rather than read about.

## 9. What this audit could not establish

1. **No external page was read in full.** Every one of the five newly
   allowlisted hosts answers 403 at the gateway, as section 0 measures, and the
   controls (`en.wikipedia.org`, `docs.blender.org`) answer `EGRESS_BLOCKED`
   too. Every external citation in section 8 is the search channel's summary of
   a named page. Every quantity relayed from one (RDR2's 2,200 days and 500,000
   lines, Disco Elysium's 105 portraits and 193 texture squares, Shadows of
   Doubt's 15 by 15 floorplan grids and five-colour palettes) is a direction and
   not a measurement.

2. **The Audio2Face-3D weights licence is unresolved**, per 7.3, and it cannot
   be resolved from this container because `huggingface.co` is blocked. It bears
   on the third of my three recommendations.

3. **Published per-category asset counts for the five games do not exist in any
   form I could reach.** I searched specifically for unique model, prop,
   building, vegetation and texture counts for RDR2 and GTA V and found none,
   and the search channel said in terms that these are not commonly published.
   So the enumeration is a list of KINDS with no scale attached, and this
   delivery makes no claim about how many of anything a finished game holds. If
   a number of that shape is wanted, a GDC talk or an art-book teardown is the
   route and both are behind a paywall or a blocked host.

4. **The Kenney city kits were not audited against the period rule.** 107 fbx
   across four kits and 50 in the car kit are held and typed as evidence for
   A1 and A19. The asset-packs delivery raised exactly this question about a
   bought pack ("the real cost of a pack is not its price, it is auditing 646
   meshes against a period rule") and named the number it most wanted and could
   not get. The same question applies to what is already on disk and I did not
   answer it either: I do not know what share of those 157 meshes survives the
   1988 to 1992 rule and the no-real-vehicles rule. It is an afternoon's work
   for somebody with the files open and it would change how much A1 and A19
   actually have.

5. **Nothing here was verified in the Unreal build**, which is the engine D16
   decided on. Group A's counts come from `production/specs/vignette-pieces.json`,
   which is the shared scene both engines generate from, and the Unity sim
   verdict. `ue-probe/Content/Ledger/Props` holds 18 static mesh uassets, one
   material and two textures, and that is the whole of the Unreal content tree.
   Where the two diverge, this document describes the Unity side.

6. **The 84 is not a census of anything.** It is what one session's enumeration
   surfaced, working backwards from five games and two discipline sources, and
   section 2.3 names the four places the grain was chosen by judgement. Cinematics
   and cutscene assets are not enumerated at all, because none of the five games
   contributed a reason to and LEDGER has named no cinematic; that is an
   omission I am aware of rather than one I have covered.

7. **No artist saw any of this.** Every judgement about whether a category is
   partial or absent is a judgement about what is ON DISK, not about whether
   what is on disk is any good. `production/quality-ladder.md` asks the best
   available versus first working question at close; this audit does not ask it
   once, and eleven `exists` rows could all be first-working.

## 10. The one contradiction, which I went looking for and did find

I looked, across all 84 categories, for material this project HOLDS that
contradicts canon, a pillar or a decision record rather than merely falling
short of it. My first draft of this section reported none. That draft was wrong,
and it was wrong because I read a file extension instead of the code that makes
it.

**D18 puts alcohol out entirely and keeps tobacco. The animation library holds
the opposite of both.**

Measured this session by listing `ledger/Assets/Characters/` and reading
`_picks.json` and `tools/mixamo-pick/pick_animations.py`:

| What D18 says | What is on disk |
|---|---|
| "Alcohol and gambling are out ENTIRELY: never shown, served, drunk or spoken of" | `Characters/C/drink__Drinking_2dee24f8...fbx` is live, and `_picks.json` records the `drink` slot as an EXACT match on `^drinking\b`, tier C |
| the same clause, on "served" | `Characters/C/work_counter__Bartending_4f5d21e1...fbx` is live and fills the `work_counter` slot |
| "Tobacco stays" | the `smoke` slot reads `found: null` after trying two patterns, and `smoke__Smoking_...fbx.rejected` sits beside it |

The picker still carries the slots as targets. `pick_animations.py:216` defines
`("drink", "C", [r"^drinking\b", r"\bdrink(ing)?\b"])` and `:273` defines
`("sit_drink", "D", [r"^sitting drinking\b", ...])`. D17 and D18 were both ruled
on 2026-09-10 and neither slot was changed.

ONE OF THE THREE IS A JUDGEMENT AND I AM NAMING IT AS ONE. That
`drink__Drinking` is a drinking animation is a measurement. That a clip named
`Bartending` in a slot named `work_counter` reads as serving alcohol is a
reading, and it could as easily dress a shop counter. The first row does not
depend on the second.

**WHAT I GOT WRONG FIRST, kept because the error is the lesson.** I wrote that
this section resolved clean, on the evidence that rejected clips under
`Characters/D` were drinking animations the pipeline had refused. Reading
`pick_animations.py:931` shows `.rejected` is what the picker renames a PREVIOUS
pick to when a better clip takes its slot. It is a slot-replacement marker with
nothing to do with content. Of the seven `.rejected` files in the repository,
one is a drinking clip and one is the smoking clip D18 keeps, which is the
inversion above rather than a refusal.

**WHY NO GATE CAUGHT IT, which is the part worth keeping.** D18 names five
enforcement sites: the rule itself, every image spec's content clause, the
word-list gate over dialogue and spoken lines, crowd generation, and the brand
bible. Every one of those is text or generation. Measured: `tools/canon-gate.py`
sets `CORPUS_ROOTS = ("content", "ledger/Assets/Scripts", "production/specs")`,
and `tools/content-gate.py` walks four named text sources (the dialogue banks,
the bark manifest, the tier-2 cards, the brand bible). Neither reaches
`ledger/Assets/Characters`. The only tool in this project that walks that
directory at all is `tools/attribution-check.py`, which reads licences rather
than content. **An ingested asset sits outside every content gate this project
has**, and that is a property of the enforcement design rather than an oversight
in any one tile.

Filed as a finding and nothing more, per CLAUDE.md rule 11. The research lane
proposes no queue item and edits no gate.

DENOMINATOR: 84 categories examined, 1 contradiction found, 0 of the project's
gates able to see it, 7 `.rejected` files opened by name rather than counted.
And it is not evidence that I looked hard enough: I read manifests, file names
and the picker, and I did not open 157 kit meshes or play a single clip.
