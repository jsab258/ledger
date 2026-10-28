# Review of CHECKS-2026-10-28.md (28 October 2026)

**Verdict: pass with fixes.** Most citations hold. One engine claim matters: as configured, Epic's material validator checks nothing. Six thresholds do not trace.

**Confirmed:**
- Engine: the commandlet's switches (148-150) and folders (153-208); PythonScriptPlugin.cpp 1381-1389; settings lines 168 and 176; every IsDataValid line; the MD5 tag lines; every editor-subsystem and Geometry Script line (all script-exposed).
- Repository: Studies 5, 6, 12, 13; 4-BUDGETS 4.7, 4.8; DECISIONS 271; BAKE-PLAN 89, 110-114; WEAR 62, 63, 95; the seven gate quotes; import_garments.py 65-68 (no LODs); nanite_audit.py; the jacket's maps at 2048×2048 (PNG headers on F:).
- The "before" table: sums and medians recomputed, correct. Spot checks: the launderette (5, 19, 3) and the newsagent (3, 24, 2) match.
- 2,917 words without table bars; ends "Method", then "First use".

## Findings

1. **Material validation is "on", but it validates nothing** (lines 19, 22 and 117; rules 1 and 7).
   - Source: EditorValidator_Material.cpp 91-94 returns false when no platforms are listed. MaterialValidationPlatforms (DataValidationSettings.h 41-42) is set in no ini: not in Engine/Config, ue-probe/Config or mh-assemble/Config. Lines 85-89 also skip the Save and Commandlet use cases unless Editor.EnableMaterialAssetValidator is set.
   - So the jacket's default-material fault would pass.
   - Fix: list the PC's SM6 platform in each project's DefaultEditor.ini (or have rule 7 compile it); prove it with the grid plant; correct lines 19 and 117.

2. **The exit code** (lines 37 and 184).
   - Main returns 0 (DataValidationCommandlet.cpp 42, 229-230). But the process returns 1 whenever any error is logged (LaunchEngineLoop.cpp 4217-4223; UseCommandletResultAsExitCode is false, Commandlet.cpp 37). Asset failures are mirrored to the log as errors (MessageLog.cpp 120, 328-333) and routed to GWarn (LogMacros.cpp 78-87).
   - Fix: "1 on any logged error, related or not, so not a verdict." The method stands: it reads the line.

3. **Two "unverified" items are settled in the source** (lines 30, 38 and 123).
   - The summary is mirrored to the log by default (MessageLog.cpp 132, 271; EditorValidatorSubsystem.cpp 1134-1135).
   - Load warnings stay warnings; only logged errors fail (EditorValidatorSubsystem.cpp 916-935, 958-978). So a missing reference logged as a warning passes rule 1, and rule 8's parts list must catch missing parts.
   - Fix: update them.

4. **The 7/21/2 split holds by count, but only 6 faults are covered.**
   - Recount of the M faults: LP 1, RF 5, IR 4, NA 2, TR 8, GR 4, CH 4, LA 2 = 30. Placement: 6+2+5+5+2+1 = 21. Others: RF:142, GR:51.
   - No rule checks facets or flat shading, so GR:117 is not caught.
   - "Placement" also holds data faults (IR:44, an OPEN sign; TR:26, a shop-file zone).
   - Fix: "six" (or a sourced shading rule); "placement and data".

5. **Rule 7 misses WEAR 62 and 63.** Those were flat-colour materials with no texture, so "one-colour texture" does not catch them. Fix: add "a non-glass slot with no texture sample".

6. **Thresholds not traceable:**
   - a. Rule 3, "at most 60% of the one before": the sources give 47/25/9% of full detail (Study 6, line 82), "about 50, 25, 10%" (line 122) and "about half the last" (4-BUDGETS 4.7). 60% appears nowhere. Record the tolerance in DECISIONS.
   - b. Rule 3, "Garments: 4": a crowd outfit has 3 LODs and an accessory 2 (4-BUDGETS). Set the count by kind.
   - c. Rule 5, hats and accessories at 1024: 4-BUDGETS gives accessories 512², and Mafia ships hats at 512 (Study 6, line 83). Use 512; keep shoes at 1024 (line 118).
   - d. Rule 5, "none over 4096, except trim sheets at 4096×2048": the exception is not over 4096. Reword it.
   - e. Rule 11, "props: simple collision, at most 10 hulls": a small prop may have "none, or one box", a display none, and a car up to 6 hulls (4-BUDGETS). As written, the planted "prop without collision" fails a valid small prop. Make the rule per kind.
   - f. Rule 2's 90% warning: no source. Mark it as our own choice.

7. **The folder exemption catches the garments.** Garments live under /Game/Ledger/MetaHumans/Garments (import_garments.py 13, 33), and rules 3 and 10 exempt "MetaHumans". Fix: exempt exact folders, with Garments mapped first.

8. **First use step 2: mh-assemble is not a safe scratch project.** The build machine mirrors its /Game/Ledger/MetaHumans folder into the game (import_garments.py 13-15; import_jacket.py 9-11). Fix: plant in a folder outside /Game/Ledger and delete the plants afterwards, under retention.

9. **asset-checks-fresh requires failed=0, which clashes with the gate rule.** CLAUDE.md says known shortfalls are "listed, failing nothing alone", but one set-aside asset fault would block every push. Fix: waivers listed in the spec, each with its DECISIONS line.

10. **Minor:**
    - Enhanced Input's validator is on by default (EnhancedInput.uplugin: EnabledByDefault true), not off (line 23).
    - The ensure is at EditorValidatorBase.cpp line 31, not 27-30.
    - Line 84, "nothing reads the imported assets": nanite_audit runs on every build inside make_base_material.py (4477-4485). Reword.
    - Line 105, "43% of the distinct faults": the 66 include 5 repeats (gate-count.md 77, 81). Say "of the counted faults".
    - Line 121: web-sources.md 112-117 lists two 404s, one 403 and two redirects, not one 404 and one 403.
    - Rule 6, "not from JPEG": name the field, the SourceCompression tag (Texture.cpp 1485; TSCF_JPEG, TextureDefines.h 341). Rita's JPEG sat inside a glb, unseen by the export-file check.

**Not re-checked:** the "24 of 64" count, the cloud REVIEW files, the web claims.
