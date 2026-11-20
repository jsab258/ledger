// LEDGER, the whole game: the system "acts" (parts 3.1.1 to 3.1.3, 7.4, 7.11; DESIGN 16).
// Act I is week one and closes on Sheila's Sunday question. Act II's beats fire on states, never on days, and end at
// a sit-down with one head. Act III is the inspection week: one deciding step each morning, then the books open.
import { register, emit, on, X } from './core.js';
import { G, day, hour } from '../state.js';
import { RULES } from '../rules.js';
import { KINDS } from '../kinds.js';
import { ui, sub, say, choose, scene } from '../ui.js';
import { note } from '../ledger.js';
import { act } from '../events.js';
import { F } from '../fight.js';
import { roomPos, ROOMS } from '../map.js';
import { hyp, clamp } from '../util.js';
import { actOf, nextBeat, sitDownHead, BEATS } from './pieces/act_beats.js';
import { ITEMS, morning, result, whereItHolds } from './pieces/act_inspection.js';
import { showSign, runEnding, readingNow, inputsNow } from './endings.js';

const T = () => RULES.game.acts;
const st = () => X('acts');
const xs = (id) => (G.x && G.x[id]) || {};
const P_ = (id) => G.people[id];
const HEADS = { widow: 'Maureen Jensen', agar: 'Geoffrey Agar', cammack: 'Danny Cammack' };
const free = () => G.story.phase === 'play' && !G.paused && !ui.modal && !ui.inScene && !F.on && !G.tom.inCar && !G.story.fare;

// ---------- the state the beats read (every other system's part with a default) ----------
export function stateNow() {
  const s = st(),
    rv = xs('rivals'),
    crew = xs('crew').men || {},
    life = xs('life');
  const rung = (k) => {
    const r = rv[k];
    return typeof r === 'number' ? r : (r && r.rung) || 0;
  };
  const fp = P_((life.friend && life.friend.who) || 'alison');
  return {
    act: s.act,
    answered: !!s.answered,
    choice: G.story.flags.choice || null,
    rung: xs('rise').rung || 1,
    rivalRungs: { widow: rung('widow'), agar: rung('agar'), cammack: rung('cammack') },
    lawStage: xs('law').stage || 0,
    seenCrimes: G.events.filter((E) => KINDS[E.kind] && KINDS[E.kind].crime >= 1 && E.wit && E.wit.length).length,
    friendHolds: life.friend && life.friend.holds !== undefined ? !!life.friend.holds : !!(fp && fp.mind && fp.mind.regard > T().friendHoldsAboveRegard),
    arrangement: xs('jobsx').arrangement || (G.story.flags.choice === 'wind' ? 'ended' : G.story.flags.job1 === 'done' ? 'kept' : null),
    faresDriven: G.money.fareCount,
    nightMoneyEarnedPence: G.money.earnedDirty,
    crewRecruits: Object.values(crew).filter((m) => m && m.recruited).length,
    fired: s.fired.slice(),
    quietDays: Math.floor((G.t - s.lastBeatT) / 1440),
    sitDown: s.sitDown,
  };
}
const giverOf = (ids) => ids.find((id) => P_(id) && !P_(id).dead && !P_(id).gone) || null;
function setAct(n) {
  const s = st();
  if (s.act === n) return;
  s.act = n;
  s.lastBeatT = G.t;
  emit('act', { act: n });
  note(n === 2 ? 'Act II. The firm has grown, and it has been noticed.' : 'Act III. A letter from Customs and Excise: the books are to be inspected.', 'note', 'act' + n, { how: 'Tom knows' });
  if (G.hooks.save) G.hooks.save();
}
// Sheila has her answer (called by the story when Act I closes).
export function actOneClosed(choice) {
  const s = st();
  s.answered = true;
  s.choice = choice;
  s.lastBeatT = G.t;
  emit('act', { act: 1, closed: true, choice });
}

// ---------- Act II: the beats ----------
const BEAT_SCENES = {
  opens: async (who) => {
    const arr = stateNow().arrangement;
    await say(who, who === 'sheila' ? 'Sit down a minute. When you came this was two cars and a tin.' : "Sheila says to tell you. When you came this was two cars and a tin.");
    await say(who, "It isn't now. People ring for us by name. That gets noticed: on the docks, in the offices on the Exchange, and by young Cammack's lot.");
    await say(who, arr === 'ended' ? "You ended Mickey's arrangement at the landing. So the ground is open, and all three know it. They'll come sooner." : "The men behind the landing are the last of an old firm. Keep carrying and they'll hand you their end of the Hook, and fade. Then you are what Mickey was.");
    note('The firm has been noticed by three outfits: Jensen on the docks, Agar on the Exchange, Cammack and his lads. Each will come and look.', 'note', 'a2opens', { who, how: who === 'sheila' ? 'Sheila says' : 'Pauline says' });
    G.story.objective = "Run the firm: fares, the debt book, the night's work. Three outfits have noticed it. Watch who comes to look.";
  },
  rival_first: async (who) => {
    await say(who, who === 'ron' ? "Boss. Somebody's been asking who drives car two of a night. Not police. Dock boots." : "So listen. Somebody's asking who drives car two of a night. Not coppers. Dock boots.");
    await say(who, "They didn't ask me twice, which means they'd asked somebody else first.");
    note('Somebody from the docks has been asking about car two and its nights. They knew something before they asked.', 'note', 'a2rival', { who, how: 'Said to his face' });
  },
  ellis_joins: async (who) => {
    await say(who, who === 'alison' ? "Mr Nowak. DS Ellis has put her Quay Street papers inside the warehouse fire file. It is one case now." : "So listen. That detective. She's put Quay Street in with the fire. One file. I heard it at the caff.");
    await say(who, who === 'alison' ? 'I thought you should hear it from somebody who writes things down.' : "I'm only saying what I heard.");
    note("DS Ellis has joined the street's crimes to the warehouse fire: one case.", 'police', 'a2ellis', { who, how: 'Said to his face' });
  },
  collision: async (who) => {
    const life = xs('life'),
      fid = (life.friend && life.friend.who) || 'alison',
      Fp = P_(fid),
      fname = Fp ? Fp.def.name : 'a friend';
    await say('', `An evening off. Tom is at a table with ${fname}, a pot of tea between them, when there is a knock.`);
    await say(who, who === 'ron' ? "Boss. Sorry. It won't wait. There's a van at the landing with nobody to meet it." : "So listen, sorry, yeah? There's a van at the landing and nobody to meet it.");
    const i = await choose('', `${fname} is looking at Tom, and so is the man at the door.`, ['Get up and go with him.', 'Send him away and stay.', `Tell ${fname.split(' ')[0]} plainly what it is, then decide.`]);
    const s = st();
    if (i === 0) {
      s.collision = 'went';
      act('collision_went', { told: [fid, who], name: fname + "'s", silent: true });
      if (Fp) Fp.mind.regard = clamp(Fp.mind.regard - 0.2, -1, 1);
      await say(fid, "Go on, then. It's what you came here for, isn't it.");
    } else if (i === 1) {
      s.collision = 'stayed';
      act('collision_stayed', { told: [fid, who], name: fname + "'s", silent: true });
      if (Fp) Fp.mind.regard = clamp(Fp.mind.regard + 0.15, -1, 1);
      await say(who, who === 'ron' ? "Right you are, boss. I'll tell them you were busy. They count." : "Right. I'll say you were busy. They count, mind.");
    } else {
      s.collision = 'told';
      if (Fp) Fp.mind.regard = clamp(Fp.mind.regard + 0.05, -1, 1);
      await say(fid, "Thank you for not lying to me. I'd rather know what I'm sitting with. Now go or stay, but don't do both.");
      act('collision_stayed', { told: [fid, who], name: fname + "'s", silent: true });
    }
    note(`His day life and his night life met at ${fname}'s door. ${i === 0 ? 'He went.' : i === 1 ? 'He stayed.' : 'He said what it was.'}`, 'note', 'a2collision', { who: fid, how: 'Tom was there' });
  },
  squeeze: async (who) => {
    await say(who, who === 'sheila' ? 'Three things, the same morning. I do not believe in the same morning.' : 'Sheila says three things came the same morning.');
    await say(who, "A charge on our drivers at the dock gate. A solicitor's letter about the hire licence. And somebody put the window in on the rank side.");
    await say(who, "Each of them has three answers: pay, tell them no, or use what you know about them. Whichever, they'll all want one head to talk to in the end.");
    note('All three outfits are squeezing at once: the dock gate, the hire licence, the window. Each can be paid, defied or answered with what Tom knows.', 'note', 'a2squeeze', { who, how: who === 'sheila' ? 'Sheila says' : 'Pauline says' });
  },
  sitdown_called: async (who) => {
    const s = st(),
      head = sitDownHead(stateNow());
    s.called = { head, t: Math.round(G.t) };
    await say(who, who === 'ron' ? "Boss. Garbutt's been in. The Fixer. He says one of them will sit down with you." : "So listen. Keith Garbutt's been round. He says one of them will sit down with you.");
    await say(who, `${HEADS[head]}. In the back of your own cab, you driving, whenever you say. After that there is no more asking.`);
    note(`Keith Garbutt has brokered a sit-down with ${HEADS[head]}, in the back of Tom's own cab. Car two, on the rank: when Tom is ready.`, 'note', 'a2called', { who, how: 'Said to his face' });
    G.story.objective = `The sit-down with ${HEADS[head]}: go to car two on the rank when you are ready [E beside the cab]. What is said there cannot be unsaid.`;
  },
};
function fireBeat(id, who, asMessage) {
  const s = st();
  if (s.fired.includes(id)) return;
  s.fired.push(id);
  s.lastBeatT = G.t;
  s.pending = null;
  s.stopWait = 1;
  return scene(async () => {
    if (asMessage) await say('', 'A message was taken at the office, and it has found him.');
    await BEAT_SCENES[id](who);
    emit('acts:beat', { id });
    if (G.hooks.save) G.hooks.save();
  });
}
function beatsTick() {
  const s = st();
  if (s.act !== 2 || s.sitDown || xs('endings').ended) return;
  if (!s.pending) {
    const b = nextBeat(stateNow(), T());
    if (!b) return;
    s.pending = { id: b.id, giver: giverOf(b.giver), t: Math.round(G.t), why: b.why };
    s.stopWait = 1;
    const Gp = P_(s.pending.giver);
    if (Gp) sub(`${Gp.def.name.split(' ')[0]} wants a word.`, '', 'over', 5);
  }
  const p = s.pending;
  // the collision is an evening scene of its own; a beat nobody can bring, or one left waiting, reaches him as a message
  const late = G.t - p.t > T().beatWaitsForHimGameHours * 60;
  if (free() && (!p.giver || late || (p.id === 'collision' && hour() >= 18 && hour() < 23))) fireBeat(p.id, p.giver || 'pauline', p.id !== 'collision');
}
async function sitDown() {
  const s = st(),
    head = s.called.head,
    name = HEADS[head];
  await scene(async () => {
    await say('', `Car two, the back lane, the engine running. ${name} gets in behind him and shuts the door.`);
    const LINES = {
      widow: ["Your uncle carried for men who are finished. I am not finished. Your cars cross my gate forty times a day.", 'So. You pay the gate and you carry what I say, and nobody on your books gets hurt. Or you tell me no, here, in your own car.'],
      agar: ['Mr Nowak. I knew your uncle as a signature. You I know as a set of accounts, and they are untidy.', 'I can make the licence, the letters and the inspection of your cars go away. For a share and a quiet partner. Or you may decline, and we shall both see.'],
      cammack: ["Tommy lad. Can I call you that? Your street's dead slow. I can make it loud or I can leave it be.", "Half the nights, my lads on your rank, and nobody puts your windows in again. Or say no. I like it when they say no."],
    }[head];
    for (const l of LINES) await say(name, l);
    const opts = ['Accept the terms.', 'Tell them no.', 'Answer with what he knows about them.'];
    let i = -1;
    while (i < 0) {
      const k = await choose(name, 'Well?', opts);
      const sure = await choose('', `"${opts[k]}" This cannot be unsaid. Is that his answer?`, ['Yes. That is his answer.', 'No. Think again.']);
      if (sure === 0) i = k;
    }
    const answer = ['accept', 'defy', 'counter'][i];
    s.sitDown = { head, answer, t: Math.round(G.t) };
    act('sitdown_' + answer, { silent: true, told: ['ron', 'sheila'], head: name });
    await say(name, i === 0 ? 'Good. Then we understand each other. Drive me back.' : i === 1 ? "Then that's said. Drive me back. Carefully." : 'Is that so. Who told you that? No. Never mind. Drive me back.');
    note(`The sit-down with ${name}: Tom ${i === 0 ? 'took the terms' : i === 1 ? 'said no' : 'put what he knows on the seat between them'}.`, 'note', 'a2sitdown', { how: 'Tom was there' });
    emit('acts:sitdown', { head, answer });
    await say('', readingNow().text.join(' '));
    s.letterDay = day() + 1;
    G.story.objective = 'The sit-down is done. Whatever comes of it comes in the morning.';
  });
  setAct(3);
}

// ---------- Act III: the inspection week ----------
const books = () => {
  const e = xs('econ'),
    f = xs('fares'),
    firm = xs('firm');
  return { booksOffPence: G.money.booksOff, overWashes: st().overWashes || 0, alibiFares: f.alibiFares || e.alibiFares || 0, wagesOwedPence: e.wagesOwedPence || firm.wagesOwedPence || 0, faresDriven: G.money.fareCount };
};
const INSPECTOR = 'Mr Pybus, Customs and Excise';
async function letter() {
  const s = st();
  s.a3 = { startDay: day() + T().letterToFirstMorningGameDays, grades: [], done: [], writings: 0, lastDay: -1, trade: null, successor: null };
  await scene(async () => {
    await say('A letter, H.M. Customs and Excise', "Dear Mr Nowak. I write to arrange a routine inspection of the records of Mickey's Cars for the purposes of Value Added Tax.");
    await say('A letter, H.M. Customs and Excise', 'I shall attend at your office each morning this week from nine, and ask for one set of records each day. Anything not to hand may be asked for in writing. Yours faithfully, L. Pybus, Officer.');
    note("A letter: a VAT inspection of Mickey's books by Customs and Excise. One set of records each morning from nine, at the office. Anything not to hand may be asked for in writing.", 'note', 'a3letter', { how: 'A letter' });
    act('inspected', { silent: true, told: ['sheila', 'pauline'] });
    G.story.objective = "The inspector comes to Mickey's each morning from nine. Be at the office: produce what he asks for, or ask for it in writing.";
  });
  if (G.hooks.save) G.hooks.save();
}
const mannerLine = { courteous: 'Thank you, Mr Nowak. That is in order.', careful: 'I see. I shall make a note of that, Mr Nowak.', cold: 'I think we both know what I am looking at, Mr Nowak.', patient: 'In writing. Very well. I shall bring the same request tomorrow.' };
async function inspectorMorning(absent) {
  const s = st(),
    a = s.a3,
    idx = a.grades.length,
    item = ITEMS[idx],
    B = books(),
    S = P_('sheila');
  a.lastDay = day();
  s.lastBeatT = G.t;
  if (absent) {
    const r = morning(item.id, 'writing', B, a.writings, T());
    if (r.putOff) a.writings++;
    else a.grades.push(r.grade);
    note(`The inspector asked for ${item.name}. Tom was not there. ${r.putOff ? 'Sheila asked for it in writing.' : 'He took it as it stood.'}`, 'note', 'a3m' + day(), { who: 'sheila', how: 'Sheila says' });
    sub(`The inspector came for ${item.name}, and Tom was not at the office.`, '', 'over', 6);
  } else
    await scene(async () => {
      const trusts = S && !S.dead && (G.story.flags.sheilaNamed || S.mind.regard > 0.3);
      if (trusts) {
        const w = whereItHolds(B, T()),
          g = w.find((x) => x.id === item.id).grade;
        await say('sheila', g === 'holds' ? 'This one stands. Give it him and look bored.' : g === 'thin' ? "This one is thin. It'll hold if he's in a hurry. Your choice." : "Not this one. If he reads it properly it's finished. Ask for it in writing and buy a day.");
      }
      await say(INSPECTOR, `Good morning, Mr Nowak. Today I should like to see ${item.name}.`);
      const left = T().inWritingAllowedTimes - a.writings;
      const i = await choose(INSPECTOR, 'If it is to hand.', ['Produce it.', left > 0 ? 'Ask for it in writing.' : 'Ask for it in writing again. He will not like it.']);
      const r = morning(item.id, i === 0 ? 'produce' : 'writing', B, a.writings, T());
      if (r.putOff) a.writings++;
      else a.grades.push(r.grade);
      await say(INSPECTOR, mannerLine[r.manner]);
      note(`The inspector asked for ${item.name}. Tom ${i === 0 ? 'produced it' : 'asked for it in writing'}. His manner: ${r.manner}.`, 'note', 'a3m' + day(), { how: 'Tom was there' });
      const res = result(a.grades, T());
      if (!res.booksHold) {
        showSign('inspector_cold');
        if (S && !S.dead) await say('sheila', "That's the line crossed. I can add up a lie, I can't add up two.");
        showSign('sheila_line');
      }
      const n = a.grades.length;
      // Ellis's trade, once, mid-week: give her a rival, and the street learns who talks
      if (n >= 2 && a.trade === null && (xs('law').stage || 0) >= 1 && P_('ellis')) {
        const head = (s.sitDown && s.sitDown.head) || 'cammack';
        await say('ellis', `Mr Nowak. A bad week for paperwork. I can be a help or I can be a second inspector. Give me ${HEADS[head]}, in a statement, and I am a help.`);
        const k = await choose('ellis', 'People will learn you talked to me. They always do.', ['Give her the statement.', 'No.']);
        const sure = k === 0 ? await choose('', 'A statement cannot be taken back, and the street will know who talks. Give it?', ['Yes.', 'No.']) : 1;
        a.trade = k === 0 && sure === 0 ? head : false;
        if (a.trade) {
          act('traded_rival', { silent: true, told: ['ellis'], head: HEADS[head] });
          emit('acts:trade', { rival: head });
          await say('ellis', 'Sign there. You have done yourself some good and you will not enjoy it.');
        } else await say('ellis', 'Then I am a second inspector. Good morning.');
      }
      // someone in the crew may ask to take it over
      if (n >= 3 && a.successor === null) {
        const men = xs('crew').men || {},
          best = Object.keys(men).filter((id) => P_(id) && !P_(id).dead && (men[id].loyalty || 0) >= 0.6)[0],
          who = best || (P_('ron') && !P_('ron').dead && P_('ron').mind.regard > 0.1 ? 'ron' : null);
        if (who) {
          a.successor = { who, st: 'offered' };
          await say(who, "Boss. If it gets too heavy. I'd take it on. The name, the book, the lot, and you walk off clean. I'll not ask twice, and not after Friday.");
          note(`${P_(who).def.name} has offered to take the firm over, so Tom can walk away. The offer will not stand after the inspection.`, 'note', 'a3offer', { who, how: 'Said to his face' });
        } else a.successor = false;
      }
    });
  if (a.grades.length >= T().mornings) await lastDay();
  if (G.hooks.save) G.hooks.save();
}
// On the last day he can reach only a few people. Then the books open.
async function lastDay() {
  const s = st(),
    a = s.a3,
    over = {};
  await scene(async () => {
    await say('', 'The last day. The inspector is writing up. There is time to reach a few people, and no more.');
    const done = {};
    for (let n = 0; n < T().lastDayReachesAtMost; n++) {
      const opts = [];
      if (!done.sheila && P_('sheila') && !P_('sheila').dead) opts.push(['sheila', 'Sheila, about the books.']);
      if (!done.friend) opts.push(['friend', 'The one friend, with the truth.']);
      if (!done.ellis && a.trade === false && P_('ellis')) opts.push(['ellis', 'DS Ellis, about her offer.']);
      if (!done.succ && a.successor && a.successor.st === 'offered') opts.push(['succ', `${P_(a.successor.who).def.name}, about taking it over.`]);
      opts.push(['none', 'Nobody else. Let it come.']);
      const k = opts[await choose('', `He can still reach ${T().lastDayReachesAtMost - n === 1 ? 'one person' : 'a few people'}.`, opts.map((o) => o[1]))][0];
      if (k === 'none') break;
      done[k] = 1;
      if (k === 'sheila') {
        const i = a.grades.indexOf('thin');
        if (i >= 0 && (G.story.flags.sheilaNamed || P_('sheila').mind.regard > 0.3)) {
          a.grades[i] = 'holds';
          await say('sheila', "I've ruled one page again, properly. That one will stand now. The rest is what it is.");
        } else await say('sheila', "There's nothing left I can make stand. I'd have told you sooner if you'd let me.");
      } else if (k === 'friend') {
        const life = xs('life'),
          fid = (life.friend && life.friend.who) || 'alison',
          Fp = P_(fid);
        const h = await choose(fid, 'So tell me. What is it you do, at night?', ['Tell the truth.', 'Tell the fare book version.']);
        if (Fp) Fp.mind.regard = clamp(Fp.mind.regard + (h === 0 ? 0.3 : -0.3), -1, 1);
        over.friendHolds = h === 0 && !!Fp && !Fp.dead && Fp.mind.regard > 0;
        await say(fid, h === 0 ? "Right. That's worse than I thought and better than being lied to. Come round after. Whatever it says." : "That's what Mrs Dunn told the police, word for word. Goodbye, Tom.");
        showSign(over.friendHolds ? 'friend_act' : 'friend_gone', true);
      } else if (k === 'ellis') {
        const head = (s.sitDown && s.sitDown.head) || 'cammack';
        a.trade = head;
        act('traded_rival', { silent: true, told: ['ellis'], head: HEADS[head] });
        emit('acts:trade', { rival: head });
        await say('ellis', 'Late. But a statement is a statement. Sign there.');
      } else if (k === 'succ') {
        const sure = await choose('', 'Handing the firm over cannot be undone. Hand it over?', ['Yes. It is theirs.', 'No.']);
        if (sure === 0) {
          a.successor.st = 'took';
          act('handed_over', { silent: true, told: [a.successor.who, 'sheila'], name: P_(a.successor.who).def.name });
          showSign('successor_took', true);
          await say(a.successor.who, "Then it's mine to carry. Go on, boss. Tom. Go on.");
        }
      }
    }
    if (a.successor && a.successor.st === 'offered') {
      a.successor.st = 'withdrawn';
      note('The offer to take the firm over has been withdrawn.', 'note', 'a3withdrawn', { how: 'Tom knows' });
    }
    const res = result(a.grades, T());
    a.result = res;
    await say(INSPECTOR, res.booksHold ? 'My report will say the records were produced and are in order, Mr Nowak. Good day.' : 'My report goes to the Collector this afternoon, Mr Nowak. You will hear from us, and from others.');
    await say('', 'Then the books open.');
  });
  over.booksHold = a.result.booksHold;
  over.handedOver = !!(a.successor && a.successor.st === 'took');
  if (a.trade) over.caseSinksFirm = false;
  a.over = over;
  await runEnding(over);
}
function actThreeTick() {
  const s = st();
  if (s.act !== 3 || xs('endings').ended) return;
  if (!s.a3) {
    if (free() && day() >= (s.letterDay || 0) && hour() >= 8) letter();
    return;
  }
  const a = s.a3;
  if (a.result || a.grades.length >= T().mornings) return;
  if (day() < a.startDay || a.lastDay === day()) return;
  const h = hour();
  if (h >= T().inspectorUntilHour) inspectorMorning(true);
  else if (h >= T().inspectorFromHour && free() && G.tom.space === 'mickeys') inspectorMorning(false);
  else if (h >= T().inspectorFromHour && !a.told) {
    a.told = day();
    sub("The inspector will be at Mickey's by now.", '', 'over', 5);
  }
  if (a.told !== day()) a.told = 0;
}

// ---------- waiting (part 7.11, ER-JOB-04): "wait until" each known appointment ----------
export function appointments() {
  const s = st(),
    d = day(),
    h = hour(),
    out = [],
    at = (label, t) => t > G.t + 5 && out.push({ label, t });
  at('Wait an hour.', G.t + 60);
  if (h < 18) at("Wait until this evening, six o'clock.", d * 1440 + 18 * 60);
  if (h < 22.25) at('Wait for the last ferry, quarter past ten.', d * 1440 + 22.25 * 60);
  if (G.story.flags.teaInvited && !G.story.flags.tea && d === 2) at("Wait until Ada's tea, seven o'clock.", d * 1440 + 19 * 60 - 10);
  if (s.act === 3 && s.a3 && !s.a3.result) at('Wait until the inspector comes, nine in the morning.', (h < 9 && d >= s.a3.startDay ? d : Math.max(d + 1, s.a3.startDay)) * 1440 + 9 * 60);
  return out;
}
async function waitMenu() {
  if (!free() || !G.hooks.passTime) return;
  const ap = appointments();
  const i = await scene(() => choose('', 'Wait. A wait always stops for what the town has for him.', ap.map((a) => a.label).concat('Not now.')));
  if (i >= ap.length) return;
  st().stopWait = 0;
  await G.hooks.passTime(ap[i].t, '');
}

// ---------- Mickey's past and the fire (part 3.1.6; ruling 30 Sep) ----------
// The fire has a street version, and it is a street fact: said as what is said, by people who were not there, and
// written in the Ledger as a guess. The truth is never the street's. Mickey is described only by regulars who knew
// him, in the two approved lines.
const STREET_FIRE = "They say it was the insurance. They say one of your uncle's cars sat on the warehouse row that night with its lights off. They say a lot. Nobody who says it was there.";
const MICKEY = { ada: 'Good to his crew, hard on himself. He sat in that office because the sea was done with him.', walsh: 'He sat at the back and left before the end. I always took that as a kind of prayer.' };
export function streetFire(P) {
  const s = st();
  (s.fire || (s.fire = {}))[P.id] = 1;
  note("What the street says of the fire at No. 4: the insurance, and one of Mickey's cars on the warehouse row that night. Nobody who says it was there.", 'fire', 'firestreet', { who: P.id, how: 'The street says', sure: 'a guess' });
  return STREET_FIRE;
}
function pastMatters(P, a) {
  const s = st();
  if (['ada', 'ron', 'darren', 'grace', 'brenda', 'albert', 'rita'].includes(P.id) && day() >= 1 && !(s.fire && s.fire[P.id]))
    a.push({
      key: 'firestreet',
      direct: true,
      ask: 'what the street says about the fire at No. 4',
      raise: "You'll have seen No. 4 on the warehouse row. Burned out. Do you want what the street says about it?",
      opts: [
        {
          agree: 1,
          q: 'Do you want it?',
          yes: ['Yes. Tell me.', 'Yes. What does the street say?'],
          no: ['No. Not now.', 'No. Leave it.'],
          keep: ['Were you there?', 'Who told you?'],
          keepSay: "I wasn't there. Nobody you'll meet was there. It's only what's said. Do you want it?",
          noSay: 'Please yourself.',
          take: () => streetFire(P),
        },
      ],
    });
  if (MICKEY[P.id] && !(s.mick && s.mick[P.id]))
    a.push({
      key: 'mickey',
      direct: true,
      ask: 'what Mickey was like',
      raise: 'You never knew him, did you. Your uncle. Do you want to know what he was like?',
      opts: [
        {
          agree: 1,
          q: 'Do you?',
          yes: ['Yes. What was he like?', 'Yes. Tell me about him.'],
          no: ['No. Not today.', 'No. Another time.'],
          keep: ['How long did you know him?', 'Did you like him?'],
          keepSay: 'Long enough to have an opinion. Do you want it?',
          noSay: 'Another time, then.',
          take: () => {
            (s.mick || (s.mick = {}))[P.id] = 1;
            note(`Mickey, as ${P.def.name} knew him: ${MICKEY[P.id]}`, 'note', 'mickey_' + P.id, { who: P.id, how: P.def.name.split(' ')[0] + ' says' });
            return MICKEY[P.id];
          },
        },
      ],
    });
}

register({
  id: 'acts',
  fresh: () => ({ act: 1, answered: false, choice: null, fired: [], pending: null, lastBeatT: 0, called: null, sitDown: null, collision: null, letterDay: 0, a3: null, overWashes: 0, lastOff: 0, stopWait: 0 }),
  loaded(s) {
    if (!s.fired) s.fired = [];
    if (G.story.ended && !s.answered) {
      s.answered = true; // a save from before the one-shot whose week had ended: the story goes on from there
      s.choice = G.story.flags.choice || 'silent';
      s.lastBeatT = G.t;
    }
    G.hooks.actOneClosed = actOneClosed;
    G.hooks.stopsWait = () => {
      const v = st().stopWait;
      st().stopWait = 0;
      return !!v;
    };
    G.hooks.actPending = () => st().pending;
  },
  minute() {
    const s = st();
    if (G.money.booksOff > s.lastOff) {
      s.overWashes++;
      s.lastOff = G.money.booksOff;
    }
    if (xs('endings').ended) return;
    const a = actOf(stateNow(), T());
    if (a === 2 && s.act === 1) setAct(2);
    beatsTick();
    actThreeTick();
  },
  beatFor(P) {
    const s = st(),
      p = s.pending;
    if (p && p.giver === P.id && p.id !== 'collision') return () => fireBeat(p.id, P.id, false);
    return null;
  },
  matters(P, a) {
    pastMatters(P, a);
  },
  hotspots(out) {
    const s = st(),
      t = G.tom;
    if (s.act === 2 && s.called && !s.sitDown && t.space === 'street' && hyp(t.x, t.z, G.car.x, G.car.z) < 4.5)
      out.push({ k: 'E', t: `Sit down with ${HEADS[s.called.head]}`, run: sitDown });
    if (s.act === 3 && s.a3 && !s.a3.result && t.space === 'mickeys' && s.a3.lastDay !== day() && day() >= s.a3.startDay && hour() >= T().inspectorFromHour && hour() < T().inspectorUntilHour)
      out.push({ k: 'E', t: 'See the inspector', run: () => inspectorMorning(false) });
  },
  key(code) {
    if (code === 'Period' && free()) {
      waitMenu();
      return true;
    }
    return false;
  },
  hook: {
    read: () => JSON.parse(JSON.stringify(st())),
    state: () => stateNow(),
    beats: () => BEATS.map((b) => b.id),
    appointments: () => appointments(),
    // the tests' way through: put the story at the start of an act, in a named state
    //   jump(2)             Sheila answered 'take', Act II open, no beat fired
    //   jump(2, 'called')   every beat fired, the sit-down called
    //   jump(3)             the sit-down answered 'defy', the letter due this morning
    //   jump(3, 'mornings') the letter read, the first morning today
    jump(n, state) {
      const s = st(),
        f = G.story.flags;
      if (!f.choice) f.choice = 'take';
      G.story.ended = true;
      f.closeSeen = 1;
      s.answered = true;
      s.choice = f.choice;
      s.lastBeatT = G.t;
      if (n >= 2) setAct(2);
      if (n === 2 && state === 'called') {
        s.fired = BEATS.map((b) => b.id);
        s.called = { head: sitDownHead(stateNow()), t: Math.round(G.t) };
        s.pending = null;
      }
      if (n >= 3) {
        s.fired = BEATS.map((b) => b.id);
        s.called = s.called || { head: 'widow', t: Math.round(G.t) };
        s.sitDown = { head: s.called.head, answer: 'defy', t: Math.round(G.t) };
        s.letterDay = day();
        setAct(3);
        if (state === 'mornings') s.a3 = { startDay: day(), grades: [], done: [], writings: 0, lastDay: -1, trade: null, successor: null };
      }
      return JSON.parse(JSON.stringify(s));
    },
    fire: (id, who) => fireBeat(id, who || 'pauline', true),
    streetFire: (id) => streetFire(G.people[id]),
    sitDown: () => sitDown(),
    morning: (absent) => inspectorMorning(!!absent),
    books: () => books(),
  },
});
void on;
void roomPos;
void ROOMS;
void inputsNow;
