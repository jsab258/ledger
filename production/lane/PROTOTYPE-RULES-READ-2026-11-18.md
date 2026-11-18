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
| Each act has a severity, a moral value and a crime level (0 to 3); 45 kinds, from arrive (0.3) to kill (1.0, crime 3, never fades below 0.6 heat) | table | `inherit:xt(.5,0,0` | read |
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
| Other schedules read (first rows only; see bundle for day variants) | Sheila office 07:30 to 18:12 with caff 12:30; Darren caff 09:00, pavement, market 13:00, phone box 18:00, video shop 20:00, corner 22:00, home 23:42; Ada at her window 05:30 to 22:36; Julie bus stop 08:30, market edge 09:36, caff 11:00, window 12:30, bus 14:00, grocer 16:00, home 16:48; Brenda fish shop 07:24 to 17:24 then window; Grace caff 06:00 to 17:12; Albert nets 06:30, window 17:36 | `sched:[` (31 people) | read |
| 31 named people, each with nerve, talkativeness, discretion, upright, local, close friends | e.g. Sheila nerve 0.95 talk 0.15 discretion 0.92; Darren 0.3 / 0.95 / 0.05; Ron 0.85 / 0.7 / 0.35 | `id:"sheila"` | read |

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
