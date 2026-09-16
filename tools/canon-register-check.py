#!/usr/bin/env python3
"""canon.md must follow its own rulings: citation and status, never agreement.

JAFAR, 2026-09-16: "a ruling that changes canon edits canon in the same
batch." The sentence is in canon's STATUS block, where every agent reads it
and nothing checks it. A rule nobody can detect the breaking of is a wish,
and the two cases that produced the ruling (D16 decided six days before canon
stopped calling the engine open, D24 absent from canon although its own text
says it is recorded there) were each days old before a human noticed. So the
rule is mechanical here. Spec: section 8 of
game-design/decision-2026-09-16-ruling-a-caught-claim-is-not-what-they-know-
and-canon-follows-its-rulings.md.

WHAT IT ASSERTS, three things, each printing the count it examined:

  A1 NO OPEN ITEM IS DECIDED. Every `Dn` cited under canon's `## OPEN`
     heading resolves to a register record that is not settled (DECIDED,
     APPROVED, SUPERSEDED, or CLOSED BY another record).
  A2 NO SUPERSEDED RECORD IS CITED WITHOUT ITS SUCCESSOR. Every `Dn` cited
     anywhere in canon whose record carries "SUPERSEDED ... BY Dm" is cited
     beside `Dm`, beside meaning in the same block of canon.
  A3 EVERY RECORD THAT NAMES CANON IS IN CANON. Every DECIDED or APPROVED
     record that says it applies to canon has its `Dn` present in canon.md.

WHAT IT DOES NOT CLAIM, and this is the important half. It does NOT claim
that canon's SENTENCES AGREE with the rulings they cite. It reads citation
and status only: a canon line that cites D19 and then says the opposite of
D19 passes here. Agreement is a reading and the reading stays the resident's
on every canon edit, the same way `tools/content-gate.py --enforceable`
prints which clauses of D18 it can read and which it cannot.

HOW A3 DECIDES THAT A RECORD "NAMES CANON", and why the tool prints it. Two
paths, in this order:

  1. THE DIRECTIVE, which is the forward fix the ruling set: a record
     carries one machine-readable line, `CANON: none` or `CANON: edits
     <lines or heading>`. Read first, and for a record dated on or after
     2026-09-16 it is the ONLY path: a new record without one is a failure,
     because the phrase fallback is what this tool exists to retire.
  2. THE PHRASE LIST, for records older than that date. THE PHRASE LIST IS
     THE WEAK LINK and the ruling says so, so this tool prints WHICH PHRASE
     MATCHED WHICH RECORD and, beside it, every record that mentions canon
     in words the list does not carry, as UNMATCHED with its line. A checker
     whose miss looks identical to a pass is the fault this project keeps
     finding. UNMATCHED is advisory, not a failure: a record may mention
     canon without ruling on it (D3's "canon gate", D7's "canon violations",
     D43's "scope, canon or a pillar"), and a gate that reddened on those
     would be a gate everybody learns to ignore. It is printed and counted
     at every run so the list's decay is visible instead of silent.

THE PHRASES WERE SET FROM A PRINTED SERIES, NOT CHOSEN. `--series` prints
the per-record reading this list came from: status, how the status was read,
date, directive, and every canon-mentioning line. Run it before touching
PHRASES. Measured on the live tree 2026-09-16: 45 records, 16 mention canon,
4 match. Markdown emphasis is stripped before matching, which is not
cosmetic: D17 writes "1. **canon.md**, as a rule and not a note." and D24
writes "Recorded **in canon beside the pillars**", so a literal match over
the raw bytes finds ONE of the four records section 8 names, not four.

EXIT CODES, one per outcome, so a caller can tell them apart:
  0  all three assertions hold
  1  an assertion failed (the violation is named, with its line)
  2  NOTHING MEASURED: canon.md or the register is missing or unreadable.
     A run that examined nothing must never look like a clean run.
  3  --selftest found this tool broken

  tools/canon-register-check.py             # the gate, on this repo
  tools/canon-register-check.py --series    # the reading behind the list
  tools/canon-register-check.py --selftest  # accepting case first
"""
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANON = os.path.join(REPO, "canon.md")
REGISTER = os.path.join(REPO, "ledger-v2", "respec", "decision-register")

#: From this date a record carries its own CANON: line and the phrases below
#: are not consulted for it. The ruling's forward fix, 2026-09-16.
FORWARD_DATE = "2026-09-16"

#: The weak link, printed at every run. Slug on the left is what appears in
#: `matched=`; values carry no spaces because every reader splits on them.
PHRASES = (
    ("canon.md-as-a-rule", "canon.md, as a rule"),
    ("apply-it-to-canon", "apply it to canon"),
    ("recorded-in-canon", "recorded in canon"),
)

#: A record mentioning canon at all. The denominator UNMATCHED is counted
#: against: mentions minus matches is what the phrase list cannot see.
MENTION_RE = re.compile(r"canon", re.I)
CITE_RE = re.compile(r"\bD(\d+)\b")
DATE_RE = re.compile(r"\b(20\d\d-\d\d-\d\d)\b")
SUPERSEDED_RE = re.compile(r"SUPERSEDED\b[^\n]{0,40}?\bBY\s+D(\d+)", re.I)
CLOSED_RE = re.compile(r"CLOSED\b[^\n]{0,40}?\bBY\s+D(\d+)", re.I)
#: NOT ANCHORED TO LINE START, and that is a measurement, not a preference.
#: The first version anchored it and read UNREADABLE for nine of 45 records,
#: because the 31 August records write "Date: 2026-08-31. Status: APPROVED."
#: mid-line. Nine records dropping silently out of A3's numerator is the
#: exact shape of a clean result that examined nothing, so the count of
#: unreadable statuses is printed on A3's head line at every run.
STATUS_RE = re.compile(r"\bSTATUS:?\s*\**\s*([A-Za-z]+)", re.I)
RULEDBY_RE = re.compile(r"^\s*Ruled by Jafar", re.I | re.M)
DIRECTIVE_RE = re.compile(r"^CANON:\s*(none|edits\s+\S.*)$", re.M)
ITEM_RE = re.compile(r"^\s*(\d+)\.\s")
#: An OPEN item that says in its own words that it is not open. Canon's item
#: 1 does exactly this ("DECIDED, Unreal (D16 ...) ... it is not open"), kept
#: numbered so "OPEN 2" above it keeps its meaning. See A1's note below.
DECLARED_CLOSED_RE = re.compile(r"\bDECIDED\b|\bCLOSED\b|\bit is not open\b")

SETTLED = ("DECIDED", "APPROVED", "SUPERSEDED", "CLOSED")
NOTHING = "nothing measured"
#: How many of a list get printed before the cap bites. It always says so.
CAP = 12


def cap(items, n=CAP, sep=","):
    """Join at most n items; a truncation that does not announce itself reads
    as a finding. Returns the string plus its own overflow note."""
    if not items:
        return "none"
    if len(items) <= n:
        return sep.join(items)
    return sep.join(items[:n]) + sep + "(+%d-more-not-shown)" % (len(items) - n)


def demark(text):
    """Strip markdown emphasis before phrase matching. D17 and D24 write the
    phrase with `**` inside it, so the raw bytes carry the words and not the
    phrase; matching raw finds 1 of 4 records on the live tree."""
    return text.replace("**", "").replace("*", "").replace("_", "")


# ------------------------------------------------------------- the readings

def read_records(path=REGISTER):
    """Parse the register once. One implementation of this idea; every
    assertion below reads this dict rather than re-walking the directory."""
    if not os.path.isdir(path):
        return None, "the register %s is not a directory" % os.path.relpath(path, REPO)
    out = {}
    for name in sorted(os.listdir(path)):
        m = re.match(r"^D(\d+)-", name)
        if not m or not name.endswith(".md"):
            continue
        n = int(m.group(1))
        raw = open(os.path.join(path, name), encoding="utf-8").read()
        head = "\n".join(raw.split("\n")[:15])
        text = demark(raw)
        sup = SUPERSEDED_RE.search(demark(head))
        clo = CLOSED_RE.search(demark(head))
        st = STATUS_RE.search(demark(head))
        if sup:
            status, how = "SUPERSEDED", "superseded-by/D%s" % sup.group(1)
        elif clo:
            status, how = "CLOSED", "closed-by/D%s" % clo.group(1)
        elif st:
            status, how = st.group(1).upper(), "status-line"
        elif RULEDBY_RE.search(head):
            status, how = "DECIDED", "ruled-by-jafar"
        else:
            status, how = "UNREADABLE", "no-status-line"
        d = DATE_RE.search(head)
        direct = DIRECTIVE_RE.search(raw)
        mentions = [(i + 1, l.strip()) for i, l in enumerate(raw.split("\n"))
                    if MENTION_RE.search(l)]
        matched = None
        for slug, phrase in PHRASES:
            hit = next(((i, l) for i, l in
                        [(i + 1, demark(l)) for i, l in enumerate(raw.split("\n"))]
                        if phrase in l.lower()), None)
            if hit:
                matched = (slug, hit[0], hit[1])
                break
        out[n] = {
            "id": "D%d" % n, "file": name, "status": status, "statusHow": how,
            "date": d.group(1) if d else "", "supersededBy":
                int(sup.group(1)) if sup else None,
            "closedBy": int(clo.group(1)) if clo else None,
            "directive": direct.group(1).strip() if direct else None,
            "mentions": mentions, "matched": matched, "text": text,
        }
    if not out:
        return None, "the register holds 0 D-records"
    return out, "read %d record(s)" % len(out)


def read_canon(path=CANON):
    """Parse canon once: its citations with line numbers, its blocks, and the
    numbered items under `## OPEN`."""
    if not os.path.exists(path):
        return None, "%s does not exist" % os.path.relpath(path, REPO)
    lines = open(path, encoding="utf-8").read().split("\n")
    if not lines or not any(l.strip() for l in lines):
        return None, "%s is empty" % os.path.relpath(path, REPO)
    cites = []          # (n, lineno)
    block_of = {}       # lineno -> block index; a block is contiguous non-blank
    b = 0
    for i, l in enumerate(lines, 1):
        if not l.strip():
            b += 1
        block_of[i] = b
        for m in CITE_RE.finditer(l):
            cites.append((int(m.group(1)), i))
    # The numbered items under `## OPEN`, each with the lines it spans.
    items, cur, in_open = [], None, False
    for i, l in enumerate(lines, 1):
        if l.startswith("## "):
            if cur:
                items.append(cur)
                cur = None
            in_open = l.strip() == "## OPEN"
            continue
        if not in_open:
            continue
        m = ITEM_RE.match(l)
        if m:
            if cur:
                items.append(cur)
            cur = {"num": m.group(1), "lines": [(i, l)]}
        elif cur is not None and l.strip():
            cur["lines"].append((i, l))
    if cur:
        items.append(cur)
    return {"lines": lines, "cites": cites, "blockOf": block_of,
            "openItems": items}, "read %d line(s)" % len(lines)


# ---------------------------------------------------------- the assertions

def assertion1(canon, recs):
    """A1: no item presented as OPEN rests on a settled record.

    DEVIATION FROM SECTION 8'S LITERAL WORDING, NAMED RATHER THAN SMOOTHED
    OVER. Section 8 says every `Dn` under `## OPEN` must not be settled.
    Section 9.2 of the same record then dictates canon's item 1 as "Engine:
    DECIDED, Unreal (D16, 2026-09-10; closes D1) ... it is not open", kept
    numbered so "OPEN 2" keeps its meaning. Taken literally the first rule
    fails the second's own text on the commit that lands it, which is the
    arrives-red gate the ruling forbade. So the unit is the ITEM, not the
    citation: an item that declares its own closure must NAME a record that
    really is settled (a positive check, not a skip, so writing the word
    DECIDED cannot silence a live violation), and every other item's
    citations must be unsettled. Both modes print, so the exemption is
    visible and counted rather than a hole.
    """
    lines, bad = [], []
    declared = ok_declared = 0
    cited_total = 0
    for it in canon["openItems"]:
        text = " ".join(l for _, l in it["lines"])
        first_line = it["lines"][0][0]
        cited = []
        for _, l in it["lines"]:
            cited += [int(m.group(1)) for m in CITE_RE.finditer(l)]
        cited_total += len(cited)
        seen = ["D%d/%s" % (n, recs[n]["status"] if n in recs else "NO-RECORD")
                for n in cited]
        if DECLARED_CLOSED_RE.search(text):
            declared += 1
            closers = [n for n in cited
                       if n in recs and recs[n]["status"] in SETTLED]
            if closers:
                ok_declared += 1
                lines.append("A1 item=%s@L%d mode=declared-closed cites=%s "
                             "closedBy=D%d/%s"
                             % (it["num"], first_line, cap(seen), closers[0],
                                recs[closers[0]]["status"]))
            else:
                bad.append("item%s@L%d" % (it["num"], first_line))
                lines.append("A1 item=%s@L%d mode=declared-closed cites=%s "
                             "VIOLATION=declares-closure-but-names-no-settled-record"
                             % (it["num"], first_line, cap(seen)))
            continue
        settled = [n for n in cited
                   if n in recs and recs[n]["status"] in SETTLED]
        lines.append("A1 item=%s@L%d mode=open cites=%s%s"
                     % (it["num"], first_line, cap(seen) if seen else "none",
                        "" if not settled else " VIOLATION=settled-record-under-OPEN"))
        for n in settled:
            bad.append("D%d/%s@item%s" % (n, recs[n]["status"], it["num"]))
    head = ("A1 openItemsWalked=%d citationsUnderOpen=%d declaredClosed=%d/%d "
            "declaredClosedNamingSettledRecord=%d/%d violations=%d"
            % (len(canon["openItems"]), cited_total, declared,
               len(canon["openItems"]), ok_declared, declared, len(bad)))
    if not canon["openItems"]:
        head += " (%s: canon has no `## OPEN` items)" % NOTHING
    return bad, [head] + lines


def assertion2(canon, recs):
    """A2: a superseded record is never cited without its successor beside it.

    BESIDE means in the same block of canon (contiguous non-blank lines), so
    the reader who meets D15 meets D19 without scrolling. The pair prints as
    one entry with both positions, never two keys whose relationship a reader
    has to remember."""
    lines, bad = [], []
    sup_records = [n for n, r in recs.items() if r["status"] == "SUPERSEDED"]
    distinct_cited = sorted({n for n, _ in canon["cites"]})
    checked = 0
    for n in sorted(sup_records):
        # DEDUPED BY LINE, with the raw count kept beside it. canon line 30
        # writes "D15's pub; D15's siting", two mentions of one site, and the
        # first version printed the identical row twice, which reads as two
        # sites to anybody grepping.
        raw_hits = [ln for c, ln in canon["cites"] if c == n]
        hits = sorted(set(raw_hits))
        if not hits:
            continue
        checked += 1
        succ = recs[n]["supersededBy"]
        for ln in hits:
            blk = canon["blockOf"][ln]
            where = [l2 for c2, l2 in canon["cites"]
                     if c2 == succ and canon["blockOf"][l2] == blk]
            if where:
                lines.append("A2 D%d@L%d supersededBy=D%s successorAt=L%d "
                             "verdict=beside mentionsAtThatLine=%d"
                             % (n, ln, succ, where[0], raw_hits.count(ln)))
            else:
                anywhere = [l2 for c2, l2 in canon["cites"] if c2 == succ]
                bad.append("D%d@L%d" % (n, ln))
                lines.append("A2 D%d@L%d supersededBy=D%s successorAt=%s "
                             "VIOLATION=successor-not-in-the-same-block"
                             % (n, ln, succ,
                                ("L%d/other-block" % anywhere[0]) if anywhere
                                else "absent-from-canon"))
    head = ("A2 supersededRecordsInRegister=%d citedInCanon=%d/%d "
            "distinctRecordsCitedInCanon=%d violations=%d"
            % (len(sup_records), checked, len(sup_records),
               len(distinct_cited), len(bad)))
    if not sup_records:
        head += " (%s: the register holds no superseded record)" % NOTHING
    elif not checked:
        head += " (%s: no superseded record is cited in canon)" % NOTHING
    return bad, [head] + lines


def assertion3(canon, recs):
    """A3: every DECIDED or APPROVED record that says it applies to canon has
    its Dn in canon. Prints which phrase matched which record, and every
    record that mentions canon in words the list cannot read."""
    lines, bad = [], []
    in_canon = {n for n, _ in canon["cites"]}
    live = {n: r for n, r in recs.items() if r["status"] in ("DECIDED", "APPROVED")}
    names_canon, unmatched, missing_directive = [], [], []
    for n, r in sorted(live.items()):
        new = r["date"] >= FORWARD_DATE if r["date"] else False
        if r["directive"]:
            how = "directive/%s" % ("none" if r["directive"].lower() == "none"
                                    else "edits")
            applies = not r["directive"].lower().startswith("none")
        elif new:
            # THE FORWARD FIX HAS TEETH or it is a comment. A record written
            # after the ruling that carries no CANON: line is unreadable by
            # the path that is meant to replace the phrases.
            missing_directive.append("D%d@%s" % (n, r["date"]))
            lines.append("A3 D%d date=%s VIOLATION=no-CANON:-line-on-a-record-"
                         "dated-%s-or-later" % (n, r["date"], FORWARD_DATE))
            bad.append("D%d/no-CANON-line" % n)
            continue
        elif r["matched"]:
            how = "phrase/%s@L%d" % (r["matched"][0], r["matched"][1])
            applies = True
        else:
            how = "none"
            applies = False
            if r["mentions"]:
                unmatched.append("D%d@L%d" % (n, r["mentions"][0][0]))
        if not applies:
            continue
        names_canon.append("D%d" % n)
        if n in in_canon:
            at = sorted(l for c, l in canon["cites"] if c == n)
            lines.append("A3 D%d matched=%s citedInCanon=L%s verdict=present"
                         % (n, how, "/L".join(str(x) for x in at[:4])))
        else:
            bad.append("D%d/absent-from-canon" % n)
            lines.append("A3 D%d matched=%s citedInCanon=none "
                         "VIOLATION=record-names-canon-but-canon-does-not-cite-it"
                         % (n, how))
    mentioners = [n for n, r in live.items() if r["mentions"]]
    present = len([l for l in lines if "verdict=present" in l])
    # WHAT WAS LEFT OUT OF THE NUMERATOR, COUNTED. A record excluded because
    # its status is superseded, closed or unreadable is not a clean result:
    # it is a record this assertion did not examine, and it says so here.
    skipped = {"superseded": [], "closed": [], "open": [], "unreadable": []}
    for n, r in sorted(recs.items()):
        if r["status"] == "SUPERSEDED":
            skipped["superseded"].append("D%d" % n)
        elif r["status"] == "CLOSED":
            skipped["closed"].append("D%d" % n)
        elif r["status"] == "UNREADABLE":
            # THE ONE THAT MUST NEVER BE SILENT: a status this tool could not
            # parse is a record it did not examine, and it is not the same
            # fact as a record that is legitimately still open.
            skipped["unreadable"].append("D%d" % n)
        elif r["status"] not in ("DECIDED", "APPROVED"):
            skipped["open"].append("D%d/%s" % (n, r["status"]))
    head = ("A3 recordsWalked=%d decidedOrApproved=%d "
            "mentionCanonAmongThose=%d/%d namesCanon=%d/%d "
            "namesCanonAndIsCited=%d/%d violations=%d"
            % (len(recs), len(live), len(mentioners), len(live),
               len(names_canon), len(live), present, len(names_canon),
               len(bad)))
    head += (" notExamined=%d/%d superseded=%s closed=%s notDecided=%s "
             "statusUnreadable=%s"
             % (sum(len(v) for v in skipped.values()), len(recs),
                cap(skipped["superseded"]), cap(skipped["closed"]),
                cap(skipped["open"]), cap(skipped["unreadable"])))
    if not live:
        head += " (%s: no DECIDED or APPROVED record)" % NOTHING
    lines = [head] + lines
    # THE MISS MUST LOOK DIFFERENT FROM THE PASS. Advisory, never a failure,
    # always printed with its denominator so the list's decay is visible.
    lines.append("A3 UNMATCHED mentionsCanonButNoPhraseOrDirective=%d/%d "
                 "advisory=not-a-failure records=%s"
                 % (len(unmatched), len(mentioners), cap(unmatched)))
    lines.append("A3 FORWARD recordsDated%sOrLater=%d missingCANONline=%d%s"
                 % (FORWARD_DATE, len([1 for r in live.values()
                                       if r["date"] and r["date"] >= FORWARD_DATE]),
                    len(missing_directive),
                    "" if any(r["date"] and r["date"] >= FORWARD_DATE
                              for r in live.values())
                    else " (%s: no record is dated %s or later yet; the "
                         "phrase fallback carried every reading above)"
                         % (NOTHING, FORWARD_DATE)))
    return bad, lines


# ----------------------------------------------------------------- the gate

def check(canon_path=CANON, register_path=REGISTER):
    recs, why_r = read_records(register_path)
    if recs is None:
        return 2, ["canon-register: NOT CHECKED (%s) - %s" % (NOTHING, why_r)]
    canon, why_c = read_canon(canon_path)
    if canon is None:
        return 2, ["canon-register: NOT CHECKED (%s) - %s" % (NOTHING, why_c)]
    b1, l1 = assertion1(canon, recs)
    b2, l2 = assertion2(canon, recs)
    b3, l3 = assertion3(canon, recs)
    out = l1 + l2 + l3
    failed = len(b1) + len(b2) + len(b3)
    # WHOLE-RUN NUMBERS ON THE DONE LINE, per-assertion numbers on the lines
    # above it. Cumulative over this run; no other statistic.
    body = canon["lines"]
    while body and not body[-1].strip():
        body = body[:-1]
    done = ("canon-register: %s assertionsHeld=%d/3 violations=%d "
            "recordsWalked=%d canonLines=%d canonCitationsRaw=%d "
            "violationsA1=%d violationsA2=%d violationsA3=%d"
            % ("PASS" if not failed else "VIOLATION",
               3 - sum(1 for b in (b1, b2, b3) if b), failed, len(recs),
               len(body), len(canon["cites"]),
               len(b1), len(b2), len(b3)))
    if failed:
        out.append("canon-register: THE RULING IS Jafar's, 2026-09-16: a "
                   "ruling that changes canon edits canon in the same batch.")
        out.append("canon-register: canon.md is the RESIDENT's to edit, with "
                   "dictated text. Report the violation; do not fix it here.")
    out.append(done)
    return (1 if failed else 0), out


def series(canon_path=CANON, register_path=REGISTER):
    """THE PRINTER THE PHRASE LIST CAME FROM. Per-record reading, one line
    each, plus every canon-mentioning line. Read this before touching
    PHRASES; a bound chosen first and defended after is a rounding."""
    recs, why_r = read_records(register_path)
    if recs is None:
        return 2, ["canon-register series: %s - %s" % (NOTHING, why_r)]
    canon, _ = read_canon(canon_path)
    cited = {n for n, _ in canon["cites"]} if canon else set()
    out, mention_n, match_n = [], 0, 0
    for n, r in sorted(recs.items()):
        if r["mentions"]:
            mention_n += 1
        if r["matched"]:
            match_n += 1
        out.append("series D%-3d status=%-11s how=%-16s date=%-10s "
                   "directive=%-9s mentions=%d matched=%s inCanon=%s"
                   % (n, r["status"], r["statusHow"], r["date"] or "none",
                      (r["directive"] or "none").split()[0][:9],
                      len(r["mentions"]),
                      r["matched"][0] if r["matched"] else "none",
                      "yes" if n in cited else "no"))
        for ln, text in r["mentions"][:2]:
            out.append("        D%d:%d %s" % (n, ln, text[:96]))
        if len(r["mentions"]) > 2:
            out.append("        (+%d-more-not-shown)" % (len(r["mentions"]) - 2))
    unread = [n for n, r in recs.items() if r["status"] == "UNREADABLE"]
    out.append("series done: records=%d mentionCanon=%d/%d matchedAPhrase=%d/%d "
               "phrasesInList=%d canonCitationsRaw=%d statusUnreadable=%d/%d"
               % (len(recs), mention_n, len(recs), match_n, mention_n,
                  len(PHRASES), len(canon["cites"]) if canon else 0,
                  len(unread), len(recs)))
    return 0, out


# ----------------------------------------------------------------- selftest

FIX_CANON = """# canon.md

STATUS: APPROVED. A ruling that changes canon edits canon in the same batch.

## Game
- The town is a town (D901, decided 2026-09-01).

## OPEN
1. Something. Nobody has ruled on this (D902).
"""

FIX_REC = {
    "D901-a-decided-world-fact.md":
        "# D901: a decided world fact\n"
        "STATUS: DECIDED 2026-09-01 by Jafar.\nCANON: edits the Game section.\n",
    "D902-an-open-question.md":
        "# D902: an open question\nDate: 2026-09-01. Status: OPEN.\n"
        "CANON: none\n",
}


def _write(d, canon_text, records):
    c = os.path.join(d, "canon.md")
    r = os.path.join(d, "register")
    if not os.path.isdir(r):
        os.makedirs(r)
    open(c, "w", encoding="utf-8").write(canon_text)
    for name in os.listdir(r):
        os.remove(os.path.join(r, name))
    for name, text in records.items():
        open(os.path.join(r, name), "w", encoding="utf-8").write(text)
    return c, r


def selftest():
    ok = fail = 0

    def c(name, cond, detail=""):
        nonlocal ok, fail
        if cond:
            ok += 1
            print("  ok   %s" % name)
        else:
            fail += 1
            print("  FAIL %s %s" % (name, detail))

    print("canon-register-check selftest - accepting case first, and it is "
          "the live tree")
    # ACCEPTING CASE FIRST, AND IT IS THE LIVE TREE. The fixture I cannot
    # fake: the real canon.md against the real register. The expensive
    # failure in this family is a validator nothing survives, so the case
    # that must PASS runs before any case that must fail.
    code, out = check()
    text = "\n".join(out)
    c("ACCEPTING: the live canon passes all three assertions (exit 0)",
      code == 0, "exit %d:\n%s" % (code, text))
    c("ACCEPTING: the done line carries its denominators",
      all(k in text for k in ("recordsWalked=", "canonLines=",
                             "canonCitationsRaw=", "assertionsHeld=",
                             "notExamined=")), text.splitlines()[-1])
    c("ACCEPTING: A3 printed which phrase matched which record",
      "matched=phrase/" in text or "matched=directive/" in text)
    c("ACCEPTING: the unmatched list prints with its denominator",
      "UNMATCHED mentionsCanonButNoPhraseOrDirective=" in text)

    import tempfile
    with tempfile.TemporaryDirectory() as d:
        # ACCEPTING, synthetic: the minimal well-formed shape.
        cp, rp = _write(d, FIX_CANON, FIX_REC)
        code, out = check(cp, rp)
        c("ACCEPTING: a minimal well-formed synthetic tree passes",
          code == 0, "exit %d:\n%s" % (code, "\n".join(out)))

        # REJECTING FIXTURES, every one of them SYNTHETIC: D9xx exists
        # nowhere in the register, so doing the work this tool prompts can
        # never break the tool.
        recs = dict(FIX_REC)
        recs["D903-already-decided.md"] = ("# D903\nSTATUS: DECIDED 2026-09-02 "
                                           "by Jafar.\nCANON: none\n")
        cp, rp = _write(d, FIX_CANON.replace("(D902)", "(D903)"), recs)
        code, out = check(cp, rp)
        c("rejecting: a DECIDED record cited under ## OPEN fails",
          code == 1 and "D903" in "\n".join(out), "exit %d" % code)

        recs = dict(FIX_REC)
        recs["D904-superseded.md"] = ("# D904\n> **SUPERSEDED 2026-09-03 BY "
                                      "D905.**\n")
        recs["D905-the-successor.md"] = ("# D905\nSTATUS: DECIDED 2026-09-03 by "
                                         "Jafar.\nCANON: none\n")
        # THE PAIR IS THE POINT, so the two fixtures differ in ONE thing: the
        # successor beside the citation or not. And the failing one asserts
        # violationsA2=1 rather than "something went red" — the first version
        # of this case passed on an A3 violation the fixture had introduced
        # by accident, which is a guard that cannot name what it caught.
        bare = FIX_CANON.replace("- The town is a town (D901, decided 2026-09-01).",
                                 "- The town is a town (D901, decided 2026-09-01).\n"
                                 "- The pub is a pub (D904).")
        cp, rp = _write(d, bare, recs)
        code, out = check(cp, rp)
        t = "\n".join(out)
        c("rejecting: a superseded record cited without its successor fails",
          code == 1 and "successor-not-in-the-same-block" in t
          and "violationsA2=1" in t and "violationsA3=0" in t,
          "exit %d:\n%s" % (code, t))

        # And the same pair PASSES when the successor is beside it: a guard
        # that cannot tell a regression from an improvement is a ratchet.
        beside = bare.replace("(D904).", "(D904, superseded by D905).")
        cp, rp = _write(d, beside, recs)
        code, out = check(cp, rp)
        c("ACCEPTING: the same citation passes with the successor beside it",
          code == 0, "exit %d:\n%s" % (code, "\n".join(out)))

        recs = dict(FIX_REC)
        recs["D906-names-canon.md"] = ("# D906\nSTATUS: DECIDED 2026-09-04 by "
                                       "Jafar.\nCANON: edits the Game section.\n")
        cp, rp = _write(d, FIX_CANON, recs)
        code, out = check(cp, rp)
        c("rejecting: a record whose CANON: line says edits, absent from canon",
          code == 1 and "record-names-canon-but-canon-does-not-cite-it"
          in "\n".join(out), "exit %d" % code)

        # The phrase path, on a record older than the forward date.
        recs = dict(FIX_REC)
        recs["D907-old-phrasing.md"] = ("# D907\nSTATUS: DECIDED 2026-09-05 by "
                                        "Jafar.\nRecorded **in canon beside the "
                                        "pillars**.\n")
        cp, rp = _write(d, FIX_CANON, recs)
        code, out = check(cp, rp)
        c("rejecting: the phrase path catches a pre-forward-date record too",
          code == 1 and "phrase/recorded-in-canon" in "\n".join(out),
          "exit %d:\n%s" % (code, "\n".join(out)))

        # THE WEAK LINK, PROVED WEAK ON PURPOSE: new words, no directive.
        recs = dict(FIX_REC)
        recs["D908-new-words.md"] = ("# D908\nSTATUS: DECIDED 2026-09-05 by "
                                     "Jafar.\nThis one belongs in the world "
                                     "bible, obviously.\nIt mentions canon "
                                     "nowhere the list can read.\n")
        cp, rp = _write(d, FIX_CANON, recs)
        code, out = check(cp, rp)
        t = "\n".join(out)
        c("ACCEPTING: a record saying it in new words does not fail the gate",
          code == 0, "exit %d:\n%s" % (code, t))
        c("rejecting: but it is PRINTED as unmatched, not silently passed",
          "D908" in t and "UNMATCHED" in t, t)

        # THE FORWARD FIX HAS TEETH.
        recs = dict(FIX_REC)
        recs["D909-after-the-ruling.md"] = ("# D909\nSTATUS: DECIDED 2026-09-20 "
                                            "by Jafar.\nNo directive here.\n")
        cp, rp = _write(d, FIX_CANON, recs)
        code, out = check(cp, rp)
        c("rejecting: a record dated after the ruling with no CANON: line fails",
          code == 1 and "no-CANON:-line" in "\n".join(out), "exit %d" % code)

        # NOTHING MEASURED IS NOT CLEAN, both halves.
        code, out = check(os.path.join(d, "gone.md"), rp)
        c("rejecting: a missing canon.md is exit 2 and says nothing measured",
          code == 2 and NOTHING in "\n".join(out), "exit %d" % code)
        code, out = check(cp, os.path.join(d, "no-register"))
        c("rejecting: a missing register is exit 2, never a pass",
          code == 2 and NOTHING in "\n".join(out), "exit %d" % code)

        # THE CAP ANNOUNCES WHEN IT BITES.
        c("the cap says how much it hid",
          cap([str(i) for i in range(20)], n=3) == "0,1,2,(+17-more-not-shown)",
          cap([str(i) for i in range(20)], n=3))
        c("and an empty list reads as none, not as a silent blank",
          cap([]) == "none")

        # THE SERIES PRINTER RUNS, because a printer nobody runs is a comment.
        code, out = series()
        c("ACCEPTING: --series prints a reading per record with its totals",
          code == 0 and "series done: records=" in "\n".join(out), "exit %d" % code)

    print("canon-register-check selftest: %d passed, %d failed" % (ok, fail))
    return 3 if fail else 0


if __name__ == "__main__":
    # FAIL READABLE: `--series | head -20` is how anybody will read this, and
    # a correct run ending in a BrokenPipeError costs twenty minutes before
    # somebody notices it worked.
    try:
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (ImportError, AttributeError, ValueError):
        pass
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if "--series" in sys.argv:
        code, out = series()
    else:
        code, out = check()
    for line in out:
        print(line)
    sys.exit(code)
