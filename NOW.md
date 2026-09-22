# NOW

THE STANDING LIST, in priority order, drawn from ROADMAP.md. Work down it.
When an item finishes, strike it and take the next without asking. The list is
kept current here; when it runs short it is extended from the next part of the
roadmap.

Last updated 2026-09-22, at the end of the second sitting on his PC.

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
- [ ] THE GAPS THE FIRST REAL FRAME SHOWS, in the order the frame says they
      matter, which is also D31's own order:
      1. NOTHING IS LIT AND NOTHING IS WET. The sheet's frame is dusk, wet,
         lamps lit; every surface here is flat overcast grey. D31 puts light
         and shadow first for this reason.
      2. THE STREET ENDS AT 42 METRES into open field. Depth beyond thirty
         metres is the named gap and the frame confirms it.
      3. NO SIGNAGE. Every fascia board on the parade is blank, and a parade
         with blank boards reads as abandoned. Four fascia decals are already
         committed and are not reaching the frame.
      4. NO CLUTTER. No lamp columns in this scene, no bins, no road markings,
         no double yellow lines - and the lines are already specified, with a
         colour taken from the game's own code.
      5. THE YARD GAP between the two west blocks reads as a black void.
      6. Surfaces are flat colour. Texture is the step after light.
- [ ] Render the pair from the sheet's viewpoint after each step. That is the
      test, and it is not optional between steps.

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
two readers of the golden table were. The street now stands as authored
fronts on both sides with a road between them, flat and unlit.
