"""Tests for frametime_summary.py. Run: python -m pytest tools/lane/test_frametime_summary.py
(or python tools/lane/test_frametime_summary.py)."""
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(__file__))
import frametime_summary as fs  # noqa: E402


def write_csv(header, rows):
    fd, path = tempfile.mkstemp(suffix=".csv")
    with os.fdopen(fd, "w", newline="") as fh:
        fh.write(",".join(header) + "\n")
        for r in rows:
            fh.write(",".join(str(x) for x in r) + "\n")
    return path


class Percentiles(unittest.TestCase):
    def test_nearest_rank(self):
        vals = list(range(1, 101))
        self.assertEqual(fs.nearest_rank(vals, 99), 99)
        self.assertEqual(fs.nearest_rank(vals, 95), 95)
        self.assertEqual(fs.nearest_rank(vals, 100), 100)
        self.assertEqual(fs.nearest_rank(vals, 0), 1)

    def test_median_even_odd(self):
        self.assertEqual(fs.median([1, 2, 3]), 2)
        self.assertEqual(fs.median([1, 2, 3, 4]), 2.5)


class Summary(unittest.TestCase):
    def test_steady_60(self):
        s = fs.summarise([16.667] * 600)
        self.assertEqual(s["frames"], 600)
        self.assertAlmostEqual(s["median_ms"], 16.67, places=2)
        self.assertAlmostEqual(s["avg_fps"], 60.0, places=0)
        self.assertEqual(s["spikes_over_2x_median"], 0)
        self.assertFalse(s["reliable_0_1_percent"])

    def test_one_percent_low_two_definitions(self):
        # 990 frames at 10 ms, 10 frames at 50 ms: total 10,400 ms.
        frames = [10.0] * 990 + [50.0] * 10
        s = fs.summarise(frames)
        # Slowest 1% by count = 10 frames of 50 ms -> 20 fps.
        self.assertEqual(s["low1_avg_fps"], 20.0)
        # 1% of time = 104 ms; the 50 ms frames reach it at the 3rd -> 20 fps.
        self.assertEqual(s["low1_timeweighted_fps"], 20.0)
        self.assertEqual(s["p99_ms"], 10.0)  # rank 990 is still 10 ms
        self.assertEqual(s["worst_ms"], 50.0)
        self.assertEqual(s["spikes_over_2x_median"], 10)

    def test_time_weighted_differs(self):
        # 1000 frames of 10 ms plus 2 of 100 ms: total 10,200 ms, 1% = 102 ms.
        # Time-weighted: 100 + 100 >= 102 at the 2nd -> 10 fps.
        # Count-based: slowest 10 = 2 x 100 + 8 x 10 = 280 / 10 = 28 ms -> 35.7 fps.
        s = fs.summarise([10.0] * 1000 + [100.0] * 2)
        self.assertEqual(s["low1_timeweighted_fps"], 10.0)
        self.assertEqual(s["low1_avg_fps"], 35.7)
        self.assertTrue(s["reliable_0_1_percent"])

    def test_too_few_frames(self):
        with self.assertRaises(ValueError):
            fs.summarise([16.0] * 50)

    def test_ignores_bad_values(self):
        s = fs.summarise([16.0] * 200 + [0.0, -1.0, float("nan"), float("inf")])
        self.assertEqual(s["frames"], 200)


class Spread(unittest.TestCase):
    def test_spread(self):
        self.assertEqual(fs.pass_spread_pct([10.0, 10.2, 10.3]), 3.0)
        with self.assertRaises(ValueError):
            fs.pass_spread_pct([10.0])


class Reading(unittest.TestCase):
    def test_v2_default_columns_and_process_filter(self):
        header = ["Application", "ProcessID", "MsBetweenPresents", "MsBetweenAppStart"]
        rows = [["Game.exe", 1, 16, 17]] * 150 + [["dwm.exe", 2, 5, 5]] * 50
        p = write_csv(header, rows)
        frames, col = fs.read_capture(p, process="game.EXE")
        self.assertEqual(col, "MsBetweenAppStart")
        self.assertEqual(len(frames), 150)
        self.assertTrue(all(f == 17 for f in frames))

    def test_v2_metrics_frametime(self):
        p = write_csv(["Application", "FrameTime", "CPUBusy"], [["G.exe", 8.3, 4]] * 120)
        frames, col = fs.read_capture(p)
        self.assertEqual(col, "FrameTime")

    def test_v1_lowercase(self):
        p = write_csv(["ProcessName", "msBetweenPresents"], [["G.exe", 20]] * 120)
        frames, col = fs.read_capture(p, process="G.exe")
        self.assertEqual(col, "msBetweenPresents")
        self.assertEqual(len(frames), 120)

    def test_na_and_skip_warmup(self):
        rows = [["G.exe", "NA"]] + [["G.exe", 100]] * 200  # 20 s of 100 ms frames
        p = write_csv(["Application", "MsBetweenAppStart"], rows)
        frames, _ = fs.read_capture(p, skip_seconds=5)
        self.assertEqual(len(frames), 150)

    def test_no_frame_column(self):
        p = write_csv(["Application", "Other"], [["G.exe", 1]] * 5)
        with self.assertRaises(ValueError):
            fs.read_capture(p)

    def test_process_filter_without_column(self):
        p = write_csv(["MsBetweenPresents"], [[16]] * 120)
        with self.assertRaises(ValueError):
            fs.read_capture(p, process="G.exe")

    def test_main_prints_json(self):
        import io
        from contextlib import redirect_stdout
        p = write_csv(["Application", "MsBetweenAppStart"], [["G.exe", 16.7]] * 300)
        buf = io.StringIO()
        with redirect_stdout(buf):
            fs.main([p, "--process", "G.exe"])
        out = json.loads(buf.getvalue())
        self.assertEqual(out["frames"], 300)
        self.assertEqual(out["column"], "MsBetweenAppStart")


if __name__ == "__main__":
    unittest.main()
