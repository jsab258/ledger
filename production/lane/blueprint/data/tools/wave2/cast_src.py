"""The named cast of the Hook for blueprint data file 3 (people/ and ties.json) and file 4 (routines.json).
Written 24 Nov 2026 by the data-build wave 2 job. One entry a person. Builder: build_people.py.

Fields (short): id; n name; a age; s sex; k kind; r role; home (a places.json id or a map.json door id, or
edge_north/edge_west for people who live off the Hook); cid the real town's id (people.json / hook-cast.json) or None;
called; proto (prototype cast.js id, whose look and card are taken over); t (nerve, dutiful, willingness) where the
traits draft gives no row; v voice id; die can_die; fb fallback_role; inv invented here (True) or proposed by the
story frame (\"frame\"); card {who, speak, life, ...} for anyone the prototype has no card for; look for anyone the
prototype has no look for; fight a fighter kind (1.3.12); rt the routine as day groups.

Routine text: \"days|HH:MM place act; HH:MM place act; ...\". Each person's groups cover all seven days once.
Every place is a places.json id or a map.json door id (a home). Times are game time, 24-hour clock.
"""

# ---- look helper: the prototype's look object (h height m, b build 0..1, skin index, hair [style, colour],
# top [type, colour, accent], bot [type, colour], x extras)
def L(h, b, skin, hair, hc, top, tc, ta, bot, bc, *x):
    return {"h": h, "b": b, "skin": skin, "hair": [hair, hc], "top": [top, tc, ta], "bot": [bot, bc], "x": list(x)}

# ---- temper from the traits draft (game-design/town-traits-draft-2026-09-29.md): nerve, loyalty, greed, saw-wounding
TRAITS = {
    "ron_kirby": (0.8, 0.7, 0.3, "no"), "sheila_dunn": (0.6, 0.6, 0.2, "no"), "pauline_kitching": (0.5, 0.6, 0.3, "no"),
    "kevin_needham": (0.5, 0.55, 0.4, "no"), "terry_hodgson": (0.6, 0.55, 0.4, "no"), "june_suddaby": (0.6, 0.3, 0.2, "yes"),
    "darren_milner": (0.3, 0.4, 0.8, "no"), "ada_vane": (0.6, 0.35, 0.2, "yes"), "alison_sedman": (0.8, 0.3, 0.2, "yes"),
    "brenda_laverack": (0.5, 0.3, 0.5, "yes"), "lee_drewery": (0.35, 0.3, 0.5, "no"), "rita_welburn": (0.55, 0.3, 0.7, "yes"),
    "wayne_harrison": (0.3, 0.3, 0.6, "never"), "hal_metcalfe": (0.3, 0.3, 0.8, "never"), "susan_coverdale": (0.7, 0.3, 0.3, "yes"),
    "brendan_walsh": (0.7, 0.35, 0.1, "yes"), "nora_cronin": (0.4, 0.3, 0.3, "yes"), "winifred_duggleby": (0.35, 0.3, 0.3, "no"),
    "doreen_harland": (0.35, 0.3, 0.4, "no"), "pat_stainton": (0.3, 0.3, 0.4, "no"), "irene_lowther": (0.35, 0.3, 0.4, "no"),
    "julie_kettlewell": (0.3, 0.3, 0.4, "no"), "tracey_scarth": (0.45, 0.3, 0.5, "yes"), "stanley_hirst": (0.35, 0.3, 0.6, "no"),
    "mandy_calvert": (0.3, 0.3, 0.5, "no"), "leslie_cotterill": (0.35, 0.3, 0.5, "no"), "colin_mastin": (0.5, 0.3, 0.4, "yes"),
    "albert_suggitt": (0.3, 0.3, 0.4, "no"), "kieran_rourke": (0.45, 0.3, 0.4, "yes"), "gary_mawer": (0.35, 0.3, 0.4, "no"),
    "ian_megginson": (0.3, 0.3, 0.5, "no"), "christine_pickering": (0.35, 0.3, 0.3, "no"), "karen_grummitt": (0.3, 0.3, 0.3, "no"),
    "gordon_leckenby": (0.4, 0.3, 0.4, "yes"), "sylvia_rennison": (0.5, 0.3, 0.6, "yes"), "edith_stockill": (0.3, 0.3, 0.3, "no"),
    "shaun_hewson": (0.35, 0.3, 0.4, "no"), "dawn_pybus": (0.3, 0.3, 0.6, "no"), "dennis_iveson": (0.3, 0.3, 0.8, "never"),
    "norman_dent": (0.6, 0.3, 0.3, "yes"), "old_firm_man": (0.7, 0.2, 0.6, "never"),
}

S = "src"
P = []
def add(**k):
    P.append(k)

# =========================== the lead
add(id="frank_nowak", n="Frank Nowak", a=32, s="m", k="principal", cid="tom", called="the new owner",
    r="Mickey Suddaby's nephew, who inherits the cab office; Polish father, British mother",
    home="toms_flat", die=False, v=None, proto=None, t=(0.7, 0.5, 0.3), quiet=True,
    look=L(1.80, 0.55, 0, "short", "#2a2018", "jacket", "#3a3a40", "#c8c0b0", "trousers", "#2a2a30"),
    card=dict(who="Frank Nowak, 32, Mickey Suddaby's nephew: a Polish father, a British mother, Mickey his mother's brother. Steps off the ferry with one suitcase, a letter and 23.50 pounds to a dead uncle's cab office. Wants to be the Hook's name by Christmas.",
              speak="The player's. Fixed lines only at authored beats. Gives everybody his whole name and spells it.",
              life="Sleeps in the flat over the office. Good at the wheel; never asks the way.",
              rivals="All three are looking at the office from his first week."),
    src="decision of 24 Nov (the lead is Frank Nowak); STORY-FRAME 3; canon", rt="lead")

# =========================== the firm and the core
add(id="ron_kirby", n="Ron Kirby", a=58, s="m", k="principal", cid="rocco", called="Ron", proto="ron", v="p227",
    r="A docker until 1989; Mickey kept him on the door and the rank", home="d_cl_14", die=True, fb="the most loyal man",
    fight="boxer", src="canon; casting ron-kirby SHEET; STORY-FRAME 3",
    rt="mon-sat|00:00 d_cl_14 asleep; 06:30 caff breakfast; 07:30 rank_mickeys on the rank; 12:00 laveracks dinner from the fish shop; 12:30 rank_mickeys on the rank; 17:00 rank_ferry the boat queue; 18:00 mickeys the door; 23:00 d_cl_14 home"
       "/sun|00:00 d_cl_14 asleep; 09:30 allotments his plot; 13:00 d_cl_14 home; 18:00 mickeys the door; 23:00 d_cl_14 home")
add(id="sheila_dunn", n="Sheila Dunn", a=53, s="f", k="principal", cid="lena", called="Sheila", proto="sheila", v="p267",
    r="Mickey's bookkeeper for thirty-one years; the book", home="edge_north", die=False, src="canon; casting sheila-dunn SHEET; STORY-FRAME 3",
    rt="mon-wed,fri|00:00 edge_north home across the river; 08:30 mickeys the counter and the book; 12:30 caff her dinner; 13:15 mickeys the counter and the book; 17:30 bus_stop_qs the bus home; 18:00 edge_north home"
       "/thu|00:00 edge_north home across the river; 08:30 newsagent the pension counter; 09:15 mickeys the counter and the book; 12:30 caff her dinner; 13:15 mickeys the counter and the book; 17:30 bus_stop_qs the bus home; 18:00 edge_north home"
       "/sat|00:00 edge_north home across the river; 08:30 mickeys the counter and the book; 13:00 bus_stop_qs the bus home; 13:30 edge_north home"
       "/sun|00:00 edge_north home across the river")
add(id="pauline_kitching", n="Pauline Kitching", a=44, s="f", k="firm", cid="zlata", called="Pauline", proto="pauline", v="p280",
    r="Mickey's dispatcher: the radio and the phone", home="edge_north", die=False, src="canon; 3.2.2",
    rt="mon-sat|00:00 edge_north home; 06:45 mickeys the radio; 12:00 rank_mickeys a cigarette by the rank; 12:20 mickeys the radio; 19:00 bus_stop_qs the bus home; 19:30 edge_north home"
       "/sun|00:00 edge_north home; 09:00 mickeys the radio, Sunday hours; 16:00 edge_north home")
add(id="kevin_needham", n="Kevin Needham", a=36, s="m", k="firm", cid="ferko", called="Kevin", proto="kevin", v=None,
    r="The day driver on Mickey's rank, car one; the Widow's eyes among the regulars", home="edge_north", die=True,
    fb="a car short until a driver is hired", fight="brawler", src="canon; 3.2.2; 2.10.2",
    rt="mon-sat|00:00 edge_north home; 06:30 caff breakfast; 07:00 rank_mickeys car one; 12:30 caff his break; 13:00 rank_mickeys car one; 19:00 edge_north home"
       "/sun|00:00 edge_north home; 12:00 rank_mickeys car one, Sunday; 18:00 edge_north home")
add(id="terry_hodgson", n="Terry Hodgson", a=52, s="m", k="firm", cid="dusan", called="Terry", proto="terry", v=None,
    r="The night driver, on the set from six", home="d_cs_9", die=True, fb="a car short until a driver is hired", fight="boxer",
    src="canon; 3.2.2",
    rt="mon-sat|00:00 rank_mickeys the night car; 03:00 d_cs_9 home to bed; 17:30 caff his breakfast at teatime; 18:00 rank_mickeys the night car"
       "/sun|00:00 rank_mickeys the night car; 03:00 d_cs_9 home to bed; 19:00 rank_mickeys the night car")
add(id="darren_milner", n="Darren Milner", a=25, s="m", k="principal", cid="sam", called="Darren", proto="darren", v="p286",
    r="The street hustler; owes Mickey's 22 pounds and pays in what he hears", home="d_nr_23", die=True,
    fb="his tips come through Pauline's radio talk and the caff, his debt closed", fight="brawler", src="canon; 2.8.1",
    rt="mon,wed,fri|00:00 d_nr_23 his mother's; 09:30 caff a tea he does not pay for; 10:30 ritas selling; 12:00 rank_mickeys hanging about; 13:30 launderette the warm; 15:00 phone_parade the phone box; 16:00 rank_mickeys hanging about; 19:00 cammack_base near the lock-ups; 21:00 phone_parade the phone box; 22:00 d_nr_23 his mother's"
       "/tue,thu,sat|00:00 d_nr_23 his mother's; 09:30 caff a tea he does not pay for; 10:30 fish_dock what fell off a box; 12:30 rank_mickeys hanging about; 14:00 rank_ferry the boat queue; 16:00 rank_mickeys hanging about; 19:00 caff the evening trade; 22:00 d_nr_23 his mother's"
       "/sun|00:00 d_nr_23 his mother's; 12:00 rank_mickeys hanging about; 15:00 d_nr_23 his mother's")
add(id="danny_cammack", n="Danny Cammack", a=27, s="m", k="principal", cid="danny", called="Danny", proto=None, v="p243",
    r="Head of the new crew; drove car two for Mickey; the main opponent", home="d_nr_40", die=True,
    fb="Craig Fewson takes his ladder at the same rung, his key and his grudge", t=(0.75, 0.5, 0.2), quiet=True, fight="wiry",
    look=L(1.78, 0.4, 0, "short", "#3a2a1a", "leather", "#1a1a1e", "#8a2a2a", "jeans", "#2a3550"),
    card=dict(who="Danny Cammack, 27. Drove car two for Mickey and never gave the key back. Thinks the office should have been his. Runs the new crew from the lock-ups behind North Road.",
              speak="Quick, funny, needling. Calls Frank 'nephew'. Prices every door out loud.",
              life="A flat on North Road; the lock-ups by day; Quay Street by night when he wants noise.",
              rivals="Wants the Hook's name and to hear the old firms say it. Fears being somebody's driver again.",
              secret="Still has his key to car two."),
    src="canon; STORY-FRAME 3 (decision of 24 Nov: the main opponent; drove Mickey's own car); casting danny-cammack",
    rt="mon-sat|00:00 d_nr_40 his flat; 10:30 caff late breakfast; 11:30 cammack_base the lock-ups; 15:00 rank_north watching the other rank; 16:00 cammack_base the lock-ups; 20:00 snooker_hall holding court; 22:30 cammack_base the lock-ups; 23:30 d_nr_40 his flat"
       "/sun|00:00 d_nr_40 his flat; 13:00 cammack_base the lock-ups; 18:00 d_nr_40 his flat")
add(id="maureen_jensen", n="Maureen Jensen", a=57, s="f", k="principal", cid="sera", called="the Widow", proto=None, v=None,
    r="Head of the dockside syndicate; the dock gate and the men at it", home="d_cs_19", die=False,
    t=(0.85, 0.6, 0.05), quiet=True,
    look=L(1.66, 0.55, 0, "set", "#8a8078", "overcoat", "#2a2a2e", "#6a5a48", "skirt", "#2a2a2e", "fur_collar"),
    card=dict(who="Maureen Jensen, 57, the Widow: runs the dockside syndicate from the office over the net store. Taxes the cabs at the dock gate. Has not walked up Quay Street in years.",
              speak="Low, slow, never asks. Calls men Mister until she owns them, then by their first name.",
              life="A house at the top of Cold Store Road. The net store office by day; home by six.",
              rivals="Wants the dock gate and the men at it; fears a gate with nobody at it."),
    src="canon; STORY-FRAME 3; casting maureen-jensen; RT2-05 (Frank's line keeps her from his hands)",
    rt="mon-sat|00:00 d_cs_19 home; 08:00 widow_base the office over the net store; 17:00 d_cs_19 home"
       "/sun|00:00 d_cs_19 home; 10:00 chapel Mass; 11:15 d_cs_19 home")
add(id="carol_ellis", n="Carol Ellis", a=40, s="f", k="officer", cid="ellis", called="DS Ellis", proto="ellis", v=None,
    r="Detective Sergeant, CID; cannot be bought", home="police_station", die=False, src="canon; STORY-FRAME 3; RT2-05",
    rt="mon-fri|00:00 edge_north home in town; 08:30 police_station her desk; 18:30 edge_north home in town"
       "/sat-sun|00:00 edge_north home in town")
add(id="geoffrey_agar", n="Geoffrey Agar", a=62, s="m", k="principal", cid="aldous", called="Mr Agar", proto=None, v="p226",
    r="Solicitor and honorary alderman; the old-money machine; Agar & Co, the letting agents", home="edge_north", die=True,
    fb="Simon Ombler takes his ladder at the same rung", t=(0.5, 0.4, 0.7), quiet=True,
    look=L(1.76, 0.6, 0, "swept", "#c0bab0", "suit", "#2a2a34", "#e8e4dc", "trousers", "#2a2a34", "glasses"),
    card=dict(who="Geoffrey Agar, 62, solicitor and honorary alderman. Agar & Co let half the Hook. Wants the cold-store road quiet and bought before the docks are redeveloped.",
              speak="Courteous, slow, every sentence a letter. Never raises his voice; sends paper instead.",
              life="Lives up in town. Calls at the agents' office on Cold Store Road on Tuesdays and Fridays.",
              rivals="Fears his name in print."),
    src="canon; STORY-FRAME 2 and 4; casting geoffrey-agar",
    rt="tue,fri|00:00 edge_north home in town; 10:00 agar_base the agents' back room; 12:30 edge_north back to town"
       "/mon,wed,thu,sat,sun|00:00 edge_north home in town")
add(id="keith_garbutt", n="Keith Garbutt", a=48, s="m", k="principal", cid="fixer", called="the Fixer", proto=None, v=None,
    r="The Fixer: brokers between all three rivals; carries a pager", home="edge_north", die=True,
    fb="no reads and no truce", t=(0.6, 0.3, 0.6), quiet=True,
    look=L(1.74, 0.6, 0, "short", "#5a5048", "car_coat", "#4a4038", "#2a2a2a", "trousers", "#30302e", "pager"),
    card=dict(who="Keith Garbutt, 48, the Fixer. Sells true reads of a rival, a meeting that then happens, and one truce a game. Paged from a box, rings that box back within half a game hour.",
              speak="Friendly, careful, never says a name he has not been paid to say.",
              life="Lives up in town; a table at the caff mid-morning, the snooker hall in the evening.",
              rivals="Wants everybody still at the table; fears a winner."),
    src="canon; 2.10.4; STORY-FRAME 2",
    rt="mon-sat|00:00 edge_north home in town; 10:30 caff his table; 12:00 edge_north about town; 19:00 snooker_hall a corner table; 22:00 edge_north home in town"
       "/sun|00:00 edge_north home in town")

# =========================== principals of the town
add(id="ada_vane", n="Ada Vane", a=78, s="f", k="principal", cid="ada", called="Ada", proto="ada", v=None,
    r="The old woman at her window opposite Mickey's", home="adas", die=False, src="canon; STORY-FRAME 4 (surname)",
    rt="mon-wed,fri-sat|00:00 adas asleep; 08:00 adas at her window; 10:00 grocer her shopping; 10:45 laveracks a bit of fish; 11:15 adas at her window"
       "/thu|00:00 adas asleep; 08:00 adas at her window; 09:30 newsagent her pension; 10:15 grocer her shopping; 11:00 adas at her window"
       "/sun|00:00 adas asleep; 09:30 chapel Mass; 11:00 chapel_hall tea after; 12:00 adas at her window")
add(id="june_suddaby", n="June Suddaby", a=38, s="f", k="principal", cid="june", called="June", proto="june", v="p277",
    r="Mickey's daughter, back for the funeral; a better claim than Frank's to the name on the board", home="boarding_house", die=False,
    src="canon; STORY-FRAME 4",
    rt="mon-fri|00:00 boarding_house her room; 10:00 mickeys his things; 11:30 tea_room alone; 13:00 boarding_house her room; 16:00 chapel a candle; 17:00 boarding_house her room"
       "/sat|00:00 boarding_house her room; 11:00 ferry_landing the boat over and back; 15:00 boarding_house her room"
       "/sun|00:00 boarding_house her room; 09:30 chapel Mass; 11:00 boarding_house her room")
add(id="brendan_walsh", n="Brendan Walsh", a=61, s="m", k="principal", cid="emil", called="Father Walsh", proto="walsh", v=None,
    r="The Irish-born parish priest; keeps Mickey's confession", home="priests_house", die=False, src="canon; RT2-05",
    rt="mon,wed,thu,sat|00:00 priests_house asleep; 07:30 chapel morning Mass; 09:00 priests_house his desk; 13:00 adas a call on Ada; 14:00 chapel the church open; 18:00 priests_house supper; 20:30 edge_north sick calls on foot; 22:30 priests_house asleep"
       "/tue,fri|00:00 priests_house asleep; 07:30 chapel morning Mass; 09:00 priests_house his desk; 11:00 market_stalls_quay a word at the barrows; 12:00 priests_house his desk; 14:00 chapel the church open; 18:00 priests_house supper; 19:00 chapel_hall the hall; 21:30 priests_house asleep"
       "/sun|00:00 priests_house asleep; 08:30 chapel Masses; 11:00 chapel_hall tea after; 13:00 priests_house the afternoon; 18:00 chapel evening Mass; 19:00 priests_house asleep")
add(id="alison_sedman", n="Alison Sedman", a=30, s="f", k="principal", cid="noor", called="Alison", proto="alison", v=None,
    r="A reporter on the Meridian Pilot; the fire", home="edge_north", die=False, src="canon; STORY-FRAME 4",
    rt="tue,thu|00:00 edge_north home in town; 09:30 bus_stop_qs off the bus; 09:45 burned_warehouse the fire; 11:00 newsagent asking; 12:00 caff her dinner; 13:00 rank_mickeys a word with whoever is on it; 14:00 edge_north back to the paper"
       "/mon,wed,fri-sun|00:00 edge_north home in town")
add(id="philip_danby", n="Philip Danby", a=33, s="m", k="principal", cid="elias", called="Mr Danby", proto=None, v=None,
    r="A teacher with the school shut; walks", home="d_cl_29", die=True, fb="that friendship ends", t=(0.4, 0.4, 0.5), quiet=False,
    look=L(1.82, 0.35, 0, "floppy", "#5a4430", "cord_jacket", "#6a5a3a", "#d8c8a8", "cords", "#4a4030", "glasses", "scarf"),
    card=dict(who="Philip Danby, 33, a teacher at the comprehensive, which stands closed for the game's window. Walks the Hook every day because he does not know what else to do with a morning.",
              speak="Mild, wry, too many words, apologises for them.",
              life="Rents 29 Chapel Lane. Walks the quay at ten and the allotments after dinner.",
              rivals="Knows none of them and says so."),
    src="canon; STORY-FRAME 4",
    rt="mon-sat|00:00 d_cl_29 asleep; 10:00 fishing_quay_west his walk on the quay; 11:30 tea_room a pot of tea; 12:30 d_cl_29 home; 14:00 allotments the allotments; 16:00 d_cl_29 home"
       "/sun|00:00 d_cl_29 asleep; 11:00 ferry_landing watching the boats; 12:30 d_cl_29 home")

# =========================== the regulars (the thirty, ruling of 30 Sep)
add(id="brenda_laverack", n="Brenda Laverack", a=50, s="f", k="regular", cid="marla", called="Brenda", proto="brenda", v=None,
    r="Keeps Laverack's fish shop; buys on the fish dock at dawn", home="d_nr_5", die=True, src="canon; 3.4.1; side story 8",
    rt="mon-fri|00:00 d_nr_5 asleep; 05:00 fish_dock buying at the boxes; 07:00 laveracks gutting and the counter; 17:45 d_nr_5 home"
       "/sat|00:00 d_nr_5 asleep; 05:00 fish_dock buying at the boxes; 07:00 laveracks the counter; 17:45 d_nr_5 home"
       "/sun|00:00 d_nr_5 asleep")
add(id="lee_drewery", n="Lee Drewery", a=24, s="m", k="regular", cid="joey", called="Lee", proto="lee", v=None,
    r="Casual on the quay; the Widow's eyes; owes 15 pounds and stands for it", home="d_nr_12", die=True, fight="brawler",
    src="canon; 2.8.1; 2.10.2; STORY-FRAME 4",
    rt="mon-sat|00:00 d_nr_12 asleep; 05:45 dock_gate the pen at six; 08:00 fish_dock what work there is; 12:00 rank_mickeys sat on the bollard; 13:00 fish_dock what work there is; 16:00 boxing_club the bag, when it is open; 18:00 ritas the step; 18:30 d_nr_12 home"
       "/sun|00:00 d_nr_12 asleep; 14:00 fishing_quay_east a line off the quay; 17:00 d_nr_12 home")
add(id="rita_welburn", n="Rita Welburn", a=56, s="f", k="regular", cid="rita", called="Rita", proto="rita", v=None,
    r="Keeps Rita's, the pawn; Danny's fence and eyes", home="d_qs_4", die=True, src="canon; 2.10.2; side story 25",
    rt="mon-sat|00:00 d_qs_4 asleep; 08:45 ritas opening up; 13:00 ritas the step, a cigarette; 13:30 ritas the counter; 17:45 d_qs_4 home"
       "/sun|00:00 d_qs_4 asleep")
add(id="wayne_harrison", n="Wayne Harrison", a=27, s="m", k="regular", cid="victor", called="Wayne", proto="wayne", v=None,
    r="Rita's back-room hand; owes 30 pounds in goods", home="d_nr_27", die=True, fight="knife_man", src="canon; 2.8.1",
    rt="mon-sat|00:00 d_nr_27 asleep; 10:00 ritas the back room; 16:00 ritas the step; 17:45 snooker_hall the tables; 22:00 d_nr_27 home"
       "/sun|00:00 d_nr_27 asleep; 14:00 snooker_hall the tables; 18:00 d_nr_27 home")
add(id="hal_metcalfe", n="Henry Metcalfe", a=66, s="m", k="regular", cid="hal", called="Hal", proto="hal", v=None,
    r="Keeps the coin shop that sells no coins; Monday visits", home="d_qs_6", die=False, src="canon; side story 26",
    rt="mon|00:00 d_qs_6 asleep; 09:45 metcalfes the shop; 11:00 ritas a Monday call; 12:00 metcalfes the shop; 17:45 d_qs_6 home"
       "/tue-sat|00:00 d_qs_6 asleep; 09:45 metcalfes the shop; 17:45 d_qs_6 home"
       "/sun|00:00 d_qs_6 asleep")
add(id="susan_coverdale", n="Susan Coverdale", a=38, s="f", k="regular", cid="tibor", called="Miss Coverdale", proto="susan", v=None,
    r="A customs officer who lives past Rita's; Agar's eyes", home="d_nr_14", die=True, src="canon; 2.10.2; side story 19",
    rt="mon-fri|00:00 d_nr_14 asleep; 08:30 customs the customs house; 16:30 harbour_board the late post; 17:15 ritas past the window; 17:45 d_nr_14 home"
       "/sat-sun|00:00 d_nr_14 asleep")
add(id="nora_cronin", n="Nora Cronin", a=67, s="f", k="regular", cid="vesna", called="Mrs Cronin", proto="nora", v=None,
    r="Keeps Father Walsh's house and buys for his table", home="d_cl_6", die=False, src="canon; side story 22",
    rt="mon,wed,fri|00:00 d_cl_6 asleep; 07:15 priests_house his breakfast; 10:30 grocer his table; 11:15 laveracks his fish; 12:00 priests_house his dinner; 19:00 d_cl_6 home"
       "/tue,thu,sat|00:00 d_cl_6 asleep; 07:15 priests_house his breakfast; 09:30 market_stalls_quay the barrows; 11:00 priests_house his dinner; 19:00 d_cl_6 home"
       "/sun|00:00 d_cl_6 asleep; 09:30 chapel Mass; 11:00 chapel_hall the tea urn; 13:00 d_cl_6 home")
add(id="winifred_duggleby", n="Winifred Duggleby", a=76, s="f", k="regular", cid="magda", called="Mrs Duggleby", proto=None, v=None,
    r="Retired; cleans the chapel and does its flowers", home="d_cl_16", die=False, t=None,
    look=L(1.55, 0.45, 0, "set", "#e0dcd4", "coat", "#6a5a6a", "#d8d0c0", "skirt", "#3a3640", "headscarf"),
    card=dict(who="Winifred Duggleby, 76, a widow who cleans the chapel and does its flowers. Her husband's anniversary falls this month.",
              speak="Precise, proper, a little deaf on purpose. 'Nobody does that any more.'",
              life="16 Chapel Lane. The chapel every weekday morning.", rivals="Has heard of all three and approves of none."),
    src="canon regular; side stories 21, 23",
    rt="mon-fri|00:00 d_cl_16 asleep; 08:00 chapel the flowers and the brass; 11:30 d_cl_16 home; 14:00 adas a cup with Ada; 15:00 d_cl_16 home"
       "/sat|00:00 d_cl_16 asleep"
       "/sun|00:00 d_cl_16 asleep; 09:30 chapel Mass; 11:00 chapel_hall tea after; 12:00 d_cl_16 home")
add(id="doreen_harland", n="Doreen Harland", a=61, s="f", k="regular", cid="zora", called="Doreen", proto=None, v=None,
    r="A washerwoman at the laundry who won't retire; the early shift", home="d_cl_25", die=True,
    look=L(1.58, 0.6, 0, "perm", "#9a8a7a", "overall", "#6a8aa0", "#e8e4dc", "skirt", "#3a3a40"),
    card=dict(who="Doreen Harland, 61, a washerwoman at the laundry, on the early shift for forty years. Saw the pay packets made up.",
              speak="Brisk, broad, says what she thinks of everybody's washing.",
              life="25 Chapel Lane. At the laundry by six.", rivals="Keeps out of it."),
    src="canon regular; side stories 9, 10",
    rt="mon-fri|00:00 d_cl_25 asleep; 05:45 launderette the boiler, the early shift; 14:00 d_cl_25 home"
       "/sat|00:00 d_cl_25 asleep; 05:45 launderette the early shift; 12:00 laveracks a bit of fish; 12:30 d_cl_25 home"
       "/sun|00:00 d_cl_25 asleep")
add(id="pat_stainton", n="Pat Stainton", a=45, s="f", k="regular", cid="iva", called="Pat", proto=None, v=None, inv=True,
    r="A presser at the laundry", home="d_nr_31", die=True,
    look=L(1.62, 0.55, 0, "perm", "#7a5a3a", "overall", "#7a9aa8", "#e8e4dc", "skirt", "#30303a"),
    card=dict(who="Pat Stainton, 45, works the presses at the laundry. Julie's friend until the summer lay-offs.",
              speak="Tired, kind, quick to laugh at herself.", life="31 North Road. The presses eight to five.", rivals="Keeps out of it."),
    src="hook-cast.json iva (unnamed; named here)",
    rt="mon-fri|00:00 d_nr_31 asleep; 07:45 launderette the presses; 17:00 grocer on the way home; 17:30 d_nr_31 home"
       "/sat-sun|00:00 d_nr_31 asleep")
add(id="irene_lowther", n="Irene Lowther", a=52, s="f", k="regular", cid="selma", called="Irene", proto=None, v=None, inv=True,
    r="A laundress at the laundry", home="d_nr_33", die=True,
    look=L(1.60, 0.5, 0, "set", "#6a5a4a", "overall", "#7a9aa8", "#e8e4dc", "skirt", "#30303a"),
    card=dict(who="Irene Lowther, 52, a laundress. Knows whose sheets come in with what on them, and says nothing.",
              speak="Few words, pursed lips, 'I couldn't say, love.'", life="33 North Road.", rivals="Keeps out of it."),
    src="hook-cast.json selma (unnamed; named here)",
    rt="mon-fri|00:00 d_nr_33 asleep; 07:45 launderette the sorting room; 16:00 d_nr_33 home"
       "/sat-sun|00:00 d_nr_33 asleep")
add(id="julie_kettlewell", n="Julie Kettlewell", a=29, s="f", k="regular", cid="tanja", called="Julie", proto="julie", v=None,
    r="Laid off from the laundry's presses; owes 9 pounds she cannot pay; can drive; the likeliest night desk", home="d_cl_9", die=True,
    src="canon; 2.8.1; 2.11.1; STORY-FRAME 4",
    rt="mon,wed,fri|00:00 d_cl_9 asleep; 08:30 newsagent the cards in the window; 09:30 launderette asking after work; 11:00 market_stalls_quay looking; 12:30 d_cl_9 home; 18:00 d_cl_9 the rent man at six"
       "/tue,thu,sat|00:00 d_cl_9 asleep; 08:30 newsagent the cards in the window; 09:30 edge_north into town for work; 15:00 d_cl_9 home"
       "/sun|00:00 d_cl_9 asleep; 14:00 caff a tea with Pat; 15:00 d_cl_9 home")
add(id="tracey_scarth", n="Tracey Scarth", a=28, s="f", k="regular", cid="katarina", called="Tracey", proto=None, v=None,
    r="A seamstress: alterations at the laundry and a stall on the market", home="d_nr_19", die=True,
    look=L(1.65, 0.35, 0, "permed_long", "#3a2418", "cardigan", "#8a3a6a", "#e8d8c8", "jeans", "#3a4a66", "pins"),
    card=dict(who="Tracey Scarth, 28, does alterations in the laundry's back room and has a stall on the Thursday market. Sees every coat on the Hook.",
              speak="Sharp, teasing, talks with pins in her mouth.", life="19 North Road.", rivals="Has seen Danny's lads run past her window."),
    src="canon regular; side stories 5, 11",
    rt="mon-wed,fri|00:00 d_nr_19 asleep; 09:00 launderette alterations; 17:00 d_nr_19 home"
       "/thu|00:00 d_nr_19 asleep; 07:30 market_stalls_quay her stall; 16:15 d_nr_19 home"
       "/sat|00:00 d_nr_19 asleep; 09:00 launderette alterations; 13:00 d_nr_19 home"
       "/sun|00:00 d_nr_19 asleep")
add(id="stanley_hirst", n="Stanley Hirst", a=63, s="m", k="regular", cid="ines", called="Mr Hirst", proto=None, v=None, inv=True,
    r="Rita's appraiser; a loupe in his waistcoat", home="d_nr_35", die=False,
    look=L(1.70, 0.4, 0, "balding", "#b0aaa0", "waistcoat", "#4a4038", "#e8e0d0", "trousers", "#3a3630", "glasses"),
    card=dict(who="Stanley Hirst, 63, appraises for Rita. Thirty years a jeweller's man in town before that.",
              speak="Dry, exact, prices aloud.", life="35 North Road.", rivals="Knows what Danny's lads bring in and what it is worth."),
    src="hook-cast.json ines (unnamed; named here)",
    rt="mon-sat|00:00 d_nr_35 asleep; 09:00 ritas the appraising; 17:15 d_nr_35 home"
       "/sun|00:00 d_nr_35 asleep")
add(id="mandy_calvert", n="Mandy Calvert", a=24, s="f", k="regular", cid="marta", called="Mandy", proto=None, v=None, inv=True,
    r="Rita's clerk: the tickets and the book", home="d_nr_37", die=True,
    look=L(1.63, 0.35, 0, "permed_long", "#c09060", "jumper", "#4a8aa0", "#f0e8d8", "skirt", "#2a2a30", "earrings"),
    card=dict(who="Mandy Calvert, 24, writes the pawn tickets at Rita's. Knows whose watch came in when.",
              speak="Bored, chatty once started.", life="37 North Road, with her nan.", rivals="Fancies one of Danny's lads and will not say which."),
    src="hook-cast.json marta (unnamed; named here)",
    rt="mon-sat|00:00 d_nr_37 asleep; 09:00 ritas the tickets; 11:00 ritas the step; 11:15 ritas the tickets; 17:15 d_nr_37 home"
       "/sun|00:00 d_nr_37 asleep")
add(id="leslie_cotterill", n="Leslie Cotterill", a=50, s="m", k="regular", cid="jelena", called="Les", proto=None, v=None, inv=True,
    r="A locksmith who works the pawn's counter in the mornings and the yard in the afternoons", home="d_nr_38", die=True,
    look=L(1.72, 0.55, 0, "short", "#6a6058", "overall", "#3a4a5a", "#2a2a2a", "trousers", "#2a2a2a"),
    card=dict(who="Les Cotterill, 50, cuts keys at Rita's counter mornings and works with Ian at the yard afternoons. Older and slower than Ian, and more careful whose keys he cuts.",
              speak="Slow, cautious, 'depends whose door'.", life="38 North Road.", rivals="Has cut a key for Danny once and regrets it."),
    src="hook-cast.json jelena (unnamed; named here)",
    rt="mon-fri|00:00 d_nr_38 asleep; 08:45 ritas key cutting; 12:00 ironmonger blanks; 12:30 iveson_yard odd jobs at the yard; 17:00 d_nr_38 home"
       "/sat|00:00 d_nr_38 asleep; 08:45 ritas key cutting; 12:00 d_nr_38 home"
       "/sun|00:00 d_nr_38 asleep")
add(id="colin_mastin", n="Colin Mastin", a=41, s="m", k="regular", cid="stipe", called="Colin", proto=None, v=None,
    r="A crane driver on the docks; offered night work off the books", home="d_cs_7", die=True,
    look=L(1.80, 0.65, 0, "short", "#4a3a2a", "donkey", "#2a2e36", "#e07a1a", "jeans", "#30384a", "flatcap"),
    card=dict(who="Colin Mastin, 41, drives a crane inside the gate. The Widow's people have offered dockers night work off the books.",
              speak="Straight, slow, asks a straight question and waits.", life="7 Cold Store Road; the gate at six.", rivals="Works under the Widow's tax like every man at the gate."),
    src="canon regular; side story 15",
    rt="mon-fri|00:00 d_cs_7 asleep; 05:45 dock_gate in at six, the cranes inside; 17:00 fish_dock off shift; 17:30 d_cs_7 home"
       "/sat|00:00 d_cs_7 asleep; 05:45 dock_gate Saturday morning; 12:30 d_cs_7 home"
       "/sun|00:00 d_cs_7 asleep")
add(id="albert_suggitt", n="Albert Suggitt", a=78, s="m", k="regular", cid="fabjan", called="Albert", proto="albert", v=None,
    r="A retired trawlerman who mends nets on the docks some mornings", home="d_cs_13", die=False, src="canon; side story 16",
    rt="mon-fri|00:00 d_cs_13 asleep; 06:30 fish_dock the nets; 12:00 caff his dinner; 13:00 d_cs_13 home"
       "/sat-sun|00:00 d_cs_13 asleep; 11:00 fishing_quay_east watching the water; 13:00 d_cs_13 home")
add(id="kieran_rourke", n="Kieran Rourke", a=44, s="m", k="regular", cid="goran", called="Kieran", proto=None, v=None, inv=True,
    r="A customs assistant on the docks; knows the bonded store", home="d_nr_41", die=True,
    look=L(1.76, 0.6, 0, "short", "#5a3a28", "tunic", "#1c2540", "#c9b04a", "trousers", "#1c2540"),
    card=dict(who="Kieran Rourke, 44, born in Wexford, a customs assistant on the docks for twenty years. Counts the bonded store's tobacco.",
              speak="Easy, Irish, a story for every question and an answer for none.", life="41 North Road; the caff two evenings.", rivals="Has watched the Widow's loads come through for years."),
    src="hook-cast.json goran (unnamed; named here)",
    rt="mon,wed,fri|00:00 d_nr_41 asleep; 07:45 customs the docks; 17:00 d_nr_41 home"
       "/tue,thu|00:00 d_nr_41 asleep; 07:45 customs the docks; 17:00 d_nr_41 home; 18:00 caff his tea; 20:30 d_nr_41 home"
       "/sat|00:00 d_nr_41 asleep; 11:00 market_stalls_quay the barrows; 12:30 d_nr_41 home"
       "/sun|00:00 d_nr_41 asleep; 09:30 chapel Mass; 11:00 d_nr_41 home")
add(id="gary_mawer", n="Gary Mawer", a=29, s="m", k="regular", cid="tomas", called="Gary", proto=None, v=None,
    r="A boat repairer at the yard; breakfast at the caff", home="d_nr_30", die=True,
    look=L(1.77, 0.5, 0, "short", "#7a5a3a", "overall", "#3a4a3a", "#2a2a2a", "jeans", "#30384a"),
    card=dict(who="Gary Mawer, 29, repairs boats at the yard. Knows Mickey rented a mooring nobody uses.",
              speak="Cheerful, gossipy over a bacon sandwich.", life="30 North Road.", rivals="Tells the Widow's man what moorings are free."),
    src="canon regular; side story 17",
    rt="mon-fri|00:00 d_nr_30 asleep; 07:00 caff breakfast; 07:45 iveson_yard the slip and the yard; 17:00 d_nr_30 home"
       "/sat|00:00 d_nr_30 asleep; 08:00 caff breakfast; 09:00 iveson_yard Saturday jobs; 12:00 d_nr_30 home"
       "/sun|00:00 d_nr_30 asleep")
add(id="ian_megginson", n="Ian Megginson", a=34, s="m", k="regular", cid="luka", called="Ian", proto=None, v=None,
    r="A locksmith and repairman at the yard; locks for the crew", home="d_nr_8", die=True,
    look=L(1.75, 0.45, 0, "short", "#3a2a1a", "overall", "#3a4a5a", "#2a2a2a", "jeans", "#30384a", "toolbag"),
    card=dict(who="Ian Megginson, 34, locksmith and repairman. Says Mickey's front lock is 'anybody with a hairpin and an hour'.",
              speak="Matter-of-fact, proud of his trade.", life="8 North Road. The allotments on Sundays.", rivals="Will open anything for whoever pays."),
    src="canon regular; 2.11.1; side story 3",
    rt="mon-fri|00:00 d_nr_8 asleep; 07:00 caff breakfast; 07:45 iveson_yard the workshop; 17:00 d_nr_8 home"
       "/sat|00:00 d_nr_8 asleep; 09:00 ironmonger odd jobs; 12:00 d_nr_8 home"
       "/sun|00:00 d_nr_8 asleep; 10:00 allotments his plot; 13:00 d_nr_8 home")
add(id="christine_pickering", n="Christine Pickering", a=39, s="f", k="regular", cid="bruno", called="Mrs Pickering", proto=None, v=None,
    r="A clerk at the Harbour Board's counter", home="d_nr_9", die=True,
    look=L(1.66, 0.4, 0, "bob", "#6a4a30", "blouse", "#e0d8c8", "#2a3a5a", "skirt", "#2a3a5a"),
    card=dict(who="Christine Pickering, 39, clerk at the Harbour Board's counter. Noticed a stranger asking who holds the yard's lease.",
              speak="Formal, kind, notices manners.", life="9 North Road; the newsagent's at dinner.", rivals="Types the Board's letters, some of them to Mr Agar."),
    src="canon regular; side story 20",
    rt="mon-fri|00:00 d_nr_9 asleep; 08:45 harbour_board the counter; 12:00 newsagent dinner hour; 12:45 harbour_board the counter; 16:45 d_nr_9 home"
       "/sat-sun|00:00 d_nr_9 asleep")
add(id="karen_grummitt", n="Karen Grummitt", a=25, s="f", k="regular", cid="petra", called="Karen", proto=None, v=None,
    r="The ferry's ticket clerk; lodges at Regent House and owes a fortnight", home="boarding_house", die=True,
    look=L(1.64, 0.35, 0, "permed_long", "#b08050", "uniform_jacket", "#2a3a6a", "#c0a040", "skirt", "#2a3a6a"),
    card=dict(who="Karen Grummitt, 25, sells tickets at the ferry window and sees who goes over and who comes back.",
              speak="Quiet, quick, wants out of the Hook.", life="Lodges at Regent House.", rivals="Has seen the Widow's men meet the last boat."),
    src="canon regular; 2.11.1; side story 28",
    rt="mon-sat|00:00 boarding_house her room; 06:30 ferry_landing the ticket window; 13:00 ferry_landing the ticket window, dinner at the window; 19:00 boarding_house her room"
       "/sun|00:00 boarding_house her room; 12:00 caff Sunday dinner; 13:00 boarding_house her room")
add(id="gordon_leckenby", n="Gordon Leckenby", a=55, s="m", k="regular", cid="dario", called="Gordon", proto=None, v=None,
    r="A ferryman; holds the parcel that came back", home="d_nr_42", die=True,
    look=L(1.78, 0.6, 0, "flatcap", "#5a5048", "jersey", "#1c2a40", "#1c2a40", "trousers", "#2a2a2a", "beard"),
    card=dict(who="Gordon Leckenby, 55, crews the Meridian Ferry. Talks only about the weather.", speak="The weather, at length.",
              life="42 North Road. The first boat at twenty to seven.", rivals="Sees the last boat's cargo and the men who meet it."),
    src="canon regular; side story 18",
    rt="mon-sat|00:00 d_nr_42 asleep; 06:00 ferry_landing the first boat; 17:15 d_nr_42 home"
       "/sun|00:00 d_nr_42 asleep")
add(id="sylvia_rennison", n="Sylvia Rennison", a=64, s="f", k="regular", cid="sanja", called="Mrs Rennison", proto="sylvia", v=None,
    r="Keeps Regent House, the boarding house; a lodger of Danny's three weeks behind", home="boarding_house", die=False,
    src="canon; side story 27",
    rt="mon-fri|00:00 boarding_house asleep; 06:30 boarding_house breakfasts; 10:30 laveracks fish for the lodgers; 11:15 boarding_house the house; 22:00 boarding_house asleep"
       "/sat-sun|00:00 boarding_house asleep; 06:30 boarding_house breakfasts and the step")
add(id="edith_stockill", n="Edith Stockill", a=79, s="f", k="regular", cid="hana", called="Mrs Stockill", proto=None, v=None,
    r="A retired shipping clerk who writes letters and fills in forms at the newsagent's pension counter", home="d_cl_12", die=False,
    look=L(1.54, 0.4, 0, "bun", "#e8e4dc", "coat", "#4a5a6a", "#d0c8b8", "skirt", "#3a3a40", "glasses", "handbag"),
    card=dict(who="Edith Stockill, 79, forty years a shipping clerk. Writes the street's letters at the pension counter for nothing.",
              speak="Exact, dry, a clerk's sentences.", life="12 Chapel Lane.", rivals="'Everybody round here talks.'"),
    src="canon regular; side story 24",
    rt="mon,wed,thu,sat|00:00 d_cl_12 asleep; 09:15 adas a word at Ada's window; 10:00 newsagent the pension counter; 12:30 d_cl_12 home"
       "/tue,fri|00:00 d_cl_12 asleep; 09:15 adas a word at Ada's window; 10:00 newsagent the pension counter; 11:00 market_stalls_quay the barrows; 12:30 d_cl_12 home"
       "/sun|00:00 d_cl_12 asleep")
add(id="shaun_hewson", n="Shaun Hewson", a=26, s="m", k="regular", cid="franjo", called="Shaun", proto="shaun", v=None,
    r="The sign painter doing the parade's boards this month", home="boarding_house", die=True, fight="brawler",
    src="canon; 2.11.1; side story 6",
    rt="mon-thu|00:00 boarding_house his room; 07:00 caff breakfast; 08:00 empty_unit his ladder on the parade's boards; 12:00 caff dinner; 13:00 launderette the next board; 17:00 boarding_house his room"
       "/fri|00:00 boarding_house his room; 07:00 caff breakfast; 08:00 mickeys his ladder at Mickey's bay; 12:00 caff dinner; 13:00 launderette the next board; 17:00 boarding_house his room"
       "/sat|00:00 boarding_house his room; 10:00 snooker_hall the tables; 14:00 boarding_house his room"
       "/sun|00:00 boarding_house his room; 10:00 allotments a walk; 13:00 boarding_house his room")
add(id="dawn_pybus", n="Dawn Pybus", a=27, s="f", k="regular", cid="danica", called="Dawn", proto=None, v=None,
    r="Runs for the rent collector, Mr Askew of Agar & Co's agents", home="edge_north", die=True,
    look=L(1.62, 0.35, 0, "ponytail", "#8a6040", "anorak", "#6a2a3a", "#e0d8c8", "jeans", "#3a4a66", "clipboard"),
    card=dict(who="Dawn Pybus, 27, runs the rent book round for Mr Askew. Apologetic on every step.",
              speak="Apologetic, quick, 'I only collect it'.", life="Lives up in town.", rivals="Works for Agar's agents and knows whose rent went up."),
    src="canon regular; side story 29; timetables weekly rent (Mr Leonard Askew)",
    rt="mon-thu|00:00 edge_north home in town; 09:00 adas the rent round, Quay Street; 10:30 d_cl_9 the rent round, Chapel Lane; 12:00 agar_base the agents' book; 13:00 edge_north back to town"
       "/fri|00:00 edge_north home in town; 09:00 adas the rent round, Quay Street; 10:30 mickeys behind Mr Askew at the counter; 12:00 agar_base the agents' book; 13:00 edge_north back to town"
       "/sat-sun|00:00 edge_north home in town")
add(id="dennis_iveson", n="Dennis Iveson", a=62, s="m", k="regular", cid="drago", called="Dennis", proto="dennis", v=None,
    r="A scrap dealer on the old warehouse row; owes 80 pounds and has it; bought out of the burned warehouse", home="d_nr_44", die=True,
    fb="the fire thread runs on through Alison and Ellis, his debt closed", fight="big_man", src="canon; 2.8.1; RT2-05",
    rt="mon-sat|00:00 d_nr_44 asleep; 07:00 caff breakfast; 07:45 iveson_yard the yard; 12:00 iveson_hut his dinner in the hut; 13:00 iveson_yard the yard; 17:15 snooker_hall a frame; 19:30 d_nr_44 home"
       "/sun|00:00 d_nr_44 asleep")
add(id="norman_dent", n="Norman Dent", a=57, s="m", k="regular", cid="filip", called="Norman", proto="norman", v=None,
    r="The night watchman on the warehouse row", home="d_cl_20", die=True, fight="big_man", src="canon; 2.11.1; side story 31",
    rt="daily|00:00 dents_warehouses his round of the row; 07:00 caff breakfast; 07:45 d_cl_20 home to bed; 19:30 dents_warehouses his round of the row")
add(id="grace_rinaldi", n="Grace Rinaldi", a=58, s="f", k="regular", cid="cafe", called="Grace", proto="grace", v=None,
    r="Keeps the caff, her Italian father's before her", home="d_bp_3", die=False, src="canon; side story 11",
    rt="mon-thu|00:00 d_bp_3 asleep; 05:30 caff opening up; 15:30 d_bp_3 home"
       "/fri-sat|00:00 d_bp_3 asleep; 05:30 caff opening up; 22:15 d_bp_3 home"
       "/sun|00:00 d_bp_3 asleep; 07:30 caff Sunday mornings; 12:15 d_bp_3 home")
add(id="peter_tang", n="Peter Tang", a=44, s="m", k="regular", cid="takeaway_m", called="Mr Tang", proto="peter", v=None,
    r="Keeps the takeaway on the parade with his wife; came from the New Territories in 1968", home="d_bp_5", die=False,
    src="canon; side stories 4, 12",
    rt="mon-sat|00:00 d_bp_5 asleep; 10:00 grocer the day's veg; 11:00 d_bp_5 the kitchen, prep; 16:30 tangs_takeaway the counter; 23:45 d_bp_5 home"
       "/sun|00:00 d_bp_5 asleep")
add(id="lily_tang", n="Lily Tang", a=41, s="f", k="regular", cid="takeaway_f", called="Mrs Tang", proto="lily", v=None,
    r="The takeaway's front and its books", home="d_bp_5", die=False, src="canon; side story 4",
    rt="mon-sat|00:00 d_bp_5 asleep; 11:00 d_bp_5 the books; 16:30 tangs_takeaway the front; 23:45 d_bp_5 home"
       "/sun|00:00 d_bp_5 asleep")
add(id="old_firm_man", n="(never named: canon)", a=60, s="m", k="minor", cid="outfit_man", called="the old firm's man", proto=None, v=None,
    r="One of the old firm Mickey's arrangement was with; at the ferry landing after ten; the one old hand who stays on", home="edge_west",
    die=True, fb="Ron's asks come by the outfit's man at the office door (this is that man)", t=None,
    look=L(1.74, 0.5, 0, "flatcap", "#4a4a48", "overcoat", "#22242a", "#3a3a3a", "trousers", "#22242a"),
    card=dict(who="A man of the old firm that worked the landing before the three rivals were anybody. Says 'Mickey's?' and nothing more.",
              speak="Two words at a time.", life="Comes and goes by the landing.", rivals="The old firm needs its envelope and no talk; fears daylight."),
    src="canon (never named); STORY-FRAME 2; hook-cast.json outfit_man",
    rt="daily|00:00 ferry_landing the landing; 01:15 edge_west gone along the quay; 09:00 caff a tea in the corner; 09:45 edge_west gone; 21:45 ferry_landing the landing")

# =========================== frame's proposed people (STORY-FRAME 4; names proposed by the story lane)
add(id="simon_ombler", n="Simon Ombler", a=44, s="m", k="rival_man", cid=None, called="Mr Ombler", inv="frame", proto=None, v=None,
    r="Agar's managing clerk; signs his letters; Agar's lieutenant on the ladder", home="edge_north", die=True,
    fb="the agents' senior partner's letters come by post", t=(0.35, 0.6, 0.4), quiet=True,
    look=L(1.75, 0.35, 0, "parted", "#4a3a2a", "suit", "#3a3a40", "#e8e4dc", "trousers", "#3a3a40", "glasses"),
    card=dict(who="Simon Ombler, 44, Mr Agar's managing clerk. Signs the letters. Keeps the cold-store book in the back room.",
              speak="Thin, polite, 'I am instructed to say'.", life="Up in town; the agents' office on Cold Store Road weekdays.",
              rivals="Agar's lieutenant: takes his ladder at the same rung if Agar falls (RT2-05)."),
    src="STORY-FRAME 4 (proposed); 2.10.2 (a named lieutenant)",
    rt="mon-fri|00:00 edge_north home in town; 09:15 agar_base the front office; 17:15 edge_north home in town"
       "/sat-sun|00:00 edge_north home in town")
add(id="alan_sowerby", n="Alan Sowerby", a=51, s="m", k="minor", cid=None, called="Mr Sowerby", inv="frame", proto=None, v=None,
    r="The council's licensing officer, who has to act on Agar's letters", home="edge_north", die=True, t=(0.3, 0.6, 0.5), quiet=False,
    look=L(1.72, 0.5, 0, "balding", "#8a8078", "suit", "#4a4a40", "#e0d8c8", "trousers", "#4a4a40"),
    card=dict(who="Alan Sowerby, 51, licensing officer. Would rather nobody wrote to him.", speak="Harassed, procedural.",
              life="The council offices up in town; the licensing hearing on Thursdays.", rivals="Answers to the committee, which answers to Agar."),
    src="STORY-FRAME 4 (proposed)",
    rt="mon-wed,fri|00:00 edge_north home in town"
       "/thu|00:00 edge_north home in town; 09:30 licensing the licensing committee; 16:30 edge_north home in town"
       "/sat-sun|00:00 edge_north home in town")
add(id="cyril_pashby", n="Cyril Pashby", a=71, s="m", k="minor", cid=None, called="the Man in Black", inv=True, proto=None, v=None,
    r="Walks behind every old docker's coffin and marks the funeral out of ten, aloud", home="d_cl_33", die=False,
    t=(0.6, 0.3, 0.3), quiet=False,
    look=L(1.70, 0.4, 0, "balding", "#d0ccc4", "overcoat", "#101012", "#101012", "trousers", "#101012", "black_hat"),
    card=dict(who="Cyril Pashby, 71, a retired docker known only as the Man in Black. Walks behind every old docker's coffin and marks the funeral out of ten, aloud.",
              speak="Solemn, deadpan, a mark out of ten for everything.", life="33 Chapel Lane. The chapel steps whenever there is a funeral.",
              rivals="Marks them all."),
    src="STORY-FRAME 4 item 16 (the role proposed; the name invented here)",
    rt="mon-sat|00:00 d_cl_33 asleep; 10:00 chapel the steps; 11:30 caff a tea; 12:30 d_cl_33 home"
       "/sun|00:00 d_cl_33 asleep; 09:30 chapel Mass, in black; 11:00 d_cl_33 home")
add(id="arvids_ozols", n="Arvids Ozols", a=58, s="m", k="minor", cid=None, called="Captain Ozols", inv="frame", proto=None, v=None,
    r="Master of the timber ship held at the wall; a cab to nowhere every night, paid in tinned fish", home="fishing_basin_north", die=True,
    t=(0.6, 0.4, 0.2), quiet=True,
    look=L(1.82, 0.6, 0, "short", "#c8c0b0", "pea_coat", "#1c2230", "#c0a040", "trousers", "#1c2230", "peaked_cap", "beard"),
    card=dict(who="Captain Arvids Ozols, 58, Latvian master of the timber ship held at the basin wall over a debt not his own. Every night a cab 'to nowhere, please, one hour'.",
              speak="Formal English, long pauses, a sailor's courtesy.", life="Aboard his ship at the basin wall.", rivals="None. He wants an hour of moving."),
    src="STORY-FRAME 4 item 17 (proposed); ship's berth provisional (the map has no ship berth: fishing_basin_north stands in)",
    rt="daily|00:00 fishing_basin_north aboard; 21:00 rank_mickeys his cab to nowhere; 22:00 fishing_basin_north aboard")
add(id="stathers", n="Vic Stathers", a=46, s="m", k="rival_man", cid=None, called="Stathers", inv="frame", proto=None, v=None,
    r="The Widow's lieutenant at the dock gate", home="d_cs_17", die=True, fb="the Widow takes the gate herself; her next man is Mark Billany",
    t=(0.75, 0.7, 0.1), quiet=True, fight="big_man",
    look=L(1.86, 0.85, 0, "short", "#3a3a3a", "donkey", "#1c1f26", "#3c4350", "trousers", "#2a2a2a"),
    card=dict(who="Stathers, 46, the Widow's man at the dock gate. Picks the pen at six. Offers Ron his old place in front of Frank.",
              speak="Flat, slow, 'Mrs Jensen says'.", life="17 Cold Store Road; the gate from half past five.",
              rivals="The Widow's lieutenant: takes her ladder at the same rung if she falls (RT2-05)."),
    src="STORY-FRAME 4 item 18 names him Frank Stathers (proposed); first name changed here to Vic because the lead is now Frank (decision of 24 Nov); for the story lane to confirm",
    rt="mon-sat|00:00 d_cs_17 asleep; 05:30 dock_gate the pen; 09:00 widow_base the office below hers; 13:00 dock_gate the hut and the tax; 18:00 d_cs_17 home"
       "/sun|00:00 d_cs_17 asleep; 10:00 chapel Mass, behind her; 11:15 d_cs_17 home")
add(id="mark_billany", n="Mark Billany", a=31, s="m", k="rival_man", cid=None, called="Billany", inv="frame", proto=None, v=None,
    r="The Widow's taxman at the gate and on the ferry rank", home="d_cs_15", die=True, t=(0.55, 0.6, 0.3), quiet=True, fight="brawler",
    look=L(1.80, 0.6, 0, "short", "#5a3a20", "donkey", "#1c1f26", "#e07a1a", "jeans", "#30384a", "cap"),
    card=dict(who="Mark Billany, 31, collects the Widow's tax off the cabs at the dock gate and the ferry rank.",
              speak="Mouthy until hit.", life="15 Cold Store Road.", rivals="The Widow's man."),
    src="STORY-FRAME 7 worked example 3 (proposed)",
    rt="mon-sat|00:00 d_cs_15 asleep; 06:00 dock_gate the tax hut; 12:00 caff dinner; 13:00 rank_ferry the tax on the ferry rank; 17:00 widow_base the take; 18:00 d_cs_15 home"
       "/sun|00:00 d_cs_15 asleep")
add(id="steve_brannigan", n="Steve Brannigan", a=38, s="m", k="rival_man", cid=None, called="Brannigan", inv=True, proto=None, v=None,
    r="The Widow's man at the net store and the van", home="d_cs_11", die=True, t=(0.6, 0.65, 0.2), quiet=True, fight="boxer",
    look=L(1.78, 0.65, 0, "short", "#2a2a2a", "car_coat", "#3a3028", "#2a2a2a", "trousers", "#2a2a2a"),
    card=dict(who="Steve Brannigan, 38, Irish-born, boxed for the club once. Minds the net store and drives the Widow's van to the last boat.",
              speak="Soft-spoken, Irish, polite to a fault before a fight.", life="11 Cold Store Road.", rivals="The Widow's man."),
    src="invented: 2.10.2 (three named men each)",
    rt="mon-sat|00:00 d_cs_11 asleep; 08:00 widow_base the net store; 16:00 boxing_club the club; 18:00 d_cs_11 home; 21:30 widow_base the van; 23:30 d_cs_11 home"
       "/sun|00:00 d_cs_11 asleep")
add(id="dougie_saltmarsh", n="Dougie Saltmarsh", a=29, s="m", k="rival_man", cid=None, called="Dougie", inv=True, proto=None, v=None,
    r="The Widow's man on the fish dock and the cold-store yard", home="d_nr_43", die=True, t=(0.5, 0.5, 0.4), quiet=True, fight="wiry",
    look=L(1.74, 0.4, 0, "short", "#a07040", "anorak", "#2a3a2a", "#2a2a2a", "jeans", "#30384a"),
    card=dict(who="Dougie Saltmarsh, 29, takes the porters' cut on the fish dock for the Widow and watches the cold-store yard.",
              speak="Quick, sly, laughs at his own jokes.", life="43 North Road.", rivals="The Widow's man; the porter answers to him."),
    src="invented: 2.10.2; side story 8 (the syndicate's man who takes the porters' cut)",
    rt="mon-sat|00:00 d_nr_43 asleep; 05:00 fish_dock the porters' cut; 09:00 cold_stores the yard gate; 14:00 snooker_hall the tables; 18:00 d_nr_43 home"
       "/sun|00:00 d_nr_43 asleep")
add(id="craig_fewson", n="Craig Fewson", a=25, s="m", k="rival_man", cid=None, called="Fewson", inv="frame", proto=None, v=None,
    r="Danny's lieutenant, who wants Danny's seat", home="d_nr_39", die=True, fb="the oldest of Danny's men takes the ladder",
    t=(0.65, 0.4, 0.3), quiet=True, fight="brawler",
    look=L(1.83, 0.6, 0, "short", "#1a1a1a", "bomber", "#1a2a1a", "#c85a1a", "jeans", "#2a3550"),
    card=dict(who="Craig Fewson, 25, Danny's lieutenant. Wants Danny's seat and his key.",
              speak="Few words, a stare.", life="39 North Road; the lock-ups.", rivals="If Danny is dead or gone, the man on the quay (STORY-FRAME 6)."),
    src="STORY-FRAME 4 item 18 (proposed)",
    rt="mon-sat|00:00 d_nr_39 asleep; 11:00 cammack_base the lock-ups; 14:00 rank_ferry watching the ferry rank; 16:00 cammack_base the lock-ups; 20:00 snooker_hall with Danny; 23:00 d_nr_39 home"
       "/sun|00:00 d_nr_39 asleep; 13:00 cammack_base the lock-ups; 18:00 d_nr_39 home")
add(id="shane_boddy", n="Shane Boddy", a=23, s="m", k="rival_man", cid=None, called="Shane", inv=True, proto=None, v=None,
    r="One of Danny's crew; sold the chapel's lead to Iveson", home="d_nr_34", die=True, t=(0.45, 0.45, 0.5), quiet=False, fight="brawler",
    look=L(1.79, 0.45, 0, "spiky", "#c09050", "shell", "#2a5a8a", "#e0e0e0", "trackies", "#2a2360"),
    card=dict(who="Shane Boddy, 23, Danny's crew. Did the chapel roof's lead with Wes and sold it to Dennis Iveson.",
              speak="Loud, cocky, laughs too long.", life="34 North Road with his mother.", rivals="Danny's man; Rita fences for him."),
    src="invented: 2.10.2; side story 23 (two of Danny's men)",
    rt="mon-sat|00:00 d_nr_34 asleep; 12:00 caff late breakfast; 13:00 cammack_base the lock-ups; 17:00 phone_parade the corner by the phone box; 20:00 snooker_hall the tables; 23:00 d_nr_34 home"
       "/sun|00:00 d_nr_34 asleep")
add(id="wes_akers", n="Wes Akers", a=26, s="m", k="rival_man", cid=None, called="Wes", inv=True, proto=None, v=None,
    r="One of Danny's crew; the car radios in the empty warehouse", home="d_nr_32", die=True, t=(0.55, 0.5, 0.3), quiet=True, fight="knife_man",
    look=L(1.76, 0.4, 0, "short", "#2a2018", "leather", "#1a1a1e", "#1a1a1e", "jeans", "#2a3550"),
    card=dict(who="Wes Akers, 26, Danny's crew. Keeps the car radios in the empty warehouse on the row.",
              speak="Quiet, flat, carries a blade he never shows first.", life="32 North Road.", rivals="Danny's man."),
    src="invented: 2.10.2; side stories 23, 31",
    rt="mon-sat|00:00 net_loft the crates; 02:30 d_nr_32 asleep; 13:00 cammack_base the lock-ups; 18:00 caff his tea; 19:00 cammack_base the lock-ups; 22:30 net_loft the crates"
       "/sun|00:00 d_nr_32 asleep; 14:00 cammack_base the lock-ups; 18:00 d_nr_32 home")
add(id="jason_pinder", n="Jason Pinder", a=20, s="m", k="rival_man", cid=None, called="the lad", inv=True, proto=None, v=None,
    r="The newest of Danny's crew; put the caff's window in", home="d_nr_28", die=True, t=(0.35, 0.3, 0.6), quiet=False, fight="wiry",
    look=L(1.74, 0.3, 0, "curtains", "#8a6a4a", "shell", "#6a2a6a", "#2ab3a6", "trackies", "#2a2a40"),
    card=dict(who="Jason Pinder, 20, the newest of Danny's crew. Put Grace's window in for a dare. The one Frank can turn.",
              speak="Nervous bravado, 'I never'.", life="28 North Road with his gran.", rivals="Danny's newest; low loyalty (STORY-FRAME 4 item 15)."),
    src="invented: side story 11 (a young man of about twenty); STORY-FRAME 4 item 15",
    rt="mon-sat|00:00 d_nr_28 asleep; 11:30 phone_parade the corner; 13:00 cammack_base the lock-ups; 17:00 phone_parade the corner; 21:00 tangs_takeaway outside at closing; 23:00 d_nr_28 home"
       "/sun|00:00 d_nr_28 asleep")
add(id="barry_coult", n="Barry Coult", a=42, s="m", k="rival_man", cid=None, called="Coult", inv=True, proto=None, v=None,
    r="A bailiff from away, hired on Agar's paper; leads the men at the cold store", home="edge_north", die=True, t=(0.7, 0.5, 0.4), quiet=True, fight="big_man",
    look=L(1.88, 0.85, 0, "shaved", "#3a3a3a", "car_coat", "#2a2a2a", "#2a2a2a", "trousers", "#2a2a2a"),
    card=dict(who="Barry Coult, 42, a certificated bailiff from away who does what Agar's paper says. Leads the men who shut the cold store's door man in.",
              speak="Officious, 'I've a warrant for that'.", life="Comes and goes in a van from up the coast.", rivals="Agar's man while the paper lasts."),
    src="invented: 2.10.2; STORY-FRAME 5 (men from away, hired on Agar's paper)",
    rt="tue,fri|00:00 edge_north from away; 10:00 agar_base his instructions; 11:00 cold_stores the yard; 15:00 edge_north gone"
       "/mon,wed,thu,sat,sun|00:00 edge_north from away")
add(id="ray_spink", n="Ray Spink", a=37, s="m", k="rival_man", cid=None, called="Spink", inv=True, proto=None, v=None,
    r="Coult's man; one of the men from away", home="edge_north", die=True, t=(0.5, 0.4, 0.5), quiet=True, fight="brawler",
    look=L(1.80, 0.7, 0, "short", "#5a4a3a", "donkey", "#2a2e36", "#2a2e36", "jeans", "#30384a"),
    card=dict(who="Ray Spink, 37, Coult's second, a hired man from away.", speak="Grunts.", life="From away.", rivals="Agar's paper."),
    src="invented: 2.10.2",
    rt="tue,fri|00:00 edge_north from away; 10:00 agar_base waiting outside; 11:00 cold_stores the yard; 15:00 edge_north gone"
       "/mon,wed,thu,sat,sun|00:00 edge_north from away")
add(id="kenny_varley", n="Kenny Varley", a=33, s="m", k="rival_man", cid=None, called="Varley", inv=True, proto=None, v=None,
    r="Coult's driver; one of the men from away", home="edge_north", die=True, t=(0.4, 0.4, 0.5), quiet=False, fight="wiry",
    look=L(1.72, 0.4, 0, "short", "#2a2018", "anorak", "#3a3a40", "#2a2a2a", "jeans", "#30384a"),
    card=dict(who="Kenny Varley, 33, drives Coult's van.", speak="Nervous, chatty when scared.", life="From away.", rivals="Agar's paper."),
    src="invented: 2.10.2",
    rt="tue,fri|00:00 edge_north from away; 10:00 agar_base the van; 11:00 cold_stores the van in the yard; 15:00 edge_north gone"
       "/mon,wed,thu,sat,sun|00:00 edge_north from away")
add(id="eric_tharratt", n="Eric Tharratt", a=54, s="m", k="minor", cid=None, called="Mr Tharratt", inv="frame", proto=None, v=None,
    r="Shift manager at the Old Basin Cold Stores; gives the contract", home="edge_north", die=True,
    fb="Malcolm Ruddock, his deputy, holds the contract (RT2-05)", t=(0.4, 0.6, 0.3), quiet=False,
    look=L(1.76, 0.6, 0, "balding", "#7a7068", "warehouse_coat", "#e0dcd0", "#3a3a3a", "trousers", "#2a2a2a", "clipboard"),
    card=dict(who="Eric Tharratt, 54, shift manager at the cold stores. Will talk once a firm with four cars meets the packing shift on time five mornings in one week.",
              speak="Clock-watching, terse, 'five mornings, then we'll talk'.", life="Up in town; the cold stores from half past five.",
              rivals="Agar holds the road; the Widow holds the gate; he wants his shift in on time."),
    src="STORY-FRAME 4 item 19 (proposed); replaces wave 1's placeholder 'Norman (the cold-store manager)'",
    rt="mon-fri|00:00 edge_north home in town; 05:30 cold_stores the packing shift; 17:45 edge_north home in town"
       "/sat|00:00 edge_north home in town; 05:30 cold_stores Saturday shift; 13:15 edge_north home in town"
       "/sun|00:00 edge_north home in town")
add(id="derek_hebblewhite", n="Derek Hebblewhite", a=49, s="m", k="officer", cid=None, called="Mr Hebblewhite", inv="frame", proto=None, v=None,
    r="VAT officer, Customs and Excise; Act III's inspector; first met in week four as a fare who asks for a receipt", home="edge_north", die=False,
    t=(0.5, 0.9, 0.7), quiet=False,
    look=L(1.74, 0.45, 0, "parted", "#6a6058", "raincoat", "#8a8070", "#3a3a40", "trousers", "#3a3a40", "glasses", "briefcase"),
    card=dict(who="Derek Hebblewhite, 49, VAT officer. Reads dents and receipts. Spells Nowak right.",
              speak="Polite, unhurried, 'produce it, or ask for it in writing'.", life="Up in town; at the counter on the inspection mornings.",
              rivals="Customs and Excise wants books that match."),
    src="STORY-FRAME 4 item 19, 5 Act III (proposed)",
    rt="daily|00:00 edge_north up in town")
add(id="trevor_garton", n="Trevor Garton", a=34, s="m", k="officer", cid=None, called="PC Garton", inv="frame", proto=None, v=None,
    r="Patrol car constable; bought: looks away from a car once (50 pounds)", home="edge_north", die=True, fb="the second constable", t=(0.5, 0.3, 0.4), quiet=True,
    look=L(1.82, 0.6, 0, "short", "#3a2a1a", "tunic", "#14161c", "#c9c9c9", "trousers", "#14161c", "cap"),
    card=dict(who="PC Trevor Garton, 34, drives the patrol car. Will look away from a car once, for fifty pounds.", speak="Bluff, matey, 'not my business, sir'.",
              life="The station; the patrol car's round.", rivals="Ellis would have his warrant card."),
    src="STORY-FRAME 2 (proposed); 2.6.8; police.json bought_look_away (whose prototype hint was PC Harker)",
    rt="mon-fri|00:00 edge_north home; 14:00 police_station the late turn; 15:00 rank_north the patrol car's stop; 15:30 police_station the patrol car's round (police.json); 22:00 edge_north home"
       "/sat-sun|00:00 edge_north home")
add(id="graham_wardell", n="Graham Wardell", a=37, s="m", k="officer", cid=None, called="DC Wardell", inv="frame", proto=None, v=None,
    r="Detective constable; bought: loses a statement once (200 pounds); a possible source of the tip", home="edge_north", die=True, t=(0.4, 0.2, 0.5), quiet=True,
    look=L(1.78, 0.5, 0, "short", "#4a3a2a", "suit", "#3a3a40", "#c8c0b0", "trousers", "#3a3a40"),
    card=dict(who="DC Graham Wardell, 37, works under Ellis. Will lose a statement once, for two hundred pounds. Ellis notices.", speak="Smooth, quick, never in writing.",
              life="The station.", rivals="Owes money in town; Ellis is his sergeant."),
    src="STORY-FRAME 2 (proposed); 2.6.8; police.json bought_lose_statement (whose prototype hint was DC Pollitt)",
    rt="mon-fri|00:00 edge_north home; 09:00 police_station CID; 13:00 caff a bacon sandwich; 13:45 police_station CID; 18:00 edge_north home"
       "/sat-sun|00:00 edge_north home")
add(id="neil_screeton", n="Neil Screeton", a=26, s="m", k="minor", cid=None, called="Iveson's lad", inv="frame", proto=None, v=None,
    r="Iveson's yard hand; chains the crane gap at five", home="d_nr_26", die=True, t=(0.6, 0.6, 0.3), quiet=True, fight="big_man",
    look=L(1.90, 0.9, 0, "short", "#6a4a2a", "overall", "#4a3a2a", "#2a2a2a", "jeans", "#30384a"),
    card=dict(who="Neil Screeton, 26, Dennis Iveson's yard hand. Chains the crane gap at five every evening since the fire.",
              speak="Slow, literal, keeps count.", life="26 North Road.", rivals="Iveson's lad; the hardest fight in the yard if fronted up (STORY-FRAME 7)."),
    src="STORY-FRAME 7 worked example 2 (proposed); 2.8.1 (a yard hand in his twenties)",
    rt="mon-sat|00:00 d_nr_26 asleep; 07:30 iveson_yard the yard; 17:00 iveson_yard chains the gap; 17:15 boxing_club the bag; 19:00 d_nr_26 home"
       "/sun|00:00 d_nr_26 asleep")

# =========================== the law, unnamed in the frame (named here or from wave 1)
add(id="pc_ibbotson", n="Martin Ibbotson", a=29, s="m", k="officer", cid=None, called="the constable", inv=True, proto="pc", v=None,
    r="The beat constable: Quay Street and the north road by day, the night beat 22:00 to 06:00 on his night weeks", home="edge_north", die=True,
    fb="the second constable takes his beat from the next night (RT2-05)", src="prototype cast.js pc (PC Ibbotson, kept by wave 1 ledger-texts); 2.6.1; FIT-L01; first name invented",
    rt="mon-fri|00:00 edge_north off duty; 08:00 police_station parade; 08:30 mickeys the day beat, Quay Street (police.json); 12:30 caff his break; 13:00 cold_stores the day beat, the north road to the cold-store road (police.json); 16:00 police_station off duty; 16:30 edge_north off duty"
       "/sat-sun|00:00 edge_north off duty")
add(id="pc_haigh", n="Brian Haigh", a=45, s="m", k="officer", cid=None, called="the other constable", inv=True, proto=None, v=None,
    r="The night beat constable (police.json's beat, 22:00 to 06:00); takes the day beat if Ibbotson is gone", home="edge_north", die=True,
    fb="a constable from town", t=(0.6, 0.8, 0.8), quiet=False,
    look=L(1.80, 0.7, 0, "helmet", "#14161c", "tunic", "#14161c", "#c9c9c9", "trousers", "#14161c", "torch"),
    card=dict(who="PC Brian Haigh, 45, walks the Hook's night beat: the short round past Mickey's door, then the landing leg.",
              speak="Slow, heavy, 'now then', a cough before he turns a corner.", life="The station; the night beat.", rivals="Honest, and tired of the Hook."),
    src="invented: 2.6.1 (the beat constable's night round); RT2-05 (the second constable); timetables beat",
    rt="daily|00:00 mickeys the night beat (police.json); 06:00 police_station off duty; 06:30 edge_north asleep; 21:30 police_station parade; 22:00 mickeys the night beat (police.json)")
add(id="sgt_bellwood", n="Roy Bellwood", a=52, s="m", k="officer", cid=None, called="the custody sergeant", inv=True, proto=None, v=None,
    r="The custody sergeant: three goes at 'Nowak'", home="edge_north", die=False, t=(0.6, 0.8, 0.6), quiet=False,
    look=L(1.78, 0.75, 0, "short", "#a09a90", "shirt", "#e8e8f0", "#14161c", "trousers", "#14161c", "stripes"),
    card=dict(who="Sergeant Roy Bellwood, 52, the custody desk. Cannot say Nowak; tries three times.", speak="Weary, comic, by the book.",
              life="The station's custody desk.", rivals="Has seen every face on the Hook through the hatch."),
    src="invented: STORY-FRAME 5 (the sergeant's three goes at Nowak)", rt="daily|00:00 police_station the custody desk")

# =========================== the empire's minor roles (2.15, RT2-05, RT-03 and the jobs)
add(id="clive_ackroyd", n="Clive Ackroyd", a=48, s="m", k="minor", cid=None, called="Clive", inv=True, proto=None, v=None,
    r="Owner of Portside Cars, the other minicab firm on the north rank (two cars); a business, never a rival", home="edge_north", die=True,
    t=(0.4, 0.5, 0.5), quiet=False,
    look=L(1.74, 0.65, 0, "balding", "#6a6058", "car_coat", "#5a4a36", "#2a2a2a", "trousers", "#30302e"),
    card=dict(who="Clive Ackroyd, 48, runs Portside Cars from the north rank with two cars. Takes the fares Mickey's loses and gives them back as the talk fades.",
              speak="Grumbling, businesslike.", life="Up in town; the north rank by day.", rivals="None: a business (2.15.3)."),
    src="invented: 2.15.3; vehicles.json portside_cars (the prototype's hint Len Wardle: surname changed so it is not mistaken for DC Wardell)",
    rt="mon-sat|00:00 edge_north home; 07:00 rank_north his cars; 19:00 edge_north home"
       "/sun|00:00 edge_north home")
add(id="malcolm_ruddock", n="Malcolm Ruddock", a=39, s="m", k="minor", cid=None, called="Ruddock", inv=True, proto=None, v=None,
    r="The cold-store manager's deputy; holds the contract if Tharratt is gone; sells a key", home="d_cs_5", die=True, t=(0.35, 0.3, 0.7), quiet=False,
    look=L(1.75, 0.55, 0, "short", "#4a3a2a", "warehouse_coat", "#e0dcd0", "#3a3a3a", "trousers", "#2a2a2a"),
    card=dict(who="Malcolm Ruddock, 39, deputy at the cold stores. Has the keys and money troubles.", speak="Shifty, ingratiating.",
              life="5 Cold Store Road.", rivals="Will sell a key to anybody (STORY-FRAME 5)."),
    src="invented: RT2-05 (the cold-store manager's deputy); STORY-FRAME 5",
    rt="mon-fri|00:00 d_cs_5 asleep; 05:30 cold_stores the yard; 14:00 d_cs_5 home; 19:00 snooker_hall a frame; 21:30 d_cs_5 home"
       "/sat|00:00 d_cs_5 asleep; 05:30 cold_stores Saturday shift; 13:15 d_cs_5 home"
       "/sun|00:00 d_cs_5 asleep")
add(id="alf_garside", n="Alf Garside", a=61, s="m", k="minor", cid=None, called="the ship's cook", inv=True, proto=None, v=None,
    r="The dock gun seller: an old ship's cook ashore who has things from abroad", home="chandlery", die=True,
    fb="guns come the other three ways (RT2-05)", t=(0.5, 0.2, 0.8), quiet=True,
    look=L(1.70, 0.7, 0, "flatcap", "#5a5048", "jersey", "#3a3a3a", "#3a3a3a", "trousers", "#2a2a2a", "tattoos"),
    card=dict(who="Alf Garside, 61, a ship's cook ashore. Has had things from abroad in a biscuit tin under the stove for thirty years.",
              speak="Gruff, coded, 'I might know a man'.", life="Lives over the chandler's store; the fish dock at dawn for scraps.", rivals="Sells to anybody, tells nobody."),
    src="invented: RT2-05 (the dock gun seller)",
    rt="daily|00:00 chandlery asleep upstairs; 06:00 fish_dock scraps off the boats; 08:00 chandlery the back room; 20:00 tea_stall a mug at the stall; 21:00 chandlery asleep upstairs")
add(id="bernard_gill", n="Bernard Gill", a=55, s="m", k="minor", cid=None, called="the car-lot man", inv=True, proto=None, v=None,
    r="The used-car lot by the north road; cars at 600 to 1,200 pounds", home="edge_north", die=True,
    fb="cars come from a man selling one (RT2-05)", t=(0.4, 0.3, 0.7), quiet=False,
    look=L(1.76, 0.75, 0, "comb_over", "#6a5a4a", "sheepskin", "#8a6a4a", "#e0d0b0", "trousers", "#3a3630"),
    card=dict(who="Bernard Gill, 55, sells used cars off the lot by the north road. Every car one careful owner.", speak="Patter, 'I'll not lie to you'.",
              life="The lot's hut.", rivals="Sells to all three."),
    src="invented: 2.15.1; RT2-05 (the car-lot man)",
    rt="mon-sat|00:00 edge_north home; 08:45 car_lot the lot's hut; 17:15 edge_north home"
       "/sun|00:00 edge_north home")
add(id="leonard_askew", n="Leonard Askew", a=58, s="m", k="minor", cid=None, called="Mr Askew", inv=True, proto=None, v=None,
    r="The landlord's agent (Agar & Co's agents): Mickey's rent at the counter on Fridays, Ada's rent", home="edge_north", die=True,
    fb="letters by post (RT2-05)", t=(0.4, 0.6, 0.5), quiet=False,
    look=L(1.72, 0.5, 0, "parted", "#9a9088", "overcoat", "#4a4a40", "#2a2a2a", "trousers", "#3a3a40", "rent_book"),
    card=dict(who="Leonard Askew, 58, Agar & Co's agent. Calls at Mickey's counter every Friday at eleven for the flat's eighteen pounds.", speak="Dry, punctual, 'I only collect it'.",
              life="The agents' office.", rivals="Agar's agent."),
    src="timetables.json weekly rent (Mr Leonard Askew, chosen there from letters-and-print.json); RT2-05 (the landlord's agent)",
    rt="mon-thu|00:00 edge_north home; 09:30 agar_base the agents' office; 17:00 edge_north home"
       "/fri|00:00 edge_north home; 09:30 agar_base the agents' office; 11:00 mickeys the rent at the counter; 12:00 agar_base the agents' office; 17:00 edge_north home"
       "/sat-sun|00:00 edge_north home")
add(id="aidan_keogh", n="Aidan Keogh", a=69, s="m", k="minor", cid=None, called="the old doctor", inv=True, proto=None, v=None,
    r="The retired doctor on Chapel Lane who stitches by knock for fifteen pounds and remembers every face", home="doctors", die=False,
    t=(0.6, 0.3, 0.2), quiet=True,
    look=L(1.75, 0.45, 0, "white", "#e0dcd4", "cardigan", "#5a5a48", "#d0c8b0", "trousers", "#3a3a34", "glasses", "bag"),
    card=dict(who="Dr Aidan Keogh, 69, Dublin-trained, retired from a practice in town. Stitches what comes to his door at 23 Chapel Lane and asks nothing. Fifteen pounds.",
              speak="Dry, Irish, clinical, 'hold still'.", life="23 Chapel Lane; the Infirmary's porch some nights.", rivals="Remembers every face."),
    src="invented: 1.3.11 (the stitching doctor); prototype fares doctor_night",
    rt="mon-sat|00:00 doctors asleep; 08:00 doctors by knock; 21:00 doctors asleep"
       "/sun|00:00 doctors asleep; 09:30 chapel Mass; 11:00 doctors by knock; 21:00 doctors asleep")
add(id="harry_holt", n="Harry Holt", a=50, s="m", k="minor", cid=None, called="Holt", inv=True, proto=None, v=None,
    r="Keeps Holt's garage on Cold Store Road; the tyre man and the recovery truck", home="d_nr_18", die=True, t=(0.5, 0.4, 0.5), quiet=False,
    look=L(1.78, 0.7, 0, "short", "#4a4038", "overall", "#3a4a3a", "#2a2a2a", "trousers", "#2a2a2a"),
    card=dict(who="Harry Holt, 50, keeps the garage on Cold Store Road. Mends what the rivals break, for money and a day.", speak="Cheerful, oily, quotes by the hour.",
              life="18 North Road.", rivals="Mends everybody's cars."),
    src="wave 1 places.json Holt (surname kept); first name invented; RT-06 (the tyre man)",
    rt="mon-fri|00:00 d_nr_18 asleep; 07:45 garage the workshop; 17:45 d_nr_18 home"
       "/sat|00:00 d_nr_18 asleep; 07:45 garage Saturday mornings; 12:15 d_nr_18 home"
       "/sun|00:00 d_nr_18 asleep")
add(id="phil_rawling", n="Phil Rawling", a=44, s="m", k="minor", cid=None, called="the glazier", inv=True, proto=None, v=None,
    r="The glazier: puts in what the Widow's men put out, for money and a day", home="edge_north", die=True, t=(0.4, 0.4, 0.5), quiet=False,
    look=L(1.76, 0.5, 0, "short", "#5a4a3a", "overall", "#d8d0c0", "#3a3a3a", "trousers", "#3a3a3a"),
    card=dict(who="Phil Rawling, 44, glazier from town with a van and a rack. Comes the next day.", speak="Tuts, 'that's a big pane'.", life="Up in town.", rivals="Fixes everybody's windows."),
    src="invented: RT-06 (the glazier)", rt="daily|00:00 edge_north up in town")
add(id="wilf_hardcastle", n="Wilf Hardcastle", a=72, s="m", k="minor", cid=None, called="the bird man", inv=True, proto=None, v=None,
    r="Keeps the pigeon loft at the back of the allotments", home="d_cl_31", die=False, t=(0.4, 0.3, 0.3), quiet=False,
    look=L(1.68, 0.45, 0, "flatcap", "#7a7068", "jacket", "#5a5a40", "#3a3a30", "trousers", "#3a3a30"),
    card=dict(who="Wilf Hardcastle, 72, keeps the pigeons at the back of the allotments. Tells the time by when the birds come home.", speak="Slow, fond, all about birds.",
              life="31 Chapel Lane; the loft from seven.", rivals="Has watched the quay from the loft roof forty years."),
    src="invented: places.json pigeon_loft ('the bird man of the allotments (people file)')",
    rt="daily|00:00 d_cl_31 asleep; 07:00 pigeon_loft the birds; 12:00 d_cl_31 his dinner; 14:00 pigeon_loft the birds; 18:30 d_cl_31 home")
add(id="edna_coulson", n="Edna Coulson", a=59, s="f", k="minor", cid=None, called="the cleaner", inv=True, proto=None, v=None,
    r="The cleaner at six: the Harbour Board, then the Copper Kettle and Agar's agents; a finder (2.5.5)", home="d_cl_7", die=True,
    t=(0.45, 0.3, 0.6), quiet=False,
    look=L(1.58, 0.55, 0, "headscarf", "#8a5a4a", "overall", "#7a5a7a", "#e0d8c8", "skirt", "#3a3a40", "bucket"),
    card=dict(who="Edna Coulson, 59, cleans the Harbour Board from six, then the tea room and the agents' office. Finds what the night left.", speak="Tutting, nosy, 'I'm not paid to see that'.",
              life="7 Chapel Lane.", rivals="Tells Nora Cronin everything."),
    src="invented: 2.5.5 (the cleaner at six)",
    rt="mon-fri|00:00 d_cl_7 asleep; 05:45 harbour_board cleaning, from six; 08:00 tea_room cleaning; 08:45 agar_base cleaning; 09:30 d_cl_7 home"
       "/sat|00:00 d_cl_7 asleep; 06:00 harbour_board Saturday clean; 08:00 d_cl_7 home"
       "/sun|00:00 d_cl_7 asleep; 09:30 chapel Mass; 11:00 d_cl_7 home")
add(id="bill_huxtable", n="Bill Huxtable", a=48, s="m", k="minor", cid=None, called="Bill", inv=True, proto=None, v=None,
    r="The first dock worker along the quay each morning (05:15, past the landing and the fish dock to the pen); a finder (2.5.5)", home="d_nr_1", die=True,
    t=(0.5, 0.4, 0.4), quiet=False, fight="big_man",
    look=L(1.84, 0.8, 0, "flatcap", "#4a4a48", "donkey", "#1c1f26", "#e07a1a", "trousers", "#2a2a2a", "bait_tin"),
    card=dict(who="Bill Huxtable, 48, docker since he was fifteen. First along the quay every morning; at the pen before anybody.", speak="Short, dry, 'mornin''.",
              life="1 North Road.", rivals="Pays the Widow's men like everybody; respects Ron."),
    src="invented: 2.5.5 (the first dock worker)",
    rt="mon-sat|00:00 d_nr_1 asleep; 05:15 ferry_landing along the quay; 05:30 fish_dock past the boxes; 05:45 dock_gate the pen; 14:30 caff his tea; 15:15 d_nr_1 home"
       "/sun|00:00 d_nr_1 asleep")
add(id="jimmy_raw", n="Jimmy Raw", a=35, s="m", k="minor", cid=None, called="a docker", inv=True, proto=None, v=None,
    r="A docker from the pen; one of the two dockers by car two who rob a beaten man (RT2-13)", home="d_nr_2", die=True, t=(0.55, 0.4, 0.4), quiet=True, fight="brawler",
    look=L(1.80, 0.7, 0, "short", "#3a2a1a", "donkey", "#1c1f26", "#e07a1a", "jeans", "#30384a"),
    card=dict(who="Jimmy Raw, 35, picked at the pen three days in five. Drinks tea at the caff and fights for money.", speak="Loud, jeering.",
              life="2 North Road.", rivals="Picks a fight for the Widow's men when told."),
    src="invented: RT2-13 (the dockers by car two); 1.3.12",
    rt="mon-sat|00:00 d_nr_2 asleep; 05:45 dock_gate the pen; 14:00 rank_mickeys by car two; 15:30 caff tea; 17:00 d_nr_2 home"
       "/sun|00:00 d_nr_2 asleep")
add(id="ken_swales", n="Ken Swales", a=40, s="m", k="minor", cid=None, called="a docker", inv=True, proto=None, v=None,
    r="A docker from the pen; Jimmy Raw's mate by car two (RT2-13)", home="d_nr_3", die=True, t=(0.5, 0.4, 0.4), quiet=True, fight="big_man",
    look=L(1.86, 0.85, 0, "shaved", "#3a3a3a", "donkey", "#1c1f26", "#e07a1a", "trousers", "#2a2a2a"),
    card=dict(who="Ken Swales, 40, a big docker who follows Jimmy Raw.", speak="Says nothing; laughs when Jimmy does.", life="3 North Road.", rivals="Same as Jimmy."),
    src="invented: RT2-13; 1.3.12",
    rt="mon-sat|00:00 d_nr_3 asleep; 05:45 dock_gate the pen; 14:00 rank_mickeys by car two with Jimmy; 15:30 caff tea; 17:00 d_nr_3 home"
       "/sun|00:00 d_nr_3 asleep")
add(id="eddie_birtwhistle", n="Eddie Birtwhistle", a=46, s="m", k="minor", cid=None, called="the porter", inv=True, proto=None, v=None,
    r="The fish-dock porter who signs for Brenda's boxes and takes them under her name", home="d_nr_4", die=True, t=(0.35, 0.3, 0.7), quiet=True, fight="wiry",
    look=L(1.72, 0.45, 0, "woolly", "#2a2a30", "smock", "#3a6a8a", "#e8e8e8", "waders", "#2a2a2a"),
    card=dict(who="Eddie Birtwhistle, 46, porter on the fish dock. Signs for boxes, and lately signs for some twice.", speak="Wheedling, 'more than my job's worth'.",
              life="4 North Road.", rivals="Pays Dougie Saltmarsh the porters' cut."),
    src="invented: side story 8 (the porter)",
    rt="mon-sat|00:00 d_nr_4 asleep; 04:45 fish_dock the boxes; 11:00 caff his dinner; 12:00 d_nr_4 home"
       "/sun|00:00 d_nr_4 asleep")
add(id="victor_tasker", n="Victor Tasker", a=60, s="m", k="minor", cid=None, called="the laundry's owner", inv=True, proto=None, v=None,
    r="Owns the laundry; held back Julie's last weeks' money", home="edge_north", die=True, t=(0.3, 0.3, 0.8), quiet=False,
    look=L(1.70, 0.7, 0, "comb_over", "#8a8078", "suit", "#4a4038", "#e0d8c8", "trousers", "#4a4038"),
    card=dict(who="Victor Tasker, 60, owns the laundry (the Washeteria and its back rooms). Held back the laid-off girls' last weeks.", speak="Pompous, aggrieved.",
              life="Up in town; the laundry office mornings.", rivals="Complains to the Harbour Board clerk."),
    src="invented: side story 9 (the laundry's owner); the steam laundry and the Washeteria are one place on wave 1's map",
    rt="mon-fri|00:00 edge_north home in town; 09:30 launderette the office; 12:30 edge_north home in town"
       "/sat-sun|00:00 edge_north home in town")
add(id="margaret_lofthouse", n="Margaret Lofthouse", a=47, s="f", k="minor", cid=None, called="the poster woman", inv=True, proto=None, v=None,
    r="Organiser for Meridian Against the Poll Tax (the town's own invented campaign); from Fairview", home="edge_north", die=True, t=(0.7, 0.6, 0.6), quiet=False,
    look=L(1.66, 0.45, 0, "short", "#5a3a2a", "anorak", "#6a2a2a", "#e0d8c8", "jeans", "#3a4a66", "posters"),
    card=dict(who="Margaret Lofthouse, 47, from Fairview, organises the town's campaign against the poll tax. Paste bucket and a roll of posters.", speak="Brisk, cheerful, certain.",
              life="Comes down on the bus mornings.", rivals="None of the three; the council."),
    src="invented: side story 14; letters-and-print.json (Meridian Against the Poll Tax)",
    rt="mon,wed,fri|00:00 edge_north home; 07:00 mickeys a poster on the glass; 08:00 market_stalls_quay leaflets; 10:00 edge_north home"
       "/tue,thu,sat,sun|00:00 edge_north home")
add(id="stan_pickles", n="Stan Pickles", a=57, s="m", k="minor", cid=None, called="the works man", inv=True, proto=None, v=None,
    r="The Harbour Board's works man, who can get a lamp seen to for a favour", home="edge_north", die=True, t=(0.4, 0.3, 0.6), quiet=False,
    look=L(1.74, 0.6, 0, "flatcap", "#5a5048", "donkey", "#2a2e36", "#e0c040", "trousers", "#2a2a2a"),
    card=dict(who="Stan Pickles, 57, the Harbour Board's works man. A lamp, a bollard, a gate: for a favour.", speak="Slow, 'I'll see what I can do'.",
              life="The Board's yard by the dock gate.", rivals="Owes the Widow, like most at the gate."),
    src="invented: side story 30 (the harbour office's works man)",
    rt="mon-fri|00:00 edge_north home; 07:30 harbour_board the works yard; 12:00 caff dinner; 12:45 harbour_board the works yard; 16:30 edge_north home"
       "/sat-sun|00:00 edge_north home")
add(id="rodney_usher", n="Rodney Usher", a=33, s="m", k="minor", cid=None, called="the shipping clerk", inv=True, proto=None, v=None,
    r="A Harbour Board clerk who sells the times of shipments (RT-03)", home="d_nr_10", die=True, t=(0.3, 0.2, 0.7), quiet=False,
    look=L(1.76, 0.35, 0, "parted", "#3a2a1a", "suit", "#4a4a50", "#e0d8c8", "trousers", "#4a4a50", "glasses"),
    card=dict(who="Rodney Usher, 33, a clerk in the Harbour Board's back office. Knows every ship's time and sells them at the snooker hall.", speak="Smarmy, whispering.",
              life="10 North Road.", rivals="Sells to the Widow too."),
    src="invented: RT-03 (a clerk who sells times of shipments)",
    rt="mon-fri|00:00 d_nr_10 asleep; 08:45 harbour_board the back office; 17:00 snooker_hall the tables; 20:00 d_nr_10 home"
       "/sat|00:00 d_nr_10 asleep; 14:00 snooker_hall the tables; 18:00 d_nr_10 home"
       "/sun|00:00 d_nr_10 asleep")
add(id="douglas_fenwick", n="Douglas Fenwick", a=56, s="m", k="officer", cid=None, called="the officer who never reports", inv=True, proto=None, v=None,
    r="A customs officer who never reports, by trade (RT-03); the bonded store", home="edge_north", die=True, t=(0.45, 0.2, 0.3), quiet=True,
    look=L(1.78, 0.55, 0, "grey_short", "#8a8480", "tunic", "#1c2540", "#c9b04a", "trousers", "#1c2540"),
    card=dict(who="Douglas Fenwick, 56, customs officer at the bonded store. Has not written a report worth reading in ten years. Trades.", speak="Weary, careful, never a direct answer.",
              life="Up in town; the customs house.", rivals="The Widow's loads pass him."),
    src="invented: RT-03 (an officer who never reports, by trade); places.json customs owner",
    rt="mon-fri|00:00 edge_north home; 08:30 customs the bonded store; 16:30 edge_north home"
       "/sat-sun|00:00 edge_north home")
add(id="anthony_raine", n="Anthony Raine", a=45, s="m", k="minor", cid=None, called="the brief", inv=True, proto=None, v=None,
    r="A solicitor, Agar's man: the brief who can argue Ron out as a messenger, at his fee", home="edge_north", die=True, t=(0.5, 0.5, 0.4), quiet=True,
    look=L(1.80, 0.45, 0, "swept", "#4a3a2a", "suit", "#202028", "#e8e4dc", "trousers", "#202028", "briefcase"),
    card=dict(who="Anthony Raine, 45, a criminal solicitor who takes Agar's referrals. Can make a messenger of a man, at his fee.", speak="Smooth, quick, bills by the quarter hour.",
              life="Up in town; the station's interview rooms.", rivals="Agar's man."),
    src="invented: STORY-FRAME 5 (the brief is Agar's man)", rt="daily|00:00 edge_north up in town")
add(id="dobson", n="Walter Dobson", a=53, s="m", k="minor", cid=None, called="Mr Dobson", inv=True, proto=None, v=None,
    r="Keeps Dobson's chip shop on Back Parade", home="chip_shop", die=True, t=(0.4, 0.4, 0.5), quiet=False,
    look=L(1.74, 0.8, 0, "short", "#6a5a4a", "whites", "#f0f0ec", "#f0f0ec", "trousers", "#2a2a2a"),
    card=dict(who="Walter Dobson, 53, fries on Back Parade. Opens Sundays from 11 November.", speak="Jolly, loud, 'salt and vinegar?'", life="Above the shop.", rivals="Feeds all three."),
    src="wave 1 places.json and timetables (Mr Dobson); first name invented",
    rt="mon-sat|00:00 chip_shop asleep upstairs; 10:30 chip_shop the fryers; 23:45 chip_shop asleep upstairs"
       "/sun|00:00 chip_shop asleep upstairs")
add(id="peart", n="Herbert Peart", a=62, s="m", k="minor", cid=None, called="Mr Peart", inv=True, proto=None, v=None,
    r="Keeps Peart's, the newsagent and tobacconist, with the pension counter", home="newsagent", die=False, t=(0.4, 0.4, 0.6), quiet=False,
    look=L(1.70, 0.55, 0, "balding", "#a09a90", "cardigan", "#6a5a40", "#d8d0c0", "trousers", "#3a3630", "glasses"),
    card=dict(who="Herbert Peart, 62, the newsagent. Witness to half the street's wills. The Pilot on the counter at six.", speak="Gossip by headline.", life="Over the shop.", rivals="Sells papers to all three."),
    src="wave 1 places.json and rooms (Peart); first name invented",
    rt="mon-sat|00:00 newsagent asleep upstairs; 05:45 newsagent the papers in; 18:15 newsagent upstairs"
       "/sun|00:00 newsagent asleep upstairs; 06:45 newsagent Sunday papers; 12:15 newsagent upstairs")
add(id="arthur_brigham", n="Arthur Brigham", a=58, s="m", k="minor", cid=None, called="the grocer", inv=True, proto=None, v=None,
    r="Keeps Hook Stores, the grocer", home="d_nr_6", die=True, t=(0.4, 0.4, 0.6), quiet=False,
    look=L(1.72, 0.65, 0, "short", "#8a8078", "brown_coat", "#6a5038", "#e0d8c8", "trousers", "#3a3630"),
    card=dict(who="Arthur Brigham, 58, keeps Hook Stores. Knows every shoplifter by sight.", speak="Fussy, polite, counts change twice.", life="6 North Road.", rivals="None."),
    src="invented: places.json grocer (unnamed keeper)",
    rt="mon-sat|00:00 d_nr_6 asleep; 08:30 grocer opening up; 17:45 d_nr_6 home"
       "/sun|00:00 d_nr_6 asleep")
add(id="tadeusz_wrona", n="Tadeusz Wrona", a=64, s="m", k="minor", cid=None, called="Mr Wrona", inv=True, proto=None, v=None,
    r="Keeps the ironmonger's on Quay Street; came from Gdynia in 1947", home="d_nr_7", die=False, t=(0.55, 0.5, 0.4), quiet=True,
    look=L(1.70, 0.5, 0, "white", "#e0dcd4", "brown_coat", "#6a5038", "#e0d8c8", "trousers", "#3a3630", "glasses"),
    card=dict(who="Tadeusz Wrona, 64, keeps the ironmonger's. Came over after the war. The only man on the Hook who says Frank's surname right first time, and corrects the others.",
              speak="Courteous, Polish cadence, exact about screws.", life="7 North Road.", rivals="Keeps out of it."),
    src="invented: places.json ironmonger (unnamed keeper); casting mix (Polish) for a 1990 northern port",
    rt="mon-sat|00:00 d_nr_7 asleep; 08:30 ironmonger opening up; 17:45 d_nr_7 home"
       "/sun|00:00 d_nr_7 asleep; 09:30 chapel Mass; 11:00 d_nr_7 home")
add(id="joyce_ellerby", n="Joyce Ellerby", a=55, s="f", k="minor", cid=None, called="Mrs Ellerby", inv=True, proto=None, v=None,
    r="Keeps the Copper Kettle tea room", home="d_cl_4", die=True, t=(0.4, 0.4, 0.6), quiet=False,
    look=L(1.62, 0.55, 0, "set", "#b0a090", "blouse", "#e8d8e0", "#8a5a6a", "skirt", "#4a4048"),
    card=dict(who="Joyce Ellerby, 55, keeps the Copper Kettle. Doilies and opinions.", speak="Genteel, nosy.", life="4 Chapel Lane.", rivals="None."),
    src="invented: places.json tea_room (unnamed keeper)",
    rt="mon-sat|00:00 d_cl_4 asleep; 08:30 tea_room the urn; 17:45 d_cl_4 home"
       "/sun|00:00 d_cl_4 asleep")
add(id="george_cammidge", n="George Cammidge", a=67, s="m", k="minor", cid=None, called="the chandler", inv=True, proto=None, v=None,
    r="Keeps the ship's chandlery on Quay Street; owns the radios Darren is selling", home="d_cl_8", die=True, t=(0.5, 0.5, 0.5), quiet=False,
    look=L(1.72, 0.5, 0, "beard", "#d0ccc4", "jersey", "#1c2a40", "#1c2a40", "trousers", "#2a2a2a"),
    card=dict(who="George Cammidge, 67, the chandler. Rope, paraffin and tinned goods for boats that rarely come.", speak="Salty, slow.", life="8 Chapel Lane.", rivals="None."),
    src="invented: places.json chandlery (unnamed keeper); side story 13",
    rt="mon-sat|00:00 d_cl_8 asleep; 08:45 chandlery the shop; 17:45 d_cl_8 home"
       "/sun|00:00 d_cl_8 asleep")
add(id="vince_lazenby", n="Vince Lazenby", a=49, s="m", k="minor", cid=None, called="the snooker man", inv=True, proto=None, v=None,
    r="Keeps the snooker hall on the quay", home="d_nr_13", die=True, t=(0.55, 0.4, 0.4), quiet=True,
    look=L(1.76, 0.6, 0, "slicked", "#2a2a2a", "waistcoat", "#2a2a2a", "#e8e4dc", "trousers", "#2a2a2a"),
    card=dict(who="Vince Lazenby, 49, keeps the snooker hall. Danny holds court at his back table; he lets him.", speak="Laconic, 'table four's free'.", life="13 North Road.", rivals="Rents tables to all three."),
    src="invented: places.json snooker_hall (unnamed keeper)",
    rt="mon-sat|00:00 d_nr_13 asleep; 10:45 snooker_hall opening up; 22:45 d_nr_13 home"
       "/sun|00:00 d_nr_13 asleep")
add(id="sid_bulmer", n="Sid Bulmer", a=61, s="m", k="minor", cid=None, called="the trainer", inv=True, proto=None, v=None,
    r="The boxing club's head trainer; men who train there can be recruited", home="d_nr_15", die=True, t=(0.7, 0.6, 0.3), quiet=True, fight="boxer",
    look=L(1.72, 0.65, 0, "short", "#a09a90", "tracksuit", "#2a2a4a", "#e0e0e0", "trackies", "#2a2a4a"),
    card=dict(who="Sid Bulmer, 61, head trainer at the boxing club. Fought for the area title in 1952.", speak="Gruff, short, 'hands up'.", life="15 North Road.", rivals="Keeps the club neutral ground."),
    src="invented: places.json boxing_club (head trainer); 2.11.1",
    rt="mon,wed,fri|00:00 d_nr_15 asleep; 17:30 boxing_club the club night; 22:00 d_nr_15 home"
       "/sat|00:00 d_nr_15 asleep; 09:30 boxing_club Saturday morning; 13:15 d_nr_15 home"
       "/tue,thu,sun|00:00 d_nr_15 asleep")
add(id="maggie_firth", n="Maggie Firth", a=50, s="f", k="minor", cid=None, called="the tea-stall woman", inv=True, proto=None, v=None,
    r="Keeps the tea stall on the quay, 22:00 to 06:00", home="d_nr_17", die=True, t=(0.6, 0.3, 0.5), quiet=True,
    look=L(1.64, 0.7, 0, "headscarf", "#6a3a3a", "duffel", "#3a3a30", "#2a2a2a", "trousers", "#2a2a2a", "fingerless_gloves"),
    card=dict(who="Maggie Firth, 50, keeps the night tea stall on the quay. Sees the landing all night and says it is none of hers.", speak="Raw, funny, 'sugar's extra'.",
              life="17 North Road; sleeps by day.", rivals="Serves the Widow's men and the beat constable alike."),
    src="invented: places.json tea_stall",
    rt="daily|00:00 tea_stall the stall; 06:15 d_nr_17 asleep; 21:30 tea_stall the stall")
add(id="ernest_shillito", n="Ernest Shillito", a=63, s="m", k="minor", cid=None, called="the barber", inv=True, proto=None, v=None,
    r="The barber on Chapel Lane", home="d_cl_10", die=True, t=(0.35, 0.4, 0.6), quiet=False,
    look=L(1.70, 0.5, 0, "brylcreem", "#c0bab0", "white_coat", "#f0f0ec", "#f0f0ec", "trousers", "#2a2a2a"),
    card=dict(who="Ernest Shillito, 63, cuts hair on Chapel Lane. Hears more than Hal and tells more.", speak="Chatty, 'something for the weekend'.", life="10 Chapel Lane.", rivals="Cuts all three."),
    src="invented: places.json barber (unnamed keeper)",
    rt="mon-sat|00:00 d_cl_10 asleep; 08:45 barber the chair; 17:15 d_cl_10 home"
       "/sun|00:00 d_cl_10 asleep")
add(id="beryl_wood", n="Beryl Wood", a=48, s="f", k="minor", cid=None, called="the launderette woman", inv=True, proto=None, v=None,
    r="Minds the Washeteria's front: the machines, the change, the late hours to 23:00", home="d_cl_11", die=True, t=(0.4, 0.3, 0.6), quiet=False,
    look=L(1.62, 0.6, 0, "perm", "#9a6a40", "tabard", "#4a8aa0", "#e8e4dc", "trousers", "#30303a"),
    card=dict(who="Beryl Wood, 48, minds the Washeteria's front for Mr Tasker. Change for the machines and the street's news.", speak="Gossipy, warm.", life="11 Chapel Lane.", rivals="None."),
    src="invented: places.json launderette ('the Washeteria's keeper')",
    rt="mon-sun|00:00 d_cl_11 asleep; 07:45 launderette the front; 23:15 d_cl_11 home")
add(id="joe_cairns", n="Joe Cairns", a=70, s="m", k="minor", cid=None, called="the second-hand man", inv=True, proto=None, v=None,
    r="Keeps the second-hand shop on the quay", home="d_cl_13", die=False, t=(0.4, 0.3, 0.6), quiet=False,
    look=L(1.68, 0.45, 0, "white", "#e0dcd4", "cardigan", "#5a4a3a", "#3a3a30", "trousers", "#3a3630", "glasses"),
    card=dict(who="Joe Cairns, 70, keeps the second-hand shop. Buys house clearances; knows whose mother died.", speak="Wandering, kind.", life="13 Chapel Lane.", rivals="None."),
    src="invented: places.json second_hand (unnamed keeper)",
    rt="mon-sat|00:00 d_cl_13 asleep; 09:00 second_hand the shop; 17:30 d_cl_13 home"
       "/sun|00:00 d_cl_13 asleep")

# =========================== fare people who are not already regulars (fares.json; each a whole person)
def fare_person(id, n, a, s, r, home, rt, who, speak, look, src="invented: 3.4.1 (40 fare people)"):
    add(id=id, n=n, a=a, s=s, k="minor", cid=None, called=n.split()[0], inv=True, proto=None, v=None, r=r, home=home, die=True,
        t=(0.45, 0.4, 0.5), quiet=False, look=look, card=dict(who=who, speak=speak, life=r, rivals="None of the three."), src=src, rt=rt)

fare_person("harold_stead", "Harold Stead", 74, "m", "A retired pilot-boat man who goes to the Infirmary for his chest on Tuesdays and Fridays", "d_cl_15",
    "tue,fri|00:00 d_cl_15 asleep; 09:30 d_cl_15 waiting for a car; 10:00 infirmary his chest; 12:00 d_cl_15 home/mon,wed,thu,sat,sun|00:00 d_cl_15 asleep",
    "Harold Stead, 74, steered pilot boats for forty years. Takes a cab to the Infirmary twice a week and tells the driver the tide.", "Wheezy, nautical, endless.",
    L(1.72, 0.45, 0, "flatcap", "#9a958a", "overcoat", "#3a3a40", "#2a2a2a", "trousers", "#2a2a2a", "stick"))
fare_person("dorothy_kirkup", "Dorothy Kirkup", 69, "f", "A widow on Chapel Lane who goes to her sister's in town on Wednesdays", "d_cl_17",
    "wed|00:00 d_cl_17 asleep; 13:30 d_cl_17 waiting for a car; 14:00 edge_north her sister's; 18:00 d_cl_17 home/mon,tue,thu-sun|00:00 d_cl_17 asleep",
    "Dorothy Kirkup, 69, goes to her sister's every Wednesday and has opinions about the sister's husband.", "Confiding, 'between you and me'.",
    L(1.56, 0.5, 0, "set", "#c0b0a0", "coat", "#5a4a6a", "#d8d0c0", "skirt", "#3a3640", "handbag"))
fare_person("neville_kaye", "Neville Kaye", 41, "m", "A commercial traveller in paint who stops at Regent House on Mondays and needs the station on Wednesdays", "edge_north",
    "mon|00:00 edge_north on the road; 18:00 boarding_house his room for two nights/tue|00:00 boarding_house his room; 09:00 ironmonger his order book; 11:00 harbour_board the Board's painters; 13:00 boarding_house his room/wed|00:00 boarding_house his room; 08:30 boarding_house waiting for a car; 09:00 edge_north the station/thu-sun|00:00 edge_north on the road",
    "Neville Kaye, 41, sells marine paint up and down the coast. Thinks every town is the same except this one.", "Salesman's bonhomie, a joke per mile.",
    L(1.78, 0.6, 0, "parted", "#4a3a2a", "suit", "#4a4a50", "#e0d8c8", "trousers", "#4a4a50", "case"))
fare_person("sandra_newbould", "Sandra Newbould", 34, "f", "A night nurse at the Infirmary from Chapel Lane", "d_cl_19",
    "mon-fri|00:00 infirmary the night shift; 07:30 d_cl_19 asleep; 20:30 d_cl_19 waiting for a car; 21:00 infirmary the night shift/sat-sun|00:00 d_cl_19 asleep",
    "Sandra Newbould, 34, nights on casualty. Has stitched half the Hook and recognises the other half.", "Brisk, tired, unshockable.",
    L(1.64, 0.4, 0, "ponytail", "#5a3a20", "coat", "#2a3a5a", "#e0e0e8", "skirt", "#2a3a5a"))
fare_person("tony_marsden", "Tony Marsden", 38, "m", "A fishing-boat skipper who wants the fish dock before dawn on landing days", "d_nr_20",
    "mon,wed,fri|00:00 d_nr_20 asleep; 04:00 d_nr_20 waiting for a car; 04:30 fish_dock his boat; 12:00 caff dinner; 13:00 d_nr_20 home/tue,thu,sat,sun|00:00 d_nr_20 asleep",
    "Tony Marsden, 38, skippers one of the last three boats landing at the fish dock. Pays in cash and haddock.", "Few words, all of them about quotas.",
    L(1.80, 0.65, 0, "woolly", "#2a2a30", "smock", "#c06a2a", "#2a2a2a", "waders", "#2a2a2a"))
fare_person("janet_lumb", "Janet Lumb", 43, "f", "A school secretary with the school shut, cleaning offices in town at night", "d_cl_21",
    "mon-fri|00:00 edge_north the offices in town; 01:30 d_cl_21 asleep; 17:30 d_cl_21 waiting for a car; 18:00 edge_north the offices in town/sat-sun|00:00 d_cl_21 asleep",
    "Janet Lumb, 43, the comprehensive's secretary, cleaning offices in town until it reopens. Knows Mr Danby.", "Prim, then funny.",
    L(1.62, 0.4, 0, "bob", "#7a5a3a", "mac", "#8a7a5a", "#2a2a2a", "skirt", "#3a3a40"))
fare_person("gerald_thwaite", "Gerald Thwaite", 66, "m", "A retired accountant who goes to the bowls club in town on Saturday afternoons and comes home late", "d_cl_22",
    "sat|00:00 d_cl_22 asleep; 13:30 d_cl_22 waiting for a car; 14:00 edge_north the bowls club; 21:30 d_cl_22 home/sun-fri|00:00 d_cl_22 asleep",
    "Gerald Thwaite, 66, did Mickey's books before Sheila took over the figures and never forgave him. Says so.", "Precise, bitter, comic.",
    L(1.74, 0.45, 0, "balding", "#c0bab0", "blazer", "#2a2a4a", "#c0a040", "trousers", "#5a5a5a", "glasses"))
fare_person("kathleen_moran", "Kathleen Moran", 58, "f", "An Irish cook at the priests' house in town who comes to the Hook's chapel on Sundays", "edge_north",
    "sun|00:00 edge_north home in town; 09:00 chapel Mass; 11:00 chapel_hall tea after; 12:00 rank_mickeys waiting for a car; 12:30 edge_north home in town/mon-sat|00:00 edge_north home in town",
    "Kathleen Moran, 58, from Mayo, cooks for the priests in town and comes back to the Hook's chapel where she was married.", "Warm, quick, a blessing for a tip.",
    L(1.60, 0.6, 0, "set", "#9a8a7a", "coat", "#4a5a4a", "#d0c8b8", "skirt", "#3a3a40", "headscarf"))
fare_person("ahmed_rashid", "Ahmed Rashid", 46, "m", "Keeps a corner shop in town; buys stock at the Thursday market", "edge_north",
    "thu|00:00 edge_north home in town; 07:30 market_stalls_quay the barrows; 09:00 rank_mickeys waiting for a car with boxes; 09:30 edge_north back to his shop/mon-wed,fri-sun|00:00 edge_north home in town",
    "Ahmed Rashid, 46, came from Mirpur in 1966, keeps a corner shop in town. Buys at the barrows on Thursdays and takes a cab back with the boxes.", "Dry, businesslike, haggles the fare for fun.",
    L(1.74, 0.6, 4, "short", "#1a1a1a", "anorak", "#3a4a3a", "#2a2a2a", "trousers", "#3a3630"))
fare_person("ted_tindall", "Ted Tindall", 52, "m", "A Harbour Board pilot who needs the landing at all hours", "edge_north",
    "mon,wed,fri|00:00 edge_north home in town; 05:30 rank_north waiting for a car; 06:00 ferry_landing the pilot launch; 14:00 edge_north home in town/tue,thu,sat,sun|00:00 edge_north home in town",
    "Ted Tindall, 52, Harbour Board pilot. Brings ships in and wants to be at the launch ten minutes ago.", "Clipped, urgent.",
    L(1.80, 0.55, 0, "short", "#7a7068", "pea_coat", "#1c2230", "#c0a040", "trousers", "#1c2230"))
fare_person("eileen_crabtree", "Eileen Crabtree", 39, "f", "A hairdresser from town who does Sylvia's and Ada's hair at home on Fridays", "edge_north",
    "fri|00:00 edge_north home in town; 09:30 boarding_house Sylvia's set; 11:00 adas Ada's set; 12:30 rank_mickeys waiting for a car; 13:00 edge_north home in town/mon-thu,sat,sun|00:00 edge_north home in town",
    "Eileen Crabtree, 39, does home perms. Carries the Hook's gossip into town and back.", "Chatty, salon voice.",
    L(1.62, 0.4, 0, "big_perm", "#c0802a", "jacket", "#c03a6a", "#f0e0e0", "skirt", "#2a2a30", "case"))
fare_person("terence_bould", "Terence Bould", 29, "m", "A merchant seaman between ships, lodging at Regent House", "boarding_house",
    "mon-sat|00:00 boarding_house his room; 11:00 harbour_board the shipping office; 12:30 caff dinner; 14:00 snooker_hall the tables; 18:00 boarding_house his room/sun|00:00 boarding_house his room",
    "Terence Bould, 29, between ships. Waits for a berth and spends what he has on cabs to the shipping office.", "Restless, homesick, tells sea stories badly.",
    L(1.78, 0.5, 0, "short", "#5a3a20", "pea_coat", "#1c2230", "#1c2230", "jeans", "#30384a", "kitbag"))

# ---- people needed by the jobs and happenings beyond the above are listed in jobs/ and happenings.json by role ('a passer')

add(id="pc_ackrill", n="Stuart Ackrill", a=33, s="m", k="officer", cid=None, called="the late-turn constable", inv=True, proto=None, v=None,
    r="The day beat's late turn constable, 14:00 to 22:00 weekdays (the rota in routines.json)", home="edge_north", die=True, t=(0.55, 0.7, 0.7), quiet=False,
    look=L(1.83, 0.55, 0, "helmet", "#14161c", "tunic", "#14161c", "#c9c9c9", "trousers", "#14161c"),
    card=dict(who="PC Stuart Ackrill, 33, walks the day beat's late turn. Keen, new to the Hook, writes everything down.", speak="Eager, formal, 'right then, sir'.",
              life="The station; the late turn.", rivals="Honest, and tells Ellis what he writes down."),
    src="invented: the day beat 06:00 to 22:00 needs a late turn (police.json; timetables shift_beat_day); the fresh review of routines", rt="sat-sun|00:00 edge_north")
