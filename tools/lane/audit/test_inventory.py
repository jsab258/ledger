import json
import os
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import inventory  # noqa: E402


def write(root, rel, text):
    p = os.path.join(root, *rel.split("/"))
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(text)


def commit(root, date, msg):
    env = dict(os.environ, GIT_AUTHOR_DATE=date + "T12:00:00", GIT_COMMITTER_DATE=date + "T12:00:00",
               GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t",
               GIT_COMMITTER_EMAIL="t@t")
    subprocess.run(["git", "add", "-A"], cwd=root, check=True, env=env)
    subprocess.run(["git", "commit", "-q", "-m", msg], cwd=root, check=True, env=env)


class InventoryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        r = cls.root = cls.tmp.name
        subprocess.run(["git", "init", "-q"], cwd=r, check=True)
        # oldest commit
        write(r, "group/old/z.txt", "zzz")
        write(r, "group/old/inner/w.txt", "www")
        write(r, "stale/s.txt", "stale file")
        commit(r, "2026-06-01", "old")
        write(r, "stale/s2.txt", "stale 2")
        commit(r, "2026-09-20", "stale touched")
        # duplicates, readme, owners
        write(r, "alpha/README.md", "# Alpha\n\n> **Alpha** does `things`.\n")
        write(r, "alpha/a.txt", "I live in alpha/ myself")
        write(r, "alpha/sub/b.txt", "b")
        write(r, "dup1/x.txt", "same x")
        write(r, "dup1/y.txt", "same y")
        write(r, "dup2/x.txt", "same x")
        write(r, "dup2/y.txt", "same y")
        write(r, "legacy/thing/t.txt", "t")
        write(r, "ledger/sim/s.cs", "class S {}")
        write(r, "production/clothing/c.txt", "c")
        write(r, "production/misc/m.txt", "m")
        write(r, "tools/lane/audit/q.py", "x")
        write(r, "headonly/README.md", "# Only A Heading\n")
        write(r, "group/live.txt", "live")
        write(r, "node_modules/pkg/index.js", "x")
        commit(r, "2026-10-15", "build")
        write(r, "docs/notes.md",
              "See alpha/sub for details, and dup1/ too.\n"
              "Windows: alpha\\sub and stale/ are used. Also alpha/subtle is not it.\n"
              "The word tools and content alone mean nothing.\n")
        write(r, "production/storage-map.json", json.dumps({"keep": "alpha/sub"}))
        write(r, "production/retention.json", json.dumps({"dirs": ["dup2"]}))
        commit(r, "2026-11-01", "refs")
        cls.inv = inventory.build_inventory(r)
        cls.by = {f["path"]: f for f in cls.inv["folders"]}

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_top_level_fields(self):
        self.assertFalse(self.inv["shallow"])
        self.assertEqual(self.inv["newest_commit"], "2026-11-01")
        self.assertIn("made", self.inv)

    def test_excludes_git_and_node_modules(self):
        for p in self.by:
            self.assertFalse(p.startswith(".git") or "node_modules" in p, p)

    def test_counts_and_size(self):
        a = self.by["alpha"]
        self.assertEqual(a["depth"], 1)
        self.assertEqual(a["file_count_direct"], 2)
        self.assertEqual(a["file_count_total"], 3)
        self.assertEqual(self.by["alpha/sub"]["depth"], 2)
        self.assertEqual(self.by["alpha/sub"]["size_bytes"], 1)
        self.assertEqual(self.by["group/old"]["file_count_total"], 2)
        self.assertEqual(self.by["group/old"]["file_count_direct"], 1)

    def test_purpose(self):
        self.assertEqual(self.by["alpha"]["purpose"], "Alpha does things.")
        self.assertEqual(self.by["headonly"]["purpose"], "Only A Heading")
        self.assertEqual(self.by["dup1"]["purpose"], "")

    def test_last_commit(self):
        self.assertEqual(self.by["group/old"]["last_commit"], "2026-06-01")
        self.assertEqual(self.by["stale"]["last_commit"], "2026-09-20")
        self.assertEqual(self.by["group"]["last_commit"], "2026-10-15")
        self.assertEqual(self.by["production"]["last_commit"], "2026-11-01")

    def test_references(self):
        sub = self.by["alpha/sub"]["referenced_by"]
        self.assertIn("docs/notes.md", sub["examples"])
        self.assertIn("production/storage-map.json", sub["examples"])
        self.assertEqual(sub["count"], 2)
        self.assertNotIn("alpha/subtle", self.by)
        # top-level name must be followed by a slash; bare words do not count
        self.assertEqual(self.by["tools"]["referenced_by"]["count"], 0)
        self.assertEqual(self.by["dup1"]["referenced_by"]["examples"], ["docs/notes.md"])
        # a file inside the folder never counts
        self.assertEqual(self.by["alpha"]["referenced_by"]["examples"], ["docs/notes.md"])  # alpha/a.txt is inside, alpha/subtle counts
        self.assertEqual(self.by["stale"]["referenced_by"]["count"], 1)

    def test_owner(self):
        o = {p: self.by[p]["owner"] for p in self.by}
        self.assertEqual(o["ledger"], "town (simulation)")
        self.assertEqual(o["ledger/sim"], "town (simulation)")
        self.assertEqual(o["tools/lane/audit"], "lane")
        self.assertEqual(o["tools"], "builder")
        self.assertEqual(o["production/clothing"], "clothing")
        self.assertEqual(o["production/misc"], "builder")
        self.assertEqual(o["production"], "shared")
        self.assertEqual(o["legacy/thing"], "none (archive)")
        self.assertEqual(o["alpha"], "shared")
        self.assertEqual(inventory.owner_of("ledger-v2/x"), "reference (old version)")
        self.assertEqual(inventory.owner_of("content/garments/a"), "clothing")
        self.assertEqual(inventory.owner_of("production/research/lane/x"), "lane")
        self.assertEqual(inventory.owner_of("production/research/x"), "shared research")
        self.assertEqual(inventory.owner_of("game-design/x"), "design")

    def test_storage_and_retention(self):
        self.assertTrue(self.by["alpha/sub"]["in_storage_map"])
        self.assertFalse(self.by["dup1"]["in_storage_map"])
        self.assertTrue(self.by["dup2"]["in_retention"])
        self.assertFalse(self.by["alpha"]["in_retention"])

    def test_content_hash_and_duplicates(self):
        self.assertEqual(self.by["dup1"]["content_hash"], self.by["dup2"]["content_hash"])
        self.assertNotEqual(self.by["dup1"]["content_hash"], "")
        self.assertEqual(self.by["dup1"]["duplicates"], ["dup2"])
        self.assertEqual(self.by["dup2"]["duplicates"], ["dup1"])
        # single-file folder has no hash
        self.assertEqual(self.by["legacy/thing"]["content_hash"], "")
        self.assertEqual(self.by["alpha"]["duplicates"], [])
        # ancestor/descendant with identical content are not duplicates
        self.assertNotIn("group/old", self.by["group/old/inner"]["duplicates"])

    def test_status(self):
        s = {p: self.by[p]["status"] for p in self.by}
        self.assertEqual(s["dup1"], "duplicate")
        self.assertEqual(s["legacy/thing"], "reference")
        self.assertEqual(s["group/old"], "dead")
        self.assertEqual(s["group/old/inner"], "dead")
        self.assertEqual(s["group"], "live")
        self.assertEqual(s["stale"], "stale")  # referenced, 42 days before newest
        self.assertEqual(s["alpha"], "live")
        self.assertEqual(self.by["group/old"]["status_basis"], "heuristic")
        self.assertTrue(self.by["group/old"]["status_reason"])

    def test_cli_outputs(self):
        out = os.path.join(self.root, "..", os.path.basename(self.root) + "-out")
        try:
            rc = inventory.main(["--repo", self.root, "--out", out])
            self.assertEqual(rc, 0)
            data = json.load(open(os.path.join(out, "inventory.json"), encoding="utf-8"))
            self.assertEqual(set(data), {"made", "shallow", "newest_commit", "folders"})
            table = open(os.path.join(out, "work", "inventory-table.md"), encoding="utf-8").read()
            self.assertIn("| alpha/sub |", table)
            self.assertNotIn("| alpha/a.txt |", table)
        finally:
            import shutil
            shutil.rmtree(out, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
