# Study 14: Combat and violence (28 October 2026)

How Kingdom Come: Deliverance II (KCD2) and Mafia: The Old Country (Unreal 5.4) make a fight read, land and end, and what the street does, set against LEDGER Combat: Final State (game-design/combat-design.md). Read from the games' own files on 28 October 2026, not their code; our own words and numbers; raw counts on F:/LedgerTools/aaa-study/kcd2/study-14/. Tags: **M** measured, **R** read, **I** inferred, **N** name only. COMBAT.md's public pass is not repeated.

**Disk.** F: filled during the morning's parallel studies, so Mafia's combat folders (close-combat plug-in, abilities, camera, hit reactions, coordination) were never exported. Mafia is read from earlier studies' exports and its package index; what needed the rest is marked not reached (disk).

**The short answer.** KCD2 is the reference for timing and consequence: one table of blows keyed by weapon, an unarmed blow landing about 0.75 s into the swing, reactions by hit zone, morale that ends fights, a town that warns, flees, reports and fines in numbers. Mafia is the reference for contact: motion warping instead of lock-on, a hit-stop per kind of blow, a melee camera held 0.8 s, layered sounds, paired moves fitted to cover by height. No hit-pause length was reached. LEDGER's strike timing survives; its recovery and reaction variety change.

## The numbers

| | KCD2 | Mafia | LEDGER now |
|---|---|---|---|
| Unarmed: swing start to contact | 0.75 s median, 0.63 to 0.80; 10 hooks and 6 kicks (M) | hit window open 0.39 to 0.66 s (right), from 0.27 s (left) (M) | B01 0.73 s |
| Contact to end of blow | about 0.4 s (I, from medians) | not read | B01 0.60 s |
| Sword; blunt, to contact | 0.70 s; 0.93 s (M) | knife: not reached (disk) | none |
| A miss | 0.67 s clip, weapons only (M) | not read | B02 1.20 s after |
| Hit reaction | 1.27 s median of 132; to unarmed blows 1.18 s; weak class 0.6 s (M) | 1.06 s to blend-out; flinch 0.9 s (R) | D03 0.60 s, D04 1.00 s |
| Reactions by side | head 25, upper left 27, upper right 27, lower 53 (M) | 4 directions by 7 body parts: 53 hits, 14 stuns, 6 flinches, probably for gunfire (M names, I) | one per footing |
| Shove reactions | none apart from a push out of a clinch (I) | civilians from 4 sides, men and women, 2.8 to 3.9 s (M) | D01 0.83 s |
| Hit-pause | none in data (M) | hit-stop plug-in, 11 curves (N); values not reached | 2 frames, judgement |
| Camera | first person, lock-on | melee camera held 0.8 s (R); 13 melee shakes (N) | 1.5° nudge |
| Closing in | unarmed hit distance 1.0 m, reach 1.6 m (M, R) | warp up to 2 m, to 1 m off, in 0.42 to 0.52 s (R) | reach 1.6 m |
| Stamina | 26 a swing (R); regen 22 a second (wiki) | pool 1.0; an opponent regains 0.18 a second (R) | swing 0.34, regen 0.09 |
| Health | 100 (wiki) | ordinary man 5, brute 10, duel opponents 10 to 35 (R) | floor 2.8 |
| Blows to put a man down | not derivable (code) | not reached (disk) | 4 (Combat.cs) |
| Attackers at once | no cap, token or slot (M); at most 2 s between a man's blows (R) | duels one against one; brawls not reached | half-gap offset |
| Paired moves | 1,683 options; 1 of 762 fragment records checks for an obstacle (M) | 19 takedown designs, 13 fitted to cover (M, names) | G01 to G04 drafted |
| Assault | fine 1,500 (tenths of a groschen), 5 days, kept 5 days; unarmed half (R) | nothing kept (Study 1) | harm book |

## The read

- **KCD2 times every blow in data** (221 options); its fields read as swing live, contact, end of the active window and clip end (I: the wiki is silent). Hooks land at 0.70 s, kicks at 0.78 s; the swing goes live about 0.17 s before contact (M).
- **Mafia's fists** come in a two-blow and a three-blow combo, the latter's window opening at 0.04 to 0.08 s (M, montage notifies); a window is not contact, which was not read. They aim by motion warping (its own class, H13MeleeWarp) and a rotation curve, not lock-on (R).
- **Telegraphs:** KCD2 has 10 combat shouts, sounds only (M); Mafia's duel opponents taunt, warn before a grab, grow impatient (N).

## The contact

- **Hit-pause:** none in KCD2's data; a perk slows time on a perfect block (R). Mafia's 11 hit-stop curves split a duel's light, heavy and guarded blow, the victim's, knife blows, and a world slow-down for fists, a "bash" (probably a gun butt, I) and knives (N).
- **Camera:** Mafia fires a shake at a fixed point in the alert-stance swing, 0.19 to 0.21 s (M), with separate shakes for a hit, a bash and a swing (N).
- **Sound layers:** Mafia: whoosh; impact by who hit whom or what; the victim's pain in three sizes, 60 events each; the attacker's effort (N). KCD2: impacts by face or body and by cloth, mail or plate; 294 triggers, 168 with a controller pulse (M).
- **Physics:** KCD2's 129 combat deaths hand over to ragdoll and its 132 combat reactions do not, but its general table allows ragdoll on 85 of 91 major reactions and on 101 paired hits (M). Mafia ships a physics hit-reaction plug-in (N). Both blend physics into hits.

## The odds

- **Blows to a knock-down:** neither gives it; LEDGER's four blows stay its own.
- **Several attackers:** KCD2 only stretches each man's gap (0.8 per extra attacker, wiki) and caps nothing (M). Mafia's duel opponents start with 1 to 5 attack points (maxima 6 to 16) and spend them to swing (R); its coordination plug-in, which names combat jobs, was not exported.
- **Morale (KCD2, R):** a landed hit moves it 0.02, an ally's death 0.2, an ally fleeing 0.1, being outnumbered 0.05 to 0.2. Fights end by events more than by wear.

## The surroundings

- **KCD2 barely uses them:** one obstacle check in 762 records (M). Its only push (so read, I) comes out of a clinch: 11 options; the unarmed one is 1.6 s, contact at 0.73 s (M).
- **Mafia builds them in:** 19 stealth takedown designs (knife kills and chokes), most in front- and back-facing versions; 13 fitted to cover by height (about 110 and 140 cm), depth, and high cover left or right (M, names). No railing, table or ground move by name.
- **Weapons at hand:** no pick-up system in either; Mafia models a police baton and a gear lever as melee weapons (N).

## Before the blows

- **KCD2 escalates in counted steps (R):** a drawn weapon brings a guard's warning, then arrest after 30 s (only the nearest man within 2 m reacts). An arrest is repeated every 6 s (±2); four unanswered demands, or one refusal, bring force. Anger runs in bands at 0.3, 0.6 and 0.9. Intimidation is a speech check.
- **Inside a fist fight (R):** five fouls end it (a drawn weapon among them); an opponent arms himself at health 30; a quest knock-out lasts 10 s.
- **Ends (KCD2, R):** surrender at morale 0.2 (the man kneels up to 550 s of game time; spared, he will not yield or run again for 30 s); flight (30 m off, 420 s); knock-out (punch, hook, kick, throw and push are flagged unable to kill, one unarmed finisher excepted); death. A beaten player is robbed by chance (0.9, 0.5 or 0.1 by anger) of 5 to 15% of his money; hostile winners end the game.

## The street's response

- **During (KCD2, R):** a witness picks among 10 reactions (attack, arrest, flee, report, watch among them); he flees rather than watches once a weapon is out; watchers keep 3 m; a computed cap of 2 to 8 react; a crime carries 10 m, an alarm 25 m; a reporter seeks a guard within 150 m; extra guards come at faction anger 0.8, checked each minute. No guard arrival time exists in data.
- **After (R):** murder 20,000 and 7 days; an unarmed hit costs 0.15 of reputation, an armed one 0.45; it reaches the faction in about three hours (wiki). Mafia's civilians panic and forget (Study 1).

## Weapons

- **KCD2, one system:** one table keyed by weapon class; reach fists and dagger 1.6 m, mace 2.1 m; slashes, smashes and kicks cost 1.2 times the stamina; a mace can kill, fists cannot (R). The dagger lives only in paired moves (M).
- **Mafia, three systems:** fists; a knife with its own duel mode, takedowns, throw and wear; a cover shooter (20 weapon curves, N).

## For LEDGER

1. **Adopt B01's contact at 0.73 s:** KCD2's unarmed median is 0.75 s; Mafia's windows open earlier, at an action game's pace. (Readable; the first combat test.)
2. **Adapt the recovery:** free 0.4 s after a landed blow (KCD2); 0.8 s after a miss, by judgement. (A miss leaves you open.)
3. **Adapt the reactions:** by side, D03 front, left and right, D04 left and right. D03 keeps 0.6 s (KCD2's weak class); D04's 1.0 s matches the games' ordinary 1.06 to 1.18 s. Physics blended over authored clips, as the design says. (The animation question; risk R4.)
4. **Adapt Mafia's contact kit, our values:** a hit-stop per kind, a brief camera close-in (about 0.8 s), offsets by hit direction, a shake from the swing. Hit-pause stays 2 frames until a value is read. (Weight; no mode.)
5. **Adopt motion warping for lock-on:** slide to a set distance in the wind-up (Mafia 1 m, at most 2 m). Unreal 5.8 ships Motion Warping; Mafia's class is its own, so the settings are ours. (No lock-on.)
6. **Adopt the four sound layers,** our own or CC0 recordings (D26). (Weight.)
7. **Adopt KCD2's morale for other men's endings:** back off, run or yield at 0.2, moved mostly by events. (How fights end.)
8. **Keep the attacker offset:** KCD2 caps nothing; Mafia's attack points are an option against NPC mashing. (Two against one; the gaps stage.)
9. **Adapt Mafia's surface method:** each paired move in both facings, fitted by height. Seven places, each with a shove-into and a pin, make 14 designs, 28 with facings, against Mafia's 19 and 36 (I). (The street is a weapon.)
10. **Adopt KCD2's street numbers as first values:** watchers flee within 3 m; all flee once a weapon is out (rung 6); 2 to 8 react; a drawn weapon brings a warning, then arrest at 30 s. Police arrival: judgement. (The ladder; police arriving.)
11. **Adopt the grading:** an unarmed hit costs a third of an armed one in reputation, half in fines. (Rungs 5 and 7.)
12. **Adapt KCD2's beaten player for Tom:** robbed by chance, no game over. (Tom cannot die.)
13. **Ignore** lock-on, first person, Mafia's duel mode, finishing clips, skill-widened windows (Tom does not improve).
14. **For Jafar:** whether fists can kill (KCD2: no) is a violence line, his to rule; the source test's 6 clips change his design's 4.

## The first combat test and the source test

The first combat test needs **22 clips**, shared by both men: COMBAT.md's 19 (sections 5.2 and 5.6) with B01's and B02's recovery changed and D03, D04 made by side.

| Kind | Clips |
|---|---|
| Stance | A01 square up, A02 hold, A03 stand down |
| Blows | B01 strike lands (contact 0.73 s, free 0.4 s after), B02 misses (free 0.8 s after), C01 shove |
| Guard | E01 raise, E02 hold, E03 takes a blow |
| Reactions | D01 shoved, D02 shoved and falls, D03 struck steady ×3 (front, left, right), D04 struck reeling ×2 (left, right), D05 reeling, D06 knocked down, D07 down, D08 gets up |
| The wall | G01 shoved into a wall, G02 rebound |

**Recommended: the animation source test reaches 6 clips**, each within one frame of its timing: B01, C01, G01 and D03 in three sides. One hit reaction cannot show that a source makes a family; both games author reactions by side. The design says 4, so this waits for his yes.

## Coverage map

Ticked: melee and close combat, damage and hit reactions, melee abilities, KCD2's attacker spacing, guns by name. Open: Mafia's combat folders (disk).

## Open blind spots

- **Not reached (disk):** Mafia's hit-stop lengths, damage, contact moments, knife timings, parry and dodge windows, attack-point regeneration, brawl coordination, shake and physics values.
- **In code:** KCD2's damage formula, perfect-block window, how a fight becomes a crime.
- **Unverified:** KCD2's timing fields, the 2 s gap (a maximum-delay field), fine and jail units; 687 wiki-only constants; retail against 1.2.
- **Only in play:** hit-pause feel, Mafia's brawl spacing, police arrival; no recording or public source measured them (COMBAT.md).

## Sources (read 28 October 2026)

- **KCD2's own files** (1.2, unpacked): Tables/combat (92 files); rpg (constants, perk overrides, crime, morale, reputation, anger, buffs, game over, shouts); ai/ScriptParams; about 700 crime and reaction behaviour trees as text; the fist-fight quest library. Counts in F:/LedgerTools/aaa-study/kcd2/study-14/ and street/.
- **Warhorse's modding wiki,** public interface: KM-A-20, KM-A-27, KM-A-12.
- **Mafia's own files,** exported earlier with FModel: the hero's fist and hit-reaction montages, civilians' reactions, attribute tables, gameplay effects, duel stance data; the package index for names. Counts after the stop order were kept in the session's scratch space, not on F:.
- **LEDGER:** game-design/combat-design.md; COMBAT.md 5.2 to 5.6; RULINGS.md, 12 October.

## The fresh review (28 October, Opus: pass with fixes, all applied)

About 45 numbers confirmed. Fixed: the unarmed sample (hooks and kicks), the obstacle base, the arrest rule, attack-point maxima, takedown designs (19, not 36), the attacker cap (KCD2 only), physics in hits, the slow-motion source, threats and cues. Hedges: window against contact, gunfire reactions, the miss as judgement, field units. Added: Mafia's shove reactions, KCD2's fist-fight rules, two questions for Jafar.

Cost, from the clock: 10:25 to 11:45 (two KCD2 helpers in parallel, synthesis, review, fixes).
