// LEDGER, the whole game: street happenings (DESIGN-ADDENDUM A18). Authored, each with its spec and its check; placed
// by the town's state and the hour, never by dice (pieces/life_happen.js); each under two minutes, a choice with the
// hands, and something the town then knows. A stranger helped can turn up days later with a small favour.
import { X, emit } from './core.js';
import { G, day, hour } from '../state.js';
import { RULES } from '../rules.js';
import { PIECE } from './pieces/life_happen.js';
import { PIECE as CALP } from './pieces/calendar_days.js';
import { say, choose, scene, bubble, sub } from '../ui.js';
import { act } from '../events.js';
import { note } from '../ledger.js';
import { pay } from '../money.js';
import { clamp } from '../util.js';

const T = RULES.game.life.happenings;
const H = PIECE.fns;
let checkT = 0,
  callT = 0;
const regard = (id, by) => {
  const P = G.people[id];
  if (P && P.mind) P.mind.regard = clamp(P.mind.regard + by, -1, 1);
};
// What each one does when Tom chooses. Each returns { kind, what, line, favour?, helped?, mark? } and the town's
// memory of it is an ordinary act.
export const SPECS = [
  {
    id: 'shoplifter',
    street: 'Quay Street',
    x: 5.6,
    z: 9,
    fromHour: 9,
    untilHour: 17,
    needs: ['grocerOpen'],
    notIf: ['marketDay', 'sunday'],
    who: 'a lad in a tracksuit top',
    calls: ['Get out of my road!', 'Shift!'],
    prompt: 'Step in',
    text: 'A lad of twenty comes out of Hook Stores at a run with a tin under each arm. The grocer is in her doorway, shouting after him.',
    opts: ['Step into his way', 'Take his arm and walk him back', 'Let him go by'],
    run: async (i) => {
      if (i === 0) {
        await say('', 'He swerves, drops both tins and is gone round the corner. The grocer picks them up and looks at Tom a moment longer than she needs to.');
        regard('k_grocer', 0.25);
        return { kind: 'good_turn', what: 'stopped a lad running out of Hook Stores with two tins', line: 'Stopped a lad running out of Hook Stores. The grocer got her tins back.' };
      }
      if (i === 1) {
        const j = await choose('', '"It is for my mam. She has had nowt since Tuesday." He does not pull away.', ['Hand him to the grocer', 'Pay for the tins and let him go (90p)']);
        if (j === 1 && pay(90, false, 'paid for a lad\'s two tins at Hook Stores')) {
          await say('', 'The grocer takes the ninety pence and says nothing. The lad says "Ta, mister" and means it.');
          regard('k_grocer', 0.1);
          return { kind: 'good_turn', what: 'paid for a hungry lad\'s two tins at Hook Stores', line: 'Paid ninety pence for a lad\'s two tins and let him go.', helped: 'shoplifter' };
        }
        await say('', 'The grocer takes the tins and the lad\'s name. "I know his mother," she says. He looks at Tom all the way up the street.');
        regard('k_grocer', 0.3);
        return { kind: 'good_turn', what: 'marched a lad back to Hook Stores with what he had taken', line: 'Marched a lad back into Hook Stores. He will know Tom again.' };
      }
      await say('', 'He goes by close enough to touch. The grocer watches Tom watch him go.');
      regard('k_grocer', -0.15);
      return { kind: 'looked_away', what: 'stood by while a lad ran off from Hook Stores', line: 'Let a lad run off from Hook Stores. The grocer saw that he could have stopped him.' };
    },
  },
  {
    id: 'van',
    street: 'the back lane',
    x: 29.5,
    z: 14,
    fromHour: 7,
    untilHour: 18,
    needs: [],
    notIf: ['sunday'],
    who: 'a van driver',
    calls: ['Give us a push, pal?', 'She has died on me.'],
    prompt: 'See to the van',
    text: 'A bread van stands dead across the back lane, bonnet up. The driver has his sleeves rolled and oil to the elbow. Nothing can get past to the yards.',
    opts: ['Put a shoulder to it', 'Tell him to get it shifted', 'Walk round'],
    run: async (i) => {
      if (i === 0) {
        await say('', 'It takes the two of them and most of ten minutes to roll it against the garages. "Ta, pal. Hartley, Copper Row Bakery. If you are ever stuck for a lift, flag me."');
        return { kind: 'good_turn', what: 'pushed a broken-down bread van clear of the back lane', line: 'Pushed the bakery van clear of the back lane. Hartley, the driver, owes a lift.', helped: 'van' };
      }
      if (i === 1) {
        await say('', '"I would if I could, would I not?" He says it to Tom\'s back. He will know the face.');
        return { kind: 'hard_word', what: 'told a broken-down van driver to shift it', line: 'Told the bakery van driver to shift it. He did not like the telling.' };
      }
      return { kind: null, line: null };
    },
  },
  {
    id: 'row',
    street: 'Quay Street',
    x: 5.8,
    z: -46.5,
    fromHour: 17,
    untilHour: 21,
    needs: ['rentDay'],
    notIf: [],
    who: 'a lodger with a holdall',
    calls: ['You will get it Friday!', 'I am not stood here for this!'],
    prompt: 'The row on the step',
    text: 'On the step of Regent House a lodger with a holdall is having it out with Mrs Rennison, who has the door half shut and one foot behind it. Curtains move over the road.',
    opts: ['Step between them', 'Stand and listen', 'Walk on'],
    run: async (i) => {
      if (i === 0) {
        await say('', '"That will do. She has said her piece." The lodger looks at Tom, then at the street watching, and goes off down the pavement. Mrs Rennison shuts the door without a word, which from her is thanks.');
        regard('sylvia', 0.25);
        return { kind: 'good_turn', what: 'stepped between Mrs Rennison and a lodger on the step of Regent House', line: 'Stepped in on the step of Regent House. Mrs Rennison shut the door without a word.' };
      }
      if (i === 1) {
        await say('', 'Three weeks owing, and he works nights at the cold store for cash that never reaches her. Both of them see Tom listening.');
        regard('sylvia', -0.1);
        return { kind: 'looked_away', what: 'stood listening to a row on the step of Regent House', line: 'A lodger at Regent House owes three weeks and works nights at the Old Basin cold stores for cash.' };
      }
      return { kind: null, line: null };
    },
  },
  {
    id: 'lostman',
    street: 'the quay',
    x: -38,
    z: 48.5,
    fromHour: 10,
    untilHour: 17,
    needs: ['ferryIn'],
    notIf: [],
    who: 'a man with a suitcase',
    calls: ['Excuse me. Excuse me?', 'Is this Quay Street?'],
    prompt: 'The man with the suitcase',
    text: 'A man off the ferry stands on the quay with a suitcase and a piece of paper, turning it round. "Regent House? I start at the Harbour Office Monday and I cannot find my own lodgings."',
    opts: ['Tell him the way', 'Carry his case up for him', '"I am new here myself."'],
    run: async (i) => {
      if (i === 0) {
        const way = (G.hooks.wayTo && G.hooks.wayTo('regent')) || 'Up Quay Street, the top on the right.';
        await say('', `"${way}" He writes it on the paper. "Obliged to you."`);
        return { kind: 'good_turn', what: 'gave a stranger off the ferry the way to Regent House', line: 'Gave a man off the ferry the way to Regent House. He starts at the Harbour Office on Monday.', helped: 'lostman' };
      }
      if (i === 1) {
        await say('', 'It is the length of Quay Street with another man\'s case, and half the street sees it. At the door: "Pickering. Harbour Office, from Monday. Ask for me at the counter."');
        regard('sylvia', 0.1);
        return { kind: 'good_turn', what: 'carried a stranger\'s case the length of Quay Street to Regent House', line: 'Carried a case up to Regent House for Pickering, who starts at the Harbour Office counter on Monday.', helped: 'lostman', strong: true };
      }
      await say('', '"Ah." He turns the paper round again.');
      return { kind: null, line: null };
    },
  },
  {
    id: 'dog',
    street: 'the quay',
    x: 47,
    z: 53.5,
    fromHour: 6,
    untilHour: 10,
    needs: ['fishDockWorking'],
    notIf: [],
    who: 'a man stacking boxes',
    calls: ['Whose is that dog?', 'It will be in the dock in a minute.'],
    prompt: 'The loose dog',
    text: 'A wire-haired terrier is loose among the fish boxes, a length of string trailing from its collar, very pleased with itself. The collar says LAVERACK.',
    opts: ['Catch the string and take it home', 'Leave it be'],
    run: async (i) => {
      if (i === 0) {
        await say('', 'It lets itself be caught for a fish head. At the shop Brenda Laverack takes the string. "Third time this month. You are a gentleman. Do not tell him I said so."');
        regard('brenda', 0.3);
        return { kind: 'good_turn', what: 'caught Brenda Laverack\'s terrier loose on the fish dock and took it home', line: 'Took Brenda Laverack\'s terrier home off the fish dock.' };
      }
      return { kind: null, line: null };
    },
  },
  {
    id: 'lockedout',
    street: 'Chapel Lane',
    x: -50,
    z: -14.4,
    fromHour: 18,
    untilHour: 22,
    needs: ['dark', 'ironmongerShut'],
    notIf: [],
    who: 'a woman on her step',
    calls: ['Of all the nights.', 'I can see them. On the table.'],
    prompt: 'The woman locked out',
    text: 'A woman in a nurse\'s cape stands on her own step on Chapel Lane with her shopping at her feet. "My keys are on the kitchen table. I can see them through the letter box. And he is on nights."',
    opts: ['Knock next door for the spare', 'Put a shoulder to the door', 'Walk on'],
    run: async (i) => {
      if (i === 0) {
        await say('', 'Next door has the spare on a nail behind the meter, as next door always does. "Mrs Blakey, number nine. I will not forget it."');
        return { kind: 'good_turn', what: 'fetched the spare key for a woman locked out on Chapel Lane', line: 'Fetched the spare for Mrs Blakey, locked out at 9 Chapel Lane.', helped: 'lockedout' };
      }
      if (i === 1) {
        await say('', 'It goes at the second try, with a noise the whole lane hears. Two doors open. "Well. I did ask," she says, looking at the frame.');
        return { kind: 'forced_for', what: null, line: 'Put a shoulder to Mrs Blakey\'s door on Chapel Lane at her asking. The whole lane heard it.', helped: 'lockedout', mark: { kind: 'forced_door', x: -50, z: -13.4, name: '9 Chapel Lane' } };
      }
      return { kind: null, line: null };
    },
  },
];
const byId = Object.fromEntries(SPECS.map((s) => [s.id, s]));
const FAVOURS = {
  shoplifter: { text: 'The lad from Hook Stores falls in beside Tom for three steps. "Mister. There was a feller round the back of your yard last night, looking at the gate. Thought you would want telling."', note: 'The lad Tom let off at Hook Stores says a man was at the yard gate last night, looking it over.', fact: 'yardwatched' },
  van: { text: 'A bread van slows alongside. "Hartley. You pushed me out of that lane. Anywhere you want dropping, any morning, I am past your door at six."', note: 'Hartley of the Copper Row Bakery will give a lift any morning at six, no questions.', fact: 'lift' },
  lostman: { text: 'A man in a Harbour Office tie stops. "Pickering. You saw me right on my first day. If you ever want something looked up at the counter, ask for me by name."', note: 'Pickering at the Harbour Office counter will look a thing up if asked by name.', fact: 'harbour' },
  lockedout: { text: 'A dish under a cloth is on the office counter. Pauline: "A Mrs Blakey left it. Hot pot. She said you would know."', note: 'Mrs Blakey of Chapel Lane left a hot pot at the office. She nurses on the Infirmary\'s night ward.', fact: 'nurse' },
};
export function facts() {
  const d = day(),
    h = hour(),
    k = CALP.fns.dayKind(d);
  const open = (id) => !!(G.hooks.shopOpen ? G.hooks.shopOpen(id) : h >= 9 && h < 17);
  const f = {};
  if (open('ironmonger')) f.ironmongerOpen = true;
  else f.ironmongerShut = true;
  if (h >= RULES.shops.grocerOpensAtHour && h < RULES.shops.grocerShutsAtHour && !k.sunday) f.grocerOpen = true;
  if (k.market) f.marketDay = true;
  if (k.sunday) f.sunday = true;
  if (d % 7 === 3 || d % 7 === 4) f.rentDay = true;
  if ((h >= 10 && h < 11.25) || (h >= 13 && h < 14.25) || (h >= 15.5 && h < 16.75)) f.ferryIn = true;
  if (!k.sunday) f.fishDockWorking = true;
  if (h >= RULES.time.nightFullHour || h < RULES.time.dawnStartsHour) f.dark = true;
  return f;
}
function borrow(x, z) {
  // a walker nobody is looking at takes the part
  const t = G.tom;
  let best = null;
  for (const P of G.crowd || []) {
    if (!/^w\d+$/.test(P.id) || P.hold || P.borrowed || P.pax || P.mark) continue;
    const far = P.gone || P.space !== 'street' || Math.hypot(P.x - t.x, P.z - t.z) > 45;
    if (far && (!best || (P.gone && !best.gone))) best = P;
  }
  if (!best) return null;
  Object.assign(best, { gone: false, space: 'street', awake: true, x, z, hold: true, borrowed: true, route: null, moving: false, state: 'idle', ang: Math.atan2(t.x - x, t.z - z) });
  return best;
}
function giveBack(P) {
  if (!P) return;
  Object.assign(P, { hold: false, borrowed: false, gone: true, space: 'off', route: null, moving: false });
}
const actorOf = (a) => (a && a.pid ? (G.crowd || []).find((P) => P.id === a.pid) : null);
export function start(id, why) {
  const x = X('life').happen,
    s = byId[id];
  if (!s || x.active) return false;
  const P = borrow(s.x, s.z);
  x.active = { id, x: s.x, z: s.z, t0: G.played, pid: P ? P.id : null, street: s.street };
  x.placements.push({ id, day: day(), hour: Math.round(hour() * 10) / 10, because: why || 'asked for by a test', at: Math.round(G.played) });
  if (x.placements.length > 80) x.placements.shift();
  x.log.push({ id, street: s.street, t: G.played, day: day() });
  if (x.log.length > 60) x.log.shift();
  emit('happening', { id, x: s.x, z: s.z });
  return true;
}
function finish(outcome) {
  const x = X('life').happen,
    a = x.active;
  if (!a) return;
  giveBack(actorOf(a));
  x.active = null;
  const last = x.placements[x.placements.length - 1];
  if (last && last.id === a.id) {
    last.outcome = outcome;
    last.tookRealSeconds = Math.round(G.played - a.t0);
  }
}
async function choice(s) {
  const x = X('life').happen;
  let r = null;
  await scene(async () => {
    const i = await choose('', s.text, s.opts);
    r = await s.run(i < 0 ? s.opts.length - 1 : i);
  });
  if (r && r.kind) {
    const E = act(r.kind, Object.assign({ zone: s.street }, r.what ? { what: r.what } : {}));
    if (r.line) note(r.line, 'happening', 'hap_' + s.id + '_' + day(), { how: 'Was there', ev: E && E.id });
    if (r.mark && G.hooks.townMark) G.hooks.townMark(r.mark.kind, r.mark, 'tom');
  } else if (r && r.line) note(r.line, 'happening', 'hap_' + s.id + '_' + day(), { how: 'Was there' });
  if (r && r.helped) x.helped.push({ id: r.helped, day: day(), returned: false });
  finish(r && r.kind ? r.kind : 'walked on');
  if (G.hooks.save) G.hooks.save();
}
export function happenStep(dt) {
  const x = X('life').happen,
    t = G.tom;
  const a = x.active;
  if (a) {
    const s = byId[a.id];
    callT -= dt;
    const P = actorOf(a);
    if (P && callT <= 0 && Math.hypot(t.x - a.x, t.z - a.z) < 25 && t.space === 'street') {
      bubble(P, s.calls[Math.floor(G.played / 7) % s.calls.length], 3.5);
      callT = 7;
    }
    if (G.played - a.t0 > T.endsAfterRealSeconds) finish('nobody came');
    return;
  }
  checkT += dt;
  if (checkT < T.checkedEveryRealSeconds) return;
  checkT = 0;
  if (t.space !== 'street' || G.story.ended || !G.story.flags.tour) return; // not before he has an office to stand in
  const st = { hour: hour(), day: day(), wet: G.weather.rain > 0.55, facts: facts(), log: x.log };
  // only what he can come upon: those within reach of where he is, and not under his nose
  const near = SPECS.filter((s) => {
    const d = Math.hypot(s.x - (t.inCar ? G.car.x : t.x), s.z - (t.inCar ? G.car.z : t.z));
    return d < T.startsWithinMetres * 2.2 && d > 12;
  });
  const p = H.place(near, st, G.played, T);
  if (p) start(p.id, p.because);
}
export function happenHotspots(out) {
  const a = X('life').happen.active,
    t = G.tom;
  if (!a || t.space !== 'street' || Math.hypot(t.x - a.x, t.z - a.z) > 3.4) return;
  const s = byId[a.id];
  out.push({ k: 'E', t: s.prompt, run: () => choice(s) });
}
// A stranger he helped comes back days later with a small favour (A18, "returns later").
export function favourStep(d, h) {
  const x = X('life'),
    t = G.tom;
  if (h < 9 || h > 18 || G.paused || t.space === 'away') return;
  const due = H.favourDue(x.happen.helped, d, T);
  if (!due.length) return;
  const id = due[0],
    f = FAVOURS[id],
    rec = x.happen.helped.find((r) => r.id === id && !r.returned);
  rec.returned = true;
  if (!f) return;
  x.favours[f.fact] = d;
  sub(f.text, '', 'over', 9);
  note(f.note, 'happening', 'favour_' + id + '_' + d, { how: 'Told to his face' });
  emit('favour', { id, fact: f.fact });
}
export const happenHook = {
  happenings: () => SPECS.map((s) => ({ id: s.id, street: s.street, fromHour: s.fromHour, untilHour: s.untilHour, needs: s.needs, notIf: s.notIf, choices: s.opts.length, x: s.x, z: s.z })),
  happenFacts: facts,
  happenStart: start,
  happenWhyNot: (id) => H.whyNot(byId[id], { hour: hour(), day: day(), wet: G.weather.rain > 0.55, facts: facts(), log: X('life').happen.log }, G.played, T),
  happenChoose: (id) => choice(byId[id]),
  favourStep,
};
