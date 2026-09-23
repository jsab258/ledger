#!/usr/bin/env python3
"""The mechanical canon gate (ledger-v2/studio-v2/verification.md, gate 1).

    python3 tools/canon-gate.py <file> [file...]     # gate the named files
    python3 tools/canon-gate.py --corpus             # gate the declared corpus
    python3 tools/canon-gate.py --selftest           # both outcomes

EXIT CODES, distinct per outcome: 0 clean, 1 finding(s), 2 NOTHING MEASURED
(a corpus walk that found no file, or a declared root that is not on disk).
A run that examined nothing is never a pass, and must not be readable as one.

WHAT IT CHECKS, and what it deliberately does not. canon.md holds three
classes of fact. Era artifacts and banned modernity are MECHANICAL: a line
containing a mobile phone or the internet is wrong in 1988 to 1992 no matter
how well written, so a grep can refuse it. Real brands are mechanical the
same way, reusing the imagegen forbidden-token list so there is one list,
not two (one idea, one implementation). TONE IS NOT MECHANICAL and is not
checked here: the D3 register needs the D7 judge, which needs Jafar's
calibration sample. A tool that pretended to check tone would be a claim
with no instrument, which is the exact thing the constitution forbids.

Every refusal names the file, the line number and the word, because a gate
whose red cannot be acted on teaches people to read red as noise. Every
clean result ships its denominator (rule 3b): files and lines examined.

FALSE-POSITIVE DISCIPLINE, learned 26 Aug on this repo: `british rail`
matched inside `British railway sign` and the fix was to reword the prose,
never to loosen the guard. A trade-mark guard that errs toward refusing is
erring the right way. The same holds here: a legitimate sentence ABOUT the
ban ("no mobiles in ordinary pockets" in canon itself) will trip the gate,
so canon.md and the decision register are EXEMPT BY NAME below, and the
exemption is printed whenever it bites.
"""
import json
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent

#: Words that cannot exist in 1988-1992 Meridian content. Word-boundary
#: matched, case-insensitive. Each entry names its reason so a refusal
#: teaches rather than scolds.
MODERNITY = {
    "mobile phone": "no mobiles in ordinary pockets (canon, Era)",
    "cell phone": "no mobiles (canon, Era); and 'cell phone' is American",
    "smartphone": "no mobiles (canon, Era)",
    "internet": "no internet (canon, Era)",
    "website": "no internet (canon, Era)",
    "email": "no internet (canon, Era); letters and phone calls",
    "wifi": "no internet (canon, Era)",
    "texted": "no SMS in the window (canon, Era); pagers exist for dealers",
    "text message": "no SMS in the window (canon, Era)",
    "social media": "no internet (canon, Era)",
    "selfie": "no camera phones (canon, Era); one camcorder in town",
    "google": "no internet (canon, Era), and a real brand besides",
    "cctv everywhere": "CCTV is rare: the bank, the ferry terminal (canon, Era)",
}

#: Paths whose text may legitimately DISCUSS banned things: the law itself,
#: the decisions that made it, and this tool.
EXEMPT = ("canon.md", "ledger-v2/", "legacy/", "tools/canon-gate.py",
          "production/queue/README.md", ".claude/agents/",
          # THE CONTENT RULE'S WORD LIST IN THE GAME, 23 September: generated
          # by tools/content-gate.py --emit-core from D18's list, so it names
          # the banned words in order to refuse them ('street walkers' read
          # as the crisps brand and turned the core tests red). It is the law
          # itself, as canon.md is; --emit-core --check keeps it equal to the
          # list, so nothing else can hide in it.
          "ledger/Assets/Scripts/Core/ContentWords.cs",
          # THE JUDGE'S REJECTING FIXTURES. Sample 2 contains canon
          # violations BY CONSTRUCTION: without them D7's zero-false-passes
          # clause cannot be measured at all. A gate that refused its own
          # rejecting fixture would be the 21 Aug incident again, where a
          # guard's fixtures pointed at live content and died the moment the
          # work was done. Exempt by path, printed whenever it bites, and
          # the selftest proves the same lines still refuse elsewhere.
          # Prefix, not a filename: the file was renamed from
          # judge-calibration-2 to judge-test-set-1 the day after it was
          # written, and the gate caught it the same minute by refusing 11
          # deliberate violations. That is the exemption being narrow, which
          # is correct. It is keyed to the judge-fixture prefix rather than
          # to any one name so a rename inside the family does not silently
          # re-arm it, while a fixture moved OUT of the family loses the
          # exemption and is screened like content again.
          "production/specs/judge-")

#: THE CORPUS THIS GATE GOVERNS, declared HERE and not in the runners, so
#: ledger/verify.py and tools/ci-checks.sh cannot drift apart about what
#: canon covers: one idea, one implementation, ruled in section 1.1 of
#: game-design/decision-2026-09-16-ruling-wire-or-delete-the-last-instrument-and-seven-settlements.md
#: under Jafar's wire-or-delete policy of 2026-09-16. These three
#: roots are where world content lives. The law and its discussion are
#: deliberately OUT: MODERNITY above contains the word for the network that
#: does not exist in 1988, and CLAUDE.md section 0 uses that word in its own
#: ban, so a corpus containing the law would arrive red on the law.
CORPUS_ROOTS = ("content", "ledger/Assets/Scripts", "production/specs")

#: Text this gate can read, as a visible suffix list rather than a binary
#: sniff a reader cannot audit. A file type that enters the tree unlisted is
#: counted as skipped and printed, never silently examined or silently
#: ignored.
CORPUS_SUFFIXES = (".md", ".txt", ".json", ".cs", ".yaml", ".yml", ".csv",
                   ".asmdef", ".shader", ".hlsl", ".cginc")

#: Build output and vendored trees: never authored text.
CORPUS_SKIP_DIRS = {".git", "bin", "obj", "Library", "Temp", "node_modules",
                    "__pycache__"}


def forbidden_brands():
    """The imagegen forbidden-token list MINUS the content-rule tokens.

    An empty list is a FAILURE here, not a pass: a brand gate with no brands
    would wave everything through and look identical to a clean run.

    WHY THE SUBTRACTION, ADDED 2026-09-10. Until D18 every token in that
    list was a real trade mark and this gate could say "contains X - real
    brand" about any of them. D18 put 62 content-rule tokens in the same
    list, because imagegen's substring check is the mechanism that refuses a
    prompt, and the first run afterwards reported eleven findings in the
    brand bible: the bible's own contentRule block NAMES the kinds it
    refuses, so `bookmaker` and `bingo` were reported as real brands in the
    file whose job is to ban them.

    So: one list still, read from one place, and the two halves separated by
    asking tools/content-gate.py which tokens are its own rather than by
    keeping a second copy here. Both counts are printed on the done line, so
    a subtraction that ate too much is a number somebody can see.
    """
    p = REPO / "tools" / "imagegen" / "prompts.json"
    toks = json.loads(p.read_text(encoding="utf-8"))["content_rules"]["forbidden_tokens"]
    if not toks:
        raise SystemExit("canon-gate: the forbidden-token list is EMPTY; refusing to run")
    content = content_rule_tokens()
    brands = [t for t in toks if t.strip().lower() not in content]
    if not brands:
        raise SystemExit(
            "canon-gate: subtracting the content-rule tokens left NO brand "
            "tokens at all (%d in, %d subtracted). That is a fault in the "
            "subtraction, not a clean list." % (len(toks), len(content)))
    return brands


def content_rule_tokens():
    """The D18 tokens, asked of the tool that owns them. Empty on failure,
    which is the SAFE direction here: this gate then screens everything it
    used to, and the worst case is a false refusal a reader can act on,
    never a silent pass."""
    gate = REPO / "tools" / "content-gate.py"
    if not gate.exists():
        return set()
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("_cg", gate)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return {t.strip().lower() for _id, _k, t in mod.PROMPT_TOKENS}
    except Exception:                                        # noqa: BLE001
        return set()


#: THE SCREENING LADDER for C# source, and the bound is the LAST rung. TWO
#: READINGS BELOW, AND THEY ARE TWO MOMENTS OF THE SAME WALK, not two
#: corpora. Both are --corpus over content/, ledger/Assets/Scripts/ and
#: production/specs/ on 2026-09-16.
#:
#:   BEFORE the two spec rewords of that day, and this is the run that chose
#:   the bound, printed before any of this machinery existed:
#:   wholeLine=134 commentsStripped=11 stringLiteralsOnly=6 urlsStripped=5
#:   notAMetricKey=4.
#:
#:   AFTER them, which is what a green run prints today and what the
#:   verify.py footer carries: wholeLine=130 commentsStripped=7
#:   stringLiteralsOnly=2 urlsStripped=1 notAMetricKey=0.
#:
#: The 4 that left were prose in two specs STATING the ban rather than
#: breaking it (learning.md L19 recurring), reworded and never exempted. So
#: of the first run's 134: 123 were words inside comments, 5 inside
#: identifiers (`float bp` is a band-pass filter, not British Petroleum), 1 a
#: cited URL, 1 the metric key `walkers={walkerCount}` whose key has 333
#: readers in this tree and cannot be renamed, and only 4 were prose.
#:
#: THE TWO FILE COUNTS ARE ALSO TWO DIFFERENT NUMBERS, not a drift:
#: filesOffered=212 is what the walk FOUND, and the done line's 209 file(s)
#: is what was READ. The 3 between them are the judge fixtures exempt by name
#: above, printed on every run. No file left the walk when the specs were
#: reworded; rewording a line cannot change a file count.
#:
#: EVERY RUNG IS PRINTED ON EVERY RUN, so a suppression that grows is a
#: number somebody can see rather than a silence.
#:
#: Rung names are what the count is a statistic OF: findings at that rung,
#: cumulative over the whole run, and the deltas between rungs are the only
#: numbers a ladder yields.
RUNGS = ("wholeLine", "commentsStripped", "stringLiteralsOnly", "urlsStripped",
         "notAMetricKey")
BOUND_RUNG = len(RUNGS) - 1

#: A URL is a citation, not prose a player can meet: `sites.google.com` in a
#: research source line is the fourth class the 26 Aug precedent calls a false
#: positive of the word list (a term inside a path). Whitespace-delimited, so
#: the sentence AROUND the URL is still screened word for word.
URL = re.compile(r"\S*://\S*|\bwww\.\S*")

#: A term that is immediately a key in a `key=value` channel (`walkers={n}`)
#: is machine output, not a line a player can meet. Narrow on purpose: the
#: term must be followed by `=` with nothing between.
METRIC_KEY = "="


def cs_layers(text):
    """Split C# into the two layers a canon gate cares about.

    Returns (code, strings): line number -> text, where `code` is the source
    with comments removed and `strings` is the contents of string literals.
    A player can read a string literal. A player cannot read a comment or an
    identifier, which is why 123 of the first run's 134 findings were noise.

    WHY NOT tools/slopcheck.py's `strings_from_cs`, which also extracts C#
    strings: its 20-character floor is load-bearing for ITS measured ceiling
    (the 88 figure its docstring explains), and it returns whole strings
    rather than per-line spans. Widening it to serve this gate would move
    another instrument's number, so the divergence is named here instead, the
    same way this file already names its divergence from the imagegen
    substring scanner below. If a third caller ever needs C# strings, this is
    the one to lift out, not to copy again.
    """
    n, i, line = len(text), 0, 1
    code, strs = {}, {}
    st = "code"
    while i < n:
        c = text[i]
        nxt = text[i + 1] if i + 1 < n else ""
        if st == "code":
            if c == "/" and nxt == "/":
                st = "lc"; i += 2; continue
            if c == "/" and nxt == "*":
                st = "bc"; i += 2; continue
            if c == "@" and nxt == '"':
                st = "vb"; i += 2; continue
            if c == '"':
                st = "st"; i += 1; continue
            if c == "'":
                st = "ch"; i += 1; continue
            if c == "\n":
                line += 1; i += 1; continue
            code.setdefault(line, []).append(c); i += 1; continue
        if st == "lc":
            if c == "\n":
                st = "code"; line += 1
            i += 1; continue
        if st == "bc":
            if c == "*" and nxt == "/":
                st = "code"; i += 2; continue
            if c == "\n":
                line += 1
            i += 1; continue
        if st == "st":
            if c == "\\":
                i += 2; continue
            if c == '"':
                st = "code"; i += 1; continue
            if c == "\n":                # unterminated: fail toward screening
                st = "code"; line += 1; i += 1; continue
            strs.setdefault(line, []).append(c); i += 1; continue
        if st == "vb":                   # @"verbatim", may span lines
            if c == '"' and nxt == '"':
                strs.setdefault(line, []).append('"'); i += 2; continue
            if c == '"':
                st = "code"; i += 1; continue
            if c == "\n":
                line += 1; i += 1; continue
            strs.setdefault(line, []).append(c); i += 1; continue
        if st == "ch":
            if c == "\\":
                i += 2; continue
            if c == "'":
                st = "code"; i += 1; continue
            if c == "\n":
                st = "code"; line += 1
            i += 1; continue
    return code, strs


def rung_text(rel, text):
    """The four rungs for one file: {rung index: [(lineno, text)]}.

    NON-CODE FILES HAVE NO LAYERS: .md and .json are content all the way
    down, so every rung is the raw line and the four counts coincide. Only
    .cs has comments and identifiers to peel, which is why the breakdown is
    per rung and the done line says how many findings each peel removed.
    """
    lines = text.splitlines()
    raw = list(enumerate(lines, 1))
    if not rel.endswith(".cs"):
        no_urls = [(n, URL.sub(" ", ln)) for n, ln in raw]
        return {0: raw, 1: raw, 2: raw, 3: no_urls, 4: no_urls}
    code, strs = cs_layers(text)
    nums = sorted(set(list(code) + list(strs)))
    no_comments = [(n, "".join(code.get(n, [])) + " " + "".join(strs.get(n, [])))
                   for n in nums]
    only_strings = [(n, "".join(strs.get(n, []))) for n in nums]
    no_urls = [(n, URL.sub(" ", t)) for n, t in only_strings]
    return {0: raw, 1: no_comments, 2: only_strings, 3: no_urls, 4: no_urls}


def screen_prefilter(brands):
    """One alternation over every screened term, used ONLY as a pre-filter.

    A piece of text this does not match cannot contain any term, so the exact
    per-term loop below is skipped for it. THE SEMANTICS ARE THE PER-TERM
    LOOP'S, UNCHANGED: this decides nothing, it only decides what to skip.
    Measured 2026-09-16: 114,156 lines x 58 terms x 4 rungs took 26s per run
    without it, and a check that slow is a check somebody removes.
    """
    words = [re.escape(w) for w in MODERNITY]
    words += [re.escape(t.strip()) for t in brands if t.strip()]
    return re.compile(r"\b(?:" + "|".join(words) + r")\b")


def term_hits(low, brands, drop_metric_keys=False, pre=None):
    """Every screened term on one lowercased piece of text.

    WORD-BOUNDED, NOT SUBSTRING, and the difference is one real incident each
    way. Substring caught 'british rail' inside 'British railway' (26 Aug):
    annoying, harmless, reword the prose. But substring 'bt ' (British
    Telecom) matches inside 'debts ', and this is a crime game about a book
    of uncollectable debts: the guard would ban the premise. The trailing
    spaces in the imagegen token list were always a crude boundary; this
    makes the boundary real. The imagegen scanner keeps its own substring
    semantics for prompts, where 'debt' does not occur; the divergence is
    named here so nobody unifies them back into the broken shape.
    """
    if pre is not None and not pre.search(low):
        return []
    out = []
    for word, why in MODERNITY.items():
        m = re.search(r"\b" + re.escape(word) + r"\b", low)
        if m and not (drop_metric_keys and low[m.end():m.end() + 1] == METRIC_KEY):
            out.append((word, why))
    for tok in brands:
        t = tok.strip()
        if not t:
            continue
        m = re.search(r"\b" + re.escape(t) + r"\b", low)
        if m and not (drop_metric_keys and low[m.end():m.end() + 1] == METRIC_KEY):
            out.append((t, "real brand (canon: Brands and law)"))
    return out


def gate(paths):
    brands = forbidden_brands()
    pre = screen_prefilter(brands)
    checked_files = checked_lines = 0
    hits = []
    rung_counts = [0] * len(RUNGS)
    exempt_bitten = []
    for path in paths:
        p = pathlib.Path(path)
        # FORWARD SLASHES BEFORE THE PREFIX TEST, 2026-09-22. EXEMPT is
        # written with "/" and a resolved path on Windows carries "\\", so
        # every exemption silently missed on Jafar's PC: canon.md screened
        # itself, and the judge's rejecting fixtures - which contain canon
        # violations BY CONSTRUCTION, because without them D7's clause cannot
        # be measured - reported sixteen findings that are the fixtures doing
        # their job. It passed in CI the whole time, because Linux uses "/".
        # The same shape as the Core suite's own line-ending fixture, found
        # the same day: a check that runs on one of the two machines this
        # project uses is a check the other cannot be asked to run.
        rel = str(p.resolve()).replace("\\", "/").replace(str(REPO).replace("\\", "/") + "/", "")
        if any(rel.startswith(e) for e in EXEMPT):
            exempt_bitten.append(rel)
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        checked_files += 1
        checked_lines += len(text.splitlines())
        rungs = rung_text(rel, text)
        for r in range(len(RUNGS)):
            for n, piece in rungs[r]:
                for word, why in term_hits(piece.lower(), brands, pre=pre,
                                           drop_metric_keys=(r == BOUND_RUNG)):
                    rung_counts[r] += 1
                    if r == BOUND_RUNG:
                        hits.append((rel, n, word, why))
    for rel in exempt_bitten:
        print(f"  exempt by name, not examined: {rel}")
    for rel, n, word, why in hits:
        print(f"  CANON: {rel}:{n} contains '{word}' - {why}")
    verdict = "RED" if hits else "clean"
    # THE LADDER, printed every run: findings at each rung, cumulative over
    # the run, and what each peel removed. A peel that starts eating real
    # findings shows up here as a delta that grows.
    print("  ladder " + " ".join(
        f"{RUNGS[r]}={rung_counts[r]}" for r in range(len(RUNGS)))
        + f" peeledComments={rung_counts[0] - rung_counts[1]}"
          f" peeledIdentifiers={rung_counts[1] - rung_counts[2]}"
          f" peeledUrls={rung_counts[2] - rung_counts[3]}"
          f" peeledMetricKeys={rung_counts[3] - rung_counts[4]}")
    print(f"canon-gate: {verdict} - {len(hits)} finding(s) in {checked_files} file(s), "
          f"{checked_lines} line(s) examined, {len(MODERNITY)} era term(s) and "
          f"{len(brands)} brand token(s) screened")
    return 1 if hits else 0


def corpus_files(roots=CORPUS_ROOTS):
    """Walk the declared corpus. Returns (per_root, files, skipped).

    THE BREAKDOWN IS PER ROOT, which is the axis the corpus actually varies
    on, and each root carries BOTH halves of the reading: whether the root
    exists at all, and how many files it offered. A root that vanished and a
    root that is empty are different faults with the same file count, and one
    number cannot tell them apart.
    """
    per_root, files, skipped = [], [], 0
    for root in roots:
        base = pathlib.Path(root)
        if not base.is_absolute():
            base = REPO / root
        if not base.is_dir():
            per_root.append((root, False, 0))
            continue
        found = []
        for p in sorted(base.rglob("*")):
            if not p.is_file():
                continue
            if any(part in CORPUS_SKIP_DIRS
                   for part in p.relative_to(base).parts[:-1]):
                continue
            if p.suffix.lower() not in CORPUS_SUFFIXES:
                skipped += 1
                continue
            found.append(p)
        per_root.append((root, True, len(found)))
        files.extend(found)
    return per_root, files, skipped


def corpus(roots=CORPUS_ROOTS):
    """Gate every file in the declared corpus, and refuse to call an empty
    walk clean.

    Exit 2 is NOTHING MEASURED and is its own outcome: a walk that found no
    file, or a declared root that is not on disk, examined nothing. Deleting
    content/ must not turn this gate green (rule 3b).
    """
    per_root, files, skipped = corpus_files(roots)
    for root, exists, n in per_root:
        # PER-ROOT numbers on the per-root line; whole-run numbers below.
        print("  corpus root=%s exists=%s filesOffered=%d"
              % (root, "yes" if exists else "NO", n))
    missing = [r for r, exists, _n in per_root if not exists]
    print("  corpus rootsDeclared=%d rootsPresent=%d filesOffered=%d "
          "filesSkippedBySuffix=%d suffixes=%s"
          % (len(per_root), len(per_root) - len(missing), len(files), skipped,
             "/".join(x.lstrip(".") for x in CORPUS_SUFFIXES)))
    if missing or not files:
        print("canon-gate: NOTHING MEASURED - %d of %d declared root(s) not on "
              "disk (%s) and the walk offered %d file(s). An empty walk is not "
              "a clean run."
              % (len(missing), len(per_root),
                 ",".join(missing) if missing else "none", len(files)))
        return 2
    return gate([str(x) for x in files])


def selftest():
    import tempfile
    ok = fail = 0

    def check(name, cond, detail=""):
        nonlocal ok, fail
        ok, fail = (ok + 1, fail) if cond else (ok, fail + 1)
        print(f"  {'pass' if cond else 'FAIL'}  {name}  {detail if not cond else ''}")

    print("canon-gate selftest")
    print("-" * 60)
    with tempfile.TemporaryDirectory() as td:
        td = pathlib.Path(td)
        good = td / "good.md"
        good.write_text("June leaves a message with the barman. The phone box "
                        "on Quay Street takes tens. Mickey's opens at eleven.\n")
        bad = td / "bad.md"
        bad.write_text("Tom checks his mobile phone.\nShe looks it up on the internet.\n"
                       "A crate of Guinness in the cellar.\n")
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc_good = gate([str(good)])
        check("ACCEPTING: a clean late-analog paragraph passes", rc_good == 0, buf.getvalue())
        check("accepting: the clean result carries its denominator",
              "line(s) examined" in buf.getvalue())
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc_bad = gate([str(bad)])
        out = buf.getvalue()
        check("REJECTING: mobile phone, internet and a real brand all refuse",
              rc_bad == 1 and out.count("CANON:") == 3, out)
        check("rejecting: every refusal names file, line and reason",
              "bad.md:1" in out and "bad.md:2" in out and "bad.md:3" in out)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc_canon = gate([str(REPO / "canon.md")])
        check("EXEMPTION: canon.md itself is exempt BY NAME and says so",
              rc_canon == 0 and "exempt by name" in buf.getvalue())
        debt = td / "debt.md"
        debt.write_text("Mickey left a book of uncollectable debts. No doubt "
                        "the rent is late too.\n")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc_debt = gate([str(debt)])
        check("BOUNDARY: 'debts' and 'doubt' pass, the premise is not a brand",
              rc_debt == 0, buf.getvalue())
        # THE EXEMPTION MUST NOT BE A HOLE. The fixture path is exempt; the
        # same text anywhere else must still refuse, or the exemption has
        # quietly become a way to smuggle canon violations into content.
        fixture_line = "Give us a ring on the mobile phone when you are outside."
        smuggled = td / "not-a-fixture.md"
        smuggled.write_text(fixture_line + "\n")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc_smug = gate([str(smuggled)])
        check("EXEMPTION IS NOT A HOLE: fixture text outside the fixture path "
              "still refuses", rc_smug == 1, buf.getvalue())
        bt = td / "bt.md"
        bt.write_text("He rang from the BT box on the corner.\n")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc_bt = gate([str(bt)])
        check("BOUNDARY: 'BT' alone still refuses", rc_bt == 1, buf.getvalue())

        # THE CORPUS WALK. ACCEPTING CASE FIRST AND IT IS THE LIVE TREE: the
        # roots really are on disk today and really do hold files, so this
        # fixture cannot be fooled by one I wrote, and doing the work the
        # gate prompts can never break it.
        per_root, live_files, _skipped = corpus_files()
        check("ACCEPTING: every declared corpus root is on disk and offers "
              "files (%s)" % "/".join("%s:%d" % (r, n) for r, _e, n in per_root),
              len(per_root) == len(CORPUS_ROOTS)
              and all(exists and n > 0 for _r, exists, n in per_root))
        check("accepting: the live walk offered files at all (%d)"
              % len(live_files), len(live_files) > 0)
        # REJECTING, AND THE FIXTURE IS SYNTHETIC: a root that exists nowhere
        # in this repo, so the rejecting case cannot be deleted by doing the
        # work. Nothing measured is its own exit, never a clean one.
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc_none = corpus(roots=("no-such-root-canon-gate-selftest",))
        out = buf.getvalue()
        check("REJECTING: a corpus root that exists nowhere is NOTHING "
              "MEASURED (exit 2), not clean",
              rc_none == 2 and "NOTHING MEASURED" in out, out)
        check("rejecting: the missing root prints exists=NO and its zero "
              "denominator", "exists=NO" in out and "filesOffered=0" in out, out)

        # THE C# LADDER. ACCEPTING FIRST: a player cannot read a comment or a
        # metric key, and 123 of the first corpus run's 134 findings were
        # comments. Both files below contain the SAME banned words; only the
        # layer differs, which is the whole claim being tested.
        cs_ok = td / "Ok.cs"
        cs_ok.write_text('// A packet of Walkers and a mobile phone, in a comment.\n'
                         'class X { void F() { Log($"walkers={n} email={a}"); } }\n')
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc_cs_ok = gate([str(cs_ok)])
        out = buf.getvalue()
        check("ACCEPTING: a brand and an era term in a C# COMMENT and in a "
              "metric key pass", rc_cs_ok == 0, out)
        check("accepting: and the ladder SAYS it peeled them, so the "
              "suppression is never silent",
              "peeledComments=" in out and "peeledMetricKeys=" in out
              and "wholeLine=" in out, out)
        cs_bad = td / "Bad.cs"
        cs_bad.write_text('class X { void F() { Say("He ate a packet of Walkers "\n'
                          '+ "and rang on his mobile phone."); } }\n')
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc_cs_bad = gate([str(cs_bad)])
        out = buf.getvalue()
        check("REJECTING: THE PEEL IS NOT A HOLE - the same words inside a C# "
              "STRING still refuse", rc_cs_bad == 1 and out.count("CANON:") == 2,
              out)

        # URLS. ACCEPTING FIRST: a citation is a path, not a line a player
        # meets. The planted rejecting case sits beside it (rule 5b): the
        # same term as prose on the same line still refuses.
        url_ok = td / "cite.md"
        url_ok.write_text("Source: UK payphones, Pay on Answer, "
                          "https://sites.google.com/site/payphone500/pay-on-answer .\n")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc_url = gate([str(url_ok)])
        check("ACCEPTING: a screened term inside a cited URL passes",
              rc_url == 0, buf.getvalue())
        url_bad = td / "cite-bad.md"
        url_bad.write_text("Google it; the source is https://sites.google.com/x .\n")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc_url_bad = gate([str(url_bad)])
        check("REJECTING: the same term as PROSE beside a URL still refuses",
              rc_url_bad == 1, buf.getvalue())

    # D18, THE SUBTRACTION. ACCEPTING FIRST: the live list still yields the
    # trade marks this gate has always screened, and a content-rule token is
    # no longer among them. Both counts, so a subtraction that ate the wrong
    # half is visible rather than quiet.
    all_toks = json.loads((REPO / "tools" / "imagegen" / "prompts.json")
                          .read_text(encoding="utf-8"))["content_rules"]["forbidden_tokens"]
    brands = forbidden_brands()
    content = content_rule_tokens()
    check("ACCEPTING: the live list still yields trade marks (%d of %d, "
          "%d content-rule token(s) subtracted)"
          % (len(brands), len(all_toks), len(content)),
          len(brands) >= 40 and "coca-cola" in [b.strip().lower() for b in brands])
    check("rejecting: 'bingo' is NOT screened here as a real brand - it is "
          "the content gate's, and the brand bible's own rule block names it",
          "bingo" not in [b.strip().lower() for b in brands])
    check("and the content token set is not empty, so the subtraction "
          "actually happened (%d)" % len(content), len(content) > 0)
    print("-" * 60)
    print(f"  {ok} passed, {fail} failed")
    return 1 if fail else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.exit(selftest())
    if "--corpus" in sys.argv[1:]:
        sys.exit(corpus())
    if len(sys.argv) < 2:
        print("usage: canon-gate.py <file> [file...] | --corpus | --selftest")
        sys.exit(2)
    sys.exit(gate(sys.argv[1:]))
