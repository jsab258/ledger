# Measured against the concept portraits, 28 September

Each concept portrait (production/casting/<person>/front.jpg) and each R1 front
(this folder) was measured by eye on a 20-pixel grid. Every length is divided by
the eye-to-chin height (the pupils' line to the bottom of the chin), so the two
pictures compare whatever their size. The concept Darren is smiling, which lifts
his mouth a little.

| | Sheila concept | Sheila R1 | Darren concept | Darren R1 |
|---|---|---|---|---|
| between the pupils | 0.58 | 0.58 | 0.57 | 0.51 |
| face width at the cheekbones | 1.33 | 1.13 | 1.09 | 1.09 |
| face width at the mouth (jaw) | | | 0.94 | 1.05 |
| chin width | | | 0.45 | 0.50 |
| eyes to the base of the nose | 0.38 | 0.43 | 0.37 | 0.39 |
| eyes to the mouth | 0.61 | 0.65 | 0.58 | 0.59 |
| lip height, both lips | 0.10 | 0.17 | | |
| mouth width | 0.42 | 0.48 | | |

What it says: Sheila's face wants about 18% more width at the cheeks, a nose
about half a centimetre shorter, the mouth about 0.4 cm higher, lips about 40%
thinner and the mouth about 12% narrower. Darren's cheeks are right, but his
jaw is about 12% too wide and his chin 10% too wide, and his eyes sit close
together. His nose is a little long.

The builder turns these into landmark moves at MetaHuman's scale
(tools/ue/make_cast_metahumans.py, SHEILA_SHAPE and DARREN_SHAPE, take S1).
