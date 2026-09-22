# NOW

THE STANDING LIST, in priority order, drawn from ROADMAP.md. Work down it.
When an item finishes, strike it and take the next without asking. The list is
kept current here; when it runs short it is extended from the next part of the
roadmap.

Last updated 2026-09-22, in the fourth sitting on his PC.

SITTING: started 2026-09-22T14:30:00+02:00, limit 6h

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
- [ ] COLOUR, AND THE MEASURE IS NOT TO BE TRUSTED ALONE. Taking a tiled
      photograph off the window panes made the picture better and this
      number worse, 16.8% to 11.5%, because a repeating dark checker is
      texture and the measure counts texture. Read it beside the picture,
      never instead of it. The honest remaining gap is that the sheet's
      frame is FULLER: its parade is close and ours recedes.
      The old wording follows, for the arithmetic: 16.8% of our
      pixels carry real colour against the sheet's 25.8%, up from 2.0% this
      morning. What is saturated in the reference is the BRICK rather than
      the paint - there is so much more of it - and ours is now at its
      value and just under its saturation. The rest is that the sheet's
      frame is fuller: its parade is close and ours recedes.
- [x] BRIGHTNESS IS SETTLED, AND NOT AT THE MATCHING NUMBER. Sky at 1.70
      lands our mean at 120.3 against the sheet's 119.7 - and at that value
      the brick loses its punch, the glass goes pale grey and the street
      reads hazy. 1.35 measures 111.6 and looks like a street. That is the
      second time today a measure moved the right way while the picture
      moved the wrong way, and both are written into the recipe.
- [x] THE GLASS STOPPED BEING A TILED PHOTOGRAPH. It carried the pack's
      glass map box-projected across it, so every window on the street had
      a repeating dark checker on it, which reads as a grille.
- [x] AND THE SHOPS HAVE ROOMS. The carcass's dark face stood 75 mm behind
      the pane and filled the opening, so the lit interior card a metre in
      had NEVER been visible - which is why two attempts at the glass
      changed nothing. The spec's interior_card_depth_m of 1.2 is what it
      was always for.
- [ ] THE PANE ITSELF IS STILL OPAQUE, at 59 against the sheet's 69, and
      this is set aside after FOUR attempts rather than two. Tried:
      lightening it (a lighter panel), the Transmission socket (no change),
      raytraced refraction per material (no change), and the room (a real
      fault, fixed, kept). The next attempt starts by finding out what in
      this EEVEE build refuses the transmission - the render method or the
      material's blend mode - and not by lightening anything again.
- [x] THE DUSK FRAME CAME BACK, and better than it was: mean 6.1 to 21.0,
      with the lit shop rooms throwing light out onto a wet road that
      mirrors it in long streaks, the lanterns lit, and the lettering
      readable on both sides. D31 asked for dusk, wet, lamps lit and a
      figure in silhouette and it now has all four. The shop rooms did it -
      there was nothing behind the windows to light the street WITH.
- [ ] DEPTH BEYOND THIRTY METRES, parked. Two failed attempts are written
      into the recipe and the next one does not start from scratch.

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
- [ ] AND THE SAME THING IN THE PACKAGED BUILD: written, not yet proven.
      The probe now saves the mill and both memories, rebuilds the world
      from the authoring, lays the save back over it and prints what
      survived - including the hop count, which is what separates the
      shopkeeper who SAW it from the lad who HEARD it. The verdict check
      judges that line the moment one arrives. It needs the runner to
      compile it, and no verdict carries the line yet.
- [ ] The witnessed run and the unwitnessed control, from equivalent clean
      starts, in the packaged build, with a save, a restart and a reload in
      between, and the control producing no mention.
- [x] THE AUTOMATIC CHECK READS THE RESULT NOW. The verdict file has said
      at its own head since it was written that nothing read it, so a run
      whose input path was dead got committed and pushed GREEN. It is read
      on every probe run and it reads the PAIRS, not the positive halves:
      a witness filed it AND an occluded one filed nothing; the rumour
      passed when the two stood together AND did not when they were apart.
      It also refuses a verdict measured on another commit.
- NOTE: the probe already commits two crimes and judges the witness every
  run. What is missing is the SAVE, the RESTART and the RELOAD between
  them, and the unwitnessed control to compare against.
- [ ] Keep the pair as a regression.
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
- [ ] SO THE QUESTION IS STAGE 2's, NOT STAGE 1's, and it is worth asking
      properly when stage 2 starts: whether image-to-3D is wanted for
      CHARACTER heads or props later, on a card with ten gigabytes. Until
      then it gates nothing and a sitting spent on AMD PyTorch buys nothing
      that is on the list.

## 4. The small-model test for conversation

- [ ] A small model behind the conversation interface, scored on a bar that
      counts a well-formed wrong answer as a FAILURE.
- It gates the hardware floor.

## 5. Character concept sheets (stage 2)

- [ ] The six archetypes, by the three-pass method.

## Where things stand

THE REFERENCE WAS WRONG ALL WEEK. Every visual comparison since the 9
September ruling went to Codex's retired sheet, which still resolves on its
branch, so nothing errored and nothing warned. The approved sheet is now at
production/reference/hook-sheet.png and that directory is the only place a
reference lives - a rule in CLAUDE.md, a refusal in the tool.

READ AGAINST THE RIGHT PICTURE, the street was 38 per cent too dark, grey
where the reference is warm, and the wrong SHAPE: the sheet's street panel
is 1.89:1 and we were rendering 1.27:1, which is eleven degrees of
horizontal field and put our parade a third further off than the
reference's however the camera moved. It now measures mean 111 against 120
and warmth +12 to +19 against +18.5, from 74 and +0.7 this morning.

THE STREET GAINED: white sash windows, which it had none of and which are
what the reference is made of; a crowned road, which the spec had specified
and nobody had built; fourteen pavement props the spec had already placed
by name; one invented car; aerials on two stacks; and shops on the near
west block by Jafar's ruling, now a line in canon.

THE SIMULATION IS WHERE IT WAS. A crime is committed by a key press, a
memory survives a save and a reload against thirty-eight golden rows, and
the rumours-across-a-restart half is untouched today.

A STOP HOOK now refuses to let a turn end while the standing list has work
on it and the sitting has time left. It is the only automation this session
gets and Jafar named it.
