# Cloud week 42: the queue

Jafar's orders of 8 October 2026 (evening): the inputs the builder needs to build Quay Street's next families quickly, prepared and checked on branch cloud/week-42 while his PC is offline, by Saturday 17 October 08:00. A lane of bounded tasks the builder checks on its return, not a second builder. No Unreal, no game pictures: everything here is research, targets, Blender-by-script pieces and 2D, each with its check.

How this file works: one line per unit, in order. A unit is **open**, **in progress** (with its start time), **done** (with its files) or **set aside** (with why). Each unit is committed and pushed when it changes state, so a new session continues from the first unit not done or set aside. Times are Swiss (CEST).

The method (7 and 8 October): exact target first, written from sources by a helper that does not build the piece, photographs over books, every detail the photographs show written down, the target tested against its sources before building; built by script (Blender's bpy, headless), the script in git, a model in git only under production/assets/ (1 MB a file by the push guard), else the script that rebuilds it exactly; an automatic check against the target, then a fresh reviewer per view judging renders against the photographs; two tries, then set aside; only sources reached; the allowlist; nothing NoAI; invented names only.

Where things go: research notes in production/cloud-week/research/; targets in production/cloud-week/targets/<family>/; kit scripts and checks in production/cloud-week/kit/<piece>/, models in production/assets/cloud-week/; 2D scripts in production/cloud-week/2d/ (pictures cannot go into git outside previews, so each picture's script rebuilds it exactly); reduced previews in production/previews/ as cloud-week-<unit>-<date>.jpg.

## 1. Research notes (the professional method end to end, dated sources)

- 1a. done (8 Oct 22:20): production/cloud-week/research/1a-sash-windows-low-angles.md. Deep-set sash windows reading as white boards and slits from low street angles, and the fix (production/audits/windows-2026-10-08/). Epic's pages unreached (network); read today: three engine manuals on GitHub; Epic claims from earlier notes read on the PC, or marked as leads.
- 1b. done (8 Oct 22:12): production/cloud-week/research/1b-walk-without-foot-slide.md. A walk without foot slide where clips join. Epic's pages unreached (network): its web claims are search leads; its causes rest on the repository's own measurements.
- 1c. done (8 Oct 22:22): production/cloud-week/research/1c-night-pools-lumen.md. Night street lighting in Lumen: pools of lamp light with darkness between. Epic's pages unreached (network); measured today: the night previews in git and four CC0 night-street photographs from Poly Haven.
- 1d. done (8 Oct 22:40): production/cloud-week/research/1d-shop-glass-without-frame-cost.md. Shop-window reflections without the frame cost: the slow frames come from re-photographing fifteen panes' street cubes with full Lumen in play (at load and each light change; the three 1024 panes draw five times the main view's pixels, with a 2.4-2.9 GB memory surge beside the voice). Shipped games bake per light state and only look up: bake each pane per state (compressed, box-projected), never catch in play; stop-gap, catch both states at load behind the title. Read today: the repository and Godot's and Unity's open code and docs; games' talks only as leads (network).
- 1e. done (8 Oct 22:36): production/cloud-week/research/1e-unreal-mcp-setup.md. Setup note for Epic's Unreal MCP server in the 5.8 editor: enable (two plugins on the editor's command line, not in the project), connect Claude Code (local scope), the toolsets, safety (prompts on, call_tool never pre-allowed), known faults, and a ten-minute test on the Play-in-Editor street (the street is built at run time; there is no level to inspect before Play). Read today: Epic's Claude Code plugin files on GitHub and Claude Code's own docs; Epic's pages from the 7 October notes.

## 2. Exact targets, one per family (production/research/asset-plan/SUMMARY.md)

- 2.1 done (8 Oct 23:33): production/cloud-week/targets/front-door/ (TARGET.md, target.json, target_drawing.py, self_check.py, TARGET-REVIEW.md); overlay production/previews/cloud-week/refs/front-door/door-photo-01-teignmouth-target-on-photo.jpg. Front door: the lab's target amended twice; its re-review passes six of seven faults; the seventh, the brick plinth's returns standing 70 mm in front of each end of the threshold (photograph 1), is the wall's, not the door piece's, and is left as written in the review for the wall kit (two tries; no third). Self-check 303 of 304 (the one disagreement reported).
- 2.2 open. Shopfronts (Rita's is the model; the other eleven by kind).
- 2.3 open. Railings.
- 2.4 open. Bollards.
- 2.5 open. Litter bins.
- 2.6 open. The pillar box.
- 2.7 open. Kerbs and drain covers.
- 2.8 open. Lamp posts.
- 2.9 done (9 Oct 00:35): production/cloud-week/targets/fascia-signs/ (TARGET.md, target.json, make_target.py, pixel_checks.py, target_drawing.py, self_check.py, make_previews.py, TARGET-REVIEW.md); previews production/previews/cloud-week/refs/fascia-signs/. Shop fascia signs, ten boards and four hanging signs. Re-review (try 2): all 13 first faults answered; two narrow ones left with exact fixes in the review (the pixel checks' hand-jitter and glyph tolerances, which fail correct boards at random; the grocer's street number on a side door the bay lacks), carried into unit 4.1, which applies them; no third try of the target. Self-check 296 of 296. No 1990 fascia photograph reached (network).
- 2.10 open. Posters and notices.
- 2.11 in progress (8 Oct 22:38, ahead of 2.2 to 2.10, which wait for photographs the network refuses; written 23:32, self-check 700 of 700, target review 1 FAIL, 12 faults (facade-wide soot missing, streaks unsourced and too strong, stacked wear without a floor, checks that pass wrong masks, gutter grime against its photograph, wet and dry double-counted, iron unworn, and more); amending, try 2). Wear: stains, grime, gum, cracked render.

## 3. Kit pieces built by script, each through its check and fresh review

- 3.1 in progress (23:33, try 1: building). The door.
- 3.2 open. The shopfront's parts: pilasters, consoles, fascia, stall riser, transom.
- 3.3 open. Railings.
- 3.4 open. Bollards.
- 3.5 open. Bins.
- 3.6 open. The pillar box.
- 3.7 open. Kerbs and drain covers.
- 3.8 open. Lamp posts.

## 4. 2D, finished

- 4.1 in progress (9 Oct 00:36, try 1: making). Fascia signs for the street's shops (names from canon.md and TOWN.md).
- 4.2 open. Posters and notices for invented 1990 events and goods, in period type (OFL fonts).
- 4.3 open. "To Let" boards.
- 4.4 open. Street name plates.
- 4.5 open. Wear textures as masks.

## 5. Handover

- 5.1 open. production/cloud-week/HANDOVER.md for the builder: each piece, its target and check, and how to bring it into the game.

## Log

- 8 Oct 21:55: branch cloud/week-42 made from wip at 8356dda; this queue written; Blender 5.2.2 (bpy, headless) installed in the cloud session.
- 8 Oct 22:05: the cloud environment's network policy refuses almost every host the week needs (Wikimedia Commons, Geograph, archive.org, dev.epicgames.com, unrealengine.com, arXiv, graphics blogs: 403 at the proxy). Reachable: raw.githubusercontent.com, polyhaven.com, ambientcg.com, pypi. Asked Jafar to open it (the environment's Network access: Full, or those hosts allowed). Meanwhile the units that need no new web sources go first: the door (the lab's photographs are in git on branch lab), the MCP note (Epic's own plugin instructions are on raw.githubusercontent.com), tools and fonts.
