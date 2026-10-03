# The check: fail the build when a file every session reads grows past its cap

**What it checks.** Words counted as `wc -w` counts them:

| File | Cap |
|---|---|
| CLAUDE.md | 1,000 |
| RULINGS.md | 2,500 |
| NOW.md | 200 |
| Each session's own status file (TOWN.md, CLOTHES.md) | 300 |

**How it fails:**
- A file over its cap fails the build, which names the file, its count and its three largest sections, so the session knows where to cut.
- A missing file fails too, because nothing measured must never read as clean, as the check runner's own rule says.
- The script and its self-test are below. Both were run here: the self-test passes all five cases. Against today's files (main at 5db99d5) it fails all five: CLAUDE.md 4,372 words, NOW.md 3,241, TOWN.md 831, CLOTHES.md 1,732, RULINGS.md missing. Against the drafts, CLAUDE.md (997) and RULINGS.md (2,497) pass.

## How it is wired

1. **The new file** is tools/doc-caps.py, the script below.
2. **Two rows go into tools/ci-checks.sh's table** (`real_table`), beside the others:
   ```
       doc-caps              "$REPO"                 "$PY tools/doc-caps.py" \
       doc-caps-selftest     "$REPO"                 "$PY tools/doc-caps.py --selftest" \
   ```
   The core-tests workflow runs the table on every push that touches `tools/*.py` or `production/**`.

   Its triggers do not include the root-level CLAUDE.md, RULINGS.md, NOW.md, TOWN.md or CLOTHES.md. **Add those five paths to `.github/workflows/ledger-core-tests.yml`'s `paths:`**, or a push that only grows them never runs the check.
3. **One line in tools/hooks/pre-commit,** before the size guard: `python tools/doc-caps.py || exit 1`. It is cheap, under a tenth of a second, so a session cannot commit an oversize file at all, not just find out on GitHub. A session that hits it cuts its file; it never uses `--no-verify` (CLAUDE.md).

## The order to land it

**The check goes in the same commit that applies the drafts and trims NOW.md, TOWN.md and CLOTHES.md under their caps.** Landed alone, it turns every push red at once, because all five files fail today.

- **NOW.md's 200 words** cannot hold the builder's list as he wrote it (about 1,600 words today). The cap waits on his answer to question 2: one line per item, with the detail in the research it names, is recommended.
- **TOWN.md and CLOTHES.md** are each trimmed by their own session, to current state and the list, with history left in git.

## The script (tools/doc-caps.py)

```python
#!/usr/bin/env python3
"""THE FILES EVERY SESSION READS STAY SHORT ENOUGH TO BE READ, NOT SKIMMED.

Jafar, 3 October: DECISIONS.md reached 23,600 words in ten days, CLAUDE.md
4,000 against a cap of 600, NOW.md 2,300 against five lines; at that length the
sessions skimmed them and could not tell which ruling was current. So the caps
are checked by the build, not by good intentions: this fails when a file is
over its cap, and when a file it must measure is missing (nothing measured
must never read as clean).

Words are counted as `wc -w` counts them: runs of non-space characters.

  python tools/doc-caps.py             # the real files; exit 1 naming each one over
  python tools/doc-caps.py --selftest  # the check itself, both ways
"""
import os
import re
import sys
import tempfile

# THE CAPS. A new session's own status file is added here, with its cap, in the
# same commit that creates it.
CAPS = [
    ("CLAUDE.md", 1000),
    ("RULINGS.md", 2500),
    ("NOW.md", 200),
    ("TOWN.md", 300),
    ("CLOTHES.md", 300),
]


def words(text):
    return len(text.split())


def sections(text):
    """The largest '## ' sections, so a refusal says where to cut."""
    parts, name, buf = [], "(before the first heading)", []
    for line in text.splitlines():
        if re.match(r"^#{1,3} ", line):
            parts.append((words("\n".join(buf)), name))
            name, buf = line.strip("# ").strip(), []
        else:
            buf.append(line)
    parts.append((words("\n".join(buf)), name))
    return sorted(parts, reverse=True)[:3]


def check(root, caps=CAPS, out=sys.stdout):
    over = 0
    for rel, cap in caps:
        path = os.path.join(root, rel)
        if not os.path.isfile(path):
            print("doc-caps file=%s words=- cap=%d outcome=MISSING" % (rel, cap), file=out)
            over += 1
            continue
        text = open(path, encoding="utf-8").read()
        n = words(text)
        ok = n <= cap
        print("doc-caps file=%s words=%d cap=%d outcome=%s" % (rel, n, cap, "PASS" if ok else "FAIL"), file=out)
        if not ok:
            over += 1
            print("  largest sections: " + "; ".join("%s (%d)" % (s, w) for w, s in sections(text)), file=out)
    print("doc-caps: %d of %d over cap or missing" % (over, len(caps)), file=out)
    return over


def selftest():
    import io
    fails = 0

    def case(name, files, want_over):
        nonlocal fails
        with tempfile.TemporaryDirectory() as d:
            for rel, text in files.items():
                open(os.path.join(d, rel), "w", encoding="utf-8").write(text)
            buf = io.StringIO()
            got = check(d, [("A.md", 5), ("B.md", 3)], out=buf)
            ok = got == want_over
            fails += 0 if ok else 1
            print("  %s %s: over=%d, wanted %d" % ("ok  " if ok else "FAIL", name, got, want_over))

    print("doc-caps selftest")
    case("ACCEPT both at or under their caps", {"A.md": "one two three four five", "B.md": "a b"}, 0)
    case("ACCEPT markdown and line breaks count as wc -w does", {"A.md": "# H\n\n- x y\n", "B.md": "a\nb\nc"}, 0)
    case("REFUSE one word over the cap", {"A.md": "1 2 3 4 5 6", "B.md": "a"}, 1)
    case("REFUSE a missing file, never read as clean", {"A.md": "1"}, 1)
    case("REFUSE both over", {"A.md": "1 2 3 4 5 6", "B.md": "a b c d"}, 2)
    print("doc-caps selftest: %s" % ("passed" if fails == 0 else "FAILED (%d)" % fails))
    return 1 if fails else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.exit(selftest())
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.exit(1 if check(root) else 0)
```
