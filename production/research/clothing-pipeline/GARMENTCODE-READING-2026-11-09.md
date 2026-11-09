# GarmentCode reading for n09-6's lab test (read 9 November 2026)

## Questions

1. GarmentCode's code licence, the dataset's licence, any non-commercial clause.
2. What it needs on Windows without an NVIDIA card: Python version; does draping need Warp/CUDA, or can patterns be exported alone.
3. Whether its patterns reach Marvelous Designer (DXF-AAMA, OBJ panels), and how.
4. The smallest 2 to 4 hour lab test that answers "does a parametric pattern library cut the cost of the next garment".

## What exists already (searched 9 Nov)

- production/research/wardrobe-at-scale/2-PATTERNS-BY-CODE.md and SUMMARY.md (1 Oct 2026): a full earlier reading. Its findings are re-checked below, not repeated.
- 4-MARVELOUS-MONTH.md (same folder): Marvelous API has ImportPatternJSON and CreatePatternWithPoints; DXF cannot be reached by API.
- F:/LedgerTools/garmentcode-lab (listed only): src-download/GarmentCode-2.0.2 (the pygarment 2.0.2 source, with assets/garment_programs, bodies, design_params, test_garmentcode.py) and venv/ (Python 3.10.6, empty: only pip, setuptools and pkg_resources; no pygarment dependencies installed). No output folder, so no test has been run.
- The allowlist (ledger-v2/research/license-allowlist.md) was searched for GarmentCode, MIT, CC BY and non-commercial: no GarmentCode entry (voices and others only; the long lines were omitted by the viewer and not read in full, unverified). A catalogue line for GarmentCode is therefore still needed if it is used.

## Answers

### 1. Licences

- **Code: MIT, "Copyright (c) 2024 Maria Korosteleva", no extra clauses.** Read in full in the local copy (F:/LedgerTools/garmentcode-lab/src-download/GarmentCode-2.0.2/LICENSE) and at https://github.com/maria-korosteleva/GarmentCode/blob/main/LICENSE (9 Nov 2026). setup.cfg of pygarment 2.0.2 also says "license = MIT".
- **The simulator is non-commercial.** NvidiaWarp-GarmentCode LICENSE.md, "NVIDIA Source Code License for Warp", read 9 Nov 2026 at https://raw.githubusercontent.com/maria-korosteleva/NvidiaWarp-GarmentCode/main/LICENSE.md: section 3.3 "The Work and any derivative works thereof only may be used or intended for use non-commercially"; "non-commercially" means "for research or evaluation purposes only"; section 3.2 requires derivative works to carry that limit. This is the only non-commercial clause found. It sits in the simulator, not in the pattern code.
- **Dataset GarmentCodeData: not confirmed.** Hugging Face returned 401 (9 Nov); the earlier note found ETH pages blocked and gave CC BY 4.0 versus CC BY-SA 4.0 as unresolved. UNVERIFIED. The lab test does not need the dataset.
- The README (github.com/.../README.md) fetched by raw link returned 404 and by the page link gave only "MIT license" and a news line; SMPL bodies' licence not confirmed here (earlier note: CC BY 4.0, unverified).

### 2. Running on Windows without NVIDIA

- Installation doc (https://github.com/maria-korosteleva/GarmentCode/blob/main/docs/Installation.md, read 9 Nov 2026): Python 3.9 (conda example `python=3.9`); dependencies numpy<2, scipy, pyyaml>=6.0, svgwrite, svgpathtools, psutil, matplotlib, CairoSVG, NiceGUI, trimesh, libigl, pyrender, CGAL; "this lib has some quirks on Windows" (cairo DLLs bundled in pygarment/pattern/cairo_dlls and added to PATH at run time). Warp is the authors' fork, "installed manually", and is only for simulation. The page says nothing about CUDA or CPU.
- setup.cfg (local copy, read in full): python_requires >=3.6, same dependency list. The lab venv is Python 3.10.6, not 3.9: whether all dependencies (notably cgal and libigl) install on 3.10 under Windows is UNVERIFIED (the PyPI cgal page would not load).
- **Pattern export needs no simulator.** The local test_garmentcode.py (read in full) builds MetaGarment(design, body), calls assembly(), and serializes with with_3d=False; it imports no Warp. Warp is referenced only in pygarment/data_config.py (8 hits for warp/cuda/device in the whole tree), not in the pattern code. Earlier note: Warp has a CPU path under Windows (not re-checked).
- Outputs, read in pygarment/pattern/wrappers.py (local): pattern JSON (panels, 3D placement, stitches), SVG (stitching lost), PNG, printable SVG and PDF. No DXF writer anywhere in pygarment/pattern (searched for dxf/aama, none). The flat-panel and draped OBJ meshes come from the data-generation side with Warp (earlier note, not re-read here: unverified in this pass).

### 3. Reaching Marvelous Designer

- DXF-AAMA: GarmentCode does not write it. Marvelous's own DXF import was not confirmed this session: help.marvelousdesigner.com did not resolve; a search found only CLO 3D and Style3D pages (same engine family: import dialog offers Standard DXF / AAMA / ASTM) and a 2011 Marvelous Designer 2 manual contents line for DXF-AAMA. UNVERIFIED for the current Marvelous.
- Routes that exist (all need an own converter script, untested): (a) JSON panels to Marvelous's API `ImportPatternJSON` or `CreatePatternWithPoints` (4-MARVELOUS-MONTH.md, documented there); (b) write DXF from the panel outlines (curves in GarmentCode are lines, quadratic and cubic Beziers and arcs, core.py; DXF needs them flattened or as splines) and import by hand in Marvelous, which is Jafar's or the bridge's step; (c) SVG panels into Marvelous by hand (format support unconfirmed).
- Stitch pairs travel only in the JSON, so (b) and (c) lose the seams and need sewing by hand.

### 4. Smallest lab test (2 to 4 hours, estimate)

Question to answer: does a parametric library make the next garment cheaper than hand-drawing it.
1. (30 min) Install pygarment's dependencies into the lab venv, no Warp. Pass criterion: test_garmentcode.py writes the T-shirt JSON, SVG, PDF. If cgal or libigl fail on 3.10 under Windows, record it and stop: that alone answers the Windows question.
2. (45 min) Generate three variants by editing design YAML only (t-shirt: length, sleeve, neckline), for two body-measurement files (mean_male, mean_female). Record the time per variant after the first.
3. (60 min) Write the smallest converter, JSON panels to Marvelous (route a), for one garment; check that panel sizes, seams and measurements match the SVG.
4. (30 min) Measure against the hand method: hours to a first sewn garment in Marvelous from pattern, against the recorded hours for an existing LEDGER shirt or trousers (cost table already in the project, not read here).
5. Write the result as hours per garment with and without the library, plus faults.
Out of scope: tailored garments (the earlier note found no jacket, coat, front opening, buttons, pockets or layers in the garment programs; list of programs re-confirmed by the local folder: bands, bodice, circle_skirt, collars, godet, meta_garment, pants, skirt_levels, skirt_paneled, sleeves, tee), the simulator, the dataset.

## Recommendation

Run the test as steps 1 to 4 only if the aim is simple crowd garments (shirts, plain skirts, basic trousers); the library cannot make 1990 tailoring (jackets, coats), so a pass says nothing about those. The code is MIT and usable; the draping simulator must not be used. Stop at step 1 if the dependencies do not install.

## Not reached or unverified

- Hugging Face dataset page (401); dataset licence unverified.
- GarmentCode README by raw link (404); help.marvelousdesigner.com (host not found); PyPI cgal page (failed to load).
- Marvelous's current DXF import list: unverified.
- Whether cgal/libigl install on Python 3.10 under Windows: unverified.
- Allowlist's long lines not read in full.
