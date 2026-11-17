# Review: Kiln M5 three-garment plan (17 November 2026)

Reviewed: KILN-M5-THREE-GARMENTS-PLAN-2026-11-17.md against KILN-M5-RIGGING-METHOD-2026-11-17.md, its review, and the licence allowlist. Nothing was run or changed except this file.

**Verdict: PASS WITH FIXES.** The split (two skinned jackets, a skirt with skinned waist and cloth pleats) follows the parent method, Mafia and Kingdom Come II. The floors match the parent's steps 11 to 22. The licences are clean. The main problems are the top of the hours range and one source the plan calls unreached.

## Holds

- Floors 13 + 8 + 8 = 29 h, matching parent steps 11 to 16, 17 to 19 and 20 to 22.
- Epic's outfit page (5.8): four LODs at 50, 30 and 10%, Closest Point on Surface, the Relax, Prune, Hammer, Clamp and Normalize fixes, and a static mesh import. All confirmed.
- Bone limits: 4 or 8 by platform, 12 in practice when unlimited, and a per-LOD Bone Influence Limit. Confirmed (page labelled 5.9).
- Painting: "A value of 0 would mean that the skinned vertex could not move." Confirmed for the brush's paint value. The page does not spell this out for Max Distance itself (labelled 5.9).
- Licences: nothing off the list is recommended. Robust-transfer MIT code is correctly flagged as needing a pick, because allowlist 10 covers only FoldCraft and ast-grep.

## Findings

1. **The top of the hours range does not add up.** The per-garment tops (22 + 14 + 16) come to 52 h, not 50, and they are not drawn from the parent's 2 to 4x overrun. Fix: say how each top was reached, or apply the parent's method (Hook list 15.6 h at 2 to 4x gives 31 to 62 h). Then fix "about 70%" to match.
2. **The shared steps are left out of the total.** Parent steps 1 to 5 (2.5 h: the turns records, the weights-body check, Darren's skeleton check, Kiln's skinning job) come before all three garments. Fix: state that they are counted with the trousers, or add them.
3. **The proxy deformer was reachable.** Epic's 5.3 Python API for the cloth asset documents the "proxy wrap deformer" ("multiple triangle influences from the simulated proxy mesh", a smooth skinned-to-simulated blend). Fix: change "unreached" to "exists (5.3 API); 5.8 setup and cost unmeasured". Keep the risk: a March 2026 forum thread asking how to wire the node has no answer.
4. **The skirt's stand-in is not tied to the one already made.** The held SheilaSkirt row already has a 480-triangle simulation mesh (parent, step h). Fix: say whether the plan reuses it or makes a new one nearer KCD2's 270 triangles, and why.
5. **Two tests have no screen and no decider.** The nylon jacket and the skirt list how failure looks, but not their offline screen or what passes them. Fix: name the tool bar (or the stride count of body through cloth) as the screen for each, and RUBRIC lines 9 to 11 in the packaged film as the decider, as Plan 1 does.
6. **One fallback goes beyond the parent without saying so.** "Two hem bones that follow the thighs" is not in the parent, which names only a short cloth hem. Fix: mark it as an addition to the parent.
7. **"Sits within" is loose.** The project's 25% at LOD2 differs from Epic's 30%, and Epic allows changes ("can be adjusted as needed"). Fix: say exactly that.
8. **Plain words.** The "In short" section is plain enough for him. The body is full of script and option names. Fix: if it reaches him, send only "In short" and the totals.

## Sources (all read 17 Nov 2026)

- https://dev.epicgames.com/documentation/metahuman/building-a-metahuman-parametric-outfit-with-an-fbx-export (5.8)
- https://dev.epicgames.com/documentation/unreal-engine/skeletal-mesh-rendering-paths-in-unreal-engine (5.9)
- https://dev.epicgames.com/documentation/unreal-engine/clothing-tool-in-unreal-engine (5.9)
- https://docs.unrealengine.com/5.3/en-US/PythonAPI/class/ChaosClothAsset.html
- https://forums.unrealengine.com/t/cloth-asset-in-5-7/2708362 (community, unanswered)
- Unreached: the Epic API pages for ApplyProxyDeformer and the proxy deformer node (empty when fetched)
