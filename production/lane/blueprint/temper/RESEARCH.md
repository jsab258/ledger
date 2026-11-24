# The temper: research

Written 24 Nov 2026 by the temper job. Every source below was read on 24 Nov 2026 unless marked; the four notes in notes/ hold the full findings with every link. Unverified points are marked so. Mafia is not used as a reference anywhere in this work.

## The questions

1. How do games known for their people model personality, how many dials, which can the player read, and what do players praise or punish?
2. What does psychology measure, and which traits predict greed and bribes, fear, obedience to the law, grudges and talk?
3. Who reports a crime in Britain and who keeps quiet; who gossips and through whom?
4. What does LEDGER already hold: the decisions townspeople make, the code that makes them, the cast, and earlier research?

## 1. Games (notes/GAMES.md)

- Shadow of Mordor and Shadow of War: named orcs with labelled strengths, weaknesses, fears and hate, scars and a memory of the player; the labels are hidden until the player gathers intel, the scars and taunts show at once. The makers built faction-wide Morale and Discipline bars and cut them back to personal villains after playtests (Gamasutra postmortem as summarised at https://gamebanshee.com/k3axd and https://www.gameinformer.com/b/news/archive/2015/01/20/shadow-of-mordor-s-nemesis-system-was-once-a-bit-more-complicated.aspx). The project's own study counted 19 of 22 Shadow of War Steam reviews valuing it (PLAYERS-STORIES, only 2 read in full).
- Hitman: no personality at all; roles (civilian, guard, enforcer) and knowledge states, telegraphed by animation and markers so players can read them (https://gamedeveloper.com/design/the-ai-of-hitman-2016-). Players punish unreadable noticing more than harsh noticing (5 of 9 players coded in the project's study).
- Kingdom Come: Deliverance II: reputation per community, shown on a tab; witnesses report to a guard or confront; talk reacts to the exact deed (https://www.videogameschronicle.com/review/kingdom-come-deliverance-2-review/; secondary guide https://deltiasgaming.com/?p=134932). No Warhorse design source on witnesses was reached.
- Red Dead Redemption 2: one continuous honour slider with a hat icon; witnesses can be paid or threatened, and threatening usually stops a report (https://www.gamespot.com/articles/red-dead-2-guide-to-honor-how-morality-and-the-hon/1100-6462777, https://www.gamespot.com/articles/red-dead-redemption-2s-world-is-full-of-snitches/1100-6462203/). No per-person personality dial was found.
- Watch Dogs: Legion: every recruit has an occupation, perks and drawbacks, read by hacking a profile; critics called the people "drearily one-note" (PC Gamer, 5 Nov 2020, via the project's study: 5 of 6 voices punish interchangeable people).
- The Sims 4: 39 labelled traits, three per adult (secondary guide https://www.playnews.gg/en/guides/the-sims-4-all-personality-traits-full-list-effects); players on EA's forum say they "barely made it into the game" (about seven posters, no count).
- RimWorld: a few labelled traits per colonist that move continuous mood-break lines (35, 20 and 5% by default; Iron-willed lowers them by 18 points) (https://www.rimworldwiki.com/wiki/Mental_Break_Threshold). Its maker aims at "simplified characterization that tries to impact gameplay as much as possible" (https://gamedeveloper.com/design/how-i-rimworld-i-fleshes-out-the-i-dwarf-fortress-i-formula).
- Dwarf Fortress: 50 facets (0 to 100) and 33 values, shown as text bands, with about 78% of facet values neutral and so shown as nothing (https://dwarffortresswiki.org/index.php/DF2014:Personality_facet). Players call the effects "seemingly random" and "mostly flavor text" (Steam thread, a few posters).
- Crusader Kings III: 35 personality traits with opposites, plus stress for acting against them (secondary guide https://segmentnext.com/crusader-kings-3-traits-guide); the dev diary was not reached.
- Design evidence: Tanya Short (Kitfox), GDC AI Summit, 22 Feb 2017, and AIIDE-17: push traits to extremes ("Extremes are easier to see"), give every trait an action, beware secret systems, and show reactions to the same event side by side (https://gamedeveloper.com/design/maximizing-the-impact-of-procedural-personalities, https://ojs.aaai.org/index.php/AIIDE/article/download/12973/12821).

What it says for LEDGER: a handful of dials, each pushed to an extreme in most people, each with an action the player sees; no hidden dial that changes nothing on screen; the same deed seen by several people should show their differences side by side. No review counts on personality systems were found beyond the project's own small samples.

## 2. Psychology (notes/PSYCHOLOGY-AND-REPORTING.md, part A)

- HEXACO's Honesty-Humility is the strongest trait predictor of wrongdoing: corrected r = -0.48 with workplace deviance, against Conscientiousness -0.40, Agreeableness -0.19, Emotionality -0.14 (Pletzer et al. 2019, https://pure.eur.nl/ws/portalfiles/portal/48180213/Pletzer-et-al.-2019-JVB.pdf). In 16 lab studies each standard deviation of it roughly halves the odds of cheating (odds ratio 0.53), and no other trait adds anything once it is in (https://www.cambridge.org/core/services/aop-cambridge-core/content/view/5B40039F2A564AEC265CEF288D917D5D/S1930297500009232a.pdf/who_lies_a_largescale_reanalysis_linking_basic_personality_traits_to_unethical_decision_making.pdf). Bribe-taking in one small lab study: Spearman -0.15 (https://pmc.ncbi.nlm.nih.gov/articles/PMC6139364). So greed is one dial of its own, and the strongest single one.
- Fear: HEXACO Emotionality (fearfulness) is its own factor and is mildly protective against deviance (-0.14, Pletzer). So nerve, the reverse of fearfulness, is a dial of its own, separate from greed.
- Grudges: Big Five Agreeableness with forgiveness r = 0.22 (Fehr et al. 2010 meta-analysis, https://ggsc.berkeley.edu/images/uploads/Fehr_et_al_2010_The_road_to_forgiveness-_A_meta-analytic_synthesis_of_its_situational_and_dispositional_correlates.pdf); HEXACO builds Agreeableness as forgiveness against retaliation (Hilbig et al. 2016, numbers not read). A grudge dial is grounded, though its effect in money games is weakly evidenced.
- Talk: gossip is about 14% of talk, about 52 minutes a day, mostly neutral; extraverts gossip far more, and wealth and schooling make no difference (Robbins and Karan, via https://webarchive.ucr.edu/news.ucr.edu/articles/2019/05/03/uc-riverside-study-busts-myths-about-gossip.html; the paper itself not read). So readiness to pass things on is a dial of its own (Extraversion), not a side of loyalty.
- Rule-following: Conscientiousness predicts less deviance (-0.40); no source was read on obedience to the police or risk taking (unverified; working hypothesis only).

## 3. Reporting and keeping quiet (notes/PSYCHOLOGY-AND-REPORTING.md, part B; earlier project research)

- Seriousness is the main reason for not reporting: BCS 1998, 44% "not serious enough", 33% "police could not do much", 22% "police would not be interested", 4% fear of reprisals (https://www.open.edu/openlearn/society-politics-law/sociology/the-meaning-crime/content-section-3.3). BCS 1992: fear of reprisals 2% of unreported incidents, 9% for assaults (Maynard 1994).
- Victims and witnesses differ sharply: on five high-crime British estates victims reported 70% of what happened to them, witnesses 29%; fear kept 22% of unreported witness incidents unreported against 6% for victims (Maynard 1994, Home Office Police Research Group paper 55, https://popcenter.asu.edu/sites/default/files/problems/witness_intimidation/PDFs/Maynard_FullReport_1994.pdf).
- Rates from the project's 1990 police research (29 Sep 2026, 1991 survey): wounding 47.7%, common assault 25.5%, robbery 47.2%, vandalism 27%, overall 43%.
- Intimidation after reporting followed 9 to 13% of reports on those estates, mostly verbal and from someone known (Maynard; Elliott 1998, https://popcenter.asu.edu/sites/default/files/problems/witness_intimidation/PDFs/Elliot_1998.pdf; Tarling et al. 2000, https://ojp.gov/ncjrs/virtual-library/abstracts/victim-and-witness-intimidation-key-findings-british-crime-survey). The project's threats research (29 to 30 Sep) found threats silenced about a quarter, and no witness-intimidation offence before 1994.
- Community: collective efficacy lowers violence (Sampson et al. 1997, https://pubmed.ncbi.nlm.nih.gov/9252316/, Chicago); a recent English estate study found informing sanctioned ("grass") and trust in police low (Davey 2021, https://orca.cardiff.ac.uk/141736/5/PoLAR%20-%202021%20-%20Davey%20-%20Everyday%20Authoritarianism%20Class%20and%20Coercion%20on%20Housing%20Estates%20in%20Neoliberal%20Britain-1.pdf). No 1980s or 1990s British port source on "no grassing" was reached (unverified for 1990). So willingness to go to the police is its own dial: trust and duty against the street's code, and it is not the same as nerve (fear is only a small part of silence).
- Bystanders: someone stepped in in 90.9% of 219 filmed public fights, more bystanders slightly raising the odds (odds ratio 1.10) (Philpot et al., https://core.ac.uk/download/211246875.pdf). People step in when danger is plain and others are there.
- Gossip runs through a few well-connected talkers: seeding with people named "good at spreading gossip" beat random seeds (Banerjee et al., https://economics.mit.edu/research/publications/using-gossips-spread-information-theory-and-evidence-two-randomized-0). Speed in hours was not found.

## 4. What LEDGER holds (notes/DECISIONS-IN-THE-BLUEPRINT.md, notes/PRIOR-AND-CAST.md)

- 42 townsperson decisions were found in the blueprint and the Core code. The Core reads only three per-person values: nerve, greed and loyalty (goodwill to Frank, which moves in play). Nothing loads the data into them, so the named cast runs on 0.5 defaults: everyone takes a bribe, pays a debt, folds to a squeeze and joins on a need.
- Of the data's fields, venal, talk and discretion are read by nothing; dutiful and willingness only by functions the Core never calls; keepsQuiet is a true/false in the data while the Core reads four words (owner, friend, anyone, nobody) and throws on anything else.
- Gossip passing reads no trait at all, though the design says a person "tells only her sister".
- The project's standards already ask for temper to show: MEM-03 (a person whose temper reaches the refusal rung refuses Frank within two game days), MEM-09 (nothing buys a memory away), MEM-11 (a refusal always leaves another road), TALK-09 (a refusal in character, for a reason of temper or loyalty).
- The traits draft of 29 Sep set nerve, loyalty and greed for 41 people; loyalty sat at 0.3 for almost all of them.
- CAST.md gives temperament words for the core six and the supporting cast; most named residents have none, so their values come from role and card.

## Not reached

The 1988 and 1992 BCS tables; Hilbig 2016, Zettler and Dunbar figures; risk-taking and obedience correlations; any 1980s or 1990s port-town "no grassing" source; gossip speed; CK3 dev diaries; GDC Vault slides; a Warhorse or Rockstar primary design source. None of these is used as evidence.
