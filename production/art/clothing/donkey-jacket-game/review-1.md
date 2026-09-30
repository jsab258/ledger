# Ron's donkey jacket made the game way, on Ron and Darren: blind review 1 (30 September 2026)

The jacket as a game mesh (tools/meshgen/blender/retopo_garment.py: a grid on the sewn jacket's flat pattern pieces,
lifted onto the eased drape, about 21,000 triangles, the drape's detail baked, the yoke painted from its own pattern
piece), skinned by skin_garment.py, carried to Darren's body by carry_garment.py. A fresh reviewer judged it on both
men, standing (textured) and in four poses (grey), against the donkey-jacket reference notes, the V&A's T.561-1993
and both casting sheets (pictures: F:/LedgerTools/tmp/clothes/retopo/gate1).

VERDICT: PASS for Ron ("it reads as a navy donkey jacket with a black yoke, and nothing tears, pokes through or
floats"); FAIL for Darren, the second body:
1. On Darren the collar's top edge ragged and crumpled all round the neck, the top button turned edge-on; the jacket
   keeping Ron's volume below the chest (a sack, the same bulge at the back) while clinging at the chest enough to
   show his pectorals.
2. In the parts the brief excused (the skirt is cloth in Unreal, the shoulders are Unreal's): walking the forward
   thigh through the front skirt, sitting the thighs through it and the back skirt rolled under the seat, arms raised
   a ragged hole at the armpit; "no picture shows a front edge or opening below the last button. If the skirt is a
   closed tube, the cloth has to stretch round both thighs instead of parting."

Narrow: the back bellying out from the waist in side view (a donkey jacket hangs straight from the shoulder blades);
the front edge only a blurred painted strip, broken between the second and third buttons; the pockets faint painted
outlines; the collar small, rounded at the back, faceted; the yoke as matte as the wool; the wool too smooth for
melton; the sleeves following the arm's muscles where melton hangs as a tube; the jacket not riding up with the arms
raised; buttoned to the neck it hides Ron's jumper.

Right: navy with a black yoke front and back, the back yoke to armpit level with a straight lower edge, the front
yoke shallow; four dark round buttons to the neck; a turn-down collar, no lapels; the hem just below the crotch;
boxy and straight, square front corners, a hem band; sleeves to the wrist; as Ron's sheet has it.

WHAT WAS DONE (the method first): the collar's tearing was the carry moving the collar with the neck's skin rather
than with the jacket it sits on (carry_garment.py now moves pieces with the main surface, and pushes a point out of
the new body only as far as it stood off the first). The sack and the cling, and the bustle on both men, were the
drape itself, a cloth simulation that follows the body's hollows and swells where the pattern had room: melton
bridges and falls plumb, so the drape is hung before the game mesh is made (tools/meshgen/blender/hang_drape.py:
below the chest each slice falls straight from the body's widest point with an even 3 cm ease, the sleeves rounded
into tubes), and Darren's jacket is now made from the drape carried and hung on his own body, not from Ron's game
mesh. The front opens below the last button (the fronts part over the thighs; each half leans to its own thigh). The
front edge is painted as one line of the overlapping front; the pockets' outlines are found texel by texel and
raised with a shadow line; the yoke has a roughness of its own; the wool a felted grain. Second review: review-2.md.
