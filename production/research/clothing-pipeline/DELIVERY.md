# Can we make period clothing ourselves, or must we buy it

Research topic 31. Delivered to the studio. Nothing here is an instruction.

**Standing egress note, re-measured today rather than recalled.** One route out
of this container reads a page in full: `curl` to package registries and
`raw.githubusercontent.com`. Measured 2026-09-18 against this topic's own hosts:
`raw.githubusercontent.com` 200, `github.com` 403, and `meshy.ai`, `tripo3d.ai`,
`dev.epicgames.com`, `docs.blender.org`, `fab.com` and `en.wikipedia.org` all
000. So **every vendor page, every Epic document and every marketplace listing in
this delivery is a search engine's summary and not a page I read.** The one
exception is marked: TRELLIS's licence, read in full.

Labels: CITED, DERIVED, ASSUMED, HOLE.

---

## Part 1. The question is already half-answered in our own files, and the earlier answer was wrong

### 1.1 What the bill of materials actually says

CITED, `production/specs/vignette-bill-of-materials.json`, row `F2_period_wardrobe`, in full:

    what:      Clothing that reads as 1988 to 1992 Britain rather than
               contemporary casual
    route:     BLOCKED
    source:    no free re-dress route exists for a Mixamo body. Allowlist
               offers MetaHuman (free under 1M revenue) and Character Creator 4
               exports, each a pipeline rather than an asset
    licence:   allowlisted either way; no purchase involved for MetaHuman
               under the threshold
    note:      BLOCKED means it needs a decision, and the decision is Jafar's
               about where the character pipeline goes, not about money.

DERIVED: the row's `licence` field says **"no purchase involved"** and its note
says the decision is **"not about money"**. `BLOCKED` in this file means "needs a
decision", and the decision it names is a pipeline decision.

### 1.2 What the asset-packs topic did with that

CITED, my own `research/asset-packs` delivery, its route-key table: it glossed
`BLOCKED` as "needs a decision from Jafar (**a purchase**, an account, a hardware
buy)", then quoted the note correctly at line 121, and then listed clothing first
under a section headed "Where buying probably IS worth it".

DERIVED, and I should say it plainly: that delivery quoted the evidence against
its own conclusion and drew the conclusion anyway. The row says no purchase is
involved; the topic named it "the one purchase on its list". The brief for this
topic is right that the conclusion did not weigh the routes we already have, and
the reason it did not is that the route key had already decided what `BLOCKED`
meant before the row was read.

### 1.3 And the pipeline decision it points at is already made

CITED, `D2-faces.md`: "Rig source per D1: **MetaHuman if Unreal** (free under 1M
revenue, usable outside Unreal, never used to train AI models per its addendum),
Character Creator 4 if Unity."

CITED, `D16-engine-unreal.md`, 2026-09-10: "The engine is Unreal."

DERIVED: D2 made the rig source conditional on D1, and D16 resolved D1. **The two
together already select MetaHuman.** F2's "decision about where the character
pipeline goes" was taken eight days before this topic was briefed, and the BOM
row predates it.

---

## Part 2. What we actually have, and what is actually wrong with it

CITED, `vignette-bill-of-materials.md:264`, row F1: "One clothed character body |
18 | **HAVE** | `ledger/Assets/Characters/*.fbx`, Mixamo on Jafar's account".

CITED, the directory: 18 FBX files, being Adam, Big Vegas, David, Elizabeth,
James, Joe, Kate, Leonard, Martha, Michelle, Pete, Remy, Shannon, Sophie, Sporty
Granny, The Boss, X Bot and Y Bot. These are the stock Mixamo character library.

CITED, F1's own note, which is the problem statement in one sentence: "These are
**game-resolution bodies in contemporary casual dress** against a photoreal bar,
and the period is 1988 to 1992."

DERIVED: that is TWO faults, not one, and they are independent.

1. **The clothes are the wrong decade.** A period problem.
2. **The bodies are the wrong fidelity.** A photoreal bar problem, and D8's.

Any route that fixes only the first leaves the second. MetaHuman fixes both,
because it replaces the body as well as what is on it. That is the strongest
argument in this delivery and it is not really a clothing argument.

### 2.1 Why a Mixamo body cannot be re-dressed, stated mechanically

DERIVED, and it is why the BOM says "no free re-dress route exists for a Mixamo
body": a stock Mixamo character is a single skinned mesh in which the clothing IS
the body. There is no nude mesh underneath a separate garment. You cannot remove
the jacket because there is no boundary between the jacket and the man. Replacing
the clothing means replacing the character.

ASSUMED: I have not opened one of the 18 FBX files to confirm the mesh is
single-piece. It is the standard Mixamo export shape and the BOM row asserts the
consequence, but this delivery has not verified it and somebody should before
acting on it.

---

## Part 3. What our own pipeline can and cannot do

CITED, checked 2026-09-18: a grep of `tools/` and `ue-probe/Source/` for
`JOINTS_0`, `WEIGHTS_0`, `"skins"`, `SkeletalMesh`, `skeletal`, `SkinWeight` and
`armature` returns **nothing**.

CITED, `tools/ue/import_prop_meshes.py`: every import path is `StaticMesh`,
`EditorStaticMeshLibrary` and `StaticMeshEditorSubsystem`. Its verdict key is
`propImported`, "assets that loaded back as a **StaticMesh**".

CITED, `tools/meshgen/meshgen.py`'s three stages end in "export GLB", and its GLB
reader parses the JSON chunk for geometry statistics.

DERIVED, and it is the hard technical boundary of this topic: **this project's
asset pipeline has no concept of a skinned mesh.** It makes static props, imports
them as static meshes, and measures them as static meshes. A garment is a skinned
mesh by definition. The pipeline that builds the street cannot carry a coat, and
that is a structural gap rather than a missing feature.

The brief's framing, "it can make a kerb and cannot make a coat", is exactly
right, and the reason is one word: skinning.

---

## Part 4. The four routes

### 4.1 MetaHuman's clothing system

CITED: "MetaHumans from the Creator include **preset, rigged clothing that moves
with the body automatically**", and outfits from the free City Sample Project are
"designed to be compatible with MetaHumans".
[Dressing MetaHumans in UE5](https://yelzkizi.org/clothes-for-metahuman/),
[Epic, MetaHumans on Fab](https://dev.epicgames.com/documentation/en-us/metahuman/metahumans-on-fab)

CITED, the two asset shapes: "The clothing can either be a **parametric outfit
that is able to be resized dynamically with the body, or skeletal with a fixed
size**". Parametric outfits (Chaos Cloth) "use multiple preset sizes and
simulation to automatically fit various body types". An Outfit Asset packages as
a `.MHPKG`.
[Epic forums, New Outfit Asset for metahumans in 5.6](https://forums.unrealengine.com/t/new-outfit-asset-for-metahumans-in-unreal-5-6/2520056),
[MetaHuman clothing and hair from Fab in UE 5.6](https://yelzkizi.org/metahuman-clothing-hair-fab-unreal-engine-5-6/)

CITED, the requirement for custom garments: "import a Skeletal Mesh **weighted to
the MetaHuman's skeleton (`metahuman_base_skel`)**, ensuring it deforms correctly
during animations".
[Custom clothes to characters/MetaHumans in Unreal Engine](https://medium.com/@Unpicked3366/custom-clothes-to-characters-metahumans-in-unreal-engine-a-comprehensive-guide-da6b40986d23)

CITED, the officially blessed authoring route: Epic ran a webinar with CLO and
Marvelous Designer on 2026-04-24 covering "the full workflow, from creating a
MetaHuman, to designing a digital outfit, to bringing it all into Unreal Engine",
with garments exported from CLO as USD.
[Unreal Engine, Tailoring for MetaHumans: CLO and Marvelous Designer](https://www.unrealengine.com/news/tailoring-for-metahumans-clo-and-marvelous-designer-to-unreal-engine-demo)

CITED, a named failure mode from the community, which is worth having in advance:
a forum thread titled "**Clothes Explode After Becoming MetaHuman Wardrobe Item**"
against 5.6.
[Epic forums](https://forums.unrealengine.com/t/clothes-explode-after-becoming-metahuman-wardrobe-item-help-5-6/2610683)

HOLE, and it is the most important one in this delivery: **I could not establish
what the base MetaHuman wardrobe actually contains.** Two searches returned the
hair slots (head hair, eyebrows, eyelashes, moustache, beard, peach fuzz) and the
asset mechanics, and no list of garments. Whether anything in it can pass for
1990 British working dress with a re-texture is the single question this topic
most needed answered and could not be, because `dev.epicgames.com` is blocked.

Licence: free under 1M revenue per D2, already allowlisted, no purchase. The
addendum constraint D2 records, "never used to train AI models", is a real limit
on combining MetaHuman assets with generative tools and I could not read the
addendum to see whether inference counts. HOLE.

### 4.2 Meshy and Tripo, paid tiers

CITED: both offer auto-rigging. Meshy "can auto rig 3D models with a full
skeleton and skin weights in under 30 seconds"; Tripo's UniRig integration
"automates the weight calculation phase ... within 1 to 5 seconds".
[Meshy, AI auto rigging](https://www.meshy.ai/features/ai-auto-rigging),
[Meshy, character auto-rigging workflow](https://www.meshy.ai/tutorials/character-auto-rigging-workflow)

CITED, the physical limitation, stated by the vendor documentation itself:
"clothing deforms with the bones it is bound to, so **fitted clothing animates
well while long flowing garments will stretch unnaturally where legs move**".
[Meshy, as above]

CITED, a garment-specific route exists and is not shipped: Tripo announced a
partnership with MetaTailor "to turn generated clothing meshes into fitted,
rigged wearables for humanoid characters", debuting "in beta during SIGGRAPH",
with "full release coming soon".
[Tripo announcement](https://x.com/tripoai/status/2079473920646996184)

DERIVED, and it is the fault line for this route: **auto-rigging rigs to the
tool's own skeleton, not to `metahuman_base_skel`.** A garment that arrives
rigged arrives rigged to the wrong thing, and re-targeting skin weights from one
skeleton to another is a modelling job, not a setting. The fitted-versus-flowing
limitation is the vendor's own and it lands directly on Part 5.

Licence: both are on our allowlist at PAID TIERS ONLY, and
`tools/meshgen/meshgen.py:161` enforces that mechanically with `BANNED` entries
reading "allowlist SHIP-SAFE 2: Meshy/Tripo paid tiers ONLY, and no purchase is
authorised here - every purchase is Jafar's".

### 4.3 TRELLIS

CITED, read in full from the primary source, which is the one thing in this
delivery I could read properly: `microsoft/TRELLIS` `LICENSE` reads "MIT License
/ Copyright (c) Microsoft Corporation."

HOLE: the allowlist names "TRELLIS/TRELLIS 2 (MIT)". I probed
`microsoft/TRELLIS2`, `microsoft/TRELLIS-2` and `microsoft/Trellis2` and all three
returned 404, so **TRELLIS 2's repository was not located** and its licence was
not verified. TRELLIS itself is confirmed MIT.

DERIVED: TRELLIS is image-to-3D and produces a static mesh. It has the same
skinning gap as our own pipeline, without the auto-rigging that Meshy and Tripo
at least offer. Fed by plates from our image lane it would produce a garment-
shaped object that nothing can put on a person. It is the wrong tool for this
specific job, and that is not a criticism of it.

### 4.4 Blender cloth simulation from flat patterns

CITED: Marvelous Designer courses run "13+ hours ... from absolute beginner to
advanced", with introductory tutorials "over 3 hours". Blender's own cloth
simulation "works beautifully" but is "not as straightforward as Marvelous
Designer". Getting a simulated garment into a game needs retopology, "important
in optimizing garments for game and animation workflows".
[Udemy, Marvelous Designer Mastery](https://www.udemy.com/course/marvelous-designer-mastery-beginner-to-advanced/),
[Class Central, Marvelous Designer to Blender 4.2](https://www.classcentral.com/course/youtube-marvelous-designer-to-blender-4-2-tutorial-2024-marvelousdesigner-blender-cloth-310638),
[CG Boost community](https://community.cgboost.com/c/share-and-learn/marvelous-designer-cloth-simulation-in-blender)

DERIVED, answering the brief's question directly: this is how garments are
genuinely made, it is the route Epic officially blessed in April, and it is a
craft discipline measured in days of training plus a retopology step plus
skinning. **For someone directing rather than modelling it is not a realistic
route**, and the honest version of that sentence is that it is not realistic for
Jafar rather than that it is impossible for the studio.

---

## Part 5. The practical question: three garments onto a character in Unreal

The brief names a donkey jacket, work trousers and an anorak. Those three split
into two easy cases and one hard one, and the hard one is the one that carries
the period.

### 5.1 What a donkey jacket actually is

CITED: "a medium-length workwear jacket, typically made of unlined black or dark
blue thick Melton woollen fabric, with the shoulders back and front reinforced
and protected from rain with leather or PVC panels". Critically for this topic:
"The garment is **untailored at the waist, so that it hangs down straight from
the shoulders**. The front vertical edges fall straight and are squared-off at
the bottom edge ... **It reaches 3 to 4 inches (8 to 10 cm) below the crotch
area.** It has no lapels ... with a broad and stiff turn-up collar."

Origin and wearer, both period-correct: designed in 1888 by George Key for
navvies on the Manchester Ship Canal, and "in its heyday, the donkey jacket was
the badge of the working man, seen on everyone from coal miners to binmen". By
the 1980s it had become a subculture marker as well.
[Wikipedia, Donkey jacket](https://en.wikipedia.org/wiki/Donkey_jacket),
[HowSafe, Remembering the donkey jacket: a workwear icon](https://www.howsafe.co.uk/blog/post/remembering-the-donkey-jacket-a-workwear-icon)

DERIVED, and this is the engineering point: **a donkey jacket's defining property
is that it does not follow the body.** It hangs straight from the shoulders,
untailored, past the hip and over the upper thigh. That is precisely the case
4.2's own vendor documentation says breaks: "long flowing garments will stretch
unnaturally where legs move".

The three garments, ranked by difficulty:

| garment | why | skinning |
|---|---|---|
| **work trousers** | fitted, follows the legs exactly | trivial |
| **anorak** | fitted at the torso, hem near the waist | easy |
| **donkey jacket** | hangs free below the crotch, untailored | **the hard case** |

The PVC shoulder panel, which reads as the jacket's signature, is the EASY half:
it is a material boundary on one mesh, not geometry.

### 5.2 Where the route breaks, named specifically as the brief asked

1. **Fitting to the wrong skeleton.** Generated garments arrive rigged to the
   generator's skeleton. MetaHuman requires `metahuman_base_skel`. Re-targeting
   skin weights between skeletons is a modelling job.
2. **Weighting so the cloth deforms with the body.** Solved by construction for
   trousers and an anorak, unsolved for the donkey jacket's skirt, which must
   either be cloth-simulated (Chaos Cloth, which is what the parametric Outfit
   Asset does) or bound to a bone chain that does not exist on a standard
   skeleton. Bind it to the thighs and it moves like trousers; bind it to the
   pelvis and it passes through the legs when he walks.
3. **Separate mesh or fused to the body.** Our 18 Mixamo bodies are fused, which
   is why they cannot be re-dressed. Generative tools generate clothed
   CHARACTERS by default and need explicit prompt work to keep parts separate;
   the vendor advice is that "props should be generated separately, then attached
   to a bone after rigging". MetaHuman's wardrobe is separate by construction,
   which is the whole point of a wardrobe slot.
4. **LODs.** Not addressed by any route in this delivery, and not measured
   anywhere in this project. HOLE.
5. **Cloth that explodes**, which is a real reported 5.6 failure when a garment
   becomes a wardrobe item.

---

## Part 6. Buying, compared honestly

CITED: Fab carries MetaHuman-compatible clothing packs "designed for MetaHuman
skeletons and set up for Chaos Cloth simulation". The listings found were a
Women's Outfit Pack, a Streetwear Clothing Pack, a Basic Clothing Pack, a Male
Dresswear Pack, a Clothing Basics Pack and a Medieval Clothes pack.
[Fab, MetaHuman channel](https://www.fab.com/channels/metahuman)

CITED, the negative result, from three differently-worded searches: **no
period-appropriate 1980s or 1990s British working-wardrobe pack was found.** The
searches returned contemporary streetwear, basics, dresswear and medieval, plus
actual vintage donkey jackets for sale on eBay and Etsy, which are garments
rather than assets.

DERIVED, and it inverts the earlier conclusion: **the one thing the asset-packs
topic said to buy appears not to be for sale.** What is for sale is a hoodie.
Buying a contemporary pack would leave the period problem exactly where it is,
and would leave the fidelity problem too if the pack is not MetaHuman-grade.

HOLE: `fab.com` is blocked, so this is an absence in search results and not an
absence from the marketplace. A direct browse of Fab's MetaHuman channel would
settle it in minutes on a machine with egress, and would cost nothing.

What a pack would still need doing to it, whatever it contained: re-texturing to
period materials (Melton wool, PVC), fitting if it is skeletal rather than
parametric, and a check that its licence permits shipping, which the allowlist
requires as a decision record naming the weights or asset licence.

---

## Part 7. What could not be established

1. **The contents of the MetaHuman base wardrobe.** The most important hole here.
   `dev.epicgames.com` is blocked.
2. **Whether TRELLIS 2 exists at a locatable repository**, and therefore whether
   its MIT licence is verified. TRELLIS itself is confirmed MIT by primary read.
3. **What the MetaHuman addendum means by "never used to train AI models"**,
   specifically whether feeding a MetaHuman render to an image-to-3D tool counts.
4. **Whether a period pack exists on Fab.** An absence in search, not a browse.
5. **Whether the 18 Mixamo FBXs are single-mesh**, asserted by the BOM and not
   opened here.
6. **Any price.** No vendor page was reachable, so this delivery contains no
   cost figure for any paid tier or any pack, which is a real gap in a
   buy-versus-build comparison and I will not invent one.
7. **LOD requirements for a garment in this project.** Never measured.

---

## Part 8. Findings and interpretation

### Findings

F1. The BOM row `F2_period_wardrobe` says "no purchase involved for MetaHuman
under the threshold" and that the decision is "not about money".

F2. The asset-packs delivery quoted that note and listed clothing first under
"Where buying probably IS worth it". Its route key glossed `BLOCKED` as "a
purchase" before the row was read.

F3. D2 makes the rig source MetaHuman if the engine is Unreal; D16 made the
engine Unreal on 2026-09-10. The pipeline decision F2 asks for is already made.

F4. F1 is `HAVE`: 18 Mixamo bodies. Its note records two faults, contemporary
dress AND game-resolution bodies against a photoreal bar.

F5. Nothing in `tools/` or `ue-probe/Source/` handles a skinned mesh. The Unreal
importer is `StaticMesh` only.

F6. MetaHuman ships preset rigged clothing; City Sample outfits are compatible
and free; custom garments must be weighted to `metahuman_base_skel`; Chaos Outfit
Assets are parametric and resize with the body.

F7. Meshy and Tripo auto-rig in seconds, to their own skeletons. Tripo's
garment-fitting partnership with MetaTailor is in beta.

F8. Vendor documentation states fitted clothing animates well and long flowing
garments stretch unnaturally where legs move.

F9. A donkey jacket is untailored at the waist, hangs straight from the
shoulders and falls 8 to 10 cm below the crotch.

F10. TRELLIS is MIT (primary read). TRELLIS 2's repository was not found.

F11. Marvelous Designer is a multi-day craft discipline plus retopology.

F12. No 1980s or 1990s British working-wardrobe pack was found in three
searches. Fab's MetaHuman clothing is contemporary or medieval.

### Interpretation

I1. The question "make or buy" has a false premise, and the premise came from my
own earlier delivery. We neither have to buy it nor make it from scratch: the
route the project already committed to ships garments that arrive dressed,
fitted and rigged, and its licence line already says no purchase is involved.

I2. The strongest argument for MetaHuman here is not about clothing at all. F1
records two faults and MetaHuman is the only route that fixes both, because it
replaces the body as well as what is on it.

I3. The generative tools are the wrong SHAPE for this job rather than too weak
for it. They rig to their own skeleton, our pipeline has no skinning at all, and
the one garment that defines the period is the one their own documentation says
deforms badly.

I4. Of the three garments, two are easy and the third is the period. Any test of
any route should use the donkey jacket, because trousers and an anorak will
succeed on every route and prove nothing.

I5. The honest state of this topic is that its central question, whether
MetaHuman's wardrobe can reach 1990 Britain with a re-texture, is unanswerable
from here and answerable in an afternoon on a machine with a browser. That is the
recommendation and it is in the summary.
