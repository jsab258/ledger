# Breakable glass names, Mafia and KCD2 (read 6 Nov 2026)

Names only, no judgement. Read only; nothing extracted from a game.

## Searched
1. Text in production/research/aaa-reference (CENSUS, CHECKLISTS, PLAYERS, STUDY-PLAN, TALKS, studies/*.md) for glass, shatter, breakable, broken window, destruct, smash. Result: no study text names a breakable or broken window asset. Closest: studies/05-visuals.md counts by name "742 window, 526 glass, 110 curtain, 73 shutter assets" (Mafia) and says window-glass materials were not in the export.
2. find (timeout 240) under F:/LedgerTools/aaa-study/mafia and kcd2, plus the index listings (mafia/index/*.txt, kcd2/index/*.csv).

## Mafia, file-name matches (index listing, under Content/Nero/)
- Window, destructible: Environment/Buildings/Elements/Window/WindowWing60x240cm_02/Destructible/ holds GC_WindowWing60x240cm_02_a, GC_WindowWing60x240cm_02_b, GC_WindowWing60x240cm_Glass_02_a (GC = geometry collection) and SM_WindowWing60x240cm_Broken_Glass_02_a (static mesh).
- Strike ForemanOffice: SM_Strike_ForemanOfficeWindow_01_Damaged and _Destroyed (a damaged and a destroyed mesh).
- GameplayBricks/Destructibles/WindowRandomizer/BP_WindowRandomizer_Template.
- Parade: BP_Parade_WindowSmash_01; Effects/.../Parade/NS_Parade_Windows_Shatter_01.
- Impact rule: Game/NeroImpactRuleDataTableAssets/DestructibleImpactRules/NewCrashObjectsDataAssets/DA_Dynamic_Collision_GlassDynamic.
- Physical material: Materials/PhysicalMaterials/Base/PM_GlassBroken_01_a (also PM_GlassSmooth_01_a).
- Material: Materials/Master/Glass/M_FakeShardsGlass (Subsurface; parameters include Refraction, DifRefraction, Fresnel Color, grunge tiling and colours).
- Effects/ParticleSystems/Destruction/Glass/: NS_Destruction_Glass_sml, _Lamp, _Car_box, _Car_cyl, _Bottle, _Bottle_Green; Meshes/SM_VFX_GlassShard; Materials MI_VFX_Glass, MI_VFX_Glass_01, MI_VFX_Glass_Flash_01, MI_VFX_Vehicle_GlassSpikes. Also Effects/Meshes/SM_VFX_GlassShard_01.
- Debris: Environment/Props/Generic/Debris/GlassShards_Debris_01 (SM_GlassShards_Debris_01_a, _b, MI_GlassShards_Debris_01, three textures).
- Cinematic: NS_Cine_1029_Glass_Shatter, NS_Cine_1420_Glass_Shatter, NS_Cine_0930_Destruction_Glass_Lamp.
- Lamps and cars: many "..._Glass_Shards" and "..._glass_broken" meshes (lamps; vehicle parts such as SM_Dufort30_frame_window_f_glass_broken).
- Sound: Wwise event veh_Glass_Break (VEH_Glass_Break); media names include veh_Car_GlassSmash_med_01 and _02; it also lists bank MS_Prologue_GlassBreak_Scripted.

## Mafia, JSON read
- PM_GlassBroken_01_a.json: PhysicalMaterial, one property, SurfaceType8. No mesh, count, particle or sound.
- veh_Glass_Break.json: AkAudioEvent, 2 sound banks, wem media (vehicle glass smash takes). Vehicle sound only.
- M_FakeShardsGlass.json: master material, parameters as above. No mesh swap stated.
- Whether a window mesh swaps on breaking: not stated in any JSON read. The names (GC_ geometry collection beside SM_..._Broken_Glass; _Damaged and _Destroyed) are names only. The GC and BP assets were listed but not exported: unread.

## KCD2
- Index (kcd2/index/*.csv): Materials/particles/glass_broken.mtl; Objects/intermediates/elements/window_bench-blocks_c-100_broken (.cgf, _lod1, _piece); Entities/BreakableObject.ent.
- Unpacked scripts, read: Entities/BreakableObject.ent points to Scripts/Entities/Physics/BreakableObject.lua (objModel default primitive_box.cgf, nBreakableType 0, PhysicsBreakable, events OnBreak and OnFirstBreak). Scripts/Entities/Others/BreakableObject.lua: fBreakImpuls 7, nDamage 10, Parts LifeTime 20 and Density 100, DyingSound (empty file name, radius 1 to 10), Physics Mass 700, bBreakByCar 1. No glass named in either.
- glass_broken.mtl and the window_bench .cgf files: listed only, not unpacked: unread.

## None found
- Study text naming breakable window assets: none found.
- KCD2 file names matching shatter, glassshard, destruct glass: none found.
