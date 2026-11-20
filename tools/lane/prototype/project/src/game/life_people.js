// LEDGER, the whole game: calling on people (DESIGN-ADDENDUM A39), someone worth being honest for (3.2.5) and the
// boxing club (A28). A visit is possible only where and when the person's routine allows, shows no score, is over
// in under two minutes, and a second call inside a day draws a cooler answer. No stakes anywhere in a pastime.
import { X, PLACES, emit } from './core.js';
import { G, day, hour } from '../state.js';
import { RULES } from '../rules.js';
import { PIECE } from './pieces/life_rules.js';
import { say, choose, scene } from '../ui.js';
import { act } from '../events.js';
import { note, meet, ledgerSeen } from '../ledger.js';
import { slot } from '../routines.js';
import { attached } from '../seeing.js';
import { comebackLine } from '../talk_lines.js';
import { advanceTo } from '../work.js';
import { clamp } from '../util.js';

const T = RULES.game.life;
const LR = PIECE.fns;
// where each may be called on: the places of their routine that are theirs to sit in
const CALLS = {
  alison: { in: ['caff'], prompt: 'Sit down with Alison Sedman', home: null },
  danby: { in: ['home', 'tearoom', 'bench'], prompt: 'Sit a while with Philip Danby', home: { x: -42, z: -14.4, prompt: "Knock at Philip Danby's door" } },
};
const SMALL = {
  alison: [
    ['I had a piece spiked today. Dredging. Nobody reads dredging, but somebody is paid not to dredge.', 'Do you ever want to be told you are wrong, Mr Nowak? I do. Nobody will oblige.'],
    ['My editor says leave the row alone. He said it nicely. That is how I know it matters.', 'You could be a decent man in an indecent chair. I have not decided.'],
    ['I was born over the bridge. I can hear when this side of it goes quiet.', 'Tell me something that is not for the paper. I am told I can keep one.'],
  ],
  danby: [
    ['I read the same six books. They change, which is more than the street does.', 'Your uncle came to one parents\' evening. For June. He stood at the back.'],
    ['When the school shut they offered me Hull. I looked at the map and stayed.', 'People tell a teacher things for years after. It is a habit. I try to deserve it.'],
    ['Father Walsh thinks I should pray. I think he should read. We meet at chess.', 'You can tell me the truth or nothing. I have no use for the middle thing.'],
  ],
};
const placeOfRoutine = (P) => {
  const w = String(slot(P).where || '');
  return w.split(':')[0];
};
export function canCall(id) {
  const P = G.people[id],
    c = CALLS[id];
  if (!P || !c || P.dead || P.gone) return { ok: false, why: 'gone' };
  if (!(G.ledger.met || {})[id] && !G.story.flags['met_' + id]) return { ok: false, why: 'not met' };
  return LR.canCall(placeOfRoutine(P), c.in, hour(), T.calls);
}
function recount() {
  const x = X('life'),
    c = x.calls;
  const a = LR.friendship(c.alison, !!c.brokenAlison, T.calls),
    d = LR.friendship(c.danby, !!c.brokenDanby, T.calls);
  const good = (v) => v.filter((q) => q.honest && !q.cool).length;
  const who = a.holds ? 'alison' : d.holds ? 'danby' : good(c.alison) >= good(c.danby) ? (c.alison.length ? 'alison' : c.danby.length ? 'danby' : null) : 'danby';
  x.friend = { who, holds: who === 'alison' ? a.holds : who === 'danby' ? d.holds : false, word: who === 'alison' ? a.word : who === 'danby' ? d.word : 'slight', alison: a.word, danby: d.word };
  emit('friend', x.friend);
}
export async function call(id) {
  const P = G.people[id],
    x = X('life'),
    c = x.calls;
  const ok = canCall(id);
  if (!ok.ok) return ok;
  const warmth = LR.callWarmth(c.last[id] == null ? null : c.last[id], G.t, T.calls);
  const cool = warmth === 'cool';
  let honest = true;
  await scene(async () => {
    if (cool) {
      await say(id, id === 'alison' ? 'You again, Mr Nowak. I have a deadline, and you had my ten minutes this morning.' : 'You again. I am glad of it, in principle. But I have said my day\'s worth.');
      return;
    }
    // what they know of him, the hottest thing first: a visit after a bad night carries it
    const m = P.mind.mem.filter((r) => attached(r) && r.src !== 'self' && !r.said && G.ev[r.e] && G.ev[r.e].kind !== 'inherit').sort((p, q) => q.heat - p.heat)[0];
    const n = c[id].length % SMALL[id].length;
    await say(id, SMALL[id][n][0]);
    if (m) {
      await say(id, comebackLine(P, m));
      m.said = true;
      ledgerSeen(G.ev[m.e], P, 'said', m.src === 'told' ? m.from : null);
      const i = await choose(id, id === 'alison' ? 'Not for the paper. For me. Is it true?' : 'I am not asking as anybody. Is it true?', ['Tell it straight', 'Make light of it', 'Say nothing']);
      honest = i === 0;
      await say(id, honest ? (id === 'alison' ? 'Thank you. That cost you something. I will not spend it.' : 'Thank you. I would rather know and mind than not know.') : i === 1 ? (id === 'alison' ? 'I interview liars for a living, Mr Nowak. You are not good at it yet.' : 'Hm. I marked essays for fifteen years. I know padding.') : 'No. Well. A silence is an answer of a kind.');
      if (i === 2) honest = false;
    } else await say(id, SMALL[id][n][1]);
  });
  c.last[id] = Math.round(G.t);
  c[id].push({ honest, cool, t: Math.round(G.t) });
  if (!cool) {
    if (honest) {
      act('visit', { target: id });
      P.mind.regard = clamp(P.mind.regard + 0.12, -1, 1);
    } else {
      act('visit_lie', { silent: true, told: [id], name: P.def.name });
      P.mind.regard = clamp(P.mind.regard - 0.15, -1, 1);
    }
    advanceTo(G.t + T.calls.visitTakesGameMinutes, false);
  }
  recount();
  if (G.hooks.save) G.hooks.save();
  return { ok: true, cool, honest };
}
const danbyIntro = () =>
  scene(async () => {
    const P = G.people.danby;
    meet(P);
    P.mind.fam = Math.max(P.mind.fam, 0.3);
    G.story.flags.met_danby = 1;
    await say('danby', 'You will be the nephew. Philip Danby. I taught at the Board School until there was no school to teach at.');
    await say('danby', 'I was told about you before you were off the bus. I try not to be told things. Come and sit, some afternoon, and tell me yourself.');
  });
export function peopleBeat(P) {
  if (P.id === 'danby' && !G.story.flags.met_danby) return danbyIntro;
  return null;
}
// ---------- the boxing club (A28) ----------
const MOVES = ['Jab and move', 'Cover and wait', 'Go to the body'];
const THEIRS = ['rushes', 'boxes at range', 'covers up'];
// jab beats a rush, covering beats a boxer, the body beats a cover; the same against the same is even
const BEATS = { 0: 0, 1: 1, 2: 2 };
export function boxingOpen(h = hour(), d = day()) {
  return d % 7 !== 6 && d % 7 !== 0 && h >= T.boxing.trainsFromHour && h < T.boxing.trainsUntilHour;
}
export async function club() {
  const x = X('life').boxing;
  await scene(async () => {
    const first = !x.seen;
    x.seen = 1;
    if (first) {
      await say('', 'The old hall behind the chandler\'s. A ring on trestles under a skylight, two heavy bags, a smell of liniment and wet wool. A dozen men, none of them talking.');
      note('The boxing club, in the old hall behind the chandler\'s: Tuesday to Saturday evenings, gloves and no money. Dockers train there.', 'place', 'boxingclub', { how: 'Went in' });
    }
    const i = await choose('', 'The trainer, a small man with a towel round his neck, holds up a pair of sixteen-ounce gloves. "In or out?"', ['Put the gloves on: three rounds', 'Watch from the ropes', 'Out']);
    if (i === 1) {
      const who = ['lee', 'shaun', 'kevin'][day() % 3],
        Q = G.people[who];
      await say('', `${Q ? Q.def.name : 'A docker'} is on the heavy bag, working it like it owes him. He nods at Tom between rounds, which is more than he does on the street.`);
      if (Q && !x.met.includes(who)) x.met.push(who);
      if (Q) Q.mind.fam = clamp(Q.mind.fam + 0.08, 0, 1);
      return;
    }
    if (i !== 0) return;
    if (G.hooks.spar) {
      await G.hooks.spar({ rounds: T.boxing.boutRounds, gloves: true, noFall: true, noBlood: true });
    } else {
      let won = 0;
      for (let r = 0; r < T.boxing.boutRounds; r++) {
        const his = (day() + r * 2 + x.bouts) % 3;
        const j = await choose('', `Round ${r + 1}. The other man ${THEIRS[his]}.`, MOVES);
        const mine = j < 0 ? 1 : j;
        const res = BEATS[mine] === his ? 1 : mine === (his + 2) % 3 ? 0 : -1;
        won += res;
        await say('', res > 0 ? 'Tom reads it and lands clean. The bell.' : res === 0 ? 'Nothing in it. The bell.' : 'He walks onto one and sees the skylight. The bell.');
      }
      await say('', won > 0 ? '"You have done this before," the trainer says, unlacing him. It is not a question and he does not wait for an answer.' : won === 0 ? '"Even. Come back Thursday." The other man touches gloves.' : '"You drop your left. Everybody will tell you." The other man touches gloves anyway.');
      x.last = won;
    }
    x.bouts++;
    act('spar', {});
    const who = ['lee', 'shaun'][x.bouts % 2],
      Q = G.people[who];
    if (Q) {
      Q.mind.fam = clamp(Q.mind.fam + 0.1, 0, 1);
      if (!x.met.includes(who)) x.met.push(who);
    }
    emit('pastime', { what: 'boxing', bouts: x.bouts });
  });
  if (G.hooks.save) G.hooks.save();
}
export function peopleHotspots(out) {
  const t = G.tom;
  for (const id in CALLS) {
    const P = G.people[id],
      c = CALLS[id];
    if (!P || !canCall(id).ok) continue;
    const where = placeOfRoutine(P);
    if (where === 'home' && c.home) {
      if (t.space === 'street' && Math.hypot(t.x - c.home.x, t.z - c.home.z) < 2.6) out.push({ k: 'T', t: c.home.prompt, run: () => call(id) });
    } else if (P.space === t.space && !P.moving && Math.hypot(t.x - P.x, t.z - P.z) < 2.8) out.push({ k: 'T', t: c.prompt, run: () => call(id) });
  }
  const b = PLACES.boxing;
  if (b && t.space === 'street' && Math.hypot(t.x - b.x, t.z - b.z) < 3.2) {
    if (boxingOpen()) out.push({ k: 'E', t: 'Go into the boxing club', run: club });
    else out.push({ k: 'E', t: 'The boxing club: dark. Tuesday to Saturday evenings' });
  }
}
export const peopleHook = {
  canCall,
  call,
  friend: () => Object.assign({}, X('life').friend),
  boxingOpen,
  club,
  calls: () => JSON.parse(JSON.stringify(X('life').calls)),
};
