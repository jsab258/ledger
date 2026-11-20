// LEDGER, the whole game: the system "count". The count with Sheila (ONE-SHOT-PROMPT 26, the first hour at 14:00,
// story S06): once a day and in twenty seconds, the tin on one side and the fare book on the other. The book can hide
// ten pounds plus four fifths of the fares really driven since the last wash. Over that the books are off, and she says
// so before she does it. The tin and the fare book move by the same sum, said in words; every penny is a flow.
import { register, X, write, P_, hourNow, dayNow } from './core.js';
import { G } from '../state.js';
import { scene, say, choose } from '../ui.js';
import { RULES } from '../rules.js';
import { flow } from '../money.js';
import { clamp, hyp } from '../util.js';
import { PIECE as MONEY } from './pieces/money.js';
import { washRoom } from './econ.js';

const T = RULES.game.back;
const W = MONEY.fns.words;
const cap1 = (s) => s.charAt(0).toUpperCase() + s.slice(1);

function put(amt, over) {
  const m = G.money,
    x = X('count');
  m.dirty -= amt;
  m.clean += amt;
  m.washed += amt;
  m.sinceWash = 0;
  flow('tin', 'pocket', amt, 'put through the fare book at the count');
  x.day = dayNow();
  x.counts.push({ t: Math.round(G.t), pence: amt, over });
  if (G.hooks.sfx) G.hooks.sfx('coin');
  if (over > 0) {
    m.booksOff += over;
    const S = P_('sheila');
    S.mind.regard = clamp(S.mind.regard - T.overWashingCostsSheilaRegard, -1, 1);
    write(`The count: ${W(amt)} out of the tin and into the fare book. ${cap1(W(over))} more than it will stand; Sheila said so.`, { key: 'count-' + x.day, who: 'sheila', how: 'Sheila says' });
  } else write(`The count: ${W(amt)} out of the tin and into the fare book as fares. The book will stand it.`, { key: 'count-' + x.day, who: 'sheila', how: 'Sheila says' });
}
export async function count() {
  await scene(async () => {
    const m = G.money,
      x = X('count');
    if (x.day === dayNow()) return say('sheila', "We've done the count today, love. Tomorrow.");
    if (m.dirty <= 0) return say('sheila', "There's nothing in the tin to count. Good.");
    const tin = m.dirty,
      cap = washRoom(),
      small = Math.min(T.smallerSumPence, cap, tin);
    const opts = [`All of it: ${W(tin)}.`];
    if (tin > cap) opts.push(`What the book will stand: ${W(cap)}.`);
    if (small < Math.min(cap, tin)) opts.push(`A smaller sum: ${W(small)}.`);
    opts.push('Leave it in the tin.');
    const i = await choose('sheila', `The count. The tin has ${W(tin)} in it. The book can hide ten pounds and four fifths of the fares really driven since it was last done: ${W(cap)} today. How much goes through?`, opts);
    let pick = opts[i] || '';
    let amt = /^All/.test(pick) ? tin : /^What the book/.test(pick) ? cap : /^A smaller/.test(pick) ? small : 0;
    if (amt > cap) {
      const j = await choose('sheila', "That's more than the book will stand, love. You sure?", ['Yes. All of it.', `No. What the book will stand: ${W(cap)}.`, 'No. Leave it in the tin.']);
      amt = j === 0 ? tin : j === 1 ? cap : 0;
    }
    if (amt <= 0) return say('sheila', 'Then it stays in the tin. It keeps.');
    const over = Math.max(0, amt - cap);
    put(amt, over);
    if (over > 0) await say('sheila', `${cap1(W(amt))} out of the tin and into the book. It doesn't add up now, and I'm the one who has to add it. Don't make me say this twice.`);
    else await say('sheila', `${cap1(W(amt))} out of the tin, and ${W(amt)} more in the fare book, as fares on a wet ${['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][dayNow() % 7]}. It goes through.`);
  });
}
G.hooks.count = count;

register({
  id: 'count',
  fresh: () => ({ day: -1, counts: [] }),
  hotspots(out) {
    const t = G.tom,
      S = P_('sheila'),
      h = hourNow();
    if (t.space !== 'mickeys' || !S || S.gone || S.space !== 'mickeys' || S.busy || h < T.countFromHour || h >= T.countUntilHour) return;
    if (X('count').day === dayNow() || G.money.dirty <= 0 || !(G.story.flags && G.story.flags.tour)) return;
    if (hyp(t.x, t.z, S.x, S.z) < T.countWithinMetres) out.push({ k: 'E', t: 'The count with Sheila: the tin and the fare book', run: count, person: true });
  },
  hook: { x: () => X('count'), room: () => washRoom() },
});
