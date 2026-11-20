// LEDGER, the whole game: the system "carry". The first carry (ONE-SHOT-PROMPT 4 at 9:00 and 11:30, 14, 21; story
// S05): the envelope under the coat goes to the ferry landing while it is open. Three ways down that he reads himself:
// the lit quay (quick and seen), the yard and the dark side of the quay by the water (slower), or the cab (quickest and
// known). The beat constable is the law's (game/law.js); this file is the landing man, the hand-over and the cut, what
// becomes of the ask when the envelope is lost or the landing missed, and the bed in the flat. Every step is a line.
import { register, X, write, P_, dayNow, hourNow } from './core.js';
import { G } from '../state.js';
import { sub, ui, noted, scene, choose } from '../ui.js';
import { RULES } from '../rules.js';
import { SPOTS, roomPos } from '../map.js';
import { earn } from '../money.js';
import { hyp, quid } from '../util.js';
import { passTime } from '../work.js';
import { has, drop } from './crime.js';
import { LANDING_WORDS } from './outfit.js';

const T = RULES.game.outfit;
const AT = () => [SPOTS.shelter[0] + T.manStandsFromShelter[0], SPOTS.shelter[1] + T.manStandsFromShelter[1]];
const man = () => G.people[T.landingManIs];
const money = (p) => quid(p).replace(/\.00$/, '');

// Is the landing open now? From ten; till one, or two and a half game hours after he took the envelope if that is later
// (the law of jobs: no lateness fail inside a window of at least two game hours).
export function landingOpen() {
  const o = X('outfit');
  if (o.ask1 !== 'yes' || !o.takenT) return false;
  const day0 = Math.floor(o.takenT / 1440) * 1440,
    taken = (o.takenT % 1440) / 60,
    night0 = taken < 12 ? day0 - 1440 : day0, // the night the envelope belongs to
    opens = night0 + T.landingOpensHour * 60,
    shuts = Math.max(night0 + 1440 + T.landingShutsHour * 60, o.takenT + T.windowAtLeastGameMinutes);
  return G.t >= opens && G.t < shuts;
}
const holdsEnvelope = () => has('envelope') || G.tom.carry === 'envelope';

function place(x) {
  // the man waits in the dark by the shelter while the landing is open and the envelope is still to come
  const M = man();
  if (!M) return;
  const want = landingOpen() && !x.envelope;
  if (want && !x.manOut) {
    x.manOut = true;
    const [mx, mz] = AT();
    Object.assign(M, { override: null, hold: true, route: null, moving: false, gone: false, space: 'street', x: mx, z: mz, awake: true, state: 'idle', inCar: false, ang: Math.PI });
  } else if (!want && x.manOut) {
    x.manOut = false;
    M.hold = false;
    M.override = { where: 'off', act: 'idle', until: G.t + 600 };
    M.goalKey = '';
  }
}
function handOver() {
  const x = X('carry'),
    t = G.tom;
  if (!holdsEnvelope() || x.envelope) return;
  if (has('envelope')) drop('envelope');
  else t.carry = null;
  x.envelope = 'done';
  X('outfit').envelope = 'done';
  x.doneT = Math.round(G.t);
  earn(T.firstCutPence, true, "his cut of the landing's envelope");
  sub(`Right. ${money(T.firstCutPence).replace('£', '')} pounds, that's yours. Tell Ron it's the same again Wednesday.`, 'The man by the shelter', 'face', 6);
  if (G.hooks.sfx) G.hooks.sfx('paper');
  write(`Handed the envelope to the man at the ferry landing. He said "Mickey's?" and nothing else worth keeping.`, { key: 'carry1-handed', how: 'He did it' });
  write(`His cut of the first envelope: ${money(T.firstCutPence)}, in notes. Night money: it goes in the tin, not the fare book.`, { key: 'carry1-cut', how: 'Counted it' });
  // the cab at the landing is the firm's name at the landing: whoever can see it there has seen Mickey's cab
  const c = G.car,
    [mx, mz] = AT();
  if (hyp(c.x, c.z, mx, mz) < T.cabAtTheLandingWithinMetres) {
    const saw = G.named.concat(G.crowd).filter((P) => !P.gone && P.space === 'street' && hyp(P.x, P.z, c.x, c.z) < RULES.game.outfit.cabNamedWithinMetres && (!G.env.los || G.env.los(P.x, P.z, c.x, c.z)));
    x.cabSeenBy = saw.map((P) => P.id);
    for (const P of saw) P.mind.look = Math.max(P.mind.look || 0, 2.5);
    noted(saw.length > 1 ? "Mickey's cab was seen at the landing, he thinks: the sign on its roof says whose it is." : "The man at the landing has seen Mickey's cab there: the sign on its roof says whose it is.");
    write("Took the cab to the landing. Quick, and nobody looks twice at a cab; but whoever saw it there saw Mickey's name on its roof.", { key: 'carry1-cab', how: 'His own reading' });
  }
}
// The envelope is gone and not to the landing: the ask has failed, and goes on as a state the outfit's man hears of.
function lost(x, how) {
  x.envelope = how;
  X('outfit').envelope = how;
  x.lostT = Math.round(G.t);
  if (how === 'police') write('The constable has the envelope. The landing is missed tonight, and the men behind it will hear so from their own man.', { key: 'carry1-lost', how: 'It happened to him' });
  else write('The landing shut with the envelope still on him. The ask is failed; Ron will hear of it before he does.', { key: 'carry1-late', how: 'His own watch' });
}
async function sleep() {
  const i = await scene(() => choose('', "The bed in the flat over the office. Mickey's blankets, his own suitcase.", ['Sleep till morning.', 'Not now.']));
  if (i !== 0) return;
  const d = hourNow() < 7 ? dayNow() : dayNow() + 1;
  write('Slept in the flat over the office.', { key: 'slept-' + d, how: 'He did it' });
  await passTime(d * 1440 + T.wakesAtHour * 60, 'Morning comes up grey over the water.');
  sub('Saved.', '', 'over', 3); // the save note: sleeping saves the game
  X('carry').slept = (X('carry').slept || 0) + 1;
}

register({
  id: 'carry',
  fresh: () => ({ envelope: null, manOut: false, asked: false, doneT: 0, lostT: 0, cabSeenBy: null, slept: 0 }),
  loaded(x) {
    x.manOut = false; // a load puts nobody at the shelter: he is put there again if the landing is open
  },
  step() {
    if (G.paused || G.story.phase !== 'play') return;
    const x = X('carry'),
      o = X('outfit'),
      t = G.tom;
    if (o.ask1 !== 'yes') return;
    place(x);
    if (x.envelope) return;
    // lost to a search: the constable keeps what he finds
    if (!holdsEnvelope() && !(G.x.crime.stored || []).some((s) => s.id === 'envelope')) return lost(x, 'police');
    if (!landingOpen() && G.t > o.takenT + 30 && G.t >= Math.floor(o.takenT / 1440) * 1440 + T.landingOpensHour * 60) return lost(x, 'late');
    // "Mickey's?": the man speaks when he comes up to him on foot with the envelope on him
    const M = man(),
      [mx, mz] = AT();
    if (M && x.manOut && !t.inCar && t.space === 'street' && hyp(t.x, t.z, mx, mz) < T.manSpeaksWithinMetres && !x.asked && holdsEnvelope()) {
      x.asked = true;
      M.ang = Math.atan2(t.x - M.x, t.z - M.z);
      sub("Mickey's?", 'A man in the dark by the shelter', 'face', 4);
    }
  },
  hotspots(out) {
    const x = X('carry'),
      t = G.tom;
    if (X('outfit').ask1 === 'yes' && !x.envelope && x.manOut && t.space === 'street' && holdsEnvelope()) {
      const [mx, mz] = AT();
      if (hyp(t.x, t.z, mx, mz) < T.manSpeaksWithinMetres) out.push({ k: 'E', t: 'Hand the envelope to the man by the shelter', run: handOver, person: true });
    }
    if (t.space === 'flat') {
      const [bx, bz] = roomPos('flat', 3.6, -2.0);
      if (hyp(t.x, t.z, bx, bz) < 1.8) out.push({ k: 'E', t: 'The bed: sleep till morning', run: sleep });
    }
  },
  hook: { x: () => X('carry'), landingOpen, at: AT, landingWords: LANDING_WORDS },
});
