# The bar for clothes: a fixed rubric (2 October 2026)

Jafar's order of 2 October, after the outside review (production/audits/2026-10-02-clothing-plan.md: "the acceptance
target is underspecified ... freeze dated clothing references and gameplay viewing distances before another review").
Every future clothing review, by me or a fresh reviewer, judges against this page and nothing else, and answers each
line below with pass or fail and the frame it saw it in. Changed only by Jafar.

## 1. How far away the game shows people (measured in play, one route walk, 2 October)

There is no separate dialogue camera: talk happens in the street camera, a spring arm 3.2 m behind Tom, 0.45 m to his
right and 0.55 m up, at the engine's default field of view, 90 degrees horizontal (about 59 vertical at 16:9)
(ue-probe/Source/LedgerProbe/Private/SliceCharacter.cpp 63-71). Measured by the builder in the route walk of
2 October, 23:30 (editor build; ue-probe/Saved/Logs, the LEDGER-ROUTE talk-open line and LedgerView lines every
5 s): the talk to Sheila opened with Tom 1.20 m from her face and **the camera 4.42 m from it**; the people in view as
he walked were, camera to face, 3.1, 4.4, 4.7, 6.0, 7.4, 8.2, 9.3, 10.8, 11.2, 15.2, 20.4, 27.7 and 28.1 m. One walk
and one talk: a first sample, to be widened with later walks.

| View | Camera to the person | At 2560 by 1440: one metre is | A jacket (0.8 m long) is | A lapel (9 cm wide) is |
|---|---|---|---|---|
| **Talk** | 4.4 m (measured) | about 290 pixels | about 230 pixels tall | about 26 pixels |
| **Street, near** | 3 to 8 m | 160 to 425 pixels | 130 to 340 pixels | 14 to 38 pixels |
| **Street, usual** | 8 to 15 m | 85 to 160 pixels | 70 to 130 pixels | 8 to 14 pixels |
| **Street, far** | 15 to 28 m | 46 to 85 pixels | 37 to 70 pixels | 4 to 8 pixels |

(One metre at distance d fills 1440 / (2 d tan 29.4°) = 1280 / d pixels.)

**What that means:** no close-up exists in play. At talk distance a jacket is about a fifth of the screen's height: its
silhouette, shoulder line, lapel shape, button stance, length, sleeve volume, cloth colour and sheen, and how it moves
all read; stitching, buttonholes, pocket welts and fine wrinkles barely do. So the rubric weighs the first group.

## 2. The references (dated photographs; links only, never copied here)

1. **John Major and George Bush at Camp David, 22 December 1990** (public domain, George Bush Presidential Library):
   https://commons.wikimedia.org/wiki/File:President_George_H._W._Bush_and_British_Prime_Minister_John_Major.jpg
   Major, full length from the front: a dark two-button single-breasted suit.
2. **Neil Kinnock in the Albert Cuyp market, Amsterdam, 5 September 1989** (CC0, Nationaal Archief / Anefo):
   https://commons.wikimedia.org/wiki/File:Wim_Kok_(PvdA)_loopt_met_de_Engelse_Labourleider_Neil_Kinnock_op_de_Albert_Cuypm,_Bestanddeelnr_934-4952.jpg
   A British suit in a crowd in daylight, at about the game's talk distance.
3. **Jennifer Pinney's retirement party, London School of Economics, December 1988** (no known restrictions, LSE
   Library): https://commons.wikimedia.org/wiki/File:Jennifer_Pinney_Retirement_Party,_December_1988_(3982883475).jpg
   Ordinary British men's suits, one seen from the side and back.
4. **The Maastricht European Council, 9 December 1991** (CC BY 4.0, European Union):
   https://commons.wikimedia.org/wiki/File:Maastricht_European_Council,_09-10-12-1991_(P-002371-06-1).jpg
   Two dozen full-length suits at about the size the street camera shows people.

What they agree on, for a man's single-breasted suit of 1987 to 1991:
- **Shoulders:** natural, lightly padded, a little wider than the body; a soft slope. Not square, not built up into
  ridges, not the narrow 2010s shoulder.
- **Lapels:** notch lapels, about 9 to 10 cm at the widest, the two the same; the notch at about the collarbone; a
  soft roll down to the top button, the lapel lying flat on the chest, never folded under or crumpled.
- **Button stance:** two buttons (three in some), the top one at the waist or just above it; the V long and open,
  shirt and tie showing well down the chest.
- **Length:** covers the seat; the hem at about the crotch; front and back hems level.
- **Body:** full in the chest, little waist shaping, the back hanging straight from the shoulder blades; the front
  falling straight, closed, from chest to hem; not a sack, not a flare, not a shelf over the belly.
- **Sleeves:** a clean tube, moderately full, ending at the wrist with a little shirt cuff showing.
- **Cloth:** matte wool in dark grey, navy or charcoal; no plastic or satin sheen.
- **With it:** a white or pale shirt collar and a tie at the neck; full trousers.

## 3. The rubric (each line pass or fail, with the frame)

**A. Cut, judged standing at talk distance, front, side and back**
1. Shoulders as above: natural, lightly padded.
2. Lapels as above: both the same, flat, a clean notch, rolling to the top button.
3. Button stance at the waist or just above; the V long.
4. Length covers the seat; front and back hems level.
5. The front falls straight and closed; no balloon, flare or shelf.
6. Sleeves a clean tube to the wrist, a little shirt cuff showing.

**B. Surface, in street light at talk and street distance**
7. Reads as matte wool at both distances; no sheen, no flat plastic grey.
8. Shirt collar and tie show at the neck; nothing of the body shows through.

**C. In motion (walking, sitting, turning, arms raised; front, side and back)**
9. No tear, hole, spike or flying piece of cloth, in any frame.
10. Nothing passes through: no body, trousers or shirt through the jacket, no jacket through the arms or legs.
11. The shape holds: the lapels stay flat, the shoulders keep their line, the skirt does not wrap the thighs walking
    or bunch into a tube sitting.

**D. Cost (on this PC's graphics card, an AMD RX 6700, the game's own frames)**
12. GPU time and video memory with the jacket on Ron and Darren together, against the same scene without: recorded.

**Verdict:** PASS when lines 1 to 11 all pass, or fail only on narrow points (small and local, not noticed at a
glance at talk distance). FAIL on any line a player would notice at a glance. Line 12 is recorded, not judged.

## 4. Screening a ready-made garment from its pictures (before anything is bought)

From the seller's own pictures, against section 2:
- **Reject** if its shoulders, button stance and length would all need rebuilding (Jafar's rule); also if its lapels
  are not notch lapels of about the period's width, or it is double-breasted when the need is single-breasted.
- **Reject** if it carries Epic's NoAI tag (it forbids use with AI tools) or a licence off the allowlist (DECISIONS.md;
  CGTrader's "Royalty Free License (no AI)" is not allowed).
- **Prefer** ready to wear on a MetaHuman (a parametric Outfit Asset or a skeletal mesh on the MetaHuman skeleton),
  with LODs and matte cloth; note the triangle count and texture size.
- The price is free or under $40 (Jafar's limit); Jafar buys.
