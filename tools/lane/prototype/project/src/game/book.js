// LEDGER, the whole game: the system "book". Mickey's debt book in play (ONE-SHOT-PROMPT 4 at 4:30 and 5:30, 25;
// stories S03 on): Sheila finishes the walk-round at the things themselves and shows the book (five names, £156, the
// rent on Friday); the debts stand in the Ledger's Open page with a person and a landmark each; a debtor fronted up on
// the street pays what his purse holds and the rest stays on the book; Darren pays in what he hears; a debt struck
// out is struck through, never removed; people near a deed look, one gathers and drifts back. Numbers: tune/econ.js.
import { register, X, on, write, P_, dayNow } from './core.js';
import { G } from '../state.js';
import { sub, ui, panel, noted } from '../ui.js';
import { RULES } from '../rules.js';
import { ROOMS, roomPos, SPOTS } from '../map.js';
import { earn } from '../money.js';
import { act } from '../events.js';
import { hyp, angDiff, pounds, quid, cap, clamp } from '../util.js';
import { send, release, goToPoint, placeAll } from '../routines.js';
import { walkInOffice } from './hour1.js';

const T = RULES.game.econ,
  H = RULES.game.hour1;
const fl = () => G.story.flags;
const NAMES = { darren: 'Darren Milner', wayne: 'Wayne Harrison', lee: 'Lee Drewery', julie: 'Julie Kettlewell', dennis: 'Dennis Iveson' };
// where each is to be found, by a landmark (the Open page says it; nothing marks it in the world)
const WHERE = {
  darren: "at the rank outside Mickey's",
  wayne: "in the pawn's back room, behind Rinaldi's caff",
  lee: 'at the fish dock, by the stacked boxes',
  julie: "at her flat across from Mickey's, by the bus stop",
  dennis: 'at his yard, west end of the quay',
};

// ---- 4:30 Sheila finishes, at the things themselves ----
const FINISH = [
  { at: [3.4, -0.8], thing: 'the fare book', line: () => `${cap(pounds(G.money.fares || 0))} for the fare book, then. It goes down there, with the hour and the name. First clean money this week.` },
  { at: [5.7, -2.3], thing: "the locked door of Mickey's inner office", line: () => "And that door is still shut. Ask me again when I know you." },
  { at: [4.4, 2.5], thing: 'the stair to the flat', line: () => "Your bed is made up, up there. The tin for anything that never saw a meter is under it." },
  { at: [3.4, -0.8], thing: 'the debt book', line: () => "And this is his other book. The debts. Five names, a hundred and fifty-six pounds between them, and not one of them paying. The rent is eighteen pounds, Friday. You will want some of this in by then." },
];
function finishing(x, dt) {
  const t = G.tom,
    S = P_('sheila'),
    h1 = X('hour1');
  if (!S || S.dead || x.fin > FINISH.length) return;
  if (x.fin === 0) {
    // it begins when he is back in the office after the first fare (or the evening has gone by without one)
    const back = G.money.fareCount > 0 || G.t > RULES.time.weekStartsGameMinute + T.sheilaFinishesWithoutAFareAfterGameMinutes;
    if (h1.round <= 6 || !back || t.space !== 'mickeys' || S.space !== 'mickeys') return;
    x.fin = 1;
    x.said = 0;
    release(S);
  }
  if (t.space !== 'mickeys') return;
  S.busy = true;
  const stop = FINISH[x.fin - 1];
  if (!walkInOffice(S, stop.at, dt)) return;
  S.ang += angDiff(S.ang, Math.atan2(t.x - S.x, t.z - S.z)) * Math.min(1, dt * 6);
  x.waitT = x.said < x.fin ? (x.waitT || 0) + dt : 0;
  if (x.said < x.fin && (x.waitT > H.sheilaCallsHimOnAfterRealSeconds || hyp(S.x, S.z, t.x, t.z) <= H.sheilaSpeaksWhenHeIsWithinMetres) && !ui.modal && !ui.subs.some((s) => s.t > s.secs - 1.2)) {
    x.waitT = 0;
    x.said = x.fin;
    x.saidAt = G.played;
    const line = stop.line();
    sub(line, 'Sheila Dunn', 'face', 7);
    write('Sheila Dunn, at ' + stop.thing + ': "' + line + '"', { key: 'finish-' + x.fin, who: 'sheila', how: 'said to his face' });
  } else if (x.said === x.fin && G.played - x.saidAt > (x.fin === FINISH.length ? 5 : 3.2)) {
    x.fin++;
    if (x.fin > FINISH.length) {
      S.busy = false;
      S.goalKey = null;
      x.shown = Math.round(G.t);
      x.shownPlayed = Math.round(G.played);
      write("Mickey's debt book: Darren Milner £22, Wayne Harrison £30, Lee Drewery £15, Julie Kettlewell £9, Dennis Iveson £80. £156. Rent £18, Friday.", { kind: 'debts', key: 'debt-book', who: 'sheila', how: 'Sheila showed him the book' });
      openBook();
    }
  }
}
// The book itself, as a page he reads: every debt ever written in it stays in it.
export function bookHTML() {
  const x = X('book');
  const row = (id) => {
    const d = G.debts[id],
      was = quid(T.debts[id].owedPence).replace(/\.00$/, '');
    if (!d) return '';
    if (d.st === 'forgiven') return `<p><s>${NAMES[id]} ${was}</s> struck out by his own hand.</p>`;
    if (d.st === 'paid') return `<p><s>${NAMES[id]} ${was}</s> ${x.paidIn && x.paidIn[id] ? 'settled in ' + x.paidIn[id] : 'paid'}.</p>`;
    return d.owed < T.debts[id].owedPence ? `<p><s>${NAMES[id]} ${was}</s> ${NAMES[id]} ${quid(d.owed).replace(/\.00$/, '')}, after ${quid(T.debts[id].owedPence - d.owed).replace(/\.00$/, '')} paid.</p>` : `<p>${NAMES[id]} ${was}</p>`;
  };
  let owed = 0;
  for (const id in G.debts) if (G.debts[id].st === 'open') owed += G.debts[id].owed;
  return `<h1>Mickey's debt book</h1><p>In his hand, in pencil. Five names.</p>${Object.keys(NAMES).map(row).join('')}<p>${quid(owed).replace(/\.00$/, '')} in all still owing.</p><p>Sheila: the rent, £18, is due on Friday.</p><div class="row"><button class="btn" data-act="close">Shut the book</button></div>`;
}
function openBook() {
  panel(bookHTML(), 'debtbook');
  if (G.hooks.sfx) G.hooks.sfx('paper');
}

// ---- 5:30 fronting up on the street: a hard look, then a shove; he pays what his purse holds ----
function frontedUp(E) {
  const x = X('book');
  if (!E || !E.target || !NAMES[E.target]) return;
  if (!x.shown) {
    // he has not seen the book yet, so he does not know what is owed: the man says so himself, and nothing is taken
    if ((E.kind === 'hard_look' || E.kind === 'shove') && G.debts[E.target] && G.debts[E.target].st === 'open') sub(E.kind === 'shove' ? "Oi! What's that for? If it's Mickey's book, go and ask Sheila what I owe before you start." : "What? If it's about Mickey's book, Sheila's got it. Ask her.", NAMES[E.target], 'face', 5);
    return;
  }
  const id = E.target,
    d = G.debts[id],
    P = P_(id);
  if (!d || d.st !== 'open' || !P) return;
  if (E.kind === 'hard_look') {
    x.looked[id] = Math.round(G.t);
    if (id === 'darren') sub("All right, chief. All right. It's the twenty-two, I know it is.", NAMES[id], 'face', 4);
    return;
  }
  if (E.kind !== 'shove') return;
  if (!x.looked[id] || G.t - x.looked[id] > T.hardLookHoldsGameMinutes) {
    // hands on him out of nowhere: he steps back and does not pay. The ladder is climbed a rung at a time.
    sub("Oi! Hands off. What's that for?", NAMES[id], 'face', 4);
    return;
  }
  const purse = x.purse[id] == null ? T.debts[id].pursePence : x.purse[id],
    amt = Math.min(purse, d.owed);
  x.purse[id] = purse - amt;
  if (amt > 0) {
    d.owed -= amt;
    if (d.owed <= 0) d.st = 'paid';
    earn(amt, true, NAMES[id] + ' paid on the debt book');
    P.mind.regard = clamp(P.mind.regard - T.squeezedRegardLost, -1, 1);
    P.mind.fear = clamp((P.mind.fear || 0) + T.squeezedFearGained, 0, 1);
    sub(d.owed > 0 ? `Here. ${cap(pounds(amt))}. That's every penny on me. The rest stands, I know it stands.` : `Here. ${cap(pounds(amt))}. That's us square.`, NAMES[id], 'face', 5);
    write(`Fronted up ${NAMES[id]} in the street: a hard look, then a shove. He paid ${quid(amt).replace(/\.00$/, '')}${d.owed > 0 ? '; ' + quid(d.owed).replace(/\.00$/, '') + ' stays on the book' : ''}. It is in the tin.`, { key: 'front-' + id + '-' + Math.round(G.t), who: id, how: 'He did it' });
    act('debt_paid', { target: id, silent: true });
  } else sub("I've nothing on me. Turn me upside down if you like.", NAMES[id], 'face', 4);
  if (id === 'darren') x.darren = x.darren || 'fronted';
}
// ---- after a deed, people near look; one gathers and drifts back (2.5.3) ----
const DEEDS = { shove: 1, strike: 1, threat: 1 };
const GATHER = { P: null, until: 0 };
function afterDeed(E) {
  if (!DEEDS[E.kind] || G.tom.space !== 'street') return;
  const t = G.tom;
  let nearest = null,
    nd = 1e9;
  for (const P of G.named.concat(G.crowd)) {
    if (P.gone || P.dead || P.space !== 'street' || P.id === E.target || P.talking) continue;
    const d = hyp(P.x, P.z, t.x, t.z);
    if (d > T.afterADeedLookWithinMetres || (G.env && G.env.los && !G.env.los(t.x, t.z, P.x, P.z))) continue;
    P.mind.look = Math.max(P.mind.look || 0, T.afterADeedLookRealSeconds);
    if (d > T.gathersNoNearerThanMetres && d < nd && !P.busy && !P.keeper) {
      nd = d;
      nearest = P;
    }
  }
  if (nearest && !GATHER.P) {
    // one comes a few steps nearer to see, stands, and goes back to what he was doing
    const k = Math.max(0, (nd - T.gathersNoNearerThanMetres) / nd);
    GATHER.P = nearest;
    GATHER.until = G.played + T.gathersForRealSeconds;
    GATHER.from = [nearest.x, nearest.z];
    goToPoint(nearest, nearest.x + (t.x - nearest.x) * k, nearest.z + (t.z - nearest.z) * k);
    X('book').gathered = { id: nearest.id, t: Math.round(G.t) };
  }
}
function gatherStep() {
  if (!GATHER.P || G.played < GATHER.until) return;
  const P = GATHER.P;
  GATHER.P = null;
  P.hold = false;
  P.hurry = 1;
  P.goalKey = null; // back to his own routine
  X('book').gathered.back = Math.round(G.t);
}

// The first night's staging, held by state: Sheila sits on at her desk until she has shown him the debt book, and Darren
// stays on the pavement by the rank until his twenty-two pounds is settled one way or another. True when anybody was sent.
function staging(x) {
  const S = P_('sheila'),
    D = P_('darren'),
    after = X('hour1').round > 6;
  let sent = false;
  if (dayNow() !== 0 && G.t > 1440 + T.firstNightStagingEndsAtGameMinute) {
    for (const P of [S, D, P_('ron')]) if (P && P.override && (P.override.where === 'pave' || P.override.where === 'rank' || P.override.where === 'mickeys:sheila') && P.override.until === undefined) release(P);
    return false;
  }
  if (S && after && x.fin <= FINISH.length && !S.busy && !(S.override && S.override.where === 'mickeys:sheila')) {
    send(S, 'mickeys:sheila', 'work');
    sent = true;
  }
  const R = P_('ron'),
    o = G.x.outfit;
  if (R && after && o && (o.ask1 === null || o.ask1 === 'put') && !R.busy && !(R.override && R.override.where === 'rank')) {
    send(R, 'rank', 'idle');
    sent = true;
  }
  if (R && o && o.ask1 && o.ask1 !== 'put' && R.override && R.override.where === 'rank' && R.override.until === undefined) release(R);
  if (D && G.debts.darren) {
    const settled = x.darren || G.debts.darren.st !== 'open';
    if (settled && !x.darren) x.darren = G.debts.darren.st === 'forgiven' ? 'struck' : 'settled';
    if (settled && !x.darrenT) x.darrenT = G.t;
    if (!settled && after && !(D.override && D.override.where === 'pave')) {
      send(D, 'pave', 'idle');
      sent = true;
    }
    if (settled && D.override && D.override.where === 'pave' && G.t - x.darrenT > T.darrenStaysAfterGameMinutes) release(D);
  }
  return sent;
}

register({
  id: 'book',
  fresh: () => ({ fin: 0, said: 0, saidAt: 0, shown: 0, purse: {}, looked: {}, paidIn: {}, darren: null, gathered: null, strikeAsked: {} }),
  loaded(x) {
    GATHER.P = null;
    // the first night's people are where the staging has them after a load too (a save holds no routine overrides)
    if (staging(x)) placeAll();
    // Darren pays in what he hears: it is his own way with the debt, raised in his own words
    G.hooks.debtMatter = (P, m) => {
      const b = X('book'),
        d = G.debts[P.id];
      if (P.id !== 'darren' || !b.shown || !d || d.st !== 'open') return;
      m.raise = "About the twenty-two quid on the book. I've not got it, chief. But I hear things. I could pay it in what I hear.";
      m.opts.unshift({
        say: ["I'll take it in what you hear.", 'What you hear, then, and we are square.'],
        q: 'What I hear, for the twenty-two. Yeah or no?',
        yes: ['Yes. What you hear, and we are square.', 'Yes. Tell me.'],
        no: ['No. I want the money.', 'No. Not that.'],
        keep: ['What do you hear?', 'Is it worth twenty-two pounds?'],
        keepSay: "Can't say till it's a deal, can I. Yeah or no?",
        noSay: "Then it stands on the book, chief. I've not got it.",
        take: () => {
          d.st = 'paid';
          d.owed = 0;
          b.paidIn.darren = 'what he hears';
          b.darren = 'words';
          if (G.x.crime && G.x.crime.facts) G.x.crime.facts.hut_tip = Math.round(G.t);
          write("Darren, for his £22: Iveson's money is in a tin in his yard hut. The yard hand leaves at six.", { key: 'tip-hut', who: 'darren', how: 'Darren says' });
          act('debt_paid', { target: 'darren', silent: true });
          return "Right. Iveson. Eighty he owes that book, and he's got it: in a tin, in the hut in his yard, west end of the quay. Bank shuts too early for him. His lad goes home at six.";
        },
      });
    };
    G.hooks.debtStruck = (id) => {
      write(`Struck ${NAMES[id] || id}'s ${quid(RULES.game.econ.debts[id].owedPence).replace(/\.00$/, '')} out of Mickey's book. Struck through, not rubbed out. It cannot be put back.`, { key: 'struck-' + id, who: id, how: 'He did it' });
      if (id === 'darren') X('book').darren = 'struck';
      noted(`${(NAMES[id] || id).split(' ')[0]} will tell the street he was let off, he thinks.`);
    };
    G.hooks.openRows = (o) => {
      const b = X('book');
      if (G.hooks.openRows2) G.hooks.openRows2(o); // the outfit's asks and what he carries (game/outfit.js)
      if (!b.shown) return;
      for (const id in NAMES) {
        const d = G.debts[id];
        if (!d) continue;
        const sum = quid(d.owed).replace(/\.00$/, '');
        if (d.st === 'open') o.push({ key: 'debt:' + id, who: id, what: `${NAMES[id]} owes ${sum} on Mickey's book. Find ${id === 'julie' ? 'her' : 'him'} ${WHERE[id]}`, how: "Mickey's book" });
        // a debt struck out or settled stays written: the old line struck through, what became of it under it
        else if (d.st === 'forgiven') o.push({ key: 'debt:' + id, who: id, what: `${NAMES[id]}'s ${quid(T.debts[id].owedPence).replace(/\.00$/, '')} is struck out of Mickey's book`, how: 'His own hand' });
        else if (d.st === 'paid') o.push({ key: 'debt:' + id, who: id, what: `${NAMES[id]}'s ${quid(T.debts[id].owedPence).replace(/\.00$/, '')} is settled${b.paidIn[id] ? ', in ' + b.paidIn[id] : ''}`, how: "Mickey's book" });
      }
    };
    G.hooks.moneyWords = () => {
      const m = G.money,
        b = X('book'),
        parts = [`${quid(m.clean)} in his pocket.`];
      if (m.fares > 0) parts.push(`${quid(m.fares)} of fares in the fare book this week.`);
      if (fl().tour) parts.push(m.dirty > 0 ? `The tin has about ${quid(Math.round(m.dirty / 100) * 100).replace(/\.00$/, '')} in it.` : 'The tin is empty.');
      parts.push(`Rent, ${quid(RULES.money.rentPence).replace(/\.00$/, '')}, Friday.`);
      if (b.shown) {
        for (const id in NAMES) {
          const d = G.debts[id];
          if (d && d.st === 'open') parts.push(`${NAMES[id].split(' ')[0]} ${d.owed < T.debts[id].owedPence ? 'still owes' : 'owes'} ${quid(d.owed).replace(/\.00$/, '')}.`);
        }
      }
      return parts.join(' ');
    };
  },
  step(dt) {
    if (G.paused || G.story.phase !== 'play') return;
    const x = X('book');
    finishing(x, dt);
    gatherStep();
    staging(x);
  },
  hotspots(out) {
    const t = G.tom,
      x = X('book');
    if (t.space === 'mickeys' && x.shown) {
      const [bx, bz] = roomPos('mickeys', 3.4, -0.8);
      if (hyp(t.x, t.z, bx, bz) < H.thingWithinMetres) out.push({ k: 'G', t: "Read Mickey's debt book", run: openBook });
    }
  },
  hook: { x: () => X('book'), bookHTML, names: NAMES, where: WHERE, finish: FINISH.map((f) => ({ at: f.at, thing: f.thing })) },
});
on('act', (E) => {
  frontedUp(E);
  afterDeed(E);
});
