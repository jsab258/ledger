// LEDGER, the whole game: the system "rise". He rises in position, never in numbers (DESIGN 14; parts 2.12.1 to
// 2.12.5, 7.7): money, crew, property, clothes, access. Four rungs; the name each person uses; greetings by regard;
// an office that changes; doors that open on soft keys. No rung, standing or heat is ever on screen.
import { register, X, write, tell, hourNow, dayNow, here, P_, emit, on } from './core.js';
import { G } from '../state.js';
import { RULES } from '../rules.js';
import { PIECE as RISE } from './pieces/rise.js';
import { PIECE as TALK } from './pieces/talk.js';
import { recruits } from './crew.js';
import { marked } from './foot.js';

const T = RULES.game.rise;
const R = RISE.fns;

// What he holds, read from the other systems.
export function holdings() {
  const f = G.x.firm.f,
    c = G.x.crew,
    x = X('rise');
  return { cars: f.cars.length, recruits: recruits().length, answeredSheila: !!G.story.flags.choice && G.story.flags.choice !== 'silent', fronts: x.fronts.length, rounds: x.rounds.length, contract: f.accounts.includes(T.accounts[0]), nightDesk: x.nightDesk, menAtTheGate: Object.values(c.men).some((m) => m.in && m.post && /Dock Road|quay/.test(m.post.zone || '')), brief: !!G.x.shops.brief };
}
function climb() {
  const x = X('rise'),
    r = R.rung(holdings());
  const now = R.reached(x.rung, r.rung);
  if (now === x.rung) return;
  x.rung = now;
  x.reachedT[now] = Math.round(G.t);
  write(`The firm is not what it was a month ago: ${T.rungs[now].name}. What opens: ${T.rungs[now].opens.join('; ')}.`, { key: 'rung:' + now, how: 'His own reading' });
  emit('rise.rung', { rung: now });
}
// Each step up the name ladder is heard within a game day of being reached (ER-RISE-02).
function hearName() {
  const x = X('rise'),
    t = G.tom;
  if (x.heard[x.rung] || x.rung < 2 || G.paused || t.inCar) return;
  const P = G.named.find((Q) => here(Q, RULES.game.law.signHeardWithinMetres) && !Q.def.police && Q.mind.fam > RULES.naming.familiarityAtLeastOnceMet && !(Q.id === 'sheila' && Q.mind.regard < 0.2));
  if (!P) return;
  const c = R.calls({ id: P.id, knowsHim: true, close: ['ron', 'darren'].includes(P.id), trusts: P.mind.regard >= 0.2, calledBefore: x.calledBy[P.id] || 0 }, x.rung);
  x.calledBy[P.id] = c.level;
  x.heard[x.rung] = { by: P.id, name: c.name, t: Math.round(G.t) };
  tell(`"Morning, ${c.name}."`, P.def.name);
  write(`${P.def.name} called him "${c.name}".`, { who: P.id, how: 'Said to his face', key: 'name:' + x.rung });
}
// How a person greets him (2.12.4): by what they hold of him, and by where he stands.
export function greetingOf(P) {
  const m = marked();
  return TALK.fns.greeting({ knowsHim: P.mind.fam > RULES.naming.familiarityAtLeastOnceMet, fear: P.mind.fear, regard: P.mind.regard, rung: X('rise').rung, marked: m.bruised, coatByDay: G.tom.coat && hourNow() > 8 && hourNow() < 17 });
}
const GREET = { afraid: ['He steps off the pavement to let him by.', '"Mr Nowak." Eyes down.'], angry: ['"You have a nerve, walking down here."', 'A door shuts as he passes.'], 'knows and likes him': ['"All right, Tom?"', 'A hand raised from across the road.'], 'his appearance': ['"Somebody has been at your face."', '"That coat again."'], neutral: ['A glance, and on.', '"Morning."'], 'a nod to a man who matters': ['A nod, held a moment longer than a stranger gives.', 'He holds the shop door.'], 'a door held': ['The door is held for him.', '"After you, Mr Nowak."'] };
// Access as soft keys (2.12.3): a door opens on any one of its keys.
const DOORS = { dockgate: { keys: ['rung', 'introduction'], rung: 3 }, harbourcounter: { keys: ['rung', 'dress', 'introduction'], rung: 3, outfit: 2 }, solicitor: { keys: ['rung', 'dress'], rung: 3, outfit: 2 }, realbook: { keys: ['trust'] }, ritaback: { keys: ['rung', 'introduction'], rung: 2 }, sitdown: { keys: ['rung', 'appointment'], rung: 4 } };
export function door(id) {
  const x = X('rise');
  return R.door(DOORS[id], { rung: x.rung, outfit: G.x.shops.outfit, introduction: !!Object.keys(G.x.crew.vouched).length, appointment: !!G.x.rivals.meeting, trust: P_('sheila') && P_('sheila').mind.regard >= 0.2 && x.rung >= 2 });
}
// Fronts and rounds (A15): held through a named man; money and trouble reach him only through that man.
export function takeFront(id, how) {
  const x = X('rise'),
    F = T.fronts[id];
  if (!F || x.fronts.includes(id)) return false;
  x.fronts.push(id);
  G.x.econ.fronts = x.fronts.length;
  write(`A share of ${F.name} is his now, got by ${how}. It is run by its own keeper, who answers to him.`, { how: 'Agreed it', key: 'front:' + id });
  emit('rise.front', { id });
  return true;
}
function weekly() {
  const x = X('rise');
  for (const id of x.fronts) {
    const trouble = G.x.rivals.threats.some((t) => G.t - t.t < 7 * 1440) ? 'two men sat in all afternoon and bought nothing' : null;
    const r = R.front(id, { held: true, manShort: G.x.law && G.x.law.edge, trouble });
    G.money.dirty += r.pence;
    G.money.earnedDirty += r.pence;
    G.hooks.flow('world', 'tin', r.pence, 'the share from ' + T.fronts[id].name);
    x.frontLog.push({ id, through: r.through, pence: r.pence, trouble: r.trouble, t: Math.round(G.t) });
    const who = P_(r.through);
    write(`${who && !who.anon ? who.def.name : 'The keeper'} brought the week's share from ${T.fronts[id].name}${r.trouble ? ', and says ' + r.trouble.what : ''}.`, { how: 'Brought to him', kind: 'money' });
  }
  for (const rd of x.rounds) {
    G.money.dirty += T.roundPaysPencePerWeek;
    G.money.earnedDirty += T.roundPaysPencePerWeek;
    G.hooks.flow('world', 'tin', T.roundPaysPencePerWeek, 'the round, by ' + rd.man);
  }
}

register({
  id: 'rise',
  fresh: () => ({ rung: 1, reachedT: { 1: 0 }, heard: {}, calledBy: {}, fronts: [], rounds: [], frontLog: [], nightDesk: false, greeted: {} }),
  minute(m) {
    if (m % 10 === 0) hearName();
    // greetings by regard: said or done as he passes, at most now and then, and remembered a day (ER-TALK-02)
    const x = X('rise'),
      t = G.tom;
    if (m % 3 || G.paused || t.inCar || t.space !== 'street') return;
    const P = G.named.find((Q) => here(Q, RULES.game.ledgerx.remarkWithinMetres) && !Q.def.police && x.greeted[Q.id] !== dayNow());
    if (!P || G.played - (x.lastGreetPlayed || -99) < RULES.game.ledgerx.streetTalkAtMostEveryRealSeconds) return;
    const g = greetingOf(P);
    x.greeted[P.id] = dayNow();
    x.lastGreetPlayed = G.played;
    x.lastGreeting = { by: P.id, kind: g, rung: x.rung };
    tell(GREET[g][(dayNow() + P.id.length) % 2], GREET[g][(dayNow() + P.id.length) % 2].startsWith('"') ? P.def.name : '');
  },
  hourly(h) {
    climb();
    const x = X('rise');
    if (G.x.firm.f.cars.length >= RULES.game.firm.nightDeskAtCars && !x.nightDesk) {
      x.nightDesk = true;
      write('With four cars out, Pauline has a girl on the radio nights. There is a night desk now.', { how: 'Pauline says', key: 'nightdesk' });
    }
  },
  daily(d) {
    if (d % 7 === 0) weekly();
  },
  hotspots(out) {
    const t = G.tom,
      x = X('rise');
    if (t.space === 'mickeys') out.push({ k: 'G', t: 'Look round the office', run: () => tell('The office: ' + T.office[x.rung] + '.', '', 7) });
    for (const id in T.fronts) {
      const F = T.fronts[id];
      if (x.rung >= 2 && !x.fronts.includes(id) && t.space === id && G.money.dirty + G.money.clean >= F.sharePence) out.push({ k: 'G', t: 'Buy into ' + F.name, run: () => {
        if (G.hooks.pay && !G.hooks.pay(F.sharePence, 'a share of ' + F.name)) return;
        takeFront(id, 'money');
      } });
    }
  },
  hook: {
    x: () => X('rise'),
    holdings,
    climb,
    rung: () => X('rise').rung,
    greetingOf: (id) => greetingOf(P_(id)),
    door,
    takeFront,
    weekly,
    office: () => T.office[X('rise').rung],
    // ER-RISE-01: the words on screen never hold a number of standing: the test reads the screen for these
    screenWords: () => ['rung', 'loyalty', 'standing', 'heat', 'reputation'],
  },
});
