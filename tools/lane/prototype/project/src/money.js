// LEDGER. Money and debts: the pocket, the tin, earning, paying and putting the tin through the fare book.
import { G, day } from './state.js';
import { pick, money, clamp, DAYS, quid } from './util.js';
import { seed } from './events.js';
import { note } from './ledger.js';
import { say, $ } from './ui.js';
import { RULES } from './rules.js';

const MONEY = RULES.money;

// ---------- money ----------
// Every movement of money is also told to the whole game's flows ledger (game/econ.js): no money from nowhere.
export const flow = (from, to, pence, why) => {
  if (pence > 0 && G.hooks.flow) G.hooks.flow(from, to, pence, why);
};
export function pay(pence, cleanOnly, why = 'spent') {
  const m = G.money;
  if (cleanOnly) {
    if (m.clean < pence) return false;
    m.clean -= pence;
    m.spent += pence;
    flow('pocket', 'world', pence, why);
    return true;
  }
  if (m.clean + m.dirty < pence) return false;
  const d = Math.min(m.dirty, pence);
  m.dirty -= d;
  m.clean -= pence - d;
  m.spent += pence;
  flow('tin', 'world', d, why);
  flow('pocket', 'world', pence - d, why);
  return true;
}

export function earn(pence, dirty, why = 'earned') {
  const m = G.money;
  if (dirty) {
    m.dirty += pence;
    m.earnedDirty += pence;
  } else {
    m.clean += pence;
    m.earnedClean += pence;
  }
  flow('world', dirty ? 'tin' : 'pocket', pence, why);
  if (G.hooks.sfx) G.hooks.sfx('coin');
}

export const washCap = () =>
  MONEY.washedSafelyPence + Math.round(G.money.sinceWash * MONEY.washedSafelyShareOfFares);

// The fare book can only wash so much before it stops adding up.
export async function wash() {
  const m = G.money,
    amt = m.dirty,
    cap = washCap(),
    S = G.people.sheila;
  if (amt <= 0) return say('sheila', "There's nothing in the tin to put through. Good.");
  m.dirty = 0;
  m.clean += amt;
  flow('tin', 'pocket', amt, 'put through the fare book');
  m.washed += amt;
  m.sinceWash = 0;
  if (amt <= cap) {
    await say(
      'sheila',
      pick(["It'll go through. Just.", "That fits behind the fares you've taken. It goes in as a wet week."]),
    );
  } else {
    const over = amt - cap;
    m.booksOff += over;
    S.mind.regard = clamp(S.mind.regard - MONEY.overWashingCostsSheilaRegard, -1, 1);
    const washed = seed('wash', ['sheila']);
    await say(
      'sheila',
      `The book says ${Math.max(MONEY.bookFaresAtLeast, Math.round(amt / MONEY.bookFarePence))} fares on a wet ${DAYS[day() % 7]}. We have two cars. That's ${money(over)} I can't hide behind anything.`,
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
