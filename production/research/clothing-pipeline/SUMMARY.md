> **PARTLY OVERTURNED, 2026-09-19.** Three findings are refuted. That Mixamo
> bodies are fused and cannot be re-dressed: see
> `production/research/clothing-assembly-line/SUMMARY.md`, where 14 of the 18
> carry separate garment items and all share one skeleton. That custom garments
> must be weighted to `metahuman_base_skel`, and that Jafar should open
> MetaHuman Creator to inspect the wardrobe: see `RECHECK.md` beside this file,
> where Epic's own documentation says clothing does not have to be skinned and
> one unnamed outfit ships rather than a wardrobe. Everything else here stands.

# We do not have to buy clothes, and my earlier answer was wrong

Research topic 31. You asked whether we can make period clothing ourselves or
must buy it. The short answer is neither, and the reason is sitting in our own
files.

## What I got wrong last time

The asset-packs research called period clothing "the one purchase on the list".

Our own bill of materials, on that exact row, says:

> **licence:** allowlisted either way; **no purchase involved** for MetaHuman
> under the threshold
>
> **note:** BLOCKED means it needs a decision, and the decision is Jafar's about
> where the character pipeline goes, **not about money**.

That earlier delivery quoted that note and then listed clothing first under
"where buying probably is worth it". It had already decided that BLOCKED meant
"buy something" before it read the row. That is my error and this topic exists
because you spotted it.

## And the decision that row is waiting for is already made

D2 says the rig source is **MetaHuman if the engine is Unreal**, Character
Creator 4 if Unity. D16 made the engine Unreal on 10 September.

So the "decision about where the character pipeline goes" was taken eight days
before you briefed this. MetaHuman is free under a million in revenue, it is
already on the allowlist, and **its clothing arrives already fitted and rigged to
the body.**

## The real problem is two problems

Our bill of materials describes the 18 Mixamo bodies we have in one sentence:

> game-resolution bodies in **contemporary casual dress** against a photoreal
> bar, and the period is 1988 to 1992.

That is a period problem **and** a fidelity problem, and they are separate. Any
route that only changes the clothes leaves the bodies looking like a 2015 asset
store next to your photoreal street.

MetaHuman is the only route that fixes both, because it replaces the body too.
That is the strongest argument here and it is not really an argument about
clothing.

## Why we cannot just make a coat ourselves

Our scene generator builds static objects. A garment is not a static object: it
has to bend when the man bends, which means it must be bound to a skeleton.

I grepped the whole toolchain for anything that touches a skinned mesh. **There
is nothing.** Our Unreal importer imports static meshes only. The pipeline that
builds the street genuinely cannot carry a coat, and it is one word that stops
it: skinning.

## The three garments split two-and-one

**Work trousers and an anorak are easy.** They are fitted. They follow the legs
and the torso, which is exactly what skinning does well.

**The donkey jacket is the hard one**, and it is the one that carries the period.
Here is why, from its actual description:

> untailored at the waist, so that it **hangs down straight from the shoulders**
> ... reaches 3 to 4 inches below the crotch

Its whole character is that it **does not follow the body**. It hangs past the
hip and over the thigh. Bind it to the legs and it stretches like trousers when
he walks; bind it to the hips and it passes straight through his legs.

The AI tools' own documentation says this in as many words: fitted clothing
animates well, and long flowing garments stretch unnaturally where legs move.

The PVC shoulder panel, which is the jacket's signature, is the easy half. That
is just a different material on the same piece of cloth.

**So if anyone ever tests a route, test it with the donkey jacket.** Trousers and
an anorak will succeed on every route and prove nothing.

## The AI generators are the wrong shape, not too weak

Meshy and Tripo will auto-rig a model in under thirty seconds. But they rig it to
**their own skeleton**, and MetaHuman needs a garment weighted to its skeleton
specifically. Moving skin weights from one skeleton to another is modelling work,
not a setting.

Tripo has announced a partnership specifically to turn generated clothes into
fitted wearables. It is in beta.

TRELLIS produces static meshes, so it has the same gap our own pipeline has.
(I did confirm its licence properly, MIT, by reading the actual file.)

And making garments the real way, flat patterns in Marvelous Designer, is what
Epic themselves recommend. It is also a multi-day craft plus a retopology step.
That is a route for a modeller, and you are directing.

## What buying would actually get you

I searched three ways for a 1980s or 1990s British working-wardrobe pack.

**I could not find one.** What Fab sells for MetaHuman is streetwear, basics,
dresswear and medieval. The only donkey jackets I found for sale were real ones,
on eBay.

So the one thing my earlier research told you to buy appears not to be for sale.
A contemporary pack would leave the period problem exactly where it is.

I should be careful here: Fab is blocked from where I work, so this is an absence
in search results, not a browse of the shop. Five minutes on your machine would
settle it properly.

## My recommendation

**Stop researching this and spend an afternoon on it.**

Specifically: open MetaHuman Creator, look at what clothing it actually ships,
and see how close a dark re-texture of a plain work jacket gets to a donkey
jacket.

I could not answer that question, and it is the question the whole topic turns
on. Epic's documentation site is blocked from my container, so I could find out
how the clothing system works in detail and not what is actually in the wardrobe.

If the wardrobe has a plain straight jacket in it, the period is a texture job
and this is nearly solved. If it does not, then we know what to commission, and
we will know it from looking rather than from me guessing.

That is an hour of your time and it replaces everything else on this page.

---

**On sources.** Every research host is still blocked, exactly as on the previous
thirty-six topics. I re-measured today: Epic's documentation, Meshy, Tripo,
Blender's manual, Fab and Wikipedia all refuse the connection outright. The only
thing I could read in full is code repositories, which is how TRELLIS's licence
above is a real reading rather than a summary. **Everything else in this topic is
a search engine's summary of a page I could not open**, and the delivery marks
each one.
