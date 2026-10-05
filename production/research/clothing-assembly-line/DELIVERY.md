# The clothing assembly line: can a spec go in and a dressed character come out

Research delivery, topic 32. Written 2026-09-18 on branch
`research/clothing-assembly-line` from `a305518b`.

Nothing in it is an instruction. It is evidence, an argument from that
evidence, and a recommendation Jafar decides on.

---

## FIRST LINE, BECAUSE THE BRIEF ASKED FOR IT

This CAN be settled from here, and mostly it already is. The brief offered
the escape hatch "if the honest answer is that this cannot be settled from a
container with every documentation host blocked, say so in the first line."
It does not apply, for two reasons neither of which was true on the earlier
topics:

1. **The assembly line is in this repository.** It is not documentation. It
   is `tools/imagegen/imagegen.py`, `tools/meshgen/meshgen.py`,
   `tools/meshgen/blender/clean_lod.py`, `tools/ue/import_prop_meshes.py`,
   and the landed evidence files those runs wrote. I read all of them and
   ran measurements against the repository's own assets rather than
   describing what such a line might look like.

2. **The Blender 4.5 Python API is readable from this container.**
   `pypi.org` answers 200. The `fake-bpy-module-4.5` distribution
   (version 20260730, 967,552 bytes, downloaded and opened today) is the
   generated stub of the entire Blender 4.5 API, and Jafar's PC runs Blender
   4.5.13 LTS. So the operator names, their parameters and their enum values
   below are read off the API surface of the version we actually have, not
   off a search summary. Caveat stated once and carried: a stub proves a
   SIGNATURE EXISTS, not that the operator behaves as intended at runtime.
   Everything marked RUNTIME-HOLE below needs the PC.

What could NOT be settled from here is named in section 8 and is four
questions, all of which are one Blender run on the PC.

**Egress, re-measured today (2026-09-18), because every earlier delivery had
to say every research host was blocked:** `pypi.org` 200 and FULLY READABLE,
`raw.githubusercontent.com` 301 (follows to content), `github.com` 400,
`docs.blender.org` 000, `projects.blender.org` 000, `dev.epicgames.com` 000.
So Blender's own manual, Epic's documentation and every vendor page remain
unreadable. Package metadata and source distributions on PyPI are a primary
source and are new to this delivery.

---

## THE SHORT ANSWER

**The same line can exist. Nothing in the three named gaps is fundamental.
What stops the line today is not clothing at all: it is that the GENERATION
stage of the 3D line has never run on any machine this project owns, and it
stops kerbs exactly as hard as it stops coats.**

That is the honest correction to the premise. The brief says "we have an
assembly line for 2D and one for 3D static objects: a spec goes in,
generation and material work happen, an artifact comes out, it is imported
and verified, and nobody hand-modelled anything." Measured:

- **The 2D line is real and complete.** 41 images written on Jafar's PC on
  2026-09-03 in 56 minutes, 0 failed, of 45 in the batch, by
  stable-diffusion.cpp running Z-Image-Turbo Q4_K under Apache-2.0. They are
  committed at `ledger/Assets/StreamingAssets/Decals/generated/` and they
  REACH THE FRAME, checked rather than assumed: the Unity build's verdict
  prints `decalsApplied=20/20`, `decalImages=15`, `decalsAbsent=none` beside
  `propsPlaced=23/23`, and `StreetVignetteAssets` exists specifically because
  on 2 September that number was zero and nothing said so. Spec in, artifact
  out, nobody drew anything, and an instrument proves the call happened.
  (`ledger/Assets/StreamingAssets/Decals/generated/PROGRESS.txt`,
  `ATTRIBUTION.json`, `game-design/sim-shots/verdict.txt`,
  `ledger/Assets/Scripts/Core/StreetVignetteAssets.cs`.)

- **The 3D line is a CLEANING line, not a generation line.** Its generation
  stage is TRELLIS, which `tools/meshgen/meshgen.py --command probe` refuses
  on Jafar's machine for four independent reasons, each sufficient alone:
  TRELLIS states an NVIDIA GPU with at least 16 GB is necessary, the machine
  is an AMD Radeon RX 6700 with 9.98 GB, there is no Visual Studio at all to
  compile the CUDA submodules, and upstream says "the code is currently
  tested only on Linux". So the `trellis` batch has never been run, and
  `tools/meshgen/specs/props-trellis-01.json` says so in its own comment.
  What DID run is the `local` batch: Blender 4.5.13 headless over 37 CC0
  props that were already in the repository, measuring, pivoting, decimating
  and exporting them. Every mesh in this project today was authored by a
  third party.

- **And the cleaning line's output never reached the engine.**
  `content/props/manifest.json` is committed and says `status: DONE 37/37`.
  The GLBs it names are not in the repository: `find content/props -name
  "*.glb"` returns 0 files, of 37 the manifest lists.
  `tools/ue/import_prop_meshes.py` reads `ledger/Assets/Props/base-mesh`
  (39 GLBs, the hand-sourced CC0 originals) and not `content/props`. The two
  halves of the static line are not joined. The 39 against the batch's 37 is
  not a discrepancy: `fascia_console_01` and `fascia_cornice_01` landed after
  the spec was written, and nothing in the spec is missing from disk.

So the accurate framing of this topic is not "can clothing join a finished
line". It is: **the line has three working stations and one that has never
run, and the clothing question is whether clothing breaks the three that
work. It does not. It breaks four lines of one Blender script and five
references in one Python file, and those are the whole of it.**

---

## 1. THE LINE, STEP BY STEP, AS IT WOULD HAVE TO WORK

Eight steps. For each: the tool, whether it runs headless and scripted,
whether it is automatable or needs a person, and the evidence.

### Step 1: garment spec from canon and the period research

| | |
|---|---|
| Tool | a JSON spec file in the shape of `tools/meshgen/specs/props-local-01.json` |
| Headless | it is a file, so yes |
| Automatable | the SHAPE is; the CONTENT is one person's judgment per garment, once, and then it is data for ever |

The input is not empty, and this corrects an assumption worth naming.

**`canon.md` says nothing about clothing.** 119 lines, and the only hit for
any clothing word is line 75, which is about swearing. So canon is not the
source for step 1 and cannot be.

**The period research exists and is CITED.**
`production/art/atlas-02/research/adult-clothing-by-occupation.md`, 182
lines, on main, carries the donkey jacket with its construction:

> CITED: the donkey jacket is a medium-length unlined jacket in black or dark
> blue thick Melton wool with the shoulders reinforced front and back in
> leather or PVC, developed in 1888 for navvies on the Manchester Ship Canal;
> the shoulder panel sheds rain and takes the weight of timber or tools
> carried on the shoulder; it was in wide use through the 1980s among dockers,
> builders, miners and binmen.

The same file carries HOLE 1 (hi-vis could not be dated, so nobody wears
any) and HOLE 2 (boot standards), which is the labelling discipline a spec
can inherit directly.

**A colour palette exists in Core.** `ledger/Assets/Scripts/Core/Wardrobe.cs`
has a `navy` band described in its own comment as "parkas, donkey jackets,
anoraks", at hue 0.60 to 0.66, saturation 0.30 to 0.52, value 0.16 to 0.30,
weight 4 of a seven-band table. The garment spec does not have to invent a
colour. It reads one.

**And the garment is already load-bearing in the moat.** The dialogue work
of 2026-09-09 records rung-2 identification clauses in which an NPC says
"the one that did the window on Quay Street had a donkey jacket on"
(`game-design/decision-2026-09-09-the-twelve-clauses-and-the-buried-grate.md`).
The donkey jacket is not set dressing. It is the descriptor the perception
ladder hands to gossip. If the town talks about donkey jackets and nobody in
it wears one, the moat's own evidence does not exist in the frame.

One thing IS missing at step 1 and it is a process fact rather than a
research fact: `git ls-tree main production/research/` returns nothing.
Every one of the 32 research topics sits on an unmerged branch. The atlas
research is on main; this lane's is not.

### Step 2: reference plate from our own image lane

| | |
|---|---|
| Tool | `tools/imagegen/imagegen.py`, spec in the schema of `tools/meshgen/specs/prop-images-01.json` |
| Headless | YES, and proven on the real machine |
| Automatable | generation yes; the review is a person and is ALREADY IN THE DESIGN |

Measured, not assumed. `PROGRESS.txt` from the 2026-09-03 run: batch
`meridian-signage-01`, 41 written, 4 already there, 0 failed, of 45, elapsed
56 minutes. Per-image times by size: 768x512 in 56 to 57 seconds, 1024x512
in 90 to 92, 640x896 in 102 to 104. So a plate for one garment costs about a
minute of PC time.

The framing needed already exists as a written rule.
`prop-images-01.json` says: "THE FRAMING IS FOR IMAGE-TO-3D, NOT FOR A WALL.
A single object, isolated, whole in frame, evenly lit, on a plain
background: that is what a reconstruction model can use." A garment plate is
that framing with a garment in it.

The human step is already named: the attribution file says "every image is
review=pending in manifest.json until a human has looked at it for real
marks and real faces". That is the 2D line's answer to "what needs a
person", and a clothing line inherits it unchanged.

### Step 3: mesh

| | |
|---|---|
| Tool | TRELLIS / TRELLIS 2 (MIT, allowlist line 2, ship-safe) |
| Headless | yes, by design |
| Automatable | yes, AND IT CANNOT RUN HERE |

**This is the step that stops the line, and it stops it for props too.** The
four blockers are quoted above. They are measured against
`game-design/agent-reports/machine-report.txt` and
`production/d1-probe/ue-machine.txt`, and the probe prints all four in under
a minute having downloaded nothing.

Three routes exist past it, and only one of them is free:

- **Meshy or Tripo at their paid tiers** are on the allowlist (line 2,
  "paid tiers only"). A purchase, and Jafar's alone.
- **A garment out of the pool we already hold.** See section 3: The Boss
  carries a separate skinned `Jacket_Geo`, Joe a separate `Ch33_Suit`. These
  are Mixamo assets on Jafar's account and are not period, but for proving
  the LINE they are free and immediate.
- **Blender from flat patterns.** Free, needs a person with an opinion, and
  is the one route that produces a garment nobody has to own.

### Step 4: fit to the target body

| | |
|---|---|
| Tool | Blender: Shrinkwrap, Surface Deform, Lattice, or a plain scale |
| Headless | YES, proven: Blender 4.5.13 ran `clean_lod.py` unattended over 37 props |
| Automatable | **YES for a shoulder-hung garment, and the measurement says why** |

Answered in full in section 4.

### Step 5: skin weights

| | |
|---|---|
| Tool | `bpy.ops.object.data_transfer(data_type="VGROUP_WEIGHTS", ...)` |
| Headless | yes |
| Automatable | **YES, and the hard version of the problem does not exist on our pool** |

Answered in full in section 5.

### Step 6: material

| | |
|---|---|
| Tool | `tools/imagegen` for the albedo, `Wardrobe.Bands` for the tint, `tools/ue/make_base_material.py` for the Unreal material |
| Headless | yes; `make_base_material.py` runs under `UnrealEditor-Cmd.exe -run=pythonscript` |
| Automatable | the plumbing yes; the albedo art is a person once |

`make_base_material.py` exists for a reason this line inherits: "Unreal
cannot build a material at runtime: a material is compiled shader code, the
shader compiler is editor-only, and a packaged game can only make INSTANCES
of materials that already exist as assets." A garment material is another
instance of that same problem and the same script shape solves it. The
project already holds 104 ambientCG texture files as the precedent for
sourced surfaces.

One measured caution. `Wardrobe.cs` records, in its own comment, that for
the twelve Mixamo bodies the palette does not reach the render at all:
"models arrive textured, `bodySkinnedEver=0` because nothing is painted, and
the wash maps over a kept Mixamo albedo instead. The yellow is the MODEL's
own texture." `bodySkinnedEver=0` is confirmed in
`game-design/sim-shots/verdict.txt` today. So the colour system and the
bodies are not currently connected, and a garment pipeline that assumes they
are will produce a correct palette nobody can see.

### Step 7: import as a skeletal mesh

| | |
|---|---|
| Tool | `tools/ue/import_prop_meshes.py`'s own route: `unreal.AssetImportTask` through `AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])` |
| Headless | YES, proven: `UnrealEditor-Cmd.exe LedgerProbe.uproject -run=pythonscript -unattended -nopause -nosplash` |
| Automatable | **YES, and the gap is five references in one file** |

Answered in full in section 6.

### Step 8: verification

| | |
|---|---|
| Tool | `glb_stats` / `mesh_verdict` in `meshgen.py`, plus the Unreal read-back |
| Headless | yes |
| Automatable | yes, AND BOTH HALVES ARE CURRENTLY WRONG FOR A GARMENT |

This is the finding I did not expect and it is the most important one after
section 5.

**The GLB verifier cannot see a skin.** `glb_stats`
(`tools/meshgen/meshgen.py:265`) walks the node graph reading the `POSITION`
accessor and the node transforms. It counts verts, triangles, primitives,
meshes, nodes, materials and images. It reads no `JOINTS_0`, no `WEIGHTS_0`,
no `skins` array. `mesh_verdict` then passes or fails on vertex count,
triangle count and largest dimension. **A garment GLB that arrived with
perfect skinning and a garment GLB whose skinning was silently destroyed are
the same file to this instrument, and both print a green string naming the
same numbers.** That is CLAUDE.md rule 3b with a number on it: a clean result
that cannot tell nothing from fine.

**And the Unreal read-back would reject a correct garment.**
`import_prop_meshes.py` resolves an imported asset through
`isinstance(o, unreal.StaticMesh)` at lines 2863 and 2912, and tallies
`appearedClasses` values equal to the string `"StaticMesh"` at line 3041. A
correctly imported SkeletalMesh is None to both, which is the exact failure
mode the file's own docstring records from run 2:
"a route that ran perfectly and imported the file reported itself as
refused, with no exception to show for it."

So verification is not merely absent for garments. It is wrong in both
directions: it would pass a broken one and fail a correct one. **The
verifier is the first thing to build, not the last** (section 9).

---

## 2. THE FOUR LINES THAT DESTROY SKINNING, NAMED

The brief asked which step stops the line. For the middle of it, the answer
is four lines in `tools/meshgen/blender/clean_lod.py`, and each is correct
for a kerb.

**`clean_lod.py:97`** `return [o for o in bpy.context.scene.objects if o.type
== "MESH"]`. The FBX and glTF importers DO bring an armature in. This filter
drops it from every selection that follows. Everything below is a
consequence.

**`clean_lod.py:169` and `:171` to `:172`** `select_only(objs)` then
`bpy.ops.transform.resize` then `transform_apply(scale=True)`. Scale is
applied to the mesh with the armature not selected and not scaled. A skinned
mesh whose scale is applied while its armature's is not has lost its bind.

**`clean_lod.py:185` to `:187`** the same shape for the pivot: the mesh is
translated to base-centre and the translation applied, while the armature
stays where it was. For a prop this is the one convention that lets a placer
drop it on a pavement. For a garment it walks the cloth off the body.

**`clean_lod.py:215`** `for m in list(c.modifiers):
bpy.ops.object.modifier_apply(modifier=m.name)`. This applies EVERY modifier
in the list, not only the `ledger_tri` and `ledger_dec` the loop just added.
**And the LOD copy loses its skinning either way, which is why this one does
not depend on a Blender behaviour I cannot check from here.** If `c =
o.copy()` at line 202 carries the source object's modifiers, then the
garment's Armature modifier is in that list and gets APPLIED, which freezes
it in its bind pose and removes the skinning. If `copy()` does not carry
them, the copy has NO armature modifier at all and therefore no binding to
export. Both branches end at an unskinned LOD. `Object.copy()` carries no
documentation in the 4.5 stub, so which branch is real is RUNTIME-HOLE 3a
and it changes nothing about the conclusion.

**`clean_lod.py:221`** `bpy.ops.export_scene.gltf(..., use_selection=True)`
with only meshes selected. Read off the 4.5 stub today: `export_skins`
defaults to `True`, so the exporter WOULD write skinning if any survived,
and `use_selection` defaults to `False` and is being set `True` here against
a selection that excludes the armature. Two independent reasons no skin
comes out.

None of these is a design decision about garments. They are four correct
decisions about props, in a script that was never asked about anything else,
and its own docstring says so: "UNRUN WHERE IT WAS WRITTEN."

---

## 3. WHAT A MIXAMO BODY ACTUALLY IS, MEASURED

Topic 31 asserted, and marked ASSUMED, that a Mixamo character's clothing IS
the body mesh. **That is wrong for 14 of the 18 bodies we hold, and I have
now opened the files rather than repeating the claim.**

Method: `tools/body-proportions.py` already contains a stdlib Kaydara FBX
parser that reads `Model`, `Geometry`, `Deformer` and `Pose` records and
skips large payloads. I used the project's own reader rather than writing a
second one. Script kept out of the repository, in the session scratchpad.

**Denominator: 18 FBX examined in `ledger/Assets/Characters/`, 18 parsed,
0 parse failures.**

| model | mesh parts | skins | clusters | mesh names |
|---|---|---|---|---|
| Adam | 7 | 7 | 126 | Body, Sneakers, Eyelashes, **Pants**, **Hoodie**, Hair, Beard |
| Big Vegas | 4 | 4 | 344 | MouthAnimGeo, EyesAnimGeo, BodyGeo, BrowsAnimGeo |
| David | 6 | 6 | 120 | Body, Sneakers, **Pants**, **Hoody**, Eyelashes, Hair |
| Elizabeth | 6 | 6 | 125 | **Pants**, **Shirt**, Body, **Heels**, Eyelashes, Hair |
| James | 1 | 1 | 65 | Ch06 (one fused mesh) |
| Joe | 9 | 9 | 144 | **Shoes, Suit, Belt, Shirt, Tie, Pants**, Body, Eyelashes, Hair |
| Kate | 6 | 6 | 113 | **Pants**, **Shirt**, Body, **Shoes**, Eyelasshes, Hair |
| Leonard | 7 | 7 | 128 | Body, **Pants**, **Sweater**, **Collar**, Eyelashes, **Shoes**, Hair |
| Martha | 7 | 7 | 134 | **Shirt**, **Pants**, **Suit**, **Heels**, Body, Eyelashes, Hair |
| Michelle | 1 | 1 | 52 | Ch03 (one fused mesh) |
| Pete | 8 | 8 | 127 | Body, **Boots**, **Helmet**, **Vest**, **Shirt**, **Pants**, Eyelashes, Hair |
| Remy | 7 | 7 | 114 | **Shoes, Tops, Bottoms**, Hair, Body, Eyelashes, Eyes |
| Shannon | 7 | 7 | 128 | **Shorts**, **Shirt**, **Socks**, Body, **Shoes**, Eyelashes, Hair |
| Sophie | 6 | 6 | 129 | **Cloth**, Eyelashes, Body, **Sneakers**, **Socks**, Hair |
| Sporty Granny | 4 | 4 | 388 | MouthAnimGeo, EyesAnimGeo, BrowsAnimGeo, BodyGeo |
| The Boss | 11 | 11 | 748 | **Jacket_Geo**, **Shoes_Geo**, Cigar_Geo, Head_Geo, Teeth_Up, **Hat_Geo**, R_Eye, L_Eye, Teeth_Down, **Pants_Geo**, Arms_Geo |
| X Bot | 2 | 2 | 129 | Beta_Surface, Beta_Joints |
| Y Bot | 2 | 2 | 104 | Alpha_Surface, Alpha_Joints |

**14 of 18 carry clothing as SEPARATE SKINNED MESHES with garment names.**
2 are fused (James, Michelle). 2 are the grey mannequins. The two
caricatures (Big Vegas, Sporty Granny) fuse their clothing into `BodyGeo`.

So the answer to "does a generated garment arrive as a separate mesh or
fused to the body" is answered for the INPUT side by the files we already
hold: in 14 of the 18 files we own, clothing is a separate skinned mesh with
its own name. Whether that is Mixamo's policy or just what these eighteen
happen to be is not something this measurement can say, and it does not
need to: the fourteen exist. Fourteen worked examples of the
exact thing we want to produce are sitting in the repository.

**And one of them is a jacket.** `The Boss` carries `mixamorig:Jacket_Geo`
as its own skinned mesh. `Joe` carries `Ch33_Suit`. Those are the nearest
things in this project to a donkey jacket, and they cost nothing.

---

## 4. GAP ONE: FITTING A GARMENT TO A BODY IT WAS NOT MADE FOR

**Is it automatable? For a shoulder-hung garment, yes, and the reason is a
single measured number.**

### The tools exist and are scriptable

Read off the `fake-bpy-module-4.5` stub today, all PRESENT in `bpy.types`:
`ShrinkwrapModifier`, `SurfaceDeformModifier`, `LatticeModifier`,
`MeshDeformModifier`, `CorrectiveSmoothModifier`, `ClothModifier`,
`VertexWeightMixModifier`, `VertexWeightProximityModifier`. In
`bpy.ops.object`, 242 operators including `modifier_add`, `modifier_apply`,
`surfacedeform_bind`, `transform_apply`, `shape_key_add`. None of these
needs a UI.

### How much fitting is actually needed

I measured the bind-pose world positions of `LeftArm`, `RightArm`, `Hips`,
`LeftLeg` and `Head` on all 18 bodies, then divided each by that model's own
head height to separate SCALE from PROPORTION. Remy is excluded and the
exclusion is printed: its stored bind pose puts the crown below the skull
and knee, ankle and toe-base at one height, and
`tools/body-proportions.py` already refuses it by name.

**Over the 13 realistic bodies (denominator stated: 13 of 17 after Remy,
excluding 2 caricatures and 2 mannequins):**

| ratio | min | median | max | spread | spread as % of median |
|---|---|---|---|---|---|
| shoulder height / head height | 0.9112 | 0.9204 | 0.9315 | 0.0203 | **2.2%** |
| hip height / head height | 0.6012 | 0.6229 | 0.7499 | 0.1487 | 23.9% |
| shoulder span / head height | 0.1497 | 0.2487 | 0.2929 | 0.1432 | 57.6% |
| head height, absolute | 136.85 | 154.45 | 160.41 | 23.56 | 15.3% |

Statistic named: each row is a per-model reading off that model's own stored
bind pose, and min/median/max are across models, not over time.

**What this says, and it is the whole answer to gap one.** Where a garment
SITS vertically is almost pure scale: shoulder height as a fraction of the
body varies by 2.2% across thirteen bodies. How WIDE it has to be is not:
shoulder span varies by 57.6% of median, and 0.1497 is Michelle, who is the
single outlier (her absolute head height is 136.85 against a median of
154.45, so she is a smaller figure AND narrower for her size). Excluding
Michelle the realistic cluster runs 0.2238 to 0.2929, about 28% of median.

So a shoulder-hung garment needs ONE number per target body: shoulder span,
read off the two bones every body carries. Vertical placement follows from
uniform scale. That is a one-parameter fit, and one parameter read off a
skeleton is a script, not an opinion.

### Why the donkey jacket is the right test and not a soft one

The brief chose it because "it hangs straight from the shoulders and does
not follow the body, and anything fitted will succeed on every route and
prove nothing." That is exactly right, and the research file supports it:
the garment is "untailored at the waist, so that it hangs down straight from
the shoulders", medium length, with a broad stiff collar and a reinforced
shoulder panel. Its fitted dimension is the shoulder seam and nothing else.

But it is not a free pass, and the hard part is the part the measurement
above does not cover: **a garment that hangs free has to NOT INTERSECT the
body underneath it through a whole walk cycle, and interpenetration is a
runtime fact, not a bind-pose fact.** The 2.2% number says the jacket will
sit at the right height at rest. It says nothing about an elbow coming
through a sleeve at frame 40 of a walk. That is RUNTIME-HOLE 1 and it needs
the PC.

---

## 5. GAP TWO: TRANSFERRING SKIN WEIGHTS BETWEEN SKELETONS

**Is it automatable? Yes, and the harder half of the question does not exist
on our pool. There are not several skeletons. There is one.**

### The measurement, and the false zero it started with

I hashed each body's set of bone names. The first run reported **11 distinct
skeletons across 18 files, and "bones present in ALL 18 files: 0"**.

That zero is the instrument, not the world. Mixamo stamps a per-export
namespace on the bone names: `mixamorig:`, `mixamorig1:`, `mixamorig5:`,
`mixamorig7:`, `mixamorig9:`, `mixamorig10:`, `mixamorig11:`. A set
intersection over raw strings cannot see that `mixamorig7:Spine2` and
`mixamorig10:Spine2` are the same bone. I stripped the namespace and
measured again. (CLAUDE.md rule 3: suspect the ruler before the reading. A
zero with no denominator would have read as "eighteen incompatible rigs",
which is precisely the conclusion this topic exists to test.)

**Namespace stripped, 18 files examined:**

- **Bones present in ALL 18 files: 65.**
- Distinct bone-name sets: 5, not 11.
- **14 of 18 carry EXACTLY that 65-bone set and nothing else**: Adam, David,
  Elizabeth, James, Joe, Kate, Leonard, Martha, Michelle, Pete, Shannon,
  Sophie, X Bot, Y Bot.
- The other 4 are SUPERSETS of it: Remy 67, The Boss 68, Big Vegas 86,
  Sporty Granny 99. The 58 non-universal bones are all secondary: hair
  chains, cape segments, collar bones, a visor, a whistle, breast and
  buttock bones, `Belly`, `Neck1`, `LeftEye` and `RightEye`.

The shared 65 are the ordinary Mixamo humanoid: Hips, Spine, Spine1, Spine2,
Neck, Head, HeadTop_End, Left/RightShoulder, Arm, ForeArm, Hand, four
segments on each of five fingers per hand, UpLeg, Leg, Foot, ToeBase,
Toe_End.

**So "transferring skin weights between skeletons" is not the problem we
have.** Within our own pool the transfer is between a body and a garment on
THE SAME SKELETON, and the only cross-file difference is a namespace prefix,
which is a string replace. The hard version of this problem appears exactly
once, and it is at the Mixamo-to-MetaHuman boundary that D2 already commits
us to (`metahuman_base_skel`), which is a different decision and not this
one.

### The operator, read off the 4.5 API today

```
bpy.ops.object.data_transfer(
    data_type      = "VGROUP_WEIGHTS",
    vert_mapping   = "POLYINTERP_NEAREST",
    layers_select_src = "BONE_DEFORM",
    layers_select_dst = "NAME",
    use_create     = True,
    use_max_distance = True,
    max_distance   = <metres>,
    ray_radius     = <metres>,
    mix_mode       = "REPLACE",
    mix_factor     = 1.0)
```

Every parameter above was read out of
`bpy-stubs/ops/object/__init__.pyi` in `fake_bpy_module_4_5-20260730`, and
the enum values out of `bpy-stubs/stub_internal/rna_enums/__init__.pyi`:

- `data_type` accepts `"VGROUP_WEIGHTS"` as its first literal.
- `layers_select_src` (`DtLayersSelectSrcItems`) accepts `"ACTIVE"`,
  `"ALL"`, `"BONE_SELECT"` and **`"BONE_DEFORM"`**, documented in the stub
  as "Deform Pose Bones. Transfer all vertex groups used by deform bones."
  That one enum value is the entire garment-weighting operation.
- `layers_select_dst` (`DtLayersSelectDstItems`) accepts `"ACTIVE"`,
  **`"NAME"`** ("Match target data layers to affect by name") and
  `"INDEX"`.
- `vert_mapping` (`DtMethodVertexItems`) accepts `"TOPOLOGY"`, `"NEAREST"`,
  `"EDGE_NEAREST"`, `"EDGEINTERP_NEAREST"`, `"POLY_NEAREST"`,
  **`"POLYINTERP_NEAREST"`** ("Nearest Face Interpolated") and
  `"POLYINTERP_VNORPROJ"` ("Projected Face Interpolated ... hit by
  normal-projection").

The fallback, if transfer gives a poor result, is also present and
scriptable: `bpy.ops.object.parent_set(type="ARMATURE_AUTO")`, whose `type`
literal includes `"ARMATURE"`, `"ARMATURE_NAME"`, `"ARMATURE_AUTO"` and
`"ARMATURE_ENVELOPE"`. And the cleanup operators a weighting pass needs are
all there: `vertex_group_limit_total` (Unreal and most engines cap
influences per vertex), `vertex_group_clean`, `vertex_group_normalize_all`.

### How big is the weighting job actually

I walked the FBX `Connections` graph to attach each skin cluster to the mesh
it deforms and the bone it weights, and printed the bone list per garment.

| garment | bones weighted |
|---|---|
| Joe `Ch33_Suit` (a jacket) | **28** |
| Leonard `Ch31_Sweater` | **28** |
| Joe `Ch33_Pants` | 13 |
| Joe `Ch33_Shirt` | 12 |
| Joe `Ch33_Shoes` | 8 |
| Joe `Ch33_Tie` | 8 |
| Leonard `Ch31_Collar` | 7 |
| Joe `Ch33_Belt` | 5 |
| Joe `Ch33_Body` | 58 |

A jacket needs weights on 28 of the 65 bones, and most of the 28 are hand
bones for where the cuff meets the wrist. The torso set is about 15: Hips,
Spine, Spine1, Spine2, Neck, Head, both Shoulders, both Arms, both ForeArms,
both UpLegs. That is the size of the job, and `BONE_DEFORM` selects exactly
that set without anybody naming it.

Note on the instrument's accepting and rejecting cases, because the numbers
above only mean something if the reader can discriminate: Joe and Leonard
give sensible per-garment subsets (5 for a belt, 8 for shoes, 28 for a
jacket), which is the accepting case. The Boss reports 68 bones on every one
of its 11 meshes including the cigar and the teeth, which at first reading
looks like the instrument failing to discriminate. The arithmetic says
otherwise: 68 x 11 = 748, and 748 is the cluster count measured
independently in section 3. The Boss genuinely binds every bone to every
mesh. That is a different export convention, not a broken reader.

---

## 6. GAP THREE: IMPORTING A SKINNED MESH INTO UNREAL

**Is it automatable? Yes. The import CALL is already class-agnostic, the
engine already ships the skeletal and cloth pipelines, and what is
StaticMesh-specific is five references in one file.**

### What the landed run measured about the engine

`production/d1-probe/ue-mesh-import.txt`, written by the real editor on
JAFAR-DESKTOP against `C:\Program Files\Epic Games\UE_5.8`, 895 plugins
scanned:

- **`propGltfApi=InterchangeManager;AssetImportTask;InterchangeGenericAssetsPipeline;ImportAssetParameters`.**
  All four present.
- **`propPipelineOpts=...InterchangeGenericMeshPipeline=9-of-86:collision,combine_skeletal_meshes_behavior,combine_static_meshes,...`**
  The pipeline our importer already drives exposes 86 options, and one of
  the nine that matched the run's filter is `combine_skeletal_meshes_behavior`.
  The skeletal path is on the same pipeline object, already enumerated by
  our own run, and `propPipelineOptsFilter=...NOTHING-SET-THIS-RUN/names-read-for-the-next-one`
  says the run deliberately read the names without setting any.
- **`propInterchangePlugins=DatasmithInterchange;InterchangeAxfAssets;InterchangeAxF;InterchangeAssets;InterchangeEditor;InterchangeChaosClothAsset;InterchangeOpenUSD;InterchangeOpenUSDChaosClothAsset;InterchangeOpenVDB;Interchange;InterchangeTests/11`.**
  **`InterchangeChaosClothAsset` is present on the machine.** DERIVED, from
  the plugin name and from topic 31's reading that the Chaos Outfit Asset is
  Epic's garment system: an engine-shipped garment path exists on this
  machine. Stated as a derivation on purpose, because this file's own rule
  is that a plugin's name is not evidence of what it does (the glTF importer
  here lives in plugins whose names contain no GLTF at all). Nothing in this
  recommendation depends on it: the route in section 6 is the plain
  AssetImportTask one we have already run 17 times.
- The import itself succeeded for 15 of 16 assets, by two routes
  (`asset-import-task=15;interchange-import-asset=2`), with the one failure
  named and diagnosed (`pavement_sign` imported as three parts).

### What is actually StaticMesh-specific in our importer

Grepped and read, `tools/ue/import_prop_meshes.py`:

1. **`:103`** `UASSET_PREFIX = "SM_"`, plus `uasset_name()` at `:177`.
2. **`:2863`** `if o is not None and isinstance(o, unreal.StaticMesh):`
3. **`:2912`** `if not isinstance(obj, unreal.StaticMesh):`
4. **`:3041`** the tally counting `appearedClasses` values equal to
   `"StaticMesh"`.
5. **`:241` and the bounds read-back**, which calls
   `unreal.StaticMesh.get_bounds()`, plus the collision reads
   (`EditorStaticMeshLibrary`, `StaticMeshEditorSubsystem` at `:2123`).

**The import call itself names no class at all.** It is
`task = unreal.AssetImportTask()`, four editor properties (filename,
destination_path, destination_name, automated, replace_existing, save), and
`import_asset_tasks([task])`. Interchange decides what to make from what is
in the file. A GLB with a `skins` array produces a SkeletalMesh and a
Skeleton on the same call.

So the honest statement of gap three is: **our importer does not handle
skeletal meshes because its NAMING, its RESOLUTION and its VERIFICATION
assume a static one, not because Unreal or the route is missing.** The
collision reads have no meaning for a garment and simply do not apply; the
bounds read-back has an equivalent (`USkeletalMesh` carries its own bounds)
but it is a different call and the number it returns has a different meaning,
because a skeletal mesh's bounds are pose-dependent.

Two facts that bound the ambition here:

- **`ue-probe` contains no character mesh of any kind today.**
  `ue-probe/Source/LedgerProbe/Public/LedgerCharacter.h` states it: "NO
  CONTENT ASSET ANYWHERE HERE. This project ships no hand-made uasset, and
  there is no Mixamo body in ue-probe yet, so this capsule carries no
  visible mesh." So step 7 would be the FIRST skeletal asset the Unreal
  project has ever held, and the SM_ naming contract has no skeletal sibling
  to be consistent with yet. That is an advantage: nothing has to be
  renamed.
- The existing frame-cost evidence is from the Unity build, not Unreal.
  `game-design/sim-shots/verdict.txt`:
  `frameCost=[all:26.3/.../noBodies:26.2/...]`, so bodies cost 0.1 ms of a
  26.3 ms frame in THAT renderer. It says nothing about Unreal and must not
  be carried across.

---

## 7. THE DONKEY JACKET, END TO END, AND WHERE IT WOULD BREAK

Walking the specific case the brief asked for, using only what is measured
above.

1. **Spec.** Reads `adult-clothing-by-occupation.md` for construction (black
   or dark blue Melton wool, leather or PVC shoulder panel front and back,
   medium length, untailored at the waist) and `Wardrobe.Bands` for the
   colour (`navy`, hue 0.60 to 0.66, sat 0.30 to 0.52, val 0.16 to 0.30).
   **Does not break.** A person writes this once.

2. **Plate.** `imagegen` with the isolated-object framing. About 60 to 100
   seconds of PC time. **Does not break.**

3. **Mesh.** TRELLIS refuses on this hardware. **BREAKS, and it breaks for
   props too.** For a first run, substitute `The Boss`'s `Jacket_Geo` or
   `Joe`'s `Ch33_Suit`: a real skinned jacket on the shared 65-bone
   skeleton, free, in the repository.

4. **Fit.** Read `LeftArm.x` and `RightArm.x` off the target body's bind
   pose, scale the garment by the span ratio, place by shoulder height
   (which varies 2.2%). **Does not break at rest.** RUNTIME-HOLE 1: whether
   it interpenetrates through a walk cycle is unmeasured.

5. **Weights.** `data_transfer(data_type="VGROUP_WEIGHTS",
   layers_select_src="BONE_DEFORM", layers_select_dst="NAME")` from the
   target body onto the jacket, then `vertex_group_limit_total`.
   **EXPECTED NOT TO BREAK, and it has not been run:** same 65 bones, about
   28 of them relevant, one operator whose signature and enum values I read
   off the 4.5 API today. That is a strong expectation, not a result.
   RUNTIME-HOLE 2: the `max_distance` and `ray_radius` numbers
   have no series printed yet, and CLAUDE.md rule 2 forbids setting them
   before one exists.

6. **Clean and LOD.** `clean_lod.py` as it stands **BREAKS IT FOUR TIMES**
   (section 2), silently, and the artifact that comes out is a static
   posed shell. RUNTIME-HOLE 3: whether Blender's Decimate COLLAPSE
   preserves vertex groups well enough for an LOD1 garment is untested here
   and untested anywhere in this project, which has never measured an LOD
   requirement for a character at all.

7. **Import.** `AssetImportTask` on a GLB carrying `skins` makes a
   SkeletalMesh. **DERIVED AND NOT RUN.** What is measured is that the call
   names no class, that the route ran 17 times for static meshes, and that
   the pipeline exposes `combine_skeletal_meshes_behavior`. That Interchange
   then produces a SkeletalMesh is the inference, and no skinned file has
   ever been handed to it here. RUNTIME-HOLE 4: what Interchange names
   the generated Skeleton asset, and whether it reuses an existing one or
   makes a new one per import, is exactly the kind of thing
   `propImportResolvedVia` was built to find out and has not been asked
   about skeletal assets.

8. **Verify.** `glb_stats` **passes a garment with no skinning left**, and
   the Unreal read-back **fails a garment imported correctly**. **BREAKS
   BOTH WAYS.**

**Count: eight steps. Three break, and one more (step 7) is expected to work
on an inference nobody has tested. One of the three breaks (step 3) is not a
clothing problem. The other two (steps 6 and 8) are one Blender script and
one Python file, both ours, both already written in a style that expects to
be extended.**

---

## 8. WHAT COULD NOT BE ESTABLISHED FROM HERE

Four runtime holes, all of them one Blender session on the PC, plus two
holes of a different kind.

**RUNTIME-HOLE 1: interpenetration through motion.** A shoulder-hung garment
sits correctly at rest by the 2.2% measurement. Whether it stays off the
body through a walk is not a bind-pose question and cannot be answered from
a file. Needs: one Mixamo walk clip, the jacket fitted, and a look.

**RUNTIME-HOLE 2: the `max_distance` / `ray_radius` series.** `data_transfer`
takes both in scene units. No series has been printed. CLAUDE.md rule 2:
ship the printer, read real runs, then set the number.

**RUNTIME-HOLE 3: does Decimate preserve vertex groups usefully.** I cannot
check this from here and will not assert it: `docs.blender.org` answers 000
and I have not run Blender. What the 4.5 stub DOES show is that
`DecimateModifier` is vertex-group-aware on its INPUT side: it carries
`vertex_group`, `vertex_group_factor` and `invert_vertex_group`, which is
how you tell it to decimate the skirt of a coat harder than its shoulders.
That is evidence it reads vertex groups. It is NOT evidence it preserves
them on output, and "preserves them" and "the LOD1 garment still deforms
correctly" are two further claims beyond that. All three need the PC. Note
also that this project has NEVER measured an LOD requirement for a
character, in any engine, so there is no target to decimate toward either.

**RUNTIME-HOLE 4: what Interchange names a generated Skeleton.** And whether
two garments imported separately share one Skeleton asset or get one each.

**HOLE 5, not a runtime question: the licence line for Mixamo BODIES.**
`ledger-v2/research/license-allowlist.md` line 3 reads "Characters:
MetaHuman ... Character Creator 4 exports per Reallusion EULA. **Mixamo
animations.**" It names Mixamo ANIMATIONS. The 18 character BODIES in
`ledger/Assets/Characters/` are Mixamo characters, and
`production/specs/vignette-bill-of-materials.json` row `F1_character_body`
records them as `licence: Mixamo, on Jafar's account`. Those two may well be
consistent in intent and I am not claiming a breach. I am saying the
allowlist, which is LAW, does not say so in words, and this topic's
recommendation (use `Jacket_Geo` or `Ch33_Suit` as the first test garment)
runs straight through that ambiguity. It should be settled by a decision
record before a Mixamo garment mesh goes anywhere near a shipped build. It
does NOT block an afternoon's experiment.

**HOLE 6: the stub is a signature, not a behaviour.** Everything read out of
`fake-bpy-module-4.5` proves the operator and its parameters exist in
Blender 4.5. It does not prove any of them does what its name says on a
Mixamo FBX. That is what the afternoon is for.

---

## 9. THE LINE, DRAWN

```
  WHAT RUNS AUTOMATICALLY               WHAT NEEDS A PERSON
  =======================               ===================

  [1] garment spec .................... a person writes it ONCE,
      JSON, reads atlas-02 research         per garment, then never again
      and Wardrobe.Bands
       |
       v
  [2] reference plate ................. a person LOOKS at it
      imagegen on the PC, 60 to 100s        (the review=pending gate the
      Z-Image-Turbo, Apache-2.0              2D line already has)
       |
       v
  [3] mesh   <== THE LINE STOPS HERE .. a person DECIDES:
      TRELLIS refuses this machine          pay for Meshy or Tripo,
      (4 blockers, each sufficient)         model from flat patterns,
       |                                    or reuse Jacket_Geo / Ch33_Suit
       v
  [4] fit ............................. nobody, for a shoulder-hung coat
      one number: shoulder span             (2.2% vertical variation
      off LeftArm.x / RightArm.x             across 13 realistic bodies)
       |
       v
  [5] skin weights .................... nobody
      data_transfer, BONE_DEFORM            (one skeleton, 65 bones,
      to NAME, ~28 bones for a jacket        shared by all 18 bodies)
       |
       v
  [6] clean + LOD  <== BREAKS SILENT .. nobody, ONCE four lines are fixed
      clean_lod.py:97, 169, 185, 215        (lines named in section 2)
       |
       v
  [7] import .......................... nobody
      AssetImportTask, class-agnostic       (UE 5.8, Interchange present,
      makes SkeletalMesh + Skeleton          ChaosClothAsset present)
       |
       v
  [8] verify  <== WRONG BOTH WAYS ..... nobody, ONCE it can see a skin
      glb_stats reads POSITION only         (passes a broken garment,
      importer asserts isinstance            fails a correct one)
      (o, unreal.StaticMesh)
```

Three stations need a person: the spec (once per garment), the plate review
(the gate that already exists), and the decision at station 3 about where
meshes come from at all. That last one is Jafar's and it is not a clothing
question.

---

## 10. RECOMMENDATION

**Build the verifier first, then spend an afternoon, and do not research
this further.**

The brief asked me to say plainly if the answer is that one route should
simply be tried rather than researched more. **It is.** Every remaining
question is a runtime question, all four fit in one Blender session, and I
have taken the desk work as far as a container can: the operators are
confirmed present in the exact Blender version we run, the skeleton question
is answered with a measurement rather than a guess, and the two broken
scripts are ours with the lines numbered.

**The first thing to build is the skin verifier, not the pipeline**, and the
reason is CLAUDE.md rule 12 and rule 3b together. Today
`mesh_verdict` returns a green string for a garment whose skinning was
destroyed. If the afternoon is spent before that is fixed, the afternoon
produces a GLB, a green verdict, a plausible number, and no way to tell
whether any of it worked. That is the silent-instrument failure this project
has already paid for more than once, and it is 30 lines of stdlib in a file
that already parses GLB JSON:

- extend `glb_stats` to read `skins`, and per primitive the `JOINTS_0` and
  `WEIGHTS_0` accessors;
- emit `skins`, `joints` (distinct joint nodes), `skinnedPrims` beside
  `primitives` as its denominator, and `maxInfluences`;
- print `nothing measured` when there is no skin, never `0`;
- extend `mesh_verdict` with a garment case that FAILS a file expected to be
  skinned and carrying none, and its accepting case is one of the fourteen
  clothed bodies already in the repository, exported to GLB. Rule 5b:
  accepting case first, and the live pool is the fixture.

**And the accepting fixture has to be MADE, which is why step 1 of the
afternoon comes before the verifier is trusted.** Measured: I ran
`meshgen.glb_json` over every GLB in the repository. **39 examined, 0
unreadable, 0 carrying a `skins` array, 39 carrying none.** There is no
skinned GLB here at all, so a verifier written and shipped today would have
run only its rejecting case, which is the exact half rule 5b says goes
unrun. The first thing the afternoon produces is therefore not a garment on
a body: it is the first skinned GLB this project has ever held, and the
verifier's accepting case with it.

**Then the afternoon, in this order**, all on the PC, all headless:

1. Export `The Boss`'s `Jacket_Geo` and `Joe`'s `Ch33_Suit` from Blender to
   GLB with `export_skins=True` and the armature selected. Run the new
   verifier on both. This proves the verifier before it is trusted, against
   a garment known to be correct.
2. Put `Ch33_Suit` on `Leonard` and on `Kate` by the one-number span fit,
   then `data_transfer` the weights from each target body. Verify. Kate is
   the interesting case: span/head 0.2325 against Joe's 0.2614, so about 11%
   narrower for her size.
3. Run the fitted garment through `clean_lod.py` UNCHANGED and confirm the
   four-line diagnosis by watching the verifier fail. Then fix the four
   lines and watch it pass. That is rule 5b on the pipeline itself.
4. Import one GLB into `ue-probe` through the existing `AssetImportTask`
   route with the `isinstance` assertions relaxed, and print what
   Interchange actually made and what it named the Skeleton.

**Time honestly estimated**, with what dominates named as rule 7 requires:
the verifier is an evening's work in a file that already has the GLB reader,
and it is tested here without Blender. The afternoon's four steps are
dominated by the PC round trip rather than by compute, since every Blender
operation above is seconds on 37-prop-sized geometry and the image lane is
not involved at all. What could blow it up is step 4: `ue-probe` has never
held a skeletal asset, and "the first asset of a new class in an engine
project" is the category this project has repeatedly found costs a build
cycle rather than a call. I would not promise step 4 inside the same
session as steps 1 to 3.

**What I would NOT do:** buy a clothing pack on this evidence. Not because
buying is wrong, but because the question the purchase would answer is
station 3, and station 3 is blocked identically for a kerb. A pack of
garments bought today lands in a pipeline whose clean stage destroys their
skinning and whose verifier cannot tell. Fix the two stations we own, prove
them on a garment we already have, and THEN the purchase decision is about
art rather than about plumbing.

---

## APPENDIX: WHERE EVERY NUMBER CAME FROM

All measurements run 2026-09-18 in this container, read-only, scripts kept
in the session scratchpad and not committed.

- **Mesh part counts, skins, clusters, bind poses (section 3).**
  `tools/body-proportions.py`'s `parse_fbx` over
  `ledger/Assets/Characters/*.fbx`. 18 examined, 18 parsed, 0 failures.
  Counts are of `Model` records with class `Mesh`, `Geometry` records,
  `Deformer` records by sub-type, and `Pose` records.
- **Bone sets (section 5).** `Model` records of class `LimbNode`, hashed as
  a sorted set, first raw and then with the `mixamorig*:` namespace
  stripped. The raw run's "0 bones in common" is reported above as the false
  zero it is.
- **Bind-pose positions (section 4).** `BindPose` `PoseNode` `Matrix`
  records, elements 12, 13, 14 of the column-major 4x4, taking the pose with
  the most `PoseNode` entries first and letting the first writer keep each
  bone. This is the same source and the same ordering
  `tools/body-proportions.py:skeleton()` uses, and the reasoning for it is
  quoted in that function.
- **Units.** FBX file units, not metres. Mixamo exports centimetres, so
  1 unit is 1 cm if that holds. Nothing in the files proves it, so every
  absolute figure above is quoted in units and the ratios carry the
  argument.
- **Garment cluster bone lists (section 5).** The FBX `Connections` `OO`
  edges walked from Cluster to Skin to Geometry to Model, and separately
  from Cluster to LimbNode.
- **Blender API (sections 4, 5, 2).** `fake-bpy-module-4.5` version
  20260730, `fake_bpy_module_4_5-20260730-py3-none-any.whl`, 967,552 bytes,
  downloaded from files.pythonhosted.org today. Blender on the PC is 4.5.13
  LTS per `production/mesh-reports/blender-setup.txt` and
  `content/props/manifest.json`. The stub was searched for `def X` first,
  which reported every operator ABSENT; the stub declares operators as
  `class X(...)`, and the corrected search is what section 5 reports.
- **Unreal (section 6).** `production/d1-probe/ue-mesh-import.txt`, one
  `key=value` line per fact, written by the editor on JAFAR-DESKTOP.
- **Image lane (section 1, step 2).**
  `ledger/Assets/StreamingAssets/Decals/generated/PROGRESS.txt` and
  `ATTRIBUTION.json`.
- **Blender install (section 1).** `production/mesh-reports/blender-setup.txt`:
  host JAFAR-DESKTOP, 2026-09-01, portable zip, 398,648,740 bytes,
  sha256 match, extracted to `C:\LedgerTools\blender\4.5.13`.
- **Mesh pipeline run (section 1).** `content/props/manifest.json`: the
  counts line reads `done: 0, skipped: 37, attempted: 0` because it is a
  RESUME, and the evidence that Blender really ran is in the per-item stage
  records (`blender: "4.5.13 LTS"`, real vertex counts, a real LOD ladder),
  not in the counts line. Said out loud because a reader taking the counts
  line alone would conclude nothing ever ran.
- **Egress (first section).** `curl -o /dev/null -w "%{http_code}"` against
  six hosts, today.
