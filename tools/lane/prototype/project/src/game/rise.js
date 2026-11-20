// LEDGER, the whole game: the system "rise". The four rungs (DESIGN section 14; parts 2.12.2, 2.12.3, 2.12.5, 7.7).
// Tom rises in position, never in numbers: nothing here is ever shown as a number (ER-RISE-01). Rules: pieces/rise_rungs.js.
import { register, emit } from './core.js';
import { G } from '../state.js';
import { sub, bubble } from '../ui.js';
import { note } from '../ledger.js';
import { PIECE } from './pieces/rise_rungs.js';
import { TUNE as T } from './tune/rise.js';
import { X, actNow, near, first } from './rise_util.js';

const R = PIECE.fns;
const st = () => X('rise');
let coolT = 0;

// What he holds, read from the other systems of the rise and from the story.
export function holdings() {
  const firm = X('firm'),
    crew = X('crew'),
    men = Object.values(crew.men || {}).filter((m) => !m.fate);
  return {
    tookItOn: G.story.flags.choice === 'take' || actNow() >= 2,
    cars: (firm.cars || []).length,
    recruits: men.filter((m) => m.road).length,
    nightDesk: !!firm.nightDesk,
    fronts: Object.keys(firm.fronts || {}).length,
    rounds: Object.keys(firm.rounds || {}).length,
    coldStore: !!(firm.accounts || {}).coldstore,
    posts: new Set(men.map((m) => m.post && m.post.gate).filter(Boolean)).size,
    solicitor: !!(firm.accounts || {}).solicitor || !!firm.brief,
  };
}
const LANDS = [
  '',
  '',
  "Rung two. The firm is his: a third cab on the rank, somebody new on the wage book, and the door in the back room stands open.",
  "Rung three. Mickey's is the Hook's firm: five cars, a night desk, the cold-store shift, a share in a shop and a round collected for him.",
  "Rung four. The port's man: his people at the dock gate, the cold store and the landing, and a solicitor who takes his calls.",
];
function land(r) {
  const x = st();
  x.rung = r;
  x.at[r] = Math.round(G.t);
  x.heardDue[r] = Math.round(G.t) + T.nameHeardWithinGameHours * 60;
  const p = R.property(r);
  x.office = p.office;
  x.flat = p.flat;
  note(LANDS[r], 'note', 'rung' + r, { how: 'As he sees it' });
  sub(`The office: ${p.office}.`, '', 'over', 6);
  if (r >= 2 && G.hooks.doorOpen) G.hooks.doorOpen();
  emit('rise:rung', { rung: r, called: R.called(r), opens: T.rungs[r].opens, changes: T.rungs[r].changes });
  if (G.hooks.save) G.hooks.save();
}
function check() {
  const x = st(),
    r = R.rungFor(holdings(), x.rung);
  if (r > x.rung) land(r);
  return x.rung;
}
const HEARD = {
  2: ['Morning, Nowak.', 'Nowak. Now then.', "It's Nowak, isn't it. Mickey's."],
  3: ['Morning, Tom.', 'Now then, Tom.', 'All right, Tom?'],
  4: ['Tommy. Good to see you.', 'Morning, Tom. After you.', 'Tommy.'],
};
function heardBy(r, P) {
  const x = st();
  x.heard[r] = Math.round(G.t);
  const line = HEARD[r][Math.floor(G.t) % HEARD[r].length];
  if (P) {
    sub(line, P.anon ? P.def.desc : P.def.name, 'face', 5);
    note(`${P.anon ? 'People' : P.def.name} called him ${R.called(r)}${r === 4 ? ', and one or two say Tommy' : ''}. It is what the street says now.`, 'note', 'called' + r, { who: P.anon ? undefined : P.id, how: 'Said to his face' });
  } else {
    sub(`Through the hatch, Pauline on the radio: "Car two for ${r === 2 ? 'Mr Nowak' : 'Tom'}." It is what they call him now.`, '', 'over', 6);
    note(`On the radio and in the street he is ${R.called(r)} now.`, 'note', 'called' + r, { how: 'Heard on the radio' });
  }
}
const access = (door) => {
  const x = st();
  return R.access(door, { rung: x.rung, dress: outfit(), introducedBy: x.intro, appointment: x.appointment });
};
const outfit = () => (G.x.shops && G.x.shops.outfit != null ? G.x.shops.outfit : st().outfit) || 0;

register({
  id: 'rise',
  fresh: () => ({ rung: 1, at: { 1: 0 }, heardDue: {}, heard: {}, outfit: 0, intro: [], appointment: [], office: T.officeByRung[1], flat: T.flatByRung[1] }),
  loaded(x) {
    if (!x.rung) x.rung = 1;
    G.hooks.access = access;
    G.hooks.riseRung = () => st().rung;
    G.hooks.riseIntroduce = (by) => {
      if (!st().intro.includes(by)) st().intro.push(by);
    };
    G.hooks.riseAppointment = (door) => {
      if (!st().appointment.includes(door)) st().appointment.push(door);
    };
    G.hooks.calledNow = () => R.called(st().rung);
  },
  hourly() {
    check();
  },
  step(dt) {
    const x = st();
    if (G.paused) return;
    // ER-RISE-02: each step up is heard within a game day, said by somebody who knows him, to his face
    for (const r in x.heardDue) {
      if (x.heard[r]) continue;
      const who = !G.tom.inCar && G.named.find((P) => P.mind && P.mind.fam > 0.15 && near(P, T.nameSaidWithinMetres));
      if (who) heardBy(+r, who);
      else if (G.t >= x.heardDue[r] - 90) heardBy(+r, null);
    }
    // greetings and bodies: how the rise is felt on the pavement (ER-RISE-03)
    coolT -= dt;
    if (x.rung >= 3 && coolT <= 0 && G.tom.space === 'street' && !G.tom.inCar) {
      const Q = G.crowd.find((P) => !P.gone && !P.keeper && near(P, 2.4));
      if (Q) {
        coolT = 50;
        bubble(Q, x.rung >= 4 ? ['After you, Tom.', 'Morning, Mr Nowak.', 'Mind out, let him by.'][Math.floor(G.t) % 3] : ['Morning, Tom.', 'All right, Tom.'][Math.floor(G.t) % 2]);
      }
    }
  },
  hook: {
    rung: () => st().rung,
    // set(rung): climb to it one rung at a time, each landing as in play
    set(rung) {
      const x = st();
      while (x.rung < Math.min(4, rung)) land(x.rung + 1);
      return x.rung;
    },
    check,
    holdings,
    missing: () => (st().rung < 4 ? R.missing(holdings(), st().rung + 1) : []),
    differences: (a, b) => R.differences(a, b),
    called: () => R.called(st().rung),
    access,
    heard: () => Object.assign({}, st().heard),
    due: () => Object.assign({}, st().heardDue),
    setOutfit: (n) => (st().outfit = n),
    introduce: (by) => G.hooks.riseIntroduce(by),
    appointment: (door) => G.hooks.riseAppointment(door),
    state: () => st(),
  },
});
void first;
