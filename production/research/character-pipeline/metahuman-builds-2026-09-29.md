# Why a MetaHuman's body settings did not reach its export (UE 5.8), research note, 29 September 2026

**The problem.** Three 178 cm male builds for the clothing session (tools/ue/make_builds.py): the Walter preset duplicated, its body constraints (Height, Fat, Muscularity) set with set_body_constraints and commit_body_state, saved; exported with export_geometry in the same run and again in a fresh run. All three came out identical and not 178 cm, though the same two calls change the cast's bodies. Two failed attempts, so researched (the two-tries rule) by a separate helper reading the installed plugin source and Epic's docs; saved by the builder. "Mine" marks the helper's inference.

**Cause** (installed UE 5.8 MetaHuman plugin source, Engine/Plugins/MetaHuman/MetaHumanCharacter/Source/MetaHumanCharacterEditor, read 29 September 2026):

1. set_body_constraints evaluates the parametric body at once and rewrites the editor's body mesh (MetaHumanCharacterEditorSubsystem.cpp 5541-5562); commit_body_state saves and applies the state in full (5125-5161). No ticks or hidden solve are needed.
2. Opening the character again rebuilds its editor data from its stored body rig when it has one and is not a fixed body type: the body mesh's positions, joints and weights come from the rig, only the normals from the saved state (1106, 1432, 677-708).
3. export_geometry copies the open session's body mesh (MetaHumanCharacterExportBlueprintLibrary.cpp 428-520). Closed after the change and reopened to export, each build was Walter's rigged body.
4. The cast script works because it re-rigs after changing the body (request_auto_rigging): the plugin then saves a new body rig built from the current state (3430-3461).
5. RemoveBodyRig, IsFixedBodyType and ParametricFitToCompatibilityBody are not exposed to Python. Every shipped preset's asset tags read bFixedBodyType False. Mine: that the copy carries Walter's body rig is the only reading that fits both source and symptom.

Epic, "MetaHuman Creator Python Scripting in Unreal Engine" (undated; accessed 29 September 2026): the export tools need the character rigged and export_geometry needs it open for editing; in batch runs use blocking = True, which returns only after the cloud operation completes or fails.

**The fix (the third and last attempt under the rule):** per build, in one editor run: open for edit, set the constraints, commit, request_auto_rigging with blocking True (JOINTS_ONLY, as the cast), export_geometry while still open, close, save. Without the cloud, exporting before closing works for the export only (the saved asset keeps Walter's rig). The known 300 s cloud timeout outside the US (casting/notes/metahuman.md) could still hit it. Check: measure the three bodies' height and girths.
