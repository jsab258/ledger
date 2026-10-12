# COMBAT: how Kingdom Come 2 and Mafia: The Old Country do melee, set beside our combat spec

13 October 2026 (Jafar's local time). Cloud week 42, unit 7b, the combat part. Public pages only. Nothing from either game (files, text, pictures, sound) is in this file: only our own sentences, our own arithmetic and the developers' published numbers, each with its source key. The keys are listed with their links at the end.

## In plain words

1. Neither game has a published timing test. The only hard numbers are Warhorse's own rules table for Kingdom Come 2 (stamina costs, about 2 seconds between a careful opponent's attacks, a slower rhythm for each extra attacker). For Mafia's knife duels there are no numbers at all, only "the timing window is different for each input".
2. Both games make a blow readable with one clear signal (a green shield, a red glint) and keep a slow, patient rhythm. That backs our spec's "telegraph, not tell". Kingdom Come's stamina, witnesses, town unrest and surrender-or-mercy choice suit LEDGER. Its stats, perks, skill-grown parry windows and lock-on do not.
3. Of 42 points taken from the spec, 12 are ADOPT, 25 are ADAPT and 5 are IGNORE (section 4).
4. The draft list for phase 3 has 17 animations for two men with a shove and a strike (section 5). Its key choice: the strike winds up for 0.65 s (20 frames at 30 fps), because a person needs about 0.2 s just to see a move and more to choose. That number is our judgement, not copied from a game.
5. Jafar needs to do nothing now. Combat waits for characters (PLAN.md defers it); section 5 is the brief for the day they land.

## 1. How to read this file

- **Marks.** official (the developer's own page or wiki), interview (a named developer's words, printed by someone else), wiki (a community wiki), player (a forum post or a named guide writer), press (a critic or a guide site), standard (a public convention), derived (our arithmetic, formula shown), judgement (ours), unverified (could not be confirmed, used in no total or ratio).
- **Date read.** Every source was read on 13 October 2026 (Jafar's local time; the machine clock showed 22:04 UTC on 12 October). No other date is given per source.
- **How much was read.** Every page was read to its end, with two kinds of exception named in the Sources list: the long patch-note pages and the official rules table were read through their combat, crime, takedown, tutorial and feature sections, and their quest-by-quest fix lists were searched by keyword, not read line by line.
- **Words used.** A frame is one picture of an animation. At 30 frames per second one frame is 0.033 s. The wind-up is the slow part before a blow lands. Hit-pause is a freeze of one or two frames at the moment of contact. Footing is the spec's word for steady, reeling or down.
- **Names.** Canon names are used: Tom Nowak and DS Carol Ellis. The spec still says Tom Novak, Mara Ellis, and that Tom "runs a bar". Canon (D19) says Mickey's is a minicab office. The spec's argument holds with a minicab office.
- **Game material.** Official parameter names are quoted only so a reviewer can find the row. Quotes are under 15 words.

## 2. Kingdom Come: Deliverance II (KCD2)

### 2.1 What it is, for this comparison

- First person, open world, set in 15th century Bohemia [K17, K39]. Melee uses a lock-on "combat rose" with spokes that show the swing direction [K23]. Warhorse's own words for it: "authentic first person combat" [K39].
- Warhorse says success comes from mastery of techniques, "rather than an unseen roll of the dice" [K5]. The official modding wiki shows that NPC choices are chance weighted (section 2.3).
- A developer says the combat is "on its basis, the same combat as in the first game", with new movement sets and more animations [K15, Tobias Stolz-Zwilling, Warhorse PR manager, 3 March 2025]. Another developer interview says there are "many iterative changes to the combat", some to make it easier, some to make it deeper [K16, Martin Ziegler, Warhorse lead scripter, 15 July 2024].

### 2.2 The moves

| Move | What it is | Source and mark |
|---|---|---|
| Directional strike | Four directions (up, down, left, right) for most weapons, three for polearms. The direction is chosen with the mouse and shown on the rose. Guides disagree on which weapon lacks which direction. | K18 wiki, K34 player, K31 press |
| Thrust | The arrow at the bottom of the rose is for stabs. One player says KCD2 has no point-stab; patch notes still speak of "slash or stab" damage for master strikes. Conflict, not resolved. | K18 wiki, K33 player, K9 official |
| Chain | Press attack again while the first swing is still going. | K18 wiki |
| Combo | A set order of directions; the last blow is a special one. Taught by trainers. Patch 1.4 cut every polearm combo to three moves. PCGamesN lists combos of three or four inputs, and three unarmed combos. After each swing the weapon moves by itself to a set next side, which is why some combos need no steering. | K27 press, K11 official, K34 player |
| Feint | Hold attack in one direction, change direction, then release. The foe has less chance to block. | K19 wiki |
| Block | Hold the block key. Costs stamina in proportion to the blow. Enemies can still land techniques on a plain block. | K18 wiki, K28 press |
| Perfect block (parry) | Press block when the green shield shows. Costs no stamina and breaks the foe's chain. | K18 wiki, K28 press |
| Riposte | A counter-blow right after a perfect block. A riposte can only be stopped by another perfect block. It costs stamina. | K18 wiki, K28 press |
| Master strike | A counter from the opposite side at the green shield. Taught by Master Tomcat after a duel. Sword only, say Gamerant and the players; one player says NPCs use it in a fist fight. | K24 press, K31 press, K32 player |
| Dodge | A sidestep that costs stamina (official cost 20, section 2.3). A perfect dodge is timed to the same shield. Guides say it suits fists best. | K1 official, K28 press |
| Clinch, lock, grip, throw | Warhorse says "locks, grips and throws" were added so a man can be grappled into submission, and that an unarmed man can disarm an armed one. A patch note says the clinch can push a man out of a fighting pen. A perk lets two unarmed men go from a clinch to an arm lock and a chokehold that knocks out. | K5 official, K9 official, K29 press |
| Shove or kick | The first game's codex has a kick that pushes a man away. For KCD2 no page read describes a kick or shove as its own verb; the clinch push above is the nearest. | K22 wiki (first game), K9 official |
| Fists | Hooks and jabs in the first game's codex. For KCD2, a wiki says a fistfight uses fists and "occasional kicks". | K22 wiki, K18 wiki |
| Tackle | A tackling attack exists (patch 1.2 mentions it). No timing published. | K9 official |

### 2.3 Timings: who measured, and what is official

**Nobody named has measured KCD2's wind-ups or parry windows.** No frame count or seconds figure for a swing, a perfect block or a master strike was found with a stated method. What exists is Warhorse's own rules table, below. It was exported on 14 January 2025, before release (4 February 2025) and before patches 1.2 to 1.5, whose notes say combat was rebalanced [K9, K10, K11, K12]. Retail values may differ. All rows are from K1 (official), the wiki page "RPG Constants/Params".

| What it is | Official name | Value | Unit |
|---|---|---|---|
| Stamina cost of one attack | BaseAttackStaminaCost | 26 | stamina points |
| Stamina cost of one dodge | BaseDodgeStaminaCost | 20 | stamina points |
| Stamina regained at rest | StamRegenBase | 22 | per second |
| Regain while a block is held or the weapon is raised | StamRegenBlockMod | 0.6 | times the base |
| Regain while moving | StamRegenMoveMod | 0.75 | times the base |
| Stamina lost when a blow is stopped | MinStaminaDamage, MaxStaminaDamage | 15 and 40 | stamina points |
| Share of a swing's stamina taken when the strike begins (the rest while the weapon is raised) | StaminaDrainRatioStriking | 0.7 | share |
| Delay before a held attack starts to charge | AttackChargingBeginCooldown | 0.2 | seconds |
| Time to reach full charge | AttackChargingCooldown | 1.4 | seconds |
| Mean gap between attacks for a defensive AI fighter | CombatAutoMaxAttackDelay | 2 | seconds |
| How the gap grows for each attacker | CombatAutoAttackDelayIncreasePerAttacker | 0.8 | "how many times the period is increased" |
| Smallest perfect-block slot at the lowest skill | MinPerfectBlockSlot01 | 0.3 | unit not stated |
| Perfect-block window, as a share of the lead time of the attack | MaxPerfectBlockSlotModifier | 0.85 | share |
| Fewest steps in an AI combo | ComboMinSteps | 3 | steps |
| Danger stays on after the last enemy stops being a threat | CombatDangerCooldown | 0.5 | seconds |
| Distance inside which the "active combat" icon is used | CombatActiveNPCRadius | 10 | metres |
| Time an AI hunts a target | CombatAutoMinHuntAttackDuration, CombatAutoMaxHuntAttackDuration | 15 and 60 | seconds |
| Morale needed so an NPC does not flee a fight | MoraleForCombat | 0.2 | scale 0 to 1 |
| Attack from behind counts from this angle, and adds | FromBehindAngle, CombatDmgRBonusFromBehind | 2.356 radians, 1.2 | angle, multiplier |

Derived from those rows (formula shown; none is an official figure):
- At rest one attack's stamina comes back in 26 / 22 = 1.18 s. With a block held it takes 26 / (22 x 0.6) = 1.97 s. A dodge takes 20 / 22 = 0.91 s. (derived)
- 2.356 radians is 135 degrees (2.35619 x 57.2958 = 135.0). (derived)
- If the gap rule is "the period grows by 0.8 of itself for each extra attacker" (our reading, unverified), the gap is 2.0 s for one attacker, 3.6 s each for two, 5.2 s each for three, 6.8 s each for four. The crowd as a whole then swings at about 0.5 to 0.6 times a second whatever its size (derived from an unverified reading).
- Reading of the perfect-block row: the window is at most 85 percent of the time between the slot opening and the hit, and it widens with the square root of relative skill (the official table gives the exponent 0.5). So a slower attack gives a longer window. This is a reading of a help text, unverified.
- The same table holds chance-weighted AI choices: block, perfect block, master strike and dodge each have a pair of probability values, and combos have step probabilities (names such as CombatPerfectBlockProb1 and ComboNextStepProbHit) [K1]. The AI is not deterministic even though the player's results are.

What the patches say about timing, without numbers [K9 patch 1.2 unless marked]:
- "Introduced a short delay between melee attacking an opponent while not locked on to reduce the effectiveness of attack spamming."
- A hit reaction now slows the player, so he cannot "easily back away from attacking enemies".
- Being hit no longer interrupts drawing a weapon.
- Patch 1.4: practice opponents "start practice fights in defense" [K11].

**Numbers from guides that could not be confirmed (unverified, used nowhere):**
- Expert Game Reviews gives a table with a perfect block of 12 to 18 frames (200 to 300 ms) and a master strike of 9 to 12 frames (150 to 200 ms) at 60 fps. It names no measurer and no method, and it says master strike unlocks at combat level 5 from Captain Bernard in Rattay, which contradicts the other guides, which name Master Tomcat [K36].
- LootLore gives a master strike window of about 0.4 s (24 frames at 60 fps), widening to 0.55 s with a perk, and says Warhorse confirmed a 30 percent reduction in a dev blog. No such post was found. It also says the skill unlocks at Defense 8 and works unarmed, which contradicts Gamerant, Seven Swords and the players [K37].
- Both contradict the official table, where the window is a share of each attack's lead time rather than a fixed length (reading above).

Official stat names tell what the system tracks, without values [K2]: the player has slots for perfect block, dodge and combo; a clinch advantage and clinch attack; knock-out and unconsciousness protection; a surrendering state; separate anger from violence and from material loss; reputation that spreads by distance, relation and ancestor. The table list [K3] shows combat data held as zones, guard stances, animation steps and combos.

### 2.4 Stamina

- Official: an attack costs 26, a dodge 20, sprinting 3.5 a second, and a stopped blow takes 15 to 40 [K1]. Wiki: attacking, blocking and sprinting spend stamina; low stamina weakens blows and leaves you open [K18, K21].
- Armour turns blows into stamina loss while stamina lasts, and into health loss when it is gone, so a fully armoured man has to be worn down first [K18 wiki, K22 wiki for the first game].
- Stamina returns "fairly quickly" if you stand still, slower in a fight [K21 wiki]. Official: x0.6 while blocking, x0.75 while moving (table above).
- A wiki states a maximum of 136 stamina. No method; unverified [K21].
- Warhorse's own tip: switching to the sword is faster than reloading a crossbow [K8].

### 2.5 How many enemies attack at once, and how the AI queues them

- **Official.** The rules table has a gap between an AI fighter's attacks (mean 2 s, defensive) and a factor that lengthens the gap for each attacker, with separate smaller factors if the victim is on a horse (0.1) or holds a ranged weapon (0.2) [K1]. A movement-activity value also drops by 0.5 for each additional attacker (the help text is terse) [K1]. That is a spacing rule, not a strict queue of one.
- **Talk.** The 2025 GDC talk by Warhorse's Matej Marko is about NPC behaviour made from goal-planning and modular behaviour trees: the desired state of an NPC is the goal, planning finds the actions [K13, abstract only]. The page does not mention melee. Its video was behind a login limit.
- **Patch.** Patch 1.2 added tutorials "providing hints about fighting multiple opponents" [K9].
- **Players disagree.** One says the others "just come close, gang up on you" while you are locked on to one [K33]. A guide writer says an attack from behind is almost impossible to block or dodge, and advises keeping all enemies in view and only single attacks [K35]. Another poster says to use terrain so they come one at a time [K33]. A search summary of a GameSpot review says enemies are less aggressive and can be taken one at a time; that page was not reached (403) and nothing from it is used.
- **Design reading (ours, unverified).** With a gap that grows with the crowd, the official numbers look built so that three or four men do not hit three or four times as often. They stay dangerous because the player can lock on to only one.

### 2.6 How fights end

- **Death or knock-out.** Armed fights can kill. Official help text for the unarmed case says health "cannot reach" a knock-out level, value 0 [K1]; our reading is that fists knock out and do not kill (unverified reading). Knock-outs get their own count in the statistics [K18 wiki]. A knock-out is held as an unconsciousness "depth": 480 after a combat hit, used up at 1 per second plus a term for vitality [K1, official names CombatHitUnconsciousDepth, UnconsciousDepthFadeoutSpeedBase]. That is about 480 s before vitality counts (derived; whether game time or real time is not stated, so unverified).
- **Surrender and mercy.** Surrender goes both ways. Patch 1.2 fixed "sometimes missing the chat option to surrender" and the reaction of an NPC "being attacked, but missed, while they're surrendering to the player" [K9]. Patch 1.3 fixed "the combat opponent asking for mercy while performing a combo" and made Cumans met on the road stop surrendering [K10].
- **The first game's rule, which KCD2's patch notes follow in part.** A beaten man can surrender honourably; the winner may let him go, refuse, or take money or gear as a price. You cannot surrender to bandits or to a mortal enemy. After one surrender to someone you must wait before you can again. Surrender is only possible within a few metres [K22 wiki, first game's codex].
- **Hardcore Mode.** Warhorse's own description: "You won't get surrendering enemies, visual cues in combat" [K6]. So surrender is a switchable assist.
- **Mercy kill.** A separate execution is used on a weakened or downed foe; a patch added the face animation for it [K9]. A wiki says a finisher is used when the enemy's health is low and needs no stealth [K18].
- **Flight and guards.** Running from guards leads to a chase and a "wanted" state; guards attack if you run when confronted [K18, K26]. An NPC with morale under 0.2 flees a fight [K1]. A patch fixed NPCs being "indecisive about bandaging themselves, fighting, or running away" [K9].
- **A fight in the story.** A fight can be a scripted bout (tourney, duel, fist fight) with its own crime rules; patch notes record many fixes where a crime during a bout broke it [K9, K10, K12].

### 2.7 Witnesses, guards, crime and reputation

This ties to KIT.md and coverage-audit-kcd2. The audit built its rows B2, B3, E4 and E5 from search summaries; the pages below were opened, and they confirm B2 and E5 and add numbers.

- **Who reports.** A guard who sees a crime reports it; civilians can report and set off an investigation [K26 press]. A witness can also ask money for silence, in the pre-release preview [K25 press, 16 August 2024]. An NPC about to raise the alarm can be killed before the alarm goes out [K30 press].
- **Where it lives.** KIT.md could not find where KCD2 records witnesses. The official crime page says the crime logic is "mainly in AI Behavioral trees" with a few values in tables [K4]. The rules table holds the perception numbers: a view radius from 2.5 m (an almost blind NPC) to 50 m, a penalty to visibility at night outdoors, 4 s of recognition time for an unremarkable person, and a 4 s decay before NPCs become unaware of you [K1].
- **Evidence.** Being seen near evidence such as a corpse still gets you accused [K25]. A corpse is hidden from the world 300 s after it is discovered, or 3,600 s if undiscovered (game time) [K1]. Crime entries carry fields named expiration and isSpreadable that the official page does not explain; the example entry for assault shows importance 130 and the violent flag set [K4, shown as an example of the table format].
- **Spreading.** Reputation moves from a person to a faction after 10,800 s of world time (3 hours, derived) plus a random bias of up to 1,800 s, and to nearby factions up to 400 m away at a quarter strength [K1]. When opinions are combined, a person's counts 5, a faction's 3 and a larger group's 1 [K1]. A developer: if you commit a crime across town, the guards there do not know until time has passed; skip 24 hours and the same guard says "aren't you that guy" [K14, Tobias Stolz-Zwilling, 18 December 2024].
- **Unrest.** If a crime goes unsolved, the area gets more watchful and people carry and ready weapons [K14]. A wiki's words: people "become more vigilant, arm themselves", and guards call reinforcements [K18]. Officially, NPCs arm everywhere once anger passes 0.67 [K1].
- **During a fight.** Patch 1.2: NPCs watching a violent event "will now flee if the source of the violence moves too close"; NPCs reacting to violence got "boosted hearing"; the anger of a place from thefts and violence was rebalanced; NPCs seeing through obstacles or behind themselves was fixed [K9]. Distances: the "investigating" icon shows for NPCs up to 100 m away, the "active combat" icon inside 10 m [K1].
- **Punishment ladder.** Fine, talk your way out, run, or accept: pillory, caning, branding, execution (press) [K26]. Warhorse's interview says a hanging is game over [K14]. The audit already notes that accepting punishment wipes your record in that place, which LEDGER must not copy.
- **Developers' own tips.** NPCs can see through an open door and remember it was shut; a stranger in a house is remembered when something goes missing [K8].
- **Behaviour icon.** A hare icon runs from white (suspicion) through yellow (being recognised, with ears that rise) and orange (confronted, or an alarm raised) to red (hostile) [K30 press].

### 2.8 Camera and targeting

- First person [K17, K39].
- Lock-on to one foe with a key; cycle between foes; the camera is locked in combat and a held block frees it [K22 wiki for the first game, K35 player]. A fix made camera clipping with a shield and free-look limits [K9, K12].
- The attack zone is picked by the mouse; zones greyed out cannot be struck [K22 wiki].
- Hardcore Mode hides health and stamina bars and shows "far less visible" combat indicators [K20 wiki, K17]. Patch 1.4 added a setting that shows UI only when relevant [K11].

### 2.9 Where KCD2 touches the content rule

Taverns, drinking, dice games and betting on fist fights exist in KCD2 and its guides [K29, K14]. Nothing about them is used here. Children: not touched.

## 3. Mafia: The Old Country (Mafia TOC)

### 3.1 What it is

Third person, linear, set in Sicily in the early 1900s, Unreal Engine 5, released 8 August 2025 [M10]. Official: "not an open-world game" [M2]. Hangar 13's own framing: "This isn't an era of advanced weaponry or easy brawls" [M2]. Combat has cover shooting, stealth, a knife used for takedowns, and one-on-one knife duels [M22, M10]. Official: even a payment collection "can lead to a standoff at gunpoint or a brutal knife duel", and the tools depend on the task [M9]. Metacritic 73 on all three platforms [M10]. KIT.md found no Hangar 13 talk; one exists (the PAX East 2025 panel), but it is a video that could not be read, so Popverse's report of it is used [M7].

### 3.2 Knife duels

- **What a duel is.** Hangar 13's president Nick Baynes at PAX East 2025: the knife is "more than just a one-shot kill"; a new knife-dueling mode puts you against "a boss character" in a "one-on-one duel to the death" [M7, press report of the panel]. The game director calls them lethal encounters that "unfold at pivotal moments in the story" [M5, official, 8 May 2025].
- **Inputs.** Five actions only: slash, thrust, strike, dodge, parry. No other action is possible during a duel [M22 press]. On PC: strike right mouse, thrust middle mouse, slash left mouse, parry left shift, dodge space, steer with WASD [M12 press].
- **Rhythm.** Official: "the timing windows for different inputs (dodge, parry, etc.) are unique", button-mashing "won't get Enzo very far", listen for audio cues and "watch for red glints indicating unparryable attacks that must be dodged" [M1]. Guides: a normal attack is parried; a heavy strike with a red glint cannot be, so you dodge and counter; your own strike breaks a guard, then you follow with slashes or thrusts [M13, M14]. Parry is called generous [M13]. A foe is open for a short time after its own dodge; slashes have a wider hit area than thrusts [M12]. Each opponent has its own timing for strong attacks [M12].
- **Shape of a boss duel.** Guides describe two phases: rapid slashes first, then unparryable strikes from about half health, and quick-time prompts at about 50 percent and 0 percent health; a late prompt lets the boss regain 25 percent [M14]. These are guide claims. A German press piece describes the duels as a matter of quick reflexes, dodging or striking at the right moment [M26].
- **Tutorial.** A sparring duel with a blunt blade; three parries are needed to advance [M14, M21].
- **Knives.** Three types: one throwable, one that allows one-hit kills in active combat, one with the best durability [M1]. Only one knife is carried; durability is spent by lockpicking, quick stealth kills, throws and one-hit kills; whetstones restore it; the plain melee attack always works and is "not as quick or stealthy as a silent takedown, but it's lethal nonetheless" [M3]. In duels the knife type does not change damage [M12].
- **Frames or seconds.** Not published. A search summary of a guide says "about a second" to parry; that page was not reached (403) and nothing from it is used.

### 3.3 Brawls and fists

- Hand-to-hand fighting as a system: not published. Hangar 13 shows "freeform melee attacks you can employ in any combat encounter" [M6, official, 22 July 2025], with no inputs or timings. One critic says "You won't be using your fists in the Sicilian underworld" [M18, press]. Hangar 13's own words are that this "isn't an era of ... easy brawls" [M2].
- A knife melee attack exists outside duels and is always available [M3].

### 3.4 Takedowns and stealth

- **Bare hands.** Approach crouched, in the target's blind spot, hold the grab and press the prompted button repeatedly to choke him out. "Of course, this takes time, and if another enemy appears nearby, he will spot you" [M15 press].
- **Knife.** A quick lethal stab from behind, faster than choking, at the cost of knife durability [M15, M3]. A throwing knife kills from range and has to be collected [M1].
- **Distraction.** Throw a coin or a bottle; every enemy close enough investigates; the nearest one comes, not necessarily the one you meant [M15, M16 press].
- **Bodies.** Official tip: stash bodies, "which will prevent guards from being alerted by the sight of a corpse" [M1]. Drag a body out of a patrol route or into a crate [M15, M17].
- **Detection.** Enemies "can spot you from a long distance" and move to where they saw you even if not fully alerted [M15]. Some sequences require staying undetected; most do not [M3].
- **Instinct.** A mode that shows enemies through walls [M1, M6].
- **Timings of takedowns:** not published.

### 3.5 What bystanders do

Not published. No page read describes civilians, witnesses or police reacting to a fight in the main story. The game is linear and its stealth is about guards. The 2K Free Ride update lists timed combat challenges against waves and assassinations, with no civilians mentioned [M25].

### 3.6 How it holds up over a whole game

GameScreed: the fights "don't change much throughout the game and get boring very quickly" [M19]. CrimeNet Gazette: another blade "starts feeling contractual" [M18]. Impulse Gamer calls the duels cinematic and a highlight that "didn't overstay their welcome" [M20]. GameIndustry: duels are story-based and not skippable, "one of the most challenging parts" [M21]. PC Gamer scored it 45 out of 100, Game Informer 6 of 10 (the Wikipedia table) [M10].

### 3.7 Accessibility

Official: "Simplified Struggle (automatically completes rapid-button-press inputs)", three difficulty levels, adjustable HUD scale, aim assist options [M3].

### 3.8 Where Mafia touches the content rule

Hangar 13's blog mentions the family's wine in a villa video [M6]. It is not used. No children, gambling or drink feature in the fighting pages read.

## 4. The comparison with game-design/combat-spec.md

The verdict says what LEDGER should do with the games' practice for that point, not whether the spec is right. ADOPT: take it as it is. ADAPT: take the idea, change the form. IGNORE: leave it. "Not published" means no page read says. The reason quotes the spec or Jafar's answers.

| # | Spec point | KCD2 | Mafia TOC | Verdict | Reason |
|---|---|---|---|---|---|
| 1 | Filter: "Violence is seen" | Witnesses report or confront; reputation spreads at a stated delay; violence makes a region more watchful; watchers flee if it comes close [K14, K1, K9] | Not published for fights; a second enemy who comes near spots a choke, and a visible corpse alerts guards [M15, M1] | ADOPT | Spec section 1 makes witnesses the cost; KCD2 builds consequence from witnesses and LEDGER's seven slots go finer |
| 2 | Not a win condition: killing a witness works, the second problem is larger | Killing the would-be reporter stops the alarm [K30], but a corpse near you still gets you accused [K25] and fades after 300 or 3,600 s [K1] | Not published | ADAPT | Keep "works, evidence remains"; drop the corpse timer, since spec 7b says nothing "touches a corpse" |
| 3 | Not empowering: Tom is "not a fighter" | Weak at the start [K27], outnumbered is deadly [K33], but skills grow and one player says "unstoppable by halfway" [K33] | Enzo is a "coiled spring" who scrapes for weapons [M7]; scarce ammunition [M8] | ADAPT | Keep "not a superhero"; drop growth, since D11 forbids stats and spec says "if the player feels good at fighting, the fiction ... break" |
| 4 | Not frequent: "a handful of fights" | Fights, tourneys and bandit events recur; no count published | Duels come at the end of each chapter [M19]; critics call them repetitive [M19, M18], one disagrees [M20] | IGNORE | Spec target is a handful per playthrough; both games run far more and Mafia's critics are the warning |
| 5 | Not free: witnesses, lasting injury, treatment, feud | Health does not heal itself, bleeding loses 1 HP per 6 s, crimes bring fines or branding, gear wears [K18, K1, K26] | Health regenerates; knife durability; no social cost published [M25, M3] | ADOPT | Spec: "Every swing has a cost even when you win"; KCD2 charges body, gear and standing |
| 6 | Not a separate mode: no arena, no lock-on state, no sting | Lock-on rose, crossed-swords icon, music and UI hint at combat (a fix mentions them) [K18, K10] | A separate one-on-one mode with five actions [M7, M22] | IGNORE | Spec: "No arena, no lock-on state you enter and exit, no music sting" |
| 7 | Verb: Square up (a stance everyone sees) | No stance verb; drawing a weapon makes NPCs confront; above anger 0.67 NPCs arm everywhere [K1, K9] | Enzo "boldly draws his knife to challenge foes" [M6]; duel start is scripted [M5] | ADAPT | Spec: "Witnesses start paying attention BEFORE anything lands"; both show a visible commitment, ours is a stance with fists |
| 8 | Verb: Strike (slow, telegraphed, heavy; a miss hurts you more) | Four-direction swing, chain, cost 26, spam delay, charge up to 1.4 s [K1, K18, K9] | Slash, thrust, red-glint heavy strike, audio cues [M1, M13] | ADAPT | Spec wants a small verb set where "the player mashes" nothing; take one-cost swing and sight-and-sound tell, drop directions and combos |
| 9 | Verb: Shove (distance, non-injuring, de-escalation) | Clinch can push a man out of a pen; "locks, grips and throws" [K9, K5]; kick in the first game [K22] | Not published | ADAPT | Spec: "Cheap, non-injuring"; KCD2's clinch is a weapon lock, ours is a two-hand push that makes space |
| 10 | Verb: Guard (absorb; cannot guard forever) | Block drains stamina with the blow, regain x0.6; perfect block free; armour turns hits into stamina loss [K18, K1, K28] | Parry and dodge; no held guard published; foes guard and can be guard-broken [M13] | ADAPT | Spec: "Absorb rather than avoid"; take stamina drain and slower regain, drop the perfect-block prize |
| 11 | Verb: Back off ("the game should say so") | Developers' tip: "consider a tactical retreat" [K8]; fleeing draws a chase [K26] | No retreat inside a duel [M22] | ADOPT | Spec: "explicitly viable"; Warhorse's own tips say the same |
| 12 | Finishing a downed man, as a decision afterwards | A separate mercy kill on a weak foe [K18, K9]; knock-out is the alternative | Quick-time kills inside the duel; one-hit knife kills mid-fight [M14, M3] | ADAPT | Spec: "never ... in the flow of a scuffle"; KCD2's separate act fits, Mafia's in-flow kills do not |
| 13 | Guns out of scope | Crossbows and early firearms are slow, and a firearm can explode in the hand [K5, K8] | Guns central; "every bullet counts" [M5] | IGNORE | Spec: "Guns are out of scope"; RULINGS: firearms rare; KCD2's fragile rare gun is the model if they return |
| 14 | No health bar, damage numbers or hit markers | Bars shown; Hardcore hides them and cuts cues; UI only when relevant [K20, K17, K11] | HUD scale option; combat bars not described [M3] | ADAPT | Spec: "No health bar"; Hardcore shows it can ship, ours is the default and keeps the data (spec 7c) |
| 15 | Your condition on your body | Low stamina weakens blows; controller feedback for low stamina [K18, K11] | Not published | ADAPT | Spec: "breathing that gets ragged, a guard that drops"; KCD2 uses haptics, ours uses the body |
| 16 | Their condition on theirs | NPCs bandage, flee or fight by state; low-health behaviour from 40 percent [K9, K1] | Not published; bosses regain health after a missed prompt [M14] | ADOPT | Spec: "how they hold the injured side"; KCD2 shows hurt people acting hurt |
| 17 | Threat read from the world (three seconds of staring) | Hare icon: suspicion, detection, warning, threat [K30] | Instinct shows enemies through walls [M1] | ADAPT | Spec: "Somebody who is about to swing has been staring"; both use a HUD aid, ours must be gaze and stance |
| 18 | Contextual prompt: fading, forgiving, buffered | Green shield and riposte icon; UI only when relevant [K28, K11] | In-game tutorials and mid-fight feedback [M1] | ADAPT | Spec: prompt "appears the way the talk prompt does"; keep learn-by-doing |
| 19 | Telegraph, not tell | Weapon position shows direction, the shield tells the moment [K27, K28] | Red glint and sound; unique window per input [M1] | ADAPT | Spec: "Every incoming strike has a readable wind-up"; take glint and sound, drop icons |
| 20 | Sound carries most of it | Patches fix missing attack, hit, battle-cry and clinch sounds [K9] | "Listen for critical audio cues" [M1] | ADOPT | Spec: "Sound carries most of it" |
| 21 | The audience: cost shown in Mickey's book or a line | Arrest dialogue lists your crimes; a reputation tab per place [K9, K18] | Not published | ADAPT | Spec: "not a toast"; KCD2's list is a menu, ours is diegetic |
| 22 | Accessibility: longer telegraph, auto-resolve | Windows widen with skill [K22, K1]; fans built mods to widen them within days [K38] | "Simplified Struggle" completes rapid presses; three difficulties [M3] | ADAPT | Spec: "the same fight at a different tempo"; Mafia's auto-complete is the model, KCD2's skill growth is not (no stats) |
| 23 | Minimal HUD later as a toggle (7c) | Hardcore and "UI only when relevant" are options [K6, K11] | Adjustable HUD [M1, M3] | ADOPT | Spec 7c: "a settings toggle rather than a rewrite" |
| 24 | Resolve has no randomness | Mastery "rather than an unseen roll" [K5]; AI picks are chance weighted [K1]; stealth kills can fail [K9] | Not published | ADAPT | Spec: "a fight the player cannot read is a fight they cannot learn"; player outcomes fixed, AI variety seeded |
| 25 | Reach 1.6 m: no hit at range | Not published (only a from-behind angle of 135 degrees with x1.2) [K1] | Not published | IGNORE | Nothing to take; spec: "a hit at four metres is the fastest way to lose a player's trust" |
| 26 | Stamina must matter; mashing gasses out | Swing costs 26, regain 22 per second: 1.18 s per swing at rest (derived); a spam delay was added by patch [K1, K9] | Button-mashing "won't get Enzo very far" [M1] | ADAPT | Spec lab: mashing won 76 percent until retuned; KCD2 needed a patch for the same flaw; ours regains far slower (0.34 cost, 0.09 per second, 3.8 s per swing, derived) |
| 27 | A fight is three to four swings; winning costs | Armoured fights are long stamina contests, unarmoured men fall fast [K18] | Two-phase duels; length not published [M14] | ADAPT | Spec: "Even the best line wins a quarter of the time"; LEDGER's men in coats match KCD2's unarmoured case |
| 28 | Witness rules: from how far, through what; alley at night vs noon | Night lowers visibility (a penalty of 0.7 outdoors); hearing boosted for violence; seeing through walls fixed; investigators shown to 100 m [K1, K9] | Enemies spot from far and investigate; bodies stashed [M15, M1] | ADAPT | Spec phase 2: "Fighting in an alley at night is genuinely different"; LEDGER's Observation is finer |
| 29 | A killing brings police (a new pressure track) | Ladder from fine to execution; unrest makes guards call in help; area more watchful even without proof [K26, K18, K14] | Not published | ADOPT | Spec 7b: "It brings police"; the audit's E5 asked for the town to change its behaviour |
| 30 | Who swings first: both | NPC anger from violence and from being robbed exists; the player can strike anyone [K2, K4] | Scripted | ADOPT | Jafar: "violence is part of our crime world and a legit tool" |
| 31 | Lethality: yes, rarely and permanently | Fists knock out (our reading); killing innocents is a crime; hanging ends the game [K1, K26, K14] | Duels are to the death, scripted [M7] | ADAPT | Jafar: "Yes, rarely and permanently"; fists as knock-out fits "finishing" being a separate act |
| 32 | A body is a fact that cannot be discredited | Corpse hidden after 300 or 3,600 s; crime memory expires [K1, K4] | A seen corpse alerts guards until hidden [M1] | IGNORE | Spec 7b: no discredit or decay "touch a corpse"; both games let evidence fade or be hidden |
| 33 | A killing solves the immediate problem completely | Kill the reporter and no alarm [K30] | Hide the body and nobody is alerted [M1] | ADOPT | Spec 7b: be "honest about this or the choice is fake" |
| 34 | Who else saw | A witness reports at once; civilians too [K26] | A nearby second enemy spots you [M15] | ADOPT | Spec 7b: killing one witness of three "is the mechanism by which this spirals" |
| 35 | The crew know; nobody who saw is the same | Per-person reputation weighs 5, faction 3, group 1 [K1]; one quest note stops friendly NPCs reporting [K11] | Not published | ADAPT | Spec 7b: "Nobody who saw it is ever quite the same about you"; LEDGER already holds loyalty |
| 36 | Rare and permanent; a playthrough without killing | The player can knock out instead of killing [K18] | Duels to the death cannot be skipped [M21] | ADAPT | Spec 7b: "possible to complete a whole playthrough having never done it"; Mafia's forced duels are the opposite |
| 37 | Camera rig and momentum: weight and readability | First person, lock-on, free look while blocking, hit reaction slows the player [K17, K35, K9] | Third person; hit-pause not published [M10] | ADAPT | Spec 5: "Weight and readability"; take the hit-reaction slow-down, keep our third-person camera with no lock-on |
| 38 | An enemy AI that can telegraph and react | 2 s mean gap, longer per attacker; practice foes start in defence [K1, K11] | Boss phases; own strong-attack timing per boss [M14, M12] | ADOPT | Spec 5: "an enemy AI that can telegraph and react"; both give concrete rhythms |
| 39 | Injuries persist and heal on a schedule | Bleeding 1 HP per 6 s; injury fades 1 percent per 20 s; health does not heal itself [K1, K18] | Health regenerates; Classic difficulty makes it sparse [M25] | ADAPT | Spec 0: "Injuries persist and heal on a schedule"; KCD2's run in game seconds, ours in days |
| 40 | The stagger model (Bumps) | A hit reaction slows the player; a too-long knock-back was fixed as a bug [K9] | A parry staggers the foe [M14] | ADAPT | Spec 5: "Bumps: contact classification and stagger"; cap distances as Bumps does (0.55 m) |
| 41 | Footing: Down, cannot act, can be finished | Knocked-out men stay unconscious while a depth value fades; unconscious men no longer idle [K1, K12] | Not published | ADAPT | Spec: "On the ground. Cannot act; can be finished"; KCD2's timed unconsciousness gives the way back up |
| 42 | The risk: combat ruins the game; stop if it distracts | Combat is a loud complaint among players [K33]; a critic finds it "overly reliant on parry & riposte" [K23]; Warhorse made it "more accessible" [K16, K15] | Critics: repetitive, "contractual" [M19, M18]; PC Gamer 45 of 100 [M10] | ADOPT | Spec 8: "the correct decision is to stop there and leave violence as something that happens TO you" |

Notes on the table:
- The rows cover every verb (six, with finishing), every "must not be" (five), the interface rules, the plan points from sections 5 and 6, Jafar's answers, the body rules of 7b and the risk of section 8.
- Not copied, because RULINGS or canon rule them out: KCD2's stats, perks, skills that rise with use, jump, horses, hunger, alcohol, dice and betting; Mafia's driving, cover shooting and quick-time bouts. RULINGS "What the game is" lists no jump, fists and improvised weapons, firearms rare, no health bar, no stats.
- Ideas from the games that are not in the spec and could be raised later: a hit from behind that counts more (KCD2 official, x1.2 from 135 degrees); hiding a body to delay its finding (Mafia's stash points); NPCs that flee a fight when it moves close to them (KCD2 patch 1.2).

## 5. DRAFT TARGET LIST for combat-spec phase 3

**Status: DRAFT.** Phase 3 in the spec is "Bodies and telegraphs. Animation, the read, hit reactions, the guard", blocked on characters. This list is what a first test needs. It names targets and timings, not clips. Where the clips come from (MetaHuman movement clips and Mixamo, per RULINGS 3 October, or our own capture) is not decided here. All names are our own and carry no drink, gambling or child words, so they pass the clip-name walk of tools/content-gate.py.

### 5.1 How the numbers were made

- One frame is 1/30 s. Each timing is marked: game (from a published game number), standard (a public convention), judgement (ours), derived (arithmetic).
- Standard: fighting-game frame data splits a move into startup (to the first hitting frame), active frames and recovery [S1]. The same page says fighting games run at 60 fps, so one of their frames is 1/60 s; our frames are 1/30 s.
- Standard: simple human reaction to a visual signal is about 190 ms for college-age people, and "on the order of 200 ms" generally [S2]. Choosing between three answers (guard, shove, back off) and pressing a key takes longer; that part is judgement.
- Game: KCD2's official numbers give a mean 2 s between a careful AI fighter's attacks and 0.2 s before a held attack starts to charge [K1]. They give no wind-up length for a plain swing. No Mafia number exists.
- The repository's own constants: reach 1.6 m and shove reach 1.9 m (Combat.cs); a stumble is at most 0.55 m (Bumps.Stagger in Interaction.cs); VerbBeat's default wind-up is 0.18 s (Interaction.cs). That default is below the 0.19 s reaction time in [S2], so a strike left at it could not be read.
- The wind-up, derived with judgement: 0.19 s to see (standard) + 0.45 s to choose and press (judgement) = 0.64 s, rounded to 20 frames (0.667 s). Range 0.50 to 0.80 s.
- Telegraph setting (spec section 4, "a longer telegraph window"): the wind-up is lengthened by 1.5 and nothing else changes. 20 frames become 30 and every later key frame moves by 10.

### 5.2 The list at a glance

| Id | Name | Length | Frames at 30 fps | Key frames | Timing source |
|---|---|---|---|---|---|
| A01 | square-up enter | 0.70 s | 21 | stance visible f6 | judgement |
| A02 | square-up hold (loop) | 2.0 s | 60 | loop seam f60 | judgement; spec says a swinger stares for 3 s |
| A03 | stand-down step | 0.90 s | 27 | hands down f6, step f14 | judgement |
| B01 | strike, lands | 1.33 s | 40 | wind-up end f20, contact f22, recovery starts f28 | judgement on a standard |
| B02 | strike, misses | 1.93 s | 58 | wind-up end f20, would-be contact f22, recovery starts f32 | judgement |
| C01 | shove | 0.80 s | 24 | wind-up end f8, contact f10, recovery starts f14 | judgement |
| D01 | shoved, steady | 0.83 s | 25 | 1.2 m reached f15 | derived from repository constants |
| D02 | shoved while reeling, falls | 1.00 s | 30 | ground f14 | judgement |
| D03 | struck, steady | 0.60 s | 18 | head snap ends f4, step ends f10 | judgement |
| D04 | struck, reeling | 1.00 s | 30 | 0.55 m reached f15 | derived from repository constants |
| D05 | reeling (loop) | 1.5 s | 45 | loop seam f45 | judgement |
| D06 | struck, knocked down | 1.50 s | 45 | ground f16 | judgement |
| D07 | down (loop) | 3.0 s | 90 | loop seam f90 | judgement |
| D08 | getting up | 3.0 s | 90 | hands and knees f30, kneeling f60 | judgement |
| E01 | guard raise | 0.17 s | 5 | guard live f3 | judgement |
| E02 | guard hold (loop) | 1.5 s | 45 | loop seam f45 | judgement |
| E03 | guard takes a blow | 0.50 s | 15 | impact f2 | judgement |

Seventeen entries. Both men use the same clips; only the camera differs for Tom Nowak.

### 5.3 The entries

Each entry: start pose, end pose, length and key frames with their source mark, blends, what it causes, sound, camera, what witnesses register and when. Sounds are our own recordings or CC0 (RULINGS D26), never from a game. "Seen" and "heard" use the repository's perception rules: seven slots (precursor, draw, act, victim, actor, flight, aftermath, from weapons-spec section 4.1) and the shout-range sound carry (Violence.SeenFrom is Acoustics.ShoutCarry).

**A01 square-up enter.** Start: standing or walking idle. End: feet a shoulder apart with the lead foot toward the other man, knees soft, hands up at chest height, chin tucked, weight forward. 21 frames (0.70 s), range 0.5 to 1.0 s, judgement. Stance visible at f6 (0.20 s), when the shoulders turn and the hands rise. Blends from walk or idle over 5 frames; to A02. Causes: nothing; it is not an attack. Sound: foot scuff at f4, cloth at f6, breath in at f8. Camera: none; no mode change (spec section 2). Witnesses: the precursor slot fills at f6 for anyone with sight of the stance; "witnesses start paying attention before anything lands" (spec section 3).

**A02 square-up hold (loop).** Start and end: the A01 end pose with a slow weight shift and chest breathing, rate tied to the body's breath rate (Rig.BreathRate, 0.25 to 0.85 a second). 60 frames (2.0 s) loop, judgement. Blends from A01, E02, D05; to B01, C01, E01, A03. Sound: breath. Camera: none. Witnesses: the precursor continues. An NPC swings only after at least 3 s of holding it (spec section 4: "has been staring for three seconds").

**A03 stand-down step.** Start: A02 pose. End: hands low, one step back, shoulders turned away. 27 frames (0.90 s), judgement. Hands down at f6 (0.20 s), step planted at f14. Displacement 0.8 m. Blends from A02 or E02 over 3 frames; to walk over 5 frames. Sound: step, breath out. Camera: none. Witnesses: at f6 the precursor ends ("he stood down"); this is the best option "and the game should say so" (spec section 3). No act is recorded.

**B01 strike, lands.** Start: A02 pose. Wind-up: weight to the back foot, right fist cocked behind the ear, torso twisted away, breath in. Contact: a heavy overhand at head height. End: follow-through, then a half-step and guard up. 40 frames (1.33 s). Wind-up end f20 (0.667 s), range 0.50 to 0.80 s (judgement on a standard, section 5.1). Contact f22 (0.733 s), with 3 active frames (f22 to f24, judgement; "first hitting frame" convention from [S1]). Recovery starts f28; free to act at f40, which is 0.60 s after contact (judgement). A strike by the same man is not started again for 2.0 s on average, spread plus or minus 0.5 s (game: KCD2 official mean gap; the spread is judgement). Blends from A02 over 4 frames; to A02 over 5 frames. Causes: a hit reaction by the target's footing: steady, D03 (0.25 m stagger, 0.33 s); reeling, D04 (0.55 m, 0.5 s); would be floored, D06 (falls, ground at 0.53 s, ends 0.6 m from where he stood). Through a guard, E03. Sound: breath in at f3, cloth swish f18 to f22, thud at f22, grunt at f24. Camera: hit-pause of 2 frames (0.067 s) on both men at f22 (judgement; Dustloop confirms hit-stop exists as a concept, its length differs by game [S1]); for Tom's camera a 1.5 degree nudge toward the blow settling over 0.4 s (judgement; spec: "a camera that drifts and settles harder"). Witnesses: at f22 the act and victim slots fill for anyone in sight; the thud carries to shout range; the actor slot fills only if the identification ladder allows. Aftermath fills when the target is down (D06, D07). The act is recorded in the harm book.

**B02 strike, misses.** As B01 to f22; the fist meets nothing. Then overbalance: torso swings past, one stumbling step forward 0.4 m by f32, then recovery. 58 frames (1.93 s); recovery starts f32; free to act at f58, which is 1.2 s after the would-be contact, twice B01's 0.6 s (judgement; spec: "misses hurt you more than them"). Blends and sound as B01 without the thud; a breath out of effort at f26. Causes: none; the target's reaction is a flinch or a step back of its own. Camera: no hit-pause; Tom's camera lurches forward slightly (judgement). Witnesses: the act slot fills at f22 with no victim: "he swung at him".

**C01 shove.** Start: A02 pose or standing, facing. Wind-up: both hands drawn to the chest. Contact: palms drive into the target's chest, rear foot pushing, lean 10 to 15 degrees. End: arms out then lowered, balance regained. 24 frames (0.80 s). Wind-up end f8 (0.267 s), range 0.20 to 0.35 s; contact f10 (0.333 s); recovery starts f14; free at f24 (judgement). Faster than the strike on purpose: 0.267 s is barely above the 0.19 s simple reaction time (standard), so a shove can be seen but hardly answered. It is cheap, and it is not a duel move. Blends from A02 over 3 frames; to A02 over 4 frames. Causes: D01 if the target is steady, D02 if he is reeling (as Combat.cs floors a reeling man on a shove). No injury. Sound: palms on coat at f10, breath out. Camera: no hit-pause; a 1 degree push (judgement). Witnesses: at f10 the shove registers as a Bumps shove, which holds the watchers' attention for 4.0 s (Bumps.AttentionSeconds). Act slot only, a quiet act. A shove does not make a victim record in the harm book.

**D01 shoved, steady.** Start: any stance. End: back in A02 pose, hands up. 25 frames (0.83 s). Two quick backward steps; displacement 1.2 m reached at f15 (0.5 s), then 10 frames to find balance. Derived: the men stand about 0.8 m apart at contact (judgement), so 0.8 + 1.2 = 2.0 m, past shove reach (1.9 m) and past strike reach (1.6 m), which is the spec's "create distance". It is more than twice the 0.55 m stumble cap on purpose, because a shove is meant to move a man. Causes: nothing further. Sound: two shoe scrapes (f4, f9), breath. Camera: none. Witnesses: the victim's stagger is the visible part of the act slot.

**D02 shoved while reeling, falls.** Start: D05 pose. End: on his back or seat. 30 frames (1.0 s). Pushed 1.4 m, feet go at f6, ground contact at f14 (0.47 s), then settles into D07. Judgement. Causes: footing becomes Down (Combat.cs). Sound: scrape, a dull body fall on the pavement at f14, breath knocked out at f15. Camera: a 2 degree drop and settle (judgement). Witnesses: aftermath begins at f14: "a man is down". Watchers may investigate or raise the alarm (weapons-spec section 8).

**D03 struck, steady.** Start: any stance. End: back in stance, a little lower. 18 frames (0.60 s). Head snaps for 4 frames, half-step of 0.25 m by f10, hand to the face, stance regained at f18. Judgement; stays under the 0.55 m stumble cap. Causes: footing stays steady. Sound: grunt, shoe scuff. Camera: none beyond B01's. Witnesses: nothing new.

**D04 struck, reeling.** Start: D03 or stance. End: hunched, hand to the face, guard low (D05's pose). 30 frames (1.0 s). Two half-steps and a lurch, 0.55 m reached at f15 (0.5 s). Derived: equal to the Bumps stagger cap. Causes: footing reeling; guard drops (spec: "Guard is dropping"). Sound: a heavy grunt, a wet breath, shoes. Camera: none. Witnesses: the injured side shows (HarmBook.LooksLike has never been displayed).

**D05 reeling (loop).** Pose: swaying, one hand to the face, ragged breath, chin up. 45 frames (1.5 s) loop, judgement. Blends from D04; to D02, D06, E02. Footing reeling. Sound: breath at the ragged rate. Camera: none. Witnesses: his state reads as hurt.

**D06 struck, knocked down.** Start: D04 or D05 pose. End: on the ground on his side, one hand on his head. 45 frames (1.5 s). Knees go in 8 frames, falls sideways, ground at f16 (0.53 s), 0.6 m from where he stood, then settles. Judgement. Causes: footing down. Sound: a gasp, a body fall at f16, a scrape of a hand on stone. Camera: on Tom's camera a 2 degree settle (judgement). Witnesses: aftermath begins at f16; the victim and a body on the ground are the strongest cue the mill can read.

**D07 down (loop).** Pose: on his side, knees drawn, hand to the head, breathing. 90 frames (3.0 s) loop, judgement. Footing down: cannot act; can be finished (spec). The finishing verb is not in this first test. Sound: breath. Camera: none. Witnesses: aftermath persists.

**D08 getting up.** Start: D07 pose. End: standing, hand on knee, reeling pose. 90 frames (3.0 s): hands and knees by f30, kneeling by f60, standing by f90. Judgement. Needed only if the test lets a downed man rise; the spec does not say. Sound: breath, a shoe on stone. Camera: none. Witnesses: a man standing up again is not a new event.

**E01 guard raise.** Start: A02 pose. End: forearms up over face and ribs, chin down. 5 frames (0.17 s), guard live at f3 (0.10 s). Judgement: the guard must be live well inside the wind-up. Blends from A02 over 2 frames; to E02. Causes: nothing. Sound: cloth. Camera: none. Witnesses: a defensive posture, no slot.

**E02 guard hold (loop).** Pose: arms up, shoulders hunched, forearms sinking slowly as stamina falls: up to 15 cm lower as stamina goes from 1.0 to 0.3 (judgement; spec: "a guard that drops as you tire"). 45 frames (1.5 s) loop. A held guard becomes a grab in the full spec; not in this test. Sound: breath. Camera: none. Witnesses: none.

**E03 guard takes a blow.** Start: E02 pose. End: E02 pose with the guard knocked slightly open. 15 frames (0.50 s). Impact at f2, slide back 0.2 m, then reset. Judgement. Causes: through a guard the blow does 0.22 of its force (Combat.cs), so the footing normally stays steady. Sound: a blow on forearms, grunt. Camera: a 0.5 degree nudge. Witnesses: the act slot fills as in B01.

### 5.4 The first test, and what it measures to pass

The scene: two men on the built Quay Street, packaged build, day and night. The second man squares up (A01), holds for 3 s or more (A02), then strikes Tom (B01). Tom guards (E01), backs off (A03) or shoves (C01). The second man swings up to three times. The three blows leave him steady, then reeling, then down (D03, D04, D06). A shove on him while reeling puts him down (D02). Nothing in the test kills anyone.

It passes when all of these hold. The thresholds are judgement unless marked.

1. **Timing.** Every key frame in 5.2 is within one frame (0.033 s) of the table in 10 of 10 runs, read from the clip's own markers and checked against a 30 fps recording.
2. **Readable.** A fresh reviewer (not the builder; CLAUDE.md's gate), shown the strike from the street camera at 3 m and at 8 m, says "he is about to hit" before the contact frame in at least 9 of 10 showings, and tells a shove from a punch in 10 of 10.
3. **Answerable.** A scripted player with a 0.45 s delay (our figure) gets the guard live by f20 with at least 3 frames to spare: 0.45 + 0.10 = 0.55 s against 0.667 s.
4. **Distances.** A shove ends with the two men more than 1.9 m apart in every run on level ground, with the shoved man moved 1.2 m, plus or minus 0.15 m. A strike moves a steady man 0.25 m, a reeling man no more than 0.55 m, a floored man ends within 0.15 m of 0.6 m from where he stood.
5. **Footing and clip agree.** With Combat.Resolve, three strikes give D03, D04, D06 in that order and no fourth is needed; a shove on a reeling man gives D02. No clip plays in the wrong footing.
6. **Joins.** No foot slide over 5 cm and no pop at any blend (NOW.md records a walk that slides at its joins, so this is a real risk).
7. **What witnesses register.** Replayed in the headless simulation with two onlookers, one 6 m away in view and one behind a wall: the first records a precursor within 0.23 s of A01 starting, and act and victim at f22; the second records sound only, at f22. Neither records anything before A01. The shove records only the 4.0 s shove attention.
8. **Tempo.** With the longer-telegraph setting on, the wind-up is 30 frames, every later key frame is 10 frames later, and the outcomes are identical.
9. **Rules of the game.** No health bar, damage number or hit marker is drawn (a screenshot check). All 17 clip names pass the content gate. Frame time stays inside PLAN.md's performance exit (median 16.7 ms) with the two men on screen.

Done means walked in the packaged build by the AI tester; it stays "ready for review" until Jafar passes it (CLAUDE.md).

### 5.5 What this list leaves out

- Finishing a downed man: a decision for the quiet afterwards, and the most sensitive scene under the content rule (violence stays, no cruelty as spectacle). Not in a first test.
- Guns, improvised weapons, knives and the grab that a held guard becomes.
- The onlookers' own animations (turn, step back, flee). The townspeople animation research covers them; this list only says when they should notice.
- Sources of the clips themselves.

## 6. Not reached, unverified, sources

### Not reached

- YouTube videos, which asked for a sign-in and were not worked around: Warhorse's official live-action combat video, the Hangar 13 PAX East panel ("Family Takes Sacrifice"), the "Breaking Omertà" developer insights video, and the "Family Code" videos. Only the official pages that describe them were read.
- The GDC 2025 talk video (the Vault page showed a login limit; only its abstract was read) and the GDC 2026 session page "Supporting Thousands of NPCs" (403).
- Fandom wikis for both games (403). The Unreal Engine developer interview on Mafia (403; the WebFetch tool could not resolve the host either).
- GameSpot reviews of both games, Stevivor, GamesHub, Checkpoint, Keengamer (403), Deltias and Sportskeeda (405), Nexus Mods (403). Nothing from them is used. Search summaries that quoted them were treated as leads only.
- The Epic Games interview with Martin Ziegler: not opened; known only through the Insider Gaming page [K16].
- Business Wire's launch release: the transfer failed.
- Steam community pages not in the list below were not opened.

### Unverified

1. Expert Game Reviews frame table for perfect block and master strike (no method; contradicts the official wiki on who teaches master strike) [K36].
2. LootLore's 0.4 s and 0.55 s windows, "30 percent" claim, Defense 8 unlock and "works unarmed" [K37].
3. A search summary of Keengamer saying "about a second" to parry in Mafia (page not reached).
4. Fextralife's maximum stamina of 136 [K21].
5. Player claims that master strikes are sword-only, and that NPCs use them in fist fights [K32].
6. Our reading of the perfect-block help text (window is a share of lead time, widens with the square root of skill).
7. Our reading of the attacker-gap rule and the rates built on it (derived rates in 2.3).
8. Whether retail values match the table exported on 14 January 2025.
9. Units not stated in the official table: MinPerfectBlockSlot01, the stealth slot and cooldown values (StealthKillMinSlot 0.05 and StealthKillMaxSlot 0.4, StealthCooldown 5). Not used in any total.
10. The Escapist's mapping of crimes to punishments (press; no official table read) [K26].
11. The official wiki's example crime entry values (assault, importance 130): shown as an example of the table format [K4].
12. Whether KCD2 has a kick or shove as a named verb; only the first game's codex and a clinch-push patch note were read [K22, K9].
13. That fists knock out and do not kill in KCD2 (our reading of one help text with value 0) [K1].
14. Any fist or brawl system in Mafia: not published; one critic says none [M18].
15. Any bystander, civilian or police reaction to a fight in Mafia: not published.
16. A player summary of KCD2 surrender prompts (E to talk): from a search summary of Steam threads, not read as a page, not used for any claim above.
17. Which weapons lack which direction in KCD2: guides conflict [K18, K34, K31].
18. The Steam post of 10 January 2025 that carries the phrase "authentic first person combat" was read through the Steam news feed [K39].

### Sources

All read 13 October 2026. "Full" means read to the end. "Sections" means the combat, crime, takedown, tutorial and feature sections were read and the rest searched by keyword.

**Our own repository (read first):** game-design/combat-spec.md (full), game-design/agency-model.md (full), game-design/weapons-spec.md (sections 4, 6, 8, 10), RULINGS.md (full), canon.md (full), CHARTER.md, PLAN.md, NOW.md, TOWN.md, CATALOGUE.md (homes table), production/research/aaa-reference/KIT.md, production/research/coverage-audit-kcd2/SUMMARY.md and DELIVERY.md (sections B, E, F), ledger/Assets/Scripts/Core/Combat.cs and Interaction.cs.

**Kingdom Come: Deliverance II**

- K1, official. Warhorse modding wiki, article KM-A-20 "RPG Constants/Params", values exported 14 January 2025, page updated 25 October 2025. Full. https://warhorse.youtrack.cloud/articles/KM-A-20 (the page is a script shell; the text was read through the wiki's public interface https://warhorse.youtrack.cloud/api/articles/KM-A-20?fields=idReadable,summary,content,updated)
- K2, official. Same wiki, KM-A-21 "Stats and skills", updated 15 January 2025. Full. https://warhorse.youtrack.cloud/articles/KM-A-21
- K3, official. Same wiki, KM-A-12 "Database tables", updated 28 January 2025. Full. https://warhorse.youtrack.cloud/articles/KM-A-12
- K4, official. Same wiki, KM-A-27 "Crime", updated 31 March 2025. Full. https://warhorse.youtrack.cloud/articles/KM-A-27
- K5, official. Warhorse Steam announcement "Weapons and combat mechanics", 18 October 2024. Full. https://steamcommunity.com/games/1771300/announcements/detail/4521142560073672483
- K6, official. Warhorse Steam announcement "Hardcore Mode is live NOW in Patch 1.2.4", 15 April 2025. Full. Steam news feed https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=1771300&count=300&maxlength=0&format=json (item 1796631172410040)
- K7, official. Deep Silver game page, Combat feature text. Full. https://www.deepsilver.com/games/kingdom-come-deliverance-ii
- K8, official. Deep Silver "Insider tips from the developers of Kingdom Come: Deliverance 2" (before the 4 February 2025 launch). Full. https://www.deepsilver.com/games/kingdom-come-deliverance-ii/news/insider-tips-from-the-developers-of-kingdom-come-deliverance-2
- K9, official. Patch 1.2 notes (Steam post of 13 March 2025 points to them). Sections plus keyword search of the quest lists. https://www.deepsilver.com/games/kingdom-come-deliverance-ii/news/patch-12
- K10, official. Patch 1.3 notes (Steam post 15 May 2025). Sections. https://www.deepsilver.com/games/kingdom-come-deliverance-ii/news/patch-13
- K11, official. Patch 1.4 notes (Steam post 9 September 2025). Sections. https://www.deepsilver.com/games/kingdom-come-deliverance-ii/news/patch-14
- K12, official. Patch 1.5 notes (page undated; hotfix 1.5.1 followed on 14 November 2025). Sections. https://www.deepsilver.com/games/kingdom-come-deliverance-ii/news/patch-15
- K13, official. GDC Vault page for "Combining GOAP and MBTs to Create NPCs' Behaviors for Kingdom Come: Deliverance II", Matej Marko, Warhorse, GDC 2025. Abstract only. https://www.gdcvault.com/play/1035576
- K14, interview. Tobias Stolz-Zwilling, Warhorse PR manager, with Stephen Farrelly, 3rd-Phase Boss, 18 December 2024. Full. https://3rd-phase-boss.com/blogs/gaming/kingdom-come-deliverance-2-developer-interview-hands-on
- K15, interview. Tobias Stolz-Zwilling, Tech4Gamers, 3 March 2025. Full. https://tech4gamers.com/kingdom-come-deliverance-2-interview-warhorse/
- K16, interview via press. Martin Ziegler quoted by Insider Gaming, 15 July 2024. Full. https://insider-gaming.com/warhorse-kingdom-come-deliverance-2-immersive/
- K17, wiki. Wikipedia, Kingdom Come: Deliverance II. Full. https://en.wikipedia.org/wiki/Kingdom%20Come:%20Deliverance%20II
- K18, wiki. Fextralife KCD2 wiki, "Combat", edited 24 August 2026. Full. https://kingdomcomedeliverance2.wiki.fextralife.com/Combat
- K19, wiki. Fextralife, "Feint". Full. https://kingdomcomedeliverance2.wiki.fextralife.com/Feint
- K20, wiki. Fextralife, "Hardcore Mode". Full. https://kingdomcomedeliverance2.wiki.fextralife.com/Hardcore+Mode
- K21, wiki. Fextralife, "Stamina". Full. https://kingdomcomedeliverance2.wiki.fextralife.com/Stamina
- K22, wiki. Kingdom Come: Deliverance Wiki on wiki.gg, "Combat" (codex entries of the first game). Full. https://kingdomcomedeliverance.wiki.gg/wiki/Combat
- K23, press. Shacknews review, 3 February 2025. Full. https://www.shacknews.com/article/142932/kingdom-come-deliverance-2-review-score
- K24, press. Gamerant, "Master Strike, Explained", 5 February 2025. Full. https://gamerant.com/kingdom-come-deliverance-2-kcd2-how-master-strikes-explained/
- K25, press. Gamerant, KCD2 crime and punishment preview, 16 August 2024. Full. https://gamerant.com/kingdom-come-deliverance-2-crime-punishment-reputation-system/
- K26, press. The Escapist, "How Crime and Punishment Work in KCD2", 21 February 2025. Full. https://www.escapistmagazine.com/how-crime-and-punishment-work-in-kingdom-come-deliverance-2/
- K27, press. PCGamesN combat and combos guide, updated 21 February 2025. Full. https://www.pcgamesn.com/kingdom-come-deliverance-2/combat-combos
- K28, press. Beebom, block, parry, dodge and riposte, 4 February 2025. Full. https://beebom.com/how-to-block-parry-dodge-riposte-in-kingdom-come-deliverance-2/
- K29, press. Gamer Guides, Unarmed leveling and perks, 4 February 2025. Sections. https://www.gamerguides.com/kingdom-come-deliverance-ii/guide/stats-and-skills/unarmed
- K30, press. Gamer Guides, "The Rabbit Icon", 5 February 2025. Full. https://www.gamerguides.com/kingdom-come-deliverance-ii/guide/getting-started/gameplay/the-rabbit-icon-stealth-and-detection
- K31, press. Seven Swords combat guide (page dated 10 October 2026). Full. https://sevenswords.uk/kingdom-come-deliverance-ii-combat-guide/
- K32, player. Steam discussion "Master strikes?", 6 February 2025. Full. https://steamcommunity.com/app/1771300/discussions/0/601895662819239243
- K33, player. Steam discussion "This combat system is utter trash", February 2025. First page of replies. https://steamcommunity.com/app/1771300/discussions/0/601895505111307429
- K34, player. Steam guide "Understanding how Combos work" by Kabirbd. Chapters 1 and 2. https://steamcommunity.com/sharedfiles/filedetails/?id=3442173547
- K35, player. Steam guide on fighting multiple enemies, by The Last Virgin. Full. https://steamcommunity.com/sharedfiles/filedetails/?id=3455238658
- K36, unverified. Expert Game Reviews, timing guide. Full. https://expertgamereviews.com/kingdom-come-deliverance-2-combat-timing-guide/
- K37, unverified. LootLore, master strike guide (dated 23 May 2026). Full. https://lootlore.online/en/kingdom-come-deliverance-2/mechanics/kcd2-master-strike-guide
- K38, press. Master of Warcraft, Easy Combat mod, 14 February 2025. Full. https://www.masterofwarcraft.net/2025/02/kingdom-come-2-easy-combat-mod-master.html
- K39, official. Warhorse Steam announcement "Catch-up on our Gameplay Showcase", 10 January 2025. Full. Steam news feed (item 1788311419052726), same link as K6.

**Mafia: The Old Country**

- M1, official. 2K, "Quick Tips". Full. https://mafia.2k.com/the-old-country/news/quick-tips/
- M2, official. 2K, "Community Q&A" (June 2025). Full. https://mafia.2k.com/the-old-country/news/community-q-and-a/
- M3, official. 2K, "Community Q&A #2" (early August 2025). Full. https://mafia.2k.com/the-old-country/news/community-q-and-a-2/
- M4, official. 2K newsroom, 8 May 2025. Full. https://newsroom.2k.com/news/mafia-the-old-country-launching-august-8-2025-debuts-official-gameplay-trailer-and-developer-insights-video
- M5, official. PlayStation Blog, Alex Cox, Hangar 13 game director, 8 May 2025. Full. https://blog.playstation.com/2025/05/08/mafia-the-old-country-uncovers-the-origins-of-organized-crime-on-august-8/
- M6, official. PlayStation Blog, Alex Cox, 22 July 2025. Full. https://blog.playstation.com/?p=407886
- M7, press report of a developer panel. Popverse, Nick Baynes at PAX East, 11 May 2025. Full. https://www.thepopverse.com/gaming-mafia-the-old-country-weapons-player-knife-duel-stealth-pax-east-2025
- M8, interview via press. GamingBolt, Joshua Zammit quoted, 8 May 2025. Full. https://gamingbolt.com/mafia-the-old-countrys-combat-has-a-life-or-death-vibe-encourages-more-tactical-play
- M9, official. 2K, "The Family Code" gameplay videos page. Full. https://mafia.2k.com/the-old-country/news/gameplay-deep-dive-videos-family-code/
- M10, wiki. Wikipedia, Mafia: The Old Country. Full. https://en.wikipedia.org/wiki/Mafia:%5FThe%5FOld%5FCountry
- M12, press. Game8, "Knife Fight Guide". Full. https://game8.co/games/Mafia-The-Old-Country/archives/542506
- M13, press. GamerBlurb, knife fight guide, 9 August 2025. Full. https://gamerblurb.com/articles/mafia-the-old-country-knife-fight-dueling-guide
- M14, press. DTGRE, Palio chapter knife guide, 7 August 2025, and its L'Ombra boss guide. Full. https://www.dtgre.com/2025/08/mafia-old-country-palio-knife-combat-guide.html and https://www.dtgre.com/2025/08/boss-fight-guide-defeating-lombra-mafia-the-old-country-palio.html
- M15, press. VGTimes, stealth guide, 13 August 2025. Full. https://vgtimes.com/guides/131564-mafia-the-old-country-stealth-guide-tips-for-silent-gameplay-and-sneaky-completion.html
- M16, press. Gameranx, ten quick tips, 8 August 2025. Full. https://gameranx.com/features/id/547457/article/mafia-the-old-country-10-quick-tips-to-become-a-made-man/
- M17, press. Game8, stealth guide. Sections. https://game8.co/games/Mafia-The-Old-Country/archives/542458
- M18, press. CrimeNet Gazette review. Full. https://www.crimenetgazette.com/post/mafia-the-old-country-review-join-the-mafia-regret-the-knife-budget
- M19, press. GameScreed review, 8 August 2025. Full. https://www.gamescreed.com/reviews/mafia-the-old-country-review
- M20, press. Impulse Gamer review, 7 August 2025. Full. https://www.impulsegamer.com/mafia-the-old-country-review-pc/
- M21, press. GameIndustry review, 22 September 2025. Full. https://www.gameindustry.com/reviews/game-review/mafia-the-old-country-is-a-crime-saga-told-with-cinematic-splendor/
- M22, press. MobileSyrup review, 18 August 2025. Full. https://mobilesyrup.com/2025/08/18/mafia-the-old-country-breathes-new-life-into-the-classic-franchise/
- M25, official. 2K, "Free Ride update". Sections. https://mafia.2k.com/the-old-country/news/free-ride-update/
- M26, press (German). PC Games, new combat video, 31 July 2025. Full. https://www.pcgames.de/Mafia-The-Old-Country-Spiel-74877/News/Neues-Video-zum-Kampfsystem-1478658/

**Standards**

- S1, standard. Dustloop, "Using Frame Data". Full. https://dustloop.com/w/Using%5FFrame%5FData
- S2, standard. Wikipedia, "Reaction time" (mental chronometry). Sections on simple reaction time. https://en.wikipedia.org/wiki/Reaction%5Ftime

Opened and not used: 2K's developer diaries 1 and 3 for Mafia (knife research, motion capture stages), Wccftech's Mafia interview piece, Gamerant's second KCD2 crime article, PatchCrazy's crime guide, Gamer Guides' other pages, a Steam guide "How To Win Fights", and a Steam "How Not to Die" guide (a joke guide).
