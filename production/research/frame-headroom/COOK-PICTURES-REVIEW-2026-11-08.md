# Review: COOK-PICTURES-PLAN-2026-11-08 (fresh reviewer, 8 Nov 2026)

**Verdict: pass with fixes.** The figures and engine claims hold. Four fixes to the method (2, 4, 5a, 5c) must land before step 3 starts. All sources were read 8 Nov 2026.

1. **Table arithmetic: holds.** Every "today" figure re-adds from RUNTIME-PICTURES section 3 and MEMORY-WHERE section 6 (630 = 21 x 30; 126; 264; 317.2; 105; 29; 3.5). Every "after" figure checks at 0.5 or 1 byte per texel times 4/3 (shop cards 224 / 210 / 74.7; sky and scalp 2.67; wear 10.8; decals 33-41). The peak follows: 6,152 - 1,952 + 400 to 450 = 4,600 to 4,650.
   - Wording fault (line 6): BC1 with mips is 0.67 MiB per 1024², not "about 1 MiB". Epic's table gives 699,192 bytes (page read 8 Nov). The table already uses 0.67.
   - The worn fronts' 55-60 holds only without mips (about 75 with mips). Fix: say which.
   - The brick ID maps are probably inside the unnamed 423 MB, so the 95-140 slightly over-counts the saving (inferred).
2. **Engine claims.**
   - Not a multiple of 4 forces uncompressed: holds (Texture.cpp:4254-4263).
   - Sides that are not powers of two never stream: holds (Texture.cpp:1841-1872, 1897-1922).
   - Mips for such sizes: now answered. The mip builder handles them (TextureCompressorModule.cpp:1195-1207).
   - **However, a fresh import sets them to TMGS_NoMipmaps, and to TC_EditorIcon (uncompressed) when a side is not a multiple of 4** (TextureImportSettings.cpp:222-249; on by default, TextureImportSettings.h:90). This probably explains the worn fronts too (inferred).
   - Fix: after import, the importer sets power_of_two_mode, mip_gen_settings and compression_settings explicitly. Step 3's readback also checks that the mip count is above 1 and reads the pixel format.
3. **No picture rewritten after load: holds.** Pixels are written only at VignetteShot.cpp:6196-6231, 6261-6266 and 9859-9861. LedgerPaper.cpp:70 and SliceCharacter.cpp:726 decode once. The calls at 8829 and SliceCharacter.cpp:729 only re-upload after a flag change.
   - Step 1 is wrong for the scalp: it goes through FImageUtils::ImportFileAsTexture2D, which takes no name (CreateTransient's name is at Texture2D.h:342). Fix: Rename() it, or route it through ImportTexture.
4. **Compression per role.**
   - Derived samplers: holds (make_base_material.py:445, 519-555; self-test cases 2376-2384).
   - The plan's open normal-map risk is settled: UnpackNormalMap rebuilds Z from R and G whatever the format (Common.ush:1698-1711), so BGRA8 to BC5 changes nothing there.
   - **Wrong: the role cannot come from the file-name ending.** The scans are named _nor_dx_2k and _rough_2k (ps5-corner.json:350-353), and the game decides the role by position (VignetteShot.cpp:8798, M == 0). Fix: take the role from each spec's map position.
   - stage_game_data.wanted() also returns whole folders (stage_game_data.py:64-84, 148-154). Fix: filter it to pictures, and leave out the ID maps, the UI art, the .hdr files and the cropped decal sources.
5. **Steps.**
   - a. **Step 2 adds behaviour.** Today the card's lit or dark state is fixed by LitOn = bLitAtNight (8489), and SetShopRoomLit never touches the card (10513-10535). Swapping on GShopsDark would change Mickey's card. Fix: show Night ? (LitOn ? lit : dark) : day, and nothing more.
   - b. **The hitch has no check.** Fix: land steps 2 and 4 in one change, so no PNG is decoded at a light change.
   - c. **Risk missing from the table: mips on the interior-mapped cards.** The Custom node's UV jumps at the room's wall seams (make_interior_material.py:44-58). Mips there would pick a tiny mip and draw a line along every room corner.
     - Fix: cook the cards with no mips. BC7 4096x2048 is 8 MB, so the shown state alone is 56 MB, not 75.
     - Or add a close shopnight crop of a room corner to the gate.
   - d. **Gate.**
     - The scalp is a whole-person look, and step 5 has no face view. Fix: add a -FaceAB view of Tom, or leave the scalp out.
     - Mips and compression on every street surface are a whole-frame change. Under CLAUDE.md it goes to his page whenever a reviewer sees a change; it is not the session's choice.
     - Add the brick-corner view (the scan maps).
   - e. **Step 7: "cut" shifts the UVs.** Fix: use ResizeToSpecificResolution to 5412x552, which keeps UV 0-1.
   - f. **Hours.** Plausible, except that the runner's BC7 encode time is not budgeted. Fix: measure it in step 3.
   - Holds: /Game/Ledger is always cooked (ue-probe/Config/DefaultGame.ini:45), so assets imported there ship without a hard reference.
