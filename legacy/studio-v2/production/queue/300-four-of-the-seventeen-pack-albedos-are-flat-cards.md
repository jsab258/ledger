line: art (the visual bar), sourcing
spec: Four of the seventeen albedo files in the city pack are near-flat cards
  and between them they clothe 411 of the street's 610 pieces. Replace them
  with ambientCG assets that have something in them, through the pipeline that
  already exists, and judge the result in the frame.
acceptance: A frame in which kerb, metal, plaster and concrete read as
  materials rather than as painted primitives, judged by Jafar's eye under D23.
  The supporting number is the per-file series in the status block below,
  re-measured on the new pack and printed beside the old one, so that a
  replacement which is merely a different flat card is visible as one.
max_sessions: 2
status: READY 2026-09-15, BEHIND QUEUE 299 and the order is deliberate. 299 is
  a parity bug with a right answer that moves the loudest surface in the frame
  by about a factor of 2.4 and costs no sourcing at all. A dark flat card is
  much quieter than a white flat card, and how much of this item survives 299
  is not knowable until 299's frame is on the screen. So 299 lands, the frame
  is looked at, and THEN this item is re-scoped against what is left.

  THE READING. Every albedo file in ledger/Assets/StreamingAssets/CityPack/
  textures, measured over every texel, sRGB bytes. 17 examined; the 34 _n and
  _r maps were not examined. lumSD is a standard deviation over the file, not a
  peak. chromaSpread is the mean of (max channel minus min channel) per texel.

    file          lumMean  lumSD  chromaSpread   pieces wearing it
    plaster         211.7    5.8     7.2            34
    kerb            184.3    6.6     0.0            95
    metal           134.8    4.6    22.5           132
    concrete        107.2    9.3     6.8           150
    ----------------------------------------------- 411 of 610
    brick_grey      114.7   44.3    26.3            12
    window          105.2   35.3    21.2            36
    brick_grey_b    117.3   28.1    39.6             -
    brick_red_b     120.7   26.9    73.6             -
    sidewalk        108.9   26.4    21.1             5
    glass            75.7   23.1    13.2            22
    brick_red       131.8   22.0    31.9            41
    wood             87.3   15.1    42.8            49
    asphalt          67.9   13.8     2.4             2
    concrete_b       93.4    7.1     7.9             -
    plaster_b       213.9   10.1     6.9             -
    roof             77.9    9.9    71.8             2
    roof_b           49.0    4.4     5.0             -

  kerb.jpg has a chroma spread of EXACTLY 0.0, so R equals G equals B on every
  texel of it. It is a greyscale card at 184 with almost nothing in it, and it
  is what 95 kerbstones wear along the whole length of the street.

  NO BOUND IS SET AND NOTHING GATES ON THESE NUMBERS. The apparent gap between
  10.1 and 13.8 is a gap in a printed series, not a measured threshold, and a
  file is not condemned by its standard deviation: roof_b at 4.4 is a dark tile
  that reads fine because it is dark. What condemns kerb, plaster and metal is
  flat AND pale together, and what condemns concrete is being the largest
  surface in the street with 9.3 in it.

  WHAT IS ALREADY THERE, so that nobody rebuilds it. ATTRIBUTION.json names
  every file's ambientCG asset id and licence: kerb is Concrete034, metal is
  Metal032, plaster is Plaster001, concrete is Concrete017, all CC0 1.0
  Universal, all 2K-JPG. ambientCG is on ledger-v2/research/license-allowlist.md
  line 5, so replacing one ambientCG id with another opens no licence question.
  tools/citypack/catalogue.json holds the whole catalogue as of 2026-09-13:
  2010 assets, of which Concrete 61, PavingStones 155, Rock 67, Metal 101,
  Plaster 7. tools/citypack/fetch_textures.py already splits the job into
  --inventory (ask, decide later) and --fetch (take the decisions), and
  .github/workflows/citypack-fetch.yml runs on a change to
  tools/citypack/choices.json and on nothing else, so committing that file IS
  the decision that a download happens.

  THE ONE THING MISSING, AND IT IS THE WHOLE DIFFICULTY. The catalogue carries
  an id, a size list and a zip link, and NOTHING ELSE: no tag, no description,
  no preview. So a surface cannot be chosen from it without seeing pixels, and
  every asset host is blocked from this container (fetch_textures.py's own
  docstring lists ambientcg.com 000 among four). Choosing by name alone is the
  guess that this tool was built to stop: its docstring records fifteen CI runs
  spent guessing at a corpus, ended by one --inventory pass that answered
  everything at once.

  SO THE SHAPE IS ONE MAXIMALLY INFORMATIVE RUN, and it is the same shape one
  level further in: a mode that downloads a SHORTLIST at 1K for the four
  surfaces, measures each candidate on the three numbers above, writes a
  contact sheet and the table, and commits both. Then the choice is made here,
  locally, in seconds, from evidence, and choices.json is committed once.

  IS THAT A NEW INSTRUMENT. Said plainly rather than argued around: it emits no
  verdict key, gates nothing and measures no frame, so it is a sourcing aid and
  not an instrument under Jafar's standing rule. If he reads it the other way
  the rule bites and something must be retired in the same batch. Flagged for
  him rather than decided here.

  AND THE FIVE VARIANT FILES REACH THE FRAME JAFAR JUDGES BY NO ROUTE AT ALL,
  which is a narrower claim than the one first written here and is the only one
  that survived being checked. THE FIRST VERSION SAID THEY WERE "worn by
  nothing" and that is FALSE: brick_grey_b, brick_red_b, concrete_b, plaster_b
  and roof_b are named in ledger/Assets/Scripts/Game/AssetLibrary.cs, which at
  line 262 describes brick_red_b as "chosen by a hash the caller already has",
  and at 520 quotes a measured facade breakdown reading
  mat_brick_grey_b#g1:95% mat_concrete_b#g1:2%. The Unity host has a per
  building variant system and uses them heavily. They were declared unreached
  after counting pieces in one spec and not after grepping the tree.
  WHAT IS TRUE. production/specs/vignette-pieces.json names sixteen surfaces
  and not one of them is a _b, and the Unreal binder has no variant mechanism:
  CandidateList builds no _b candidate and MapsFrom has no variant branch, so
  the probe binds exactly one file per surface name. So the street in the
  vignette wears ONE brick where the Unity host wears two, and the same for
  plaster, concrete and roof. That is a difference between the two engines
  rendering one street, which is the single thing D1 exists to catch, and it
  is worth more than the miscount it replaced: the variation is already
  fetched, already attributed, already committed, and the engine that takes
  the judged frame cannot ask for it.

  THE REFERENCE, so the shortlist has a target. The Hook sheet's material strip
  names four materials and one of them is QUAY STONE. Concrete034 is smooth
  cast concrete, which is the wrong material identity for a late-80s British
  port kerb quite apart from being too pale. Railings in such a town are
  painted iron, usually dark, usually weathered. Both are sourcing decisions
  with a right answer in the panel, and the panel is
  production/art/atlas-01/concepts/hook.png on origin/art/atlas-01.

  RUN 44 MOVED THIS ITEM TO THE TOP OF THE VISIBLE PROBLEM, and the number is
  new. After the grade landed, the five bins on screen in vign_hook_day render
  at 177.6 to 200.0 with a median of 177.6, measured on solid objects wide
  enough that the patch is the object rather than its background. In the same
  frame the ground band median is 69.1, brick_red is 127.7 and the kerb is
  93.7. SO THE BINS ARE NOW THE BRIGHTEST THING IN THE STREET, and in absolute
  terms they sit close to where the kerb was BEFORE the fix (179.7). One of
  the three things Jafar named is fixed and another has become the worst.

  AND THE GRADE BARELY TOUCHED THEM: the bins' before-and-after ratio is 0.884
  where the predicted texel ratio for metal is 0.747. A LIKELY REASON IS NAMED
  AND NOT ASSERTED: they stand at 18 to 27 m, the fog cap is 0.100 and the sky
  is around 205, so aerial perspective lifts a far object toward the sky value
  and the albedo it started from matters less. THAT IS A HYPOTHESIS AND NOT A
  READING. What would test it is the same bin measured at two distances in one
  frame, or the fog set to 0.000 in a single cell, and neither has been done.

  WHAT THIS DOES TO THE ITEM. metal.jpg is lumMean 134.8 with lumSD 4.6, a
  near-blank card, so nothing in the pack gives a bin its dents, its rust or
  its grime, and the darkening this batch shipped cannot supply them. But if
  the fog hypothesis holds, a better texture will be lifted by the same fog
  and may not fix the brightness either. SO THE ORDER IS NOT OBVIOUS ANY MORE
  and this item should not be picked up as though it were: measure the
  distance term first, because a sourcing round that cannot move the pixel is
  the shape of waste this project keeps finding.

  THE DISTANCE TEST RAN AND THE FOG HYPOTHESIS IS REFUTED FOR THE BINS,
  2026-09-15, ordered by Jafar to run BEFORE any texture sourcing. It cost no
  dispatch: run 44 already carried a fog 0.000 cell on cam_hook
  (vign_fog_maxop0000, status WROTE), so the control was a file on disk and
  the entry point was cheaper than the argument, per .claude/rules/ci.md.

  SAME camera, SAME grade, SAME pieces, only the fog cap differs:

    piece                dist_m   fog 0.100   fog 0.000   ratio
    dustbin0               18.3       200.0       195.1   0.976
    dustbin0_lid           18.3       177.6       166.7   0.939
    dustbin1               18.9       177.6       167.6   0.943
    dustbin1_lid           18.9       169.4       156.5   0.924
    prop_outdoor_bin_0     26.6       197.5       190.2   0.963
    bollard (decorative)   16.1        76.8        33.9   0.441
    bollard (decorative)   19.6        78.9        31.0   0.392

  7 of the 8 bin and bollard pieces in the spec are wide enough to sample at
  8 px or more; the eighth is not and was not sampled.

  SO: TAKING THE FOG AWAY ENTIRELY DROPS A BIN BY BETWEEN 2 AND 8 PER CENT.
  They read 156 to 195 with NO FOG AT ALL, against a ground band median of
  69.1. The bins are not fog-lifted. They are bright on their own, and the
  hypothesis recorded here yesterday, that aerial perspective was doing the
  work, is WRONG. It was recorded as a hypothesis with its test named rather
  than as a reading, and the test refuted it, which is the only reason this
  paragraph can be written instead of a wasted sourcing round.

  THE ANSWER TO JAFAR'S QUESTION IS THEREFORE: a better texture WILL move the
  pixel, and THIS ITEM IS THE RIGHT ONE. The bins are lit metal wearing a
  near-blank pale card (metal.jpg, lumMean 134.8, lumSD 4.6) with no dirt, no
  dents and no rust in it, and the grade cannot supply what the file lacks.

  AND THE TEST FOUND SOMETHING NOBODY ASKED FOR: THE BOLLARDS ARE FOG-LIFTED
  AND THE BINS ARE NOT, on the same surface at the same distances. A bollard
  falls to 0.39 and 0.44 when the fog goes, from about 77 to about 31, so fog
  was supplying roughly 60 per cent of what it rendered at; a bin at a GREATER
  distance falls to 0.96. Same material, same camera, opposite behaviour. The
  reading that fits without further evidence is that the bins face the sky and
  are lit while the bollards are shadowed or turned away, so the bin starts
  bright and has little headroom for fog to add while the bollard starts dark
  and is mostly fog. THAT IS A READING OF ONE FRAME AND NOT A MEASUREMENT OF
  THE LIGHTING, and it is written as such. It matters here because it means a
  single number for how metal renders would be wrong: the same surface is
  doing two different things in one street.

