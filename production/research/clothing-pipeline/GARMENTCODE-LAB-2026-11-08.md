# GarmentCode lab test, item n09-6 (8 Nov 2026)

Within DECISIONS 8 Nov 20:40: pygarment (MIT) only, no simulator; nothing barred installed or imported. All files under F:\LedgerTools\garmentcode-lab (278 MB: venv 250, source 27, outputs 1). Nothing committed. No GUI app opened.

## Installed (all with --no-deps, licence read on PyPI first, 8 Nov)
pygarment 2.0.2 MIT; source archive v2.0.2 from GitHub, MIT (repo licence via GitHub API). numpy 1.26.4 BSD-3; scipy 1.14.1 BSD-3; svgwrite 1.4.3 MIT; svgpathtools 1.8.0 MIT; PyYAML 6.0.3 MIT; psutil 7.2.2 BSD-3; ezdxf 1.4.5 MIT; pyparsing 3.3.3 MIT; typing_extensions 4.16.0 PSF-2.0; fonttools 4.60.1 MIT. Python 3.10 venv. Not installed: CairoSVG, cgal, Warp fork, libigl, trimesh, pyrender, nicegui, matplotlib (would pull in Pillow, whose HPND licence is off the allowed list). Unverified: numpy/scipy Windows wheels bundle OpenBLAS and the GCC runtime, whose licences were not read.

## What worked, what did not
- The PyPI wheel is mis-packaged: its modules import `pygarment.*` but install as top-level `garmentcode`/`pattern`, and `pygarment/data_config.py` is missing. Fix: run from the v2.0.2 source tree (path put first by lab/gcpath.py).
- `pattern/wrappers.py` imports cairosvg and matplotlib at module top, and every garment pulls it in; its `serialize()` always renders a PNG through CairoSVG. Fix: two inert placeholder modules of ours (lab/stubs; they raise if called, and never were), JSON written by `core.BasicPattern.serialize`, SVG by `get_svg().save()` (svgwrite). So the pattern code runs without any barred package; no PNG or PDF output.
- The repo's own garment programs (MetaGarment: Shirt, Pants, sleeves, collars, bands) on its mean_male body (height 1,789, chest 1,028, waist 890 mm) built all four first try, none self-intersecting.
- Limits found: lengths are fractions of the body, not mm (first try: trousers to 90 mm below the floor, shirt 542 mm long), retuned once; fronts are sewn shut (shirt centre front 595 mm seam, jacket 334 mm below the V): no opening, placket, buttons, pockets, yoke or two-piece collar; "shirt collar" is the Turtle band; trousers waist has no ease and the front/back hip seam differs 25 mm; jumper hem band is 45 to 75 mm shorter than the body hem (gathers, as a rib).

## Patterns (flat, mm; outputs F:\LedgerTools\garmentcode-lab\lab\out\<name>\: _specification.json, _pattern.svg, .dxf, _seams.json)
| Garment | Panels / seams | Key measurements |
|---|---|---|
| Trousers | 6 / 24 | outseam 1,093 (leg 1,044 + band 49); inseam 700; waist 890; hem 623 per leg |
| Collared shirt | 16 / 30 | back length 762; chest 1,172; sleeve 511 + cuff 57 = 568 |
| Crew-neck jumper | 14 / 28 | back length 646 (with band); chest 1,131; sleeve 568 with cuff |
| Working jacket (lapel) | 12 / 23 | back length 735; chest 1,233; sleeve 568 |
Inseam 700 is short for a 1,789 mm man: the pattern's crotch depth follows the body file's (about 344 mm waist to crotch), deeper than a tailored rise.

## Editing in code: sleeve +30 mm (lab\out_sleeve30)
One argument (`build_patterns.py out_sleeve30 30`). Only the 4 sleeve panels changed in each top (bodies, armholes, cuffs, collars and the trousers unchanged; seams still match within 1.1 mm). But the panels grew 25.1 mm, not 30: the sleeve parameter is a fraction of (arm length minus armhole opening, about 95 mm), not of the arm. Exact mm edits need that divisor in our wrapper.

## DXF converter and check (lab\convert_dxf.py, validate_dxf.py)
R12 DXF, one block per panel, outline as a closed polyline on AAMA layer 1 (sew line, no seam allowance), grain line layer 7, Piece Name / Quantity / Size text, "Units: METRIC" (R12 cannot carry $INSUNITS); curves sampled every 5 mm. Seams in the side JSON (panel, edge, length, polyline vertex range, and the "right_wrong" flag on lapel seams). Read back with ezdxf: all 48 panels in both sets pass (block count = spec, one insert each, closed, no self-crossing, every spec corner within 0.02 mm of the outline, perimeters within 0.003% of exact curve length, trouser outseam 1,092.8 mm in range); failed=none. A tampered copy (one outline opened, one panel removed) failed both, as it should. Not checked: that Marvelous accepts these files (no GUI opened).

## Time (PowerShell Get-Date, wall clock)
Step 1 install 20:30 to 20:34 (0.05 h); step 2 patterns, retune and edit 20:34 to 20:38 (0.07 h); step 3 converter and checks 20:35 to 20:39 (0.06 h, overlapping); report 0.05 h. Total about 0.2 h of the 3 h cap.

## Verdict: yes, worth a Marvelous import trial
Patterns-as-code runs on our allowed licences, rebuilds four garments in seconds, an edit touches only the panels it should, and our DXF reads back exact. The trial must answer what this lab could not: whether Marvelous takes our R12 file at mm scale, and how the seams from the side JSON get sewn there. Against it: the stock programs lack openings, plackets, pockets and real collars, so period garments need our own panel code on pygarment's API, and length parameters need mm wrappers.
