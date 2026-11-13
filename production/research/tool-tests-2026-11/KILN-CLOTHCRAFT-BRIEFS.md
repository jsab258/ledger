# ClothCraft porting briefs for DrapeStudio, Seamshift and Loomwright (13 Nov 2026)

Method researched: ClothCraft repository (github.com/erythrofr/ClothCraft, main at 8 Nov 2026), read by the advisor; text received through the advisor channel 13 Nov 16:40 (advisor 151).

Full text of https://claude.ai/artifact/DMSWtYf5MnqSZcpZckqNuy, sent through the advisor channel because the builder's docs connector could not read it. Since 13:43 these briefs feed Kiln: Brief 1 = the drape engine and the front end, Brief 2 = fit and rig (Seamshift as base), Brief 3 = what Kiln's cloth must do better than Loomwright's, and the shared checks for all of Kiln.

## How to use this

Hand this document and the repository erythrofr/ClothCraft (https://github.com/erythrofr/ClothCraft) to whoever builds the tools. ClothCraft is written in Rust like all three tools and is MIT-licensed, so its code can be copied in directly, with its licence notice kept.

- Who it is for: the person or AI agent that writes the tools. Each brief names the files to open in ClothCraft.
- Order to port in: the start check and the contact method first (they fix the layering and poke-through faults shared by all three tools), then the checks and test fixtures, then everything else.
- How each fix is proven: every brief ends with an acceptance test. The LEDGER builder reruns that test with the same bodies, garments and measuring script as before, and reports the numbers beside the previous round.
- What ClothCraft is not: a finished tool. Its own README calls it a research prototype. Take its contact, solver and test methods; leave its editor.

## What ClothCraft is, and what to take

ClothCraft (Cargo package marvelous-cloth, MIT, about 58,000 lines of Rust, 218 commits to 8 Nov 2026) is a pattern editor and cloth simulator whose real value is its contact handling and its evidence discipline.

| Part | What it does | Where in the repository | Take it? |
|---|---|---|---|
| Offset Geometric Contact (OGC) | Cloth against body and cloth against cloth, vertex-face in both directions plus edge-edge, with a movement bound per vertex each step so no point can cross a surface. Independent Rust implementation of Chen et al., SIGGRAPH 2025 (https://graphics.cs.utah.edu/research/projects/ogc/) | src/ogc/ (world.rs 1,073 lines; geometry, bvh, candidates, potential, directional) and docs/ogc.md | Yes: the core fix for poke-through and layering |
| Start check | Refuses to simulate if any two faces intersect or touch at the start ("reset/rearrange before simulating") | OgcWorld::validate_start, src/ogc/world.rs line 392; check_vbd_initialization in src/avatar/diagnostics.rs | Yes: OGC only keeps a separated start separated |
| Vertex Block Descent (VBD) solver | Stable implicit cloth solver, vertex by vertex in colour groups, seams as energy terms; optional GPU candidate search | src/vbd.rs, src/vbd/ (local_step, coloring, seam_blocks, prediction); src/gpu_vbd.rs | Yes, where a tool uses one-substep XPBD |
| Sewing | Whole, partial and multi-edge seams, explicit easing for unequal lengths, seam gap as a penalty energy | src/garment/seam.rs, src/vbd/seam_blocks.rs, docs/documents-and-sewing.md, docs/elastic-seams.md | Yes, the model and its tests |
| Body mesh inspection | Open, non-manifold and flipped edges, duplicate faces, a fingerprint of the body used | src/avatar/diagnostics.rs, docs/avatar-diagnostics.md | Yes |
| Measures | Stretch as area-weighted 95th percentile and maximum; energy accounting per step | src/garment/diagnostics.rs, src/vbd/audit.rs | Yes |
| Test fixtures | A headless settling zoo with negative controls, continuation runs and a measurement contract | examples/settling_zoo.rs, docs/settling-zoo.md; 52 validation JSON files beside 114 notes in docs/ | Yes |
| Fabric presets | Mass, thickness and stretch from published measured data (MIT material-properties dataset; Wang et al. 2011) | src/fabrics.rs, docs/fabrics.md | As a starting point |
| Formats | Body in: OBJ, glTF, GLB (static). Garment out: OBJ with UVs. Patterns in: DXF and SVG subsets | src/avatar_import.rs, src/gltf_avatar.rs, src/garment/export.rs, dxf_import.rs, svg_import.rs | Body import yes; no FBX, no skinning |
| Editor (atelier, board, selection) | The window and its tools | src/atelier/, src/editor.rs | No |

- Speed it reports: a draped garment of 6,731 vertices and 12,682 triangles at 1/60 s and 16 iterations ran at 14.76 ms a step over 1,800 steps, bitwise repeatable (docs/draped-realtime.md, 16 Oct; hybrid GPU path, the author's NVIDIA card).
- Layers: no special layer feature. Several panels in one garment collide through the same self-contact, so a jacket over a jumper is one cloth system with self-contact. Copy that model.
- Its own open problems (README, 8 Nov): residual jitter at rest, cost on dense meshes, friction, seam treatment, measured material calibration.
- Licence: MIT. Keep the copyright notice in any copied file and in the credits.

## Brief 1: DrapeStudio (the Marvelous replacement; in Kiln: front end and drape engine)

Layering is the blocker: the jumper comes through the jacket. Port OGC contact and the start check first; they address faults 1 and 2 together. Numbers from the 11 Nov round on Tom's MetaHuman body (the 13 Nov re-test found the program unchanged; its final version of 13 Nov 14:45 is being tested now).

| # | Fault | Our numbers (11 Nov) | What to take from ClothCraft | Files to read |
|---|---|---|---|---|
| 1 | Jacket over the jumper: the jumper comes through at shoulders, chest, sleeves and the front | 2,006 jumper points through the jacket; 68 min for the layer job against 587 s for the jacket alone | OGC contact between all cloth, with the frozen jumper as a fixed collision surface (OGC keeps cloth and fixed surfaces in separate trees) or both garments in one system with self-contact; the start check refuses a jacket placed inside the jumper | src/ogc/world.rs (validate_start line 392, detect), src/ogc/bvh.rs, src/ogc/directional.rs, docs/ogc.md |
| 2 | The arm pokes through the upper sleeve; its check passes | Body through 158 (sleeves 142) against Marvelous's 103 | Edge-edge contact against the body; movement bounds per vertex | src/ogc/world.rs, src/ogc/primitive_distance.rs, src/vbd/local_step.rs |
| 3 | Cuffs bunch into rings while its check says ok | Worst edge 6.05x; check passes while 1% of edges are over | Stretch per piece as 95th percentile AND maximum; fail on the maximum | src/garment/diagnostics.rs (extension_percent) |
| 4 | Slow | Jumper 246 s against 124 s; jacket 587 s against 102 s; jeans 226 s against 86 s | VBD in colour groups, cached contact candidates, optional GPU search; stop when still | src/vbd.rs, src/vbd/coloring.rs, src/ogc/candidates.rs, src/ogc/incidence.rs, docs/draped-realtime.md |
| 5 | Jeans waistband 2 cm high, stands off at the hips | 1,074 to 1,141 mm against Marvelous's 1,066 to 1,120 | Fabric presets from measured mass, thickness and stretch under a reference pull (100 N/m); seam easing for the waistband | src/fabrics.rs (stiffness_for_extension), docs/fabrics.md, src/garment/seam.rs |
| 6 | "Auto" seam direction breaks the waistband | Seam gap 29.6 mm, 4,596 edges over 1.2x | Seam direction always explicit, never inferred | docs/documents-and-sewing.md |
| 7 | Pattern import takes FreeSewing's marks as pieces, loses names | 14 pieces in, 3 real | Reject unsupported artwork and nested or overlapping outlines; preview units and layers | src/garment/svg_import.rs, src/garment/dxf_import.rs, docs/svg-import.md |

Acceptance test: (1) jacket over jumper: no jumper visible through the jacket from front, side and back cameras; jacket cloth under the jumper's surface counted from the camera, target 0. (2) Jacket alone: body through at or below Marvelous's 103, none in the upper sleeves. (3) Jumper cuffs: worst edge at or below Marvelous's, no ring by eye. (4) Time at or below 1.5x Marvelous per garment. (5) Jeans waistband within 5 mm of Marvelous's height, lying on the hips. (6) Same result twice; its own check fails a garment that fails ours.

## Brief 2: Seamshift (the MetaTailor replacement; in Kiln: the base, fit and rig)

What remains comes from pushing cloth out of the body point by point after the refit. The fix ClothCraft offers is one step: after the shape carry, a short relaxation with real cloth energies (stretch, bending, seams) and OGC contact against the body and lower layers, in the rest pose and each test pose. Membrane energy keeps bands at length, bending smooths ragged edges, OGC keeps layers apart without crossing. Numbers updated to round 4 (13 Nov) where known; note the "heavy" test body was identical to the average one (advisor 148).

| # | Fault still open | Our numbers | What to take from ClothCraft | Files to read |
|---|---|---|---|---|
| 1 | Heavy body sitting: the cardigan balloons over belly and seat | Round 3: 328 through (bar 299); round 4: 10 by count but still a hoop by eye | Pose-by-pose relaxation: VBD steps with OGC against the posed body, started from the skinned result (separated at rest, so the start check passes); plus a shape check (hem distance from thighs and seat) | src/vbd.rs, src/vbd/local_step.rs, src/ogc/world.rs |
| 2 | Pullover over a lower layer lost band height | 0.86 in round 3; fixed in round 4 (0.97 to 1.02) | Keep it fixed: membrane energy against rest; stretch per band ring | src/energy.rs, src/garment/diagnostics.rs |
| 3 | Front shoulder line of an outer layer saw-toothed | Better in round 4, still rippled by eye | Bending energy in the relaxation; edge-edge contact keeps it off the lower layer | src/energy.rs, src/ogc/world.rs |
| 4 | Ron's jacket vent opens over the seat (round 4 camera check) | 140 and 143 points, bar 100 | Vent kept closed at rest, rigged to the pelvis; checked from the camera | (shared checks) |
| 5 | Input bodies | Stale bone name; three "build" bodies identical | Inspect and fingerprint every input body; refuse identical bodies under different names | src/avatar/diagnostics.rs |

Acceptance test: (1) cardigan over blouse on a real heavy body sitting: at or below the bar, no balloon by eye; (2) Tom's jumper over Sheila's blouse on Lena: every band within 5%; (3) front shoulder line smooth on all four bodies; (4) everything that passed still passes, the 0.0 mm fit onto the source body and the same bytes twice included; (5) under 5 s a garment with the relaxation.

## Brief 3: Loomwright cloth (what Kiln's cloth must do better)

Loomwright's cloth is replaced by Kiln; its round 2 (13 Nov) fixed the tears on its built-in body and added crumple, self-crossing and camera layer checks, binary FBX, skinning and a body-file input, but on Tom's real body its jacket was lost 2 to 2.7 m below the floor. Lessons for Kiln: start every layer separated and refuse an overlapping start; VBD and OGC instead of one-substep XPBD; a real body input; keep its crumple, self-crossing and camera layer checks; add an "all layers present and on the body" check; skinning through Seamshift's transfer; binary FBX.

Acceptance test: Tom's shirt, jumper and jacket on Tom's MetaHuman body: no tear or crumple by eye; no lower layer visible through an upper one from front, side and back; its own check fails a deliberately broken run (layers started overlapped); output skinned to the MetaHuman skeleton with an exact bind pose in Unreal; at or under Marvelous's body-through and stretch numbers; same result twice.

## Shared: checks that cannot be fooled (all of Kiln)

1. Negative controls in every test suite: a jacket started inside the jumper must fail; a sleeve with the arm through must fail; a buried hair card must fail. (examples/settling_zoo.rs, docs/settling-zoo.md)
2. Labels with stated thresholds, not "ok": quiet (every point within 10 micrometres, top speed under 0.1 mm/s, leftover force under 1% of weight), quiet but forces unbalanced (jammed), still moving, or not observed long enough.
3. Worst case per piece beside the share; fail on the maximum. (src/garment/diagnostics.rs)
4. The identity case: a correction on something already correct changes nothing.
5. Start and end inspections: validate_start before any step, and an independent intersection check on the final surface.
6. Seen from the camera: what shows through from front, side and back at the game's distances. Our addition.
7. Same bytes twice, recorded.
8. Evidence beside each claim (ClothCraft keeps a validation JSON next to each design note).

## Sources

ClothCraft repository (main at 8 Nov 2026): README.md, Cargo.toml, LICENSE, docs/architecture.md, docs/ogc.md, docs/settling-zoo.md, docs/avatar-diagnostics.md, docs/first-fit.md, docs/draped-realtime.md, docs/documents-and-sewing.md, docs/elastic-seams.md; src/ogc/world.rs, src/avatar/diagnostics.rs, src/garment/diagnostics.rs, src/vbd/audit.rs, src/fabrics.rs, src/bin/cloth-fit.rs. Chen et al., Offset Geometric Contact, SIGGRAPH 2025. Our test reports (DrapeStudio 10, 11, 13 Nov; Seamshift rounds 1 to 4; Loomwright cloth rounds 1 and 2). No ClothCraft code was built or run by the advisor.
