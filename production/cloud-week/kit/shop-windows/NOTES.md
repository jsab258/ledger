# Rita's shop (unit 7, stage 1): build notes

PROGRESS LOG (kept current for a reset; the final notes replace this section)

- 13 Oct: step 0 done. 45 Poly Haven models + 2 textures fetched into /home/user/ledger-scratch/polyhaven (1k). Contact sheets looked at.
  Blanking by sw_assets.py (python sw_assets.py blank / verify): 48 of 48 INV-06 script rows pass; looked at 100 per cent beside the originals.
  New marks found at 1k that the target's list lacks (applied in sw_assets.EXTRA_BLANK): Camera_01 strap "INGRID" (a name), cardboard_box_01 print
  (incl. "Keep Out of Reach of Children"), pliers VDE/GS marks, seadogs_compass bezel "LONDON 1965 / RADOLIER".
  Looked at, kept: binoculars/vintage_binocular numerals and "6X30" print (no maker), hand_plane "MADE IN ENGLAND" and "NO 4", cross_pein "300".
  (c) The approved pawnbroker pictures at full size (2048 wide): no legible maker's name in any of the three. Seen: the till's drawer plate as a
  pale two-word smudge on a dark plate (about 30 x 5 px, letters not resolved), a red roundel dot on the cassette player, a badge on the boombox.
  "Dixons" is not legible in any of them.
- 13 Oct: front built (sw_front.py -> production/assets/cloud-week/shop-windows/ritas_front.glb 55k triangles, 11.6 MB with its textures: out of git;
  ritas_grille_night.glb 24.5k triangles). Looked at in elevation and at the doors: band above the doors, fanlight, three toplights, panel, head all present.
  Next: room (sw_room.py), display, gate, checks.
- 13 Oct (later): display built (sw_display.py: 31 pieces of 26 models, ~146k triangles, 7 MB). Room stage launched (`python build_ritas.py room`, 64 samples,
  log /home/user/ledger-scratch/shop-windows/room_stage.log); pictures go to /home/user/ledger-scratch/shop-windows/rooms/. Gate pipeline tested at low res (bake through
  trace takes seconds; renders work, day and night, lattice at night). check_ritas.py written; front rows pass. If the session resets: run `python build_ritas.py gate checks`
  once rooms/pawnbroker_*.png exist, then write the final notes (this file) and copy the pictures to production/assets/cloud-week/shop-windows/rooms/.
