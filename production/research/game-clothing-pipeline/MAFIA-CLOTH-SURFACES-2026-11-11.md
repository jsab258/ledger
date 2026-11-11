# Mafia: The Old Country, cloth and leather surfaces (extraction)

Date: 11 November 2026. Source: material JSON already exported under F:/LedgerTools/aaa-study/mafia/exports/MafiaTheOldCountry/Content/Nero/ (read only, nothing exported). Short name "Clothing" = Characters/Male/Clothing; "Library" = Materials/Functions/Characters/OutfitMatLayerLibrary.

## Questions
1. Boots and leather shoes: parent, parameters, textures. 2. Trousers (denim, work). 3. Cotton/canvas jackets. 4. The shared master material. 5. Table of per-kind numbers.

## Answers

**Finding that frames all five.** No garment has its own cloth parameters. Every instance (MI_*) has parent M_layeredBase (Materials/Master/Characters/OutfitMatLayer/M_layeredBase.json) or an earlier MI. Each instance picks up to 6 material layers (static MaterialLayers list) from the Library, by name. The fabric lives in the layer instance (MLI_*), found in Library/Fabric and Library/Leather. The instance adds only colour tweaks, wear and grime per layer slot (parameters tagged with a layer index).

**Q4 Master.** M_layeredBase.json is the one parent seen in all samples. Exported properties: BlendMode Masked, ShadingModel MSM_Cloth (shading-model field 256), used with skeletal mesh, morph targets and clothing. Instances repeat these as BasePropertyOverrides (Masked, MSM_Cloth, clip 0.3333). No Substrate. The JSON holds no expression graph, so its parameter list with defaults is unread. Parameter names visible only through instances: texture MacroDiffuse, MacroNormal, MacroSGRB; per layer AtlasID, UVTilingX/Y, UVRotation, ColorIntensity, ColorTint, PatternColorTint, NormalStrength, FuzzIntensity, EdgeFuzzFalloff, FuzzCoreIntensity, CoreFuzzFalloff, ScratchLevel/Smoothing/Depth/Roughness/Metallic/Color, ScratchHeightContrast/Strength, Grime Level/Smoothing/Depth/Roughness/Metallic/Color; global MacroColorIntensity, MacroNormalIntensity, MacroRoughnessIntensity, AOIntensity, BaseDarknening, GlobalGrimeLevel/Color, GrimeContribution, ScratchContribution, IDNumber/TopIDNumber/BottomIDNumber. Fuzz function: MF_CharacterFuzzyShading.json (described as velvet or moss emulation). Texture streaming list names T_UniNormal_01a_N (a shared detail normal) and T_burn_N.
**Detail "array":** AtlasID indexes three texture arrays in Materials/Base/Character/CharacterArrays: T_Character_Atlas_D (BC7), _N (normal map), _RMTH (BC7, linear; channel meaning by name only). Slice count and size are not in the JSON.

**Atlas slices (AtlasID in the layer base)**: Canvas 0, Denim 1, Twill 4, Burlap 8, Corduroy 9, Cowhide 18, Fine leather 19, Tempered steel 23.

**Q1 Boots.** Shoes_011_Boots/Materials/MI_Ma_Shoes_011_Boots.json (parent M_layeredBase, Masked, MSM_Cloth). Layers: LeatherFine black, SteelTempered, LeatherFineGrain black, Stitches. Instance values: UVTiling 5x5 on layer 0, ColorIntensity 1.2, NormalStrength 0.96, ScratchSmoothing 0.36, ScratchDepth 0.76, GrimeSmoothing 0.02, ScratchContribution 0.1, BaseDarknening 0.6, ScratchColor (0.19,0.16,0.12), GrimeColor (0.07,0.06,0.05). Textures: MacroDiffuse T_Ma_Shoes_011_Boots_D, MacroNormal _N, MacroSGRB _SGRB, each 2048x2048; SGRB BC7 not sRGB, D sRGB texture group 30, N normalmap group 31, SGRB group 32. SGRB name implies Smoothness, Grime(?), Roughness(?), B(?): letters unverified. Variants _b to _f swap in Cowhide (SaturatedBrown, DesaturatedBrown etc.) and Fine leather. Shoes_014_Boots (inherits 011): layer 0 tiling 5x4, layer 1 tiling 20, NormalStrength 0.72, MacroColorIntensity 1.5, ScratchSmoothing 1.04, GrimeRoughness 0.264. Shoes_013_Boots (inherits 014): layer 5 tiling 12, NormalStrength 2.0. Shoes_009_Fancy (leather, tiling 60 to 80, GrimeSmoothing up to 2.8). Shoes_003_Peasant uses Cowhide (6 uses); SGRB 2048.

**Q2 Trousers.** Pants_025_Hero (MI_..._a to _g): layer 0 swaps by variant: CottonTwill BeigeDirty/Grey (a to c), CottonDenim BrownDarkMiner/GreyDark (d, e), CottonCanvas BrownDarkDesaturated (f), WoolPoplin stripes (g); layer 1 Fine leather or Cowhide; layer 4 LinenBurlap. Instance values: MacroNormalIntensity 1.5, AOIntensity 0.2, Grime 0 to 0.74. Textures T_MI_Ma_Pants_025_Hero_DAO, _N, _SGRB, SGRB 4096x4096 BC7. Denim also in Pants_007, 017, 027 (Racing), 029, 036. Work trousers Pants_002 (seven variants): LinenCorduroy brownDark, Canvas Beige, SteelTempered, plastic; layer 2 tiling 10, ColorIntensity 1.5, ScratchRoughness 0.67; textures D/N/SGRB 2048. Canvas also in Pants_010, 020, 021, 022.

**Q3 Jackets.** Jacket_004_Beggar: layers Denim Brown (or Twill brown / GreenKakhiDesaturated), Fishbone BrownLight, Stitches, Canvas, Pewter, Tears; AtlasID 24 on layer 2; Twill variant d has ScratchLevel 0.78, GrimeLevel 0.97; texture SGRB_M 2048. Jacket_008_Lombra (Twill Khaki), Jacket_002 (Twill brown-grey), VestJacket_006_BanditLeader (Canvas WhiteDirty). No Jackets_* use Canvas/Twill as a "work jacket" class by name; Twill is the common tailoring cotton.

## Q5 Table (layer instance defaults, Library; ML_Base)
| Kind | AtlasID | Tiling (UV) | Normal strength | Fuzz int / edge falloff / core | Notes |
|---|---|---|---|---|---|
| Denim (01a base, Library/Fabric) | 1 | 20 (Blue child 20, BlueDark 15) | 5.0 | 1.2 / 0.5 / 1.0 | Blue tint (0.18,0.27,0.43), ScratchRoughness 2.0, GrimeRoughness 2.0, UVRotation 0.232 |
| Cotton twill | 4 | 20 (Khaki and brown 25) | 5.0 | 1.1 / 3.0 / 0.0 (core falloff 3) | ScratchRoughness 1.0 (brown 0.5), GrimeRoughness 1.33 |
| Cotton canvas | 0 | 20 (Beige 18, Brown 10, BrownDark 14x15) | 5.0 | 1.7 / 1.6 / -1.0 (core falloff 16) | ScratchRoughness 1.0 to 2.0 |
| Corduroy | 9 | 20 | 4.0 | 1.0 / 0.6 / 0.75 | |
| Leather cowhide | 18 | 15 (Lightbrown 5) | 2.0 (SaturatedBrown 3.5) | none | ScratchRoughness 1.1 to 2.0 |
| Leather fine | 19 | 20 (black 15x7) | 3.5 | none | ScratchRoughness 1.3 (BrownDark) |

"Tiling" is the value of UVTilingX/Y; that it means repeats per UV unit of the atlas slice is assumed from the name. Colour and roughness detail strengths beyond these (ColorIntensity 0.9 to 1.5; MacroNormalIntensity 1.0 to 1.5; ScratchContribution 0.1 on boots) vary by instance.

## Unverified / not found
- M_layeredBase's expression graph, defaults and the shading of fuzz in cloth: not in the JSON.
- Atlas array size, slice count, resolution and channel packing of RMTH/SGRB: not in JSON; letters only by name.
- Fuzz or sheen colour: no such parameter appeared anywhere; only intensity and falloff scalars.
- No explicit "detail strength" scalar for colour or roughness; ColorIntensity, MacroRoughnessIntensity (1.0 on Shoes_014) are the nearest.
- Every instance in the studied garments was not read; counts are from a sample (about 25 instances, 30 layer instances).
