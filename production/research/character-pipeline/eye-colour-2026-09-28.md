# MetaHuman eye colour: why every candidate came out green (28 September 2026)

The problem: iris colour set by script (`MetaHumanCharacterEyeIrisProperties`: pattern, primary_color_u, primary_color_v; `commit_eyes_settings`) with values copied from Epic's presets whose pictures show blue or grey eyes (u 0.34 v 0.79, u 0.45 v 0.6) gave green eyes in every build, twice (26 September). Researched by a separate helper from the MetaHuman Character plugin's own files on this PC and Epic's documentation.

## Found

- U is "Primary Color Hue" and V "Primary Color Value": positions on one chart, T_iris_color_picker (512 x 256), read as pixel x and y from the top left (MetaHumanCharacterEyes.h lines 33-96; SUVColorPicker.cpp 361-370). Across: slate blue 0 to 0.3, grey-green about 0.35 to 0.45, olive 0.5, amber and brown 0.6 to 1. Down: dark at the top, paler and greyer lower. (Read from the texture's low-resolution preview; approximate.)
- A fresh `MetaHumanCharacterEyeIrisProperties` has every other field at its C++ default: secondary colour 0.5/0.5 (olive), colour blend 0.5, global saturation 2.0. The presets' blue comes from their secondary colour, blend and saturation, which the script did not copy; so an olive secondary at double saturation turned every eye green.
- Epic's twelve eye presets (Content/Tools/EyePresets, T_EyePreset_001-012) decoded:
  - Preset 004, grey-blue: IRIS007; primary 0.2359/0.7703; secondary 0.2837/0.4953; colour blend 0.6267; softness 0.77; STRUCTURAL; shadow details 0.5364; limbal ring 0.8062 / 0.085 / grey 0.84; global saturation 0.76; tint white.
  - Preset 006, pale blue: IRIS002; primary 0.234/0.9891; secondary 0.2837/0.4953; blend 0.7327; softness 0.77; STRUCTURAL; shadow 0.89; limbal ring 0.775 / 0.085 / grey 0.686; saturation 0.88; tint white.
  - Preset 012, grey: preset 006 with saturation 0.4, tint 1.05, limbal ring grey 0.44.
- The colour is baked at build (BP_DefaultLegacyPipeline_High: bBakeMaterials; T_EyeIrisL_BC and MI_EyeL_Baked in the built character), so a change needs a recommit and rebuild.
- Epic documentation: https://dev.epicgames.com/documentation/metahuman/eye-material-tools (undated, read 28 September 2026).

## Documented or inferred

Read from files: field meanings, defaults, the chart, the presets' values, the baking. Inferred: the chart's colours (from a preview), and that the defaults caused the green (not yet tested in a build).
