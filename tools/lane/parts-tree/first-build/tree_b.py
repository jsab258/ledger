from tree_a import P, G
# ---------------- GROUP 6 ----------------
P("6", "The interface and the Ledger", "What is on screen: almost nothing, plus Tom's notebook and a paper map.", tr="both", o="lane", f=1,
  std="Nothing on screen Tom could not know (ER-SCREEN-01); no minimap, waypoints, meters (D12, D20, D37)", ss="DESIGN §17; rulings", des="DESIGN §10, §17")
P("6.1", "On screen in play", "The minimal screen.", tr="both", o="lane", f=1, std="ER-SCREEN-01, 02", ss="DESIGN §17", des="DESIGN §17")
P("6.1.1", "The prompt", "Names the person or thing ahead and in view.", std="ER-INPUT-02: held 0.2 s; everything usable has one", ss="DESIGN §17", des="DESIGN §17", tr="both", f=1, o="lane",
  h="0.5|8|guess", rk="low|", t="H: walk-up sweep")
P("6.1.2", "Subtitles", "Only with their audio; large; switches for chatter subtitles.", std="A subtitle shows only with its audio (ruling 23 Sep); nothing under 24 units; no overlap at four window sizes (ER-SCREEN-02)", ss="RULINGS; DESIGN §17", des="DESIGN §17", tr="both", f=1, o="lane", n=["8.4"],
  h="0.5|8|guess", rk="medium|round 6 gate fails: subtitles under the talk box at 1280 by 720 (lane row 20:36)", t="S: layout test at four sizes")
P("6.1.3", "The belief line", "A line low on screen when Tom comes to believe something new.", std="Within 3 s of a perceivable change (ER-CORE-02)", ss="DESIGN §10, §1", des="DESIGN §10", tr="both", f=1, o="lane", n=["6.2.2"],
  h="0.5|8|guess", rk="low|", t="S: trigger each perceivable change")
P("6.1.4", "Light and sound cues", "The picture's corners follow the light value; no meters.", std="Cue matches the rule's light value (DESIGN §2)", ss="DESIGN §2", des="DESIGN §2", tr="both", f=1, o="lane", n=[],
  h="0.5|8|guess", rk="medium|may read as a meter if overdone", t="H: ER-EYES-01 with the cue off and on")
P("6.2", "The Ledger notebook", "Tom's notebook of people and events: the one place he sees where he stands.", tr="both", o="lane", f=1,
  std="ER-LEDG-01 to 03: traced entries, opens in 120 ms, a person in three inputs, 'what next and where' answered from it alone", ss="DESIGN §10", des="DESIGN §10; LEDGER-SCREEN-STUDY-2026-11-18")
P("6.2.1", "People", "What he knows of each, and what he believes they know of him, with how sure.", std="Sure, thinks so, guesses by how learned (DESIGN §10)", ss="DESIGN §10", des="DESIGN §10", tr="both", f=1, o="lane", n=["2.3.1"],
  h="1|16|guess", rk="low|", t="S: no entry without a source event")
P("6.2.2", "Day book", "Events in order; nothing erased; wrong beliefs struck through with day and reason.", std="ER-LEDG-01", ss="DESIGN §10", des="DESIGN §10", tr="both", f=1, o="lane",
  h="0.5|8|guess", rk="low|", t="S: struck through, never removed")
P("6.2.3", "Open", "Jobs, debts, promises and appointments, each naming a person and a landmark.", std="ER-LEDG-03; ER-JOB-01", ss="DESIGN §10, §4", des="DESIGN §10", tr="both", f=1, o="lane", n=["3.5.6"],
  h="0.5|8|guess", rk="medium|direction without markers depends on it", t="H: 'what next, and where' from the Ledger alone")
P("6.2.4", "Money in words", "What he has and what is owed by Friday, in words.", std="ER-MONEY-02", ss="DESIGN §9", des="DESIGN §10", tr="both", f=1, o="lane", n=["2.7.7"],
  h="0.5|4|guess", rk="low|", t="H: asked what he has")
P("6.2.5", "Tom's reading", "On request and at each act's end: how things stand as Tom sees them, from signs he was given.", std="ER-END-02, 03", ss="DESIGN §10, §16", des="DESIGN §10", tr="both", f=1, o="lane", n=[],
  h="1|16|guess", rk="medium|", t="H predicts the ending from it")
P("6.3", "The paper map", "A map of the Hook that marks only places he has been or been told of.", std="No minimap (D37); only known places", ss="D12, D20, D37; DESIGN §10", des="DESIGN §10", tr="both", f=1, o="lane", n=["4.1.3"],
  h="1|16|guess", rk="low|", t="S: no unknown place marked; H: finds a told place")
P("6.4", "Menus", "Title, pause, settings, save and load, credits.", std="ER-START-01; ER-SAVE-02 (Esc pauses everywhere, no destructive choice one press from Resume)", ss="DESIGN §17; basics 1 to 5, 19", des="DESIGN §17", tr="both", f=1, o="lane", n=["8.3"],
  h="1|24|guess", rk="low|pause buttons still need the mouse on a pad (NOT_DONE)", t="S and B: pause, continue, quit on every device")
P("6.5", "Teaching the player", "Hints on first need or hesitation, each once; the interface appears piece by piece.", std="ER-FIRST-03: never two hints within 12 s; never on the clock", ss="DESIGN §15", des="DESIGN §15 Teaching", tr="both", f=1, o="lane",
  h="1|16|guess", rk="medium|onboarding is a top punished theme when slow (PLAYERS punish 4)", t="S: idle test")
P("6.6", "Controls", "Keyboard with mouse and a pad each drive everything; rebinding.", std="ER-INPUT-03; ER-INPUT-01", ss="DESIGN §17", des="DESIGN §17", tr="both", f=1, o="lane", n=["8.4"],
  h="1|16|guess", rk="medium|pad cannot type in talk; pause needs mouse (NOT_DONE)", t="S: the same scripted evening by each device")
P("6.7", "Talk screen", "Typing, suggested lines, the game's own decision lines, Leave always there.", std="ER-TALK-03, 05, 06", ss="DESIGN §11", des="DESIGN §11", tr="both", f=1, o="lane", n=[],
  h="1|16|guess", rk="low|", t="S: typing never moves Tom; Leave always offered")
P("6.8", "Photo mode", "Optional presentation: a free camera to take pictures, off the play path.", std="Optional presentation allowed (ruling 23 Sep floor)", ss="ruling 23 Sep genre line", des="not designed", tr="unreal", f=1, o="builder", n=["5.8.1"],
  h="0|16|guess", rk="low|optional; never before the verbs", t="S: opens, hides the screen, returns to play")

# ---------------- GROUP 7 ----------------
P("7", "The game's shape", "Pacing and structure: a minute, an evening, a week, three acts.", tr="both", o="lane", f=1,
  std="ER-CORE-05 to 07; ER-TENS-01, 02; panel M1 to M5", ss="DESIGN §1, §3; BUILD-ORDER measures", des="DESIGN §1, §3, §15, §16")
P("7.1", "The first hour", "Minute by minute: control at 0:20, first fare 2:30, a choice and a deed at 5:30, the carry, the morning after.",
  std="ER-FIRST-01 to 04: control within 1.5 min, a verb within 3, a choice within 20; town visibly knows him by minute 30 (Meridian Test)", ss="DESIGN §15; Study 2 (leads); canon targets", des="DESIGN §15 (restaging, QUESTIONS 4 open)", tr="both", f=1, o="lane", n=["3.1.1", "6.5"],
  h="3|40|guess", rk="high|round 5: first verb at 4.1 min, the impatient player quit at 3 (status-prototype)", t="H: first-hour run timed; S: control timing")
P("7.2", "An evening", "One game day: an easy day, a tightening dusk, the job, getting home, the count, the sting next morning.",
  std="M1 4 of 8 on the evening run; 16 to 20 real minutes a game day", ss="BUILD-ORDER M1; DESIGN §1", des="DESIGN §1, §3", tr="both", f=1, o="lane", n=["7.6", "2.9.1"],
  h="4|20|guess", rk="high|stage A's whole goal", t="H: the evening run and the panel")
P("7.3", "A week", "Act I, Monday to Sunday, about two hours.", std="M1 5 of 8 on the week run", ss="BUILD-ORDER", des="DESIGN §16", tr="both", f=1, o="lane", n=["3.1.1"],
  h="6|40|guess", rk="high|", t="H: the week run and the panel")
P("7.4", "Acts II and III pacing", "State-fired beats across seven weeks, then the inspection week.", std="Beats fire on states, never on days (DESIGN §16)", ss="DESIGN §16", des="DESIGN §16", tr="both", f=1, o="town", n=["3.1.2", "3.1.3"],
  h="4|40|guess", rk="high|no measured pacing for a 15 to 20 hour arc", t="H: sampled stretches; S: no dead weeks")
P("7.5", "The hour budget", "How play time is shared: on foot, driving, talk, jobs, fights and chases, the Ledger, waiting.",
  std="DESIGN table (on foot 25%, driving 22%, talk 19%, jobs 17%, fights and chases 8%, Ledger 6%, waiting 3%) rests on judgement; to be measured from timed one-hour stretches of reference games", ss="DESIGN §1 (judgement); his question 20:29 (advisor 257)", des="DESIGN §1", tr="both", f=1, o="lane", n=["9.9"],
  h="1|0|guess", rk="high|the shares are not measured (his point, advisor 257)", rn=["RN-14"], t="H: play time booked by activity against the measured shares")
P("7.6", "Tension and retellable moments", "Nine sources of tension; a retellable moment each evening.",
  std="ER-TENS-01: at least 12 tense moments per 30 min from at least four sources, none over half; ER-TENS-02", ss="DESIGN §3", des="DESIGN §3", tr="both", f=1, o="lane",
  h="1|0|guess", rk="high|round 5: three quarters of tense moments one kind", t="H: tense log; panel 'most exciting moment'")
P("7.7", "Rising in position, felt", "What a newcomer can point to at each rung: the name, greetings, property, clothes, access, the fleet.",
  std="ER-RISE-01 to 03: no number on screen; each rung changes three things a newcomer can point to", ss="DESIGN §14", des="DESIGN §14", tr="both", f=1, o="lane", n=["2.12.2"],
  h="2|40|guess", rk="medium|", t="H: same street at rung 1 and 3")
P("7.8", "Saving", "An autosave after every deed, consequence and job step; reloading never stopped.",
  std="ER-SAVE-01: a reload gives the same next hour; held during a fight, never refused", ss="DESIGN §17; D35, D58", des="DESIGN §17", tr="both", f=1, o="lane", n=["8.2"],
  h="1|24|guess", rk="medium|manual saving open (map-players A8)", t="S: reload at random moments; SaveChaos")
P("7.9", "Failure without reload", "Beaten, arrested, refused, late: each ends in a state the town can talk about.",
  std="ER-CORE-04: no game-over screen; control back within 2 real minutes", ss="DESIGN §1", des="DESIGN §1, §4, §7, §8", tr="both", f=1, o="lane",
  h="1|16|guess", rk="low|", t="S: every failure route timed")
P("7.10", "Difficulty as assists", "No stats, no difficulty ladder: assists only (seeing assist, hints, aim of driving help).",
  std="D11: difficulty only as assists", ss="D11; RULINGS What the game is", des="DESIGN-ADDENDUM §A6", tr="both", f=1, o="lane", n=["1.4.6", "8.4"],
  h="1|16|guess", rk="medium|PLAYERS punish 12: too hard early; assists not listed before the addendum", t="S: each assist changes only its own thing; H: an impatient player finishes the first hour with assists on")
P("7.11", "Waiting and time skips", "'Wait until' each known appointment; sleep as a skip; a wait stops for what the town has for him.",
  std="ER-JOB-04; never force waiting (Study 17)", ss="DESIGN §4, §6", des="DESIGN §6; waiting design 29 Sep", tr="both", f=1, o="lane",
  h="1|8|guess", rk="medium|waiting 41% in round 5", t="S: the week of waits")
P("7.12", "Always something to do", "By day, with no job live, a fare, a debt or a person with a word for him within 30 real seconds.",
  std="ER-CORE-07; ER-CORE-05 (never more than 5 minutes with nothing new)", ss="DESIGN §1", des="DESIGN §1", tr="both", f=1, o="lane", n=["3.4.1", "3.3"],
  h="2|0|guess", rk="high|longest empty stretch 10.8 min in round 5", t="S: idle probe at 20 daytime moments; H empty minutes")
P("7.13", "The game clock", "How fast a game hour passes in real time.", std="45 real s a game hour in DESIGN (his feel decision still open, C11); the code runs 30", ss="DESIGN §15; C11 on his page", des="DESIGN §15", tr="both", f=1, o="lane", n=["9.6"],
  h="0.5|4|guess", rk="medium|DESIGN and code disagree (status-unreal note)", t="S: one value in the tuning table, read by both")
P("7.14", "Variety", "No set piece twice in 30 minutes; no fare wrinkle twice running.", std="ER-JOB-06", ss="DESIGN §4", des="DESIGN §4", tr="both", f=1, o="lane", n=["3.4.2"],
  h="1|8|guess", rk="medium|nothing measures it yet (status-prototype)", t="H: the log")
P("7.15", "After the ending", "What happens when the story ends: the close, credits, and whether play continues.", std="Optional presentation after the ending (ruling 23 Sep floor)", ss="ruling 23 Sep", des="DESIGN-ADDENDUM §A7", tr="both", f=1, o="lane", n=["3.1.4", "10.4"],
  h="0.5|8|guess", rk="low|", t="S: the close plays, credits roll, the player returns to a stated place")
