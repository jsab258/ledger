# Study 15: The crime toolkit (28 October 2026)

How Kingdom Come: Deliverance II makes stealing, trespassing, selling stolen goods and getting caught work as systems, with Mafia: The Old Country as the second opinion; read from their data and Warhorse's public modding wiki, not their code. Our own words and numbers; raw notes on F:/LedgerTools/aaa-study/kcd2/study-11-15/s15/ and F:/LedgerTools/aaa-study/mafia/study-11-15/, read 28 October 2026. Study 1's crime table and witnesses are not repeated. Kingdom Come II stores prices in tenths of a groschen (Study 11); figures here are in groschen (gr). Tags: **M** measured, **R** read, **I** inferred, **N** a name only.

**The short answer.** Kingdom Come II builds small crime from four parts: a stolen mark on every item, fading with its value and with distance from the theft; a privacy label on every place, stricter at night, with a watcher's counter that warns, then escalates; guards at posts who search strangers on a chance roll; and punishments set by the crime, from the pillory to branding. A merchant offered marked goods haggles harder or refuses; no fence is identifiable in its data. Mafia has trespass zones that end in a fight, and no theft, fence, fine or jail. LEDGER should take the mark, privacy by hour and the counter, and leave the punishments, which belong to 1403, not 1990.

## The numbers

| Kingdom Come II | | Tag |
|---|---|---|
| Stolen mark by value | 0.015 h per tenth of a groschen: 1 gr item 9 min; 10 gr 1.5 h; 100 gr 15 h; 1,000 gr 6.25 days | R; I (an item coefficient also enters, in code) |
| Stolen mark by distance | full within 600 m of the theft; 0.15 at 1,800 m; under 0.15 counts as clean | R |
| Never fades | 16 of 5,184 items (money, keys) | M |
| How long the crime is known | theft, pickpocketing, lockpicking 4 days; trespass 2; murder 7 | R (Study 1's table) |
| Stolen keys | lock changed after 3 days | R |
| Search | guards at posts; calm guard and stranger 0.5 a roll, a roll every 3 min, 90 min between searches | R, I |
| Selling marked goods | haggles harder from suspicion 0.1, refuses from 0.5; a first-game script pays 0.4 | R |
| Trespass counter | every 6 to 9 s: + place's severity 0 to 3, +1 night, +1 weapon drawn, +1 hostile, +1 angry watcher. Personal and forbidden places escalate past 12, camps past 25; semi-public and semi-personal stop at 3 | R |
| Fastest escalation | forbidden place, night, weapon drawn: about 27 s (21 s with a nervous watcher) | I |
| Trespass memory | counter 10 min; trespasser remembered 2 h | R |
| Locks, Kuttenberg map | 1,098 doors, grades 1 to 5: 528 / 301 / 42 / 93 / 134 (grade 1 includes 170 without a model); chests with a known model, 1,042: 3 / 250 / 448 / 282 / 59 | M |
| Fines | trespass 25 gr; theft 50 + item's value; pickpocketing 55; lockpicking 60; assault 150; murder 2,000. Pickpocketing, assault, murder and theft's base × 0.5 to 4 by the victim's class | R |
| Talking a charge away | 6 grades by fine; from 2,000 gr it cannot pass | R |
| Jail | 1 to 7 days a crime, scaled like the fine; then three stats × 0.6 for a fifth of the time served | R; I (days) |

**Mafia:** people notice ten times faster in a trespass zone (R); trespass climbs three levels to a drawn weapon and hostility (R); an apprehender's grab distances default to 2.5 and 3 m, one replaced by a setting not exported (I).

## Theft and pickpocketing

- **Who knows a marked item (R):** the owner and his friends, the moment they see it worn; the victim, checking his pockets and up to 4 hiding places within 40 m (anger +0.1, 0.15 or 0.2 for a loss under 50, under 500, above; groschen I); guards on a search; merchants at the sale, where shop stock weighs 10 in the suspicion sum (R; its effect I).
- **Pickpocketing (R):** within 2.4 m, charged 2 to 30 s; harder away from directly behind (0.0027 a degree) and for each earlier robbery of the same person (0.05); sleepers easier (× 0.5). The crime: 55 gr, 2 days, items taken back.
- **Mafia** has no ownership or theft by name (M); loot lists coins, valuables, hairpins and pocket watches (R).

## Trespass, locks and lockpicking

- **Labels (M):** 2,910 labelled areas on the whole Kuttenberg map, town and villages; one area can carry several labels: private 1,176, semi-personal 585, personal 382, semi-public 171, forbidden 29, interior 586. Semi-public counts as semi-personal at night (R).
- **Doors keep hours (R, M):** unlocked 07:30 to 19:30 by default, 05:00 to 21:00 on most placed doors; 44% start locked; a shop locks while closed.
- **The counter (R):** starts at 1 to 3 by the watcher's nerves; a warning every tick, the last at 12; 20 s of grace on leaving.
- **Locks (R):** five grades in fifths of difficulty, taken from the model (doors 0.17 to 0.94, the prison door hardest). The pick wears off the sweet spot and makes noise; a door he opens leaves a marker for 24 h. The crime: 60 gr, 3 days. The formula is in code (N).
- **Mafia (R):** zones are neutral, trespass or hostile; three trespass and three confront levels, then a drawn weapon; the apprehend tree tries a grab and fights if it fails. Picking shows only as a hairpin attachment and knife-picking animations (N, I); safes by type names only (N).

## Fencing

- **A merchant answers a basket four ways (R):** buy; haggle harder (suspicion 0.1); refuse (0.5); never buy back his own stock.
- **No fence in the files (M).** A script function that no readable file calls (I) would soften a refusal to haggling for a class marked as dealing in stolen goods, and harden every other merchant's haggling into a refusal; no class carries the mark. Two traffickers and a smuggler appear among shop names (N), unconfirmed as fences.
- **Prices (R, I):** an honest sale pays about 0.85 of value for rings and loot, 0.3 to 0.5 for gear (I, from the shops' multipliers). A marked deal that goes through pays 0.4, in a script kept from the first game; whether the sequel runs it is unverified. A merchant pays no more than his cash, 35 to 1,500 gr (R).
- **Mafia** has no fence and no selling (M).

## Getting caught

- **The search (R):** guards at posts only; likelier with an angry guard and a stranger, less with a friend; a guard on the move never searches. Refusing is a crime (10 gr, 1 day). It takes every marked item, on him, his horse and within 3 m.
- **The arrest (R):** pay (if he can), talk (six difficulties set by the fine), fight, flee, or accept a punishment; items are confiscated unless he talked his way out. No bribe for a guard was found (I); a victim may settle privately for payment (R). The class multiplier is 0.5, 1, 2 and 4 in the parameters and 0.5, 1.5, 2 and 6 in a script; which the engine uses is unknown (R).
- **The punishment (R):** branding for murder, poaching or a fine over 2,000 gr; a beating for violence; else the pillory. A second branding is execution, a game over. The pillory lowers charisma and makes him easier to notice; branding halves reputation gains while it lasts (permanently in hardcore). Jail comes if guards knock him out: days added up, three stats cut after. Then time skips: short between 08:00 and 17:00, long otherwise; far from the site, to 10:00.
- **Mafia** has no arrest, fine or jail (M): capture is a fight; a failed mission returns to its checkpoint (R).

## Reputation by place and crime

Beside Study 1: witnesses' reactions median −0.1, murder −0.45 (M); theft −0.25 with the victim, −0.15 once reported (R). A charge talked away still costs 0.18 (R). No fading parameter was found (M). Mafia has none.

## For LEDGER

Every item below is a target for the crime layer when it is built (D56, stage 3), not work for now: new systems wait for a place in PLAN.md (29 September ruling).

**Buying, selling and fencing (the 23 September ruling):**
1. **Adopt: a hot mark on goods, fading by value and distance, while the memory never fades.** Hot to those who know it: owner, household, anyone told. Start from 0.015 h per tenth of its value, rescaled to LEDGER's 1990 prices; full in the theft's district, gone across town. The moat holds (memory permanent, remedies behavioural): the item cools, the owner never forgets; the crime itself stays known as the moat says, not 4 days. Serves the Coat and the ruling.
2. **Adapt: three answers at the counter:** buy at the honest rate; haggle harder once the goods are a little hot (Kingdom Come II: 0.1); refuse once plainly hot (0.5) or when the buyer knows the owner. Plus a fourth: he remembers, and may tell (Gossip). Serves D24 (trade must not look broken) and D25.
3. **Adapt: the fence is a person,** which Kingdom Come II lacks. The pawnbroker (Empire's fencing line already needs the pawnshop) buys hot goods at 0.4 of an honest sale to start, pays only what is in his drawer (Purses), and becomes a second person who knows, with his nerve and loyalty: D56's rule that the accomplice is the risk. 0.4 is Kingdom Come II's figure; the 1990 rate is owed to LEDGER's own research.
4. **Buying:** shops with opening hours from their people and doors, finite cash and a weekly restock (Study 11).

**The crime layer:**
5. **Adopt: privacy by place and hour.** Each room on Quay Street gets a label (private, personal, semi-public, forbidden) and a night rule; Access already gates rooms by hour and has a person say the refusal. Serves Access, phase 3's prompts and P4.
6. **Adopt: the warning counter as the refusal's escalation:** warn, warn again, call someone or act; a tick every few seconds, faster at night and with a weapon, under half a minute at worst; semi-public places warn but never escalate. **Adapt** the 2-hour memory: the counter resets, the sighting is kept for good (the moat). Serves the 23 September ruling on deeds seen, and D25.
7. **Adapt locks:** one key among several (Access: nothing is simply locked), forced at a cost: noise, a door that shows it for a day, a crime. No lockpicking minigame (D24's spend rule).
8. **Adopt the search's reasons, not its chance roll:** a search follows suspicion, never chance (Coat); a stranger and an angry or unfriendly officer feed it. Refusing is not an offence in LEDGER, but people see it (Coat); hot goods found are kept as evidence, as Custody keeps the coat.
9. **Ignore** the fines, pillory, beating, branding, jail days and execution: in 1990 an arrest means hours, a caution, or a charge and bail (Custody, from LEDGER's research), and canon's endings hold (D58).
10. **Ignore** reputation numbers (D33, D34): a talked-away charge costs that the person remembers.

**The owed verbs (D56):**
- **Verb 4, lean on a witness:** in neither game. LEDGER's rulings already let a witness be talked round or threatened (1 and 3 October); Kingdom Come II's nearest, a victim paid to settle privately, shows the bought retraction's simplest form.
- **Verb 5, move or hide a body:** Kingdom Come II carries bodies (Mafia has carry-body tags, N); an undiscovered one vanishes after an hour; a missing-person record (not a crime) exists. **Ignore** the vanishing (a killing is remembered forever; a body never fades in Gossip). **Adopt** the missing person: a resident who stops keeping his routine (CastDay) becomes a question the town asks, the gap between act and finding.
- **Verbs 1, 2, 3, 6, 7, 8:** in neither game (M); LEDGER's own design.

## Coverage map

To tick in REFERENCE.md: crime (arrest, search, punishment, theft, trespass, fencing; both games); doors and world interaction (locks); abilities and effects (punishments as buffs); perception (trespass awareness).

## Open blind spots

- **The engines' code:** the lockpicking formula; how a merchant judges suspicion; whether the fence and 0.4 scripts run; how a witness chooses to arrest, settle or report; which class multipliers apply.
- **Not in the data:** who fences (the traffickers by name only); units of buff and jail durations; Trosky not counted. **Mafia:** lockpick and loot tables not exported, as the F: drive filled on 28 October.
- **Shown only in play,** such as how a search looks. No recordings (25 October).

## Sources (read 28 October 2026)

- **Kingdom Come II's files:** behaviour trees in Scripts.pak (AI/crime, AI/npc/basic/switch, the punishment quest); Crime.lua, AnimDoor.lua; Libs tables (crime, buff, game_over, social_class, item, shop, ScriptParams); the Kuttenberg map's objects and layers. Warhorse's wiki (warhorse.youtrack.cloud) through its public interface, in full: KM-A-20, 21, 27.
- **Mafia's files:** the confront and apprehend state trees, the calm awareness config, type names, DefaultGame.ini.
- **LEDGER:** Core (Access, Coat, Custody, Purses, Empire, Gossip, CastDay); RULINGS.md; the D56 record.

## Review

A fresh reviewer (28 October) checked about 45 numbers, 22 re-measured: pass with fixes, all applied (escalation by place, the time skip, which fines scale, the missing person, the fence script, the escalation example, map-wide labels, Mafia's tags, Coat's refusal, verb 4, item 3; added crime duration, honest sale rates, the 29 September ruling). Cost, from the clock: with Study 11, 10:35 to 11:37.
