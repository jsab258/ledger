"""Per-system checks (stage 2, first four), through the game's test hook (window.LEDGER) only.

Order as in the scope draft: seeing and naming, the Ledger, money and the tin, saving.
One headless Chromium and one new week for the whole class; the tests run in name order
and each builds on the street as the one before left it. Needs the pictures in the folder
named by LEDGER_PROTO_ASSETS (as the smoke test); skipped otherwise, never passed.

Field meanings, read from the bundle (src/bundle/) on 18 Nov 2026:
  G.events / G.ev   every act of Tom's the town could know of: {id, kind, t, zone, wit:[ids who saw]}; ev indexes by id
  G.sightIdx        "kind:day:two-hour block:zone" -> event id, so one sighting kind is one event per block, however many see it
  G.minds / p.mind  each person's memory: mem[] and by[event id] = {src saw|told|heard|self, who man|coat|cab|owner|tom, sure, heat}, fam (how well they know his face)
  G.named           the named people (person objects); what each calls him climbs with what they know of him
  G.ledger          what Tom believes: acts[{e, seen:{person: how}}], notes, calls, met, names
  G.money           pennies: clean = pocket, dirty = the tin; fares, fareCount, earnedClean, earnedDirty, washed, sinceWash, booksOff, spent
  G.debts           Mickey's book: person -> {owed (pennies), st open|paid|part|forgiven}
"""
import json, os, re, sys, tempfile, threading, functools, http.server, unittest
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import build  # noqa: E402

ASSETS = os.environ.get("LEDGER_PROTO_ASSETS")
GL = ["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader"]
SAVE_KEY = "ledger.save.v4"
GOSSIP = "(r => r.split('\\n'))(LEDGER.reportText())"


def report_line(lines, prefix):
    for ln in lines:
        if ln.startswith(prefix):
            return ln
    raise AssertionError("report has no line starting %r" % prefix)


@unittest.skipUnless(ASSETS and os.path.isdir(ASSETS), "LEDGER_PROTO_ASSETS not set: pictures missing, system checks skipped")
class Systems(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from playwright.sync_api import sync_playwright
        cls.tmp = tempfile.TemporaryDirectory()
        build.build(assets_dir=ASSETS, dist=cls.tmp.name)
        with open(os.path.join(cls.tmp.name, "ledger.js"), encoding="utf-8") as f:
            # The fare places table, found by the shape of its data ({station:{n:"...",p:[x,z]},...}),
            # not by the bundler's short names, which change on any rebuild.
            m = re.search(r'=(\{station:\{n:"[^"]*",p:\[[^\]]*\]\}(?:,\w+:\{n:"[^"]*",p:\[[^\]]*\]\})*\})[;,]', f.read())
        cls.fare_places_js = m.group(1) if m else None

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
        # From here the clock moves only when a test calls LEDGER.step (the page's own switches).
        cls.pg.evaluate("window.LEDGER_MANUAL = true; window.LEDGER_NORENDER = true")
        cls.start_report = cls.pg.evaluate(GOSSIP)
        cls.start_arrival = cls.pg.evaluate("Object.fromEntries(['ron', 'darren', 'kevin'].map(k => [k, LEDGER.G.people[k].mind.by[2] && LEDGER.G.people[k].mind.by[2].who]))")

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

    # 1. Seeing and naming -------------------------------------------------------------
    def test_1a_witnessed_act_is_recorded_with_its_witnesses(self):
        # Wearing Mickey's coat in daylight on the street is a sighting kind (coat_day).
        self.assertEqual(self.js("LEDGER.G.tom.space"), "street")
        before = self.js("LEDGER.G.events.length")
        self.js("LEDGER.G.tom.coat = true; LEDGER.step(20)")
        new = self.js("LEDGER.G.events.slice(%d).filter(e => e.kind === 'coat_day')" % before)
        self.assertTrue(new, "a coat in daylight in front of people must make a coat_day event")
        named = set(self.js("LEDGER.G.named.map(p => p.id)"))
        for e in new:
            wit = [w for w in e["wit"] if w in named]
            self.assertTrue(wit, "event %d must have named witnesses, has %s" % (e["id"], e["wit"]))
            for w in wit:
                mem = self.js("LEDGER.G.people[%r].mind.by[%d] || null" % (w, e["id"]))
                self.assertIsNotNone(mem, "%s is a witness of %d but has no memory of it" % (w, e["id"]))
                self.assertEqual(mem["src"], "saw")
            # Sheila is at her desk inside Mickey's: she cannot have seen it.
            self.assertNotIn("sheila", e["wit"])
            self.assertIsNone(self.js("LEDGER.G.people.sheila.mind.by[%d] || null" % e["id"]))
        # One event per sighting kind and two-hour block, however many people saw it.
        idx = self.js("Object.entries(LEDGER.G.sightIdx).filter(([k]) => k.startsWith('coat_day:'))")
        ids = sorted(v for _, v in idx)
        all_coat = sorted(self.js("LEDGER.G.events.filter(e => e.kind === 'coat_day').map(e => e.id)"))
        self.assertEqual(ids, all_coat, "every coat_day event must be the one sightIdx names for its block")
        self.assertTrue(any(l["tag"] == "saw" for l in self.js("LEDGER.G.log")), "the log must say who saw")

    def test_1b_no_coat_no_new_sighting(self):
        self.js("LEDGER.G.tom.coat = false")
        n = self.js("LEDGER.G.events.filter(e => e.kind === 'coat_day').length")
        self.js("LEDGER.step(20)")
        self.assertEqual(self.js("LEDGER.G.events.filter(e => e.kind === 'coat_day').length"), n)

    def test_1c_the_street_learns_a_name(self):
        # At the start: the street knows only that Mickey's nephew inherited ("the new owner"), and
        # the three on the rank saw Tom get off the bus as a stranger ("man").
        start = self.start_report
        self.assertIn("Street calls him: the new owner.", report_line(start, "Ended "))
        for name in ("Ron Kirby", "Darren Milner", "Kevin Needham", "Brenda Laverack"):
            self.assertTrue(any(l.startswith("- %s: the new owner (" % name) for l in start), name)
        self.assertEqual(self.start_arrival, {"ron": "man", "darren": "man", "kevin": "man"})
        # The coat sightings (1a) put Tom's face to the rank: each witness now calls him more than
        # "the new owner" and has linked the stranger off the bus to him.
        lines = self.js(GOSSIP)
        for k, name in (("ron", "Ron Kirby"), ("darren", "Darren Milner"), ("kevin", "Kevin Needham")):
            row = [l for l in lines if l.startswith("- %s: " % name)][0]
            self.assertNotIn(": the new owner (", row, "%s saw his face and must call him more" % name)
            mem = self.js("LEDGER.G.people[%r].mind.by[2]" % k)
            self.assertIn(mem["who"], ("owner", "tom"), "%s must put the arrival to Tom now" % name)
            self.assertEqual(mem.get("linked"), 1)
        # Brenda saw nothing: no change for her, and three men on the rank are not the street.
        self.assertTrue(any(l.startswith("- Brenda Laverack: the new owner (") for l in lines))
        self.assertIn("Street calls him: the new owner.", report_line(lines, "Ended "), "three men are not the street")
        # Threshold check only: face familiarity is forced to 0.9 for everyone (no play makes it), to
        # show the street's own name climbs once most of it knows his face; restored afterwards.
        fams = self.js("LEDGER.G.named.map(p => p.mind.fam)")
        self.js("LEDGER.G.named.forEach(p => { p.mind.fam = Math.max(p.mind.fam, 0.9) })")
        street = report_line(self.js(GOSSIP), "Ended ")
        self.js("LEDGER.G.named.forEach((p, i) => { p.mind.fam = %s[i] })" % json.dumps(fams))
        self.assertNotIn("Street calls him: the new owner.", street)

    # 2. The Ledger --------------------------------------------------------------------
    def counts(self):
        m = re.search(r"Known (\d+), Ledger right (\d+), missed (\d+)\.", self.js("LEDGER.reportText()"))
        self.assertIsNotNone(m, "report must carry the Known / right / missed counts")
        return tuple(int(x) for x in m.groups())

    # Recomputed here from the minds and the Ledger, the way the report states it: the inheritance
    # left out; one row per kind of act, day (from 05:00) and target; a person counted once per row
    # if they saw it or were told it and put Tom to it; right if the Ledger has them for that row.
    TRUTH_JS = """(() => { const G = LEDGER.G, rows = new Map();
      for (const e of G.events) { if (e.kind === 'inherit') continue;
        const key = e.kind + ':' + Math.floor((e.t - 300) / 1440) + ':' + (e.target || '');
        if (!rows.has(key)) rows.set(key, {knew: new Set(), led: new Set()});
        const r = rows.get(key), acts = G.ledger.acts.find(a => a.e === e.id);
        if (acts) Object.keys(acts.seen).forEach(k => k !== 'anon' && r.led.add(k));
        for (const p of G.named) { const m = p.mind.by[e.id];
          if (m && (m.who === 'tom' || m.who === 'owner')) r.knew.add(p.id); } }
      let known = 0, right = 0;
      for (const r of rows.values()) { known += r.knew.size; for (const k of r.knew) if (r.led.has(k)) right++; }
      return [known, right, known - right]; })()"""

    def test_2a_report_counts_match_the_truth(self):
        known, right, missed = self.counts()
        self.assertGreater(known, 0, "by now people on the street know things about him")
        self.assertEqual([known, right, missed], self.js(self.TRUTH_JS))

    def test_2a_hand_counted_rank(self):
        # Counted by hand from the opening, not by the report's rule: Ron, Darren and Kevin on the rank
        # saw the bus (put to Tom in 1c) and saw the coat (1a), and Tom saw each of them looking.
        # That is 3 + 3 = 6 known and 6 right at least; gossip since can only add.
        lines = self.js(GOSSIP)
        rank = {"Ron Kirby", "Darren Milner", "Kevin Needham"}
        for start in ("- Tom got off the bus", "- Tom wore the runner's coat"):
            row = [l for l in lines if l.startswith(start)]
            self.assertTrue(row, "report has no row for %r" % start)
            saw = set(row[0].split("| saw: ")[1].split(" |")[0].split(", "))
            led = set(row[0].split("ledger believed: ")[1].split(", "))
            self.assertLessEqual(rank, saw, "%s: the rank must be listed as having seen it" % start)
            self.assertLessEqual(rank, led, "%s: Tom must believe the rank saw it" % start)
        known, right, missed = self.counts()
        self.assertGreaterEqual(known, 6)
        self.assertGreaterEqual(right, 6)

    def test_2b_tom_only_believes_seen_by_people_who_saw(self):
        for a in self.js("LEDGER.G.ledger.acts"):
            wit = set(self.js("(LEDGER.G.ev[%d].wit || []).concat(LEDGER.G.ev[%d].party || [])" % (a["e"], a["e"])))
            for who, how in a["seen"].items():
                if how["b"] == "saw" and who != "anon":
                    self.assertIn(who, wit, "Ledger says %s saw event %d but they are not a witness" % (who, a["e"]))

    def test_2c_gossip_he_did_not_see_is_missed(self):
        known, right, missed = self.counts()
        e = self.js("(LEDGER.G.events.find(e => e.kind === 'coat_day') || {}).id || null")
        self.assertIsNotNone(e, "no coat_day event: this check needs test_1a's coat sighting to have happened first")
        self.assertIsNone(self.js("LEDGER.G.people.brenda.mind.by[%d] || null" % e))
        # Brenda is told about the coat behind his back (as gossip does), so Tom cannot know she knows.
        self.js("""(() => { const m = LEDGER.G.people.brenda.mind, s = {e: %d, src: 'told', from: 'ron', who: 'tom', sure: 0.7,
          heat: 0.6, t: LEDGER.G.t, said: false, hop: 1, face: 0}; m.mem.push(s); m.by[%d] = s; })()""" % (e, e))
        self.assertEqual(self.counts(), (known + 1, right, missed + 1))
        row = [l for l in self.js(GOSSIP) if l.startswith("- Tom wore the runner's coat")][0]
        self.assertIn("told: Brenda Laverack", row)
        self.assertNotIn("Brenda", row.split("ledger believed:")[1])

    # 3. Money and the tin -------------------------------------------------------------
    def test_3a_a_fare_goes_in_the_pocket_not_the_tin(self):
        self.assertIsNotNone(self.fare_places_js,
            "fare places table ({station:{n:..., p:[x, z]}, ...}) not found in the built script: the bundle "
            "was rebuilt or reshaped; update the search in setUpClass, or expose the table on LEDGER")
        self.assertTrue(7 <= self.js("(LEDGER.G.t / 60) % 24") < 23, "fares are offered from 7 to 23 only")
        m0 = self.js("Object.assign({}, LEDGER.G.money)")
        # Pauline's radio offers a fare once he sits in the cab with the keys.
        # The radio picks a random pickup and drop and drops the pair when they are too close: try a few.
        self.js("LEDGER.G.tom.coat = false; LEDGER.G.car.keys = true; LEDGER.G.tom.inCar = true")
        fare = None
        for _ in range(40):
            self.js("LEDGER.G.story.fareCool = 0; LEDGER.step(0.1)")
            fare = self.js("LEDGER.G.story.fare")
            if fare:
                break
        self.assertIsNotNone(fare, "a fare must be offered on the radio")
        self.assertEqual(fare["st"], "offer")
        self.assertGreater(fare["pay"], 0)
        # Taking it (key Y) and picking up are UI steps: put the passenger in and the cab at the drop.
        self.js("""(() => { const F = %s, f = LEDGER.G.story.fare, c = LEDGER.G.car;
          f.st = 'carry'; f.pid = 'pax0'; c.x = F[f.dest].p[0]; c.z = F[f.dest].p[1]; c.v = 0; })()""" % self.fare_places_js)
        self.js("LEDGER.step(0.5)")
        self.assertIsNone(self.js("LEDGER.G.story.fare"), "the fare must end at the drop")
        m1 = self.js("Object.assign({}, LEDGER.G.money)")
        self.js("LEDGER.G.tom.inCar = false")
        pay = fare["pay"]
        self.assertEqual(m1["clean"], m0["clean"] + pay, "the fare goes in his pocket")
        self.assertEqual(m1["dirty"], m0["dirty"], "a fare never goes in the tin")
        self.assertEqual(m1["fares"], m0["fares"] + pay)
        self.assertEqual(m1["fareCount"], m0["fareCount"] + 1)
        self.assertEqual(m1["earnedClean"], m0["earnedClean"] + pay)
        self.assertEqual(m1["sinceWash"], m0["sinceWash"] + pay, "fares are what the book can hide washed money behind")
        money = report_line(self.js(GOSSIP), "Money: ")
        self.assertIn("(%d fares)" % m1["fareCount"], money)
        self.assertIn("pocket £%.2f" % (m1["clean"] / 100), money)

    def test_3b_report_shows_the_tin_apart_from_the_pocket(self):
        m = self.js("Object.assign({}, LEDGER.G.money)")
        self.js("LEDGER.G.money.dirty = 6000")
        money = report_line(self.js(GOSSIP), "Money: ")
        self.js("LEDGER.G.money.dirty = %d" % m["dirty"])
        self.assertIn("tin £60.00", money)
        self.assertIn("pocket £%.2f" % (m["clean"] / 100), money)

    def test_3c_open_debts_can_be_demanded_settled_ones_cannot(self):
        d = self.js("LEDGER.G.debts")
        self.assertEqual({k: v["owed"] for k, v in d.items()},
                         {"dennis": 8000, "lee": 1500, "darren": 2200, "julie": 900, "wayne": 3000})
        self.assertEqual(self.js("LEDGER.G.hooks.demandFor(LEDGER.G.people.darren)"), {"type": "debt"})
        self.assertIsNone(self.js("LEDGER.G.hooks.demandFor(LEDGER.G.people.ron)"), "Ron owes nothing")
        self.js("LEDGER.G.debts.darren.st = 'paid'")
        try:
            self.assertIsNone(self.js("LEDGER.G.hooks.demandFor(LEDGER.G.people.darren)"))
        finally:
            self.js("LEDGER.G.debts.darren.st = 'open'")

    @unittest.skip("not reachable through the hook: the tin fills only when he knocks at a night job's drop door "
                   "(key E prompt) or collects a debt in talk or a fight; washing it goes through Sheila's talk")
    def test_3d_night_job_and_debt_money_go_in_the_tin(self):
        pass

    # 4. Saving and restore ------------------------------------------------------------
    KEY_FIELDS = ["t", "money", "debts", "events", "ledger", "nextE", "sightIdx", "transfers", "log"]

    def snapshot(self):
        return self.js("JSON.parse(JSON.stringify({%s}))" % ", ".join("%s: LEDGER.G.%s" % (k, k) for k in self.KEY_FIELDS))

    def test_4a_save_falls_back_to_the_browser_and_restore_returns_the_state(self):
        self.assertEqual(self.js("typeof window.claude"), "undefined", "outside claude.ai there is no claude.use")
        self.js("localStorage.removeItem(%r)" % SAVE_KEY)
        self.assertTrue(self.js("LEDGER.saveNow()"), "saveNow must report a save")
        raw = self.js("localStorage.getItem(%r)" % SAVE_KEY)
        self.assertTrue(raw, "with no claude.use the save must land in the browser")
        saved = json.loads(raw)
        self.assertEqual(saved["v"], 4)
        live = self.snapshot()
        for k in self.KEY_FIELDS:
            self.assertEqual(saved[k], live[k], "saved %s differs from the live state" % k)
        self.assertEqual(saved["story"]["phase"], "play")
        self.assertTrue(all("by" not in m for m in saved["minds"].values()), "the by-index is rebuilt, not saved")
        mem0 = self.js("Object.fromEntries(Object.entries(LEDGER.G.minds).map(([k, m]) => [k, m.mem.length]))")
        # Change the world, then restore.
        self.js("LEDGER.G.money.clean = 1; LEDGER.G.debts.dennis.st = 'paid'; LEDGER.G.ledger.acts = []; LEDGER.step(30)")
        self.assertNotEqual(self.snapshot(), live)
        self.assertTrue(self.js("LEDGER.restore(localStorage.getItem(%r))" % SAVE_KEY))
        after = self.snapshot()
        for k in self.KEY_FIELDS:
            self.assertEqual(after[k], live[k], "restored %s differs from the save" % k)
        self.assertEqual(self.js("Object.fromEntries(Object.entries(LEDGER.G.minds).map(([k, m]) => [k, m.mem.length]))"), mem0)
        self.assertTrue(self.js("Object.values(LEDGER.G.events).every(e => LEDGER.G.ev[e.id] === e)"), "ev must index the restored events")

    def test_4b_restore_refuses_another_save_version(self):
        before = self.snapshot()
        bad = self.js("JSON.stringify(Object.assign(JSON.parse(localStorage.getItem(%r)), {v: 3, t: 1}))" % SAVE_KEY)
        self.assertFalse(self.js("LEDGER.restore(%s)" % json.dumps(bad)))
        self.assertEqual(self.snapshot(), before)

    @unittest.expectedFailure
    def test_4c_restore_through_the_hook_relinks_people_to_their_minds(self):
        # Finding (18 Nov): LEDGER.restore replaces G.minds but leaves every person holding the old
        # mind object, and the restored minds have no by-index. The game's own Continue rebuilds the
        # people afterwards (the bundle's qd()); the hook does not, so after a hook restore the people
        # act on the pre-restore memories. Marked expected-to-fail so a fix shows as an unexpected pass.
        self.js("LEDGER.restore(localStorage.getItem(%r))" % SAVE_KEY)
        self.assertTrue(self.js("LEDGER.G.named.every(p => p.mind === LEDGER.G.minds[p.id] && !!p.mind.by)"))


if __name__ == "__main__":
    unittest.main()
