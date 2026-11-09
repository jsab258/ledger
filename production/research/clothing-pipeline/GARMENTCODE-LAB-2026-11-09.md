# GarmentCode lab, item n09-6, 9 Nov 2026

Follows GARMENTCODE-LAB-2026-11-08.md. Pattern part only: no simulator, Warp or dataset; Marvelous not started. Files in F:\LedgerTools\garmentcode-lab; nothing committed.

## Licence
- https://github.com/maria-korosteleva/GarmentCode, tag v2.0.2, downloaded again 9 Nov (archive/refs/tags/v2.0.2.zip). SHA-256 12fbc2d8…9d83, the same as the 8 Nov copy.
- LICENSE read in full on 9 Nov: plain MIT (c) 2024 Maria Korosteleva. Commercial use allowed; keep the notice. It is the tree's only licence file, and the source has no non-commercial or NVIDIA wording. The non-commercial terms belong only to the separate Warp fork, which was not fetched. **The pattern part is allowed commercially.**

## What ran
Fresh venv (venv-1109, Python 3.10.6, 264 MB). The 8 Nov licence-checked packages, installed from PyPI with --no-deps. All Python run with -I; scripts in lab\, outside the download. lab\jacket1109.py: the repo's MetaGarment on mean_male with the chest set to 100 cm. Then the 8 Nov DXF converter and check, and two new scripts: lab\dxf_png.py (standard library only, no Pillow) and lab\gc_to_mdspec.py.

## Pattern (lab\out1109\)
| | Work jacket (stand collar, cuffs, hem band) | Plain shirt |
|---|---|---|
| Panels / seams | 18 / 36 | 16 / 30 |
| Back length | 706 mm (2nd try) | 700 mm (1st) |
| Chest, flat | 1,160 mm | 1,100 mm |

- No self-crossings.
- Units: the spec is in cm; the DXF and seam list are in mm.
- Seams are described (both panels and edges) in the JSON; the DXF cannot carry them.
- DXF read-back: failed=none.
- The hem band is cut to the 890 mm waist and gathers the hem, blouson style.
- The fronts meet in one centre-front seam. Leaving it unsewn gives the zip opening, but the front band is one piece and must be split.
- No zip, pockets or yoke.
- Picture: F:\LedgerTools\garmentcode-lab\lab\out1109\workjacket\workjacket_panels.png.

## Into Marvelous Designer Personal
1. **Script, through our bridge (best).** gc_to_mdspec.py writes the format of tools/md/make_jacket_job.py. That writer, then write_pattern.py, put the 17-panel Jaeger jacket into Marvelous with 26 to 27 seam groups on 1 to 2 Oct (import_sewn results in the md-bridge outbox). Dry run today: 18 panels, all 35 seams on whole panel lines, job file written (md_job_workjacket.py). **Unverified**: not run in Marvelous; seam direction untested.
2. **DXF by hand.** Read on disk only: the Marvelous 2026.1.237 program file contains ImportDXF, DialogImportDXF and "This software supports DXF-AAMA or DXF-ASTM file formats". The API cannot reach it (measured 26 Oct), so it is a hand step and seams are sewn by hand. **Unverified**: whether Personal shows the menu item and takes our R12 mm file. A support FAQ snippet says Marvelous lacks DXF import. Its page returned 403 (support.marvelousdesigner.com article 47358309052313), so it was not read and is not evidence.
3. OBJ panels: not checked.

## Hours
19:26 to 19:40 (PowerShell clock), about 0.25 h. First pattern after 0.04 h, including the download, venv and install.

## Verdict
**Usable for the library's simple garments, not yet for 1990 work wear.**
- For: MIT core; exact sizes in seconds; seams described; output fits our proven Marvelous script route.
- Against: no openings, zips, pockets or yokes, so each period garment needs its own panel code; lengths are body fractions, so we need mm wrappers.
- Next: one bridge run of md_job_workjacket.py, then write_pattern.py, to see the seams arrive untwisted.
