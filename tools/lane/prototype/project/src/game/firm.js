// LEDGER, the whole game: the system "firm". The firm grows: fleet, drivers, ranks, accounts, fronts and rounds, and
// the board (DESIGN sections 12 and 14; ADDENDUM A14, A15). Parts 1.7.3, 2.15.1, 2.15.2, 2.17.
// All of it is run on the board and through people: no screen of numbers (ER-FIRM-01, ER-FRONT-02).
import { register, emit } from './core.js';
import { G, day, hour } from '../state.js';
import { act } from '../events.js';
import { sub, say, choose, scene } from '../ui.js';
import { note } from '../ledger.js';
import { pay, earn } from '../money.js';
import { roomPos, SPOTS } from '../map.js';
import { PIECE } from './pieces/firm_rules.js';
import { TUNE as F } from './tune/firm.js';
import { TUNE as C } from './tune/crew.js';
import { P_, X, actNow, rungNow, moneyAll, first } from './rise_util.js';

const R = PIECE.fns;
const st = () => X('firm');
const men = () => X('crew').men || {};
const names = () => {
  const o = { mal: 'Mal', tom: 'himself' };
  for (const id in G.people) if (G.people[id] && !G.people[id].anon) o[id] = first(G.people[id]);
  return o;
};
const dress = () => (G.x.shops && G.x.shops.outfit != null ? G.x.shops.outfit : (G.x.rise && G.x.rise.outfit) || 0);
const freeMan = () => {
  const x = st(),
    busy = new Set(Object.values(x.fronts).concat(Object.values(x.rounds)).map((s) => s.man));
  return ['julie', 'darren', 'karen', 'shaun', 'megginson', 'lee', 'ron'].find((id) => men()[id] && !men()[id].fate && !busy.has(id)) || null;
};

function buyCar(o = {}) {
  const x = st(),
    r = R.buyCar(x, o.free ? 1e9 : moneyAll());
  if (!r.ok) return r;
  if (!o.free && !pay(r.pence, false, 'a car, bought off Dennis Iveson')) return { ok: false, why: 'He has not got it.' };
  x.cars.push(r.car);
  act('car_bought', { target: F.carSeller, silent: true, told: [F.carSeller] });
  // a driver for it: a recruit who can drive, else from the fourth car a stranger who asked at the counter
  const d = Object.keys(men()).find((id) => men()[id].can.includes('drive') && !men()[id].fate && !x.cars.some((c) => c.driver === id));
  const who = d || (x.cars.length >= F.strangerDriverFromCars ? 'mal' : null);
  if (who && who !== 'mal') x.cars = R.crew(x, r.car.id, who).cars;
  else if (who === 'mal' && !x.cars.some((c) => c.driver === 'mal')) x.cars = R.crew(x, r.car.id, 'mal').cars;
  if (x.cars.length >= F.nightDeskFromCars && !x.nightDesk) {
    x.nightDesk = true;
    note('The office keeps a night desk now, and a second telephone has gone in.', 'note', 'nightdesk', { how: 'Arranged it' });
  }
  const c = x.cars[x.cars.length - 1];
  note(`Bought a car off Dennis Iveson. ${c.id.charAt(0).toUpperCase() + c.id.slice(1)} is on the board${c.driver ? ', with ' + (names()[c.driver] || c.driver) + ' driving' : ', with nobody to drive it yet'}.`, 'note', 'car' + x.cars.length, { who: F.carSeller, how: 'Bought it' });
  emit('firm:car', { car: c });
  return { ok: true, car: c };
}
function place(carId, rankId) {
  const x = st(),
    r = R.place(x, carId, rankId);
  if (r.ok) {
    x.cars = r.cars;
    x.boardDay = day();
  }
  return r;
}
function account(id, viaId, o = {}) {
  const x = st(),
    r = R.account(x, id, { rung: o.force ? 4 : rungNow(), dress: o.force ? 2 : dress(), met: [viaId] });
  if (!r.ok) return r;
  x.accounts[id] = true;
  act('account_won', { target: viaId, what: r.name, silent: true, told: [viaId] });
  note(`The firm has ${r.name}, through ${P_(viaId) ? P_(viaId).def.name : viaId}. Its fares go in the book every day.`, 'note', 'account' + id, { who: viaId, how: 'Agreed it' });
  if (id === 'solicitor') x.brief = true;
  emit('firm:account', { id });
  return r;
}
function front(id, how, o = {}) {
  const x = st(),
    f = F.fronts[id],
    K = f && P_(f.keeper),
    man = o.man || freeMan();
  const zone = K ? G.env.zone(K.x, K.z) : 'Quay Street';
  const r = R.front(x, id, how, { man, moneyPence: moneyAll(), keeper: K ? { regard: K.mind ? K.mind.regard : 0, fear: K.mind ? K.mind.fear : 0 } : {}, streetOnEdge: G.hooks.streetOnEdge ? G.hooks.streetOnEdge(zone) : false });
  if (how === 'pressure') act('front_pressed', { target: f ? f.keeper : undefined, what: f ? f.name : '' });
  if (!r.ok) return r;
  if (r.pence && !pay(r.pence, false, 'a share of ' + f.name)) return { ok: false, why: 'He has not got it.' };
  x.fronts[id] = r.front;
  if (how !== 'pressure') act('front_bought', { target: f.keeper, what: f.name, silent: true, told: [f.keeper] });
  note(`A share of ${f.name}, with ${names()[man] || man} put in to mind it. Its money, and any trouble, come through ${names()[man] || man}.`, 'note', 'front' + id, { who: man, how: 'Arranged it' });
  emit('firm:front', { id, man });
  return r;
}
function round(id, man) {
  const x = st();
  if (!F.rounds[id] || x.rounds[id]) return { ok: false, why: 'No such round, or it is his already.' };
  if (!man || !men()[man] || men()[man].fate) return { ok: false, why: 'It needs one of his men to walk it.' };
  x.rounds[id] = { man };
  act('round_taken', { what: F.rounds[id].name, silent: true, told: [man] });
  note(`${names()[man]} collects on ${F.rounds[id].name} for him now, of a Saturday. What comes of it comes through ${names()[man]}.`, 'note', 'round' + id, { who: man, how: 'Told him to' });
  emit('firm:round', { id, man });
  return { ok: true };
}
// A day ends: ranks worked, the day's fares without him, Pauline keeping the board if he has not.
function dayEnd() {
  const x = st();
  if (x.boardDay < day() - 2 && !x.ranks.ferry?.held) {
    const spare = x.cars.find((c, i) => i >= 2 && c.driver && c.rank === 'mickeys');
    if (spare) spare.rank = 'ferry'; // if he never touches the board, Pauline runs it
  }
  const rd = R.rankDay(x);
  x.ranks = rd.ranks;
  for (const id of rd.won) {
    act('rank_won', { what: F.ranks[id].name, silent: true, told: ['pauline'] });
    note(`${F.ranks[id].name.charAt(0).toUpperCase() + F.ranks[id].name.slice(1)} is the firm's now. A Mickey's car has stood on it every day and nobody says otherwise.`, 'note', 'rank' + id, { who: 'pauline', how: 'Pauline says' });
    sub(`Pauline, on the radio: "${F.ranks[id].name.replace('the ', 'The ')} is ours. Nobody else has stood on it all week."`, '', 'over', 6);
    emit('firm:rank', { id });
  }
  // the first two cars' fares are the old game's own; here the cars and accounts the firm has gained
  const fares = R.dayFares(Object.assign({}, x, { cars: x.cars.slice(2) }), G.hooks.holdupFaresTimes ? { mickeys: G.hooks.holdupFaresTimes() } : {});
  if (fares.pence) {
    earn(fares.pence, false, "the day's fares from the firm's other cars and its accounts");
    G.money.fares += fares.pence;
    G.money.sinceWash += fares.pence;
    x.flows.push(...fares.flows.map((f) => Object.assign({ t: Math.round(G.t) }, f)));
    if (x.flows.length > 120) x.flows.splice(0, 40);
  }
  return { won: rd.won, fares };
}
// Saturday morning: the fronts' and rounds' money, each through its man.
function weekEnd() {
  const x = st(),
    w = R.week(x, men());
  for (const f of w.flows) {
    earn(f.pence, f.to === 'the tin', f.from + ', ' + f.why);
    x.flows.push(Object.assign({ t: Math.round(G.t) }, f));
  }
  x.washExtraPence = w.washExtraPence;
  for (const tr of w.trouble) {
    const M = P_(tr.through);
    sub(M ? `${first(M)}, not quite looking at him: "${tr.at.replace(/^the /, 'The ')}. ${tr.what === 'it came short' ? 'It came short this week.' : 'Nobody could collect.'}"` : `Nobody brought the money from ${tr.at}.`, '', 'over', 6);
    note(`${tr.at.charAt(0).toUpperCase() + tr.at.slice(1)}: ${tr.what}. It reached him through ${names()[tr.through] || tr.through}.`, 'note', 'trouble' + tr.at + day(), { who: M ? tr.through : undefined, how: M ? first(M) + ' says' : 'Nobody came' });
  }
  if (w.flows.length) sub('Saturday. The men bring what the week made, each in his own envelope.', '', 'over', 5);
  emit('firm:week', w);
  return w;
}
function wagesDay() {
  const x = st(),
    extra = Object.assign({}, x, { cars: x.cars.slice(2) }),
    w = R.wages(extra, C.driverWeekPence, G.money.clean);
  if (!w.due) return w;
  if (w.paid) pay(w.paid, true, "the drivers' wages");
  x.unpaid = w.unpaid;
  for (const d in w.unpaid) if (G.hooks.crewStrain) G.hooks.crewStrain(d, 'paidLate');
  for (const d of extra.cars.map((c) => c.driver).filter((d) => d && !w.unpaid[d])) if (G.hooks.crewStrain) G.hooks.crewStrain(d, 'paidFair');
  if (Object.keys(w.unpaid).length) {
    act('wages_missed', { silent: true, told: ['sheila'] });
    sub("Sheila: \"There is not enough in the book for Friday's wages. Somebody goes home short, and they will say so.\"", '', 'face', 7);
    note("Could not pay every driver on Friday. Sheila said who went short.", 'money', 'wages' + day(), { who: 'sheila', how: 'Sheila says' });
  }
  for (const d of w.left) {
    const c = x.cars.find((k) => k.driver === d);
    if (c) c.driver = null;
    delete x.unpaid[d];
    if (men()[d]) men()[d].fate = 'left unpaid';
    note(`${names()[d] || d} has left the firm: two Fridays with no wage. The car stands in the yard.`, 'note', 'left' + d, { how: 'Sheila says' });
    emit('firm:left', { who: d });
  }
  return w;
}
const boardLines = () => R.board(st(), names());
const boardScene = () =>
  scene(async () => {
    const x = st(),
      t0 = G.played;
    const lines = boardLines();
    await say('', 'The board, in chalk. ' + lines.join('. ') + '.');
    const moves = [];
    for (const c of x.cars) if (c.driver && c.driver !== 'tom') for (const r in F.ranks) if (r !== (c.rank || 'mickeys')) moves.push({ c: c.id, r });
    const opts = ['Leave it as it stands.'].concat(moves.slice(0, 5).map((m) => `${m.c.charAt(0).toUpperCase() + m.c.slice(1)} to ${F.ranks[m.r].name}.`));
    const i = await choose('', 'Chalk in his hand.', opts);
    if (i > 0) {
      const m = moves[i - 1];
      place(m.c, m.r);
      await say('pauline', `${m.c.charAt(0).toUpperCase() + m.c.slice(1)}, ${F.ranks[m.r].name}. I'll call it.`);
    }
    x.boardDay = day();
    x.boardSecs = (x.boardSecsDay === day() ? x.boardSecs : 0) + (G.played - t0);
    x.boardSecsDay = day();
  });

register({
  id: 'firm',
  fresh: () => ({
    cars: [
      { id: 'car one', driver: 'kevin', rank: 'mickeys', off: false },
      { id: 'car two', driver: 'terry', rank: 'mickeys', off: false },
    ],
    ranks: {},
    accounts: {},
    fronts: {},
    rounds: {},
    unpaid: {},
    nightDesk: false,
    brief: false,
    washExtraPence: 0,
    boardDay: -9,
    boardSecs: 0,
    boardSecsDay: -1,
    radio: [],
    flows: [],
  }),
  loaded(x) {
    if (!x.cars) Object.assign(x, this.fresh());
    // an alibi or a witness: a cab of the firm's on a rank near where he was (the driver saw him there)
    G.hooks.alibi = (px, pz) => {
      for (const c of st().cars) {
        const s = SPOTS[F.ranks[c.rank || 'mickeys'].spot];
        if (c.driver && c.driver !== 'tom' && !c.off && s && Math.hypot(s[0] - px, s[1] - pz) < C.alibiWithinMetres) return c.driver;
      }
      return null;
    };
    G.hooks.firmWashExtra = () => st().washExtraPence || 0;
  },
  hourly(h, d) {
    const x = st();
    // a car on a rank is the firm's eyes there: what its driver sees goes over the radio
    for (const c of x.cars) {
      if (!c.driver || c.driver === 'tom' || c.off) continue;
      const s = SPOTS[F.ranks[c.rank || 'mickeys'].spot];
      for (const id of ['ellis', 'pc', 'gary', 'clive', 'dean', 'garbutt', 'jensen', 'agar', 'cammack']) {
        const Q = P_(id);
        if (!Q || Q.gone || Q.space !== 'street' || Math.hypot(Q.x - s[0], Q.z - s[1]) > C.rankEyesWithinMetres) continue;
        x.radio.push({ t: Math.round(G.t), car: c.id, rank: c.rank || 'mickeys', saw: id });
        if (x.radio.length > 30) x.radio.shift();
        if (G.tom.inCar || G.tom.space === 'mickeys') sub(`${c.id.replace('car', 'Car')}, ${F.ranks[c.rank || 'mickeys'].name}: "${Q.def.desc.replace(/^./, (m) => m.toUpperCase())} just went by."`, 'On the radio', 'over', 5);
      }
    }
    if (d % 7 === C.wagesDayIndex && h === 17) wagesDay();
    if (d % 7 === F.weekSettlesOnDayIndex && h === F.weekSettlesAtHour) weekEnd();
  },
  daily() {
    dayEnd();
  },
  hotspots(out) {
    const t = G.tom;
    if (t.space !== C.boardAtRoom) return;
    const [bx, bz] = roomPos(C.boardAtRoom, C.boardAt[0], C.boardAt[1]);
    if (Math.hypot(t.x - bx, t.z - bz) < C.boardWithinMetres + 0.8) out.push({ k: 'T', t: 'The board', run: boardScene });
  },
  matters(P, a) {
    const x = st(),
      id = P.id,
      D = day();
    const once = (k) => {
      if (P['off_' + k] === D) return false;
      return true;
    };
    const done = (k) => (P['off_' + k] = D);
    // a car, from a man selling one
    if (id === F.carSeller && rungNow() >= 1 && (G.x.acts ? actNow() >= 2 : G.story.flags.choice === 'take') && x.cars.length < F.carsAtMost && once('car') && G.debts.dennis.st !== 'open')
      a.push({
        key: 'car',
        ask: 'whether he buys a car off Dennis Iveson',
        raise: "I've a runner in the yard. Four doors, taxed, a hundred and eighty. It would take a roof sign.",
        keep: ['Does it run?', 'Where did it come from?'],
        keepSay: 'It runs. It came from a man who needed a hundred and eighty less than I do.',
        opts: [
          {
            say: ["I'll take it.", "A hundred and eighty. It's mine."],
            q: 'A hundred and eighty, cash. Yes?',
            yes: ['Yes. Cash.', 'Yes.'],
            no: ['No. Not today.', 'No. Leave it.'],
            keep: ['Does it run?', 'Where did it come from?'],
            keepSay: 'It runs. A hundred and eighty. Yes?',
            take: () => {
              done('car');
              const r = buyCar();
              return r.ok ? "Keys are in it. Tell Pauline she's another on the board." : r.why;
            },
          },
        ],
      });
    // accounts, each through its person
    for (const aid in F.accounts) {
      const A = F.accounts[aid];
      if (A.via !== id || x.accounts[aid] || !once('acc')) continue;
      const can = R.account(x, aid, { rung: rungNow(), dress: dress(), met: [id] });
      a.push({
        key: 'account',
        direct: true,
        ask: `whether the firm takes on ${A.name}`,
        raise: aid === 'coldstore' ? 'The packing shift wants cabs, morning and evening. The firm they had let them down. I could say a word for Mickey\'s.' : aid === 'harbour' ? "The Board's late men need running home after ten. It goes out to whoever the cold store trusts." : 'A solicitor I know wants a car on account. Quiet drivers. I can make the appointment.',
        opts: [
          {
            agree: 1,
            q: 'Shall I say the word?',
            yes: ['Yes. Say it.', "Yes. We'll cover it."],
            no: ['No. Not yet.', 'No. We are not ready.'],
            keep: ['What does it need?', 'Who decides?'],
            keepSay: 'Cars enough to cover it, every day, and a name they have heard. Shall I say the word?',
            take: () => {
              done('acc');
              if (!can.ok) return can.why;
              account(aid, id);
              return "Then it's yours. Don't make me look a fool.";
            },
          },
        ],
      });
    }
    // fronts, through whoever keeps the business
    for (const fid in F.fronts) {
      const f = F.fronts[fid];
      if (f.keeper !== id || x.fronts[fid] || actNow() < 2 || rungNow() < 2 || !once('front')) continue;
      const mk = (how, sayIt, q) => ({
        say: sayIt,
        q,
        yes: ['Yes. That is the offer.', 'Yes.'],
        no: ['No. Forget it.', 'No. Another time.'],
        keep: ['How is trade?', 'Who else has asked?'],
        keepSay: 'Trade is what it is. Nobody has asked. ' + q,
        take: () => {
          done('front');
          const r = front(fid, how);
          return r.ok ? 'Then we are partners, of a sort. Send me somebody I can stand to look at.' : r.why;
        },
      });
      a.push({
        key: 'front',
        ask: `whether he takes a share of ${f.name}`,
        raise: 'It is not what it was. Half the street buys on tick and the other half has gone.',
        keep: ['How is trade?', 'Who else has asked?'],
        keepSay: 'Trade is what it is. Nobody has asked.',
        opts: [mk('money', ['I would put money into it.', 'I will buy a share.'], 'You would put money in, for a share? You mean it?'), mk('favour', ['You said you owed me one.', 'Call it a favour returned.'], 'A share, for what I owe you? Is that it?'), mk('pressure', ['It would be a pity if anything happened to it.', 'You want me as a partner. Believe me.'], 'Is that a threat? Say it plain.')],
      });
    }
    // a round, walked by one of his men
    if ((id === 'ron' || id === 'lee') && men()[id] && !men()[id].fate && actNow() >= 2 && rungNow() >= 2 && once('round')) {
      const rid = Object.keys(F.rounds).find((r) => !x.rounds[r]);
      if (rid)
        a.push({
          key: 'round',
          direct: true,
          ask: `whether this man starts collecting on ${F.rounds[rid].name}`,
          raise: `${F.rounds[rid].name.replace(/^the /, 'The ')} paid Mickey once, for a quiet life. Nobody has asked them since. I could ask.`,
          opts: [
            {
              agree: 1,
              q: 'Do I start asking? Once I ask, they all know who sent me.',
              yes: ['Yes. Start Saturday.', 'Yes. Ask them.'],
              no: ['No. Leave them be.', 'No. Not that.'],
              keep: ['What did they pay?', 'What if they say no?'],
              keepSay: 'A few pounds each. If they say no I come back and tell you, and then it is your problem. Do I start asking?',
              take: () => {
                done('round');
                return round(rid, id).ok ? 'Saturday, then.' : 'Not this week.';
              },
            },
          ],
        });
    }
  },
  hook: {
    state: () => st(),
    // buy(what, opts): 'car' | 'front:<id>' | 'round:<id>' | 'account:<id>'; opts { free, how, man, via, force }
    buy(what, o = {}) {
      const [k, id] = String(what).split(':');
      if (k === 'car') return buyCar(o);
      if (k === 'front') return front(id, o.how || 'money', o);
      if (k === 'round') return round(id, o.man || 'ron');
      if (k === 'account') return account(id, o.via || F.accounts[id].via, o);
      return { ok: false, why: 'a car, a front, a round or an account' };
    },
    crew: (carId, driverId) => {
      const r = R.crew(st(), carId, driverId);
      if (r.ok) st().cars = r.cars;
      return r;
    },
    place,
    board: boardLines,
    dayEnd,
    weekEnd,
    wagesDay,
    alibi: (px, pz) => G.hooks.alibi(px, pz),
    radio: () => st().radio,
    flows: () => st().flows,
    boardSeconds: () => st().boardSecs,
  },
});
void hour;
