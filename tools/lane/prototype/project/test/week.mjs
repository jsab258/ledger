// One full week, Monday to Friday, played through the test hook alone (no key presses), as a player might:
// the written scenes, talks by suggested lines and typed words, the night job to its drop door, the tin
// through Sheila's book, a fare, sleep, the rent, a debt, the Ledger opened and the playtest asks answered.
// Writes the measures JSON to out/measures.json and prints what happened.
//   node test/week.mjs [low|medium]
import fs from 'fs';
import { launch, sleep } from './harness.mjs';

const h = await launch({ port: 8795, quality: process.argv[2] || 'low', width: 1280, height: 720 });
const { ev } = h;
const L = (fn, ...a) => ev(fn, ...a);
const log = (...a) => console.log(...a);
const said = [];

// Answer whatever box is up until the game runs again: read written lines on, take choice n, and in a talk
// take the decision (or leave). Returns what it met.
async function clear(o = {}) {
  const met = [];
  for (let i = 0; i < 80; i++) {
    await h.step(0.2);
    const r = await L(() => { const r = LEDGER.read(); return { box: r.boxOpen, paused: r.paused, why: r.pausedBecause, w: LEDGER.written.read(), t: LEDGER.talk.state(), lines: LEDGER.talk.lines() }; });
    if (r.box === 'dialog' && r.w.open) {
      met.push((r.w.speaker || '') + ': ' + r.w.text.slice(0, 60) + (r.w.choices ? ' [' + r.w.choices.join(' | ') + ']' : ''));
      if (r.w.choices) await L((n) => LEDGER.written.choose(n), Math.min(o.choice || 0, r.w.choices.length - 1));
      else await L(() => LEDGER.written.next());
    } else if (r.box === 'talk') {
      if (r.t.waitingForTheReply) { await L(() => LEDGER.talk.idle()); continue; }
      if (r.t.deciding) {
        const a = await L((what, n) => LEDGER.talk.answer(what, n), o.answer || 'yes', o.proposal || 0);
        met.push('decided ' + r.t.deciding + ': ' + (a.said || []).join(' / '));
        if (!a.answered) await L(() => LEDGER.talk.leave());
      } else {
        const x = await L(() => LEDGER.talk.say('leave'));
        if (!x) await L(() => LEDGER.talk.leave());
      }
      await sleep(120);
    } else if (r.paused) await sleep(150);
    else {
      await sleep(60); await h.step(0.2);
      if (!(await L(() => LEDGER.read().paused))) return met;
    }
  }
  return met;
}
const clock = () => L(() => { const r = LEDGER.read(); return r.date + ' ' + r.clock; });
const money = () => L(() => { const m = LEDGER.read().money; return `pocket ${m.pocketPence}p, tin ${m.tinPence}p`; });
// a talk by suggested lines: greet, then whatever is asked, a personal line, and leave
async function chat(id, o = {}) {
  await clear();
  await L((id) => LEDGER.talk.open(id), id); await h.step(0.3);
  if ((await L(() => LEDGER.read().boxOpen)) === 'dialog') { await clear(); await L((id) => LEDGER.talk.open(id), id); }
  const t0 = await L(() => LEDGER.talk.state());
  if (!t0.open) return log('  no talk with', id);
  if (o.unfold) await L(() => LEDGER.talk.key('F2'));
  const out = [];
  for (const job of o.jobs || ['greet', 'personal', 'leave']) {
    const st = await L(() => LEDGER.talk.idle());
    if (!st.open) break;
    if (st.deciding) { const a = await L((w) => LEDGER.talk.answer(w), o.answer || 'no'); out.push(`(${st.deciding}: ${(a.said || []).join(' / ')})`); }
    if (job === 'type') { await L((x) => LEDGER.talk.type(x), o.words || 'What do they say about me on this street?'); out.push('typed'); continue; }
    const r = await L((j) => LEDGER.talk.say(j), job);
    if (r) out.push(r.said);
  }
  if ((await L(() => LEDGER.talk.state())).open) await L(() => LEDGER.talk.leave());
  if (o.unfold) await L(() => { if (LEDGER.talk.state().open) LEDGER.talk.key('F2'); });
  await clear();
  log(`  talk with ${t0.shownAs}: ${out.join(' | ')}`);
}
// open the Ledger, look at each part for a moment, answer the ask if one is up, close
async function ledgerVisit(o = {}) {
  await clear();
  const r = await L((p) => LEDGER.ledger.open(p, 'keyboard'), o.part);
  if (!r.open) return log('  the Ledger would not open');
  await sleep(o.ms || 400);
  if (r.ask) {
    let found = null;
    // look for the fact as a player would: part by part, page by page, marking the row that answers it
    for (let part = 0; part < 4 && !found; part++) {
      const pages = (await L(() => LEDGER.ledger.read().part)) === 'people' ? (await L(() => LEDGER.ledger.pages().length)) : (await L(() => LEDGER.ledger.read().part)) === 'daybook' ? (await L(() => LEDGER.read().dayIndex + 1)) : 1;
      for (let pg = 0; pg < pages && !found; pg++) {
        const rows = await L(() => LEDGER.ledger.rows());
        for (const row of rows) {
          const want = /bus/.test(r.ask) ? row.kind === 'belief' && /got off the bus/.test(row.what + ' ' + JSON.stringify(row)) || (row.kind === 'belief' && row.sourceEvent === (await L(() => (LEDGER.G.events.find((e) => e.kind === 'arrive') || {}).id)))
            : /rent/.test(r.ask) ? row.kind === 'open' && /^Rent/.test(row.what)
            : /Ron Kirby call/.test(r.ask) ? row.kind === 'call' && row.who === 'ron' && !row.struckThrough
            : row.sum === 'tin';
          if (want) { const m = await L((i) => LEDGER.ledger.mark(i, 'keyboard'), row.row); if (/That is the one/.test(m.said)) { found = row.what; break; } }
        }
        if (!found) await L(() => LEDGER.ledger.key('ArrowRight', 'keyboard'));
        await sleep(120);
      }
      if (!found) await L(() => LEDGER.ledger.key('KeyE', 'keyboard'));
    }
    log(`  ask "${r.ask}" -> ${found ? 'found: ' + found : 'NOT FOUND'}`);
  }
  await L(() => LEDGER.ledger.close());
}
const sleepTill = async (label) => { // the bed at Regent House, by its prompt and its written choices
  await clear();
  await L(() => LEDGER.goInside('the bed at Regent House')); await h.step(0.4);
  const p = await L(() => LEDGER.prompts());
  await L(() => LEDGER.press('E')); await h.step(0.3);
  const w = await L(() => LEDGER.written.read());
  if (!w.open || !w.choices) return log('  no bed menu', JSON.stringify(p), JSON.stringify(w).slice(0, 100));
  const n = w.choices.findIndex((c) => c.includes(label));
  await L((n) => LEDGER.written.choose(n), n < 0 ? w.choices.length - 2 : n);
  for (let i = 0; i < 60; i++) { await sleep(150); await h.step(0.1); if (!(await L(() => LEDGER.read().paused))) break; }
  await clear();
};
const runTo = async (gameMinute, o = {}) => { // let the game run to a time, answering whatever comes up
  for (let i = 0; i < 4000; i++) {
    const r = await L(() => LEDGER.read());
    if (r.gameMinute >= gameMinute || r.weekEnded) return;
    if (r.paused) { const m = await clear(o); if (m.length) said.push(...m); continue; }
    await h.step(o.step || 4);
  }
};

try {
  await h.newWeek();
  log('START', await clock(), await money());
  // ---------------- Monday ----------------
  await L(() => LEDGER.goTo('the rank')); await h.step(1.5);
  log(' rank:', (await clear()).length, 'lines read');
  await L(() => LEDGER.talk.open('darren')); await h.step(0.5);
  log(' the lad with the pager:', (await clear()).length, 'lines read');
  await L(() => LEDGER.goTo("Mickey's Cars (street door)")); await h.step(0.5);
  log(' prompts at the door:', JSON.stringify(await L(() => LEDGER.prompts())));
  await L(() => LEDGER.goInside("Mickey's Cars")); await h.step(1); await clear();
  // Sheila's first scene: she reads him the book
  await L(() => { const G = LEDGER.G, P = G.people.sheila, t = G.tom; t.x = P.x; t.z = P.z + 1.9; t.ang = Math.PI; }); await h.step(0.5);
  log(' prompts by Sheila:', JSON.stringify(await L(() => LEDGER.prompts())));
  await L(() => LEDGER.press('E')); await h.step(0.3);
  const tour = await clear();
  log(' Sheila reads the book:', tour.length, 'lines;', tour.filter((x) => /decided/.test(x)).join('; '));
  log(' flags', JSON.stringify(await L(() => { const f = LEDGER.read().story.flags; return { tour: f.tour, metRon: f.metRon }; })), await money());
  await L(() => LEDGER.goOutside());
  await chat('brenda'); await chat('grace', { unfold: true, answer: 'yes' }); await chat('albert', { jobs: ['greet', 'type', 'leave'] });
  await ledgerVisit({ part: 'people', ms: 900 });
  // Ron's ask at twenty past five: the job is offered and taken
  await runTo(17.4 * 60);
  await L(() => LEDGER.goOutside()); await h.step(1);
  log(' Ron is', JSON.stringify(await L(() => { const p = LEDGER.person('ron'); return [p.place, p.doing, p.walking]; })));
  await L(() => LEDGER.talk.open('ron')); await h.step(0.4);
  log(' Ron asks:', (await clear({ answer: 'yes' })).filter((x) => /decided/.test(x)).join('; '), '| job', JSON.stringify(await L(() => LEDGER.job.read())).slice(0, 160));
  await L(() => LEDGER.goInside("the coat hook at Mickey's")); await h.step(0.4);
  log(' at the hook:', JSON.stringify(await L(() => LEDGER.prompts())));
  await L(() => LEDGER.press('E')); await h.step(0.3); await clear(); await L(() => LEDGER.press('C'));
  await L(() => LEDGER.goOutside());
  await runTo(22.7 * 60);
  // the night job: pick up at the shelter, carry it, knock at the drop door
  await L(() => LEDGER.job.goToPickUp()); await h.step(1);
  log(' at the pick-up:', JSON.stringify(await L(() => LEDGER.prompts())), await clock());
  await L(() => LEDGER.press('E')); await h.step(1.5);
  for (const [x, z] of [[-30, 43], [-7, 43], [-6.4, 30], [-6.4, 0], [-6.4, -20], [-21, -24.5]]) { await L((x, z) => LEDGER.goTo({ xMetres: x, zMetres: z }), x, z); await h.step(2.5); }
  await L(() => LEDGER.job.goToDrop()); await h.step(0.6);
  log(' at the drop door:', JSON.stringify(await L(() => LEDGER.prompts())));
  await L(() => LEDGER.press('E')); await h.step(0.5); await clear();
  log(' after the drop:', await money(), JSON.stringify(await L(() => LEDGER.job.read())).slice(0, 80));
  await L(() => LEDGER.press('C'));
  await ledgerVisit({ part: 'daybook', ms: 1200 });
  await sleepTill('morning');
  log('TUESDAY', await clock(), await money());
  // ---------------- Tuesday: wash the tin, the first ask, a fare ----------------
  await runTo(1440 + 9.6 * 60);
  await ledgerVisit({ ms: 600 });
  await L(() => LEDGER.goInside("Mickey's Cars"));
  await L(() => LEDGER.talk.open('sheila'));
  await L(() => LEDGER.talk.say('greet'));
  const wash = await L(() => LEDGER.talk.state());
  log(' Sheila raises:', wash.deciding);
  const wa = await L(() => LEDGER.talk.answer('yes')); await h.step(0.3); await clear();
  log(' washed:', (wa.said || []).join(' / '), '|', await money());
  await L(() => LEDGER.goOutside());
  // a fare: take the cab, have Pauline call, accept, pick up, drop off
  await L(() => { LEDGER.G.car.keys = LEDGER.G.car.keys || true; });
  log(' in the cab:', await L(() => LEDGER.cab.getIn()));
  const offer = await L(() => LEDGER.fare.call());
  log(' fare offered:', JSON.stringify(offer).slice(0, 220));
  await L(() => LEDGER.fare.accept()); await h.step(0.5);
  await L(() => LEDGER.fare.pickUp()); await h.step(1);
  log(' picked up:', JSON.stringify(await L(() => LEDGER.fare.read().state)));
  const drop = await L(() => LEDGER.fare.dropOff()); await h.step(0.5); await clear();
  log(' dropped off:', JSON.stringify(drop).slice(0, 160), '|', await money());
  await L(() => LEDGER.cab.driveTo(4.1, 37.4)); await L(() => LEDGER.cab.getOut());
  await chat('kevin'); await chat('ron', { answer: 'no' }); await chat('darren', { unfold: true, answer: 'no' });
  await runTo(1440 + 17.2 * 60);
  await L(() => LEDGER.goOutside()); await L(() => LEDGER.talk.open('ron')); await h.step(0.4);
  log(' Tuesday parcel:', (await clear({ answer: 'no' })).filter((x) => /decided/.test(x)).join('; '));
  await sleepTill('morning');
  log('WEDNESDAY', await clock(), await money());
  // ---------------- Wednesday: a debt collected, tea with Ada ----------------
  await chat('lee', { jobs: ['greet', 'leave'], answer: 'yes' });
  await chat('lee', { jobs: ['greet', 'leave'], answer: 'yes' });
  log(' debts:', JSON.stringify(await L(() => LEDGER.read().debts)).slice(0, 300), await money());
  await runTo(2 * 1440 + 12.2 * 60);
  await ledgerVisit({ ms: 500 });
  await chat('walsh'); await chat('june');
  await runTo(2 * 1440 + 18.9 * 60, { answer: 'no', proposal: 1 });
  await L(() => LEDGER.goTo({ xMetres: -6.4, zMetres: 30.6 })); await h.step(0.5);
  log(' at Ada\'s door:', JSON.stringify(await L(() => LEDGER.prompts())));
  await L(() => LEDGER.press('E')); await h.step(0.5); await clear();
  await sleepTill('morning');
  log('THURSDAY', await clock(), await money());
  // ---------------- Thursday: the rent, the third ask ----------------
  await runTo(3 * 1440 + 10.2 * 60);
  await ledgerVisit({ ms: 500 });
  await L(() => LEDGER.goInside('Regent House')); await L(() => LEDGER.talk.open('sylvia')); await h.step(0.3);
  if ((await L(() => LEDGER.read().boxOpen)) === 'dialog') { log(' Mrs Rennison, first meeting:', (await clear()).length, 'lines read'); await L(() => LEDGER.talk.open('sylvia')); }
  await L(() => LEDGER.talk.say('greet'));
  log(' Mrs Rennison raises:', (await L(() => LEDGER.talk.state())).deciding);
  const rent = await L(() => LEDGER.talk.answer('keep')); const rent2 = await L(() => LEDGER.talk.answer('yes')); await clear();
  log(' rent:', (rent.said || []).concat(rent2.said || []).join(' / '), '|', await money(), '| flag', await L(() => LEDGER.read().story.flags.rent));
  await L(() => LEDGER.goOutside());
  await chat('ada'); await chat('sheila', { answer: 'no' });
  await ledgerVisit({ part: 'open', ms: 700 });
  await sleepTill('morning');
  log('FRIDAY', await clock(), await money());
  // ---------------- Friday: the last ask, Sheila's question ----------------
  await runTo(4 * 1440 + 9.2 * 60);
  await ledgerVisit({ ms: 500 });
  await runTo(4 * 1440 + 16.2 * 60);
  await L(() => LEDGER.goInside("Mickey's Cars"));
  await L(() => { const G = LEDGER.G, P = G.people.sheila, t = G.tom; t.x = P.x; t.z = P.z + 1.9; }); await h.step(0.5);
  log(' prompts by Sheila on Friday:', JSON.stringify(await L(() => LEDGER.prompts())));
  await L(() => LEDGER.press('E')); await h.step(0.5);
  const end = await clear({ answer: 'yes', proposal: 0 });
  log(' the end:', end.filter((x) => /decided/.test(x)).join('; '));
  for (let i = 0; i < 40 && !(await L(() => LEDGER.read().weekEnded)); i++) { await sleep(200); await h.step(0.2); await clear(); }
  await sleep(2500);
  const m = await L(() => LEDGER.measures());
  fs.mkdirSync('out', { recursive: true });
  fs.writeFileSync('out/measures.json', JSON.stringify(m, null, 2));
  const { visits, noted, ...top } = m;
  log('ENDED', await L(() => LEDGER.read().weekEnded), await clock());
  log('MEASURES', JSON.stringify(Object.assign({}, top, { findTheFact: { keyboard: top.findTheFact.keyboard, pad: top.findTheFact.pad, asks: top.findTheFact.asks.map((a) => `${a.id}: ${a.state}${a.found != null ? (a.found ? ' found in ' + a.realSecondsFromOpenToEntry + 's' : ' not found') : ''}`) } }), null, 1));
  const bookOut = await L(() => LEDGER.ledger.book());
  fs.writeFileSync('out/book.json', JSON.stringify(bookOut, null, 1));
  const bad = bookOut.filter((e) => /\b(I|me|my|myself|mine)\b/.test(e.what) || e.what.split(/\s+/).length > 22);
  log('ENTRIES', bookOut.length, '| with I or me, or over 22 words:', bad.length, bad.slice(0, 5).map((e) => e.what).join(' || '));
  log('PAUSE FAULTS', await L(() => LEDGER.pauseFaults()), '| pauses logged', await L(() => LEDGER.pauses().length));
} catch (e) { log('TEST FAIL', String(e.stack || e).slice(0, 900)); try { log('state', JSON.stringify(await L(() => { const r = LEDGER.read(); return { clock: r.clock, date: r.date, paused: r.paused, why: r.pausedBecause, box: r.boxOpen }; }))); } catch (e2) { /* */ } }
log('ERRORS', h.errors.length, [...new Set(h.errors)].slice(0, 8).join('\n  '));
await h.close();
