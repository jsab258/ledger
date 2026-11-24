"""Fixes after the fresh review of people and ties (wave2/REVIEW-people.md), 24 Nov 2026. Applied by build_people.py."""
COVER_RULE = "Frank's line (RT-09, RT2-05) covers every woman, anyone of sixty or over and the priest: can_die false for them; everyone else can be killed or hospitalised and names a fallback_role."
FIELDS = {   # id: {field: value}  (card keys go in 'card')
 "ron_kirby": {"fb": "Ron's asks come by the old firm's man at the office door (RT2-05)"},
 "old_firm_man": {"a": 59, "fb": "the landing stands empty until the highest rival fills it (STORY-FRAME 5 Act IIa)"},
 "alf_garside": {"a": 57},
 "peter_tang": {"fb": "Lily keeps the takeaway; Mickey's Friday ends (side story 4)", "card": {"who": "Peter Tang, 44, keeps the takeaway on the parade with his wife Lily. Came from the New Territories in 1968."}},
 "sgt_bellwood": {"fb": "another custody sergeant from town"},
 "derek_hebblewhite": {"fb": "another VAT officer sent from town; the inspection runs on (STORY-FRAME 5 Act III never depends on one killable person)"},
 "carol_ellis": {"k": "principal"},
 "sheila_dunn": {"card": {"secret": "Mickey's arrangement was with the old firm at the landing, from before the three rivals were anybody; Garbutt only carries messages. She has kept the true count of every night in her own hand."}},
 "sylvia_rennison": {"card": {"who": "Sylvia Rennison, 64, a widow who keeps Regent House, the boarding house on the quay. House rules first. One of Danny Cammack's lot is three weeks behind with his rent."}},
 "alison_sedman": {"card_replace": [("Meridian Evening Mail", "Meridian Pilot"), ("Evening Mail", "Pilot"), ("the Mail", "the Pilot")]},
 "julie_kettlewell": {"card": {"who": "Julie Kettlewell, 29, laid off from the laundry's presses in the summer; the laundry runs on with fewer hands. Owes Mickey's nine pounds she cannot pay. Can drive anything.", "life": "Rents 9 Chapel Lane, the house with the blue step. The cards in the newsagent's window every morning."}},
 "darren_milner": {"card_replace": [("on Chapel Lane", "on North Road")]},
 "june_suddaby": {"card": {"life": "Stayed on at Regent House past the funeral, sorting her father's things, with no date to leave."}, "card_replace": [("until Friday", "for now"), ("going home on Friday", "staying on for now")]},
 "kieran_rourke": {"card": {"who": "Kieran Rourke, 44, a customs assistant on the docks for twenty years. Counts the bonded store's tobacco.", "speak": "Plain, careful, a counter of things: 'that's eleven, not twelve'."}},
 "steve_brannigan": {"card": {"who": "Steve Brannigan, 38, minds the Widow's net store and drives her van to the last boat. Drove a bakery van until the lay-offs.", "speak": "Quiet, polite, does what Mrs Jensen says."}},
 "kathleen_moran": {"card": {"who": "Kathleen Moran, 58, a cook at a works canteen in town who comes back to the Hook's chapel, where she was married.", "speak": "Brisk, warm, talks about the canteen."}},
 "aidan_keogh": {"card": {"who": "Dr Aidan Keogh, 69, retired from a practice in town. Stitches what comes to his door at 23 Chapel Lane and asks nothing. Fifteen pounds.", "speak": "Dry, clinical, 'hold still'."}},
 "ahmed_rashid": {"card": {"speak": "Dry, in a hurry, counts his boxes twice."}},
 "janet_lumb": {"r": "Cleans offices in town at night; walks from Chapel Lane", "card": {"who": "Janet Lumb, 43, cleans offices in town at night. Knows Mr Danby from the chapel.", "speak": "Prim, then funny."}},
 "jimmy_raw": {"card": {"who": "Jimmy Raw, 35, picked at the pen three days in five. Fights when the Widow's men tell him to."}, "fight": "boxer"},
 "frank_nowak": {"look_h": 1.75},
 "kevin_needham": {"card": {"secret": "Tells the Widow's people what goes out over Mickey's radio; she is his landlord at the gate (2.10.2)."}},
 "stathers": {"card_replace": [("if she falls", "if she is gone (by Frank's line she is never his to hurt)")]},
 "danny_cammack": {"card_replace": [("Drove car two for Mickey and never gave the key back.", "Drove car two, Mickey's own car, and never gave the key back.")]},
}
NO_FIGHT_60 = True   # covered people carry no fight kind
EXTRA_TIES = [("sheila_dunn", "pauline_kitching", 0.8), ("danny_cammack", "sheila_dunn", 0.3), ("danny_cammack", "pauline_kitching", 0.4),
              ("danny_cammack", "kevin_needham", 0.4), ("danny_cammack", "terry_hodgson", 0.3), ("maureen_jensen", "ron_kirby", 0.4),
              ("june_suddaby", "ron_kirby", 0.4), ("kevin_needham", "terry_hodgson", 0.6), ("grace_rinaldi", "jason_pinder", 0.3),
              ("grace_rinaldi", "danny_cammack", 0.3), ("julie_kettlewell", "victor_tasker", 0.3), ("darren_milner", "arvids_ozols", 0.4),
              ("darren_milner", "george_cammidge", 0.3), ("dennis_iveson", "alison_sedman", 0.3), ("dennis_iveson", "carol_ellis", 0.2),
              ("simon_ombler", "alan_sowerby", 0.5)]
# ties that never meet in a week but the frame needs: how they reach each other instead
BY_MESSAGE = {("maureen_jensen", "kevin_needham"): "by the radio (Mickey's set, overheard) and her men at the gate",
              ("keith_garbutt", "maureen_jensen"): "by pager and phone box", ("keith_garbutt", "geoffrey_agar"): "by pager and phone box",
              ("geoffrey_agar", "susan_coverdale"): "letters, carried to his office in town", ("geoffrey_agar", "alan_sowerby"): "letters; the licensing committee in town",
              ("geoffrey_agar", "anthony_raine"): "in town, off the Hook", ("carol_ellis", "alison_sedman"): "the station and the paper, in town",
              ("ron_kirby", "danny_cammack"): "Danny comes to the rank when the story brings him (STORY-FRAME 3)",
              ("dennis_iveson", "carol_ellis"): "only through the fire file", ("dennis_iveson", "alison_sedman"): "only through the fire story",
              ("pc_ibbotson", "pc_haigh"): "at the station at the change of shift",
              ("alison_sedman", "darren_milner"): "he rings her from the phone box with what he hears",
              ("danny_cammack", "rita_welburn"): "his men carry the goods to her back room",
              ("kevin_needham", "terry_hodgson"): "the car changes hands on the rank at 06:00 and 18:00"}

HEADS = {"danny_cammack", "maureen_jensen", "geoffrey_agar", "keith_garbutt"}   # the bank's no_kind: rival heads speak only in authored scenes and live talk
SHARED_ONLY = {"sheila_dunn", "alison_sedman", "ada_vane"}                       # 3.6.3
MOST_SEEN = ["ron_kirby", "pauline_kitching", "darren_milner", "kevin_needham", "terry_hodgson", "pc_ibbotson", "grace_rinaldi",
             "brenda_laverack", "wayne_harrison", "rita_welburn", "lee_drewery", "brendan_walsh"]
def has_own(p):
    pid = p["id"]
    if pid == "frank_nowak" or pid in SHARED_ONLY or pid in HEADS:
        return False
    return p["k"] in ("principal", "firm", "regular", "rival_man") or pid in MOST_SEEN
import re as _re
_KINDS = [("shopkeeper", r"keep|shop|caff|chip|newsagent|grocer|ironmonger|chandl|barber|tea room|takeaway|pawn|boarding house|appraiser|tea stall"),
          ("dock_worker", r"dock|crane|porter|fish|trawler|ship|ferry|pen|skipper|seaman|net"),
          ("driver", r"driver|cab|car lot|minicab"), ("laundry_worker", r"laundr|presser|washer|seamstress"),
          ("tradesman", r"locksmith|repair|garage|glazier|sign painter|works man|boat|scrap|bailiff"),
          ("night_shift", r"night watchman|night nurse|night beat"),
          ("office_worker", r"clerk|officer|customs|solicitor|agent|teacher|reporter|nurse|cleans offices|dispatcher|bookkeeper|licensing|VAT|CID|constable|sergeant|pilot|traveller|hairdresser|cook|campaign|organiser|priest|doctor|rent"),
          ("casual_worker", r"casual|laid off|hustler|crew|man at|man on|lieutenant")]
def speaker_kind(p, bank_members):
    if p["id"] in HEADS or p["id"] == "frank_nowak":
        return None
    if p.get("cid") in bank_members:
        return bank_members[p["cid"]]
    if p["a"] >= 65:
        return "pensioner"
    for k, rx in _KINDS:
        if _re.search(rx, p["r"], _re.I):
            return k
    return "anyone"
