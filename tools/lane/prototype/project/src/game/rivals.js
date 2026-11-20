// LEDGER, the whole game: the system "rivals". Three rivals, each after a different ledger, each knowing only what
// its own people have seen or heard (DESIGN section 13). Parts 2.10.1 ladders, 2.10.3 pressures and answers,
// 2.10.4 the Fixer, 3.5.5 sit-downs. Rules: pieces/rival_ladder.js. No faction is a number; nothing here is a meter.
import { register, emit, on } from './core.js';
import { G, hour } from '../state.js';
import { act, seed } from '../events.js';
import { sub, say, scene } from '../ui.js';
import { decision } from '../talk.js';
import { note, meet } from '../ledger.js';
import { pay } from '../money.js';
import { send, release } from '../routines.js';
import { attached } from '../seeing.js';
import { PIECE } from './pieces/rival_ladder.js';
import { TUNE as V } from './tune/rivals.js';
import { P_, X, actNow, runEnded, moneyAll, first, near } from './rise_util.js';

const R = PIECE.fns;
const IDS = ['jensen', 'agar', 'cammack'];
const st = () => X('rivals');
const HEADN = { jensen: 'Maureen Jensen', agar: 'Geoffrey Agar', cammack: 'Danny Cammack' };

// What this rival's own people hold about him: the only things it can act on (ER-RIV-01).
function sightings(id) {
  const out = [];
  for (const eye of V.rivals[id].eyes) {
    const P = P_(eye);
    if (!P || P.dead || !P.mind) continue;
    for (const m of P.mind.mem) {
      const E = G.ev[m.e];
      if (!E || E.kind === 'inherit' || !attached(m)) continue;
      out.push({ by: eye, e: m.e, t: Math.round(m.t), how: m.src });
    }
  }
  return out.concat((st().extra || {})[id] || []);
}
const ctxOf = (id) => ({ t: Math.round(G.t), act: actNow(), runEnded: runEnded(), sightings: sightings(id) });

function advance(id, o = {}) {
  const x = st();
  if (o.force) {
    // a test call: the last rung counts as shown, the wait is over, and one of its people is given something to have seen
    x[id].shown = true;
    x[id].since = -1e9;
    x[id].holdUntil = 0;
    if (!sightings(id).length) (x.extra[id] = x.extra[id] || []).push({ by: V.rivals[id].eyes[0], e: 'told' + Math.round(G.t), t: Math.round(G.t), how: 'told' });
    if (actNow() < V.startsFromAct) (G.x.acts = G.x.acts || {}).act = Math.max(2, actNow());
  }
  const r = R.advance(id, x[id], ctxOf(id));
  if (!r.move) return { ok: false, why: r.why };
  x[id] = Object.assign(r.rival, { due: Math.round(G.t) + V.shownOnTheStreetAfterGameHours * 60, open: r.rival.rung === 3 || r.rival.rung === 4, answered: null });
  x.moves.push(Object.assign({ t: Math.round(G.t) }, r.move));
  deliver(id);
  emit('rival:move', r.move);
  return { ok: true, move: r.move };
}
// Each rung is said to his face or shown on his street: somebody comes and waits where he will pass.
function deliver(id) {
  const r = st()[id],
    def = V.rivals[id],
    until = G.t + V.shownOnTheStreetAfterGameHours * 60;
  if (r.rung >= 2 && r.rung <= 4 && P_(def.man)) send(P_(def.man), V.manWaitsAt, 'idle', until);
  if (r.rung === 5 && P_(def.head)) send(P_(def.head), V.headWaitsAt, 'idle', until + 1440);
}
const SHOWN = {
  jensen: [
    '',
    'Lee Drewery stops talking when a Mickey\'s cab goes by the dock gate. Somebody up there has been asking about the firm.',
    "One of the Widow's men stood across from the office for an hour this morning, in a donkey jacket, looking at nothing but the door.",
    "Kevin comes back from the dock gate short. The Widow's men are taking a pound off every Mickey's car that goes through.",
    "Word at the rank: the Widow has offered one of his own people a place, at better money. He has not said which.",
    'Maureen Jensen will sit down with him. The word came by the rank, twice, so nobody could say it was not given.',
  ],
  agar: [
    '',
    "Susan Coverdale at the Harbour Board asked Pauline who signs for Mickey's now. Somebody upstairs wanted to know.",
    "A clerk with a briefcase came into the office, wrote down the licence number off the wall, and left without a word.",
    "A solicitor's letter on the counter, by hand: the private-hire licence was Mickey's, not the firm's, and the council may wish to look again.",
    'A second letter. The council will inspect every car on a day of its choosing. A car that fails comes off the road.',
    'Mr Agar will see him. A card came by hand, with a time on it and no address, because everybody knows the address.',
  ],
  cammack: [
    '',
    "Rita had a lad in asking what Mickey's nephew is like. She told him. She told Tom she told him.",
    "One of Cammack's lads sat on the bonnet of car two for ten minutes at dinner time, where the whole street could see.",
    "A fight outside the office at closing time, nothing to do with the firm, and the police took the firm's name all the same.",
    "The office window is put in during the night, and somebody shouts his name down the street while it happens.",
    'Danny Cammack wants a sit-down. He had it shouted across the street, so everybody knows he asked.',
  ],
};
function shownOnStreet(id) {
  const r = st()[id];
  if (r.shown) return;
  r.shown = true;
  const text = SHOWN[id][r.rung];
  sub(text, '', 'over', 8);
  note(text, 'note', 'rival' + id + r.rung, { how: 'Shown on his street' });
  if (r.rung === 4 && id === 'cammack') seed('rival_trouble', ['ada', 'ron'], { zone: 'Quay Street' });
  st().log.push({ t: Math.round(G.t), rival: id, rung: r.rung, how: 'shown' });
}
function said(id, who) {
  const r = st()[id];
  r.shown = true;
  note(SHOWN[id][r.rung], 'note', 'rival' + id + r.rung, { who, how: 'Said to his face' });
  st().log.push({ t: Math.round(G.t), rival: id, rung: r.rung, how: 'said', by: who });
}
// ---------- the three answers: pay, defy, or counter with what he knows (ER-RIV-03) ----------
function answer(id, how) {
  const x = st(),
    def = V.rivals[id],
    r = R.answer(id, x[id], how, { t: Math.round(G.t), moneyPence: moneyAll(), knows: x.knows[id] });
  if (!r.ok) return r;
  const rung = x[id].rung;
  x[id] = Object.assign(r.rival, { open: false });
  const man = P_(def.man);
  if (how === 'pay') {
    pay(r.effects[0].pence, false, 'paid to ' + HEADN[id]);
    act('rival_paid', { target: def.man, name: HEADN[id], silent: true, told: [def.man, def.eyes[0]] });
  } else if (how === 'defy') {
    act('rival_defied', { target: def.man, name: HEADN[id], silent: true, told: [def.man, def.eyes[0]] });
    if (id === 'jensen') {
      if (rung === 3) x.taxUntil = Math.round(G.t) + V.defyTaxGameDays * 1440;
      else {
        const men = (G.x.crew && G.x.crew.men) || {},
          weak = Object.keys(men).filter((k) => !men[k].fate && k !== 'sheila').sort((a, b) => men[a].loyalty - men[b].loyalty)[0];
        if (weak && G.hooks.crewStrain) {
          G.hooks.crewStrain(weak, 'rivalOffer');
          G.hooks.crewStrain(weak, 'rivalOffer');
          x.offered = weak;
        }
      }
    } else if (id === 'agar') x.inspectionAt = Math.round(G.t) + V.defyLetterBringsInspectionInGameDays * 1440;
    else {
      for (let i = 0; i < V.defyTroubleSeenDeeds; i++) seed('rival_trouble', ['ada', 'ron', 'pauline'], { zone: 'Quay Street' });
      emit('street:edge', { zone: 'Quay Street', until: G.t + 2880, deeds: V.defyTroubleSeenDeeds, by: 'ada' });
    }
  } else act('rival_countered', { target: def.man, name: HEADN[id], silent: true, told: [def.man] });
  if (man) release(man);
  const words = { pay: 'Paid what was asked', defy: 'Told them no', counter: 'Used what he knew' }[how];
  note(`${words}: ${HEADN[id]}, over ${R.pressure(id, rung)}. ${how === 'pay' ? 'It will keep them off for a week, and they will ask for more.' : how === 'defy' ? 'It will cost, and they will come sooner.' : 'They step back, for now.'}`, 'note', 'answer' + id + rung + Math.round(G.t), { who: def.man, how: 'Said it' });
  x.log.push({ t: Math.round(G.t), rival: id, rung, answer: how, effects: r.effects });
  emit('rival:move', { rival: id, rung: x[id].rung, kind: 'answered', answer: how });
  if (G.hooks.save) G.hooks.save();
  return r;
}
function sitDown(id, how) {
  const x = st(),
    r = R.sitDown(id, x[id], how, { knows: x.knows[id] });
  if (!r.ok) return r;
  x[id] = Object.assign(r.rival, { open: false });
  act('rival_sat_down', { target: V.rivals[id].head, name: HEADN[id], silent: true, told: [V.rivals[id].head, V.rivals[id].eyes[0]] });
  note(`Sat down with ${HEADN[id]}. ${{ accept: 'Took what was offered.', defy: 'Refused it to the face.', counter: 'Put what he knew on the table.' }[how]} It is settled between them, whatever it costs.`, 'note', 'sat' + id, { who: V.rivals[id].head, how: 'Was there' });
  if (P_(V.rivals[id].head)) release(P_(V.rivals[id].head));
  x.log.push({ t: Math.round(G.t), rival: id, rung: 5, answer: how });
  emit('rival:move', { rival: id, rung: 5, kind: 'sitdown', answer: how });
  emit('sitdown', { rival: id, answer: how });
  if (G.hooks.save) G.hooks.save();
  return r;
}
// ---------- the Fixer: true reads, a meeting, one truce ----------
function fixer(what, id) {
  const x = st(),
    r = R.fixer(what, x, { rival: id, moneyPence: moneyAll(), t: Math.round(G.t) });
  if (!r.ok) return r;
  pay(r.pence, false, 'the Fixer, for ' + (what === 'read' ? 'a read' : what === 'meeting' ? 'a meeting' : 'a truce'));
  act('fixer_paid', { target: 'garbutt', silent: true, told: ['garbutt'] });
  if (what === 'read') {
    const rd = r.read,
      eyes = rd.through.map((e) => (P_(e) ? P_(e).def.name : e)).join(' and '),
      fact = `${HEADN[id]} hears of him through ${eyes}`;
    x.fixer.reads.push(Object.assign({ t: Math.round(G.t) }, rd));
    if (!x.knows[id].includes(fact)) x.knows[id].push(fact);
    r.words = `${HEADN[id]}. Where it stands with you: ${rd.standsAt}. What it is after: ${rd.after}. Who tells it things: ${eyes}. What comes next: ${rd.next}.`;
    note(`The Fixer's read on ${HEADN[id]}: ${rd.standsAt}; after ${rd.after}; hears through ${eyes}; next, ${rd.next}.`, 'note', 'read' + id + Math.round(G.t), { who: 'garbutt', how: 'Paid for it' });
  } else if (what === 'meeting') {
    if (G.hooks.riseAppointment) G.hooks.riseAppointment('sitDown');
    x.fixer.meeting = id;
    r.words = `${HEADN[id]} will hear you out. I will say when.`;
    note(`The Fixer has brokered a meeting with ${HEADN[id]}.`, 'note', 'meeting' + id, { who: 'garbutt', how: 'Paid for it' });
  } else {
    x.fixer.truceUsed = true;
    x[id].holdUntil = r.holdUntil;
    r.words = `A fortnight. ${HEADN[id]} will leave your people be until then. I sell that once.`;
    note(`The Fixer sold him a fortnight's truce with ${HEADN[id]}. He sells it once.`, 'note', 'truce', { who: 'garbutt', how: 'Paid for it' });
  }
  return r;
}

// ---------- the scenes ----------
const three = (id, extra) => ({
  ask: `how he answers ${HEADN[id]}`,
  leaveIdx: -1,
  keep: ['Who sent you?', 'What happens if I say no?'],
  keepSay: extra,
  opts: [
    { agree: 1, say: ["I'll pay it.", 'Here. Take it.'], q: `${(R.price(id, st()[id]) / 100).toFixed(0)} pounds, now, and it goes away for a week. Yes?`, yes: ['Yes. Take it.', 'Yes.'], no: ['No. Not that.', 'No. Wait.'], keep: ['Who sent you?', 'What happens if I say no?'], keepSay: extra },
    { refuse: 1, say: ['No. Tell them no.', "I'm not paying and I'm not moving."], q: 'That is your answer? It will be carried back as you said it.', yes: ['Yes. Carry it back.', "Yes. That's my answer."], no: ['No. Wait.', 'No. Let me think.'], keep: ['Who sent you?', 'What happens if I say no?'], keepSay: extra },
    { say: ['Tell them I know how they hear about me.', 'I know something they would rather I did not.'] },
  ],
});
const SAY = {
  jensen: {
    2: ["Mrs Jensen says good morning. She knew your uncle. She says he always knew which gate was hers.", 'She would like you to know she has noticed the new cars.'],
    3: ["Mrs Jensen's gate. Your cabs go through it. From Monday that is a pound a car, each way. It is not personal.", 'Pay it, or do not come through the gate, or tell me something she would want to hear.'],
    4: ['One of yours has been offered a place with us. Better money than you pay. Mrs Jensen thought you should hear it from her side first.', 'It need not happen.'],
    5: ['Your uncle and I never had a cross word, Mr Nowak. He knew which gate was mine.', 'You carry my people to the cold store, your men stand on my landing, and nobody asked me. So. I ask you now. The gate and the landing are mine and you pay to use them, for good. Or they are not, and we find out whose they are.'],
  },
  agar: {
    2: ['Mr Nowak? I am from Mr Agar\'s office. I am only to note the licence number. Thank you. Most irregular wall to keep it on.', 'Mr Agar likes things in order. He asked me to say so.'],
    3: ['I am to see that you have read it, Mr Nowak. The private-hire licence was granted to Mr Suddaby in person. Mr Agar feels the council should be told he has died.', 'There is a fee for regularising it. Or the council may take its own view.'],
    4: ['A second letter, Mr Nowak. The council will inspect every vehicle. Mr Agar sits on that committee. He is very thorough.', 'It can still be regularised.'],
    5: ['Sit down, Mr Nowak. Nothing personal. It is only that the paperwork must be in order.', 'I hold the licence, the lease on your yard and the ear of the committee. You may keep your cabs and your name on the door. What I ask is that the firm banks with my office and does as it is advised. Or you may see how long a cab firm lasts without paper.'],
  },
  cammack: {
    2: ['Danny says hello. He says nice little office. He says it is a shame about the street it is on.', "That's all. He just wanted you to have a look at me."],
    3: ['Shame about last night, pal. Coppers taking your name and you not even in it. Danny says that can stop. Costs, though.', 'Or it can get worse. Up to you, pal.'],
    4: ['Windows are dear, pal. Danny says next time it might not be a window. He says you know what he wants.', 'Last time of asking.'],
    5: ['Here he is. The nephew. Sit down, pal, you are making the place look respectable.', 'Quay Street. I want it loud and I want it mine, and you are in the way being quiet. So you work under me and keep your cabs, or we carry on until one of us cannot.'],
  },
};
const visit = (id) =>
  scene(async () => {
    const x = st(),
      r = x[id],
      def = V.rivals[id],
      M = P_(def.man);
    meet(M);
    for (const line of SAY[id][r.rung]) await say(def.man, line);
    said(id, def.man);
    if (r.rung < 3) {
      release(M);
      return;
    }
    const i = await decision(def.man, 'So. What do I take back?', three(id, 'I only carry it. What do I take back?'));
    if (i < 0) {
      await say(def.man, 'Then I will be here tomorrow. After that it is taken as a no.');
      return;
    }
    const how = ['pay', 'defy', 'counter'][i],
      res = answer(id, how);
    if (!res.ok) {
      await say(def.man, how === 'pay' ? 'That is not enough, and you know it. Tomorrow.' : 'You know nothing. I will say you tried. Tomorrow.');
      return;
    }
    await say(def.man, { pay: 'Sensible. Same again when it is asked.', defy: 'I will tell it as you said it. Mind how you go.', counter: 'I see. I will say that word for word.' }[how]);
  });
const noticed = (id, eye) =>
  scene(async () => {
    const E = P_(eye);
    await say(eye, { jensen: 'They were asking about you up at the dock gate. Mrs Jensen. I said what I had seen. I am not hiding it.', agar: 'Somebody upstairs asked who signs for Mickey\'s now. I told them. It is my job to tell them.', cammack: "Danny Cammack had a lad in, asking what Mickey's nephew is like. I told him what I have seen. Fair is fair." }[id]);
    said(id, eye);
    void E;
  });
const table = (id) =>
  scene(async () => {
    const def = V.rivals[id],
      H = P_(def.head);
    meet(H);
    for (const line of SAY[id][5]) await say(def.head, line);
    said(id, def.head);
    const i = await decision(def.head, 'Well?', {
      ask: `what he says to ${HEADN[id]} at the sit-down`,
      leaveIdx: -1,
      keep: ['What do I keep?', 'And if I say no?'],
      keepSay: 'You keep your name on the door. If you say no, we both find out what the Hook is worth. Well?',
      opts: [
        { agree: 1, say: ['Agreed.', 'I accept it.'], q: 'You accept it. It is not a thing that gets said twice. Yes?', yes: ['Yes. Agreed.', 'Yes.'], no: ['No. Not yet.', 'No.'], keep: ['What do I keep?', 'And if I say no?'], keepSay: 'Your name on the door. Yes?' },
        { refuse: 1, say: ['No. The Hook is not yours to give.', "No. I'll take my chance."], q: 'That is a no, to my face. You are sure?', yes: ["Yes. It's a no.", 'Yes.'], no: ['No. Wait.', 'No. Let me think.'], keep: ['What do I keep?', 'And if I say no?'], keepSay: 'Then we find out. You are sure?' },
        { say: ['Before you go on. I know how you hear about me, and what you would rather was not said.', 'There is something I know. Hear it first.'] },
      ],
    });
    if (i < 0) return void (await say(def.head, 'Then we sit again. Not many more times.'));
    const how = ['accept', 'defy', 'counter'][i],
      res = sitDown(id, how);
    if (!res.ok) return void (await say(def.head, 'You have nothing. Do not waste my afternoon. Well?'));
    await say(def.head, { accept: 'Good. Then we understand each other.', defy: 'Then we know where we are. Mind your people.', counter: 'I see. Then we are both holding something. That will do, for now.' }[how]);
  });

register({
  id: 'rivals',
  fresh: () => {
    const o = { fixer: { reads: [], truceUsed: false, meeting: null }, moves: [], log: [], extra: {}, knows: { jensen: [], agar: [], cammack: [] }, taxUntil: 0, inspectionAt: 0, offered: null };
    for (const id of IDS) o[id] = { rung: 0, shown: false, since: 0, used: [], paid: 0, holdUntil: 0, settled: null, answered: null, open: false, due: 0 };
    return o;
  },
  loaded(x) {
    if (!x.jensen) Object.assign(x, this.fresh());
    G.hooks.rivalFaresTimes = () => (st().taxUntil > G.t ? V.defyTaxFaresTimes : 1);
    G.hooks.rivalKnows = (id, fact) => {
      if (st().knows[id] && !st().knows[id].includes(fact)) st().knows[id].push(fact);
    };
    for (const id of IDS) if (x[id].rung >= 2 && !x[id].shown) deliver(id);
  },
  hourly(h) {
    const x = st();
    // the Fixer keeps his table at Rinaldi's of an afternoon, once the business has grown
    if (h === Math.floor(V.fixerFromHour) && actNow() >= V.startsFromAct && P_('garbutt')) send(P_('garbutt'), V.fixerAt, 'sit', Math.floor(G.t / 1440) * 1440 + V.fixerUntilHour * 60);
    for (const id of IDS) {
      const r = x[id];
      if (r.rung > 0 && !r.shown && G.t >= r.due) shownOnStreet(id);
      // a pressure left unanswered three days is taken as a no
      if (r.open && r.shown && G.t >= r.due + 2 * 1440) answer(id, 'defy');
    }
    if (x.inspectionAt && G.t >= x.inspectionAt) {
      x.inspectionAt = 0;
      const car = ((G.x.firm && G.x.firm.cars) || []).slice().reverse().find((c) => !c.off);
      if (car) {
        car.off = true;
        x.carBackAt = Math.round(G.t) + 2 * 1440;
        x.carOff = car.id;
        sub(`The council's man goes round every car with a clipboard. ${car.id.replace('car', 'Car')} fails on a tyre and comes off the road for two days.`, '', 'over', 7);
        note(`The council inspected the cars, as Mr Agar's letter said it would. ${car.id.replace('car', 'Car')} is off the road for two days.`, 'note', 'inspected' + Math.round(G.t), { how: 'Was there' });
      }
    }
    if (x.carBackAt && G.t >= x.carBackAt) {
      const car = ((G.x.firm && G.x.firm.cars) || []).find((c) => c.id === x.carOff);
      if (car) car.off = false;
      x.carBackAt = 0;
    }
  },
  daily() {
    if (actNow() < V.startsFromAct && !runEnded()) return;
    for (const id of IDS) advance(id);
  },
  beatFor(P) {
    const x = st();
    for (const id of IDS) {
      const r = x[id],
        def = V.rivals[id];
      if (r.settled) continue;
      if (r.rung === 1 && !r.shown && def.eyes.includes(P.id)) return () => noticed(id, P.id);
      if (r.rung >= 2 && r.rung <= 4 && P.id === def.man && (!r.shown || r.open)) return () => visit(id);
      if (r.rung === 5 && P.id === def.head) return () => table(id);
    }
    return null;
  },
  // a sit-down can happen in the back of his own cab: the head is waiting by the rank, and he lets them in
  carPrompts(out) {
    const x = st();
    for (const id of IDS) {
      const H = P_(V.rivals[id].head);
      if (x[id].rung === 5 && !x[id].settled && H && H.space === 'street' && Math.hypot(H.x - G.car.x, H.z - G.car.z) < 9 && Math.abs(G.car.v) < 0.5)
        out.push({ k: 'E', t: `Let ${id === 'jensen' ? 'her' : 'him'} get in the back`, run: () => table(id) });
    }
  },
  matters(P, a) {
    if (P.id !== 'garbutt') return;
    const x = st(),
      id = IDS.filter((k) => !x[k].settled).sort((p, q) => x[q].rung - x[p].rung)[0];
    if (!id) return;
    const mk = (what, sayIt, q) => ({
      say: sayIt,
      q,
      yes: ['Yes. Here.', 'Yes.'],
      no: ['No. Not today.', 'No.'],
      keep: ['Who do you work for?', 'Is it true, what you sell?'],
      keepSay: 'All three, and none. It is true, or nobody would pay twice. ' + q,
      take: () => {
        const r = fixer(what, id);
        return r.ok ? r.words : r.why;
      },
    });
    a.push({
      key: 'fixer',
      ask: `what he buys from the Fixer about ${HEADN[id]}`,
      raise: 'I sell three things, Mr Nowak. What is so, a chair at a table, and once only a fortnight of peace.',
      keep: ['Who do you work for?', 'Is it true, what you sell?'],
      keepSay: 'All three, and none. It is true, or nobody would pay twice.',
      opts: [mk('read', [`Tell me where I stand with ${HEADN[id]}.`, 'What is so. I will pay for that.'], 'Ten pounds, and I tell you what is so. Yes?'), mk('meeting', ['Get me a chair at the table.', 'I want a meeting.'], 'Twenty-five, and they will hear you. Yes?'), mk('truce', ['The fortnight of peace.', 'I will buy the truce.'], 'Sixty pounds. A fortnight. I sell it once and you are spending it now. Yes?')],
    });
  },
  hook: {
    state: () => st(),
    rung: (id) => st()[id].rung,
    sightings,
    // advance(rival, { force }): one rung, by the rules; with force the wait and the showing are taken as done
    advance: (id, o = { force: true }) => advance(id, o),
    show: (id) => shownOnStreet(id),
    answer,
    sitDown,
    fixer,
    know: (id, fact) => G.hooks.rivalKnows(id, fact),
    pressure: (id) => R.pressure(id, st()[id].rung),
    moves: () => st().moves,
    log: () => st().log,
    canAdvance: (id) => R.canAdvance(id, st()[id], ctxOf(id)),
  },
});
// a man of his who goes over takes what he knows with him: that rival now has a sighting of its own
on('crew:broke', (b) => {
  if (b.to !== 'rival') return;
  const x = st();
  (x.extra.jensen = x.extra.jensen || []).push({ by: V.rivals.jensen.eyes[0], e: 'broke:' + b.who, t: Math.round(G.t), how: 'told' });
});
// what his own people see at a rival's gate is something he knows
on('crew:order', (o) => {
  if (o.verb === 'watch_that' && G.hooks.crewAt && G.hooks.crewAt('dockGate')) G.hooks.rivalKnows('jensen', "what goes through the Widow's gate at night, seen by his own man");
});
void hour;
void first;
void near;
