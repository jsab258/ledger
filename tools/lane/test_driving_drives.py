"""Tests for driving_drives.py (lane session, 17 November 2026).

Run from the repository root:
  python3 -m pytest tools/lane/test_driving_drives.py
  python3 -m unittest tools/lane/test_driving_drives.py
Synthetic telemetry with known answers checks each metric function; the drives
then run end to end on the reference car (not the game's handling).
"""
import json
import math
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import driving_drives as dd  # noqa: E402

MPH = dd.MPH
DT = 1.0 / 120


def row(t, **kw):
    r = {c: 0.0 for c in dd.REQUIRED_COLUMNS}
    r["t"] = t
    r["phase"] = ""
    r["front_load_share"] = 0.6
    r.update(kw)
    return r


def straight_accel(a, t_end, phase="run"):
    """Constant acceleration a (m/s^2) along +y from rest."""
    rows = []
    n = int(round(t_end / DT))
    for i in range(n + 1):
        t = i * DT
        rows.append(row(t, y=0.5 * a * t * t, speed=a * t, long_g=a / dd.G, phase=phase))
    return rows


class MetricSyntheticTest(unittest.TestCase):
    def test_d1_constant_acceleration_exact(self):
        a = 2.0
        rows = straight_accel(a, 20.0)
        m = dd.metric_d1(rows)
        self.assertAlmostEqual(m["M1.0_60_s"], 60 * MPH / a, places=6)
        self.assertAlmostEqual(m["M1.0_30_s"], 30 * MPH / a, places=6)
        self.assertAlmostEqual(m["M2.top_speed_mph"], 40.0 / MPH, places=6)
        # v at 100 m = sqrt(2 a d)
        self.assertAlmostEqual(m["M2.speed_at_100m_mph"], math.sqrt(2 * a * 100) / MPH, places=2)
        self.assertFalse(m["M2.top_speed_settled"])

    def test_d1_settled_flag(self):
        rows = straight_accel(2.0, 10.0)
        t_last = rows[-1]["t"]
        for i in range(1, 7 * 120):
            t = t_last + i * DT
            rows.append(row(t, y=rows[-1]["y"] + 20 * DT, speed=20.0, phase="run"))
        self.assertTrue(dd.metric_d1(rows)["M2.top_speed_settled"])

    def test_d2_constant_deceleration(self):
        v0, dec = 30 * MPH, 6.5
        rows = [row(-1 + i * DT, y=-v0 * (1 - i * DT), speed=v0, phase="approach",
                    front_load_share=0.58) for i in range(120)]
        n = int(math.ceil(v0 / dec / DT))
        k = 0.45 / 2.4
        for i in range(n + 1):
            t = min(i * DT, v0 / dec)
            v = max(v0 - dec * t, 0.0)
            g = -dec / dd.G if v > 0 else 0.0
            rows.append(row(t, y=v0 * t - 0.5 * dec * t * t, speed=v, long_g=g,
                            pitch_deg=3.0 * g, front_load_share=0.58 - k * g,
                            phase="brake"))
        m = dd.metric_d2(rows)
        self.assertAlmostEqual(m["distance_m"], v0 * v0 / (2 * dec), places=3)
        self.assertAlmostEqual(m["pitch_at_0_8g_deg"], 2.4, places=3)
        self.assertAlmostEqual(m["front_share_at_0_8g"], 0.58 + k * 0.8, places=4)

    def test_d2_no_stop_gives_none(self):
        rows = [row(i * DT, y=10 * i * DT, speed=10.0, phase="brake") for i in range(100)]
        self.assertIsNone(dd.metric_d2(rows)["distance_m"])

    def test_d3_wheel_columns_circle(self):
        rows = []
        for i in range(400):
            th = i / 399 * 2.5 * math.pi
            rows.append(row(i * 0.05, heading=th, phase="lock",
                            wfl_x=5.2 - 5.2 * math.cos(th), wfl_y=5.2 * math.sin(th),
                            wfr_x=4.0 - 4.0 * math.cos(th), wfr_y=4.0 * math.sin(th)))
        self.assertAlmostEqual(dd.metric_d3(rows)["M4.turning_circle_m"], 10.4, places=6)

    def test_d3_geometry_fallback(self):
        L, a, track, w = 2.4, 1.0, 1.4, 0.2
        r_rear = 3.8
        r_cg = math.hypot(r_rear, L - a)
        rows = [row(i * 0.05, heading=i / 299 * 2.5 * math.pi, phase="lock",
                    x=r_cg - r_cg * math.cos(i / 299 * 2.5 * math.pi),
                    y=r_cg * math.sin(i / 299 * 2.5 * math.pi)) for i in range(300)]
        meta = {"wheelbase": L, "cg_to_front": a, "track": track, "tyre_width": w}
        want = 2 * math.hypot(r_rear + track / 2 + w / 2, L)
        self.assertAlmostEqual(dd.metric_d3(rows, meta)["M4.turning_circle_m"], want, places=6)
        self.assertIsNone(dd.metric_d3(rows, {})["M4.turning_circle_m"])

    def test_d5_first_order_response(self):
        tau, r_ss, tc = 0.2, 0.3, 0.5
        rows = [row(-1 + i * DT, phase="approach") for i in range(120)]
        for i in range(int(2 / DT)):
            t = i * DT
            rows.append(row(t, yaw_rate=r_ss * (1 - math.exp(-t / tau)), phase="step"))
        y_rel = rows[-1]["yaw_rate"]
        for i in range(int(4 / DT)):
            t = i * DT
            rows.append(row(2 + t, yaw_rate=y_rel * math.exp(-t / tc), phase="release"))
        m = dd.metric_d5(rows)
        self.assertAlmostEqual(m["M5.yaw_63_s"], tau, delta=0.002)
        # under 5% of settled: t = tc * ln(y_rel / (0.05 * settled))
        settled = sum(r["yaw_rate"] for r in rows if r["phase"] == "step" and r["t"] >= 1.5)
        settled /= len([r for r in rows if r["phase"] == "step" and r["t"] >= 1.5])
        want = tc * math.log(y_rel / (0.05 * settled))
        self.assertAlmostEqual(m["M5.self_centre_s"], want, delta=0.002)

    def test_yaw_lag_shift(self):
        rows = []
        for i in range(1200):
            t = i * DT
            rows.append(row(t, steer=math.sin(2 * math.pi * 0.4 * t),
                            yaw_rate=0.3 * math.sin(2 * math.pi * 0.4 * (t - 0.15))))
        self.assertAlmostEqual(dd.yaw_lag(rows), 0.15, delta=DT)

    def test_slalom_clean_and_not(self):
        def run(amp):
            rows = []
            y = 200.0
            while y < 420:
                x = amp * math.cos(math.pi * (y - 250) / 18) if 241 <= y <= 385 else 0.0
                rows.append(row(len(rows) * DT, x=x, y=y, phase="cones"))
                y += 0.1
            return rows
        self.assertTrue(dd.slalom_clean(run(1.2)))
        self.assertFalse(dd.slalom_clean(run(0.5)))
        self.assertFalse(dd.slalom_clean(run(-1.2)))
        m = dd.metric_d4({30: run(1.2), 32: run(1.2), 34: run(0.5), 36: run(1.2)})
        self.assertEqual(m["M5.slalom_max_clean_mph"], 32)  # stops at first unclean

    def test_d7_turn_then_settle(self):
        # yaw rate 2 rad/s for 0.8 s, then zero: turned 1.6 rad, settled at 0.8 s
        rows = [row(-1 + i * DT, phase="approach") for i in range(120)]
        h = 0.0
        for i in range(int(3 / DT)):
            t = i * DT
            r = 2.0 if t < 0.8 else 0.0
            rows.append(row(t, heading=h, yaw_rate=r, phase="turn" if t < 0.6 else "stop"))
            h += r * DT
        m = dd.metric_d7(rows)
        self.assertAlmostEqual(m["M9.handbrake_settle_s"], 0.8, delta=DT)
        self.assertAlmostEqual(m["M9.handbrake_yaw_deg"], math.degrees(1.6), delta=0.5)

    def test_d8_camera(self):
        rows = [row(i * DT, speed=0.0, cam_dist=6.0, cam_height=1.9, cam_fov=65.0, phase="rest")
                for i in range(120)]
        for i in range(1, 2000):
            v = 0.025 * i
            rows.append(row(1 + i * DT, speed=v, cam_dist=6.0 + 0.2 * v, cam_height=1.9,
                            cam_fov=65 + 12 * min(1, v / (90 * MPH)), phase="run"))
        m = dd.metric_d8(rows)
        self.assertAlmostEqual(m["M10.cam_dist_m"], 6.0, places=3)
        self.assertAlmostEqual(m["M10.cam_lag_s"], 0.2, places=6)
        self.assertAlmostEqual(m["M10.fov_30_deg"], 65 + 12 / 3, places=3)
        self.assertAlmostEqual(m["M10.fov_widen_deg"], 12.0, delta=0.01)  # kink at 90 mph between samples


class TelemetryFormatTest(unittest.TestCase):
    def test_round_trip_csv_and_jsonl(self):
        rows = dd.run_drive("D5")
        meta = dd.ReferenceCar().info()
        with tempfile.TemporaryDirectory() as d:
            for ext in (".csv", ".jsonl"):
                p = os.path.join(d, "D5" + ext)
                dd.write_telemetry(p, rows, meta)
                back, m = dd.read_telemetry(p)
                self.assertEqual(len(back), len(rows))
                self.assertAlmostEqual(m["max_steer_deg"], dd.ReferenceCar().max_steer_deg)
                self.assertEqual(back[500]["phase"], rows[500]["phase"])
                a, b = dd.metric_d5(rows), dd.metric_d5(back)
                for k in a:
                    self.assertAlmostEqual(a[k], b[k], places=3)

    def test_missing_column_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "D1.csv")
            with open(p, "w") as f:
                f.write("t,x,y\n0,0,0\n")
            with self.assertRaises(ValueError):
                dd.read_telemetry(p)


class ReferenceDrivesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.result, cls.runs = dd.run_all_reference(cls.tmp.name)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_every_drive_ran_and_ended(self):
        for name in ["D1", "D2-30", "D2-50", "D2-70", "D2-wet-30", "D3", "D4-30", "D5", "D6", "D7", "D8"]:
            self.assertIn(name, self.runs)
            self.assertLess(self.runs[name][-1]["t"], make_cap(name))

    def test_reference_meets_first_targets(self):
        # the reference car is tuned to the ordinary set, not the game set
        self.assertEqual(dd.REFERENCE_SET, "ordinary")
        rep = dd.compare_targets(self.result, dd.default_targets(dd.REFERENCE_SET))
        fails = [r for r in rep["rows"] if r["status"] in ("fail", "missing")]
        self.assertEqual(fails, [], fails)
        self.assertTrue(rep["pass"])

    def test_physics_sanity(self):
        m = self.result["metrics"]
        self.assertLess(m["M3.brake_30_m"], m["M3.brake_50_m"])
        self.assertLess(m["M3.brake_50_m"], m["M3.brake_70_m"])
        self.assertGreater(m["M3.wet_brake_30_m"], m["M3.brake_30_m"])
        self.assertLess(m["M1.0_30_s"], m["M1.0_60_s"])
        self.assertTrue(m["M2.top_speed_settled"])
        self.assertGreaterEqual(m["M5.slalom_max_clean_mph"], 30)
        self.assertIsNotNone(m["M8.recovery_s"])
        self.assertGreater(m["M8.slide_onset_mph"], 30)

    def test_drives_follow_their_script(self):
        brake = [r for r in self.runs["D2-50"] if r["phase"] == "brake"]
        self.assertTrue(all(r["brake"] == 1.0 and r["steer"] == 0.0 for r in brake))
        self.assertAlmostEqual(brake[0]["speed"] / MPH, 50, delta=0.6)
        turn = [r for r in self.runs["D7"] if r["phase"] == "turn"]
        self.assertTrue(all(r["handbrake"] == 1 for r in turn))
        self.assertAlmostEqual(turn[0]["speed"] / MPH, 30, delta=0.6)

    def test_deterministic(self):
        again = dd.run_drive("D6")
        first = self.runs["D6"]
        self.assertEqual(len(again), len(first))
        self.assertEqual(again[-1]["x"], first[-1]["x"])

    def test_metrics_from_written_files_match(self):
        res = dd.metrics_from_dir(self.tmp.name)
        cmp = dd.compare_results(res, self.result, rel=1e-4, abs_tol={k: 0.0 for k in res["metrics"]})
        self.assertTrue(cmp["pass"], [r for r in cmp["rows"] if r["status"] != "pass"])

    def test_result_json_written(self):
        with open(os.path.join(self.tmp.name, "result.json")) as f:
            self.assertIn("M4.turning_circle_m", json.load(f)["metrics"])


def make_cap(name):
    return dd.make_drive(name.replace("wet-", ""), dd.ReferenceCar().info()).max_time


class CompareTest(unittest.TestCase):
    def res(self, **m):
        return {"metrics": m}

    def test_targets_pass_fail_placeholder_missing(self):
        tg = {"targets": {"M1.0_60_s": {"min": 11, "max": 15, "status": "first"},
                          "M3.brake_30_m": {"min": 12, "max": 16, "status": "first"},
                          "M8.recovery_s": {"min": None, "max": None, "status": "placeholder"}}}
        rep = dd.compare_targets(self.res(**{"M1.0_60_s": 13.0, "M3.brake_30_m": 16.0}), tg)
        self.assertTrue(rep["pass"])  # edges count as inside; placeholder not failed
        rep = dd.compare_targets(self.res(**{"M1.0_60_s": 15.01, "M3.brake_30_m": 14}), tg)
        self.assertFalse(rep["pass"])
        rep = dd.compare_targets(self.res(**{"M1.0_60_s": 13.0}), tg)
        self.assertFalse(rep["pass"])
        self.assertEqual({r["metric"]: r["status"] for r in rep["rows"]}["M3.brake_30_m"], "missing")

    def test_car_to_car_relative_and_absolute(self):
        browser = self.res(**{"M3.brake_70_m": 70.0, "M5.yaw_63_s": 0.20})
        # 5% of 70 m = 3.5 m
        self.assertTrue(dd.compare_results(self.res(**{"M3.brake_70_m": 73.4, "M5.yaw_63_s": 0.2}), browser)["pass"])
        self.assertFalse(dd.compare_results(self.res(**{"M3.brake_70_m": 73.6, "M5.yaw_63_s": 0.2}), browser)["pass"])
        # 5% of 0.20 s is 0.01 s, but the absolute floor for seconds is 0.05 s
        self.assertTrue(dd.compare_results(self.res(**{"M3.brake_70_m": 70, "M5.yaw_63_s": 0.249}), browser)["pass"])
        self.assertFalse(dd.compare_results(self.res(**{"M3.brake_70_m": 70, "M5.yaw_63_s": 0.26}), browser)["pass"])
        # custom absolute tolerance overrides the unit default
        self.assertFalse(dd.compare_results(self.res(**{"M3.brake_70_m": 70, "M5.yaw_63_s": 0.24}), browser,
                                            abs_tol={"M5.yaw_63_s": 0.01})["pass"])

    def test_car_to_car_missing(self):
        a = self.res(**{"M4.turning_circle_m": None, "M9.handbrake_settle_s": 2.0})
        b = self.res(**{"M4.turning_circle_m": None, "M9.handbrake_settle_s": None})
        rep = dd.compare_results(a, b)
        st = {r["metric"]: r["status"] for r in rep["rows"]}
        self.assertEqual(st["M4.turning_circle_m"], "skip")
        self.assertEqual(st["M9.handbrake_settle_s"], "missing")
        self.assertFalse(rep["pass"])

    def test_fast_set_and_unknown_set(self):
        f = dd.default_targets("fast")["targets"]
        self.assertEqual((f["M1.0_60_s"]["min"], f["M1.0_60_s"]["max"]), (8.0, 9.0))
        self.assertEqual((f["M2.top_speed_mph"]["min"], f["M2.top_speed_mph"]["max"]), (118.0, 122.0))
        self.assertEqual((f["M8.max_steady_lat_g"]["min"], f["M8.max_steady_lat_g"]["max"]), (0.82, 0.90))
        self.assertEqual(f["M1.0_30_s"]["status"], "placeholder")
        self.assertEqual(f["M10.cam_dist_m"]["min"], 5.0)  # shared with the ordinary set
        with self.assertRaises(ValueError):
            dd.default_targets("sports")

    def test_wet_ratio_metric(self):
        runs = {}
        for name, dist in (("D2-30", 13.0), ("D2-wet-30", 21.0)):
            v0 = 30 * MPH
            dec = v0 * v0 / (2 * dist)
            rows = [row(-0.5 + i * DT, speed=v0, phase="approach") for i in range(60)]
            n = int(math.ceil(v0 / dec / DT))
            for i in range(n + 1):
                t = min(i * DT, v0 / dec)
                rows.append(row(t, y=v0 * t - 0.5 * dec * t * t, speed=max(v0 - dec * t, 0.0),
                                long_g=-dec / dd.G, phase="brake"))
            runs[name] = rows
        m = dd.compute_metrics(runs)["metrics"]
        self.assertAlmostEqual(m["M3.wet_ratio_30"], 21.0 / 13.0, places=3)

    def test_default_targets_shape(self):
        t = dd.default_targets("ordinary")["targets"]
        self.assertEqual((t["M1.0_60_s"]["min"], t["M1.0_60_s"]["max"]), (13.0, 17.0))
        self.assertEqual((t["M4.turning_circle_m"]["min"], t["M4.turning_circle_m"]["max"]), (9.0, 10.5))
        self.assertEqual((t["M9.handbrake_yaw_deg"]["min"], t["M9.handbrake_yaw_deg"]["max"]), (90.0, 150.0))
        self.assertEqual(t["M3.wet_ratio_50"]["status"], "first")
        self.assertEqual(t["M3.wet_brake_30_m"]["status"], "placeholder")
        self.assertEqual(dd.abs_tol_for("M2.top_speed_mph"), 1.0)
        self.assertEqual(dd.abs_tol_for("M6.roll_deg_at_0_5g"), 0.3)
        self.assertEqual(dd.abs_tol_for("M7.front_load_brake_pct_at_0_8g"), 1.0)
        self.assertEqual(dd.abs_tol_for("M8.max_steady_lat_g"), 0.02)
        self.assertEqual(dd.abs_tol_for("M1.0_60_s"), 0.05)


# The game set of 18 Nov 2026 (his rulings 12:32 and 12:36), exactly as given.
GAME_BANDS = {
    "M1.0_30_s": (3.0, 4.5),
    "M1.0_60_s": (10.0, 14.0),
    "M2.top_speed_mph": (95.0, 110.0),
    "M2.speed_at_100m_mph": (44.0, 52.0),
    "M3.brake_30_m": (8.0, 11.0),
    "M3.brake_50_m": (22.0, 30.0),
    "M3.brake_70_m": (44.0, 58.0),
    "M3.wet_ratio_30": (1.3, 1.6),
    "M3.wet_ratio_50": (1.3, 1.6),
    "M3.wet_ratio_70": (1.3, 1.6),
    "M4.turning_circle_m": (8.5, 9.8),
    "M5.yaw_63_s": (0.15, 0.25),
    "M5.self_centre_s": (0.4, 0.9),
    "M6.roll_deg_at_0_5g": (3.5, 6.0),
    "M6.pitch_brake_deg_at_0_8g": (2.5, 5.0),
    "M6.pitch_throttle_deg": (1.0, 2.5),
    "M7.front_load_brake_pct_at_0_8g": (72.0, 82.0),
    "M8.max_steady_lat_g": (0.82, 0.92),
    "M8.recovery_s": (0.3, 0.8),
    "M9.handbrake_yaw_deg": (120.0, 180.0),
    "M9.handbrake_settle_s": (1.0, 1.6),
    "M10.cam_dist_m": (5.0, 6.5),
    "M10.cam_height_m": (1.6, 2.0),
    "M10.cam_lag_s": (0.1, 0.25),
    "M10.fov_0_deg": (60.0, 65.0),
    "M10.fov_30_deg": (64.0, 70.0),
    "M10.fov_60_deg": (70.0, 78.0),
    "M10.fov_90_deg": (76.0, 86.0),
}


class GameSetTest(unittest.TestCase):
    def test_game_is_the_default(self):
        self.assertEqual(dd.DEFAULT_SET, "game")
        t = dd.default_targets()
        self.assertEqual(t["set"], "game")
        self.assertIn("game band", t["note"])  # what tools/driving_feel_check.py looks for
        self.assertIn("PROVISIONAL", t["note"])
        self.assertEqual(dd.default_targets()["targets"], dd.default_targets("game")["targets"])

    def test_every_game_band_exact(self):
        t = dd.default_targets()["targets"]
        for key, (lo, hi) in GAME_BANDS.items():
            self.assertIn(key, t)
            self.assertEqual((t[key]["min"], t[key]["max"]), (lo, hi), key)
            self.assertEqual(t[key]["status"], "provisional", key)
        self.assertEqual(dict(dd.TARGET_SETS["game"]), GAME_BANDS)

    def test_game_set_covers_m1_to_m10(self):
        keys = dd.default_targets()["targets"]
        checked = {k.split(".")[0] for k, v in keys.items() if v["status"] != "placeholder"}
        self.assertEqual(checked, {"M%d" % i for i in range(1, 11)})
        # M11 and M12 are not measured by the drives, in any set
        self.assertFalse(any(k.startswith(("M11.", "M12.")) for k in keys))

    def test_game_set_placeholders_kept(self):
        t = dd.default_targets()["targets"]
        for k in dd.PLACEHOLDERS:
            self.assertEqual(t[k]["status"], "placeholder", k)

    def test_old_sets_still_selectable(self):
        o = dd.default_targets("ordinary")
        self.assertEqual(o["set"], "ordinary")
        self.assertEqual((o["targets"]["M1.0_60_s"]["min"], o["targets"]["M1.0_60_s"]["max"]), (13.0, 17.0))
        self.assertEqual(o["targets"]["M1.0_60_s"]["status"], "first")
        f = dd.default_targets("fast")
        self.assertEqual((f["targets"]["M1.0_60_s"]["min"], f["targets"]["M1.0_60_s"]["max"]), (8.0, 9.0))

    def test_game_set_judges_a_car(self):
        mid = {k: (lo + hi) / 2 for k, (lo, hi) in GAME_BANDS.items()}
        self.assertTrue(dd.compare_targets({"metrics": mid}, dd.default_targets())["pass"])
        slow = dict(mid, **{"M1.0_60_s": 15.0})  # a real 1990 hatch time, slower than the game band
        rep = dd.compare_targets({"metrics": slow}, dd.default_targets())
        self.assertFalse(rep["pass"])
        self.assertEqual({r["metric"]: r["status"] for r in rep["rows"]}["M1.0_60_s"], "fail")

    def test_command_line_default_set(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "t.json")
            self.assertEqual(dd.main(["targets", "--out", p]), 0)
            with open(p) as f:
                self.assertEqual(json.load(f)["set"], "game")
            self.assertEqual(dd.main(["targets", "--set", "ordinary", "--out", p]), 0)
            with open(p) as f:
                self.assertEqual(json.load(f)["set"], "ordinary")


if __name__ == "__main__":
    unittest.main()
