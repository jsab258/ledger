#!/usr/bin/env python3
"""Write schemas.json (blueprint data file 19): the record format of every data file.

Written 24 Nov 2026. For the thirteen files made in wave 1 the formats are read from the files
themselves (types of every field, fields present in every record marked required) and then held
fixed: a later edit that drops a required field or changes a type fails validate_data.py. The six
files still to come (people, ties, routines, lines, jobs and the rest, scenes) are written by hand
from TECH-PLAN section 3 and the data sweep's section 3, so the story lane's output can be tested
the day it lands. Schema dialect: a small subset of JSON Schema (type, required, properties, items,
additionalProperties, enum, minimum, maximum, pattern), checked by validate_data.py with no library.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, '..')
WAVE1 = ['map.json', 'rooms.json', 'places.json', 'timetables.json', 'tune.json', 'police.json', 'crowd.json', 'vehicles.json',
         'ledger-texts.json', 'letters-and-print.json', 'ui-text.json', 'content-words.json', 'light-weather.json', 'sounds.json']

def jtype(v):
    if v is None: return 'null'
    if isinstance(v, bool): return 'boolean'
    if isinstance(v, int): return 'integer'
    if isinstance(v, float): return 'number'
    if isinstance(v, str): return 'string'
    if isinstance(v, list): return 'array'
    return 'object'

def merge_types(ts):
    ts = set(ts)
    if 'number' in ts and 'integer' in ts:
        ts.discard('integer')
    return sorted(ts)[0] if len(ts) == 1 else sorted(ts)

def infer(values, depth=0):
    """Schema for a list of sample values of one field."""
    types = [jtype(v) for v in values]
    s = {'type': merge_types(types)}
    if depth > 4:
        return s
    objs = [v for v in values if isinstance(v, dict)]
    if objs and len(objs) == len([t for t in types if t == 'object']):
        keys = {}
        for o in objs:
            for k, v in o.items():
                keys.setdefault(k, []).append(v)
        # a dict used as a map (many keys, few repeats) is described by its values only
        if len(keys) > 40 and max(len(v) for v in keys.values()) <= 2:
            allv = [v for vs in keys.values() for v in vs]
            s['additionalProperties'] = infer(allv, depth + 1)
        else:
            s['properties'] = {k: infer(v, depth + 1) for k, v in sorted(keys.items())}
            req = sorted(k for k, v in keys.items() if len(v) == len(objs))
            if req and len(objs) > 1:
                s['required'] = req
    arrs = [v for v in values if isinstance(v, list)]
    if arrs:
        items = [x for a in arrs for x in a]
        if items:
            s['items'] = infer(items, depth + 1)
    return s

def from_file(name):
    data = json.load(open(os.path.join(D, name)))
    s = infer([data])
    s['required'] = sorted(k for k in ('file', 'version', 'sources', 'open_points') if k in data) + (['clock'] if 'clock' in data else [])
    s['x-made'] = 'wave 1, read from the file 2026-11-24'
    return s

ID = {'type': 'string', 'pattern': '^[a-z0-9_.:-]+$'}
SRC = {'type': 'string'}
HEAD = {'file': {'type': 'string'}, 'version': {'type': 'string'}, 'clock': {'type': 'object', 'required': ['realSecondsPerGameHour'],
        'properties': {'realSecondsPerGameHour': {'type': 'integer', 'minimum': 120, 'maximum': 120}}},
        'sources': {'type': 'array', 'items': {'type': 'string'}}, 'open_points': {'type': 'array'}}
TIME = {'type': 'string', 'pattern': '^([01][0-9]|2[0-9]):[0-5][0-9]$'}
DAYS = {'type': 'string', 'pattern': '^(mon|tue|wed|thu|fri|sat|sun)(-(mon|tue|wed|thu|fri|sat|sun))?(,(mon|tue|wed|thu|fri|sat|sun))*$|^daily$'}

TO_COME = {
    'people/<id>.json': {
        'x-made': 'by hand from TECH-PLAN section 3 (people); waits on the story frame', 'type': 'object',
        'required': ['id', 'cast_id', 'name', 'age', 'sex', 'role', 'kind', 'voice', 'look', 'temperament', 'keepsQuiet', 'sched', 'card', 'can_die', 'src'],
        'properties': {
            'id': ID, 'cast_id': {'type': ['string', 'null']}, 'called': {'type': 'string'}, 'name': {'type': 'string'},
            'age': {'type': 'integer', 'minimum': 18, 'maximum': 95}, 'sex': {'type': 'string', 'enum': ['m', 'f']},
            'role': {'type': 'string'}, 'kind': {'type': 'string', 'enum': ['principal', 'firm', 'regular', 'minor', 'rival_man', 'passer', 'officer']},
            'voice': {'type': ['string', 'null']}, 'look': {'type': 'object'},
            'nerve': {'type': 'number', 'minimum': 0, 'maximum': 1}, 'venal': {'type': 'number', 'minimum': 0, 'maximum': 1},
            'talk': {'type': 'number', 'minimum': 0, 'maximum': 1}, 'discretion': {'type': 'number', 'minimum': 0, 'maximum': 1},
            'temperament': {'type': 'object', 'required': ['nerve', 'dutiful', 'willingness'],
                            'properties': {k: {'type': 'number', 'minimum': 0, 'maximum': 1} for k in ('nerve', 'dutiful', 'willingness')}},
            'keepsQuiet': {'type': 'boolean'},
            'sched': {'type': 'array', 'items': {'type': 'array'}, 'x-note': '[fromHour, where (a places.json id), act, days?]'},
            'lines': {'type': 'object'}, 'card': {'type': 'object', 'required': ['who', 'speak', 'life']},
            'can_die': {'type': 'boolean'}, 'fallback_role': {'type': 'string'}, 'src': SRC},
        'x-rules': ['age 18 or over: no children anywhere (canon)', 'every sched place is a places.json id', 'Tom has can_die false']},
    'ties.json': {
        'x-made': 'by hand from TECH-PLAN section 3 (ties, the real town\'s form)', 'type': 'object', 'required': ['file', 'version', 'ties'],
        'properties': dict(HEAD, ties={'type': 'array', 'items': {'type': 'array', 'x-note': '[a, b, strength 0..1, "place hh:mm days; ..."]'}})},
    'routines.json': {
        'x-made': 'by hand from the sweep (file 4)', 'type': 'object', 'required': ['file', 'version', 'clock', 'routines'],
        'properties': dict(HEAD, routines={'type': 'array', 'items': {'type': 'object', 'required': ['person', 'rows', 'src'],
            'properties': {'person': ID, 'src': SRC, 'rows': {'type': 'array', 'items': {'type': 'object', 'required': ['from', 'place', 'act'],
                'properties': {'from': TIME, 'place': ID, 'act': {'type': 'string'}, 'days': DAYS}}}}}}),
        'x-rules': ['every place is a places.json id', 'a move between consecutive rows is reachable on the map graph at walking pace in the game time between them (the 200 m walking-reach rule checked on the 120 s hour)']},
    'lines/<file>.json': {
        'x-made': 'by hand from TECH-PLAN section 3 (lines)', 'type': 'object', 'required': ['file', 'version', 'lines'],
        'properties': dict(HEAD, lines={'type': 'array', 'items': {'type': 'object', 'required': ['id', 'who', 'situation', 'text', 'once', 'src'],
            'properties': {'id': ID, 'who': {'type': 'string'}, 'situation': {'type': 'string'}, 'text': {'type': 'string'}, 'words': {'type': 'integer'},
                           'once': {'type': 'string', 'enum': ['day', 'week', 'game', 'never']}, 'tokens': {'type': 'array'}, 'src': SRC}}}),
        'x-rules': ['every text passes content-words.json', 'no line names a real brand, person or anything after 1992']},
    'jobs/<id>.json': {
        'x-made': 'by hand from TECH-PLAN section 3 (jobs)', 'type': 'object', 'required': ['id', 'kind', 'giver', 'steps', 'pay', 'src'],
        'properties': {'id': ID, 'kind': {'type': 'string', 'enum': ['carry', 'collection', 'break_in', 'lift', 'tail', 'minding', 'fare', 'sit_down', 'send']},
                       'giver': {'type': 'string'}, 'act_min': {'type': 'integer'}, 'rung_min': {'type': 'integer'}, 'offer': {'type': 'array'},
                       'steps': {'type': 'array', 'items': {'type': 'object', 'required': ['id', 'at', 'verb', 'keys'],
                           'properties': {'id': ID, 'at': ID, 'verb': {'type': 'string'}, 'keys': {'type': 'array', 'x-note': 'three ways to every lock'}, 'fail': {'type': ['string', 'null']}}}},
                       'pay': {'type': 'object'}, 'ledger': {'type': 'string'}, 'src': SRC},
        'x-rules': ['every step "at" is a places.json or rooms.json id', 'every break-in step has three keys']},
    'fares.json': {'x-made': 'by hand from the sweep (file 11)', 'type': 'object', 'required': ['file', 'version', 'fare_people'],
        'properties': dict(HEAD, fare_people={'type': 'array', 'items': {'type': 'object', 'required': ['id', 'name', 'rides', 'src'],
            'properties': {'id': ID, 'name': {'type': 'string'}, 'rides': {'type': 'array', 'items': {'type': 'object', 'required': ['from', 'to', 'wrinkle']}}, 'src': SRC}}})},
    'happenings.json': {'x-made': 'by hand from TECH-PLAN section 3 (scenes and happenings) and DEFINITIONS G6', 'type': 'object', 'required': ['file', 'version', 'happenings'],
        'properties': dict(HEAD, happenings={'type': 'array', 'items': {'type': 'object', 'required': ['id', 'kind', 'when', 'who', 'where', 'beats', 'src'],
            'properties': {'id': ID, 'kind': {'type': 'string'}, 'when': {'type': ['object', 'string']}, 'who': {'type': 'array'}, 'where': ID, 'beats': {'type': 'array'},
                           'sets': {'type': 'array'}, 'once': {'type': 'boolean'}, 'cool_real_minutes': {'type': 'number'}, 'src': SRC}}})},
    'side-stories/<id>.json': {'x-made': 'by hand from the sweep (file 11)', 'type': 'object', 'required': ['id', 'title', 'steps', 'src'],
        'properties': {'id': ID, 'title': {'type': 'string'}, 'steps': {'type': 'array'}, 'src': SRC}},
    'scenes/<id>.json': {'x-made': 'by hand from TECH-PLAN section 3 (scenes); waits on the story pick', 'type': 'object',
        'required': ['id', 'when', 'who', 'where', 'beats', 'src'],
        'properties': {'id': ID, 'when': {'type': ['object', 'string'], 'x-note': 'a state condition, never a clock time alone'}, 'who': {'type': 'array'},
                       'where': ID, 'beats': {'type': 'array'}, 'sets': {'type': 'array'}, 'once': {'type': 'boolean'}, 'cool_real_minutes': {'type': 'number'}, 'src': SRC}},
}

out = {'file': 'schemas.json', 'version': '2026-11-24', 'clock': {'realSecondsPerGameHour': 120},
       'sources': ['the wave 1 data files themselves', 'production/lane/blueprint/TECH-PLAN.md section 3', 'data-sweep/DATA-SWEEP-2026-11-25.md section 3'],
       'open_points': ['Wave 1 formats are read from the files as made: they hold the files to their present shape, not to an ideal one. The keeper may tighten them.',
                       'paper-map.svg and map-topdown.svg are drawings, checked by rule in validate_data.py (made from map.json, every place mark present), not by schema.'],
       'dialect': 'subset of JSON Schema: type, required, properties, items, additionalProperties, enum, minimum, maximum, pattern',
       'files': {}, 'files_to_come': TO_COME,
       'cross_checks': ['every door, plot, road and place id named by rooms, places, police, vehicles, crowd and timetables exists in map.json',
                        'every room prompt id exists in ui-text.json, or is listed in rooms.json new_prompts_needed',
                        'every room reverb kind exists in sounds.json', 'every tune:<key> reference in any file exists in tune.json',
                        'every file carries clock.realSecondsPerGameHour 120', 'no file contains a word from content-words.json patterns in player-facing text (screen only, with the out-of-fiction exemptions)',
                        'the paper map has one place mark for every map place']}
for f in WAVE1:
    out['files'][f] = from_file(f)
json.dump(out, open(os.path.join(D, 'schemas.json'), 'w'), indent=1)
print('wrote schemas.json', len(out['files']), 'wave 1 files,', len(TO_COME), 'to come')
