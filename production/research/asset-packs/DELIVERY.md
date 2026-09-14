# Topic 16: asset packs, what they cost, and what buying actually saves

STATUS: SPEC (research delivery). Branch `research/asset-packs`, from commit
`074f85b`. Written 2026-09-14 by the research lane.

NOTHING IN THIS FILE IS AN INSTRUCTION. No purchase is proposed, no queue item
filed, no tile proposed, no decision record written. D6 reserves the spend
decision to Jafar and nothing here changes that.

## 0. How to read this file

Claim labels are CITED, DERIVED, ASSUMED and HOLE. Sourcing limit unchanged.
Repository claims name their file and line.

Most of this topic's evidence turned out to be in our own specs rather than on
the web, which is why sections 2 and 3 are longer than section 1.

## 1. The market, and one real price

CITED (search summaries of Vagon's marketplace round-up, Epic's own Fab launch
post and the 2026 marketplace guides): Epic merged the Unreal Marketplace,
ArtStation and Sketchfab into Fab in 2024; "as of early 2026, Fab lists well over
30,000 Unreal-compatible products"; and for indies the received wisdom is that
"for most projects under $50,000 in art budget, the Marketplace beats
commissioning custom work on cost and speed."

CITED, and it is the only hard price I could get: the British City Pack by
PolySphere Studio is **$169.99 regular, listed at $118.99 with a 30 percent
discount**, with "over 600 unique meshes", blueprints, five Niagara systems, and
a project size of about 4.5 GB. Detail from the listing: 646 static meshes, 10
master materials, 337 material instances, 333 textures, 11 blueprints.

Against `ledger-v2/respec/decision-register/D6-spend.md`: "roughly 50 to 150 per
month average, 300 to 700 one-off in year one, targeted precisely at the two
named gaps: the CC0 asset ceiling (paid vehicle, interior and clothing packs when
the milestone hits the ceiling) and faces."

DERIVED: one pack of that class is one to three months of the monthly average, or
a quarter to a half of the whole year-one one-off allowance. **So this is not a
question of whether we can afford a pack. It is a question of whether one pack is
worth a quarter of the year's discretionary art money**, and sections 2 and 3 are
why I think the answer for the packs that exist is no.

## 2. The two disqualifiers, both from our own files

### 2.1 The packs are the right country and the wrong decade

CITED: British packs exist and are good. The British City Pack is "high-quality
realistic assets to build a realistic and immersive British/London/UK/European
cityscape". "London - British Environment" offers "scan-based British streets [...]
over 1,500 assets", built from photogrammetry "captured on location" at London's
Seven Dials. There is also a "British Street Asset Pack" and a "UK Urban Props"
blueprint pack.

CITED, from the same search, stated by the search channel itself: "the search
results do not specifically indicate assets targeting the 1980s-1990s aesthetic
or period vehicles."

DERIVED: photogrammetry captured on location in the 2020s is, by construction,
a 2020s street. And our own scene spec names the failure mode with a precision
nobody would guess:

`production/specs/vignette-scene.json`, on the period: "Late analog Britain.
Landlines, cash, paper. **Nothing on this street may imply a mobile phone, the
internet, a wheeled refuse bin, or blister tactile paving**, whose introduction
date is unverified and which the BOM excludes for that reason."

A modern British city pack is full of wheeled refuse bins. And blister tactile
paving. And uPVC, and modern signage, and satellite dishes, and double glazing.
The cost of a pack is therefore not its price, it is the audit: 646 meshes, each
of which has to be checked against a period rule, and the ones that fail are
either deleted or reworked.

**HOLE, and it is the number I most want and could not get: what share of a
modern British pack is period-safe.** Somebody with the pack open could answer it
in an afternoon. My guess is not worth writing down.

### 2.2 Canon forbids the thing D6 earmarked money for first

`canon.md`, under Brands and law: "Every brand, band, club, product, weapon and
vehicle is fictional. No real people, voices, logos, lyrics, **car models**."

D6 names "paid vehicle, interior and clothing packs" as the first target for
money.

And our own bill of materials already caught this. Read this session,
`production/specs/vignette-bill-of-materials.json`, line `F4_parked_vehicle`:
"One parked period British car, boxy hatchback or estate", certainty
NEEDS-CHECKING, and the note: "Largest quality risk on the list if included. The
vignette can be shot without a vehicle and probably should be for the first pair.
**canon also forbids real car models, so a recognisable real shape is a canon
violation**."

DERIVED: a period British vehicle pack is, necessarily, a pack of recognisable
period British cars. That is what makes it a period British vehicle pack. So the
first thing D6's money was earmarked for is substantially blocked by canon rather
than by budget, and the BOM had already noticed.

This does not close the question, because a vehicle pack could be bought and
kit-bashed into something unrecognisable. It does mean the purchase does not buy
what it looks like it buys.

## 3. What the built street actually needs bought, with its denominator

This is the most useful thing in the file and it comes entirely from reading
`production/specs/vignette-bill-of-materials.json`.

The BOM's own route vocabulary:

| Route | Its own definition | Count |
|---|---|---|
| `HAVE` | "the bytes are in this repository now, licensed and attributed" | 33 |
| `GENERATE` | "no library route; made here" | 33 |
| `ENGINE` | "not an asset at all; a renderer feature" | 6 |
| `FETCH` | "a free allowlisted library is the candidate route" | 5 |
| `BLOCKED` | "needs a decision from Jafar (a purchase, an account, a hardware buy)" | **1** |
| | | **78** |

**One line in seventy-eight is a purchase decision**, and it is
`F2_period_wardrobe`: "Clothing that reads as 1988 to 1992 Britain rather than
contemporary casual." Its own note says the decision "is Jafar's about where the
character pipeline goes, not about money", and recommends not blocking on it.

The five `FETCH` lines are all surfaces from free allowlisted libraries, and two
of them carry honest doubt: `C4_render_pebbledash` notes "I have not looked at
ambientCG's catalogue for a pebbledash set and will not claim one exists", and
`C10_roller_shutter` is "mandatory because the night condition needs at least one
shut unit, and an open lit shopfront at 2am is the wrong picture."

**DERIVED, and it is the answer to the brief's question.** On the street that
exists, buying saves essentially nothing, because the pipeline was built so the
street composes itself from primitives. Thirty-three of seventy-eight lines are
`GENERATE` with `make_by` of `PROC`, defined as "composed from primitives by the
scene generator from the shared JSON. No tool needed beyond the generator D1b
requires anyway. **Zero cost.**"

### 3.1 And the generator law makes a pack awkward in a way price does not capture

`production/specs/vignette-scene.json` states its own law: "**THIS FILE IS THE
SCENE.** Every object in either engine arrives via that engine's generator
reading THIS file. A hand-placed object, a hand-edited binary scene or a
hand-edited uasset disqualifies the still as D1b evidence, so a dimension that is
not here may not be invented in an emitter."

DERIVED: an asset pack is a set of meshes AND a way of using them, which is
placing them by hand. Our law forbids the second half. So a pack can supply
MESHES that the generator places against dimensions in the scene file; it cannot
supply a scene, a kit-bash, or a demo level. That halves what a pack is worth and
it is not a criticism of either the pack or the law, it is a structural fact
about the fit.

It also means the useful purchase shape for us is narrower and cheaper than a
600-mesh environment pack: **individual objects the generator can place**, which
is what `HAVE` and `FETCH` already deliver for free.

## 4. What the literature says the hidden costs are, which agrees

CITED (search summaries of Game World Observer's "Buying ready-made 3D assets for
your game", 3DSkillUp's buying checklist and its piece on visual style, and the
Juego Studio outsourcing guide): "a render-ready model may look excellent offline
while still requiring retopology, UV work, texture conversion, or material
rebuilding before use in a game"; "hidden rework, inconsistent topology, and
delayed integration inflate the total cost far beyond the original quote"; "the
model's rendered image on the site doesn't allow you to consider all potential
problems"; and "an incompatible silhouette or proportion system affects the asset
from every angle".

DERIVED, and it is a fourth disqualifier specific to us: our street has published
dimensions. `vignette-scene.json` fixes a 6.0 m bay, an 8.0 m carcass depth, a
3.4 m ground storey, a 2.0 m footway, a 0.125 m kerb upstand and a 0.915 m kerb
block. A bought pack has its own proportion system, and "incompatible silhouette
or proportion system affects the asset from every angle" is exactly what would
happen to a pack building dropped next to a generated terrace built to British
trade standards.

## 5. Where buying probably IS worth it

Honesty requires this section, because sections 2 to 4 are all negative.

1. **Clothing** (`F2_period_wardrobe`), the one BLOCKED line, and the one thing
   the generator cannot compose from primitives. It is also the thing D6 names
   and the thing topic 4's phone-photogrammetry route cannot supply.
2. **Faces**, which D6 names separately and D2 rules, and which is a rig-source
   decision rather than a pack.
3. **Interiors**, when D14's authored interiors start, because a room's contents
   are hundreds of small distinct objects and that is precisely where a pack's
   economics are best and where our generator's economics are worst.
4. **Middleware and tools rather than art.** The literature's own note is that
   "professional game studios buy middleware, license engines, and use asset
   libraries constantly", and the coverage audit found the tooling gap (Articy
   froze on Disco Elysium's script). A tool purchase does not have a period
   problem, a canon problem or a proportion problem.

## 6. Findings

1. **One real price: $169.99 list, $118.99 discounted, for 646 meshes**, which is
   a quarter to a half of D6's year-one one-off allowance (1).
2. **The packs are the right country and the wrong decade**, and our own scene
   file names the tell: a wheeled refuse bin (2.1).
3. **Canon forbids recognisable car models, which is what a period vehicle pack
   is made of**, and the BOM already caught it (2.2).
4. **One line in seventy-eight is a purchase decision** (3), and 33 of 78 are
   generated from primitives at zero cost.
5. **The generator law means a pack can sell us meshes but not a scene** (3.1).
6. **Our published dimensions make proportion mismatch a first-order risk** (4).
7. **The good purchases are clothing, faces, interiors later, and tools** (5).

## 7. What could not be established

1. **What share of a modern British pack is period-safe** (2.1). The most useful
   number in this topic and I could not get it. An afternoon with the pack open
   answers it.
2. **Prices for anything except the British City Pack.** `fab.com` is not
   fetchable from here and the search summaries return feature lists. For a topic
   titled "what they cost" that is a real limitation and it is why section 1 is
   short.
3. **Whether any period-correct British 1988-1992 pack exists at all.** I looked
   and found none; I cannot distinguish that from not finding it.
4. **What the interiors bill will look like**, which is where section 5's
   strongest case lives and which D14 has not produced yet.
5. **Whether a vehicle pack could be kit-bashed unrecognisable cheaply enough**
   to satisfy canon (2.2). That is an art judgement.
6. **Not covered:** audio packs, which have a different licence surface; the
   free tiers and monthly giveaways, which the sources mention and which are the
   obvious first thing to exhaust; and Reallusion's Character Creator, already on
   the allowlist and relevant to section 5's clothing line.

## 8. Sources

Search channel summaries, retrieved 2026-09-14; none read in full.

- Fab, "British - City Pack", https://www.fab.com/listings/cd93dec3-bb73-4a5e-b621-e420d66b1eb6
- 80.lv, "A New Asset Pack for Creating British Cities in Unreal Engine 5", https://80.lv/articles/a-new-asset-pack-for-creating-british-cities-in-unreal-enigne-5 (EGRESS BLOCKED)
- Fab, "London - British Environment", https://www.fab.com/listings/e714ec2e-e31a-4390-a666-abee93c8d579
- Fab, "British Street Asset Pack", https://www.fab.com/listings/8c9feafc-de83-4127-b901-a7e2c49a829b
- Unreal Marketplace, "UK Urban Props (Blueprint)", https://www.unrealengine.com/marketplace/en-US/product/uk-urban-props
- Epic, "Fab, Epic's New Unified Content Marketplace, Launches Today", https://www.unrealengine.com/en-US/blog/fab-epics-new-unified-content-marketplace-launches-today
- Vagon, "Best Marketplaces for Unreal Engine Assets and Plugins in 2026", https://vagon.io/blog/best-marketplaces-for-unreal-engine-assets-and-plugins
- Practice Test Geeks, "Unreal Engine Marketplace 2026 August Guide", https://practicetestgeeks.com/unreal/unreal-engine-marketplace
- Epic, "Free Epic Games Content for Unreal Engine", https://dev.epicgames.com/documentation/unreal-engine/free-epic-games-content-for-unreal-engine
- Game World Observer, "Buying ready-made 3D assets for your game, a time saver or a waste of money?", https://gameworldobserver.com/2023/01/13/ready-made-3d-assets-in-game-development-pros-cons-belka-games/
- 3DSkillUp, "3D Asset Buying Checklist: What to Check Before You Download", https://3dskillup.art/3d-asset-buying-checklist/
- 3DSkillUp, "How to Choose Game Assets That Match Your Visual Style", https://3dskillup.art/how-to-choose-game-assets-visual-style/
- Juego Studio, "3D Game Art Outsourcing in 2026: Costs, Execution Models and Partner Evaluation", https://www.juegostudio.com/blog/3d-game-art-outsourcing-costs-studios
- CG Channel, "Get 50+ free assets for building a city scene in Unreal Engine", https://www.cgchannel.com/2025/05/get-50-free-modular-assets-for-building-an-alley-in-unreal-engine/

Repository sources, read this session at commit `074f85b`:
`production/specs/vignette-bill-of-materials.json` (the `route_values` and
`make_by_values` blocks and all 78 routed lines, counted this session),
`production/specs/vignette-scene.json` (the law, the period note and the
dimensions), `canon.md` (Brands and law),
`ledger-v2/respec/decision-register/D6-spend.md`,
`ledger-v2/research/license-allowlist.md`, `production/systems-inventory.json`.
