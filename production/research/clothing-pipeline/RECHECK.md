# RECHECK: what MetaHuman actually ships, and what fitting a garment involves

STATUS: SPEC (research recheck). Branch `research/clothing-pipeline`, added on
top of `c7765b2`. Written 2026-09-19 by the research lane.

NOTHING IN THIS FILE IS AN INSTRUCTION. No queue item, no decision record, no
purchase proposed.

## 0. What opened

`dev.epicgames.com` returned 200 this session, for the first time in this
lane's history. Topic 31's standing egress note recorded it at 000 on
2026-09-18, one day ago.

Epic's documentation is an Angular application: the page body is not in the
HTML, it is in an embedded `serverApp-state` JSON blob, which is why a naive
fetch of a content page returns a hundred characters of chrome. It was
extracted properly. THE DENOMINATOR, because a negative result needs one: **60
pages of the MetaHuman documentation tree were crawled by title and
description, and 14 were read in full body text.** Of those 60, exactly ONE
page's title or description mentions clothing in any form.

Still refused: `fab.com`, `www.unrealengine.com`, `mixamo.com`. So topic 31's
part 6 negative result about the marketplace is NOT upgraded here and remains
an absence in search results rather than a browse.

## 1. Question one: what garments ship with MetaHuman? One outfit.

From "Hair and Clothing Tools", updated 2026-09-02, quoted exactly:

> The wardrobe is initially populated with grooms and **an outfit** shipped with
> MetaHuman Creator as part of the additional content enabled during
> installation. You can add your own MetaHuman-compatible groom and outfit
> assets to curate your own wardrobe.

Singular. And the page that describes that additional content, "Getting Started
in MetaHuman Creator", lists it without clothing at all:

> This content includes presets, grooms, texture models, and the non-Unreal
> Engine files needed to export MetaHumans to other applications (such as Maya).

Two Epic pages, two slightly different lists, neither naming the outfit. I
record the disagreement rather than reconciling it.

What the wardrobe IS, from the same page: a set of pre-defined slots that you
populate. Hair slots for head hair, eyebrows, eyelashes, mustache, beard and
peach fuzz. Clothing slots split by how the garment was built: **Outfit
Clothing** (a Chaos Outfit Asset, resizable across body shapes) and **Skeletal
Clothing** (a SkeletalMesh, fixed size). A character wears one item per slot at
a time, and an item must be "prepared" before first use, which caches computed
data onto the character asset and "can cause it to become quite large".

The only garment Epic names anywhere in the clothing documentation read here is
the **MetaHuman Techwear Outfit on Fab**, used as the worked example in its own
authoring tutorial.

## 2. Question two: is a plain straight work jacket among them? No.

Not because the shipped outfit is the wrong garment, but because the premise is
wrong. **There is no MetaHuman garment catalogue.** One outfit ships, Epic's
documentation does not name it, and the wardrobe is a container rather than a
collection.

So topic 31's own words, "I could not establish what the base MetaHuman
wardrobe actually contains ... whether anything in it can pass for 1990 British
working dress with a re-texture is the single question this topic most needed
answered", resolve by dissolving. There is nothing to re-texture toward 1990. A
donkey jacket, work trousers and an anorak have to come from somewhere else
whatever else is decided, and MetaHuman's contribution is the body, the slots
and the fitting system, not the clothes.

## 3. Question three: what fitting a garment actually involves

Read from Epic's six-page parametric clothing workflow. The short form:

1. **Enable two plugins**: MetaHuman Creator and Chaos Cloth.
2. **Bring a model**, as one of three documented paths, and the path decides the
   work: **FBX** from Maya, render mesh only, which is also the path for
   converting existing MetaHuman clothing; **USD** from CLO or Marvelous
   Designer, which carries a sim mesh and a render mesh; or a **render mesh**
   with a sim mesh you built by hand. Epic's words: "Unless you have created
   one, or if you've done a USD export from Clo or Marvelous Designer, you will
   be working with a render mesh only."
3. **Build the Outfit Asset.** What it does, quoted: "The outfit asset
   associates your clothing with the body it was made for (source body). It then
   warps the clothing based on the difference between the source body and a new
   body with different measurements (target body)."
4. **Choose a LOD workflow path**, then test and configure the outfit.
5. **Package with MetaHuman Manager** into `.mhpkg`, which is only needed for
   publishing to Fab.

### 3.1 The correction that matters most

Topic 31 finding F6 and its section 5.2 named the first break in the route:
custom garments "must be weighted to the MetaHuman's skeleton
(`metahuman_base_skel`)", and re-targeting skin weights between skeletons "is a
modelling job, not a setting".

Epic's own page says otherwise for fixed-size clothing under the 5.6 parametric
body system, quoted exactly:

> Skeletal mesh clothing does not resize, but one important distinction from the
> previous version of MetaHuman is that now, because of parametric bodies, you
> can create that clothing for any body shape you want, as opposed to the base
> 18 archetypes. You can now distribute that body shape via preset, even as a
> part of the package you sell. **This also means that you do not have to skin
> your clothing. All you need is the model, and it will function exactly the
> same.**

That is the single largest correction in this file. The step topic 31 called the
hard break is documented as not required.

### 3.2 And the failure mode Epic warns about is the donkey jacket

Quoted from the same page:

> In some cases, the source body and target body are too different, which can
> cause warping. This is especially the case with more realistic and detailed
> (not stylized or simplified) clothing. Due to this, we encourage you to create
> multiple outfits for multiple source bodies, with the idea that the closer to
> an original source body a target body is, the less warping artifacts a user
> will get.

Topic 31's I4 said any test of any route should use the donkey jacket, because
trousers and an anorak succeed everywhere and prove nothing. Epic's own caution
names the donkey jacket's category: realistic, detailed, and fitted to a body it
was not authored for. I4 is strengthened rather than changed, and the remedy is
now named too: author more than one source body.

## 4. What changes

1. **Topic 31's recommendation does not survive in its stated form.** It asked
   Jafar to open MetaHuman Creator himself to inspect the wardrobe. There is no
   wardrobe to inspect, and the question that hour was meant to answer is
   answered above from Epic's own documentation.
2. **What is worth the equivalent hour is a studio job, not his.** Take any
   garment model through the three-path workflow to an Outfit Asset on a body,
   because the step topic 31 called the break is documented as unnecessary and
   the step Epic warns about is the one the period depends on. Epic supplies a
   free practice asset for exactly this, the Techwear Outfit, and says to use
   the render-mesh path with it.
3. **Topic 31's part 3 is untouched and still decides the shape of the work.**
   Nothing in `tools/` or `ue-probe/Source/` handles a skinned mesh. Epic's
   workflow lives entirely inside the Unreal Editor and does not go through this
   project's importer, so it is a new pipeline rather than an extension of one.
4. **I1 and I2 stand.** The route was already chosen by D2 plus D16, the licence
   line already says no purchase, and MetaHuman is still the only route that
   replaces the body as well as the clothes.
5. **Nothing here says where a 1990 donkey jacket MODEL comes from.** That is
   now the open question in this topic, and it is a smaller and better-posed one
   than the question topic 31 ended on.

## 5. What could not be established

1. **What the one shipped outfit is.** Epic does not name it on any of the 14
   pages read.
2. **Whether a period pack exists on Fab.** `fab.com` refused again, so topic
   31's part 6 is unchanged: an absence in search results, not a browse.
3. **Any price**, for the same reason.
4. **What the MetaHuman addendum means by "never used to train AI models".** The
   data-use page exists at `/documentation/metahuman/metahuman-data-use` and was
   not read: it is outside the three questions this recheck was sent to answer,
   and it is one fetch away for whoever wants it.
5. **Whether the 18 Mixamo FBXs are single-mesh.** Unopened here too, as in
   topic 31.
6. **Anything about how it actually looks or behaves.** This file read
   documentation. No garment was imported, no Outfit Asset built, no frame
   rendered. Rule 4 applies: none of this is an artifact opened.

## 6. Sources

Primary, read 2026-09-19 from `dev.epicgames.com`. Crawled by title and
description: 60 pages of the MetaHuman documentation tree. Read in full body
text, the ones this file rests on:

- `metahuman/hair-and-clothing-controls` ("Hair and Clothing Tools", updated 2026-09-02)
- `metahuman/getting-started-with-metahuman-creator-in-unreal-engine`
- `metahuman/metahumans-on-fab`
- `metahuman/presets`
- `metahuman/metahuman-creator-in-unreal-engine`
- `unreal-engine/creating-parametric-clothing-for-fab`
- `metahuman/creating-parametric-clothing-for-metahuman`
- `metahuman/getting-started-for-creating-parametric-clothing-in-metahuman`
- `metahuman/parametric-asset-setup-for-metahuman`
- `metahuman/building-an-outfit-asset-in-unreal-engine`
- `metahuman/metahuman-devkit-in-unreal-engine`
- `metahuman/metahuman-fashion-starter-kit`
- `metahuman/metahuman-creator-overview`
- `metahuman/metahuman-documentation`

Refused this session: `fab.com`, `www.unrealengine.com`, `mixamo.com`,
`huggingface.co`, `arxiv.org`, `github.com`.

Repository sources are quoted from topic 31 at its own commit and were not
re-read here.
