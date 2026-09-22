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
- [ ] THE GAPS THE RIGHT PAIR SHOWS, re-cut 22 September against the
      approved sheet, in the order they matter. The first three are worth
      more than everything below them put together:
      1. THE FRAME IS POINTED AT THE WRONG THING. A blank windowless gable
         takes the left third of our picture and the road takes most of the
         rest; the parade is a sliver down the right edge. The sheet puts
         shopfronts across two-thirds of the frame with the near corner
         building large and detailed. Every piece of dressing built this
         week is sitting in 8 per cent of the image.
      2. VALUE. Ours is mean 74 against the sheet's 120 and its brightest
         five per cent is 163 against 229. Nothing in our frame is bright.
      3. COLOUR. Ours is grey - red, green and blue within 0.8 of a level
         of each other - against a sheet that is warm (R-B +18.5) and a
         quarter saturated. Two parts to it: the brick must come back to
         WARM RED, reversing a lightening made against the wrong sheet, and
         the shopfronts must be a PARADE OF DIFFERENT PAINTED COLOURS -
         cream, green, blue, oxblood, side by side - which is the single
         loudest thing in the reference.
      4. WHITE JOINERY. The sheet's character is white-painted sash windows
         and white shopfront frames against red brick, everywhere. Ours are
         dark. This is most of where the missing highlights are.
      5. THE YELLOWS ARE RIGHT AND TOO LOUD. The approved sheet does carry
         double yellows, so they stay; ours are the brightest thing in the
         frame where the sheet's are worn and nearly lost.
      6. NO CARS. The sheet has one parked well up the street, not three.
      7. NO CLUTTER on the pavement.
      8. THE UPPER WINDOWS ARE BARE: the spec's per-bay roller blind, bare
         pane or lit interior card is not reaching the street.
      9. THE ROOFLINE IS PLAIN: no aerials, and the stacks read thin.
     10. DEPTH BEYOND THIRTY METRES, parked. Two failed attempts are written
         into the recipe and the next one does not start from scratch.
- [ ] Render the pair from the sheet's viewpoint after each step, in DAYLIGHT
      as the sheet is. The dusk frame is a second, occasional check.

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
