"""Traffic stage 1 reference model (lane, 18 Nov 2026).

Background cars at the street's end: a clock-seeded timetable, a pool of
three cars, a follower that keeps its gap with the Intelligent Driver Model
(IDM), gives way to people in the road and sounds its horn.

This file is the behaviour of record. The Unreal follower (a plain actor that
slides along a spline, no physics) must reproduce the golden traces in
goldens/ within the tolerances in TOLERANCES. Only behaviour carries over,
never engine settings.

Everything here is plain arithmetic chosen so that C++ can reproduce it:
- random numbers: SplitMix64 (Vigna, public domain), keyed by
  (seed, game day, game hour, lane index);
- the step: fixed 0.1 s (the game's FixedClock step), ballistic update
  (Treiber and Kesting, Traffic Flow Dynamics, ch. 10 and 11);
- times in integer milliseconds where they are events.

Spec: production/lane/TRAFFIC-STAGE1-REFERENCE-MODEL-2026-11-18.md
"""
from __future__ import annotations

import json
import math
import os
from dataclasses import dataclass, field

HERE = os.path.dirname(os.path.abspath(__file__))
DT = 0.1  # seconds, the game's fixed step
MASK64 = (1 << 64) - 1

TOLERANCES = {
    "position_m": 0.05,
    "speed_mps": 0.02,
    "event_time_s": 0.1,   # horn, stop, despawn
    "arrival_ms": 1,       # timetable
}


# ---------------------------------------------------------------- random
def splitmix64(state: int) -> tuple[int, int]:
    """One SplitMix64 step: returns (new_state, output)."""
    state = (state + 0x9E3779B97F4A7C15) & MASK64
    z = state
    z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & MASK64
    z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & MASK64
    z = z ^ (z >> 31)
    return state, z


class Rng:
    """SplitMix64 stream. key() mixes integers into the starting state."""

    def __init__(self, *keys: int):
        s = 0x4C45444745520000  # "LEDGER\0\0"
        for k in keys:
            s, out = splitmix64((s ^ (k & MASK64)) & MASK64)
            s = out
        self.state = s

    def next_u64(self) -> int:
        self.state, out = splitmix64(self.state)
        return out

    def uniform(self) -> float:
        """A double in [0, 1) from the top 53 bits."""
        return (self.next_u64() >> 11) * (1.0 / (1 << 53))

    def between(self, lo: float, hi: float) -> float:
        return lo + (hi - lo) * self.uniform()


# ---------------------------------------------------------------- data
def load_json(name: str) -> dict:
    with open(os.path.join(HERE, name), encoding="utf-8") as f:
        return json.load(f)


def band_for_hour(rates: dict, hour: int, minute: int = 0) -> dict:
    """The rate band holding game time hour:minute (bands may wrap midnight)."""
    t = hour * 60 + minute
    for band in rates["bands"]:
        a = _hm(band["from"])
        b = _hm(band["to"])
        if a <= b:
            if a <= t < b:
                return band
        else:
            if t >= a or t < b:
                return band
    raise ValueError(f"no band for {hour:02d}:{minute:02d}")


def _hm(s: str) -> int:
    h, m = s.split(":")
    return int(h) * 60 + int(m)


# ---------------------------------------------------------------- timetable
def hour_arrivals(seed: int, day: int, hour: int, lane_index: int,
                  rates: dict, horizon_s: float) -> list[int]:
    """Arrival times (integer ms of unpaused street time after the game hour
    began) for one lane in one game hour, up to horizon_s.

    Poisson arrivals: gaps drawn as -ln(1 - u) * mean, mean being the band's
    mean gap per lane (the band's mean for both directions times two), then
    floored at the band's minimum gap. Rounded to whole milliseconds, so
    C++ and Python agree unless a log differs by more than half a millisecond.
    """
    band = band_for_hour(rates, hour)
    mean_lane = band["mean_gap_s"] * rates["lanes_sharing_rate"]
    rng = Rng(seed, day, hour, lane_index)
    out = []
    t = 0.0
    while True:
        u = rng.uniform()
        gap = -math.log(1.0 - u) * mean_lane
        gap = max(gap, rates["min_gap_same_lane_s"])
        t += gap
        if t >= horizon_s:
            break
        out.append(int(round(t * 1000.0)))
    return out


def car_traits(seed: int, day: int, hour: int, lane_index: int, n: int,
               cars: dict) -> dict:
    """Per-car desired speed and look, drawn from their own stream so that
    changing the rates never changes which car is which."""
    rng = Rng(seed, day, hour, lane_index, 0xCA5, n)
    v0 = rng.between(cars["desired_speed_mps"]["min"], cars["desired_speed_mps"]["max"])
    variant = int(rng.uniform() * len(cars["variants"]))
    colour = int(rng.uniform() * cars["colour_count"])
    return {"v0": v0, "variant": cars["variants"][variant], "colour": colour}


class ArrivalStream:
    """The same draws as hour_arrivals, taken one at a time with no horizon,
    so a game hour held by talk keeps producing cars for as long as it lasts."""

    def __init__(self, seed: int, day: int, hour: int, lane_index: int, rates: dict, start_ms: int):
        band = band_for_hour(rates, hour)
        self.mean_lane = band["mean_gap_s"] * rates["lanes_sharing_rate"]
        self.min_gap = rates["min_gap_same_lane_s"]
        self.rng = Rng(seed, day, hour, lane_index)
        self.key = (day, hour, lane_index)
        self.start_ms = start_ms
        self.t = 0.0
        self.n = -1
        self.due_ms = 0
        self.advance()

    def advance(self) -> None:
        u = self.rng.uniform()
        self.t += max(-math.log(1.0 - u) * self.mean_lane, self.min_gap)
        self.n += 1
        self.due_ms = self.start_ms + int(round(self.t * 1000.0))


# ---------------------------------------------------------------- follower
@dataclass
class Car:
    cid: int
    lane: int
    x: float          # front bumper distance along the lane, m
    v: float          # m/s
    v0: float
    variant: str
    colour: int
    length: float
    a_now: float = 0.0
    stopped_steps: int = 0      # whole 0.1 s steps stopped for a person
    horns: int = 0
    held: bool = False          # halted by an emergency stop
    events: list = field(default_factory=list)


def _pow4(r: float) -> float:
    r2 = r * r
    return r2 * r2


def idm_accel(v: float, v0: float, gap: float | None, dv: float, p: dict) -> float:
    """Plain IDM below the desired speed (Treiber, Hennecke, Helbing 2000;
    Zhou et al. 2025, eq. 1 and 2):
      a_free = a * (1 - (v/v0)^4)
      s* = s0 + max(0, v*T + v*dv / (2*sqrt(a*b))),  dv = v - v_leader
      acc = a_free - a * (s*/s)^2
    Above the desired speed (entering a speed cap) a hybrid: the Improved
    IDM's free term -b * (1 - (v0/v)^(a*delta/b)) with the plain IDM's
    interaction term. It is not the full published Improved IDM; it brakes
    slightly harder than it would, the safe side.
    Braking is capped at b_max. (v/v0)^4 is computed as r2*r2 so C++ gets
    the same bits."""
    a, b, T, s0, d = p["a"], p["b"], p["T"], p["s0"], p["delta"]
    assert d == 4
    if v <= v0:
        acc = a * (1.0 - _pow4(v / v0))
    else:
        acc = -b * (1.0 - (v0 / v) ** (a * d / b))
    if gap is not None:
        s = max(gap, 0.01)
        s_star = s0 + max(0.0, v * T + v * dv / (2.0 * math.sqrt(a * b)))
        z = s_star / s
        acc -= a * z * z
    return max(acc, -p["b_max"])


def obstacles_for(c: Car, cars: list[Car], people: list[float], p: dict):
    """The nearest thing ahead of car c in its lane. Returns
    (gap, leader_speed, kind, beside) where beside is True if a person stands
    between the car's bumpers (the car must not move at all).
    People within detect_m ahead are standing obstacles at
    person - person_standoff_m, or at person - contact_m once the car is
    already past the stand-off point (after an emergency stop)."""
    best = None
    beside = False
    for o in cars:
        if o is c or o.lane != c.lane or o.x <= c.x:
            continue
        g = (o.x - o.length) - c.x
        if best is None or g < best[0]:
            best = (g, o.v, "car")
    for bx in people:
        if c.x - c.length < bx <= c.x:
            beside = True
        elif c.x < bx <= c.x + p["detect_m"]:
            point = bx - p["person_standoff_m"]
            if point <= c.x - 0.5:
                point = bx - p["contact_m"]
            g = point - c.x
            if best is None or g < best[0]:
                best = (g, 0.0, "person")
    if best is None:
        return None, None, None, beside
    return best[0], best[1], best[2], beside


def step_lane(cars_on: list[Car], people_by_lane: dict[int, list[float]],
              lanes: list[dict], p: dict, horn: dict, t: float) -> None:
    """Advance every car one fixed step, in this order:
    1. for every car, in list order, its acceleration from the old state;
    2. for every car, in list order: move (ballistic, never backwards), then
       the contact clamp, then the horn count."""
    plans = []
    for c in cars_on:
        lane = lanes[c.lane]
        v0 = c.v0
        for z in lane.get("speed_caps", []):
            if z["from_m"] - z["lookahead_m"] <= c.x <= z["to_m"]:
                v0 = min(v0, z["cap_mps"])
        people = people_by_lane.get(c.lane, [])
        gap, vl, kind, beside = obstacles_for(c, cars_on, people, p)
        if gap is None:
            acc = idm_accel(c.v, v0, None, 0.0, p)
        else:
            acc = idm_accel(c.v, v0, gap, c.v - vl, p)
        ahead = [bx for bx in people if bx > c.x]
        plans.append((acc, kind, beside, min(ahead) if ahead else None))
    for c, (acc, kind, beside, person_x) in zip(cars_on, plans):
        x_before, v_before = c.x, c.v
        if beside:
            c.v = 0.0
            acc = min(acc, 0.0)
        elif c.v + acc * DT < 0.0:
            c.x += (-0.5 * c.v * c.v / acc) if acc < 0 else 0.0
            c.v = 0.0
        else:
            c.x += c.v * DT + 0.5 * acc * DT * DT
            c.v += acc * DT
        c.a_now = acc
        # a rail car never drives into a person: a person who stepped out
        # inside the stopping distance halts it at the contact line, and one
        # beside its body holds it where it is (unphysical, rare; stage 2's
        # physics replaces it). Never moves the car backwards.
        if person_x is not None and c.x > person_x - p["contact_m"]:
            c.x = max(x_before, person_x - p["contact_m"])
            c.v = 0.0
            c.a_now = min(c.a_now, 0.0)
            if not c.held and v_before > 0.0:
                c.events.append((round(t + DT, 1), "emergency_stop", 0))
            c.held = True
        elif beside:
            if not c.held:
                c.events.append((round(t + DT, 1), "emergency_stop", 0))
            c.held = True
        else:
            c.held = False
        if (kind == "person" or beside) and c.v < horn["stopped_below_mps"]:
            c.stopped_steps += 1
            if c.horns < len(horn["after_s"]) and \
                    c.stopped_steps >= int(round(horn["after_s"][c.horns] / DT)):
                c.horns += 1
                c.events.append((round(t + DT, 1), "horn", c.horns))
        elif not (kind == "person" or beside):
            c.stopped_steps = 0
            c.horns = 0


def brake_lamp(c: Car, p: dict) -> bool:
    return c.a_now < p["brake_lamp_below_mps2"] or c.v < 0.05


def wheel_angle_rad(c: Car, cars: dict) -> float:
    return c.x / cars["wheel_radius_m"]


# ---------------------------------------------------------------- the street
def clock_1to120(start_day: int = 1, start_hour: int = 0):
    """Game clock at 2 game minutes a real second: a game hour is 30,000 ms
    of unpaused street time. Returns a function t_ms -> (day, hour)."""
    def f(t_ms: int) -> tuple[int, int]:
        h = start_hour + t_ms // 30_000
        return start_day + h // 24, h % 24
    return f


class Street:
    """Pool, spawning and despawning out of view, and the tick. One tick:
    (1) if the game hour changed, new arrival streams for each lane, keyed
    by (seed, day, hour, lane), and earlier hours' cars not yet due are
    forgotten; (2) each lane in order moves its due arrivals to the waiting
    list; (3) the waiting list, sorted by (due_ms, lane, day, hour, n), is
    tried in order: spawn, keep waiting, or drop after max_defer_s;
    (4) step_lane; (5) events and despawns in car-list order."""

    def __init__(self, seed: int, lanes_doc: dict, rates: dict, cars_doc: dict):
        self.seed = seed
        self.lanes = lanes_doc["lanes"]
        self.rates, self.cars_doc = rates, cars_doc
        self.p = cars_doc["follower"]
        self.horn = cars_doc["horn"]
        self.cars: list[Car] = []
        self.streams: list[ArrivalStream] = []
        self.waiting: list[tuple] = []  # (due_ms, lane, day, hour, n)
        self.next_id = 1
        self.log: list[tuple] = []
        self.current: tuple[int, int] | None = None

    def in_view(self, c: Car) -> bool:
        lane = self.lanes[c.lane]
        return c.x > lane["view_from_m"] and c.x - c.length < lane["view_to_m"]

    def run(self, t0_ms: int, t1_ms: int, clock, people_at=lambda t_ms: {}) -> None:
        """Simulate from t0 to t1 (integer ms of unpaused street time).
        clock(t_ms) -> (day, hour); people_at(t_ms) -> {lane: [positions]}."""
        t_ms = t0_ms
        while t_ms < t1_ms:
            t = t_ms / 1000.0
            day, hour = clock(t_ms)
            if (day, hour) != self.current:
                self.current = (day, hour)
                self.streams = [ArrivalStream(self.seed, day, hour, li, self.rates, t_ms)
                                for li in range(len(self.lanes))]
            for s in self.streams:
                while s.due_ms <= t_ms:
                    self.waiting.append((s.due_ms, s.key[2], day, hour, s.n))
                    s.advance()
            self.waiting.sort()
            band = band_for_hour(self.rates, hour)
            keep = []
            for item in self.waiting:
                due, li, d, h, n = item
                if t_ms - due > self.rates["max_defer_s"] * 1000:
                    self.log.append((round(t, 1), "dropped", li, d, h, n))
                elif self._can_spawn(li, band):
                    tr = car_traits(self.seed, d, h, li, n, self.cars_doc)
                    c = Car(self.next_id, li, 0.0, min(tr["v0"], self.lanes[li]["entry_speed_mps"]),
                            tr["v0"], tr["variant"], tr["colour"], self.cars_doc["length_m"])
                    self.next_id += 1
                    self.cars.append(c)
                    self.log.append((round(t, 1), "spawn", c.cid, li, d, h, n, round(c.v0, 4)))
                else:
                    keep.append(item)
            self.waiting = keep
            step_lane(self.cars, people_at(t_ms), self.lanes, self.p, self.horn, t)
            for c in list(self.cars):
                for ev in c.events:
                    self.log.append((ev[0], ev[1], c.cid, ev[2]))
                c.events.clear()
                if c.x - c.length > self.lanes[c.lane]["length_m"]:
                    self.cars.remove(c)
                    self.log.append((round(t + DT, 1), "despawn", c.cid))
            t_ms += int(DT * 1000)

    def _can_spawn(self, li: int, band: dict) -> bool:
        """A pool place free; fewer than the band's limit of cars on the road
        and not yet past the view (approaching or in view); the lane start
        clear."""
        if len(self.cars) >= self.rates["pool_size"]:
            return False
        if sum(1 for c in self.cars if c.x - c.length < self.lanes[c.lane]["view_to_m"]) \
                >= band["max_in_view"]:
            return False
        for c in self.cars:
            if c.lane == li and c.x - c.length < self.rates["spawn_clear_m"]:
                return False
        return True


def default_street(seed: int = 1990) -> Street:
    return Street(seed, load_json("lanes.json"), load_json("rates.json"), load_json("cars.json"))
