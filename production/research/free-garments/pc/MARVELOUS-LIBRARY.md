# Marvelous Designer's own garment library, seen on this PC (2 October 2026)

The cloud's research listed Marvelous's built-in trench-coat module as a lead whose licence it could not read. Both
are on this PC: the modules in C:/Users/Public/Documents/MarvelousDesigner/New Assets/Modular Library (installed with
Marvelous Designer 2026.1 Personal, files dated 20 August 2026), and the terms in C:/Program Files/Marvelous Designer
Personal/MD_Global_Terms_of_Service.PUB.txt (General Terms last updated 30 March 2026, with the "MARVELOUS DESIGNER
Additional Terms").

## What is there (seen: each module's preview picture, 500 by 500, white cloth on black)

Each garment is four modules (front body, back body, collar, sleeves), each a .zmod: a zip holding a binary pattern
block (.blo), its buttons (.btn) and the preview. Made by CLO (the file paths inside name a CLO staff account).

| Silhouette | Module set | What I saw | Close | Grade |
|---|---|---|---|---|
| M3 suit jacket, M4 sports jacket | Men / Jackets / **Simple Jacket** | Single-breasted, two buttons, notch lapel of medium width rolling to the top button, front darts, a curved front edge below the lower button, side body seams; a two-piece sleeve with four cuff buttons; a separate collar. No pockets drawn. Clean, professional drafting. | 3: the 1990 suit jacket's shape, pockets and a centre vent to add | A as a pattern |
| M5 overcoat (and W2's start) | Men / Jackets / **Raglan Trench** and **Set-In Trench** | Double-breasted trench, knee length, wide notch collar with a throat tab, epaulettes, cuff straps, a belt; raglan or set-in sleeves. A trench, not a Crombie: a single-breasted overcoat means re-cutting the front. | 2 for M5, 3 for a mac | A as a pattern |
| W4 skirt-suit jacket | Women / Jackets / **Blazer** | A fitted single-button blazer with a deep V and a shawl-like lapel, princess seams, a two-piece sleeve with buttons. Modern and slim; 1990 needs a padded shoulder and a fuller body. | 2 | A as a pattern |
| W2 belted mac | Women / Jackets / **Raglan Trench** and **Set-In Trench** | Double-breasted women's trench with a large collar, a belt and cuff straps. | 3 | A as a pattern |

Nothing in the library for M1 (donkey jacket), M2 (anorak), M6 (shell suit or blouson), W1 (wool coat) or W3 (quilted).

## The licence, as read in the installed terms

- 2.3: "'CLO Samples' means samples provided by CLO in the Licensed Materials, including, but not limited to, sample
  patterns and designs, modules for patterns and designs ... CLO Samples may be modified where such Modifications are
  permitted by the intended functionality of the Licensed Materials." The modules are CLO Samples.
- 3.3: for "the limited duration of the applicable Subscription Term for which the applicable Fees have been paid ...
  (B) to the extent any Modification contains any CLO Sample, a worldwide, royalty-free license in respect of such CLO
  Sample".
- 5.1 (f): the licensee shall not "distribute CLO Samples as Licensee's work product without substantial and original
  material Modifications, which were independently created by the Licensee and possess its own degree of creativity".
- So: usable in a sold game once substantially modified (re-cut to 1990, re-draped on our bodies, our pockets, cloth
  and finish), made under the paid month, not the trial (3.1.1, as recorded on 1 October). Not on the allowlist as
  such: it falls under Jafar's ruling that garments made with Marvelous are ours to sell (DECISIONS.md, 1 October);
  **his yes is asked before anything made from them ships**.
- **A clause that touches his CONNECT ruling**, 2.16: "'Restricted CLO Samples' means CLO Avatars, non-modifiable
  dummies ..., pre-designed clothing, trims and accessories ... included in the Licensed Materials or made available by
  CLO via CLO-SET CONNECT", and 5.1 (g): the licensee shall not "distribute Restricted CLO Samples". Whether CONNECT's
  free patterns count as "pre-designed clothing" here, or are governed by the item's own CONNECT licence, is not said;
  it is to be read on the CONNECT item pages and re-checked before release, as his ruling asks.
- CLO's avatars (the stock man used to place the proof jacket's pieces) never ship: 5.4.1 asks $3,000 an avatar or an
  attribution to disseminate one. The game ships only our MetaHuman bodies.

## Getting at them by script: not yet

No script call loads a Modular Configurator module (the 2026.1 module dump: AddBlockTypeToStyle and AddStyleToCategory
add a style to the library; nothing assembles one into the scene). ImportFile may open a dialog (research of
2 October), which would stall the bridge. Testing a module therefore needs one action in Marvelous's own window, put
to Jafar with exactly what to click, unless a safe scripted route is found first.
