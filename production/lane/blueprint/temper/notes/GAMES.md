# How NPC-focused games model personality, and how players feel it

All pages read 24 Nov 2026 through WebFetch (after WebSearch). Fetch tool returns a model-made summary of each page, so quotes are as the tool gave them. "Unverified" marks anything not confirmed by a primary source. Mafia series not used. No GTA VI material.

## 1. Per game

**Shadow of Mordor / Shadow of War (Nemesis)**
- Models: named orcs with a rank, strengths, weaknesses, fear and hate triggers, scars, and memory of the player (who killed whom, who burned whom). Also power struggles and promotion.
- Dials: no official total found (unverified). Examples only: weaknesses such as stealth attacks or arrows to the head; strengths such as bodyguards or immunity; hate trigger (Thrak grows stronger when his health drops); fear of fire after being set alight. Discrete labels, not sliders. https://gamesradar.com/shadow-mordor-nemesis-system-amazing-how-works
- Readable: strengths and weaknesses are not shown at first. Intel unlocks them (mind-read a lower orc, or fight and learn). Scars show on the orc's body. Dialogue refers to past meetings. Same GamesRadar page. Shadow of War dev: orcs should "remember you" and speak to "the most important interactions or stories". https://www.gamespot.com/articles/shadow-of-wars-dev-on-new-nemesis-system-movie-con/1100-6448595/
- Changes over play: yes, strongly (promotion, scars, revenge, betrayal). Same pages.
- Designer view: the early build had too many layers. Per the Gamasutra postmortem as summarised: factions each had Morale and Discipline bars, the hierarchy UI "looked somewhat like a Christmas tree", and playtesting pulled it back to "personal villains". https://gamebanshee.com/k3axd (Gamasutra summary; see also https://www.gameinformer.com/b/news/archive/2015/01/20/shadow-of-mordor-s-nemesis-system-was-once-a-bit-more-complicated.aspx). De Plater's inspiration was sport, "systems which generate stories every year". https://www.pcgamer.com/shadow-of-mordors-nemesis-system-inspired-by-multiplayer-sports
- Praise/punish: TechRadar (20 Sep 2017, preview) calls it "brilliant" but found repeated unskippable monologues after each death ("a good few minutes") overbearing. https://techradar.com/news/shadow-of-wars-nemesis-system-is-at-once-brilliant-and-yet-incredibly-frustrating . No counts found.
- GDC 2018 talk "Helping Players Hate (or Love) Their Nemesis" (Chris Hoge, Monolith): description only; I could not see the slides or video. https://www.gdcvault.com/play/1025150/contactUs

**Hitman (2016 to World of Assassination)**
- Models: not personality but knowledge states. Each NPC has its own knowledge base, fed by sensors; a shared service holds what is commonly known about 47 (compromised or not, last seen). A disguise service tells NPCs whether an outfit looks wrong. Civilians can confront or alert but not fight; guards fight; enforcers see through certain disguises. https://gamedeveloper.com/design/the-ai-of-hitman-2016-
- Dials: roles (civilian, guard, enforcer, bodyguard) plus a few states. The article gives no meter values (it says so). Scale numbers: 300+ behaviour-tree characters per level, 1,000+ crowd NPCs in 2016, 2,000+ in Hitman 2.
- Readable: enforcers carry "a big, bright triangle over their heads" (GamesRadar impressions, 2016: https://www.gamesradar.com/hitman-everybodys-gunning-sharp-dressed-man/). Player forum report (speculation, unverified): "!" for alerted, orange for a witness who has compromised the disguise, "Crime Noticed" when fully compromised; some witnesses show nothing, which confused players. https://www.hitmanforum.com/t/witnesses-mechanics/21574
- Designer view: stealth players "need to read what NPCs are thinking", so animation must telegraph decisions; routines must be predictable. Same Game Developer article.
- Changes over play: no personality drift; state resets per mission.

**Kingdom Come: Deliverance II**
- Models: per-settlement reputation that builds gradually; witnesses report to guards or confront; many crimes in one area cause "Unrest" (people arm up). Fix by quests, an indulgence or a pilgrimage. https://deltiasgaming.com/?p=134932 (secondary guide)
- Dials: reputation per community; the guide gives no numeric scale. For the first game, the wiki gives 0 to 100 per village, built from demographic groups (soldiers, villagers, monks). I could not confirm KCD2 uses the same. https://kingdomcomedeliverance.wiki.gg/wiki/Reputation
- Readable: a Reputation tab in the Player screen, with an icon whose colour shows how content a community is. Dialogue also reacts (VGC review: "thousands of permutations" by deeds, stats and clothing). https://www.videogameschronicle.com/review/kingdom-come-deliverance-2-review/
- Changes over play: yes, and it can be repaired.
- Praise/punish: no NPC-behaviour criticism in the VGC review. Could not reach primary Warhorse design talk on witnesses.

**Red Dead Redemption 2**
- Models: honour as a single slider (white to red, hat icon). It is continuous: one horse collision cost "about one eighth". Witnesses may report; a good Arthur can pay off or threaten them, a bad one usually cannot. Bounties are by region. Music, journal, shop discounts and killcam change with honour. https://www.gamespot.com/articles/red-dead-2-guide-to-honor-how-morality-and-the-hon/1100-6462777
- Witness detail: faces uncovered can be recognised, a bandana helps; hygiene and blood are noticed; a scared witness may talk anyway. https://www.gamespot.com/articles/red-dead-redemption-2s-world-is-full-of-snitches/1100-6462203/
- Readable: HUD hat icon on each change; check any time on the D-pad. No per-NPC personality dial found.
- Praise/punish: no counts found.

**Watch Dogs: Legion**
- Models: every recruit has an occupation, abilities, perks and drawbacks (one example: habitual hiccups that blow cover). Seen by hacking their profile. No fixed trait count found. https://www.gameskinny.com/1bnn7/ubisoft-digs-into-watch-dogs-legions-recruitment-system
- Discrete labels, mostly gameplay modifiers rather than behaviour. Designer reasoning not stated in that source. No review counts found.

**The Sims 4**
- Models: traits plus moods (emotion). 39 traits in four categories (emotional 10, hobby 8, lifestyle 11, social 10), plus 6 pack/occult and reward traits outside the count. Adults hold 3 plus 1 from aspiration. . https://www.playnews.gg/en/guides/the-sims-4-all-personality-traits-full-list-effects (secondary guide)
- Discrete labels in a panel; changes only at life stage or baby (https://www.gamepressure.com/thesims4/personality/z268ca).
- Players' view (EA forum thread, about seven comments, no poll count): traits "play like they barely made it into the game", want "more concrete game effects", one would prefer sliders as "people tend to fall between two extremes", and fear is missing as an emotion. https://forums.ea.com/discussions/the-sims-4-general-discussion-en/does-the-sims-4-require-a-trait-overhaul/1438382

**RimWorld**
- Models: up to a few traits per colonist (exact cap and total unverified in my reads), backstory, and a mood bar. Mood 0 to 100%, a white triangle shows the target; thoughts are listed with numbers (for example "Hungry (-6)"). Break lines default to 35%, 20% and 5% (minor, major, extreme; the threshold page puts them as 35 / 20 / 5). Traits move those lines: Iron-willed lowers by 18 points of threshold, Volatile raises by 15, Neurotic by 8, Very neurotic by 14. https://www.rimworldwiki.com/wiki/Mood , https://www.rimworldwiki.com/wiki/Mental_Break_Threshold
- Mixed: traits are discrete labels, mood is continuous. Readable by label and by numbers. Mood changes constantly; traits are fixed ("you cannot change the character's traits at ease"). https://gamedeveloper.com/design/rimworld-dwarf-fortress-and-procedurally-generated-story-telling
- Designer view (Sylvester, as quoted by Game Developer): "the simplified characterization that tries to impact gameplay as much as possible"; RimWorld "shows enough that it constrains the imagination a little bit", and he wanted to avoid "design traps" that "marred Dwarf Fortress". https://gamedeveloper.com/design/how-i-rimworld-i-fleshes-out-the-i-dwarf-fortress-i-formula
- The full GDC video and his book were not read.

**Dwarf Fortress**
- Models: 50 personality facets, each 0 to 100 in seven bands, and 33 values, each -50 to +50 in seven bands. The neutral band gives no report (about 78% of facet values are neutral per the wiki). https://dwarffortresswiki.org/index.php/DF2014:Personality_facet , https://dwarffortresswiki.org/index.php/Belief
- Continuous underneath, shown as text per band on the personality screen (for example "is in a constant state of internal rage"). Changes slowly, mostly through events and stress.
- Player complaints (Steam thread, a few posters, no counts): effects "seemingly random and inconsistent", "a pretty frontend that promises lots of complexity, with little backend"; a "cruel" dwarf never fought. Defenders: "It's just subtle", effects appear under low mood and stress, and some call it "mostly flavor text". https://steamcommunity.com/app/975370/discussions/0/3716062978748076649
- Kitfox's Tanya Short says players only reached dramatic personality stories after 40+ hours in DF (see section 2).

**Crusader Kings III**
- Models: personality traits with opposites, plus stress from acting against nature. A table lists 35 personality traits, each with AI weights (boldness, compassion, greed, honour and so on) and opinion effects. https://segmentnext.com/crusader-kings-3-traits-guide (secondary; per-character cap not stated there, so unverified)
- Stress: forcing disliked actions raises it; overload triggers coping behaviour; prolonged stress can end badly. https://www.fanatical.com/en/blog/crusader-kings-3-character-traits-effects (secondary). Traits are shown as icons with tooltips (my knowledge, not confirmed by a source read).
- Could not read Paradox Dev Diary 58 (stress and traits): the forum returned a browser check page. Not reached.

## 2. Why few, legible traits beat many hidden ones

Best source: Tanya X. Short (Kitfox, co-author with Tarn Adams of Procedural Generation in Game Design), Game Developer, 22 Feb 2017, from her GDC AI Summit talk: https://gamedeveloper.com/design/maximizing-the-impact-of-procedural-personalities . Paper version, AIIDE-17: https://ojs.aaai.org/index.php/AIIDE/article/download/12973/12821
- "Extremes are easier to see and understand." Real people are mostly mild; players will not notice that, so push traits to the edge. CK2 says "Wroth", not "irritable".
- "Actions are easier to see than non-actions." Give passive traits an active expression (a chaste character who reacts to flirting).
- Beware secret systems: Age of Conan NPCs had a detailed needs model (five Maslow levels) that players never saw, so NPCs seemed to have no inner life.
- Reactions to the same event, shown side by side, reveal personality fastest; logs and after-the-fact questioning help; a visible change of trait in a crisis is compelling (Darkest Dungeon).
- The Shrouded Isle gives each villager one virtue and one vice.
- Subtlety can work (King of Dragon Pass) but too much blunt signalling makes cartoons.
- Her eight mechanisms are named in the paper.

Supporting evidence from the games above: Nemesis shed its Morale and Discipline layers and went back to personal villains (postmortem, above); Hitman insists on telegraphed, predictable behaviour; RimWorld's author explicitly aims at characterisation that "impact[s] gameplay as much as possible".

Counter-view: some DF players say overt traits would make the game unmanageable and that subtlety is intended (same Steam thread). Sims 4 players ask for more effect from only 39 traits, so few labels do not rescue a trait that has no visible effect.

## 3. Take-aways for a 1990 Britain street sim

1. Three to six labelled traits per person, each with a visible action, beats dozens of hidden facets.
2. Show the label (or an unmistakable behaviour) at least once early; unlock the rest by watching or asking (Nemesis intel).
3. Let one or two traits change through events, with a visible mark (scar, new habit).
4. Keep witness and suspicion as a few readable states with a clear marker, not a hidden meter (Hitman's unmarked witnesses confused players).
5. Keep a single continuous standing (honour, reputation) separate from the discrete personality labels.

## 4. Not reached or weak

- Paradox CK3 Dev Diaries 31 and 58: blocked by a browser check.
- GDC Vault slides and video for Nemesis talks; Sylvester's GDC talk video; Watch Dogs Legion designer talk on trait counts; KCD2 primary Warhorse design source (wiki pages returned were for the first game); RDR2 Rockstar sources.
- No number found for total Nemesis traits, Legion perks, RimWorld traits, or any review-score or survey counts about NPC personality. Hitman forum details are player speculation.
- Fetch summaries are by a small model; reread the primary page before quoting in canon.
