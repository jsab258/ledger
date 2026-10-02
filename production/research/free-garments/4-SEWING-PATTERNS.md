# Free sewing patterns for jackets and coats, for Marvelous Designer (helper 4, 2 October 2026)

Marks: **[READ]** read at the source; **[SS]** search summary only; **[I]** my inference. About thirty minutes, read only. The shared web-search budget ran out (200 of 200) before the end, so some checks were not made (section 4).

## 1. In short

1. **Nothing free and allowlisted is clearly better at tailoring than FreeSewing's Jaeger.** The free sources split into good shapes we may not use and usable shapes that are not professional enough [I].
2. **The best new find is "Gent jacket (with tummy)".** It sits in the sample collections of Seamly2D and Valentina. It is a 36-piece Finnish bespoke draft (StindeDesign, pattern Jacket_20160914), with chest canvas, upper and under collar, a side body and a two-piece sleeve with linings. Its default figure is 180 cm tall, chest 122, waist 130 and hip 122: a heavy man with a belly, like Ron [READ]. Seamly2D exports DXF-AAMA, which Marvelous can import [READ source]. **But** its licence is only GPL-3.0, by being included in those repositories, so it needs the owner's ruling. I could not render it, so its grade comes from its list of pieces only.
3. **W.D.F. Vincent's *Cutter's Practical Guide* is public domain** (Vincent lived 1860 to 1926) [SS]. It is a professional British system covering lounges, reefers, overcoats, military greatcoats and ladies' garments, including corpulent figures [SS]. However, it is scanned drafting instructions, not pattern files: we would have to draft it ourselves, in Seamly2D for instance, and its proportions are those of 1900 [I]. archive.org is blocked here.
4. **FreeSewing's outerwear** is Jaeger, Carlton, Carlita, Devon and Jett, plus hoodies [READ]. All are MIT. Carlita (women) and Carlton (men) are the best MIT starts for W1 and M5, and Jett for M6. FreeSewing has moved to Codeberg, which is blocked here. Version 4.10.2 (13 September 2026) can still be drafted from npm, which is reachable [READ].
5. **Pattern companies' free patterns are all ruled out by their terms.** Mood Fabrics has free blazers, trenches and coats; the others checked are Peppermint, Fibre Mood, Wardrobe By Me and Style Arc. All are for personal or home use only [SS]. Those terms bind us as a contract, even though the copyright in a garment's bare shape is weak [I].
6. **No open dataset holds professional jackets.** Korosteleva's 2021 jacket templates (MIT) are crude [READ]. GarmageSet (Style3D) is NC-ND [earlier LEDGER note].
7. **Marvelous's own Modular Configurator has a Blazer set** (since version 9.5) [SS]. It is already inside the program. Whether its sample assets, and our trial licence, allow commercial use is unclear [SS]. It is worth one check by the owner [I].
8. **A US Navy peacoat study** (DTIC ADA243702) includes pattern diagrams [SS]. As a US government work it is probably public domain [I]. It was not reached.

## 2. The items

Closeness order: M1 donkey, M2 anorak, M3 suit, M4 sports, M5 overcoat or car coat, M6 shell suit or blouson, W1 wool coat, W2 mac, W3 quilted anorak, W4 skirt-suit jacket.

| # | Item and link | Author | Date | PATTERN or MESH, format | Licence (exact) and class | Sold game with modification | Credit | Grade | Closeness | Access |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | FreeSewing **Jaeger**, sport coat [2, 3] | Joost De Cock and FreeSewing contributors | npm 4.10.2, 13 Sep 2026 | PATTERN: JavaScript draft giving points and paths; SVG or PDF; to MD by points JSON and MD's API (done already) | MIT, **ALLOWED** | yes | MIT notice with any copy of the code; none needed for a drafted shape [I] | **B** (from code). It has the real pieces: chest piece, collar, collar stand, under collar, facing, side panel, two-piece sleeve. Against the bar, though: there is no lapel-width setting (the lapel falls out of collar spread and notch settings); the front is always cut away and rounded (at least 1° and a 35% hem radius); length can only grow by 25%; the sleeve-cap ease is 1% of the armhole by default [READ]. A tailored sleeve head usually takes 3 to 4 cm [I]. It failed our review | M1 0, M2 0, M3 2, M4 2, M5 1, M6 0, W1 0, W2 0, W3 0, W4 1 | [READ] code; maker notes [SS] |
| 2 | FreeSewing **Carlton**, men's long double-breasted coat (the coat from BBC's *Sherlock*) [2, 3, 5] | as above | 2018; 4.10.2 | PATTERN, as above; 20 parts: collar plus collar stand, two-piece sleeve, back half-belt, pleated tail, cuff, pocket flaps | MIT, **ALLOWED** | yes | as above | **B** (from code and makers' notes). Length runs from 35 to 100% [READ]. Makers found it too big in the armholes and sleeves, and it has no instructions [SS]. Double-breasted only [READ] | M1 1, M2 0, M3 0, M4 0, M5 2, M6 0, W1 1, W2 1, W3 0, W4 0 | [READ] code; [SS] makes |
| 3 | FreeSewing **Carlita**, women's Carlton with a side panel and bust shaping [2, 3] | as above | 4.10.2 | PATTERN, as above | MIT, **ALLOWED** | yes | as above | **B** (from code) | M1 0, M2 0, M3 0, M4 0, M5 1, M6 0, W1 2, W2 1, W3 0, W4 1 | [READ] code |
| 4 | FreeSewing **Devon**, denim trucker jacket built on Bent [2, 3] | as above | 4.10.2 | PATTERN: front and back yokes, upper and under collar, two-piece sleeve, cuff, waistband, flap pockets | MIT, **ALLOWED** | yes | as above | **B** for casual wear (from code) | M1 1, M2 0, M3 0, M4 0, M5 0, M6 1, W1 0, W2 0, W3 1, W4 0 | [READ] code |
| 5 | FreeSewing **Jett**, bomber or letterman [2, 3] | as above | 4.10.2 | PATTERN: ribbed collar, waistband and cuffs, welt pockets, back yoke, full lining, a belly adjustment | MIT, **ALLOWED** | yes | as above | **B** (from code) | M1 0, M2 1, M3 0, M4 0, M5 0, M6 2, W1 0, W2 0, W3 1, W4 0 | [READ] code |
| 6 | FreeSewing **Huey** (zip hoodie) and **Hugo** (raglan hooded jumper) [2] | as above | 4.10.2 | PATTERN | MIT, **ALLOWED** | yes | as above | **C** for outerwear: knit garments (from description) | M2 1, M6 1, all others 0 | [READ] npm listing |
| 7 | **Gent jacket (with tummy)**, `gent_jacket_with_tummy.sm2d` in Seamly2D; `Gent_Jacket_with_tummy.val` in Valentina [6, 7] | "StindeDesign" (the file's company field); added by Roman Telezhynskyi | pattern dated 14 Sep 2016; added 23 Sep 2016 | PATTERN: Seamly2D or Valentina parametric draft. 36 pieces with linings and interfacings; a proportional Finnish system with a fall-and-stand collar (2.5 and 4 cm) and a break point; measurements built into the file. To MD: open in Seamly2D (free), set five measurements, export the layout as DXF R10 or R11/12 AAMA, then use MD's File > Import > DXF (AAMA/ASTM). The DXF carries outlines, internal lines, notches and grainlines [READ source] but no seams, so the pieces are sewn again in MD [I] | No licence in the file; ships inside **GPL-3.0** repositories [READ]. Class: **RULING**, leaning **NO**: GPL is copyleft like ShareAlike, and the pattern ships inside a sold game [I] | **unclear** | GPL terms if counted as a derivative [I] | **B, possibly A** (from the list of pieces and formulas only; not seen drawn). Its structure is a real tailor's: canvas, separate under and upper collar, side body, two-piece sleeve [READ] | M1 0, M2 0, M3 2, M4 2, M5 1, M6 0, W1 0, W2 0, W3 0, W4 0 | [READ] file |
| 8 | Seamly2D sample `jacket1_52-176.sm2d`, from a 1961 Soviet system (GOST man size 52, height 176) [6, 8] | Seamly community | 1961 system; file 0.6.8 | PATTERN: 5 pieces (back, front, facing, one-piece sleeve, collar); a casual jacket | GPL-3.0 by inclusion; the book is marked "Creative Commons" on archive.org [SS], which is unverified. **RULING / NO** | unclear | as row 7 | **C** (from the file: 105 points, one-piece sleeve) | M1 1, M2 0, M3 0, M4 0, M5 0, M6 1, W1 0, W2 0, W3 0, W4 0 | [READ] file; [SS] origin |
| 9 | Valentina/Seamly2D **IMK zhaketa poluprilegayushchego silueta** (a women's semi-fitted jacket block with a two-seam sleeve) [6, 7] | not stated | file 0.2.4 | PATTERN: a block only; no collar, lapel or facing | GPL-3.0 by inclusion: **RULING / NO** | unclear | as row 7 | **C** (block only) | W1 1, W4 1, all others 0 | [READ] file |
| 10 | W.D.F. Vincent, ***The Cutter's Practical Guide***: Part 9, jackets (lounges, reefers, Norfolks; 1897 and about 1903), ladies' garments, and Part 13, British military uniforms with overcoats (1902) [18] | W.D.F. Vincent, 1860 to 1926; John Williamson Co. | 1897 to about 1903 | Not a file: scanned drafting instructions with diagrams. To MD: draft each step in Seamly2D, then export DXF-AAMA as in row 7 [I]. Part 13 is partly transcribed on Wikisource [SS] | **Public domain** (author died 1926; published before 1931) [SS for the dates; I for the status], **ALLOWED** | yes | none | **A as a system** (from description): professional British tailoring, with disproportionate (corpulent) figures treated [SS]. The proportions are 1900's, and the drafting would be our own work [I] | M1 1, M2 0, M3 2, M4 2, M5 2, M6 0, W1 1, W2 1, W3 0, W4 1 | [SS] |
| 11 | US Navy peacoat analysis, DTIC report **ADA243702**, "patterns and diagrams from p. 38" [20] | US Navy research | about 1991 [I, from the report number] | Not a file: scanned PDF diagrams [SS] | US government work: **public domain** [I, 17 USC 105], **ALLOWED** if confirmed | yes [I] | none | not seen | M1 1, M5 1, all others 0 | [SS]; DTIC blocked |
| 12 | Korosteleva 2021 garment templates `jacket.json`, `jacket_hood.json` [10] | Maria Korosteleva | code 2021; last commit 14 Jun 2024 | PATTERN: JSON panels (4-vertex sleeves; front, back, hood) | Code **MIT, ALLOWED** [READ]; dataset on Zenodo CC BY 4.0 [SS], RULING | yes (code) | MIT notice | **C** (from the JSON) | M2 1, all others 0 | [READ] |
| 13 | **Mood Fabrics** free patterns: Heywood, Zea, Nepeta and Gladiolus blazers; Lita (unisex), Ivy and Tansy trenches; Clark, Bellis and Cardoon coats [13] | Mood Fabrics | various | PATTERN: tiled PDF; would need tracing or vector conversion [I] | "© MoodFabrics.com … Mass production, resale, or distribution of this pattern in any form is strictly prohibited" [SS]. **NO** | no | n/a | not seen | From titles only: M3 2, W2 2, W4 2, W1 2 if they were allowed | [SS]; site blocked |
| 14 | Other companies' free patterns: **Peppermint** (West End jacket, robe jacket), **Fibre Mood**, **Wardrobe By Me**, **Style Arc** [14 to 17] | the companies | various | PATTERN: PDF; Wardrobe By Me's are password-protected and cannot be edited [SS] | Peppermint: "individual home use only", "cannot be used for commercial purposes of any kind" [SS]. Fibre Mood: "own limited private use" [SS]. Wardrobe By Me: "personal use only" [SS]. Style Arc: commercial use prohibited [SS]. All **NO** | no | n/a | not seen | not scored (licence NO) | [SS] |
| 15 | **Marvelous Designer's own library and Modular Configurator**, Blazer set since 9.5 [23] | CLO Virtual Fashion | 9.5 onward | PATTERN, native to MD | MD's EULA; "sample-asset licences are separate", and some samples are "educational-only" [SS]; the trial's terms were not checked. **RULING / unclear** | unclear | unknown | not seen | M3 1, W4 1 (guess from the name only) | [SS] |
| 16 | **atelier-skills**: agent skills for drafting with the Müller & Sohn system and the Russian *Atelier* magazine's men's jacket, including a prominent-belly variant, with a bridge to Valentina [11] | Andrey Granat | created 21 Sep 2026, last change 30 Sep 2026; no stars | Not a pattern: instructions in Russian for an AI to draft in Valentina | MIT [READ], but paraphrased from copyrighted books it does not ship [READ]. **unclear** | unclear | MIT notice | not applicable; unproven, 12 days old | not scored (a method) | [READ] in part |

**Skipped (6):**
- darrenstarr/Patterns: corsets and stays only, and no licence.
- Seamly2D's other jacket samples, `jacket2` to `jacket6`: GOST child sizes 40-146 and 30-110, crude.
- Olcroy: software only (a GPL Valentina fork).
- The Müller & Sohn jacket files shared on the Seamly forum: the forum is blocked and their licence is unknown.
- GarmentCodeData: it has no jackets.
- GarmageSet: CC BY-NC-ND. Both are covered in an earlier LEDGER note [24].

**Does "personal use only" stop using the pattern's shape for a game asset?**
- In practice, yes. Downloading accepts the terms, and "no commercial purposes of any kind" binds us as a contract, whatever copyright says [I].
- On copyright alone it is uncertain:
  - In the US, a garment's shape is a useful article, and a pattern's protection is thin, covering the drawings and the text [SS; I].
  - In the UK, CDPA section 51 lets anyone make "an article" to a design document without infringing copyright. A game mesh is arguably a copy of the drawing, not an article, and unregistered design right protects a garment's shape for up to 15 years [I, from memory; not checked this session].
- Treat it as **NO**.

## 3. Per silhouette

- **M1 donkey jacket:** nothing free and good enough in this area.
  - The nearest base is FreeSewing Devon (MIT): merge its front and back yokes over the shoulder, lengthen it, drop the waistband [I]. Or use Brian or Bent, as in the earlier note [24].
  - The peacoat diagrams (row 11) would help if they can be reached.
- **M2 anorak:** nothing free and good enough. Huey or Hugo (MIT) are a knit base only.
- **M3 suit jacket:**
  - The best-built free draft is **Gent jacket (with tummy)** (row 7), cut for a man with a belly. It needs the owner's ruling on GPL, and it should be drawn and judged before anyone relies on it.
  - Among MIT sources, Jaeger is still the best.
  - Vincent's lounge system (row 10) is public domain and professional, but we would have to draft it ourselves.
- **M4 cord or sports jacket:** the same three as M3. Jaeger already has patch pockets.
- **M5 overcoat or car coat:**
  - Carlton (MIT) at full length. It is double-breasted only, so a single-breasted fly front means re-cutting [I].
  - Vincent's overcoats (Parts 9 and 13) are public domain.
- **M6 shell suit or blouson:** Jett (MIT) for the blouson, with the rib collar replaced by a stand collar for a Harrington [I]. Huey for the shell-suit top.
- **W1 wool coat:** Carlita (MIT) is the best free start. Mood's coats are better matched but ruled out.
- **W2 belted mac:** nothing allowed and good enough. Carlita or Carlton is only a base, and Mood's free trenches are ruled out.
- **W3 quilted anorak:** nothing free and good enough. Jett or Devon is a base at most.
- **W4 skirt-suit jacket:** nothing free and good enough. Bases: Jaeger re-cut with FreeSewing's bust plugin, or the Russian block (row 9, GPL). Mood's blazers are ruled out.

**Against Jaeger:** no MIT or public-domain *file* is better. Row 7 looks better built, but it is GPL and unseen. Row 10 is a better *method*, but it is a book to draft from. The earlier LEDGER note held that Jaeger's failure lay as much in draping and finishing (canvas, roll line, collar layers) as in the draft [24]. Nothing found here changes that [I].

## 4. What I could not reach or verify

- **Blocked:** freesewing.eu, Codeberg (FreeSewing's home since 2025), forum.seamly.io, archive.org, Wikisource, DTIC, Marvelous Designer's site and support pages, Mood Fabrics, Zenodo, HathiTrust and Project Gutenberg. GitHub, GitLab and npm worked.
- **Gent jacket (row 7) not drawn:** there is no Seamly2D build here, so its lapel and shoulder were not seen. Who StindeDesign is, and whether they meant it to be GPL, is unknown.
- **Search budget ran out (200 of 200)**, so these were not checked:
  - Burda's and Seamwork's free-pattern terms;
  - Mitchell's systems and the 1928 *Modern Tailor Outfitter and Clothier*. Bridgland's dates are unknown, so its UK status is unknown;
  - Susan Spencer's tmtp historical drafts;
  - MD trial terms and the terms of its library assets;
  - the actual content of the DTIC peacoat report.
- **The UK points in section 2** (section 51, design right) are from memory.
- **Vincent's public-domain status** rests on his death date in a search summary (1926).

## 5. Sources (all read or searched 2 October 2026)

1. FreeSewing GitHub repository (archived; README "FreeSewing has moved to Codeberg"), last commit 2 Apr 2025. https://github.com/freesewing/freesewing [READ]
2. npm registry, @freesewing/* 4.10.2, published 13 Sep 2026. https://registry.npmjs.org/@freesewing/jaeger [READ]
3. FreeSewing source: designs jaeger, carlton, carlita, bent, brian (GitHub develop branch, Apr 2025); jett, devon, carlita 4.10.2 npm tarballs (13 Sep 2026). [READ]
4. FreeSewing Jaeger docs, instructions and "Jaeger by Roberta" showcase, undated. https://freesewing.eu/docs/designs/jaeger/ [SS; fetch blocked]
5. "FreeSewing Carlton Coat", English Girl at Home, 8 Feb 2020, https://englishgirlathome.com/2020/02/08/freesewing-carlton-coat/; showcases by Boris, Em and Charlotte, undated, https://freesewing.eu/showcase/ [SS]
6. Seamly2D repository: share/samples, src/test/CollectionTest/share, LICENSE (GPL-3.0), src/libs/vdxf (AAMA export); last commit 1 Oct 2026. https://github.com/FashionFreedom/Seamly2D [READ]
7. Valentina repository, src/app/share/collection; Gent_Jacket_with_tummy.val added 23 Sep 2016 by Roman Telezhynskyi; LICENSE_GPL.txt. https://gitlab.com/smart-pattern/valentina [READ]
8. Seamly forum: "Men Jackets and Trousers (screenshot)", https://forum.seamly.io/t/men-jackets-and-trousers-screenshot/3142; "A 1961 pattern system from archive.org", https://forum.seamly.io/t/a-1961-pattern-system-from-archive-org/7896; undated [SS; fetch blocked]
9. Seamly DXF AAMA export: forum threads 4495 and 4708, undated; "Seamly2D and Open-Source Pattern CAD", Minerva Patterns, undated, https://minervapatterns.com/blog/seamly2d-and-open-source-pattern-cad-a-practical-look [SS]
10. Garment-Pattern-Generator, Korosteleva, MIT, last commit 14 Jun 2024. https://github.com/maria-korosteleva/Garment-Pattern-Generator [READ]; dataset https://zenodo.org/records/5267549 [SS]
11. atelier-skills, Andrey Granat, MIT, 21 to 30 Sep 2026. https://gitlab.com/elgranat/atelier-skills (LICENSE, SOURCES.md, SKILL-TEST-RESULTS.md, mens-jacket.md read in part); Olcroy, https://gitlab.com/elgranat/olcroy (description read) [READ]
12. GitLab project search ("valentina pattern", "seamly", "sewing pattern", "tailoring", "jacket pattern", "freesewing"), 2 Oct 2026. [READ]
13. Mood Fabrics free patterns and the Heywood, Zea and Gladiolus blazer pages, undated. https://www.moodfabrics.com/blog/free-sewing-patterns/ [SS; fetch blocked]
14. Peppermint Sewing FAQ and Terms and Conditions, undated. https://peppermintmag.com/sewing-faq/, https://peppermintmag.com/termsandconditions/ [SS]
15. Fibre Mood terms of use, undated. https://www.fibremood.com/pages/terms-of-use [SS]
16. Wardrobe By Me terms of sale and FAQ, undated. https://wardrobebyme.com/pages/terms-and-conditions-of-sale [SS]
17. Style Arc magazine and terms (search result), undated. https://www.stylearc.com/magazine/ [SS]
18. Vincent, *Cutter's Practical Guide*: archive.org items "cutters-prac-guide-jacket-cutting" (1897), "cutters-prac-guide-cutting-jackets" (about 1903), "cutters-guide-brit.-mil.-uniforms.-1", "cutterspractical00vinc" (gives Vincent's dates 1860 to 1926); Wikisource "The Cutters' Practical Guide (1902)/Part 13"; costumes.org, 18 Jul 2020. [SS; all blocked]
19. Bridgland, *The Modern Tailor Outfitter and Clothier*, 1928 (Google Books listing). [SS]
20. DTIC ADA243702 (peacoat analysis, cited in a search summary); US Navy uniform regulation 3501.41, undated. [SS]
21. DLA Troop Support Clothing and Textiles industry support and specification requests, undated. https://www.dla.mil/Troop-Support/Clothing-and-Textiles/Industry-Support/ [SS]: patterns go to manufacturers on request, not to the public.
22. "Crown copyright", Wikipedia; National Archives, "Copyright and related rights" (2022). [SS]
23. Marvelous Designer: "Suit: Pants, Shirt, Jacket and Layering" (support); "Marvelous Designer 9.5: Blazer Modular Configurator" (YouTube); "3D Clothing Software for Commercial Work" (marvelousdesigner.com, 2026). [SS; fetch blocked]
24. Earlier LEDGER notes: production/research/wardrobe-at-scale/2-PATTERNS-BY-CODE.md (1 Oct 2026), clothing-pipeline/pattern-jacket-2026-09-29.md, MD-TAILORED-JACKET-2026-10-01.md, READY-MADE-TAILORING-2026-10-02.md. [READ]
