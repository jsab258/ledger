# Review of the asset-import skill, 2 November 2026

One fresh reviewer (general-purpose, read only; no scripts, builds, games, downloads, sign-ins, clicks, computer use or UI Automation) checked .claude/skills/asset-import/SKILL.md against its sources. Those were CLAUDE.md, RULINGS.md, the licence allowlist, CATALOGUE.md and THIRD-PARTY.md, and the tools' usage texts and code: catalogue.py, attribution-check.py, asset_checks.py with asset-budgets.json, prop-dimensions.py, prop-reach.py, body-proportions.py, stage_game_data.py, the import_*.py scripts, retarget_sitting.py, nanite_audit.py, fab_closure.py, make_base_material.py, push_guard.py, canon-gate.py and ci-checks.sh. It also read the build machine's workflow, DefaultGame.ini, 13 memory notes and the 12 DECISIONS entries the skill cites.

**Verdict: PASS WITH FIXES.** About 120 claims checked: 6 wrong or unbacked, 13 imprecise, 8 points missing, and four character names leaked into method lines. Every DECISIONS citation by date and time was exact. Before applying the fixes, the builder checked these against the files: W2, W4, M1, M2, M4 and M5, I5 and I7.

## Wrong or unbacked (all applied)

1. Step 10's check, "`--list` reports nothing missing", proves nothing about a new file: a file never listed cannot show as missing. The folder walks see only the checkout. Now: the path is in FIXED or named by a computed list, the count rose, missing=0; a picture kept only on F: is staged only when a spec names it.
2. Step 3 said stage_game_data and import_street "read a file the checkout lacks" from game-inputs. In fact each importer has its own rule. import_street and import_shop_rooms take the newer of the checkout and F:. import_shop_displays, import_front_joinery and retarget_sitting read F:. import_vehicles, import_people, import_sounds and import_figure read the checkout only, so their sources must be in git under 1 MB.
3. Step 5's check, "the run's own new line", fits ue-material.txt only. The MetaHuman-project scripts rewrite their whole report each run (import_garments.py and import_fab_clothes.py open it with "w"). Now: the report's time against the run's start, and no RAISED line.
4. Step 5 named LEDGER_FAB_DIR as the one-package switch. The switch is LEDGER_FAB_ONLY. Without it each run replaces fab-clothes.json. A package may keep its own folder layout, so fab-clothes.json is where the assets actually landed.
5. Step 2 said CC BY was for "clothes only". It covers clothes and their accessories (shoes, belts, hats, bags), never one marked NoAI (RULINGS 30 Oct; SHIP-SAFE 2). Aligned with the Always line.
6. Step 7 called the street complex-as-simple beside a check by rule 11, which fails every complex-as-simple mesh in a kind's folder. Now: the street's folder needs an exempt kind or a waiver.

## Imprecise (all applied)

7. The budget kinds map only the garment folders today, so props, kit pieces and the street are checked by none of rules 2, 3, 4 and 11. Now said in step 7.
8. The triangle cap per kind, the 90% warning (warn_fraction) and the texture caps (the kind's texture_max, 4096 overall) are now named.
9. The asset checks' line lands beside whichever project runs them, not always ue-probe. LEDGER_CHECK_FOLDERS is now named.
10. The workflow's commandlet arguments also include `-nosplash -stdout`. Added.
11. The build step's call list lacked make_root_motion_clips, make_tom_retarget and nanite_audit. import_front_joinery runs with materials only (import_mesh=False). Added.
12. import_prop_meshes.py: no live workflow or tool calls it. The step's "check first" is replaced by that fact, and its usage text's relative -script is flagged.
13. retarget_sitting.py carries only its named clips and Epic's sample idles, so a new clip is an edit to its lists. Added.
14. Reference first: tools/order_ledger.py reads the order's item for a "Reference:" line ("none found" allowed) or a study's path, not the item's plan. Corrected.
15. attribution-check's WATCHED covers every directory of third-party content. Adding one is an edit to WATCHED or OURS plus a THIRD-PARTY.md row with its token. catalogue.py also fails stale entries. Corrected.
16. The Fab plugin was switched off because an Epic update broke every build, to be undone when Epic ships matching rules. It is not a download policy. Corrected.
17. The NEEDS YOU form is RULINGS 1 Nov, and the item also goes on his one page (RULINGS 2 Nov). Corrected.
18. import_figure.py measures only its one body. Any other body is now marked "check first".
19. The deleting rule (RULINGS 29 Oct) lacked three parts: his yes also covers what cannot be made again; never delete what the game, a build or the backup holds; when in doubt, it is his. Completed.

## Missing (all added)

- Which MetaHuman project ships. Only C:\LedgerTools\mh-assemble\Content\Ledger\MetaHumans reaches the build (mirrored), and nothing under /Game/Fab is copied (fabClothesCopied=NONE-NoAI). What lands in the dressing project, /Game/Fab or import_anim's default folder is therefore not in the game. Opened without LEDGER_MH_SCRIPT, a project runs the cast maker (init_unreal.py).
- RULINGS 25 Oct: a design check before any kit import (reads at the game's distance, textures sharp enough, no real name); routine imports of designed pieces run on Sonnet, Opus for diagnosis and final review.
- RULINGS 11 Oct: nothing from Mafia or Kingdom Come II, study extracts included, enters LEDGER or git.
- The commit guard (tools/git-size-guard.py: allowed folders, 25 MB at commit, while the push guard still refuses over 1 MB), and the 500 KB cap on previews.
- production/retention.json: F:/LedgerTools/tmp is deleted after 7 days and scratch after 3, so lasting sources go in protected folders (fab, garments, game-inputs, bodies, polyhaven). The already-downloaded fab and polyhaven folders are now in step 1's search.
- A garment's prerequisites: its garments.json row (LEDGER_GARMENTS limits a run) and an asset-budgets piece whose parts name SKM_<Name>, which `--check-spec` enforces.
- The licence process: the licence tag on every asset (PROCESS 1); his Sketchfab token and his Mixamo account and token; Unreal-only content never outside an Unreal build (SHIP-SAFE 3, 8). The reviewer's mention of meshgen.py's licence gate was not checked by the builder and is left out.
- DECISIONS 2 Nov 13:16: Epic's garment meshes cannot be exported, and a game MetaHuman is rebuilt over only after a hashed backup.

## Setting, story, length and shape

- Character names in method lines (steps 1, 5 and 6) are replaced by "a character", "a cast member" and "T_<Name>_Detail", and "the size of the town" by "as big as the whole street". The examples list keeps its names, as the other skills do.
- Nothing about 1990 leaked.
- Length and shape fit the other skills: front matter with a pushy description, a Why paragraph, Always, a requests list, 11 numbered steps each with a **Check:** line, and Records. After the fixes it is 100 lines.
