# A. TextureCraft and MaterialCraft: first-pass reading (read 10 November 2026)

Licence (one line, not a step): both are MIT or Apache-2.0 at the user's option (https://craft.wiki/apps/texturecraft/overview, https://github.com/storytold/materialcraft).

Short names: TC = TextureCraft, MC = MaterialCraft. All links read 10 Nov 2026. Both are young and change daily; versions seen: TC 0.4.0, MC 0.2.0 (both released 6 Nov 2026).

## Questions
1. What each does: inputs, outputs, map types, resolutions, tiling.
2. How each runs: installer or portable, local or cloud, card and memory needs, Windows.
3. Control without clicks: command line, JSON channel, MCP; start and accepted input.
4. TC bakes from high to low mesh; smart materials; masks and layers.
5. MC procedural tiling materials (weaves, brick bonds incl. Flemish, wallpaper, painted timber); parameters; maps.
6. Unreal export presets: packed maps, naming, colour space.
7. Repeatability: same inputs, same pixels? Seeds?
8. Known faults, crashes, maintainers' activity, trackers.

## 1. What each does
- TC: 3D texture painting app in Rust. Paint layered PBR materials with masks onto a model, bake mesh maps, export for an engine. Import glTF/GLB, FBX, COLLADA, USD, Alembic, OBJ, PLY, STL; models without UVs get generated UVs. One `.tcraft` project file. Export PNG, JPEG, TGA, TIFF, BMP, WebP, EXR, HDR at 8/16/32 bit, UDIM tiles; mesh export OBJ, GLB, USD. Product page claims it targets 8K texture sets. Sources: https://getartcraft.com/apps/texturecraft ; https://craft.wiki/apps/texturecraft/overview
- MC: node-based procedural material designer. Outputs base colour, normal, roughness, metallic, height, ambient occlusion (README); product page says maps tile seamlessly because noises and patterns use whole-number lattices; resolution range 16 px to 8K; export dialog up to 8192 px. Files: `.sbs` packages (also opens another app's .sbs, with many nodes shown as placeholders), `.mcmat` portable material. Sources: https://getartcraft.com/apps/materialcraft ; https://craft.wiki/apps/materialcraft/overview/ ; https://craft.wiki/apps/materialcraft/workflows/ ; https://github.com/storytold/materialcraft
- Both pages say "In development"; TC page says pen tilt/pressure missing on macOS and Linux, README estimates ~93% of a texture artist's daily workflow present (unverified claim by makers).

## 2. How each runs
- Local and offline; no AI model or cloud mentioned on either page. Free.
- Windows: MSI installer (all users, Program Files, needs admin) or portable ZIP, x64/x86/ARM64 (MC install page: https://craft.wiki/apps/materialcraft/install-update/). TC lists the same on its product page. Also ArtCraft Launcher v0.15.0, macOS, Linux, FreeBSD, WebAssembly.
- TC needs a GPU with Vulkan, Metal or DirectX 12; no RAM/VRAM figures given (https://craft.wiki/apps/texturecraft/troubleshooting/). MC page lists no minimum hardware. Source build needs Rust 1.95+.
- The CLI `texturecraft-cli` / `materialcraft-cli` ships next to the app on Windows.

## 3. Control without clicks (confirmed from makers' docs; not run)
- TC (https://craft.wiki/apps/texturecraft/ai-agents/ ; https://raw.githubusercontent.com/storytold/texturecraft/main/docs/control-protocol.md):
  - Command line: `texturecraft-cli` with `new`, `bake`, `export`, `render`, `info`, `commands`, `run <input> <command-id>`, `batch <script.json>`, `serve`. Example: `texturecraft-cli export model.tcraft textures --preset "Unreal Engine (Packed)" --format png`.
  - JSON channel: `texturecraft-cli serve [--port]` (JSON lines over stdio, or loopback TCP with token); app channel `texturecraft --control <port>` with token.
  - MCP: `texturecraft-cli mcp --read-root X --write-root Y` (headless) or `--bridge <port>` to the running app. Every command has a stable id (e.g. `layer.add.fill`), run via `command.run`; `command.list` lists them. File commands through command_run are refused; agents use the workspace tools.
  - Gap: the docs do not give the JSON schema for `serve`, the `batch` script format or the control port messages (the page points to `--help`).
- MC (https://craft.wiki/apps/materialcraft/workflows/ ; https://raw.githubusercontent.com/storytold/materialcraft/main/docs/control-protocol.md): `materialcraft-cli` with `new, info, nodes, cook, run, batch, serve, export, render, mcp`; `--set` assigns exposed inputs; `outputs.export {dir, format, pattern, depth, size, graph}`; `material.export` writes `.mcmat`. JSON request form `{"id","method","params"}`. Token from `MATERIALCRAFT_CONTROL_TOKEN` or a temp token file; set `MATERIALCRAFT_NO_PREFS=1` for scripted runs.

## 4. TC bakes, smart materials, masks
Source: https://raw.githubusercontent.com/storytold/texturecraft/main/docs/features.md ; https://craft.wiki/apps/texturecraft/workflows/
- Bakers: ambient occlusion, curvature, thickness, world-space normal, normal, position, ID, bent normals, height, opacity, colour, direction. Normal and height from high-poly meshes with a cage, ray distances, matched by mesh name (features page). GPU (stated ~12x CPU, maker's claim, unverified) or CPU. Own images can be dropped in as mesh maps. CLI `bake --maps a,b --resolution N`.
- Workflows page does not cover cage setup, per-baker settings or the high-to-low specifics (unverified in detail).
- Library: 72 materials, 21 smart materials (named examples: rusted iron, worn paint, bronze statue), 24 smart masks; all procedural. Mask generators include edge wear, dirt, thin areas, curvature, AO, position/direction gradients, world-space noise; they need the bake run first. Layers: paint, fill, folder; blend mode and opacity per channel. Own smart materials can be saved. No fabric-wear or grime-gradient smart material is named (unverified whether any exists in the list).

## 5. MC procedural materials
- Product page lists 12 templates: empty, PBR, brick wall, stone tiles, wood planks, painted metal plates, rusty metal, lava rock, polished marble, wicker weave, woven fabric, mossy ground (https://getartcraft.com/apps/materialcraft).
- But the overview page says version 0.2 rebuilt the node library from basic blocks and "the ready-made noises, patterns and sample materials from earlier versions are gone for now" (https://craft.wiki/apps/materialcraft/overview/). The two pages disagree; which templates exist in 0.2.0 is unverified. README counts: 30 main-graph entries, 85 function operations, three pattern node kinds.
- Building blocks: blend, blur, levels, curves, gradient maps, HSL, warps, normal maps, transforms, text, SVG/bitmap, FX-Map (Quadrant, Switch, Iterate, Dot), pixel/value processors. A random seed exists. Exposed inputs become sliders.
- Brick bonds (Flemish), wallpaper, painted timber: no page names them. Unverified; would be built from FX-Map nodes if possible.
- Link to TC: send as `.mcmat` fill layer; but TC reads only .mcmat v1 while MC writes v2 (TC issue 317, listed on https://craft.wiki/apps/texturecraft/troubleshooting/).

## 6. Unreal export
- TC presets: glTF PBR Metal Roughness, Unreal Engine (Packed), Unity HDRP (Mask Map), Unity Standard, Blender (Principled BSDF), Godot 4 (ORM), OpenPBR separate maps. Templates assign channels to images (RGB, RGBA, Gray, Gray+A), can be edited and exported as JSON. OpenGL or DirectX normals; padding; size override. `$udim` for tile naming.
- The pages do NOT state the Unreal packed channel order, file naming or colour-space (sRGB/linear) handling. Unverified. Colour in commands: `[r,g,b]` linear, `"#rrggbb"` sRGB (CLI page).
- MC: export pattern for file names, format and bit depth; no engine presets seen.

## 7. Repeatability
- Neither page states determinism. TC docs say a live-preview bake gives the same pixels as a single bake (control-protocol). MC has a seed (`randomseed`). TC issue 307 (6 Nov, high priority) reports that after undoing "Add mask" the cached composite can differ from a full recomposite (https://github.com/storytold/texturecraft/issues). Same-input-same-pixels: unverified, needs a test run.

## 8. Faults and activity
- TC: 545 commits, 569 stars, 193 forks, 70 open issues, 72 PRs (https://github.com/storytold/texturecraft). Issues 10 Nov: GLB export mesh issue (382), offset UVs wrong (375), colour param that fails to parse is silently ignored (369, automation), Blender-baked normal maps shade wrong on quads (365), GPU not used (358). Known unfixed (troubleshooting page): crash at start on Intel HD/UHD 620; projects over 8 GiB unpacked will not reopen; slow save with 4K/UDIM; slow high-resolution baking; GLB textures not applied; UVs regenerated unexpectedly. Release v0.4.0 (6 Nov): 17 changes, 6 contributors (https://github.com/storytold/texturecraft/releases/tag/v0.4.0).
- MC: 374 commits, 333 stars, 140 forks, 27 open issues (https://github.com/storytold/materialcraft/issues). Open: "Not Opening" on Windows, critical (28); cannot open saved materials after updating to v2, critical (138); MCP `ui_input` schema makes Claude Desktop drop the server (146); function graph caching issue (148). v0.2.0 (6 Nov) about 50 PRs, 15 contributors, hardened control server, many crash fixes (https://github.com/storytold/materialcraft/releases/tag/v0.2.0). v0.2 broke file compatibility with v0.1.
- Activity: very high (many issues and PRs dated 6 to 10 Nov 2026); the project is days old in this form. Open-issue counts are as shown on the page, not confirmed as open-only.

## Unreached
- TC and MC "getting-started", "install-update" (TC) pages, MC "troubleshooting" page, and the repos' `features.md` for MC, `ROADMAP.md`, `docs/architecture.md`, `docs/atomic-workflow.md`.
- Release asset lists (failed to load).
- Individual issue bodies (only list pages read), Discord.
- Any running of the tools (not allowed).

## Unverified
- Which MC templates (brick, fabric, planks) exist in 0.2.0; Flemish bond; wallpaper; timber.
- Unreal Packed channel layout, naming, colour space.
- Determinism and seed behaviour of either tool.
- Cage/high-to-low bake quality; fabric-wear and grime smart materials.
- Windows crash cases beyond issue 28 (MC) and Intel 620 (TC); VRAM/RAM needs.
- The 12x GPU bake speed and the "93%" workflow claims (makers' own).
- Fetch summaries came through a page-reading model, not raw text, so exact wording and counts are unconfirmed until read in full.
