"""Rule checks: catch a Fable round that changes one of the prototype's rule numbers.

The rules come from production/lane/PROTOTYPE-RULES-READ-2026-11-18.md (read by hand from the
bundle, 18 Nov 2026, bundle version 1794862482-9f9b). Rule ids below are that file's section and
row, counted from the top of each table (1.01 is the first row of "Seeing and witnessing").

Two layers:

1. Static (no browser, no pictures): for each clearly read rule, the piece of the built bundle
   that holds its number must still be there, as often as it was when read. When a rule's number
   moves, the failing row names the rule. Most rows search by the bundler's shortened names
   (single letters like x, ue, Ve); those rows carry the bundle_names mark. When Fable's readable
   source replaces the bundle, this table is to be re-pointed at the readable files (same rule
   ids, new search strings); until then a rebuild with new short names fails these rows even
   when no rule changed, and that is the signal to re-point, not a rule change.
   Rows marked inferred: the number was read, but its unit or purpose was worked out from context.

2. Live (headless Chromium, through the game's test hook window.LEDGER): a handful of rules
   checked by what the game does, not by its text: the hour length, the week's start, starting
   money, Mickey's book, Ron's schedule, people's traits, who never makes a statement, the save
   version, heat fading, and the arrest's hold and bill. Needs the pictures in the folder named
   by LEDGER_PROTO_ASSETS, as the smoke test; skipped otherwise, never passed. Also skipped when
   Playwright's Chromium cannot start.

Run with pytest (python -m pytest tests/rules_test.py). Rule reads found wrong are kept as strict
expected failures, so a later fix to the reading file or the game shows up.
"""
import functools, http.server, math, os, re, sys, tempfile, threading, time

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import build  # noqa: E402

ASSETS = os.environ.get("LEDGER_PROTO_ASSETS")
GL = ["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader"]
HOUR = 45  # LEDGER.step real seconds per game hour (rule 6.01)

S = "short"   # the search uses the bundler's shortened names
P = "plain"   # the search is plain data or text (survives a renaming, maybe not a reformat)

# (rule id, plain name with its number, search string in the minified bundle, times found, kind)
# kind is S or P, with " inferred" added where the rule file marks the meaning as inferred.
RULES = [
    # 1. Seeing and witnessing
    ("1.01", "sight range 4 + 44 x light^1.2, x(1 - 0.3 rain), x(1 - 0.22 mist at night)",
     "(4+44*Math.pow(ue(i,0,1),1.2))*(1-.3*x.weather.rain)*(1-.22*x.weather.mist*qn())", 1, S),
    ("1.02", "cab headlights: seen from at least 34 m", "e.lights&&(o=Math.max(o,34))", 1, S),
    ("1.03", "indoors: seen from at least 14 m", "o=Math.max(o,14)", 1, S),
    ("1.04", "field of view on the street 1.08 rad each side", "fov:1.08", 1, P),
    ("1.05", "field of view from a home window 1.35 rad each side", "fov:1.35", 1, P),
    ("1.06", "under 3 m seen unless well behind (1.9 rad)", "n<3&&l<1.9", 1, S),
    ("1.07", "line of sight checked against walls", "x.env.los(t.x,t.z,e.x,e.z)", 1, S),
    ("1.08", "clarity = 1 - distance / range, 0.05 to 1", "a=ue(1-n/o,.05,1)", 1, S),
    ("1.09", "noise radius: cab 8 to 30, still 0.5, running 12, walking 5",
     "i.inCar?8+22*Math.min(1,Math.abs(x.car.v)/12):i.v<.2?.5:i.run?12:5", 1, S),
    ("1.10", "noise by hour: x0.5 10-16, x2 before 5, x1.5 5-7, x1.3 after 22, else x0.8",
     "i>=10&&i<16?.5:i<5?2:i<7?1.5:i>=22?1.3:.8", 1, S),
    ("1.11", "rain muffles noise x(1 - 0.6 rain)", "em()*(1-.6*x.weather.rain)", 1, S),
    ("1.12", "a sleeper hears at 70 percent of the radius", "hear:c<=e.noiseR*.7", 1, S),
    ("1.13", "attention rises 0.45 + 1.4 x clarity a second, x1.5 during an act",
     "attn+=i*(.45+1.4*a.c)*(t?1.5:1)", 1, S),
    ("1.14", "night out counts from 23:30 to 05:00", "i>=23.5||i<5", 1, S),
    ("1.14b", "the cab at night is its own kind of being seen", '"cab_night":"cab_drive"', 1, P),
    ("1.15", "one sighting event per kind per two-hour block", "Math.floor(Ve()/2)", 1, S),
    ("1.16", "a heard memory at most every 90 game minutes", "r.heardT||x.t-r.heardT>90", 1, S),
    ("1.17", "loud acts reach hearers as a man at 0.3 sure", 'src:"heard",who:"man",sure:.3', 1, P),
    ("1.18", "sureness 0.35 + 0.65 x clarity, x0.85 unless named",
     'ue(.35+.65*t.c,0,1)*(r==="tom"?1:.85)', 1, S),
    ("1.19", "a memory's starting heat is severity + 0.3", "ue(a.sev+.3,0,1)", 1, S),
    ("1.20", "named as Tom above face score 0.36", 's>.36&&o?"tom"', 1, S),
    ("1.20b", "the coat at night cuts the face score x0.4", "n.coat&&qn()>.5&&(s*=.4)", 1, S),
    ("1.21", "act table: inherit severity 0.5", "inherit:xt(.5,0,0", 1, S),
    ("1.21b", "act table: arrive severity 0.3", "arrive:xt(.3,0,0", 1, S),
    ("1.21c", "act table: kill severity 1, crime 3", "kill:xt(1,-1,3", 1, S),
    ("1.22", "a non-act glance raises familiarity once every 20 game minutes", "seenCool=x.t+20", 1, S),
    ("1.23", "timid people (nerve under 0.62) step back", "nerve==null?.5:i.def.nerve)<.62", 1, S),
    ("1.24", "night: day 07:45 to 17:15, full night 18:45 to 06:15",
     "i>=7.75&&i<17.25?0:i>=18.75||i<6.25?1", 1, S),
    # 2. Gossip and rumour
    ("2.01", "a gossip round every 4 game minutes", "Va.g>=4&&(Va.g=0,V2())", 1, S),
    ("2.02", "talking distance 4.8 m street, 8 m indoors", '>(t.space==="street"?4.8:8)', 1, S),
    ("2.03", "closeness weight 0.42, +0.38 close friends, x(0.4 + talk) x(0.6 + 0.4 talk)",
     "t+=.38),t*(.4+(i.def.talk??.6))*(.6+.4*(e.def.talk??.6))", 1, S),
    ("2.04", "heat under 0.12 is not passed on", "s.heat<.12||e.mind.by[s.e]", 1, S),
    ("2.05", "a discreet person holds back by their discretion", "Sn(i.def.discretion", 1, S),
    ("2.06", "each telling: sure x0.8, heat x0.92, hop +1; teller heat +0.12",
     "sure:t.sure*.8,heat:t.heat*.92,hop:t.hop+1}),t.heat=Math.min(1,t.heat+.12)", 1, S),
    ("2.08", "passers-by pass on stories over heat 0.2 at 35 percent", "s.heat>.2);if(n&&Sn(.35))", 1, S),
    ("2.09", "heat fades x e^(-minutes/1700)", "Math.exp(-i/1700)", 1, S),
    ("2.09b", "heat fades every 10 game minutes", "Va.d>=10&&(Y2(Va.d),Va.d=0)", 1, S),
    ("2.09c", "a forever act (a killing) keeps heat 0.6", "forever?.6:0", 1, S),
    ("2.10", "certainty does not fade, only heat", "n.heat=Math.max(s,n.heat*e)", 1, S),
    ("2.11", "Tuesday push at 08:45 on day 1", "i===1&&e>=8.75", 1, S),
    ("2.12", "seeing two tell a story within 18 m makes a note", "x.tom.z)<18", 1, S),
    ("2.13", "knowing score 0.25 + 0.09 per kind (up to 6) + 0.4 familiarity",
     "return(e.inh?.25:0)+Math.min(t.size,6)*.09+e.fam*.4", 1, S),
    ("2.13b", "names at 0.2, 0.5, 0.8, 1.05", "e>=1.05?4:e>=.8?3:e>=.5?2:e>=.2?1:0", 1, S),
    ("2.14", "the street's name: reached by 40 percent of locals", "length>=i.length*.4", 1, S),
    ("2.15", "a story said to his face at most every 40 game minutes", "coolSay=x.t+40", 1, S),
    # 3. The Ledger
    ("3.01", "every act goes on his own list", "x.ledger.acts.find(e=>e.e===i.id)||x.ledger.acts.push", 1, S),
    ("3.02", "belief ranks: talking 0, window 1, saw 2", "talking:0,window:1,saw:2", 1, P),
    ("3.03", "saw only when noticed: 34 m, 0.9 rad beyond 2.5 m, window 9 m, lit 0.2 beyond 7 m",
     "o>34||o>2.5&&Math.abs(_n(x.env.camYaw(),Math.atan2(t.x-n,t.z-s)))>.9||t.win&&!i.winLit&&o>9"
     "||o>7&&x.env.lightAt(t.x,t.z,t.space)<.2", 1, S),
    ("3.04", "there: done in front of them", 'Os(e,i,"there")', 1, S),
    ("3.05", "asked: he asked and was told", 'Os(a,i,"asked"', 1, S),
    ("3.06", "two heads together in the caff make a note", "had their heads together at Rinaldi's", 1, P),
    ("3.07", "first note shows the Ledger hint", "L opens the Ledger", 1, P),
    # 4. Money and debts
    ("4.01", "Tom starts with 23.50 clean", "clean:2350", 1, P),
    ("4.02", "Mickey's book: Dennis 80, Lee 15, Darren 22, Julie 9, Wayne 30",
     'debts:{dennis:{owed:8e3,st:"open"},lee:{owed:1500,st:"open"},darren:{owed:2200,st:"open"},'
     'julie:{owed:900,st:"open"},wayne:{owed:3e3,st:"open"}}', 1, P),
    ("4.03", "a debtor pays if fear over 0.45, or liking over 0.3 and owing 15 or less",
     "i.mind.fear>.45||i.mind.regard>.3&&o.owed<=1500", 1, S),
    ("4.04", "a collected debt goes in the tin", "oh(n,!0)", 1, S),
    ("4.05", "striking a debt out: liking +0.5", "regard+.5", 1, P),
    ("4.06", "Julie's slate: nine pounds", "Nine pounds, since the summer", 2, P),
    ("4.07", "fare 80p plus 0.9p a metre, rounded to 10p", "(80+We(t.sx,t.sz,n.p[0],n.p[1])*.9)/10)*10", 1, S),
    ("4.08", "radio fares 07:00 to 23:12", "Ve()>=7&&Ve()<23.2", 1, S + " inferred"),
    ("4.08b", "a new fare offer every 16 to 34 seconds", "fareCool=_t(16,34)", 1, S + " inferred"),
    ("4.08c", "an offer lasts 26 seconds", "t.t=26", 1, S + " inferred"),
    ("4.08d", "after a missed offer, 20 to 40 seconds", "e.fareCool=_t(20,40)", 1, S + " inferred"),
    ("4.08e", "after a paid fare, 14 to 30 seconds", "n.fareCool=_t(14,30)", 1, S + " inferred"),
    ("4.10", "the book hides 10.00 + 80 percent of fares since the wash",
     "1e3+Math.round(x.money.sinceWash*.8)", 1, S),
    ("4.11", "job 1 pays sixty", "Sixty. Count it somewhere else.", 1, P),
    ("4.11b", "job 1 (the Monday bag) pay 60.00", "toZ:\"Metcalfe's back door\",pay:6e3", 1, P),
    ("4.12", "a job not done by 03:30 to 12:00 next day is a no-show", "Ve()>=3.5&&Ve()<12", 1, S),
    ("4.13", "rent 18.00", "sr(1800,!0)", 1, S),
    ("4.13b", "rent late from Saturday (day 5)", "i>=5&&!t.rent", 1, S),
    ("4.14", "Ron's door and Darren's good word: 5.00", "sr(500)", 2, S),
    ("4.14b", "Darren's hearsay: 3.00", "sr(300)", 1, S),
    ("4.15", "tea and paper: 20p", "sr(20,!0)", 2, S),
    ("4.15b", "tea passes 25 game minutes", "or(x.t+25,!1)", 1, S),
    ("4.15c", "tea: caff people familiarity +0.06", "t.mind.fam=ue(t.mind.fam+.06,0,1)", 1, S),
    ("4.16", "the paper", "tf(x.story.flags.dead", 1, S),
    ("4.17", "spending takes dirty money first", "function sr(", 1, S),
    ("4.18", "beaten down: pays up to 8.00 from clean", "Math.min(t.clean,800)", 1, S),
    # 5. Suspicion and police
    ("5.01", "statements taken at 04:00 from Tuesday", "e>=4&&i>=1&&Yx(i-1)", 1, S),
    ("5.02", "a statement needs sure at least 0.55", "a.sure<.55", 1, S),
    ("5.03", "ten people never make a statement", "nostmt:1", 10, P),
    ("5.04", "violence (crime 2+) sends Ellis", "violent:n&&Wt[n.kind].crime>=2", 1, S),
    ("5.05", "the police come at 09:00", "(i+1)*1440+540", 1, S),
    ("5.06", "held 4 hours (5 violent), +2 if he ran; bill 25.00 (40.00 if he ran)",
     "(e.violent?5:4)+(t?2:0),a=t?4e3:2500", 1, S),
    ("5.07", "they give up after 7 s out of sight, 70 m or 60 s", "t.lost>7||r>70||t.ct>60", 1, S + " inferred"),
    ("5.08", "loudness: heat x severity x badness, x0.6 if not by name",
     'n.val<0&&(i+=t.heat*n.sev*-n.val*(t.who==="tom"?1:.6))', 1, S),
    ("5.09", "Ellis walks Thursday or Friday, 10:00 to 13:00", "e<3||e>4||i.ellisDays[e]||t<10||t>13", 1, S),
    ("5.09b", "Ellis walks at loudness 2.2", "n<2.2&&", 1, S),
    ("5.09c", "Ellis asks up to 5 locals", ".slice(0,5).map(r=>r.id)", 1, S),
    ("5.10", "Cammack's lads at loudness over 1.2", "Ba()>1.2", 1, S),
    ("5.11", "fear +0.07 told, +0.18 seen", 'e.src==="told"?.07:.18', 1, S),
    ("5.12", "liking moves x0.15 told, x0.26 seen", 'e.src==="told"?.15:.26', 1, S),
    # 6. Time of day and routines
    ("6.01", "one game hour is 45 real seconds", "let e=i*60/45", 1, S),
    ("6.02", "a new week starts Monday 15:36 (save version 4)", "v:4,t:936", 1, P),
    ("6.05", "the weather list", '["mist","drizzle","drizzle","rain","dry","heavy"]', 1, P),
    ("6.06", "Ron: home 00:00, caff 06:36, rank 08:06, fish 12:18, rank 12:48, Tang's 17:24, rank 17:54, home 23:36",
     'sched:[[0,"home","sleep"],[6.6,"caff:s1","sit"],[8.1,"rank","idle"],[12.3,"fish:q1","queue"],'
     '[12.8,"rank","idle"],[17.4,"tangs:q1","queue"],[17.9,"rank","smoke"],[23.6,"home","sleep"]]', 1, P),
    ("6.07", "Sheila: office 07:30 to 18:12, caff 12:30",
     'sched:[[0,"off"],[7.5,"mickeys:sheila","work"],[12.5,"caff:s7","sit"],[13.1,"mickeys:sheila","work"],[18.2,"off"]]', 1, P),
    ("6.07b", "Grace: caff 06:00 to 17:12",
     'sched:[[0,"home","sleep"],[6,"caff:grace","work"],[17.2,"home","idle"],[22.5,"home","sleep"]]', 1, P),
    ("6.08", "Sheila: nerve 0.95, talk 0.15, discretion 0.92", "nerve:.95,venal:0,talk:.15,discretion:.92", 1, P),
    ("6.08b", "Darren: nerve 0.3, talk 0.95, discretion 0.05", "nerve:.3,venal:.95,talk:.95,discretion:.05", 1, P),
    ("6.08c", "Ron: nerve 0.85, talk 0.7, discretion 0.35", "nerve:.85,venal:.8,talk:.7,discretion:.35", 1, P),
    # 7. Talk
    ("7.01", "Tab opens the suggested lines", 'i==="Tab"?(V.open', 1, S),
    ("7.02", "at most three suggested lines", "e.length<3&&t.keep", 1, S),
    ("7.05", "a live reply is cut to three sentences and 380 characters",
     'e.slice(0,3).join("").trim()),i.slice(0,380)', 1, S),
    ("7.07", "talking costs 1.5 game minutes an exchange", "x.t+=1.5,await", 1, S + " inferred"),
    # 8. Saving
    ("8.01", "save version 4; any other refused", "e.v!==4", 1, S),
    ("8.01b", "browser save key ledger.save.v4", 'yT="ledger.save.v"+4', 1, S),
    ("8.02", "account saves in chunks of 150,000 characters", "hw=15e4", 1, S),
    ("8.03", "the newer save wins", "t(e)>t(i)?e:i", 1, S),
    ("8.04", "autosave every 75 real seconds", "fw>75&&!z.on&&(fw=0,el(!1))", 1, S),
    ("8.05", "what is saved", 'var gT=["v","t","played"', 1, S),
    ("8.06", "restore through the hook does not rebuild memory; Continue does", 'qd(),x.story.phase="play"', 1, S),
]
# Left out of the static table, and why: 2.07 and 4.19 are absences (no hop limit, no wages);
# 4.09 has no number and no unique string; 6.03, 6.04, 7.03 and 7.04 are read from the game's own
# design notes only, whose headings carry no number; 7.06 (a name learned when said) has no number.


@functools.lru_cache(maxsize=1)
def bundle():
    with tempfile.TemporaryDirectory() as d:
        build.build(dist=d)
        with open(os.path.join(d, "ledger.js"), encoding="utf-8") as f:
            return f.read()


def _param(row):
    rid, name, search, count, kind = row
    marks = [pytest.mark.bundle_names] if kind.startswith(S) else []
    return pytest.param(rid, name, search, count, id="%s %s" % (rid, name[:50]), marks=marks)


@pytest.mark.parametrize("rid,name,search,count", [_param(r) for r in RULES])
def test_static_rule_still_in_bundle(rid, name, search, count):
    found = bundle().count(search)
    assert found == count, "rule %s (%s): %r found %d times, expected %d; the rule may have moved" % (
        rid, name, search, found, count)


def test_static_rule_ids_unique():
    ids = [r[0] for r in RULES]
    assert len(ids) == len(set(ids))


def _act_kinds():
    # The act table starts at "Wt={inherit:"; its top-level keys are name:xt(...).
    b = bundle()
    start = b.find("Wt={inherit:xt(")
    assert start >= 0, "act table not found"
    end = b.find("}", b.find("choice_silent:xt(", start))
    return re.findall(r"[{,](\w+):xt\(", b[start:end])


@pytest.mark.bundle_names
def test_static_act_table_has_51_kinds_as_found():
    assert len(_act_kinds()) == 51


# 30 schedule blocks: 28 named people plus the fare passenger and the yard lad (rules read corrected 18 Nov).
def test_static_30_schedule_blocks():
    assert bundle().count("sched:[") == 30



# ---------------------------------------------------------------------------------------------
# Live layer: one headless Chromium, one new week; tests run in file order and share the street.

@pytest.fixture(scope="module")
def game():
    if not (ASSETS and os.path.isdir(ASSETS)):
        pytest.skip("LEDGER_PROTO_ASSETS not set: pictures missing, live rule checks skipped")
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        pytest.skip("playwright not installed")
    tmp = tempfile.TemporaryDirectory()
    build.build(assets_dir=ASSETS, dist=tmp.name)

    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=tmp.name))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    pw = sync_playwright().start()
    try:
        b = pw.chromium.launch(args=GL)
    except Exception as e:  # Chromium missing or unable to start here
        pw.stop(); srv.shutdown(); tmp.cleanup()
        pytest.skip("Chromium could not start: %s" % str(e).splitlines()[0])
    pg = b.new_page(viewport={"width": 1280, "height": 720})
    pg.errors = []
    pg.on("pageerror", lambda e: pg.errors.append(str(e)))
    pg.goto("http://127.0.0.1:%d/index.html" % srv.server_address[1])
    pg.wait_for_function("window.LEDGER && window.LEDGER.G", timeout=90000)
    pg.evaluate("LEDGER.startNew()")
    pg.wait_for_function("LEDGER.G.story.phase === 'play'", timeout=30000)
    pg.evaluate("window.LEDGER_MANUAL = true; window.LEDGER_NORENDER = true")
    yield pg
    try:
        b.close(); pw.stop()
    finally:
        srv.shutdown(); srv.server_close(); tmp.cleanup()


@pytest.fixture
def js(game):
    yield game.evaluate
    assert game.errors == [], "page errors: %s" % game.errors[:3]


def test_live_6_02_week_starts_monday_1536(js):
    # The page runs a frame or so before the clock is stopped, so allow a few game minutes.
    t = js("LEDGER.G.t")
    assert 936 <= t < 940, "a new week should start at Monday 15:36 (936), not %.1f" % t
    assert js("LEDGER.G.v") == 4


def test_live_6_01_one_game_hour_is_45_real_seconds(js):
    t0 = js("LEDGER.G.t"); js("LEDGER.step(45)"); t1 = js("LEDGER.G.t")
    assert abs((t1 - t0) - 60) < 0.01, "45 real seconds moved the clock %.2f game minutes" % (t1 - t0)
    js("LEDGER.step(4.5)")
    assert abs(js("LEDGER.G.t") - t1 - 6) < 0.01


def test_live_4_01_starting_money(js):
    m = js("LEDGER.G.money")
    assert (m["clean"], m["dirty"]) == (2350, 0)


def test_live_4_02_mickeys_book(js):
    d = js("LEDGER.G.debts")
    assert {k: v["owed"] for k, v in d.items()} == {
        "dennis": 8000, "lee": 1500, "darren": 2200, "julie": 900, "wayne": 3000}
    assert all(v["st"] == "open" for v in d.values())


def test_live_6_06_rons_schedule(js):
    assert js("LEDGER.G.people.ron.def.sched") == [
        [0, "home", "sleep"], [6.6, "caff:s1", "sit"], [8.1, "rank", "idle"], [12.3, "fish:q1", "queue"],
        [12.8, "rank", "idle"], [17.4, "tangs:q1", "queue"], [17.9, "rank", "smoke"], [23.6, "home", "sleep"]]


def test_live_6_08_traits(js):
    got = js("Object.fromEntries(['sheila','darren','ron'].map(k => { const d = LEDGER.G.people[k].def;"
             " return [k, [d.nerve, d.talk, d.discretion]]; }))")
    assert got == {"sheila": [0.95, 0.15, 0.92], "darren": [0.3, 0.95, 0.05], "ron": [0.85, 0.7, 0.35]}


def test_live_named_people_as_found(js):
    assert js("LEDGER.G.named.length") == 28
    assert js("LEDGER.G.named.every(p => Array.isArray(p.def.sched))")


def test_live_5_03_who_never_makes_a_statement(js):
    assert set(js("LEDGER.G.named.filter(p => p.def.nostmt).map(p => p.id)")) == {
        "sheila", "ron", "darren", "ellis", "rita", "wayne", "lee", "hal", "dennis", "pc"}
    assert not js("LEDGER.G.people.terry.def.nostmt"), "Terry can make a statement"


def test_live_8_01_save_version_4_in_the_browser(js):
    # Outside claude.ai saving falls back to the browser only (as systems_test.py).
    js("LEDGER.saveNow()")
    v = js("(() => { try { const s = localStorage.getItem('ledger.save.v4'); return s ? JSON.parse(s).v : null; }"
           " catch (e) { return 'err ' + e; } })()")
    assert v == 4


def test_live_2_09_heat_halves_in_about_20_game_hours(js):
    # A memory planted for Ada, who stays at home (gossip never runs at home, so nothing else moves
    # her heat). Five game hours later its heat must be x e^(-300/1700); heat fades in 10-minute
    # ticks, so allow one tick either way.
    assert js("LEDGER.G.people.ada.space") == "home"
    eid = js("""(() => { const G = LEDGER.G, id = G.nextE++;
        const e = {id, kind: 'stare', t: G.t, zone: G.tom.zone, x: 0, z: 0, coat: false, car: false, wit: []};
        G.events.push(e); G.ev[id] = e;
        const m = G.people.ada.mind, s = {e: id, src: 'told', from: null, who: 'tom', sure: 0.9, heat: 0.8,
          t: G.t, said: false, hop: 0, face: 1};
        m.mem.push(s); m.by[id] = s; return id; })()""")
    js("LEDGER.step(%d)" % (5 * HOUR))
    assert js("LEDGER.G.people.ada.space") == "home"
    heat = js("LEDGER.G.people.ada.mind.by[%d].heat" % eid)
    lo, hi = 0.8 * math.exp(-310 / 1700), 0.8 * math.exp(-290 / 1700)
    assert lo <= heat <= hi, "heat %.4f after five game hours, expected %.4f to %.4f" % (heat, lo, hi)


def test_live_5_06_arrest_hold_and_bill_when_he_ran(js, game):
    # The hook's arrestNow is the arrest for assaulting an officer: violent and counted as running,
    # so the top of the range: 5 + 2 = 7 hours and a 40.00 bill, paid from clean, the rest owed.
    # Kept last: it moves the clock seven hours. The lower rows (4 hours, 25.00) need the
    # constable's talk choice, a key press; they are held by the static row 5.06 only.
    t0, clean = js("LEDGER.G.t"), js("LEDGER.G.money.clean")
    js("LEDGER.G.hooks.arrestNow(LEDGER.G.people.pc)")
    time.sleep(0.2)
    game.wait_for_function("!LEDGER.G.paused", timeout=60000)
    assert abs(js("LEDGER.G.t") - t0 - 7 * 60) < 0.5, "held %.1f game minutes" % (js("LEDGER.G.t") - t0)
    paid = min(clean, 4000)
    assert js("LEDGER.G.money.clean") == clean - paid
    assert (js("LEDGER.G.story.flags.oweAgar") or 0) == 4000 - paid
    assert js("LEDGER.G.story.arrest") is None
