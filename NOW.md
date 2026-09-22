# NOW

THE STANDING LIST, in priority order, drawn from ROADMAP.md. Work down it.
When an item finishes, strike it and take the next without asking. The list is
kept current here; when it runs short it is extended from the next part of the
roadmap.

Last updated 2026-09-22, in the fifth sitting on his PC.

SITTING: started 2026-09-22T20:53:35+02:00, limit 11.11h

That one line is read by the stop hook, which will not let the turn end while
items below are unstruck and the six hours have not run out. It is written at
the start of every sitting; without it the hook permits and says it measured
nothing.

## 1. Toward the Hook sheet (stage 1)

- [x] The shopfront's two faults: the doors where they meet, and the transom
      light that did not separate from the glazing. Both fixed and both now
      measured rather than looked at.
- [x] The rest of the terrace fronts. All three blocks build and render: the
      six-bay parade with a rhythm rather than one stencil, and the two plain
      rows, which are a different building rather than the parade with parts
      switched off.
- [x] The street from the sheet's own viewpoint, with the road between the two
      sides and somebody standing in it. That frame is what the stage is
      judged on and it did not exist before today.
- [x] LIGHT AND WET, D31's first step, done against the sheet rather than
      against my own idea of it. The lanterns light the street instead of
      being sealed inside their own housings; the day is wet, which the scene
      file had said all along; there is a tone curve.
- [x] THE PAIR IS OF THE SAME STREET. Ours was the mirror of the reference -
      wrong pavement AND wrong way along - so nobody could have said which
      way the gap ran. tools/hook-pair.py builds it now, every step.
- [x] SURFACES, D31 step two. Brick, slate, setts, tarmac, kerb, timber, off
      a pack we already hold. The photograph supplies pattern and relief; the
      project supplies the palette, because the pack's own names do not match
      its own colours.
- [x] SIGNAGE. The four signs that were already drawn are on their boards, and
      the boards are painted from the spec's period list, in waves.
- [x] Double yellows, lit shop windows you can see into, rooms behind the
      other windows rather than holes, six people in coats.
- [x] THE REFERENCE ITSELF WAS WRONG, and it is fixed. Every comparison
      this week went to Codex's retired sheet, which still resolves on its
      branch, so nothing ever failed. The approved in-house sheet is now at
      production/reference/hook-sheet.png and that is the only place a
      reference lives; the pair tool refuses when it is missing.
- [x] VALUE. Ours measured mean 74 against the sheet's 120 this morning and
      measures 118.6 now. Three passes: the palette read off the sheet, then
      corrected against our OWN render per channel, because a value that
      passes through AgX does not stay where it was put.
- [x] COLOUR, the warmth half. +0.7 against the sheet's +18.5 this morning,
      +17.0 now. The brick is warm red on both rows; the plain row's
      neutrality was most of the deficit, since it takes the left third.
- [x] WHITE JOINERY. Every upper window now carries a two-over-two box sash
      in a joiner's sections. There was no frame at all before - a pane in a
      hole with a stone sill - and it is what the street is made of.
- [x] THE YELLOWS, halved. Right to be there, wrong to be the loudest thing.
- [x] ONE CAR, invented from class-average numbers rather than fetched,
      because canon forbids a recognisable real one.
- [x] THE WET ROAD ACTUALLY REFLECTS. EEVEE ships with raytracing off, so
      nothing in this street reflected anything and the roughness curve had
      nothing to work with.
- [x] THE FRAME IS THE SHEET'S OWN SHAPE, and that was the structural one.
      The sheet's street panel is 617x326, an aspect of 1.89; ours was
      1400x1100, 1.27, very nearly square. At a 60 degree vertical field
      that is a horizontal half-field of 47.5 degrees against 36.2, and it
      decides how far down the street the parade has to be before it enters
      the frame at all: 6.7 m against 10.0. No amount of moving the camera
      could close that, and two hours went on trying to.
- [x] THE PAVEMENT IS USED. Fourteen props - bins, crates, a skip, pallets,
      a barrel, bollards, cones, a barrier, an A-board, the gully grate -
      loaded from meshes we already hold and placed where the scene spec
      already said, every measured height agreeing with the spec's own.
- [x] THE ROAD IS CROWNED. The scene file has carried a 1-in-40 crossfall
      since it was written, with its own warning that a flat carriageway
      puts the wet-condition water everywhere instead of at the kerb. It
      was one flat box. 75 mm from crown to channel, derived not typed.
- [x] WARMTH IS MATCHED: +18.9 against the sheet's +18.5, from +0.7 this
      morning.
- [x] THE NEAR WEST BLOCK CARRIES SHOPS, ruled by Jafar and now in canon:
      east side the six-bay parade, near west block shops by the cab
      office, far west block plain terraces. The spec's reason for it being
      plain - "because cam_B stands here and never photographs it" - had
      lapsed the day the hook camera moved onto that pavement.
- [x] LETTERING READS THE RIGHT WAY ROUND. The west blocks are built as a
      REFLECTION of the east, which reverses their handedness with them, so
      the first frame with shops on the near west had MICKEY'S painted
      backwards across it. Flipped per side, and checked, because no
      geometry check can see a mirrored box.
- [x] THE FIGURES HAVE LEGS AND A NECK, and two of them have moved back
      down the street: one was standing three metres from the lens.
- [x] THE JOINERY IS ACTUALLY WHITE. It was rendering CREAM because the
      tint gain is clamped at 6.0 and white over the wood map needs 12 on
      blue. Painted joinery takes the plaster map now - gloss paint does
      not show grain - and the clamp stays where it protects the brick.
- [x] AERIALS on the two stacks the spec names, elements at the 0.27 m its
      own physics derives. They read clearly on the skyline.
- [x] THE PIERS ARE PAINTED and the wetness reaches the render. Two of the
      largest painted areas on every bay were `stone` taking the concrete
      map; and _wetten had been writing to sockets that already carried
      texture links, so none of it had ever rendered.
- [x] THE ROAD IS WET, with the water where the camber sends it: the crown
      drains, the channel mirrors the sky.
- [x] COLOUR, AND ALL FOUR NUMBERS TOGETHER. The tone-mapping look and the
      exposure turned out to be one decision, and the answer changed once
      everything else was in place: Punchy was right when the street was
      three times too dark, and with the palette, the road, the glazing and
      the haze where they belong it is CONTRAST that carries the colour.
      High Contrast at exposure 0.05 measures mean 123.0, highlights 224.7,
      warmth +19.3 and 22.6% of pixels carrying real colour, against the
      sheet's 119.7, 229.3, +18.5 and 25.8%. It was 74.4, 163, +0.7 and
      2.0% this morning. AND THE PICTURE AGREES, which was checked rather
      than assumed - twice today it did not.
- [x] WEATHER AND WEAR, WHICH THE LIST NEVER CARRIED AND THE ROADMAP
      NAMES. Stage 1, in its own words: "GRIME IS THE STRATEGY, not a
      finishing pass... a surface carries its wear as a SEPARABLE LAYER,
      and the floor for how much is a number measured off the first
      authored facades rather than invented." Ours had none at all. The
      number: the sheet's brick varies by 46.8 and ours varied by 16.2 -
      three times too clean, on the surface there is most of. It is two
      things a real wall does, kept separable: soft patches over a few
      metres, because rain does not wash a wall evenly, and a darker foot
      to every wall from splash and rising damp. 22.5 now; the rest of that
      gap is photographic detail in the map rather than wear on top of it.
- [x] THE FAR END IS THE BASIN END, and the world had already said so. The
      scene file: "0 at the south end, +x north". The hook camera stands at
      33 and looks at 2, so it looks SOUTH. The town form bible: "Quay
      Street links an OLD BASIN to the market", the market uphill north,
      behind the camera. MICKEYS.md routes the pub's deliveries "from the
      basin approach". So the one thing already at this end of this street
      is the basin, and nothing here decides anything stage 6 decides: a
      quay apron the road runs out onto, nine dock sheds gable-on at two
      ranges, one crane. No door, no window, nothing anyone can walk to,
      every piece named backdrop_*.
      THE MEASURE IT WAS FOR, which could not be taken at all before,
      because the far end was sky. On the sheet the near brick reads mean
      57.3 at saturation 0.535 and the far buildings mean 136.0 at 0.146 -
      distance makes things paler and greyer, which is most of what says
      how far the eye is carrying. Ours now reads 72.6/0.416 near and
      148.2/0.063 far: a falloff of 75.6 and 0.353 against the sheet's
      78.7 and 0.389.
      AND IT IS THE FIRST TEST OF TODAY'S RULE. The sheet closes both its
      views with a WOODED HILLSIDE; R08's photograph of the working water
      is "warehouses on piles, a distant crane/bridge and chain-edged
      quay". Where they disagree the photograph wins, so: sheds and a
      crane, not a hill.
      TWO ATTEMPTS AND THEN THE DIMENSIONS. Attempt one put a 1.7 m-thick
      crane in the middle of the view, which came back a solid wedge the
      size of a building, and an 11.5 m shed dead centre that read as a
      grain silo. Attempt two thinned the crane to 0.5 m in two pieces and
      moved it off axis, and split the row into two ranges. What finished
      it was neither attempt but a CHECK: no mass may stand taller than the
      street's own ridge, which the selftest asks the spec for rather than
      typing, and which caught three ridges over it that the eye had
      passed.

## 2. Rumours surviving a restart (stage 3)

- [x] Memories survive a save and a reload, held by thirty-eight golden rows
      against the real C#, with four engine-versus-bench disagreements found
      and fixed.
- [x] AND AN INDEPENDENT CHECK BROKE IT NINE WAYS, none of them reachable
      from the fixtures I had written. The worst: a corrupt save was a
      harmless no-op in Unity and silently destroyed gossip state in
      Unreal. Every one is fixed and pinned by a row.
- [x] THE JSON HALF IS PORTED. A memory's save format is the markdown, and
      both engines already read it; a RUMOUR is not in that markdown - it
      lives in the mill and goes into the save FILE as JSON under "agents",
      a different format with a different parser, and the port could not
      read a save at all. It can now, and thirty golden rows pin the state
      the restore arrives at: how many rumours came back, at what
      confidence and hop count, which topics stay suppressed, and the
      agent's own numbers. Zero mismatches against the real C#.
      THE SAVE'S OWN BYTES ARE ONE OF THE ROWS, because the port cannot
      capture, only restore - a fixture the port wrote itself would prove
      only that the port agrees with the port.
- [x] THE ROUND TRIP IS PROVEN IN BOTH ENGINES: save, restart, reload, and
      both rumours come back with their confidence, their hop count, the
      loyalty, the leash, the suppressed topic and the known fact - while
      the control, an agent who witnessed nothing, comes back holding
      nothing. Each engine uses ITS OWN writer, so a match is the two of
      them agreeing about a file the other never saw. The port could only
      read a save this morning; it can write one now.
- [x] AND IT IS PROVEN IN THE PACKAGED BUILD. The verdict from run
      a1eac56 carries it: the mill saved to 730 bytes, the world rebuilt
      from the authoring, the save laid back over it, and afterwards the
      shopkeeper still holds her rumour at confidence 0.94 and HOPS 0 while
      the lad still holds his at HOPS 1. That pair is the whole claim - she
      SAW it and he HEARD it, and a restore that handed everyone the same
      records would have collapsed them into each other. Both memories came
      back with their events and the markdown round-tripped byte for byte.
- [x] THE WITNESSED CRIME AND THE UNWITNESSED CONTROL, and the control is
      in the SAME RUN, which is stronger than the two runs the item asks
      for. Two separate starts differ in everything the engine does not pin
      - tick order, frame timing, whatever the scheduler did that second -
      and any of it could explain a difference. What is here is two crimes
      in one run with one witness position each: A is seen from a metre and
      a half, B has both agents behind west_south_bay2 and their traces
      stop on the building. Same build, same mill, same perception code,
      same frame; the only thing that differs is whether anybody could see
      it. The verdict now counts what followed from each - observations
      filed, and rumours naming each crime's own victim - because a rumour
      with no observation behind it is the mill inventing, and each is a
      separate way to fail. Written; the runner proves it.
- [x] THE PAIR IS THE REGRESSION. tools/crime-verdict-check.py runs on
      every probe run and judges both halves - the witness who filed and
      the occluded one who did not, the round that passed and the round
      that did not, and the hop count that separates seeing from hearing.
      Twenty-four checks of its own, its accepting case the landed verdict
      and its rejecting cases that same file doctored one value at a time.
- It touches memory, so its tests and the independent check apply.

## 3. The 3D generation test on this machine's card

- [x] ANSWERED WITHOUT RUNNING ANYTHING, and the answer is that it decides
      nothing about stage 1. Counted off the street's own bill of materials:
      78 lines, of which 33 are GENERATE from primitives, 33 HAVE, 6 ENGINE,
      5 FETCH and 7 made by the 2D image generator that already runs on this
      machine. NOT ONE is routed MESH3D. The single BLOCKED line is period
      WARDROBE, not shape - and its own note says it waits on a decision
      about the character pipeline rather than on money, a decision D2 and
      D16 took on 10 September: MetaHuman, free under a million in revenue,
      already on the allowlist, and its clothing arrives fitted and rigged.
- MOVED TO STAGE 2, UNSCHEDULED, and Jafar corrected what it is for:
  THE CASE WAS NEVER HEADS, IT IS VOLUME. Hundreds of distinct props once
  the street becomes a town. So it comes back when MAKING PROPS ONE AT A
  TIME BECOMES THE BOTTLENECK - which is a thing that will be obvious when
  it happens - and not merely when stage 2 starts. Until then it gates
  nothing.

## 4. The small-model test for conversation

- DEFERRED BY JAFAR TO THE NEXT SITTING, 22 September, in his words: "1,
  fetch it and run the test next sitting... Use the Vulkan build, since the
  card is AMD." It is not an open item of THIS sitting and is written
  without a box so the stop hook does not demand it against his ruling.
  A small model behind the conversation interface, scored on a bar that
  counts a well-formed wrong answer as a FAILURE.
- IT GATES THE HARDWARE FLOOR, and here is exactly where it stands so the
  next sitting does not rediscover it:
  THE MODEL IS ALREADY ON THIS MACHINE. Qwen3-4B-Instruct-2507-Q4_K_M.gguf,
  2.5 GB, under ~/ledger-imagegen/models - Apache-2.0, already on the
  allowlist, already attributed, already used here as the image
  generator's text encoder. Nothing needs buying and nothing needs
  deciding about licence.
  WHAT IS MISSING IS A CHAT RUNTIME. That folder holds sd-cli and
  sd-server and no llama.cpp; the ggml DLLs beside them are the image
  generator's. So the fetch is one binary, MIT, and it is the only thing
  between here and an answer.
  AND THE BAR IS ALREADY ARGUED FOR. production/research/
  conversation-model-capability read three papers in full and its finding
  is the item's own premise: constraining a small model to a closed set
  makes the FORMAT perfect and can make the CHOICE worse. That is why a
  well-formed wrong answer has to score as a failure.

## 5. Character concept sheets (stage 2)

- BLOCKED AND NOT THIS STAGE'S. The six archetypes, by the three-pass
  method. Two reasons it carries no box: it is STAGE 2, and stage 1's own
  rule in ROADMAP.md is "what may not happen here: ... more unique buildings
  or animation polish before the presentation order above is done"; and its
  terms - what an archetype is, how many passes of what - are not defined
  anywhere yet, so there is nothing to work down. Defining them is Jafar's
  or a sitting of its own.

## 6. What the audit of the sheet leaves to do (stage 1)

- [x] ONE METAL SHOPFRONT ON THE PARADE, and the check chose its colour. The audit's second contradiction:
      there is not one metal shopfront on the approved sheet and every
      frontage we built copies it, while D01 gives Quay Stores "a plain
      metal shopfront" and D06 says "Hook shops receive METAL FRAMES,
      practical light fittings and repair patches within older masonry" -
      both decided from R05's 1989 photograph. Under the rule recorded
      today the photograph wins. Not every bay: D06 says metal refits AMONG
      older masonry, so the street should show the mixed fabric the
      research records rather than a uniform timber parade.
      DONE: bay 1, the fish shop, which MICKEYS.md puts in the bay north of
      the cab office and which is the trade that most wants a washable
      front. Slimmer sections - 45 per cent of the timber ones, which is
      the whole visual difference, since a grey timber shopfront still
      reads as timber - sitting nearly flush instead of proud with a
      moulding, over a glazed tile stallriser instead of the shop's painted
      board. FOUR CHECKS HOLD IT: that one front is metal, that the parade
      is MIXED and not all metal (2 of 9 shopfront bays; the keying is by
      bay index so west_north's bay 1 takes it too, which D06 covers since
      it speaks of Hook shops generally), that the sections really are
      under half, and that the stallriser is tile.
      AND THE COLOUR WAS CHOSEN BY THE CHECK. A dark anodised grey is a
      real period finish and came out at luminance 0.1554 against grey
      brick's 0.1330 - inside the 0.02 this recipe refuses - so the new
      front would have vanished into the wall it was cut into. Silver mill
      finish at 0.339 is clear of the brick below and of the white timber
      beside it, and is the commoner 1989 front anyway. Fourth time that
      check has caught a colour picked for being plausible rather than for
      being visible.
      WHAT IT IS NOT: R05's stallriser is PATTERNED tile and ours is plain,
      because we hold no tile map and noise pretending to be a pattern is a
      texture pretending to be evidence. And at thirty metres the thinness
      carries the read more than the colour does.
- [x] THE TYING FRAME, LOOKED AT WITH THE STREET FINISHED, IN HIS WORDS: "one screenshot of the street at dusk,
      wet, lamps lit, a figure in silhouette." wet_night has been rendered
      before, but not since the wear, the haze, the basin end, the crowned
      road, the glazing and the props all landed. It is the frame the whole
      stage is supposed to tie together and nobody has looked at it with
      the street finished.

## 7. THE ORDER JAFAR SET ON 22 SEPTEMBER, AND IT REPLACES THE ONE ABOVE

His words: "Stop tuning palette and colour now; every adjustment at an
unmeasured lens against a flawed sheet is work that will be redone." So
nothing above this line is worked on until the sheet is replaced.

- [x] REGENERATE THE HOOK SHEET, through the image lane, from the research
      and canon rather than the old prompt, at a resolution where a
      shopfront's detail is evidence and at least four times the current
      panel size. Correcting all four contradictions: Mickey's is a minicab
      office with a rank outside (D19); the shopfronts are the 1989 working
      street, metal frames and practical lights and repair patches in older
      masonry (D01, D06, R05), not the conservation-area refit; the basin
      carries working coastal craft, not canal narrowboats (D04, R08); and
      Mickey's and the fish shop are separate six-metre bays in a party-wall
      run (MICKEYS.md). The invented wooded hill goes; if the view closes on
      anything it is the bible's contour-following terraces. Shops carry
      signage from the period list. THREE PASSES, and the candidate goes to
      him beside the old one as a choice.
      The spec is `tools/imagegen/hook-sheet-2026-09-22.json`, written from
      canon and the bible with every item's sources in its own `governed_by`.
      Panels rather than a poster: street 2048x1088 (3.3x linear, 11x the
      area of the old 617x326 panel), a shopfront study at 1536x1024 because
      no street view at any resolution resolves a frame section, and the
      basin at 1536x1024.
      PASS 1 IS MADE AND READ. THE BASIN FIXES ITS CONTRADICTION OUTRIGHT -
      working coastal craft, a stone quay with bollards and chain, brick
      warehouses, a lattice crane, a lorry at a door, and no narrowboats.
      Its miss is the inland rise: green fields and white cottages instead
      of the bible's contour terraces behind retaining walls.
      THE STREET PANEL IS NOT A CANDIDATE. Mickey's came back a
      delicatessen with no rank outside; not one metal shopfront appeared
      although two were asked for. It DID fix signage, the cars, the far
      end, and legibility - 200 px of shopfront against the old panel's 60.
      THE SHOPFRONT STUDY SAID WHY: it produced R05's tiled stallriser,
      fluorescent strip and stacked goods inside a PAINTED TIMBER frame
      with pilasters. A clause in the middle of a long prompt loses to the
      subject.
      PASS 2 IS RUNNING, written from those faults: the cab office is the
      subject and is described by its contents; the metal front is the
      nearest bay and is described as an object; lettering is cut to one
      legible piece, because the model garbled every fascia it was given
      and the retired prompt's "only two pieces of lettering" clause
      existed for that; CCTV is in the negative, because two cameras
      appeared and canon says CCTV is rare.
      PASS 2 IS MADE AND IT FIXES BOTH OF ITS CONTRADICTIONS. The cab
      office is unmistakable - flat aluminium front, a counter with a man
      at it, a tariff card taped in the glass, a strip light, a grimy
      patterned tiled stallriser, brick repair patches - which is R05's
      photograph and D19's ruling in one frontage. The metal shopfront
      arrived with it.
      AND IT INTRODUCED TWO OF MINE. The rank came back as THREE LONDON
      HACKNEY CARRIAGES: canon forbids real car models, a TX is one of the
      most recognisable vehicles in Britain, and a minicab office has
      ordinary saloons rather than hackney carriages anyway. The prompt
      said 'ordinary dark saloon cars' and then said RANK. And MICKEY'S
      CARS is painted across the fascia in letters a foot high - a trading
      name canon has never minted.
      MICKEY'S IS ALSO A CORNER BUILDING AGAIN, with a return elevation,
      which is the audit's fourth contradiction reproduced by a prompt that
      never said otherwise. Naming what a thing IS does not stop a model
      giving it a corner; the party-wall run has to be described.
      FOUR PROMPT CORRECTIONS ARE WRITTEN DOWN AND NOT APPLIED, because two
      of them need Jafar: the trading name, the fleet, the furnishing of
      the anchor interior, and 'every gutter / every wall', which commands
      the uniformity the bible forbids.
      THE CANDIDATES ARE BANKED at production/art/compare/hook-2026-09-22/
      with their manifest and attribution.
      PASS 3 AND THE SIDE-BY-SIDE ARE NEXT SITTING'S. 2048x1088 is
      nineteen minutes on this card and 1536x1024 is ten, so a pass of the
      street is not a coffee. The side-by-side needs no new tool:
      hook-pair.py with the candidate passed as `--ours` produces exactly
      the old sheet beside the new one.
      PASS 4 IS THE CANDIDATE AND IT IS WITH HIM, 22 September, fifth sitting:
      the first to clear all four contradictions. Mickey's is a cab office,
      one bay of the terrace at its south end, on the left as the turned
      camera sees it, with a slim front over a patterned tiled stallriser;
      plain saloons outside; contour terraces at the far end. Faults: the
      next shop also says MICKEY'S, three cars not one or two, a satellite
      dish. Recommended to approve with those listed as not citable.
      WHAT PASS 4 LEARNED FROM PASS 3: the negative half of the prompt is
      ignored at the only setting this model runs at, so every fix has to be
      said as what IS there; and a model handed one SUBJECT isolates it,
      which is how the cab office became a kiosk.
- APPROVED 22 SEPTEMBER, and the steps now live in section 9. Then, in his order: derive the lens from the
      new sheet's own geometry and write down how; re-close palette and
      colour against the new sheet at that lens; then rework the shopfronts
      that were built to the old sheet's tidy timber, starting with the
      parade.

## 8. Stage 3, extended from ROADMAP.md because the list ran short

- [x] THE ARREST HAS TO BE REACHABLE FROM LIVE PLAY - AND IT IS, proven 22 September.
      MEASURED 22 September, not assumed: `Reaction.Confront` is the only
      function in the codebase that produces an arrest outcome, and it has
      ZERO callers outside Core - all five are in CoreTests.
      `CoatHost.Arrested`, the Game-layer function that would act on one,
      has zero callers as well, and `Homicide.cs:61` already says so in its
      own comment. The end of the story is reachable only from a test.
      ROADMAP puts this in the stage-3 gate for exactly this reason: "it
      was added the day the terminal state of the consequence spine was
      found to have no callers at all, which would have let the gate go
      green with the end of the story unreachable." It is not a bug in
      Core; Core is right and nothing calls it.
      BUILT, 22 September, fifth sitting, and waiting on the probe to prove
      it live. The rule is carried into the Unreal port (Reaction.h) and 79
      golden rows prove it answers as the C# does, including the exact line
      between "cannot place you" and "arrest". A constable stands across the
      road from crime A and in the yard for crime B, and his own sighting
      goes through the rule; the verdict prints the outcome, how many times
      it was asked and by whom. AN INDEPENDENT CHECK found four weaknesses,
      all fixed before commit - the worst, that the verdict check believed
      the run about itself. THE BOX CLOSES when a probe verdict reads
      outcomeA=Arrest and outcomeB=NothingToArrest.
      CLOSED. Probe run 35774194198 on 647c1ac, green, first try: the
      constable watched crime A for 2.5 s from across the road, reached rung 4
      and ARRESTED; for crime B, behind the terrace, rung 0, occluded, NO
      ARREST. Asked twice, caller named, ruled 0.35 and used 0.35.
      WHO THE CONSTABLE IS TO TOM IS JAFAR'S (decision 3): a stranger can
      never place him, so the arrest can only happen if the policeman knows
      him by sight. Built with that, one number to change.
- [x] RUMOUR REACH: PRINT THE FOUR NUMBERS BEFORE HE RULES, ordered by
      Jafar 2026-09-22. "I am not turning a constant up until a rumour
      crosses the town; my instinct is that one act reaching a circle is
      right, and that town-wide knowledge should come from severity,
      repetition and the newspaper. The series tells me whether that
      instinct survives."
      WHAT TO PRINT: how strong the town's friendships actually are; how
      confident a witness is at first sight; what counts as one retelling;
      and then a SERIES showing how reach moves as each is changed ALONE.
      WHERE THEY LIVE, found 22 September so the next sitting does not
      rediscover it: one retelling is `Gossip.cs` `HopDecay = 0.8` and
      `MinConfidenceToShare = 0.2`, with confidence multiplied by tie
      strength as well, which is the whole of "confidence x tie x 0.8,
      refused below 0.2". Tie strength is `SocialGraph.Link(a, b, weight)`
      and the authored weights come from the town builder in
      `StreetMap.cs`. FIRST-SIGHT CONFIDENCE IS PINNED TOO, and it is not one
      number. The mill's `Witness(...)` DEFAULTS to 1.0, certain, and only
      0.95 or above becomes hard knowledge rather than a rumour - but the
      real callers pass much less: a body is `Violence.BodyConfidence`,
      which is 1.0 in the open and 0.6 occluded; street trouble is a flat
      0.5; a racket sighting is `0.45 + 0.35 * (1 - competence)`, so 0.45
      to 0.80 depending on who was running it. So "how confident a witness
      is at first sight" has a DISTRIBUTION rather than a value, and the
      series has to say which caller it is measuring.
      NOTHING IS TUNED. The series changes one constant at a time and
      reports; no constant is left changed.
      PRINTED, 22 September: `dotnet run --project ledger/Soak -c Release --
      --reach-series --residents 200`. As shipped, 15 to 22 of 200 ever
      remember, two or three retellings deep - the witness's circle of about
      twenty. Filed as severe, the way a body is, 189 to 191 of 200. A
      realistic witness (0.5 to 0.6 sure) reaches only 5 to 10. Friendship
      strength is the steepest dial by far. Three towns agree. His instinct
      survives; the numbers and the choice are in FOR-JAFAR.md.

- RUMOUR REACH IS FLAT WITH POPULATION, and it is JAFAR'S to decide rather
  than an item to work. ROADMAP records it measured and unresolved: at 7,
  50, 200, 300 and 500 residents only 15 to 22 ever remember anything,
  because a rumour arrives at confidence times tie strength times 0.8 and
  is refused below 0.2, so with the authored tie weights ordinary talk
  dies at the second transfer. The constants are untouched. What reach the
  moat requires is his.

## 9. OVERNIGHT, 22 TO 23 SEPTEMBER - Jafar's list, in his order

He went to bed with this list and the ruling "nothing waits for me: any
decision, take your recommendation, write it in FOR-JAFAR.md, and carry on."
The sitting runs to 08:00.

THE VISUAL LANE, now the sheet is approved - the pair rendered after each step.
- [x] PASS 4 BECOMES THE REFERENCE at production/reference/hook-sheet.png, the
      old sheet kept beside it as retired. Not citable on it: the second
      MICKEY'S sign, the third car. The satellite dish IS citable - the
      household research records dishes as new and contested in 1990.
- [x] DERIVE THE LENS from the new sheet's own geometry, and write down how.
      DONE: production/reference/hook-sheet-lens.md. 46 degrees vertical on
      the sheet's own 1.882 frame (77 horizontal), camera LEVEL at 1.9 m with
      the picture shifted, turned 20.4 degrees towards the parade, at x -3.2,
      y -2.2. Checked by finding our render's vanishing point the same way as
      the sheet's: 0.732, 0.570 against 0.734, 0.570.
- [x] RE-CLOSE PALETTE AND COLOUR against the new sheet at that lens.
      DONE, measured region by region rather than on the whole frame,
      because the frames still differ in composition. Sheet against ours
      after: sky 244-248 / 239-244; brick 112/81/72 / 111/80/71; road
      149/150/154 / 145/147/151, and its texture variation now matches (31
      against 31) because the silver sheen is gone; pavement 100/83/61 /
      100/83/62; road paint faded to the sheet's cream. The sky is brighter
      to the camera than to the street, so the wet road did not brighten
      with it. The far parade (sat 0.16 against 0.24) is composition.
- [x] THE COMPOSITION, which the new sheet now answers.
      DONE: brick gable ends on every block (the terrace simply stopped, and
      the turned camera looked into its end building); the pavement turns
      the corner; the rank - two plain saloons at the east kerb just beyond
      Mickey's, tails to the camera, as the sheet has them; large stone
      FLAGS on the footway, where it had setts - the sheet and R09 agree;
      darker slate; and the far end closed by the inland rise, contour
      terraces behind retaining walls to the bible's 45 m crest.
      THE RISE HAD ITS TWO ATTEMPTS and is set aside as it stands: attempt
      one was a crowd of warehouses, attempt two reads as a hillside of
      houses but denser and more regular than the sheet's.
      NOT CHANGED, AND WHY: our terrace is taller than the sheet's (eaves
      6.2 m against about 5 to 5.5) - the spec is the geometry and the sheet
      is the look; the sheet's road bends where ours is straight, the same;
      the people are blocks, which is stage 2's; the west side is canon.
- [x] THE SHOPFRONTS to the 1989 photographs, starting with the parade.
      DONE for the parade. Mickey's is R05's metal front and patterned tile
      in the sheet's slate blue-grey, its name signwritten in plain capitals
      (PT Sans, lettered by the 2D maker, refused unless canon mints it);
      the fish shop's frame is metal all through, not metal jambs round white
      timber bars; the empty unit is whitened and has a TO LET board. FOUND
      ON THE WAY: the recipe put the parade's signs on EVERY shop block, so
      the street had two MICKEY'S across the road from each other - the very
      fault ruled uncitable on the sheet - and pasted three signs as whole
      shopfront photographs, ignoring the spec's crops. Both fixed from the
      spec. Measured on the front, sheet against ours: frame 57/72/86 vs
      52/64/75, tile 158/151/132 vs 132/126/112. STILL OPEN: the windows
      render opaque (the known EEVEE fault), which is now the largest
      difference on the cab office; and the game's own scene file still
      names the pub board, to move with the next push that runs the probe.

WHILE THE CARD IS BUSY - the work that does not need it.
- [x] THE ARREST FROM LIVE PLAY, proven: the box closes when a probe verdict
      reads outcomeA=Arrest and outcomeB=NothingToArrest. Ruled (a): a beat
      constable who knows the new owner by sight. (Section 8's item.)
- [x] RUMOUR REACH WRITTEN AS A MORNING DECISION in FOR-JAFAR.md, plain words,
      with a recommendation. NO CONSTANT CHANGES. It is decision 2 there,
      the series table in it, recommendation (a) leave the numbers.
- [x] RUMOURS SURVIVING A RESTART, the witnessed and unwitnessed pair: through
      save, restart and reload in the packaged build, with the automatic
      check - the control must still hold nothing after the reload.
      PROVEN on the runner, first time (adfacb3d, green): rumours about the
      seen crime 2 before the save and 2 after the reload, about the unseen
      one 0 and 0; the shopkeeper back first-hand, the lad one retelling
      out, his memory text identical. The check fails the run on any loss
      or any rumour about the control, and its restart fixture is now
      isolated the way the others are. Read as one run with two crimes and
      the rebuilt world as the clean start - said in FOR-JAFAR.md.
- [x] THE SMALL-MODEL TEST with llama.cpp on Vulkan, when the card is free.
      DONE: the intent router's own prompt and validator on Qwen3-4B Q4_K_M,
      llama.cpp b11111 Vulkan, 42 lines with one right answer each. Right
      33/42 (lexical path alone 18/42); WELL FORMED AND WRONG 8/42 - all
      three command lines obeyed, all three novel attempts missed, a paid
      tip for information routed to pay_off. JSON-constrained mode: the same
      33/42. Median 432 ms, 90th percentile 734 ms. Report in
      production/research/conversation-model-capability/SMALL-MODEL-TEST.md;
      the reading is decision 4 in FOR-JAFAR.md.
- [ ] THE "OVERNIGHT" SECTION at the top of FOR-JAFAR.md, five lines, before
      08:00: what got done, what is waiting on him, what went wrong.

AFTER HIS LIST, stage 3's gate from ROADMAP.md.
- [x] A WITNESSED CRIME REACHING A THIRD RESIDENT WITHIN ONE IN-GAME WEEK.
      PROVEN on the runner, first time (adfc53d7, green): three residents
      hold crime A, the lad's mate at two retellings, heard on day 4 at
      18:00 by his own memory - 78 hours after the crime - at 0.217 against
      the 0.2 floor, a margin of +0.017 that is printed and not moved. He
      survives the restart too (1 rumour and 1 memory before and after, two
      retellings out). The independent check found eight faults in the first
      version; all fixed before the push.

## 10. AFTER HIS LIST: stage 1 continued, the Hook match leading

Extended from ROADMAP.md's stage 1 at 23:00 on 22 September, when the
overnight list had only its Overnight section left. Visual first, as ruled.

- [x] THE CENTRE LINE. On the new sheet, in R09, and named by the scene file
      as the street's next step. Diagram 1008's own dimensions: 2 m marks,
      4 m gaps, 100 mm, on the crown.
- [x] CHIMNEY POTS AND CAPS. BOM line D3 was MANDATORY and never built: two
      roll-top pots on every two-flue stack (one buff replacement on every
      other), and an oversailing cap on each stack, as the new sheet's are.
      Pot colours sampled off the sheet's nearest stack.
- [x] THE LIGHTING COLUMN'S SHAPE, the retired sheet's last geometry in the
      street (retired-sheet-inheritance.md, row 4): look for a column on the
      new sheet to trace; if it shows none, the shape stays with R07's
      "plain bent-arm lighting" and the retired constants are marked so.
      DONE: the new sheet shows NO column; marked so in the recipe and the
      inheritance list, whose rows 2 and 3 are brought up to date too.
- [x] THE SCENE SPEC'S cam_hook FOLLOWS THE DERIVED LENS - SET ASIDE FOR
      JAFAR'S DECISION 5, 22 September, and struck so the list is honest
      about what can move tonight. Checking it found the two lanes build the
      street as MIRROR IMAGES: Unreal maps the file's z to its Y and puts
      the east parade on the right looking north (its own hook frame shows
      it); Blender and Unity put it on the left. MICKEYS.md's layout agrees
      with Unreal. Which way the camera turns depends on which is ruled
      true, so the spec is not moved until he rules.
- [x] THE ROUTING INDEX'S CLAIMS (retired-sheet-inheritance.md, row 5):
      GOVERNS.md's nine measured claims, each checked against the new sheet
      and the photographs, and marked kept, changed or unverifiable.
      DONE for all seventeen families: 2 kept, 10 changed, 5 not on the
      sheet. What the new sheet shows that the street lacks becomes the next
      items below.
- [x] SEGMENTAL ARCHED HEADS over the terrace's windows, and the dentil course
      under the eaves: the two things every window and roofline on the new
      sheet has and ours do not. DONE in two attempts: the first ring, at the
      sheet's measured 1.15 of the wall, vanished at the raking angle; the
      second curves the sash's head to the arch and glazes the segment, and
      lifts the ring to 1.3. The openings keep the scene file's dimensions.
- [x] THE KERB against the new sheet: pale grey with a clean arris; ours is
      dark and rough. DONE: its face 38/34/28 -> 77/73/66 against the sheet's
      96/84/71; still rougher than the sheet's. AND THE ROAD'S RED FLECKS,
      found beside it: the pack's asphalt has a red aggregate the sheet's
      road does not; its saturation is quartered, its value unchanged.

## 11. Stage 1 continued, from the re-read of the routing index

- [x] THE SATELLITE DISH the approved sheet has on the cab office, ruled
      citable by Jafar: a 60 cm solid dish on a wall bracket under the
      eaves beside the upper right-hand window, its receiver on an arm,
      aimed south along the wall and tipped up. No make, no mark.
- [x] GULLIES IN THE CHANNEL at a real spacing: the sheet shows gully
      gratings along both kerbs, and our street has one grate prop.
      NOT BUILT, and struck as decided rather than done: the scene spec
      places ONE gully by design (street.gully, B3), so more is a spec
      change and goes with the next probe run that touches the spec.

- [x] EVERY FLAG ITS OWN STONE: the footway read as a boarded floor (the
      concrete map's streaks at a raking angle) with lines drawn on it. Two
      attempts: a per-flag tone from the joints' own Brick texture, then the
      plaster map's undirected mottle under it. Its value did not move
      (111/95/77 -> 112/97/78).

- [x] THE BRICKS THEMSELVES: the widest surface gap left - the sheet's wall
      is individual bricks, bright and soot-dark, in dark joints; ours was a
      soft pink mush from the pack's low-contrast photograph. Real bricks
      now (215 x 65 mm, 10 mm joints, stretcher bond), each drawing a tone
      from the sheet's measured range, the pack map kept as staining. Two
      attempts: the second darkened the joints and warmed the faces.

- [x] THE ROOFLINE'S EDGE: a pale stone eaves course read down the whole row
      as a concrete coping; the sheet's roofline ends in a black cast-iron
      gutter. The course is brick now, with a 115 mm black gutter along it.

## Where things stand

THE SHEET ITSELF WAS THE PROBLEM, and that is what the sitting turns on. It
had never been checked against the research or canon; checked now, four things
on it contradict a ruling - Mickey's drawn as a pub against D19, not one metal
shopfront against D01/D06/R05, canal narrowboats in a coastal port against
D04/R08, and Mickey's sharing a corner building with the fish shop against
MICKEYS.md. Three of the four were COMMANDED: the approved sheet's prompt is
Codex's retired prompt, translated, and it asked for a pub and for unlettered
painted timber fronts.

JAFAR STOPPED THE PALETTE WORK AND SET A NEW ORDER: regenerate the sheet
first, from the research and canon, at a resolution where a shopfront is
evidence; then derive the lens from it; then re-close colour; then rework the
shopfronts. Pass 1 of three is generating as this was written.

WHAT THE STREET GAINED TODAY ANYWAY: the far end, which was sky and is now the
basin end the world already said was there - a quay apron, nine dock sheds
gable-on at two ranges and a crane, giving the aerial falloff the sheet has
and we had none of (75.6 and 0.353 against its 78.7 and 0.389). One metal
shopfront on the fish bay, whose colour the recipe's own check chose after the
plausible one came within 0.02 of the brick. And the tying frame, looked at
for the first time with everything in place.

WHAT IS SUSPECT: everything derived from the retired sheet, listed in
production/reference/retired-sheet-inheritance.md - the whole cam_hook row in
the governing spec including its 39 degree field, the lighting column's traced
ratios, GOVERNS.md's seventeen rows, and the prompt itself.

WHAT WAITS ON JAFAR, and the first one is the big one:

WHICH WAY THE PAIR IS SHOT. The hook camera looks the OPPOSITE WAY from the
sheet it is defined to reproduce. The approved sheet's prompt says "camera at
1.6m standing at SOUTH END LOOKING NORTH"; ours stands at the north end and
looks south. Both put the shops on the right, which is why nothing gave it
away, but the sheet's far end is the inland rise and ours is the basin. So
today's backdrop is right for our camera and wrong for the sheet. Either the
camera turns, which costs this week's composition work and the backdrop, or
the new sheet is prompted for a south view. Not a thing to settle by picking.

THEN: the trading name and the fleet outside the cab office; and his choice
between the regenerated sheet and the old one once pass 3 exists.

THE TOKEN ARRIVED and the probe's red is diagnosed and fixed: the check's own
selftest was failing on the runner because its fixture stopped being the only
control line in the file. Rotate the token when this is done - it came through
chat and is in a transcript.

llama.cpp Vulkan is next sitting's, as he ruled.
