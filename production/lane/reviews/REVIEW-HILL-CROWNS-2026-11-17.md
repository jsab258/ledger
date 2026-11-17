# Review: hill crowns research and test plan (17 Nov 2026)

Verdict: PASS WITH FIXES

Checked: the plan against its parent target, canon.md, RULINGS.md (trees, hill, 7 Nov, Blender, licence), the allowlist. Arithmetic re-done: 5.4 cm and 10.1 cm a pixel, 164 px and 262 px, 2048 frames to about 120 m and 193 m, 11 MB and 43 MB a type all hold.

## Findings

1. Season is wrong. Canon names no month. The story design puts Tom's arrival in October (game-design/warehouse-fire-2026-09-29.md lines 26-27) and the parent target says "October, mostly green and yellowing". Finding 9 misreads the parent as November. Fix: bake an October crown (sycamore in leaf, yellowing; oak green-brown; ash starting to drop). Remove "part-bare helps the soft edge": the soft edge has to come from the impostor itself, which makes the test harder.
2. The licence pick is not needed as written. The allowlist only covers what ships. Its PROCESS 2 asks for a decision record. The add-on has no weights, never ships, and its output is ours. The only link to him is the 12 Nov install rule, and an add-on inside Blender, already approved, is arguably covered by it. Option B is not a real choice, since Route B is already out. Fix: write a DECISIONS line citing GPL-3.0-or-later, name it in the hourly row and start. If the 12 Nov rule is read strictly, raise one ACTION item, but do not make step 1 wait on it.
3. The cost line cannot reliably fail. A 0.2 ms difference in a five-second average frame time is inside the noise. Fix: measure GPU time (stat gpu or ProfileGPU), three runs with the 100 copies and three without, and report the spread. Pass only if the mean plus the spread is at most 0.2 ms. Show where 0.2 ms comes from, as the impostors' share of the hill's 0.5 to 1.2 ms.
4. The memory line does not scale. 50 MB passes one type at 4096, but six types come to about 256 MB, on a card already 330 MB over. Fix: add a whole-hill memory cap and default to 2048 unless the hook frame shows 4096 is needed.
5. The fail clause contradicts step 4. Step 4 already bakes all three variants, so "try the other variant" adds nothing. Fix: the test passes if one variant passes, and fails if none does.
6. The try count is not stated. Three tries are spent, and the 5 Nov closure and the parent say the next one needs his yes. CLAUDE.md also says a third try needs his yes. RULINGS 7 Nov (amended 9 Nov) allows one genuinely different researched method with "none asks him". Fix: name the conflict, and settle which rule governs before step 1. RULINGS normally wins as his latest word. Record the choice either way.

## Sources

- extensions.blender.org/add-ons/sapling-tree-gen, read 17 Nov 2026: 1.0.0, released 4 Nov 2026, "all new code", Blender 5.2 LTS or newer, GPL-3.0-or-later. Confirmed.
- dev.epicgames.com impostor-baker-plugin-in-unreal-engine (5.9 page), read 17 Nov 2026: 8 triangles against a billboard's 72, three frames blended, not labelled experimental, Upper Hemisphere for things not seen from below, GBuffer capture does not work with translucency. Confirmed. 5.8 state still unread.
- Nanite Foliage still being experimental: not re-checked here, so it rests on the plan's own read.
