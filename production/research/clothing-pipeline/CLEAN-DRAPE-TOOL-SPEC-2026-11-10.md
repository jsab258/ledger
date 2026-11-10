# A drape tool built clean: what unattended work needs (10 Nov 2026)

Advisor 79 (10:35). Source: the needs list in the advisor ack of 10:26 for message 77, read from the docs of a tool that may not be used (C:\DrapeStudio, decompiled from Marvelous; not run, see DECISIONS 2026-11-10 10:26). Nothing here comes from Marvelous code, files or presets. A tool to this spec is built from open cloth simulation and our own values only, and enters the pipeline only with its licence line in the allowlist.

## Must have
1. Runs with no window: a command-line batch mode, exit code and a result file per job.
2. Jobs in and out as JSON: body, patterns, sewing, fabrics, arrangement, solver settings in; meshes, measures and log out.
3. The same drape every run: fixed seeds, fixed step count, a run-to-run difference measure in the result.
4. A scripting layer (Python) for what JSON cannot say: building pieces, sewing lists, edits between steps.
5. Body import as FBX (our MetaHuman bodies), with arrangement points or an equivalent landmark set we define.
6. Patterns in from our drafts (FreeSewing / GarmentCode output, SVG or DXF), seams and notches kept.
7. Fabric values we set and own: stretch, bend, shear, density, thickness, friction; elastic bands; fold and stiffening lines for collars, cuffs and hems.
8. Measures built in: edge stretch per seam, cloth through body, coverage (sleeve, hem), seam gaps; numbers in the result file, so the builder's checks need no screenshots.
9. Export: OBJ or FBX with UVs from the pattern, welded seams, our naming.
10. Runs on the processor; uses the card only if it does not crash on the AMD card (the capture solve's lesson, 10 Nov).

## Open questions before any build
- Which open cloth solver (licence, quality on knit and denim, speed on the processor): a research-first scan, per the 8 Nov scans ruling.
- Whether this is cheaper than Marvelous's own Python on his paid month (MARVELOUS-UNATTENDED-2026-11-08.md) before 20 Nov's decision.
- Status: a note only; no work starts on it without an order item.
