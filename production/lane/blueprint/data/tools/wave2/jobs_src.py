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
  [S("do", "rank_north", "one Portside windscreen, at night", ["by hand, at night", "send a man (hit a rival's property)", "a word with Clive Ackroyd instead"], None, "Put a Portside windscreen in on the north rank. Clive Ackroyd will know who by morning.")],
  {"to": "none"}, "Ron: one Portside windscreen, at night, as a message.", "prototype jobsx.js damage_portside; 1.6.14; 2.15.3 (a business, never a rival)",
  "Clive Ackroyd knows who by morning", people=["ron_kirby", "clive_ackroyd"])

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
  when="Frank at the third rung, or any rival at threat, or end of game week four; never before the end of week three", people=["ron_kirby", "maureen_jensen", "steve_brannigan", "mark_billany", "danny_cammack"])

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
  [TW], [S("watch", "dock_gate", "watch what comes through the gate at night", ["from the phone box", "Lee's word", "Kieran Rourke's count"], None, TW)],
  {"to": "none", "note": "a hook on the Widow"}, TW, "RT-03 dock gate (smuggled loads seen)", TW, people=["lee_drewery", "kieran_rourke"])
J("board_account", "carry", "christine_pickering", 3, 3, "An account at the Harbour Board",
  [TW], [S("counter", "harbour_board_counter", "open an account at the counter (the decent jacket)", ["the decent jacket", "an introduction", "an appointment the Fixer brokers"], None, TW)],
  {"to": "book", "band": "account work (economy)"}, TW, "RT-03 Harbour Board; 2.12.3 (soft keys)", TW, people=["christine_pickering"])
J("shipment_times", "collection", "rodney_usher", 3, 3, "The times of shipments",
  [TW], [S("buy", "snooker_hall", "a clerk who sells the times of shipments", ["pay", "lean on him", "trade a hook"], None, TW)],
  {"to": "usher", "band": "a few pounds a time (judgement)"}, TW, "RT-03 Harbour Board (a clerk who sells times of shipments)", TW, people=["rodney_usher"])
J("officer_trade", "sit_down", "douglas_fenwick", 3, 3, "The officer who never reports",
  [TW], [S("trade", "customs", "an officer who never reports, by trade", ["a trade of favours", "money", "a hook"], None, TW)],
  {"to": "fenwick", "band": "by trade (economy)"}, TW, "RT-03 customs", TW, people=["douglas_fenwick"])
J("bonded_store", "break_in", "kieran_rourke", 3, 3, "The bonded store",
  [TW], [S("in", "customs", "the bonded store: tobacco and boxed goods, never drink", ["Kieran's count and a night", "Fenwick looks away", "force (a place of risk)"], None, TW)],
  {"to": "tin", "band": "tobacco 100 pounds a case (economy EC-07)"}, TW, "RT-03 customs (the bonded store)", TW, people=["kieran_rourke", "douglas_fenwick"])

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
         ("lean_on_witness", "norman_dent", "dents_warehouses"), ("move_body", "steve_brannigan", "fishing_quay_west"),
         ("dock_own_man", "kevin_needham", "rank_mickeys"), ("hit_property", "danny_cammack", "cammack_base"), ("vouch", "lee_drewery", "dock_gate")]
for verb, target, at in SENDS:
    J("send_" + verb, "send", "frank_nowak", 2, 2, "Send: " + verb.replace('_', ' '),
      [], [S("send", at, verb.replace('_', ' ') + " (through a named man; the man's nerve against the target's)", ["the board's line", "a word in talk", "the night his routine allows"], None, TW)],
      {"to": "man", "band": "set by the job"}, TW, "BLUEPRINT-01 1.7.2 and RT-08 (the eight verbs); an example target, not a script",
      "Frank learns the morning after from the man's own line; the town can trace the chain", people=[target])

# =================== fixes after the fresh review (wave2/REVIEW-jobs.md), 24 Nov 2026
_by = {j['id']: j for j in JOBS}
def _drop(i):
    JOBS.remove(_by.pop(i))
# duplicates: the hut is a key of debt_iveson; Lee's fifteen pounds is debt_lee; the first front stays a job
_drop("ivesons_hut"); _drop("fifteen_pounds")
d = _by["debt_iveson"]; d["offer"].append("Darren's tip (prototype jobsx.js hut): 'Iveson keeps it in a tin box in the hut. The lad chains the gap at five. Not that I'm telling you anything.'")
d["steps"][1]["keys"] = ["front up the yard hand, Neil Screeton (words with Dennis himself: Frank's line covers a man of 62)", "the hut at night for the tin box (the back way before five, or force)", "lean on what he bought out of the burned warehouse (words)"]
d["steps"].append(S("box", "iveson_hut", "the tin box under the bench: eighty pounds, the debt closed", ["open it", "take it whole", "leave it and look"], None, "The tin box: eighty pounds."))
_by["debt_lee"]["steps"][1]["keys"] = ["fists on the quay (a brawler)", "claim car three to his face, and win him: the first man at a post later (STORY-FRAME 4 item 5)", "let Ron fill the doorway"]
FIND = {"debt_darren": ("rank_mickeys", "12:30 to 13:30 and 16:00 to 19:00 at the rank (routines.json)"), "debt_wayne": ("ritas_back_room", "10:00 to 16:00 in Rita's back room"),
        "debt_lee": ("fish_dock", "08:00 to 12:00 at the fish dock, 12:00 to 15:00 on the rank's bollard"), "debt_julie": ("home_cl_9", "at home, 9 Chapel Lane, mornings and after 14:30"),
        "debt_iveson": ("iveson_yard", "07:30 to 17:15 in the yard; the hut at 12:00")}
PAYS = {"debt_darren": {"to": "tin", "pence": 0, "pays_in": "what he hears (a hook or a tip), never cash (ECONOMY 5.3)"},
        "debt_wayne": {"to": "pocket", "pence": 0, "pays_in": "goods from the pawn's back room to 30 pounds' value, haggled; sold on at a fence's third"},
        "debt_julie": {"to": "tin", "pence": 0, "pays_in": "nothing: she cannot pay; 'take what she has' is a few shillings and the street's shame"}}
for k, (at, hours) in FIND.items():
    j = _by[k]; j["steps"][0] = S("find", at, "find the debtor where the routine has him: " + hours, ["the routine (ask Ron where he'll be)", "wait for him there", "send Darren to fetch him"], None, TW)
    if k in PAYS:
        j["pay"] = PAYS[k]
# sends: templates, three ways of doing the deed, the target chosen from the Ledger, the covered never
for v, _, _ in SENDS:
    j = _by["send_" + v]
    j["people"] = []
    j["steps"] = [S("send", "rank_mickeys", v.replace('_', ' ') + ": given at the board or in talk; the named man does it on the next night his routine allows", ["at night, unseen, at the target's door or his road home", "in the open, as a message the street can read", "at the quietest hour of the target's routine (routines.json)"], None, TW)]
    j["target"] = "chosen from the Ledger (a person or place Frank knows); never Sheila, Pauline, Ada, June, Alison, Ellis, the Widow, Father Walsh or anyone 60 or over (RT2-05, RT-09): Frank refuses in his own words"
    j["man"] = "chosen: one of his men; resolved by the man's nerve against the target's, the watchers, the light and the noise, within two game nights (1.7.2)"
# the big jobs' keys and outcomes
c = _by["crisis_dock_gate"]; c["kind"] = "fight"; c["giver"] = "pauline_kitching"
c["offer"] = ["Pauline, on the radio: Ron's at the gate, and they've got him in front of the pen."]
c["steps"] = [S("go", "dock_gate", "Stathers's men have Ron cornered in front of the pen", ["go and fight beside him (one of the five heaviest scenes)", "send somebody with nerve and stay at the office", "stay away and hear it told"], None, TW)]
f = _by["five_mornings"]; f["window"] = ["04:00", "06:00"]
f["steps"] = [S("convoy", "cold_stores", "four cars meet the packing shift on time (by 06:00), five mornings in one game week", ["through the dock gate, paying the Widow's tax", "through the gate on a bluff or a push", "round by Agar's cold-store road and the fish dock in the dark"], None, TW)]
f["fail_rule"] = "no lateness fail inside the window (3.5.6); a morning missed counts; three missed in a week loses the contract; won again once"
f["pay"] = {"to": "book", "pence": 0, "pence_per_car_per_week": 4000, "note": "the contract: 40 pounds more a car a week (economy)"}
g = _by["item_gate"]; g["steps"][0]["keys"] = ["pay her price", "the receipt she wrote in week one, made out to Mr Nowack (if he asked for it)", "trade the landing (her price if allied)"]
L = _by["the_landing"]
L["by_path"] = {"widow_ally": "the load is Danny's, at his lock-ups' van", "alone": "the load of whichever rival reached threat", "wound_down": "done in the open, every car on the quay for the display, carrying the town home past her taxmen"}
L["steps"] = [S("look", "ferry_landing", "a day of looking", ["from the tea stall", "from the snooker hall window", "Karen Grummitt's ticket window"], None, TW),
              S("in", "ferry_landing", "the load off the last boat (boxed goods and tobacco, two to four cases)", ["the road: the van, driven by a man he has met (Mark Billany, if spared)", "the gate: in with the contract cars at shift change, to the net store under her office (widow_net_store)", "the boat: on the stage as she ties up"], "wrong", TW),
              S("wrong", "ferry_landing", "one thing always goes wrong: Frank is needed at the load, and the car has to be brought round", ["Ron brings it round at eleven miles an hour (four lessons)", "a crewman with nerve brings it", "on foot by the yards' lane with what they can carry"], None, TW),
              S("hold", "post_landing", "a man standing there in the morning", ["Ron", "a crewman with nerve", "Danny's man, if allied"], None, TW)]
L["people"] = ["ron_kirby", "maureen_jensen", "steve_brannigan", "mark_billany"]; L["people_note"] = "Danny only if allied (STORY-FRAME 5)"
L["pay"] = {"to": "tin", "pence": 0, "band": [20000, 40000], "note": "two to four cases at 100 pounds off the boat (EC-07); the take never over MP-02's cap (the greater of 150 pounds or 1.5 weeks' income): the excess is unsellable that week"}
q = _by["the_quay"]; q["kind"] = "fight"
q["steps"] = [S("fight", "fishing_quay_east", "Danny in Mickey's own car on the quay's edge with the day book", ["fists (Frank may have one good arm)", "talk him off the edge with what Frank knows", "block Mickey's car in with car three"], "lost", TW),
              S("won", "fishing_quay_east", "the book back and Danny at the edge", ["let him go on the morning boat", "put him back on the board under Frank", "keep him for Ellis"], None, TW),
              S("lost", "rank_mickeys", "the book goes where Danny takes it; the choice is made for him; car two back on the rank by morning, its keys on Mickey's board (RT2-06)", ["take it", "go to the counter at five with nothing", "send for Ellis"], None, TW)]
q["dial_rule"] = "if the dial stands at Fired or War, Danny shows a gun and the quay is talk only: no gunfight is built (for the story lane to confirm)"
for k in ("board_account", "bonded_store", "officer_trade", "shipment_times"):
    _by[k]["act_min"] = 2; _by[k]["rung_min"] = 3
_by["shipment_times"]["steps"][0]["at"] = "harbour_board_counter"
p = _by["post_dock_gate"]; p["giver"] = "ron_kirby"; p["act_min"] = 2; p["rung_min"] = 3
for post, at in (("post_cold_store", "post_cold_store"), ("post_landing", "post_landing")):
    J(post, "minding", "ron_kirby", 2, 3, "A man at the " + post.split('_', 1)[1].replace('_', ' '), [TW],
      [S("post", at, "a man of his posted, by his own nerve and loyalty; Frank never stands it himself", ["a need recruit", "a hook recruit", "a man won from the pen at six"], None, TW)],
      {"to": "tin", "pence": 0, "pence_per_week_paid": 4000}, TW, "RT2-09; STORY-FRAME 5 midpoint (posts after the Landing); economy 5.6 (40 pounds a week)", TW)
w = _by["item_wages"]; w["people"] = ["lee_drewery"]; w["people_note"] = "the man paid off the book: whoever Frank paid from the tin; Lee Drewery by default (home_nr_12 is his house)"
for n, k in enumerate(["item_wages", "item_car_records", "item_invoice", "item_gate"], 1):
    _by[k]["order"] = n
J("item_the_line", "sit_down", "derek_hebblewhite", 3, 1, "Week one: the line", [TW],
  [S("line", "mickeys_office", "the inspector asks for week one on the last morning; at five Sheila turns the book round and lays her pen on it", ["leave it as it stands", "write it true, in his own hand", "put Danny's name to it (Ellis's trade)"], None, TW)],
  {"to": "book", "pence": 0}, TW, "STORY-FRAME 5 The early deed (the last line) and Act III item 5", "the ending", people=["sheila_dunn", "carol_ellis"])
_by["item_the_line"] = JOBS[-1]; _by["item_the_line"]["order"] = 5
t = _by["tail_coverdale"]; t["steps"] = [S("follow", "bus_stop_qs", "follow her from the customs house at 17:15 on a Tuesday or Thursday to the bus and the solicitor's in town", ["on foot to the bus stop", "by cab behind the bus", "send Darren"], None, "Followed Susan Coverdale to the bus for town, with letters for the solicitor's: Agar's.")]
cl = _by["crisis_landing"]; cl["giver"] = "pauline_kitching"; cl["offer"] = ["Pauline, on the radio: the landing's not answering."]
cl["steps"][0]["keys"] = ["the tea stall (Maggie Firth saw the van)", "Karen at the ticket window", "the snooker hall's window"]
_by["gate_tax_receipt"]["pay"] = {"to": "book", "pence": 0, "cost_pence_per_car_per_week": 500, "note": "the Widow's tax from five cars (economy section 1)"}
# new main-line jobs the frame needs
J("danny_visit", "sit_down", "danny_cammack", 2, 2, "Danny's visit: car two, six minutes, the offer",
  ["That's how you park it."], [S("ride", "rank_mickeys", "Danny takes Mickey's own car off the rank on his old key, roof sign lit, and drives Frank the whole Hook in six minutes, pricing every door", ["ride with him", "follow in car three", "refuse to get in"], None, "That's how you park it."),
   S("offer", "fishing_quay_east", "his men, his car on the board and his nerve, for a share of the nights; he opens at half", ["take it, and say where his name is chalked", "refuse it", "keep him waiting"], None, TW)],
  {"to": "book", "pence": 0}, TW, "STORY-FRAME 3 (Danny's deed) and 5 Act IIa (Danny's visit)", "the pact or the wall", people=["danny_cammack"])
J("ron_lessons", "carry", "ron_kirby", 2, 2, "Ron's lessons: one to five",
  [TW], [S("lesson_%d" % i, at, verb, keys, None, TW) for i, (at, verb, keys) in enumerate([
      ("rank_mickeys", "lesson one, the dock road: Ron drives; Frank has the handbrake and one word, 'Stop'", ["say stop", "pull the handbrake", "let him go"]),
      ("dock_gate", "lesson two: the gate road", ["the quay road", "Cold Store Road", "the cut"]),
      ("fishing_quay_west", "lesson three: reversing on the quay ('Going astern')", ["coach him", "take the wheel", "let him hit the bollard"]),
      ("cold_stores", "lesson four: the convoy pace, so a man with four lessons can bring a car round", ["the dawn convoy", "the empty road at night", "the yard"]),
      ("rank_mickeys", "lesson five: he stops the car properly for once and asks what is in the book (the breach: Frank answers, true or false)", ["the truth", "a lie", "say nothing"])], 1)],
  {"to": "book", "pence": 0}, TW, "STORY-FRAME 3 (the bond, weeks 2 to 5); lesson five gates the turn; the Landing's getaway needs four", "Ron's loyalty and the breach", people=["ron_kirby"])
J("sheila_trust", "sit_down", "sheila_dunn", 2, 2, "Mickey's locked office",
  [TW], [S("open", "mickeys_inner_office", "Sheila's trust: the key to Mickey's locked office", ["earn it: a clean week in the book", "ask her straight", "force the door (she never trusts him after)"], None, TW),
         S("book", "mickeys_inner_office", "the real book (at least five new names), the page about the fire, and the revolver under it, which Ron puts back", ["read it all", "read the page and leave the rest", "leave the revolver where it lies"], None, TW)],
  {"to": "book", "pence": 0}, TW, "STORY-FRAME 5 Act IIa (Sheila's trust); BLUEPRINT-07 7.4 (the real book)", "the fire thread", people=["sheila_dunn", "ron_kirby"])
J("protection_round", "collection", "ron_kirby", 2, 2, "The first round",
  [TW], [S("sign", "laveracks", "sign the parade's shops to a weekly round (Laverack's, the grocer, the newsagent, the launderette, the ironmonger, the Copper Kettle)", ["a fair price, 10 pounds a shop, and a man who turns up", "a squeeze, 25 to 40 pounds a shop (shops refuse and tell after three weeks)", "a favour done first (a window mended, a thief caught)"], None, TW),
         S("collect", "grocer", "a crewman of nerve collects on Fridays", ["Ron", "a need recruit", "a hook recruit"], None, TW)],
  {"to": "tin", "pence": 0, "band": [500, 1500], "note": "per shop per week; the man's cut a quarter (ECONOMY 5.1, EC-06); rung 3 needs a front and a round"},
  TW, "ECONOMY 5.1, EC-06; STORY-FRAME 5 table week 3; BLUEPRINT-03 3.5.2 (later a crewman does rounds)", "the shops' boards and talk", people=["ron_kirby"])
J("night_between", "sit_down", "carol_ellis", 2, 3, "The night between",
  ["That you, boss? Say nowt."],
  [S("arrest", "police_station", "arrested on the entry; custody in hours; through the wall, Ron has offered a statement, to be signed at nine; bailed that evening", ["say nothing", "say what the line said", "ask for a brief"], None, "That you, boss? Say nowt."),
   S("before_nine", "police_station", "before nine the next morning", ["sign first: walk back in and put the line on paper under his own name (Ron walks; Frank charged, on bail to the end, the licence suspended a fortnight, a post lost)", "a cheaper way, only if his record earned it: the brief (Agar's man, at the brief's fee) argues Ron out as a messenger, or DC Wardell loses the statement (200 pounds, once; Ellis notices); Ron allows either only if Frank came for him at the gate or redeemed Mickey's watch", "let it stand: at nine Ron signs, and goes in on remand to the end"], None, "Saying's nowt, boss. You've a firm to stand in. I've a door.")],
  {"to": "tin", "pence": 0, "cost_band": [20000, 20000], "note": "Wardell's price 200 pounds once (economy); the brief's fee (economy)"},
  TW, "STORY-FRAME 5 The night between (decision of 24 Nov: Ron goes inside unless Frank pays to stop it); RT2-05 (if Ron is gone, the most loyal man stands in)", "Act III's charge or Ron's absence",
  people=["ron_kirby", "carol_ellis", "graham_wardell", "anthony_raine", "sgt_bellwood"])
J("the_yard", "fight", "frank_nowak", 2, 3, "The yard",
  [TW], [S("fight", "mickeys_yard", "men he made, cast from everybody he beat, shamed or let down, in by a gate somebody had a key to; the hardest fight costs him the arm either way", ["stand at the yard gate", "hold the back fence", "go out into the yards' lane to meet them"], None, TW),
         S("who_comes", "mickeys_yard", "who comes decides the rest: Ron (if free), Darren (if he slept in the spare car), Ada's call (if Frank came to her tea), the night desk (if Julie has it)", ["walks out on his feet with the tin and the board", "is carried out", "comes round in Grace Rinaldi's kitchen (nobody came)"], None, TW)],
  {"to": "tin", "pence": 0}, TW, "STORY-FRAME 5 Act IIb (the yard), worked example 2 (Neil Screeton the hardest fight if fronted up)", "the arm, for days; who he has to ask",
  people=["neil_screeton", "ron_kirby", "darren_milner", "grace_rinaldi"])
WHEN = {
 "envelope_landing": "night one after 22:00, Ron at the office door; then nights 1, 3, 5 and 7 of Act I", "car_three": "week one, the first day Danny's car stands across Mickey's rank (Danny's noticed rung)",
 "debt_darren": "day two: Sheila opens Mickey's debt book on the counter", "debt_wayne": "day two: the debt book", "debt_lee": "day two: the debt book",
 "debt_julie": "day two: the debt book", "debt_iveson": "day two: the debt book; Darren's tip about the tin box when he owes the office",
 "ritas_back_room": "Wayne owes and has been fronted once; Wayne waits by car two on the rank", "tail_coverdale": "rung 2 and Agar's licence letter has come; Sheila at the counter",
 "mind_julie": "Julie knows Frank by name and a Friday rent day is due; she asks at Chapel Lane", "mind_boxing": "rung 2; Ron on the rank in the week of a Saturday show",
 "lift_medals": "Rita's back room open (rung 2) and Frank has fenced once; Wayne in the back room", "word_to_portside": "Portside Cars taking fares after a hit-and-run; Ron on the rank",
 "ferry_rank": "rung 2; Ron says the ferry rank is Danny's now", "five_mornings": "four cars on the board; a packing-shift fare has said the cold store wants a firm that turns up",
 "rita_back_room_front": "rung 2 and Wayne's debt settled or open; Rita at her counter", "the_landing": "Frank at the third rung, or any rival at threat, or the end of game week four; never before the end of week three",
 "crisis_landing": "after the Landing, when the landing post's man is leaned on (his silence on Pauline's radio)", "crisis_cold_store": "after the Landing, when the cold-store post's man is leaned on (Tharratt rings the office before dawn)",
 "crisis_dock_gate": "after the Landing, when Ron is leaned on at the gate (Pauline's radio)", "clear_the_office": "the evening before the search: a constable's word or Sheila's warning",
 "sit_down_jensen": "the Widow's ladder at sit-down, or the fail-safe four game days before Act II ends", "sit_down_agar": "Agar's ladder at sit-down, or the fail-safe",
 "sit_down_cammack": "Danny's ladder at sit-down, or the fail-safe", "garbutt_meeting": "Garbutt's card given (Act IIa); page him from a box",
 "gate_tax_receipt": "five cars on the board: the Widow's men tax Kevin at the gate (Act IIa)", "post_dock_gate": "after the Landing, a man of his with nerve free",
 "post_cold_store": "after the Landing and the contract held", "post_landing": "after the Landing, the landing held",
 "loads_seen": "rung 3 and Lee or Kieran Rourke on side", "board_account": "rung 3 and the decent jacket", "shipment_times": "rung 3; Rodney Usher at the counter",
 "officer_trade": "rung 3 and a hook on the bonded store", "bonded_store": "rung 3; Kieran Rourke's count told",
 "item_wages": "Act III, morning one: the inspector at the counter", "item_car_records": "Act III, morning two", "item_invoice": "Act III, morning three",
 "item_gate": "Act III, morning four", "item_the_line": "Act III, the last morning; at five, the counter", "the_quay": "the last day, after Pauline says car two is not answering",
 "danny_visit": "a week after car three (Act IIa)", "ron_lessons": "week two onward: one lesson a week offered by Ron on the rank; lesson five in week five",
 "sheila_trust": "Sheila calls him Frank (her trust rung) and rung 2", "protection_round": "rung 2 and a man of nerve on the board (week three)",
 "night_between": "the turn: after the Landing and lesson five, the tip with Ellis (by the end of week five at the latest)", "the_yard": "week six, after the night between",
}
for j in JOBS:
    if j["id"] in WHEN:
        j["when"] = WHEN[j["id"]]
    elif j["id"].startswith("send_"):
        j["when"] = "from Act II, at the board or in talk with one of his men"
