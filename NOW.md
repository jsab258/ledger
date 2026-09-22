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
- [ ] COLOUR, THE SATURATION HALF, IS STILL THE LAST BIG ONE. 6.7% of our
      pixels carry real colour against the sheet's 25.8%. Adding shops to
      the near west did NOT close it and cost warmth (+18.9 to +12.3),
      because a shopfront replaces warm brick with dark glass. What the
      sheet has that we do not is a parade of SATURATED PAINT - oxblood,
      bottle green, deep navy, cream - filling the frame at close range.
      Ours is mostly the brick between the shops.
- [ ] THE SHOP GLAZING READS AS BLACK HOLES at this value key. It was
      tuned when the street was three times darker.
- [ ] THE ROAD IS A WIDE PALE BAND: right value, no wheel tracks, no
      standing water, no reflection worth the name near the camera.
- [ ] DEPTH BEYOND THIRTY METRES, parked. Two failed attempts are written
      into the recipe and the next one does not start from scratch.

## 2. Rumours surviving a restart (stage 3)

- [x] Memories survive a save and a reload, held by thirty-eight golden rows
      against the real C#, with four engine-versus-bench disagreements found
      and fixed.
- [ ] The JSON half: the save's own format ported, so a rumour in flight
      survives a restart the way a memory now does.
- [ ] The witnessed run and the unwitnessed control, from equivalent clean
      starts, in the packaged build, with a save, a restart and a reload in
      between, and the control producing no mention.
- [ ] The automatic check that reads the result, so a run where the key press
      silently stops working goes red.
- [ ] Keep the pair as a regression.
- It touches memory, so its tests and the independent check apply.

## 3. The 3D generation test on this machine's card

- [ ] Whether TRELLIS, TRELLIS 2 or Hunyuan3D runs for shape on ten gigabytes
      of AMD memory. One image through it, and what it needed.
- It decides how stage 1's remaining content gets made.

## 4. The small-model test for conversation

- [ ] A small model behind the conversation interface, scored on a bar that
      counts a well-formed wrong answer as a FAILURE.
- It gates the hardware floor.

## 5. Character concept sheets (stage 2)

- [ ] The six archetypes, by the three-pass method.

## Where things stand

The Unreal safeguard is confirmed on a real failed build, and the build runs
again after five red pushes that never reached it. A crime is committed by a
key press. A memory survives a save and a reload, and the engine and the test
bench have been caught disagreeing twice - about NaN, and about how strict the
two readers of the golden table were. The street stands as authored fronts on
both sides with a road between them, textured, wet, painted, lettered and
lit, with people on it - and it is compared against the sheet from the
sheet's own viewpoint after every change.
