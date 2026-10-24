# The launderette's gate (24 October 2026)

The design (the cloud team's steam_laundry): its street review passed, its close review failed on three faults (production/cloud-week/kit/shop-windows/REVIEW-steam_laundry-v1-close.md). Each fixed to that review's exact fix on the PC before it came in:
- **The towels read as plaid cushions:** a fine soft weave at a sixth of its size and a third of its contrast, one woven border band across each towel, a terry normal map at roughness 1.0, the folded edge a half round, each towel jittered and sagging (sw_goods_b.towel_folded, towel_atlas_fine, terry_normal).
- **The washing was smooth blobs:** no scanned cloth pile exists in the free libraries (Poly Haven's 521 models searched); three cotton sheets in each basket by cloth simulation, an open box just inside the weave as their collider, its floor at 55 per cent of the basket's depth so the cloth heaps to the rim (sw_goods_b.laundry_by_cloth; the prototype's lessons in sw_cloth_proto.py).
- **BRIGHTWELL, a real firm in the laundry trade:** renamed CLAYBROOK (Companies House's first page of 38 matches and two web searches found no soap, detergent or laundry firm of that name; the second page did not load); the design's check now fails BRIGHTWELL (check_shop.py PC_BRAND_BLOCKLIST, the target not edited).
- From its narrow points: the room's floor lifted to the review's mid grey (150, 152, 150) and its tile at 1.2 m a repeat; the dado tile at Poly Haven's 1.27 m; POWDER, SOAP FLAKES and BLEACH cards each before its own good; the "1 litre" box made a powder; the display's returns 1 mm off the front's door jamb.

Built on the PC 24 October (front, display, room at 128 samples, 28 minutes), made ready (--mask=glass_row_13,glass_row_14; the box sign's faces and the fascia glowing at night; the display's linings raised and headed), keyed into the street (terrace-front.py CLOUD_FRONTS east_parade bay 4; its window has two lights, CLOUD_LIGHTS), its interiors entry dark at night as the target has it (production/specs/shop-interiors.json).

Brief: F:/LedgerTools/gate/new/launderette-2026-10-24/BRIEF.md.

## Round 1 (r1)
- **Across the road by day (r1): PASS.** The front sits clean in its bay (cornice, pilasters, pavement); fascia, box sign and glass lettering read right; the towels read as towels, the washing as cloth in baskets; nothing burns. Narrow points: the shop door's lower glass a uniform black at the display's height (the chandler's fault by day; fixed for r2 with the same flat lower panel to 0.60 m, sw_front.py PC_DOOR_KICK_MM); the left console crossing the street's downpipe by about 12 px; faint drip marks at the fascia's top edge; the washing barely over the rims.
- **Square on by day (r1): FAIL.**
  - **F1, the left basket's cream and coral sheets pass through each other:** islands of each through the other, reading as a stained rag (in a crime game, a menace misread). The settled cloth had been smoothed by a subdivision, which moved it a few millimetres.
  - **F2, the floor sheets' corners come out through the basket walls** (the basket narrows toward its foot).
  - **Fix, try 1 each:** no subdivision (the simulation's own surface, shaded smooth) and 4 mm between sheets; the coral sheet lilac; the floor sheet inset 35 mm.
  - Passed: the towels (a clear gain over the design's cushions), the card and posts, every packet's lettering (CLAYBROOK), each price card before its own good, the glass, the room. Listed: the soft white smear at a fixed height; stair-steps; plain packets and machines; the return walls a flat two-tone (the design review's narrow point 5); the towels' sides single smooth slabs up close.
