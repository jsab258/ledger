# Review of the shopfront skill (8 November 2026)

Reviewed: .claude/skills/shopfront/SKILL.md against SHOPFRONT-SKILL-SOURCES-2026-11-08.md. The reviewer opened FRONTAGE, SHOPFRONTS-INTEGRATION, gate-ritas-front/GATE.md, GATE-OFFICE, CORNER-PLAN, STEP9-PLAN, UNIT-COSTS, 04-street-world, MAFIA-KIT §2, MAFIA-WEAR §1 and §5, unreal-look.json (glass_cube_*), the shop_views.py docstring, RULINGS.md, canon.md (content rule, brands) and the four skills it points to. RECIPE.md and DECISIONS.md were read only through grep on the cited entries. Most numbers check out exactly: sizes, wear values, lumens, the 30 s settle, the 90 frames, 4.3 ms of 4.98, 487.6 px/m, F0, 45:1, the costs and 0.2 of 255. No contradiction was found with RULINGS, canon or the four skills.

**Verdict: PASS WITH FIXES** (7 faults, none blocking)

1. **Line 3 (description) and line 49 (§5 heading).** The skill says step 9 "9a to 9d" was proven in phase 1. In fact 9c is not solved (the skill's own line 62 says so). The gilt, 9b and 9d passed in the editor only ("Editor only; packaged tonight"), and only 9a has a packaged record, on weak evidence. Sources: DECISIONS 5 Nov 05:45, 13:45, 13:55, 15:30, 15:53; 7 Nov 15:37. Fix: say "9a, 9b and 9d (9c set aside); only 9a recorded packaged", and mark the rest as passed in the editor.

2. **Line 38.** "One cube capture per window ... at 1024" is wrong. The default capture is 256. Only the hero windows the cameras stand at are 1024, and Mickey's door glass is 512. Sources: unreal-look.json glass_cube_size 256, glass_cube_hero_size 1024, glass_cube_heroes_note; DECISIONS 7 Oct. Fix: "256 per window, 1024 for the windows a camera stands at (glass_cube_heroes)".

3. **Line 10.** "Reference first (RULINGS 28 Oct)" points to a ruling that does not exist: RULINGS.md has no such line. The rule is in CLAUDE.md ("Reference first (his rule, 28 October)"). Fix: cite CLAUDE.md instead.

4. **Line 14.** The no-real-brand rule is cited to RULINGS 3 Oct. That line covers minted names, placeholders and poll-tax posters. The rule's home is canon.md "Brands and law", plus RULINGS 25 Oct (a kit import carries no real name). Separately, "no children's goods shown" is not in canon, whose rule is "no children anywhere". Fix: cite canon.md and RULINGS 25 Oct, and either cite a source for the children's-goods line or mark it as a project choice.

5. **Line 75 and line 3.** "The gate skill's ten views": the gate skill defines no ten views. Its §1 lists kinds of view. The ten shop views come from the shop gates (RECIPE 23 Oct fifth and sixth shops; 24 Oct launderette: "ten views"). Fix: list the ten views (the four shop views by day and at night, the hook by day and at night) and cite RECIPE, keeping the gate skill for the method.

6. **Line 8.** FRONT-WEAR-BAKE-2026-10-22.md and production/audits/gate-chandler/GATE.md are listed as research and records, but the sources file says they were cited through other records and never opened. Fix: mark both "cited through GATE.md and RECIPE, not read" until someone reads them.

7. **Line 80 (and line 22, narrow).** The 5.5 h estimate in STEP9-PLAN covers 9a and 9b only, not the whole of step 9. On line 22, "no glazing bar width, no sill section" is in FRONTAGE §1 (its lines 48 and 58), not in "In brief" or "Unreached". Fix: write "5.5 h for 9a and 9b" and cite FRONTAGE §1.

**Order and usability.** The steps run in a usable order: references, kit, glass, signs, paint, wear, night light, checks. A fresh session could follow them. The stated shortfalls are labelled honestly: the blown window, the JPEG blocks, 9c, Mickey's night front and the sash fix shown as unverified.

**Not a fault, worth a line.** RECIPE 30 Oct (the chandler's joinery) records a glTF specular factor arriving at twice the engine's default, which darkened paint by 45%. That is a import trap the skill does not carry.
