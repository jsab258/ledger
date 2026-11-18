// The hook's two checks, run as tests:
//   1. arrivals: every named person who sets off for a place gets there (Tuesday night, Tom at the rank: the
//      night Ron used to stand three metres from the rank until morning);
//   2. the same check must catch a person who is held on the spot (so we know it can fail);
//   3. nights: Tuesday and Wednesday night with Tom out on the street: every pause has a resume.
import { launch } from './harness.mjs';
const h = await launch({ port: 8796 });
const L = (fn, ...a) => h.ev(fn, ...a);
const log = (...a) => console.log(...a);
let ok = true;
try {
  await h.newWeek();
  // past the first meetings, so the nights are ordinary nights
  await L(() => { const f = LEDGER.G.story.flags; Object.assign(f, { tour: 1, metRon: 1, metDarren: 1, metPauline: 1, metJune: 1, metSylvia: 1, metWalsh: 1, ask1: 'no', unpacked: 1 }); LEDGER.G.story.lastSleepDay = 9; });
  const a = await L(() => LEDGER.check.arrivals({ fromGameMinute: 1440 + 22 * 60, forGameHours: 9, tomAt: 'the rank' }));
  log('ARRIVALS Tue night, Tom at the rank:', JSON.stringify({ from: a.from, until: a.until, walksSetOff: a.walksSetOff, walksArrived: a.walksArrived, walksGivenUp: a.walksGivenUpForAnotherPlace, toOrFromTheMapEdge: a.ofThoseToOrFromTheMapEdge, longestWalkGameMinutes: a.longestWalkGameMinutes, stoodStill: a.stoodStill, pauseNeverEnded: a.pauseNeverEnded, ok: a.ok }));
  for (const f of a.gaveUp) log('   gave up:', f.person, '|', f.from, '->', f.goingTo, '|', f.setOffAt, '|', f.fault, f.involvesTheMapEdge ? '| map edge' : '');
  log(' Ron at the end:', JSON.stringify(await L(() => { const p = LEDGER.person('ron'); return { place: p.place, walking: p.walking, doing: p.doing }; })));
  ok = ok && a.ok;
  // the check must be able to fail: hold somebody on the spot and see that it says so
  await L(() => { const G = LEDGER.G; G.story.lastSleepDay = 9; });
  const b = await L(async () => { const G = LEDGER.G; const P = G.people.kevin; P.pauseT = 1e9; const r = await LEDGER.check.arrivals({ forGameHours: 14, stoodStillRealSeconds: 30 }); P.pauseT = 0; return r; });
  log('SELF-TEST (Kevin held on the spot):', JSON.stringify({ walksSetOff: b.walksSetOff, stoodStill: b.stoodStill.map((f) => f.person + ': ' + f.fault), ok: b.ok }));
  const caught = b.stoodStill.some((f) => f.personId === 'kevin') && !b.ok;
  log(caught ? ' the check caught him' : ' THE CHECK DID NOT CATCH HIM');
  ok = ok && caught;
} catch (e) { ok = false; log('TEST FAIL', String(e.stack || e).slice(0, 700)); }
log('ERRORS', h.errors.length, h.errors.slice(0, 4).join('\n '));
await h.close();

// a fresh week for the nights check
const g = await launch({ port: 8797 });
try {
  await g.newWeek();
  await g.ev(() => { const f = LEDGER.G.story.flags; Object.assign(f, { tour: 1, metRon: 1, metDarren: 1, metPauline: 1, metJune: 1, metSylvia: 1, metWalsh: 1, ask1: 'yes', job1: 'done', unpacked: 1 }); LEDGER.G.tom.hasCoat = true; });
  const n = await g.ev(() => LEDGER.check.nights({}));
  for (const N of n.nights) {
    log(`NIGHT ${N.night}: ${N.from} to ${N.until}, Tom at ${N.tomAt}. ${N.pauses.length} pauses, ${N.pausesWithNoResume.length} with no resume.`);
    for (const p of N.pauses) log(`   ${p.at}  ${p.reason}  ->  ${p.resumed ? p.resumedBecause + ' (' + p.realSecondsPaused + ' s)' : 'NO RESUME'}`);
  }
  log('NIGHTS', JSON.stringify({ pauseNeverEnded: n.pauseNeverEnded, watchdogFaults: n.watchdogFaults, ok: n.ok, now: n.now }));
  ok = ok && n.ok;
} catch (e) { ok = false; log('TEST FAIL', String(e.stack || e).slice(0, 700)); }
log('ERRORS', g.errors.length, g.errors.slice(0, 4).join('\n '));
await g.close();
log(ok ? 'PASS' : 'FAIL');
