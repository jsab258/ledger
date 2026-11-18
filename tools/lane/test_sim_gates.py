"""Tests for sim_gates.py's judging and golden comparison (no dotnet needed)."""
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(__file__))
import sim_gates as g  # noqa: E402


class Judge(unittest.TestCase):
    def test_coretests_pass(self):
        self.assertTrue(g.passed("CoreTests", 0, "  ok - x\n\nAll 5255 checks passed.\n"))

    def test_coretests_failed_line(self):
        self.assertFalse(g.passed("CoreTests", 0, "FAILED: x\nAll 1 checks passed"))

    def test_nonzero_exit_fails(self):
        self.assertFalse(g.passed("Soak", 1, "soak ok"))

    def test_marker_needed(self):
        self.assertTrue(g.passed("SaveChaos", 0, "save chaos ok — all 149 checks passed"))
        self.assertFalse(g.passed("SaveChaos", 0, "nothing"))

    def test_stranger_sweep(self):
        self.assertTrue(g.passed("StrangerTest", 0, "strangerSweep paths=108/108"))
        self.assertFalse(g.passed("StrangerTest", 0, "strangerSweep paths=107/108"))
        self.assertFalse(g.passed("StrangerTest", 0, "strangerSweep"))


class Goldens(unittest.TestCase):
    def _repo(self, parts):
        d = tempfile.mkdtemp()
        f = os.path.join(d, "ue-probe", "perception-golden")
        os.makedirs(f)
        for i, p in enumerate(parts, 1):
            open(os.path.join(f, f"part-{i:02d}.txt"), "wb").write(p)
        return d

    def test_match_in_order(self):
        repo = self._repo([b"ab", b"cd"])
        e = os.path.join(repo, "e.txt")
        open(e, "wb").write(b"abcd")
        self.assertTrue(g.goldens_match(repo, e))

    def test_mismatch(self):
        repo = self._repo([b"ab", b"cd"])
        e = os.path.join(repo, "e.txt")
        open(e, "wb").write(b"cdab")
        self.assertFalse(g.goldens_match(repo, e))


    def test_no_parts_fails(self):
        repo = self._repo([])
        e = os.path.join(repo, "e.txt")
        open(e, "wb").write(b"")
        self.assertFalse(g.goldens_match(repo, e))

    def test_missing_output_fails(self):
        repo = self._repo([b"ab"])
        self.assertFalse(g.goldens_match(repo, os.path.join(repo, "none.txt")))


class Work(unittest.TestCase):
    def test_used_work_folder_refused(self):
        w = tempfile.mkdtemp()
        open(os.path.join(w, "x"), "w").write("old")
        with self.assertRaises(SystemExit):
            g.prepare("/nonexistent", w)


if __name__ == "__main__":
    unittest.main()
