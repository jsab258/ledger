# Near hair dark against cards, 7 November 2026

Diagnosis only; nothing run. E: is C:/Program Files/Epic Games/UE_5.8/Engine.

## Is the measure wrong? Partly

- **Read:** Epic's conversion, E:/Shaders/Private/HairShadingCommon.ush 62-97. **Measured** (computed from it): Sheila's settings give base colour 37/17/2, Darren's 32/13/1, Ron's 72/48/20, before white. So black is close to Sheila's and Darren's settings; the cards are far off.
- **Measured:** approved S4-front: crown 65/43/29, side 14/9/6. Her sides were already near black; her lights differ.
- **Measured:** the Keep log ran in editor -game, not packaged (near.log line 32).

**Measured**, median sRGB, 6 November talk frames, patches by eye; cheek ratio 1.05-1.08, so exposure is equal:

| Place | Strands | Cards |
|---|---|---|
| Ron crown | 64/41/37 | 97/83/80 |
| Ron side | 16/8/5 | 103/92/88 |
| Ron moustache | 125/98/81 | 116/88/73 |
| Sheila top | 23/12/8 | 80/74/66 |
| Sheila side | 7/4/3 | 70/63/61 |
| Darren front | 11/3/1 | 65/46/27 |

## 1. Cause

Ruled out:
- **Read:** settings. The only hair line is DefaultEngine.ini:104, commit 55a362413, 2 November; black was noted 26 September (LedgerHair.h 1-3, da55b8b9b).
- **Read:** the talk key. Grooms left its channel on 28 September (LedgerTalkLight.h:84-85).
- **Read:** groom colour. GroomDesc.h has no colour switch. **Unverified:** M_hair_v4 holds the name BaseColorHairAttribute, graph unread.

Likely cause, lighting:
- **Read:** strands take indirect light as pi x hair response x radiance from one direction (E:/Shaders/Private/HairStrands/HairStrandsEnvironmentLighting.usf 771, 780). Cards take 2 pi x response x Lumen's gathered light (DiffuseIndirectComposite.usf 578-579; HairStrandsEnvironmentLightingCommon.ush:91).
- **Unverified:** side fibres look level and miss the overhead sky.
- **Read (names only):** MF_Hair_SaltAndPeper has separate Cards and Strands branches, a possible colour part. Darren, white 0, shows it is not the whole.

Confidence: lighting main, about 70%; this mechanism, about 50%. Rival: voxel self-shadow on direct light.

## 2. Lighting or colour

**Measured:** same values (near.log 2628, 2635), same frame: Ron's moustache 125/98/81, his head side 16/8/5. Card-to-strand linear ratio: crown 2-4, side 25-58. One colour change cannot vary so. Lighting, for Ron; Sheila and Darren unverified.

Test: `-dpcvars=r.HairStrands.SkyLighting.IntegrationType=1` (HairStrandsEnvironment.cpp:64). Sides lift: mechanism confirmed. No change: rival stands; then r.HairStrands.ViewMode=15 shows strand base colour (GroomVisualizationData.cpp:61; packaged use unverified).

## 3. Levers

Run the test first: it sets the near target. The approved crown sits between strands and cards.

1. **Card and mesh slots' values at spawn.** The only lever making near and far equal; no frame cost; about 2 hours (estimate). Risk: the match may hold only in its fitted light; check night and office.
2. **IntegrationType 1 or 0**, one ini line, brings strands towards approved. Cost unmeasured (16 samples, cpp:46). Risk: every strand head changes, Tom's crown, noise.
3. **Lower melanin on strand slots.** Cheap. Risk: pale in direct light (28 September, moustache 8.5 times); approvals lapse.
4. **LODSync 1,1,5,7:** moves the seam only.
5. **Hair back on the key:** rejected 28 September; talks only.

## Not checked

Material graphs; night; strand milliseconds; Tom's cause; the portrait's lights.

## The test, 7 November 16:25

**Seen**, packaged, by eye on one middle frame of each person: with -dpcvars=r.HairStrands.SkyLighting.IntegrationType=1 the sides lift: Ron grey, Darren light brown, Sheila pale grey, indoors. Mechanism confirmed for all three; nothing measured in numbers yet. Frames: F:/LedgerTools/gate/new/hair-near-2026-11-07/integration1. The game ran only with the street's switches (-LedgerSlice -LedgerCrime -Encounter=live -LiveFresh -TalkFake -NoTitle); without them it sits on the title. Taken as try 2 of 2, lever 2, in place of lever 1: one line, near and far by the same light. Owed: its frame cost; Tom's crown; noise; Sheila against her approved S4, which may now be too pale; his look.

## The result, 7 November 19:15

**Seen,** packaged, build 5fd1310, the same film with the setting on and with it put back by -dpcvars: at IntegrationType 1 Darren's hair reads blond with dark roots and Sheila's carries white specks at about 2.6 m; at the engine's default 2 both are dark, as approved. Ron, grey, changes little. Judged by eye on two frames each, in one light (F:/LedgerTools/gate/new/dress-cast-2026-11-07/wide4 and wide4-sky2). The setting is out; try 2 of 2 failed. The near hair's darkness and the change where strands hand over to cards stay as they were, listed; night not looked at. Method lesson: the 16:25 test judged a near middle frame only; the same film at distance would have shown it.
