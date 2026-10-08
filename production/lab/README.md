# The lab (branch lab, 7 October 2026 onward)

A separate session testing one method while the builder works: give the AI an exact, measurable target and check every attempt automatically, in small units, with notes kept outside the agent (the lesson of AI-driven decompilation), against work judged by taste alone.

| Test | Notes | State |
|---|---|---|
| 1. Unreal's source answers two open problems | [1-unreal-source/NOTES.md](1-unreal-source/NOTES.md) | done: both answered from the installed 5.8.2; the GitHub clone refused |
| 2. One sash window from measured numbers | [2-sash-window/NOTES.md](2-sash-window/NOTES.md) | done: passes its check and, on narrow points, a fresh review |
| 3. One jacket from a pre-1929 draft | [3-jacket/NOTES.md](3-jacket/NOTES.md) | done: the pattern exact and checked; the drape failed its review; the lapel did not hold |
| 4. Ron's plain 1990 clothes, modelled to a pattern (8 Oct) | [4-plain-clothes/NOTES.md](4-plain-clothes/NOTES.md) | done: no body through the cloth, the outline within about 1 cm, 3 of 22 seams; the fresh review failed it, mostly on the target's own choices. Page: [4-plain-clothes/REPORT.md](4-plain-clothes/REPORT.md), https://claude.ai/artifact/5rTRS2pewmoWbjXgcPLiPo |

| The wet road's near-white mirror, for the builder (8 Oct) | [ROAD-NOTES.md](ROAD-NOTES.md) | done: why (our film is optically water at the engine's default reflectance), a per-view target and the change (a film specular of about 0.13) |
| The shop glass's stair steps, for the builder (8 Oct) | [GLASS-NOTES.md](GLASS-NOTES.md) | done: an unanti-aliased Scene Colour capture at 512; the fix (exclude the capture from the scene-texture extents, catch the two hero windows at 1024) |
| 5. The four-panel front door from Ellis and the photographs, for phase 2 (8 Oct) | [5-front-door/NOTES.md](5-front-door/NOTES.md) | built, passing its check, proportions right by the check and both reviewers; failed two fresh reviews on detail the target did not write down (profiles, ironmongery, the frame's square edges in the photographs): set aside for phase 2 |

The page for Jafar: [LAB-REPORT.md](LAB-REPORT.md), also published as a private page: https://claude.ai/artifact/GAgntnYAoqJVR6irjqjeBk

Rules kept: Unreal never opened; Blender headless, Workbench only or no render at all; large files on F:\LedgerTools\lab; nothing bought; pushes to lab only. Time per test: [time-log.jsonl](time-log.jsonl). Shared tools: [tools/outline.py](tools/outline.py) (outlines and sections from triangles, compared in millimetres, no renderer) and [tools/panel_mesh.py](tools/panel_mesh.py) (flat pattern pieces to sewing meshes).
