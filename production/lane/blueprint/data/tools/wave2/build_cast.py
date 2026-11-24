#!/usr/bin/env python3
"""Build cast.json: the index of people/, the fighter kinds (1.3.12), Frank's name ladder and the rule that will make
the 200 to 300 residents after the first loops (his ruling: the rule now, the people later). Written 24 Nov 2026."""
import json, os, sys
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.normpath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, HERE)
from build_people import C

people = [{"id": p['id'], "name": p['n'], "called": p.get('called') or p['n'], "kind": p['k'], "age": p['a'],
           "invented": (p.get('inv') if p.get('inv') != 'frame' else 'proposed by the story frame') or False} for p in C.P]
counts = Counter(p['k'] for p in C.P)
inv = Counter('invented here' if p.get('inv') is True else 'proposed by the frame' if p.get('inv') == 'frame' else 'canon or earlier cast files' for p in C.P)
out = {
    "file": "cast.json", "version": "wave2-2026-11-24", "clock": {"realSecondsPerGameHour": 120},
    "sources": ["tools/wave2/cast_src.py", "STORY-FRAME-2026-11-26 sections 3 and 4", "production/cloud-week/town/people.json (44)",
                "production/specs/hook-cast.json (41)", "tools/lane/prototype/project/src/cast.js (28 looks and cards)",
                "game-design/town-traits-draft-2026-09-29.md (temper figures)", "tools/lane/prototype/project/src/game/tune/fightx.js (fighter kinds)"],
    "counts": {"people": len(C.P), "by_kind": dict(counts), "by_origin": dict(inv)},
    "name_ladder": ["the new owner", "Nowak", "Frank", "Frankie"],
    "name_ladder_note": "Decision of 24 Nov: the lead is Frank Nowak (Polish father, British mother, Mickey Suddaby's nephew). Nobody says Tom or Tommy. The frame's 'three people say Tommy at the fourth rung' becomes Frankie: the Widow to own him, Danny to needle him, Ron once, if ever. Danny's own needle is 'nephew', outside the ladder.",
    "fighter_kinds": {
        "rule": "1.3.12: every fight's men are one of five kinds; a big man has the most hidden capacity and a knife man the least; no two fights in a row use the same mix. guards and rushes are shares of the time; takes is hidden capacity against an average man's 1.0.",
        "boxer": {"guards": 0.7, "rushes": 0.2, "takes": 1.0, "keeps_distance": False, "src": "prototype fightx.js"},
        "brawler": {"guards": 0.1, "rushes": 0.8, "takes": 1.0, "keeps_distance": False, "src": "prototype fightx.js"},
        "big_man": {"guards": 0.3, "rushes": 0.3, "takes": 1.6, "keeps_distance": False, "src": "prototype fightx.js ('big man')"},
        "knife_man": {"guards": 0.2, "rushes": 0.55, "takes": 0.75, "keeps_distance": True, "src": "prototype fightx.js 'knife' (takes 0.9 there); lowered to 0.75 so a knife man has the least capacity, as 1.3.12 says (chosen)"},
        "wiry": {"guards": 0.4, "rushes": 0.3, "takes": 0.85, "keeps_distance": False, "slips_and_runs": True, "src": "1.3.12 (from the fit check: a wiry one who slips and runs); figures chosen here"},
        "note": "Each person who fights carries fight_kind in people/<id>.json. Capacities are working values until the fights are measured (1.3.12 is pending a reference-game study)."},
    "residents_rule": {
        "ruling": "His ruling: the 200 to 300 residents beyond the named cast are added after the first loops. Not made now; this is the rule that will make them.",
        "count": "200 to 300 in all, made in one seeded pass (seed written into the file) so the same town comes out every time.",
        "homes": "One to three adults to each map.json plot whose use is home and which no named person holds (people/<id>.json home), no plot over its storeys times two.",
        "ages": "18 to 90 only (no children anywhere). Spread for a 1990 northern port with the docks run down: about a third 60 and over, a fifth 18 to 29.",
        "names": "First names and surnames drawn from a list of 1990 northern English port names with Irish (about one in eight), Polish (about one in twenty-five, mostly 60 and over: the post-war settlers and their children) and other origins as production/casting research gives; never a name already in people/; never a real public figure.",
        "work": "From the places.json staff each place needs and the crowd.json bands: dock and cold-store shifts, shop staff, retired. Every resident's routine follows routines.json's rules and is checked by tools/wave2/build_people.py's reach and hours check.",
        "kind": "passer; temperament drawn from a small table by age and work (the traits draft's figures for an unnamed worker: nerve 0.3 to 0.5, loyalty 0.3, a wounding seen yes or no); keepsQuiet false unless loyalty 0.6 or more.",
        "lines": "Shared street lines by speaker kind only (lines/shared-street.json); no own lines.",
        "look": "crowd.json's 1990 look tables.",
        "content": "No alcohol or gambling in any routine or line, no children, every brand fictional (the content rule)."},
    "people": people,
    "open_points": [
        "The story lane's CAST.md and CAST-CHANGES.md had not landed when this file was made; every name marked proposed by the frame, and every invented one, is open to them.",
        "Frank Stathers (frame, proposed) is renamed Vic Stathers here so that the lead is the only Frank; the story lane should confirm or choose another.",
        "Wave 1 placeholders replaced here: the cold-store manager 'Norman' becomes Eric Tharratt (frame); the Harbour Board 'clerk Susan' is Christine Pickering (canon regular, side story 20; Susan Coverdale is the customs officer); the bought officers' prototype hints PC Harker and DC Pollitt become the frame's PC Trevor Garton and DC Graham Wardell; Portside Cars' owner Len Wardle becomes Len Ackroyd so he is not mistaken for DC Wardell.",
        "Prototype card texts that named a real police force or city (Humberside CID, Hull vowels) are scrubbed to CID and northern vowels."]}
json.dump(out, open(os.path.join(D, 'cast.json'), 'w'), indent=1, ensure_ascii=False)
print('cast.json', len(people), dict(counts), dict(inv))
