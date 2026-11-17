Method researched: TARGET-IMAGE-TO-3D-PROPS-2026-11-17.md checked against repository files and allowlist.

# Review: TARGET-IMAGE-TO-3D-PROPS-2026-11-17.md (17 Nov 2026)

Verdict: PASS WITH FIXES

Checked: local files (allowlist, RULINGS, asset-budgets.json, 4-BUDGETS location, TRIED-2026-09-24, F:/LedgerTools/trellis copies, meshgen README, hour arithmetic). Web sources (GitHub, Hugging Face, AMD, Epic, arXiv) were not opened: marked UNCHECKED, taken only as the note's own "R" claims, not as evidence here.

## Confirmed
- Allowlist line 5 names "TRELLIS/TRELLIS 2 (MIT)"; Hunyuan3D is NEVER SHIP 3; Meshy/Tripo paid tiers only. Note's table matches.
- DINOv3 and BiRefNet not on the allowlist; the note says so. The 24 Sep stop on DINOv3 (TRIED-2026-09-24 lines 90-94) is quoted correctly.
- prop_medium budget (5,000 tris, 3 LODs, 1024, 10 hulls) matches production/specs/asset-budgets.json line 46.
- Camera 3.1 m / 86 degrees matches RULINGS 28 Oct. Hour totals (27-37 and 15-19) add up from the table.
- Decision-record marker rule (`TOOL-DECISION:`) matches tools/meshgen/README.md.
- Reference-game line says "none found" and names KCD2 and Mafia methods. AMD card claims are marked U with ROCm excluded.

## Findings

F1 (must fix). Section 4, line 89 and line 47. The note's recommendation relies on a Vulkan Windows build, while TRIED-2026-09-24 line 88 recorded "prebuilt Windows Vulkan, res 512 fits about 6 GB". The note flags both as U, but does not say the 24 Sep claim is an unsourced earlier note that this pass failed to reproduce. Fix: add one sentence in Section 2 (trellis.cpp row) that the 24 Sep claim is unsourced and conflicts with the releases list read today, so it is not evidence.

F2 (must fix). Pass bar item 5 and Section 3 mechanical list. Aims are mostly measurable, but item 3 (one Sonnet reviewer, "equal or better") and item 2 ("no shadow that does not move") have no numeric or named-view pass rule beyond "three fixed cameras". Fix: state that item 2 is judged on the named 1.5 m capture under two named light directions, and that item 3's "equal" is decided by the reviewer's written per-view verdict, all three views required.

F3 (must fix). Rulings line, 13 Nov authored-breadth ruling (RULINGS line 6). The note cites 22 Sep as the binding ruling but does not mention that the 13 Nov ruling ("generation is welcome when it carries out a plan") sits beside it; the test needs a spec and check per prop to satisfy it. Fix: add a clause saying each prop has its spec (TARGET-PROPS-DRESSING lines) and the section 3 judge as its check, so the test is not "filler a generator could make".

F4 (should fix). Section 2, Objaverse line 44. RULINGS 3 Oct bars NoAI-marked content "even as a reference", with only Epic-published content excepted. Training-data provenance is not "content used", but the note leaves it as "his call" while the recommendation (line 47) already proceeds. Fix: make the Objaverse question a blocking item before stage 2, not a parenthesis, and say no generator run happens before it is answered.

F5 (should fix). Line 45. Input pictures: Z-Image-Turbo is named as a possible source but its weights licence is unread and it is an AI generator whose outputs would feed a generator. Fix: drop it from preferred inputs until its licence is read and the allowlist covers it; keep CC0 photographs and own Blender renders.

F6 (minor). Line 35 (Pixal3D) relies on an HC note not re-read today; marked as such. Line 39 (blender-game-skills) licence unread; marked U. Acceptable.

F7 (minor). Line 55-62 pixel table: arithmetic is the note's own and the 64/86 degree ambiguity is marked U (item 9). Acceptable; fix only if the built camera is read first.

## Reuse-first
Own pieces searched (props-trellis-01.json, meshgen CLEAN stage, dustbin E13, Megascans and Poly Haven comparators). CATALOGUE.md has no image-to-3D line, stated. No conflict found with RULINGS 22 Sep: the test is framed as the measurement, nothing adopted on its result alone.

## Unverified points
Fourteen listed and marked; the list is complete as far as checked. Unreached sources are listed and not used.
