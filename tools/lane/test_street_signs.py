"""Tests for street_signs.py (lane session, 17 November 2026).

Run from the repo root: python3 -m pytest tools/lane/test_street_signs.py
"""
import json
import os
import sys
import xml.etree.ElementTree as ET

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import street_signs as ss  # noqa: E402


def part(stop, name):
    return next(p for p in stop["parts"] if p["name"] == name)


# ---- sizes

def test_flag_size_from_research():
    flag = part(ss.bus_stop(), "flag")
    assert flag["size"]["width"] == {"mm": 300, "source": "sourced"}
    assert flag["size"]["height"] == {"mm": 450, "source": "sourced"}


def test_route_numerals_one_inch():
    assert ss.BUS_STOP["route_numeral_height"] == (25.4, "sourced")


def test_unsourced_sizes_marked_est():
    for key in ("pole_height", "pole_diameter", "timetable_case_width",
                "shelter_length", "flag_bottom_height"):
        assert ss.BUS_STOP[key][1] == "est"
    for key, (_, src) in ss.TIME_PLATE.items():
        assert src == "est", key


def test_every_dimension_has_a_source_tag():
    for table in (ss.BUS_STOP, ss.TIME_PLATE):
        for value, src in table.values():
            assert value > 0 and src in ("sourced", "est")


def test_flag_above_head_height_and_below_pole_top():
    stop = ss.bus_stop()
    flag, pole = part(stop, "flag"), part(stop, "pole")
    top = flag["position"][2] + flag["size"]["height"]["mm"]
    assert flag["position"][2] >= 2100
    assert top <= pole["size"]["height"]["mm"]


def test_timetable_case_below_flag():
    stop = ss.bus_stop()
    case, flag = part(stop, "timetable_case"), part(stop, "flag")
    assert case["position"][2] + case["size"]["height"]["mm"] < flag["position"][2]


def test_shelter_off_by_default_on_when_asked():
    assert "shelter" not in [p["name"] for p in ss.bus_stop()["parts"]]
    assert "shelter" in [p["name"] for p in ss.bus_stop(shelter=True)["parts"]]


def test_flag_only_mount_has_no_pole():
    names = [p["name"] for p in ss.bus_stop(mount="flag")["parts"]]
    assert "pole" not in names and "flag" in names


def test_bad_mount_and_route():
    with pytest.raises(ValueError):
        ss.bus_stop(mount="wall")
    with pytest.raises(ValueError):
        ss.bus_stop(route_numbers=("X99A",))


def test_time_plate_size_and_height():
    plate = ss.time_plate()
    assert plate["size"]["width"]["source"] == "est"
    assert plate["mount_height"]["mm"] + plate["size"]["height"]["mm"] < 2500


# ---- text legal for 1990

def test_default_plate_text():
    assert ss.time_plate()["text"] == ["No waiting", "Mon - Sat", "8 am - 6 pm"]


def test_noon_and_pm():
    assert ss.time_plate(start_hour=8, end_hour=18)["text"][2] == "8 am - 6 pm"
    assert ss.time_plate(start_hour=9, end_hour=17)["text"][2] == "9 am - 5 pm"
    assert ss._hour_text(12) == "noon"


@pytest.mark.parametrize("args", [
    ("double", "Mon", "Wed", 8, 18),   # three days
    ("double", "Mon", "Fri", 9, 16),   # seven hours
    ("double", "Mon", "Fri", 10, 17),  # seven hours
    ("double", "Mon", "Fri", 3, 14),   # 11 h, but only 7 inside 7 am to 7 pm
    ("double", "Mon", "Fri", 13, 23),  # 10 h, but only 6 inside
    ("double", "Fri", "Mon", 8, 18),   # days reversed
    ("triple", "Mon", "Fri", 8, 18),
])
def test_restrictions_refused(args):
    assert ss.validate_restriction(*args)
    with pytest.raises(ValueError):
        ss.time_plate(*args)


@pytest.mark.parametrize("start,end,shown", [
    (7, 20, "7 am - 8 pm"),    # runs past 7 pm: Hansard rule still met
    (9, 17, "9 am - 5 pm"),    # exactly eight hours passes
    (6, 18, "6 am - 6 pm"),
])
def test_double_hours_counted_inside_7_to_7(start, end, shown):
    assert ss.validate_restriction("double", "Mon", "Fri", start, end) == []
    assert ss.time_plate("double", "Mon", "Fri", start, end)["text"][2] == shown


def test_midnight():
    assert ss._hour_text(0) == "midnight"
    assert ss._hour_text(24) == "midnight"
    assert ss.time_plate("single", "Mon", "Sun", 0, 24)["text"][2] == \
        "midnight - midnight"


def test_waiting_plates_on_columns_marked_inferred():
    assert ss.time_plate()["on_lamp_columns"] == {"value": True,
                                                  "source": "inferred"}


def test_flag_facing_explicit_and_est():
    stop = ss.bus_stop()
    flag, pole = part(stop, "flag"), part(stop, "pole")
    assert flag["face_normal"] == [1, 0, 0]
    assert flag["width_axis"] == "y"
    assert flag["facing"]["source"] == "est"
    assert flag["orientation"]["source"] == "est"
    # stands out from the pole toward the carriageway (smaller y)
    assert flag["position"][0] == pole["position"][0]
    assert flag["position"][1] < pole["position"][1]


def test_operator_is_the_invented_name():
    assert ss.DEFAULT_OPERATOR == "Saltmarrow Omnibus Company"
    assert "Saltmarrow Omnibus Company" in part(ss.bus_stop(), "flag")["text"]


def test_single_line_may_be_shorter():
    plate = ss.time_plate("single", "Mon", "Fri", 8, 10)
    assert plate["text"][2] == "8 am - 10 am"


def test_no_modern_or_canon_words_in_any_output():
    texts = (ss.time_plate()["text"] + part(ss.bus_stop(), "flag")["text"]
             + part(ss.bus_stop(), "timetable_case")["text"])
    assert ss.check_text(texts) == []
    # Every visible word on both SVG faces, not the SVG namespace URL.
    svg_text = []
    for svg in (ss.time_plate()["svg"], ss.bus_stop()["flag_svg"]):
        svg_text += [t.text for t in ET.fromstring(svg).iter(
            "{http://www.w3.org/2000/svg}text")]
    assert ss.check_text(svg_text) == []
    blob = " ".join(svg_text).lower()
    for word in ("http", "www", "cctv", "at any time", "pub", "betting", "casino"):
        assert word not in blob


def test_check_text_catches_modern_words():
    assert "at any time" in ss.check_text(["No waiting at any time"])
    assert "cctv" in ss.check_text(["CCTV enforcement"])
    assert "www" in ss.check_text(["www.example"])
    assert ss.check_text(["Barton Road"]) == []   # 'bar' only as a whole word


@pytest.mark.parametrize("line,word", [
    ("Next to the (pub)", "pub"), ("pub-side stop", "pub"),
    ("beer's here", "beer"), ("CHILDREN crossing", "children"),
    ("Near the playground", "playground"), ("Nursery Lane", "nursery"),
    ("SCHOOL KEEP CLEAR", "school keep clear"), ("Bingo/hall", "bingo"),
])
def test_check_text_splits_on_non_letters(line, word):
    assert word in ss.check_text([line])


def test_check_text_no_false_hits_inside_words():
    assert ss.check_text(["Sale Street", "Betty Road", "Puberty"]) == []


def test_operator_with_forbidden_word_refused():
    with pytest.raises(ValueError):
        ss.bus_stop(operator="Casino Coaches")


# ---- SVG

def test_svgs_parse_and_carry_text():
    for svg, words in ((ss.time_plate()["svg"], "No waiting"),
                       (ss.bus_stop()["flag_svg"], "Bus stop")):
        root = ET.fromstring(svg)
        assert root.tag.endswith("svg")
        texts = [t.text for t in root.iter("{http://www.w3.org/2000/svg}text")]
        assert words in texts


def test_svg_viewbox_matches_plate_size():
    root = ET.fromstring(ss.time_plate()["svg"])
    assert root.get("viewBox") == "0 0 250 200"
    root = ET.fromstring(ss.bus_stop()["flag_svg"])
    assert root.get("viewBox") == "0 0 300 450"


def test_svg_escapes_text():
    svg = ss.bus_flag_svg(["Bus stop", "A & B Buses", "7"])
    ET.fromstring(svg)


# ---- placement

def check_spacing(res, length, interval):
    xs = [p["x"] for p in res["plates"]]
    assert xs == sorted(xs)
    assert xs[0] <= interval / 2
    assert xs[-1] >= length - interval / 2 or xs[-1] == length
    for a, b in zip(xs, xs[1:]):
        assert b - a <= interval + 1e-6


def test_columns_cover_kerb_no_posts():
    res = ss.place_time_plates(48000, [8000, 28000], interval=40000)
    assert res["posts"] == 0 and res["gaps_needing_posts"] == []
    assert all(p["mount"] == "lamp_column" for p in res["plates"])
    check_spacing(res, 48000, 40000)


def test_no_columns_all_posts():
    res = ss.place_time_plates(100000, [], interval=30000)
    assert res["posts"] == len(res["plates"]) == len(res["gaps_needing_posts"])
    check_spacing(res, 100000, 30000)


def test_gap_between_columns_reported():
    res = ss.place_time_plates(100000, [10000, 90000], interval=30000)
    assert res["posts"] >= 2
    for g in res["gaps_needing_posts"]:
        assert 10000 < g["post_at"] < 90000
    check_spacing(res, 100000, 30000)


def test_close_columns_before_a_post_get_one_plate():
    # Review case: kerb 100 m, columns at 29 m and 31 m, interval 60 m.
    # Old greedy gave 29, 31 and a post at 91; now 29 and a post at 89.
    res = ss.place_time_plates(100000, [29000, 31000], interval=60000)
    xs = [(p["x"], p["mount"]) for p in res["plates"]]
    assert xs == [(29000, "lamp_column"), (89000, "post")]
    assert res["posts"] == 1
    check_spacing(res, 100000, 60000)


def test_close_columns_kept_when_they_save_a_post():
    # 29 and 31 m with a third column at 85 m: the run goes on from 31 m.
    res = ss.place_time_plates(100000, [29000, 31000, 85000], interval=60000)
    assert res["posts"] == 0
    check_spacing(res, 100000, 60000)


def test_short_kerb_single_plate():
    res = ss.place_time_plates(5000, [], interval=60000)
    assert len(res["plates"]) == 1
    assert res["plates"][0]["x"] == 5000


def test_column_at_ends_and_outside_kerb_ignored():
    res = ss.place_time_plates(20000, [-500, 0, 20000, 25000], interval=20000)
    xs = [p["x"] for p in res["plates"]]
    assert -500 not in xs and 25000 not in xs
    assert all(p["mount"] == "lamp_column" for p in res["plates"])
    check_spacing(res, 20000, 20000)


def test_duplicate_and_unsorted_columns():
    a = ss.place_time_plates(60000, [40000, 10000, 10000, 40000], interval=30000)
    b = ss.place_time_plates(60000, [10000, 40000], interval=30000)
    assert a == b


def test_bad_inputs():
    with pytest.raises(ValueError):
        ss.place_time_plates(0, [])
    with pytest.raises(ValueError):
        ss.place_time_plates(1000, [], interval=0)


@pytest.mark.parametrize("length,interval", [(1000, 600), (48000, 7000),
                                             (123456, 25000), (90000, 90000)])
def test_spacing_rule_holds(length, interval):
    cols = list(range(3000, length, 11000))
    check_spacing(ss.place_time_plates(length, cols, interval=interval),
                  length, interval)


def test_plates_on_columns_use_mount_height():
    res = ss.place_time_plates(48000, [8000, 18000, 28000, 38000], interval=20000)
    assert all(p["z"] == ss.TIME_PLATE["mount_height"][0] for p in res["plates"])


# ---- determinism

def test_deterministic_and_json_able():
    a = json.dumps({"b": ss.bus_stop(shelter=True), "t": ss.time_plate(),
                    "p": ss.place_time_plates(48000, [8000, 18000, 28000, 38000])},
                   sort_keys=True)
    b = json.dumps({"b": ss.bus_stop(shelter=True), "t": ss.time_plate(),
                    "p": ss.place_time_plates(48000, [8000, 18000, 28000, 38000])},
                   sort_keys=True)
    assert a == b
