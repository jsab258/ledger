# The face follows the body (2 November 2026)

**Questions, written first.** (1) How do Epic's MetaHumans keep the face on the body? (2) In a native proxy, the engine's way to put the body's neck and head on the face, keeping expressions? (3) Each route's cost and breakage (curves, mouth, LOD, look)? (4) Which route, what test?

**Sources, read 2 November 2026.**

- **Engine:** UE 5.8 source (E = the engine folder).
- **Epic's plugin assets:** saved node settings decoded tag by tag (scratch parser, no editor).
- **The game:** PersonAnim, CrimeProbe, previews `ron-seated-office-night-2026-10-07.jpg` and `sit-stand-office-2026-10-08.jpg`.
- **Epic's pages,** through a fetch tool that renders rather than copies: [Play a Custom Animation](https://dev.epicgames.com/documentation/metahuman/play-a-custom-animation?lang=en-US); the LODSync and Controlling LODs pages (no face-animation content).

## 1. Epic's way: the face's post-process copies the body

- **Epic's page:** the Face copies the Body's bones in its post-processing AnimBP (Copy Pose From Mesh); other parts use leader-follower; face curves take priority.
- **Epic's editor actor** (`MetaHumanCharacterEditorActor.cpp`):
  - It attaches Face to Body (`:32`) and sets `ABP_Face_PostProcess` on the face (`:77`).
  - In Manual mode it nulls both anim classes (`:91`), so the post-process alone carries the face.
- **The cast's face meshes** (LenaS4, RoccoP2, SamS6) name `ABP_Face_PostProcess` and store no post-process LOD threshold. Their blueprint's `ABP_Face` (one Copy Pose From Mesh) is replaced in the game by ULedgerPersonAnim.
- **The post-process still runs** under any other main class (`SkeletalMeshComponent.cpp:1366-1373`). Its input is the main instance's pose and curves (`:2597-2618`).
- **`ABP_Face_PostProcess`, decoded:**
  - Root ← BlendListByBool("Eable Facial Animation") ← RigLogic ← BlendListByBool (head-movement IK Control Rig or not) ← Layered Blend Per Bone.
  - The blend's **base** is Copy Pose From Mesh: attached parent, copy curves on, mesh pose off, no root bone.
  - Its **layer** is the input pose (our instance). Weight 1, no branch filters (all 875 per-bone weights 0), curves Override. Every node's LOD threshold is -1.
- **Meaning:** every body bone, root to head, comes from the body each frame; our face instance's bones (Look At, calm, the idle's head turns) are discarded. Its curves override the body's copied ones (`AnimationRuntime.cpp:338-345, 2392-2413`; `AnimCurveTypes.h:896-912`). RigLogic writes only the face's variable joints (`AnimNode_RigLogic.cpp:600-620`) and reads its driver joints from the copied pose (`:410-440`), so neck correctives follow the body's neck.
- **Seen in the game:** Ron's seated loop (7 October) and his stand and sit (8 October) played on the body's skeleton only, his face on its standing idle; his head stayed on his neck, even bent double.
- **So the premise is wrong:** a walk, or a break through spine and neck, on the body carries the head. `PersonAnim.h:52-57` and `PersonAnim.cpp:103-104` want correcting.

## 2. The engine's mechanisms

**`FAnimNode_CopyPoseFromMesh`** (`AnimNode_CopyPoseFromMesh.h:23-44`): SourceMeshComponent, bUseAttachedParent, bCopyCurves, bCopyCustomAttributes, bUseMeshPose, RootBoneToCopy.

- **Game thread, before update:** copies the source's (or its leader's) component-space bones, and with bCopyCurves its curves (`.cpp:56-61, 134-204`).
- **Evaluate:** resets to reference, then sets only bones found by name in the source, as local transforms with translation (`:223, 252-276, 330-339`). Bones the source lacks stay at reference; it has no input. bCopyCurves replaces the curves outright (`:280-283`).
- **Native proxy:** works; custom nodes with a pre-update step are registered (`AnimInstanceProxy.cpp:343-353`).
- **Same frame:** a child ticks after its attach parent (`SceneComponent.cpp:2491`), whose tick ends after its evaluation (`SkeletalMeshComponent.cpp:3088-3096`).

**Leader pose:** a follower does not tick its pose (`SkeletalMeshComponent.cpp:1885-1888`), and bones the leader lacks are drawn at reference (`SkeletalRender.cpp:470-497`). On the face: no expressions, blinks or RigLogic.

## 3. Cost and what breaks

| Route | Frame cost | Breaks |
|---|---|---|
| Epic's post-process copy (today) | Paid already: a game-thread array copy, an 875-bone blend, RigLogic. **Not measured.** | Nothing for walks or breaks; the face proxy's Look At, Modify Bones and space conversions are wasted. |
| Copy Pose in our face proxy | A second copy | Duplicates Epic's; facial joints reset unless RigLogic follows. Only if the post-process is off. |
| Leader pose on the face | Cheapest | No expressions, blinks or mouth. |

**Mouth curves (SpeakTick, SayMadeLine)** pass as before.

**Risks:**

- **Head-movement IK:** probably switched by a `HeadControlSwitch` curve (inferred from names); it turns the face's `neck_02` and `head` alone from HeadYaw/Pitch/Roll curves. Keep such curves off both parts (Copy Curves brings the body's to the face).
- **Visibility tick:** `OnlyTickPoseWhenRendered` is in `BP_MH_LenaS4` (component unverified); a body not ticking while its face renders gives a stale copy.
- **Attachment:** the copy finds its source by attachment; the face must stay on the Body.

## 4. Recommended route

1. Keep Epic's face post-process as the face's only source of bones. Nothing needs adding.
2. Make every bone decision on the body alone: walk, breaks (now free to reach spine and neck), Look At, calm, moves, feet.
3. Make the face instance curves-only: face idle (blinks, brows) → Mouth → Said, without Look, Calm, Feet or the space conversions. This saves work.
4. Keep the face attached to the Body, and keep head curves off both parts.

**Test (editor as a screen, then the packaged walk):**

- **Seam:** log each frame body `head` against face `head` (GetSocketTransform) through a walk, a spine-to-head break, a full look, speech while walking, and ForcedLOD 0 to 7. Pass: under 0.05 cm and 0.1 degrees every frame.
- **The copy wins:** face look on with body look off, then the reverse; the head follows the body only.
- **Occlusion:** body behind Mickey's counter, face in view.
- **Mouth:** the face's jaw curve still follows SpeakTick.
- **Cost:** `stat anim` or Insights, three speakers, before and after step 3.
- **Gate:** a close film of the neck seam, a fresh reviewer.

**Unverified or unreached:** which bool drives which blend list; all frame times; the tick option's component; Epic's other 5.8 animation pages. Two forum threads (5.6 "head pops out"; a GASP leader-posed face) are anecdotal only.

**Confidence:** high that the face already follows (source, decoded asset and two pictures agree); medium on the IK switch; costs unmeasured.
