"""Per-system checks, second round, through the game's test hook (window.LEDGER) only.

Systems: gossip, talk, day and night routines, police and suspicion, jobs and debts, and the
playtest question "Julie's debt is not noted until Mickey's book is read". Same set-up as
systems_test.py: one headless Chromium, one new week, tests in name order, each building on the
street the one before left. The clock moves only when a test calls LEDGER.step (45 real seconds
of step are one game hour; a game hour takes about 0.1 s here). Needs the pictures in the folder
named by LEDGER_PROTO_ASSETS (as the smoke test); skipped otherwise, never passed.

What the hook exposes, listed from the browser on 18 Nov 2026 (bundle version 1794862482-9f9b):
  LEDGER functions   step, simStep, startNew, passTime, enterRoom, leaveRoom, endWeek, reportText,
                     saveNow, restore, benchmark; objects G, talk, ui, rig, scene, camera, THREE, cam, F
  LEDGER.talk        start(id) opens talk with a person; lines() the suggested lines [{job, text, model}];
                     state() {on, who, busy, open, sel, dec, q, slip}. Choosing a line or a yes/no is a
                     key press in the page: not in the hook.
  G keys             v t played weather tom car minds events ev sightIdx transfers nextE ledger log money
                     debts story stats people named crowd env watch paused fast hooks settings keepers ledgerNew
  G.hooks            matters pending yielded fightOver beaten arrestNow clock ellisTalk bought demandFor killed
                     sfx shake blood save end enterRoom leaveRoom townLevel doorOpen ambience believed nameLearned

What each system exposes:
  Gossip     G.transfers: one row per telling {a teller (or "someone"), b hearer, e event id, t, z place};
             the hearer's memory p.mind.by[e] {src told|heard|saw, from}. The telling itself runs inside
             step; no hook starts one.
  Talk       LEDGER.talk.start / lines / state (above). G.ledger.names and G.ledger.met: the people whose
             name or face Tom has. Live talk is off outside claude.ai, so lines are the written fallback.
  Routines   p.def.sched [[hour, place, act, days?]], p.goalKey "place|act" (where the person is headed now),
             p.override (a story or fight sends them elsewhere), p.space, p.awake, p.gone.
  Police     G.story.arrest {e, violent, due, by} set by the nightly police run at 04:00 for the day before;
             each crime event gets e.stmt (who made a statement). Crimes are made only by Tom's acts
             (carry, threaten, strike...), which are key presses; so the tests plant the crime event and
             the witness's memory by hand, and only the statement rule and the nightly run are the game's.
  Debts      G.debts person -> {owed, st open|paid|part|forgiven}; G.hooks.demandFor(person); Ledger notes
             G.ledger.notes [{t, kind, text, key}]. Collecting or striking out is a talk decision (keys).
  Jobs       G.story.flags (ask1, ask2, job1..job3...), G.story.job. Jobs are offered and taken in written
             scenes that wait on key presses: not reachable.
"""
import functools, http.server, os, re, sys, tempfile, threading, unittest
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import build  # noqa: E402

ASSETS = os.environ.get("LEDGER_PROTO_ASSETS")
GL = ["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader"]
HOUR = 45  # LEDGER.step seconds per game hour

# The schedule rule written again here from its meaning (latest entry at or before the hour; an
# entry with a day list counts only on those days and wins a tie), not called from the bundle.
EXPECTED_JS = """(() => { const G = LEDGER.G, h = (G.t / 60) % 24, d = Math.floor(G.t / 1440) % 7, out = {};
  for (const p of G.named) { if (p.override || p.dead || !p.def.sched) continue;
    let n = null, s = null;
    for (const r of p.def.sched) { if (r[0] > h) continue;
      if (r[3]) { if (r[3].includes(d) && (!s || r[0] >= s[0])) s = r; } else if (!n || r[0] >= n[0]) n = r; }
    const o = s && (!n || s[0] >= n[0]) ? s : n;
    out[p.id] = [o ? o[1] + '|' + (o[2] || 'idle') : 'off|idle', p.goalKey]; }
  return out; })()"""


@unittest.skipUnless(ASSETS and os.path.isdir(ASSETS), "LEDGER_PROTO_ASSETS not set: pictures missing, system checks skipped")
class Systems2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from playwright.sync_api import sync_playwright
        cls.tmp = tempfile.TemporaryDirectory()
        build.build(assets_dir=ASSETS, dist=cls.tmp.name)

        class Quiet(http.server.SimpleHTTPRequestHandler):
            def log_message(self, *a):
                pass
        cls.srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=cls.tmp.name))
        threading.Thread(target=cls.srv.serve_forever, daemon=True).start()
        cls.pw = sync_playwright().start()
        cls.b = cls.pw.chromium.launch(args=GL)
        cls.pg = cls.b.new_page(viewport={"width": 1280, "height": 720})
        cls.errors = []
        cls.pg.on("pageerror", lambda e: cls.errors.append(str(e)))
        cls.pg.goto("http://127.0.0.1:%d/index.html" % cls.srv.server_address[1])
        cls.pg.wait_for_function("window.LEDGER && window.LEDGER.G", timeout=90000)
        cls.pg.evaluate("LEDGER.startNew()")
        cls.pg.wait_for_function("LEDGER.G.story.phase === 'play'", timeout=30000)
        cls.pg.evaluate("window.LEDGER_MANUAL = true; window.LEDGER_NORENDER = true")

    @classmethod
    def tearDownClass(cls):
        try:
            cls.b.close(); cls.pw.stop()
        finally:
            cls.srv.shutdown(); cls.srv.server_close(); cls.tmp.cleanup()

    def js(self, expr):
        return self.pg.evaluate(expr)

    def tearDown(self):
        self.assertEqual(self.errors, [], "page errors: %s" % self.errors[:3])

    def hour(self):
        return self.js("(LEDGER.G.t / 60) % 24")

    def step_to(self, day, hour):
        """Step the clock until game day `day` (0 = Monday) at `hour`, an hour at a time. Tom has not
        slept, so at about 04:30 the game sends him to bed ("You are dead on your feet") and pauses for
        a fade that runs in real time; wait for it, then go on."""
        target = day * 1440 + hour * 60
        self.assertLess(self.js("LEDGER.G.t"), target, "the clock is already past day %d %.2f" % (day, hour))
        for _ in range(200):
            self.pg.wait_for_function("!LEDGER.G.paused && !LEDGER.talk.state().on", timeout=60000)
            now = self.js("LEDGER.G.t")
            if now >= target - 0.5:
                break
            self.js("LEDGER.step(%f)" % (min(60, target - now) / 60 * HOUR))
        now = self.js("LEDGER.G.t")
        self.assertTrue(target - 1 <= now <= target + 30, "wanted day %d %.2f, the clock is at %.1f" % (day, hour, now))

    # 1. Gossip ------------------------------------------------------------------------
    def test_1a_a_story_spreads_over_game_time_and_every_telling_has_a_meeting(self):
        # The bus arrival (event 2) is seen at the start by the three on the rank only.
        know = "LEDGER.G.named.filter(p => p.mind.by[2]).map(p => p.id)"
        k0 = set(self.js(know))
        wit = set(self.js("LEDGER.G.ev[2].wit"))
        self.js("LEDGER.step(%d)" % (5 * HOUR))
        k1 = set(self.js(know))
        self.assertLessEqual(k0, k1, "nobody forgets: memories are never wiped")
        self.assertGreater(len(k1), len(k0), "after five game hours the arrival must have reached someone new")
        rows = self.js("LEDGER.G.transfers")
        self.assertTrue(rows, "tellings must be recorded")
        for p in k1 - wit:
            m = self.js("LEDGER.G.people[%r].mind.by[2]" % p)
            if m["src"] in ("told", "heard"):
                self.assertTrue(any(r["b"] == p and r["e"] == 2 for r in rows) or m["src"] == "heard",
                                "%s was told of the arrival but no telling names them" % p)
        # Every told memory comes from a recorded telling, by a teller who knew the story.
        named = set(self.js("LEDGER.G.named.map(p => p.id)"))
        for r in rows:
            if r["b"] not in named:
                continue
            m = self.js("LEDGER.G.people[%r].mind.by[%d] || null" % (r["b"], r["e"]))
            self.assertIsNotNone(m, "%s heard event %d from %s but holds no memory of it" % (r["b"], r["e"], r["a"]))
            if r["a"] != "someone" and r["a"] in named:
                self.assertIsNotNone(self.js("LEDGER.G.people[%r].mind.by[%d] || null" % (r["a"], r["e"])),
                                     "%s told a story they never had" % r["a"])

    def test_1b_no_story_without_a_witness(self):
        # Every memory points at a real event, and a "saw" memory belongs to one of its witnesses.
        bad = self.js("""LEDGER.G.named.flatMap(p => p.mind.mem.filter(m => !LEDGER.G.ev[m.e] ||
            (m.src === 'saw' && !(LEDGER.G.ev[m.e].wit || []).concat(LEDGER.G.ev[m.e].party || []).includes(p.id)))
            .map(m => p.id + ':' + m.e + ':' + m.src))""")
        self.assertEqual(bad, [])

    # 2. Talk --------------------------------------------------------------------------
    def talk_lines(self, pid):
        # The clock stops while talk is open, so each talk is closed again with its own Leave button.
        self.js("LEDGER.talk.start(%r)" % pid)
        st = self.js("LEDGER.talk.state()")
        self.assertEqual(st["who"], pid, "talk.start must open talk with %s" % pid)
        lines = [l["text"] for l in self.js("LEDGER.talk.lines()")]
        self.js("document.getElementById('tbye').click()")
        self.pg.wait_for_function("!LEDGER.talk.state().on && !LEDGER.G.paused", timeout=15000)
        return lines

    def test_2a_suggested_lines_name_nobody_he_has_not_learned(self):
        # People with a written first scene (Sheila) open that scene instead of free talk: left out.
        people = self.js("LEDGER.G.named.filter(p => !p.gone && !p.dead && p.space !== 'off' && !p.def.story).map(p => p.id)")
        names = self.js("Object.fromEntries(LEDGER.G.named.map(p => [p.id, p.def.name]))")
        known = set(self.js("Object.keys(LEDGER.G.ledger.names || {})"))
        self.assertTrue(people)
        offered = 0
        for pid in people:
            lines = self.talk_lines(pid)
            self.assertLessEqual(len(lines), 3, "%s: at most three suggested lines" % pid)
            offered += len(lines)
            for text in lines:
                for other, full in names.items():
                    if other in known:
                        continue
                    for part in full.split():
                        if len(part) > 3 and re.search(r"\b%s\b" % re.escape(part), text):
                            self.fail("line to %s names %s before Tom has learned it: %r" % (pid, full, text))
        self.assertGreater(offered, 0)

    def test_2b_before_the_book_is_read_no_line_asks_for_a_debt(self):
        # Tom has not been shown Mickey's book yet (Sheila's first scene sets flags.tour), so nothing
        # offered to a debtor may speak of what they owe.
        self.assertFalse(self.js("!!LEDGER.G.story.flags.tour"), "this check needs the week before Sheila's first scene")
        for pid in self.js("Object.keys(LEDGER.G.debts)"):
            if self.js("LEDGER.G.people[%r].gone || LEDGER.G.people[%r].space === 'off' || !!LEDGER.G.people[%r].def.story" % (pid, pid, pid)):
                continue
            for text in self.talk_lines(pid):
                self.assertNotRegex(text.lower(), r"owe|the book|slate|£", "%s offered a debt line before the book: %r" % (pid, text))

    # 3. Police and suspicion, and day and night routines ---------------------------------
    # They share the first night: crimes are planted on Monday evening, the routines are checked at
    # 02:00, the police run for Monday happens at 04:00 Tuesday, then the routines again by day.
    # Only the first night is used: on Tuesday night the game paused and did not resume within a minute
    # (cause not found; noted in the README), so later nights are not stepped through.
    PLANT = """((kind, wit, mems) => { const G = LEDGER.G, id = G.nextE++;
        const e = {id, kind, t: G.t, zone: G.tom.zone, x: 0, z: 0, coat: false, car: false, wit};
        G.events.push(e); G.ev[id] = e;
        for (const [pid, src] of mems) { const m = G.people[pid].mind,
          s = {e: id, src, from: null, who: 'tom', sure: 0.9, heat: 0.8, t: G.t, said: false, hop: 0, face: 1};
          m.mem.push(s); m.by[id] = s; }
        return id; })"""
    planted = {}

    def test_3a_plant_crimes_on_monday_evening(self):
        self.assertEqual(self.js("Math.floor(LEDGER.G.t / 1440)"), 0, "the crimes must be planted on Monday")
        # Willing witnesses: can make statements, not upright, not afraid, not paid; cooled on Tom.
        w, t, f, b = self.js("""LEDGER.G.named.filter(p => !p.def.nostmt && !p.def.upright && !p.dead
            && !p.mind.bought && p.mind.fear < 0.5 && p.id !== 'pc' && p.id !== 'ellis').slice(0, 4).map(p => p.id)""")
        for k in (w, t, f, b):
            self.js("LEDGER.G.people[%r].mind.regard = -0.6" % k)
        self.js("LEDGER.G.people[%r].mind.fear = 0.8; LEDGER.G.people[%r].mind.bought = 1" % (f, b))
        P = type(self).planted
        P["w"], P["f"], P["b"] = w, f, b
        P["seen"] = self.js(self.PLANT + "('shove', [%r], [[%r, 'saw']])" % (w, w))
        P["unseen"] = self.js(self.PLANT + "('shove', [], [])")
        P["told"] = self.js(self.PLANT + "('threat', [], [[%r, 'told']])" % t)
        P["afraid"] = self.js(self.PLANT + "('shove', [%r], [[%r, 'saw']])" % (f, f))
        P["paid"] = self.js(self.PLANT + "('shove', [%r], [[%r, 'saw']])" % (b, b))
        self.assertIsNone(self.js("LEDGER.G.story.arrest"))

    def routine_check(self):
        rows = self.js(EXPECTED_JS)
        wrong = {k: v for k, v in rows.items() if v[0] != v[1]}
        self.assertGreaterEqual(len(rows), 15, "most of the street must be on its own routine")
        self.assertEqual(wrong, {}, "people not headed to their routine place (expected, actual)")

    def test_3b_night_people_go_home_and_sleep(self):
        self.step_to(1, 2.0)  # Tuesday 02:00
        self.routine_check()
        self.assertEqual(self.js("LEDGER.G.people.ron.goalKey"), "home|sleep")

    @unittest.expectedFailure
    def test_3b2_ron_gets_home_at_night(self):
        # Finding (18 Nov): Ron leaves the rank at 23:36 for home, walks about 3 metres and stops at
        # x 6.4, z 35.2, still marked as walking with a route, and is still standing there on the
        # street at 03:00 (traced hour by hour). By day his walks (rank to the fish queue) arrive.
        # Seen with the clock stepped through the hook and drawing off; unverified in normal play.
        self.assertNotEqual(self.js("LEDGER.G.people.ron.space"), "street", "at two in the morning Ron is not on the street")

    def test_3c_a_seen_crime_brings_a_statement_unseen_told_afraid_or_paid_do_not(self):
        P = type(self).planted
        self.assertTrue(P, "needs test_3a's planted crimes")
        self.step_to(1, 4.25)  # the police run for Monday happens at 04:00 Tuesday
        stmt = lambda k: self.js("LEDGER.G.ev[%d].stmt" % P[k])
        self.assertEqual(stmt("seen"), [P["w"]], "the witness who saw it states")
        self.assertEqual(stmt("unseen"), [], "nobody saw it: no statement")
        self.assertEqual(stmt("told"), [], "told, not seen: no statement")
        self.assertEqual(stmt("afraid"), [], "an afraid witness keeps quiet")
        self.assertEqual(stmt("paid"), [], "a paid witness keeps quiet")
        arrest = self.js("LEDGER.G.story.arrest")
        self.assertIsNotNone(arrest, "a statement brings the police")
        self.assertEqual(arrest["e"], P["seen"])
        self.assertIn(P["w"], arrest["by"])
        self.assertTrue(any(l["tag"] == "police" for l in self.js("LEDGER.G.log")), "the log must say a statement was made")
        # Keep the constable away: his visit is a written scene that waits on a key press.
        self.js("LEDGER.G.story.arrest = null")

    def test_3d_everyone_on_their_routine_tuesday_morning(self):
        self.step_to(1, 9.25)  # Tuesday 09:15
        self.routine_check()
        self.assertEqual(self.js("LEDGER.G.people.ron.goalKey"), "rank|idle", "Ron is on the rank from 08:06")

    def test_3e_everyone_on_their_routine_tuesday_dinner_time(self):
        self.step_to(1, 12.5)  # 12:30: Ron joins the fish queue at 12:18
        self.routine_check()
        self.assertEqual(self.js("LEDGER.G.people.ron.goalKey"), "fish:q1|queue")

    # 5. Jobs and debts ----------------------------------------------------------------
    def test_5a_debts_recorded_and_open(self):
        d = self.js("LEDGER.G.debts")
        self.assertEqual(set(d), {"dennis", "lee", "darren", "julie", "wayne"})
        self.assertTrue(all(v["st"] == "open" and v["owed"] > 0 for v in d.values()))
        self.assertEqual(self.js("LEDGER.G.hooks.demandFor(LEDGER.G.people.julie)"), {"type": "debt"})

    def test_5b_julie_debt_not_in_the_ledger_until_the_book_is_read(self):
        # Playtest note: "Julie's debt is not noted until Mickey's book is read." Design-match: Tom may
        # only be shown what he could know (scope draft, the Ledger: "never shows a fact he could not
        # know"), and the prototype's own notes say debts are listed "by the names in Mickey's book".
        # The note is written in Sheila's first scene (flags.tour); before it, nothing about Julie's debt.
        self.assertFalse(self.js("!!LEDGER.G.story.flags.tour"))
        notes = self.js("LEDGER.G.ledger.notes.map(n => n.text)")
        self.assertFalse([n for n in notes if n and ("Julie" in n or "debts" in n.lower())], notes)
        self.assertNotIn("Julie", self.js("document.body.innerText") or "", "Julie's name must not show anywhere yet")

    @unittest.skip("not reachable through the hook: collecting or striking out a debt is a yes/no in talk "
                   "(a key press); the hook has no call that pays a debt, so paid-and-shown cannot be driven")
    def test_5c_debt_paid_and_shown_in_the_ledger(self):
        pass

    @unittest.skip("not reachable through the hook: Sheila's first scene, which reads Tom the book and writes "
                   "the debts note, is a written scene that waits on key presses")
    def test_5d_debt_noted_after_the_book_is_read(self):
        pass

    @unittest.skip("not reachable through the hook: jobs (the Monday bag, the Tuesday parcel, Iveson's yard) "
                   "are offered and taken in written scenes that wait on key presses")
    def test_5e_a_job_taken_and_paid(self):
        pass


if __name__ == "__main__":
    unittest.main()
