# Mechanics mapped to the parts list

Built from the four raw lists GTA-V, KCD2, MAFIA-DE, RDR2 and SLEEPING-DOGS (refmech-2026-11-20) against PARTS-TREE.md. Mechanics that mean the same thing are merged across games. Games: G = GTA V, K = KCD2, M = Mafia DE, R = RDR2, S = Sleeping Dogs.

Ruling short names: STATS (stats, levels, skills, perks), UI (minimap, waypoints, objective markers, meters), OVER (game over), JUMP (jumping), VEH (boats and buses as scenery only), MULTI, CRAFT, MINI (lockpicking and crafting minigames), NEEDS (hunger, tiredness, fuel, wear), RACE (racing, tuning, garage), PRICE (price tables, supply chains), RANDOM (random fights and encounters), COMBAT (lock-on, finishers, duels, combat music), VICE (drink, gambling, drugs, prostitution, children), BRAND, HORSE, FIRST (first person).

A GAP row marked "decline" is a mechanic nothing builds and no ruling names, but LEDGER should not want it. It is listed so the decline is on record.

| Mechanic | Games | Verdict | Part id or ruling | Note |
|---|---|---|---|---|
| Walk, run, sprint, toggle walk | G K M R S | MAP | 1.1.1 | |
| Jump, bullet jump, stunt jumps, base jumps, parachute | G K R | RULED_OUT | JUMP | |
| Swimming, diving, scuba | G S | RULED_OUT | VEH | Water is scenery; the quay edge is a fight tool at 1.3.5 |
| Crouch, sneak, stealth mode | G K M R | MAP | 1.1.5 | Part text says no crouch-walk stealth game; hiding is by doorways and shadow |
| Climb fences, vault, rooftop free run | M S | GAP | proposed 1.5.1.1 | See Gaps; JUMP boundary |
| Interact key (doors, objects, talk) | K M S | MAP | 1.1.3, 1.6.8 | |
| Doors, thresholds | K M | MAP | 1.1.3 | |
| Carry a load; carry or drop a body | M R | MAP | 1.1.4, 1.6.7, 2.16 | |
| Take cover from gunfire, destructible cover | G M S | GAP | proposed 1.3.10.1 | |
| Cover from sight, light and dark | K R | MAP | 1.4.2 | |
| Combat roll, dodge | G K M S | MAP | 1.3.2 | Block and dodge on a readable wind-up |
| Block, parry, counter, riposte, perfect block | K M S | MAP | 1.3.2 | Window is read from the man, no prompt icon |
| Strike timing, light and heavy, combos, spacing, herding | K S | MAP | 1.3.1, 1.3.8 | |
| Lock on, next target, combat free look | G K S | RULED_OUT | COMBAT | Replaced by 1.3.3 |
| Finishers, combo enders, environmental kills, Dim Mak, takedown prompts | K S | RULED_OUT | COMBAT | |
| Duels, master strike, sword training | K | RULED_OUT | COMBAT | |
| Stamina in combat, strength bar, Face meter, overdrive | G K S | RULED_OUT | UI, STATS | Condition shows on the body at 1.3.7 |
| Grapple, grab, shove, drag | S | MAP | 1.3.4 | Grab is one of the lower rungs |
| Throw a man off a ledge, human shield, hostage | S | GAP | decline | Spectacle moves; off the plain-fight design |
| Quiet blow from behind, stealth kill, knock out a sleeper | G K M S | GAP | proposed 1.3.4.1 | |
| Street as a weapon (rails, walls) | S | MAP | 1.3.5 | |
| Melee weapons, found and carried | G K M S | MAP | 1.3.6 | |
| Weapon breaks or dulls | K S | RULED_OUT | NEEDS | wear |
| Dirty weapon, cleaning, sharpening | K R | RULED_OUT | NEEDS | wear |
| Disarm a man | K S | MAP | 1.3.4 | Hand-to-hand lower rung; confirm disarm is among the acts |
| Firearms: aim, shoot, reload | G M R S | MAP | 1.3.10 | Rare late guns |
| Headshots, weapon damage by type, recoil, sway | G M R S | MAP | 1.3.10 | |
| Aim assist levels | G M S R | MAP | 7.10 | Assists only |
| Reticle, ammo display | G M S | RULED_OUT | UI | |
| Holster to avoid scaring people | M R | MAP | 1.4.4 | Weapon in hand is a give-away |
| Warning shot, threaten a witness | R | MAP | 2.5.2, 1.4.5 | |
| Slow motion (bullet time, Dead Eye, vault slow-mo) | G R S | RULED_OUT | UI, STATS | Spirit of the rulings: it is a meter-driven special ability |
| Special ability meters, rage, Dead Eye | G R | RULED_OUT | UI, STATS | |
| Explosives, grenades, Molotovs | G M S | MAP | 1.3.10, 1.6.7 | Rare and late; firearm family |
| Grenade launcher, military hardware | S G | RULED_OUT | COMBAT | Spirit; no war game. Armed response at 2.6.6 |
| Cars, bikes: driving | G M S | MAP | 1.2.1 | Bikes are not in the parts list; treat as scenery |
| Motorcycles as a rideable | G M S | RULED_OUT | VEH | Spirit: only the firm's cars drive |
| Boats, aircraft, helicopters | G S | RULED_OUT | VEH | |
| Handbrake, drift, driving models | M S G | MAP | 1.2.1 | |
| Speed limiter, manual gearbox | M | RULED_OUT | NEEDS | Spirit: fuel and wear options; no gearbox game. Driving help at 7.10 |
| Horn, look back, camera switch | M S G | MAP | 1.2.2 | |
| Enter and exit a car, pull a driver out | M S | MAP | 1.2.3 | |
| Carjack a moving car | G M S | GAP | decline | Draws police, random street event; LEDGER takes parked cars (see Gaps) |
| Take a parked car (window, tool, quiet key) | G M S | GAP | proposed 1.6.1.1 | |
| Lockpick cars and doors | G K M S | RULED_OUT | MINI | Getting in at 1.6.1 |
| Ram a vehicle, car as a weapon | G M S | MAP | 1.2.4, 1.2.5 | |
| Run down people | G S R | MAP | 1.2.5 | Hurt, never kills |
| Shoot from a car | G M S | MAP | 1.3.10 | Firearm family; chases at 1.5.3 |
| Shoot out tyres, flip pursuers | S G | MAP | 1.5.3 | |
| Action hijack, dismount slow-mo | S | RULED_OUT | COMBAT | Spectacle finisher |
| Vehicle damage, sinking, car wrecks | G M | MAP | 1.2.4 | |
| Fuel gauge, fuel drain | G M | RULED_OUT | NEEDS | |
| Weather affects handling | G | MAP | 4.8, 1.2.1 | |
| Race events, races, drag, stunt time trials | G M S | RULED_OUT | RACE | |
| Garage of owned cars, vehicle customisation, valet | G M S | RULED_OUT | RACE | |
| Buy vehicles online | G | RULED_OUT | RACE | |
| Hitchhikers, giving rides | G | MAP | 3.4, 1.2.7 | Fares |
| Taxi as fast travel | G S K R | GAP | proposed 1.2.7.1 | See Gaps; stagecoach, train fast travel fall under VEH |
| Towing a car to a drop-off | G | MAP | 3.5.1 | A carry job |
| Driver talk while driving | M | MAP | 1.2.7 | |
| Horse riding, whistle, bonding, stamina, tack, stable | K R | RULED_OUT | HORSE | |
| Lasso, hogtie, carry a captive | R | RULED_OUT | HORSE | Spirit; 1970s Western kit |
| Bow, hunting, animal study, scent, bait, clean kill | K R G | GAP | decline | Not a port crime verb; ruling spirit is the 1990 port |
| Fishing minigame | R | GAP | decline | Fish dock is set dressing at 4.2.2; a minigame is off-pillar |
| Dog companion (fights, tracks, fetches) | G K R | GAP | proposed 4.11.1 | See Gaps (guard dogs and company) |
| Distract a guard dog with meat | K | GAP | proposed 4.11.1 | Same gap |
| Pet or call a dog | K R | GAP | proposed 4.11.1 | Same gap |
| Throw a stone to distract | K | GAP | proposed 1.4.3.1 | |
| Lure a guard away, separate a target | K S | GAP | proposed 1.4.3.1 | Same gap; 1.7.2 can send a man |
| Lockpicking minigame, pick breaking, noise | K M S | RULED_OUT | MINI | |
| Pickpocketing minigame and timer | K | RULED_OUT | MINI | Spirit; the taking is 1.6.3 without a game |
| Search bodies and containers, loot | G K M R | MAP | 1.6.2 | |
| Safe cracking, hacking minigames | R S | RULED_OUT | MINI | Safes are searched at 1.6.2 |
| Dynamite a safe | R | MAP | 1.6.1 | Force that is loud and shows |
| Store robbery, hold up a clerk | G R | MAP | 1.6.3, 2.7.5 | |
| Armoured van, coach, train robbery | G R S | MAP | 3.5.3, 3.5.4 | Authored job content |
| Home robbery, break-in | K R | MAP | 3.5.3, 1.6.1 | |
| Heist: scout, plan, crew choice, cut | G R | MAP | 1.7.3, 2.11.1 | |
| Crew improves if it survives | G | MAP | 2.11.3 | |
| Companion orders | K | MAP | 1.7.1 | |
| Intimidate, threaten, antagonise, rob a person | K R S | MAP | 1.6.4, 1.3.4 | |
| Greet, call out, compliment | R G | MAP | 2.12.4, 3.6.1 | |
| Persuasion, speech checks, fast talk | K S | RULED_OUT | STATS | Live talk at 3.6.1 does it |
| Bribery | K | GAP | proposed 2.6.8 | See Gaps (squaring the law); witness bribe is 2.5.2 |
| Intervene in someone else's fight | R | MAP | 3.3 | Authored side story found on foot |
| Chance encounters, random events, ambushes | G R | RULED_OUT | RANDOM | Authored side stories at 3.3 |
| Bounty hunters sent after you | R | MAP | 2.10.3 | Pressure from rivals, not spawned |
| Talk to passers-by, life stories | G | MAP | 3.6.4, 3.3 | |
| Hang out, dates, romance | G S | MAP | 3.2.5, 3.3 | One person worth honesty; romance not built |
| Phone calls start missions, texts | G S | MAP | 3.4.3, 1.6.8 | The radio and phone box, no mobile in 1990 |
| Phone camera, Snapmatic, photograph a target | G S | GAP | proposed 1.6.10 | See Gaps |
| Bugging, phone tracking, eavesdrop | S | GAP | proposed 1.4.7 | See Gaps |
| Karaoke | S | GAP | proposed 4.10.1 | See Gaps (pub games and a turn) |
| Darts, tennis, golf, yoga, triathlon | G | GAP | proposed 4.10.1 (darts only) | Others decline: off-pillar |
| Poker, blackjack, dice, dominoes for stakes, betting, cockfights | K R S | RULED_OUT | VICE | Gambling. Dominoes and darts without stakes are in the 4.10.1 gap |
| Drink, schnapps, hangover, saviour schnapps save | K R M S | RULED_OUT | VICE | |
| Drugs (drug busts, drug effects) | S | RULED_OUT | VICE | |
| Massage, escorts, dates for pay | S | RULED_OUT | VICE | |
| Children, family kids | all | RULED_OUT | VICE | |
| Shooting range, flight school, skill training places | G | RULED_OUT | STATS | |
| Dojo, sifu, learn moves with collected items | S K | RULED_OUT | STATS | |
| Wanted stars, heat meter, flashing stars | G M S | RULED_OUT | UI | Police stages at 2.6.5 and the dial 2.13 |
| Police need a witness or sight to start | G M R S | MAP | 2.5, 2.6.3 | |
| Silence or kill the witness caller | G K R | MAP | 2.5.2, 1.4.5 | |
| Witness walks to tell | K R M | MAP | 2.5.1 | |
| Delayed discovery of unseen crimes | K R | MAP | 2.6.5, 2.16 | |
| Crime linking across offences | K | MAP | 2.3, 2.6.3 | |
| Lose the police by breaking line of sight, search resumes on sight | G M S R | MAP | 1.5.4, 2.6.5 | |
| Search phase, red search zone | G R | RULED_OUT | UI | Zone circle is a marker; searching is 2.6.5 |
| Police escalation with units (roadblocks, helicopters, NOOSE, military) | G M | MAP | 2.6.6, 2.13 | Slow armed response only; no helicopters or military |
| Police boats, helicopters, tanks | G | RULED_OUT | VEH | |
| Stop and search, challenge | K R | MAP | 2.6.2 | |
| Pull-over, ticket, minor offence fine | G M K | GAP | proposed 2.6.7 | See Gaps |
| Fine scaled to crime, speeding, red lights, no torch at night | M K G | GAP | proposed 2.6.7 | Same gap |
| Arrest, surrender, resisting | G K R S | MAP | 2.6.3, 2.6.4 | |
| Jail time, bail, bail cost | G K R | MAP | 2.6.4 | Custody as hours; paying bail is in the 2.6.8 gap |
| Gang frees you from jail | R | MAP | 2.6.4, 1.7.2 | Duty solicitor; crew can vouch |
| Pillory, caning, branding, execution | K | RULED_OUT | OVER | Execution reload is game over; stat penalties are STATS; the mark is 2.12.1 |
| Unrest, town lockdown, hostile town escalation | K R | MAP | 2.13, 2.5.3 | Dial and crowd reaction |
| Per-town and per-class reputation | K | MAP | 2.12.1, 2.12.2 | |
| Honor meter, good and bad deeds | R | RULED_OUT | UI | Regard is held in memory at 2.3 and 2.12 |
| Face currency, Triad and cop dual standing | S | MAP | 2.12.1, 2.9 | Arrangement and name ladder |
| Dirty and bloody look shunned or feared | K R S | MAP | 1.4.4, 2.2.5 | |
| Outfit changes how people treat you | S K R | MAP | 1.4.4, 2.12.3 | Dress is part of access |
| Change clothes, outfit presets | G K S R | MAP | 1.6.6, 1.4.4 | |
| Haircut, shave, barber, tattoos, clothing shops | G R | GAP | proposed 1.4.4.1 | See Gaps (changing his look); tattoos decline |
| Mask, bandana, visor to hide face | K R | MAP | 1.4.4, 2.2.2 | Disguise by dress; no heavy mask kit |
| Recognition, white and red witness icons | R | MAP | 2.2.2, 2.3.2 | Identification ladder; no icons (UI) |
| Visibility, noise, conspicuousness | K R | MAP | 1.4.1, 1.4.3, 2.2.3, 2.2.4 | |
| Scent detection by animals or men | K R | RULED_OUT | NEEDS | Spirit; hygiene need |
| Bathing, laundry, wash blood and dirt | K R | MAP | 1.6.7 | Blood washed with water and privacy |
| Dirt and Reeky debuff | K | RULED_OUT | NEEDS | Dirt as a give-away is 1.4.4, no debuff |
| NPC sleep, patrol at night, routines | K G | MAP | 2.1.1, 2.1.2 | |
| Traffic obeys lights; pedestrians cross, flee, gawk | G M | MAP | 4.5, 2.5.3, 2.1.5 | |
| Weekend traffic density, time-of-day details | G | MAP | 2.1.2, 4.7 | |
| Weather changes who is out | G R | MAP | 2.1.4 | |
| Extreme weather drains cores | R | RULED_OUT | NEEDS | |
| Rain washes blood | G | MAP | 4.8, 5.3.3 | |
| Bodies float or sink, dump a body | G | MAP | 2.16, 1.6.7 | |
| Blood and wounds on screen | G K | MAP | 1.3.7, 5.9 | |
| Wanted fences, fence stolen goods | K R S | MAP | 2.7.6 | |
| Stolen goods pay less; marked car payout | K S G | MAP | 2.7.6, 1.6.3 | Hot mark |
| Shopkeepers remember a robber | G | MAP | 2.7.5 | |
| Shakedowns, protection money, debt collection | S | MAP | 1.6.4, 3.5.2 | |
| Property income each week, buy businesses | G | GAP | proposed 2.7.8 | See Gaps (premises); stocks side is PRICE |
| Stock market, assassination stock trades | G | RULED_OUT | PRICE | |
| Trader haggling, merchant patience, trade basket | K | MAP | 2.7.5 | Shops haggle and refuse |
| Prices by reputation | K S | MAP | 2.7.5, 2.12.3 | Shops remember |
| Money display, spending display | G M S | MAP | 6.2.4 | Money in words |
| Camp donations, camp upgrades, base improvement | R | GAP | proposed 2.7.8 | Same gap as premises |
| Rent and wages | K R | MAP | 2.7.4 | |
| Jobs for bed and income | K | MAP | 2.15, 3.4 | Fares |
| Smithing, alchemy, soap, cooking, camp crafting, recipes | K R | RULED_OUT | CRAFT | |
| Skill books, pamphlets that teach recipes | K R | RULED_OUT | STATS | |
| Stats, levels, skills, perks (all trees) | G K S R | RULED_OUT | STATS | |
| Carry weight, armour weight, armour coverage | K R | RULED_OUT | STATS | Pockets are limited at 1.6.9 |
| Gear condition and repair | K | RULED_OUT | NEEDS | wear |
| Hunger, food, eating, weight, cores, energy | K R G | RULED_OUT | NEEDS | |
| Health regen, first aid, tonics, food heals | G K M R S | MAP | 1.3.7 | Condition shows on the body; how a man mends is left to 1.3.7 |
| Bandage a wound | K | MAP | 1.3.7 | |
| Sleep to save and heal | K R G S | MAP | 7.11, 7.8 | Sleep is a skip; saves are automatic |
| Cigarettes, tobacco | R | MAP | 5.2.5, 5.9 | Tobacco allowed; no stat effect (STATS) |
| Praying at shrines for health | K S | RULED_OUT | STATS | Health shrines are max-health progression |
| Hospital respawn, wasted, wake in clinic | G S | MAP | 4.3.8, 7.9 | Where a beaten Tom wakes |
| Death costs money, gear loss | G | MAP | 7.9 | Each failure ends in a state |
| Game over, execution reload | K | RULED_OUT | OVER | |
| Checkpoint restart after a failed mission | G M S R | MAP | 7.9, 7.8 | Failure without reload |
| Mission replay, medals, gold objectives | G R S | GAP | decline | Autosave after every deed makes replay impossible by design |
| Chapters, progress panel | R M | MAP | 3.1 | |
| Story set in any order | G | MAP | 3.3, 7.12 | |
| Three protagonists, switching | G | RULED_OUT | STATS | No ruling names it; LEDGER is one man, Tom, by design (VISION). Decline |
| Linear campaign, three acts | M | MAP | 3.1.1 to 3.1.3 | |
| Faction choices, endings | K G | MAP | 3.1.4 | |
| Stranger missions, favours, question-mark contacts | G R S | MAP | 3.3, 3.4.2 | No markers (UI) |
| Time-limited missions | R | MAP | 3.5.6 | Appointments in the day book |
| Delivery missions, collection missions | G S | MAP | 3.5.1, 3.5.2 | |
| Escort a person | S | MAP | 1.2.7, 3.4.2 | |
| Lure the police then escape | S | MAP | 1.5.4, 3.5.4 | |
| Tail a target | S G | MAP | 1.1.6, 1.2.6 | |
| Interior set-piece missions | M | MAP | 4.3, 3.5.3 | |
| Cases, investigations, cell phone tracking | S | MAP | 3.5.4, 3.3 | Authored tail and search content |
| Open world from the start, districts | G M S | MAP | 4.1, 4.2 | One dense district |
| Varied terrain, countryside, mountains | G K M R | RULED_OUT | VEH | Spirit: no overland travel, no horses; the Hook only |
| Landmarks, lighthouse, church bells | G M | MAP | 4.1.3, 5.5.3 | |
| Restricted zones (docks, base) | G | MAP | 4.2.3, 2.6.1 | |
| Safe houses, apartment, furniture, pets | S G R | MAP | 4.3.2 | The flat above; furniture cosmetic only |
| Hotels, baths, rooms to sleep | R K | MAP | 7.11 | |
| Collectibles (foxes, statues, graves, postcards, cards, dreamcatchers) | all | GAP | decline | Completion lists need markers (UI); side stories at 3.3 cover found things |
| Treasure maps, riddles, digging | K R | GAP | decline | |
| Readable letters, newspapers, in-game internet news | M G K R | GAP | proposed 6.2.6 | See Gaps (things to read) |
| TV shows, in-game internet | G | MAP | 4.9 | Period detail; no web in 1990 |
| Radio stations, signal fade, radio shows song name | G M S | MAP | 5.7.1, 5.5.5 | |
| Characters nod to the radio | G | MAP | 5.2.5 | |
| Night lighting, car interior lights | G | MAP | 5.4.2 | |
| Sweat, shoes squeak, sound details | G | MAP | 5.5.1 | |
| Camera positions, shoulder swap | R M G | MAP | 5.8.1 | |
| First person view | G R | RULED_OUT | FIRST | |
| Cinematic ride, follow NPC camera | R K | MAP | 5.8.1, 5.8.2 | |
| Cutscenes, expanded scenes | M | MAP | 5.8.2 | |
| Music reacts to honour or combat | R | RULED_OUT | COMBAT | Spirit; 5.7 silence the commonest music |
| Minimap, radar, mini-map toggle | G M S R | RULED_OUT | UI | |
| Waypoint, GPS route, objective marker, world-space arrows | G M S R | RULED_OUT | UI | |
| Paper map | R M S G K | MAP | 6.3 | |
| Health, stamina, Face meters on HUD | G S R | RULED_OUT | UI | |
| Weapon wheel, quick items | G M K R | MAP | 1.6.9, 6.6 | Pockets, no wheel needed |
| Character wheel | G | RULED_OUT | STATS | See switching above |
| Phone menu: contacts, email, internet, settings | G S | MAP | 6.2, 1.6.8 | Notebook and box phone |
| Journal, codex, compendium, game log | K R S | MAP | 6.2 | |
| Player screen, reputation tab | K | MAP | 6.2.1, 6.2.5 | People and Tom's reading |
| Prompts for greet, rob, interact | R K | MAP | 6.1.1 | |
| Subtitles, quick chat lines | S K | MAP | 6.1.2, 3.6.6 | |
| Hints and tutorial teaching | M S G | MAP | 6.5 | |
| Hide HUD, crosshair, location name options | R M | MAP | 7.10, 8.4 | |
| Controls, remapping, toggles for hold actions | all | MAP | 6.6, 8.4 | |
| Tap assist | R | MAP | 8.4 | |
| Photo mode | K R G | MAP | 6.8 | |
| Rockstar Editor, social uploads, leaderboards | G R S | RULED_OUT | MULTI | Online features |
| Difficulty levels | M K S G | MAP | 7.10 | Assists only |
| Police setting independent of difficulty | M | MAP | 7.10, 2.13 | |
| Hardcore mode | K | RULED_OUT | STATS | Spirit; difficulty ladder is out (7.10) |
| Autosave, manual save, quicksave, sleep saves | all | MAP | 7.8, 8.2 | |
| Save slots | G R S | MAP | 8.2, 7.8 | |
| Graphics, FOV, DOF, presets, 4K | M G R | MAP | 8.3, 8.1 | |
| Console commands, cheats | K | RULED_OUT | MULTI | Spirit; none |
| Support report | S | MAP | 10.9 | |
| Editions, DLC, platforms, store | all | MAP | 10.1, 10.2, 10.7 | |
| Free Ride mode, sightseeing | M | RULED_OUT | OVER | Spirit; the town is always the game (7.12) |
| Online or multiplayer modes | G R S | RULED_OUT | MULTI | |

## Gaps

1. Taking cover from gunfire (snap to a wall or car, shots chip it). Parent 1.3.10 as 1.3.10.1. Games G M S. Why: guns are rare and late but armed callers are the worst night in the Hook, and doorways and car sides are what the street has. Fits the 1.4.2 dark-as-cover idea.
2. Vaulting and climbing low obstacles. Parent 1.5.1 as 1.5.1.1. Games M S. Why: running from a witness or a constable across yards, rails and fences is the core foot chase. JUMP boundary: a mantle over a fence is not a jump button; Jafar's call.
3. Minor offences and fines (traffic stop, ticket, loitering). Parent 2.6 as 2.6.7. Games G M K. Why: Tom drives a minicab for a living; a traffic constable stopping a cab is the lowest rung of the law and costs the tin.
4. Squaring the law (bail, a blind eye, paying a charge away). Parent 2.6 as 2.6.8. Games K R G. Why: a firm with night money would pay; Ellis and the beat constable need a price or a refusal. Overlaps 2.5.2 (witness only).
5. Taking a parked car. Parent 1.6.1 as 1.6.1.1. Games G M S. Why: 1990 Britain's car crime; a hot car is a job for the firm and feeds 2.7.6 fencing. No lockpick game; window or a tool, loud or quiet.
6. Photograph as evidence or leverage. Parent 1.6 as 1.6.10. Games G S. Why: a 35mm camera feeds frames, blackmail and witnesses (2.2.5 already counts a camera).
7. Overhearing and bugging a phone box or office phone. Parent 1.4 as 1.4.7. Games S. Why: surveillance by the firm and on the firm; fits 1990 payphones. Lowest priority.
8. Drawing a watcher away (thrown thing, noise, a decoy). Parent 1.4.3 as 1.4.3.1. Games K S. Why: opens a door or clears a witness's eyeline without a blow.
9. Quiet blow from behind on an unaware man (cosh). Parent 1.3.4 as 1.3.4.1. Games G K M S. Why: the cosh is in 1.3.6; not a finisher, a single contextual hit with no prompt.
10. Guard dogs and a dog for company. Parent 4.11 as 4.11.1. Games G K R. Why: yards and the dock have dogs; scraps or noise quiet one; a dog also marks a home.
11. Changing his look (barber, clothes shop, second-hand coat). Parent 1.4.4 as 1.4.4.1. Games G R. Why: the coat is the identity give-away; a new coat or a shave is how Tom escapes a witness.
12. Being driven by the firm (a ride as a time skip). Parent 1.2.7 as 1.2.7.1. Games G S K R. Why: Kevin or Terry drive Tom; replaces fast travel without a marker; 3.5.5 already has sit-downs in the back.
13. Things to read (the local paper, letters, notes, posters). Parent 6.2 as 6.2.6. Games M G K R. Why: a paper reflects what the town knows; gossip made visible.
14. Pub games and a turn (darts, pool, dominoes, karaoke, no stakes). Parent 4.10 as 4.10.1. Games G R S. Why: pubs exist without drink (4.10); something to do there that puts Tom among people.
15. Premises and office improvements (a lock-up, a second phone, a better radio). Parent 2.7.4 as 2.7.8. Games G R S. Why: the firm grows; spending on the base ties money to place without price tables.

Declined: collectibles; treasure maps; mission replay and medals; hunting and fishing; throws and hostages; carjacking a moving car; tennis, golf, yoga; tattoos.
