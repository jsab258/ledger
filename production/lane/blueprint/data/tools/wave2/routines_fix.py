"""Routine rewrites after the first walking-reach check (24 Nov 2026): the 120 s hour makes a 450 m walk about
2.7 game hours, so each day keeps a person inside one part of the Hook or gives a long stay before a crossing.
Applied by build_people.py over cast_src.py."""
HOME = {"albert_suggitt": "boarding_house", "mark_billany": "boarding_house", "pat_brannigan": "boarding_house",
        "terry_hodgson": "d_cl_24"}
RT = {
"ada_vane": "mon-wed,fri-sat|00:00 adas asleep; 08:00 adas at her window; 10:00 grocer her shopping; 10:45 laveracks a bit of fish; 11:15 adas at her window"
  "/thu|00:00 adas asleep; 08:00 adas at her window; 09:30 newsagent her pension; 10:15 grocer her shopping; 11:00 adas at her window"
  "/sun|00:00 adas asleep; 08:00 adas at her window (Father Walsh brings her communion)",
"albert_suggitt": "mon-fri|00:00 boarding_house asleep; 06:30 fish_dock the nets; 12:00 caff his dinner; 12:45 boarding_house his room"
  "/sat-sun|00:00 boarding_house asleep; 11:00 fishing_quay_east watching the water; 13:00 boarding_house his room",
"alison_sedman": "tue,thu|00:00 edge_north home in town; 09:30 newsagent asking; 10:30 rank_mickeys a word with whoever is on it; 11:30 caff her dinner; 12:30 edge_north back to the paper (the warehouse row is her fare)"
  "/mon,wed,fri-sun|00:00 edge_north home in town",
"arvids_ozols": "daily|00:00 fishing_basin_north aboard; 21:00 rank_mickeys his cab to nowhere; 22:00 fishing_basin_north by cab: back aboard",
"bill_huxtable": "mon-sat|00:00 d_nr_1 asleep; 05:45 dock_gate the pen, first in by the quay road; 14:00 caff his tea; 15:30 d_nr_1 home"
  "/sun|00:00 d_nr_1 asleep",
"brenda_laverack": "mon-sat|00:00 d_nr_5 asleep; 05:00 fish_dock buying at the boxes; 08:15 laveracks gutting and the counter; 17:45 d_nr_5 home"
  "/sun|00:00 d_nr_5 asleep",
"brendan_walsh": "mon,wed-sat|00:00 priests_house asleep; 07:30 chapel morning Mass; 09:00 priests_house his desk; 13:00 adas a call on Ada; 17:00 chapel the church open; 18:00 priests_house supper; 20:30 edge_north sick calls on foot; 22:30 priests_house asleep"
  "/tue|00:00 priests_house asleep; 07:30 chapel morning Mass; 09:00 priests_house his desk; 13:00 adas a call on Ada; 17:00 chapel the church open; 18:00 priests_house supper; 19:00 chapel_hall the Tuesday tea and talk; 21:30 priests_house asleep"
  "/sun|00:00 priests_house asleep; 08:30 chapel Masses; 13:00 priests_house the afternoon; 18:00 chapel evening Mass; 19:00 priests_house asleep",
"brian_tindall": "mon,wed,fri|00:00 edge_north home in town; 05:30 rank_north waiting for a car; 06:00 ferry_landing by cab: the pilot launch; 14:00 edge_north home in town"
  "/tue,thu,sat,sun|00:00 edge_north home in town",
"christine_pickering": "mon-fri|00:00 d_nr_9 asleep; 08:45 harbour_board the counter, sandwiches at her desk; 16:45 d_nr_9 home"
  "/sat|00:00 d_nr_9 asleep; 10:00 newsagent the Saturday paper and a chat; 11:30 d_nr_9 home"
  "/sun|00:00 d_nr_9 asleep",
"colin_mastin": "mon-fri|00:00 d_cs_7 asleep; 05:45 dock_gate in at six, the cranes inside; 17:30 d_cs_7 home"
  "/sat|00:00 d_cs_7 asleep; 05:45 dock_gate Saturday morning; 12:30 d_cs_7 home"
  "/sun|00:00 d_cs_7 asleep",
"craig_fewson": "mon-sat|00:00 d_nr_39 asleep; 11:00 cammack_base the lock-ups; 15:00 rank_ferry watching the ferry rank; 20:00 snooker_hall with Danny; 23:00 d_nr_39 home"
  "/sun|00:00 d_nr_39 asleep; 13:00 cammack_base the lock-ups; 18:00 d_nr_39 home",
"cyril_pashby": "mon-sat|00:00 d_cl_33 asleep; 10:00 chapel the steps; 13:00 d_cl_33 home"
  "/sun|00:00 d_cl_33 asleep; 09:30 chapel Mass, in black; 11:00 d_cl_33 home",
"danny_cammack": "mon-sat|00:00 d_nr_40 his flat; 11:00 cammack_base the lock-ups; 15:00 rank_north watching the other rank; 16:00 cammack_base the lock-ups; 20:00 snooker_hall holding court; 23:30 d_nr_40 his flat"
  "/sun|00:00 d_nr_40 his flat; 13:00 cammack_base the lock-ups; 18:00 d_nr_40 his flat",
"darren_milner": "mon,wed,fri|00:00 d_nr_23 his mother's; 10:00 caff a tea he does not pay for; 11:00 ritas selling; 12:30 rank_mickeys hanging about; 13:30 launderette the warm; 15:00 phone_parade the phone box; 16:00 rank_mickeys hanging about; 19:00 cammack_base near the lock-ups; 22:30 d_nr_23 his mother's"
  "/tue,thu,sat|00:00 d_nr_23 his mother's; 10:00 caff a tea he does not pay for; 11:00 rank_ferry the boat queue; 13:00 rank_mickeys hanging about; 16:00 snooker_hall the tables; 18:30 rank_mickeys hanging about; 21:00 d_nr_23 his mother's"
  "/sun|00:00 d_nr_23 his mother's; 12:00 rank_mickeys hanging about; 15:00 d_nr_23 his mother's",
"dawn_pybus": "mon-thu|00:00 edge_north home in town; 09:00 adas the rent round, Quay Street; 12:15 d_cl_9 the rent round, Chapel Lane; 15:00 agar_base the agents' book; 16:00 edge_north back to town"
  "/fri|00:00 edge_north home in town; 09:00 adas the rent round, Quay Street; 11:00 mickeys behind Mr Askew at the counter; 15:00 agar_base the agents' book; 16:00 edge_north back to town"
  "/sat-sun|00:00 edge_north home in town",
"dennis_iveson": "mon-sat|00:00 d_nr_44 asleep; 07:30 iveson_yard the yard; 12:00 iveson_hut his dinner in the hut; 13:00 iveson_yard the yard; 17:15 d_nr_44 home"
  "/sun|00:00 d_nr_44 asleep",
"doreen_harland": "mon-sat|00:00 d_cl_25 asleep; 05:45 launderette the boiler, the early shift; 14:00 d_cl_25 home"
  "/sun|00:00 d_cl_25 asleep",
"dougie_saltmarsh": "mon-sat|00:00 d_nr_43 asleep; 05:00 fish_dock the porters' cut; 09:30 cold_stores the yard gate; 14:30 snooker_hall the tables; 20:00 d_nr_43 home"
  "/sun|00:00 d_nr_43 asleep",
"eddie_birtwhistle": "mon-sat|00:00 d_nr_4 asleep; 04:45 fish_dock the boxes; 11:00 caff his dinner; 12:45 d_nr_4 home"
  "/sun|00:00 d_nr_4 asleep",
"edith_stockill": "mon-sat|00:00 d_cl_12 asleep; 09:15 adas a word at Ada's window; 10:00 newsagent the pension counter; 14:00 d_cl_12 home"
  "/sun|00:00 d_cl_12 asleep",
"edna_coulson": "mon-fri|00:00 d_cl_7 asleep; 06:00 mickeys cleaning the front office, from six; 07:00 tea_room cleaning; 08:15 snooker_hall cleaning; 11:45 d_cl_7 home"
  "/sat|00:00 d_cl_7 asleep; 06:00 mickeys Saturday clean; 09:30 d_cl_7 home"
  "/sun|00:00 d_cl_7 asleep; 09:30 chapel Mass; 11:00 d_cl_7 home",
"gary_mawer": "mon-fri|00:00 d_nr_30 asleep; 07:30 iveson_yard the slip and the yard; 17:00 d_nr_30 home"
  "/sat|00:00 d_nr_30 asleep; 09:00 iveson_yard Saturday jobs; 12:00 d_nr_30 home"
  "/sun|00:00 d_nr_30 asleep",
"gerald_pashley": "sat|00:00 d_cl_22 asleep; 13:30 d_cl_22 waiting for a car; 14:00 edge_north by cab: the bowls club; 21:30 d_cl_22 home"
  "/mon-fri,sun|00:00 d_cl_22 asleep",
"ian_megginson": "mon-fri|00:00 d_nr_8 asleep; 07:30 iveson_yard the workshop; 17:00 d_nr_8 home"
  "/sat|00:00 d_nr_8 asleep; 09:00 ironmonger odd jobs; 12:00 d_nr_8 home"
  "/sun|00:00 d_nr_8 asleep; 10:00 allotments his plot; 13:30 d_nr_8 home",
"jason_pinder": "mon-sat|00:00 d_nr_28 asleep; 11:30 cammack_base the lock-ups; 17:00 phone_parade the corner; 21:00 tangs_takeaway outside at closing; 23:00 d_nr_28 home"
  "/sun|00:00 d_nr_28 asleep",
"jimmy_raw": "mon-sat|00:00 d_nr_2 asleep; 05:45 dock_gate the pen; 14:00 rank_mickeys by car two; 15:30 snooker_hall a frame; 18:30 d_nr_2 home"
  "/sun|00:00 d_nr_2 asleep",
"ken_dobbin": "mon-sat|00:00 d_nr_3 asleep; 05:45 dock_gate the pen; 14:00 rank_mickeys by car two with Jimmy; 15:30 snooker_hall a frame; 18:30 d_nr_3 home"
  "/sun|00:00 d_nr_3 asleep",
"julie_kettlewell": "mon,wed,fri|00:00 d_cl_9 asleep; 08:30 newsagent the cards in the window; 09:30 launderette asking after work; 11:00 caff a tea she makes last; 14:30 d_cl_9 home; 18:00 d_cl_9 the rent man at six"
  "/thu|00:00 d_cl_9 asleep; 08:30 newsagent the cards in the window; 09:30 market_stalls_quay looking; 13:00 d_cl_9 home"
  "/tue,sat|00:00 d_cl_9 asleep; 08:30 newsagent the cards in the window; 09:30 edge_north into town for work; 15:00 d_cl_9 home"
  "/sun|00:00 d_cl_9 asleep",
"june_suddaby": "mon-fri|00:00 boarding_house her room; 10:00 mickeys his things; 11:30 tea_room alone; 13:00 boarding_house her room"
  "/sat|00:00 boarding_house her room; 11:00 ferry_landing the boat over and back; 15:00 boarding_house her room"
  "/sun|00:00 boarding_house her room; 09:30 chapel Mass and a candle; 13:30 boarding_house her room",
"karen_grummitt": "mon-sat|00:00 boarding_house her room; 06:30 ferry_landing the ticket window; 19:00 boarding_house her room"
  "/sun|00:00 boarding_house her room; 10:30 ferry_landing a walk on the quay; 12:00 boarding_house her room",
"kathleen_moran": "sun|00:00 edge_north home in town; 09:00 chapel Mass; 12:00 chapel waiting for a car; 12:30 edge_north by cab: home in town"
  "/mon-sat|00:00 edge_north home in town",
"kevin_needham": "mon-sat|00:00 edge_north home; 06:15 caff breakfast; 07:00 rank_mickeys car one; 12:30 caff his break; 13:15 rank_mickeys car one; 19:00 edge_north home"
  "/sun|00:00 edge_north home; 12:00 rank_mickeys car one, Sunday; 18:00 edge_north home",
"lee_drewery": "mon-sat|00:00 d_nr_12 asleep; 05:55 dock_gate the pen at six; 08:00 fish_dock what work there is; 12:00 rank_mickeys sat on the bollard; 15:00 fishing_quay_east a line off the quay; 18:00 ritas the step after closing; 19:15 d_nr_12 home"
  "/sun|00:00 d_nr_12 asleep; 14:00 fishing_quay_east a line off the quay; 17:00 d_nr_12 home",
"len_garside": "daily|00:00 chandlery asleep upstairs; 08:00 chandlery the back room; 21:00 chandlery asleep upstairs",
"leonard_askew": "mon-thu|00:00 edge_north home; 09:30 agar_base the agents' office; 17:00 edge_north home"
  "/fri|00:00 edge_north home; 11:00 mickeys the rent at the counter; 12:00 edge_north back to the agents"
  "/sat-sun|00:00 edge_north home",
"leslie_cotterill": "mon-fri|00:00 d_nr_38 asleep; 08:45 ritas key cutting; 13:00 iveson_yard odd jobs at the yard; 17:00 d_nr_38 home"
  "/sat|00:00 d_nr_38 asleep; 08:45 ritas key cutting; 12:00 d_nr_38 home"
  "/sun|00:00 d_nr_38 asleep",
"malcolm_ruddock": "mon-fri|00:00 d_cs_5 asleep; 05:30 cold_stores the yard; 14:00 d_cs_5 home"
  "/sat|00:00 d_cs_5 asleep; 05:30 cold_stores Saturday shift; 13:15 d_cs_5 home"
  "/sun|00:00 d_cs_5 asleep",
"mark_billany": "mon-sat|00:00 boarding_house asleep; 06:00 dock_gate the tax hut; 12:00 caff dinner; 13:00 rank_ferry the tax on the ferry rank; 17:00 widow_base the take; 21:00 boarding_house his room"
  "/sun|00:00 boarding_house asleep",
"maureen_jensen": "mon-sat|00:00 d_cs_19 home; 08:00 widow_base the office over the net store; 18:00 d_cs_19 home"
  "/sun|00:00 d_cs_19 home; 10:00 chapel Mass; 13:15 d_cs_19 home",
"neil_screeton": "mon-sat|00:00 d_nr_26 asleep; 07:30 iveson_yard the yard; 17:00 iveson_yard chains the gap; 18:45 d_nr_26 home"
  "/sun|00:00 d_nr_26 asleep",
"nora_cronin": "mon-sat|00:00 d_cl_6 asleep; 07:15 priests_house his breakfast; 13:00 grocer his table; 14:00 laveracks his fish; 17:30 priests_house his supper; 19:30 d_cl_6 home"
  "/sun|00:00 d_cl_6 asleep; 09:30 chapel Mass; 13:00 d_cl_6 home",
"norman_dent": "daily|00:00 dents_warehouses his round of the row; 07:00 d_cl_20 home to bed; 19:30 dents_warehouses his round of the row",
"paddy_rourke": "mon-fri|00:00 d_nr_41 asleep; 07:45 customs the docks; 17:00 d_nr_41 home"
  "/sat|00:00 d_nr_41 asleep"
  "/sun|00:00 d_nr_41 asleep; 09:30 chapel Mass; 13:00 d_nr_41 home",
"pat_brannigan": "mon|00:00 boarding_house asleep; 11:00 widow_base the net store; 16:00 boxing_club the club; 18:00 boarding_house his room; 22:00 widow_base the van to the last boat"
  "/tue-sat|00:00 widow_base the van back from the last boat; 04:00 boarding_house asleep; 11:00 widow_base the net store; 16:00 boxing_club the club; 18:00 boarding_house his room; 22:00 widow_base the van to the last boat"
  "/sun|00:00 widow_base the van back from the last boat; 04:00 boarding_house asleep",
"pat_stainton": "mon-fri|00:00 d_nr_31 asleep; 07:45 launderette the presses; 17:00 d_nr_31 home"
  "/sat-sun|00:00 d_nr_31 asleep",
"philip_danby": "mon-sat|00:00 d_cl_29 asleep; 10:00 fishing_quay_west his walk on the quay; 11:30 tea_room a pot of tea; 14:00 d_cl_29 home; 16:00 allotments the allotments; 18:00 d_cl_29 home"
  "/sun|00:00 d_cl_29 asleep; 11:00 ferry_landing watching the boats; 14:00 d_cl_29 home",
"raymond_kaye": "mon|00:00 edge_north on the road; 18:00 boarding_house his room for two nights"
  "/tue|00:00 boarding_house his room; 09:00 ironmonger his order book; 11:00 chandlery his order book; 13:00 boarding_house his room"
  "/wed|00:00 boarding_house his room; 08:30 boarding_house waiting for a car; 09:00 edge_north by cab: the station"
  "/thu-sun|00:00 edge_north on the road",
"shane_boddy": "mon-sat|00:00 d_nr_34 asleep; 12:00 cammack_base the lock-ups; 17:00 phone_parade the corner by the phone box; 20:00 snooker_hall the tables; 23:00 d_nr_34 home"
  "/sun|00:00 d_nr_34 asleep",
"shaun_hewson": "mon-thu|00:00 boarding_house his room; 07:00 caff breakfast; 08:00 empty_unit his ladder on the parade's boards; 12:00 caff dinner; 13:00 launderette the next board; 17:00 boarding_house his room"
  "/fri|00:00 boarding_house his room; 07:00 caff breakfast; 08:00 mickeys his ladder at Mickey's bay; 12:00 caff dinner; 13:00 launderette the next board; 17:00 boarding_house his room"
  "/sat|00:00 boarding_house his room; 11:00 snooker_hall the tables; 14:00 boarding_house his room"
  "/sun|00:00 boarding_house his room; 11:00 fishing_quay_west a walk; 13:00 boarding_house his room",
"stan_pickles": "mon-fri|00:00 edge_north home; 07:30 harbour_board the works yard; 16:30 edge_north home"
  "/sat-sun|00:00 edge_north home",
"stathers": "mon-sat|00:00 d_cs_17 asleep; 05:30 dock_gate the pen; 09:00 widow_base the office below hers; 13:00 dock_gate the hut and the tax; 18:00 d_cs_17 home"
  "/sun|00:00 d_cs_17 asleep; 10:00 chapel Mass, behind her; 13:15 d_cs_17 home",
"susan_coverdale": "mon-fri|00:00 d_nr_14 asleep; 08:30 customs the customs house; 17:15 ritas past the window; 18:30 d_nr_14 home"
  "/sat-sun|00:00 d_nr_14 asleep",
"sylvia_rennison": "mon-fri|00:00 boarding_house asleep; 06:30 boarding_house breakfasts; 10:30 laveracks fish for the lodgers; 11:30 boarding_house the house; 22:00 boarding_house asleep"
  "/sat-sun|00:00 boarding_house asleep; 06:30 boarding_house breakfasts and the step",
"tadeusz_nowicki": "mon-sat|00:00 d_nr_7 asleep; 08:30 ironmonger opening up; 17:45 d_nr_7 home"
  "/sun|00:00 d_nr_7 asleep; 09:30 chapel Mass; 13:00 d_nr_7 home",
"terence_bould": "mon-sat|00:00 boarding_house his room; 11:00 harbour_board the shipping office; 16:00 snooker_hall the tables; 19:00 boarding_house his room"
  "/sun|00:00 boarding_house his room",
"terry_hodgson": "mon-sat|00:00 rank_mickeys the night car; 03:00 d_cl_24 home to bed; 18:00 rank_mickeys the night car"
  "/sun|00:00 rank_mickeys the night car; 03:00 d_cl_24 home to bed; 19:00 rank_mickeys the night car",
"tony_marsden": "mon,wed,fri|00:00 d_nr_20 asleep; 04:00 d_nr_20 waiting for a car; 04:30 fish_dock by cab: his boat; 12:00 caff dinner; 14:00 d_nr_20 home"
  "/tue,thu,sat,sun|00:00 d_nr_20 asleep",
"wayne_harrison": "mon-sat|00:00 d_nr_27 asleep; 10:00 ritas the back room; 16:00 ritas the step; 17:45 snooker_hall the tables; 22:00 d_nr_27 home"
  "/sun|00:00 d_nr_27 asleep",
"wes_akers": "mon-sat|00:00 net_loft the crates; 02:30 d_nr_32 asleep; 13:00 cammack_base the lock-ups; 22:30 net_loft the crates"
  "/sun|00:00 net_loft the crates; 02:30 d_nr_32 asleep; 14:00 cammack_base the lock-ups; 18:00 d_nr_32 home",
"wilf_hardcastle": "daily|00:00 d_cl_31 asleep; 07:00 pigeon_loft the birds; 12:00 d_cl_31 his dinner; 14:30 pigeon_loft the birds; 18:30 d_cl_31 home",
"winifred_duggleby": "mon-fri|00:00 d_cl_16 asleep; 08:00 chapel the flowers and the brass; 11:30 d_cl_16 home; 15:00 adas a cup with Ada; 18:30 d_cl_16 home"
  "/sat|00:00 d_cl_16 asleep"
  "/sun|00:00 d_cl_16 asleep; 09:30 chapel Mass; 12:00 d_cl_16 home",
"grace_rinaldi": "mon-thu|00:00 d_bp_3 asleep; 05:30 caff opening up; 15:30 d_bp_3 home"
  "/fri-sat|00:00 d_bp_3 asleep; 05:30 caff opening up; 22:15 d_bp_3 home"
  "/sun|00:00 d_bp_3 asleep; 10:00 chapel Mass; 13:15 d_bp_3 home",
"old_firm_man": "mon-sat|00:00 ferry_landing the landing; 01:15 edge_west gone along the quay; 09:00 caff a tea in the corner; 09:45 edge_west gone; 21:45 ferry_landing the landing"
  "/sun|00:00 ferry_landing the landing; 01:15 edge_west gone along the quay; 21:45 ferry_landing the landing",
}
