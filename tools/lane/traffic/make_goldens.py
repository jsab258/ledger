"""Write the golden traces the Unreal follower must reproduce.

python make_goldens.py          writes goldens/*.csv
python make_goldens.py --check  fails if the files differ from a fresh run

Scenarios (each fixed, no randomness except the timetable's seed):
  G1 free road: one car, desired 11.0 m/s, entering at 8.0 m/s, no caps
  G2 following: a leader at 8.0 m/s desired, a follower at 12.5 behind it
  G3 person in the road: one car, a person standing at 70 m from 3.0 to 25.0 s
  G4 the speed cap: one car at 12.5 m/s through the mouth of Quay Street
  G7 emergency stop: a person steps out 8 m ahead of a car at 12.5 m/s
  G8 rush hour blocked: a person in lane 0 for 60 s across an hour change
  G5 the timetable: seed 1990, day 1, both lanes, all 24 game hours
  G6 a full game day on the street: seed 1990, day 1, 720 s, the event log
"""
from __future__ import annotations

import csv
import io
import os
import sys

import traffic_model as m

OUT = os.path.join(m.HERE, "goldens")


def _lanes(caps: bool):
    doc = m.load_json("lanes.json")
    if not caps:
        for ln in doc["lanes"]:
            ln["speed_caps"] = []
    return doc["lanes"]


def trace(cars, lanes, blockers_at, seconds, cars_doc):
    p, horn = cars_doc["follower"], cars_doc["horn"]
    rows = []
    t_ms = 0
    while t_ms <= seconds * 1000:
        t = t_ms / 1000.0
        for c in cars:
            rows.append([f"{t:.1f}", c.cid, f"{c.x:.4f}", f"{c.v:.4f}", f"{c.a_now:.4f}",
                         int(m.brake_lamp(c, p)), c.horns])
        m.step_lane(cars, blockers_at(t), lanes, p, horn, t)
        t_ms += 100
    return [["t_s", "car", "x_m", "v_mps", "a_mps2", "brake_lamp", "horns"]] + rows


def scenarios() -> dict[str, list[list]]:
    cd = m.load_json("cars.json")
    L = cd["length_m"]
    out = {}
    lanes = _lanes(False)
    out["G1-free-road"] = trace([m.Car(1, 0, 0.0, 8.0, 11.0, "hatch", 0, L)], lanes,
                                lambda t: {}, 15, cd)
    out["G2-following"] = trace([m.Car(1, 0, 30.0, 8.0, 8.0, "hatch", 0, L),
                                 m.Car(2, 0, 0.0, 12.5, 12.5, "hatch", 1, L)], lanes,
                                lambda t: {}, 20, cd)
    out["G3-person-in-road"] = trace([m.Car(1, 0, 0.0, 11.0, 11.0, "hatch", 0, L)], lanes,
                                     lambda t: {0: [70.0]} if 3.0 <= t < 25.0 else {}, 35, cd)
    out["G4-speed-cap"] = trace([m.Car(1, 0, 0.0, 12.5, 12.5, "hatch", 0, L)], _lanes(True),
                                lambda t: {}, 14, cd)
    # G7: a person steps out 8 m ahead of a car at 12.5 m/s (inside its
    # stopping distance): the car halts at the contact line
    out["G7-emergency-stop"] = trace([m.Car(1, 0, 0.0, 12.5, 12.5, "hatch", 0, L)], lanes,
                                     lambda t: {0: [33.0]} if t >= 2.0 else {}, 6, cd)
    rates = m.load_json("rates.json")
    rows = [["lane", "hour", "n", "arrival_ms", "v0_mps", "variant", "colour"]]
    for li in range(2):
        for h in range(24):
            # the first 120 s of each hour's stream (an unheld hour lasts 30 s)
            for n, ms in enumerate(m.hour_arrivals(1990, 1, h, li, rates, 120)):
                tr = m.car_traits(1990, 1, h, li, n, cd)
                rows.append([li, h, n, ms, f"{tr['v0']:.6f}", tr["variant"], tr["colour"]])
    out["G5-timetable"] = rows
    st = m.default_street(1990)
    st.run(0, 720_000, m.clock_1to120(1, 0))
    out["G6-day-log"] = [["t_s", "event", "a", "b", "c", "d", "e", "f"]] + [list(e) for e in st.log]
    # G8: a stress run of the pool logic, rates at one car every 10 s (both
    # lanes) in every band; a person stands in lane 0 at 70 m for 60 s across
    # the 08:00 change (street time 15 s to 75 s, starting 07:30): queueing,
    # the full pool, waiting, dropping, horns
    st = m.default_street(1990)
    for band in st.rates["bands"]:
        band["mean_gap_s"] = 10
    st.run(0, 120_000, lambda t_ms: (1, 7 + (15_000 + t_ms) // 30_000),
           lambda t_ms: {0: [70.0]} if 15_000 <= t_ms < 75_000 else {})
    out["G8-blocked-rush"] = [["t_s", "event", "a", "b", "c", "d", "e", "f"]] + [list(e) for e in st.log]
    return out


def render(rows) -> str:
    buf = io.StringIO()
    csv.writer(buf, lineterminator="\n").writerows(rows)
    return buf.getvalue()


def main(argv) -> int:
    os.makedirs(OUT, exist_ok=True)
    bad = 0
    for name, rows in scenarios().items():
        path = os.path.join(OUT, name + ".csv")
        text = render(rows)
        if "--check" in argv:
            with open(path, encoding="utf-8") as f:
                if f.read() != text:
                    print("DIFFERS", name)
                    bad += 1
        else:
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            print("wrote", name, len(rows) - 1, "rows")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
