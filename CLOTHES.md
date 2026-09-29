# Clothes: the clothing session's list

The third session (Jafar, 29 September): clothes for the people of a British port town in 1990, made in Blender only, in C:\Users\Jafar\ledger-clothes on the branch clothes, pushed to main. Bodies come from the builder in F:\LedgerTools\bodies ("Handovers to clothing" in NOW.md); finished garments go to F:\LedgerTools\garments with a line under Handovers in NOW.md. Worked in order; when an item is done, take the next.

## The list, in order (Jafar, 29 September)

- [x] 1. Research the sleeve problem first, and read the builder's jacket records so you do not repeat what failed. DONE 29 September: the helper's note (production/research/clothing-pipeline/SLEEVES-RECIPE-2026-09-29.md: weld the seams once stitched, sewing force unlimited, the wrapped pieces as the rest shape) and my own finding in it: the pattern was cut for the wrong body (Ron's armpit measured 15 cm under his shoulder in the raised-arm pose; it is 22), which gave a shirt's armhole and a 4 cm sleeve cap; the measuring is fixed and the pattern redrafted (production/art/clothing/donkey-jacket-sewn).
- [ ] 2. The donkey jacket on Ron's body, through the gate, handed to the builder.
- [ ] 3. The same jacket for the slim, average and heavy builds.
- [ ] 4. Proper work trousers and a flat cap from FreeSewing's patterns.
- [ ] 5. Sheila's clothes, from her casting sheet.
- [ ] 6. Then the clothes on each principal's casting sheet, in order.

## Status

- 29 September: item 1 done; item 2 in hand (tools/meshgen/blender/sew_donkey.py and tailor.py: the new pattern placed round Ron with every seam shut and nothing inside him, now sewing).
- Bodies: Ron, Darren and Sheila are READY in F:\LedgerTools\bodies; the slim, average and heavy builds are NOT READY (the builder's line), so item 3 waits for its word.
- The jacket's standing: Jafar's ruling of 29 September allows one more sleeve attempt, capped at one day, which the builder began (about two hours; the back armholes still opened 24 cm) and handed over; this session finishes it inside the rest of that day; if it fails, find out whether Marvelous Designer can be driven entirely by its own scripting and bring it to him as a decision; buy nothing.
- Tools: the jacket scripts run in Blender 4.5.13 (the rest-shape-key workaround was proved there); the live Blender 5.2.2 connection is registered but Blender is not running (tools/blender-live/start-blender-live.ps1 starts it); cloth on the processor, renders short, scratch on F:.
- Disk and pushes: C: 34 GB free (the builder's cleanup page, waiting on him), F: 31 GB; nothing large goes on C:. Blender scripts and these records set off nothing on push; records under production/ run the free Core tests; production/specs and production/assets would start the Unreal build on the build machine, so garments never go there.
