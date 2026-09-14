# What 1990 looked like on film stock

Research topic 23. Delivered to the studio. Nothing here is an instruction.

The brief's question read literally: not "what did 1990 look like", which is a
content question the atlas research is already answering, but what the
PHOTOGRAPHIC PROCESS of 1990 did to everything it recorded. That matters for
two separate reasons, and the second one turned out to be the bigger finding:
it is what a period grade would have to reproduce, and it is what our reference
material has already done to the evidence.

Labels follow `production/art/atlas-02/research/`: CITED, DERIVED, ASSUMED,
HOLE.

---

## Part 1. The film of 1990, named

### 1.1 The motion picture stocks are datable to thirteen months before our window

CITED: the Eastman EXR family was introduced on 17 January 1989, using tabular
grain emulsion technology. The family in use through our window:

- **5245, EXR 50D**: low speed, daylight balanced, very fine grain
- **5248, EXR 100T**: medium speed, tungsten balanced, very fine grain
- **5296, EXR 500T**: 500 speed, balanced for 3200K tungsten

The 5296 was noted for reproducing "absolute black without compromising
highlights and midtones", and high contrast "without bleed-through or
wrap-around from light to dark areas".
[Kodak, History of Film chronology](https://www.kodak.com/en/motion/page/chronology-of-film/),
[Kodak, EASTMAN EXR 50D Color Negative Film 5245 datasheet](https://125px.com/docs/motionpicture/kodak/5245-1999.pdf),
[Filmmakers Academy, The Hollywood history of iconic Kodak film stocks](https://www.filmmakersacademy.com/blog-hollywood-kodak-film-stocks/)

DERIVED: "the look of 1990 on film" is not a vague nostalgia. It is a named
family of three stocks introduced a year before our window opens, and the
choice between them was the choice between grain and light. A wet overcast
British exterior at the D8 visual target is a LOW-LIGHT scene, which in 1990
means the 500T, which means the grainiest of the three.

That is worth saying because it inverts a natural instinct. Our scene is the
one where period film looked WORST, not best. Grain is not a decorative layer
to be dialled in tastefully; on the kind of day this game is set in, it was the
dominant texture.

### 1.2 The four pillars, and we have one of them

CITED, and this is the most useful single sentence found: "The four fundamental
pillars of film emulation are color response, grain, halation, and gate weave."
[Digital Production, Halation and diffusion: on the hunt for the ultimate film look](https://digitalproduction.com/2024/01/30/halation-and-diffusion-on-the-hunt-for-the-ultimate-film-look/),
[No Film School, The 4 elements that can make digital footage look like the 1970s](https://nofilmschool.com/four-elements-film-emulation)

CITED, what halation actually is, because it is routinely confused with bloom:
colour film has three colour-sensitive emulsion layers plus an anti-halation
backing. Light penetrates the layers, is only partially absorbed by the
backing, and the strongest rays bounce back into the RED layer. The reflected
light is filtered of its blue and green components, so it backlights the red
emulsion and produces "reddish-orange halos" around strong highlights.
[Prodigium Pictures, Halation on film and digitally imitating it](https://www.prodigium-pictures.com/blog/insight09-halation-on-film-digitally-imitating-it),
[Dehancer blog, Halation and its simulation](https://blog.dehancer.com/articles/halation/),
[CineD, Chasing the glow: understanding halation](https://www.cined.com/chasing-the-glow-understanding-halation-and-why-filmmakers-keep-coming-back-to-it/)

CITED, on grain being more than speckle: "Film grain isn't just monochrome
speckles. Each grain interacts with color dyes, subtly shifting hues and
saturation."
[HolyGrain, How 35mm film grain shapes the cinematic look](https://www.holygrain.com/blog/35mm-film-grain-vs-digital-cinematic-comparison/)

DERIVED: bloom and halation are different effects. Bloom is white or
scene-coloured and symmetrical; halation is REDDISH-ORANGE and is a property of
the red layer specifically. A stack that uses bloom where halation belongs
produces a glow of the wrong colour, which reads as "modern game with the glow
turned up" rather than as film.

### 1.3 The stills, which is where most of our reference comes from

CITED: Kodak Gold 200 "was the most popular choice amongst holidaymakers in the
1980s and 1990s". It produces "strong color casts, particularly heavy yellow
and magenta tones", "leans more on the yellows and blues to create that warm
feel", is "a little more muted and warmer in its tones compared to ... Fujicolor
200", and its grain is "noticeable, but not distracting ... fine, smooth, and
subtle".
[The Darkroom, Kodak Gold 200 film review](https://thedarkroom.com/film/gold-200/),
[My Favourite Lens, Kodak Gold 200 35mm film review](https://www.myfavouritelens.com/kodak-gold-200-35mm-film-review/),
[Analogue Wonderland, Kodak Gold 200 35mm](https://analoguewonderland.co.uk/products/kodak-gold-35mm-film)

DERIVED: the amateur photographs that survive of an ordinary British street in
1990 were mostly taken on a warm, yellow-and-magenta-leaning consumer film,
printed by an automated minilab, and are today seen after a scan and usually an
upload. Part 3 is what follows from that.

---

## Part 2. What this project has, and where it lives

### 2.1 The grade exists and is in the archived engine

CITED, `ledger/Assets/Resources/LedgerFilmGrade.shader`, its own header: "Grain,
vignette and bloom in one shader (art direction §4, 'Post: film grain, vignette,
slight bloom on light sources')." Three passes: composite, bright-pixel extract,
blur. Parameters `_Threshold, _Bloom, _Grain, _Vignette, _Seed, _Exposure`.
Ambient occlusion deliberately lives in a separate shader so a compile failure
there cannot take the grade down.

CITED, the grain line at :190: `col.rgb += g * _Grain * (1.0 - lum * 0.7)`,
with a comment at :182 saying it "hides banding" and at :187 that it puts grain
"where film grain actually lives instead of speckling the lamps".

DERIVED, and it is a point in the shader's favour: scaling grain inversely with
luminance is the right instinct. Grain in a film image is least visible in the
brightest areas, and a uniform digital noise over a whole frame is one of the
two commonest tells of a fake film look.

CITED, checked today: `ue-probe/Source/` contains no grain, halation, film
grade, LUT or colour grade. Grepping for those terms returns only tonemap
commentary in `VignetteSpec.h` about what `shotMeanLuma` is a statistic of.

DERIVED: this is the same pattern topic 17 found with `Core/FrameRate.cs` and
`Core/Detail.CostIndex`. The look was built, argued and tuned in the engine D16
archived on 2026-09-10, and the engine that will ship has none of it. Three
separate systems now: the frame-time instrument, the graphics preset cost
model, and the film grade.

### 2.2 Scored against the four pillars

| pillar | this project |
|---|---|
| grain | HAVE, in Unity, with a good luminance curve |
| halation | NO. Bloom stands where halation belongs, and bloom is the wrong colour |
| colour response | NO. There is a tonemap and an exposure, which is not the same thing |
| gate weave | NO, and see below |

On gate weave, stated as an open question rather than a recommendation: it is
the small frame-to-frame instability of film moving through a camera gate. In a
film it is invisible until pointed out. In a real-time render at a player's
chosen frame rate it would be a whole-frame sub-pixel jitter, permanently, on
every frame they ever play. I could find nothing about anyone shipping it in a
game and I would not assume it transfers. It is the one of the four pillars
whose medium does not obviously carry over.

---

## Part 3. The finding that matters most: our reference material is not evidence of colour

### 3.1 Three layers of process between us and the street

A photograph of a British street in 1990, as we can see it today, has been
through at least three transformations before it reaches an artist's eye:

1. **The film**, which had a colour response of its own. Kodak Gold's warm
   yellow-magenta lean is a property of the emulsion, not of the day.
2. **The print**, made by an automated minilab that applied its own colour
   correction to every frame, aiming at a pleasing average rather than at
   accuracy.
3. **The scan**, made years or decades later by somebody with their own
   settings, and frequently adjusted again before upload.

HOLE, and it is a real one: I could not establish, from the sources available
here, how much of the characteristic 1990 warmth is emulsion and how much is
minilab printing. The reviews cited above describe scanned negatives today,
which is a fourth process again. What is well supported is that the warmth is
PROCESS, not weather. What is not established is which part of the process.

### 3.2 Why this collides with the visual bar specifically

`canon.md` states the visual target as "photoreal, wet, overcast, grimy
Britain. Weather and grime are the strategy, not stylization."

A wet overcast British street is, in physical terms, lit by a high colour
temperature diffuse source. It is COOL and grey and low in contrast. The
photographs of such a street that survive from 1990 are warm and yellow,
because of section 3.1.

DERIVED: an art process that reads colour off period photographs will pull the
game warm, and will pull it warm in exactly the scene canon says is the whole
strategy. The reference lies about the one variable the visual bar cares about
most, and it lies consistently rather than randomly, which is the kind of error
that survives review because every reference agrees with every other one.

This is CLAUDE.md rule 3 applied to visual reference: suspect the instrument
first, and a photograph is an instrument.

### 3.3 The remedy already exists in-house, which is why this is a cheap finding

`production/specs/vignette-scene.json:266` derives the colour of a low pressure
sodium lamp from physics rather than from a picture: 589 nm monochromatic,
interpolated through the CIE 1931 two-degree colour matching functions,
transformed by the sRGB D65 matrix, clipped and normalised, with the note that
"the derivation was run rather than recalled" and that the range and intensity
are explicitly NOT derived and are the first values of an unprinted series.

That is exactly the right method and it is already this project's own. The
generalisation is one sentence: **derive COLOUR from the physics of the light,
and take from photographs only what a photograph is reliable evidence of.**

What a period photograph IS good evidence of: composition, geometry,
proportion, material, wear, what objects were present, how people stood and
dressed, how dirty things were, what a shopfront's layout was. The atlas
research already uses photographs for exactly those things, and measures rather
than eyeballs them.

What it is NOT good evidence of: colour, colour temperature, contrast ratio,
highlight behaviour, or how dark the shadows were.

### 3.4 And the separate question of whether we WANT the film look at all

Worth separating cleanly, because the two get conflated.

- Making the WORLD look like 1990 is a content and physics question: what was
  there, what it was made of, what the light did.
- Making the IMAGE look like 1990 is a grade: grain, halation, colour response.

They are independent. A game can be scrupulously period and render clean, or be
anachronistic and render through a heavy film emulation. `canon.md` says
"weather and grime are the strategy, not stylization", which reads as a
preference for the first, and the existing shader header quotes an art
direction line asking for "film grain, vignette, slight bloom", which is a
modest amount of the second.

ASSUMED, and flagged as mine rather than as a finding: a heavy film emulation
would fight the Meridian Test's first condition, which is that somebody who
loves GTA or KCD2 does not bounce off the visuals in thirty minutes. Neither
comparator ships a strong period grade. A restrained grade that a player stops
noticing after a minute is a different proposition from a look that announces
itself.

---

## Part 4. What could not be established

1. **How much of the 1990 warmth is emulsion versus minilab printing.** The
   single most useful thing to know here and not settled by any source found.
2. **What Prime Suspect and the other 1991 British dramas were actually shot
   on**, film or video, and at what stock. Topic 22 established their register;
   this topic did not establish their look.
3. **Whether anybody has shipped gate weave in a real-time game.** Nothing
   found either way.
4. **Any datasheet numbers**: the EXR stocks' actual characteristic curves,
   grain measurements (RMS granularity) or spectral sensitivities. The Kodak
   PDFs were found but not read.
5. **What a low pressure sodium lamp does to a colour negative.** Our sodium
   derivation is of the LAMP. How a 1990 film recorded a 589 nm monochromatic
   source, which is a colour it essentially cannot reproduce, is a separate and
   quite striking question nobody has asked.

---

## Part 5. Findings and interpretation

### Findings

F1. The Eastman EXR family (5245 EXR 50D, 5248 EXR 100T, 5296 EXR 500T) was
introduced 17 January 1989 and is the motion picture film of LEDGER's window.

F2. A wet overcast exterior in 1990 meant the fastest of those stocks, so our
target scene is the one where period film was grainiest.

F3. Film emulation has four pillars: colour response, grain, halation, gate
weave.

F4. Halation is a red-layer effect producing reddish-orange halos, physically
distinct from bloom.

F5. `LedgerFilmGrade.shader` implements grain, vignette, bloom and a tonemap,
and scales grain inversely with luminance, which is correct behaviour.

F6. `ue-probe/Source/` contains no grade of any kind. The look lives entirely
in the engine D16 archived, making it the third such system after the
frame-time instrument and the preset cost model.

F7. Of the four pillars this project has one, with bloom standing in for
halation at the wrong colour.

F8. Kodak Gold 200 was the dominant consumer film of the 1980s and 1990s and
carries strong warm yellow and magenta casts.

F9. A surviving photograph of 1990 has passed through emulsion, automated
minilab printing, and a modern scan, and is therefore weak evidence of colour
and strong evidence of geometry, material and content.

F10. `vignette-scene.json:266` already derives a light's colour from CIE
matching functions rather than from an image, and is the in-house model for how
to handle this.

### Interpretation

I1. The reference-colour problem is the finding worth acting on. It is
systematic rather than random, every reference agrees with every other one, and
it pulls exactly the variable the visual bar is built on. A rule as short as
"photographs for geometry and material, physics for colour" would close it.

I2. Halation at the correct colour is probably worth more per unit of effort
than more grain. It is the effect people read as "film" without being able to
name, and the current stack produces its wrong-coloured cousin.

I3. The grade being stranded in the archived engine is now a pattern rather
than an incident. Three systems that represent real thinking (frame time,
preset costs, film grade) were built, argued and tuned in Unity and have no
counterpart in Unreal. None of them is lost, all of them are unported, and
nothing in the project currently counts them.

I4. Separating "period world" from "period image" is worth doing explicitly.
Canon leans toward the first and the shader header quotes an art direction
asking for a little of the second, and nothing records that as a decision.
