// LEDGER, the whole game: the system "crew". Tom's power is people (DESIGN section 12; ADDENDUM A16, A40).
// Parts 1.7.1 orders in the field, 1.7.2 sending, 1.7.4 men at his side, 2.11.1 recruiting, 2.11.2 nerve, loyalty and
// breaking, 2.11.3 fates, 2.11.4 pay and the cut. The board (1.7.3) is in firm.js. Rules: pieces/crew_rules.js.
// No number of loyalty or nerve is ever on screen: a man shows it in what he says and where he stands.
import { register, emit, on } from './core.js';
import { G, hour } from '../state.js';
import { act, seed } from '../events.js';
import { sub, bubble } from '../ui.js';
import { note } from '../ledger.js';
import { target } from '../fight.js';
import { pay } from '../money.js';
import { goToPoint, send, release } from '../routines.js';
import { SPOTS } from '../map.js';
import { RULES } from '../rules.js';
import { PIECE } from './pieces/crew_rules.js';
import { TUNE as C } from './tune/crew.js';
import { P_, X, actNow, near, first, moneyAll } from './rise_util.js';

const R = PIECE.fns;
const st = () => X('crew');
const men = () => st().men;
const nerveOf = (id) => (RULES.people[id] ? RULES.people[id].nerveZeroToOne : 0.5);
const GATES = { dockGate: 'boxes', coldStore: 'row1', landing: 'shelter' };
const GATE_NAMES = { dockGate: 'the dock gate', coldStore: 'the cold store', landing: 'the landing' };
let followT = 0;

function freshMen() {
  const o = {};
  for (const id in C.inherited) {
    const d = C.inherited[id];
    o[id] = { id, role: d.role, can: d.can.slice(), road: null, nerve: nerveOf(id), loyalty: d.loyaltyStarts, ceiling: d.loyaltyCeiling, brittle: false, wear: 0, owedPence: 0, agreedPence: 0, signed: null, signShown: true, fate: null, withTom: false, post: null };
  }
  return o;
}
const say = (P, text) => {
  sub(text, first(P), 'face', 3.5);
  bubble(P, text, 3);
};
const gateNear = (x, z) => {
  for (const g in GATES) {
    const s = SPOTS[GATES[g]];
    if (s && Math.hypot(s[0] - x, s[1] - z) < 26) return g;
  }
  return null;
};
export function crewStrain(id, what) {
  const m = men()[id];
  if (m && !m.fate) men()[id] = R.strain(m, what);
  return men()[id];
}
const night = () => hour() >= 20 || hour() < 5;

// ---------- orders in the field: face the man, press the digit (two inputs at most, ER-CREW-01) ----------
function manAhead() {
  const T = target();
  if (T && men()[T.id] && !men()[T.id].fate) return T;
  let best = null,
    bd = C.orderReachMetres;
  for (const id in men()) {
    const P = P_(id);
    if (!P || men()[id].fate || !near(P, bd)) continue;
    bd = Math.hypot(P.x - G.tom.x, P.z - G.tom.z);
    best = P;
  }
  return best;
}
export function giveOrder(id, verb, o = {}) {
  const x = st(),
    m = men()[id],
    P = P_(id),
    t = G.tom;
  const ctx = { act: actNow(), near: o.near != null ? o.near : !!P && near(P, C.orderReachMetres), hasMark: !!x.mark, carrying: !!t.carry };
  const r = R.order(m, verb, ctx);
  if (P && ctx.near) say(P, r.say);
  else if (!r.ok) sub(r.say, '', 'over', 3);
  x.last = { t: Math.round(G.t), who: id, verb, ok: r.ok, say: r.say };
  if (!r.ok) return r;
  const M = x.mark ? P_(x.mark) : null;
  if (verb === 'with_me') {
    m.withTom = true;
    m.post = null;
    P.hold = true;
    if (night() && !m.agreedPence) {
      m.agreedPence = C.nightCutPence; // the cut is agreed in a line of talk before the job (A40)
      say(P, 'Behind you. A tenner for the night, as it was with Mickey.');
    }
  } else if (verb === 'wait_here') {
    m.withTom = false;
    goToPoint(P, P.x, P.z);
  } else if (verb === 'watch_that') {
    m.withTom = false;
    goToPoint(P, P.x, P.z);
    m.post = { x: Math.round(P.x), z: Math.round(P.z), zone: G.env.zone(P.x, P.z), since: Math.round(G.t), gate: gateNear(P.x, P.z), saw: [] };
    if (m.post.gate) note(`${P.def.name} stands at ${GATE_NAMES[m.post.gate]} for him now.`, 'note', 'post' + id + m.post.gate, { who: id, how: 'Told him to' });
  } else if (verb === 'fetch_him' || verb === 'lean_on') {
    m.withTom = false;
    goToPoint(P, M.x, M.z, RULES.routines.walkingMetresPerSecond * 1.4);
    x.pending.push({ type: verb, man: id, mark: x.mark, until: G.played + 45 });
  } else if (verb === 'take_this') {
    m.carrying = t.carry;
    t.carry = null;
    m.withTom = false;
    goToPoint(P, SPOTS.door[0], SPOTS.door[1]);
    x.pending.push({ type: 'take_this', man: id, thing: m.carrying, until: G.played + 60 });
  } else if (verb === 'drive') {
    x.pending.push({ type: 'drive', man: id, until: G.played + 15 });
  } else if (verb === 'thats_all') {
    m.withTom = false;
    m.post = null;
    P.hold = false;
    release(P);
  }
  emit('crew:order', { who: id, verb, target: x.mark || null });
  return r;
}
function settlePending(dt) {
  const x = st(),
    t = G.tom;
  for (const p of x.pending.slice()) {
    const P = P_(p.man),
      M = p.mark ? P_(p.mark) : null,
      m = men()[p.man];
    const there = M && Math.hypot(P.x - M.x, P.z - M.z) < 3;
    if (!there && G.played < p.until && p.type !== 'drive' && p.type !== 'take_this') continue;
    if ((p.type === 'drive' || p.type === 'take_this') && G.played < p.until) continue;
    x.pending.splice(x.pending.indexOf(p), 1);
    if (p.type === 'fetch_him') {
      const comes = M && !M.dead && (M.mind.fear > 0.15 || M.mind.regard > -0.2 || m.nerve > 0.8);
      if (comes) {
        goToPoint(M, t.x + 1.2, t.z + 0.6);
        seedBy('crew_fetched', p.man, p.mark);
        sub(`${first(P)} is bringing ${first(M)} over.`, '', 'over', 4);
      } else sub("He'll not come, boss. Not for me.", first(P), 'face', 4);
      goToPoint(P, t.x - 1, t.z - 1);
      m.withTom = true;
    } else if (p.type === 'lean_on') {
      if (M && !M.dead) {
        seedBy('crew_leaned', p.man, p.mark, true);
        M.mind.fear = Math.min(1, M.mind.fear + 0.25);
        men()[p.man] = R.strain(m, 'sentViolent');
        sub(`${first(P)} has a word with ${first(M)}, close, with a hand on his collar. It does not take long.`, '', 'over', 5);
        note(`Had ${P.def.name} lean on ${M.def.name}. ${first(P)} knows what was said, and so does ${first(M)}.`, 'note', 'lean' + p.man + p.mark + Math.round(G.t), { who: p.man, how: 'Told him to' });
      }
      goToPoint(P, t.x - 1, t.z - 1);
      men()[p.man].withTom = true;
    } else if (p.type === 'take_this') {
      x.stored.push(p.thing);
      m.carrying = null;
      P.hold = false;
      release(P);
      sub(`${first(P)}, back at the office: "It's in the drawer."`, '', 'over', 4);
      note(`${P.def.name} took the ${p.thing} to the office for him. It is in the locked drawer.`, 'note', 'took' + Math.round(G.t), { who: p.man, how: 'Told him to' });
    } else if (p.type === 'drive') {
      if (t.space === 'street' && !t.inCar) {
        // a crewman at the wheel is an AI driver and always brakes for people: the car is brought to the kerb beside Tom
        G.car.x = t.x + 3;
        G.car.z = t.z + 1;
        G.car.v = 0;
        say(P, "Car's at the kerb, boss.");
      } else say(P, "I'll have her outside when you come out.");
    }
  }
  void dt;
}
// What a man of his did, on his word: the man holds it and so does the one it was done to, who knows whose man came.
function seedBy(kind, via, targetId, seen) {
  const V = P_(via),
    Tg = P_(targetId);
  const E = seed(kind, [via, targetId], { target: targetId, name: Tg ? Tg.def.name : 'someone', via, viaName: V ? V.def.name : null, zone: Tg ? G.env.zone(Tg.x, Tg.z) : 'Quay Street', x: Tg ? Math.round(Tg.x) : 0, z: Tg ? Math.round(Tg.z) : 0 });
  const tm = Tg && Tg.mind.by[E.id];
  if (tm) {
    tm.who = 'owner';
    tm.sure = 0.7;
  }
  if (seen && Tg)
    for (const Q of G.named)
      if (Q.id !== via && Q.id !== targetId && !Q.dead && Q.space === Tg.space && Math.hypot(Q.x - Tg.x, Q.z - Tg.z) < 12 && !Q.mind.by[E.id]) {
        const r = { e: E.id, src: 'saw', from: null, who: 'owner', sure: 0.5, heat: 0.6, t: G.t, said: false, hop: 0, face: 0 };
        Q.mind.mem.push(r);
        Q.mind.by[E.id] = r;
        E.wit.push(Q.id);
      }
  return E;
}

// ---------- sending: the eight verbs, from Act II, each through a named man (D56) ----------
export function sendMan(id, verb, targetId) {
  const x = st(),
    m = men()[id],
    r = R.send(m, verb, { act: actNow(), target: targetId });
  x.last = { t: Math.round(G.t), who: id, verb, ok: r.ok, say: r.say };
  if (!r.ok) return r;
  const rec = { t: Math.round(G.t), verb, via: id, target: targetId, chain: r.chain, settleAt: Math.round(G.t) + C.sentSettlesAfterGameHours * 60, done: false, e: null };
  x.sent.push(rec);
  if (C.sent[verb].violent) men()[id] = R.strain(m, 'sentViolent');
  emit('crew:order', { who: id, verb, target: targetId });
  return r;
}
function settleSent(tm) {
  const x = st();
  for (const s of x.sent) {
    if (s.done || tm < s.settleAt) continue;
    s.done = true;
    const V = P_(s.via),
      Tg = P_(s.target),
      m = men()[s.via];
    if (!m || m.fate || !V || V.dead) {
      s.failed = 'the man was gone';
      note(`What ${V ? V.def.name : 'his man'} was sent to do never got done.`, 'note', 'sentfail' + s.t);
      continue;
    }
    const E = seedBy('sent_' + s.verb, s.via, s.target, C.sent[s.verb].violent);
    s.e = E.id;
    if (Tg) {
      if (s.verb === 'hurt') {
        Tg.mind.fear = Math.min(1, Tg.mind.fear + 0.4);
        send(Tg, 'home', 'idle', G.t + 1440);
      } else if (s.verb === 'lean_witness') {
        Tg.mind.fear = Math.min(1, Tg.mind.fear + 0.3);
        if (G.hooks.holdupReached) G.hooks.holdupReached(s.target);
      } else if (s.verb === 'vouch') Tg.mind.regard = Math.min(1, Tg.mind.regard + 0.15);
      else if (s.verb === 'discipline' && men()[s.target]) {
        men()[s.target] = R.strain(men()[s.target], 'paidShort');
        for (const k in men()) if (k !== s.target && k !== s.via) men()[k] = R.strain(men()[k], 'sawViolence');
      }
    }
    const name = Tg ? Tg.def.name : s.target;
    sub(`${first(V)}, quietly: "It's done."`, '', 'over', 5);
    note(`Sent ${V.def.name} to ${C.sent[s.verb].words}: ${name}. ${first(V)} says it is done. ${first(V)} knows, and so does whoever was there.`, 'note', 'sent' + s.t + s.verb, { who: s.via, how: first(V) + ' says', ev: E.id });
    emit('crew:sent', s);
  }
}

// ---------- recruiting, by a need or by a hook (2.11.1) ----------
function needMet(id) {
  const firm = X('firm'),
    cars = (firm.cars || []).length,
    drivers = (firm.cars || []).filter((c) => c.driver).length;
  if (id === 'julie') return cars > drivers || cars >= 2;
  if (id === 'megginson') return moneyAll() >= 500;
  if (id === 'lee') return (G.debts.lee && G.debts.lee.st !== 'open') || (G.x.rise && G.x.rise.rung >= 2);
  if (id === 'norman') return G.money.fareCount >= 3;
  if (id === 'karen') return (firm.cars || []).some((c) => c.rank === 'ferry');
  if (id === 'shaun') return cars >= 3;
  return false;
}
function hookHeld(id) {
  if (G.debts[id]) return G.debts[id].st === 'open';
  return !!st().hooksKnown[id];
}
export function recruit(id, road, o = {}) {
  const x = st();
  if (men()[id]) return { ok: false, why: 'He is the firm\'s already.' };
  const r = R.recruit(id, road, { needMet: o.force || needMet(id), hookHeld: o.force || hookHeld(id), nerve: nerveOf(id) });
  if (!r.ok) return r;
  x.men[id] = Object.assign(r.man, { agreedPence: 0, signShown: true });
  const P = P_(id);
  act(road === 'need' ? 'crew_joined' : 'crew_hooked', { target: id, silent: true, told: [id] });
  if (id === 'megginson' && road === 'need') pay(500, false, "keys cut at Megginson's");
  note(`${P ? P.def.name : id} works for the firm now: ${C.recruits[id].use}. ${road === 'need' ? 'He met what was needed, and it should hold.' : 'Held by what he has over them. That kind of hold is quick and brittle.'}`, 'note', 'recruit' + id, { who: id, how: 'Agreed it' });
  emit('crew:joined', { who: id, road });
  return r;
}

// ---------- nerve, loyalty and breaking (2.11.2), fates (2.11.3) ----------
const SIGNS = {
  looks_away: (P) => `${first(P)} does not meet his eye, and finds something to do with his hands.`,
  asks_cut: (P) => `${first(P)}: "I want what I'm owed. Before anything else."`,
  not_at_post: (P) => `Pauline, on the radio: "${first(P)} has not turned in. Nobody has seen him since last night."`,
};
function lookAt(id) {
  const x = st(),
    r = R.look(men()[id]),
    P = P_(id);
  men()[id] = r.man;
  if (r.sign && !r.broke && men()[id].signShown !== r.sign) {
    men()[id].signShown = false; // shown to him at the first chance (step), always before any break
    men()[id].signAt = Math.round(G.t);
    x.log.push({ t: Math.round(G.t), who: id, sign: r.sign });
    if (r.sign === 'not_at_post' && P) send(P, 'off', 'idle', G.t + 1440);
  }
  if (r.broke) {
    x.log.push({ t: Math.round(G.t), who: id, broke: r.broke });
    if (P) {
      P.hold = false;
      if (r.broke === 'rival') send(P, 'off', 'idle', G.t + 1440 * 60);
    }
    if (r.broke === 'police') seed('crew_talked', ['ellis'], { target: id, name: P ? P.def.name : id });
    note(r.broke === 'rival' ? `${P ? P.def.name : id} has gone to work for somebody else, and took what he knows with him.` : `${P ? P.def.name : id} has been to the police. What he did for the firm, they have now.`, 'note', 'broke' + id, { how: 'It came back' });
    sub(r.broke === 'rival' ? `${P ? first(P) : id} is not coming back. He works for somebody else now.` : `Word from the rank: ${P ? first(P) : id} was seen going into the station.`, '', 'over', 7);
    emit('crew:broke', { who: id, to: r.broke });
  }
  return r;
}
function fate(id, what) {
  const m = men()[id];
  if (!m) return null;
  m.fate = what;
  m.withTom = false;
  m.post = null;
  emit('crew:fate', { who: id, fate: what });
  return m;
}
// ---------- pay and the cut (2.11.4) ----------
export function payCut(id, pence, late) {
  const m = men()[id];
  if (!m || !m.agreedPence) return { ok: false, why: 'Nothing was agreed.' };
  if (pence > 0 && !pay(pence, false, 'a cut, to ' + id)) return { ok: false, why: 'He has not got it.' };
  const agreed = m.agreedPence,
    r = R.settle(m, agreed, pence, late);
  men()[id] = Object.assign(r.man, { agreedPence: r.man.owedPence });
  st().flows.push(Object.assign({ t: Math.round(G.t) }, r.flow));
  if (r.short) act('crew_paid_short', { target: id, silent: true, told: [id] });
  return { ok: true, short: r.short, man: men()[id] };
}

register({
  id: 'crew',
  fresh: () => ({ men: freshMen(), mark: null, pending: [], sent: [], log: [], stored: [], hooksKnown: {}, flows: [], last: null, lookDay: -1 }),
  loaded(x) {
    if (!x.men) x.men = freshMen();
    x.pending = []; // a save holds no order half carried out
    for (const id in x.men) x.men[id].withTom = false;
    G.hooks.sideMen = () => Object.keys(men()).filter((id) => men()[id].withTom && near(P_(id), 8));
    G.hooks.crewOdds = (foes) => R.odds(1 + G.hooks.sideMen().length, foes);
    G.hooks.crewStrain = crewStrain;
    G.hooks.crewAt = (gate) => Object.values(men()).some((m) => !m.fate && m.post && m.post.gate === gate);
  },
  step(dt) {
    if (G.paused) return;
    const x = st(),
      t = G.tom;
    settlePending(dt);
    // men at his side (A16): about two metres behind, out of his way, never left more than ten seconds behind
    followT -= dt;
    if (followT <= 0) {
      followT = 0.5;
      let i = 0;
      for (const id in men()) {
        const m = men()[id],
          P = P_(id);
        if (!m.withTom || !P || m.fate) continue;
        if (t.inCar || t.space !== 'street') continue; // he waits at the door, or rides: he is beside Tom again on the pavement
        const fp = R.followPoint(t.x, t.z, t.ang, C.followsAtMetres + i++ * 0.9),
          d = Math.hypot(P.x - fp.x, P.z - fp.z);
        m.lag = d > 4 ? (m.lag || 0) + 0.5 : 0;
        if (P.space !== 'street' || d > C.followerCatchesUpBeyondMetres || m.lag > C.followerLagsAtMostRealSeconds) {
          P.space = 'street';
          P.x = fp.x;
          P.z = fp.z;
          P.route = null;
          P.moving = false;
          m.lag = 0;
        } else if (d > 1.4) goToPoint(P, fp.x, fp.z, d > 5 ? RULES.tom ? 3.4 : 3 : RULES.routines.walkingMetresPerSecond);
      }
    }
    // a sign is shown to him the first time he is near the man (or at once, for a man who is not at his post)
    for (const id in men()) {
      const m = men()[id],
        P = P_(id);
      if (!m.signed || m.signShown !== false || m.fate) continue;
      if (m.signed === 'not_at_post' || (P && near(P, 6) && !t.inCar)) {
        m.signShown = m.signed;
        sub(SIGNS[m.signed](P), '', m.signed === 'asks_cut' ? 'face' : 'over', 6);
        note(m.signed === 'asks_cut' ? `${P.def.name} asked for his cut before anything else. He is owed.` : m.signed === 'not_at_post' ? `${P.def.name} was not at his post. Nobody has said why.` : `${P.def.name} would not look at him today.`, 'note', 'sign' + id + m.signAt, { who: id, how: 'Saw it' });
        x.log.push({ t: Math.round(G.t), who: id, shown: m.signed });
      }
    }
  },
  minute(tm) {
    settleSent(tm);
  },
  hourly(h) {
    // a man on a post is the firm's eyes there: who he saw go by (named people only, a few an hour)
    for (const id in men()) {
      const m = men()[id],
        P = P_(id);
      if (!m.post || m.fate || !P) continue;
      for (const Q of G.named)
        if (Q.id !== id && !Q.dead && Q.space === 'street' && Math.hypot(Q.x - m.post.x, Q.z - m.post.z) < C.rankEyesWithinMetres && m.post.saw.length < 12) m.post.saw.push({ who: Q.id, h, t: Math.round(G.t) });
    }
    // the night's cut falls due at six in the morning
    if (h === 6) for (const id in men()) if (men()[id].agreedPence && !men()[id].owedPence) men()[id].owedPence = men()[id].agreedPence;
  },
  daily(d) {
    const x = st();
    for (const id in men()) {
      const m = men()[id];
      if (m.fate) continue;
      if (m.owedPence > 0 && m.agreedPence) men()[id] = R.strain(m, 'paidLate');
      if (d % 7 === 0) men()[id] = R.strain(men()[id], 'quietWeek');
      lookAt(id);
    }
    x.lookDay = d;
  },
  hotspots(out) {
    const P = manAhead();
    if (!P || G.tom.inCar) return;
    const m = men()[P.id];
    out.push({ k: '1', t: m.withTom ? "That's all [8]" : `With me (orders: 1 to 8)`, run: () => giveOrder(P.id, m.withTom ? 'thats_all' : 'with_me') });
  },
  key(code) {
    if (!/^Digit[1-9]$/.test(code) || G.tom.inCar) return false;
    const x = st();
    if (code === C.orders.mark_him) {
      const T = target();
      if (!T || men()[T.id]) return false;
      x.mark = T.id;
      sub('Him.', '', 'over', 1.5);
      return true;
    }
    const P = manAhead();
    if (!P) return false;
    const verb = Object.keys(C.orders).find((k) => C.orders[k] === code);
    if (!verb) return false;
    giveOrder(P.id, verb);
    return true;
  },
  matters(P, a) {
    const x = st(),
      id = P.id,
      m = men()[id],
      D = Math.floor(G.t / 1440);
    if (m && !m.fate) {
      if (m.owedPence > 0) {
        const owed = m.owedPence;
        a.push({
          key: 'cut',
          ask: 'what this man is owed for the night',
          raise: m.signed === 'asks_cut' ? "I want what I'm owed. Before anything else." : "There's last night to square, boss.",
          keep: ['What was agreed?', 'Is it worth that?'],
          keepSay: 'A tenner for the night. Same as it was with Mickey.',
          opts: [
            { say: ["Here. All of it.", "That's what was agreed."], take: () => (payCut(id, owed, false).ok ? 'Right. Thanks, boss.' : "You've not got it on you. I can see that.") },
            { say: ["Half now. That's what there is.", 'Here is half.'], take: () => (payCut(id, Math.round(owed / 2), false).ok ? "Half. Right. I'll remember which half." : "You've not even got that.") },
          ],
        });
      } else if (m.signed && m.signed !== 'asks_cut' && P['off_steady'] !== D)
        a.push({
          key: 'steady',
          direct: true,
          ask: 'whether he stands by this man',
          raise: "It's been a lot, lately. I'm only saying.",
          opts: [
            {
              agree: 1,
              q: "You'd stand by me if it came to it? Say it.",
              yes: ['Yes. I stand by my people.', "Yes. You're mine and I look after mine."],
              no: ['No. Do as you are told.', 'No. Get on with it.'],
              keep: ['What has been a lot?', 'Who has been at you?'],
              keepSay: "Things I've done for you that I'd not tell my wife. Would you stand by me?",
              take: () => {
                P['off_steady'] = D;
                crewStrain(id, 'steadied');
                crewStrain(id, 'stoodBy');
                return "Right. That's all I wanted to hear.";
              },
            },
          ],
        });
      if (actNow() >= C.sentFromAct && x.mark && x.mark !== id && P_(x.mark)) {
        const Tg = P_(x.mark),
          tn = Tg.def.name;
        a.push({
          key: 'send',
          ask: `what he sends this man to do about ${tn}`,
          raise: `${tn}. What do you want done?`,
          keep: ['Can you do it quietly?', 'Who would know?'],
          keepSay: "I'd know, and they'd know. That's two more than now.",
          opts: Object.keys(C.sent).map((verb) => {
            const v = C.sent[verb];
            const o = {
              say: [v.words.charAt(0).toUpperCase() + v.words.slice(1) + '.', 'I want you to ' + v.words + '.'],
              take: () => sendMan(id, verb, x.mark).say,
            };
            if (v.cannotBeUndone)
              Object.assign(o, {
                q: 'That cannot be taken back once it is done. You are sure?',
                yes: ["Yes. I'm sure.", 'Yes. Do it.'],
                no: ['No. Leave it.', 'No. Not that.'],
                keep: ['Can you do it quietly?', 'Who would know?'],
                keepSay: "I'd know, and they'd know. You are sure?",
              });
            return o;
          }),
        });
      }
      return;
    }
    // a regular who could be the firm's: by a need (slow, holds) or by a hook (quick, brittle)
    const def = C.recruits[id];
    if (!def || m || P['off_recruit'] === D) return;
    const can = needMet(id),
      hook = hookHeld(id);
    if (!can && !hook) return;
    const opts = [];
    if (can)
      opts.push({
        agree: 1,
        say: ["There's a place for you at Mickey's.", 'Come and work for the firm.'],
        q: 'Work for you. Regular. You mean it?',
        yes: ['Yes. Start Monday.', 'Yes. I mean it.'],
        no: ['No. Not yet.', 'No. Let me think.'],
        keep: ['What would you want from it?', 'What can you do for the firm?'],
        keepSay: def.need + ' Do you mean it?',
        take: () => {
          P['off_recruit'] = D;
          return recruit(id, 'need').ok ? "Then I'm yours. You'll not regret it." : 'Not yet. Ask me again.';
        },
      });
    if (hook)
      opts.push({
        say: ['You owe, and I know what you did. You work for me now.', "You'll do as I ask. You know why."],
        q: 'So that is how it is. You would hold that over me?',
        yes: ['Yes. That is how it is.', 'Yes.'],
        no: ['No. Forget I said it.', 'No. Not like that.'],
        keep: ['What would you want from it?', 'What can you do for the firm?'],
        keepSay: 'You know what you have on me. Would you hold it over me?',
        take: () => {
          P['off_recruit'] = D;
          return recruit(id, 'hook').ok ? "Then I've no choice, have I. Tell me what you want." : 'You have nothing on me.';
        },
      });
    a.push({ key: 'recruit', ask: 'whether this person comes to work for the firm', raise: def.need, keep: ['What can you do for the firm?', 'What would you want from it?'], keepSay: `I can give you ${def.use}. ${def.need}`, opts });
  },
  hook: {
    men: () => men(),
    man: (id) => men()[id],
    setMan: (id, f) => Object.assign(men()[id], f),
    recruit: (id, road, o = { force: true }) => recruit(id, road, o),
    // order(id, verb, target): as if Tom stood by the man and gave it; target becomes the marked person
    order(id, verb, targetId) {
      if (targetId) st().mark = targetId;
      return giveOrder(id, verb, { near: true });
    },
    mark: (id) => (st().mark = id),
    send: (id, verb, targetId) => sendMan(id, verb, targetId),
    sent: () => st().sent,
    settleSent: () => settleSent(1e12),
    chain: (i) => (st().sent[i] ? st().sent[i].chain : null),
    look: (id) => lookAt(id),
    strain: crewStrain,
    payCut,
    fate,
    log: () => st().log,
    last: () => st().last,
    odds: (foes) => G.hooks.crewOdds(foes),
    side: () => G.hooks.sideMen(),
    orders: () => C.orders,
    needMet,
    hookHeld,
    knowHook: (id) => (st().hooksKnown[id] = true),
    flows: () => st().flows,
  },
});
on('fight:end', () => {
  for (const id of G.hooks.sideMen ? G.hooks.sideMen() : []) {
    crewStrain(id, 'sawViolence');
    crewStrain(id, 'stoodBy');
  }
});
on('arrest', () => {
  for (const id in men()) if (men()[id].withTom) crewStrain(id, 'policeAsked');
});
on('dial', (d) => {
  // at War a man can be killed for good, and each death is a named, permanent event: the rivals' side sees to it rarely
  if (d.state === 3) for (const id in men()) crewStrain(id, 'rivalThreat');
});
