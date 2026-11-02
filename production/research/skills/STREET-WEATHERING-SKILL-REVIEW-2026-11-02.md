# Review of the street-weathering skill, 2 November 2026

One fresh reviewer (general-purpose helper, read only, no clicks) checked .claude/skills/street-weathering/SKILL.md against its sources: the street-wear research files, Study 5, the corner plan and its review, the ten tools' usage and code, DECISIONS.md, RULINGS.md, the memory notes and CLAUDE.md.

**Verdict: PASS WITH FIXES.** The commands, switches and numbers hold up almost everywhere. Two statements were wrong, and one of them would have hung the next wall picture upside down.

## Fixes (all applied, each claim re-checked against its source first)

1. Step 4: "a wall decal prints its picture's first row at its foot, so the picture is stored the other way up" was out of date. DECISIONS 29 Oct 17:52 turned the spawner instead (VignetteShot.cpp SpawnWear; make_wear_masks.py 196-197). Now: draw wall pictures the right way up.
2. Step 3: the office smoke was one wall-wide mark per wall plus the ceiling's own colour (DECISIONS 29 Oct 16:56, 17:31). It was not painted by height into textures.
3. Step 4: anti-aliasing and streaming off is settled. The chandler's runs used `--exec "r.AntiAliasingMethod 0,r.TextureStreaming 0"` with office_look.py --editor --buffers (F:/LedgerTools/gate/new/chandler-wear/det/bare/command.txt).
4. Step 4 and step 7: the commandlet needs `-EnablePlugins=PythonScriptPlugin -unattended -nopause`, as the build machine runs it (ledger-probe-unreal.yml). Check for the run's own new line in ue-probe/ue-material.txt and for no LogPython error (memory unreal-commandlet-script-full-path).
5. Step 4: only `--camera` writes stain-marks.json, and `--wear`, `--on` and `--inner` work only with it.
6. Step 4: counting decals is settled. The placed marks are street-wear.json "decals" by "on" (188); vignette-scene.json decals.items holds 10 bill-of-materials pieces. Change the rule in street_wear.py; never edit the file by hand.
7. Always: NIGHT-GAPS' recommendation is not used unless he asks. Its sections 1 to 3 stand with the review's corrections.
8. The "none among 7,572" citation is Study 5 item 4 and WET-GROUND-METHOD §2.
9. Step 3: brick changes stay on the piece's own houses. A change to the shared material waits for his yes (CORNER-PLAN-REVIEW fix 6).
10. Step 3: M_LedgerKitPaintWood is held back with its rebuilt mesh. New trims go in the material only, and the lit pier is not reopened (DECISIONS 30 Oct 17:33, 1 Nov 22:21).
11. Homes:
    - The bands' home is the two research files; surface_values.py's BANDS derives from them.
    - The BANDS flags band (0.11 to 0.20) differs from FLAGS-BRICK-BANDS' wet base colour (0.09 to 0.22). That file is the flags' one home (WET-GROUND-METHOD fix 5). Marked "check first".
    - The night pin is in the look file. Only the day pins are in vignette-scene.json.
12. The gains were tuned from early October (surface_gain_note_3_october) and found too dark on 29 Oct.
13. Step 1: chart_read.py reads fixed spots in the frame. A moved chart needs `--row` and `--cols`.
14. Step 1: C1 is partly measured (chandler_wear_check.py c6 --chart). Only the 24-patch colour-difference check has no tool.
15. Step 4, pictures:
    - The default make_wear_masks.py run writes into ledger/Assets/StreamingAssets/Decals/ours, which is in git.
    - `--street-wear` writes only wear_rust and wear_threshold.
    - New pictures go to F:/LedgerTools/game-inputs, gitignored, and `push_guard.py --staged` runs first.
16. Records:
    - RECIPE gets its lines when a unit finishes or is set aside.
    - New art or research gets a CATALOGUE.md line (tools/catalogue.py).
    - Previews go to production/previews/ as JPEG.

## Missed in the draft, now added

- The ground cuts its water coat wherever a decal's roughness times coverage nears 0.6 (make_base_material.py). A ground stain at M_LedgerStain's default 0.85 may therefore strip the water under it. This is read from the code and untested, so it is marked "check first".
- A change that shows across the whole street frame reaches his page before merging (CLAUDE.md; RULINGS 29 Oct).
- Reuse first and the licence allowlist, with a THIRD-PARTY.md line for anything from outside.
- The pale line passed in the editor only. Its packaged check and the far pavement's pale patch wait for the morning pictures.
- Near-black is measured two ways that cannot be compared: measure_night_pools.py uses linear luminance under 0.005, and the 87% figure was luma under 10.
- Commit before any standalone Unreal run.
- The night's highlight contrast has no look-file key yet; only local_highlight_contrast_day exists.

## Named but not real

- tools/pool_clip.py does not exist. The skill already gives the right path, production/audits/night-2026-10-08/pool_clip.py.
- No debug view of the water cover exists. The skill's "check first" is right.
- Every other tool, switch, constant and look-file key exists. The builder also checked -NoBrickStreaks in VignetteShot.cpp.

## Size and shape

About 90 lines, well under 200. It is shaped like the three sibling skills: front matter, numbered steps each with a Check line, and records at the end. Its rules carry their dated reasons, and town values point to the look, scene and wear files.
