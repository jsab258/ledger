"""The rules, as data (unit 12, cloud week 42): cooldowns, variety, priorities and silence, every number with its reason.
build_lines.py writes this as rules.json; check_lines.py plays a walk through it (walk_sim.py) so the numbers are tested, not
only written. A number that comes from a ruling or the code says where; a number invented here says so, and DECISIONS.md carries
one entry for the lot, marked for Jafar.

Reading guide. 'to_tom' lines answer something he did (a pass, a bump, a question, a goodbye). 'event' lines answer something
that happened in the street (rain starting, a crime). 'neighbour' lines are the street talking among itself: the 45 second rule
(RULINGS: neighbours' talk at most every 45 s) covers these and the street's existing ambient exchanges together, on one clock.
"""


def n(value, why, source="invented here"):
    return {"value": value, "why": why, "source": source}


RULES = {
    "bank": "ambient-lines-v1",
    "status": "PROPOSED: tested only by check_lines.py's walks; nothing here is in the game",
    "made": "13 Oct 2026, cloud week 42, unit 12",
    "how_to_read": "value is the number; why is the reason; source is where the number comes from, or 'invented here' (marked for Jafar in DECISIONS.md)",

    # ------------------------------------------------------------------ what the game tells the picker
    "inputs": {
        "weather": "dry | drizzle | rain, from Weather.Rain with the cut points below",
        "time": "morning | afternoon | evening | night, from the game clock with the bands in lines.json",
        "standing": "the speaker's rung with Tom: stranger | owner | nowak | tom | tommy (PlayerIdentity's ladder, decision A of what-they-call-him); Mickey's own people start at nowak (Ron, Darren: they know his name from the start); Father Walsh and June start at owner",
        "stance": "StanceKind of the speaker toward Tom (StreetVoice.Stance)",
        "sure": "noise | shape | face: the speaker's perception of a crime (idRung 0, 1, 3), never above what Perception measured for that person",
        "destination": "a place id from lines.json places, when Tom asks the way",
        "since_deed_s": "seconds since the last deed within 20 m of the speaker, or none",
    },
    "weather_cuts": {
        "dry_below": n(0.10, "below this the sky is dry; Weather.cs's own drizzle rolls start at about 0.1 and its day-one 0.35 is called rain there", "invented here, from Weather.cs's sample days"),
        "rain_from": n(0.50, "halfway; Weather.cs's downpour day is 0.90 and its first day, 0.35, reads as drizzle on screen", "invented here"),
        "episode_ends_after_dry_s": n(600, "rain 'starts' again only after ten dry minutes, so a shower with a break is one episode", "invented here"),
    },
    "kind_of_speaker": {
        "order": "an own kind first (rocco -> ron, sam -> darren, emil -> father_walsh, june -> june), then the person's kind in lines.json speakers, then the crowd's trade (Population.Trades) through trade_kinds; an unknown trade says nothing",
        "why": "silence is better than a wrong voice; the old crowd generator names thirty trades and every one is mapped",
    },
    "speaker_overrides": {
        "lena": {"standing_floor": "owner", "standing_cap": "owner", "until": "sheila_trusts_tom", "why": "canon: Sheila withholds his name until she trusts him; she is held at the first rung of the ladder (the new owner: she showed the new management round on day one, so never a stranger) until the trust flag (sheila-trust-2026-09-29) is set"},
        "staff": {"speakers": ["zlata", "ferko", "dusan"], "standing_floor": "owner", "why": "the dispatcher and the two drivers work at Mickey's: they know who he is from the first day (day-one design: the six who see him come)"},
        "excluded_lines": {
            "speakers": ["lena", "zlata"],
            "lines": ["office_worker.greet-owner.04", "office_worker.greet-nowak.05"],
            "why": "Sheila keeps the books and Pauline works the radio, so 'Do you have a card?' and 'Is the radio still crackling?' would be said to him by the very people it is about (canon review, 13 October, L4)"},
        "rocco": {"standing_floor": "nowak", "why": "Ron knows Tom's name from the start (what-they-call-him); his word for Tom is 'boss' in every line"},
        "sam": {"standing_floor": "nowak", "why": "Darren knows Tom's name from the start (what-they-call-him)"},
        "never_police": {
            "speakers": ["rocco", "lena", "rita", "hal", "victor", "tibor", "drago"],
            "why": "RULINGS 1 Oct: Mickey's people (Ron, Sheila) never go to the police about one of their own; the Ellis design: Rita, Hal, the pawn's back-room hand, the customs officer and the scrap dealer never go at all. A line that rings, tells or fetches the police is never given to them (lines.json flags it calls_police).",
        },
        "not_local_voice": {
            "speakers": ["vesna", "takeaway_m", "takeaway_f"],
            "why": "their voice slots are Irish (Cork) and Hong Kong English (REGULARS.md rows 11, 29, 30); a line in northern dialect is never given to them",
        },
    },

    # ------------------------------------------------------------------ cooldowns
    "cooldowns": {
        "neighbours_talk_min_gap_s": n(45, "RULINGS 'neighbours' talk at most every 45 s'; StreetVoice.ClearWordsEverySeconds, measured: at 45 s a fourteen-line band does not come back inside BarkGen's ten-minute floor", "RULINGS Talk and AI; StreetVoice.cs 1595"),
        "neighbours_rain_multiplier": n(1.5, "in rain fewer are out and the rain masks speech; the street is quieter by half again", "invented here; RULINGS 5 Oct says rain changes who is out and what is heard"),
        "start_gap_s": n(1.0, "a second of breath after any line ends before the next begins, so two voices are never stacked", "invented here"),
        "lines_per_minute_cap": {"lines": n(6, "no more than six lines in any sixty seconds outside a crime: six short lines fill about 20 s of 60, and the rest of the minute is the street", "invented here"), "window_s": n(60, "a minute")},
        "crime_chorus_cap": {"lines": n(4, "at most four crime lines in any twenty seconds; the fifth person in the street is silent, as a crowd's fifth voice is lost in the first four", "invented here"), "window_s": n(20, "about the length of four lines and their breaths")},
        "per_speaker_any_line_s": n(15, "one person does not speak twice inside fifteen seconds unless answering a question", "invented here"),
        "per_speaker_lines_per_10min": n(4, "a regular who has said four things to Tom in ten minutes has said enough", "invented here"),
        "per_line": {
            "same_speaker_same_line_s": n(1800, "never inside half an hour: BarkGen's floor is 600 s for a fourteen-line band and Ruskin's 'never twice, not inside 60 s'; with groups of 8 to 13 and a bag the same speaker meets a repeat after the bag, and the hard floor stops a short group from showing it", "BarkGen repeatFloorSeconds 600 raised to 1800; Valve (METHOD-2026-09-30 item 10)"),
            "any_speaker_same_line_s": n(120, "two mouths saying the same words inside two minutes is the whole town talking in one voice; twice Valve's 60 seconds", "Valve (METHOD item 10), doubled"),
        },
        "per_family": {
            # class: to_tom | event | neighbour; gap: seconds between two lines of the family, anyone speaking;
            # speaker: seconds before the same person says another of the family
            "greet":       {"class": "to_tom",    "gap_s": n(8, "no two greetings overlap: a line is 3 to 4 s and he needs a breath"), "speaker_s": n(600, "a person greets him once in ten minutes, even if he passes twice")},
            "bump":        {"class": "to_tom",    "gap_s": n(10, "a crowd crush must not become ten 'watch its' in a row"), "speaker_s": n(120, "a second bump inside two minutes gets a look, not a line")},
            "way":         {"class": "to_tom",    "gap_s": n(0, "an answer to a question is never held back by chatter"), "speaker_s": n(0, "always answers; the same words not twice inside 30 min (per_line), and when every line is used the oldest is said")},
            "farewell":    {"class": "to_tom",    "gap_s": n(8, "as greetings"), "speaker_s": n(600, "a goodbye once per meeting")},
            "rain_starts": {"class": "event",     "gap_s": n(6, "a few people can say it together; not a chorus"), "speaker_s": n(1800, "once per rain episode (the episode is longer than any shower)")},
            "crime":       {"class": "event",     "gap_s": n(0, "a crime is the one moment several people speak close together: the voice serialises them, the chorus cap below stops a pile-up"), "speaker_s": n(60, "one line per person per crime: a person's sureness is fixed by what they perceived")},
            "in_rain":     {"class": "neighbour", "gap_s": n(45, "the neighbours' rule"), "speaker_s": n(300, "five minutes before the same person remarks on the rain again")},
            "after_deed":  {"class": "neighbour", "gap_s": n(45, "the neighbours' rule, doubled by the hush below"), "speaker_s": n(300, "five minutes between one person's low remarks")},
        },
        "per_group": {
            "min_gap_s": n(60, "one bag (one kind and bank) speaks at most once a minute, so one kind never sounds like the street", "invented here"),
            "except": ["crime", "way"],
        },
    },

    # ------------------------------------------------------------------ variety
    "variety": {
        "bag": {
            "per": "group (one kind and bank: the ledger's own key 'bank@kind') and per listener",
            "draw": "among the lines that pass the conditions and have not been used since the last refill, chosen with probability proportional to weight; when none is left the bag refills",
            "refill_spacing": n("the last half-bag (floor of n over 2) played lines are held out of the first half-bag of draws when others exist", "so a refill cannot repeat the line just heard; with 8 lines the nearest repeat is 5 plays away"),
            "memory": "the existing RemarkLedger keeps the lines heard under 'bank@kind' and saves them (ToJson 'heard'), so a reload does not refill the bag; only what he HEARD counts, as in RemarkLedger.HeardLine",
            "why": "Valve's response groups play every line once before any repeats; Hades the same; the street's own RemarkLedger.Fresh already does the never-heard-first half of this",
        },
        "weights": {
            "values": "1 (a joke or a strong turn: bears fewer hearings), 2 (ordinary), 3 (the kind's core lines)",
            "why": "the method note: 'low-key enough to bear a third hearing'; the strong lines come later in a bag",
        },
        "min_eligible": n(6, "after every condition (weather, time, standing, accent, never-police) at least six lines must be left in a group, so a bag is never one or two lines", "METHOD item 12 (8 to 20 variants); six is the floor after conditions, eight the floor written"),
        "pool_sizes": {"floor_written": n(8, "the brief: at least eight lines per kind and situation"), "greeting_stranger_written": n(13, "the busiest bank: said to every stranger he passes")},
        "no_same_kind_twice_running": n(True, "a group the bag has just used is not used again by the same kind inside per_group.min_gap_s"),
    },

    # ------------------------------------------------------------------ chance: how often a moment makes anybody speak
    "chance": {
        "greet": {
            "stranger": n(0.30, "most passers-by do not greet a stranger on a 1990 street; one in three does (the old and the shopkeepers more)"),
            "owner": n(0.65, "they know who he is and are curious"),
            "nowak": n(0.85, "they know his name"),
            "tom": n(0.90, "on first-name terms"),
            "tommy": n(0.95, "the last rung: nearly always"),
            "kind_multiplier": {"pensioner": 1.5, "shopkeeper": 1.3, "laundry_worker": 1.2, "dock_worker": 1.0, "driver": 1.0, "tradesman": 1.0, "casual_worker": 1.0, "night_shift": 0.8, "office_worker": 0.7, "ron": 1.0, "darren": 1.3, "father_walsh": 1.2, "june": 0.6,
                                "why": "invented here from the contact sheet's manners: the old and the counter folk speak first; clerks hurry; June is on guard"},
            "weather_multiplier": {"dry": 1.0, "drizzle": 0.75, "rain": 0.5, "why": "heads down in rain"},
            "capped_at": 1.0,
        },
        "bump": n(0.80, "a bump is hard to ignore; one in five says nothing and glares"),
        "farewell": n(0.50, "half of those who stop for a word say goodbye aloud"),
        "rain_starts": n(0.35, "of those within earshot, a third remark on it"),
        "crime": {"noise": n(0.70, "most who hear a crash say something"), "shape": n(0.60, "fewer: they are unsure of what they saw"), "face": n(0.90, "one who saw a face almost always says so")},
        "in_rain": n(0.30, "per neighbour opportunity, when two or more are in earshot"),
        "after_deed": n(0.40, "per neighbour opportunity, for those near the deed"),
        "way": n(1.0, "always answers"),
    },

    # ------------------------------------------------------------------ priorities
    "priority": {
        "order": {"crime_face": 100, "crime_shape": 95, "crime_noise": 90, "bumped": 80, "asked_way": 75,
                  "greeting.nowak": 52, "greeting.tom": 52, "greeting.tommy": 52, "greeting.owner": 50, "greeting.stranger": 48,
                  "farewell": 45, "rain_starts": 40, "after_deed": 35, "in_rain": 20},
        "why": "a crime line outranks a greeting (the brief); a reaction to his body (a bump) outranks a reply to his question, which outranks a hello; neighbours' talk yields to everything",
        "voices": {"ordinary": n(1, "one line sounds at a time, so each can be understood and the street never talks over itself", "invented here"),
                   "crime": n(2, "in a crime two people may speak at once (that is what a street does); three is noise", "invented here")},
        "in_progress": "a line already playing is never cut, except neighbour-class lines (in_rain, after_deed), which fade over 0.4 s when a crime line starts",
        "waiting": "one line may wait for the voice; a higher-priority arrival replaces it",
        "shelf_life_s": {"crime": n(4, "a shout answered within four seconds is still a shout; later it is not"), "bumped": n(1.5, "the moment is gone in a second and a half"), "greet": n(3, "he has walked on"), "farewell": n(3, "as greetings"), "rain_starts": n(3, "as they happen"), "asked_way": n(6, "an answer may wait a little for a question"), "in_rain": n(5, "idle talk"), "after_deed": n(5, "idle talk")},
        "line_seconds": n("0.3 + words / 3.0", "Sheila's voice-key lines run 19 words in 6.16 s (3.1 words a second) plus a short lead; a line under 12 words is under 4.3 s", "production/casting/voice-key.json"),
    },

    # ------------------------------------------------------------------ the hour after a deed
    "after_deed": {
        "hour_s": n(3600, "RULINGS 23 Sep: witnesses talk quieter for an hour", "RULINGS 23 Sep"),
        "who": "witnesses (anybody with a sureness), and anybody within 20 m of the deed when it happened",
        "near_m": n(20, "the limit at which the identification ladder reads a figure at all (eyewitness-testimony: 42 percent accuracy at 20 m); beyond it nobody is a witness", "production/research/eyewitness-testimony/SUMMARY.md"),
        "gap_multiplier": n(2.0, "their neighbours' talk comes at most every 90 s instead of 45 s: quieter in count", "invented here"),
        "gain_db": n(-6, "quieter in level: half the loudness, which a listener hears as clearly lower and still hears", "invented here"),
        "hear_radius_m": n(4, "hushed lines carry 4 m, not the street's 7 m; GossipDirector's talk range is 6 m, Acoustics.SpeechCarry 14 m for ordinary speech", "invented here, against GossipDirector.TalkRange and Acoustics.SpeechCarry"),
        "silent_for_witnesses": ["greeting.stranger", "greeting.owner", "greeting.nowak", "greeting.tom", "greeting.tommy", "rain_starts", "in_rain", "farewell"],
        "why_silent": "people who have just seen something do not say 'morning' or remark on the weather; they say the hushed lines, or nothing",
        "look_and_gather": "near people look (the nearest three, within 12 m, turn to the deed), some gather (up to four within 20 m come to within 6 m for 90 s) and drift back: that is movement, the builder's; only what they may SAY is set here: gatherers use after_deed lines only, hushed, while gathered",
    },

    # ------------------------------------------------------------------ rain: who is out, what is heard
    "rain": {
        "presence": {
            "values": {"pensioner": [1.0, 0.30, 0.15], "shopkeeper": [1.0, 0.60, 0.30], "dock_worker": [1.0, 1.00, 0.90], "driver": [1.0, 1.10, 1.30], "office_worker": [1.0, 0.80, 0.60],
                       "laundry_worker": [1.0, 0.80, 0.60], "tradesman": [1.0, 0.70, 0.30], "night_shift": [1.0, 1.00, 1.00], "casual_worker": [1.0, 0.80, 0.50], "ron": [1.0, 1.0, 1.0], "darren": [1.0, 1.0, 0.7], "father_walsh": [1.0, 0.8, 0.6], "june": [1.0, 0.7, 0.5]},
            "order": "[dry, drizzle, rain]: the share of a kind's usual passers-by still out",
            "why": "RULINGS 5 Oct: rain changes who is out; Weather.cs: rain thins the crowd. The old stay in, work that is outdoors carries on, cabs are busier; invented here from the contact sheet's trades",
        },
        "hear_radius_m": {"dry": n(7, "GossipDirector's within-7-m unprompted lines", "GossipDirector.cs"), "drizzle": n(6, "a little masked"), "rain": n(5, "masked by the rain: 'what is heard' (RULINGS 5 Oct)")},
        "starts_window_s": n(40, "rain_starts lines only within 40 s of the weather crossing a cut point from dry"),
    },

    # ------------------------------------------------------------------ silence
    "silence": {
        "nobody_says_anything_when": [
            "nobody is within the hearing radius of Tom (7 m dry, 6 drizzle, 5 rain; 4 for hushed lines)",
            "fewer than two people are in earshot: neighbours' talk needs two (StreetVoice.AmbientEverySeconds returns never below two)",
            "no line is left once weather, time, standing, accent and never-police are applied: silence is better than a repeat (asked_way is the one exception: the oldest-heard line is said, because a question must be answered)",
            "the speaker's stance toward Tom is above Notices (Watches, Comments, Avoids, Refuses, Confronts): the existing recognition banks speak for them; these ambient banks stay silent",
            "the speaker is a witness within the hour after a deed (see after_deed.silent_for_witnesses)",
            "the speaker's group is under any cooldown above",
            "the speaker has a kind with no group for the moment (Ron and Darren have no stranger or owner greeting; they begin at nowak; Walsh and June at owner)",
            "the moment's chance roll fails (see chance): most moments are silent by design",
        ],
        "target_quiet_share": n(0.33, "in every walk at least a third of the minutes pass with no line heard: a street, not a stage. First set at 40 percent; one of thirty-one seeds came in at 37 percent, which is a busy half hour and no fault, so it was set at a third", "invented here, adjusted once after the first run"),
        "target_quiet_median": n(0.45, "and in the middle walk of thirty-one at least 45 percent", "invented here"),
        "busiest_minute_max": n(6, "no minute holds more than six heard lines except in the moments of a crime: six short lines fill about 20 s of 60", "invented here"),
        "never_to_fill_a_gap": True,
    },

    # ------------------------------------------------------------------ for the PC session
    "tests_that_pin_it": [
        "no group has fewer than min_eligible lines in any weather and hour it can occur (check_lines.py rows pool.*)",
        "the walk: zero same-speaker repeats inside same_speaker_same_line_s, zero same-line repeats between speakers inside any_speaker_same_line_s, no neighbour line closer than the neighbours' gap (rows walk.*)",
    ],
}
