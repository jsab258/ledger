Method researched: tools/meshgen/blender/import_md_drape.py, retopo_pieces.py, uv_pack_low.py, zip_bake.py, skin_garment.py, tools/md/unpose_garment.py, tools/ue/import_garments.py (docstrings and code, read 17 Nov 2026); Kiln's engines/drapestudio/src/export.rs, fbxout.rs, serve.rs (export_obj, avatar_obj, open_project), python/kiln_front/compat.py; Tom's jeans chain records (F:/LedgerTools/garments/tom/jeans/chain-n7: import.json, retopo.json, skin.json); KILN-M5-RIGGING-METHOD-2026-11-17.md; studies/06-characters-wardrobe.md.

Game item: n16-1, Kiln's parity list gap 1 (F:/LedgerTools/tool-dev/reports/KILN-PARITY-LIST-2026-11-17.md): prove the path from a Kiln drape to the game once. A plan and one machine-free adapter; nothing was run in Unreal or Blender, nothing imported, nothing committed. Tags: **U** unverified, **E** estimate (hours).

# Kiln drape to the game: the chain, the adapter, the steps left (17 November 2026)

## First garment: Ron's work trousers

- **Skinned only, no cloth hand-off.** Trousers are skinned in Mafia and Kingdom Come II alike (studies/06 lines 117, 124, 138) and under the 30 Sep ruling. Sheila's pleated skirt (the fallback) would also need the Chaos cloth hand-off, which has never run packaged (parity list row "Long loose parts"). That would make it a second unknown in the same proof.
- **A passing drape exists.** The 16 Nov armline run (F:/LedgerTools/tool-dev/runs/kiln-armline-2026-11-16) settled. Its check reads body through cloth over 1 mm 0, and cloth inside 0 over 1 mm and 0 over 3 mm (work_trousers_check.json).
- **Plain body, no bend-back.** That drape was made on Ron's raw MH_RoccoP2_FullBody.fbx (the .drape's body path). That is before the straight-forearm standard bodies (16 Nov 22:17). It stands in the reference pose, so no bend-back or turns record is needed. Arms do not move trousers anyway (pose_trousers.py's docstring).
- **A proven route.** Its plan follows the jeans route. The piece order matches (frontR 0, frontL 1, backR 2, backL 3), so Tom's passed jeans give every chain option.
- **Ron's outfit needs it.** It is the trousers half of Ron's M6 outfit (RON-KILN-OUTFIT-PLAN-2026-11-16.md).

## Reference for the skinning step

- **Mafia (studies/06):** skinned pieces on one leader skeleton. Trousers 8,000 to 10,000 triangles. Up to 8 influences at the top two levels of detail, 4 below.
- **Kingdom Come II:** the same study records baked, skinned garments, with no separate skinning method found. For KCD2's own files, **none found**.
- **The project's copy:** bind_garment.py through skin_garment.py. The body's weights are copied only where the body is near and faces the same way, and the rest is filled in, after Epic's inpainting method (KILN-M5-RIGGING-METHOD section 4). Neither Kiln nor Marvelous hands over weights. Both routes take them from the wearer's body FBX.

## 1. The Marvelous chain as it runs (Tom's jeans, chain-n7)

| # | Step | Script | Takes | Gives |
|---|---|---|---|---|
| 1 | Drape | tools/md-bridge/<job>.py through md_job.py | the job file, the avatar (FBX at scale 10 plus its .avt) | OBJ (mm, y up, one group per piece, each piece's UVs centred in fabric-tile units, avatar LODs as *_LOD0..3); .zprj; <job>.plan.json (pieces: key, fabric, outline points in mm) |
| 2 | Bend-back (only when draped on a posed body) | tools/md/unpose_garment.py DRAPE_BODY.fbx DRAPE_BODY.json OBJ OUT.obj | Marvelous-layout OBJ; the body picked by "_LOD0", then by size | the same OBJ layout, in the reference pose |
| 3 | Weld, pattern layer | import_md_drape.py OBJ PLAN OUT.blend --body FBX --object NAME --materials fab:Mat | OBJ imported at scale 0.001, forward -Z, up Y, split by group. Each piece's UVs are fitted to the plan outline (positive tile, no flip). Welded at 0.01 mm. Materials come from plan fabrics. The body and armature come from --body | .blend (welded mesh with "piece" attribute and true-size "pattern" layer, Body, armature); import.json |
| 4 | Game mesh | retopo_pieces.py SEWN.blend PLAN IMPORT.json OUT --object NAME --tris-target N | the "piece" attribute, the plan's patch corners | LOW.blend, retopo.json (jeans: 9,600 predicted, ok) |
| 5 | Texture layout | uv_pack_low.py LOW.blend PLAN IMPORT.json --tex 2048 | the pattern layer | "UVMap" packed, uvpack.json (overlap 0) |
| 6 | Bake | zip_bake.py LOW.blend OUT --name N --tex 2048 --plan PLAN --object NAME --rib-height 0 | LOW and the high drape | normal, occlusion, packed maps; bake.json (hits 97% or more) |
| 7 | Game blend | the jeans' scripts/make_game_blend.py (renames "Low" to NAME) | LOW.blend | GAME.blend |
| 8 | Skin | skin_garment.py BODY.fbx GAME.blend OUT NAME --no-skirt --leg-sides 0,2:1,3 --crotch-fade 0.07 --centre-seam 0,2:1,3 | the body's weights (bind_garment.py, reach 0.06 m, angle 50 degrees), at most 8 influences | NAME_skinned.fbx, skin.json (notButtons, uvReordered, legSides, crotch) |
| 9 | Pose tests | pose_trousers.py (walk, sit, stair); pose_skinned.py --own-weights | the skinned .blend | pose-test.json, pictures |
| 10 | Into the game | a row in production/specs/garments.json, then tools/ue/import_garments.py in C:/LedgerTools/mh-assemble | the skinned FBX, maps, tint, detail tile | SKM at /Game/Ledger/MetaHumans/Garments/<Name>/; garments_shipped_check.py PASS |
| 11 | Packaged | tools/nightly_package.py; -WearHeld film (packaged-walk skill); the gate | the held row | the film, RUBRIC lines 9 to 11 |

Import's "ok" is advisory: Tom's jeans went on with ok false (boundary 3.5 mm, body fit 20 mm after the bend-back; chain-n7/bake/import.json).

## 2. What a Kiln run writes, against that

| Point | Marvelous | Kiln (code read; real files measured) | Effect |
|---|---|---|---|
| Units, axes | mm, y up | mm, y up ("app" space) from a job's ExportOBJ (compat.py passes no "space"). An export with space "body" would be cm, z up | match. Never export with space "body" for this chain |
| Pieces | one group per piece, plan keys | one "g" per pattern, the plan's keys (checked on both files) | match |
| UVs | each piece centred, fabric-tile units | true size in metres, v negated; measured as the plan's frame shifted along x per piece (signs (1, 1), y shift 0, worst 0.011 mm) | the import's fit accepts both (Kiln's tile 1000). The adapter makes it exact and checks it before Blender |
| Weld | unwelded, partners coincide | welded at 8 mm (SEW_CLOSE_GAP), partners averaged, separate UVs per piece | the import splits by group and re-welds at 0.01 mm. Expect welded over 0 and openings 3 (waist, two hems; U until run) |
| Body in the OBJ | avatar LODs, named *_LOD0..3 | one group "Avatar" (avatar_obj) | **mismatch.** The import finds no _LOD0, so bodyFitMm counts as 99 and a stray body mesh stays in the .blend. Adapter renames it to KilnBody_LOD0 |
| Materials | usemtl per fabric | none in the OBJ | none: the import names materials from the plan's fabrics |
| Plan file | <job>.plan.json | the same job writer, the same file layout | match (the armline plan and the garments copy hold identical pieces) |
| Pose | posed body, then unpose | before 16 Nov 22:17, the raw FBX. Since then, the standard body (straight forearms, joined head) | the armline trousers need no bend-back. Any later Kiln drape needs unpose_garment.py with a turns record per standard body (ron_standard_body.json exists; whether it holds "turns" is U) |
| Weights | none | none (fbxout.rs writes no skin) | match: skin_garment.py from the body |
| The final OBJ kept | exported and kept (month-end rule) | the armline run's final OBJ is **gone**. Its .drape (with the 16,395 particle positions) and pictures remain | re-export through Kiln's open_project, which restores the saved positions (serve.rs 1446 to 1500) |

## 3. The adapter (written, self-tested)

tools/kiln_to_game.py (plain Python, no Blender; inputs read-only, sha256 checked before and after; outputs only under F:/LedgerTools/game-inputs/kiln-to-game/):

- per piece: finds the boundary, fits the plan outline (straight fit, a flip only when that misses, and then refused), checks the scale is true size, and rewrites the UVs as plan mm / 1000;
- renames "g Avatar" to "g KilnBody_LOD0";
- refuses a missing or extra piece;
- writes kiln_to_game.json.

Self-test (`python tools/kiln_to_game.py --selftest`) on two real Kiln files: PASS.
- Ron's trousers. The surviving trousers export is the 20 mm pass's first stage (kiln-patcheck-2026-11-16/work_trousers/stages/p20_000.obj): 6 pieces, worst boundary 0.011 mm, scale off 0.00005.
- Tom's jumper j3, a final welded export with "Avatar": 9 pieces, worst 0.0015 mm.
- Positions, normals and faces unchanged on both. A plan naming a missing piece is refused, and so is an output outside game-inputs.
- Not tested: the final trousers drape itself (gone until step A).

## 4. Steps left for the session (Ron's work trousers, route A)

Before any Blender or Unreal run: `python tools/retention.py space --job "kiln trousers chain" --drives CF`; no runner build, no night job within 15 minutes; one Unreal at a time. Paths below: K = F:/LedgerTools/tool-dev/runs/kiln-armline-2026-11-16, G = F:/LedgerTools/garments/ron/kiln-trousers-chain (a new folder), P = K/work_trousers_plan.json, BODY = F:/LedgerTools/bodies/MH_RoccoP2/MH_RoccoP2_FullBody.fbx.

| # | Step | Needs | Command | Expected check | Hours (E) |
|---|---|---|---|---|---|
| A | Re-export the passing drape | Kiln engine only, a quiet machine (no Kiln gate running) | through kiln_front's session: `open_project path=K/work_trousers/work_trousers.drape`, then `export_obj path=G/kiln/work_trousers.obj garment=true avatar=true` (weld default true, app space) | 6 groups plus Avatar; fewer "v" than "vt" (welded). The run's own measures re-taken on the new OBJ match work_trousers_check.json (body through 0, cloth inside 0). U: whether opening a raw-FBX project passes the start check (if refused, route B) | 0.5 |
| B0 | Adapter | Python | `python tools/kiln_to_game.py G/kiln/work_trousers.obj P F:/LedgerTools/game-inputs/kiln-to-game/ron-work-trousers --name work_trousers` | ok true; boundaryWorstMm 0.05 or less; flippedPieces []; bodyGroup true | 0.1 |
| B1 | Weights-body match check (M5 note, section 1) | Blender headless | the FullBody against MH_RoccoP2_Body.fbx: bone names and rest to 0.01 mm, shared points' weights to 0.001 | both pass, else skin from the _Body file as Ron's jumper did | 0.5 |
| C | Weld, pattern layer | Blender headless | `blender -b --factory-startup -P tools/meshgen/blender/import_md_drape.py -- <B0 out>/work_trousers.obj P G/import/work_trousers.blend --body BODY --object Trousers --materials wool:Wool` | boundaryWorstMm 0.05 or less; bodyFitMm 2 or less; nonManifoldEdges 0; parts 1; openings 3; ok true | 0.3 |
| D | Game mesh | Blender headless | `retopo_pieces.py -- G/import/work_trousers.blend P G/import/import.json G/retopo --name work_trousers --object Trousers --tris-target 9600 --tris-min 8000 --tris-max 10000` | ok; sidesUnequal []; nonManifold 0; 8,000 to 10,000 triangles (Mafia) | 0.7 |
| E | Layout | Blender headless | `uv_pack_low.py -- G/retopo/<low>.blend P G/import/import.json --tex 2048` | overlap 0; 0.9 px/mm or more (jeans 1.43) | 0.3 |
| F | Bake | Blender headless (GPU: not while the runner's perf step runs) | `zip_bake.py -- G/retopo/<low>.blend G/bake --name work_trousers --tex 2048 --plan P --object Trousers --rib-height 0` | hits 97% or more; normals over 60 degrees under 1% per piece. Crease and fly in the normal map are not needed for the proof; listed as a shortfall | 0.8 |
| G | Game blend, skin | Blender headless | make_game_blend.py as in the jeans' chain; `blender -b -P tools/meshgen/blender/skin_garment.py -- BODY G/skinned/work_trousers_game.blend G/skinned work_trousers --no-skirt --leg-sides 0,2:1,3 --crotch-fade 0.07 --centre-seam 0,2:1,3` | skin.json: notButtons [], uvReordered true, legSides and crotch recorded; 8 influences or fewer | 0.7 |
| H | Pose tests | Blender headless | `pose_trousers.py -- G/skinned/work_trousers_skinned.blend G/pose`; pose_skinned.py --own-weights | cloth inside over 3 mm per pose within Kiln's parity bar (44); sit shape beside Tom's jeans. The boots: this drape had no boots proxy, so the hem over Ron's boots is a known shortfall, judged in the film | 0.7 |
| I | Row and import | editor (mh-assemble, unattended), session only; commit first | a held row in production/specs/garments.json (RonWorkTrousersKiln, Ron, hides lower, hold, maps from F, Tom's twill tile as detail for the proof, U), `python tools/ue/import_garments.py --selftest`, then `set LEDGER_MH_SCRIPT=import_garments` and `UnrealEditor.exe C:/LedgerTools/mh-assemble/MHAssemble.uproject -unattended` | the SKM present; `python tools/garments_shipped_check.py` garmentsShipped=PASS | 0.8 |
| J | Packaged | the runner (packaged-walk skill) | `tools/nightly_package.py`; a -WearHeld film of Ron walking and sitting | the film read against RUBRIC lines 9 to 11; one fresh reviewer per view beside the last good picture; then the parity list's M7 reads 1 (held) | 1.0 session, plus the runner |

**Total about 6.4 h (E)**, or 6 to 13 h with the 2 to 4x overrun the garment records show (BREADTH-PATTERNS). Reviews and the night walk come on top.

**Route B (any drape on a standard body, and every later garment):**
- step A on a fresh Kiln-main run;
- then, before C, `blender -b --factory-startup -P tools/md/unpose_garment.py -- F:/LedgerTools/bodies/standard-2026-11-16/ron/ron_standard_body.fbx .../ron_standard_body.json <B0 out>.obj OUT.obj`, with the turns record checked first. Expect bodyFitMm over 2 at the hands if the body group is not bent back (U);
- adds about 1 to 2 h (E).

## 5. What stays open

- **Ron's whole look waits.** The proof's row stays held. Ron's passed jeans are replaced only on his whole-person page (M5 note).
- **Keep the final OBJ.** The 16 Nov final OBJ vanished from the run folder. Step A's OBJ should be kept in G, and its loss recorded in DECISIONS.md by the session. Why it went is not known here.
- **Front-end licence.** RON-KILN-OUTFIT-PLAN risk 3: whether the Kiln front end's adoption tap was answered must be checked before step I.
