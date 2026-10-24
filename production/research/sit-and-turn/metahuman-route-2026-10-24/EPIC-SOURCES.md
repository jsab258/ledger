# Epic's own sources: a MetaHuman on the Game Animation Sample's character, and keeping its feet planted

Read 24 October 2026 (all sources below were read that day, between about 07:30 and 08:45 Swiss time). Primary sources only: Epic documentation, Epic release notes, Epic's tech blog, Epic's Fab listing, one Epic release post on the forums. Non-Epic forum posts are listed separately as leads and prove nothing. Epic's wording is paraphrased here; asset, node and setting names are given exactly.

How read: pages marked "full" were read as their whole page text in the browser pane. Release notes (400k to 720k characters) were searched for keywords and the matching sections read in full. WebFetch was refused by unrealengine.com (403) and, for a while, rate-limited by dev.epicgames.com (429); those pages were then read in the browser pane. One Cloudflare check on dev.epicgames.com was not bypassed; the page loaded normally on a later try.

## The main finding in one paragraph

Epic's documentation for putting a character or MetaHuman on the sample has not been rewritten since the 5.4/5.5 layout. The documentation served as "5.6" and "5.8" still names CBP_Sandbox_Character, CBP_SandboxCharacter_Metahuman_Kellan, ABP_SandboxCharacter and the Character Movement component. No Epic page, blog post or release note found names SandboxCharacter_CMC, SandboxCharacter_CMC_ABP, AC_VisualOverrideManager, or the retargeter RTG_UEFN_to_Metahuman_ovw. What Epic does document is the mechanism: a hidden mover mesh keeps animating, a MetaHuman Body under it runs Retarget Pose From Mesh with a UEFN-to-MetaHuman retargeter, and the other body parts follow the Body by Leader Pose. Epic's only foot-sliding method for retargeting is Speed Planting, documented as an offline workflow. Epic gives no slide figures.

## 1. Epic's documented way to put a MetaHuman (or any character) on the sample's character

Four Epic pages describe it. They agree on the mechanism and differ in detail.

**a. Any character: the sample's own page, section "Importing Your Own Character" [S1, full].**
- Make an IK Retargeter with UEFN_Mannequin as source and your mesh as target.
- Open Content/Blueprints/RetargetedCharacters/ABP_GenericRetarget. Add the retargeter to its IKRetargeter_Map variable under the name RTG_UEFN_to_{name}.
- Make a child Blueprint of CBP_Sandbox_Character. Turn off Visible on its Mesh (CharacterMesh) component.
- Add a Skeletal Mesh component as a child of that Mesh, set to your mesh. Give it the Component Tag RTG_UEFN_to_{name}; the tag picks the retargeter from the map.
- The page says to set that child's Animation Blueprint to ABP_SandboxCharacter. This contradicts [S2], which says ABP_GenericRetarget, and the map step above. It is probably an error in Epic's page (unverified).
- The page's link for the IK Retargeter goes to a 404 page. Its MetaHuman link is an unfilled template placeholder.
- The same procedure is served for doc versions 5.4, 5.6 and 5.8 (checked with application_version=5.4 and 5.6).

**b. A MetaHuman: "Adding a MetaHuman to the Game Animation Sample Project" [S2, full].** This page exists in the 5.6 and 5.8 doc sets. The 5.4 and 5.5 doc sets redirect to their home pages.
- In Content/Blueprints/RetargetedCharacters, duplicate CBP_SandboxCharacter_Metahuman_Kellan.
- Delete its Body skeletal mesh component, all of Body's children, and its LODSync component.
- From your MetaHuman's Blueprint, copy Body (with its children) and LODSync. Paste them onto the Mesh component, and drag Body under Mesh.
- Set Body's Anim Class to ABP_GenericRetarget.
- Add the Component Tag RTG_UEFN_to_Metahuman_nrw to Body. The page explains this tells the retarget Anim Blueprint the body type.
- In the viewport, move Body down until the feet meet the bottom of the capsule, and turn it to face the forward arrow.
- Repair the Construction Script: drag the Feet, Legs and Torso references back in so that each Enable Master Pose node has a target.
- In the EnableMasterPose function, wire Body into the New Leader Bone Component pin of the existing Set Leader Pose Component node.
- The page says the sample holds a MetaHuman with preview meshes for every MetaHuman body type, which can be switched on in the Game Utility Widget.
- It says nothing about the Face, the hidden mover mesh's tick setting, the ovw retargeter, or feet beyond placing them on the capsule.

**c. A MetaHuman: MetaHuman documentation, "Runtime Retargeting", section on the Game Animation Sample [S3, full].**
- Make an Anim Blueprint on the MetaHuman's skeletal mesh. In it, connect a Retarget Pose From Mesh node to Output Pose. Leave Retarget Pose on Parental Skeletal Mesh Component. Set IK Retargeter Asset to RTG_UEFN_to_MetaHuman_nrw.
- Paste the MetaHuman's components into a duplicate of Manny's Blueprint, with Body under Mesh (CharacterMesh0).
- Zero Body's transform, then give it a -2 location offset to line up with Manny. The page ties this to the removal of MetaHumans' +2 cm offset. It does not name the axis; vertical is an inference.
- The clothing skeletal mesh may need the same Anim Blueprint.
- Hide Manny by turning off Visible on Mesh (CharacterMesh0).
- The same page also describes a Retarget Component route. It needs the experimental Performance Capture Core plugin and is not used by the sample.

**d. Any hidden source: engine page "Runtime IK Retargeting" [S4, full] and the node's API page [S5, full].**
- Retarget Pose From Mesh on the target's Anim Blueprint, with the target mesh parented to the source. The page still names the old Use Attached Parent option; in the 5.8 API that option is deprecated and replaced by RetargetFrom, which takes the pose either from the anim graph or from another skeletal mesh component.
- When the source character is hidden, Epic says its Visibility Based Anim Tick Option must be set to Always Tick Pose and Refresh Bones (under Optimizations). This is the only Epic statement found on keeping a hidden mover mesh animating. The sample pages [S1, S2, S3] only say to turn Visible off.
- The API says the source mesh component is assumed to be animated and to tick before the target's anim instance [S5].

**Retarget, Leader Pose or Copy Pose.**
- The Body is retargeted with Retarget Pose From Mesh, through ABP_GenericRetarget [S2, S3].
- Torso, Legs and Feet follow the Body through Set Leader Pose Component, in Kellan's EnableMasterPose function, called from the Construction Script [S2].
- No Epic GASP page uses the Copy Pose From Mesh node. The 5.6 release notes say Copy Pose From Mesh logic now sits inside the IK Retargeter (the Copy Base Pose op) and that Retarget Pose From Mesh gained a pose input pin [S10, S6].

**The Face.**
- No Epic GASP page says how the MetaHuman Face follows. Unverified; it needs the assets read.
- Epic's MetaHuman pages say the assembled Blueprint holds Body and Face skeletal meshes, grooms, a LODSync and a MetaHuman component [S19]. They also say it holds functions for retargeting setup [S19], and that LODSync lets Body and Face drive the LODs of Face, Torso, Legs, Feet and the grooms [S20].

**What changed between sample versions (Epic's own record).**
- 5.4: first release. Fab shows it published 11 June 2024 [S15]. Its documentation is [S1].
- 5.5: Epic's 5.5 release post (12 November 2024) says only to try the Chooser features in the updated sample [S16]. No other Epic text on the 5.5 sample was found.
- 5.6: Fab shows an update on 3 June 2025 with no notes [S15]. No Epic text on the 5.6 sample's contents was found, so when AC_VisualOverrideManager, SandboxCharacter_CMC and the _ovw retargeter appeared is unverified.
  - Engine and MetaHuman changes of that release: the IK Retargeter became an op stack; Copy Pose From Mesh logic moved inside the retargeter; Retarget Pose From Mesh gained a pose input pin; source motion can be globally scaled to better pin IK goals [S10].
  - MetaHumans assembled in 5.6 or later lost their +2 cm floor offset and are standardised barefoot. The Body's Component Based Offset can add a sole height back [S17].
- 5.7: Epic blog of 3 December 2025 [S13]; Fab update the same day [S15].
  - New: a character on the experimental Mover plugin, a new locomotion dataset (400 more animations), two Mover modes (Simple Spring Walking, Smooth Walking), a Smart Object level, basic NPCs that sit on benches, a Pose Search column in Choosers, a slide move, and a Footplacement Control Rig node.
  - The blog points to "the GASP documentation" for details. No such page was found.
- 5.8: Epic blog of 12 August 2026 [S14]; Fab updates on 17 June 2026 (no notes) and 17 August 2026 ("UE 5.8 GASP update") [S15].
  - New: the SandboxCharacter_Mover_Ragdoll pawn, physics control, multi-character motion matching, a Look-At Control Rig, a reworked Mover pawn blend stack driven by a Chooser with a Pose Match column, slope blend spaces, and player bench interaction through State Tree.
  - Nothing is said about MetaHumans or retargeting.
- Fab lists the sample for engine versions 5.4 to 5.8 [S15].

## 2. What Epic says about feet sliding when retargeting to different proportions

**Epic's dedicated page, "Fix Foot Sliding with IK Retargeter" [S8, full].**
- Epic's cause: sliding appears when the source and target have very different leg lengths and stances, so leg retargeting is imperfect.
- Epic's fix is Speed Planting, which pins IK goals while they should be still:
  1. Add a speed curve to each source animation with a Motion Extractor modifier per foot bone. The example uses ball_l and ball_r, Translation Speed, axis XYZ, giving curves such as ball_l_translation_speed_XYZ.
  2. Give the target's IK Rig foot goals and a Full Body IK solver rooted at the pelvis. Preferred angles on thigh and calf are given in the example.
  3. Set each leg chain's speed curve name and a Speed Threshold just above the curve's flat part; the example uses 30.
- The page then exports retargeted sequences. It does not say whether Speed Planting works live behind motion matching. Unverified.
- The 5.8 API shows the speed-planting op reads data from the anim graph while it evaluates and lists the speed curves it requires [S9]. That suggests a live use. Unverified: which mesh's curves it reads, and whether the sample's database animations carry such curves.

**The retargeter's op stack in 5.6 and later [S6, full; S7, full; S10, S11, S12 sections].**
- IK goals on the leg chains are needed for Speed Planting, Stride Warping and Blend to Source [S7].
- Pelvis Motion:
  - Epic calls it critical to stop animation sliding, because it scales pelvis translation between characters of different proportions.
  - Scale Horizontal and Scale Vertical scale the pelvis motion.
  - Affect IK Horizontal and Affect IK Vertical decide whether the IK goals follow a modified pelvis.
  - A floor constraint uses crotch offsets and a ground falloff. 5.8 added control so the vertical pelvis motion of shorter characters is not damped [S12].
- Run IK Rig sub-ops:
  - **Speed Plant IK Goals**: per chain Alpha and Speed Curve Name. Op-wide Alpha, Speed Threshold, Blend Method (Spring, or Move Towards, which only blends out of a plant), and Critical Damping.
  - **Stride Warp IK Goals**: Direction Source (Goals for bipeds), Forward Direction (usually Y), Warp Forwards, Sideways Offset and Warp Splay.
  - **Floor Constraint**: holds a goal at the source's height near the floor. Since 5.8 it has foot settings: Use Foot, Use Toes, and heel, toe, side and vertical offsets, all defaulting to 10 cm [S6, S12].
  - Blend to Source, Offset Goals and Scale Goals were split into separate ops in 5.8 [S12].
- Scale Source: scales the whole source pose. It affects goals that use Blend to Source. Epic says it works best at the top of the stack and, together with Pin Bones, improves transfer between characters of different heights.
- Stretch Chains: matches chain length to the source.
- Root Motion op:
  - Root motion is either copied from the source root (scaled by height) or generated from the target pelvis. Root height is copied from the source or snapped to the ground.
  - Ignore Root Lock in Preview has no effect at runtime, where root motion is copied from the source [S7].
- 5.7 release notes list better foot contact: crotch height, floor constraint on feet, Stretch Chain, a source-scale pivot, and Filter Bones [S11].
- 5.8 release notes list a foot definition (foot plane and toes) for runtime and capture retargeting. The 17 biped templates now split each leg chain at the ankle, with a new foot chain for ball and toe, and keep the IK goal at the ankle [S12].

**The sample's own anti-slide pieces, on the mover's skeleton before any retarget [S1, full].**
- Offset Root Bone (experimental) keeps the mesh planted when the capsule and the animation disagree. Epic lists three known issues: no collision check, a release problem with montages, and hard-coded interpolation.
- Leg IK pins the feet to the IK foot bones, which pose warping moves.
- Enable Steering keeps idle animations from being steered, which Epic says could cause sliding.
- Orientation Warping and Steering live in the Motion Matching node's blend stack graph.
- Epic does not say whether a retargeted body keeps the planting these pieces give the source. Unverified.

**nrw and ovw.**
- Both MetaHuman pages use RTG_UEFN_to_Metahuman_nrw [S2, S3]. No Epic source mentions the _ovw retargeter.
- Epic's body-type list has 18 types: f or m, then med, srt or tal, then nrw, ovw or unw, plus BlendableBody. Epic does not expand the codes [S18].
- Epic's shared skeleton sits in a folder named Female/Medium/NormalWeight [S19]. That supports "nrw = normal weight, med = medium height". "ovw = overweight" is inference.
- No Epic source says which retargeter a given MetaHuman body should use for its feet.

**Numbers.** No Epic source gives a foot-slide tolerance or any measured slide. Nothing in Epic's sources speaks to a 3 cm bar.

## 3. Puppet or possessed; how input and gait are read

- Epic documents the sample's characters only as the player's pawn. The Game Animation Widget's Character Override swaps the Game Mode's pawn class [S1].
- No Epic source documents driving the sample's character as a puppet from another pawn.
- Epic mentions non-player use only in passing: basic NPCs that sit on benches (5.7) and an NPC-style patrol for Look-At (5.8). It does not say how they are driven [S13, S14].
- The runtime-retargeting page only asks that the source character be one the player can control, for previewing [S4].
- Input:
  - Enhanced Input is used; Epic names no input actions [S1].
  - Controls: WASD or left stick moves. Left Ctrl or the right shoulder button toggles walk and run. The middle mouse button toggles free rotation and strafe. The right mouse button aims. Space jumps or traverses [S1].
- Gait:
  - The Chooser called in Update_MotionMatching lets only walk databases be searched while the character walks, which the player's input controls [S1].
  - The lean calculation uses the Character Movement component's Max Acceleration and Max Braking Deceleration [S1].
  - Epic gives no walk or run speed values anywhere.
- Mover (the other character, not SandboxCharacter_CMC):
  - Mover is experimental. Its inputs are made by the controlling owner [S22].
  - A NavMoverComponent with a NavWalking mode serves navigation [S22].
  - The input-producer interface is mentioned in Epic's API pages (seen in search only, not read).

## 4. What Epic says is needed to migrate and package the character

- The sample's page covers only migrating the animations: right-click Migrate on Content/Characters/UEFN_Mannequin/Animations, or export them [S1].
- The Motion Matching page requires the Pose Search plugin and animations with root motion enabled [S21].
- Mover is an experimental plugin [S13, S22].
- The Relative IK and Body Intersect retarget ops need the experimental Spatially Aware Retarget Ops plugin [S6].
- No Epic source lists the plugins, project settings, collision or trace channels, Chooser setup or packaging steps needed to move SandboxCharacter_CMC into another project. Not documented by Epic. Any such list must come from the sample's own files.

## Sources (all read 24 October 2026)

| # | Link | What it gives |
|---|---|---|
| S1 | https://dev.epicgames.com/documentation/en-us/unreal-engine/game-animation-sample-project-in-unreal-engine (also ?application_version=5.4 and 5.6) | Sample overview; importing your own character; controls; Anim Blueprint nodes and functions (Offset Root Bone, Leg IK, Enable Steering, Chooser gait). Served as 5.8 docs; describes the 5.4 layout. Full. |
| S2 | https://dev.epicgames.com/documentation/unreal-engine/adding-a-metahuman-to-the-game-animation-sample-project-in-unreal-engine?application_version=5.6 (and the 5.8 default) | MetaHuman steps from the Kellan Blueprint: ABP_GenericRetarget, tag RTG_UEFN_to_Metahuman_nrw, Set Leader Pose Component for Torso, Legs and Feet. Not present in the 5.4 and 5.5 doc sets. Full. |
| S3 | https://dev.epicgames.com/documentation/metahuman/runtime-retargeting | Retarget Pose From Mesh with RTG_UEFN_to_MetaHuman_nrw; Body under CharacterMesh0; -2 offset; hide Manny. Full. |
| S4 | https://dev.epicgames.com/documentation/en-us/unreal-engine/runtime-ik-retargeting-in-unreal-engine | Hidden source needs Visibility Based Anim Tick Option = Always Tick Pose and Refresh Bones. Full. |
| S5 | https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/IKRig/FAnimNode_RetargetPoseFromMesh | RetargetFrom mode; the source must tick first; Use Attached Parent deprecated; override sets. Full. |
| S6 | https://dev.epicgames.com/documentation/en-us/unreal-engine/retargeting-operation-stack-in-unreal-engine (resolves to the 5.8 page) | Every retarget op and setting, including Speed Plant, Stride Warp, Floor Constraint, foot settings, Pelvis Motion, Root Motion and Scale Source. Full. |
| S7 | https://dev.epicgames.com/documentation/en-us/unreal-engine/ik-rig-animation-retargeting-in-unreal-engine | IK goals needed for planting and warping; override sets and variables on Retarget Pose From Mesh; root lock note. Full. |
| S8 | https://dev.epicgames.com/documentation/en-us/unreal-engine/fix-foot-sliding-with-ik-retargeter-in-unreal-engine | Cause of sliding and the Speed Planting workflow with example values. Full. |
| S9 | https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/IKRig/FIKRetargetSpeedPlantingOp | The op reads anim-graph data and lists its required speed curves. Full. |
| S10 | https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-6-release-notes?application_version=5.6 | Op stack; Scaled Proportioned Retargeting; Copy Pose From Mesh logic in the retargeter; pose input pin. Keyword sections. |
| S11 | https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-7-release-notes?application_version=5.7 | Better Foot Contact and Proportioned Retargeting; runtime retarget performance. Keyword sections. |
| S12 | https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-8-release-notes | Foot Definition for Retargeting; override sets; biped templates split leg and foot chains. Keyword sections. |
| S13 | https://www.unrealengine.com/tech-blog/explore-the-updates-to-the-game-animation-sample-project-in-ue-5-7 | 5.7 sample changes (3 Dec 2025). Full, in the browser pane (WebFetch got 403). |
| S14 | https://www.unrealengine.com/en-US/tech-blog/download-the-latest-game-animation-sample-project-now-updated-for-ue-5-8 | 5.8 sample changes (12 Aug 2026). Full, in the browser pane. |
| S15 | https://www.fab.com/listings/880e319a-a59e-4ed2-b268-b32dac7fa016 | Versions 5.4 to 5.8; published 11 Jun 2024; changelog dates. Full, including the changelog panel. |
| S16 | https://forums.unrealengine.com/t/unreal-engine-5-5-released/2117936 | Epic's 5.5 release post (Amanda Schade, 12 Nov 2024): the sample was updated for Choosers. No staff badge visible; read via WebFetch. |
| S17 | https://dev.epicgames.com/documentation/metahuman/base-skeleton-offset-update | +2 cm offset removed for MetaHumans assembled in 5.6+; Component Based Offset. Full. |
| S18 | https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/MetaHumanSDKRuntime/EMetaHumanBodyType | The 18 body-type codes, not expanded. Full. |
| S19 | https://dev.epicgames.com/documentation/metahuman/assets-overview | MetaHuman Blueprint contents; skeleton path .../Medium/NormalWeight/...; RTG_MH_IKRig. Full. |
| S20 | https://dev.epicgames.com/documentation/metahuman/lodsync-component-for-unreal-engine | Body and Face drive the LODs of the other parts; Forced LOD and Min LOD. Full. |
| S21 | https://dev.epicgames.com/documentation/en-us/unreal-engine/motion-matching-in-unreal-engine | Pose Search plugin; root motion required. First half full, rest keyword-scanned. |
| S22 | https://dev.epicgames.com/documentation/en-us/unreal-engine/mover-features-and-concepts-in-unreal-engine | Mover is experimental; inputs come from the controlling owner; NavMover. Short page, keyword-scanned. |
| S23 | https://dev.epicgames.com/documentation/metahuman/updating-retarget-source-asset-in-the-body-rig | Post-process Anim Blueprint pose assets need their retarget source updated for some imported MetaHumans (5.6+). Full; marginal. |
| S24 | https://dev.epicgames.com/documentation/metahuman/metahuman-creator-body-params-tool-in-unreal-engine | Fixed (compatibility) body types exist; no codes given. WebFetch summary only. |

## Could not be reached, or not found

- No Epic page documents the 5.6+ layout (SandboxCharacter_CMC, SandboxCharacter_CMC_ABP, AC_VisualOverrideManager, MetaHumans/Kellan, RTG_UEFN_to_Metahuman_ovw). Searched; none found.
- The "GASP documentation" for 5.7 changes that Epic's blog points to was not found. Fab's notes for the June 2025, December 2025 and June 2026 updates are empty.
- No Epic text on the 5.5 or 5.6 sample's contents beyond [S16].
- The GASP page's MetaHuman link is an unfilled placeholder, and its IK Retargeter link goes to a 404.
- FIKRetargetSpeedPlantingOpSettings API page: redirected to the docs home.
- Not read: Pose Warping page (Orientation and Stride Warping nodes), "Retargeting Bipeds with IK Rig", Migrating Assets, and Epic videos (Unreal Fest and Inside Unreal sample talks); no readable transcripts were sought.
- Whether Retarget Pose From Mesh still copies curves in 5.6+: the 5.8 API shows no copy-curves property. Unverified.
- unrealengine.com refuses WebFetch (403). dev.epicgames.com rate-limited WebFetch (429) for part of the session.

## Leads from non-Epic people (not evidence)

- Forum 2837097, Onub3nse52, 14 Oct 2026, UE 5.8: in the sample, the MetaHuman is retargeted from the pawn's own CharacterMesh0. The hidden mesh drops to a lower LOD without finger bones, so the hands freeze. Setting Forced LOD Model = 1 on CharacterMesh0 fixed it for them. The toggle DDCvar.VisualOverride was used for testing. https://forums.unrealengine.com/t/gameanimationsample-5-8-bad-retargeting-to-metahuman/2837097
- Forum 2836922, ChenDong, 5 Oct 2026: describes the hidden mannequin with Always Tick Pose and Refresh Bones; ABP_GenericRetarget plus a tag; face and clothing by Set Leader Pose to Body; pick the retargeter variant for the body type. https://forums.unrealengine.com/t/has-anyone-figured-out-how-to-add-a-character-to-the-game-animation-sample-project-in-ue-5-8/2836922
- Forum 2835719, 30 Sep 2026: a user says CBP_SandboxCharacter_Metahuman_Kellan is no longer in the 5.8 sample. The reply: Leader Pose does not retarget between skeletons; do not use LODSync as a pose leader. https://forums.unrealengine.com/t/ue-5-8-game-animation-sample-gasp-how-to-apply-metahuman-to-mover-based-sandboxcharacter-without-crash/2835719
- Forum 2795879, BRS_GerDAngelo, 17 Sep 2026: hunched and stretched MetaHumans in the sample put down to the retarget pose and FK translation modes. https://forums.unrealengine.com/t/help-with-game-animation-sample-project-and-metahumans/2795879
