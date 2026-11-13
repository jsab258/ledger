# Loomwright streets, round 1 (13 November 2026)

His own replacement for Houdini (C:\Game Dev Tools\Loomwright), advisor 119 and 120: its street module, the last of its parts (hair: LOOMWRIGHT-HAIR-ROUND1-2026-11-12.md; cloth: LOOMWRIGHT-CLOTH-ROUND1-2026-11-13.md). Work folder F:/LedgerTools/tool-tests-2026-11/loomwright-street; nothing written into his folder; nothing enters the game.

Method researched: production/research/phase5-procedural/RESEARCH-2026-10-28.md, 28 Oct 2026 (phase 5's route, RULINGS 25 Oct: designed kits placed by Unreal's procedural tools, checked by samples; with MAFIA-KIT-2026-10-28.md and TERRACE-KIT-TABLE-2026-10-29.md for the kit and its period numbers).

## Verdict

**Level 1 (is it good at the job): a layout tool, not a street.** Its terrace job makes a believable row's plan in 0.4 s: twelve houses of mixed width and storeys, bays, a shop front, chimneys, lamps, bins, kerb and road, every size inside its period ranges, 9,690 triangles and 21 draw calls. But what it draws is a grey-box: flat colours, boxes for bays, no brick, slate, wear, glass or depth in the openings. Against the Hook sheet or the Kingdom Come II frames it is nowhere; as phase 5's placement step it is a fair start.

**Level 2 (can the builder use it): passes.** One job file, no clicks, 0.4 s, same bytes twice (its verify), a report, and street_layout.json: every piece by name with position and turn, which is what a placement step must hand to the kit in Unreal.

## The test

| Job | Result |
|---|---|
| street_terrace (its example: 12 houses, 4.4 to 5.2 m frontage, 2 or 3 storeys, bays 60%, shop slot 1, 35 to 40 degree roofs) | rc 0, 0.4 s, 10 checks pass |
| Same job again (verify) | identical output |
| Our kit pieces in its layout | not run: its layout names its own five kit pieces (house shell, shop front, sash window, door, pot, bin); mapping to our terrace kit is the next round's job |

Picture: production/previews/loomwright-street-round1-2026-11-13.jpg (street by day | by night | from above).

## What works

- Rules in the job (frontage, storeys, openings, roof pitch, pots, kerb, clutter per metre) with a check per period range and a triangle and draw-call budget.
- The layout written as data (street_layout.json, street_rules_used.json), separate from the meshes.
- Clutter by rate per metre (bins, bags, litter, stains, puddles), lamps by spacing.

## What fails, and why

1. **The look is a grey-box.** It writes its own simple kit pieces; none of the materials, wear or detail our pieces carry.
2. **One straight row only.** Our street climbs and bends (atlas-01, RULINGS 5 Oct); the job has no curve, slope or second side.
3. **Its period checks are its own ranges**, not our measured tables (TERRACE-KIT-TABLE); a range check passes a row that reads wrong (every house the same brick tone, identical bays).
4. Night view: one flat wash, no lamp pools (RULINGS 1 Oct).

## Improvements, most useful first

1. Read our kit's piece names and sizes (a mapping file), so its layout places our own pieces in Unreal.
2. A path for the street (a curve with heights) instead of a straight line, both sides.
3. Period ranges read from our tables, not its own.
4. Variation rules beyond size: brick tone, door colour, curtains, repairs per house.

## Against the others

Houdini's free edition does the same job (the industry route for rule-built streets) but its free edition limits what it exports (PLAN-2026-11-11; not tested for streets); Unreal's own procedural tools (PCG, already measured in PCG-RESULT-HOME) place our real kit in the engine. Loomwright's layout step could feed either. Worth a round 2 only if the mapping to our kit (improvement 1) exists; otherwise PCG alone covers it.

Cost: about 0.15 h, no helpers ("tool test: Loomwright streets round 1").
