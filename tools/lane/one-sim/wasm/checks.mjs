// ONE SIMULATION IN THE BROWSER: the checks themselves (first slice, 19 November 2026).
//
// One copy of the checks, run two ways: under Node (test_one_sim.mjs) and inside a real
// web page (browser/index.html, driven by browser_test.py). Nothing here is Node-only.
//
// The table is the golden table the REAL C# Core writes (ledger/PerceptionGolden, built
// and run by one-sim.sh reference). Nothing expected here was typed by hand. The modules
// are loaded as a page loads them (one-sim.mjs): no files, no clock, no random numbers;
// the cast and news files are handed in as text.
//
// T1  every golden row, asked through JavaScript of the check build;
// T2  routines through the bridge: where each person is, each hour of the week;
// T3  the week hour by hour through the bridge: six scripted weeks, every hour's
//     thirteen fields against the C# Core's TownWeekHour rows;
// T4  the same calls twice give the same town, to the last character. Inside one engine this can
//     hardly fail (the loader answers the clock and the random numbers with zero). The real test is
//     across engines: one-sim.sh all compares this digest from Node with the one from the browser
//     (engines_agree.py, printed as T4x);
// T5  speed, measured;
// T6  rough handling: wrong calls must not knock the module over;
// T7  the Ledger's facts (who knows what, and how) read back through the bridge.
//
// And the bridge the prototype will call (one-sim-bridge.mjs), which turns its clock into those calls:
// T8  the six scripted weeks again, driven by a clock in odd steps through the bridge, the town's
//     talk run by the hour as the reference week runs it: every hour against the C# Core's rows;
// T9  the same with the talk run by the minute, the packaged game's way: the same town whatever
//     the size of the clock's steps, and a count of the hours that differ from the C# rows;
// T10 a save in the middle of each week, loaded into a fresh module, played on: the same town;
// T11 rough handling of the bridge.
import { loadOneSim, NightAnswer, WeekAnswer, Offence } from './one-sim.mjs';
import { openTown, PROTOTYPE_TO_CAST, BRIDGE_SAVE_VERSION } from './one-sim-bridge.mjs';

async function sha256(text) {
  const d = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text));
  return [...new Uint8Array(d)].map((b) => b.toString(16).padStart(2, '0')).join('');
}

/// brainBytes, checkBytes: the two modules' bytes. tableText: the golden table. dataText:
/// { 'hook-cast.json': text, 'quay-cast.json': text, 'town-news.json': text }.
export async function runChecks({ brainBytes, checkBytes, tableText, dataText, log = () => {} }) {
  brainBytes = await WebAssembly.compile(brainBytes);
  checkBytes = checkBytes ? await WebAssembly.compile(checkBytes) : null;   // null: the bridge checks only (T2 to T5)
  const castText = { 'hook-cast.json': dataText['hook-cast.json'], 'quay-cast.json': dataText['quay-cast.json'] };
  const lines = tableText.split('\n').map((l) => l.replace(/\r$/, '')).filter((l) => l && !l.startsWith('#'));
  const byRule = new Map();
  for (const l of lines) { const r = l.slice(0, l.indexOf('|')); if (!byRule.has(r)) byRule.set(r, []); byRule.get(r).push(l); }

  let failed = 0;
  const results = [];
  const report = { table: { rows: lines.length, rules: byRule.size, sha256: (await sha256(lines.join('\n'))).slice(0, 16) } };
  const result = (name, ok, detail) => { if (!ok) failed++; results.push({ name, ok, detail }); log(`${ok ? 'ok  ' : 'FAIL'} ${name}: ${detail}`); };
  const printed = [];
  const quiet = { print: (t) => printed.push(t) };


  // ---- T1: every golden row through JavaScript -------------------------------------------------
  if (checkBytes) {
    const sim = await loadOneSim(checkBytes, quiet);
    for (const [name, body] of Object.entries(dataText)) sim.check.castFile(name, body);
    const tally = { ok: 0, mismatch: 0, unknown: 0, short: 0, skip: {} };
    const firstBad = [];
    const t0 = performance.now();
    for (const l of lines) {
      const a = sim.check.row(l);
      if (a === 'ok') tally.ok++;
      else if (a.startsWith('skip:')) tally.skip[a.slice(5)] = (tally.skip[a.slice(5)] ?? 0) + 1;
      else if (a === 'unknown') { tally.unknown++; if (firstBad.length < 5) firstBad.push('UNKNOWN ' + l.slice(0, 160)); }
      else if (a === 'short') { tally.short++; if (firstBad.length < 5) firstBad.push('SHORT ' + l.slice(0, 160)); }
      else { tally.mismatch++; if (firstBad.length < 5) firstBad.push(a.slice(0, 120) + ' <- ' + l.slice(0, 160)); }
    }
    const ms = performance.now() - t0;
    const skipped = Object.values(tally.skip).reduce((a, b) => a + b, 0);
    const addsUp = tally.ok + tally.mismatch + tally.unknown + tally.short + skipped === lines.length;
    report.T1 = { ...tally, skipped, ms: Math.round(ms), asksOutside: sim.asksOutside };
    result('T1 golden rows through JavaScript', tally.ok > 0 && tally.mismatch === 0 && tally.unknown === 0 && tally.short === 0 && addsUp,
      `${lines.length} rows of ${byRule.size} rules from the C# Core: ${tally.ok} agree, ${tally.mismatch} differ, ${tally.unknown} unanswered, ` +
      `${tally.short} too short, ${skipped} skipped by name ${JSON.stringify(tally.skip)}; ${Math.round(ms)} ms`);
    for (const b of firstBad) log('     ' + b);
    // Only the named holes may be skipped: the unported claims scenario and the rows that need exceptions.
    const knownHoles = Object.keys(tally.skip).every((k) => k === 'claims' || k === 'FactNull');
    result('T1b only the two named holes are skipped', knownHoles && (tally.skip.claims ?? 0) === 7 && (tally.skip.FactNull ?? 0) === 4,
      `claims ${tally.skip.claims ?? 0} (the player's claims, not ported), FactNull ${tally.skip.FactNull ?? 0} (need exceptions, off in the game's build too)`);
    const seeded = (byRule.get('GossipFuzz') ?? []).length;
    result('T1c seeded runs are in the table', seeded >= 3000, `${seeded} GossipFuzz rows (fixed seeds, each a digest of a whole run) are among the rows above`);
  }

  // ---- T2: routines through the bridge ---------------------------------------------------------
  {
    let rows = 0, bad = 0;
    const firstBad = [];
    for (const file of Object.keys(castText)) {
      const sim = await loadOneSim(brainBytes, quiet);
      sim.newTown(castText[file]);
      for (const l of byRule.get('CastPlaceOf') ?? []) {
        const f = l.split('|');           // CastPlaceOf|file|person|day|hour|place
        if (f[1] !== file) continue;
        rows++;
        const got = sim.placeOf(f[2], Number(f[3]), Number(f[4]));
        if (got !== f[5]) { bad++; if (firstBad.length < 5) firstBad.push(`${l} got=${got}`); }
      }
    }
    report.T2 = { rows, bad };
    result('T2 routines through the bridge', rows > 0 && bad === 0, `${rows} person-hours of both cast files: ${rows - bad} agree with the C# Core, ${bad} differ`);
    for (const b of firstBad) log('     ' + b);
  }

  // ---- T3 and T4: the week, hour by hour, through the bridge ------------------------------------
  // The six scripted weeks of the C# Core's TownWeekHour rows (ledger/PerceptionGolden/Program.cs,
  // mirrored by the port's CoreGolden.h TownWeekAnswers): what the player does is written here once
  // more, as bridge calls; what the town then does is the module's business, and every hour's
  // answer is checked against the C# Core's row for that hour.
  const WINDOW = ['ritas', 'rita_window', "somebody put Rita's window in", 'sam:4'];
  async function playWeeks(onHour) {
    const parts = [];
    let hours = 0, ms = 0;
    for (const run of ['no', 'away', 'held', 'days', 'winddown', 'teaday']) {
      const sim = await loadOneSim(brainBytes, quiet);
      sim.newTown(castText['hook-cast.json']);
      const from = run === 'held' ? 14 : run === 'days' || run === 'teaday' ? 9 : run === 'winddown' ? 6 * 24 + 9 : 19;
      const to = run === 'days' ? 5 * 24 : run === 'winddown' ? 7 * 24 + 7 : run === 'teaday' ? 2 * 24 + 12 : 24 + 7;
      sim.age(Math.floor(from / 24), from % 24, 0);
      if (run === 'held') {
        // Taken at two for a wounding Darren named him in: eight hours, out at ten at night.
        sim.policeReport('sam', 'player.cut_d0', Offence.Wounding, 4, 0);
        sim.takeIn('player.cut_d0', 0, 14, 0);
      }
      for (let abs = from; abs < to; abs++) {
        const day = Math.floor(abs / 24), hod = abs % 24;
        const t0 = performance.now();
        const row = sim.hour(day, hod, 'mickeys');
        ms += performance.now() - t0;
        hours++;
        parts.push(`${run}|${day}|${hod}|${row}\n`);
        onHour?.(run, day, hod, row, sim);
        if (run === 'no' && day === 0 && hod === 21 && sim.askDelivered(0)) {
          sim.roundsTo(0, 21, 29);
          sim.answerAsk(0, NightAnswer.Refused, 0, 21, 30);
        }
        if (run === 'days') {
          if (day === 1 && hod === 12) {
            sim.roundsTo(1, 12, 29);
            sim.deed(1, 12, 30, ...WINDOW, 'window_d1', "the new owner put Rita's window in", 1.0);
          }
          if (day === sim.teaDay() && (hod === 21 || hod === 22)) {
            for (let m = 0; m < (hod === 21 ? 60 : 31); m++) sim.teaWithHer(day, hod, m);
          } else if (hod === 22 && sim.asksOn(day) && sim.askDelivered(day)) {
            sim.roundsTo(day, 22, 29);
            sim.answerAsk(day, NightAnswer.Did, day, 22, 30);
          }
        }
        if (run === 'teaday' && day === 0 && hod === 12) {
          sim.roundsTo(0, 12, 29);
          sim.deed(0, 12, 30, ...WINDOW, 'window_d0', "the new owner put Rita's window in", 1.0);
        }
        if (run === 'winddown' && day === sim.weekDay() && hod === 10 && sim.weekAsksNow(day, 10, 30, true)) {
          sim.weekAsk(day, 10, 30);
          sim.roundsTo(day, 10, 39);
          sim.weekGive(WeekAnswer.WindDown, day, 10, 40);
        }
      }
      parts.push(sim.state() + '\n' + sim.stories() + '\n');
    }
    return { digest: await sha256(parts.join('')), hours, ms };
  }

  {
    const want = new Map();
    for (const l of byRule.get('TownWeekHour') ?? []) {
      const f = l.split('|');             // TownWeekHour|run|day|hour|thirteen fields
      want.set(f.slice(1, 4).join('|'), f.slice(4).join('|'));
    }
    let rows = 0, bad = 0;
    const firstBad = [], seen = new Set();
    // T7's tally: the Ledger's facts (who knows what, and how), read back after every scripted hour.
    // The only witness in these weeks is the one named in the deed ('sam', at rung 4: recognised).
    const facts = { hours: 0, unread: 0, countBad: 0, sawByNonWitness: 0, deedHours: 0, witnessHolds: 0, first: [] };
    const ledgerFacts = (run, day, hod, row, sim) => {
      let list;
      try { list = sim.knows(); } catch (e) { facts.unread++; if (facts.first.length < 3) facts.first.push(`${run}|${day}|${hod}: not readable, ${String(e).slice(0, 80)}`); return; }
      facts.hours++;
      const said = row.split('|')[10];     // the hour's own count of stories held, which T3 holds to the C# Core's row
      if (String(list.length) !== said) { facts.countBad++; if (facts.first.length < 3) facts.first.push(`${run}|${day}|${hod}: ${list.length} facts read back, the hour's row says ${said}`); }
      const windowStories = list.filter((f) => f.topic.startsWith('player.window_d'));
      for (const f of windowStories) {
        if (f.saw && f.who !== 'sam') { facts.sawByNonWitness++; if (facts.first.length < 3) facts.first.push(`${run}|${day}|${hod}: ${f.who} is said to have seen ${f.topic}`); }
      }
      const deedDone = (run === 'days' && (day > 1 || (day === 1 && hod > 12))) || (run === 'teaday' && (day > 0 || hod > 12));
      if (deedDone) {
        facts.deedHours++;
        if (windowStories.some((f) => f.who === 'sam' && f.saw === true && f.hops === 0 && f.rung === 4 && f.names === true)) facts.witnessHolds++;
        else if (facts.first.length < 3) facts.first.push(`${run}|${day}|${hod}: the witness does not hold the deed first-hand: ${JSON.stringify(windowStories.filter((f) => f.who === 'sam')).slice(0, 200)}`);
      }
    };
    const first = await playWeeks((run, day, hod, row, sim) => {
      const key = `${run}|${day}|${hod}`;
      seen.add(key);
      rows++;
      if (want.get(key) !== row) { bad++; if (firstBad.length < 5) firstBad.push(`${key}\n       got  ${row}\n       want ${want.get(key)}`); }
      ledgerFacts(run, day, hod, row, sim);
    });
    const unasked = [...want.keys()].filter((k) => !seen.has(k)).length;
    report.T3 = { rows, bad, tableRows: want.size, unasked };
    result('T3 the week hour by hour through the bridge', rows > 0 && bad === 0 && unasked === 0 && rows === want.size,
      `${rows} game hours of six scripted weeks: ${rows - bad} agree with the C# Core's TownWeekHour rows field for field, ${bad} differ, ` +
      `${unasked} of the table's ${want.size} rows not reached`);
    for (const b of firstBad) log('     ' + b);

    report.T7 = facts;
    result("T7 the Ledger's facts through the front door", facts.hours === rows && facts.unread === 0 && facts.countBad === 0 && facts.sawByNonWitness === 0
        && facts.deedHours > 0 && facts.witnessHolds === facts.deedHours,
      `who knows what and how, read back after each of ${facts.hours} scripted hours: the number of facts is the hour's own count (held to the C# Core by T3) at ` +
      `${facts.hours - facts.countBad}; nobody but the witness is said to have seen the window go (${facts.sawByNonWitness} wrong); the witness holds it first-hand, ` +
      `recognised, at ${facts.witnessHolds} of the ${facts.deedHours} hours after the deed`);
    for (const b of facts.first) log('     ' + b);

    const second = await playWeeks();
    report.T4 = { first: first.digest.slice(0, 16), second: second.digest.slice(0, 16) };
    result('T4 the same calls twice give the same town', first.digest === second.digest,
      `digest of every hour, the final state and every held story: ${first.digest.slice(0, 16)} and ${second.digest.slice(0, 16)}`);

    // ---- T5: speed (size is measured by the caller, who holds the files) -------------------------
    const perDay = (first.ms / first.hours) * 24;
    const t0 = performance.now();
    const brain = await loadOneSim(brainBytes, quiet);
    report.T5 = { hours: first.hours, msPerGameDay: Number(perDay.toFixed(3)), loadMs: Number((performance.now() - t0).toFixed(1)) };
    log(`info T5 speed: ${first.hours} game hours in ${first.ms.toFixed(1)} ms, so ${perDay.toFixed(2)} ms a game day (the Hook's cast, town talk included); loading the module ${report.T5.loadMs} ms`);
    report.asksOutside = brain.asksOutside;
    report.version = brain.version();
    log(`info what the brain asks of the outside world: ${brain.asksOutside.join(', ') || 'nothing'}`);
  }


  // ---- T6: the front door takes rough handling ----------------------------------------------------
  // Not a rule check: a page must not be able to knock the module over with a wrong call.
  {
    const problems = [];
    const tryIt = (what, fn, fine) => {
      try { const got = fn(); if (!fine(got)) problems.push(`${what}: answered ${JSON.stringify(got).slice(0, 120)}`); }
      catch (e) { problems.push(`${what}: fell over, ${String(e).slice(0, 120)}`); }
    };
    const sim = await loadOneSim(brainBytes, quiet);
    const WIN = ['ritas', 'rita_window', 'x', 'sam:4', 'window_d0', 'y'];
    tryIt('reading before a town is made', () => [sim.hour(0, 9, 'mickeys'), sim.placeOf('sam', 0, 9), sim.people().join(), sim.state(), sim.stories()],
      (g) => g.join('|') === '|||{}|');
    tryIt('acting before a town is made', () => {
      sim.deed(0, 12, 30, ...WIN, 1.0); sim.age(0, 9, 0); sim.roundsTo(0, 9, 0); sim.teaWithHer(0, 21, 0);
      return [sim.answerAsk(0, 0, 0, 22, 30), sim.asksOn(0), sim.askDelivered(0), sim.weekAsksNow(6, 10, 30), sim.weekAsk(6, 10, 30),
        sim.weekGive(1, 6, 10, 40), sim.policeReport('sam', 'player.x', 1, 4, 0), sim.takeIn('player.x', 0, 10, 0), sim.teaDay(), sim.weekDay()];
    }, (g) => g.slice(0, 8).every((v) => v === false) && g[8] === -1 && g[9] === -1);
    for (const [what, text] of [['a broken cast file', '{not json'], ['an empty cast file', ''], ['a cast file that is a list', '[1,2,3]']]) {
      tryIt(what + ' is refused with a reason', () => { try { sim.newTown(text); return 'accepted'; } catch (e) { return String(e.message); } },
        (g) => g !== 'accepted' && g.includes('cast not read'));
    }
    tryIt('and no town was made by them', () => sim.people().length, (g) => g === 0);
    sim.newTown(castText['hook-cast.json']);
    tryIt('somebody not in the cast is nowhere', () => sim.placeOf('nobody_at_all', 0, 9), (g) => g === '');
    tryIt('a time that is no time is refused', () => [sim.hour(-1, 5, 'mickeys'), sim.hour(3, 24, 'mickeys'), sim.hour(3, -1, 'mickeys')], (g) => g.every((v) => v === ''));
    tryIt('answers outside the list are refused', () => [sim.answerAsk(0, 9, 0, 22, 30), sim.answerAsk(0, -1, 0, 22, 30), sim.weekGive(7, 6, 10, 40),
      sim.policeReport('sam', 'player.x', 42, 4, 0), sim.answerAsk(0, 0, 0, 22, 61), sim.takeIn('player.x', 0, 25, 0)], (g) => g.every((v) => v === false));
    const before = sim.state();
    tryIt('acts at a time that is no time change nothing', () => {
      sim.deed(0, 12, 99, ...WIN, 1.0); sim.deed(-2, 12, 30, ...WIN, 1.0); sim.roundsTo(0, 30, 0); sim.teaWithHer(0, 21, -4); sim.age(-1, 0, 0);
      return sim.state();
    }, (g) => g === before);
    tryIt('routines wrap for any day and hour', () => [sim.placeOf('sam', -3, -5), sim.placeOf('sam', 100000, 99)], (g) => g.every((v) => typeof v === 'string'));
    tryIt('a deed with nothing named, nobody there, or a witness who is not in the cast', () => {
      sim.deed(0, 12, 30, '', '', '', '', '', '', 1.0);
      sim.deed(0, 12, 31, 'ritas', 'rita_window', 'x', 'nobody_at_all:4,:,sam', 'w_d0', 'y', NaN);
      return sim.state().length > 2 && sim.hour(0, 13, 'nowhere_at_all').split('|').length === 13;
    }, (g) => g === true);
    tryIt('long text and odd characters', () => {
      sim.deed(0, 14, 0, 'ritas', 'rita_window', 'é|~^\n"\\\u{1F600}'.repeat(2000), 'sam:4', 'odd_d0', 'said', 0.5);
      return sim.stories().length > 0 && sim.state().length > 2;
    }, (g) => g === true);
    const t0 = performance.now();
    tryIt('a jump of thirty days is caught up', () => sim.hour(30, 9, 'mickeys').split('|').length, (g) => g === 13);
    const jumpMs = performance.now() - t0;
    tryIt('a second town replaces the first', () => { sim.newTown(castText['quay-cast.json']); return sim.people().length; }, (g) => g > 0 && g < 41);
    report.T6 = { problems, jumpThirtyDaysMs: Math.round(jumpMs) };
    result('T6 the front door takes rough handling', problems.length === 0, problems.length ? problems.join('; ')
      : `calls before a town, broken cast files, times that are no time, answers outside the list, empty and odd text, a thirty-day jump (${Math.round(jumpMs)} ms), a second town: nothing fell over`);
  }

  // ---- T8 to T11: the bridge the prototype will call ----------------------------------------------
  {
    const want = new Map();
    for (const l of byRule.get('TownWeekHour') ?? []) { const f = l.split('|'); want.set(f.slice(1, 4).join('|'), f.slice(4).join('|')); }
    const RUNS = ['no', 'away', 'held', 'days', 'winddown', 'teaday'];
    const span = (run) => ({
      from: run === 'held' ? 14 : run === 'days' || run === 'teaday' ? 9 : run === 'winddown' ? 6 * 24 + 9 : 19,
      to: run === 'days' ? 5 * 24 : run === 'winddown' ? 7 * 24 + 7 : run === 'teaday' ? 2 * 24 + 12 : 24 + 7,
    });
    const cast = castText['hook-cast.json'];
    const window_ = (minute, fact) => ({ minute, area: 'ritas', thing: 'rita_window', said: "somebody put Rita's window in",
      witnesses: [{ id: 'darren', rung: 4 }], fact, words: "the new owner put Rita's window in", certainty: 1.0 });   // 'darren' is the prototype's id for the cast's 'sam'

    // ONE SCRIPTED WEEK THROUGH THE BRIDGE. The clock moves in `step` game minutes (any size, fractions
    // too), stopping on each whole hour, as a clock ticked many times a minute does. What he does is the
    // same script as T3's, done at its own minute after the clock has been ticked to it. With saveAfter,
    // the town is saved once that many hours have run (at a minute inside an hour), written out as text,
    // and the week goes on in a FRESH module loaded from that text.
    async function bridgeWeek(run, { talk, step, saveAfter = -1 }) {
      const { from, to } = span(run);
      let town = await openTown({ wasm: brainBytes, castJson: cast, startMinute: from * 60, talk, print: quiet.print });
      if (run === 'held') { town.sim.policeReport('sam', 'player.cut_d0', Offence.Wounding, 4, 0); town.sim.takeIn('player.cut_d0', 0, 14, 0); }
      const due = [], lines = [], rows = [];
      const at = (minute, fn) => due.push([minute, fn]);
      let hours = 0, heldBad = 0, savedBytes = 0, heldAtSave = null, heldAfterLoad = null, ticks = 0, ms = 0;
      const afterHour = (ev) => {
        const { day, hour: hod, minute: H } = ev;
        if (run === 'no' && day === 0 && hod === 21 && town.askDelivered(0)) at(H + 30, () => town.answerAsk(0, NightAnswer.Refused, H + 30));
        if (run === 'days') {
          if (day === 1 && hod === 12) at(H + 30, () => town.deed(window_(H + 30, 'window_d1')));
          if (day === town.teaDay() && (hod === 21 || hod === 22)) { for (let m = 0; m < (hod === 21 ? 60 : 31); m++) at(H + m, () => town.teaMinute(H + m)); }
          else if (hod === 22 && town.asksOn(day) && town.askDelivered(day)) at(H + 30, () => town.answerAsk(day, NightAnswer.Did, H + 30));
        }
        if (run === 'teaday' && day === 0 && hod === 12) at(H + 30, () => town.deed(window_(H + 30, 'window_d0')));
        if (run === 'winddown' && day === town.weekDay() && hod === 10 && town.weekAsksNow(H + 30, true)) {
          at(H + 30, () => town.weekAsk(H + 30));
          at(H + 40, () => town.weekGive(WeekAnswer.WindDown, H + 40));
        }
      };
      const end = (to - 1) * 60;
      for (let t = from * 60; ;) {
        const t0 = performance.now();
        const evs = town.tick(t, 'mickeys');
        ms += performance.now() - t0;
        ticks++;
        for (const ev of evs) {
          hours++;
          lines.push(`${run}|${ev.day}|${ev.hour}|${ev.row}\n`);
          rows.push([`${run}|${ev.day}|${ev.hour}`, ev.row]);
          if ((town.held() !== null) !== ev.held) heldBad++;       // the bridge's own "held" against the hour's answer
          afterHour(ev);
        }
        while (due.length && due[0][0] <= t) due.shift()[1]();
        if (saveAfter >= 0 && !savedBytes && hours >= saveAfter && t % 60 !== 0 && !due.length) {
          heldAtSave = town.held();
          const text = JSON.stringify(town.save());
          savedBytes = text.length;
          town = await openTown({ wasm: brainBytes, castJson: cast, saved: JSON.parse(text), print: quiet.print });
          heldAfterLoad = town.held();
        }
        if (t >= end && !due.length) break;
        t = Math.min(t + step, (Math.floor(t / 60) + 1) * 60, due.length ? due[0][0] : Infinity);
      }
      lines.push(town.sim.state() + '\n' + town.sim.stories() + '\n');
      return { digest: await sha256(lines.join('')), rows, hours, heldBad, savedBytes, heldAtSave, heldAfterLoad, ticks, ms };
    }
    const allWeeks = async (opts) => { const out = {}; for (const run of RUNS) out[run] = await bridgeWeek(run, typeof opts === 'function' ? opts(run) : opts); return out; };
    const against = (weeks) => {
      let rows = 0, bad = 0; const first = [], fields = {};
      for (const run of RUNS) for (const [key, row] of weeks[run].rows) {
        rows++;
        const w = want.get(key);
        if (w === row) continue;
        bad++;
        if (first.length < 4) first.push(`${key}\n       got  ${row}\n       want ${w}`);
        const a = row.split('|'), b = (w ?? '').split('|');
        ['found', 'went', 'ellis', 'taken', 'invite', 'ron', 'tea', 'held', 'asks', 'outfit', 'stories', 'ellisFirst', 'takenFirst'].forEach((name, i) => { if (a[i] !== b[i]) fields[name] = (fields[name] ?? 0) + 1; });
      }
      return { rows, bad, first, fields };
    };
    const sum = (weeks, k) => RUNS.reduce((n, run) => n + weeks[run][k], 0);

    // T8: by the hour, in steps of 7.3 game minutes.
    const hourly = await allWeeks({ talk: 'by the hour', step: 7.3 });
    const h = against(hourly);
    report.T8 = { rows: h.rows, bad: h.bad, tableRows: want.size, heldBad: sum(hourly, 'heldBad') };
    result('T8 the bridge, talk by the hour, gives the C# Core\'s rows', h.rows > 0 && h.bad === 0 && h.rows === want.size && report.T8.heldBad === 0,
      `${h.rows} game hours of the six scripted weeks, the clock ticked in steps of 7.3 game minutes through the bridge (${sum(hourly, 'ticks')} ticks): ` +
      `${h.rows - h.bad} agree with the C# Core's TownWeekHour rows field for field, ${h.bad} differ; the bridge's own "held" disagreed with the hour's answer at ${report.T8.heldBad} hours`);
    for (const b of h.first) log('     ' + b);

    // T9: by the minute, the packaged game's way, in three sizes of step.
    const byStep = {};
    for (const step of [1, 0.37, 7.3]) byStep[step] = await allWeeks({ talk: 'by the minute', step });
    const digestOf = (weeks) => RUNS.map((run) => weeks[run].digest.slice(0, 16)).join(' ');
    const sameTown = digestOf(byStep[1]) === digestOf(byStep[0.37]) && digestOf(byStep[1]) === digestOf(byStep[7.3]);
    const m = against(byStep[1]);
    const perDay = (sum(byStep[1], 'ms') / m.rows) * 24;
    report.T9 = { sameTown, rows: m.rows, differFromHourlyRows: m.bad, fields: m.fields, heldBad: sum(byStep[1], 'heldBad') + sum(byStep[0.37], 'heldBad') + sum(byStep[7.3], 'heldBad'),
      msPerGameDay: Number(perDay.toFixed(3)), ticks: { 1: sum(byStep[1], 'ticks'), 0.37: sum(byStep[0.37], 'ticks'), 7.3: sum(byStep[7.3], 'ticks') } };
    report.bridge = { digest: (await sha256(digestOf(byStep[1]))).slice(0, 16) };
    result('T9 the bridge, talk by the minute, gives the same town whatever the clock\'s steps', sameTown && m.rows === want.size && report.T9.heldBad === 0,
      `the six weeks with the clock ticked every game minute, every 0.37 and every 7.3 (${report.T9.ticks[1]}, ${report.T9.ticks[0.37]} and ${report.T9.ticks[7.3]} ticks): ` +
      `${sameTown ? 'the same digest of every hour, final state and held story in all three' : 'DIFFERENT towns: ' + [1, 0.37, 7.3].map((k) => digestOf(byStep[k])).join(' / ')}; ` +
      `the bridge's own "held" disagreed with the hour's answer at ${report.T9.heldBad} hours`);
    log(`info T9 by the minute against the C# Core's rows (which are played by the hour): ${m.rows - m.bad} of ${m.rows} hours identical, ${m.bad} differ` +
      (m.bad ? `, by field ${JSON.stringify(m.fields)}` : '') + `. A measurement, not a check: the order of talk and steps inside an hour is the game's here, the reference week's there.`);
    for (const b of m.first.slice(0, 2)) log('     ' + b);
    log(`info T9 speed: the bridge's ticks cost ${perDay.toFixed(2)} ms a game day when ticked every game minute (the Hook's cast)`);

    // T10: a save in the middle of each week.
    const saveAfter = (run) => Math.floor((span(run).to - span(run).from) * 0.4);
    const reloaded = await allWeeks((run) => ({ talk: 'by the minute', step: 7.3, saveAfter: saveAfter(run) }));
    const sameAfterLoad = RUNS.filter((run) => reloaded[run].digest === byStep[7.3][run].digest && reloaded[run].savedBytes > 0);
    const heldKept = reloaded.held.heldAtSave !== null && reloaded.held.heldAfterLoad !== null && reloaded.held.heldAtSave.until === reloaded.held.heldAfterLoad.until;
    const biggest = Math.max(...RUNS.map((run) => reloaded[run].savedBytes));
    report.T10 = { weeks: RUNS.length, same: sameAfterLoad.length, heldKept, biggestSaveChars: biggest, savedAfterHours: Object.fromEntries(RUNS.map((run) => [run, saveAfter(run)])) };
    result('T10 a saved town, loaded into a fresh module, plays on the same', sameAfterLoad.length === RUNS.length && heldKept,
      `each of the six weeks saved after two fifths of its hours (as text, at a minute inside an hour) and played on in a fresh module: ${sameAfterLoad.length} of ${RUNS.length} end as the ` +
      `week played straight through (same digest); in the cells at the save, he is still held after the load until the same minute: ${heldKept ? 'yes' : 'NO'}; the biggest save is ${biggest} characters`);

    // T11: rough handling of the bridge.
    const problems = [];
    const refuses = async (what, fn, word) => {
      try { await fn(); problems.push(`${what}: accepted`); }
      catch (e) { if (!String(e.message).includes(word)) problems.push(`${what}: refused with other words, ${String(e.message).slice(0, 100)}`); }
    };
    const fresh = () => openTown({ wasm: brainBytes, castJson: cast, startMinute: 936, print: quiet.print });   // Monday 15:36, where the prototype's week starts
    const town = await fresh();
    const first = town.tick(936.4);
    if (first.length !== 0) problems.push(`a week that starts at 15:36 ran ${first.length} hour(s) before sixteen o'clock`);
    const two = town.tick(17 * 60 + 5);
    if (two.map((e) => e.hour).join() !== '16,17') problems.push(`a jump from 15:36 to 17:05 gave hours ${two.map((e) => e.hour).join()}, not 16,17`);
    await refuses('a clock that goes back', () => town.tick(900), 'went back');
    await refuses('a clock that is no number', () => town.tick(NaN), 'not a number');
    await refuses('a clock with no end', () => town.tick(Infinity), 'not a number');
    await refuses('a clock that jumps a thousand years', () => town.tick(1000 * 366 * 1440), 'more than a year');
    await refuses('an act in an hour the clock has not reached', () => town.answerAsk(0, NightAnswer.Did, 19 * 60 + 30), 'tick the clock');
    await refuses('an act before the town\'s clock', () => town.saw({ minute: 100, who: 'ron', rung: 3, fact: 'x_d0', area: 'mickeys', words: 'x' }), 'before the town');
    if (town.saw({ minute: 17 * 60 + 5, who: 'nobody_at_all', rung: 3, fact: 'seen_d0', area: 'mickeys', words: 'somebody saw him' }) !== false) problems.push('a sighting by nobody in the cast was taken');
    const knewBefore = town.knows().length;
    if (town.saw({ minute: 17 * 60 + 5, who: 'ron', rung: 3, fact: 'seen_d0', area: 'mickeys', words: 'Ron saw him on the rank' }) !== true) problems.push('a sighting by Ron (the prototype\'s id) was not taken');
    const ronKnows = town.knows().filter((f) => f.who === PROTOTYPE_TO_CAST.ron && f.topic === 'player.seen_d0');
    if (town.knows().length !== knewBefore + 1 || ronKnows.length !== 1 || ronKnows[0].saw !== true || ronKnows[0].rung !== 3) problems.push(`Ron's sighting is not in the Ledger's facts as his own, at a face: ${JSON.stringify(ronKnows).slice(0, 160)}`);
    if (town.placeOf('ron', 12 * 60) !== town.placeOf('rocco', 12 * 60) || town.placeOf('ron', 12 * 60) === '') problems.push('the prototype\'s id for Ron does not reach his routine');
    if (town.placeOf('nobody_at_all', 12 * 60) !== '') problems.push('somebody not in the cast has a place');
    const t0 = performance.now();
    const month = town.tick(30 * 1440 + 17 * 60 + 5);
    const jumpMs = performance.now() - t0;
    if (month.length !== 30 * 24) problems.push(`a jump of thirty days gave ${month.length} hours, not 720`);
    const good = town.save();
    await refuses('a save that is no save', () => openTown({ wasm: brainBytes, castJson: cast, saved: { hello: 1 } }), 'not a saved town');
    await refuses('a save from a later version', () => openTown({ wasm: brainBytes, castJson: cast, saved: { ...good, v: BRIDGE_SAVE_VERSION + 1 } }), 'this build reads');
    await refuses('a save made with another cast', () => openTown({ wasm: brainBytes, castJson: castText['quay-cast.json'], saved: good }), 'another cast');
    await refuses('a save with a piece missing', () => openTown({ wasm: brainBytes, castJson: cast, saved: { ...good, texts: { ...good.texts, town: undefined } } }), 'not whole');
    await refuses('a save whose week\'s pieces are from a later version', () => openTown({ wasm: brainBytes, castJson: cast, saved: { ...good, texts: { ...good.texts, town: '{"version":99}' } } }), 'version');
    await refuses('a save whose talk is cut short', () => openTown({ wasm: brainBytes, castJson: cast, saved: { ...good, texts: { ...good.texts, agents: good.texts.agents.slice(0, 200) } } }), 'not whole');
    await refuses('a save whose talk is cut short inside, braces whole', () => openTown({ wasm: brainBytes, castJson: cast, saved: { ...good, texts: { ...good.texts, agents: good.texts.agents.slice(0, 200) + '}' } } }), 'not a whole');
    await refuses('a save whose week is no object', () => openTown({ wasm: brainBytes, castJson: cast, saved: { ...good, texts: { ...good.texts, town: '[]' } } }), 'not whole');
    // And the good save itself still loads, twice over, and comes out as the same text: saving is not a one-way street.
    const again = await openTown({ wasm: brainBytes, castJson: cast, saved: JSON.parse(JSON.stringify(good)), print: quiet.print });
    if (JSON.stringify(again.save()) !== JSON.stringify(good)) problems.push('a town saved, loaded and saved again does not give the same save');
    await refuses('no cast file', () => openTown({ wasm: brainBytes, castJson: '' }), 'no cast file');
    await refuses('a broken cast file', () => openTown({ wasm: brainBytes, castJson: '{not json' }), 'cast not read');
    report.T11 = { problems, jumpThirtyDaysMs: Math.round(jumpMs) };
    result('T11 the bridge takes rough handling', problems.length === 0, problems.length ? problems.join('; ')
      : `a week starting at 15:36, a jump over two hours, a sighting by nobody, the prototype's own ids, a thirty-day jump (720 hours, ${Math.round(jumpMs)} ms), ` +
        `a save loaded and saved again, and sixteen things that must be refused (four clocks, two acts out of turn, eight saves, two cast files): all as they should be`);
  }

  if (printed.length) log(`info the modules printed ${printed.length} line(s); first: ${printed[0].slice(0, 120)}`);
  report.failed = failed;
  report.results = results;
  return report;
}
