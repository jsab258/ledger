# A wardrobe, not a garment: how to dress the Hook (research summary, 1 October 2026)

The question (Jafar, 1 October): LEDGER needs hundreds of people dressed true to 1990 and to who they are, from about fourteen principals down to a crowd. Every garment so far was made one at a time with free tools; simple pieces pass, every tailored garment, jackets above all, has failed blind reviews against the bar. He will pay for one month of a tool if it leaves a permanent library; no subscriptions, no hiring. Which route, ranked, and what is the first proof?

Five separate helpers each took one question, given the problem and not a theory, about thirty minutes each, reading only, with dated sources. Their notes are beside this file:
1. `1-STUDIOS-AND-CROWDS.md`: how studios dress crowds and casts, how many pieces, how they get the period right.
2. `2-PATTERNS-BY-CODE.md`: GarmentCode and every newer pattern-by-code tool.
3. `3-METAHUMAN-AND-FAB.md`: Epic's 5.8 clothing, and what Fab sells.
4. `4-MARVELOUS-MONTH.md`: Marvelous Designer as a one-month sprint.
5. `5-SCANS-AND-AI.md`: scanned libraries, and AI garments in October 2026.

This session then read the deciding sources itself (below, "Checked here"). **D** marks what a source says; **I** marks inference. Much of the web was blocked to all six of us (Fab, Marvelous Designer's own site, Epic's forums, ArtStation, most vendors), so many vendor facts are search summaries; each note says which.

## What has failed, and why it matters for the choice

From the clothing session's own records (CLOTHES.md; production/art/clothing; production/research/clothing-pipeline): the donkey jacket failed its blind reviews in every form it was made (sewn and draped as cloth, shaped from the wearer's skin, made the game way), and the MakeHuman suit jacket failed three, the last on "torn black shards where the lapel roll ends", skin through below the collar, and a shape that read as the wrong man. The fit and the skinning now hold: the suit jacket walked, raised its arms and squatted cleanly in Unreal on Ron and Darren (production/art/clothing/suit-jacket-ingame-2026-10-01). **So the failure is the tailoring itself, the cut, the collar, the lapel's roll, the layers, not the binding to the skeleton.** That rules out any route that only changes how a garment is fitted, and favours one that builds a jacket the way a tailor does: layered cloth, a pressed roll line, a stiffened front and collar.

## The routes, ranked

| | Route | Can it make a 1990 tailored jacket at the bar? | What it leaves | Cost | Verdict |
|---|---|---|---|---|---|
| **1** | **Marvelous Designer, one month, then keep what was made** | The likeliest (I): it is what Epic documents for MetaHuman outfits and what studios use for the base drape, before finishing by hand (D, notes 1, 3, 4); layered, stiffened pieces are its everyday work (I) | Patterns, draped and finished garments, exported meshes; ownership after the month is **probably** permanent but **not yet read at its source** (see below) | US$39, one month, bought privately (Personal licence) (D, note 4); a free 14-day trial first (D) | **Recommended for the tailored outerwear** |
| 2 | **Ready resizable MetaHuman outfits on Fab** | Unknown: suits, blazers, overcoats, trench coats, a cardigan, an A-line skirt and a boxy bomber exist, but no one has seen them; **nobody sells 1990 northern workwear**: no donkey jacket, car coat, anorak, shell suit, flat cap or headscarf (D/I, notes 3, 5) | A perpetual Fab Standard Licence per item, allowing "Modify and adjust" (D) | About US$20–35 an item, one at $60 (D, search summaries) | **Second: test one before buying more**; it can cover suits and women's coats only |
| 3 | **What already passes, kept for the basics** | No (every tailored attempt failed); yes for simple pieces: skirt, T-shirt, belt, handbag, spectacles (D, CLOTHES.md); Epic's free Sweater, Jeans, Boots, Flats, Oxfords recoloured by script (D, plain-1990-clothes) | Already ours | Nothing | **Keep for shirts, knitwear, skirts, footwear, accessories** |
| 4 | **The modular kit itself** (Unreal 5.8's MetaHuman Collections, or the game's own recipes) | Not a source of garments; it is how every studio multiplies a few: slots, one base garment fitted to every body type, variety from fabric, colour, wear and accessories, recipes per kind of person (D, note 1) | The town's structure | Nothing; Collections are **Experimental** in 5.8 (checked here) | **The method for the town, whatever the source** |
| 5 | **Patterns by code (GarmentCode and newer)** | **No**: GarmentCode has no jacket or coat at all, no front opening, buttons, pockets, layers or fold lines (D, checked here); its drape simulator is non-commercial (checked here); everything newer reuses its garment types or is non-commercial (D, note 2) | MIT code for simple garments | Nothing; drape on our own | **Only for simple crowd variety, later, if ever** |
| 6 | **AI garment generators** (Rodin, Meshy, Tripo, TRELLIS) | **No** (I, note 5): one fused shell with folds baked in, no lapel roll or layers, never skinned to MetaHuman; no shipped game uses AI for realistic tailored clothing (D) | Props and accessories at best | $20–40 a month, cloud; Rodin's outputs are not on the allowlist | **Props, bags, caps and textures only** |
| 7 | **Scanned clothing** | **No**: no scanned 1990 British workwear anywhere; scanned people have their clothes fused to the body; 3D Scan Store's separate garments are modern and about £236 each with a commercial licence (D, note 5) | Fabric surfaces (Megascans on Fab, Texturing XYZ) for the material library | Per item | **Fabrics only** |

Fitting tools (MetaTailor, rented; Clothy3D, free beta) solve a problem Epic's own outfit resizer already solves (D, notes 3, 5): not needed.

## How many garments (note 1)

Studios dress a crowd from a few base garments, each fitted to every body type, multiplied by material and colour, and combined by a written recipe for each kind of person: City Sample dresses a city of 35,000 from 111 pieces on six bodies; RDR2 gives each type of townsperson 2 to 13 authored outfits (D). People notice a repeated outfit before a repeated face, and look at the head and upper body (D). Applied to the Hook (I):

- **The first street (14 principals, about 30 regulars): about 40 base garments**, each fitted to the six builds: men's outerwear 6 (donkey jacket, anorak, suit jacket, cord or sports jacket, overcoat or car coat, shell-suit jacket or blouson); women's outerwear 4 (wool coat, belted mac, quilted anorak, skirt-suit jacket); shirts and knitwear 8; trousers and skirts 7; footwear 6; head and small items about 8. Then 4 to 8 fabric-and-colour variants of each from a muted 1990 palette, wear and dirt; 8 to 10 one-off pieces for principals (Agar's three-piece suit, the Widow's fur-collared coat); 1 to 3 outfits per principal, one fixed outfit per regular so the street can recognise them.
- **The town (200 to 500 on screen): about 60 to 70 base garments**, adding work clothes (fish-market whites, overalls, tabards, the cab driver's car coat), with the variety spent on the upper body and outer layer, and a cap on loud items (a red anorak, a shell suit) per scene.
- **The hard part is small:** of the forty, only about **ten are tailored outerwear**. Everything else is the kind of piece that already passes, or Epic's free set recoloured. The month of a tool is for those ten.

**Getting the period right** (note 1): every period game that got it right ran a costume process: L.A. Noire hired a film costume designer and dressed its population by scanning and "shader swapping" real costumes; KCD used historians and museums (D). The project's casting sheets and dress notes (production/research/casting/dress-and-bearing-2026-09-28.md, plain-1990-clothes) are the start of that; what is missing is a costume plan per principal and a fabric library: melton wool, gaberdine, worsted, tweed, cord, polyester slacks cloth, denim, nylon shell, machine knit.

## The recommended route (I)

**For the principals and regulars of the first street:**
1. **Prove one jacket first, in Marvelous Designer's free 14-day trial** (the proof below). Nothing is bought until it passes.
2. **If it passes, buy one month** of the Personal licence (US$39, privately, not as a company), after CLO confirms in writing that garments made in the month stay ours to use and sell after it ends (the one thing not read at its source). In the month, make the ten tailored outerwear silhouettes on Epic's four Clothing Construction Preset bodies, export each as an outfit with its pattern, fabrics and meshes, and finish them as skinned outfits in the project's existing chain (retopology over the flat pattern, folds baked, Unreal's Outfit Asset, only hems and coat tails as cloth). Ship nothing from Marvelous Designer's own library, only our own patterns (note 4).
3. **Keep the rest on today's route:** Epic's free set recoloured to the 1990 palette by script, the pieces that already pass, and simple new pieces made in Blender as now.
4. **Fab only if the proof shows a gap:** if a bought suit or women's coat would pass where ours does not, test one item (about $20–35) before buying more.

**Then the town:** fit every base garment to the six crowd builds through the Outfit Asset's sizes; build the fabric library as material layers with wear, dirt and tint; write recipes per kind of person (docker, fish-market worker, shop assistant, pensioner, young man) and test 5.8's Experimental Collections early, keeping the game's own recipe system as the fallback.

## The first proof: one jacket on two bodies, passing a blind review against the bar

- **The jacket:** a 1990 single-breasted suit jacket in charcoal wool: notch lapels of the period's width, the roll to the top button, flap pockets, a breast pocket, a centre vent, soft shoulders; shirt and tie under. Chosen because it is the garment that failed last, its reference photographs and reviewers' points already exist (production/art/clothing/suit-jacket, review 3: John Major at Camp David, 22 December 1990; Neil Kinnock, 1990), and its base serves many of the cast (Agar, Father Walsh, Danby's corduroy jacket, regulars' Sunday suits).
- **The bodies:** Ron (MH_RoccoP2) and Darren (MH_SamC5), the versions the builder exports now, named in the handover with their checksums.
- **Made the tailor's way** in the trial: our own pattern (drafted in the program, or FreeSewing's Jaeger converted by script); the fronts and collar fused, a shoulder pad, the lapel's roll line set as a fold; draped on Epic's nearest construction body and resized to each man by Unreal's Outfit Asset, which is the route the town would use.
- **Tested as the game wears it:** walking, arms raised, sitting, in the game's camera and light (the builder's tests of 1 October).
- **Judged** against the same references, the Hook sheet and the KCD2 frames, first by our own check, then by a fresh reviewer who has not seen it made. **Passes** when that reviewer fails it on narrow points only, as the gate rule says.
- **What each outcome decides:** pass, buy the month; fail on the cut or the lapel, the tool is not the cure, and before any money the method is researched again; fail only on the game's side (skin, weights), the fault is in the chain the project already owns.

## Decisions this needs (his)

1. **Money, one tool:** a free trial now, then US$39 for one month of Marvelous Designer if the jacket passes and CLO confirms ownership in writing (recommended). His brief of 1 October allows a month of a tool; DECISIONS.md of 30 September said "no Marvelous Designer" for suits and coats, so this reopens it.
2. **Money, Fab:** whether any paid Fab garment may be tested at all (30 September: "not Fab's paid ones"). Recommended: not now; only if the proof shows a gap.

## Checked here (this session, 1 October 2026)

- **GarmentCode's code is MIT** ("Copyright (c) 2024 Maria Korosteleva"): https://raw.githubusercontent.com/maria-korosteleva/GarmentCode/main/LICENSE (read).
- **Its draping simulator is non-commercial**, NVIDIA Source Code License for Warp, section 3.3: "The Work and any derivative works thereof only may be used or intended for use non-commercially… 'non-commercially' means for research or evaluation purposes only"; section 3.2 carries that to derivative works: https://raw.githubusercontent.com/maria-korosteleva/NvidiaWarp-GarmentCode/main/LICENSE.md (read).
- **NVIDIA's own Warp is Apache 2.0** today: https://raw.githubusercontent.com/NVIDIA/warp/main/LICENSE.md (read).
- **GarmentCode has no jacket or coat program:** its garment programs are bands, bodice, circle skirt, collars, godet, meta garment, pants, skirt levels, skirt paneled, sleeves and tee: https://github.com/maria-korosteleva/GarmentCode/tree/main/assets/garment_programs (read).
- **Marvelous Designer's signed-licence EULA** (PDF of 6 October 2023, text recovered from its scrambled font): on expiry "Licensee must cease all use of the Licensed Materials to which such license applies and uninstall all copies"; sections 6 to 12 of the Terms survive. **It says nothing about the licensee's own work**: that sits in the Terms at marvelousdesigner.com/terms/agreement, which is blocked here: https://flashbackj-general-storage.s3.amazonaws.com/data/clo/marvelous_designer_eula_new.pdf (read).
- **Unreal 5.8's MetaHuman Collections** are "**Experimental** … use caution when shipping with it", with Top and Bottom garment slots taking a Chaos Outfit or a skeletal mesh, and per-character "material tints": https://dev.epicgames.com/documentation/metahuman/metahuman-collections-in-unreal-engine (read).
- **Fab and Marvelous Designer's site** refused this session too (egress blocked).
- One helper's line was corrected: DINOv3 was stopped to wait for a ruling on 24 September, not stopped by one (production/research/clothing-pipeline/TRIED-2026-09-24.md).

## What could not be verified

- **Marvelous Designer's Terms**: whether garments, patterns and meshes made in a month stay ours to use and sell after it ends; the definition of "Licensed Materials"; any data or AI clause; whether work made in the free trial may be used commercially. Settled only by reading that page or a written answer from CLO.
- **Every Fab listing at source**: pictures, ratings, dates, the "Created with AI" flag, most prices, how many source bodies each outfit carries; whether any of them would pass the bar. Nothing was seen.
- **Whether Marvelous Designer's USD export reaches Unreal 5.8's Outfit Asset with its simulation mesh**, and the 5.8 faults reported on the forums (cloth lost as a wardrobe item, stretched cuffs): the trial would show.
- **How many base garments a month really yields:** 6 to 12 is the helper's estimate from thin evidence (note 4).
- **KCD2's own clothing pipeline:** no source found.
- **When players notice repeated clothes in a crowd:** no published threshold; the counts above are inference.
- **GarmentCodeData's licence** (CC BY 4.0 or CC BY-SA 4.0), and the licences of the AI pattern models' weights: not needed for the route.
- **The City Sample crowd's licence text** and the free MetaHuman Crowd Sample's clothing: not needed for the route.
