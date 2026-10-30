# Driving Marvelous Designer 2026.1 by script (26 October 2026)

The question: how far can Marvelous Designer (MD) be driven by Python script, so the operator works through files and scripts instead of screenshots and clicks? The aim is one garment set (zip-front rain jacket, plain jumper, jeans) on our own MetaHuman body (`F:/LedgerTools/bodies/MH_TomL1/`, FBX, A-pose), exported as OBJ or FBX for Blender.

The installed program is **Marvelous Designer Personal 2026.1.237** (file version 2026, 1, 237, 58920, read from the exe on this PC on 26 October 2026). All web sources were read on **26 October 2026**. "UNVERIFIED" means no CLO page says it; "measured" means checked on this PC without opening MD.

## Short answers

1. **Yes, Personal has the Python API.** CLO's plans page says every plan has every feature, and its "Pipeline" row includes "scripting support". The documented menu path is Main Menu ▶ Script ▶ Python. That menu was renamed **Plugins** in 2025.2, so in 2026.1 the editor is probably Plugins ▶ Python Editor (UNVERIFIED in CLO's docs).
2. **No documented way runs a script without a click.** There is no documented command-line flag, start-up script, auto-run folder or server mode. Two documented routes exist, both needing a person to start them: the Python editor's Run button, and a .py file registered as a plug-in (Plug-in Manager), which is then one click. The 2026.1 program does contain an **undocumented "Headless API"** that takes command-line options and a "run python file" option. It needs CLO-issued access keys tied to an account sign-in (UNVERIFIED; see below). Community projects open a local socket from a one-click plug-in; this is unofficial.
3. **Every step we need has a documented function**, in the modules `import_api`, `pattern_api`, `fabric_api`, `utility_api` and `export_api`, with option types in `ApiTypes`. Gaps are listed below: no zipper creation, no weld setting on export, no fabric-physics setters except through fabric files, and no unit stated for pattern coordinates.
4. **The only official examples are on one page**, the developer site's "API Scenario": four short scripts. **CLO has no official GitHub sample repository.**
5. **No Personal-plan limit was found** on the API, export formats or avatar import. The terms' limits on reverse engineering, automated extraction and access "by any means other than the interface we provide or authorize" are a licence question for Jafar before any socket bridge is used.

## 1. Is scripting in the Personal plan, and where is it?

- The plans page says "All plans have full access to every feature in Marvelous Designer". It lists Personal beside every Enterprise plan, and its Pipeline row reads "Import/export, DCC integrations, LiveSync, and scripting support." Source: https://www.marvelousdesigner.com/pricing (read 26 Oct 2026; section expanded in the page).
- The developer docs give the location "Main Menu > Script > Python". The editor's buttons are New Document, Save, Save As, Run Script, Source, Open, Script Editor and Console Log. Source: https://developer.marvelousdesigner.com/python.html (read 26 Oct 2026).
- CLO's support article "Python Script" (dated 31 October 2025) gives the same path, plus Main Menu ▶ Script ▶ API Reference, and points to the developer site. Source: https://support.marvelousdesigner.com/hc/en-us/articles/47358277921177-Python-Script (read 26 Oct 2026).
- The 2025.2 release notes (November 2025) include "Change the Script menu to Plugins." Source: https://support.marvelousdesigner.com/hc/en-us/articles/47358120307353-Marvelous-Designer-2025-0-2025-1-2025-2-New-Feature-List (read 26 Oct 2026). **So the exact 2026.1 menu path is UNVERIFIED.** One third-party README gives "Main Menu → Plugins → Python Editor" (https://github.com/matty/marvelous-designer-plugins, read 26 Oct 2026).
- Measured: the installed program contains the menu labels "Python Editor", "API Reference" and "Plug-in Manager". It ships Python 3.11 (`python311.dll` and `python311.zip` in the install folder). Its library sits in `C:\Users\Public\Documents\MarvelousDesigner\Configuration\python311`, with pip 24.0 and setuptools 65.5.0. The API changelog adds "the built-in pip module for Windows Python environments" in 2025.1.107. Source: https://developer.marvelousdesigner.com/changelog.html (read 26 Oct 2026).
- The API docs call themselves "Marvelous Designer API 0.1 documentation". Their changelog stops at MD 2025.1.201, so **the docs may lag 2026.1**. Two third-party projects say the running program exposes more calls than the docs list (one counts 688), and that the live program, not the docs, is the authority (UNVERIFIED).

## 2. Can a script run without clicking?

**What CLO documents**
- Python plug-ins: "Open Plugin tab → Plug-in Manager", click "+ ADD", pick the .py file, name it and choose its place. It then appears in the Plugin tab and under Main Menu ▶ Settings ▶ Plug-in. Source: https://developer.marvelousdesigner.com/register.html (read 26 Oct 2026). The changelog for 2025.1.107 adds "a capability to add .py (Python file) as a plugin via the plugin manager".
- None of the six developer pages (index, changelog, list, optiontype, python, register, scenario) mention a command-line flag, a start-up script, an auto-run folder, headless running or a server mode (all read 26 Oct 2026).
- In a community thread from about 2022, CLO staff answered "There is no headless Marvelous Designer session at the moment". Source: https://support.marvelousdesigner.com/hc/en-us/community/posts/48272742764441 (read 26 Oct 2026; four years old).
- The `REST_API` module only **sends** HTTP requests (`CallbackRestRequest`, `CallbackRestMultiRequest`, `CallRESTPut`). It is not a server. Source: https://developer.marvelousdesigner.com/list.html (read 26 Oct 2026).

**What is in the 2026.1 program but undocumented (measured; UNVERIFIED, do not rely on)**
- The plug-in list lives at `C:\Users\Public\Documents\MarvelousDesigner\Plugins\pluginSettings.json`. Today it holds `{"plugins": [], "version": 2}`.
  - The program's messages name each entry's fields: an absolute .py path (`m_PlugInFileName`) and a menu (`m_BaseMenuTreeByObjectName`).
  - They also name folder entries (`m_SourcePath`) that register every .py in a folder as a submenu, and a `defaultPluginFolders.txt`.
  - So a plug-in could be listed by writing this file while MD is closed. It still needs one click to run. The Laboon2501 project (below) does exactly this.
- The program contains a "Headless API" with command-line options:
  - `headless`: "Run python file at <file>."
  - `headlessconfig`: "Register an access key and a secret key."
  - `accesskey`, `secretkey`, `pw` ("User Password"), `months` ("Headless Key periods"), `deleteKey`
  - `remote`: "Executed in a remote environment."
  - `headlesslog`, `performlog`
  - It writes a log at `Headless/headless_log.txt` and signs in through a step named `HEADLESS_SIGNIN`.
  - Nothing public explains it; searches of CLO's sites found nothing. It looks like it needs CLO-issued keys and an account password, which Claude must not enter. **Whether Personal may use it, and whether it works, is UNVERIFIED.**
- The program also has start-up argument strings `-python` and `.py` (beside `-GoZ`), and API functions `RegisterPythonScript` and `RegisterPythonScriptFolder` that the docs do not list. Their meaning is UNVERIFIED.
- **How this was measured, and a caution:** readable text was pulled out of the installed exe and the update manifest. Nothing was run, and the program was not decompiled or opened. CLO's General Terms forbid reverse engineering, "data mining or similar data gathering and extraction methods in connection with the Services and Software", and access "by any means other than the interface we provide or authorize" (https://legal.clo-set.com/modal-tou-general, "Use of the Services" (c)(v), (c)(viii), (d)(vi); last updated 30 March 2026; read 26 Oct 2026). The text extract was deleted after reading. **Recommendation: dig no further and use no undocumented flag without CLO's word.**

**What others do (unofficial, untested here)**
- matty/marvelous-designer-plugins: a .py listener run once from the Python editor (or one click on its plug-in entry) binds 127.0.0.1:5121 on MD's main thread. An outside MCP server then sends scripts. Source: https://github.com/matty/marvelous-designer-plugins (README read 26 Oct 2026). It warns that it runs arbitrary Python over an unauthenticated loopback port.
- Laboon2501/MarvelousDesigner-MCP: a registered plug-in, `md_start_listener`, opens 127.0.0.1:7421 using a Windows timer. It was "Verified" on "Windows, MD 2026.0.315, embedded Python 3.11.8"; other versions are unverified. Source: https://github.com/Laboon2501/MarvelousDesigner-MCP (README read 26 Oct 2026). It is based on ysk424/marvelous-designer-mcp.
- Both still need **one click per MD session** to start the listener. Whether this is "the interface we provide or authorize" under the General Terms (c)(viii) is a licence question.

## 3. The functions for each step (as documented)

Source for all signatures: https://developer.marvelousdesigner.com/list.html (read 26 Oct 2026; all 593 signatures read, and docstrings read for the functions named here). Module names and imports are from https://developer.marvelousdesigner.com/scenario.html (read 26 Oct 2026). Option fields are from https://developer.marvelousdesigner.com/optiontype.html (read 26 Oct 2026). Most functions also have a `...W` twin for Unicode paths.

**Start**
- `utility_api.NewProject() -> None`: "Clear the current garment and begin a new garment".

**Import our body (avatar)**
- `import_api.ImportFBX(_filePath : str, _options : ImportExportOption) -> bool` and `import_api.ImportOBJ(_filePath : str, _options : ImportExportOption) -> bool`. With options given, they import "not allowing user for selecting options in Import Dialog".
- `import_api.ImportFile(filePath : str, _options : ImportExportOption) -> bool`: "Load File(obj, fbx, gltf) by obj type ... loadObjectType 0 : avater, 1 : trim". Its docstring says it "will show up the dialog", so prefer ImportFBX/ImportOBJ.
- `import_api.ImportAvatar(_avtPath : str, _opt : ImportExportOption) -> bool` is for MD's own .avt avatars.
- The import-side `ApiTypes.ImportExportOption` fields are:
  - `ImportObjectType:int`, `scale:float`
  - `axisX/axisY/axisZ:int`, `bInvertX/Y/Z:bool`
  - `bAddArrangementPoints:bool`, `bAutoCreateFittingSuit:bool`
  - `bAutoTranslate`, `bAdd`, `translationValueX/Y/Z:float`
  - `bCreateAnimation`, `bCreateCacheAnimation`, `bMoveGarment`, `bTrace2DPatternsUVMap`
- **Units:** the docs never define `scale`. The `AutoHang` docstring says "if the file is in cm, scale should be 10". That implies MD works in millimetres and our Unreal FBX (centimetres) needs `scale = 10.0`. This is **UNVERIFIED for ImportFBX**, so check by measuring the imported height.
- The manual says FBX files carry their units and auto-scale reads them, while OBJ files do not (Register Accessory article, unit passages only: https://support.marvelousdesigner.com/hc/en-us/articles/47358145246361-Register-Accessory-Hair-Shoes-Glasses-Earring-Hat-zacs-Ver-2025-0, read 26 Oct 2026).
- Arrangement points are generated on import "only when imported OBJ is either in T or A pose" (https://support.marvelousdesigner.com/hc/en-us/articles/47358223288601-3D-File-OBJ-Import-Export, read 26 Oct 2026). Our body is in A-pose. The FBX import has the same option for humanoid avatars (https://support.marvelousdesigner.com/hc/en-us/articles/47358232885017-3D-File-FBX-Import-Export, read 26 Oct 2026).
- Aside: since 2025.2, MD can import a MetaHuman directly from its Body and Head `.dna` files (File ▶ Import ▶ DNA, with unit/scale and auto arrangement points). This is GUI only; no API function lists `.dna`. Source: https://support.marvelousdesigner.com/hc/en-us/articles/51752244831897-MetaHuman-DNA-Importer (read 26 Oct 2026).
- Avatar collision: `utility_api.SetAvatarProperties(_avatarIndex : int, avatarPropertyMap : map[str, str]) -> None`, with keys such as `SkinOffsetMM`, `KineticFriction` and `StaticFriction`.

**Make a 2D pattern from points**
- `pattern_api.CreatePatternWithPoints(_points : list[tuple[float, float, int]]) -> int`. Each tuple is (x, y, vertex type), where the type is 0 straight, 2 spline curve or 3 Bezier curve.
- `pattern_api.CreateInternalShapeWithPoints(_patternIndex : int, _points : list[tuple[float, float, int]], _isClosed : bool) -> int`
- `pattern_api.CreateBaseShapeWithPoints(...)` has the same shape.
- `pattern_api.SetPatternPieceName(_patternIndex : int, _patternName : str) -> None`
- `pattern_api.SetPatternPiecePos(_patternIndex : int, _x : float, _y : float) -> None`
- Read back with `pattern_api.GetPatternCount() -> int`, `GetPatternInformation(patternIndex : int) -> str` (JSON), `GetLineLength(_patternIndex : int, _lineIndex : int) -> float` and `GetBoundingBoxOfPattern(...)`.
- The coordinate unit is **not stated** in the docs. One third party measured millimetres (UNVERIFIED).
- Whole-pattern documents: `pattern_api.ExportPatternJSON(_path : str) -> bool` and `ImportPatternJSON(_path : str) -> bool`. The JSON schema is undocumented.

**Arrange around the avatar**
- `pattern_api.GetArrangementList() -> list[map[str, str]]` gives each point's name, type, offset x/y/z and orientation.
- `pattern_api.SetArrangement(_patternIndex : int, _arrangementIndex : int) -> None`
- `pattern_api.SetArrangementPosition(_patternIndex : int, _positionX : int, _positionY : int, _offset : int) -> None`
- `pattern_api.SetArrangementOrientation(_patternIndex : int, _orientation : int) -> None`
- `pattern_api.SetArrangementShapeStyle(_patternIndex : int, _shapeStyle : str) -> None`, where the style is "Flat" or "Curved".
- `pattern_api.GetArrangementOfPattern(...)`
- No free 3D move or rotate of a piece is documented.

**Sew two edges**
- `pattern_api.AddSeamlinePairGroup(_patternAIndex : int, _lineAIndex : int, _patternBIndex : int, _lineBIndex : int, _directionA : bool, _directionB : bool) -> bool`. The directions are true forward, false backward.
- Two overloads add inner-shape indices (`_childIndex`, or `_childAIndex` and `_childBIndex`).
- The docstring says it returns the "name of sewing group" while the signature says bool, so the docs disagree.
- Whole lines only; partial sewing is not documented.
- Read back with `GetSeamlinePairGroupCount() -> int` and `GetSeamlinePairGroupListInPattern(_patternIndex : int) -> list[int]`.
- **Zipper:** only zipper-*style* setters are listed (`SetZipperStyle...`). No function creates a zipper (UNVERIFIED gap for the rain jacket).

**Fabric and particle distance**
- `fabric_api.AddFabric(inputFilePath : str) -> int` takes a 'zfab' (MD file) or 'jfab' (JSON) path.
- `fabric_api.AssignFabricToPattern(_fabricIndex : int, _patternIndex : int, _assignOption : int) -> bool`. The option is 1 current colourway, 2 all colourways unlinked, or 3 all linked.
- `fabric_api.ExportFabric(filePath : str, index : int) -> str` writes .jfab or .zfab. `CombineZfab(_filePath, _baseZfabPath, _targetZfabPath)` takes the physical properties from one fabric file and the image from another.
- **No setter for stretch, bending or density is documented**: physical properties travel only inside zfab/jfab files. PBR look setters exist (roughness, metalness, normal map and so on).
- `pattern_api.SetParticleDistanceOfPattern(_patternIndex : int, _length : float) -> None`, `SetParticleDistanceOfPatterns(_length : float) -> None` and `GetParticleDistanceOfPattern(...)`.
- The manual gives particle distance in mm, range 0.8 to 700, "20mm when making a Garment" and "under 5mm" once finished. Source: https://support.marvelousdesigner.com/hc/en-us/articles/47358268602777-Particle-Distance-Setting (read 26 Oct 2026).
- `pattern_api.SetMeshType(_patternIndex : int, _meshType : str) -> None` takes "Triangle" or "Quad". The manual says thickness exports only from Quad meshes (OBJ and FBX articles above).

**Simulate**
- `utility_api.Simulate(_steps : int) -> bool`: "how many steps(=frames) to simulate".
- `utility_api.SetSimulationQuality(_quality : int, _simulationMode : int) -> None`. Quality is 0 Normal, 1 Animation, 2 Fitting or 3 FAST(GPU); mode is 0 CPU or 1 GPU.
- `utility_api.SetSimulationTimeStep(_timeStep : float)` (default 0.03333 s) and `SetSimulationNumberOfSimulation(_numberOfSimulation : int)` (substeps 1 to 50).
- There are also setters for CG iterations, gravity, air damping, self-collision and layer-based collision.
- `utility_api.ResetClothArrangement() -> None` restores the cloth to its loaded shape.
- `utility_api.GetClothPositions(positions : list[float]) -> None` fills x, y, z for each cloth vertex, which allows checks without pictures.
- One third party reports that `Simulate` returns True for any input and that `Simulate(1)` leaves the garment flat (UNVERIFIED).

**Export for Blender**
- `export_api.ExportOBJ(_filePath : str, _options : ImportExportOption) -> list[str]` and `export_api.ExportFBX(_filePath : str, _options : ImportExportOption) -> list[str]`. With options given, there is no dialog.
- Save the project with `export_api.ExportZPrj(_filePath : str) -> str`.
- The export-side `ImportExportOption` fields are:
  - `bExportGarment`, `bExportAvatar`
  - `bSingleObject`: false means separate objects (the GUI's "Multiple Objects").
  - `bThin`: false means thick.
  - `bUnifiedUVCoordinates`, `bCreateUnifiedTexture`, `unifiedTextureSize`
  - `bIncludeInnerShape`, `bIncludeHiddenObject`
  - `scale`, `axisX/Y/Z`, `bInvertX/Y/Z`
  - `bSaveInZip`, `bExportAnimation`, `bEmbedded`, `bMetaData`, `bSaveColorWays`
- CLO's own example sets `bExportGarment = True`, `bCreateUnifiedTexture = True`, `bSingleObject = True` and `scale = 1.0`, then calls `export_api.ExportOBJ("C:/output/file.obj", option)`.
- Quad or triangle is set per pattern with `SetMeshType`, not on export.
- **Not in the options:** Weld/Unweld, "Weld Turned Sewing Lines", FBX binary/ASCII and the texture path mode. What the API uses for these is UNVERIFIED.
- The direction of the export scale (mm to m for Blender) is not documented (UNVERIFIED; check by measuring).
- UV tools: `utility_api.UVPacking(...)` and `ResetUVTo2DArrangement()`.

## 4. Official examples and samples

- The developer site's "API Scenario" page has four scripts. **Simulation** (NewProject, ImportAvatar, ImportZpac, Simulate(100)) and **Pattern** (three pieces from points) are the useful ones; Animation and Substance are the others. Source: https://developer.marvelousdesigner.com/scenario.html (read 26 Oct 2026). The option example is at https://developer.marvelousdesigner.com/optiontype.html.
- **No official GitHub sample repository.**
  - The CLO organisation `clo3d` has four public repositories (libigl, a Qt patch, test_imscore, webpage_Fabric5K): https://github.com/orgs/clo3d/repositories (read 26 Oct 2026).
  - `clovirtualfashion` has none: https://github.com/orgs/clovirtualfashion/repositories (read 26 Oct 2026).
- Measured: the 2026.1 install has no example scripts. No .py files exist outside the bundled Python library. A 2022 community post mentions an `example.py` in Program Files then; a 2024 post says it was missing (https://support.marvelousdesigner.com/hc/en-us/community/posts/48267759477401, read 26 Oct 2026).
- Unofficial code to read before writing our own is listed in section 2 (matty, Laboon2501/ysk424). FittingHome/APIthon (2023) drives the Windows interface by automation. None of these were reviewed line by line.

## 5. Personal versus Enterprise

- Plans page: all plans have every software feature. The plans differ in seats, administration, billing and support level (https://www.marvelousdesigner.com/pricing, read 26 Oct 2026).
- Licence types: Personal is $39 a month. Linux exists only as "Enterprise Linux" ($2,300 per seat per year). Source: https://support.marvelousdesigner.com/hc/en-us/articles/47358269350041-What-kind-of-licenses-does-Marvelous-Designer-offer (dated 5 Aug 2026, read 26 Oct 2026).
- The MD Additional Terms contain no clause on API, scripts, automation, headless running or batch work. Searched for those words: https://legal.clo-set.com/additional-md (read 26 Oct 2026). They also say Personal was renamed Individual on 13 October 2026, in name only.
- Terms that bear on automation are all in the General Terms' "Use of the Services": no reverse engineering (c)(v); no service-bureau use (c)(vii); no access "by any means other than the interface we provide or authorize" (c)(viii); no "data mining or similar data gathering and extraction methods" (d)(vi). Source: https://legal.clo-set.com/modal-tou-general (read 26 Oct 2026).
- Limits on what may ship (CLO avatars, samples, AI features) are in the earlier note, MD-LICENCE-2026-10-26.md, in this folder.
- **No limit found for Personal on the Python API, OBJ/FBX export or OBJ/FBX avatar import.** The headless mode's availability on Personal is unknown.

## What it means for the work

The documented, licence-clean route is a plug-in .py that reads a job file from disk and does all the steps: import the body, build pieces from points, arrange, sew, set fabric and particle distance, simulate, export, then write a result file. It needs **one click per run** in MD's Plugin tab, by Jafar or by the operator through a screenshot. A socket listener would cut that to one click per session, but should wait for Jafar's view on the terms. Expect to build the zipper, and possibly the fabric physics, by hand in the GUI or from a saved .zfab or .zprj made once.

## Unverified / not reached

- The exact 2026.1 menu path of the Python editor (the docs say Script ▶ Python; the menu became Plugins in 2025.2).
- Whether the undocumented Headless API (`headless`, `headlessconfig`, access keys) works, and whether Personal may use it. Same for the `-python` start-up argument and for `RegisterPythonScript`/`RegisterPythonScriptFolder`.
- Whether `ImportFBX` honours the FBX file's own units or needs `scale = 10.0` for centimetres. The direction of the export `scale`.
- The unit of `CreatePatternWithPoints` coordinates (thought to be mm).
- What the API does for Weld/Unweld, Weld Turned Sewing Lines, FBX binary/ASCII and texture paths, which are not in `ImportExportOption`.
- Whether zippers can be made by script (no function listed), and whether `ImportPatternJSON` can carry one.
- Whether `.dna` (MetaHuman) import is reachable by script.
- Whether the program exposes more functions than the docs list (third parties say 688 calls).
- All third-party claims (Simulate's return value, mm lengths, socket bridges): untested here.
- The 2026.1 API changelog: the developer changelog stops at 2025.1.201.
- **Not reached:** http://manual.marvelousdesigner.com/display/MD4M/Script (the old manual; the host does not resolve); https://developer.marvelousdesigner.com/py-modindex.html (Access Denied); the pricing page's other FAQ answers (only "Which plan is right for me?" was opened); the "Import and Export Preset" manual article (not read); the CGChannel and Digital Production coverage of 2026.1 (secondary, not needed).
- **Read only in part:** the Register Accessory article (unit passages only) and the API list's docstrings (only those for the functions named above; all signatures were read).

## 30 October 2026: the bridge started through UI Automation (his ruling of that morning)

- Measured on this PC: Marvelous 2026.1 ships Qt 6 (Qt6Core.dll, qwindows.dll), and its main window (class TitleFrame) exposes its menu bar to UI Automation: every top item (File to Help) carries the Invoke, Value and ExpandCollapse patterns. A closed menu's items are not in the tree.
- Expanding Plugins shows Plug-in, Plug-in Manager, AI Studio Activation, Python Editor and API Reference; expanding Plug-in shows the registered plug-in as "     LEDGER bridge      " (its title padded with spaces), its popup hung under the Plug-in item inside the main window, not as a separate top window. So the 2026.1 menu path of the Python editor is Plugins > Python Editor (this file's open question, answered).
- Try 1 (09:32): the exact title not found (the padding). Try 2 (09:32:50): matched trimmed, invoked; the heartbeat began the same second; the window in front unchanged. Then stop.job and md_job.py --start restarted it alone (09:33:50).
- tools/md-bridge/start_bridge.ps1 holds the one permitted path (Plugins > Plug-in > LEDGER bridge) and starts only when Marvelous runs and answers Windows, no job is running (busy.json) and the heartbeat is over 30 s old or stopped; every start is a line in F:/LedgerTools/md-jobs/starts.jsonl.
