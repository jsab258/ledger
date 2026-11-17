"""Scripted test drives for LEDGER's driving: the drives, the telemetry format,
the metric functions, the compare step, and a small reference car.

Written by the lane session, 17 November 2026. Python 3, standard library only.

What carries over from the browser prototype (Fable's JavaScript game) to the
Unreal car is behaviour, measured by the same fixed scripted drives, never raw
physics settings: the same settings feel different in a different physics
engine. Each car (browser, Unreal, or the Python reference car below) runs the
drives D1 to D8, exports one telemetry file per run, and this module turns the
telemetry into the shared metric numbers M1 to M10, then compares them against
target ranges or against another car's numbers.

Metric IDs follow the shared list (production/lane, feel-targets sheet):
M1 acceleration, M2 top speed, M3 braking, M4 turning circle, M5 steering
response and self-centring, M6 roll and pitch, M7 front load share, M8 grip and
slide, M9 handbrake, M10 camera. M11 (collisions) and M12 (sound) are not
measured here.

TELEMETRY FORMAT (one file per drive run)
-----------------------------------------
File name: the run name plus ".csv" or ".jsonl", for example D1.csv,
D2-50.csv, D2-wet-30.csv, D4-30.csv, D4-36.csv, D5.jsonl. Run names are listed
in RUN_NAMES below.

CSV: a header row with the column names, then one row per sample. Lines that
start with "#" are comments; "# key=value" lines are read as metadata (for
example "# car=browser-r2", "# max_steer_deg=32").
JSON lines: one JSON object per line, keys as the column names. An optional
first line {"meta": {...}} carries metadata.

Sample at the physics step (120 Hz is the target) or at least 60 Hz. Units are
SI except where named. Coordinates are a flat world seen from above: x to the
right, y forward along the car's start direction, origin where the car starts
(its centre of mass, or the point the car reports as its position).

Required columns:
  t                 time since the run started (s)
  x, y              car position, world (m)
  heading           yaw angle (rad), 0 = facing +y, positive = turned right
                    (clockwise seen from above); unwrapped, never jumps at +-pi
  speed             horizontal speed, always >= 0 (m/s)
  yaw_rate          d(heading)/dt (rad/s), positive = turning right
  lat_g             sideways acceleration of the body, in g, positive = to the
                    car's right (what a level accelerometer in the car reads)
  long_g            forward acceleration of the body, in g, braking negative
  roll_deg          body roll (deg), positive = right side down
  pitch_deg         body pitch (deg), positive = nose up
  front_load_share  share of the car's weight on the front axle (0..1)
  steer             steering actually applied after the car's own smoothing,
                    -1 (full left lock) .. +1 (full right lock)
  throttle, brake   applied pedal, 0..1
  handbrake         0 or 1
  phase             the drive's phase label at that sample (see DRIVES)
Camera columns (required for D8, optional elsewhere):
  cam_dist          horizontal distance from car position to camera (m)
  cam_height        camera height above the road (m)
  cam_fov           horizontal field of view (deg)
  cam_lag           the game's own camera position lag (s), optional
Optional columns:
  wfl_x, wfl_y, wfr_x, wfr_y   outer edge (side away from the car's centre line)
                    of the front left and front right tyre's contact patch,
                    world (m); used for the kerb to kerb turning circle (M4)
  slip_deg          body slip angle (deg); worked out from x, y if missing
Any other columns are allowed and ignored.

Metadata the drives need from the car (CSV "# key=value" or the meta line):
  max_steer_deg     road-wheel angle at full lock (deg)
  wheelbase         (m)
Only for M4 without wheel columns: track (m), tyre_width (m), cg_to_front (m).

HOW A CAR EXPORTS TELEMETRY
---------------------------
Browser: each physics step, push one object with the columns above into an
array; at the end of the run, join them as JSON lines (or CSV) and offer the
file as a download. Unreal: the same columns from the vehicle's tick at a fixed
sub-step, written by a small logger to Saved/Telemetry/<run>.csv. Convert
Unreal centimetres to metres and its left-handed axes to the frame above.

THE DRIVES
----------
Every drive is scripted: inputs come from the script, never a person. The
scripts below are the specification; a JavaScript or Unreal port must use the
same controllers, gains, phases and end conditions. See DRIVES for the list
and DRIVING-DRIVES-README.md for the plain-words version.

Controllers shared by the drives (inputs are recomputed every physics step):
  speed hold   e = v_target - speed; integral I += e*dt, I kept in 0..10;
               throttle = clamp(0.5*e + 0.1*I, 0, 1);
               brake = clamp(0.3*(-e - 0.5), 0, 1) (only when over by > 0.5 m/s)
  pure pursuit look-ahead ld = max(4, 0.6*speed) m to a point on the path;
               alpha = angle from the nose to that point (positive right);
               wheel angle = atan(2*wheelbase*sin(alpha)/ld);
               steer = clamp(wheel angle / max_steer, -1, 1)
  settled      |speed - v_target| < 0.25 m/s for 2 s in a row

THE REFERENCE CAR IS NOT THE GAME'S HANDLING. ReferenceCar is a plain bicycle
model (one front, one rear tyre), linear tyres cut off at a grip limit, weight
transfer front to back, and simple roll and pitch springs. It exists only to
make synthetic telemetry for the tests and as a worked example of a car that
runs the drives and exports the format. Its numbers are tuned near the first
targets so the tests mean something; they say nothing about how LEDGER's car
should be built.

Usage (from the repository root):
  python tools/lane/driving_drives.py reference --out DIR
      runs every drive on the reference car, writes telemetry and result.json
  python tools/lane/driving_drives.py metrics DIR [--out result.json] [--car NAME]
      reads every telemetry file in DIR, writes the metric result
  python tools/lane/driving_drives.py targets [--set ordinary|fast] [--out targets.json]
      writes a named first target set (ordinary is the default car)
  python tools/lane/driving_drives.py compare result.json [--set fast | --targets targets.json]
  python tools/lane/driving_drives.py compare unreal.json --against browser.json
      [--rel 0.05]
"""
import argparse
import csv
import json
import math
import os
import sys

G = 9.81
MPH = 0.44704  # metres per second in one mph

REQUIRED_COLUMNS = [
    "t", "x", "y", "heading", "speed", "yaw_rate", "lat_g", "long_g",
    "roll_deg", "pitch_deg", "front_load_share", "steer", "throttle", "brake",
    "handbrake", "phase",
]
CAMERA_COLUMNS = ["cam_dist", "cam_height", "cam_fov", "cam_lag"]
WHEEL_COLUMNS = ["wfl_x", "wfl_y", "wfr_x", "wfr_y"]
ALL_COLUMNS = REQUIRED_COLUMNS + CAMERA_COLUMNS + WHEEL_COLUMNS

PHYSICS_HZ = 120

# Fixed drive parameters (the specification; ports copy these numbers).
BRAKE_SPEEDS_MPH = (30, 50, 70)
TURN_SPEED_MPH = 5.0
SLALOM_SPACING_M = 18.0
SLALOM_CONES = 8
SLALOM_FIRST_CONE_Y = 250.0
SLALOM_AMPLITUDE_M = 1.2
SLALOM_CLEARANCE_M = 0.9   # car centre at least this far on the right side of each cone
SLALOM_SWEEP_MPH = (30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50)
STEP_SPEED_MPH = 30.0
STEP_WHEEL_DEG = 2.0       # road-wheel angle of the step steer
STEP_HOLD_S = 2.0
CIRCLE_RADIUS_M = 40.0
CIRCLE_CENTRE = (40.0, 0.0)  # car starts at the origin facing +y, turns right
CIRCLE_START_SPEED = 6.7     # m/s (15 mph)
CIRCLE_RAMP = 0.15           # m/s per s, after 10 s
CIRCLE_SLIDE_ERR_M = 2.0     # outward radial error that marks slide onset
HANDBRAKE_SPEED_MPH = 30.0
CAMERA_TOP_MPH = 90.0

RUN_NAMES = (
    ["D1"]
    + ["D2-%d" % s for s in BRAKE_SPEEDS_MPH]
    + ["D2-wet-%d" % s for s in BRAKE_SPEEDS_MPH]
    + ["D3"]
    + ["D4-%d" % s for s in SLALOM_SWEEP_MPH]
    + ["D5", "D6", "D7", "D8"]
)


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------

def clamp(v, lo, hi):
    return lo if v < lo else hi if v > hi else v


def wrap(a):
    """Angle into -pi..pi."""
    return (a + math.pi) % (2 * math.pi) - math.pi


def col(rows, name):
    return [r[name] for r in rows]


def first_crossing(ts, vs, level, start=0):
    """Time at which vs first reaches level (rising), linear interpolation."""
    for i in range(max(start, 1), len(vs)):
        if vs[i - 1] < level <= vs[i]:
            f = (level - vs[i - 1]) / (vs[i] - vs[i - 1])
            return ts[i - 1] + f * (ts[i] - ts[i - 1])
    if vs and start < len(vs) and vs[start] >= level:
        return ts[start]
    return None


def interp(xs, ys, x):
    """Linear interpolation of ys at x; xs increasing."""
    if not xs:
        return None
    if x <= xs[0]:
        return ys[0]
    for i in range(1, len(xs)):
        if xs[i] >= x:
            f = (x - xs[i - 1]) / (xs[i] - xs[i - 1]) if xs[i] != xs[i - 1] else 0.0
            return ys[i - 1] + f * (ys[i] - ys[i - 1])
    return None


def linfit(xs, ys):
    """Least-squares line y = a + b*x; returns (a, b)."""
    n = len(xs)
    if n < 2:
        return None
    mx = sum(xs) / n
    my = sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    if sxx == 0:
        return None
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx
    return my - b * mx, b


def fit_circle(xs, ys):
    """Algebraic least-squares circle fit (Kasa). Returns (cx, cy, r)."""
    # x^2 + y^2 + D x + E y + F = 0
    s = [[0.0] * 3 for _ in range(3)]
    rhs = [0.0] * 3
    for x, y in zip(xs, ys):
        row = (x, y, 1.0)
        z = -(x * x + y * y)
        for i in range(3):
            rhs[i] += row[i] * z
            for j in range(3):
                s[i][j] += row[i] * row[j]
    d, e, f = solve3(s, rhs)
    cx, cy = -d / 2, -e / 2
    return cx, cy, math.sqrt(max(cx * cx + cy * cy - f, 0.0))


def solve3(a, b):
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for c in range(3):
        p = max(range(c, 3), key=lambda r: abs(m[r][c]))
        m[c], m[p] = m[p], m[c]
        if m[c][c] == 0:
            raise ValueError("singular circle fit")
        for r in range(3):
            if r != c:
                k = m[r][c] / m[c][c]
                for j in range(c, 4):
                    m[r][j] -= k * m[c][j]
    return [m[i][3] / m[i][i] for i in range(3)]


def path_length(rows):
    d = 0.0
    for a, b in zip(rows, rows[1:]):
        d += math.hypot(b["x"] - a["x"], b["y"] - a["y"])
    return d


def slip_angles(rows):
    """Body slip angle (rad) per row from position change; positive = moving
    to the right of the nose."""
    out = []
    for i, r in enumerate(rows):
        if "slip_deg" in r and r["slip_deg"] is not None:
            out.append(math.radians(r["slip_deg"]))
            continue
        j0, j1 = max(i - 1, 0), min(i + 1, len(rows) - 1)
        dx = rows[j1]["x"] - rows[j0]["x"]
        dy = rows[j1]["y"] - rows[j0]["y"]
        if math.hypot(dx, dy) < 1e-6:
            out.append(0.0)
        else:
            out.append(wrap(math.atan2(dx, dy) - r["heading"]))
    return out


def phase_rows(rows, phase):
    return [r for r in rows if r.get("phase") == phase]


def phase_start(rows, phase):
    for r in rows:
        if r.get("phase") == phase:
            return r["t"]
    return None


# ---------------------------------------------------------------------------
# Telemetry read and write
# ---------------------------------------------------------------------------

def write_telemetry(path, rows, meta=None):
    meta = meta or {}
    cols = [c for c in ALL_COLUMNS if any(c in r for r in rows[:1])]
    extra = sorted({k for r in rows[:1] for k in r} - set(cols))
    cols += extra
    if path.endswith(".jsonl"):
        with open(path, "w", encoding="utf-8") as f:
            if meta:
                f.write(json.dumps({"meta": meta}) + "\n")
            for r in rows:
                f.write(json.dumps({k: r[k] for k in cols if k in r}) + "\n")
    else:
        with open(path, "w", encoding="utf-8", newline="") as f:
            for k, v in meta.items():
                f.write("# %s=%s\n" % (k, v))
            w = csv.writer(f)
            w.writerow(cols)
            for r in rows:
                w.writerow([fmt(r.get(c, "")) for c in cols])


def fmt(v):
    if isinstance(v, float):
        return "%.9g" % v
    return v


def _num(v):
    if v is None or v == "":
        return None
    if isinstance(v, (int, float)):
        return float(v)
    try:
        return float(v)
    except ValueError:
        return v


def read_telemetry(path):
    """Returns (rows, meta). Numbers become floats; 'phase' stays text."""
    rows, meta = [], {}
    with open(path, encoding="utf-8") as f:
        if path.endswith(".jsonl"):
            for line in f:
                line = line.strip()
                if not line:
                    continue
                obj = json.loads(line)
                if "meta" in obj and len(obj) == 1:
                    meta.update(obj["meta"])
                    continue
                rows.append(obj)
        else:
            lines = []
            for line in f:
                if line.startswith("#"):
                    body = line[1:].strip()
                    if "=" in body:
                        k, v = body.split("=", 1)
                        meta[k.strip()] = v.strip()
                elif line.strip():
                    lines.append(line)
            for r in csv.DictReader(lines):
                rows.append(dict(r))
    for r in rows:
        for k in list(r):
            if k != "phase":
                r[k] = _num(r[k])
    for k in list(meta):
        meta[k] = _num(meta[k])
    missing = [c for c in REQUIRED_COLUMNS if rows and c not in rows[0]]
    if missing:
        raise ValueError("%s lacks columns: %s" % (path, ", ".join(missing)))
    return rows, meta


# ---------------------------------------------------------------------------
# Metric functions: telemetry rows in, numbers out (keys "M<n>.<name>")
# ---------------------------------------------------------------------------

def metric_d1(rows):
    """D1 straight run: M1 0-30 and 0-60 (s), M2 top speed (mph), speed at
    100 m (mph), M6 pitch under full throttle (deg, largest nose-up in the
    first 5 s)."""
    run = phase_rows(rows, "run") or rows
    t0 = run[0]["t"]
    ts = [r["t"] - t0 for r in run]
    vs = col(run, "speed")
    out = {
        "M1.0_30_s": first_crossing(ts, vs, 30 * MPH),
        "M1.0_60_s": first_crossing(ts, vs, 60 * MPH),
        "M2.top_speed_mph": max(vs) / MPH,
    }
    # speed after 100 m of travel
    dist, prev, at100 = 0.0, run[0], None
    for r in run[1:]:
        seg = math.hypot(r["x"] - prev["x"], r["y"] - prev["y"])
        if dist + seg >= 100.0:
            f = (100.0 - dist) / seg if seg else 0.0
            at100 = (prev["speed"] + f * (r["speed"] - prev["speed"])) / MPH
            break
        dist += seg
        prev = r
    out["M2.speed_at_100m_mph"] = at100
    # settled: gained under 0.1 mph in the last 5 s
    last = run[-1]
    back = [r for r in run if r["t"] >= last["t"] - 5.0]
    out["M2.top_speed_settled"] = bool(
        back and last["t"] - back[0]["t"] >= 4.9
        and (last["speed"] - back[0]["speed"]) < 0.1 * MPH)
    early = [abs(r["pitch_deg"]) for r in run if r["t"] - t0 <= 5.0]
    out["M6.pitch_throttle_deg"] = max(early) if early else None
    return out


def metric_d2(rows):
    """D2 braking run (one speed): braking distance from the moment the brake
    phase starts to standstill (m); pitch and front load share fitted against
    long_g over the steady part of the stop and read at 0.8 g."""
    brake = phase_rows(rows, "brake")
    if not brake:
        return {"distance_m": None}
    stop = len(brake)
    for i, r in enumerate(brake):
        if r["speed"] <= 0.05:
            stop = i + 1
            break
    stopped = stop <= len(brake) and brake[stop - 1]["speed"] <= 0.05
    seg = brake[:stop]
    out = {"distance_m": path_length(seg) if stopped else None,
           "start_mph": brake[0]["speed"] / MPH}
    t0 = brake[0]["t"]
    # the last second before the brake (about 0 g) plus the steady stop:
    # a straight line through both, read at 0.8 g
    before = [r for r in rows if r.get("phase") != "brake" and t0 - 1.0 <= r["t"] < t0]
    steady = before + [r for r in seg if r["t"] - t0 >= 0.5 and r["speed"] > 1.0]
    out.update(_fit_at(steady, "long_g", "pitch_deg", -0.8, "pitch_at_0_8g_deg", absval=True))
    share = _fit_at(steady, "long_g", "front_load_share", -0.8, "front_share_at_0_8g", absval=False)
    out["front_share_at_0_8g"] = share["front_share_at_0_8g"]
    out["peak_brake_g"] = max((-r["long_g"] for r in seg), default=None)
    return out


def _fit_at(rows, xcol, ycol, xval, key, absval):
    if len(rows) < 3:
        return {key: None}
    xs, ys = col(rows, xcol), col(rows, ycol)
    if max(xs) - min(xs) < 0.02:
        # one level only: scale by the ratio (spring through zero)
        mx = sum(xs) / len(xs)
        my = sum(ys) / len(ys)
        v = my * (xval / mx) if mx else None
    else:
        a, b = linfit(xs, ys)
        v = a + b * xval
    if v is not None and absval:
        v = abs(v)
    return {key: v}


def metric_d3(rows, meta=None):
    """D3 full-lock loop at 5 mph: kerb to kerb turning circle (m). Uses the
    outer tyre edge columns when present (largest fitted diameter), else the
    car's path plus geometry from metadata."""
    meta = meta or {}
    lock = phase_rows(rows, "lock")
    if not lock:
        return {"M4.turning_circle_m": None}
    h0 = lock[0]["heading"]
    loop = [r for r in lock if abs(r["heading"] - h0) >= math.pi / 2]
    if len(loop) < 10:
        return {"M4.turning_circle_m": None}
    if all(k in loop[0] and loop[0][k] is not None for k in WHEEL_COLUMNS):
        dl = 2 * fit_circle(col(loop, "wfl_x"), col(loop, "wfl_y"))[2]
        dr = 2 * fit_circle(col(loop, "wfr_x"), col(loop, "wfr_y"))[2]
        return {"M4.turning_circle_m": max(dl, dr)}
    cx, cy, r = fit_circle(col(loop, "x"), col(loop, "y"))
    try:
        L = float(meta["wheelbase"])
        a = float(meta["cg_to_front"])
        half = float(meta["track"]) / 2 + float(meta["tyre_width"]) / 2
    except (KeyError, TypeError, ValueError):
        return {"M4.turning_circle_m": None,
                "M4.note": "no wheel columns and no geometry metadata"}
    b = L - a
    r_rear = math.sqrt(max(r * r - b * b, 0.0))  # rear axle centre radius
    return {"M4.turning_circle_m": 2 * math.hypot(r_rear + half, L)}


def slalom_clean(rows):
    """True when the car passed every cone on its own side with clearance."""
    for k in range(SLALOM_CONES):
        yk = SLALOM_FIRST_CONE_Y + SLALOM_SPACING_M * k
        side = 1 if k % 2 == 0 else -1
        ys = col(rows, "y")
        if max(ys) < yk:
            return False
        xk = None
        for a, b in zip(rows, rows[1:]):
            if a["y"] < yk <= b["y"]:
                f = (yk - a["y"]) / (b["y"] - a["y"])
                xk = a["x"] + f * (b["x"] - a["x"])
                break
        if xk is None or xk * side < SLALOM_CLEARANCE_M:
            return False
    return True


def yaw_lag(rows, max_lag_s=1.0):
    """Delay (s) between steer and yaw_rate that best lines them up
    (largest correlation), searched from 0 to max_lag_s."""
    ts = col(rows, "t")
    if len(ts) < 10:
        return None
    dt = (ts[-1] - ts[0]) / (len(ts) - 1)
    s, y = col(rows, "steer"), col(rows, "yaw_rate")
    ms, my = sum(s) / len(s), sum(y) / len(y)
    s = [v - ms for v in s]
    y = [v - my for v in y]
    best, best_k = None, 0
    for k in range(0, int(round(max_lag_s / dt)) + 1):
        n = len(s) - k
        if n < 10:
            break
        num = sum(s[i] * y[i + k] for i in range(n))
        ds = math.sqrt(sum(v * v for v in s[:n]))
        dy = math.sqrt(sum(v * v for v in y[k:k + n]))
        c = num / (ds * dy) if ds and dy else 0.0
        if best is None or c > best:
            best, best_k = c, k
    return best_k * dt


def metric_d4(runs):
    """D4 slalom. runs: {speed_mph: rows}. Highest speed passed cleanly (mph,
    only speeds from a clean 30 mph upward with no failure below count) and
    the yaw lag at 30 mph (s)."""
    out = {"M5.slalom_max_clean_mph": None, "M5.slalom_yaw_lag_s": None}
    best = None
    for spd in sorted(runs):
        if slalom_clean(runs[spd]):
            best = spd
        else:
            break
    out["M5.slalom_max_clean_mph"] = best
    if 30 in runs:
        cones = phase_rows(runs[30], "cones")
        out["M5.slalom_yaw_lag_s"] = yaw_lag(cones) if cones else None
    return out


def metric_d5(rows):
    """D5 step steer at 30 mph: time for yaw rate to reach 63.2% of its
    settled value after the step (s), and self-centring time from release
    until yaw rate stays under 5% of that settled value (s)."""
    t_step = phase_start(rows, "step")
    t_rel = phase_start(rows, "release")
    if t_step is None or t_rel is None:
        return {"M5.yaw_63_s": None, "M5.self_centre_s": None}
    step = phase_rows(rows, "step")
    tail = [r["yaw_rate"] for r in step if r["t"] >= t_rel - 0.5]
    settled = sum(tail) / len(tail)
    sign = 1 if settled >= 0 else -1
    ts = [r["t"] for r in step]
    ys = [sign * r["yaw_rate"] for r in step]
    t63 = first_crossing(ts, ys, (1 - math.exp(-1)) * abs(settled))
    rel = phase_rows(rows, "release")
    t_ctr = None
    thresh = 0.05 * abs(settled)
    for i, r in enumerate(rel):
        if abs(r["yaw_rate"]) < thresh and all(abs(q["yaw_rate"]) < thresh for q in rel[i:]):
            if i > 0:
                a = rel[i - 1]
                ya, yb = abs(a["yaw_rate"]), abs(r["yaw_rate"])
                f = (ya - thresh) / (ya - yb) if ya != yb else 1.0
                t_ctr = a["t"] + f * (r["t"] - a["t"])
            else:
                t_ctr = r["t"]
            break
    return {"M5.yaw_63_s": None if t63 is None else t63 - t_step,
            "M5.self_centre_s": None if t_ctr is None else t_ctr - t_rel}


def metric_d6(rows):
    """D6 rising-speed circle, slide, counter-steer recovery: M8 highest
    steady lateral g (0.5 s average, while within the slide error of the
    circle), slide onset speed (mph) and lateral g, recovery time (s); M6 roll
    at 0.5 g, fitted from the steady part."""
    circ = phase_rows(rows, "circle")
    cx, cy = CIRCLE_CENTRE
    steady = [r for r in circ
              if abs(math.hypot(r["x"] - cx, r["y"] - cy) - CIRCLE_RADIUS_M) < CIRCLE_SLIDE_ERR_M]
    out = {"M8.max_steady_lat_g": None, "M8.slide_onset_mph": None,
           "M8.slide_onset_lat_g": None, "M8.recovery_s": None,
           "M6.roll_deg_at_0_5g": None}
    if steady:
        best = 0.0
        ts = col(steady, "t")
        lg = [abs(v) for v in col(steady, "lat_g")]
        j = 0
        acc = 0.0
        for i in range(len(ts)):
            acc += lg[i]
            while ts[i] - ts[j] > 0.5:
                acc -= lg[j]
                j += 1
            if ts[i] - ts[0] >= 0.5:
                best = max(best, acc / (i - j + 1))
        out["M8.max_steady_lat_g"] = best
        quasi = [r for r in steady if abs(r["lat_g"]) > 0.1]
        if len(quasi) > 5:
            xs = [abs(r["lat_g"]) for r in quasi]
            ys = [abs(r["roll_deg"]) for r in quasi]
            fit = linfit(xs, ys)
            if fit:
                out["M6.roll_deg_at_0_5g"] = fit[0] + fit[1] * 0.5
    rec = phase_rows(rows, "recover")
    if rec:
        out["M8.slide_onset_mph"] = rec[0]["speed"] / MPH
        out["M8.slide_onset_lat_g"] = abs(rec[0]["lat_g"])
        beta = slip_angles(rows)
        idx0 = rows.index(rec[0])
        t_on = rec[0]["t"]
        ok_since = None
        for i in range(idx0, len(rows)):
            r = rows[i]
            good = abs(beta[i]) < math.radians(2.0) and abs(r["yaw_rate"]) < 0.1
            if good:
                ok_since = r["t"] if ok_since is None else ok_since
                if r["t"] - ok_since >= 0.5:
                    out["M8.recovery_s"] = ok_since - t_on
                    break
            else:
                ok_since = None
    return out


def metric_d7(rows):
    """D7 handbrake turn from 30 mph: yaw turned when the turn has settled
    (deg) and the time the turn took to settle (s): from the handbrake pull
    until the yaw rate stays under 0.1 rad/s to the end of the run (the turn
    and stop phases together)."""
    t_pull = phase_start(rows, "turn")
    if t_pull is None:
        return {"M9.handbrake_yaw_deg": None, "M9.handbrake_settle_s": None}
    turn = [r for r in rows if r["t"] >= t_pull]
    h0, t0 = turn[0]["heading"], turn[0]["t"]
    settle = None
    for i in range(len(turn) - 1, -1, -1):
        if abs(turn[i]["yaw_rate"]) >= 0.1:
            settle = turn[i + 1] if i + 1 < len(turn) else None
            break
    else:
        settle = turn[0]
    if settle is None:
        return {"M9.handbrake_yaw_deg": math.degrees(abs(turn[-1]["heading"] - h0)),
                "M9.handbrake_settle_s": None}
    return {"M9.handbrake_yaw_deg": math.degrees(abs(settle["heading"] - h0)),
            "M9.handbrake_settle_s": settle["t"] - t0}


def metric_d8(rows):
    """D8 camera run 0 to 90 mph: distance and height at rest (m), position
    lag (s), FOV at 0, 30, 60, 90 mph (deg) and the widening 0 to 90.
    Lag = median of (distance at speed - distance at rest) / speed above
    10 m/s: a camera that trails like a first-order lag of tau seconds keeps
    tau*speed extra distance."""
    if not rows or rows[0].get("cam_dist") is None:
        return {}
    rest = (phase_rows(rows, "rest") or [r for r in rows if r["speed"] < 0.1]
            or rows[:1])
    d0 = sum(r["cam_dist"] for r in rest) / len(rest)
    h0 = sum(r["cam_height"] for r in rest) / len(rest)
    lags = sorted((r["cam_dist"] - d0) / r["speed"] for r in rows if r["speed"] > 10.0)
    out = {"M10.cam_dist_m": d0, "M10.cam_height_m": h0,
           "M10.cam_lag_s": lags[len(lags) // 2] if lags else None}
    rep = [r["cam_lag"] for r in rows if r.get("cam_lag") is not None]
    if rep:
        out["M10.cam_lag_reported_s"] = sorted(rep)[len(rep) // 2]
    # FOV against speed: rows are in rising speed order during the run
    run = phase_rows(rows, "run") or rows
    pairs, top = [], -1.0
    for r in run:
        if r["speed"] > top:
            pairs.append((r["speed"], r["cam_fov"]))
            top = r["speed"]
    sp = [p[0] for p in pairs]
    fv = [p[1] for p in pairs]
    for mph in (0, 30, 60, 90):
        v = mph * MPH
        out["M10.fov_%d_deg" % mph] = (sum(r["cam_fov"] for r in rest) / len(rest)
                                       if mph == 0 else
                                       (interp(sp, fv, v) if sp and sp[-1] >= v else None))
    if out["M10.fov_90_deg"] is not None:
        out["M10.fov_widen_deg"] = out["M10.fov_90_deg"] - out["M10.fov_0_deg"]
    else:
        out["M10.fov_widen_deg"] = None
    return out


def compute_metrics(runs, metas=None, car="unnamed"):
    """runs: {run name: rows}. Returns the result dict with flat metric keys."""
    metas = metas or {}
    m = {}
    per_run = {}
    if "D1" in runs:
        m.update(metric_d1(runs["D1"]))
    brake_pitch, brake_share = [], []
    for wet in ("", "wet-"):
        for s in BRAKE_SPEEDS_MPH:
            name = "D2-%s%d" % (wet, s)
            if name in runs:
                r = metric_d2(runs[name])
                per_run[name] = r
                key = "M3.%sbrake_%d_m" % ("wet_" if wet else "", s)
                m[key] = r["distance_m"]
                if not wet:
                    brake_pitch.append(r.get("pitch_at_0_8g_deg"))
                    brake_share.append(r.get("front_share_at_0_8g"))
    for sp in BRAKE_SPEEDS_MPH:
        d, w = m.get("M3.brake_%d_m" % sp), m.get("M3.wet_brake_%d_m" % sp)
        if d and w:
            m["M3.wet_ratio_%d" % sp] = w / d
    bp = [v for v in brake_pitch if v is not None]
    bs = [v for v in brake_share if v is not None]
    if bp:
        m["M6.pitch_brake_deg_at_0_8g"] = sum(bp) / len(bp)
    if bs:
        m["M7.front_load_brake_pct_at_0_8g"] = 100.0 * sum(bs) / len(bs)
    if "D3" in runs:
        m.update(metric_d3(runs["D3"], metas.get("D3")))
    sl = {int(n.split("-")[1]): rows for n, rows in runs.items()
          if n.startswith("D4-")}
    if sl:
        m.update(metric_d4(sl))
    if "D5" in runs:
        m.update(metric_d5(runs["D5"]))
    if "D6" in runs:
        m.update(metric_d6(runs["D6"]))
    if "D7" in runs:
        m.update(metric_d7(runs["D7"]))
    if "D8" in runs:
        m.update(metric_d8(runs["D8"]))
    return {"car": car, "format": "ledger-driving-result-1",
            "runs": sorted(runs), "metrics": m, "per_run": per_run}


def metrics_from_dir(folder, car=None):
    runs, metas = {}, {}
    for fn in sorted(os.listdir(folder)):
        base, ext = os.path.splitext(fn)
        if ext in (".csv", ".jsonl") and base in RUN_NAMES:
            rows, meta = read_telemetry(os.path.join(folder, fn))
            runs[base], metas[base] = rows, meta
    car = car or next((m.get("car") for m in metas.values() if m.get("car")), "unnamed")
    return compute_metrics(runs, metas, car=car)


# ---------------------------------------------------------------------------
# Targets and compare
# ---------------------------------------------------------------------------

# FIRST TARGETS from the researched feel-targets sheet (17 Nov 2026): the
# "game band", the real range widened by the sheet's allowed game departures.
# "first" = a number to tune to now; "placeholder" = no number yet, reported
# but never failed. Two sets, chosen by name: "ordinary" (the default car, an
# ordinary 1990 small hatch) and "fast" (a 1990 fast hatch).
TARGET_SETS = {
    "ordinary": {
        "M1.0_30_s": (3.6, 6.0),
        "M1.0_60_s": (13.0, 17.0),
        "M2.top_speed_mph": (90.0, 100.0),
        "M2.speed_at_100m_mph": (40.0, 46.0),
        "M3.brake_30_m": (9.5, 14.0),
        "M3.brake_50_m": (25.5, 38.0),
        "M3.brake_70_m": (51.0, 75.0),
        "M3.wet_ratio_30": (1.5, 2.0),
        "M3.wet_ratio_50": (1.5, 2.0),
        "M3.wet_ratio_70": (1.5, 2.0),
        "M4.turning_circle_m": (9.0, 10.5),
        "M5.yaw_63_s": (0.20, 0.35),
        "M5.self_centre_s": (0.6, 1.2),
        "M6.roll_deg_at_0_5g": (3.0, 6.0),
        "M6.pitch_brake_deg_at_0_8g": (2.0, 5.0),
        "M6.pitch_throttle_deg": (0.5, 2.25),
        "M7.front_load_brake_pct_at_0_8g": (75.0, 82.0),
        "M8.max_steady_lat_g": (0.70, 0.85),
        "M8.recovery_s": (0.5, 1.0),
        "M9.handbrake_yaw_deg": (90.0, 150.0),
        "M9.handbrake_settle_s": (1.2, 2.0),
        "M10.cam_dist_m": (5.0, 7.0),
        "M10.cam_height_m": (1.6, 2.2),
        "M10.cam_lag_s": (0.1, 0.3),
        "M10.fov_0_deg": (60.0, 65.0),
        "M10.fov_30_deg": (62.0, 68.0),
        "M10.fov_60_deg": (66.0, 74.0),
        "M10.fov_90_deg": (70.0, 80.0),
    },
}
# The fast hatch: the ordinary set with these replaced; town-feel numbers the
# sheet gives only for the ordinary car become placeholders.
TARGET_SETS["fast"] = dict(TARGET_SETS["ordinary"], **{
    "M1.0_60_s": (8.0, 9.0),
    "M2.top_speed_mph": (118.0, 122.0),
    "M3.brake_30_m": (8.5, 12.0),
    "M3.brake_50_m": (24.0, 33.0),
    "M3.brake_70_m": (47.0, 65.0),
    "M6.roll_deg_at_0_5g": (2.0, 4.5),
    "M8.max_steady_lat_g": (0.82, 0.90),
    "M1.0_30_s": None,
    "M2.speed_at_100m_mph": None,
})
PLACEHOLDERS = [
    "M3.wet_brake_30_m", "M3.wet_brake_50_m", "M3.wet_brake_70_m",
    "M5.slalom_max_clean_mph", "M5.slalom_yaw_lag_s",
    "M8.slide_onset_mph", "M10.fov_widen_deg",
]


def default_targets(name="ordinary"):
    if name not in TARGET_SETS:
        raise ValueError("unknown target set %r (have: %s)" % (name, ", ".join(TARGET_SETS)))
    t = {"set": name,
         "note": "FIRST TARGETS (%s set) from the feel-targets sheet's game band. "
                 "Braking is braking distance only, no thinking distance; wet "
                 "ratio is wet distance over dry distance." % name,
         "targets": {}}
    for k, rng in TARGET_SETS[name].items():
        if rng is None:
            t["targets"][k] = {"min": None, "max": None, "status": "placeholder"}
        else:
            t["targets"][k] = {"min": rng[0], "max": rng[1], "status": "first"}
    for k in PLACEHOLDERS:
        t["targets"][k] = {"min": None, "max": None, "status": "placeholder"}
    return t


# Absolute tolerance by unit, used beside the relative one in car-to-car checks.
ABS_TOL = {"_s": 0.05, "_m": 0.3, "_mph": 1.0, "_deg": 0.3, "_pct": 1.0, "_g": 0.02}


def abs_tol_for(key):
    """The unit is the last unit word in the key: "M6.roll_deg_at_0_5g" is in
    degrees, "M8.max_steady_lat_g" in g."""
    words = key.split(".", 1)[-1].split("_")
    for w in reversed(words):
        if "_" + w in ABS_TOL:
            return ABS_TOL["_" + w]
    return 0.0


def compare_targets(result, targets):
    """Each metric against its range. Returns {"pass": bool, "rows": [...]}.
    Placeholders and metrics with no target are reported, never failed; a
    first target with a missing number fails."""
    rows, ok = [], True
    m = result["metrics"]
    for key, tg in sorted(targets["targets"].items()):
        v = m.get(key)
        lo, hi = tg.get("min"), tg.get("max")
        if tg.get("status") == "placeholder" or lo is None or hi is None:
            status = "no target"
        elif not isinstance(v, (int, float)) or isinstance(v, bool):
            status = "missing"
            ok = False
        elif lo <= v <= hi:
            status = "pass"
        else:
            status = "fail"
            ok = False
        rows.append({"metric": key, "value": v, "min": lo, "max": hi, "status": status})
    return {"pass": ok, "rows": rows}


def compare_results(result, reference, rel=0.05, abs_tol=None, keys=None):
    """result (for example Unreal) against reference (the browser). A metric
    passes when |a - b| <= max(rel * |b|, absolute tolerance for its unit).
    Missing on one side fails; missing on both is skipped."""
    abs_tol = abs_tol or {}
    a, b = result["metrics"], reference["metrics"]
    keys = keys or sorted(set(a) | set(b))
    rows, ok = [], True
    for k in keys:
        va, vb = a.get(k), b.get(k)
        if isinstance(va, bool) or isinstance(vb, bool) or isinstance(va, str) or isinstance(vb, str):
            continue
        if va is None and vb is None:
            rows.append({"metric": k, "status": "skip"})
            continue
        if va is None or vb is None:
            rows.append({"metric": k, "value": va, "reference": vb, "status": "missing"})
            ok = False
            continue
        tol = max(rel * abs(vb), abs_tol.get(k, abs_tol_for(k)))
        good = abs(va - vb) <= tol + 1e-12
        ok = ok and good
        rows.append({"metric": k, "value": va, "reference": vb, "tolerance": tol,
                     "status": "pass" if good else "fail"})
    return {"pass": ok, "rows": rows}


# ---------------------------------------------------------------------------
# The drives (scripts). Each drive gets the car's latest state each physics
# step and returns the inputs, its phase label, and whether it is done.
# ---------------------------------------------------------------------------

class SpeedHold:
    def __init__(self):
        self.i = 0.0

    def __call__(self, v_target, speed, dt):
        e = v_target - speed
        self.i = clamp(self.i + e * dt, 0.0, 10.0)
        throttle = clamp(0.5 * e + 0.1 * self.i, 0.0, 1.0)
        brake = clamp(0.3 * (-e - 0.5), 0.0, 1.0)
        return throttle, brake


def pursuit_steer(s, target, car):
    """Steer input toward a world point (pure pursuit)."""
    dx, dy = target[0] - s["x"], target[1] - s["y"]
    ld = max(math.hypot(dx, dy), 1e-3)
    alpha = wrap(math.atan2(dx, dy) - s["heading"])
    wheel = math.atan(2 * car["wheelbase"] * math.sin(alpha) / ld)
    return clamp(wheel / math.radians(car["max_steer_deg"]), -1.0, 1.0)


def lookahead(speed):
    return max(4.0, 0.6 * speed)


class Drive:
    """Base: subclasses set name and implement step(t, s, dt) -> dict of
    inputs plus 'phase' and 'done'."""
    name = "D?"
    max_time = 60.0

    def __init__(self, car_info):
        self.car = car_info
        self.hold = SpeedHold()
        self.settled_since = None

    def settled(self, t, speed, v_target):
        if abs(speed - v_target) < 0.25:
            if self.settled_since is None:
                self.settled_since = t
            return t - self.settled_since >= 2.0
        self.settled_since = None
        return False


def _inp(phase, steer=0.0, throttle=0.0, brake=0.0, handbrake=0, done=False):
    return {"phase": phase, "steer": steer, "throttle": throttle, "brake": brake,
            "handbrake": handbrake, "done": done}


class D1Straight(Drive):
    """D1: full throttle from standstill on flat road, no steering. Ends when
    speed gains under 0.1 mph in 5 s (top speed settled) or at 150 s. (A
    hatch takes over a minute to settle near its top speed, so the 30 s in
    the first brief is too short for M2; M1 is read in the first seconds.)"""
    name = "D1"
    max_time = 150.0

    def __init__(self, car_info):
        super().__init__(car_info)
        self.hist = []

    def step(self, t, s, dt):
        self.hist.append((t, s["speed"]))
        while self.hist and self.hist[0][0] < t - 5.0:
            self.hist.pop(0)
        done = (t > 10.0 and t - self.hist[0][0] >= 4.9
                and s["speed"] - self.hist[0][1] < 0.1 * MPH)
        return _inp("run", throttle=1.0, done=done or t >= self.max_time)


class D2Brake(Drive):
    """D2: speed hold to the set speed, settled for 2 s, then full brake, no
    steering, until standstill (speed 0.01 m/s or less). Phases: approach,
    brake. D2-wet-N is the same drive with the car's wet-grip setting applied."""
    max_time = 120.0

    def __init__(self, car_info, mph):
        super().__init__(car_info)
        self.v = mph * MPH
        self.braking = False
        self.name = "D2-%d" % mph

    def step(self, t, s, dt):
        if not self.braking and self.settled(t, s["speed"], self.v):
            self.braking = True
        if self.braking:
            return _inp("brake", brake=1.0, done=s["speed"] <= 0.01 or t >= self.max_time)
        th, br = self.hold(self.v, s["speed"], dt)
        return _inp("approach", throttle=th, brake=br, done=t >= self.max_time)


class D3Circle(Drive):
    """D3: speed hold at 5 mph straight until settled, then full right lock
    (+1) with speed hold, until the heading has turned 1.25 loops (the first
    quarter is the run-in, the metric uses the last full loop). Phases:
    approach, lock."""
    name = "D3"
    max_time = 90.0

    def __init__(self, car_info):
        super().__init__(car_info)
        self.v = TURN_SPEED_MPH * MPH
        self.h0 = None

    def step(self, t, s, dt):
        th, br = self.hold(self.v, s["speed"], dt)
        if self.h0 is None and self.settled(t, s["speed"], self.v):
            self.h0 = s["heading"]
        if self.h0 is None:
            return _inp("approach", throttle=th, brake=br, done=t >= self.max_time)
        done = abs(s["heading"] - self.h0) >= 2.5 * math.pi or t >= self.max_time
        return _inp("lock", steer=1.0, throttle=th, brake=br, done=done)


def slalom_path_x(y):
    y0 = SLALOM_FIRST_CONE_Y
    y_last = y0 + SLALOM_SPACING_M * (SLALOM_CONES - 1)
    if y < y0 - SLALOM_SPACING_M / 2 or y > y_last + SLALOM_SPACING_M / 2:
        return 0.0
    return SLALOM_AMPLITUDE_M * math.cos(math.pi * (y - y0) / SLALOM_SPACING_M)


class D4Slalom(Drive):
    """D4: speed hold at the set speed, pure pursuit along the slalom path.
    Cones on the line x = 0 at y = 250 + 18k (k = 0..7); the path is
    x = 1.2 cos(pi (y - 250) / 18) between half a gap before the first cone
    and half a gap after the last, x = 0 elsewhere, so cone k is passed on
    the right (+x) for even k. Clean = the car's centre passes each cone at
    least 0.9 m on its side (half a car's width plus 0.1 m). Ends 40 m after the last cone. Phases: approach,
    cones (from half a gap before the first cone to half after the last),
    exit. Run at 30 mph, then 32, 34 ... 50 until the first unclean run."""
    max_time = 120.0

    def __init__(self, car_info, mph):
        super().__init__(car_info)
        self.v = mph * MPH
        self.name = "D4-%d" % mph

    def step(self, t, s, dt):
        th, br = self.hold(self.v, s["speed"], dt)
        ly = s["y"] + lookahead(s["speed"])
        steer = pursuit_steer(s, (slalom_path_x(ly), ly), self.car)
        y0 = SLALOM_FIRST_CONE_Y - SLALOM_SPACING_M / 2
        y1 = SLALOM_FIRST_CONE_Y + SLALOM_SPACING_M * (SLALOM_CONES - 1) + SLALOM_SPACING_M / 2
        phase = "approach" if s["y"] < y0 else "cones" if s["y"] <= y1 else "exit"
        done = s["y"] > y1 + 40.0 or t >= self.max_time
        return _inp(phase, steer=steer, throttle=th, brake=br, done=done)


class D5StepSteer(Drive):
    """D5: speed hold at 30 mph straight until settled, then step the steer
    input to the value giving a 2 degree road-wheel angle (right), speed hold
    on; after 2 s release the steer to 0, speed hold on, for 4 s more.
    Phases: approach, step, release."""
    name = "D5"
    max_time = 90.0

    def __init__(self, car_info):
        super().__init__(car_info)
        self.v = STEP_SPEED_MPH * MPH
        self.t_step = None

    def step(self, t, s, dt):
        th, br = self.hold(self.v, s["speed"], dt)
        if self.t_step is None and self.settled(t, s["speed"], self.v):
            self.t_step = t
        if self.t_step is None:
            return _inp("approach", throttle=th, brake=br, done=t >= self.max_time)
        if t - self.t_step < STEP_HOLD_S:
            st = STEP_WHEEL_DEG / self.car["max_steer_deg"]
            return _inp("step", steer=st, throttle=th, brake=br)
        return _inp("release", throttle=th, brake=br,
                    done=t - self.t_step >= STEP_HOLD_S + 4.0 or t >= self.max_time)


class D6SteadyCircle(Drive):
    """D6: from standstill, pure pursuit on a 40 m radius circle (centre at
    x = 40, y = 0, turning right), look-ahead point on the circle ld metres of
    arc ahead. Target speed 6.7 m/s (15 mph) for the first 10 s, then rising
    0.15 m/s each second. Slide onset: the car is more than 2 m outside the
    circle (after the first 10 s). Then recovery: throttle 0, brake 0, the
    front wheels steered toward where the car is moving and yaw damped:
    wheel angle = slip angle - 0.2 * yaw_rate. Ends 6 s after onset or at
    150 s. Phases: circle, recover. Also gives M6 roll at 0.5 g."""
    name = "D6"
    max_time = 150.0

    def __init__(self, car_info):
        super().__init__(car_info)
        self.onset = None
        self.prev = None

    def step(self, t, s, dt):
        cx, cy = CIRCLE_CENTRE
        if self.onset is None:
            err = math.hypot(s["x"] - cx, s["y"] - cy) - CIRCLE_RADIUS_M
            if t > 10.0 and err > CIRCLE_SLIDE_ERR_M:
                self.onset = t
        if self.onset is None:
            v_t = CIRCLE_START_SPEED + CIRCLE_RAMP * max(0.0, t - 10.0)
            th, br = self.hold(v_t, s["speed"], dt)
            theta = math.atan2(s["y"] - cy, cx - s["x"])  # clockwise from the start
            theta += lookahead(s["speed"]) / CIRCLE_RADIUS_M
            target = (cx - CIRCLE_RADIUS_M * math.cos(theta), cy + CIRCLE_RADIUS_M * math.sin(theta))
            self.prev = (s["x"], s["y"])
            return _inp("circle", steer=pursuit_steer(s, target, self.car), throttle=th,
                        brake=br, done=t >= self.max_time)
        beta = 0.0
        if self.prev is not None:
            dx, dy = s["x"] - self.prev[0], s["y"] - self.prev[1]
            if math.hypot(dx, dy) > 1e-6:
                beta = wrap(math.atan2(dx, dy) - s["heading"])
        self.prev = (s["x"], s["y"])
        wheel = beta - 0.2 * s["yaw_rate"]
        steer = clamp(wheel / math.radians(self.car["max_steer_deg"]), -1.0, 1.0)
        return _inp("recover", steer=steer,
                    done=t - self.onset >= 6.0 or t >= self.max_time)


class D7Handbrake(Drive):
    """D7: speed hold at 30 mph straight until settled, then at once: steer
    full right lock (+1), handbrake on, throttle 0, brake 0, for 0.6 s
    (phase turn). Then handbrake off, steer 0, full brake (phase stop) until
    the car is below 0.5 m/s and turning slower than 0.1 rad/s, or 8 s after
    the pull. Phases: approach, turn, stop. Gives the yaw turned and the time
    the turn took to settle (yaw rate under 0.1 rad/s from then on)."""
    name = "D7"
    max_time = 90.0
    PULL_S = 0.6

    def __init__(self, car_info):
        super().__init__(car_info)
        self.v = HANDBRAKE_SPEED_MPH * MPH
        self.t_turn = None

    def step(self, t, s, dt):
        if self.t_turn is None and self.settled(t, s["speed"], self.v):
            self.t_turn = t
        if self.t_turn is None:
            th, br = self.hold(self.v, s["speed"], dt)
            return _inp("approach", throttle=th, brake=br, done=t >= self.max_time)
        if t - self.t_turn < self.PULL_S:
            return _inp("turn", steer=1.0, handbrake=1)
        done = ((s["speed"] < 0.5 and abs(s["yaw_rate"]) < 0.1)
                or t - self.t_turn >= 8.0 or t >= self.max_time)
        return _inp("stop", brake=1.0, done=done)


class D8Camera(Drive):
    """D8: 1 s at rest, then full throttle, no steering, until 90 mph (or
    180 s), logging the camera columns throughout. Phases: rest, run."""
    name = "D8"
    max_time = 180.0

    def step(self, t, s, dt):
        if t < 1.0:
            return _inp("rest")
        return _inp("run", throttle=1.0,
                    done=s["speed"] >= CAMERA_TOP_MPH * MPH or t >= self.max_time)


DRIVES = {
    "D1": "Straight-line run: full throttle from standstill until top speed settles (M1, M2, M6 throttle pitch)",
    "D2": "Braking from 30, 50, 70 mph: hold speed, full brake, no steering; dry and wet (M3, M6 brake pitch, M7)",
    "D3": "Turning circle: full lock at 5 mph for a loop and a quarter (M4)",
    "D4": "Slalom: cones every 18 m, 30 mph then rising in 2 mph steps (M5 slalom extras)",
    "D5": "Step steer at 30 mph, 2 degree road-wheel angle, release after 2 s (M5)",
    "D6": "Steady 40 m circle at rising speed until slide, then counter-steer recovery (M8, M6 roll)",
    "D7": "Handbrake turn from 30 mph: yaw turned and time to settle (M9)",
    "D8": "Camera run 0 to 90 mph (M10)",
    "D9": "Braking pitch and roll: no run of its own, read from D2 and D6 (M6, M7)",
}


def make_drive(run_name, car_info):
    if run_name == "D1":
        return D1Straight(car_info)
    if run_name.startswith("D2-"):
        return D2Brake(car_info, int(run_name.split("-")[-1]))
    if run_name == "D3":
        return D3Circle(car_info)
    if run_name.startswith("D4-"):
        return D4Slalom(car_info, int(run_name.split("-")[1]))
    if run_name == "D5":
        return D5StepSteer(car_info)
    if run_name == "D6":
        return D6SteadyCircle(car_info)
    if run_name == "D7":
        return D7Handbrake(car_info)
    if run_name == "D8":
        return D8Camera(car_info)
    raise ValueError("unknown run " + run_name)


# ---------------------------------------------------------------------------
# Reference car. NOT THE GAME'S HANDLING: a worked example and a source of
# synthetic telemetry for the tests only.
# ---------------------------------------------------------------------------

class ReferenceCar:
    """Bicycle model, front-wheel drive, est. numbers near a 1990 small hatch.
    Body axes: u forward, v to the right, r yaw rate positive turning right."""

    def __init__(self, wet=False, **over):
        self.m = 950.0
        self.iz = 1800.0
        self.L = 2.4
        self.a = 0.96            # centre of mass to front axle (60% static front)
        self.b = self.L - self.a
        self.h = 0.52            # centre of mass height
        self.track = 1.40
        self.tyre_width = 0.165
        self.max_steer_deg = 33.0
        self.cf = 90000.0        # front cornering stiffness, N/rad (axle)
        self.cr = 65000.0
        self.mu = 0.82 * (0.5 if wet else 1.0)
        self.mu_lock = 0.70 * (0.5 if wet else 1.0)  # locked rear wheels
        self.power = 34000.0     # W at the wheels
        self.drive_max = 2600.0  # N, traction and first gear
        self.brake_max = 0.68 * self.m * G
        self.brake_front = 0.70
        self.cda = 0.68
        self.rr = 0.013
        self.steer_tau_in = 0.14   # applied steer follows the input, turning in
        self.steer_tau_out = 0.25  # and returning toward centre
        self.roll_k = 9.0          # deg per g
        self.pitch_k = 3.0         # deg per g
        self.spin_damp = 3000.0   # N m s/rad, see step()
        self.cam_dist = 6.0
        self.cam_height = 1.9
        self.cam_tau = 0.2
        self.fov0 = 62.0
        self.fov_add = 12.0
        for k, v in over.items():
            setattr(self, k, v)
        self.reset()

    def info(self):
        return {"max_steer_deg": self.max_steer_deg, "wheelbase": self.L,
                "track": self.track, "tyre_width": self.tyre_width,
                "cg_to_front": self.a, "car": "reference (not the game)"}

    def reset(self):
        self.x = self.y = self.hd = 0.0
        self.u = self.v = self.r = 0.0
        self.ax = self.ay = 0.0
        self.steer = 0.0
        self.roll = self.roll_v = 0.0
        self.pitch = self.pitch_v = 0.0
        self.cam_extra = 0.0
        self.inp = _inp("")

    def state(self, t):
        fwd = (math.sin(self.hd), math.cos(self.hd))
        right = (math.cos(self.hd), -math.sin(self.hd))
        fz_f = self.m * G * self.b / self.L - self.m * self.ax * self.h / self.L
        off = self.track / 2 + self.tyre_width / 2
        fa = (self.x + self.a * fwd[0], self.y + self.a * fwd[1])
        speed = math.hypot(self.u, self.v)
        return {
            "t": t, "x": self.x, "y": self.y, "heading": self.hd, "speed": speed,
            "yaw_rate": self.r, "lat_g": self.ay / G, "long_g": self.ax / G,
            "roll_deg": self.roll, "pitch_deg": self.pitch,
            "front_load_share": fz_f / (self.m * G), "steer": self.steer,
            "throttle": self.inp["throttle"], "brake": self.inp["brake"],
            "handbrake": self.inp["handbrake"], "phase": self.inp["phase"],
            "cam_dist": self.cam_dist + self.cam_extra, "cam_height": self.cam_height,
            "cam_fov": self.fov0 + self.fov_add * min(1.0, speed / (CAMERA_TOP_MPH * MPH)),
            "cam_lag": self.cam_tau,
            "wfl_x": fa[0] - off * right[0], "wfl_y": fa[1] - off * right[1],
            "wfr_x": fa[0] + off * right[0], "wfr_y": fa[1] + off * right[1],
        }

    def step(self, inp, dt):
        self.inp = inp
        # steering smoothing
        target = clamp(inp["steer"], -1.0, 1.0)
        tau = self.steer_tau_in if abs(target) > abs(self.steer) else self.steer_tau_out
        self.steer += (target - self.steer) * min(1.0, dt / tau)
        delta = self.steer * math.radians(self.max_steer_deg)
        m, a, b, L = self.m, self.a, self.b, self.L
        fz_f = m * G * b / L - m * self.ax * self.h / L
        fz_r = m * G - fz_f
        u_eff = max(abs(self.u), 0.5)
        # longitudinal forces
        fxf = inp["throttle"] * min(self.power / max(self.u, 1.0), self.drive_max)
        sgn = 1.0 if self.u >= 0 else -1.0
        moving = abs(self.u) > 0.01
        fb = inp["brake"] * self.brake_max if moving else 0.0
        fxf -= sgn * min(fb * self.brake_front, self.mu * fz_f)
        fxr = -sgn * min(fb * (1 - self.brake_front), self.mu * fz_r)
        fxf = clamp(fxf, -self.mu * fz_f, self.mu * fz_f)
        # lateral forces: linear, cut off at what grip is left (friction circle)
        cap_f = math.sqrt(max((self.mu * fz_f) ** 2 - fxf ** 2, 0.0))
        if self.u >= 0.0:
            alpha_f = delta - math.atan2(self.v + a * self.r, u_eff)
            fyf = clamp(self.cf * alpha_f, -cap_f, cap_f)
        else:
            # moving backwards in a spin: the front tyre slides sideways
            # (friction against the wheel-frame side velocity)
            vf_x = self.u * math.cos(delta) + (self.v + a * self.r) * math.sin(delta)
            vf_y = -self.u * math.sin(delta) + (self.v + a * self.r) * math.cos(delta)
            vm = math.hypot(vf_x, vf_y)
            fyf = -cap_f * vf_y / vm if vm > 0.05 else 0.0
        if inp["handbrake"] and moving:
            vr_lat = self.v - b * self.r
            vmag = math.hypot(self.u, vr_lat)
            if vmag > 0.05:
                fxr = -self.mu_lock * fz_r * self.u / vmag
                fyr = -self.mu_lock * fz_r * vr_lat / vmag
            else:
                fxr = fyr = 0.0
        else:
            alpha_r = -math.atan2(self.v - b * self.r, u_eff)
            cap_r = math.sqrt(max((self.mu * fz_r) ** 2 - fxr ** 2, 0.0))
            fyr = clamp(self.cr * alpha_r, -cap_r, cap_r)
        drag = 0.5 * 1.225 * self.cda * self.u * abs(self.u) + (self.rr * m * G * sgn if moving else 0.0)
        fx = fxf * math.cos(delta) - fyf * math.sin(delta) + fxr - drag
        fy = fxf * math.sin(delta) + fyf * math.cos(delta) + fyr
        mz = a * (fxf * math.sin(delta) + fyf * math.cos(delta)) - b * fyr
        if abs(math.atan2(self.v, max(abs(self.u), 0.1))) > math.radians(15):
            # spin damping once the car is well sideways (arcade-style, as
            # many game cars have; stands in for the four-tyre scrub a
            # bicycle model lacks)
            mz -= self.spin_damp * self.r
        self.ax, self.ay = fx / m, fy / m
        u_old = self.u
        self.u += (self.ax + self.v * self.r) * dt
        self.v += (self.ay - self.u * self.r) * dt
        self.r += mz / self.iz * dt
        if (moving and u_old * self.u <= 0 and inp["throttle"] == 0
                and math.hypot(self.u, self.v) < 0.5):
            self.u = self.v = self.r = 0.0   # brakes hold at a stop, no reversing
            self.ax = self.ay = 0.0
        if (abs(self.u) < 0.3 and inp["throttle"] == 0 and abs(self.v) < 0.3
                and not inp["handbrake"]):
            # low-speed settle: tyres stop lateral creep at a crawl
            self.v *= 0.9
            self.r *= 0.9
        self.hd += self.r * dt
        self.x += (self.u * math.sin(self.hd) + self.v * math.cos(self.hd)) * dt
        self.y += (self.u * math.cos(self.hd) - self.v * math.sin(self.hd)) * dt
        # roll and pitch springs (second order)
        for name, k, target_deg, wn, zeta in (
                ("roll", self.roll_k, -self.roll_k * self.ay / G, 2 * math.pi * 1.0, 0.5),
                ("pitch", self.pitch_k, self.pitch_k * self.ax / G, 2 * math.pi * 1.2, 0.6)):
            p, pv = getattr(self, name), getattr(self, name + "_v")
            acc = wn * wn * (target_deg - p) - 2 * zeta * wn * pv
            pv += acc * dt
            p += pv * dt
            setattr(self, name, p)
            setattr(self, name + "_v", pv)
        # chase camera: trails like a first-order lag of cam_tau seconds
        speed = math.hypot(self.u, self.v)
        self.cam_extra += (speed * self.cam_tau - self.cam_extra) * min(1.0, dt / self.cam_tau)


def run_drive(run_name, car=None, hz=PHYSICS_HZ):
    """Runs one drive on a car at a fixed step; returns telemetry rows."""
    wet = "-wet-" in run_name
    car = car or ReferenceCar(wet=wet)
    car.reset()
    drive = make_drive(run_name.replace("wet-", ""), car.info())
    dt = 1.0 / hz
    rows, t = [], 0.0
    s = car.state(t)
    n = 0
    while True:
        inp = drive.step(t, s, dt)
        car.inp = inp
        s = car.state(t)
        rows.append(s)
        if inp["done"]:
            break
        car.step(inp, dt)
        n += 1
        t = n * dt
        s = car.state(t)
    return rows


def run_all_reference(out_dir=None, slalom_until_unclean=True):
    runs, metas = {}, {}
    for name in RUN_NAMES:
        if name.startswith("D4-") and slalom_until_unclean:
            prev = [n for n in runs if n.startswith("D4-")]
            if prev and not slalom_clean(runs[max(prev, key=lambda n: int(n.split("-")[1]))]):
                continue
        car = ReferenceCar(wet="-wet-" in name)
        rows = run_drive(name, car)
        runs[name], metas[name] = rows, car.info()
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
            write_telemetry(os.path.join(out_dir, name + ".csv"), rows, car.info())
    result = compute_metrics(runs, metas, car="reference (not the game)")
    if out_dir:
        with open(os.path.join(out_dir, "result.json"), "w", encoding="utf-8") as f:
            json.dump(result, f, indent=1)
    return result, runs


# ---------------------------------------------------------------------------
# Command line
# ---------------------------------------------------------------------------

def _print_rows(rep):
    for r in rep["rows"]:
        print("  %-36s %-10s %s" % (r["metric"], r["status"],
                                     "" if r.get("value") is None else "%.3f" % r["value"]))
    print("PASS" if rep["pass"] else "FAIL")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("reference")
    p.add_argument("--out", required=True)
    p = sub.add_parser("metrics")
    p.add_argument("folder")
    p.add_argument("--out")
    p.add_argument("--car")
    p = sub.add_parser("targets")
    p.add_argument("--out")
    p.add_argument("--set", default="ordinary", help="ordinary (default) or fast")
    p = sub.add_parser("compare")
    p.add_argument("result")
    p.add_argument("--targets")
    p.add_argument("--against")
    p.add_argument("--rel", type=float, default=0.05)
    p.add_argument("--set", default="ordinary", help="named target set: ordinary or fast")
    a = ap.parse_args(argv)
    if a.cmd == "reference":
        res, _ = run_all_reference(a.out)
        rep = compare_targets(res, default_targets())
        _print_rows(rep)
        return 0
    if a.cmd == "metrics":
        res = metrics_from_dir(a.folder, a.car)
        text = json.dumps(res, indent=1)
        if a.out:
            with open(a.out, "w", encoding="utf-8") as f:
                f.write(text)
        else:
            print(text)
        return 0
    if a.cmd == "targets":
        text = json.dumps(default_targets(a.set), indent=1)
        if a.out:
            with open(a.out, "w", encoding="utf-8") as f:
                f.write(text)
        else:
            print(text)
        return 0
    if a.cmd == "compare":
        with open(a.result, encoding="utf-8") as f:
            res = json.load(f)
        if a.against:
            with open(a.against, encoding="utf-8") as f:
                rep = compare_results(res, json.load(f), rel=a.rel)
        else:
            tg = default_targets(a.set)
            if a.targets:
                with open(a.targets, encoding="utf-8") as f:
                    tg = json.load(f)
            rep = compare_targets(res, tg)
        _print_rows(rep)
        return 0 if rep["pass"] else 1
    return 2


if __name__ == "__main__":
    sys.exit(main())
