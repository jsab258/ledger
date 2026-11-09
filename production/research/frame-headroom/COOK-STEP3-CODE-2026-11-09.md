# Cooking step 3, the code (9 November 2026)

Item n09-3 step 3 (COOKING-PLAN-2026-11-09.md s5 step 3; fixes 1, 3, 4, 13). Code only; nothing run in Unreal.

## What changed

- **tools/ue/import_vehicles.py, import_glb**: after Nanite calls the new texture_settings(): one `glbTextures=OK|PARTIAL|OFF|RAISED dest= textures= set= resized= refused= left= unchecked= readbackFailed=` line printed and appended to ue-material.txt; LAST_TEXTURE_LINE and TEXTURE_TOTALS for callers. It never fails the mesh; the return tuple and callers are unchanged.
- **tools/ue/glb_texture_settings.py** (new): apply() maps each texture to its role by the Interchange parameter binding it (BaseColorTexture, NormalTexture, MetallicRoughness/OcclusionTexture, EmissiveTexture) and sets compression_settings, srgb, lod_group, mip_gen_settings, never_stream, compression_no_alpha, power_of_two_mode, resize_during_build_x/y. Read back, saved. Sizes: the fascia boards 4096x512, the rest each side's nearest power of two (24 B2 rows asserted), halved together to the kind's texture_max. CompressionNoAlpha where the source alpha is opaque (channel min/max); unknown keeps alpha. Unbound, other-parameter or disagreeing-role textures: logged LEFT. The derived sampler type (make_base_material.derived_sampler_type) is compared with each bound expression's declared type; a mismatch is REFUSED, texture untouched; an unread type is set as unchecked (LEDGER_GLB_TEXTURE_STRICT=1 refuses). **Switch: LEDGER_GLB_TEXTURE_SETTINGS=0 turns the pass off** (on by default).

## API names, 5.8 headers (Engine/Source/Runtime/Engine/...)

- TextureCompressionSettings TC_Default/TC_Normalmap: Classes/Engine/TextureDefines.h 391, 393, 394; property Texture.h 1512
- SRGB: Texture.h 1573. CompressionNoAlpha: Texture.h 1322-1324
- TextureMipGenSettings TMGS_FromTextureGroup: TextureDefines.h 128, 131; MipGenSettings Texture.h 1427
- ETexturePowerOfTwoSetting ResizeToSpecificResolution: TextureDefines.h 178, 198; PowerOfTwoMode Texture.h 1395; ResizeDuringBuildX/Y 1407, 1411
- TextureGroup TEXTUREGROUP_World/WorldNormalMap/WorldSpecular: TextureDefines.h 30-32; LODGroup Texture.h 1544
- NeverStream: Classes/Engine/StreamableRenderAsset.h 370
- ComputeTextureSourceChannelMinMax: Texture.h 1658. Blueprint_GetSizeX: Texture2D.h 361
- EMaterialSamplerType: Classes/Engine/EngineTypes.h 946-954; SamplerType in Public/Materials/MaterialExpressionTextureBase.h 31; ParameterName in MaterialExpressionTextureSampleParameter.h 21; MaterialFunction in MaterialExpressionMaterialFunctionCall.h 86
- GetMaterialExpressions / GetMaterialFunctionExpressions: Editor/MaterialEditor/Public/MaterialEditingLibrary.h 141, 137
- glTF parameter names: Plugins/Interchange/Runtime/Source/Import/Public/Gltf/InterchangeGLTFMaterial.h 18, 54, 59, 81, 84, 88

No Python stubs installed. TMGS_FROM_TEXTURE_GROUP and TC_NORMALMAP are already used here (import_glass_bake.py:145, import_front_joinery.py); TexturePowerOfTwoSetting.RESIZE_TO_SPECIFIC_RESOLUTION and TEXTUREGROUP_WORLD_* are snake-case conversions (**unverified**); a missing name gives READBACK-FAILED.

## Checked

py_compile both; selftest 44/44 (inside import_vehicles' 4/4); displays, rooms, joinery selftests green. `--dry` on the glbs on disk: 45 glbs, 709 images, 698 set, 212 resized, 47 fascia at 4096x512; 11 left unbound, unreferenced duplicates no material loads.

## Unverified until the real import

- Whether the glTF parent's expressions read in a commandlet (else all "unchecked"); whether its orm sampler is LINEAR_COLOR (MASKS: refused).
- Whether blueprint_get_size_x gives the source size after import, and Interchange names textures as the glb's images (fallback only).
- Whether asset_checks.py:867 then reads 4096x512; only then do the fascia rows leave street-sweep-known.json.

## Re-import command (Git Bash; no build or game running)

```
export MSYS_NO_PATHCONV=1
E="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/Win64/UnrealEditor-Cmd.exe"
for s in import_shop_displays import_front_joinery import_vehicles import_shop_rooms; do
  "$E" "C:/Users/Jafar/ledger-local/ue-probe/LedgerProbe.uproject" -run=pythonscript \
    -script="C:/Users/Jafar/ledger-local/tools/ue/$s.py" -EnablePlugins=PythonScriptPlugin \
    -unattended -nopause -nosplash -stdout
done
grep "glbTextures=" ue-probe/ue-material.txt | tail -60
```

Joinery after displays: import_glb deletes the front's folder; joinery re-sets the chandler's slots. LEDGER_DISPLAYS_ONLY=<stems> narrows the first.
