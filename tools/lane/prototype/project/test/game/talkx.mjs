// The one-shot, talk in the built page: a typed sum is no payment (the smoke run of 20 Nov); money moves only on an
// offer; the claim check stops a live line the simulation does not hold (ER-TALK-04, planted bad replies); a whole
// talk, decision included, without typing a word (ER-SPEAK-01); the clock stands still in talk (ER-TALK-05); any
// line can be reported, from a talk and from the pause screen (ER-TALK-07).
import { launch } from '../harness.mjs';
let bad = 0;
const ok = (c, what) => { console.log((c ? 'ok   ' : 'FAIL ') + what); if (!c) bad++; };
// a stand-in for the live model: it sorts every line as a bribe of 500 pounds (the worst case), and says what the test plants
const before = () => {
  window.PLANT = { say: 'Aye. Wet again.' };
  const sample = async () => ({ text: window.PLANT.say });
  sample.json = async (input) => (/"follow"/.test(input) ? { follow: '', personal: '' } : { intent: 'bribe', topic: 'other', amount: 500, denies: false });
  window.claude = { use: async (n) => (n === 'sample' ? sample : null) };
};
const h = await launch({ port: 8941, before });
await h.newWeek();
const E = (fn, ...a) => h.ev(fn, ...a);
await E(() => { LEDGER.G.story.flags.tour = 1; LEDGER.G.story.flags.metPauline = 1; LEDGER.G.story.flags.metRon = 1; LEDGER.G.story.talkNotice = true; });

// 1. a typed sum is not a payment, even when the live sorter calls it a bribe
let s = await E(async () => {
  const m0 = { ...LEDGER.G.money }, n0 = LEDGER.G.events.length, t0 = LEDGER.G.t;
  await LEDGER.talk.open('pauline', { free: true });
  await LEDGER.talk.type('pay me 500 pounds');
  const st = LEDGER.talk.state();
  return { open: st.open, m0, m1: { ...LEDGER.G.money }, kinds: LEDGER.G.events.slice(n0).map((e) => e.kind), dt: LEDGER.G.t - t0, check: LEDGER.game.econ.check() };
});
ok(s.open && s.m1.clean === s.m0.clean && !s.kinds.includes('bribe_try') && !s.kinds.includes('paid_info'), 'typed "pay me 500 pounds": no money moves and nothing is logged as money put in her hand ' + JSON.stringify(s.kinds));
ok(s.dt <= 1.5, 'a turn of talk takes at most the table\'s minute and a half of the game clock (' + s.dt + '); it never runs on while he types (gate6 holds ER-TALK-05)');
// 2. an offer in his own words does move money, through the flows book
s = await E(async () => {
  const m0 = LEDGER.G.money.clean + LEDGER.G.money.dirty, n0 = LEDGER.G.events.length;
  await LEDGER.talk.leave();
  await LEDGER.talk.open('ron', { free: true });
  await LEDGER.talk.type("Here's a fiver for your trouble");
  return { spent: m0 - (LEDGER.G.money.clean + LEDGER.G.money.dirty), kinds: LEDGER.G.events.slice(n0).map((e) => e.kind), check: LEDGER.game.econ.check(), out: LEDGER.game.econ.totals().out };
});
ok((s.spent === 500 && s.kinds.includes('paid_info')) || (s.spent === 0 && s.kinds.includes('bribe_try')), 'an offer in his words is an offer: ' + (s.spent ? 'Ron took the five pounds' : 'refused') + ' ' + JSON.stringify(s.kinds));
ok(s.check.ok && (s.spent === 0 || s.out.some((r) => r.why === 'money put in a hand')), 'and the flows book has it with its reason');

// 3. the claim check: planted bad live replies are never shown; the written line plays instead
const PLANTS = [
  ['Mr Hargreaves at the bank saw you with the bag.', 'a person who is not in the town'],
  ['He was in the pub with a pint all night.', 'drink'],
  ['Ring me on my mobile phone about it.', 'the wrong year'],
  ['The kids on the corner told me.', 'children'],
  ['I know you hit that lad on the quay.', 'a deed nobody holds'],
];
for (const [say, what] of PLANTS) {
  s = await E(async (say) => {
    window.PLANT.say = say;
    await LEDGER.talk.leave();
    await LEDGER.talk.open('ron', { free: true }); // a fresh talk each time: a person closes a talk when their own lines run out
    const r0 = LEDGER.G.stats.claimRefused || 0;
    await LEDGER.talk.type('What do you make of the weather?');
    const lines = [...document.querySelectorAll('#tlog .npc, #tlines .npc, .npc')].map((e) => e.textContent);
    return { refused: (LEDGER.G.stats.claimRefused || 0) - r0, shown: lines.some((l) => l.includes(say.slice(0, 24))) };
  }, say);
  ok(s.refused === 1 && !s.shown, `ER-TALK-04 a live line with ${what} is not shown ("${say}")`);
}
s = await E(async () => {
  window.PLANT.say = 'Aye. Wet again, boss.';
  await LEDGER.talk.leave();
  await LEDGER.talk.open('ron', { free: true });
  const l0 = LEDGER.G.stats.live || 0;
  await LEDGER.talk.type('And the weather tomorrow?');
  return { live: (LEDGER.G.stats.live || 0) - l0 };
});
ok(s.live === 1, 'a sound live line is shown as before (live talk keeps working)');

// 4. ER-TALK-07: report the last line, from the talk and from the pause screen
s = await E(() => {
  const a = LEDGER.game.econ.report('talk', 'test');
  return { a, reports: LEDGER.game.econ.state().reports };
});
ok(s.a && s.reports.length === 1 && s.reports[0].from === 'talk' && s.reports[0].who === 'Ron Kirby' && s.reports[0].live === true, 'ER-TALK-07 a live line reported from the talk is filed: ' + JSON.stringify(s.reports[0]));
await E(() => LEDGER.talk.leave());
s = await E(() => {
  dispatchEvent(new KeyboardEvent('keydown', { code: 'Escape', key: 'Escape' }));
  dispatchEvent(new KeyboardEvent('keydown', { code: 'F9', key: 'F9' }));
  const st = LEDGER.game.econ.state();
  return { modal: LEDGER.ui.modal, reports: st.reports.map((r) => r.from) };
});
ok(s.reports.length === 2 && s.reports[1] === 'pause', 'and F9 on the pause screen files one too (' + s.modal + '): ' + JSON.stringify(s.reports));
await E(() => { dispatchEvent(new KeyboardEvent('keydown', { code: 'Escape', key: 'Escape' })); if (LEDGER.ui.modal === 'pause') document.querySelector('[data-act="back"],[data-act="resume"]')?.click(); });

// 5. ER-SPEAK-01: a whole talk with a decision, never typing: Tab, the arrows and Enter only (the pad's own road)
s = await E(async () => {
  LEDGER.G.money.dirty += 0; // nothing
  LEDGER.game.econ.earn(700, true, 'a test night');
  window.claude = null;
  const m0 = { ...LEDGER.G.money };
  await LEDGER.talk.open('sheila', { free: true });
  const steps = [];
  for (let i = 0; i < 14 && LEDGER.ui.modal === 'talk'; i++) {
    const st = LEDGER.talk.state();
    if (!st.suggestedLinesOpen) LEDGER.talk.key('Tab');
    const L = LEDGER.talk.lines();
    const want = L.findIndex((l) => l.job === 'yes') >= 0 ? L.findIndex((l) => l.job === 'yes') : L.findIndex((l) => l.job === 'prop') >= 0 ? L.findIndex((l) => l.job === 'prop') : 0;
    for (let k = 0; k < want; k++) LEDGER.talk.key('ArrowDown');
    steps.push(L[want] ? L[want].job : 'none');
    dispatchEvent(new KeyboardEvent('keydown', { code: 'Enter', key: 'Enter' }));
    LEDGER.talk.key('Enter');
    await LEDGER.talk.idle();
    if (LEDGER.written.read().open) break;
  }
  const w = LEDGER.written.read();
  for (let i = 0; i < 6 && LEDGER.written.read().open; i++) await LEDGER.written.next();
  return { steps, wrote: w.open ? w.text : null, m0, m1: { ...LEDGER.G.money }, lines: steps.length };
});
ok(s.steps.includes('yes') && s.m1.dirty < s.m0.dirty, 'ER-SPEAK-01 the tin put through the book with Sheila by Tab, arrows and Enter alone: ' + JSON.stringify(s.steps) + ' tin ' + s.m0.dirty + ' to ' + s.m1.dirty);

s = await E(() => ({ faults: LEDGER.game.faults.slice(0, 5), un: LEDGER.game.econ.state().unexplained }));
ok(s.faults.length === 0 && s.un === 0, 'no fault in any system, no money from nowhere: ' + JSON.stringify(s));
ok(h.errors.length === 0, 'no page errors: ' + JSON.stringify(h.errors.slice(0, 3)));
await h.close();
console.log(bad ? 'TEST FAIL (' + bad + ')' : 'PASS');
process.exit(bad ? 1 : 0);
