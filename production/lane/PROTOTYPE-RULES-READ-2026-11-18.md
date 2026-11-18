# Prototype rules, read by hand from the bundle (18 Nov 2026)

Status: UNVERIFIED. Everything below was read from the minified game script (tools/lane/prototype/src/bundle, joined), not from a readable source. Until Fable's own source confirms each rule, none of it is the spec of record.

How it was read: the two parts were joined into a scratch copy and pretty-printed with jsbeautifier (MIT, pip) outside the repository; src/ was not touched. The game's code is the last ~15,500 lines of the 39,700-line pretty copy, after three.js. Each "search" string below is an exact piece of the ORIGINAL minified bundle (checked: each occurs once unless noted; `sr(500)`, `sr(20,!0)` and `Nine pounds, since the summer` each occur twice, the two uses agreeing), so it can be found with a plain text search in the joined ledger.js.

A large help: the game carries its own design notes in plain words (search `["Witness numbers",`, `["Gossip",`, `["Money",` and so on; the title menu shows them as "Design notes"). Where the code and the notes agree it says so; where they differ it says so.

Units: game time `x.t` is in game minutes from Monday 00:00 (Monday is day 0). Money is in pence. Distances are metres. "Real seconds" means seconds of play at normal speed.

Confidence: "read" = the code was read and the meaning is clear; "inferred" = the number was read but its unit or purpose was worked out from context.

## 1. Seeing and witnessing

| Rule in plain words | Number(s) | Search | Confidence |
|---|---|---|---|
| Sight range grows with the light at Tom's spot, cut by rain and by mist at night | range = (4 + 44 x light^1.2) x (1 - 0.3 rain) x (1 - 0.22 mist x night) | `4+44*Math.pow` | read (matches notes) |
| Cab headlights on: seen from at least 34 m | 34 | `e.lights&&(o=Math.max(o,34))` | read |
| Indoors: seen from at least 14 m | 14 | `o=Math.max(o,14)` (same function as above) | read |
| Field of view, out on the street | 1.08 rad half-angle each side (about 124 degrees in all) | `fov:1.08` | read (notes say "about 120") |
| Field of view from a window at home | 1.35 rad half-angle (about 155 degrees), only if awake and at the window | `fov:1.35` | read |
| Very close (under 3 m) they see him unless he is well behind them | under 3 m and within 1.9 rad | `n<3&&l<1.9` | read |
| Line of sight is checked against walls | env.los | `x.env.los(t.x,t.z,e.x,e.z)` | read |
| How clearly seen (0.05 to 1) falls off with distance | clarity = 1 - distance / range | `a=ue(1-n/o,.05,1)` | read |
| Noise radius by what Tom does | still 0.5 m, walking 5, running 12, cab 8 to 30 with speed | `i.v<.2?.5:i.run?12:5` | read (matches notes) |
| Noise carries further by hour | x0.5 from 10:00 to 16:00, x2 before 05:00, x1.5 05:00 to 07:00, x1.3 after 22:00, x0.8 otherwise | `i>=10&&i<16?.5` | read |
| Rain muffles noise | x (1 - 0.6 rain) | `em()*(1-.6*x.weather.rain)` | read |
| A sleeper hears only through the window, at 70 percent of the radius; loud acts wake them | 0.7 | `hear:c<=e.noiseR*.7` | read |
| Watching builds up before a sighting counts | attention rises by (0.45 + 1.4 x clarity) per real second, x1.5 during a notable act; a sighting when it reaches 1 | `attn+=i*(.45+1.4*a.c)` | read |
| Which acts count as being seen merely by being out | night out (23:30 to 05:00), coat by day, running in daylight, carrying the bag, the cab on a late night or with the bag, the cab by day | `H2()` area; search `"cab_night":"cab_drive"` | read |
| One sighting event per kind, per two-hour block, per day, per zone, however many see it | 2 game hours | `Math.floor(Ve()/2)` near `x.sightIdx[e]` | read (matches the README check) |
| Night noise unseen makes a "heard" memory at most every 90 game minutes per person | radius over 7 m, small hours only, 90 min | `r.heardT||x.t-r.heardT>90` | read |
| Deliberate acts (talk, fight, jobs) tell everyone who sees them at once; loud acts also reach those who only hear, as "a man" at 0.3 sure | sure 0.3, heat 0.3 | `src:"heard",who:"man",sure:.3` | read |
| A witness's sureness | 0.35 + 0.65 x clarity, x0.85 unless they put his name to it | `ue(.35+.65*t.c,0,1)*(r==="tom"?1:.85)` | read |
| A memory's starting heat | the act's severity + 0.3 (cap 1) | `ue(a.sev+.3,0,1)` | read |
| Naming: face score = familiarity x (0.35 + 0.65 clarity); coat at night x0.4; in the cab x0.6 if under 10 m and lit, else x0.1 | thresholds 0.36 (Tom), 0.2 (the new owner); below that a man, a coat or a cab; naming also needs knowing of the inheritance or familiarity over 0.5 | `s>.36&&o?"tom"` and `n.coat&&qn()>.5&&(s*=.4)` | read (matches notes) |
| Each act has a severity, a moral value and a crime level (0 to 3); 51 kinds (corrected 18 Nov by rules_test.py; first read said 45), from arrive (0.3) to kill (1.0, crime 3, never fades below 0.6 heat) | table | `inherit:xt(.5,0,0` | read |
| Seeing raises familiarity; a non-act glance at most once every 20 game minutes | +0.02 to 0.05 if named, else up to 0.6 cap | `seenCool=x.t+20` | read |
| Timid people (nerve under 0.62) step back when they see a crime or anything at night; others pause their walk 0.9 to 2.5 seconds | nerve 0.62 | `nerve==null?.5:i.def.nerve)<.62` | read |
| Night is a smooth 0 to 1 by hour | day 07:45 to 17:15, full night 18:45 to 06:15, blends between | `i>=7.75&&i<17.25?0` | read |

## 2. Gossip and rumour

| Rule in plain words | Number(s) | Search | Confidence |
|---|---|---|---|
| A gossip round runs every 4 game minutes | 4 | `Va.g>=4` | read |
| Only named people who are awake, not at home, not police, in the same space; within talking distance; not both walking | 4.8 m street, 8 m indoors | `>(t.space==="street"?4.8:8)` | read |
| Chance a pair talks per round | 0.9 x closeness weight; weight = 0.42 (+0.38 if close friends) x (0.4 + talkativeness of the teller) x (0.6 + 0.4 x the hearer's) | `t+=.38` | read |
| What is told: the teller's hottest story the hearer lacks, weighted heat x (0.4 + severity), x0.6 if it does not name him; heat under 0.12 is not passed; private acts and stories about the hearer are not passed | 0.12 | `s.heat<.12||e.mind.by[s.e]` | read |
| A discreet person holds back: the chance to say nothing is their discretion | Sheila 0.92, Darren 0.05, default 0.25 | `Sn(i.def.discretion` | read |
| Each telling: certainty x0.8, heat x0.92, hop count +1; the teller's own heat +0.12 | 0.8, 0.92, 0.12 | `sure:t.sure*.8` | read (notes say "drops 20 percent", matches) |
| No limit on hops and no minimum certainty to pass on | none found | n/a | inferred (absence) |
| Passers-by (the crowd) pass what they saw to a named person within 3.2 m, 35 percent chance, then forget it (heat 0) | 3.2 m, 0.35, heat over 0.2 | `Sn(.35)` (second of two matches) | read |
| Heat fades every 10 game minutes | heat x e^(-minutes/1700): halves in about 19.6 game hours; "forever" acts (a killing) never below 0.6 | `Math.exp(-i/1700)` | read (notes say "about 20 hours") |
| Certainty does not fade, only heat | n/a | `n.heat=Math.max(s,n.heat*e)` | read |
| Tuesday morning push: at 08:45 on day 1, if none of seven people (Grace, Brenda, Kevin, Pauline, Albert, Julie, Lee) has been told anything, one telling from Ron, Darren, Ada, Terry or Hal is forced | 08:45 Tuesday | `i===1&&e>=8.75` | read (matches notes) |
| Seeing two people tell a story about him (lit, in view, under 18 m) makes a Ledger "talking" note, once per pair per day | 18 m | `x.tom.z)<18` near `A5(i,e)` | read |
| What people call him: knowing score = 0.25 (knows of the inheritance) + 0.09 per kind of thing known (up to six) + 0.4 x familiarity | names at 0.2, 0.5, 0.8, 1.05 | `e>=1.05?4:e>=.8?3` | read (matches notes) |
| The street's name for him: the highest name that 40 percent of locals have reached | 0.4 | `length>=i.length*.4` | read |
| A person says a story to his face at most every 40 game minutes, never the inheritance, and not a thing done to them unless it was a grudge over 4 game hours old | 40, 240 min | `coolSay=x.t+40` | read |

## 3. The Ledger

| Rule in plain words | Number(s) | Search | Confidence |
|---|---|---|---|
| Every act he does goes on his own list of acts, unless marked "noself" (things done about him) | n/a | `x.ledger.acts.find(e=>e.e===i.id)||x.ledger.acts.push` | read |
| A person goes in an act's entry only by how Tom came to believe it, ranked: talking 0, window 1, saw 2, bought 3, asked 3, there 4, said 5; a higher rank replaces a lower | ranks | `talking:0,window:1,saw:2` | read |
| "Saw" is entered only when Tom noticed the watcher: within 34 m, within about 52 degrees of the camera's facing beyond 2.5 m, lit (0.2) beyond 7 m, a window lit beyond 9 m, and in line of sight | 34, 0.9 rad, 2.5, 7, 9, 0.2 | `o>34||o>2.5` | read (matches notes) |
| "There": he did it in front of them, or they were the target | n/a | `Os(e,i,"there")` | read |
| "Said": they said it to his face; "asked": he asked and was told; "bought": Ron or Darren paid | n/a | `Os(a,i,"asked"` | read |
| Ada's tea and two heads together in the caff make notes | n/a | `had their heads together at Rinaldi's` | read |
| The hint "L opens the Ledger" shows the first time a note is made | n/a | `L opens the Ledger` | read |

## 4. Money and debts

| Rule in plain words | Number(s) | Search | Confidence |
|---|---|---|---|
| Tom starts with 23.50 clean, nothing dirty | 2350p | `clean:2350` | read (matches notes) |
| Mickey's book: five debts, all open, no due date stored | Dennis Iveson 80.00, Lee Drewery 15.00, Darren Milner 22.00, Julie Kettlewell 9.00, Wayne Harrison 30.00 | `dennis:{owed:8e3` | read |
| A debtor pays in full when asked if afraid (fear over 0.45), or if they like him (over 0.3) and owe 15 or less; otherwise refuses | 0.45, 0.3, 1500p | `i.mind.fear>.45||i.mind.regard>.3&&o.owed<=1500` | read |
| A collected debt goes in the tin (dirty money) | n/a | `oh(n,!0)` in `VS` | read |
| Striking a debt out: liking +0.5 | 0.5 | `regard+.5` in `WS` | read |
| Julie offers to pay her fare when he drives her; he may waive it and strike the slate | slate 9.00 | `Nine pounds, since the summer` | read |
| Fare price: 80p plus 0.9p a metre from pick-up to destination, rounded to 10p | 80, 0.9 | `(80+We(t.sx` | read (notes say "80p plus distance") |
| Radio offers fares only in the cab with keys, 07:00 to 23:12, not carrying the bag; every 16 to 34 seconds; an offer lasts 26 seconds; a missed one waits 20 to 40; after a fare is paid, 14 to 30 | 16-34, 26, 20-40, 14-30 | `fareCool=_t(16,34)` and `t.t=26` | inferred (units taken as real seconds from the docket's "s") |
| Fares go to the pocket (clean) | n/a | `oh(` in fare payment | read (matches README check) |
| The fare book can hide 10.00 plus 80 percent of fares since the last wash; anything over is "books off", Sheila's liking -0.12 and a "wash" act she knows | 1000p, 0.8, 0.12 | `1e3+Math.round(x.money.sinceWash*.8)` | read (matches notes) |
| Night jobs pay into the tin | job 1 (Monday holdall) 60.00, job 2 (Tuesday parcel) 40.00, job 3 (Iveson, Wednesday) 100.00 for collecting 80.00 | `Sixty. Count it somewhere else.`; notes `["Night work` | read for 60 and 40; 100 from the notes only |
| A job not done by 03:30 to 12:00 the next day is a no-show | 03:30 | `Ve()>=3.5&&Ve()<12` | read |
| Rent: 18.00 to Sylvia Rennison, asked from Thursday; late if unpaid by Saturday 00:00 | 1800p, day 3, day 5 | `sr(1800,!0)` and `i>=5&&!t.rent` | read (the line says "Friday, by six"; the code marks late only at Saturday) |
| Ron sells what the door saw for 5.00; Darren what he heard for 3.00, a good word for 5.00 | 500, 300, 500 | `sr(500)`, `sr(300)` | read (matches notes) |
| Tea at Grace's: 20p, passes 25 game minutes, caff people familiarity +0.06 | 20p, 25 min, 0.06 | `sr(20,!0)` | read |
| Paper: 20p | 20p | `tf(x.story.flags.dead` | read |
| Spending takes dirty money first, unless clean is required | n/a | `function sr(` | read |
| Beaten down: wakes at Grace's, pays up to 8.00 from clean | 800p | `Math.min(t.clean,800)` | read (notes also say half the tin if carried; not traced) |
| No wages found | none | n/a | not found |

## 5. Suspicion and police

| Rule in plain words | Number(s) | Search | Confidence |
|---|---|---|---|
| Each morning at 04:00 (from Tuesday), statements are taken for the previous day's crimes | 04:00 | `e>=4&&i>=1&&Yx(i-1)` | read |
| A witness makes a statement only if: saw it or was there (not told or heard), named him, sure at least 0.55, fear under 0.5, not paid, and liking at most 0.05 (upright people) or -0.15 (others); people marked nostmt never do | 0.55, 0.5, 0.05, -0.15 | `a.sure<.55` | read (matches notes and the README police check) |
| nostmt people: Sheila, Ron, Darren, Ellis, Rita, Wayne, Lee, Hal, Dennis, PC Ibbotson (Father Walsh explicitly 0; Terry has no nostmt field, so he can make a statement) | list | `nostmt:1` (ten matches, one per person) | read |
| The most serious crime with a statement is chosen; violence (crime 2+) or running from police sends Ellis, otherwise the constable | crime 2 | `violent:n&&Wt[n.kind].crime>=2` | read |
| They come at 09:00 the same morning | 540 min | `(i+1)*1440+540` | read (notes: "a constable comes at nine") |
| Held 4 hours (5 for violence), +2 if he ran; Agar's brief bill 25.00 (40.00 if he ran), from clean, the rest owed to Agar; coat kept if worn; bag kept | 4/5, +2, 2500/4000p | `e.violent?5:4` and `t?4e3:2500` | read (notes say "four to seven hours, 25 to 40 pounds") |
| Running: they give up after 7 s out of sight, 70 m away or 60 s; it becomes a new offence | 7, 70, 60 | `t.lost>7||r>70||t.ct>60` | inferred (seconds) |
| Loudness = sum over everyone's bad memories naming him of heat x severity x badness (x0.6 if not by name) | formula | `function Ba()` | read |
| Ellis walks Quay Street on Thursday or Friday, 10:00 to 13:00, once a day, if loudness is 2.2 or more (or a killing); she asks up to 5 random locals, who remember being asked | 2.2, days 3-4, 5 people | `e<3||e>4` and `n<2.2&&` | read (matches notes) |
| Cammack's lads start trouble at night if loudness over 1.2 or he carries the bag or said no | 1.2 | `Ba()>1.2` | read |
| Fear rises when told or seeing a crime 2+ | +0.07 told, +0.18 seen, x(1.2 - nerve) | `e.src==="told"?.07:.18` | read |
| Liking moves by the act's value x 0.26 seen (0.15 told) x sureness, x1.4 for upright people on bad acts | 0.26, 0.15, 1.4 | `e.src==="told"?.15:.26` | read |

## 6. Time of day and routines

| Rule in plain words | Number(s) | Search | Confidence |
|---|---|---|---|
| One game hour is 45 real seconds (1.33 game minutes a second) | 60/45 | `i*60/45` | read (matches notes) |
| A new week starts Monday 15:36 | x.t 936 | `v:4,t:936` | read |
| The week is Monday 15 to Friday 19 October 1990; the end report runs to Saturday | dates in notes | `["Calendar and clock"` | read (notes) |
| Hold Z to pass time; the clock stops in talk and reading | n/a | `["Calendar and clock"` | read (notes) |
| Weather changes from a list by hour, rain and mist blend over about 25 seconds | n/a | `["mist","drizzle","drizzle","rain","dry","heavy"]` | read |
| Each named person has a day schedule of (hour, place, activity); some have day-specific extra rows | e.g. Ron: home asleep 00:00, caff 06:36, the rank 08:06, fish queue 12:18, rank 12:48, Tang's queue 17:24, rank smoking 17:54, home asleep 23:36 | `id:"ron"` then `sched:` | read |
| Other schedules read (first rows only; see bundle for day variants) | Sheila office 07:30 to 18:12 with caff 12:30; Darren caff 09:00, pavement, market 13:00, phone box 18:00, video shop 20:00, corner 22:00, home 23:42; Ada at her window 05:30 to 22:36; Julie bus stop 08:30, market edge 09:36, caff 11:00, window 12:30, bus 14:00, grocer 16:00, home 16:48; Brenda fish shop 07:24 to 17:24 then window; Grace caff 06:00 to 17:12; Albert nets 06:30, window 17:36 | `sched:[` (30 blocks: 28 named people plus the fare passenger and the yard lad; corrected 18 Nov) | read |
| 28 named people (corrected 18 Nov; first read said 31), each with nerve, talkativeness, discretion, upright, local, close friends | e.g. Sheila nerve 0.95 talk 0.15 discretion 0.92; Darren 0.3 / 0.95 / 0.05; Ron 0.85 / 0.7 / 0.35 | `id:"sheila"` | read |

## 7. Talk

| Rule in plain words | Number(s) | Search | Confidence |
|---|---|---|---|
| Tab opens and closes the suggested lines; arrows choose; Enter says; F2 opens the slip | keys | `i==="Tab"?(V.open` | read |
| At most three suggested lines: a decision's yes/no plus a keep-talking line, or greet/follow, personal, leave | 3 | `e.length<3&&t.keep` | read (matches README talk check) |
| Only a yes decides; a no or other words decide nothing | n/a | `["Talk pass: decisions"` | read (notes) |
| Live talk: two calls per line (intent, then voice), a third for Tom's follow-up; fall back to the written line on failure or delay; a word filter | n/a | `["Live talk"` | read (notes only; timeout not traced) |
| A live reply is cut to three sentences and 380 characters | 3, 380 | `e.slice(0,3).join("").trim()),i.slice(0,380)` | read |
| A name is learned when it is said in talk | n/a | `function om(` area: `new RegExp("\\b"+r+"\\b")` | read |
| Talking costs 1.5 game minutes per exchange | 1.5 | `x.t+=1.5,await` | inferred |

## 8. Saving

| Rule in plain words | Number(s) | Search | Confidence |
|---|---|---|---|
| Save version 4; any other version is refused | 4 | `e.v!==4` | read |
| Saved to the browser (key ledger.save.v4) and, when signed in, to the Claude account database in chunks of 150,000 characters | 150000 | `hw=15e4` | read |
| On loading, the newer of browser and account saves wins (by time stamp) | n/a | `t(e)>t(i)?e:i` | read |
| Autosave to the browser only every 75 real seconds of play; full save on sleeping, after beats and from pause | 75 | `fw>75` | read |
| What is saved: time, weather, Tom, car, minds (without their index), events, sightings, tellings, Ledger, log (last 600), money, debts, story, stats; a fare or Ellis walk in progress is dropped | list | `var gT=["v","t","played"` | read |
| Restore through the test hook does not rebuild people's memory index; the game's Continue does (qd()) | n/a | `function dw(` vs `qd(),x.story.phase="play"` | read (explains the README expected failure) |

## What could not be found or was not traced

- Wages: none exist in the prototype; Tom's only income is fares, jobs and collected debts.
- Debt due times: debts carry only an amount and a state; there is no due date or interest. Julie's "till Thursday" is a line only.
- The exact light field values (lightAt) and the line-of-sight geometry (los) are in the renderer, not read.
- The routine walker (how people move between schedule rows, the Ron stop at the rank) was not read.
- Fighting rung thresholds (nerve against rung) were not read beyond the notes.
- Live-talk timeout and the word filter list were not read.
- Job 3's 100.00 pay and "half the tin" when beaten were seen in the notes only.
- The day-specific schedule rows were not unpacked.

## Where the prototype disagrees with the design documents (noticed, not exhaustive)

- Clock: the prototype runs one game hour in 45 real seconds; rumour-reach-2026-09-23.md records the C# game at 2 game minutes a second (30 seconds an hour).
- Talk distance and rounds: prototype 4.8 m on the street (8 m indoors), a round every 4 game minutes with a closeness chance; C# 6 m, a round every 6 game minutes.
- Passing a story on: both cut certainty by 0.8 a telling, but C# also multiplies by friendship strength and drops anything under 0.2, so a second retelling almost never happens; the prototype has no friendship multiplier and no floor on certainty (only heat under 0.12 stops it), so stories can travel several hops.
- Fading: C# halves certainty every 96 game hours; the prototype never fades certainty and instead halves heat in about 20 game hours.
- Arrest: arrest-2026-09-29.md has about six hours for a minor offence (two if he owns up), eight for a wounding, twelve for a robbery, a caution if he owns up, else charged and bailed; the prototype holds 4 or 5 hours (+2 if he ran), no charge, and Agar's firm sends a 25.00 or 40.00 bill.
- Debts: counterparty-purses-spec.md speaks of Rita owing 180 (in dollars, and a pub's takings); the prototype's book has Wayne (Rita's side) at 30.00, no Rita debt, and no purse for debtors (a debtor either pays in full or refuses).
- Rent: the line says "Friday, by six"; the code marks it late only from Saturday 00:00 (small, inside the prototype).

## Is Fable's readable source still needed?

Yes. The bundle reads better than expected: the game's own design notes state most rules, and the constants above were found and match those notes in nearly every case. But every name is shortened, the routine walker, light and line-of-sight code, fighting and live talk were not read, and a hand reading can miss a rule hidden in a branch. Fable's source, as written before bundling, is still the only way to make these rules the spec of record. Until then this file is a reading aid and a list of numbers to check, nothing more.

## Round two (18 Nov)

Status: UNVERIFIED, like everything above. Read the same way (joined copy pretty-printed with js-beautify outside the repository; src/ not touched). Every search string was checked with a plain fixed-string search (grep -F) in the joined original ledger.js; each occurs once unless the row says otherwise. Strings were chosen without the bar character where possible so the tables render.

Units as above. "dt" is real seconds per tick (the game ticks in steps of up to 0.05 s). Positions are metres on the street map; x above 900 means inside a room.

### 9. Light map

| Rule in plain words | Number(s) | Search | Confidence |
|---|---|---|---|
| Light is a grid over the street, four layers: street lamps, windows lit all night, windows lit late, windows lit early | cells 0.75 m | `ho=.75` | read |
| A window joins a layer by its closing hour: 30 or more all night, over 22 the late layer, otherwise the early layer | 30, 22 | `E5=i=>i.until>=30?1:i.until>22?2:3` | read |
| Each light adds to the cells around it, falling off to its edge; full strength 1 for a lamp, 0.55 for a dim one, 0.8 for a window | add = k x (1 - d/r)^1.5 x 0.95, capped at 1 a cell | `e.k*Math.pow(1-u/e.r,1.5)*.95` and `k:e.dim?.55:1` | read |
| A wall between the light and a cell (beyond 1.5 m) leaves only 6 percent | 0.06 | `u>1.5&&!Z0(e.x,e.z,l,h)&&(d*=.06)` | read |
| Twelve dark patches (alleys and doorways) keep only 12 percent of any light | 0.12 | `E2=[Ue(7.2,-.5,8.2,3.5)` and `d*=.12;break` | read (that they are alleys and doorways is inferred from the places) |
| 32 street lamps: Quay Street both sides about every 16 to 19 m (radius 13), eight along the waterfront, the market lanes (radius 12), the ferry lamp (radius 10), two dim ones | radius mostly 13 | `[5.7,38],[-5.7,22]` and `.forEach(i=>ms(i,43.2))` | read (count by hand) |
| Ten lit windows, e.g. Rita's till 00:36 (radius 7), Tang's till 23:30 (radius 8), Mickey's and the brazier all night, two shops till 19:00 and 20:00 | as listed | `x:6.6,z:-29,r:7,col:"w",until:24.6,id:"rita"` and `until:23.5,id:"tangs"` | read |
| Light at a spot = daylight + lamps on x (lamps + all-night windows) + late x late windows + early x early windows, capped 0 to 1; indoors always 0.85 | daylight = 0.07 + 0.93 x (1 - night) | `function j2(i,e,t){if(t&&t!=="street")return .85` and `day:.07+.93*(1-e)` | read |
| Lamps come on as night passes 0.3 and are full at 0.55 | on = (night - 0.3) / 0.25, 0 to 1 | `t=ue((e-.3)/.25,0,1)` | read |
| Late windows are lit 16:30 to 23:36 and before 00:36; early windows 15:30 to 19:30. Each window's own closing hour only picks its layer, so Rita's (00:36) and Tang's (23:30) both follow the layer's hours | 16:30 to 00:36, 15:30 to 19:30 | `i>=16.5&&i<23.6` and `s=i>=15.5&&i<19.5?1:0` | read (the mismatch with each window's own hour is a reading, not tested) |
| The ferry lamp goes out 23:00 to 05:00 and its patch is taken back out of the lamp layer | 23 to 5 | `o=i>=23` and `r<Zo.r&&(s=Math.max(0,s-Math.pow(1-r/Zo.r,1.5)*.95))` | read |
| The light word shown: under 0.2 "IN THE DARK", under 0.5 "HALF LIT", else "IN THE LIGHT" | 0.2, 0.5 | `Z2=i=>i<.2?"IN THE DARK":i<.5?"HALF LIT":"IN THE LIGHT"` | read |

### 10. Line of sight

| Rule in plain words | Number(s) | Search | Confidence |
|---|---|---|---|
| The game's line-of-sight and light are these two functions | n/a | `x.env.los=Z0,x.env.lightAt=j2` | read |
| Sight is blocked only by building boxes (flat rectangles, no height); people, cars, lamp posts and the dark do not block it | n/a | `k2=ps.concat(Dd)` | read |
| The test is a segment-against-box clip; any box the segment crosses blocks | n/a | `function A2(i,e,t,n,s)` | read |
| Anyone inside a room (x over 900) is always "in sight" by this test; rooms rely on the other checks | 900 | `function Z0(i,e,t,n){if(i>900||t>900)return!0` | read |
| A leftover check in the loop does nothing (it reads a field and throws it away) | n/a | `c.st===1&&c.k` | read (harmless) |

### 11. The routine walker

| Rule in plain words | Number(s) | Search | Confidence |
|---|---|---|---|
| Where a person should be: the latest general row at or before the hour, unless today has a day-specific row at or after that row's hour; a temporary order (override) beats both until it runs out | day = game day mod 7, Monday 0 | `function V1(i,e=Ve(),t=Ze())` and `r[3]?r[3].includes(t%7)` | read |
| A new plan starts a walk only when the place or activity changes, and never while the person is "held" by a scene, a fight or a fare | n/a | `s!==i.goalKey&&!i.hold` | read |
| Home is the spot just outside their window (0.9 m out), or a named spot (default Chapel gate) if they have no window | 0.9 m | `gs[i.def.homeSpot||"chapelgate"]` | read |
| Path finding: A star over a hand-made walking graph (pavements both sides of Quay Street, the waterfront, side streets, the market lanes), nodes every 6 to 10 m, plus any two nodes under 2.6 m apart joined | 6 to 10 m, 2.6 m | `function Fd(i,e){if(i===e)return[i]` and `We(yt[i].x,yt[i].z,yt[e].x,yt[e].z)<2.6&&xi(i,e)` | read |
| Walks under 6 m go straight; longer ones go to the nearest node, along the path, then straight to the spot; the first and last nodes are dropped if they would mean doubling back | 6 m, 0.6 m | `if(We(s,o,r,a)>6)` and `u.length>1&&We(s,o,yt[u[1]].x` | read |
| Each person keeps a lane, a sideways offset so walkers do not all tread one line | offset -0.42 to +0.42 m | `i.lane??(i.lane=_t(-.7,.7))` | read |
| If no path is found the route is simply start node then end node (a straight line) | n/a | `return[i,e]}` | read |
| Walking speed 1.35 m/s, 1.1 over 60, 0.95 if frail, times any hurry (fleeing 2.6x); 3.2x faster when more than 90 m from Tom or in another space | 1.35, 1.1, 0.95, 3.2, 90 m | `i.def.frail?.95:i.def.age>60?1.1:1.35` and `(t?1:3.2)` and `s.space===e.space&&We(s.x,s.z,t,n)<90` (twice, named and crowd) | read |
| Near Tom a walker passes at most one path point per tick | n/a | `if(i.x=s.x,i.z=s.z,r-=l,n.legs.shift(),s=n.legs[0],t)break` | read |
| Walkers do not collide with walls, people or the car; there is no stuck check, no re-plan and no time-out on a walk | none found | n/a | read (absence) |
| A walker stops in place while "paused"; a pause is set each time a moving person sees one of Tom's acts within 26 m: 0.9 + 1.6 x the act's severity, in real seconds; they stay marked as walking | 26 m, 0.9 + 1.6 sev | `!i.fight&&!i.lad&&t.d<26&&` and `.9+1.6*a.sev` and `i.pauseT>0&&(i.pauseT-=e,i.moving&&!i.fight)` | read |
| Ron is held on the rank on Monday from 17:12 until Tom has been asked about the bag (each hold lasts 400 game minutes and is renewed while the condition stands); on Wednesday 16:18 to 22:00 the one who asks about Iveson (Ron if Tom said yes on Monday, else Darren) is held on the rank or pavement for 300 minutes at a time. Answering does not cancel a hold already running | 400, 300 min | `Hr(it("ron"),"rank","idle",x.t+400)` and `Ze()===2&&Ve()>=16.3` | read |
| Shop keepers stand in their shop 08:00 to 18:00 and are gone otherwise | 8 to 18 | `Ve()>=8&&Ve()<18` (twice, same use) | read |
| Passers-by: how many are out by hour: 1 before 05:00, 3 to 06:30, 9 to 08:00, 16 to 18:00, 10 to 21:00, 5 to 23:30, 2 after; each walks node to node, waits 4 to 26 s, and leaves by a town exit with chance 0.25 or when over the hour's number | as listed | `function Y1(){let i=Ve();return i<5?1:i<6.5?3:i<8?9:i<18?16:i<21?10:i<23.5?5:2}` and `_t(4,26)` | read |

#### Hypothesis for Ron stopping about 3 m from the rank after 23:36 (unverified)

The lane's check (tools/lane/prototype/tests/systems2_test.py, test_3b2) found Ron with the right plan ("home, sleep"), a route, marked as walking, standing at about x 6.4, z 35.2 until at least 03:00. That rules out the Monday rank hold (his plan would read "rank, idle") and a blocked path (walkers pass through walls).

Likely cause: the witness pause never runs out while he can see Tom. From 23:30 to 05:00 Tom being out on the street at all counts as an act ("night out", severity 0.35): `S1=(i=Ve())=>i>=23.5` and `S1(e)?"night_out"`. A watcher's attention builds at (0.45 + 1.4 x clarity) x 1.5 per real second and on reaching 1 the sighting is recorded again and attention goes back to zero (`r.attn=0,t)`), so a moving watcher in clear view is re-paused every 0.36 s (close and lit) to 1.3 s (at the edge of sight). Each sighting sets the pause to at least 0.9 + 1.6 x 0.35 = 1.46 s (`.9+1.6*a.sev`). The pause is always topped up before it ends, so Ron never takes another step while Tom stands within 26 m and in his sight, and he stays marked as walking (`i.pauseT>0&&(i.pauseT-=e,i.moving&&!i.fight)`).

It fits the facts: he is still and smoking on the rank until 23:36 (not moving, so no pause), sets off, gets about 3 m toward the first point of his path (the Quay Street node at x 6.4, z 35.7, shifted up to 0.42 m by his lane) in the second or so before his attention first fills, and is then held. By day his walks arrive because Tom's being out is not an act by day. The rank to the second rank spot (rank2) is also 2.9 m, which may be why "3 m from the rank" looked like a place.

To confirm: in the same check, move Tom indoors or more than 26 m away at 23:40 and see Ron go on; or read pauseT on Ron, which should sit between 0 and 1.46 and never reach 0. The same freeze would hit anyone walking near Tom while he carries the bag, wears the coat by day or runs in daylight. A fix for Fable: set the pause only on the first sighting of an event, or not top it up while it is running.

### 12. Fighting

| Rule in plain words | Number(s) | Search | Confidence |
|---|---|---|---|
| The ladder: 1 stare, 2 square up, 3 threaten, 4 shove, 5 strike, 6 weapon out; R steps up, X walks away | 6 rungs | `Mt("No. Not "` area (ladder names in `TI`) | read |
| Who he fronts: the nearest person within 3.6 m and about 69 degrees of his facing; named people count 1.2 m nearer, anyone with a mark 1 m more | 3.6 m, 1.2 rad | `n.anon?0:1.2` | read |
| Women, the frail, anyone 60 or over and Father Walsh: he will not go to rung 4 with his hands; a nearby lad of theirs steps in instead, or nothing happens | age 60 | `i.id==="walsh"` and `Mt("No. Not "` | read |
| Rung 4 on a police officer is assault and an arrest on the spot | rung 4 | `n.police&&s>=4` | read |
| Pressure at each rung: 0, 0.18, 0.32, 0.5, 0.66 for rungs 0 to 4, plus their guilt (below), plus 0.3 if armed, minus 0.16 for each friend of theirs within 9 m, minus 0.25 x his hurt | as listed | `[0,.18,.32,.5,.66][s]+Ud(i)+(e.armed?.3:0)-o.length*.16-e.hurt*.25` | read |
| Guilt: 0.12 x sureness for each crime they believe of him that is clearly bad (x1.6 for crime 2 and up), capped 0.45 | 0.12, 1.6, 0.45 | `e+=.12*t.sure*(n.crime>=2?1.6:1)` and `return Math.min(.45,e)` | read (that it measures what they know of him is inferred) |
| They give way if pressure beats their nerve (+0.12 for Cammack's lads): fear +0.14 x rung, liking -0.1 x rung; a demand is met from rung 2 | nerve, 0.12, 0.14, 0.1 | `r>(n.nerve??.5)+(i.lad?.12:0)` and `t.fear+.14*s` | read |
| If they hold: at rung 4 it comes to blows; at rung 3 a lad or yard lad with nerve over 0.7 swings first 60 percent of the time | 0.7, 0.6 | `Sn(.6))&&Vm(i,!1)` | read |
| Rungs 3 and up make a noise of 14 m; the shove pushes them 1.2 m back | 14 m, 1.2 m | `noiseR:s>=3?14:0` | read |
| Friends who join: Cammack's lads with each other, Dennis with his yard lad, within 9 m | 9 m | `We(t.x,t.z,i.x,i.z)>9` | read |
| Before blows, walking more than 7 m off ends it | 7 m | `(n>7||t.gone)&&Xa()` | read |
| Tom's stamina: +0.13 a second, -0.05 a second while blocking; a light blow costs 0.15, a heavy 0.28; under 0.15 he cannot swing | 0.13, 0.05, 0.15, 0.28 | `z.st==="block"?-.05:.13` and `z.stam<.15` | read |
| Tom's blow: wind-up 0.2 s (heavy 0.55); lands within 1.75 m and about 52 degrees; a guarding foe blocks 36 percent of light and 15 percent of heavy blows; recovery 0.28 or 0.45 s if it lands, 0.6 or 0.95 s and an opening if it misses | as listed | `o&&r<1.75&&Math.abs(_n(e.ang,Math.atan2(o.P.x-e.x,o.P.z-e.z)))<.9` and `Sn(z.heavy?.15:.36)` | read |
| Tom's damage: 0.15 light, 0.3 heavy, times the weapon (cosh 1.7, flick knife 2.1, brick 1.6, chair 1.5, wheel brace 1.8, cargo hook 1.9, dustbin lid 1.1, else 1.5), times (1 - 0.3 x his hurt) | as listed | `z.heavy?.3:.15` and `cosh:1.7,"flick knife":2.1,brick:1.6,chair:1.5,"wheel brace":1.8,"cargo hook":1.9,"dustbin lid":1.1` | read |
| A foe's hurt is capped at 1.2; down at 1. On his first hit, a foe with nerve under 0.4 runs 60 percent of the time | 1, 1.2, 0.4, 0.6 | `+e,0,1.2)` and `(n.def.nerve??.5)<.4&&Sn(.6)` | read |
| When one goes down, each other foe with nerve under 0.85 runs 60 percent of the time; a staggered foe over 0.75 hurt with nerve under 0.9 runs half the time | 0.85, 0.6, 0.75, 0.9, 0.5 | `(h.P.def.nerve??.5)<.85&&Sn(.6)` and `>.75&&(l.def.nerve??.5)<.9` | read |
| Each hit on a foe: fear +0.12, liking -0.25; first strike makes a noise of 26 m | 0.12, 0.25, 26 m | `n.mind.fear=ue(n.mind.fear+.12,0,1),n.mind.regard=ue(n.mind.regard-.25,-1,1)` | read |
| Foes close in at 2.4 m/s to about 1.25 m, spread around him; wind-up 0.5 s (heavy 0.75 s, 30 percent of swings); they hit within 1.9 m unless he steps back; rest 0.7 to 1.6 s between swings (+0.5 if more than one) | as listed | `let d=2.4*i` and `c.heavy=Sn(.3),c.t=c.heavy?.75:.5` and `c.t=_t(.7,1.6)+(s.length>1?.5:0)` | read |
| Their damage to Tom: 0.125 light, 0.23 heavy, x1.7 with a weapon, x(1 - 0.3 x their hurt); a block he faces cuts it to 15 percent (3 percent with a dustbin lid) and costs 0.12 stamina; hit during his opening x1.5 | as listed | `(c.heavy?.23:.125)*(l.weapon?1.7:1)*(1-(l.hurt||0)*.3)` and `z.stam-=.12` and `z.open>0&&(d*=1.5)` | read |
| Tom is beaten at hurt 1 | 1 | `e.hurt>=1){It("beaten"` | read |
| Step back (Space): 1.6 m, then 0.9 s before the next | 1.6 m, 0.9 s | `e.x-Math.sin(e.ang)*1.6` and `z.cool=.9` | read |
| Weapon out (rung 6): each foe whose 0.55 + guilt beats nerve + 0.25 runs | 0.55, 0.25 | `.55+Ud(e.P)` | read |
| A kill (V) needs a weapon out and a downed foe within 2 m | 2 m | `e=z.foes.find(n=>n.st==="down"&&We(n.P.x,n.P.z,i.x,i.z)<2)` | read |
| It ends when he is more than 16 m from them, or 1.2 s after all foes are down or gone (6 s if a downed foe lies near him and he is armed) | 16 m, 1.2 s, 6 s | `r>16&&Xa(!0)` and `z.endT>(c&&e.armed?6:1.2)` | read |
| A runner goes home (or off) for 300 game minutes, hurrying 2.6x, fear +0.3; a downed one gets up after 25 game minutes, goes home for 600, hurt 0.7, then heals very slowly | 300, 25, 600 min, 0.7 | `act:"sleep",until:x.t+300},i.goalKey="",i.mind.fear=ue(i.mind.fear+.3,0,1)` and `t.downT=x.t+25` and `until:x.t+600` | read (healing rate per tick not converted) |

### 13. Live talk: time limits and word filter

| Rule in plain words | Number(s) | Search | Confidence |
|---|---|---|---|
| The line Tom types is first read by built-in word rules (bribe, threaten, lie, agree, refuse and so on, and the topic); the model's reading replaces it only if it answers with one of eight known intents | 8 intents; offered money capped 0 to 500 pounds | `BI=["ask","smalltalk","threaten","bribe","flatter","lie","refuse","agree"]` and `Math.max(0,Math.min(500,+o.amount||n.amount||0))` | read |
| Time limits: reading Tom's line 9 s, the character's reply 14 s; no limit on the very first call (so the permission question can be answered) | 9 s, 14 s, first call none | `V.consent?9e3:0` and `V.consent?14e3:0` | read |
| Suggested follow-up and personal lines from the model: dropped after 6 s, only after the first call and once talk has begun | 6 s | `cS(o&&o.follow)` and `},6e3)` | read |
| All three calls use the quick model tier | quick | `modelTier:"quick"` (three times, one per call) | read |
| Busy (rate limited): live talk rests 60 s; permission refused, switched off or session ended: live talk is off for the session and people use written lines | 60 s; six error kinds | `V.cool=Date.now()+6e4` and `"not_granted","sampling_disabled","not_declared","capability_disabled","capability_removed","session_expired"` | read |
| The reply prompt carries the content rules, the character's card, how they feel about him (liking and fear in words), his eight hottest memories they hold, the last six lines of talk, and the outcome the game has already decided | 8, 6 | `hS=` then `ABSOLUTE CONTENT RULES` and `.slice(0,8)` | read |
| Clean-up: strips stars, quotes, brackets, a leading "Name:", turns dashes into commas, then three sentences and 380 characters | 3, 380 | `e.slice(0,3).join("").trim()),i.slice(0,380)` | read |
| Word filter: a reply containing any of these words is thrown away and the written line used: pint, beer, lager, whisky, whiskey, vodka, brandy, wine, booze, boozer, drunk, hangover, betting, bookie, bookies, gamble, gambling, the horses, casino, child, children, kiddies, toddler, baby, babies, schoolboy, schoolgirl, pupil, heroin, cocaine, cannabis, internet, mobile phone, email (whole words, any case); while streaming, a filtered piece shows blank | 34 words or phrases | `Nx=/\b(pint|beer|lager` and `Nx.test(o)` | read |
| A suggested line is also refused if over 12 words or 96 characters, already used, filtered, or if it names Tom | 12 words, 96 characters | `i.length>96` and `/\b(tom|tommy|thomas|nowak)\b/i` | read |
| Every fallback to a written line is counted, as is every live answer | n/a | `x.stats.fallback++` and `x.stats.live++` | read |

### 14. Day-specific schedule rows

Only three people have them. A day row wins from its hour until the next general row that is later.

| Rule in plain words | Number(s) | Search | Confidence |
|---|---|---|---|
| Ada, Wednesday: chapel 08:00, back at her window 09:12 | day 2 | `[8,"chapel:p1","sit",[2]]` and `[9.2,"home","window",[2]]` | read |
| Ada, Friday: fish queue 10:00, back at her window 10:42 | day 4 | `[10,"fish:q2","queue",[4]]` and `[10.7,"home","window",[4]]` | read |
| June, Monday: at Mickey's 13:30 (instead of the bench) until her general 14:00 row; boarding house 17:36 (instead of the ferry) until 19:00 | day 0 | `[13.5,"mickeys:june","idle",[0]]` and `[17.6,"boarding:june","sit",[0]]` | read |
| Julie, Monday and Wednesday: laundrette 08:30 instead of the bus stop, until 09:36 | days 0 and 2 | `[8.5,"laund:b2","sit",[0,2]]` | read |
| No other person, Ron included, has a day row; Thursday and Friday differ only through story holds (Ellis's walk, Sheila on Friday, the Wednesday ask) | n/a | search `sched:[` (30 occurrences in the bundle; 28 schedules were listed in this round, the rest not identified) | read |

### Still not read or not settled after round two

- How the test's own Tom position at 23:36 sits against Ron's sight; the Ron hypothesis is a reading, not a run.
- The "Tuesday night pause" found by the lane's check was not looked for in this round.
- The fixed light map is built once from fixed lamps; whether the renderer's lamp textures match these numbers was not checked.
- Tom's starting stamina and the exact wording of every ladder line were not copied.
- Live talk: the built-in word rules for intent were read in outline only (the bribe, threat, lie and agree word lists are in `function zI(` area, not copied here).
