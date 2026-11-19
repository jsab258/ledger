# Pack 01: canon, rulings, plan, charter, old answers

Digest only. Extracted and compressed from five files. No opinions added. Every item names its source as path plus section heading. Dates are as the sources give them. Numbers are exact.

Files digested: canon.md, RULINGS.md, PLAN.md, CHARTER.md, legacy/studio-v2/game-design/decisions-answered.md.

## 1. Canon digest

canon.md status: "APPROVED 2026-08-31 by Jafar". It "outranks every document and agent". Violating it in content is a gate failure (tools/canon-gate.py --corpus, era and brands). Tone is the judge's under D7, not a gate. A ruling that changes canon edits canon in the same batch (canon.md, header).

### 1.1 Game and platform (canon.md, Game)

- LEDGER: "open-town crime sim and social RPG. Single player, PC first."
- "Third-person, never first-person. PC only, on Windows." (Jafar, 2026-09-24.)
- Town: Meridian, a fictional British port town. One map, seven districts.
- The seven districts: the Hook (old port, Mickey's, the player's minicab office); Copper Row (market quarter); the Exchange (offices, lawyers); the Parade (nightlife); Fairview (residential hills); Ironside (industrial); Gullwing (faded resort waterfront).
- Streets minted: Quay Street, Weighhouse Lane, Tannery Row.
- Street districts (minted 2026-09-02, struck on sight if Jafar disagrees): Quay Street in the Hook, Weighhouse Lane in Copper Row, Tannery Row in Ironside.
- "THE BUILT STREET IS QUAY STREET, IN THE HOOK", and Mickey's stands on it (Jafar 2026-09-08, option C).
- The 593 pieces keep their east_parade_* identifiers. These are asset names and carry no claim about where the street is.
- Quay Street's three sides (Jafar 2026-09-22, reworded 2026-09-23): the east side is the six-bay parade; the west block across from the north half of the parade carries shops; the west block across from Mickey's, at the quay end, is plain terraces.
- Mickey's is a minicab office (D19, decided 2026-09-14, supersedes D15's pub). Its information room is the business: "a book of every fare, a radio nobody can help overhearing, a yard with two escapes, a rank outside."
- Other pubs remain as buildings on the street, boarded or serving food, "never entered for drink."
- Graffiti tags minted 2026-09-02: TANNER (Ironside), SNIDE (Copper Row), GULL (Gullwing), QUAY FIRM (the Hook), PARADE RATS (the Parade). They are wall names, not the three rival organisations.

### 1.2 Era (canon.md, Era)

- Late 1980s to early 1990s. Working window 1988 to 1992.
- Late-analog: landlines, phone boxes, answering machines, pagers for dealers and fixers, cash and paper.
- CCTV rare: the bank, and a second site that is Jafar's to name. The off-licence was struck 2026-09-10 under D18 and nothing was minted in its place. Tape recycled weekly.
- One camcorder in town, a rare witness type.
- "No internet, no mobiles in ordinary pockets."
- "Any 1950s or 1970s framing is wrong, corrected on sight."

### 1.3 Tone and look (canon.md, Tone)

- Grounded noir. Comedy: dry British wit plus seaside-postcard smut, sparingly. Tabloid and Viz-adjacent flavour. "Never GTA-style American satire."
- Visual target: "photoreal, wet, overcast, grimy Britain." Weather and grime are the strategy, not stylization.
- The bar is the Meridian Test (D8, D9). GTA V PS3 is retired as a reference bar.

### 1.4 Premise and cast (canon.md, Premise and cast; baseline Jafar 2026-09-28)

- Player: Tom Nowak, 32. Son of a Polish post-war settler and Mickey's sister. Arrives with one suitcase and a letter.
- Uncle Mickey (Michael Suddaby) has died. He left Tom Mickey's, "a half-dead criminal outfit and a book of uncollectable debts."
- Tom has never been to the Hook. He is a stranger to everyone, known only as Mickey's nephew by name (2026-09-23). His life before the Hook is left unsaid: nobody asks, he never tells (2026-09-28).
- Inherited loyalists: Ron Kirby (old muscle, 58, a docker until 1989, kept on for the door and the rank); Sheila Dunn (bookkeeper, 53, at Mickey's since she was 22).
- Three rival organisations: the old-money machine (corruption and lawyers, head Geoffrey Agar); the dockside syndicate (muscle and smuggling, head Maureen Jensen, "the Widow"); the new crew (flashy and reckless, head Danny Cammack).
- Detective: DS Carol Ellis.
- Day-life ring: Darren Milner (25, street hustler); Ada; June Suddaby (Mickey's estranged daughter); Father Brendan Walsh (Irish-born parish priest); Alison Sedman (journalist love interest); Philip Danby (teacher love interest); the Fixer; Keith Garbutt (broker between all three rivals).
- "Ada was never a teacher" (2026-09-28).
- Standing ladder in what the town calls Tom: the new owner, then Nowak, then Tom, then Tommy. "The gate is knowing, not liking."
- Sheila is the one exception (2026-09-29): she withholds his name until she trusts him, as she promised Mickey.
- Names ruled 2026-09-24 and 2026-09-28: Lena to Sheila Dunn; Rocco to Ron Kirby; Sam to Darren Milner; Mara to Carol Ellis; Aldous Vane to Geoffrey Agar; Sera Kest to Maureen Jensen; Noor to Alison Sedman; Elias to Philip Danby; Danny Ro to Danny Cammack; Tom Novak to Tom Nowak; Toma to Tommy; Father Emil to Father Brendan Walsh (Father Walsh to the street); the Fixer is Keith Garbutt; June's surname is Suddaby. Mickey's, Ada and June are kept.
- Old names survive only as internal ids (lena, rocco, sam and the rest). They are never what the player sees or hears.

### 1.5 The content rule (canon.md, The content rule; D18, permanent, approved 2026-09-10)

- It is "a RULE, not a note". It governs what may exist at all, in image and in speech.
- Alcohol and gambling out "ENTIRELY": never shown, served, drunk or spoken of. "PUBS MAY EXIST AS PLACES." What the pub is for without drink "is a design task, not a subtraction."
- Tobacco stays.
- Violence stays, including blood and light gore. No torture and no cruelty as spectacle.
- "Killing is possible, rare, permanent, and the town remembers it forever."
- Cars (his pick, 18 Nov 2026, 22:07, keeping his July answer): a car can knock a person down and hurt them badly, and never kills. Only the player's car can strike anybody; AI drivers always brake for people. Then the choice: stop and help, or drive off and be chased as a hit-and-run.
- Full period swearing is allowed. "NO SLURS OF ANY KIND."
- Drugs exist as an off-screen economy other people run: never shown, never used, never a player verb.
- No prostitution and no sexual content. Seaside-postcard innuendo is not sexual content and stays.
- "NO CHILDREN ANYWHERE": none rendered, none in the crowd, none in dialogue or image prompts. "THE SCHOOL STANDS CLOSED" for the game's window; the building is there and nobody is in it.
- Racism and sectarianism may exist as facts about characters, never voiced as slurs, never rewarded.
- Religion is present as part of life, never mocked, never a mechanic.
- Police are corruptible as individuals, never as a thesis.
- Enforced at six sites: the rule; every image spec's content clause; tools/content-gate.py over dialogue and spoken lines; crowd generation (code); the brand bible; the animation library (walked by clip and slot name, added 2026-09-21). The gate cannot read intent.

### 1.6 The moat, unchangeable (canon.md, The moat)

- Every act exposes seven perceivable slots.
- Five-rung identification ladder; the top rung, recognition, "is gated by relationship, never by distance and light alone."
- Permanent per-NPC memory. "Nothing is ever wiped; remediation is behavioral."
- Gossip spreads through schedule intersections.
- Live LLM conversations with per-character memory and local voice.
- "Deterministic Core decides every outcome the player feels. LLMs classify, never adjudicate."

### 1.7 Pillar: verbs first (canon.md, Pillar; Jafar 18 November 2026)

- The player mostly acts: jobs done with the hands, break-ins, fights, driving, working the street. The living town watches and reacts.
- Talk is where consequences surface and are dealt with. The Ledger keeps track. "Talk stays the moat, never the main thing the player does."
- Target numbers (Study 2 and the player study): about ten distinct activities per thirty minutes; nothing new for at most about five minutes; talk well under half of play time.
- Enforced by the prototype's AI playtester each round, and by P4 in the real game (advisor 224).
- His words (18 Nov, 16:02, advisor 226): "we don't want a gossip simulator. We want an exciting, immersive, novel game."
- Memory and gossip are "the engine under the hood, not the show". The player feels tension, risk and a rise to power. Every job is tense because the town is watching.

### 1.8 What LEDGER is not (canon.md, What LEDGER is not; D24, 2026-09-14)

- NOT an open-world sandbox, NOT a shooter, NOT a driving game, NOT an economy simulation, NOT a story-first narrative game. "A small dense town where what people know about you is the mechanic."
- Anything not feeding perception, memory, gossip or consequence gets the smallest budget that keeps it from looking wrong. A spend rule, not a ban.
- Fighting must look and feel AAA (Jafar, 12 October 2026).
- Driving, when it comes, must end at AAA quality: background traffic in the friends' build, a simple car once the map is bigger, AAA driving the end state (17 November 2026).

### 1.9 Brands and law (canon.md, Brands and law)

- Every brand, band, club, product, weapon and vehicle is fictional. No real people, voices, logos, lyrics, car models. The licence allowlist is law.
- Minted: Mickey's, the Tivoli (cinema), Meridian Harbour Board, Meridian Ferry.
- Brand bible still owes: football club, local paper, pirate radio station, regional TV channel, telephone operator (kiosk mark), postal cypher (pillar box).

### 1.10 Fixed decisions recorded in canon (canon.md, OPEN)

- Item 1: engine DECIDED, Unreal (D16, 2026-09-10). Unity is the legacy reference build. The C# Core stays the source of truth the C++ port is checked against.
- Item 2: narrative DECIDED 2026-09-28. Tom Nowak, the three acts, the three rivals and the empire roster are the baseline, per game-design/story-outline-2026-09-28.md.
- Still open from item 2: the cast-sketch versus built-cards mismatch (Sam and Ada, written at one-street scale), which the cards settle as written.

## 2. RULINGS digest

RULINGS.md header: his binding rulings in force; the later stands; canon outranks them. Cap 4,900 words, raised only with his yes. Dates are day and month as written (2026).

### 2.1 Play and design

- RULINGS.md, What the game is, 30 Oct: Tom rises in position (money, respect, crew, property, clothes, access), never in numbers. A hard opening: nothing and nobody.
- Same section, D27 and D30: the end state is the ambition; the narrative is owed.
- Same section, D33, D34, D11: the player sees his own position, never other minds. No reputation numbers. No stats; difficulty only as assists.
- Same section, D35 and D58: reloading is never stopped, the game says what is permanent. No redemption. Hunted-state endings reachable.
- Same section, D12, D20, D37: the Ledger is a notebook of people and events. No minimap. A paper map and street signs.
- Same section, 23 Sep genre: no jump; crew act on orders; others drive traffic and the firm's cars; boats and buses are scenery; few short skippable cutscenes; jobs, no waypoints; coat, pockets, cab-office storage; buying, selling, fencing, no crafting; English only, text out of code; no multiplayer. Floor: object interaction; optional presentation (photo mode, credits, after the ending); making the game.
- Same section, D56: the crime layer owes eight verbs, in order. D26: sound is a lane, CC0 only. D13: the map is drawn from canon as data with testable layout rules. 5 Oct: the September atlas (atlas-01) is the town's map, updated to the built street (48 m, its climb, its bend east behind the parade).
- Combat (12 Oct, same section): his "LEDGER Combat: Final State" is the design (game-design/combat-design.md). 30 Oct: fists knock a man out and never kill alone; a fall against a kerb, wall or step after a blow can kill, rarely, and the town treats it as a killing. Must look and feel AAA; the animation source gets a lab test first.
- RULINGS.md, The release, Combat 18 Nov: end state A, guns rare, after melee, AAA when used; an escalation dial once guns exist; no silenced .22.
- Same section, Cars 17 and 18 Nov: parked cars, then traffic from their kit in the friends' build after one passes; an arcade car once the map grows; AAA driving the end state, costed for him first. Fun first, as non-sim open-world games; 1990 by sound, sway, look, relative speed; real figures a floor; game-band targets; automatic gearbox. A car hurts, never kills.
- Same section, Story 28 Oct: one main story with two or three endings.
- Same section, Live talk 28 Oct: every named character if possible, main characters at least. At release through the studio's server (24 Sep: sold once, key never shipped, each copy's allowance above a playthrough's measured cost, then a spending stop and written lines; an own-key mode later). A local model on the player's card re-tested about every three months.
- RULINGS.md, The story and the first week, 28 Sep: story spine is canon's baseline; outline approved (game-design/story-outline-2026-09-28.md); the first hour is the plan. 29 Sep: the first week's nine designs stand as written. 30 Sep: thirty regulars stand as written.
- Same section, 30 Sep: Mickey died of his heart at the office early one morning; Ron found him; nobody thinks otherwise. Winding the business down ends Mickey's arrangement. The warehouse fire: the street's version is a street fact; the truth is never the street's.
- Same section, 1 Oct: Mickey's people (Ron, Sheila) never go to the police about one of their own. A neighbour who sees Tom put a window in reports him, unless on his side or talked round.
- Same section, 30 Sep and 28 Sep: a witness's story is only as sure as the witness was; a noise or a shape is suspicion, never "he did it". Tom's reading of the ending's cost comes from what he saw and heard, never the true state.
- RULINGS.md, People and the street's life, 23 Sep: after a deed, near people look, some gather and drift back; witnesses talk quieter for an hour. D25: everyone perceives, remembers and gossips. D29: half-recognition, lying and having heard of Tom show in posture first.
- Same section, 30 Sep: townspeople measured at 0, 5, 10 and 20 packaged; walkers' feet fixed; one approved in the game before twenty.
- Same section, motion: the walk on Epic's Game Animation Sample with motion matching (13 Oct), third try the default (26 Oct); other poses from MetaHuman clips and Mixamo; sitting reopened (28 Oct). 9 Nov: he never films or performs anything; Pexels and Pixabay clips allowed as references.
- RULINGS.md, Talk and AI, 24 Sep: everything the town says unprompted is written ahead, generated and checked once; live talk only when the player talks to someone. 25 Sep: a character says only what the simulation knows; the claim check is a net, not a wall.
- Same section, Speech (7 to 28 Oct): no prepared openings; no cloud voice; replies cite their facts; a hard rule refuses any sentence naming a person, place, event, number or year the speaker's facts lack. The 2 s bar is a newcomer's real questions; small talk reported beside, never instead.
- Same section: 23 Sep, offline or slow: the authored street carries on, an in-character brush-off and a small sign; a slow line dropped after about 8 s. 3 Oct: a threat can stop a report to the police, never the street's talk. 1 Oct: suggested lines "Mixed", Tab on keyboard. Neighbours' talk at most every 45 s.
- Same section, 28 Sep and 23 Sep: a short thinking sound with a glance before an answer, no loading sign; a subtitle appears only with its audio.
- Same section, 29 Sep: live talk names no real make, brand, shop, club, programme, paper or public figure, and nothing after 1992.
- RULINGS.md, The look and the street, 4 Oct: Mickey's office is the front room Tom walks into: real glass reflecting the street, a 1990 cab office's wear and clutter (radio set, ashtrays, kettle, telephone, scuffed counter); no glitches.
- Same section, 3 Oct trades: bay 1 fishmonger, bay 3 empty unit to let (whitewashed), bay 4 launderette, bay 5 grocer; west_north a newsagent and tobacconist, an ironmonger, a tea room; east_chandler a ship's chandler. Poll-tax posters are an invented local campaign.
- Same section, camera 28 Oct: street camera at the Between picture's height and 86-degree lens, pulled back to 3.1 m so his feet are in frame; changing by situation as Mafia's (closer for talk, wider for fights).
- RULINGS.md, 18 Nov prototype (How the work runs): each round names its real-game decision or design question and study findings served; new verbs welcome to find the fun; town simulation frozen until C#'s replaces it; no polish. Designs carry experience rules: never stuck, smooth input, no silent failure, camera out of walls.
- RULINGS.md, The look and the street, 5 and 7 Oct weather: a grey range (dry overcast, drizzle, rain), the street drying and wetting; rain changes who is out, what is heard and seen; never sunshine in the friends' build; day and night now, four or five states later, no moving sun. 1 Oct night: pools of lamp light with darkness between, lit windows.

### 2.2 Quality and testing

- RULINGS.md, The release, Authored breadth 13 Nov: AAA breadth "from AI authoring at scale, not hundreds of people". Everything is authored: spec, AI author or tool, verifier against references. Out: unplanned filler, anything shipped unchecked. Test: can the spec and the check be pointed to.
- Same section, 5 and 6 Nov: full scope stays the target; no path chosen on extrapolated numbers. If cost per piece has not clearly fallen by 1 February, "scope moves first, never quality". Deep before wide: one dense district proves the method. No money for motion capture. From phase 3, short rough feel checks judged only on fun.
- RULINGS.md, How the work runs, 11 Nov: efficiency, never at quality's cost, is the first philosophy. Records and process under about 15% of spend.
- Same section, 6 and 7 Nov testing: AI testing so what reaches his hands is "99% done"; lean checks, one added only after a fault slipped past, dropped after a month catching nothing.
- Same section, 7 Nov tries: professional method researched first in a dated note; two failed tries set a fault aside; then one different researched method; up to four while each closes the gap to the bar by a third with no new fault.
- Same section, 3 Nov, reviews sized to the piece: small piece, own check plus one fresh Sonnet reviewer, one round; medium piece, the gate, at most two rounds; whole street frames and whole people, the full gate and his look.
- Same section, 3 Oct: the AI tester's walk is played as a player would and reports each morning whether the town visibly knows Tom.
- RULINGS.md, The look and the street, 21 Sep and 1 Oct: the Hook sheet (pass 4) governs mood, palette, composition; dated photographs win on what things looked like. Every visual but clothes is judged against the Hook sheet and KCD2 frames; yes only for 2026-grade work.
- Same section, 3 Oct bars: the wet street dark, glistening, mirroring sky and buildings, puddles water; the hill built, not hazed; windows with white frames, sash bars, sky in the glass.
- Same section, 29 Oct: the day's exposure one stop darker, kept, never brightened again.
- Same section, 23 Sep and 24 Oct: 60 fps at 3440 by 1440 on the RX 6700 with voice running, never below 30, by drawing smaller and upscaling. The 6 GB card line is the game alone for now; 1.7 ms spare accepted.
- RULINGS.md, Clothes, 3 Oct: clothes are the one exception to the visual bar. Floor: plain, period-plausible, no modern giveaways, no clipping or holes, nobody frozen stiff. Only gated garments from CC0, unmarked CC-BY with credit, Blender or Marvelous Designer.
- Same section, 6 to 8 Nov: the tailor boss falls only when a garment set passes the 2026 bar close up, holds in walk, sit and turn on film, the cast wear distinct outfits and repeats are cheap. No second Marvelous month unless he decides by 25 November.
- RULINGS.md, Faces, hair and voices, 30 Sep and 8 Oct: faces frozen: Ron P2, Sheila S4 with hair, Darren S6 with Epic's short cut, Tom L1. 25 Sep: the other eleven casting sheets approved as text.
- Same section, 3 Nov: no hair skill until one character's hair passes the full gate.
- Same section, voices: no voice cast without his yes; no hiring ever; voices judged by ear, accent checker a screen. In game (3 Oct, 26 and 27 Oct): Sheila p267 and Ron p227 on Pocket; Darren recast on Pocket, VCTK p286 (Newcastle); Agar p226; dispatcher p280. D50: voice watermark kept.

### 2.3 Reference games

- RULINGS.md, Sources, licences and money, 17 Nov: other games studied from the outside only (gameplay footage in the browser, developer talks, published analysis) into a feel-targets sheet. Never decompiled, files never opened, copy protection never bypassed, videos never downloaded. Only own words and numbers; studies stay notes.
- Same item: six footage frames kept for one blind line-up (18 Nov). His driving study tunes to the sheet. "KCD2 is the bar (GTA: why people play long); Mafia only a period Unreal study, never the yardstick (18 Nov)." GTA VI: no story, fates, mission plots or endings reach him; systems only.
- RULINGS.md, The look and the street, 21 Sep and 1 Oct: every visual but clothes is judged against the Hook sheet and KCD2 frames. Other games' screenshots never in the repository.
- RULINGS.md, The camera 28 Oct: camera changing by situation "as Mafia's".
- RULINGS.md, Talk and AI: no other game cited.

### 2.4 Scope and money

- RULINGS.md, The release, 28 Oct: one full release late in 2027, not early access; a friends' build at the end of every phase from phase 4 on, on his PC. Length 15 to 20 hours.
- Same item: map is the Hook plus the docks; more districts in updates after release. If time runs short, the docks are cut first.
- Same section, 3 Oct, 4 Oct, 1 Nov: a thirty-minute Quay Street build his friends play, passing the Meridian Test; his PC and own account, a shortcut, his key capped at five dollars an evening, no relay; the twenty basics; nothing a friend sees unfinished; Sheila's face whole when she talks; no debug text. The friends' evening comes after the whole street. 25 Oct: the cast voice on the card is fine for their evening.
- Same section, 5 Oct and 29 Sep: CHARTER.md and PLAN.md replace every list; no new system before its place in PLAN.md.
- Same section, 22 Oct and 8 Nov: Rita's front is the shops' sample; the fishmonger and the empty unit to let are built in phase 2. 25 Oct: phase 5 uses kits plus Unreal procedural tools, sampled checks, designed during phase 2.
- RULINGS.md, Sources, licences and money, 16 Sep: purchases and accounts are his alone; nothing for the street or cars; 1 Nov no new hardware; 29 Sep no paid voice service.
- Same section, 1 Nov and 16 Nov: monthly API credit ($200, lapsing about the 11th) pays for the game's own calls and bulk checks, never beyond; no bought credits or automatic reload.
- Same section, 3 Oct: sources in order: free assets that fit (Poly Haven, ambientCG, CC0 Sketchfab scans, unmarked CC-BY with credit); else own, in Blender from photographs and generated textures, as kits with variation. 30 Oct: CC BY 4.0 allowed for clothes and accessories.
- Same section, 3 Oct narrowed 13 Oct: nothing marked NoAI is used, even as a reference, except content Epic itself publishes on Fab. Sources in THIRD-PARTY.md.
- Same section, 24 Sep: nothing ships off the allowlist. Allowed: OFL fonts; CMU motion capture inside the game; Mixamo on his account; VCTK voices (consent a stated risk); CLO CONNECT patterns. Not allowed (2 Oct): CGTrader's licence.
- RULINGS.md, How the work runs, 13 Nov and 18 Nov: Kiln (the clothing tool) takes 70% of weekly usage this week, else 15%; its three proofs come before any props, vehicles or buildings module.
- Same section, 16 to 23 Nov (his picks): double pace, eight helpers a session; Fable up to 40%.

### 2.5 Process (brief)

- RULINGS.md, How the work runs: 30 Oct decide-it-yourself within canon and rulings; 4 Nov advisor channel (his orders only within canon, rulings and the week's order); 25 Oct every order is a ledger; 2 Nov his page "LEDGER: Needs you"; 8 Oct engine questions go to the installed 5.8.2 source first.
- Same section, 7 and 10 Nov: an hourly-checked line of weekly usage, 0% at Monday 13:00 to 90% next Monday 07:00, with banded rules for being ahead or behind.
- Same section, 8 Nov models: Opus for session, code, diagnosis, final reviews; Sonnet or Haiku for extraction and routine edits. 9 Nov records: NOTEBOOK.md and RECIPE.md; DECISIONS.md one line per choice.
- Same section, 29 and 30 Oct computer use: only in Marvelous Designer; 11 Nov builder may click in the Epic launcher and fab.com only for named tasks.
- RULINGS.md, Disk, git and backup: 17 Nov storage map with floors (F: 20 GB, C: 40 GB); 29 Oct Claude deletes only what it made and nothing uses; 3 Oct no MetaHuman files in git; 6 Oct packaged builds only for evidence, nightly if wip moved, or main.

## 3. PLAN.md and CHARTER.md

### 3.1 CHARTER.md

- Adopted 5 October 2026 from the outside audit's draft (production/audits/2026-10-04-charter-draft.md) with Jafar's edits (CHARTER.md, header).
- Goal (CHARTER.md, Goal): "Thirty minutes of Quay Street that Jafar wants to play and his friends can launch on his PC, on his own account." They accept the street's appearance, see the town remember what they did, and find the conversation responsive.
- Scope (CHARTER.md, Scope): one continuous playable street; Mickey's usable front office; the three existing conversational principals (Ron, Sheila, Darren); only the further people and places needed to make the approved first-week beats visible (game-design/first-hour-2026-09-29.md). A deed produces an intelligible later consequence that survives reload. Every visible person takes part in perception and memory unless ruled scenery. "No new acts, combat programme, district production or crowd of hundreds before this works."
- Bar (CHARTER.md, Bar): Hook-quality street composition, materials, depth, wear and atmosphere in the moving game, reverse views included. Approved identities and voices preserved. Clothes keep their exception and floor. "A static approved picture never approves a broken walk."
- Weather (CHARTER.md, Weather): dry overcast, drizzle and rain; wetting and drying over time; rain changes who is out, what is heard and seen. Sunshine never in the friends' build.
- Constraints (CHARTER.md, Constraints): AI does the implementation; no hiring, new subscriptions or unapproved purchases. Only verified AI-permitted sources; nothing NoAI. One RX 6700 (10 GB), shared with the voice. Weekly allowance 70% production, 10% independent review, 20% kept for Jafar. The $1-a-day measurement and $5-a-friends'-evening caps stand.
- Authority (CHARTER.md, Authority): Jafar decides taste, identity and money and gives orders on Mondays. One production session owns implementation, sequencing within the phase, evidence and corrective work; town and clothing work are bounded tasks.
- Stop condition, binding (CHARTER.md, Stop condition): if a representative street-and-person sample cannot pass the bar within its capped proof budget, the failed capability is reported plainly. "Failure is never disguised as another plan, and a town is never promised on an unproved method."

### 3.2 PLAN.md

PLAN.md, header and opening: adopted 5 October 2026 from the outside audit's draft with Jafar's edits; replaces every earlier list. Numbers are ceilings and estimates. W is one weekly allowance: at most 0.70W production and 0.10W review a week; 0.20W is Jafar's. Each task's time recorded (tools/timelog.py). Phase 1 measures an accepted family's cost and reuse time before town production is extrapolated. Every exit bundle names commit and package, raw logs, fixed-camera images, a walking recording and the failures. A fresh model verifies the exit; Jafar makes taste decisions.

Phase 0, Recover control (PLAN.md, Phases). Ceiling 0.20W, two to three working days, nothing bought.
- Goal: caps on TOWN.md and CLOTHES.md; recover unseen work (branches, drives, approval answers, old studio repository); CATALOGUE.md with a homes table; checks failing the build; every friends-build ruling mapped to one item, owner and packaged proof; one Shipping launch from the shortcut on his own account; history cleaned after telling him.
- Exit: a fresh reviewer checks each item before phase 1. His checkpoint: only open money and identity choices.

Phase 1, Prove the bottlenecks. Ceiling 1.00W, one to two weeks, $1 a day measuring.
- First proof: Mickey's front office (room kit, real glass reflecting the street, 1990 wear and clutter, no glitches), plus one frontage and three fixed street views. One complete Tom and one speaker walking, sitting and turning.
- P2 the voice: two measured approaches at most, timed beside checked talk. P1 completed packaged: day, night, walking, Windows memory, sustained speech.
- Exit: samples meet the bar; render and voice pairing has measured headroom; median first meaningful speech two seconds or less (no prepared openings, 7 October ruling). His checkpoint: one whole-frame and moving-character review.
- Binding stop: a sample that cannot pass within the ceiling halts expansion.
- Prototype's place: the PLAN.md text names no prototype. (See section 5.)

Phase 2, Produce Quay Street from proved families. Ceiling 2.00W, three to four weeks, no new spending.
- Goal: from the asset plan (production/research/asset-plan/SUMMARY.md): building kit re-seeded; mapped upper rooms; real near shop rooms; ground, wear, signage, furniture, food, vegetation, the hill's distance versions. Only approved samples multiplied. P7 walking, P6 plain clothes, P20 exposure, P13 ambience. Parked cars once one sample car passes (P9).
- Exit: a whole-street day and night walk passes asset, source and budget checks, reverse views and the office camera (P15) included. His checkpoint: street, people and ambience, at most three decisions.

Phase 3, Make thirty minutes hold. Ceiling 0.75W, one to two weeks, the existing talk caps.
- Goal: N3 ported with only the first-week content P4's gaps need: visible arrivals and deliveries, consequence, a useful office and ledger, prompts. Every visible person has a simulation identity. The weather proof. Debug keys, typing and collision faults removed.
- The fight lab test: after his combat pick and a Fable melee round, a punch, hit reaction and fall a witness sees through real perception code.
- Exit: two different thirty-minute newcomer routes and one continuous checked-live route within the cap; no critical fault; at most five empty minutes; a consequence seen and kept after restart. His checkpoint: he plays thirty minutes and judges it.

Phase 4, Friends' candidate. Ceiling 0.50W, about a week, at most $5 an evening.
- Goal: traffic from the car kit (17 Nov). Package frozen; P5 on his own account and shortcut; source credits; voice and save separate; packaged performance in rain, at night, with speech; the two routes repeated.
- Exit: the twenty basics proved by output; no visible placeholder, hole or debug display; no development tools needed. Friends' first thirty minutes logged, blockers fixed before scope is added. His checkpoint: appearance and the evening's spend.

Phase 5, First town. A 1W pilot, then 6 to 12W provisional (three to six months).
- Goal: one adjacent block from existing kits; then the 14 principals, about 30 regulars and the population in batches, load-tested at 0, 5, 10 and 20 visible people first; every story or routine tied to playable evidence.
- Exit per batch: new-seed variety, weather attendance, witness, memory, reload and performance hold; no unproved family multiplied.

Other stated scope (PLAN.md, after Phase 5): consolidates P1 to P22 (production/research/pre-production/3-PROOFS.md); P12's face solver only if the conversation sample fails; P17 combat and P18 music deferred. "Friends: eight to twelve weeks, conditional on phase 1", low confidence; a failed gate voids the date.

Measures of success (PLAN.md, Performance exit and Weather proof):
- Median frame at most 16.7 ms, p99 25 ms, dedicated memory 6 GB with the voice on the card, at native output with speech, a wet night and the full population. P1's High at 55% leaves about 2.5 ms by day, 1.4 ms at night.
- Weather proof: one saved wetness value driven by dry, drizzle and rain, wetting and drying timed independently; a recorded dry-rain-dry walk with surface, sound and visibility changes; same-seed runs show changed attendance and consistent witnesses, nobody vanishing in view; reloading mid-change reproduces it. No sunshine in the friends' build.

PLAN.md, Session, models and orders: one production session; town and clothing work are bounded tasks. Sonnet for routine implementation; Opus for bounded diagnosis, planning and each gate's fresh review; Haiku only for mechanical extraction. Town tasks: N3 with a packaged port; newcomers' common questions grounded in authored facts; P4's reachable gaps. Stopped: new systems, unreachable depth, reviews of unported features. Clothing tasks: one allowed plain outfit fitted to approved bodies. Stopped for the builder: wardrobe and town multiplication, whole-street parameter sweeps. Monday review updates R1 to R10 (production/research/pre-production/6-RISKS.md). Two failed attempts bring a failed-capability report.

CHARTER.md success measures, as stated: the street's appearance accepted; the town seen to remember; conversation responsive (CHARTER.md, Goal); the Bar and the Stop condition above.

## 4. decisions-answered.md: earlier answers for the OLD version of the game

Source file: legacy/studio-v2/game-design/decisions-answered.md. Its own header says "STATUS: LOG, 2026-07-31. NOT CURRENT." It is a log, not a queue. The old game was an American-leaning pub game with a laundering ledger. Every line below is marked history. None stands.

1. history: carry or flag. Violence is a verb, with weapons (fists, knives, later guns), inventory, buying, stealing, finding; "approved" 2026-07-29, weapons-spec.md v3. Source: Decisions answered, "is violence a verb?". Flag: canon now has combat under RULINGS 12 Oct and 30 Oct.
2. history: carry or flag. Standing quality bar from 2026-07-29: "as close to the best games in the genre as our limits allow." Source: same section.
3. history: carry or flag. Act III's crisis is an audit by a mandated official reading the books; five endings. Answered "1 audit", 2026-07-27. Source: Open now, item 1. Flag: RULINGS.md says two or three endings.
4. history: carry or flag. Inspector named Tobias Reese, Board of Excise, nineteen years; not corrupt, not cruel; override freely. Source: Open now, item 8.
5. history: carry or flag. Inspector relief halved: ScopeFactor cooperation term 0.09 to 0.045, stonewalling kept at 0.15. Answered "Halve the relief now", 2026-07-27. Source: Open now, item 10.
6. history: carry or flag. Copper Row to be re-cut as the cash-economy market quarter, not industrial. Recommended, answered by build, 2026-07-27. Source: Open now, item 2.
7. history: carry or flag. Detail concentrates in two dense cores (Hook and Copper Row) with a distance ramp to a floor, not to nothing. Source: Open now, item 4 (2026-07-29).
8. history: carry or flag. Purses extended to bribes and payoffs, not supplier payments. Source: Open now, item 6.
9. history: carry or flag. Rackets coupled to street prosperity: "Couple it." (2026-07-27); below 0.7 someone says the street has nothing to hold out with. Source: Open now, item 9.
10. history: carry or flag. Sim bot coats up from night two; the week's difficulty left to playtest. Source: Open now, item 5.
11. history: carry or flag. Options reachable from the pause menu; one OptionsScreen shared. Done 2026-07-27. Source: Open now, item 7.
12. history: carry or flag. UI smoke-test pass in CI recommended (open, panels). Source: Open now, item 3.
13. history: carry or flag. Protagonist named Tom Novak (since renamed Nowak in canon). "The new owner" is what people call you before they know you; name is something the street learns; ladder the new owner, Novak, Tom, Toma. Source: Previously open, item 0 (2026-07-27).
14. history: carry or flag. A day is 12 real minutes; never checked by play. Source: Previously open, item 0b.
15. history: carry or flag. Empire tuning: aggressive play nets $94 less than no rackets; "position over profit"; one knob SqueezeCostsProsperity. Source: Previously open, item 1.
16. history: carry or flag. Deferred purchases as late as possible: asset pack (~$40 to 60), Character Creator (~$99 a year), HDRP swap, ElevenLabs voice, the is-this-fun gate, API-key batch session. Player direction 2026-07-26. Source: Will need you at the vertical slice (M5). Flag: RULINGS.md says no paid voice service (29 Sep).
17. history: carry or flag. Traffic: collisions hurt but do not kill; only the player's car can strike anybody; AI drivers always brake; victim remembers, nearby people hold it at 0.95 confidence. Answered 2026-07-27, "the middle option". Source: Traffic: can you run people over?. Note: matches canon's 18 Nov car rule.
18. history: carry or flag. Prison: option C, a strain term (PublicRecord x1.15) on what the inspection sees when the street knows did_time. Decided 2026-07-28 by recommendation (delegated). Source: Does prison launder the information landscape?.
19. history: carry or flag. Dirty money may pay the drayman (weekly drink and flour supplier), written into the fiction as a grey counterparty. Decided 2026-07-28. Source: Should dirty money pay the drayman?. Flag: involves drink; canon D18 bans alcohol.
20. history: carry or flag. M15: make the city audible; bodies that perceive (gaze; notice, watch, comment, avoid, refuse, confront ladder); real character models are a purchase and his. Playtest note 2026-07-28: "overall feel is very text heavy / text adventure like". Source: M15, the immersion milestone.
21. history: carry or flag. Voice engine Chatterbox chosen on measured evidence (direction, emphasis, consistency); Kokoro and Piper rejected; XTTS moot; Kokoro dropped, one engine. 2026-07-28. Source: THE VOICE, Engine and Kokoro dropped. Flag: RULINGS.md names Pocket as the voice program.
22. history: carry or flag. Voice sourcing: "I'm not going to record anything"; clips collected from speech-technology corpora with donated voices (Common Voice CC0 first); no identifiable public figures. 2026-07-28. Source: THE VOICE, Where do the reference voices come from?.
23. history: carry or flag. Voice casting briefs written for five principals, eight street characters and crowd; Mara Ellis warmest and most reasonable; Hal least distinctive; Rocco tired, not tough. Source: THE VOICE, Who sounds like what.
24. history: carry or flag. Accent: first American base (2026-07-30), then option 1, "the city became British" (2026-07-31); VCTK corpus chosen; all nineteen voices cast. Source: OPEN, the voice corpus is wrong; DECIDED, the city is British.
25. history: carry or flag. Non-verbal voice (grunts, pain, exertion) from CC0 effort recordings, free: "free obviously. i won't be recording anything." 2026-07-31. Source: OPEN, non-verbal voice.
26. history: carry or flag. Cloning a donor's voice inside the consent rule: recommended proceed; STILL OPEN as of the log. Source: OPEN, is cloning a donor's voice inside the consent rule?.
27. history: carry or flag. Mains hum 50 Hz recommended; settled by the British setting. Source: Small, and genuinely trivial; DECIDED, the city is British.
28. history: carry or flag. British consequences: $ to GBP; "the bar" to "the pub" (395 references); the audit becomes Customs and Excise; Downtown and The Strip renamed; five picks to be re-cast. Source: DECIDED, the city is British. Flag: "pub" and landlord framing sits against canon D18 and D19.
29. history: carry or flag. Standing rule (2026-07-26): every queued decision is also spelled out in chat as answerable options. Source: header.

## 5. Open tensions between the files

Facts only. Each item gives both sources.

1. Conversation weight. CHARTER.md, Goal: friends "find the conversation responsive"; Scope names three conversational principals. canon.md, Pillar: "Talk stays the moat, never the main thing the player does"; talk well under half of play time.
2. Principals count. CHARTER.md, Scope: three conversational principals (Ron, Sheila, Darren). RULINGS.md, The release, Live talk: every named character if possible, main characters at least. PLAN.md, Phase 5: 14 principals, about 30 regulars.
3. Map extent. RULINGS.md, The release, Map: the Hook plus the docks. canon.md, Game: seven districts on one map. "The docks" is not a district name in canon.md. CHARTER.md, Scope: one continuous street.
4. Endings and acts. canon.md, OPEN item 2: three acts as baseline. CHARTER.md, Scope: "No new acts". RULINGS.md, The release, Story: two or three endings. decisions-answered.md, Open now item 1: five endings (old game).
5. Prototype's place. canon.md, Pillar, and RULINGS.md, 18 Nov prototype, name a prototype and its AI playtester. PLAN.md and CHARTER.md do not mention a prototype.
6. Simulation freeze versus port. RULINGS.md, 18 Nov prototype: "town simulation frozen until C#'s replaces it". PLAN.md, Phase 3: "N3 ported". The files do not link the two.
7. Dates. RULINGS.md, The release: one full release "late in 2027". PLAN.md: friends' build "eight to twelve weeks" from adoption, conditional; phase 5 then 3 to 6 months provisional.
8. Friends' build cadence. RULINGS.md, The release, 28 Oct: a friends' build at the end of every phase from phase 4 on. PLAN.md: only phase 4 is named "Friends' candidate"; phase 5 has no friends' exit.
9. Empty minutes. canon.md, Pillar: "nothing new for at most about five minutes". PLAN.md, Phase 3 exit: "at most five empty minutes". One measures novelty, the other emptiness; neither file defines the other.
10. Voice engine. RULINGS.md, Faces, hair and voices: Pocket with VCTK picks (Sheila p267, Ron p227, Darren p286). decisions-answered.md, THE VOICE: Chatterbox engine, Common Voice corpus first, later VCTK. canon.md, The moat: "local voice".
11. Talk delivery. canon.md, The moat: "Live LLM conversations ... and local voice". RULINGS.md, Talk and AI: "no cloud voice", live talk at release through the studio's server, API credit pays for the game's calls.
12. Old drink and pub design. decisions-answered.md (drayman, pub, "the bar" to "the pub", landlord) against canon.md, The content rule: alcohol "never shown, served, drunk or spoken of", and Mickey's is a minicab office (D19).
13. Name forms. canon.md, Premise and cast: Nowak, ladder ends at Tommy, Sheila withholds the name. decisions-answered.md, Previously open item 0: Novak, ladder ends at Toma, "the new owner" is a landlord's title in the British rewrite.
14. Combat lethality. canon.md, The content rule: killing possible, rare, permanent. RULINGS.md, What the game is, 30 Oct: fists never kill alone; a fall can kill rarely. decisions-answered.md, Traffic: nothing in the code can produce a death by car. All three state a car never kills, and RULINGS.md, Cars, 18 Nov agrees.
15. Reference bar. canon.md, Tone: GTA V PS3 retired; bar is the Meridian Test. RULINGS.md, Sources, 17 Nov: "KCD2 is the bar", Mafia only a period study. decisions-answered.md, header of the quality bar: "best games in the genre". RULINGS.md, 28 Oct camera: camera as Mafia's.
16. Weekly allowance. PLAN.md and CHARTER.md: 0.70W production, 0.10W review, 0.20W his. RULINGS.md, 13 Nov: Kiln takes 70% of weekly usage this week, else 15%; 16 to 23 Nov: Fable up to 40%. The files do not say how these shares nest.
17. Spend caps. CHARTER.md, Constraints: $1-a-day measurement and $5 a friends' evening. RULINGS.md, 1 and 16 Nov: monthly API credit of $200 pays the game's calls; "no bought credits".
18. Cast sketch versus cards. canon.md, OPEN item 2: Sam and Ada written at one-street scale, a mismatch the cards settle. Not resolved in the other four files.
19. Second CCTV site. canon.md, Era: a second site is "Jafar's to name"; nothing minted. No other file names one.
