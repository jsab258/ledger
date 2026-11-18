"""Checks of the traffic stage 1 reference model. Run: python -m pytest -q"""
from __future__ import annotations

import csv
import math
import os
import statistics

import pytest

import make_goldens
import traffic_model as m

CD = m.load_json("cars.json")
RATES = m.load_json("rates.json")


CLOCK = m.clock_1to120(1, 0)


# --- random numbers: fixed outputs so the C++ port can be checked line by line
def test_splitmix64_known_values():
    # SplitMix64 from state 0: first output is the published 0xE220A8397B1DCDAF
    s, out = m.splitmix64(0)
    assert out == 0xE220A8397B1DCDAF
    s, out = m.splitmix64(s)
    assert out == 0x6E789E6AA1B965F4


def test_rng_keyed_streams_differ_and_repeat():
    a = [m.Rng(1990, 1, 7, 0).next_u64() for _ in range(3)]
    b = [m.Rng(1990, 1, 7, 0).next_u64() for _ in range(3)]
    c = m.Rng(1990, 1, 7, 1).next_u64()
    assert a == b and a[0] != c
    u = m.Rng(5).uniform()
    assert 0.0 <= u < 1.0


# --- the timetable
def test_bands_cover_every_hour_once():
    for h in range(24):
        assert m.band_for_hour(RATES, h)
    assert m.band_for_hour(RATES, 2)["name"] == "night"
    assert m.band_for_hour(RATES, 8)["name"] == "morning rush"


def test_arrival_rate_matches_band_mean():
    # over many days the mean gap per lane is close to band mean x lanes
    gaps = []
    for day in range(1, 60):
        arr = m.hour_arrivals(7, day, 12, 0, RATES, 30000)  # long horizon: no cut-off bias
        gaps += [b - a for a, b in zip([0] + arr, arr)]
    mean = statistics.mean(gaps) / 1000.0
    want = 75 * 2
    assert abs(mean - want) / want < 0.05, mean


def test_min_gap_in_one_lane():
    for day in range(1, 50):
        arr = m.hour_arrivals(3, day, 8, 1, RATES, 600)
        assert all(b - a >= RATES["min_gap_same_lane_s"] * 1000 - 1 for a, b in zip(arr, arr[1:]))


def test_traits_do_not_depend_on_rates():
    import copy
    t1 = m.car_traits(1990, 1, 9, 0, 2, CD)
    fast = copy.deepcopy(RATES)
    for b in fast["bands"]:
        b["mean_gap_s"] = 7
    a1 = m.hour_arrivals(1990, 1, 9, 0, RATES, 600)
    a2 = m.hour_arrivals(1990, 1, 9, 0, fast, 600)
    assert a1 != a2  # the timetable changed ...
    t2 = m.car_traits(1990, 1, 9, 0, 2, CD)
    assert t1 == t2  # ... but car n of that hour and lane is the same car
    assert CD["desired_speed_mps"]["min"] <= t1["v0"] < CD["desired_speed_mps"]["max"]


# --- the follower
def test_free_road_reaches_desired_speed_and_never_exceeds_it():
    c = m.Car(1, 0, 0.0, 0.0, 11.0, "hatch", 0, 4.0)
    lanes = [{"length_m": 1e9, "speed_caps": []}]
    for i in range(400):
        m.step_lane([c], {}, lanes, CD["follower"], CD["horn"], i * m.DT)
        assert c.v <= 11.0 + 1e-9
    assert c.v > 10.5


def test_never_reverses_and_stops_short_of_person():
    c = m.Car(1, 0, 0.0, 12.5, 12.5, "hatch", 0, 4.0)
    lanes = [{"length_m": 1e9, "speed_caps": []}]
    for i in range(300):
        x0 = c.x
        m.step_lane([c], {0: [60.0]}, lanes, CD["follower"], CD["horn"], i * m.DT)
        assert c.x >= x0 and c.v >= 0
    assert c.v == 0.0
    assert c.x < 60.0 - CD["follower"]["person_standoff_m"]


def test_emergency_stop_once_held_and_horns():
    # a person steps out 10 m ahead of a car at 12.5 m/s: braking is capped
    # at b_max, so it cannot stop in time; it halts at the contact line,
    # logs one emergency stop, shows no positive acceleration while held,
    # and horns 3 s later
    c = m.Car(1, 0, 0.0, 12.5, 12.5, "hatch", 0, 4.0)
    lanes = [{"length_m": 1e9, "speed_caps": []}]
    events = []
    for i in range(80):
        m.step_lane([c], {0: [10.0]}, lanes, CD["follower"], CD["horn"], i * m.DT)
        assert c.x <= 10.0 - CD["follower"]["contact_m"] + 1e-9
        if c.held:
            assert c.a_now <= 0.0 and c.v == 0.0
        events += c.events
        c.events.clear()
    kinds = [e[1] for e in events]
    assert kinds.count("emergency_stop") == 1
    assert kinds.count("horn") == 1


def test_clamp_never_moves_car_backwards():
    c = m.Car(1, 0, 10.0, 5.0, 12.5, "hatch", 0, 4.0)
    lanes = [{"length_m": 1e9, "speed_caps": []}]
    m.step_lane([c], {0: [10.1]}, lanes, CD["follower"], CD["horn"], 0.0)
    assert c.x >= 10.0 and c.v == 0.0


def test_person_beside_body_holds_car():
    c = m.Car(1, 0, 20.0, 8.0, 12.5, "hatch", 0, 4.0)
    lanes = [{"length_m": 1e9, "speed_caps": []}]
    for i in range(20):
        m.step_lane([c], {0: [18.0]}, lanes, CD["follower"], CD["horn"], i * m.DT)
        assert c.x == 20.0 and c.v == 0.0
    assert [e[1] for e in c.events].count("emergency_stop") == 1


def test_horns_at_3_and_10_seconds_after_stopping():
    rows = list(csv.DictReader(open(os.path.join(m.HERE, "goldens", "G3-person-in-road.csv"))))
    stop_t = next(float(r["t_s"]) for r in rows if float(r["v_mps"]) < CD["horn"]["stopped_below_mps"])
    h1 = next(float(r["t_s"]) for r in rows if r["horns"] == "1")
    h2 = next(float(r["t_s"]) for r in rows if r["horns"] == "2")
    assert abs(h1 - stop_t - 3.0) <= 0.2 and abs(h2 - stop_t - 10.0) <= 0.2


def test_following_keeps_gap():
    lead = m.Car(1, 0, 30.0, 8.0, 8.0, "hatch", 0, 4.0)
    fol = m.Car(2, 0, 0.0, 12.5, 12.5, "hatch", 1, 4.0)
    lanes = [{"length_m": 1e9, "speed_caps": []}]
    for i in range(400):
        m.step_lane([lead, fol], {}, lanes, CD["follower"], CD["horn"], i * m.DT)
        assert lead.x - lead.length - fol.x > CD["follower"]["s0"] * 0.9
    assert abs(fol.v - 8.0) < 0.1


def test_brake_lamps_and_wheels():
    c = m.Car(1, 0, 2 * math.pi * CD["wheel_radius_m"], 0.0, 10.0, "hatch", 0, 4.0)
    assert abs(m.wheel_angle_rad(c, CD) - 2 * math.pi) < 1e-9
    assert m.brake_lamp(c, CD["follower"])  # standing
    c.v, c.a_now = 10.0, 0.5
    assert not m.brake_lamp(c, CD["follower"])


# --- the street: soak over many seeds
@pytest.mark.parametrize("seed", range(1, 41))
def test_soak_no_overlap_pool_and_view_caps(seed):
    st = m.default_street(seed)
    t_ms, end = 0, 720_000
    slow_since = {}
    while t_ms < end:
        st.run(t_ms, t_ms + 100, CLOCK)
        t_ms += 100
        assert len(st.cars) <= RATES["pool_size"]
        band = m.band_for_hour(RATES, CLOCK(t_ms - 100)[1])
        for c in st.cars:  # no person on the road here: nobody waits 20 s
            if c.v < 0.3:
                slow_since.setdefault(c.cid, t_ms)
                assert t_ms - slow_since[c.cid] < 20_000, (seed, c.cid)
            else:
                slow_since.pop(c.cid, None)
        assert sum(1 for c in st.cars if st.in_view(c)) <= max(band["max_in_view"], 0) + 0
        for a in st.cars:
            assert a.v >= 0
            for b in st.cars:
                if a is not b and a.lane == b.lane and a.x < b.x:
                    assert b.x - b.length - a.x > 0.5, (seed, t_ms)


def test_same_seed_same_day_log():
    a = m.default_street(1990); a.run(0, 720_000, CLOCK)
    b = m.default_street(1990); b.run(0, 720_000, CLOCK)
    c = m.default_street(1990); c.run(0, 720_000, m.clock_1to120(2, 0))
    assert a.log == b.log and a.log != c.log


def test_second_day_is_not_a_replay():
    st = m.default_street(1990)
    st.run(0, 1_440_000, CLOCK)
    day1 = [e[4:] for e in st.log if e[1] == "spawn" and e[4] == 1]
    day2 = [e[4:] for e in st.log if e[1] == "spawn" and e[4] == 2]
    assert day2 and [d[1:] for d in day1] != [d[1:] for d in day2]


def test_held_clock_keeps_cars_coming():
    # talk holds the game clock at 12:00 for 300 s: the hour's stream runs on
    st = m.default_street(11)
    st.run(0, 1_800_000, lambda t_ms: (1, 12))
    late = [e for e in st.log if e[1] == "spawn" and e[0] > 900]
    assert len(late) >= 2


def test_blocked_rush_golden_exercises_the_pool():
    rows = list(csv.reader(open(os.path.join(m.HERE, "goldens", "G8-blocked-rush.csv"))))[1:]
    kinds = [r[1] for r in rows]
    assert "dropped" in kinds and "horn" in kinds
    hours = {r[5] for r in rows if r[1] == "spawn"}
    assert len(hours) >= 2  # spawns from both sides of the hour change
    live, peak = 0, 0
    for r in rows:
        live += {"spawn": 1, "despawn": -1}.get(r[1], 0)
        peak = max(peak, live)
    assert peak == RATES["pool_size"]


def test_goldens_current():
    assert make_goldens.main(["--check"]) == 0
