# Topic 4: how small teams reach photoreal on a budget

STATUS: SPEC (research delivery). Branch `research/photoreal-on-a-budget`, from
commit `074f85b`. Written 2026-09-14 by the research lane.

NOTHING IN THIS FILE IS AN INSTRUCTION. No queue item filed, no tile proposed,
no decision record written, no art commissioned.

## 0. How to read this file

Claim labels are CITED, DERIVED, ASSUMED and HOLE.

SOURCING LIMIT unchanged: no external page was read in full; every external
citation is the search channel's summary of a named page. Repository claims name
their file and line and were produced by commands run this session.

SCOPE, stated because three of my queue topics touch this ground. Topic 4 is
about TECHNIQUE: what small teams buy, what they fake, and what actually carries
a frame. Topic 16 is about MARKETPLACES (what asset packs cost and which are
worth it). Topic 17 is about FRAME TIME. Topic 23 is about what 1990 looked like
on FILM STOCK, which is a period question rather than a rendering one. Where
this file touches those it hands over rather than deciding.

## 1. Where the project actually is, because the advice has to land somewhere

Read from this repository this session, so that nothing below is generic:

- `production/ladder.md` makes rung 1 current: "The built Quay Street rendered
  from the SAME viewpoint as the lower panel of OUR OWN Hook sheet [...] with
  rain, a wet road, worn materials and sky, and you judging the two side by
  side. Your judgement is the gate; no number passes this rung."
- The inventory's tile "the street you walk" (partial): "The last probe run
  committed here wrote a street with no sky, and the road reads near white from
  its own albedo."
- The tile "weather and wet streets" (partial): "The last probe run committed
  here wrote no sky over the Unreal street, so nothing wet reaches it, which is
  queue 186 and why the sky comes before the wetness."
- D8 sets the bar as "photoreal wet overcast grimy Britain", with the Meridian
  Test as the instrument, and retires GTA V on PS3.
- `production/specs/vignette-scene.json` gives the street: 42.0 m, 6.0 m
  carriageway, 2.0 m footways, first floor at 3.4 m, eaves at 6.30 m.

So the live question is not "how do we get photoreal eventually". It is: **a
street with no sky and a too-bright road has to become a wet overcast British
street, judged by eye, against our own reference panel.** Everything below is
aimed at that.

## 2. The finding: for overcast, the sky IS the lighting, and we have not got one

CITED (search summaries of Epic's "Day Interior - Overcast: HDRI Backdrop"
tutorial, World of Level Design's UE5 HDRI guide and its "Create Overcast Day
Lighting with Sky Atmosphere" article): "HDRI lighting (also called Image-Based
Lighting) is one of the fastest ways to light exteriors realistically, and it
will light a scene, produce shadows, provide a background, and create
reflections." Overcast can be built from Sky Atmosphere, a Sky Light, or an HDRI,
and "overcast lighting scatters light in all directions and removes strong light
and shadows".

DERIVED, and it reframes the project's own sequencing note. The inventory says
"the sky comes before the wetness" and treats the missing sky as a blocker on
the WET pass. That is right, and it undersells it. In an overcast scene the sky
is not a backdrop that also lights things: **it is substantially the entire light
source.** A direct sun contributes almost nothing under full cloud; the
hemisphere does the work. So a street with no sky is not a street missing its
background. It is a street missing its lighting, which is also why "the road
reads near white from its own albedo" is the symptom you would predict: with no
sky contribution to grade against, exposure has nothing to sit on and material
albedo shows through raw.

**That makes the sky the single highest-leverage item on rung 1, ahead of
materials, props and wetness, and for a reason stronger than the ordering the
inventory currently gives.** Not a new task; a stronger argument for one that
already exists as queue 186.

## 3. The four things that carry a photoreal frame, in order of what they cost

### 3.1 Tonemapping, which is nearly free and does most of the work

CITED (search summaries of Evergine's post-processing documentation, Unity and
Unreal post-process guides, and Boris FX on chromatic aberration): tonemapping
"transforms rendered output by adjusting how colors and brightness values are
mapped, essentially making the image more closely resemble how cameras or film
capture light and color". The other effects are described as doing something
different: chromatic aberration "simulates the imperfections of real-world camera
lenses"; vignette "adds a dark border [...] often seen in images shot with
low-quality camera lenses"; film grain "adds texture that mimics old film
photography"; bloom "gives the impression of a bright, sunny day".

DERIVED, and it is the useful ranking: tonemapping is the only one of the five
that changes whether the image reads as PHOTOGRAPHED. The other four make an
already-photographic image read as shot on a particular KIND of camera. Both
matter for LEDGER, and they are different jobs with different owners: the first
is rendering and belongs to rung 1; the second is period look and belongs to
queue topic 23, where 1990 film stock is the question.

Worth recording that the project already has the second half and not obviously
the first. `ledger/Assets/Scripts/Game/FilmGrade.cs` exists in the Unity Game
layer, with a counter whose comment is exactly the project's habit ("an effect
that silently stops running looks exactly like one that is running and doing
nothing"), and the inventory records grain as "a live setting applied by
FilmGrade with no row on that screen". HOLE: I did not establish what the Unreal
probe's tonemapping and grading path is, only that the Unity one exists, and the
tile "visual identity in the Unreal build" is typed absent.

### 3.2 Overcast is the most forgiving light and the hardest to make good, and there is a named fix

CITED (search summary of The Gnomon Workshop's "Lighting Realistic Rainy Weather
in Unreal Engine 5" and the UE5 HDRI guides): "When lighting characters under an
overcast sky, you can add shape back in with Rect Light and Point Light fills
that serve as ambient bounce without flattening the diffused look."

DERIVED, and it is the counter-intuitive half of pillar 5. The pillar calls wet
overcast Britain "the most forgiving photorealism there is", and for MATERIALS
that is true: diffuse light hides the sins that a hard sun exposes. For SHAPE it
is the opposite. Removing directional light removes the thing that tells an eye
where a surface turns, which is why overcast reference photographs look flat and
overcast renders look like grey plastic. The named technique is to put small
directional fills back in where shape matters, without letting them read as sun.

This is worth having written down before rung 1 is judged, because the likely
failure mode of a correctly-lit overcast street is "it looks flat", and the
correct response to that is not more contrast in the grade.

### 3.3 Density without texture memory: trim sheets, tiling materials and decals

CITED (search summary of gamineai's "25 Free Environment Texture and Trim-Sheet
Sources for Indie Teams 2026"): "Environment art delays often occur when every
wall, floor edge, and modular prop needs its own material pass, and small teams
typically run out of clean, reusable surfaces rather than ideas." A trim-first
workflow "involves defining regions, describing materials, and instantly
generating a clean, consistent atlas ready for modular assets, props, and
environment kits".

CITED (search summaries of the Evermotion material-layering tutorial, cgguru's
Unreal dirt and wetness system, and an itch.io devlog on switching to vertex
painting): vertex painting "means you give a color to each of the vertices and
the material changes according to that color by layering and masking up to 4
different materials, 3 for RGB and one for black"; the devlog reports frame
rates going "from around 100 to above 130" with "much less texture memory usage"
after switching; and "for wear and tear, tileable detail materials blended via
masks in-engine, rather than baking unique grunge into every color map, saves
massive amounts of memory". CITED also: because vertex colours have four
channels, "you can pack multiple masks, with each channel carrying different
weathering effects like edge wear, dirt accumulation, and rust".

**THIS IS THE DIRECT LINK TO TOPIC 2 AND IT IS THE MOST ACTIONABLE THING IN THIS
FILE.** Topic 2 established that the hardware floor is a memory wall, that the
street's video memory has never been measured, and that my assumed 6 GB for it is
the load-bearing guess in the whole budget. Texture memory is the largest
controllable part of that number, and trim sheets plus in-engine blending are
the standard way to cut it. So the technique that makes a small team's street
look dense is the same technique that makes it fit on a 12 GB card. Two of my
topics recommending the same thing for different reasons has happened once
before in this queue (topics 1 and 2 both wanting Chatterbox Turbo) and it was
right then.

DERIVED and worth stating plainly: LEDGER's street is already generated from one
JSON file with nothing hand-placed, which is the ideal condition for a trim-sheet
workflow. A generator that emits geometry can emit UVs into a trim atlas and
vertex colours for wear as easily as it emits positions. A hand-built street
cannot be retrofitted this way cheaply; ours can, because it is a file.

HOLE: the 100-to-130 frame figure is one developer's devlog relayed by a search
summary, on an unnamed scene, on unnamed hardware. It is a direction, not a
measurement, and topic 17 is where ours would come from.

### 3.4 Real surfaces, free, from a phone

CITED (search summaries of StraySpark's "Photogrammetry for Indie Open Worlds:
RealityCapture, Polycam, and Luma in 2026", 3dmag and KIRI Engine's app
round-ups): "RealityScan from Epic Games is completely free on both iOS and
Android, including for commercial use, making it one of the only zero-cost
options with no export ceiling." Polycam's tiers are given as Free, Basic $30 a
month, Business $400 a year. Photogrammetry "usually beats depth-first capture
when the subject is a small, textured object and the goal is a detailed textured
asset [...] where you care less about room-scale depth sensing and more about
overlap, consistent lighting, and a clean textured-mesh output". And: "the
pipeline that took weeks per asset in 2018 takes hours per asset in 2026."

DERIVED, against this project's own constraints:

- **The licence position is unusually clean**, which matters because the
  allowlist is law. A surface captured on a phone is the project's own work,
  with no weights licence, no attribution chain and no ship-time re-verification.
  Compare the allowlist's current art routes, which all carry conditions: Fab
  purchases under the Fab Standard License, CC0 libraries, Objaverse "only with
  per-object license filtering".
- **What to capture is not British architecture, it is British SURFACES.** The
  atlas research already covers period form: clothing by occupation, hillside
  housing, household contents, a measured pub plan, transport timetables. What no
  research can supply is what forty years of rain does to a brick, a kerb, a
  painted shopfront or a rusted downpipe. Those are the surfaces pillar 5's
  "wet, overcast, grimy" is made of, and a phone in a wet northern-European
  street is a legitimate source for most of them.
- **HOLE, and a real one:** Jafar is in Switzerland, not Britain. Brick bond,
  kerb profile and shopfront proportion are British and not capturable there;
  weathered render, moss, rust, wet asphalt, peeling paint and concrete stain
  substantially are. Which of the atlas's surfaces are geography-independent is a
  question I cannot answer and an art lead can.

### 3.5 What the marketplace situation now is, because it changed

CITED (search summaries of the Epic Developer Community forum threads on
Megascans licensing after Fab, Quixel's own news post, and CG Channel): Megascans
was free to use in Unreal projects after Epic acquired Quixel in 2019; it was
free to all under Fab's Standard License "until the end of 2024"; and "in 2025,
Epic began charging for Megascans assets". Content acquired on Fab, free or paid,
"you can use it forever".

The allowlist already reflects the current world correctly: "Fab purchases under
the Fab Standard License" and "CC0 libraries (Poly Haven, ambientCG, Sketchfab
CC0 filter)". No change is needed there and I am recording it only because "just
use Megascans, it is free with Unreal" is advice that was true for five years and
is no longer, and it will be offered by somebody.

CONTESTED AND NOT RESOLVED: one summary says "As of 2026, assets on Fab are free
to use under the Fab Standard License", which reads as contradicting the 2025
charging change. The most likely reading is that FREE assets on Fab carry the
Standard License, not that all assets are free. I could not open the page to
check and have not relied on it.

## 4. What I would actually do, if it were mine to say

It is not, and this is a recommendation and not a plan.

1. **The sky, and treat it as lighting rather than background** (section 2). It
   is queue 186 already; the argument for its priority is stronger than the one
   currently written down.
2. **Check what the Unreal probe's tonemapper is doing before adding any grade
   on top of it** (3.1). Grain, aberration and vignette on an untonemapped image
   make it look like a bad photograph rather than a photograph.
3. **Expect flat, and know the fix is fills and not contrast** (3.2).
4. **Put wear in vertex channels and surfaces in a trim atlas, while the street
   is still a generator** (3.3). This is the one with a second payoff in topic
   2's memory budget, and the window for doing it cheaply is open precisely
   because nothing is hand-placed yet.
5. **Try one phone capture, end to end, and see what it costs in hours**
   (3.4). RealityScan is free and commercial-safe, so the experiment has no
   licence overhead, and one wet kerb through the whole pipeline would answer
   more than any amount of reading.

## 5. What could not be established

1. **What the Unreal probe's post-processing chain is.** I established that
   Unity has `FilmGrade.cs` and that the tile "visual identity in the Unreal
   build" is typed absent. I did not read the probe's rendering setup, and every
   section 3.1 recommendation is therefore aimed at a chain I have not seen.
2. **Any solo-developer postmortem with real numbers** on what buying assets
   saved. My search returned forum posts and checklists and no measured
   postmortem. Queue topics 16 and 18 are where that belongs and this file does
   not pre-empt them.
3. **The 100-to-130 frame claim**, which is one devlog relayed by a summary.
4. **Whether Fab's free tier means what one summary says it means** (3.5).
5. **Which of the atlas's surfaces are capturable outside Britain** (3.4).
6. **Any measurement of our own street's texture memory**, which is topic 2's
   named hole and topic 17's first job.
7. **Not covered:** characters and faces, which are MetaHuman and Mixamo by the
   allowlist and a different problem; vegetation, of which a port town has
   little; and interiors, which D14 rules are authored layouts.

## 6. Sources

Search channel summaries, retrieved 2026-09-14; none read in full.

- Epic Developer Community, "Day Interior - Overcast: HDRI Backdrop for Overcast or Purely Indirect Light", https://dev.epicgames.com/community/learning/tutorials/wdZ/unreal-engine-day-interior-overcast-hdri-backdrop-for-overcast-or-purely-indirect-light
- Epic, "Post Process Effects in Unreal Engine", https://dev.epicgames.com/documentation/en-us/unreal-engine/post-process-effects-in-unreal-engine
- World of Level Design, "UE5: Guide to Using HDRI Lighting", https://www.worldofleveldesign.com/store/ue5-hdri-lighting.php
- World of Level Design, "UE4: Create Overcast Day Lighting with Sky Atmosphere", https://www.worldofleveldesign.com/categories/ue4/overcast-lighting-sky-atmosphere.php
- The Gnomon Workshop, "Lighting Realistic Rainy Weather in Unreal Engine 5", https://www.thegnomonworkshop.com/workshops/lighting-realistic-rainy-weather-in-unreal-engine-5
- Evergine documentation, "Tonemapping, Chromatic Aberration, Vignette, Grain, Distortion", https://docs.evergine.com/2024.6.28/manual/graphics/postprocessing_graph/default_postprocessing_graph/tonemapping.html
- Boris FX, "What is Chromatic Aberration in Games", https://borisfx.com/blog/what-is-chromatic-aberration-in-games/
- Wayline, "Unity Post-Processing Effects: Enhancing Visuals", https://www.wayline.io/blog/unity-post-processing-effects-enhancing-visuals
- gamineai, "25 Free Environment Texture and Trim-Sheet Sources for Indie Teams 2026, License-Checked Edition", https://gamineai.com/blog/25-free-environment-texture-and-trim-sheet-sources-for-indie-teams-2026-license-checked-edition
- Evermotion, "Material Layering in Unreal Engine", https://evermotion.org/tutorials/show/13180/material-layering-in-unreal-engine
- CG Guru, "Unreal material dirt and wetness system", https://www.cgguru.com/unreal-material-dirt-and-wetness-system
- StraySpark, "Procedural Weathering in Blender with Geometry Nodes: Edge Wear, Rust, and Dirt", https://www.strayspark.studio/blog/procedural-weathering-blender-geometry-nodes
- Mad Hat Game Studios devlog, "switch to vertex painting", https://madhatgamestudios.itch.io/rebirth/devlog/62601/switch-to-vertex-painting
- StraySpark, "Photogrammetry for Indie Open Worlds: RealityCapture, Polycam, and Luma in 2026", https://www.strayspark.studio/blog/photogrammetry-indie-open-worlds-2026
- 3dmag, "Best 3D Scanner Apps in 2026: LiDAR, AI and More Compared", https://www.3dmag.com/3d-scanners/best-3d-scanning-apps/
- KIRI Engine, "Best LiDAR 3D Scanner Apps for iPhone (2026)", https://www.kiriengine.app/blog/best-lidar-3d-scanner-apps-iphone-2026
- Epic Developer Community Forums, "Question about megascans license after fab launch", https://forums.unrealengine.com/t/question-about-megascans-license-after-fab-launch/2026269
- Quixel, "Quixel on Fab: New Megascans and Megaplants", https://quixel.com/news/quixel-on-fab-new-megascans-and-megaplants
- Quixel, license page, https://quixel.com/license
- CG Channel, "Epic has made Megascans free to all, but only until the end of 2024", https://www.cgchannel.com/2024/10/epic-games-has-made-megascans-free-to-all-but-only-until-the-end-of-2024/
- RMCAD, "Environment Artist Playbook: From Blockout to Final Pass", https://www.rmcad.edu/blog/environment-artist-playbook-from-blockout-to-final-pass/
- Epic Developer Community Forums, "I Started With Zero Game-Dev Experience, Now I'm Building This Photoreal Survival Game Solo in UE5", https://forums.unrealengine.com/t/i-started-with-zero-game-dev-experience-now-im-building-this-photoreal-survival-game-solo-in-ue5/2746708

Repository sources, read this session at commit `074f85b`:
`production/ladder.md`, `production/specs/vignette-scene.json`,
`production/systems-inventory.json`,
`ledger-v2/respec/decision-register/D8-visual-bar.md`,
`ledger-v2/research/license-allowlist.md`,
`ledger-v2/respec/vision-pillars-v2.md`,
`ledger/Assets/Scripts/Game/FilmGrade.cs`,
`production/art/atlas-02/research/` (file listing).
