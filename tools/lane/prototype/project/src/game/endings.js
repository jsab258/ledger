// LEDGER, the whole game: the system "endings". The endings are states, never picked from a list (DESIGN 16, A7,
// A39; parts 3.1.4, 3.1.5, 3.2.5, 3.2.7, 7.15): three shown (the Kingdom, the Straight Life, Burn Both), the five
// built states kept underneath. Every cost that decides the ending shows its sign before it decides, and no ending
// lands while Tom's own reading says things are quiet. Then the close, the credits, and the town as it stands.
import { register, X, write, tell, hourNow, dayNow, here, P_, emit, on, PLACES } from './core.js';
import { G, setPaused } from '../state.js';
import { attached } from '../seeing.js';
import { KINDS } from '../kinds.js';
import { choose, scene, say, fade, panel } from '../ui.js';
import { advanceTo } from '../work.js';
import { RULES } from '../rules.js';
import { PIECE as STORY } from './pieces/story.js';
import { PIECE as TALK } from './pieces/talk.js';
import { sign, signsShown, reading } from './ledgerx.js';

const T = RULES.game.endings;
const S_ = STORY.fns;
const FRIENDS = { ada: { place: 'ada', fromHour: 10, untilHour: 20 }, alison: { place: 'caff', fromHour: 12, untilHour: 14 } };

// How many people hold his rackets as fact: told or seen, attached to him, a crime (never a number on screen).
function streetHoldsRackets() {
  let n = 0;
  for (const P of G.named) if (P.mind.mem.some((m) => attached(m) && KINDS[G.ev[m.e].kind] && KINDS[G.ev[m.e].kind].crime >= 1 && m.sure > 0.4)) n++;
  return n >= T.streetHoldsRacketsAsFactAtTellers;
}
// The state the ending is read from.
export function endState() {
  const a = G.x.acts,
    x = X('endings');
  const hunted = G.x.law.ellis.stage >= 3 && G.x.law.charges.some((c) => c.offence === 'killing');
  const business = a.answer !== 'wind' && G.x.firm.f.cars.some((c) => c.driver) && !a.handedOver;
  return { business, booksHold: a.insp ? a.insp.result === 'the books hold' : G.money.booksOff < RULES.game.acts.bookStrainedIfOffUnderPence, friendHolds: TALK.fns.friendship(x.friend) === 'holds', streetHoldsRackets: streetHoldsRackets(), hunted, handedOver: !!a.handedOver, charged: G.x.law.charges.length > 0 };
}
export const endingNow = () => S_.ending(endState());
// ---- calling on people (A39): only where and when the routine allows; no score; too soon is cooler ----
async function visit(id) {
  const x = X('endings'),
    P = P_(id);
  const lastNight = P.mind.mem.find((m) => attached(m) && KINDS[G.ev[m.e].kind].crime >= 1 && G.t - m.t < 2 * 1440);
  const v = TALK.fns.visit({ routineAllows: true, lastVisitT: x.lastVisit[id] ?? null, knowsOfLastNight: !!lastNight }, G.t);
  x.lastVisit[id] = G.t;
  const cooler = /cooler/.test(v.door);
  let honest = null;
  const t0 = G.played;
  await scene(async () => {
    await say(id, cooler ? 'You again. I have only just washed the cups.' : id === 'ada' ? 'Come in, then. Wipe your feet. You look like him round the eyes when you are tired.' : 'Sit down. I am off the clock, so this is not for the paper.');
    if (v.carries) {
      const i = await choose(id, id === 'ada' ? 'They are saying things about last night. I would sooner hear it from you.' : 'I heard about last night. Is it true?', ['Tell the truth of it.', 'Say it was nothing.']);
      honest = i === 0;
      await say(id, honest ? 'Well. You said it to my face. That is more than he ever did.' : 'I see. I was told otherwise, by somebody with no reason to lie.');
    } else if (!cooler) {
      honest = true;
      await say(id, id === 'ada' ? 'He sat in that chair every Wednesday for nine years and told me nothing. You can do better than that.' : 'Tell me one true thing about that office and I will tell you one about the fire.');
    }
  });
  if (honest === true) x.friend.honestVisits++;
  else if (honest === false) x.friend.lieCaught = true; // she knew: a lie caught ends it
  x.friend.who = x.friend.who || id;
  x.visits.push({ id, door: v.door, honest, seconds: Math.round(G.played - t0), score: v.score, t: Math.round(G.t) });
  if (TALK.fns.friendship(x.friend) === 'holds' && !x.friendSaid) {
    x.friendSaid = true;
    sign('friend', `${P.def.name} sent word round with a plate of something, unasked.`);
  }
  if (x.friend.lieCaught && !x.lostSaid) {
    x.lostSaid = true;
    write(`${P.def.name} knows he lied to her face. The door is civil now, and no more.`, { who: id, how: 'Saw it himself' });
  }
}
// ---- the ending lands: its owed signs first, then the close, the credits, and control again ----
async function land() {
  const x = X('endings');
  if (x.done) return;
  let end = endingNow();
  let may = S_.mayLand(end, signsShown());
  if (!may.may) {
    // every cost that decides the ending shows its sign before it decides: the sign now, the ending a day later
    for (const s of may.owed) {
      const kind = Object.keys(T.signs).find((k) => T.signs[k] === s);
      sign(kind, kind === 'police' ? 'A police car at the kerb on Quay Street, and his description said aloud.' : kind === 'inspector' ? 'The inspector has stopped being courteous.' : "Sheila: \"I can't make this add up any more, and I'm done trying.\"");
      tell(kind === 'police' ? 'A police car at the kerb on Quay Street, and his description said aloud.' : 'Sheila shuts the fare book. "I can\'t make this add up any more."', '', 8);
    }
    x.owedShownT = G.t;
    x.landAfterT = G.t + 1440;
    return;
  }
  x.done = { built: end.built, shown: end.shown, turn: end.turn, close: end.close, t: Math.round(G.t), reading: reading().expects, signs: signsShown() };
  setPaused(true, 'the ending');
  const a = S_.after(end);
  await fade(true, `${end.shown}.\n\n${end.close}`);
  await new Promise((r) => setTimeout(r, 1500));
  await fade(true, 'LEDGER\n\nA town that remembers.\n\nThe Hook, autumn 1990.');
  await new Promise((r) => setTimeout(r, 1500));
  write(`${end.shown}. ${end.close}`, { key: 'ending', how: 'How it ended' });
  write(a.ledgerLastPage, { key: 'lastpage', how: 'The last page' });
  // after the credits: control returns in the town at the ending's state (ER-AFTER-01)
  const p = PLACES[end.shown === 'The Straight Life' ? 'landing' : 'mickeys'];
  const t = G.tom;
  if (t.space !== 'street' && G.hooks.leaveRoom) G.hooks.leaveRoom();
  Object.assign(t, { space: 'street', inCar: false, x: p.x - 2.5, z: p.z + (p.id === 'landing' ? 0 : 2.5) });
  x.done.placed = p.id;
  if (G.hooks.save) G.hooks.save();
  await fade(false);
  setPaused(false, 'after the ending: the town goes on');
  G.story.objective = 'The story is told. The town goes on.';
  emit('endings.done', x.done);
}

register({
  id: 'endings',
  fresh: () => ({ friend: { honestVisits: 0, lieCaught: false, who: null }, lastVisit: {}, visits: [], done: null, landAfterT: null, owedShownT: null, friendSaid: false, lostSaid: false }),
  hourly() {
    const x = X('endings');
    if (!x.done && x.landAfterT != null && G.t >= x.landAfterT && !G.paused) land();
  },
  hotspots(out) {
    const t = G.tom;
    for (const id in FRIENDS) {
      const f = FRIENDS[id],
        P = P_(id),
        p = PLACES[f.place];
      if (!P || P.dead || hourNow() < f.fromHour || hourNow() >= f.untilHour) continue; // only where and when her routine allows
      const at = p.room && t.space === p.room && P.space === p.room;
      if (at && G.ledger.met[id]) out.push({ k: 'G', t: 'Sit down with ' + P.def.name.split(' ')[0], run: () => visit(id) });
    }
  },
  hook: {
    x: () => X('endings'),
    state: endState,
    now: endingNow,
    visit,
    land,
    mayLand: () => S_.mayLand(endingNow(), signsShown()),
    after: () => S_.after(endingNow()),
  },
});
on('acts.inspected', () => {
  X('endings').landAfterT = G.t + 60; // the books open; then it ends as the state says
});
