# Can Marvelous Designer be driven entirely by script? (research note, 29 September 2026)

Asked under Jafar's ruling of 29 September (the jacket: if Blender's last attempt fails, "check whether Marvelous Designer can be driven entirely by its own scripting, and only if it can, bring it back to him") and the clothing session's own instructions ("first find out whether it can be driven entirely by its own scripting, then bring it to me as a decision; buy nothing"). A separate helper, about thirty minutes, every source read 29 September 2026; nothing downloaded, installed or signed into. **D** documented; **I** the helper's inference. Saved by the clothing session.

## In short

**Partly; not with nobody at the controls.** The Python API covers most of the work (the avatar, pattern pieces from coordinates, sewing, fabric from a file, simulation, pose and animation, export with the flat pattern as UVs). But there is no command-line or headless mode and no documented way to run a script at start-up: someone must click once each time the program starts (to run the script, or a listener that then takes jobs over a local socket). It must also be online and signed in; any dialog stops a script dead; there is no quit call; DXF import is unclear; arrangement points on a custom avatar cannot be made by script. The 2026.0 (April) and 2026.1 (August) releases change none of this.

## Step by step

- **Start, run, quit.** No headless session or simulation without the interface (its own team, forum, 2022) (D); nothing since adds one (changelog to 2025.1.201; 2026.0 and 2026.1 feature lists) (D). Scripts run from the Python editor or as .py plug-ins launched from inside the program; nothing says they run at start-up (D). Every third-party bridge found needs a click on its plug-in menu after each launch (D, third-party). No quit function (D, by absence); a Windows kill from outside, or UI automation to click the menu, fragile (I).
- **Avatar.** `ImportFBX(path, options)` without a dialog, options including arrangement points, animation, scale, axes (D); no skeleton functions (D, by absence); FBX avatars unverified by one bridge (D, third-party).
- **Patterns.** `CreatePatternWithPoints` from coordinates (straight, spline, Bezier), internal shapes, pattern JSON in and out (D); DXF import unclear (D).
- **Placing.** `SetArrangement`, `SetArrangementPosition` (whole numbers), orientation and shape (D); no function creates arrangement points (D); placement "not a verified world-space transform" (D, third-party).
- **Sewing.** `AddSeamlinePairGroup` and variants (D); it checks only that the indices exist (D, third-party).
- **Fabric.** `AddFabric` from a .zfab or .jfab file, `AssignFabricToPattern` (D); no setters for stretch, bending or density (D, by absence): a melton would be written as a .jfab (I). Per-piece particle distance, thickness, collision (D).
- **Simulation.** `Simulate(steps)`, quality presets, CPU or GPU, time step, gravity (D).
- **Pose.** Its own pose files, Alembic, animation recording (D); a MetaHuman pose change by importing the FBX with animation, then recording (I).
- **Export.** FBX, OBJ, Alembic, USD; thin or thick, single object, the avatar, animation, unified UVs; `ResetUVTo2DArrangement` and UV packing (D). No separate simulation mesh in FBX or OBJ (only USD carries simulation data) (D); two exports instead (I).
- **Still needs a person:** starting the script after every launch (D, third-party); signing in if not remembered (I); any dialog, which hangs a listener (D); DXF probably; arrangement points on a custom avatar (I); a clean quit (I).

## Licence and cost

- Personal: US$39 a month or US$280 a year; for individuals, freelancers and sole proprietors, commercial use allowed; companies of two or more need Enterprise (D). A lone developer selling a game appears to qualify; the licence text itself was not read (clause 2.1.1 to check) (I, thin).
- Enterprise: US$199 a month (one machine) or US$2,000 a year (floating) (D).
- A 14-day free trial (D). Internet access required for every licence type but Enterprise Network Offline (D). Subscription only (D).

## Hardware

- GPU simulation needs NVIDIA CUDA; AMD cards gain nothing but display fine, and CPU simulation works anywhere; CPU and GPU results matched since 2024.2 (D). No official speed penalty; one jacket at the Fitting preset should be practical on the CPU (I, thin).

## People automating it

- matty/marvelous-designer-plugins (688 calls exposed; avatar import, drafting, sewing, fabric, simulation, OBJ export tested; started by pasting into the Python editor); the ysk424 and showhe-dev MCP bridges (MD 2026; a click after every launch); Laboon2501 (verified on 2026.0.315); FittingHome/APIthon (Windows automation, method unclear). No example of a run unattended from start to finish (D).

## Sources (all read 29 September 2026)

- developer.marvelousdesigner.com: API List, ApiTypes, Plug-in Management, API Scenario, Changelog (latest 2025.1.201); undated.
- support.marvelousdesigner.com: "Python Command Line Example ?" (13 June 2022); "run simulation through cmd" (10 September 2023); Python Script (updated 31 October 2025); System Requirements (April 2026, updated 20 April 2026); Simulation manual (17 November 2025); "What kind of licenses..." (5 August 2026); "I'm a freelancer/sole proprietor..." (29 May 2025); "Difference between Personal and Enterprise" (26 May 2025); "Due to a network issue..." (29 May 2025); 2026.0 feature list (12 May 2026); 2026.1 feature list (24 August 2026).
- CG Channel: 2026.0 release (20 April 2026); 2026.1 release (24 August 2026); Linux edition (1 October 2025). Digital Production: indie pricing (12 January 2026). marvelousdesigner.com pricing comparison (18 September 2026). 80.lv: GPU simulation (29 October 2024).
- GitHub READMEs (undated): matty/marvelous-designer-plugins; ysk424/marvelous-designer-mcp; showhe-dev/marvelous-designer-mcp; Laboon2501/MarvelousDesigner-MCP; FittingHome/APIthon.
