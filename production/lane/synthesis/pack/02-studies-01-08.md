# Pack 02: Studies 01 to 08 (digest)

Source folder for every item: production/research/aaa-reference/studies/. Each study is named by file; sections are named in brackets.

Reading rules for this digest:
- Part a of each section is copied word for word from the study. The copied blocks are inside quotation rules (lines starting with ">"). Their numbers that the study took from a game's own files are leads, not evidence, even where the copied text does not repeat the mark.
- Part b marks every number the study read from a game's own files (extracted data, configs, game files) as "(lead, from game files)". Numbers from reviews, talks, interviews, public pages and LEDGER's own files stand as they are, with their source named.
- Study tags in the originals: M measured from the data, R read in a file or a named page, I inferred, N a name only. Where a study tags "R" without saying file or wiki, this digest says so.
- The studies hold no recordings (ruling of 25 October); every minute, loudness or feel claim is unplayed.

---

## Study 01: NPC life and AI (25 October 2026)

Source: studies/01-npc-life.md. Games: Kingdom Come: Deliverance II (KCD2), Mafia: The Old Country. Method: the games' own data; engine code not read; part of the KCD2 figures come from Warhorse's modding wiki (KM-A-93 scheduler links, KM-A-27 crime, KM-A-20 RPG constants). Reviewed once (pass with fixes).

### a. For LEDGER (the study's "What LEDGER already does" and "What to adopt", in full)

> ## What LEDGER already does, and how it differs
>
> - Named residents keep hour-by-hour routines (CastDay). Talk passes only where routines meet, within six metres; confidence falls each hop; each person knows who told them; rumours fade on a 96-hour half-life, a body never (Gossip). Kingdom Come II also passes crime information to friends and through factions, but by broadcast: it has no who-told-whom, no falling confidence and no need to meet.
> - Witnesses walk to report, can be stopped on the way, and what they report becomes permanent only on arrival (Witnesses, the delivery window). The law can be pointed at others (Informing).
> - Perception has a wider cone than either game (its outer part sees only movement). Its range is shorter than Kingdom Come II's longest (40 m against 50 m), and up close it is not faster than Mafia's guards.
>
> ## What to adopt
>
> 1. **Crime expiry by kind** (1 to 7 days, from Kingdom Come II's table) in place of the single 96-hour half-life, the body staying as it is. The spread stays by routine meetings: Kingdom Come II's daily faction broadcast would break canon ("gossip spreads through schedule intersections"), so it is not adopted.
> 2. **Make the witness's walk visible in the game:** the simulation already does it; the item is seeing a witness go to someone and hand it over, in the Unreal game.
> 3. **Benches, tables, doors and beds as places in the routine,** each seat its own slot with a cap and an owner: Tom's bench (item 2, this week) uses the first seats file; residents next, through the same file.
> 4. **For the crowd, not the named:** a few clock windows and priority for the rest (Kingdom Come II times 3.4% of links); the hours from LEDGER's own research on a 1990 British town, not a medieval one. Named residents are already fully timed in CastDay.
> 5. **What gives you away:** dirt, blood, a drawn weapon, the wrong clothes for your class; running already counts in LEDGER.
> 6. **Detail by distance:** full detail for the nearest, freeze the unseen beyond 70 m (Study 12).

### b. Key measured numbers

The study's short answer: KCD2 simulates a town (home, bed, working day, class; crimes become information that witnesses carry); Mafia stages a town (people loop one activity where they stand, react in the moment, forget). Source for all rows: 01-npc-life.md [The numbers; Daily life; Usable objects; Crowds and detail; Noticing; Witnesses].

Schedules and activities
- KCD2 scheduler, Kuttenberg's map: 64,529 places, 117,225 links; both maps 86,162 places and 159,787 links (lead, from game files: scheduler.xml).
- 3.4% of links carry a clock window (4,005 links; 299 windows, median 12 h); the rest chosen by priority, stay time, role, class and weather (lead, from game files).
- KCD2 links end in 1,123 behaviours (lead, from game files). Weather filters 2,289 links: 1,399 sun only, 890 rain only (lead, from game files).
- Commonest windows 08 to 20 (696 links) and 07 to 19 (640); 1,981 timed links vary by 30 min either way (lead, from game files).
- Timed links live at midday about 2,600 to 2,760, against 340 to 450 between midnight and five, six to seven times more (lead, from game files).
- One traced townswoman: bed by class (12 h); 08:00 to 09:00 wash, eat, fetch wood, collect eggs; 19:00 to 23:00 bench in sun, indoors in rain, or tavern seat (lead, from game files).
- Kutná Hora: 53 households of median 4; 1,256 beds for about 1,320 humans (lead, from game files; the "nearly everyone sleeps indoors" step is inferred). 726 fillers come out through a door by day (hours unverified).
- Mafia: no schedule key found in AI, interaction, spawner or character data (lead, from game files). 389 looping scenes, 478 slots, none ending or cooling down; 374 scenes carry their own person (lead, from game files). Walkers patrol a path with 60 s stops (read; file or wiki not split).
- Mafia: 52 smart-object definitions; 290 objects with one slot, 22 with two, 11 with three (lead, from game files). 422 spawn definitions (lead, from game files).
- KCD2: 1,256 beds, 1,279 tables, 1,041 benches, 442 chests in the town (lead, from game files); 16 named streets, median 1,286 scheduler places each (range 436 to 2,995) (lead, from game files).
- KCD2 claiming: 2,254 links cap their users (1,694 at one); 829 can push the current user off; 5,995 cannot follow themselves (lead, from game files, with wiki reading).

People and detail
- KCD2 Kutná Hora: 1,354 people (1,171 stock faces, 151 named, 32 animals) (lead, from game files). A filler has a home link with priorities 0 to 5; a named person up to 144 links, story priorities 45 to 200 (lead, from game files). 6,038 dress, voice, ability and name rules (read; file or wiki not split).
- KCD2 full detail: 70 people within 150 m (80 within 180 to 220 m at top levels; 300 lighter on smallest console); update budget 3.5 (2.5 in performance modes; unit unverified); the dead replaced after 7 days (3 for public enemies); undiscovered bodies vanish after an hour (read; file or wiki not split, treat as a lead).
- Mafia: civilians simplify from 10 m, pause look-at beyond 32 m, freeze unseen beyond 70 m after 3 s, never within 10 m, removed 5 m out of view; set-piece crowds 14 set-ups (lead, from game files).
- Mafia named definitions: 176; 78 use civilians' controller, 46 the companion's, 77 have reactions off for their scenes (lead, from game files).

Noticing (comparison table)
- KCD2: field of view 90 to 100 degrees plus 1 degree per hearing point; range 2.5 to 50 m; at once within 2.5 m; recognising about 4 s neutral, 2 s high, 8 s low (inferred, combined from constants); night outdoors -0.7, indoors -0.5, fog -0.5, tall grass -0.35; dirt over 0.9, blood, health under 30, smell, drawn weapon, no torch at night give you away (lead, from game files, with wiki).
- Mafia: civilians 80 degrees (40 each side), 25 m, hearing 50 m (lead, from game files). Guard investigates in about 0.15 s and turns hostile in 0.30 s at 3 m, 0.51 s at 10 m, 3.6 s at 19.5 m, against a walking player, never from behind (inferred, reproduced from its curves) (lead, from game files). Facing x1.6 ahead, x0.1 side-back, 0 behind; trespass zones x10.
- LEDGER column (LEDGER's own files): 120 degrees, outer 60 sees only movement; 40 m; face at 8 m, recognised at 25 m; glance to look 0.35 s (0.7 s if still, 1.0 s at edge of view); 1.2 s to identify; running x2, still x0.5.

Crime, memory and talk (KCD2; read, file or wiki not split, so each is also a lead)
- 30 kinds, 22 crimes, 9 violent, 25 can spread. Fines and jail: murder 20,000 and 7 days, assault 1,500 and 5, theft 500 and 3, trespass 250 and 1; 7 kinds rise with class.
- About 43 interruption kinds. Information carries 10 m (40 m long-range); alarms 25 m; reports within 15 m, up to 150 m (500 m important); 5 to 10 watchers at most; the fleeing keep 30 m away for 7 min.
- Kept a day times the crime's expiry of 1 to 7; re-broadcast through the faction tree once a day when the player is more than 30 m away.
- Reputation: weighted median of person, faction, wider faction at 5:3:1; reaches faction after about 3 h; nearby factions within 400 m take a quarter. Murder -0.6 to person / -1.5 when reported; theft -0.25 / -0.15; assault -0.3 / -0.3.
- Mafia keeps nothing: no wanted level, heat or gossip; civilians have three states; 9 arrest voice lines (lead, from game files).

### c. Open blind spots

- Both engines' code: scheduler scoring, the perception formula, units of time in script settings.
- Mafia's reaction rules, bark table, faction attitudes and cooldowns (compiled or not exported).
- People on screen per street by hour; usable objects per street; reactions to the player (greetings, stepping aside) and to noise; Mafia and weather.
- Only about 12 of KCD2's 308 crime behaviour trees were read, as outlines.
- Wiki defaults may differ from the shipped data.
- A wake-up hour earlier for villagers is unverified; hours for the 726 fillers unverified.

### d. The twenty basics

No mention in this study.

---

## Study 02: The first 30 minutes (28 October 2026)

Source: studies/02-first-30-minutes.md. Games: KCD2, Mafia. Method: game files (cutscene lengths, objective order, prompts, saves, failures) plus public pages; no recording, so every minute is an estimate (cutscenes plus spoken lines plus an allowance for play, low/middle/high). Reviewed (Opus, pass with fixes).

### a. For LEDGER (in full)

> ## For LEDGER
>
> 1. **Adopt: something new at least every three minutes,** counted in the tester's log. Both games manage about 10 activities and 10 to 12 prompts in 30 minutes. This makes "at most five empty minutes" checkable and orders P4's content list. Serves phase 3's exit and risk R6.
> 2. **Adopt: hints fired by the player's own hesitation,** not by the clock. KCD2 shows the walking hint only after 10 seconds without moving, and the attack hint after 20. LEDGER's four lines are clock-fired and all over within 90 seconds. Fire each on first need or after a pause, and keep it up for about 10 seconds. Serves phase 3's "prompts" and basic 7 (a hint for each key).
> 3. **Adopt: reveal the interface piece by piece,** from a table of story points, as Mafia does from checkpoints. Show the ledger, the clock and talk as each is taught. Serves basics 7 and 8 and phase 3's "useful office and ledger".
> 4. **Adapt: frequent autosaves that keep the town's memory.**
>    - Mafia's checkpoint every minute or two makes failure cheap; KCD2's sparse saves are PLAYERS.md's PUNISH 19.
>    - Autosave after every deed and every consequence. Reloading stays allowed, and the game says what is permanent.
>    - Serves D35, D58, basics 19 and 20, phase 3's "kept after restart", and his question on reloading to un-see a witness.
> 5. **Adapt: a named, cheap setback,** as in Mafia (named within 3 s, last checkpoint). In LEDGER it is social, named in the world, and costs at most two minutes; the detail is for Studies 11 and 15. Serves R6 and D35.
> 6. **Adapt: a soft edge.** Turn the player back inside the world, never fail them for leaving as Mafia does. Serves phases 2 and 3.
> 7. **Adopt: nudges when the player stalls.** KCD2 nudges after 2, 5 and 60 s idle and again after four minutes; Mafia uses nagging lines. Sheila or Ron speaks after a minute idle, and someone reminds Tom of the night's errand. Serves P4's item 7.
> 8. **Ignore: the long watched opening and the class pick.** KCD2 shows 40 minutes of cutscene before free roam, and a slow opening is players' PUNISH 4. RULINGS 23 Sep (few short skippable scenes) holds, and LEDGER has no stats (D11, D33, D34).
> 9. **Ignore as a template: consequence.** Neither game gives a newcomer a lasting consequence in 30 minutes, so LEDGER's own P4 run against these numbers is the only test. Serves R6.
>
> **Proposed benchmark for the friends' build:**
> - control within 1.5 min;
> - talk within 3;
> - a choice and a deed within 20;
> - no stretch over 3.5 min without control;
> - something new every 3 min;
> - a failure costs at most 2 min;
> - watching well under 29%.
>
> The producer decides.

### b. Key measured numbers

Source: 02-first-30-minutes.md [The measurements; The openings; Side by side]. Cutscene lengths are from game files (lead, from game files); the minute placements are estimates (I). Public-source rows keep their source.

- Newness rate: something new about every three minutes in both games; no stretch without anything new runs much past 5 min (inferred from file lengths plus estimates).
- First control: KCD2 at least 3.5 min (logo 13 s plus a 199 s video; lead, from game files; first objective about 1 min later per PowerPyx, public). Mafia 1.4 min after an 82 s cinematic (lead, from game files; placement inferred).
- Watching in the first 30 min: KCD2 8.4 to 13.1 min, 28 to 44% (lead, lengths from game files, placement inferred). Mafia 5.4 to 10.1 min, 18 to 34%, middle about 29% (lead, from game files, placement inferred).
- Watching before free roam: KCD2 40.4 min (44.4 with a 4-min vision; includes a 74 s scene on one path only); Mafia 35.0 min to Chapter 2's end (lead, from game files).
- Longest without control in first 30 min: KCD2 4.9 min (two videos); Mafia 3.5 min (one cinematic) (lead, from game files).
- Opening cutscene seconds: KCD2 13+199, 123+170, 263, 15, 176+199+27; Mafia 82, 73, 82, 43, 16+25, 207, 55+25+30+34, 67+40+19 (lead, from game files).
- Open world in KCD2 after the third quest, at 128 / 176 / 255 min (inferred); "three to four hours guided" (Player2, Insider Gaming, public). Mafia Free Ride opens after Prologue, Chapter 2 (2K, Nov 2025) or Chapter 3 depending on source (public); Chapter 2 ends at 108 / 143 / 178 min (inferred).
- Choices: KCD2 26 choice points in the first quest (lead, from game files); Mafia has no dialogue choice (the conversation player has no choice function; read from files, lead).
- Tutorials: KCD2 251 tutorials (lead, from game files); first prompts only on hesitation (movement after 10 s, attack 20 s, marker 30 s), kept 10 s, combat lessons until cleared (read; the study names ids from files, lead); 73 calls before free roam, about 63 in a normal run; 14 blocked in the siege. Mafia 77 tutorial assets: 26 of 8 s, walk and look untimed, 24 blank, 21 re-readable pages (lead, from game files).
- Prompts in 30 min: KCD2 at most about 12; Mafia about 10. Distinct activities in 30 min about 10 each (inferred).
- Longest beat with no new control or scene: about 5 min in both (KCD2 the ride; Mafia the walk outside the mine) (inferred).
- Saves: KCD2 16 scripted autosaves before free roam (lead, from game files), about 3 in 30 min; 3 save locks before free roam, 2 within 30 min (inferred); manual saves by consumable, bed, or Save and Quit (Shacknews, public). Mafia 38 checkpoints in the prologue (lead, from game files), about 20 in 30 min, 13 in play (inferred); one slot, no manual save (Gamerblurb, PowerPyx, public).
- Failure cost: KCD2 siege death, or game over if walls fall or the player idles 10 min (read); reloads cost one writer 10 to 19 min each (PPE.pl, public), another over an hour in one quest (Xbox Tavern, public). Mafia failure from the first beat: leaving the friend or area (instant), killed or spotted (3 s); back about 1 to 2 min (inferred).
- KCD2 nudges: after 2, 5 and 60 s idle and again after four minutes (as quoted in For LEDGER item 7; read from files, lead).
- LEDGER's own column (production/playtest/thirty-minutes-2026-10-03.md): 11 of 30 minutes empty; the window seen by six; DS Ellis trail at minutes 21, 24 and 27; four clock lines within 90 s; first control minute 1; not yet tested across a restart.
- Neither game gives a second route or a consequence the player caused and the world kept; Mafia has no dialogue choices; 2K says some later missions offer a choice of route (2K Q&A, public). KCD2 switches crime notices off in its opening battle.

### c. Open blind spots

- A real player's clock: every minute is an estimate, and skipping compresses cutscenes.
- Mafia: what fires its tutorials and failures is inferred; script logic not exported.
- KCD2: engine-fired tutorials, the reload point, the siege's own scenes, the order of the videos.
- Not reached for lack of disk (F: filled on 28 October): Mafia's face-clip cross-check stopped at 134 of 491 (43 of 49 matched within 0.05 s); Chapter 3 onward not exported.
- Not reached otherwise: Warhorse's wiki (an empty page); HowLongToBeat; IGN, Polygon, Eurogamer, PC Gamer, GamesRadar, 2K support, Deltias, Sportskeeda (refused or blocked).

### d. The twenty basics

The study cites basics by number only, in its "For LEDGER" block (quoted in full in part a): "basic 7 (a hint for each key)"; "basics 7 and 8"; "basics 19 and 20". The list itself is not in this study.

---

## Study 03: Dialogue and barks (28 October 2026)

Source: studies/03-dialogue-barks.md. Games: KCD2, Mafia. Method: game files and Warhorse's public wiki (KM-A-18, KM-A-91 read in full); code not read; no game text quoted. Reviewed (about 130 numbers re-measured, pass with fixes).

### a. For LEDGER (in full)

> ## For LEDGER
>
> Targets, not work now: the voices and the town's talk work are not reopened (3 October); new systems wait for PLAN.md (29 September). Items 1 to 3, 5 and 6 are phase 5 proposals for his page.
>
> **How much each kind of character needs (phase 5's batches; the 24 September ruling: everything unprompted written ahead):**
> 1. **Adopt for the 30 regulars:** about 30 own street lines each, for the situations their day lets them hold (Kingdom Come II's upper quartile for a one-voice role; Darren has 33). Today's cast stays as ruled: own lines for Ron, Darren, Father Walsh and June, shared for Sheila, Alison and Ada.
> 2. **Adopt for the crowd:** per situation at least 6 lines per kind of speaker, each crowd voice owning a fixed 2 or 3, so a person repeats himself as people do while the street varies. Serves VoiceBank's named risk (six voices is thin); for the town, Mafia's 14 (man or woman, by age), cast only on his yes.
> 3. **Adopt the missing situations,** written ahead: greeting him by regard in Kingdom Come II's order on LEDGER's values (afraid or suspicious, angry, knows and likes him, his appearance, neutral), no numbers shown (D33, D34); bumping; neighbours greeting each other; talking to oneself at work; a small rain bank (phase 3's weather proof). Serves the Meridian Test: the town visibly knows them.
> 4. **Ignore** the conversation-opening greeting bank (his 7 October ruling: no prepared openings), skill checks, the community voice categories (accents come from the casting sheets) and Mafia's mission nags.
>
> **Ambient lines with no model call, played at once (StreetVoice, extended):**
> 5. **Adopt the two-level gate:** the situation from the simulation; a street-wide wait by kind with priority (a deed breaks a greeting's wait; the 45 s floor stays for everyday talk); a personal wait (10 to 20 s; one greeting a person a game day; a pair's greeting once in a few real minutes); Fresh's never-heard-first within that voice's share; the prepared clip and subtitle at once.
> 6. **Adopt as starting values:** crime reactions 20 to 40 s; gossip 10 min a pair; self-talk 15 min a person.
>
> **Staging and length (phase 1's speaker; phase 3):**
> 7. **Adopt:** speakers face each other and turn only when speaking; gaze eases over about 0.5 s; a gesture on three lines in four, a face mood on two in five; a prepared reply starts a beat after its opener (about 0.3 s, I). Any conversation camera (the interface is not reopened, 3 October) alternates close shot and close-up, about 3.3 s a shot; street lines never move it.
> 8. **Adopt length targets:** street lines about 7 words (ours are); replies about 12 words, 4 s at 2.6 to 2.8 words a second, keeping a live reply's first sentence short (the 2 s bar); Tom's suggested lines about 4 words, like Kingdom Come II's prompts. Subtitles split above 120 characters, bark subtitles a separate switch, when the interface is next touched.
> 9. **Adapt hearing:** Kingdom Come II's barks carry 35 m; LEDGER says a remark within 7 m, its words clear within about 6 m in quiet (Acoustics), the murmur beyond (ChatterLevel).

### b. Key measured numbers

Source: 03-dialogue-barks.md [The numbers; How dialogue is stored; How much is written; Bark situations; Keeping it fresh; Staging; Line length]. All KCD2 and Mafia figures below are (lead, from game files) unless a public source is named (the Warhorse wiki items are public and stand, and are marked "wiki").

Volume
- KCD2 spoken lines written 137,969; 280,343 English voice files; English text table 155,813 entries; 18,691 quest files (lead, from game files; the quest-file count also read from wiki KM-A-18). Player's share 30% (40,962 lines).
- By where played: conversations 60,164; game-started 30,986; in the world 43,833 (one-sided barks 20,024, short exchanges 15,117, chats 7,034, greetings 1,658); cutscenes 2,986; 6% have no English voice (lead).
- By character: 74,275 lines for 1,897 one-voice roles; 22,732 for 1,696 crowd roles (another split 67,451 and 29,618); companion 3,385 (lead).
- One-voice role lines: median 9, p75 31, p90 89, 15 over 500. 84 voices with 100 or more files; 71 with over 1,000. Crowd voice lines: median 1,663 street, 1,191 quest (lead).
- A crowd line is recorded by a median 4 voices (p90 16); in street pools each voice records a median 2 of 5 (lead).
- Mafia: 5,690 exported lines of 12,558 voiced; 5,901 scripted and 6,657 systemic voice events; 73 characters; player 1,363, next 810; player's share 24% of exported; one-voice role median 25, 12 with 100 or more; 49 bark voices (14 civilian, 12 enemy); crowd voice median 73 lines over about 33 situations; civilians 2 variants per situation (greeting and bumping 3 to 4), enemies 3 (lead).
- Mafia systemic events cover 659 situations (grouped by name, inferred): mission nags 142, combat 138, narration at world interactions 90, perception and alert 63, street reactions 60, ambient conversations 57. Mafia Lexicon: 1,880 scenes, median 2 lines; 115 ambient conversation assets, median 3 parts, 15 generic by class pairing (lead).
- LEDGER now (LEDGER's own files): 491 shared lines, 217 own; Ron 159, Darren 33, Father Walsh 17, June 8; 6 crowd voices; 14 everyday, 6 per event variants; 45 s floor.

Structure and choices (KCD2, lead)
- Dialogue nodes: 2,241 player-started conversations, 670 game-started, 5,421 world lines with no camera, 1,216 condition graphs, 169 cutscenes; 33,325 decisions, 75,614 sequences.
- Choices: median 2 options (p90 4); 4-word prompt then median 8 words spoken; about 400 timed (mostly 5 to 10 s); 1,280 skill checks at eleven difficulties; 250 greetings move reputation; 5,306 sequences play once only.
- Mafia: no choices found; game linear (lead, inferred).

Cooldowns and freshness
- KCD2 street wait: median 32 s; crime 20 to 40 s; gossip 10 min; self-talk 15 min (lead). 46% of street sequences carry a cooldown: median 32 s, p25 15 s, p75 5 min, p90 30 min; opening greeting 30 min, friend's greeting 32 min; street decisions median 2 variants (p90 6), half only one; 2,169 carry a voice cap (1 to 6); cap holds in only 938 of 2,142 pools (lead).
- KCD2 street-wide waits by kind (read; wiki or file not split in the study, so also a lead): companion comment 4.5 s, body 5.5 s, drawn weapon 10 s, crouching 12 s, greeting 40 s, mourning 80 s; priorities greeting 10, weapon 40, threat 85, body 95; per person 10 s any, 20 s greeting, 45 s after crime interruption; pair greeting once in 6 game hours (about 24 real minutes, inferred); 3,997 street dialogues carry a clash class.
- Mafia mission speaker repeats every 7 to 10 s, greets and parts at 10 to 15 s, waits 2 to 5 s after a bark; priority threshold 100 (read, lead). Bark table not exported.
- LEDGER's Fresh: never-heard first, then oldest; one remark per person per story; 45 s floor keeps a 14-line band from returning inside 10.5 to 22 minutes (LEDGER measurement, 28 September).

Bark situations (KCD2 line counts, lead): greeting 419 lines; weapon drawn or crouching 118 lines at 20 s; bumping 13 lines at 20 s among 334 small provocations (median 40 s); crime 4,747 lines in 763 files, 6 voices a line, 30 s; refusing to talk at low reputation 111; greetings by pairing 659 lines at 32 s; gossip by class pairing and place 2,607 lines at 10 min; self-talk 357 lines at about 15 min; rain in 33 conditions. Mafia: greeting 12 voices x 3 to 4; bumping 12 to 14 voices x 3; 115 ambient conversations; idle 22 voices.
- Greeting chain (read; lead): low reputation or brand; violent anger; property anger; high reputation with renown; high charisma; neutral. Pools of 4 to 12 one-liners; neutral 29.

Staging (lead)
- KCD2: 78% of conversation lines carry a camera command; shots close shot 46%, close-up 41%, medium 13%; 77% carry a gesture (1.06 a line; 179 kinds); 39% a facial mood (25 moods); 55% a direction note; gaze on a 3x3 grid, easing most often 0.5 s; start delay on 13% of lines, median 0.27 s (meaning inferred). Street lines carry camera 0.7%, gestures 25%.
- Distances: street barks carry 35 m in 76% of dialogues that set it (10 m quiet, 50 to 200 m loud); conversation limit 10 m in 1,060 of 1,209; caller stands 2 to 4 m off, calls up to four times.
- Mafia: cutscene shots median 3.3 s (p25 2.1, p75 5.3; 2,583 shots in 171 sequences); 96% of line rows name a face clip.

Length
- Words per line median: street 7, conversation 12, player 8; Mafia 7; LEDGER shared 7. Seconds per line: street 3.6, conversation 4.3 (field meaning inferred); Mafia 2.5. Words per second 2.8 (KCD2), 2.6 (Mafia). P90: 19 words 7.2 s (KCD2), 16 words 6.3 s (Mafia) (lead).
- Subtitles: KCD2 separate switches for conversation and bark subtitles plus name, background, size (read); Mafia splits over 120 characters, never under 40 (read); Sicilian a voice language only.

### c. Open blind spots

- Mafia, not exported (F: full): systemic text, bark table and settings, voice data, 29 reaction bark assets, so its bark cooldowns, chances, ranges, and whether crowd voices say different words are unknown.
- Code: how either picks within a pool; KCD2's 51,000 camera commands with no named shot.
- Units: whether KCD2's per-line cooldowns count play time (inferred; 131 sequences name the world clock explicitly); what its line-length field and start delay mean (inferred). Its cap on lines per voice holds in only 938 of 2,142 pools.
- Shown only in play: density, subtitle look, how barks land. No recordings (25 October).

### d. The twenty basics

No mention in this study.

---

## Study 04: Street and world building (25 October 2026)

Source: studies/04-street-world.md. Games: Mafia (Palermo_Main only; San Celeste exported ground meshes and layer states only), KCD2 (Kuttenberg's level text files; loose meshes stored apart, so props not countable). Method: level files. "(helper)" marks a helper's measure the reviewer could not reproduce. Reviewed (pass with fixes).

### a. Targets for LEDGER's phase 2 (the study's stand-in section, in full)

> ## Targets for LEDGER's phase 2
>
> Quay Street today: a 48 m road with 36 m of frontage, 10.25 m from front to front, two-storey terraces; its scene file places 43 props and 10 decals (about 9 per 10 m of street, read from production/specs/vignette-scene.json, not counted in the built level).
>
> 1. **Width:** a check that every street's front-to-front width lies between 9 and 15 m (Kingdom Come II's median 9.9 m to Mafia's 14.7 m); Quay Street's 10.25 m passes.
> 2. **Props per 10 m of street:** counted in the built level, both sides, per 10 m of street length, from a fixed list of kinds: bins, signs, boxes and crates, pots and planters, seating, lamps and posts, bikes, litter heaps, post boxes and kiosks. At least 5 per 10 m (Mafia's 4.9, from one 73 m sample; its neighbouring streets run 2.2 and 0). Ground dressing (kerbs, paving breaks, moss, stains) is counted apart and has no bar yet.
> 3. **Dress where the player walks:** Mafia concentrates its dressing on the mission's path. Quay Street is that path; streets beyond it can be thinner. A rule, not a check.
> 4. **Kit and its reuse:** a check counting, per street, the distinct facade meshes and the placements per kit mesh. Mafia's measured street: 18 to 19 facade pieces from 2 families, kit meshes used about 15 times each. For Quay Street: the terraces share one family with stacked floor types; the shops and Mickey's are the one-offs, as San Celeste's hero blocks are.
> 5. **Interiors:** enterable only where the story goes (Mickey's office); fake rooms sparingly (Mafia: 24 in about 8,100 windows); shells for the rest. A rule.
> 6. **Street ends:** every fixed camera's view along the street ends on a building or a turn, never open ground. A check on the camera views.
> 7. **Weather dressing:** small life tied to weather and hour (flies, smoke, leaves, drips, birds), as Kingdom Come II does; none in Quay Street yet. No number yet.
> 8. **Layers by time and story:** one switchable layer per street state (day, night, market, blocked), as San Celeste does, once the town grows past one street.

### b. Key measured numbers

Source: 04-street-world.md. All below are (lead, from game files) unless marked (helper) (a helper's figure, not reproduced by the reviewer, so weaker still) or LEDGER's own.

The two streets
- Mafia Palermo main street: 73 m segment; width building to building 14.7 m (facing windows 14.5 to 14.9; facades 14.9); facade 18 m and 22 m, 4 to 5 storeys (from kit heights, not building bounds); plot module 7.8 to 8.3 m; window spacing 3.2 m and 2.6 m (helper); 13 ground-floor doors in 146 m of frontage (one per 8 m plot).
- Across Palermo: median facing-window width 14.7 m; alleys 3 to 9 m; wide streets 20.5 and 28 m.
- KCD2 Tarmark: about 191 m, curved; narrowest 5.9 to 6.8 m; median 9.9 m (20 of 49 stations measurable; a tenth above 12.7 m); over 20 m at the square; two-storey townhouses, ridge 18.5 m; small houses 8.7 to 11.5 m (helper); plot 12.6 to 12.9 m gable to street, small houses about 7 m (helper); windows 3.2 m upstairs, three per front; one or two doors per house front.
- Props: Mafia true props 4.9 per 10 m (plant pots 1.2, boxes and buckets 1.0, laundry 0.7, lamps 0.5, signs and post boxes 0.5, seating 0.4, ropes 0.4); props plus ground dressing 17.4 per 10 m, 21 with decals and add-ons; under them in 73 m: 91 ground-dressing pieces, 8 decals, 18 facade add-ons; 9 pots. The measured street holds 134 placed actors, its two neighbours 6 and 4 (neighbouring streets run 2.2 and 0 props per 10 m). KCD2's 15.8 per 10 m counted every entity and is not a prop count (discarded by the study).

Kit against unique
- Mafia: game-wide 540 facade, 585 roof, 60 interior, 1,163 distant meshes. Palermo main-street group (about 100 buildings): 33,986 placements of 433 meshes, 78.5 uses per mesh, 88% kit elements, 32 meshes used once; facades 299 pieces of 26 meshes in about 11 house families of about 3 floor types. Measured street alone: about 2,350 placements of about 150 meshes (about 15 each), 18 to 19 facade pieces from 2 families. San Celeste: 134 packed kit actors, 13 hand-built blocks, 111 shape meshes.
- KCD2: 232 building instances from 77 meshes (about 3 uses each); 387 buildings in the distant tree with 221 names; sheds and lean-tos reused 11 to 19 times; most reused house 7; library 465 templates, 5,553 structure meshes, 1,873 houses.

Interiors, edges, streaming
- Mafia: 3 fake-room shapes placed 24 times against about 8,100 window pieces; Town Hall 381 assets, Opera 462. KCD2: of 166 city houses, 88 furnished, 78 shells; 80 have door entities, 71 beds; 619 working doors, 95 shops.
- Edges: Mafia 74 distant set-piece assets game-wide. KCD2 town ring 542 wall entities, gates, 14 bastions; gates 30 to 33 m (helper); town-hall tower about 42 m (helper); four churches.
- Streaming: Mafia Palermo main grid 73 cells at 128 m, plus 33 always-loaded and 7 coarser; props grid 32 m; 130 cells carry 50 data layers; distant detail six layers, nine deep (read); San Celeste 21 day states plus night, market day, blocked and chapter states (read). KCD2 about 96,000 entity records always loaded, about 49,000 streamed (helper: 90,294 and 48,537); town 34,167 always-on; 523 merged distant meshes (helper).
- Weather dressing: KCD2 1,883 weather effects in town (rain 1,168, flies 571, smoke 120, leaves 15). Animals: chickens 51, rats 32, horses 21, dogs 11, cats 8. Mafia none found by name (unverified); no parked vehicles.
- LEDGER's own: Quay Street 48 m road, 36 m frontage, 10.25 m front to front, 43 props and 10 decals in the scene file (about 9 per 10 m; production/specs/vignette-scene.json, not counted in the built level).

### c. Open blind spots

- San Celeste's actors, props and widths (its map was not exported).
- KCD2's loose meshes (barrels, crates, carts, signs), so its props per 10 m.
- Block lengths; sightlines; fog as an edge; KCD2's cell sizes; clutter by the brief's kinds (bins, bikes, litter) and parked carts.
- Building heights in Mafia come from kit heights, not building bounds.
- Visibility of KCD2 landmarks from the street not computed; no Mafia landmarks measured; decals per street not counted; Mafia weather dressing "none found by name (unverified)".

### d. The twenty basics

No mention in this study.

---

## Study 05: Visuals (25 October 2026)

Source: studies/05-visuals.md. Games: Mafia (Palermo, 191 cells), KCD2 (light entities, probe files, settings). Method: material instances, light components, presets, decals read as settings; master material graphs, lamp Blueprints and window-glass materials not exported, so internal scaling unknown. Reviewed (pass with fixes).

### a. One target per open visual problem (the study's stand-in section, in full)

> ## One target per open visual problem
>
> 1. **Windows:** our own research (aaa-street/WINDOWS-GRAZING-2026-10-08.md) finds the white boards are flat-lit joinery at a low angle, where the reveal hides any room behind, and that fake rooms fail at shopfronts (shop-glass-reflections, close range). So: shade the frames first; a fake-room material, with one global night tint as Mafia has, only for upper and distant windows. Check: no window reads as a flat white or black board in the three morning views.
> 2. **Shop glass:** keep the per-window captures. Our research found software Lumen's front layer showed almost no street, which is why the captures exist, and the 23 October card-time study (frame-headroom/CARD-TIME-2026-10-23.md) found the front layer itself costs about 0.06 ms. Add the dirt mask (Mafia has one; it fits our recipe). Nothing in either game changes this.
> 3. **Night pools:** each lamp as Mafia builds it, a key spot with a light profile and some volumetric scattering in the fog, plus a tiny bulb light; point lights cast no shadows. The street-lamp pools keep their shadows (a choice made for our street, to be priced against the shadow-light budget of Study 12). The pool comes from the ratio of lamp to ambient light, so judge that ratio, not the exposure. Check: pools on the pavement with dark between them, in the street-at-night view.
> 4. **Wet streets:** wetness as one global value driving roughness (Mafia: 0.1 flat, 0.2 slopes; our asphalt's 0.06 is glassier). Our research found roughness 0.16 read as dry, so set it by eye between those. Puddles as decals in low spots return only when the puddles set aside on 8 October are taken up again (aaa-street/PUDDLES-2026-10-02.md). Check: no sky mirrored across the whole road.
> 5. **Wear:** a decal mix close to Mafia's street mix: leak stains under sills, gutters and pipes (about two in five), grime at wall bases, plaster grunge, densest where the player walks. Check: Quay Street's decal count by kind, against the mix.
> 6. **Materials:** one main master (colour, packed height-roughness-occlusion, normal, tint) and one two-layer vertex-painted wall master for dirt at the base.
> 7. **Texture budget:** our own budget stands (4-BUDGETS.md: 512 px a metre, 2048 tiling sets, 4096×2048 trim sheets); Mafia's spread of sizes (a fifth at 4096) is consistent with it.

### b. Key measured numbers

Source: 05-visuals.md [By problem; Settings sheet]. All game numbers are (lead, from game files); LEDGER column from LEDGER's own files; Mafia's light units and scale are not physical.

Windows and glass
- Mafia window material: fake interior switch, depth offset -7, refraction 3, glow 0.3, warm tint, flat atlas of room pictures, one global colour dims all. One exported use is an opera window (30 uses); three fake-room shapes exist, no Palermo cell places them. By name: 742 window, 526 glass, 110 curtain, 73 shutter assets. Curtains use the main opaque material.
- KCD2 window kit about 219 window and 38 shutter mesh names; plane lights in openings: 290 in Kuttenberg's region, 104 in Trosecko; about 0.5 m wide, wall thickness median 0.25 m, up to 1.5 m (meaning inferred from field names).
- Mafia: no reflection captures or planar reflections in Palermo; Lumen, no ray tracing; front layer allowed from reflection level 2 (PC default); whether window glass uses it not seen. KCD2: 23,270 probe files in Kuttenberg's region and 7,893 in Trosecko, about 0.10 MB a pair, baked at 11 times of day, about 7.2 GB total; screen-space reflections at half resolution, full at top two levels. No reflection cost figure for either game.
- From LEDGER's own research: front layer costs about 0.06 ms (frame-headroom/CARD-TIME-2026-10-23.md, 23 October).

Night light
- Mafia lamps are two lights: key spot plus tiny bulb point. Common lamp (39 in Palermo): spot 1.5 cd, reach 20 m, cone 80 degrees, 4500 K; bulb 0.45 cd, 1 m; key spots 0.5 to 25 cd; 20 of 39 volumetric scattering 2.5; 25 of 39 shadows off, 14 unstated; Blueprint multiplier 3 (true values may be higher). Second lamp (9): 4 cd, 15 m, 2400 K, IES. Wall lamps 0.25 to 0.5 cd, 8 m, 2400 to 2750 K, IES. None of 135 point lights stating shadows casts one. Medians: points 0.2 cd, 1 m; spots 8 m, 70 degrees, drawn to 30 m.
- Mafia scale: sun 7 to 15 by day, 0.0035 to 0.1 at night; sky 1.2 to 7 by day, 0.0005 to 0.045 at night; exposure compensation +2.75 to +4.0 at night (-1 to +1.5 by day), floor 1.0 (103 presets); night fog 0.035 to 0.05; fill light 0.1, 4500 K.
- KCD2: no physical units; town light reach median 4.3 m (a tenth reach 8 m), warm orange; 150 of 1,000 lantern pattern; 14 of 1,000 clock-switched; 525 fog volumes; night exposure not found.
- LEDGER now: lumens (lantern 40, pool 500); night_exposure_pin 0.4; fog gain 0.2; per-window captures 256 px (1,024 hero).

Wet and wear
- Mafia: one global wetness (default 0) drives roughness 0.1 flat, 0.2 slopes; puddle decals 232 in Palermo; flood switch used 4 times. KCD2: rain screen-space layer to 150 m (40 m low); no puddle or wet-street material among 7,572 materials.
- LEDGER: paving 0.1, kerb 0.15, asphalt 0.06; roughness 0.16 read as dry (LEDGER research); puddles set aside 8 October.
- Mafia decals: 2,461 of 180 materials: 40% water and rust leak stains, 9% puddles, 9% plaster grunge, 8% flood-line stains, 2% lichen; in 41 cells, median 11 a cell; densest cell 878 (an underground tunnel); about 650 decal materials on 5 masters; 14 grunge types. KCD2 decal atlas 256 px in 12 slices; 212 decal materials.

Materials and textures
- Mafia library: 253 masters and 1,189 instances in the exported set (whole game index 328 masters and 11,843 instances); main master 307 instances, three textures plus tint; walls 130 on main master, 38 on two-layer vertex-painted master.
- KCD2: 7,572 materials (one per asset) drawing on 135 shared surface materials (26 ground, 24 wall, 19 wood, 8 stone, 5 metal, 2 glass).
- Mafia texture sizes (about 350 each of colour, normal, mask): 4096 px 21%, 2048 px 36%, 1024 px 38%; 110 carry own bias of -1; in-game cap unknown. KCD2 archive bytes: buildings median 2.8 MB (a tenth above 11), people 1.4, furniture 0.7, small props 0.35.
- LEDGER budget: 512 px a metre; 2048 tiling sets; 4096x2048 trim sheets (pre-production/4-BUDGETS.md).

### c. Open blind spots

- KCD2's time of day, exposure and sun values (only 33 profile names found); material parameters and window depths.
- Mafia's master material graphs, lamp Blueprints (the real scaling of candela), window-glass materials, and whether its front layer is used on windows.
- Lights and decals per street; windows from a low angle; net curtains; any cost figure for reflections.
- What 6,374 of KCD2's 7,572 materials are.
- Window frame depth in the meshes not measured.

### d. The twenty basics

No mention in this study.

---

## Study 06: Characters and wardrobe (25 October 2026)

Source: studies/06-characters-wardrobe.md. Games: Mafia, KCD2. Method: FModel property exports and name index (Mafia); tables, Storm rules, character files, mesh and texture headers (KCD2); public pages (2K Valencia, Hangar 13 talk excerpts, Warhorse GDC 2025 abstract, Epic MetaHuman spec, Marvelous Designer guide and pricing). Reviewed (34 of 41 claims confirmed; fixes applied).

### a. For LEDGER (in full)

> ## For LEDGER
>
> **The clothing target for Tom's outfit** (item 3):
>
> | Piece | Full-detail triangles | Textures | Moves |
> |---|---|---|---|
> | Jacket | 18,000 to 22,000 | 2048: colour and occlusion, normal, packed roughness | skinned; tails or vents on a short rigid-body chain, not cloth |
> | Jumper | 15,000 to 20,000 | 2048 | skinned only |
> | Trousers | 8,000 to 10,000 | 1024 to 2048 | skinned only |
> | Shoes | about 6,000 | 512 to 1024 | rigid |
>
> - The jacket and trousers are anchored on Mafia's medians; the jumper and shoes are our pick within Mafia's ranges.
> - These rows sum to 47,000 to 58,000 with the jumper under the jacket; Mafia's median outfit is about 43,000, so the jumper is the piece to trim if the budget is tight. All of this is our choice, not a measured target.
> - Four levels of detail at about 50%, 25% and 10%.
> - Mafia imports its textures at 4096 and ships 2048. Whether its small folds are baked from a finer model is not shown by the files (an unverified artist's note says so); which folds sit in the mesh and which in the texture, and how lapels and collars are modelled, were not read: open blind spots.
> - The ruling of 30 September already matches both games: garments are skinned meshes, and only loose parts move.
>
> **Colour by material, not by mesh.** One layered garment material with tint, grime, scratch and wet values, as both games do. One jumper mesh then gives four to eight period colourways. Its grime value can follow our street's grime.
>
> **Fit to our bodies (our choice).** LEDGER's people are MetaHumans. His ruling of 2 October stopped fitting every garment to six bodies, and Mafia makes most garments for its one base body. So: one base body per sex for the crowd, garments made to it, the skin under each garment cut away or hidden; a second body type only where a cast member needs one.
>
> **The crowd recipe for Quay Street:**
> - presets with slots and tag filters (social standing, age, clean or worn), a random pick per slot, colourways from the material;
> - a pool of about 10 tops, 8 bottoms, 6 coats, 6 hats and 5 shoes, at 4 to 8 colourways each. This gives hundreds of looks for a street of a few dozen, with Tom and the cast hand-set;
> - a hat left out by chance (Mafia: 20 to 80% per preset).
> - These are a first figure scaled down from both games, to be tested on the street.
>
> **The facts for the clothes decision (the Marvelous month):**
> - Mafia's own character pipeline names Marvelous Designer.
> - Both games ship baked, skinned garments, which is the target above.
> - Marvelous Designer's vendor guide says its Personal plan "permits commercial use for eligible freelancers and sole proprietors". Its binding terms could not be reached (404 and 403).
> - So the licence for game use is still to be read in full before anything made in it goes into the game, as his order says.
> - Money: his ruling names 39 USD for one month; the pricing page read today shows 23.3 a month billed yearly for an individual. The monthly price and his eligibility for the Personal plan ("eligible freelancers and sole proprietors") are still to be checked. Both go on his page with the sign-up.
>
> **Dirt as gameplay:** Kingdom Come II's "too dirty to greet" and "blood raises suspicion" are taken up by Studies 11 and 15.

### b. Key measured numbers

Source: 06-characters-wardrobe.md [Answers; Budgets]. Game numbers are (lead, from game files) unless a public source is named. Items the study marks unverified keep that mark.

Bodies and heads
- KCD2: male body five parts, 17,318 triangles full detail (8,268 and 3,868 at next two levels); female body one mesh, 16,588; heads median 19,455 triangles, facial rig about 360 bones; pre-merged distance mesh 2,597 to 3,100 triangles; 53 hiding groups and 35 morphs (about 19 and 10 for animals). Texture sizes (unverified, helper header reads, not saved): body 2048; heads 1024 colour, 2048 normal, two wrinkle maps. Visible man up to about 71,000 triangles with head, hair, hands (the study's own sum).
- Mafia: 32 male body meshes in five families, 21 female; unique heads 101 male, 20 female; four levels of detail at screen sizes 1.0, 0.4, 0.15, 0.08 (about half, quarter, tenth of triangles; median kept 47%, 25%, 9%); male skeleton 272 bones, 28 coat-flap bones. Body, head and hair triangle counts not exported.
- Epic's MetaHuman specification: body 30,500 vertices at full detail (public).

Outfits
- Mafia: preset fills up to 12 slots (body, head, hair, three groom slots, hat, top, bottom, one-piece, shoes, prop); median 8 filled; 780 presets; 126 of 176 tagged garment meshes for the base body. KCD2: 10 body layers, 22 equipment slots; 2,518 clothing presets, median 5 items.
- Variety: Mafia base garments male tops 62, bottoms 39, hats 49, one-pieces 14, shoes 14; female tops 25, bottoms 17, hats 10; 1,010 male garment-and-colour rows (tops 338, bottoms 255, hats 229, one-pieces 103, shoes 85); median colourways 4 to 10 per mesh; 1,213 of 1,416 garment materials children of one layered master. KCD2: 2,139 garment variants on about 513 meshes at 4 to 6 colourways; 2,661-material colour tree.
- Crowd dressing: KCD2 Kutná Hora 1,354 soul slots, 139 hand-set appearances, 90 heads. Mafia presets by social sub-class: peasant 72, townsfolk 65, farmer 52, merchant 50, rich 42 (that spawners draw from them is inferred). Hat left out by chance 20 to 80% in 326 presets. Far away: 14 male and 7 female single-mesh puppets.

Garment budgets (full detail)
- Mafia vest-jacket 19,131 triangles (then 8,509, 4,781, 1,505), one material, 15 colourways, textures shipped 2048 (authored 4096); trousers 7,906 down to 750, 8 colourways, 1024; tailed jacket 25,422 on 244 bones, 30-body physics asset (22 flap, 8 colliders).
- KCD2 tunic torso 3,734, arms 2,824, skirt 904 (7,462), skirt simulated via 270-triangle proxy; hose 6,806, 25 or more colourways.
- Table: Mafia top or jacket median 21,994 (87 tops; range 6,112 to 57,369); trousers 9,566 (61; 5,396 to 23,022); shoes 6,718 (18; 1,780 to 9,964); hat 4,495 (59; 1,578 to 14,797); whole outfit about 43,000. KCD2 tunic set 7,462; hose 6,806; caps median 5,400 (unverified); outfit median 24,532 men, 16,548 women (sample of 44 presets). Mafia textures mostly 1024 for tops and bottoms, 512 shoes and hats.

Movement, hair, dirt
- Mafia Chaos cloth on 10 meshes (8 garments, 9 named characters' pieces); 68 of 74 garment animation blueprints use rigid-body bones; 239 of 1,416 garment materials add a shader wobble. KCD2 cloth only hems and skirts (173 male, 29 female elements); 1,926 pendulum joints.
- Hair: Mafia 183 male strand rows on about 24 grooms; 147 of 269 hatted male presets swap to cap-hair. KCD2 (unverified) median 9,700 triangles, 39 haircuts in 9 colours; 1,445 beard meshes.
- Dirt: Mafia grime on 880 garment materials, scratch on 801, five blood masks. KCD2 54 blood-mask spheres (24 human); dirt over 0.9 refuses a greeting.
- Public: 2K Valencia names Marvelous Designer, ZBrush, MetaHuman facial rigging; Hangar 13 Unreal Fest 2025 talk (excerpts, unverified): more than 100 NPC assets in about three months; Warhorse GDC 2025 (abstract excerpt, unverified); Marvelous Designer pricing 23.3 a month billed yearly for an individual (read 25 October); his ruling 39 USD one month.

### c. Open blind spots

- Mafia's body, head and hair triangle counts (not exported).
- How many looks one Mafia crowd spawner produces.
- KCD2's level-of-detail switch distances.
- How either game's hiding maps to vertices (read from names only).
- Lapel and collar modelling; which folds sit in the mesh and which in the texture.
- Mafia's shared MetaHuman face folder (not exported).
- Marvelous Designer's binding terms (404 and 403) and monthly price; his eligibility for the Personal plan.

### d. The twenty basics

No mention in this study.

---

## Study 07: Animation (25 October 2026)

Source: studies/07-animation.md. Games: Mafia (1,508 property exports via FModel), KCD2 (animation databases, tables), plus public sources (2K dev diary 17 June 2025; CzechCrunch interview with Warhorse mocap lead, 19 January 2022; Epic 5.8 pages; Clavet For Honor talk notes; 2011 perception study known from a search snippet only). Reviewed (about 40 items confirmed, fixes applied).

### a. For LEDGER (in full)

> ## For LEDGER
>
> - **For the walk (item 2):**
>   - **The best-evidenced professional stop is Kingdom Come II's:** a clip chosen by the remaining distance and the quarter of the stride, in a left-leg, a right-leg and a long version.
>   - **Our motion matching instead searches all 223 of Epic's walking clips,** and 134 of them carry a flat foot that travels more than 3 cm in Epic's own data (measured 25 October).
>   - **Today's two tries** (holding a low, still foot, and a lock that holds a half-marked foot) are tested on the street first because they keep the sample as it is. They are judged by eye.
>   - **If they do not pass:** stops and turns-on-the-spot chosen like Kingdom Come II's, by distance window and stride quarter with per-foot clips, inside the same graph.
> - **Play rate:** keep a clip's play rate within about 10% faster and 20% slower of its authored speed (Clavet), so feet do not skate when speed and clip disagree. Mafia's stride-warping clamp of 0.5 to 1.5 is a different setting and no bound on skating.
> - **The bar itself:** the only perception figure found says viewers notice slides below 21 mm. It is from a snippet, unverified, but it makes 3 cm a lenient bar.
> - **For sitting (item 2's second half):**
>   - every activity as In, Loop and Out, tied to an anchor point on the seat;
>   - ground alignment off while fitted to furniture.
>   - Epic's sample in our project already holds a bench interaction built this way, on smart objects: approach clips from five sides, each on either foot, an idle loop and a stand-up.
> - **Quay Street's ambient animations:** a first floor from what both games use most often, not a target. Every route is to be checked: that Mixamo has each one, with matched In, Loop and Out, is not yet checked. No child, alcohol or gambling animation is wanted.
>
> | Action | Count | Route |
> |---|---|---|
> | Stand idles and fidgets, men and women | 4 | Epic's MetaHuman clips, then Mixamo |
> | Lean on a wall or shop front | 2 | Mixamo |
> | Sit on a bench, a chair, the office stool | 3 | Epic's bench interaction, then Mixamo |
> | Smoke a cigarette | 1 | Mixamo |
> | Read a newspaper standing and sitting | 2 | Mixamo |
> | Talk in pairs | 8 | Mixamo |
> | Behind a shop counter | 2 | Mixamo |
> | Sweep the pavement | 1 | Mixamo |
> | Carry a bag or a box | 2 | Mixamo |
> | Open and close a door, inward and outward | 4 | Mixamo, both sides |
> | Wait at the bus stop or the phone box | 2 | Mixamo |
> | Turn and look | 1 | Mixamo |
> | Startle | 1 | Mixamo |
> | Point | 1 | Mixamo |
>
> - The pair talk covers agree, disagree, listen, speak, point, shrug, think and laugh.
> - The counter actions are idle and wiping.
> - Turn and look is for noticing Tom; the startle is for a deed seen.
> - **Talk's body language:** Kingdom Come II's gesture families and its 3 by 3 look grid are the model.
> - **Faces:** both games pre-bake every line, which LEDGER's live talk cannot do. The ruling of 1 October stands: prepared lines use Epic's audio-driven mouths, live lines the voice's loudness.
> - **Ignore for now: animation sharing and vertex-animated crowds.** Quay Street's own count of people is set in Study 1 and Study 4; these come back with phase 5's town and Study 12.

### b. Key measured numbers

Source: 07-animation.md [Answers]. Game numbers are (lead, from game files); public items keep their source.

Walking and stops
- Neither game uses motion matching. Mafia: 54 animation classes read with 59 state machines, 239 states, 563 transitions (183 inertialized); 16 small state machines in the ordinary layer; no motion-matching node; name index of 139,791 packages holds no pose-search asset; 144 classes not read (lead). KCD2 Mannequin: 842 blend-space files, 94 animation databases with 22,342 options (lead).
- KCD2 stop table: remaining distance walk 0.6 to 2.1 m, travel angle tolerance 5 degrees, quarter of the animation; turn clips at 45, 90, 135, 180 degrees each way (lead; that it keeps the planted foot matched is the study's reading).
- Mafia per movement set: 12 starts, 6 stops, 4 idle turns, 2 pivots; all 38 hero stops carry a distance curve; distance matching proven in the cover layer only; stride warping clamp 0.5 to 1.5; about 155 of hero's 577 no-weapon clips are movement; movement assets reference 552 clips (lead).
- Hangar 13 captured "systemic" movement on its Brno stage (2K dev diary, June 2025, public).

Feet
- Mafia (54 classes read): no foot lock on walk; control rig at close range only: 5 cm sphere trace per foot, pelvis offset up to 40 cm, feet up to 50 cm, solver 20 iterations; duel layer foot placement with ball-pivot lock (plant below speed 80, release at 50 cm); 51 clips with planted-foot curves (turns, some stops, landings, none on starts or cycles); civilians two-bone leg IK only (lead).
- KCD2: skeleton declares 3-bone leg IK, 5-joint foot-align chain, feet lock; ground alignment off in 932 of 1,055 male-set uses (lead). No foot-IK tuning numbers in data.
- Epic's own walking clips (LEDGER measurement, 25 October, clip_feet_all.py): 223 clips, 134 with a flat foot travelling more than 3 cm.
- Public: Clavet (GDC 2016) play-rate within about 10% faster, 20% slower; 2011 study (Pražák, Hoyet, O'Sullivan), search snippet only, unverified: sliding noticed below 21 mm; LEDGER's bar is 3 cm.

Interaction, talk, crowds
- Mafia world folder 2,144 animations (montages 990, special 396, standing 230, sitting 191, leaning 119, mining 104, patrol 84, sleeping 20); 389 smart objects (87 prop attachments, 12 props beside); by name across all animations: sitting 451, leaning 196, smoking 198, doors about 190, carrying 108, talking 526; world folder alone: doors 18, carrying 17 (lead).
- KCD2: 279 smart-object classes, 510 anchor points; 622 activity poses each with In, Loop, Out; doors 2 sets of 6 stages; male set 336 sitting, 260 carrying, about 400 trade-work fragments (lead).
- KCD2 gestures: 4,183 entries in 344 families across 70 moods, median 2.9 s; 25 male and 13 female look poses (lead). Mafia conversation set 123 animations (59 sequences, 64 montages); 93 named gestures (lead).
- Faces: Mafia 12,802 face clips, one per line; KCD2 18,449 facial files (8.2 GB), one per scene and speaker, no phoneme data (lead).
- Crowds: Mafia 14 sharing setups, 745 randomised instances, 13 vertex-animated assets; KCD2 no crowd animation system; reduces AI beyond 150 m, 70 to 80 in full detail (lead).
- Unreal 5.4 against LEDGER's 5.8.2: every method named exists by name in plugins (checked by the study).
- LEDGER's ambient animation first floor: 31 actions in 14 kinds (table above), not a target; Mixamo routes unchecked.

### c. Open blind spots

- How Mafia's ordinary walk times its stops: distance curves not decoded, transition rules not read.
- 144 of Mafia's animation classes, including the female walk and strafe layers.
- KCD2's foot-IK tuning (in code).
- Ambient animations per street, in both games.
- Anything only seen in play: no public talk by either studio on locomotion or feet was reachable.
- Not reached: Hangar 13's Unreal Fest 2025 talk (video only), Epic's interview with Alex Cox (403), the GDC Vault (down). The 2011 figure is from a snippet only.

### d. The twenty basics

No mention in this study.

---

## Study 08: Sound (28 October 2026)

Source: studies/08-sound.md. Games: Mafia (Unreal 5.4, Wwise), KCD2 (CryEngine, FMOD). Method: metadata only (event and table exports, sample names from bank headers, package index); no sound extracted or heard. Public: Jennifer Walden interview on Mafia's audio, A Sound Effect, 19 November 2025, seen only through a fetch tool's summary, not read in full. Reviewed (52 numbers re-measured, 44 matched; fixes applied).

### a. For LEDGER (in full)

> ## For LEDGER
>
> For phase 2's Quay Street and proof P13 (his ear decides), under the 5 October weather ruling and D26 (CC0 only). Unit 10 (production/cloud-week/sound) still waits for his ear (q-sound-listening).
>
> 1. **Adopt the three-part street** (P13; FEASIBILITY row 28, "near-silent"): unit 10's beds, spawned one-shots capped by hour, placed sources with set distances.
> 2. **Adopt four states of the hour,** crossfaded: dawn, day, evening, night, mixed from unit 10's day and night loops (I).
> 3. **Adapt weather** (5 October ruling): one rain parameter, dry through drizzle to rain, fades the rain layers, road hiss and gulls; rain halves spawned voices and activity (I).
> 4. **Adopt for footsteps** (the twenty basics, 18): 8 walk and 8 run per surface (unit 10 has 8 a surface, one gait); wet as a splash layer over the dry step; two shoe sets, soft (Tom's trainers) and hard; others' steps heard to 20 m.
> 5. **Adopt echo zones** with Unreal's own audio volumes, checked against 5.8 before building: street, shop doorways (Kingdom Come II's gate and arcade kinds), a small shop room, Mickey's office; the echo changes across about 1 m at a doorway, beds fade over about 10 m; an open door lets the street in, a shut one muffles it. Listener halfway between camera and Tom.
> 6. **Adopt layered doors** (phase 2's shopfronts): creak, hit and latch, 3 to 5 takes each, plus a shared grit layer; heard to 30 m, knocks to 10 m.
> 7. **Adapt the mix** (P13; phase 1's talk): the quietest lead voice is the reference; a talk state lowers the beds (by how much is in neither game's readable data: by ear); a full, TV or night range choice when the settings are next touched.
> 8. **Music, only if P18 rules it in:** priority states, silence the commonest; a 2 to 15 s hold; never combat music (12 October).
> 9. **Ignore:** Wwise or FMOD (outside the allowlist; any licence is his call), six shoe kinds, per-story mix states, vehicles (P9), animals beyond gulls, a cat and a far dog.
>
> **Quay Street ambience plan (P13).** Bed and one-shot levels are unit 10's (BRIEF.md section 5: EBU R128, −23 LUFS programme, −1 dBTP), kept; counts and distances come from this study.
>
> | Layer | Day / night / rain | Heard within | Unit 10 | From |
> |---|---|---|---|---|
> | Distant traffic (bed) | −40 / −45 / −42 LUFS | everywhere | has | brief |
> | Harbour water (bed) | −41 / −43 / −43 | everywhere | has | brief |
> | Wind (bed, gusts by parameter) | −46 / −47 / −43 | everywhere | has | Mafia |
> | Gulls (bed plus 0 to 2 spawned calls) | −48 / −56 / −54 | 150 m | loop only | Mafia |
> | Distant voices, no words (spawned) | at most 3 / 0 / 1; dawn 0, evening 2 | 15 to 40 m off (I; Mafia's quiet street 50 to 70) | lacks | Mafia |
> | Street activity: crate, bin lid, pan, a door indoors, a cat, a far dog (spawned; ≥30 takes in ≥8 kinds, I) | at most 3 / 0 / 1 | 15 to 40 m off (I) | lacks | Mafia |
> | Water lapping at the quay (spawned) | up to 14 by day, 6 at night | 25 m | in the bed | Mafia |
> | Voices through a window (point) | −50 / −53 / −55 | 20 m | has, as a loop | Mafia |
> | Radio through a window (point) | −52 / −54 / −54 | 20 to 30 m (I) | has, as a loop | brief |
> | Work or cooking through a window (point) | by ear, near the window voices (I) | 30 to 40 m | lacks | Mafia |
> | Rain on pavement, awning, gutter (one parameter) | −37, −42, −47 | near | has, one strength | brief, Kingdom Come II |
> | Shop door and bell, house door, knock | −23 to −29 LUFS-M | 30 m; knock 10 m | has, no knock | Mafia |
> | Phone box | −23 to −31 LUFS-M | 30 m (I) | stand-in ring | brief |
> | Others' footsteps | −27 LUFS-M | 20 m | lacks | Kingdom Come II |
>
> Bed mixes stay −36.5 (day), −39.5 (night), −33.5 (rain) LUFS. Spawned sounds are made at the brief's one-shot levels and placed by distance, so they land under the bed (I). Checks: spawned counts per hour, a minimum gap before a take repeats, each source's distance, the bed mixes within 1.5 LU.

(The original uses the minus sign character in the loudness figures; they are copied as found.)

### b. Key measured numbers

Source: 08-sound.md [The numbers; Ambience; Footsteps; Spaces; Objects; Music and mix]. Game numbers are (lead, from game files: event and table exports, bank-header sample names). The interview items are public and stand, but the study saw them only through a summary, so treat them as thin. No loudness target is in either game's readable data.

- Files and events: Mafia 25,600 effect and music files, 15,406 sound events (12,558 dialogue), 1,775 step files; KCD2 6,243 effect files in two main banks, music 202 cutscene files and 278 sequences, 2,164 triggers plus 11,097 for cutscenes (lead). LEDGER in game: 1 traffic bed, 16 steps; built, not in game: 97 (unit 10).
- Zones: Mafia 19 ambience kinds painted on land, 5 of them town; KCD2 Kuttenberg 956 areas, 365 with a bed, 583 setting the echo; the city 323 areas, 88 with a bed (town-wide, street 6 shapes, market 3, square 2); along Tarmark's 49 stations the town bed covers all, a street bed 3; bells 13, point sources 22, a butcher call every 48 to 64 s; 60 one-shots cut from beds (lead).
- Time of day (Mafia, read): dawn 05:00, morning 06:30, day 08:00, evening 18:00, night 21:00. Spawned voices at once (dawn/morning/day/evening/night): quiet street 0/1/3/2/0; crowded 4/12/18/10/6; market 4/14/25/12/6. KCD2 timed calls every 22 to 97 s. LEDGER now a line every 18 to 40 s within 16 m.
- Mafia spawner 76 rows, sounds 20 to 70 m off (quiet street 50 to 70); street activity 32 kinds; birds about 17 species (2 at once in a street by day, none at night); water lapping up to 14 within 25 m; emitters: window activity 40 m, window talk 20 m, cooking and work 30 to 60 m, groups 35 m, church bells 150 m, gulls 57 call files at 150 m, harbour ropes 20 to 50 m; placed ambience median 30 m (p25 15, p75 60). Rain only in mission-named sounds (named, inferred); wind bed above intensity 2.9.
- KCD2 weather: rain, wind, lightning, puddle parameters; rain drops on fabric, plate, wood (13, 11, 8 takes). Fade median 10 m (p75 15); echo switches over 1 m.
- Footsteps: Mafia 53 physical surfaces, 37 step sounds, 5 shod kinds share one set; takes walk 8 (cobbles) to 30 (rough road), smooth concrete 27, wood 20; cobbles set 8 walk, 10 run, 10 sprint, 10 sneak; puddles 10 or 20 plus splash layer 14 or 26; heard to 30 m. KCD2 15 surfaces; stone 13, wood 15, mud 14, water 52 takes (inferred); others' steps heard to 15 to 20 m. LEDGER: Tom's trainers on paving, built 5 surfaces, 8 takes a surface.
- Echo: Mafia 18 reverb sends on 9 impulse responses (3 outdoor share one); Palermo 43 rooms, 75 doorways, 7 shut at start; 4 reverb volumes at once, 3 room sends a sound; sector value outdoor 0, forest 0.2, urban 0.3, indoor 1; listener halfway from camera to player. KCD2 128 settings on 34 reverbs (20 indoor, 12 outdoor).
- Doors: Mafia six kinds, each open, close-creak, close-hit; layers 3 to 5 takes plus shared grit layer (7); heard 30 m; knocks 6 takes, 10 m. KCD2 115 door samples. Church bells in both, no shop bell; phone boxes none (period).
- Music and mix: Mafia 818 score files in 15 chapter folders, restarts after 25 s calm, world music heard 15 to 65 m; 396 mix-state events (314 per story beat); 3 mastering presets, settings unread; fades 2 or 3 s. KCD2 287 music states by priority (time of day 11 to 13, weather 22 to 23, crime 31 to 37, combat 150, cutscene 502); silence most-used confirmed playlist (31 of 299); 14 states hold 2 to 15 s; 3 volume groups; 10 mix setups (one for dialogue) (read). Interview (public, summary only): dialogue is the centre of the mix, wide range, little compression, silence used on purpose, mixed to the quietest lead voice.
- LEDGER's own: day bed 13.5 LU under -23 LUFS (EBU R128, BRIEF.md); bed mixes -36.5 (day), -39.5 (night), -33.5 (rain) LUFS.

### c. Open blind spots

- Inside the banks and as played: bus volumes, falloff curves, reverb and mastering settings, random and sequence rules, music transitions (binaries not parsed); no recordings (25 October). So the relative loudness of ambience, voices, effects and music is unmeasured in both.
- KCD2: how beds change by daytime and rain inside each event; the "d" footstep set; the puddle parameter's use.
- Mafia: emitters placed beyond the Palermo opera level; systemic rain (none found by name).
- The Walden interview was seen only through a fetch tool's summary, not read in full.

### d. The twenty basics

One mention, in the "For LEDGER" block quoted in part a: "**Adopt for footsteps** (the twenty basics, 18): 8 walk and 8 run per surface (unit 10 has 8 a surface, one gait); wet as a splash layer over the dry step; two shoe sets, soft (Tom's trainers) and hard; others' steps heard to 20 m." The list itself is not in this study.

---

## Cross-study note (from the studies' own text only)

Basics cited by number only: Study 02 cites basic 7 ("a hint for each key"), basics 7 and 8 (interface revealed piece by piece) and basics 19 and 20 (autosave and consequence; named only by number). Study 08 cites basic 18 (footsteps). No study in 01 to 08 states the twenty-basics list.
