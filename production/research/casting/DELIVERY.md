# Casting the Hook: the 1991 census, how people looked, and a plan that starts from both

STATUS: SPEC (research delivery). Branch `research/casting`. Written
2026-09-24. Audited against `BRIEF.md`, which was written and committed first,
and against Jafar's correction of the same day: "names are not constraints …
fit the names to the town", and "I decide; you propose".

NOTHING HERE IS AN INSTRUCTION. Nothing was generated, cast or downloaded.
Every rename below is a proposal. So is every age and background, and so is
every voice route, and each of those routes needs his ruling.

Labels: CITED (a page opened), CITED-SUMMARY (a search result only), DERIVED,
ASSUMED, HOLE. DATA (a survey or census figure) and OBSERVATION (from
photographs or fashion history) say what kind of evidence a CITED figure is.

## 0. Sourcing

Seven helpers researched in parallel on 2026-09-24:
- the census
- how people looked
- building a MetaHuman from a portrait
- crowds
- the rules on real people, stereotypes and children
- voices, added when the project's own records showed the cast voices are all
  21 to 38
- period names, added after Jafar's correction

Their full records are in `notes/`, where every fact carries its link, its
date, and whether the page was opened. This document cites what the plan rests
on, and for everything else `notes/` is the source list. All pages were read
through a fetch tool that returns a model-written summary. The census figures
are the exception: they were read from the official tables through the Nomis
API.

## 1. Who lived there: the 1991 census for Hull and Great Grimsby

CITED, DATA: the official 1991 Census tables (Local Base Statistics and the
simplified tables) read from Nomis on 2026-09-24. Census day was 21 April 1991.
Full tables and cell references are in `notes/census.md`.

- **Population:** Hull 254,117 and Great Grimsby 90,517. There were 94 men to
  100 women. At 65 and over, about 153 women to 100 men; at 75 and over, about
  206.
- **Ethnic group:** 1.25% of Hull and 0.98% of Grimsby were not White. For
  comparison: Liverpool 3.8%, Middlesbrough 4.4%, England 6.2%.
  - Hull's largest group was Chinese (537 people), mostly from Hong Kong.
  - Grimsby's was Indian (188), ahead of Chinese (117).
- **Born outside the UK:** 2.3% and 2.7%, against about 10% for England.
  Europe outside the UK and Ireland was at most 0.6%. No separate count exists
  for the Polish, Baltic or Scandinavian settlers.
- **Households:**
  - Hull: 37% rented from the council, 51% had no car, 29% lived alone, and 16%
    were a pensioner living alone.
  - Grimsby: 20% rented from the council and 44% had no car, close to the
    English average.
- **Work:**
  - Unemployment in April 1991 was 15.3% (Hull) and 13.5% (Grimsby), and
    18.8% and 17.0% for men. Scaled back to 1990 by the claimant count: about
    11.8% and 11.1% (DERIVED).
  - In Hull, about as many women worked part-time as full-time.
  - Fishing was about 0.9% of working residents in both towns.
  - Grimsby had twice Hull's share in "other manufacturing" (20.4% against
    10.1%), consistent with fish and frozen-food processing.
- **The trades that shaped the town:**
  - **Hull's fishing, CITED:** at its height about 8,000 trawlermen and 320
    trawlers, with three times as many ashore in fish. Hull's main fish dock
    closed in 1975.
  - **Docks, CITED:** 9,400 registered dockers nationally in April 1989. The
    dock labour scheme ended in July 1989. Grimsby and Immingham lost 498 dock
    jobs in 1989.

**The casting table, DERIVED from the census: adults 16 and over, Hull and
Grimsby together, 268,387 people.**

| | | share |
|---|---|---|
| Age | 16-29 / 30-44 / 45-59 / 60-74 / 75+ | 28.6% / 25.8% / 19.2% / 17.9% / 8.5% |
| Sex | men / women (60-74: 54% women; 75+: 67% women) | 47.6% / 52.4% |
| Ethnic group (all ages) | White / Chinese / Black / South Asian / Other | 98.8% / 0.19% / 0.31% / 0.32% / 0.37% |
| Birthplace | outside the UK / Scotland or Wales | 2.4% (Ireland 0.31%, rest of Europe 0.57%) / 1.9% |
| What adults did | in work / retired / keeping house / unemployed (use about 7% for 1990) / permanently sick / student / training scheme | 48.4% / 18.8% / 14.3% / 8.7% / 4.7% / 3.8% / 1.3% |
| Of adults, working in | market, shops, pubs, catering / manufacturing and industry (fish and food processing about 3-5% in a Grimsby-like town, ESTIMATE) / council, health, schools, police / docks, shipping, road, rail, post (docks alone under 1%, ESTIMATE) / banks and offices / fishing | 11.4% / 16.6% / 12.7% / 3.8% / 3.1% / 0.4% |
| Overlay | clerical and secretarial | about 6.7% of adults |

HOLES:
- No count of Hull's dockers.
- Fish processing is not separable from other manufacturing.
- Minority shares are for all ages. Minority groups were younger, so their
  share among adults is slightly lower.
- One quirk to know about: the Nomis simplified industry and occupation tables
  carry each other's labels. The full tables were used.

## 2. How working people looked, c.1990

Full record: `notes/looks.md`. DATA where a survey exists; the rest is
OBSERVATION and says so.

**DATA:**
- **Smoking:** 30% of adults in Great Britain smoked in 1990 (ONS), against
  20% in 2011. Hand-rolled tobacco was mainly smoked by 18% of male smokers.
- **No natural teeth, England 1988** (Adult Dental Health Survey):
  - all adults 20%, against 6% in 2009
  - 45-54: 15%
  - 55-64: 35%
  - over 65: about two thirds
  - The north was among the worst regions.
- **Height, 1993** (Health Survey for England): men 174.4 cm, women 161.1 cm.
- **Obesity:** men 13% and women 16% in 1993, against about 30% of adults
  now.
- **Tattoos:** 7% of people born before 1950 had one (2015 survey).
- **Glasses:** NHS frames ended in 1985-86. The old NHS plastic came in flesh
  pink, brown mottle and crystal.

**OBSERVATION and ESTIMATE (fashion history, and Tom Wood's Liverpool market
photographs; not a survey):**
- Moustaches on about 25-35% of men aged 35-60, untrimmed. Full beards under
  5%. Men under 30 mostly clean-shaven.
- About half of women over 45 with a perm or a shampoo-and-set, and headscarves
  on the oldest.
- Younger women: bleached or highlighted hair with volume and a fringe.
- Men: short back and sides, side partings, receding hair left as it is. Some
  mullets and grown-out perms at 25-40.
- Tattoos on about 15-25% of working men aged 30-60 in a fishing port,
  blue-black and blurred, on forearms and hands. Almost none on women.
- Glasses on about 30-40% of adults: large lenses, gold aviator or NHS-style
  plastic.
- Among working men 30-60 in a northern port, about 40-50% smokers, with
  yellow fingertips, stained teeth and lined lips.

**1990 against today, at a glance:**
1. Faces mostly shaved, and nothing groomed.
2. One adult in seven obese, not one in three. The middle-aged man has thin
   limbs and a belly.
3. Dentures and gaps past 45, grey fillings, nothing whitened.
4. Smokers' fingers, teeth and lips.
5. Perms and sets from 40 up.
6. Big glasses.
7. Tattoos only on seafarers and hard men, faded.
8. Ears the only piercings.
9. Coloured eyeshadow and frosted lipstick, natural brows, no lash extensions,
   fake tan or filler.
10. Weathered, ruddy outdoor faces, sallow smokers' faces.
11. Shorter, and the old visibly shorter still. People look older for their
    age.
12. Gold sovereign rings, chains and hoops.

HOLE:
- The period photograph archives yielded almost nothing about faces. Peter
  Marshall's Hull work is streets and buildings.
- The best lead is Historic England's trawlermen slides (collection FIS01).
  It returned an access error and needs opening by hand.
- The photographs are LINKS only, by the project's rule. They may be looked at
  to judge a render, and never fed to a generator.

## 3. Building a MetaHuman to match an approved portrait

Full record: `notes/metahuman.md`.

**What Unreal accepts (DOCUMENTATION):**
- There is **no official photo-to-MetaHuman route** in 5.6, 5.7 or 5.8.
- What the tools do accept:
  - presets, blended and sculpted;
  - DNA files;
  - a mesh in MetaHuman's own topology;
  - a **mesh of any topology**: 5.8's "From Custom Mesh" fits head and body in
    one step, and names outside AI-generated meshes as an intended input, but
    does not carry the texture across;
  - footage **with depth**, from an iPhone TrueDepth camera or a stereo rig.
    That cannot take a generated portrait.
- A script in 5.8 can **read and set the whole face-shape vector**
  (`Get/SetFaceModelCoefficients`).
- Skin comes from tone and texture settings, or from our own texture maps.
- Auto-rig and texture synthesis are cloud services. A thread from 3 August
  2026 reports them failing on a 300-second timeout outside the US.
- Nothing is NVIDIA-only. Epic recommends an RX 6800 XT or better, and our RX
  6700 is just below it.

**How close a match gets:** HOLE, measured nowhere. There are no landmark or
recognition scores anywhere. Qualitative reports, all from before 5.6: faces
come out "vaguely similar" and drift toward the template at the ears, eyes,
nose and mouth. Age, wrinkles and complexion come from the skin, not from the
fit.

**Third-party tools:**
- Usable:
  - KeenTools FaceBuilder for Blender: several views, exports a
    MetaHuman-layout texture, $16-20 a month, 15-day trial.
  - MetahumanModeler: $59, low accuracy.
  - Reallusion Headshot 3.1 with Character Creator 5: $500 together.
- Excluded:
  - Hunyuan3D: its licence excludes the EU and the UK.
  - FaceLift, DECA/EMOCA/SMIRK and PanoHead: non-commercial.
  - TRELLIS.2: CUDA only, and not made for heads.

**What our image lane can feed it:** the local generator runs Qwen-Image-Edit
(Apache 2.0), which takes a reference image. It can make three-quarter and
profile views from the approved front portrait: neutral expression, even
light, hair off the face, no glasses. PuLID, InstantID and PhotoMaker depend
on non-commercial face models, so they are out. The MetaHuman licence forbids
training a model on MetaHuman renders.

**The practical route (DERIVED):**
1. Free: start from the nearest preset. Script the face-shape vector against
   the approved portrait: render at the same framing, compare, adjust, repeat.
   Set the skin for age and life.
2. If the likeness falls short: make the three views with Qwen-Image-Edit,
   build the head in FaceBuilder on its trial, fit it with "From Custom Mesh",
   rig it in the cloud, and apply FaceBuilder's texture. A subscription beyond
   the trial is money, so it is Jafar's call.

## 4. A crowd of hundreds without clones

Full record: `notes/crowd.md`.

**What people notice (MEASURED):**
- Clone Attack!, 2008: people spot a repeated outfit before a repeated face.
  Recolouring clothes doubled the time to spot a clone (5.7 s to 12.3 s).
- A repeated walk hides when the loops start out of step.
- Eye-tracking (2009): people look at the head and upper body, almost never
  at the legs.

**What shipped:**
- **Hitman: Absolution:** 500 people on screen on a PS3. Each was scaled at
  random by ±5%, clothing colours were swapped, and walk loops started at
  random points.
- **Assassin's Creed Unity:** at most 40 fully detailed people. 2,000 people
  in 230 MB.
- **Epic's City Sample:** 35,000 people from 12 heads and 6 bodies, about 10
  hairstyles, 63 tops, 33 trousers or skirts, 15 pairs of shoes and 16 skin
  tones. The clothes are modern, so only the method carries over.
- **Unreal 5.8's MetaHuman crowd tool (experimental):** full MetaHumans close
  up and lighter ones beyond. Epic's example is 10 up close and hundreds in
  the distance. There is one open report of a memory leak.
- **Cost, measured by users:**
  - hair for 50 MetaHumans took about 800 MB;
  - turning off body corrections at distance gave about 40% more frames per
    second;
  - the animation budget defaults to 1 ms.

**Recipe for 200-500 on screen (DERIVED from the above):**
- **Close up:** 10-20 full MetaHumans nearest the camera; everyone else from
  the crowd tool.
- **Faces:** 12-16, older than City Sample's set.
- **Bodies:** 6, each person scaled ±5%.
- **Hair and skin:** 10-12 card hairstyles plus moustaches, a hair-colour
  setting, and 12-16 skin tones.
- **Clothes, top half first:** about 30 tops and jackets in 6-12 period colours
  each, 15 trousers or skirts, and 8 pairs of shoes.
- **Accessories:** about 10 for the head (flat cap, woolly hat, headscarf,
  glasses) and about 10 for the hands (carrier bag, newspaper, cigarette,
  umbrella).
- **Movement:** 6-10 walks by sex and age, started at random points, speed
  varied ±10%.
- **Routes:** from each person's routine, so people don't share paths.
- **Loud items:** the risk is a few of them repeating, so cap them per scene.

## 5. The rules, and how the plan keeps them

Full record: `notes/rules.md`. Not legal advice.

**No children anywhere (canon D18).**
- The test that matters everywhere is *apparent* age.
- The plan's floor:
  - every brief says at least 25, except crowd faces at 21 or more that read
    unmistakably adult;
  - adult proportions, a defined jaw and neck, skin texture;
  - no small figures and no child props;
  - no young-sounding voices.
- An apparent-age test before any face is accepted: portraits and crowd frames
  are shown without names to a few people, and anyone guessed under 21 is
  recast.
- The main sitting's AI tester already took Lena for a child because she stood
  short beside Tom. Height and proportion are part of this test.

**No recognisable real people.**
- The legal test in the UK, the US and Switzerland is recognisability (Swiss
  ZGB Art. 28 covers ordinary people's image and voice too).
- Voices count: Midler v Ford, and the 2025 SAG-AFTRA games agreement.
- Generated faces can reproduce often-seen faces (Carlini et al. 2023).
- The plan's checks:
  - never a real name, celebrity or "style of" in a prompt;
  - record every prompt and seed;
  - reverse image search (Google Lens, TinEye) on every approved portrait and
    final render, plus a "who does this remind you of?" look;
  - a "who does this sound like?" listen for every voice;
  - no face-recognition services such as PimEyes or Clearview, which carry
    their own legal risk;
  - anyone scanned or used as a reference signs a release;
  - names checked against obvious public figures, which is why one proposal
    below avoids Janet Ellis.

**Avoiding stereotypes.**
- Evidence first:
  - the town was 98.8% White, and its minorities were real communities with
    histories;
  - erasing them is inaccurate;
  - forced diversity reads as "preachy" in period drama, to viewers of colour
    as strongly as to white viewers (BBC review, January 2026);
  - older women are the most missing group in games (94% of over-50 characters
    in 2023's best-sellers were men).
- The plan therefore:
  - places each minority character inside a family or community the evidence
    supports, never alone as a token;
  - applies the Riz Test to any Muslim character;
  - puts older women among the principals;
  - writes working people as competent, with inner lives, not flat caps and
    whippets;
  - keeps racism as a fact about characters, with consequences and never a
    reward (canon D18);
  - commissions a paid sensitivity read per community depicted.

## 6. Voices: why they do not match, and the routes

- CITED, from the project's own records (the 24 September voice-permissions
  record and the 31 July voice casting):
  - All 23 cast voices come from the VCTK corpus, whose speakers are 21 to 38.
    **Lena is voiced by a 22-year-old (p228).** Rocco's is the oldest voice
    VCTK holds, 38.
  - The accents are English (unspecified), Scottish, Irish and Northern Irish.
    None is from Humberside.
- CITED, MEASURED (arXiv 2607.23027, July 2026): Chatterbox zero-shot cloning
  "preserve[s] speaker timbre but flatten[s] the accent". Accent similarity
  rose from 0.51 to 0.64 with fine-tuning.
- The routes (full record: `notes/voices.md`), cheapest first:
  1. Older Yorkshire and northern volunteers from Mozilla Common Voice (CC0).
     About 15% of the British English subset is over 50, but only 204 clips are
     tagged Yorkshire. The volunteers' consent is worded for recognition, not
     synthesis.
  2. Fine-tune Chatterbox on Google's SLR83 northern English set. It has
     studio quality and signed releases "with no restriction on … commercial
     … use", but only 19 northern speakers, no ages, and the question of
     whether CC BY-SA reaches generated audio.
  3. Record three or four older Hull or Grimsby locals under a written
     synthesis consent, modelled on Equity's AI toolkit and the SAG-AFTRA
     clauses. The Equity game minimum is reported at £300 an hour
     (CITED-SUMMARY).
- Each route needs a ruling:
  - Route 3 needs the allowlist to admit consenting hired people.
  - Route 2 needs CC BY-SA accepted for reference audio.
  - Route 1 needs Common Voice's wording accepted inside the "stated risk"
    ruling of 24 September.
- No voice is cast without his yes.

## 7. The proposed casting plan

### 7.1 The town's mix, as the plan uses it

Every tier is drawn from the casting table in section 1 unless a line below
says otherwise. For a crowd, the census sets the **spawn weights**, not the
face count. A face that stands for 1% of the town is placed 1% of the time,
however many faces exist.

### 7.2 How many people in each tier

| tier | how many | face | body | voice |
|---|---|---|---|---|
| **1. Principals**: the canon roles | 14 living, and Mickey in a photograph | its own face, built to an approved portrait (section 3) | its own, from the six base bodies with personal proportions | its own, cast by age and accent (section 6) |
| **2. Street regulars**: the named people of Quay Street | about 30 | 1 of the 12-16 crowd faces, individualised by skin, hair and glasses | from the six | from a pool of 8-10 regular voices, reused across the regulars by age and sex |
| **3. The crowd** | 200-500 on screen | 12-16 faces | 6 bodies ±5% | the barks pool: 3 men and 3 women today, rebalanced toward older voices |

**The 30 regulars, from the census (DERIVED; the numbers are the census
shares rounded to 30):**
- **Age:** 8 aged 20s, 8 in their 30s and early 40s, 6 aged 45-59, 5 aged
  60-74 (3 of them women), 3 aged 75 and over (2 women).
- **Sex:** 14 men, 16 women.
- **What they do:**
  - 4 cab drivers and a dispatcher;
  - 5 fish market and fish-processing workers;
  - 6 shopkeepers and shop or café staff;
  - 2 office workers;
  - 2 dock or shipping men;
  - 5 retired;
  - 3 who keep house;
  - 2 out of work.
- **Minority families:** one Hong Kong Chinese family running the parade's
  takeaway, 2 people.
  - That is more than 1.25% of 30. The plan chooses a family over a lone
    token, because the evidence is that minorities there were communities. It
    is the most evidence-backed community (Hull's largest minority group).
  - The Italian-descended café family (Hull's Penna ice-cream family, since
    1889, gave its children English first names under the Italian surname)
    counts among the White majority, and fits.

**The 12-16 crowd faces (DERIVED):**
- **Women (8):** about 23, 33, 41, 49, 57, 65, 72, 80.
- **Men (8):** about 24, 32, 40, 48, 56, 63, 70, 77.
- **One of the sixteen is East Asian and one South Asian**, each placed about
  1 time in 150. That keeps the street near the census 0.19% and 0.32% while
  never making anyone the only one of their kind for long.
- **Looks:** each face gets the section 2 period traits in the census
  proportions, applied as settings. Moustaches on about a third of men 35-60.
  Perm or set on about half of women over 45. Glasses on about a third.
  Smokers' marks on about 4 in 10 working men.

### 7.3 The principals: a name, an age, a background and a look, fitted to the town

Names follow `notes/names.md`:
- First names from the official England and Wales lists for each person's
  birth decade.
- Surnames from Hull's 1990 phone book and from the 1890 survey of East Riding
  and Lincolnshire names. The Yorkshire textile-town names (Sykes, Haigh,
  Hirst) are avoided.

"Keep" or "change" is a proposal each time. **Touches** counts the files in
the game's code, content and tools that use the name today, from a search of
the repository on 2026-09-24. It also names the other decisions a rename
would reach.

| role (canon) | today | proposed | age, background | the look | keep or change, and why | touches |
|---|---|---|---|---|---|---|
| the late owner | Mickey | **keep "Mickey's"**: Michael "Mickey" Suddaby, born 1924, died 1990 | Hessle Road born; a trawlerman until the fleet went, then the cab office | a framed photograph: flat cap, moustache | Shops named for their owner's first name were how Hull did it (Brenda's Cafe, 1981). Michael was in use in the 1920s, though not among the top names (the 1924 list's top is Arthur, Albert, Frederick); "Mickey" is the nickname, and the name is kept for what it touches rather than because it is typical. The surname is local East Riding colour. | **Mickey is lettered on the fascia and in the Hook sheet's prompts**: 73 code or content files, 34 art or reference files. Keeping it touches nothing. |
| the player | Tom Novak | **Tom Nowak**, 32 (born 1958) | Son of a Polish post-war settler and Mickey's sister. The family moved away when he was small, as most Hull landing families did, so he is a stranger to the Hook. | 1990 at 32: short hair, clean-shaven, no tattoos | **Change one letter.** The evidence's typical case is a foreign-born man who married a local woman, and whose children had English first names and his surname (Nowak is on the evidence's list). That makes Tom's surname real, and his tie to Mickey legible. Tom stays: Thomas was in use for 1950s births, though not among the top twelve. | 27 code files. **The standing ladder** (the new owner, then Novak, then Tom, then Toma) needs its last rung reconsidered: in Hull the intimate form would be **Tommy**. |
| the bookkeeper | Lena Moreau | **Sheila Dunn**, 53 (born 1937) | Started at Mickey's at 22, thirty-one years ago. A widow, in a council flat. | Grey-brown shampoo-and-set, large glasses on a chain, cardigan, no make-up but lipstick, smoker's lines, dentures | **Change.** Lena was an Edwardian name, and Moreau is French with no tie to the town. Sheila was a top name of the mid-1930s; Dunn is a surname the 1890 survey ties to Hull. | 51 code files. **The cast MetaHuman "Lena" (from Grace), her voice id and her card.** Her voice has to be recast anyway: it is 22. |
| Mickey's doorman | Rocco | **Ron Kirby**, 58 (born 1932) | A docker until the labour scheme ended in 1989. Mickey kept him on the door and the rank. | Big, heavy-set, bald, full moustache, tattooed forearms, donkey jacket | **Change.** A Hull-born Italian descendant would usually carry an English first name (the evidence's Penna pattern). Ronald was a top 1930s name; Kirby is tied to Hull. | 51 code files. **The cast MetaHuman "Rocco" (from Jorge) and his voice.** |
| the street hustler | Sam | **Darren Milner**, 25 (born 1965) | Out of work since a YTS scheme, lives at his mother's, pager and phone boxes | Bleached-tip grown-out perm, shell suit or bomber jacket, thin | **Change.** Samuel was rare in the 1960s. Darren was a top mid-60s name; Milner is tied to Hull. | 47 code files. **The cast MetaHuman "Sam" (from Orlando).** His voice is Scottish (p241), which a local man would not be. |
| the detective | Mara Ellis | **DS Carol Ellis**, 40 (born 1950) | Humberside CID, one of few women detectives then (HOLE: the share of women in CID in 1990 was not sourced) | Feathered bob, blazer, minimal make-up | **Keep Ellis; change Mara.** Mara was not in use. Carol was a top name c.1950. Janet was set aside as a well-known name. | 8 code files for Mara; Ellis stays. |
| head of the old-money machine | Aldous Vane | **Geoffrey Agar**, 62 (born 1928) | Solicitor and alderman, from a timber-merchant family | Silver hair swept back, rimless glasses, three-piece suit | **Change.** Aldous is literary and was not in use. Vane is an aristocratic name elsewhere. Geoffrey fits his class and decade; Agar is East Riding. | 6 + 12 code files. **His voice (p226) is also outside the 31 July ruling.** |
| head of the dockside syndicate | Sera Kest, "the Widow" | **Maureen Jensen, "the Widow"**, 57 (born 1933) | Trawler-owner's widow from a Hessle Road fishing family (Jensen is on the evidence's list of fishing-family names) | Blonde set, heavy gold, fur-collared coat, hard face | **Change the name; keep the nickname.** Sera Kest was invented. Maureen was a top 1930s name. | 12 code files each. **The game's id `sera` points at the Kest voice.** |
| head of the new crew | Danny Ro | **Danny Cammack**, 27 (born 1963) | Grimsby-side, loud money | Mullet, gold chain, leather blouson | **Keep Danny; change Ro.** Ro is not a name; Cammack is Lincolnshire. | 9 code files for Danny. |
| the old woman of the street | Ada | **keep Ada**, 78 (born 1912) | Widow, keeps a window on Quay Street | Headscarf, hunched, dentures | **Keep, and make her old.** Ada belongs to the Edwardian lists (ASSUMED: the 1904 list was not read here). | none |
| Mickey's estranged daughter | June | **keep June**, 38 (born 1952); surname Suddaby | Left the Hook young, back for the funeral | Highlights, shoulder pads | **Keep, provisionally.** June was a top name c.1934; for a 1952 birth it is less typical (HOLE: the 1954 list's top names are Susan, Linda, Christine). A ruling either way costs little. | 9 code files |
| the priest | Father Emil | **Father Brendan Walsh**, 61; or keep Emil as the Polish mission's priest | Irish-born parish priest (ASSUMED: many English Catholic priests of that generation were Irish-born, unsourced here); or the priest of Hull's Polish community, who would have known Tom's father | Black suit and collar, thinning grey hair | **Change, or keep with a reason.** Emil fits only a Polish congregation, which is unsourced for Hull. Keeping it would tie Tom's father to the church. | 10 code files |
| the journalist | Noor | **Alison Sedman**, 30 (born 1960), a Hull Daily Mail reporter | Local, grammar school, the first of her family at college | Big permed hair, big glasses, a notebook | **Change.** A South Asian woman reporter in 1990s Hull is possible and rare (0.32% South Asian, all ages). A lone one would be the token the rules warn against. The plan's grounded minorities are elsewhere (7.2). Sedman is East Riding. | 11 code files |
| the teacher | Elias | **Philip Danby**, 33 (born 1957) | Teaches at the comprehensive, which stands closed for the game's window (canon) | Side parting, knitted tie, corduroy jacket | **Change.** Elias was not in use for English boys of the 1950s. | none in code |
| the Fixer | (no name) | **Keith Garbutt**, 48 (born 1942) | Brokers between all three | Neat moustache, car coat | Proposed name only | none |

**The other street voices named in the game** (Vesna, Zlata, Marla, Joey,
Rita, Hal, Tobias Reese) are regulars in tier 2:
- **Change Vesna and Zlata:** there is no evidence of Yugoslav families in
  Hull. If a Baltic or Ukrainian settler family is wanted, use the evidence's
  names for a woman of about 65.
- **Keep Rita** (a top name of the mid-1930s) and **Hal** (as Harold, 70 or
  more).
- **Change Marla and Joey** to names of their birth decades.
- **Tobias Reese** of Customs and Excise: keep Reese, change Tobias.

What else these touch: 10 to 23 code files each, and their six crowd voices'
2,010 pre-rendered barks, which are by voice, not by name.

### 7.4 What this reaches, for Jafar to weigh

- **Keeping "Mickey's" leaves the fascia, the Hook sheet and 107 files
  alone.** It is the costliest name to change, and the evidence supports it.
- **Renaming Lena, Rocco and Sam** touches the three cast MetaHumans made
  today from Grace, Jorge and Orlando, their cards, their voice ids, and about
  50 code files each. Their faces and voices are being recast in any case.
- **Tom's surname** reaches the standing ladder.
- **Every rename touches `canon.md`**, which only Jafar changes.
- **A place-name note, out of this brief's scope:** Meridian, the Hook and
  Quay Street were also chosen without research. They are 34, 41 and 17 code
  files, and 35, 25 and 31 art files. The Hook and Quay Street are ordinary for
  a northern port; Meridian is not a name a Humberside town would have. Not
  proposed here.

### 7.5 The order of work, once he rules

1. **Portraits for the principals:**
   - a brief each: age at least 25, not based on anyone;
   - the image lane;
   - his approval;
   - a reverse image search;
   - the apparent-age test.
2. **Faces:** the free preset-and-script fit (section 3), then the paid route
   only if it falls short.
3. **Voices:** the route he rules on (section 6), each voice with his yes.
4. **The crowd:** 16 faces and 6 bodies, and the variation kit of section 4,
   weighted by section 7.2.

## 8. What could not be sourced

1. **How many dockers Hull had in 1990**, and fish processing apart from other
   manufacturing.
2. **Separate counts for the Polish, Ukrainian, Baltic, Italian, Irish and
   Scandinavian communities** in either town.
3. **Any survey of hair, facial hair, glasses or make-up in 1990.** Section 2
   marks those as observation.
4. **Faces in the period photograph archives.** The trawlermen slides need
   opening by hand.
5. **Any measured likeness for a MetaHuman fitted to a portrait.**
6. **A regional (Yorkshire and Humberside) first-name list**, a Grimsby phone
   book, and period taxi-firm names.
7. **The share of women in CID in 1990**, and whether English Catholic
   priests of that generation were mostly Irish-born.
8. **Older, Humberside, consented voices in any open corpus.**
