# Card memory, step 4's next change: the pictures compressed (plan, 12 Nov 2026)

Item n09-3. Written by the session from RUNTIME-COMPRESSION-READING-2026-11-12.md (engine source, 5.8.2) and RUNTIME-PICTURES-2026-11-08.md. Unreviewed: one fresh reviewer checks it against those two before the first try.

## Where it stands (measured)
- Build 4e3e4b8 (one shop picture of three loaded): steady 5,172 MB, peak 5,538 (line 5,650; was 5,541 / 5,873). Windows' budget for the game about 4,870 MB, so about 300 MB still over it.
- Run-time pictures are the largest holder (about 1.9 GB on 8 Nov, before today's 420 MB cut): all decoded to BGRA8, one mip, never streamed (VignetteShot.cpp ImportTexture, CreateTransient PF_B8G8R8A8).

## What the source allows (from the reading)
- No texture compressor runs in a packaged game (TextureCompressor, TextureFormatDXT, ISPC texcomp are editor/program-only).
- CreateTransient accepts BC formats (PF_DXT1, PF_DXT5, PF_BC7) when handed already-compressed blocks, sizes a multiple of 4 (1855 is not: pad to 1856), one mip as written; extra mips by hand UNVERIFIED.
- A cooked asset gets compressed mips but a non-power-of-two size never streams (Texture.cpp IsPossibleToStream).
- BC1 is 1/8 of BGRA8 (4096x1856: 3.8 MB against 30.4); BC7 1/4.

## Two routes, cost against gain
A. Compress offline when the game data is staged (stage_game_data.py): each run-time PNG also written as a block-compressed file (BC1 for opaque colour, BC7 or BC3 where alpha matters), padded to a multiple of 4, with mips; ImportTexture reads that file when present and makes the transient texture in that format; the PNG stays the source and the fallback. Needs: a compressor on this PC (Microsoft DirectXTex's texconv, MIT, a new tool: an allowlist record first; or the engine's own compressor driven from an editor commandlet at staging time, no new tool), about 60 lines of C++ for the block upload and mips, a staging step. Gain: about 1.9 GB of pictures to about 0.3 to 0.5 GB. Keeps the run-time-file workflow every piece already uses.
B. Import the run-time pictures as cooked texture assets (the professional default: the cook compresses and mips them). Needs an import script per family, every call site moved from file paths to asset paths, and the build machine's import step; non-power-of-two pictures stay resident. Bigger change to how pieces are made; same memory gain for resident pictures.

## Recommendation
Route A with the engine's own compressor at staging time if a commandlet can reach it (no new tool), else texconv after its allowlist record. First the shop pictures only (7 resident, 30 MB each: about 180 MB saved), measured on the build machine's perf line against build 4e3e4b8; then the decals and scans. Look unchanged is the bar: the hook and reverse frames compared at true size, BC1 artefacts on the shop rooms judged by one small reviewer.

## Reference
Kingdom Come II and Mafia ship cooked, block-compressed textures throughout (studies/12-tech-budgets.md); neither loads pictures from loose files at run time, so route B is their method and route A our closest equivalent within our run-time-file pipeline.
