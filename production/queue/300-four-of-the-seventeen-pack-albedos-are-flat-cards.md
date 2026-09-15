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
