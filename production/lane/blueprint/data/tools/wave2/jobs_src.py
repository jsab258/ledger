"""Authored jobs for blueprint data file 11 (jobs/). Written 24 Nov 2026 by the data-build wave 2 job.
Structure only, with the words the blueprint, the frame or the prototype already give; every other line is TO WRITE.
Each step: (id, at: a places.json or rooms.json id, verb, [three keys], fail: next step id or None, words)."""
TW = "TO WRITE (story lane)"
JOBS = []
def J(id, kind, giver, act, rung, name, offer, steps, pay, ledger, src, returns, when=None, window=None, people=None):
    JOBS.append(dict(id=id, kind=kind, giver=giver, act_min=act, rung_min=rung, name=name, offer=offer, steps=steps, pay=pay,
                     ledger=ledger, src=src, returns=returns, when=when, window=window, people=people or []))
def S(id, at, verb, keys, fail=None, words=TW):
    return dict(id=id, at=at, verb=verb, keys=keys, fail=fail, words=words)

# ---------------- Act I: the carry and the five debts
J("envelope_landing", "carry", "ron_kirby", 1, 1, "Mickey's arrangement: the envelope to the landing",
  ["Aye. Well. Envelope still wants carrying."],
  [S("take", "mickeys_office", "take the envelope", ["from Ron's hand", "from the hook by the dark coat", "send it back with Ron"], None, "Ron: Mickey's arrangement, down to the ferry landing after ten."),
   S("go", "ferry_landing", "carry it to the landing, 22:00 to 01:00", ["the lit quay (quick, seen)", "the yards' lane behind the warehouses, slow in the dark (footsteps carry half as far)", "the cab (quickest; anyone who sees it names the car)"], "searched", "At the landing a man says 'Mickey's?'"),
   S("cut", "ferry_landing", "take the cut back for the tin", ["hand it over and take the cut", "open it first (a carbon of the night's fare sheet)", "keep it and walk"], None, TW),
   S("searched", "ferry_landing", "stopped by the beat constable", ["stand and be searched (the constable keeps the envelope; the ask goes on as a state)", "run (a chase with no timer)", "talk (the claim check)"], None, TW)],
  {"to": "tin", "pence": 2000, "note": "economy: Frank's cut a run, nights one, three, five and seven of Act I"},
  "An envelope to the landing, for Mickey's arrangement.", "BLUEPRINT-03 3.5.1; STORY-FRAME 1 and 2 (the envelope holds a carbon of the night's fare sheet, decision of 24 Nov); economy 2.9.1",
  "the line in the book next morning (Sheila); Ron's look", when="night one after 22:00; asks on nights 1, 3, 5, 7", window=["22:00", "01:00"], people=["ron_kirby", "old_firm_man", "pc_haigh"])
DEBTS = [
    ("debt_darren", "darren_milner", 2200, "pays in what he hears", ["front him up at the rank", "take what he hears instead", "strike the debt out"], "rank_mickeys"),
    ("debt_wayne", "wayne_harrison", 3000, "pays in goods from the pawn's back room, haggled", ["haggle for goods in Rita's back room", "front him up on the step", "send Ron"], "ritas_back_room"),
    ("debt_lee", "lee_drewery", 1500, "stands, with the docks behind him, and it comes to blows", ["fists on the quay (a brawler)", "claim car three and win him (STORY-FRAME 7)", "let Ron fill the doorway"], "fish_dock"),
    ("debt_julie", "julie_kettlewell", 900, "cannot pay: mercy or shame", ["strike it out (mercy)", "take what she has (shame, told on the street)", "give her work (the night desk later)"], "home_cl_9"),
    ("debt_iveson", "dennis_iveson", 8000, "has the money, a yard and a yard hand; three keys", ["front up the yard hand, Neil Screeton", "the hut at night (break in for the tin box)", "lean on what he bought out of the burned warehouse"], "iveson_hut"),
]
for id, who, pence, lesson, keys, at in DEBTS:
    J(id, "collection", "sheila_dunn", 1, 1, "Mickey's debt book: %s, %d pounds" % (who.split('_')[0].capitalize(), pence // 100),
      ["Mickey's debt book, the page for %s." % who.split('_')[0].capitalize()],
      [S("find", at, "find the debtor where his routine has him", ["the routine (routines.json)", "ask Ron", "ask the caff"], None, TW),
       S("collect", at, "collect: " + lesson, keys, None, TW)],
      {"to": "tin", "pence": pence, "note": "a debtor pays only what his purse holds; the rest stays on the book (3.5.2)"},
      TW, "BLUEPRINT-02 2.8.1; BLUEPRINT-03 3.5.2; STORY-FRAME 7 (worked examples 1 and 2)", "squeezing or letting a debt go is told on the street within a game day",
      people=[who] + (["neil_screeton", "norman_dent"] if who == "dennis_iveson" else []))
J("car_three", "lift", "danny_cammack", 1, 1, "Car three: Danny's car across Mickey's rank",
  [], [S("move", "rank_mickeys", "drive Danny's car off the rank (the keys are in it)", ["round the corner", "to the quay's edge, front wheels over the water", "into the water"], None, "It's on my rank, so it's on my board. Car three. Two pound forty to the quay. Sheila, put it in the book."),
       S("board", "mickeys_office", "hang the keys on Mickey's board and chalk CAR 3", ["chalk it", "leave the keys with Sheila", "give them back to Danny"], None, TW)],
  {"to": "book", "pence": 240, "note": "two pound forty to the quay; Sheila asks whether Mr Cammack wants a receipt"},
  "Car three.", "STORY-FRAME 3 (the one deed only Frank would do) and 5 Act I (Danny's noticed rung)", "Ada and Shaun saw it; by noon Brenda has it whole (STORY-FRAME 7 worked example 1)",
  people=["danny_cammack", "ron_kirby", "shane_boddy", "wes_akers"])

# ---------------- Act I to II: the prototype's jobs (jobsx.js), on the new map
J("ivesons_hut", "break_in", "darren_milner", 1, 1, "Iveson's hut",
  ["Iveson keeps it in a tin box in the hut. The lad chains the gap at five. Not that I'm telling you anything."],
  [S("in", "iveson_hut", "get into the hut", ["the back way before five (the crane gap)", "a key (talk)", "force"], None, "Got into Iveson's hut."),
   S("box", "iveson_hut", "the tin box under the bench", ["open it", "take it whole", "leave it and look"], None, "The tin box: eighty pounds.")],
  {"to": "pocket", "pence": 8000}, "Darren's tip: Iveson's tin box, in the hut at the scrap yard.", "prototype jobsx.js hut; 2.8.1 (Iveson's three keys)",
  "Norman Dent has a noise and a shape (STORY-FRAME 7 worked example 2)", people=["dennis_iveson", "neil_screeton", "norman_dent"])
J("ritas_back_room", "break_in", "wayne_harrison", 1, 1, "Rita's back room",
  ["There's a clock on the back shelf she has not written down. Side door is on the latch till six. We split it."],
  [S("in", "ritas_back_room", "in at the side door", ["the side door before six", "a key from Wayne (talk)", "force"], None, "In at Rita's side door."),
   S("clock", "ritas_back_room", "the carriage clock off the back shelf", ["take it", "take it and something else", "leave it"], None, "The carriage clock, off the back shelf.")],
  {"to": "pocket", "band": "fence at a third of retail (economy 2.7.6), split with Wayne"}, "Wayne's offer: the clock off Rita's back shelf, and a split.", "prototype jobsx.js ritaback",
  "Rita never forgets her own goods", people=["wayne_harrison", "rita_welburn"])
J("tail_coverdale", "tail", "sheila_dunn", 2, 2, "Where Miss Coverdale goes",
  ["Somebody at the Harbour Office is writing letters about our licence. I would like to know who she takes them to."],
  [S("follow", "customs", "follow her from the customs house at half past four", ["on foot", "by cab", "send Darren"], None, "Followed Susan Coverdale to the solicitor's door: Agar's.")],
  {"to": None, "note": "a hook: Susan is Agar's eyes (2.10.2)"}, "Sheila wants to know who Susan Coverdale takes her letters to.", "prototype jobsx.js tail_susan; 2.10.2; 3.5.4",
  "Susan looks back every 20 to 40 s; a face she knows ends the tail", people=["susan_coverdale", "geoffrey_agar"])
J("mind_julie", "minding", "julie_kettlewell", 1, 1, "Standing at Julie Kettlewell's door",
  ["The rent man comes at six and he does not come alone. Would you just stand there. You need not say anything."],
  [S("stand", "home_cl_9", "stand at her door while the rent man comes", ["stand at her door", "sit in the cab outside", "send Ron"], None, "Stood at Julie Kettlewell's door while the rent man came and went. He looked, and said nothing.")],
  {"to": "none", "note": "the town records who stood with whom"}, "Julie Kettlewell wants somebody stood at her door at six, when the rent man comes.", "prototype jobsx.js mind_julie; 3.5.4",
  "Julie's need met: a need recruit (2.11.1)", window=["17:30", "20:00"], people=["julie_kettlewell", "leonard_askew"])
J("mind_boxing", "minding", "ron_kirby", 2, 2, "The door at the boxing club",
  ["The club's got a show on Saturday. They want a face on the door who is not from the docks."],
  [S("stand", "boxing_club", "stand the door on show night", ["stand on the door", "send Ron", "stand with Ron"], None, "Stood the door at the boxing club. People saw who stood there.")],
  {"to": "pocket", "band": "minding pay set by the job (3.5.4)"}, "Ron: the boxing club wants a face on the door on Saturday.", "prototype jobsx.js mind_ron",
  "men who train there can be recruited (2.11.1)", window=["17:00", "22:00"], people=["ron_kirby", "sid_bulmer"])
J("lift_medals", "lift", "wayne_harrison", 2, 2, "The tray in Metcalfe's window",
  ["Metcalfe leaves a tray of medals in the window overnight. Rita would take them, if she did not know whose they were."],
  [S("take", "metcalfes_shop", "the tray of medals", ["the window, at night", "the back door in the alley", "a lift in the day while Hal is at Rita's (Monday 11:00)"], None, "Put Metcalfe's window in and took the tray of medals. Hal Metcalfe never forgets his own goods.")],
  {"to": "pocket", "band": "fence at a third of retail; honest value 90 pounds"}, "Wayne says Metcalfe leaves a tray of medals in his window overnight.", "prototype jobsx.js lift_coin; 1.6.3",
  "Hal never forgets his own goods; the buy-back within 7 game days", people=["wayne_harrison", "hal_metcalfe"])
J("word_to_portside", "send", "ron_kirby", 2, 2, "A word to Portside Cars",
  ["Portside are sat on the north rank taking our fares. One windscreen, at night, and they will read it right."],
  [S("do", "rank_north", "one Portside windscreen, at night", ["by hand, at night", "send a man (hit a rival's property)", "a word with Len Ackroyd instead"], None, "Put a Portside windscreen in on the north rank. Len Ackroyd will know who by morning.")],
  {"to": "none"}, "Ron: one Portside windscreen, at night, as a message.", "prototype jobsx.js damage_portside; 1.6.14; 2.15.3 (a business, never a rival)",
  "Len Ackroyd knows who by morning", people=["ron_kirby", "len_ackroyd"])

# ---------------- Act IIa: the rise (STORY-FRAME 5)
J("ferry_rank", "minding", "ron_kirby", 2, 2, "The ferry rank",
  [TW], [S("hold", "rank_ferry", "a car on the ferry rank five days in a fortnight", ["stand it, back to back with Ron before the boat queue", "a word with whoever holds it (Craig Fewson)", "fists in front of the boat queue"], None, TW)],
  {"to": "book", "note": "a good rank: 210 pounds a car a week (economy)"}, TW, "STORY-FRAME 5 Act IIa; 2.15", "Mark Billany down in front of the queue returns at the Landing (STORY-FRAME 7 worked example 3)",
  people=["ron_kirby", "craig_fewson", "mark_billany"])
J("five_mornings", "carry", "eric_tharratt", 2, 2, "The packing shift: five mornings",
  ["Eric Tharratt, cold stores. The packing shift met on time, five mornings running. Then he'll talk."],
  [S("convoy", "cold_stores", "four cars meet the packing shift on time, before six", ["through the dock gate (pay, bluff or push the Widow's men)", "round by Agar's cold-store road and the fish dock in the dark", "the fifth car is Frank's own"], "late", TW),
   S("late", "dock_gate", "the gate swinging shut on every car he has", ["pay the tax", "bluff", "push"], None, TW)],
  {"to": "book", "pence_per_week": 4000, "note": "the contract: 40 pounds more a car a week (economy); won on five on-time mornings in one game week; lost after three missed in a week; won again once (places.json accounts)"},
  "Eric Tharratt, cold stores. The packing shift met on time, five mornings running. Then he'll talk.", "STORY-FRAME 5 Act IIa (the contract); 2.15.2; places.json accounts", "the fifth morning, the gate swinging shut",
  window=["05:00", "06:00"], people=["eric_tharratt", "stathers", "kevin_needham", "terry_hodgson"])
J("rita_back_room_front", "send", "rita_welburn", 2, 2, "The back room, the first front",
  [TW], [S("terms", "ritas_back_room", "terms for the back room as the firm's first front", ["pay Wayne's debt into it", "lean on Rita with what Hal knows", "buy in clean"], None, TW)],
  {"to": "tin", "band": "a front washes 60 pounds a week (economy, places.json fronts)"}, TW, "STORY-FRAME 4 item 13 (new: The back room, the first front)", "Danny hears his fence has a partner",
  people=["rita_welburn", "wayne_harrison"])
J("fifteen_pounds", "collection", "lee_drewery", 1, 1, "Fifteen pounds",
  [TW], [S("stand", "fish_dock", "Lee stands for his fifteen pounds", ["fists", "claim car three to his face", "pay his debt off with work at a post"], None, TW)],
  {"to": "tin", "pence": 1500}, TW, "STORY-FRAME 4 item 5 (new: Fifteen pounds, which can make him the first man at a post)", "Lee as the first man at a post", people=["lee_drewery"])

# ---------------- The midpoint
J("the_landing", "break_in", "ron_kirby", 2, 3, "The Landing",
  [TW],
  [S("look", "ferry_landing", "a day of looking", ["from the tea stall", "from the snooker hall window", "Karen Grummitt's ticket window"], None, TW),
   S("in", "widow_net_store", "the Widow's weekly load off the last boat (boxed goods and tobacco)", ["the road: the van, driven by a man he has met", "the gate: in with the contract cars at shift change, to the net store under her office", "the boat: on the stage as she ties up"], "wrong", TW),
   S("wrong", "ferry_landing", "one thing always goes wrong; the car brought round by a man with four lessons", ["Ron at the wheel", "Frank at the wheel", "on foot by the yards' lane"], None, TW),
   S("hold", "post_landing", "a man standing there in the morning", ["Ron", "a crewman with nerve", "Danny's man (if allied)"], None, TW)],
  {"to": "tin", "band": "the load: tobacco 100 pounds a case off the boat (economy EC-07); the landing's nights after"},
  TW, "STORY-FRAME 5 The midpoint; timetables bonfire_night_display (5 Nov, the display on the quay)", "Danny's name on the town's telling (STORY-FRAME 3)",
  when="Frank at the third rung, or any rival at threat, or end of game week four; never before the end of week three", people=["ron_kirby", "maureen_jensen", "pat_brannigan", "mark_billany", "danny_cammack"])

# ---------------- Act IIb: the three crises
J("crisis_landing", "tail", "maureen_jensen", 2, 3, "The landing, by night",
  [TW], [S("find", "ferry_landing", "his man has stopped answering; a load is due on the last boat", ["the tea stall", "Karen at the window", "the snooker hall"], None, TW),
         S("snatch", "ferry_landing", "Craig Fewson has him in a van: a tail and a snatch on the night quay", ["by the road", "by the water", "trade for him"], None, TW)],
  {"to": "none", "note": "the post held or lost"}, TW, "STORY-FRAME 5 Act IIb (crisis one); the danger: a gun shown", TW, people=["craig_fewson"])
J("crisis_cold_store", "break_in", "eric_tharratt", 2, 3, "The cold store, before dawn",
  [TW], [S("in", "cold_store_office", "men from away have shut the door man in a cold room and locked the shift out", ["Ian Megginson's locks", "a key bought from Malcolm Ruddock", "force, against the clock"], None, TW)],
  {"to": "none", "note": "the contract kept or lost"}, TW, "STORY-FRAME 5 Act IIb (crisis two)", TW, window=["04:00", "06:00"], people=["barry_coult", "ray_spink", "kenny_varley", "malcolm_ruddock", "ian_megginson"])
J("crisis_dock_gate", "minding", "ron_kirby", 2, 3, "The dock gate, by day",
  [TW], [S("go", "dock_gate", "Stathers's men have Ron cornered in front of the pen", ["go and fight beside him", "hold, send somebody", "hear about it"], None, TW)],
  {"to": "none"}, TW, "STORY-FRAME 5 Act IIb (crisis three); one of the five heaviest scenes", TW, people=["ron_kirby", "stathers", "mark_billany"])
J("clear_the_office", "carry", "sheila_dunn", 2, 3, "Clearing the office the night before the search",
  [TW], [S("clear", "mickeys_office", "one night to clear the office by the yard's two ways; the day book has to stay", ["the yard gate to the quay", "the back fence into the yards' lane (the vault)", "Ron carries it"], None, TW)],
  {"to": "none"}, TW, "STORY-FRAME 5 Act IIb (the turn)", TW, people=["sheila_dunn", "ron_kirby"])

# ---------------- sit-downs (the act's end, 2.10.1) and the Fixer
for rival, place, lt in [("maureen_jensen", "widow_dock_office", "stathers"), ("geoffrey_agar", "agar_back_room", "simon_ombler"), ("danny_cammack", "cammack_lockup", "craig_fewson")]:
    J("sit_down_" + rival.split('_')[1], "sit_down", rival, 2, 2, "The sit-down: " + rival.replace('_', ' ').title(),
      [TW], [S("sit", place, "the sit-down: accept, defy, or counter with what he knows", ["accept the terms", "defy", "counter with a hook he holds"], None, TW)],
      {"to": "none", "note": "the act closes on it; Frank goes in hurt"}, TW, "2.10.1; STORY-FRAME 5 Act IIb (the sit-down)", "the rival's ladder and pact", people=[rival, lt])
J("garbutt_meeting", "sit_down", "keith_garbutt", 2, 2, "A meeting the Fixer brokers",
  [TW], [S("page", "phone_parade", "page Garbutt from a box; he rings that box back within half a game hour", ["the parade's box", "the landing's box", "the dock gate's box"], None, TW),
         S("meet", "snooker_hall", "a true read, a meeting, or the one truce a game", ["a read", "a meeting", "the truce"], None, TW)],
  {"to": "garbutt", "band": "his prices follow the economy curve (2.10.4)"}, TW, "2.10.4", TW, people=["keith_garbutt"])

# ---------------- RT-03: the dock gate, the Harbour Board, customs
J("gate_tax_receipt", "collection", "kevin_needham", 2, 2, "The receipt at the gate",
  [TW], [S("pay", "dock_gate", "the Widow's men tax Kevin at the gate", ["pay, and ask for a receipt in front of the pen", "defy", "counter"], None, TW)],
  {"to": "widow", "band": "the gate tax (economy)"}, TW, "STORY-FRAME 5 Act I (a receipt in her own hand, made out to Mr Nowack); RT-03 dock gate", "the fourth morning of Act III (M. Jensen on the receipt)",
  people=["kevin_needham", "mark_billany", "maureen_jensen"])
J("post_dock_gate", "minding", "stathers", 3, 4, "A man at the dock gate",
  [TW], [S("post", "post_dock_gate", "a man of his posted at the gate, 06:00 to 22:00", ["a need recruit", "a hook recruit", "a man won from the pen at six"], None, TW)],
  {"to": "man", "pence_per_week": 4000, "note": "rung 4 posts: 40 pounds a week each from cash (economy)"}, TW, "RT-03 dock gate; RT2-09 (posts held by their men, never by Frank: STORY-FRAME 5)", TW, people=["stathers"])
J("loads_seen", "tail", "lee_drewery", 2, 3, "Smuggled loads seen",
  [TW], [S("watch", "dock_gate", "watch what comes through the gate at night", ["from the phone box", "Lee's word", "Paddy Rourke's count"], None, TW)],
  {"to": "none", "note": "a hook on the Widow"}, TW, "RT-03 dock gate (smuggled loads seen)", TW, people=["lee_drewery", "paddy_rourke"])
J("board_account", "carry", "christine_pickering", 3, 3, "An account at the Harbour Board",
  [TW], [S("counter", "harbour_board_counter", "open an account at the counter (the decent jacket)", ["the decent jacket", "an introduction", "an appointment the Fixer brokers"], None, TW)],
  {"to": "book", "band": "account work (economy)"}, TW, "RT-03 Harbour Board; 2.12.3 (soft keys)", TW, people=["christine_pickering"])
J("shipment_times", "collection", "rodney_usher", 3, 3, "The times of shipments",
  [TW], [S("buy", "snooker_hall", "a clerk who sells the times of shipments", ["pay", "lean on him", "trade a hook"], None, TW)],
  {"to": "usher", "band": "a few pounds a time (judgement)"}, TW, "RT-03 Harbour Board (a clerk who sells times of shipments)", TW, people=["rodney_usher"])
J("officer_trade", "sit_down", "douglas_fenwick", 3, 3, "The officer who never reports",
  [TW], [S("trade", "customs", "an officer who never reports, by trade", ["a trade of favours", "money", "a hook"], None, TW)],
  {"to": "fenwick", "band": "by trade (economy)"}, TW, "RT-03 customs", TW, people=["douglas_fenwick"])
J("bonded_store", "break_in", "paddy_rourke", 3, 3, "The bonded store",
  [TW], [S("in", "customs", "the bonded store: tobacco and boxed goods, never drink", ["Paddy's count and a night", "Fenwick looks away", "force (a place of risk)"], None, TW)],
  {"to": "tin", "band": "tobacco 100 pounds a case (economy EC-07)"}, TW, "RT-03 customs (the bonded store)", TW, people=["paddy_rourke", "douglas_fenwick"])

# ---------------- Act III: the five mornings, each fetched by play
J("item_wages", "collection", "derek_hebblewhite", 3, 1, "The wages: a man paid off the book",
  [TW], [S("find", "home_nr_12", "find him at his own door and bring him in, or keep him away", ["his need", "a hook", "Ron at the door"], None, TW)],
  {"to": "none"}, TW, "STORY-FRAME 5 Act III item 1", TW)
J("item_car_records", "tail", "derek_hebblewhite", 3, 1, "The cars' records: Kevin and car one's log",
  [TW], [S("chase", "rank_north", "Kevin has gone with car one's log and its missing miles", ["a chase across the Hook", "his price", "Pauline's radio"], None, TW)],
  {"to": "none"}, TW, "STORY-FRAME 5 Act III item 2; side story 1 (The long way round)", TW, people=["kevin_needham"])
J("item_invoice", "break_in", "derek_hebblewhite", 3, 1, "An invoice: the cold-store book in Agar's office",
  [TW], [S("in", "agar_back_room", "the cold-store book", ["a break-in by night", "a word with Simon Ombler", "Ian's locks"], None, TW)],
  {"to": "none"}, TW, "STORY-FRAME 5 Act III item 3", TW, window=["21:00", "05:00"], people=["simon_ombler"])
J("item_gate", "carry", "derek_hebblewhite", 3, 1, "The gate: the Widow in the back of his cab",
  [TW], [S("drive", "dock_gate", "a drive to the gate, the Widow in the back, and her price for signing", ["pay her price", "the landing (her price if allied)", "the receipt she wrote"], None, TW)],
  {"to": "none"}, TW, "STORY-FRAME 5 Act III item 4", TW, people=["maureen_jensen"])
J("the_quay", "sit_down", "danny_cammack", 3, 1, "The quay at four: the day book",
  [TW], [S("fight", "fishing_quay_east", "Danny in Mickey's own car on the quay's edge with the day book", ["fists (unless the dial stands at Fired or War)", "talk", "the car itself"], None, TW)],
  {"to": "none", "note": "lose and the choice is made for him (a new input to the ending rule)"}, TW, "STORY-FRAME 5 Act III (the last day)", "the counter at five",
  window=["16:00", "17:00"], people=["danny_cammack"])

# ---------------- the eight sent verbs (1.7.2), one authored example each
SENDS = [("hurt", "craig_fewson", "cammack_base"), ("plan", "mark_billany", "widow_base"), ("frame", "wes_akers", "net_loft"),
         ("lean_on_witness", "norman_dent", "dents_warehouses"), ("move_body", "pat_brannigan", "fishing_quay_west"),
         ("dock_own_man", "kevin_needham", "rank_mickeys"), ("hit_property", "danny_cammack", "cammack_base"), ("vouch", "lee_drewery", "dock_gate")]
for verb, target, at in SENDS:
    J("send_" + verb, "send", "frank_nowak", 2, 2, "Send: " + verb.replace('_', ' '),
      [], [S("send", at, verb.replace('_', ' ') + " (through a named man; the man's nerve against the target's)", ["the board's line", "a word in talk", "the night his routine allows"], None, TW)],
      {"to": "man", "band": "set by the job"}, TW, "BLUEPRINT-01 1.7.2 and RT-08 (the eight verbs); an example target, not a script",
      "Frank learns the morning after from the man's own line; the town can trace the chain", people=[target])
