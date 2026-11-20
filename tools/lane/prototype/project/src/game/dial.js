// LEDGER, the whole game: the system "dial". The escalation dial and firearms (DESIGN section 7; parts 2.13, 1.3.10).
// The dial is a fact in the town's memory, not a meter: it moves only on what somebody saw or heard, and nothing on
// screen ever shows it as a number. Rules: pieces/dial_rules.js. Hold-ups (A41) are in holdup.js.
import { register, emit } from './core.js';
import { G, hour } from '../state.js';
import { act } from '../events.js';
import { sub, news, say, scene } from '../ui.js';
import { decision } from '../talk.js';
import { note } from '../ledger.js';
import { target } from '../fight.js';
import { pay } from '../money.js';
import { roomPos, INSIDE } from '../map.js';
import { PIECE } from './pieces/dial_rules.js';
import { TUNE as D } from './tune/dial.js';
import { P_, X, knowers, rungNow, moneyAll } from './rise_util.js';
import './holdup.js';

const R = PIECE.fns;
const GUN = 'revolver';
const st = () => X('dial');
const SAID = [
  '',
  'By dinner time the Hook has heard it: somebody down here has a gun.',
  'A shot on the Hook. Everybody who heard it knows where they were standing.',
  'It is a war now. Armed police in cars, doors shut early, and nobody looks at a cab that slows.',
];
const HEAD = ['', 'GUN SEEN ON THE HOOK', 'SHOT FIRED ON THE HOOK', 'ARMED POLICE ON QUAY STREET'];

function setState(to, why) {
  const x = st();
  if (to === x.state) return false;
  const up = to > x.state;
  x.state = to;
  x.lastLoudT = G.t;
  x.why.push({ t: Math.round(G.t), state: to, why });
  if (x.why.length > 40) x.why.shift();
  x.carriers = carriers(to);
  if (up) {
    sub(SAID[to], '', 'over', 7);
    news(HEAD[to], 'Police appeal for witnesses');
    note(SAID[to], 'note', 'dial' + to, { how: 'The street says' });
  } else {
    sub('A quiet fortnight. People have stopped looking for guns, though nobody has forgotten them.', '', 'over', 6);
    note('Two quiet weeks. The talk of guns has cooled a step. Nobody has forgotten.', 'note', 'dialfell' + Math.round(G.t));
  }
  emit('dial', { state: to, why });
  return true;
}
// Guns stay rare: only a few named men carry, the rivals' own, and everyone knows who.
function carriers(state) {
  const n = R.carriersPerSide(state),
    side = { jensen: ['gary'], cammack: ['dean', 'cammack'], agar: [] },
    out = [];
  for (const k in side) out.push(...side[k].slice(0, n));
  if (state >= 3) out.push('jensen');
  return out;
}
// The town learns of something. type as the piece's; E the event; the witnesses are whoever holds it.
export function dialTell(type, E, witnesses) {
  const n = witnesses != null ? witnesses : E ? knowers(E).length : 0;
  const r = R.step(st().state, { type, witnesses: n });
  if (n > 0 && type !== 'blade_seen') st().lastLoudT = G.t;
  if (r.moved) setState(r.state, r.why);
  return r;
}
const hasGun = () => G.tom.weapon === GUN;
function giveGun(from) {
  const x = st();
  G.tom.weapon = GUN;
  G.tom.armed = false;
  x.gun = { has: true, from };
}
function draw() {
  const t = G.tom;
  if (!hasGun() || t.armed || t.inCar) return null;
  t.armed = true;
  const T = target();
  const E = act('gun_shown', { target: T && !T.anon ? T.id : undefined, weapon: GUN });
  if (G.hooks.sfx) G.hooks.sfx('paper');
  sub('The gun is out. It cannot be put away unseen.', '', 'over', 4);
  return dialTell('gun_seen', E);
}
function fire() {
  const t = G.tom,
    x = st();
  if (!hasGun() || !t.armed || t.inCar) return null;
  const T = target(),
    reach = R.shotReach(hour(), G.weather.rain),
    aimed = T && Math.hypot(T.x - t.x, T.z - t.z) < D.gunAimsWithinMetres;
  const E = act('gun_fired', { target: aimed && !T.anon ? T.id : undefined, weapon: GUN, noiseR: reach });
  x.shots++;
  if (G.hooks.sfx) G.hooks.sfx('thud');
  if (G.hooks.shake) G.hooks.shake(0.5);
  const told = dialTell('gun_fired', E);
  let hit = null;
  if (aimed) {
    hit = R.shotOutcome(x.state, x.deathsThisAct, Math.random());
    T.down = true;
    if (hit.kills) {
      x.deathsThisAct++;
      T.dead = true;
      G.story.flags.dead = G.story.flags.dead || {};
      G.story.flags.dead[T.id] = 1;
      act('kill', { target: T.id, weapon: GUN });
      if (G.hooks.killed) G.hooks.killed(T);
    }
    if (G.hooks.blood) G.hooks.blood(T.x, T.z);
    sub(hit.kills ? 'He goes down and does not move.' : 'He goes down, hurt badly, and alive.', '', 'over', 5);
  } else sub('The shot goes out over the water. The whole street heard it.', '', 'over', 5);
  emit('shot', { E, hit, reach });
  return { told, hit, reach, E };
}
// Found once at Mickey's: the bottom drawer of his desk, once the back room is Tom's (rung 2).
const drawer = () =>
  scene(async () => {
    const x = st();
    x.gun.foundOffered = true;
    await say('', "The bottom drawer of Mickey's desk. Under the receipt books, wrapped in a yellow duster: a revolver, old, oiled, loaded.");
    const i = await decision('sheila', 'I knew it was there. I never touched it. Nobody on this street has seen a gun in ten years, and you would be the one who brought it back.', {
      leaveIdx: 1,
      ask: "whether he takes Mickey's revolver out of the drawer",
      opts: [
        {
          agree: 1,
          say: ["I'll take it.", "It's coming with me."],
          q: 'You are taking it out of this office? Once it is seen, it is seen for good.',
          yes: ["Yes. I'm taking it.", 'Yes.'],
          no: ['No. Leave it where it is.', 'No. Shut the drawer.'],
          keep: ['Did Mickey ever use it?', 'Who else knows it is here?'],
          keepSay: 'He never fired it that I heard. I know, and now you know. Are you taking it?',
        },
        { refuse: 1, say: ['Leave it where it is.', 'Shut the drawer.'] },
      ],
    });
    if (i === 0) {
      giveGun('found');
      note("Took Mickey's revolver out of the bottom drawer. Sheila saw him take it.", 'note', 'gunfound', { who: 'sheila', how: 'Was there' });
      const E = act('gun_got', { silent: true, told: ['sheila'] });
      void E; // Sheila never goes to anybody with it: the dial does not move until the gun is seen
    } else note("Mickey's revolver is in the bottom drawer of his desk. Left it there.", 'note', 'gunleft', { who: 'sheila', how: 'Was there' });
  });

register({
  id: 'dial',
  fresh: () => ({ state: 0, why: [], lastLoudT: 0, gun: { has: false, from: null, foundOffered: false }, shots: 0, deathsThisAct: 0, carriers: [], drawT: -99 }),
  loaded(x) {
    if (!x.gun) x.gun = { has: false, from: null, foundOffered: false };
    G.hooks.dial = () => Object.assign({ state: st().state, carriers: st().carriers }, R.police(st().state), R.town(st().state));
    G.hooks.dialTell = dialTell;
  },
  daily() {
    const x = st(),
      q = R.quiet(x.state, (G.t - x.lastLoudT) / 1440);
    if (q.fell) setState(q.state, 'two quiet weeks');
  },
  hotspots(out) {
    const t = G.tom,
      x = st();
    if (t.space === 'mickeys' && rungNow() >= D.gunFoundAtMickeysFromRung && !x.gun.foundOffered) {
      const h = INSIDE.backDoor,
        [bx, bz] = roomPos(h.room, h.x, h.z);
      if (Math.hypot(t.x - bx, t.z - bz) < h.within + 0.6) out.push({ k: 'G', t: "Go through Mickey's desk", run: drawer });
    }
    if (hasGun() && !t.inCar) out.push({ k: '0', t: t.armed ? 'Fire' : 'Draw the gun (press twice)', run: () => (t.armed ? fire() : draw()) });
  },
  key(code) {
    if (code !== 'Digit0' || !hasGun() || G.tom.inCar) return false;
    const x = st();
    if (G.tom.armed) fire();
    else if (G.played - x.drawT <= D.drawAsksTwiceWithinRealSeconds) draw();
    else {
      x.drawT = G.played; // a weapon comes out only on a deliberate input (ER-FIGHT-08): the first press only asks
      sub('Draw it? Press again.', '', 'over', 1.5);
    }
    return true;
  },
  // Guns come only through people: Lee Drewery knows a man off the boats (bought from the docks, and the town remembers who).
  matters(P, a) {
    if (P.id !== 'lee' || hasGun() || rungNow() < D.gunBoughtFromRung || P['off_gun'] === Math.floor(G.t / 1440)) return;
    a.push({
      key: 'gun',
      ask: 'whether he buys a gun through Lee Drewery',
      raise: 'There is a man off the boats sells a thing nobody down here has. A hundred and twenty. I would not ask if I were you.',
      keep: ['Who is he?', 'Has anybody else bought one?'],
      keepSay: "I don't say who. Nobody has, that I know. That's rather the point of telling you.",
      opts: [
        {
          say: ['Get me one.', "I'll have it. A hundred and twenty."],
          q: 'A gun. On the Hook. You are sure? It will be known who brought it in.',
          yes: ['Yes. Get it.', "Yes. I'm sure."],
          no: ['No. Forget I asked.', 'No. Leave it.'],
          keep: ['Who is he?', 'Has anybody else bought one?'],
          keepSay: "I don't say who. You are sure?",
          take: () => {
            P['off_gun'] = Math.floor(G.t / 1440);
            if (moneyAll() < D.gunPricePence || !pay(D.gunPricePence, false, 'a gun, through Lee Drewery')) return 'Come back with the money. All of it.';
            giveGun('bought');
            const E = act('gun_got', { target: 'lee' });
            dialTell('guns_bought', E, knowers(E).length);
            note('Bought a revolver through Lee Drewery, from a man off the boats. Lee knows who brought it in.', 'note', 'gunbought', { who: 'lee', how: 'Was there' });
            return "It's in the paper bag. You never got it through me.";
          },
        },
      ],
    });
  },
  hook: {
    state: () => st().state,
    set: (state, why = 'set by a test') => setState(Math.max(0, Math.min(3, state)), why),
    tell: (type, witnesses) => dialTell(type, null, witnesses),
    giveGun: (from = 'test') => giveGun(from),
    draw,
    fire,
    quietDays: (n) => {
      st().lastLoudT = G.t - n * 1440;
      const q = R.quiet(st().state, n);
      if (q.fell) setState(q.state, 'two quiet weeks');
      return st().state;
    },
    info: () => (G.hooks.dial ? G.hooks.dial() : null),
    why: () => st().why,
  },
});
void P_;
