# 5. Definition of done, for every kind of asset

An asset is **done** only when every line of the common list and every line for its kind is true and shown. Until then it is "in progress". A big item (a family's proof, the proof view) is "ready for review" until an independent review passes it (CLAUDE.md). Clothes on people, faces, voices and whole street frames also need Jafar's yes on his page.

The checks marked **[auto]** can be scripted. The asset audit proposed in 4-BUDGETS.md, 4.8 does the numbers; `approvals.py`, `attribution-check.py`, `canon-gate.py` and `names-gate.py` already exist. The rest is the gate's eye.

## Sources for the list

- **Epic's engine side** [R, 3 Oct, UE 5.8 pages]: type prefixes (SM_, SK_, M_, MI_, T_); 1 unit = 1 cm; LODs each about half the last; collision by name (UCX_ and the rest), at most 10 hulls; textures powers of two, 2K or less, with mips; Data Validation on save and in the build.
- **Keith's "Defining Done"**, "appropriately named and fit within budgets" [SS; the page UNREACHED].
- **LEDGER's own rules:** the gate; tools/approvals.py; THIRD-PARTY.md; the NoAI ruling (3 Oct); git holds text and small files only (3 Oct); handovers name the exact version (30 Sep); nothing reaches his page with a visible fault (2 Oct).

## The common list (every asset)

| # | Done when | Check |
|---|---|---|
| C1 | **In the game.** Placed by data (a spec or placement list, not by hand in the editor). Seen in the **packaged** build on his PC. Walked past by the AI tester on its route. | the packaged build; the tester's run |
| C2 | **Named and scaled.** Epic's prefix and the project's id; 1 unit = 1 cm; pivot where it stands; on the kit's grid where it has one. | [auto] |
| C3 | **Distance versions.** The LOD chain for its kind (4-BUDGETS.md, 4.7), each about half the last, with switch distances set. A merged distance version where its kind has one. No visible pop at walking pace, checked in a walking film by day and night. | [auto] counts; the eye for pop |
| C4 | **Collision.** As its kind says: simple shapes, at most 10 hulls. Nothing traps the player: the AI tester's walk, as at Rita's pavement on 30 Sep. The camera neither passes through it nor snaps on it. | the tester's walk; [auto] hull count |
| C5 | **Inside budget.** Triangles, materials, texture sizes and memory within its kind's line in 4-BUDGETS.md. The build's performance step shows no regression past the family's share. | [auto] audit; the perf step |
| C6 | **Source and licence recorded.** A THIRD-PARTY.md row (source and link, licence, date fetched, author, credit text if required) **and the NoAI status read at download**. Or, for our own work, the recipe path and seed beside it (tools/art-recipes/...). On the allowlist. No real brand, model or person: the canon gate and names gate pass. | [auto] attribution-check, canon-gate, names-gate; NoAI by reading |
| C7 | **Judged against its bar.** First by the builder, against dated photographs and the Hook sheet or KCD2 frames, in the game's own camera and exposure at 2560×1440, by day and at night, wet. Then by a fresh reviewer who did not see it made. Small assets end there; people, whole street frames and light go to his page. Clothes are judged against their floor, not the sheet: passers-by at 8 m, the people Tom talks to close. | the gate; his page |
| C8 | **Approval recorded.** An approval file beside it (tools/approvals.py) naming what it was judged against, so it lapses when that changes. Listed in production/specs/in-game.json. | [auto] approvals.py (today 8 of 8 placed things lack a current approval) |
| C9 | **No visible fault.** No placeholder, test chart, debug object, hole, float or sink over 1 cm, z-fighting, stretched texture or wrong scale. Checked by a fresh reviewer frame by frame (rule of 2 Oct). | the gate |
| C10 | **Wet and lit.** Responds to the street's wetness where it stands outdoors. Correct by day and at night under the game's own exposure. | the eye |
| C11 | **Stored right.** Source text and small files in git; meshes, renders and audio on F: under retention, with a hold if it must outlive its limit. git-size-guard passes. | [auto] |
| C12 | **Versioned.** Any handover about it names the exact file or take (MH_LenaS4, not "Sheila"), checked current by the receiver. | the handover line |

## Per kind

| Kind | Also done when |
|---|---|
| **Building and frontage** | On the kit's grid. Brick bond right for its age: Flemish or English garden-wall for a Victorian solid wall, not stretcher bond. Trims from the shared sheets. Reveals of 100–115 mm that read as shadow. Sills with a drip. Windows with a room (real or mapped), nets and a night state by the town's hours. Wear by rule from its seed. No visible repeat at the near corner at 2560×1440. Its hill version comes from the same kit. Collision on walls, plinths and steps. Doors either open or plainly shut. |
| **Interior and room behind glass** | The trade of his ruling (3 Oct). A real room where seen at 1–3 m, a mapped room beyond. Lit by day and at night by the shop's hours. Glass with front-layer reflection. Goods scanned or CC0, never made in code. The display inside its budget: the pawnbroker's display is today 203,355 triangles and 48 materials against ≤ 60,000 and ≤ 8. If walked into: the camera passes P15's test. |
| **Street furniture and props** | Sits on the ground. Two to four material states with wear. Placed by rule. A 1990 British type, checked against a dated photograph. Marks and cyphers from canon's minted names, never real ones. Interactive props block the player and the camera. |
| **Food and shop goods** | From allowed scans (CC0, tags read for NoAI) or our own Blender work. Piles from the generator (3–6 distinct pieces). Nothing the content rule bars (no alcohol, no gambling: no pools coupons, D18). Judged at 1–3 m beside Rita's. |
| **Signage, posters, text** | Every word is our own text layer in an OFL font, spelled right (read back from the render). Names minted by canon. The content gate passes. Aged by its wall's seed. Never words drawn by the image model. |
| **Car** | Fictional: passes the asset plan's blind test (no model named with confidence; placed in Britain or Europe, 1985–91). Badge illegible at game distance. A 1990 plate format with an invented registration. Paint from the shared car-paint master, wet. Stance checked first. Simple collision. Parked by rule, never on the pavement line people walk. Until a car passes, the street has none (2 Oct). |
| **Person (principal, regular, passer-by)** | A face from its casting sheet, approved and frozen (people are his). The body built for that person (the build re-rigged in the same session). The LOD chain, and hair cards beyond the nearest few. An idle set and a walk with planted feet, out of step with others. Contact shadows. Lit in passing, not only in conversation. A voice approved by ear (only those who speak). **In the town's simulation** if seen in the street (D25: everyone perceives, remembers and gossips), or declared scenery by his ruling. |
| **Clothes** | Fitted to the exact body version (MH_LenaS4, not "Sheila"). Skinned; only loose parts simulated. Deformation shown walking, sitting and with arms raised, with no clipping at any LOD. Plain and period-plausible, with no modern giveaway (contrast stitching, trainers). Fabric from CC0 or our own. Judged at 8 m for passers-by, close for principals. |
| **Hair** | From the MetaHuman plugin's library or our own work (Fab grooms are NoAI). A period cut for the sheet. Cards at distance. |
| **Vegetation** | Placed by rule where water and neglect put it. Masked leaves kept small on screen (overdraw inside the budget). Wind subtle. |
| **Sound** | CC0 (D26), each file's source recorded and the site's AI terms read. Placed in space. Judged by his ear (D42). |

## What could not be verified

- **Whether Epic's Data Validation** can carry this project's checks without new code [R: it can check names and budgets; the effort here is unmeasured].
- **Whether the pop at walking pace** can be judged from the build machine's films alone.
