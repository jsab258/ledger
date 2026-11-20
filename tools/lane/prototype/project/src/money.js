// LEDGER. Money: the pocket, the tin, earning, paying and putting the tin through the fare book.
// The rules are the rule pieces' (game/pieces/money.js, flows.js): this file only holds the game's pots to them and
// writes every movement into the flows book, so no pound comes from nowhere (ER-MONEY-01).
import { G, day } from './state.js';
import { pick, money, clamp, DAYS, quid } from './util.js';
import { seed } from './events.js';
import { note } from './ledger.js';
import { say, choose } from './ui.js';
import { RULES } from './rules.js';
import { ensureX, emit } from './game/core.js';
import * as M from './game/pieces/money.js';
import * as FLOWS from './game/pieces/flows.js';

const MONEY = RULES.money;

// ---------- the flows book ----------
// Kept in the save under G.x.econ.book. It opens at whatever the pots hold when it is first needed (a new game, or a
// save from before the one-shot), so the check holds from there on.
export function flowsBook() {
  const x = ensureX().econ || (G.x.econ = {});
  if (!x.book) x.book = FLOWS.open(G.money.clean, G.money.dirty);
  return x;
}
function record(flows, who) {
  const x = flowsBook();
  for (const f of flows) {
    if (who) f.who = who;
    const r = FLOWS.add(x.book, f);
    if (r.ok) x.book = r.book;
    else console.error('GAME FAULT money: a flow was refused (' + r.why + '): ' + JSON.stringify(f));
    emit('flow', { from: f.from, to: f.to, pence: f.pence, dirty: !!f.dirty, why: f.why, who: f.who || null });
  }
}
const pots = () => ({ clean: G.money.clean, dirty: G.money.dirty });
const setPots = (p) => {
  G.money.clean = p.clean;
  G.money.dirty = p.dirty;
};

// ---------- money ----------
// why: what it was for, in a few plain words ("rent", "a fare", "the Monday bag"). who: a person's id, if any.
export function pay(pence, cleanOnly, why, who) {
  flowsBook();
  const r = M.pay(pots(), pence, !!cleanOnly, why || 'paid');
  if (!r.ok) return false;
  setPots(r.pots);
  G.money.spent += Math.max(0, Math.round(pence));
  record(r.flows, who);
  return true;
}

export function earn(pence, dirty, why, who) {
  flowsBook();
  const r = M.earn(pots(), pence, !!dirty, why || (dirty ? 'night money' : 'earned'));
  if (!r.flows.length) return;
  setPots(r.pots);
  const m = G.money;
  if (dirty) m.earnedDirty += Math.round(pence);
  else m.earnedClean += Math.round(pence);
  record(r.flows, who);
  if (G.hooks.sfx) G.hooks.sfx('coin');
}

// What the fare book can hide now: the fixed sum, a share of the fares he drove since the last wash, a share of
// what the firm's own drivers took, and what his fronts add (G.x.firm.washExtraPence, the rise's).
export const washCap = () => {
  const x = flowsBook();
  return M.washCap(G.money.sinceWash, x.firmFaresSinceWash || 0, (G.x.firm && G.x.firm.washExtraPence) || 0);
};

// The count with Sheila. She says what the book will hide before anything goes through (ER-MONEY-04); over that
// the choice is his: only what fits, all of it (asked twice: the inspection reads every such week), or leave it.
export async function wash() {
  const m = G.money,
    amt = m.dirty,
    cap = washCap(),
    S = G.people.sheila,
    x = flowsBook();
  if (amt <= 0) return say('sheila', "There's nothing in the tin to put through. Good.");
  const warn = M.washWarning(amt, cap);
  let all = true;
  if (warn.warns) {
    const i = await choose(
      'sheila',
      `The book will hide ${money(cap)} behind the fares. There's ${money(amt)} in that tin. Put it all through and it's ${money(warn.over)} I can't hide behind anything.`,
      ['Only what the book will hide.', 'All of it.', 'Leave it in the tin.'],
    );
    if (i === 2) return say('sheila', "Then it stays in the tin, and the tin stays where I can't see it.");
    if (i === 1) {
      const sure = await choose(
        'sheila',
        "All of it. Then the book stops adding up this week, and a book that doesn't add up stays that way. Anybody who reads it later reads this. You're sure?",
        ['Yes. All of it.', 'No. Only what it will hide.'],
      );
      all = sure === 0;
    } else all = false;
  }
  const r = M.wash(pots(), cap, all);
  if (!r.washed) return say('sheila', 'The book is full as it is. Drive some fares and ask me again.');
  setPots(r.pots);
  m.washed += r.washed;
  m.sinceWash = 0;
  x.firmFaresSinceWash = 0;
  record(r.flows, 'sheila');
  if (!r.booksOffAdded) {
    await say(
      'sheila',
      r.left
        ? `${money(r.washed)} goes through as a wet week. The other ${money(r.left)} stays in the tin.`
        : pick(["It'll go through. Just.", "That fits behind the fares you've taken. It goes in as a wet week."]),
    );
  } else {
    const over = r.booksOffAdded;
    m.booksOff += over;
    weekRow(x).booksOffPence += over;
    S.mind.regard = clamp(S.mind.regard - MONEY.overWashingCostsSheilaRegard, -1, 1);
    const washed = seed('wash', ['sheila']);
    await say(
      'sheila',
      `The book says ${Math.max(MONEY.bookFaresAtLeast, Math.round(amt / MONEY.bookFarePence))} fares on a wet ${DAYS[day() % DAYS.length]}. We have two cars. That's ${money(over)} I can't hide behind anything.`,
    );
    await say(
      'sheila',
      "I've put it through. It doesn't add up, and I'm the one who has to add it. Don't make me say this twice.",
    );
    note(
      `The fare book has stopped adding up. ${quid(m.booksOff)} too much has gone through it.`,
      'money',
      'wash' + day(),
      { who: 'sheila', how: 'Sheila says', ev: washed.id },
    );
  }
}
// The book's record of each week, read by the inspection in Act III: { week, booksOffPence, lies, liesBroken }.
export function weekRow(x = flowsBook()) {
  const w = Math.floor(day() / DAYS.length);
  if (!x.weeks) x.weeks = [];
  let row = x.weeks.find((r) => r.week === w);
  if (!row) x.weeks.push((row = { week: w, booksOffPence: 0, lies: 0, liesBroken: 0 }));
  return row;
}
