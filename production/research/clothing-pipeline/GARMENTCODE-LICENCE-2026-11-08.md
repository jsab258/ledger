# GarmentCode (pygarment) licence reading, item n09-6

Read 8 Nov 2026 (all links below read on that date). Method: pages fetched through a summarising fetch tool, not a raw file save, so every quote is the tool's rendering and the exact text of the licences below should be re-read at adoption (marked where it matters). Nothing installed or downloaded. No project conclusion drawn; each question ends with the allowlist line and a status.

Allowlist read: ledger-v2/research/license-allowlist.md (8 Nov 2026). Tailor scan: none found in production/research/field-scans/ (only HAIR and CARS scans exist).

## The allowlist lines that bear on this

- Process 2: "New tool adoption requires a decision record citing the weights license."
- Process 1: "Every asset and generated output carries a license tag; untagged fails the license gate."
- SHIP-SAFE 9: garments made in Marvelous Designer on his own plan; "no CLO avatar, sample garment, pattern or trim in anything shipped".
- SHIP-SAFE 2: "CC BY 4.0 for clothes and their accessories ... only, each maker credited ... never one marked NoAI".
- SHIP-SAFE 1, Piper: the active fork "is GPL-3.0, acceptable for generated audio, check before embedding code" (the only line treating a copyleft tool licence; it is about generated output, a precedent in kind, not a rule for this tool).
- The allowlist has no line on pattern-drafting tools, on cloth simulators, or on non-commercial tool licences (not-listed means no allowlist line either way).

## Q1. Code licence, pygarment licence, dataset

Repo home: https://github.com/maria-korosteleva/GarmentCode (the name "maywalt" in the brief is wrong; the owner is maria-korosteleva). Public, main branch. Read 8 Nov 2026.

- Repo LICENSE (https://raw.githubusercontent.com/maria-korosteleva/GarmentCode/main/LICENSE): standard MIT text, "Copyright (c) 2024 Maria Korosteleva", full grant to use, copy, modify, sell; keep the notice in copies. Read in full.
- PyPI pygarment 2.0.2, released 18 Apr 2025: licence field MIT (https://pypi.org/project/pygarment/). setup.cfg in the repo also says "license = MIT" and "version = 2.0.2" (https://raw.githubusercontent.com/maria-korosteleva/GarmentCode/main/setup.cfg). The PyPI sdist/wheel's bundled licence file was not opened (unverified; the metadata field is MIT).
- Dataset GarmentCodeData v2 (released 4 Sep 2024, https://doi.org/10.3929/ethz-b-000690432): the ETH Research Collection record lists "Creative Commons Attribution 4.0 International" (https://www.research-collection.ethz.ch/handle/20.500.11850/690432). File list and sizes not obtained (the page returned 429 for the files). v1 (https://doi.org/10.3929/ethz-b-000673889) licence not read: unverified. The project page says 115,000 data points (https://igl.ethz.ch/projects/GarmentCodeData/); it states no licence.
- Dataset needed for writing our own patterns? The pip package ("pip install pygarment installs the core library for writing garment programs", docs/Installation.md) is the pattern library; the code read (pygarment/pattern/core.py, wrappers.py) imports no dataset. The dataset and body samples are for data generation/simulation (system.template.json paths 'datasets_path', 'body_samples_path'). The docs read do not say the library needs the dataset: not needed for pattern writing on the evidence read; confirm at the lab test.

Allowlist status:
- Code and pygarment, MIT: no allowlist line for tool code licences; MIT matches the kind of licence the allowlist accepts for tools (Kokoro Apache 2.0, Chatterbox MIT, TRELLIS MIT). Allowed in kind; needs the Process 2 decision record. No ruling needed on the licence text itself.
- Dataset CC BY 4.0: line SHIP-SAFE 2 allows CC BY 4.0 for clothes and accessories only, with credit. Whether dataset garments (simulated meshes/patterns) count as "clothes" for that line is not decided by the line's words. Only matters if the dataset is used; not needed per above. Status: not needed; if wanted, needs his ruling.

## Q2. Run-time dependencies and licences

Source: install_requires in setup.cfg (read in full, URL above) and docs/Installation.md (https://raw.githubusercontent.com/maria-korosteleva/GarmentCode/main/docs/Installation.md), 8 Nov 2026. pyproject.toml holds only the build-system (setuptools>=42).

The core install list: pyyaml>=6.0, numpy<2, scipy, svgwrite, svgpathtools, psutil, matplotlib, CairoSVG, nicegui, trimesh, libigl, pyrender, cgal. Licences as read:

| Package | Licence | Source read 8 Nov 2026 |
|---|---|---|
| svgwrite | MIT (requires Python >=3.6) | https://pypi.org/project/svgwrite/ |
| svgpathtools | MIT (>=3.8) | https://pypi.org/project/svgpathtools/ |
| trimesh | MIT (>=3.10) | https://pypi.org/project/trimesh/ |
| pyrender | MIT | https://pypi.org/project/pyrender/ |
| nicegui | MIT (>=3.11 on its current release) | https://pypi.org/project/nicegui/ |
| libigl | MPL 2.0 (>=3.8; Windows x86-64 wheels cp38 to cp312) | https://pypi.org/project/libigl/ |
| CairoSVG | LGPL-3.0-or-later (>=3.10) | https://pypi.org/project/CairoSVG/ |
| cgal (Python bindings) | PyPI licence field empty; classifier "GPLv3+"; Windows win_amd64 wheels exist for the 5.5 builds, 6.0.1 files not seen | https://pypi.org/pypi/cgal/json (only the first 100,000 of 485,174 characters read) |
| numpy, scipy, pyyaml, psutil, matplotlib | licences not read (unverified) | none |

Cloth simulator (needed only for simulated drape/meshes, not for patterns):
- Docs say "Install the NVIDIA Warp fork (NvidiaWarp-GarmentCode) manually" (docs/Installation.md). Fork: https://github.com/maria-korosteleva/NvidiaWarp-GarmentCode, based on NVIDIA Warp v1.0.0-beta.6, changes all in the XPBD solver.
- Fork licence: "NVIDIA Source Code License for Warp" (https://github.com/maria-korosteleva/NvidiaWarp-GarmentCode/blob/main/LICENSE.md). Section 3.3: "The Work and any derivative works thereof only may be used or intended for use non-commercially." Non-commercially means "for research or evaluation purposes only"; NVIDIA and affiliates may use commercially. The README states the licence currently allows only non-commercial use and that the authors will follow later NVIDIA revisions. Read via the fetch tool's rendering of the file; the section wording should be re-read verbatim before any decision record.
- Current upstream Warp (PyPI warp-lang) is Apache-2.0 (https://pypi.org/project/warp-lang/); the fork is based on an older version under the non-commercial terms above. Whether upstream's newer Apache code contains the fork's solver changes: not so (the changes are the fork's); unverified whether the pattern code can run on upstream Warp.
- CUDA: the fork's README lists "CUDA Toolkit of version 11.5 or higher" as a prerequisite; without CUDA_PATH it builds "without CUDA support" (fork README, same page). The fork's page does not document a CPU-only run (unverified). Upstream Warp states that Windows x86-64 wheels support CPU and CUDA, CUDA needs an NVIDIA driver and Turing or newer GPU, and the page mentions no AMD support. Our RX 6700 is AMD: GPU simulation is not available on it on the evidence read; CPU execution of this fork is unverified. The only documented environment (issue #17, https://github.com/maria-korosteleva/GarmentCode/issues/17): Ubuntu 22.04, Python 3.9 conda, RTX 4080, CUDA 12.2.
- Build on Windows needs Visual Studio 2019 or later, Git LFS, symlinks enabled (Developer Mode), per the fork README.
- NoAI clause: none found in the MIT licences, the fork licence (as rendered) or the dataset record. No "NoAI" text seen in any page read (not searched in the dataset's own terms files, which were not reached).
- Non-commercial clause: yes, the Warp fork (above). Nothing else non-commercial found.

Allowlist status:
- MIT/MPL deps: no line; same kind as accepted tool licences. Allowed in kind.
- CairoSVG (LGPL) and cgal (GPLv3+): not on the allowlist. The nearest line is Piper's ("GPL-3.0, acceptable for generated audio, check before embedding code"), a precedent for using a GPL tool to make output, not text covering this. These are used inside a dev tool that writes pattern files; nothing is embedded in the game. Needs his ruling (or a decision record under Process 2) on whether tool-side GPL/LGPL is accepted when only output ships.
- Warp fork (non-commercial, research or evaluation only): the allowlist's NEVER SHIP 1 bars non-commercial weights output (XTTS-v2, F5-TTS) by analogy, but no line covers a non-commercial simulator whose output is a drape mesh. A 2 to 4 hour lab test is arguably evaluation; shipping anything made with it is the open point. Needs his ruling. The fork cannot be used for anything shipped on the allowlist's analogy unless he rules otherwise.
- CUDA/NVIDIA: not a licence matter; a hardware fact (AMD card).

## Q3. Outputs and Marvelous Designer / Blender

From pygarment/pattern/core.py and wrappers.py read raw (https://raw.githubusercontent.com/maria-korosteleva/GarmentCode/main/pygarment/pattern/core.py, .../wrappers.py), 8 Nov 2026:
- JSON: BasicPattern.serialize writes `<name>_specification.json` with json.dump of the spec.
- SVG: wrappers.py writes `<name>_pattern.svg` (svgwrite).
- PNG: pattern picture and a matplotlib 3D view.
- PDF: only when `with_printable` is true, via cairosvg.svg2pdf (needs CairoSVG; on Windows its DLLs are in pygarment/pattern/cairo_dlls and must be on PATH, docs/Installation.md).
- DXF: no writer found in core.py or wrappers.py. Other pygarment files were not listed in full (the directory listing was cut off, "View all files"), so a DXF writer elsewhere is unverified, but the README and CHANGELOG mention none (README: "SVG, DXF, OBJ: Not mentioned").
- OBJ/meshes: no writer in those two files. The simulation step produces meshes; its formats were not read (unverified); the dataset's file formats were not reached (429).
- Marvelous Designer reading it: MD imports DXF (DXF-AAMA); the library writes no DXF in the files read, so a pattern cannot go straight in. SVG and JSON are not MD import formats to our knowledge, not checked against MD docs here (unverified). Blender reading it: no native reader for these specs (unverified, not checked); an SVG can be imported as curves in Blender, not checked here.
- README mentions "Running Old Maya+Qualoth tools" (a separate older simulator, Qualoth is commercial Autodesk Maya software; its licence not read).

Allowlist status: no line covers file formats. Process 1 applies: each output needs a licence tag; MIT code places no claim on output in the MIT text read, and the dataset has its own CC BY 4.0. Allowed in kind; whether a pattern from the Warp-fork path carries NVSCL conditions is for his ruling.

## Q4. Python and platform

- pygarment on PyPI: "Requires-Python >=3.6", classifier "Operating System :: OS Independent" (https://pypi.org/project/pygarment/).
- Repo manual setup: "conda create -n garmentcode python=3.9" (docs/Installation.md); the only documented working environment is Python 3.9 on Ubuntu (issue #17).
- Dependencies' floors vary: CairoSVG >=3.10, nicegui >=3.11 (current releases), trimesh >=3.10; libigl Windows wheels go to cp312. A single Python version that satisfies the latest of all and the repo's 3.9 was not tested (unverified; older releases may fit 3.9).
- Windows: a path exists (cairo DLLs shipped, Warp fork has Windows build steps, libigl and cgal have win_amd64 wheels). No page read says the whole stack was run on Windows (unverified).

Allowlist status: not a licence question; no line.

## Q5. Summary of statuses

1. GarmentCode and pygarment code, MIT: no explicit allowlist line; same kind as listed MIT tools; needs the Process 2 decision record. Allowed in kind.
2. Dataset, CC BY 4.0: not needed for writing patterns (on evidence read); if ever used, whether it counts as "clothes" for SHIP-SAFE 2 needs his ruling.
3. Warp fork, non-commercial: needs his ruling; also needs NVIDIA CUDA, which the AMD RX 6700 lacks.
4. cgal (GPLv3+) and CairoSVG (LGPL): no allowlist line; needs his ruling (Piper line is only an analogy).
5. Other deps, MIT or MPL: allowed in kind; numpy, scipy, pyyaml, psutil, matplotlib licences unread.
6. Outputs: JSON spec, SVG, PNG, optional PDF; no DXF or OBJ writer found in the two core files read; direct Marvelous Designer import not possible on that evidence.

## Not reached or unverified

- The dataset's file list, formats, sizes (ETH page returned 429); v1 dataset licence; any dataset terms file.
- cgal 6.0.1 wheel list and Windows availability of the current version; licences of numpy, scipy, pyyaml, psutil, matplotlib.
- The pygarment sdist's own licence file; the rest of the pygarment folder (other writers, e.g. DXF); simulation output formats.
- Whether the Warp fork runs on CPU or on AMD; whether the whole stack runs on Windows.
- The fetch tool summarised pages; licence wording to be re-read in the raw file at adoption (fork LICENSE.md especially).
- Marvelous Designer's and Blender's own import documentation (not read for this note).
