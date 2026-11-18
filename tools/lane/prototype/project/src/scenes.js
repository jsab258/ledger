// The week. Beats fire on states, not on the clock, and no single beat can fail the run.
import { G, day, hour, resetState, pausedWhile, setPaused } from './state.js';
import { hyp, pick, rnd, money, pounds, clamp, listAnd } from './util.js';
import { act, seed, logLine } from './events.js';
import { comeback, markSaid, tell, loudness, nameLevel } from './gossip.js';
import { heardCall, meet, note, ledgerSeen, learnName } from './ledger.js';
import { attached, tomNotices, sense, tomTarget, nightF } from './seeing.js';
import { KINDS, NAMES } from './kinds.js';
import { comebackLine, OVERHEARD, HEADLINES } from './talk_lines.js';
import { BARKS } from './cast.js';
import { initPeople, send } from './routines.js';
import { SPOTS, ROOMS, roomPos, INSIDE } from './map.js';
import { sub, say, scene, bubble, news, fade, tomName, ui, after } from './ui.js';
import { startTalk, talkSay, endTalk, decision } from './talk.js';
import { F, frontUp, setOn, recover } from './fight.js';
import { pay, earn, wash, washCap } from './money.js';
import { rest, advanceTo, workStep, beaten, tomAt } from './work.js';
import { fareOffer } from './fares.js';
import { startJob, jobHotspots, jobClock } from './jobs.js';
import { nightly } from './police.js';
import { ellisClock, arrestNow } from './police.js';
import { RULES } from './rules.js';

const REST = RULES.rest,
  MONEY = RULES.money,
  PRICE = RULES.prices;

const fl = () => G.story.flags;
const P_ = (id) => G.people[id];
let tick = 0,
  sayCool = 0,
  overCool = 8,
  barkCool = 10,
  ladT = 0;

export function newWeek() {
  resetState();
  initPeople();
  seed('inherit', [
    'sheila',
    'ron',
    'pauline',
    'kevin',
    'terry',
    'darren',
    'june',
    'walsh',
    'ada',
    'sylvia',
    'brenda',
    'grace',
    'rita',
    'albert',
    'peter',
    'lily',
    'hal',
    'nora',
    'dennis',
  ]);
  G.story.phase = 'play';
  G.story.objective = "Find Mickey's. The letter says Quay Street, the quay end, under the blue sign.";
  tick = 0;
  sayCool = 0;
  overCool = 8;
}
const askVia = () =>
  P_('ron').dead ? 'darren' : fl().ask1 === 'yes' ? 'ron' : P_('darren').dead ? 'ron' : 'darren';
const ask1Due = () => fl().tour && !fl().ask1 && day() === 0 && hour() >= 17.2;
const ask15Due = () => day() === 1 && hour() >= 17 && fl().job1 === 'done' && !fl().ask15;
const ask2Due = () => day() === 2 && hour() >= 16.3 && hour() < 22 && !fl().ask2;
const alisonDue = () => day() >= 2 && !fl().alison && hour() >= 9.3 && hour() < 17.2;
const endReady = () => !G.story.ended && (day() > 4 || (day() === 4 && hour() >= 16));
const job3On = () => fl().ask2 === 'yes' && !fl().job3 && day() === 2 && hour() >= 18.6 && hour() < 22;
const teaOn = () => fl().teaInvited && !fl().tea && day() === 2 && hour() >= 18.5 && hour() < 21.6;

// ---------- scenes ----------
const tour = () =>
  scene(async () => {
    const t = G.tom;
    meet(P_('sheila'));
    P_('sheila').mind.fam = 0.9;
    await say('sheila', "New management. Sit down, you're making the place look untidy.");
    await say(
      'sheila',
      "Sheila Dunn. I kept your uncle's books. Thirty-one years. I know what a quiet week costs, and this is a quiet year.",
    );
    await say(
      'sheila',
      "The fare book. Every fare Pauline calls goes in it. That's the clean money, such as it is.",
    );
    await say(
      'sheila',
      'The radio. Nobody in this building can help overhearing it. Remember that before you say anything near it.',
    );
    await say('sheila', 'The yard, through there. Two ways out. Your uncle liked a choice.');
    await say(
      'sheila',
      'And his other book. The debts. Iveson eighty pounds, Harrison thirty, young Milner twenty-two, Drewery fifteen, the Kettlewell girl nine. Nobody on it can pay, and they all know I know.',
    );
    const i = await decision('sheila', 'That door stays shut.', DEC.door);
    if (i === 0)
      await say(
        'sheila',
        "The real book. You'll see it when I've decided what you are. I told Mickey I'd look you over first, and I keep what I tell people.",
      );
    else await say('sheila', "Good. First sensible thing anyone's said in here since the funeral.");
    await say(
      'sheila',
      "Keys to car two. Kevin has car one. Drive it yourself if you want the book to look honest. Pauline will call you fares when you're sat in it.",
    );
    await say(
      'sheila',
      "Mrs Rennison at Regent House has your room, top of the street on this side. Mickey paid the week. After that, rent's Friday.",
    );
    fl().tour = 1;
    G.car.keys = true;
    if (t.carry === 'suitcase') t.carry = null;
    fl().unpacked = 1;
    note(
      "Mickey's book of debts: Iveson £80.00, Harrison £30.00, Milner £22.00, Drewery £15.00, Kettlewell £9.00. Nobody can pay.",
      'debts',
      'debts',
      { who: 'sheila', how: 'Sheila says' },
    );
    note('A door in the back room Sheila will not open. The real book is behind it.', 'note', 'door', {
      who: 'sheila',
      how: 'Sheila says',
    });
    G.story.objective =
      'Learn the street. Drive a fare if you like: sit in car two at the rank [F]. Ron Kirby will want a word before dark.';
  });
const ronIntro = () =>
  scene(async () => {
    meet(P_('ron'));
    P_('ron').mind.fam = 0.85;
    fl().metRon = 1;
    await say(
      'ron',
      "You'll be the nephew. Ron Kirby. I do the door and the rank, same as I did for Mickey.",
    );
    await say(
      'ron',
      "Thirty years on that dock till they finished the scheme. Now I stand here. I see who comes down this street and I don't forget it.",
    );
    await say(
      'ron',
      'Boss. You want the door watched, or you want it watched proper? Different money. Think on.',
    );
  });
const darrenIntro = () =>
  scene(async () => {
    meet(P_('darren'));
    P_('darren').mind.fam = 0.8;
    fl().metDarren = 1;
    await say(
      'darren',
      "So listen. You're him, yeah? The nephew. One suitcase. I said to Ron, that'll be him.",
    );
    await say(
      'darren',
      "Darren. I did bits for Mickey. Messages. Watching a door. I owe the book a few quid an' all, I'm not hiding it.",
    );
    await say(
      'darren',
      "Anything you want to know round here, I'm not saying I know. I'm saying I could find out.",
    );
  });
const juneIntro = () =>
  scene(async () => {
    meet(P_('june'));
    P_('june').mind.fam = 0.6;
    fl().metJune = 1;
    await say('june', "You're Tom. June Suddaby. His daughter, for what that was worth to either of us.");
    await say(
      'june',
      "I'm here for a box of photographs and I go home Friday. I want nothing from that office. I'll say it as often as you need.",
    );
  });
const paulineIntro = () =>
  scene(async () => {
    meet(P_('pauline'));
    P_('pauline').mind.fam = 0.7;
    fl().metPauline = 1;
    await say('pauline', 'Car to the station, two minutes. No, love, two real minutes. Hang on.');
    await say(
      'pauline',
      "You'll be him. Pauline. I'm the voice. Sheila's in the back and she's been expecting somebody since the funeral.",
    );
  });
const sylviaIntro = () =>
  scene(async () => {
    meet(P_('sylvia'));
    P_('sylvia').mind.fam = 0.6;
    fl().metSylvia = 1;
    await say(
      'sylvia',
      'Mr Nowak. Feet. Mat. Thank you. Your uncle paid the week. Your room is through there.',
    );
    await say(
      'sylvia',
      "Front door's locked at eleven and I hear who comes in after. Rent's Friday, and Friday means Friday.",
    );
  });
const walshIntro = () =>
  scene(async () => {
    meet(P_('walsh'));
    P_('walsh').mind.fam = 0.5;
    fl().metWalsh = 1;
    await say(
      'walsh',
      "You're Michael's nephew. I buried him from here three weeks ago. A good turnout. He'd have counted it.",
    );
    await say(
      'walsh',
      "He sat at the back and left before the end. I always took that as a kind of prayer. You're welcome to the same seat.",
    );
  });
const ask1 = () =>
  scene(async () => {
    const R = P_('ron');
    R.mark = null;
    await say('ron', "Boss. Got a minute? It's a thing of Mickey's that didn't die with him.");
    await say(
      'ron',
      "Last ferry of a Monday, a bag gets left under the bench in the shelter on the landing. It goes to Metcalfe's back door. The coin shop. Round by the alley off Chapel Lane.",
    );
    await say(
      'ron',
      "Sixty quid for the walk. There's a coat on the hook in the back room goes with it. Mickey always wore the coat.",
    );
    const i = await decision('ron', "So. Do I tell them it's still on?", ask1Spec());
    if (i === 0) await takeJob1();
    else if (i === 1) await refuseJob(1);
    else {
      fl().ask1 = 'think';
      R.pendingAsk = 'Do I tell them the Monday bag is still on?';
      await say('ron', "Think quick. The ferry's in at half ten whether you've thought or not.");
      G.story.objective = 'Ron wants an answer about the Monday bag before the last ferry, half past ten.';
    }
  });
async function takeJob1() {
  fl().ask1 = 'yes';
  P_('ron').pendingAsk = null;
  act('job_yes', { silent: true, told: ['ron'] });
  startJob(1);
  await say(
    'ron',
    "Half ten the ferry's in. The customs woman goes off at eleven, and the landing lamp goes off with her. Your choice which you'd rather have: her eyes or the dark.",
  );
  await say(
    'ron',
    "And boss. This street's quieter than you think after midnight. A footstep carries. Rain helps. Stay out from under the lamps.",
  );
  G.story.objective =
    "Tonight: the coat is on the hook in the back room [C to wear it]. After the last ferry, half past ten, a holdall under the bench in the landing shelter. Take it to Metcalfe's back door, in the alley off Chapel Lane.";
}
async function refuseJob(n) {
  fl()['ask' + n] = 'no';
  P_('ron').pendingAsk = null;
  act('job_no', { silent: true, told: [askVia() === 'ron' || n === 1 ? 'ron' : 'darren'] });
  if (n === 1) {
    await say('ron', "That's an answer. I'll pass it on. They'll not like it, but they'll hear it.");
    G.story.objective =
      'You told them no. The office is still yours. See what the street makes of it in the morning.';
  }
}
const ask15 = () =>
  scene(async () => {
    fl().ask15 = 1;
    P_('ron').mark = null;
    const i = await decision(
      'ron',
      "Boss. There's a Tuesday one if you want it. A parcel behind the smoke house door on the quay, to Rita's side door on Chapel Lane. Young Harrison takes it. Forty.",
      DEC.ask15,
    );
    if (i === 0) {
      startJob(2);
      send(P_('wayne'), 'ritaside', 'smoke', G.t + 60 * 9);
      await say(
        'ron',
        'After ten. Same rules. Rita works late with her light on, mind. That window sees the whole corner.',
      );
      G.story.objective =
        "Tonight, after ten: a parcel behind the smoke house door on the quay. Take it to Rita's side door on Chapel Lane.";
    } else await say('ron', "Suit yourself. It'll keep for somebody.");
  });
const ask2 = () =>
  scene(async () => {
    const via = askVia(),
      M = P_(via);
    M.mark = null;
    if (via === 'ron') {
      await say(
        'ron',
        "Boss. They've another. Tonight, seven. Iveson at the scrapyard, west end of the quay.",
      );
      await say(
        'ron',
        'Eighty behind and laughing about it. They want it collected, or they want him to stop laughing. A hundred in it for you, on top of the eighty for the book.',
      );
    } else {
      await say(
        'darren',
        "So listen. Don't shoot the messenger, yeah? They said ask you once more. Different money.",
      );
      await say(
        'darren',
        "Iveson, the scrap man, west end of the quay. Tonight at seven. He owes the book eighty and he's laughing about it. They want it collected or they want him to stop laughing. Hundred in it.",
      );
    }
    const opts = ["I'll see him.", "No. I'm not their collector."];
    if (fl().teaInvited) opts.push("I've somewhere to be at seven.");
    const i = await decision(via, 'What do I tell them?', ask2Spec(via, opts.length > 2));
    if (i < 0) {
      await say(
        via,
        via === 'ron'
          ? "They'll want an answer before seven, boss."
          : "They want an answer by seven, yeah? I'm just saying.",
      );
      return;
    }
    if (i === 0) {
      fl().ask2 = 'yes';
      act('job_yes', { silent: true, told: [via] });
      send(P_('dennis'), 'scrap', 'work', G.t + 60 * 6);
      await say(
        via,
        via === 'ron'
          ? "He has a yard lad. Big. Slow. And Iveson respects a name more than a fist, if you've got one by now."
          : "He's got a lad up there, big lad. I'm just saying. Nice one.",
      );
      G.story.objective =
        "Seven o'clock: Iveson's scrapyard, west end of the quay. Eighty pounds. Front him up [Q] and decide how far it goes." +
        (fl().teaInvited ? ' Ada expects you at seven as well.' : '');
    } else if (i === 1) {
      fl().ask2 = 'no';
      act('job_no', { silent: true, told: [via] });
      await say(
        via,
        via === 'ron'
          ? "Then that's twice. They count."
          : "Alright. Alright. I'll tell them. I'd not want to be the one telling them, but I'll tell them.",
      );
      G.story.objective = fl().teaInvited
        ? "Ada expects you at seven. Knock at her door, opposite Mickey's."
        : 'You told them no.';
    } else {
      fl().ask2 = 'tea';
      act('job_no', { silent: true, told: [via] });
      await say(
        via,
        via === 'ron'
          ? "Ada's. Aye. Well. She'd not have waited, and nor will they. You've picked."
          : "Tea? You're having tea? Right. No, fair enough. I'll say you were busy.",
      );
      G.story.objective = "Seven o'clock: Ada's door, opposite Mickey's.";
    }
  });
const adaInvite = () =>
  scene(async () => {
    meet(P_('ada'));
    learnName('ada');
    fl().teaInvited = 1;
    fl().metAda = 1;
    await say('ada', "You. Mickey's nephew. Stand where I can see you.");
    await say(
      'ada',
      "You'll come for your tea tonight. Seven. I knew your uncle forty years and I'll see what he's left us.",
    );
    await say('ada', "I don't ask twice.");
    G.story.objective =
      'Ada has asked you to tea at seven tonight. She does not ask twice.' +
      (fl().ask2 === 'yes' ? " Iveson's yard is at seven as well." : '');
  });
const teaScene = (late) =>
  scene(async () => {
    const A = P_('ada'),
      t = G.tom;
    act(late ? 'tea_late' : 'tea', { told: ['ada'], noiseR: 4 });
    fl().tea = late ? 'late' : 'yes';
    A.mind.regard = clamp(A.mind.regard + (late ? 0.1 : 0.4), -1, 1);
    A.mind.fam = 1;
    if (G.hooks.enterRoom) G.hooks.enterRoom('ada', true);
    {
      const sa = ROOMS.ada.spots.ada,
        st2 = ROOMS.ada.spots.tom,
        [ax, az] = roomPos('ada', sa[0], sa[1]),
        [tx, tz] = roomPos('ada', st2[0], st2[1]);
      A.hold = true;
      A.route = null;
      A.space = 'ada';
      A.x = ax;
      A.z = az;
      A.ang = sa[2];
      A.state = 'sit';
      A.moving = false;
      A.atWindow = false;
      t.x = tx;
      t.z = tz;
      t.ang = st2[2];
      t.sit = true;
    }
    await say(
      'ada',
      late
        ? "Tea's stewed. You're late, and I can see your knuckles. Sit down anyway."
        : "Wipe your feet. Sit there. That was his chair when he came, which wasn't often.",
    );
    await say(
      'ada',
      'Forty years I knew your uncle. Good to his crew, hard on himself. He sat in that office because the sea was done with him.',
    );
    await say('ada', "Now. I'll tell you what I've seen, since nobody else will say it to you plain.");
    const ms = A.mind.mem
      .filter(
        (m) => attached(m) && !['inherit', 'tea', 'tea_late'].includes(G.ev[m.e].kind) && m.src !== 'self',
      )
      .sort((a, b) => b.heat - a.heat)
      .slice(0, 3);
    if (!ms.length)
      await say('ada', "Nothing. You've been careful or you've been dull, and I can't yet tell which.");
    for (const m of ms) {
      await say('ada', comebackLine(A, m));
      m.said = true;
      ledgerSeen(G.ev[m.e], A, 'said', m.src === 'told' ? m.from : null);
    }
    await say(
      'ada',
      "I don't sleep. I sit. In the dark, mostly. You'll not see me unless I want you to. Remember there's others the same.",
    );
    const i = await decision(
      'ada',
      "This street will call you what it decides. It decided about Mickey in a week. It's had you three days.",
      DEC.ada,
    );
    await say(
      'ada',
      i === 0 ? 'That he was theirs. Whoever they are this year.' : 'Nobody does, love. Drink your tea.',
    );
    await say('ada', "Go on. I've a window to mind.");
    note(
      'Ada sits at her window in the dark, not to be seen unless she wants it. There are others the same.',
      'note',
      'adadark',
      { who: 'ada', how: 'Ada says' },
    );
    t.sit = false;
    A.hold = false;
    A.space = 'home';
    A.atWindow = true;
    A.state = 'window';
    A.goalKey = 'home|window';
    advanceTo(G.t + 75, false);
    if (G.hooks.leaveRoom) G.hooks.leaveRoom();
    G.story.objective = 'Thursday and Friday are yours. Sheila will want an answer by Friday evening.';
  });
const alisonAsk = () =>
  scene(async () => {
    const A = P_('alison');
    A.mark = null;
    fl().alison = 1;
    meet(A);
    act('talk_press', { target: 'alison' });
    await say('alison', "Mr Nowak? Alison Sedman, Evening Mail. I'll not keep you.");
    await say(
      'alison',
      "No. 4 on the warehouse row burned five weeks ago. One of your uncle's cars was on the row that night. Did he keep a book that would say why?",
    );
    const i = await decision(
      'alison',
      'Off the record is still a record, Mr Nowak. It just has better manners.',
      DEC.alison,
    );
    fl().alisonAns = i;
    if (i === 0) {
      await say(
        'alison',
        "That's what Mrs Dunn told the police, word for word. Funny how a fare book learns a sentence.",
      );
      A.mind.regard -= 0.05;
    } else if (i === 1) {
      await say('alison', "Then I'll hold a paragraph for you. I'm at Rinaldi's most mornings.");
      A.mind.regard = clamp(A.mind.regard + 0.3, -1, 1);
      note(
        'Promised the reporter a look in the book for the night of the fire. The real book: not seen yet.',
        'fire',
        'promise',
        { who: 'alison', how: 'Said it' },
      );
    } else {
      await say('alison', "That's a quote, in its way. Good morning, Mr Nowak.");
      A.mind.regard -= 0.15;
    }
    note(
      "Evening Mail reporter: one of Mickey's cars was on the warehouse row the night No. 4 burned.",
      'fire',
      'alison',
      { who: 'alison', how: 'Alison says' },
    );
  });
const ellisTalk = () =>
  scene(async () => {
    const E = P_('ellis');
    meet(E);
    act('talk_ellis', { target: 'ellis' });
    await say('ellis', "Mr Nowak. Carol Ellis, CID. I've been getting to know your street.");
    await say(
      'ellis',
      "I'm not here about you. Yet. I'm here about a warehouse, and a cab that was seen beside it, and a man who died before I could ask him.",
    );
    const i = await decision(
      'ellis',
      'People down here have started to say your name. I notice when that happens. Is there anything you want to tell me first?',
      DEC.ellis,
    );
    if (i === 2) {
      E.mind.regard = clamp(E.mind.regard + 0.2, -1, 1);
      fl().ellisDeal = 1;
      await say('ellis', "I'll hold you to that. Most people I hold to things regret it.");
    } else if (i === 1) {
      P_('sheila').mind.regard -= 0.15;
      fl().blamedSheila = 1;
      await say('ellis', "I have. She's very good. Thirty-one years of very good.");
    } else await say('ellis', 'No. They never do, first time.');
    note('DS Ellis is asking the street about Tom. She is here about the fire.', 'police', 'ellis', {
      who: 'ellis',
      how: 'Ellis says',
    });
  });
const dennisScene = () =>
  scene(async () => {
    const D = P_('dennis');
    meet(D);
    await say('dennis', "If it's about the eighty quid, I'm out.");
    const i = await decision('dennis', "Your uncle's dead, son. Dead men don't send bills.", DEC.dennis);
    if (i === 0) after(0.05, () => frontUp(D, { type: 'debt' }));
    else if (i === 1) {
      forgive(D);
      fl().job3 = 'forgave';
      await say(
        'dennis',
        "You what? Struck out? Well. Well, I'll be damned. Your uncle never struck a thing out in his life.",
      );
      G.story.objective = 'You struck Iveson out of the book. The people who sent you will hear.';
    }
  });
function forgive(P) {
  const d = G.debts[P.id];
  if (!d || d.st !== 'open') return;
  d.st = 'forgiven';
  act('debt_forgive', { target: P.id });
  P.mind.regard = clamp(P.mind.regard + 0.5, -1, 1);
}
function collect(P, part = 1) {
  const d = G.debts[P.id];
  if (!d || d.st !== 'open') return 0;
  const amt = Math.round(d.owed * part);
  d.st = part >= 1 ? 'paid' : 'part';
  d.owed -= amt;
  if (d.owed > 0) d.st = 'open';
  earn(amt, true);
  act('debt_paid', { target: P.id });
  return amt;
}
const endScene = () =>
  scene(async () => {
    const S = P_('sheila'),
      f = fl(),
      lv = nameLevel(S);
    S.mark = null;
    if (G.hooks.doorOpen) G.hooks.doorOpen();
    await say(
      'sheila',
      "Sit down. It's Friday. I said I'd decide what you are, and I haven't. So you can tell me.",
    );
    f.sheilaAsked = 1; // the Open part may now say "Today": she has asked
    await say(
      'sheila',
      'This is the real book. Thirty-one years of it. Every arrangement, every name, every night one of our cars went somewhere with its lights off.',
    );
    await say(
      'sheila',
      'The warehouse row, the night No. 4 went up. Ten past two. No charge. His own hand. The page after is cut out, and not by me.',
    );
    const did = [];
    if (f.job1 === 'done') did.push('carried their bag');
    if (f.job2 === 'done') did.push('carried their parcel');
    if (f.job3 === 'done') did.push("collected for them at Iveson's");
    if (f.job3 === 'forgave') did.push('struck Iveson out of the book');
    const no = (f.ask1 === 'no' ? 1 : 0) + (f.ask2 === 'no' || f.ask2 === 'tea' ? 1 : 0);
    await say(
      'sheila',
      (did.length ? 'This week you ' + listAnd(did) + '. ' : 'This week you carried nothing for them. ') +
        (no ? `You told them no ${no === 2 ? 'twice' : 'once'}. ` : '') +
        (G.money.booksOff > 0
          ? 'You put more through my fare book than it could hold. '
          : G.money.fareCount > 3
            ? 'You drove fares yourself, and the book liked it. '
            : '') +
        (f.tea === 'yes'
          ? "You sat down at Ada's when she asked."
          : f.tea === 'snub'
            ? 'You left Ada sat waiting.'
            : ''),
    );
    const town = NAMES[G.hooks.townLevel ? G.hooks.townLevel() : 1] || 'nothing yet';
    await say('sheila', `The street calls you ${town}. I hear it through the wall.`);
    const i = await decision('sheila', 'So which is it going to be?', DEC.end);
    if (i < 0) {
      await say('sheila', "It'll keep an hour. No longer.");
      return;
    }
    const choice = ['wind', 'take', 'silent'][i];
    f.choice = choice;
    const earned = lv >= 3 || S.mind.regard > 0.15;
    if (i === 0)
      await say('sheila', "Then I'll tell Garbutt myself. He'll not take it from you. He might from me.");
    else if (i === 1) await say('sheila', "Then you'd better learn to read this faster than he did.");
    else await say('sheila', 'No. Well. The street will decide for you, then. It usually does.');
    if (earned) {
      f.sheilaNamed = 1;
      await say(
        'sheila',
        i === 2
          ? "Go home, Tom. It'll keep till Monday."
          : 'Right then, Tom. Shut that door behind you. Not the other one. That one stays open now.',
      );
    } else await say('sheila', 'Shut the door on your way out, new management.');
    heardCall(S);
    await endWeek(choice);
  });
export async function endWeek(choice) {
  const st = G.story;
  if (st.ended) return;
  st.ended = true;
  fl().choice = choice;
  act('choice_' + choice, { silent: true, told: ['sheila', 'pauline'] });
  setPaused(true, 'the end of the week');
  await fade(
    true,
    choice === 'silent'
      ? 'You say nothing.\n\nBy Saturday dinner time the street has said it for you.'
      : 'By Saturday dinner time the whole of Quay Street knows what you said in that back room.',
  );
  st.endT = Math.round(G.t);
  advanceTo(G.t + 20 * 60);
  nightly(day());
  if (G.hooks.save) G.hooks.save();
  if (G.hooks.end) G.hooks.end();
}

// ---------- hooks for talk, fights and the controller ----------
export function beatFor(P) {
  const f = fl();
  switch (P.id) {
    case 'sheila':
      if (!f.tour) return tour;
      if (endReady()) return endScene;
      break;
    case 'ron':
      if (!f.metRon) return ronIntro;
      if (ask1Due() || f.ask1 === 'think') return f.ask1 === 'think' ? null : ask1;
      if (ask15Due()) return ask15;
      if (ask2Due() && askVia() === 'ron') return ask2;
      break;
    case 'darren':
      if (!f.metDarren) return darrenIntro;
      if (ask2Due() && askVia() === 'darren') return ask2;
      break;
    case 'june':
      if (!f.metJune) return juneIntro;
      break;
    case 'pauline':
      if (!f.metPauline) return paulineIntro;
      break;
    case 'sylvia':
      if (!f.metSylvia) return sylviaIntro;
      break;
    case 'walsh':
      if (!f.metWalsh) return walshIntro;
      break;
    case 'alison':
      if (alisonDue()) return alisonAsk;
      break;
    case 'dennis':
      if (job3On() && G.debts.dennis.st === 'open') return dennisScene;
      break;
    case 'ellis':
      if (G.story.ellis && !G.story.ellis.tom) {
        G.story.ellis.tom = 1;
        return ellisTalk;
      }
      break;
    case 'ada':
      if (day() === 2 && hour() >= 9 && hour() < 18.5 && !f.teaInvited) return adaInvite;
      break;
  }
  return null;
}
function ronEyes() {
  // what the door saw that Tom did not
  const out = [];
  const led = G.ledger.acts;
  for (let i = G.events.length - 1; i >= 0 && out.length < 2; i--) {
    const E = G.events[i];
    if (G.t - E.t > 1440 * 1.2 || KINDS[E.kind].noself) continue;
    const a = led.find((x) => x.e === E.id);
    for (const id of E.wit) {
      const W = G.people[id];
      if (!W || W.anon || W.id === 'ron' || (a && a.seen[id])) continue;
      const m = W.mind.by[E.id];
      if (!m) continue;
      ledgerSeen(E, W, 'bought');
      out.push(
        `${W.def.name} ${W.space === 'home' || m.window ? 'was at a window' : 'was looking'} when you ${KINDS[E.kind].mine(E).replace(/^./, (c) => c.toLowerCase())}`,
      );
      break;
    }
  }
  return out.length
    ? out.join('. And ') + ". That's what the door saw."
    : "Nobody saw a thing you don't already know about, boss. That's worth knowing an' all.";
}
function darrenHeard(p) {
  const D = P_('darren');
  let b = null;
  for (const m of D.mind.mem)
    if (attached(m) && m.src === 'told' && G.ev[m.e].kind !== 'inherit' && (!b || m.heat > b.heat)) b = m;
  let s = b
    ? `${comebackLine(D, b)} ${b.from && G.people[b.from] ? 'Had it off ' + G.people[b.from].def.name.split(' ')[0] + '.' : ''}`
    : "Nothing going round that I've heard. Honest.";
  if (b) ledgerSeen(G.ev[b.e], D, 'bought', b.from);
  if (p >= 500) {
    seed('good_word', ['darren']);
    s += " And I'll put it about that you're all right. Leave it with me.";
  }
  return s;
}
// ---------- decisions, written by the game: a yes, a no and a line that keeps talking ----------
const HOLD = ['No, hold off for now.', "No. I'll think on it."],
  NOT = ['No. Not today.', 'No. Leave it for now.'],
  MICK = ["What happens if I don't?", 'What would Mickey have done?'];
const PRINT = {
  q: 'Is that what you want me to print?',
  yes: ['Yes. Print that.', "Yes. That's my answer."],
  no: ["No. Don't print that.", 'No. Let me think.'],
  keep: ['Who told you to ask me?', 'What have you got already?'],
  keepSay:
    "I don't give my sources, Mr Nowak. I'd not give you up either. Is that what you want me to print?",
};
const COP = {
  q: "That's your answer to me, is it?",
  yes: ["Yes. That's my answer.", 'Yes.'],
  no: ['No. Let me put it another way.', 'No. Give me a minute.'],
  keep: ['Who has been saying my name?', "What is it you think I've done?"],
  keepSay: "I ask, Mr Nowak. I don't tell. Is that your answer?",
};
const DEC = {
  door: {
    leaveIdx: 1,
    opts: [
      { say: ["What's behind it?", 'What do you keep in there?'] },
      { say: ['Fair enough.', 'Then it stays shut.'] },
    ],
  },
  ada: {
    leaveIdx: 1,
    opts: [
      { say: ['What did it decide about him?', 'And what did it decide about Mickey?'] },
      { say: ["I didn't come here to be decided about.", "I'd sooner decide for myself."] },
    ],
  },
  ask15: {
    direct: true,
    noIdx: 1,
    leaveIdx: 1,
    ask: 'whether he will move the Tuesday parcel for forty pounds',
    opts: [
      {
        agree: 1,
        q: 'Forty. Yes or no?',
        yes: ["Yes. I'll move it.", "Yes. Tuesday's on."],
        no: ['No. Not tonight.', 'No. Not this one.'],
        keep: ['Who is it for?', "What's in the parcel?"],
        keepSay: "You don't ask that, boss. Nobody asks that. Forty. Yes or no?",
      },
    ],
  },
  alison: {
    leaveIdx: 2,
    ask: 'what he will say to the paper about the warehouse fire',
    opts: [
      Object.assign(
        {
          say: [
            "There's a fare book. It shows nothing for that night.",
            'The fare book shows nothing for that night.',
          ],
        },
        PRINT,
      ),
      Object.assign(
        {
          say: [
            "I'll look. If there's something, you'll hear it from me.",
            "Let me look. You'll hear it from me first.",
          ],
        },
        PRINT,
      ),
      Object.assign(
        { refuse: 1, say: ["I've nothing to say to the paper.", 'Nothing for the paper. Not from me.'] },
        PRINT,
      ),
    ],
  },
  ellis: {
    leaveIdx: 0,
    ask: 'whether he has anything to tell the detective',
    opts: [
      Object.assign({ refuse: 1, say: ['No.', 'No. Nothing.'] }, COP),
      Object.assign(
        {
          say: [
            'Ask Sheila Dunn about the books. I only got here Monday.',
            'I only got here Monday. Ask Sheila Dunn about the books.',
          ],
        },
        COP,
      ),
      Object.assign(
        {
          agree: 1,
          say: ["If I find something, I'll bring it to you.", "Anything I find, you'll have it from me."],
        },
        COP,
      ),
    ],
  },
  dennis: {
    leaveIdx: 2,
    ask: 'the eighty pounds Iveson owes the book',
    keep: ['What was it for?', 'How long has it stood?'],
    keepSay: 'Two year. And your uncle never once came up here for it himself. Now then.',
    opts: [
      { say: ['Then we settle it here.', "I'm not leaving without it."] },
      {
        say: ["I'm striking it out. It dies with Mickey.", "Forget the eighty. It's struck out."],
        q: 'Struck out? For good?',
        yes: ['Yes. For good.', 'Yes. Struck out.'],
        no: ['No. Leave it stand for now.', 'No. Let me think.'],
        keep: ['What was it for?', 'How long has it stood?'],
        keepSay: 'Scrap he had and never paid for. Two year. Struck out, you said. For good?',
      },
    ],
  },
  end: {
    ask: 'what he will do with what his uncle left him',
    opts: [
      {
        say: ['Wind it down. Just the cabs.', "I'm getting out of Mickey's business."],
        q: "You're winding it down. The cabs stay and the rest stops. Is that it?",
        yes: ['Yes. Wind it down.', 'Yes. Just the cabs.'],
        no: ['No. Give me a bit longer.', 'No. Let me think.'],
        keep: ['What would that mean for you?', 'What happens to Ron, then?'],
        keepSay:
          "I keep a fare book, Ron keeps a door, and somebody tells them it's done. That's what it means. So. You're winding it down?",
      },
      {
        say: ["I'm taking it on. All of it.", "I'll keep it going. All of it."],
        q: "You're taking it over. All of it, with your name on it. Is that it?",
        yes: ["Yes. It's mine now.", "Yes. I'm keeping it going."],
        no: ['No. Not yet.', 'No. I need longer.'],
        keep: ['What comes with it, exactly?', 'Who else knows about it?'],
        keepSay:
          "The book behind that door, and everybody who is in it. More know than you'd like. So. You're taking it over?",
      },
      {
        say: ["I'm not saying. That's my answer.", "That's my business, Sheila."],
        q: "You're telling me nothing. That's the answer I write down?",
        yes: ["Yes. I'm saying nothing.", "Yes. That's for me to know."],
        no: ['No. Give me a minute.', 'No. Ask me again later.'],
        keep: ['Why does it matter so much?', 'What would you do?'],
        keepSay:
          "Because on Monday I open that book for somebody, and I'd sooner know who. I'd do as I'm told, same as ever. So. You're telling me nothing?",
      },
    ],
  },
};
function ask1Spec(yes, no) {
  // Ron's ask: said while it stands, then his plain question
  return {
    leaveIdx: 2,
    ask: 'whether he will carry the Monday bag from the ferry',
    keep: ["What is it I'd be carrying?", 'Who are they, Ron?'],
    keepSay:
      "You don't ask, boss. Mickey never asked. It's a bag and it's sixty quid. Do I tell them it's on?",
    opts: [
      {
        agree: 1,
        take: yes,
        say: ["I'll do it. Tell them it's on.", "All right. I'll carry it."],
        q: "You'll carry it? Once I tell them it's on, it's on.",
        yes: ["Yes. Tell them it's on.", "Yes. I'll carry it."],
        no: HOLD,
        keep: MICK,
        keepSay:
          "Mickey carried it every Monday for nine years. If you don't, I tell them, and they count. So. You'll carry it?",
      },
      {
        refuse: 1,
        take: no,
        say: ["Tell them no. I'm not doing it.", "I'm not carrying it. Count me out."],
        q: 'You want me to tell them no?',
        yes: ['Yes. Tell them no.', "Yes, I'm sure."],
        no: HOLD,
        keep: MICK,
        keepSay:
          "Mickey carried it nine years and never once said no. If you don't, they count it. You want me to tell them no?",
      },
    ],
  };
}
function ask2Spec(via, tea) {
  const r = via === 'ron',
    o = [
      {
        agree: 1,
        say: ["I'll see him.", "All right. I'll go and see Iveson."],
        q: r ? "I tell them you'll see Iveson at seven. Yes?" : "So I say you'll see Iveson at seven, yeah?",
        yes: ["Yes. Seven o'clock.", 'Yes. Tell them.'],
        no: HOLD,
        keep: ["What happens if I don't?", 'What has Iveson done to them?'],
        keepSay: "He owes and he laughs. They can stand the owing. So. Do I tell them you'll see him?",
      },
      {
        refuse: 1,
        say: ["No. I'm not their collector.", "Tell them no. I don't collect."],
        q: r
          ? "You want me to tell them no? That's twice."
          : "You want me to tell them no, yeah? That's twice.",
        yes: ['Yes. Tell them no.', "Yes, I'm sure."],
        no: HOLD,
        keep: MICK,
        keepSay: 'Twice is a number they remember. You want me to tell them no?',
      },
    ];
  if (tea)
    o.push({
      say: ["I've somewhere to be at seven.", "Seven's no good. I'm expected."],
      q: 'So I tell them not tonight. Yes?',
      yes: ['Yes. Not tonight.', "Yes. I'm expected elsewhere."],
      no: HOLD,
      keep: MICK,
      keepSay: 'Not tonight is a no with manners. So I tell them not tonight?',
    });
  return { ask: 'whether he will collect from Iveson at seven', opts: o };
}
function mattersFor(P) {
  // what is open between Tom and this person, raised by them once he has spoken
  const a = [],
    f = fl(),
    m = G.money,
    id = P.id,
    d = G.debts[id],
    today = (k) => {
      if (P['off_' + k] === day()) return false;
      return true;
    },
    mark = (k) => {
      P['off_' + k] = day();
    };
  const book = () =>
    `Fares this week ${money(m.fares)}, ${m.fareCount} of them. ${m.washed ? money(m.washed) + " put through that wasn't fares. " : ''}${m.booksOff ? 'It is ' + money(m.booksOff) + ' out and I know where. ' : 'It adds up. '}Pocket ${money(m.clean)}.`;
  if (id === 'sheila' && m.dirty > 0)
    a.push({
      key: 'wash',
      direct: true,
      ask: 'whether to put the tin through the fare book',
      raise: `There's ${money(m.dirty)} in the tin that never came off a meter. The fare book will hide about ${money(washCap())} of it. Do you want it put through?`,
      opts: [
        {
          agree: 1,
          q: 'Through the book, or not?',
          yes: ['Yes. Put it through.', 'Yes. Through the book.'],
          no: ['No. Leave it in the tin.', 'No. Not yet.'],
          keep: ['What does the book say this week?', 'How much will it hide?'],
          keepSay: book() + ' Through the book, or not?',
          take: async () => {
            endTalk();
            await scene(wash);
          },
        },
      ],
    });
  if (id === 'ron') {
    if (f.ask1 === 'think')
      a.push(
        Object.assign(
          { key: 'ask1', raise: "The Monday bag, boss. Do I tell them it's still on?" },
          ask1Spec(
            async () => {
              endTalk();
              await scene(takeJob1);
            },
            async () => {
              endTalk();
              await scene(() => refuseJob(1));
            },
          ),
        ),
      );
    else if (today('door'))
      a.push({
        key: 'door',
        direct: true,
        ask: 'whether to pay Ron five pounds to watch the door',
        raise:
          'I can watch the door proper for you, boss. A fiver, and I tell you who looks at this office. Want it?',
        opts: [
          {
            agree: 1,
            q: 'A fiver. Yes or no?',
            yes: ['Yes. Five pounds.', 'Yes. Watch the door.'],
            no: NOT,
            keep: ['What have you seen so far?', 'Who looks at this office?'],
            keepSay: "That's what the fiver is for, boss. Yes or no?",
            noSay: 'Right you are, boss.',
            take: () => {
              mark('door');
              if (!pay(PRICE.ronWatchesTheDoorPence)) return "Come back when you've got it, boss.";
              act('paid_info', { target: 'ron' });
              P.mind.regard = clamp(P.mind.regard + 0.1, -1, 1);
              return ronEyes();
            },
          },
        ],
      });
  }
  if (id === 'darren') {
    if (today('heard'))
      a.push({
        key: 'heard',
        direct: true,
        ask: 'whether to pay Darren three pounds for what he has heard',
        raise: "So listen. Three quid and I tell you what I've heard. Yeah?",
        opts: [
          {
            agree: 1,
            q: 'Three quid. Yeah or no?',
            yes: ['Yes. Three pounds.', 'Yes. Tell me.'],
            no: NOT,
            keep: ['Heard from who?', 'Is it worth three pounds?'],
            keepSay: "Can't say till I've said it, can I. Three quid. Yeah or no?",
            noSay: 'Suit yourself, chief.',
            take: () => {
              mark('heard');
              if (!pay(PRICE.darrenSaysWhatHeHeardPence))
                return "So listen, I'd love to, but I've got to eat.";
              act('paid_info', { target: 'darren' });
              return darrenHeard(300);
            },
          },
        ],
      });
    else if (today('word'))
      a.push({
        key: 'word',
        direct: true,
        ask: 'whether to pay Darren five pounds to speak well of him',
        raise: 'And a fiver gets a good word put about for you. Yeah?',
        opts: [
          {
            agree: 1,
            q: 'A fiver. Yeah or no?',
            yes: ['Yes. Five pounds.', 'Yes. Talk me up.'],
            no: NOT,
            keep: ['Who listens to you?', 'What would you say about me?'],
            keepSay: "Everybody listens to me, chief. They just don't let on. Fiver. Yeah or no?",
            noSay: 'No bother. Offer stands.',
            take: () => {
              mark('word');
              if (!pay(PRICE.darrenPutsAGoodWordAboutPence)) return 'Not for nothing, chief.';
              act('paid_info', { target: 'darren' });
              return darrenHeard(500);
            },
          },
        ],
      });
  }
  if (d && d.st === 'open') {
    const owe = pounds(d.owed),
      ASK = ['How long has it stood?', 'What was it for?'],
      asked = "Since before your uncle went. It was a loan, that's all it was.";
    a.push({
      key: 'debt',
      ask: 'the ' + owe + ' this person owes the book',
      raise: `If it's about the ${owe} on Mickey's book, I know about it.`,
      keep: ASK,
      keepSay: asked,
      opts: [
        {
          say: [`I've come for the ${owe} on the book.`, `It's the ${owe}. I want it paid.`],
          q: 'You want it now? Today?',
          yes: ['Yes. Today.', 'Yes. Now.'],
          no: ['No. It can wait a bit.', 'No. Not today.'],
          keep: ASK,
          keepSay: asked + ' You want it now?',
          take: () => {
            if (P.mind.fear > 0.45 || (P.mind.regard > 0.3 && d.owed <= 1500)) {
              const amt = collect(P);
              return `Here. ${money(amt)}. That's us square. Tell Sheila to cross it through.`;
            }
            talkSay('sys', 'You could leave it, strike it out, or front up to them on the street [Q].');
            return id === 'dennis'
              ? "Eighty quid? Your uncle's dead, son. Dead men don't send bills."
              : "I haven't got it. You can see I haven't got it.";
          },
        },
        {
          say: ["I'm striking it out of the book.", 'Forget it. It dies with Mickey.'],
          q: 'Struck out? For good?',
          yes: ['Yes. For good.', 'Yes. Struck out.'],
          no: ['No. Leave it stand for now.', 'No. Let me think.'],
          keep: ASK,
          keepSay: asked + ' Struck out, you said. For good?',
          take: () => {
            forgive(P);
            if (id === 'dennis' && fl().ask2 === 'yes') fl().job3 = 'forgave';
            return [
              "You what? Struck out? Well. I'll not forget that.",
              'You mean it? Mickey never struck anybody out. Ta. I mean it. Ta.',
            ][d.owed % 2];
          },
        },
      ],
    });
  }
  if (id === 'grace')
    a.push({
      key: 'tea',
      direct: true,
      ask: 'whether he wants tea',
      raise: "Tea? Twenty pence. Sit by the window and you'll hear the lot.",
      opts: [
        {
          agree: 1,
          q: 'Tea, then?',
          yes: ["Yes. Tea, and I'll sit a while.", "Yes, please. I'll sit."],
          no: ['No. Not just now.', 'No. Another time.'],
          keep: ["What's the talk in here today?", 'Who comes in of a morning?'],
          keepSay: "Sit with a tea and you'll hear it yourself. I only pour. Tea, then?",
          noSay: "It'll be here.",
          take: async () => {
            endTalk();
            teaSit();
          },
        },
      ],
    });
  if (id === 'sylvia' && day() >= 3 && !f.rent)
    a.push({
      key: 'rent',
      direct: true,
      ask: 'the eighteen pounds rent, due Friday',
      raise: "It's eighteen pounds, Mr Nowak, due on the Friday. Have you got it?",
      opts: [
        {
          agree: 1,
          q: 'Eighteen pounds. Have you got it?',
          yes: ["Yes. Here's the eighteen pounds.", "Yes. I'll pay it now."],
          no: NOT,
          keep: ['When exactly is it due?', 'Did my uncle ever stop here?'],
          keepSay: "Friday, by six. I don't chase and I don't forget. Eighteen pounds. Have you got it?",
          keepDid: () => {
            f.rentBySix = 1; // the Open part may now give the hour: she has said it
          },
          noSay: 'Friday, Mr Nowak.',
          take: () => {
            if (!pay(MONEY.rentPence, true)) return "That's not eighteen pounds, Mr Nowak. I can count.";
            f.rent = 1;
            act('rent_paid', { target: 'sylvia' });
            P.mind.regard = clamp(P.mind.regard + 0.25, -1, 1);
            return 'Thank you. On the Friday. I shall say so if anybody asks.';
          },
        },
      ],
    });
  if (id === 'wayne' && today('wares')) {
    const w = [
      ['cosh', PRICE.coshPence],
      ['flick knife', PRICE.flickKnifePence],
    ].filter(([x]) => G.tom.weapon !== x);
    if (w.length)
      a.push({
        key: 'wares',
        ask: 'things Wayne sells that are not in the window',
        raise: `If you want something that's not in the window: ${w.map(([x, c]) => `a ${x}, ${money(c)}`).join('. Or ')}.`,
        keep: ['What would I want one for?', 'Who else have you sold to?'],
        keepSay: "I don't ask what for and I don't say who to. You following?",
        opts: w.map(([x, c]) => ({
          say: [
            `I'll have the ${x}.`,
            `The ${x}. ${pounds(c).replace(/^./, (m) => m.toUpperCase())}, you said.`,
          ],
          q: `${money(c)}. Cash. Yes?`,
          yes: ['Yes. Cash.', 'Yes. Here.'],
          no: NOT,
          keep: ['Is it any good?', 'Where did it come from?'],
          keepSay: `It does what it's for. ${money(c)}. Yes?`,
          take: () => {
            mark('wares');
            if (!pay(c)) return "Cash, pal. I'm not the Co-operative.";
            G.tom.weapon = x;
            return 'You never got that here. You following?';
          },
        })),
      });
  }
  if (id === 'pauline' && G.car.keys && !G.story.fare)
    a.push({
      key: 'fare',
      direct: true,
      ask: 'whether car two wants the next fare',
      raise: "Car two? I've one on the radio if you want it. Do you?",
      opts: [
        {
          agree: 1,
          q: 'Do you want the fare?',
          yes: ["Yes. I'll take it.", 'Yes. Give it to car two.'],
          no: ['No. Give it to Ron.', 'No. Not this one.'],
          keep: ['Is it busy today?', 'Who rings most?'],
          keepSay: "Steady. It's the same eight people and the station. Do you want the fare?",
          noSay: "I'll give it to car one.",
          take: async () => {
            endTalk();
            fareOffer();
          },
        },
      ],
    });
  if (id === 'june' && day() === 4 && hour() >= 12 && !f.juneFare && !f.juneGone)
    a.push({
      key: 'june',
      direct: true,
      ask: 'whether he will drive June to the station himself',
      raise: "My train goes this afternoon. I don't suppose you'd run me to the station yourself?",
      opts: [
        {
          agree: 1,
          q: 'Would you? Yourself?',
          yes: ["Yes. I'll run you myself.", "Yes. I'll bring the car round."],
          no: ['No. Ron will take you.', "No. I can't today."],
          keep: ["Where is it you're going?", 'Will you be back?'],
          keepSay: 'Home. And I doubt it. Would you run me yourself?',
          noSay: "I'll ring for a car, then.",
          take: async () => {
            f.juneFare = 1;
            endTalk();
            const s = SPOTS.laundrygate;
            send(P, 'laundrygate', 'idle', G.t + 240);
            sub("I'll be outside Regent House in a few minutes. Bring the car round.", tomName(P));
            after(4, () =>
              fareOffer({ from: 'Regent House', sx: s[0], sz: s[1] + 14, dest: 'station', who: 'june' }),
            );
          },
        },
      ],
    });
  return a;
}
function pending(P, it) {
  const f = fl();
  if (P.id === 'ron' && f.ask1 === 'think') {
    if (it.intent === 'agree')
      return {
        say: "Right. Half ten. The coat's on the hook.",
        directive:
          'He has said yes to carrying the Monday bag. Tell him the ferry is in at half past ten and the coat is on the hook.',
        after: () => scene(takeJob1),
        close: true,
      };
    if (it.intent === 'refuse')
      return {
        say: "That's an answer.",
        directive:
          'He has said no to the Monday bag. Accept it flatly: that is an answer, and you will pass it on.',
        after: () => scene(() => refuseJob(1)),
        close: true,
      };
  }
  return null;
}
function yielded(P, demand, rung) {
  if (!demand || demand.type !== 'debt') return;
  const d = G.debts[P.id];
  if (!d || d.st !== 'open') return;
  const amt = collect(P, rung >= 3 ? 1 : 0.5);
  sub(
    rung >= 3
      ? `Take it. ${money(amt)}. Take it and get out of my yard.`
      : `Here\'s ${money(amt)}. It\'s all there is today.`,
    tomName(P),
    'face',
  );
  if (P.id === 'dennis' && fl().ask2 === 'yes' && !fl().job3) {
    fl().job3 = 'done';
    earn(PRICE.scrapyardCollectionPayPence, true);
    note("Iveson paid. £100.00 from Garbutt's people is in the tin.", 'money', null, { how: 'Counted it' });
    G.story.objective =
      'It is done. Thursday and Friday are yours. Sheila will want an answer by Friday evening.';
  }
}
function fightOver() {
  const D = P_('dennis');
  if (fl().ask2 === 'yes' && !fl().job3 && (D.down || D.hurt > 0.5) && F.struck) {
    fl().job3 = 'done';
    earn(PRICE.scrapyardCollectionPayPence, true);
    note("Iveson has stopped laughing. £100.00 from Garbutt's people is in the tin.", 'money', null, {
      how: 'Counted it',
    });
  }
}

// ---------- small verbs ----------
async function teaSit() {
  if (!pay(REST.teaAtTheCaffPence, true)) return sub("You haven't twenty pence.", '', 'over');
  const here = G.named.filter((p) => p.space === 'caff' && !p.gone);
  sub(`${tomName(P_('grace'))} puts a mug down in front of you. You sit, and listen.`, '', 'over', 3.5);
  await pausedWhile('tea at the caff', async () => {
    await fade(true);
    advanceTo(G.t + REST.teaAtTheCaffGameMinutes, false);
    await fade(false);
  });
  for (const P of here) P.mind.fam = clamp(P.mind.fam + REST.caffFamiliarityGain, 0, 1);
  const talkers = here.filter((p) =>
    p.mind.mem.some((m) => attached(m) && m.heat > 0.2 && G.ev[m.e].kind !== 'inherit'),
  );
  if (talkers.length >= 2) {
    sub(`${tomName(talkers[0])} and ${tomName(talkers[1])} stop talking when you look up.`, '', 'over', 5);
    note(
      `${tomName(talkers[0])} and ${tomName(talkers[1])} had their heads together at Rinaldi's and stopped when Tom looked up.`,
      'talking',
      'tea' + day() + talkers[0].id,
      { who: talkers[0].id, sure: 'a guess' },
    );
  }
  overhear(true);
}
function paper() {
  if (!pay(PRICE.eveningPaperPence, true)) return sub("You haven't twenty pence.", '', 'over');
  const d = day();
  news(
    G.story.flags.dead ? 'MAN FOUND DEAD ON THE HOOK' : G.story.lastNews || HEADLINES[d % HEADLINES.length],
    d === 0 ? 'Humberside CID decline to close the case of No. 4, Warehouse Row' : '',
  );
  fl().paper = d;
}
function overhear(force) {
  const o = pick(OVERHEARD.filter((x) => (force ? x.n : true)));
  sub(o.s, 'overheard', 'over', 5);
  if (o.n) note(o.n, 'rival', 'ov:' + o.k, { how: 'Overheard it' });
  overCool = rnd(16, 30);
}
export function hotspots() {
  const out = [],
    t = G.tom,
    f = fl(),
    sp = t.space;
  if (t.inCar) return out;
  const at = (h) => {
    const [x, z] = roomPos(h.room, h.x, h.z);
    return tomAt(x, z, h.within);
  };
  if (sp === 'mickeys') {
    if (at(INSIDE.coatHook) && f.ask1 === 'yes' && !t.hasCoat && !f.coatGone)
      out.push({
        k: 'E',
        t: "Take the runner's coat",
        run: () => {
          t.hasCoat = true;
          sub('Heavier than it looks. Something is sewn in the hem. [C] puts it on.', '', 'over', 5);
        },
      });
    if (at(INSIDE.photograph))
      out.push({
        k: 'E',
        t: 'Look at the photograph',
        run: () =>
          sub(
            "Michael Suddaby. A cap, a trawler's bow behind him, a look that gives nothing away.",
            '',
            'over',
            5,
          ),
      });
    if (at(INSIDE.backDoor) && !endReady())
      out.push({
        k: 'E',
        t: 'Try the door',
        run: () => {
          if (P_('sheila').space === 'mickeys') sub('That one stays shut.', tomName(P_('sheila')));
          else sub('Locked. A good lock, newer than the door.', '', 'over');
        },
      });
    if (at(INSIDE.cot)) out.push({ k: 'E', t: 'The cot: rest', run: () => rest('cot') });
  } else if (sp === 'boarding') {
    if (at(INSIDE.bed)) out.push({ k: 'E', t: 'Your bed: sleep or rest', run: () => rest('bed') });
  } else if (sp === 'caff') {
    if (at(INSIDE.caffCounter) && P_('grace').space === 'caff')
      out.push({ k: 'T', t: 'Tea, and sit a while (20p)', run: teaSit });
  } else if (sp === 'news') {
    if (at(INSIDE.paperCounter)) out.push({ k: 'T', t: 'Evening Mail (20p)', run: paper });
  } else if (sp === 'tangs') {
    if (at(INSIDE.chipCounter) && hour() >= 17)
      out.push({
        k: 'T',
        t: 'Chips (45p)',
        run: () => {
          if (pay(PRICE.chipsPence, true)) {
            sub("Ten minutes. If I say ten, it's ten.", tomName(P_('peter')));
            for (const id of ['peter', 'lily']) P_(id).mind.fam = clamp(P_(id).mind.fam + 0.08, 0, 1);
          }
        },
      });
  } else if (sp === 'chapel') {
    if (at(INSIDE.chapelPew) && f.chapelDay !== day())
      out.push({
        k: 'T',
        t: 'Sit at the back a while',
        run: async () => {
          f.chapelDay = day();
          act('chapel', {});
          await pausedWhile('sitting in the chapel', async () => {
            await fade(true);
            advanceTo(G.t + REST.chapelGameMinutes, false);
            await fade(false);
          });
        },
      });
  } else if (sp === 'street') {
    const A = P_('ada'),
      ad = SPOTS.adadoor;
    if (tomAt(ad[0], ad[1], 2.2)) {
      if (teaOn())
        out.push({ k: 'E', t: "Knock at Ada's", run: () => teaScene(hour() > 19.9 || G.tom.hurt > 0.2) });
      else if (A.space === 'home' && A.awake && A.atWindow)
        out.push({
          k: 'E',
          t: 'Speak up to Ada at her window',
          run: () => {
            const b = beatFor(A);
            if (b) b();
            else startTalk(A);
          },
        });
    }
    jobHotspots(out);
  }
  return out;
}

// ---------- the running week ----------
function comebacks() {
  const t = G.tom;
  if (G.paused || t.inCar || F.on || G.t < sayCool) return;
  const T = tomTarget();
  let best = null,
    bm = null,
    bs = 0;
  for (const P of G.named) {
    if (P.gone || P.dead || P.down || P.space !== t.space || !P.awake || P.fight || P.def.police) continue;
    const d = hyp(P.x, P.z, t.x, t.z);
    if (d > 5.5) continue;
    if (d > 3 && !sense(P, T).see) continue;
    const m = comeback(P);
    if (!m) continue;
    const sc = m.heat * (1.4 - d / 8);
    if (sc > bs) {
      bs = sc;
      best = P;
      bm = m;
    }
  }
  if (!best) return;
  const line = comebackLine(best, bm);
  markSaid(best, bm);
  heardCall(best);
  best.mind.look = 6;
  best.alert = { x: t.x, z: t.z, t: 5 };
  sub(line, tomName(best), 'face', 6.5);
  bubble(best, '“…”', 4);
  sayCool = G.t + 7;
  if (G.hooks.sfx) G.hooks.sfx('face');
  logLine(`${best.def.name} said it to his face: ${line}`, 'face');
}
const HAIL = {
  sheila: ["When you've a minute.", "A word, when you're ready."],
  ron: ['Boss. A word.', "Boss. When you've a minute."],
  darren: ['Here. Got a sec?', 'Oi. A quick word, yeah?'],
  alison: ['Excuse me. A moment?', 'Could I have a word?'],
  sylvia: ["It's Friday, you know.", 'A word about Friday.'],
};
function marks() {
  const f = fl(),
    d = day(),
    h = hour();
  P_('sheila').mark = !f.tour || endReady() ? '!' : null;
  P_('ron').mark =
    ask1Due() || ask15Due() || (ask2Due() && askVia() === 'ron') ? '!' : f.ask1 === 'think' ? '?' : null;
  P_('darren').mark = ask2Due() && askVia() === 'darren' ? '!' : null;
  P_('alison').mark = alisonDue() ? '?' : null;
  P_('sylvia').mark = d === 4 && !f.rent ? '£' : null;
  P_('dennis').mark = job3On() && G.debts.dennis.st === 'open' ? '!' : null;
  // nobody carries a mark over their head now: someone who wants a word turns, lifts a hand and says so
  if (!ui.modal && !G.paused && !F.on)
    for (const id of ['sheila', 'ron', 'darren', 'alison', 'sylvia']) {
      const P = P_(id),
        t = G.tom;
      if (!P.mark || P.gone || P.dead || P.space !== t.space || t.inCar || hyp(P.x, P.z, t.x, t.z) > 12)
        continue;
      const now = performance.now();
      if ((P.hailAt || 0) > now) continue;
      P.hailAt = now + 50000;
      P.mind.look = Math.max(P.mind.look || 0, 3.5);
      if (!P.moving) {
        P.react = 'point';
        P.reactT = 1.4;
      }
      sub(HAIL[id][(d + (P.hailN = (P.hailN || 0) + 1)) % HAIL[id].length], tomName(P), '', 4);
    }
  if (endReady() && !G.story.ended) {
    const S = P_('sheila');
    if (!S.override) send(S, 'mickeys:sheila', 'work');
    G.story.objective =
      'It is Friday. The door in the back room is open, and Sheila is waiting behind her desk.';
  }
  if (ask1Due() && !P_('ron').override) send(P_('ron'), 'rank', 'idle', G.t + 400);
  if (ask2Due()) {
    const M = P_(askVia());
    if (!M.override) send(M, askVia() === 'ron' ? 'rank' : 'pave', 'idle', G.t + 300);
  }
  if (d === 3 && h >= 8 && !f.d4obj) {
    f.d4obj = 1;
    if (!G.story.objective.includes('Friday'))
      G.story.objective =
        'Thursday. Fares, the book of debts, the street. Rent is due at Regent House tomorrow. Sheila will want an answer by Friday evening.';
  }
  if (d === 1 && h >= 7.5 && !f.d2obj) {
    f.d2obj = 1;
    G.story.objective =
      'Tuesday. Walk the street and hear what it made of yesterday. The Ledger [L] holds only what you have seen and heard yourself.';
  }
  if (d === 2 && h >= 7.5 && !f.d3obj) {
    f.d3obj = 1;
    if (!f.teaInvited)
      G.story.objective =
        "Wednesday. Somebody has been watching you from the window opposite Mickey's all week.";
  }
}
function proximity() {
  const t = G.tom,
    f = fl();
  if (G.paused || t.inCar || F.on || ui.modal) return;
  const nearP = (id, r) => {
    const P = P_(id);
    return !P.gone && P.space === t.space && hyp(P.x, P.z, t.x, t.z) < r && !P.dead;
  };
  if (!f.metDarren && day() === 0 && nearP('darren', 6)) return darrenIntro();
  if (!f.metRon && nearP('ron', 4.5)) return ronIntro();
  if (!f.metJune && nearP('june', 3.2)) return juneIntro();
  if (!f.metPauline && nearP('pauline', 3.6) && t.space === 'mickeys') return paulineIntro();
  if (!f.adaSaw && t.space === 'street' && tomAt(-6.5, 32, 6) && P_('ada').atWindow && nightF() < 0.5) {
    f.adaSaw = 1;
    sub("You'll be the Suddaby nephew. You've his walk.", 'A voice from the window above', 'face', 6);
    note("An old woman sits at the window opposite Mickey's. She knew Tom by his walk.", 'note', 'adawin', {
      who: 'ada',
    });
  }
  if (
    day() === 2 &&
    hour() >= 9 &&
    hour() < 18.5 &&
    !f.teaInvited &&
    t.space === 'street' &&
    tomAt(-6.5, 32, 7) &&
    P_('ada').atWindow
  )
    return adaInvite();
  if (alisonDue() && nearP('alison', 5) && t.space === 'street') return alisonAsk();
}
function ambient(dt) {
  const t = G.tom;
  overCool -= dt;
  barkCool -= dt;
  if (overCool <= 0 && !G.paused) {
    overCool = 6;
    for (const P of G.named) {
      if (!P.chat || P.space !== t.space || P.gone) continue;
      if (hyp(P.x, P.z, t.x, t.z) < 9 && tomNotices(P)) {
        overhear(false);
        break;
      }
    }
  }
  if (barkCool <= 0 && !G.paused && !t.inCar) {
    for (const P of G.crowd) {
      if (P.gone || P.space !== t.space || P.lad || P.pax) continue;
      if (hyp(P.x, P.z, t.x, t.z) < 2.6 && P.mind.look > 0) {
        bubble(P, pick(P.keeper ? P.def.bark : nightF() > 0.6 ? BARKS.night : BARKS.day), 3);
        barkCool = rnd(14, 26);
        break;
      }
    }
  }
}
function lads(dt) {
  // at night two of Cammack's lads on your road is dangerous
  const t = G.tom;
  if (t.inCar || F.on || G.paused || t.space !== 'street') {
    ladT = 0;
    return;
  }
  const near = G.crowd.filter(
    (p) => p.lad && !p.gone && !p.down && !p.dead && p.space === 'street' && hyp(p.x, p.z, t.x, t.z) < 5.5,
  );
  if (!near.length) {
    ladT = Math.max(0, ladT - dt);
    return;
  }
  const night = nightF() > 0.6,
    hot = loudness() > 1.2 || t.carry === 'bag' || fl().ask1 === 'no' || fl().ask2 === 'no';
  if (ladT === 0) {
    bubble(near[0], pick(BARKS.lads), 4);
    near.forEach((p) => {
      p.alert = { x: t.x, z: t.z, t: 6 };
    });
    if (!fl().ladsNote) {
      fl().ladsNote = 1;
      note(
        "Cammack's lads stand about outside the video shop on Copper Row, and on the quay late on. They know Tom.",
        'rival',
        'lads',
      );
    }
  }
  ladT += dt;
  if (night && hot && ladT > 5.5 && near.length >= 2 && !fl().ladsDone) {
    fl().ladsDone = day() + 1;
    ladT = 0;
    sub('Cammack says hello.', tomName(near[0]), 'face');
    setOn(near);
  }
}
export function clock() {
  const d = day(),
    h = hour(),
    f = fl();
  if (h >= 4 && d >= 1) nightly(d - 1);
  jobClock();
  ellisClock();
  if (f.ask1 === 'think' && (d > 0 || h < 4) && d >= 1 && h >= 3.5) {
    f.ask1 = 'noshow';
    P_('ron').pendingAsk = null;
    seed('no_show', ['ron']);
  }
  if (d === 1 && h >= 8.75 && !f.nudge) {
    f.nudge = 1;
    nudge();
  }
  if (f.ask2 === 'yes' && !f.job3 && (d > 2 || (d === 2 && h >= 22.2))) {
    f.job3 = 'noshow';
    seed('no_show', [askVia(), 'dennis']);
  }
  if (f.teaInvited && !f.tea && (d > 2 || (d === 2 && h >= 21.6))) {
    f.tea = 'snub';
    seed('tea_snub', ['ada']);
    P_('ada').mind.regard = clamp(P_('ada').mind.regard - 0.35, -1, 1);
  }
  // "Friday, by six": the rent is late from six on Friday evening, as Mrs Rennison says
  const rentLateFrom = MONEY.rentDueDayIndex * 1440 + MONEY.rentLateFromHour * 60;
  if (G.t >= rentLateFrom && !f.rent && !f.rentLate) {
    f.rentLate = 1;
    seed('rent_late', ['sylvia']);
  }
  if (d === 2 && h >= 13 && h < 18 && !f.teaInvited && !G.paused && !P_('ada').dead) {
    f.teaInvited = 1;
    learnName('ada');
    sub(
      'Word from over the road: Ada says you are to come for your tea at seven. She says she does not ask twice.',
      'Passed along the street',
      'face',
      8,
    );
    note("Ada, at the window opposite Mickey's, wants Tom for tea at seven on Wednesday.", 'note', 'adatea', {
      who: 'ada',
      how: 'Passed along the street',
    });
    if (!G.story.objective.includes('Iveson'))
      G.story.objective =
        "Ada has asked you to tea at seven tonight: her door is opposite Mickey's. She does not ask twice.";
  }
}
// Tuesday: what he did on Monday comes back from someone close to the people he met.
function nudge() {
  const tos = ['grace', 'brenda', 'kevin', 'pauline', 'albert', 'julie', 'lee']
    .map(P_)
    .filter((p) => !p.dead);
  if (
    tos.some((p) => p.mind.mem.some((m) => attached(m) && m.src === 'told' && G.ev[m.e].kind !== 'inherit'))
  )
    return;
  for (const a of ['ron', 'darren', 'ada', 'terry', 'hal']) {
    const A = P_(a);
    const m = A.mind.mem
      .filter((x) => attached(x) && !['inherit'].includes(G.ev[x.e].kind) && !KINDS[G.ev[x.e].kind].priv)
      .sort((x, y) => y.heat - x.heat)[0];
    if (!m) continue;
    const B = tos.find((p) => !p.mind.by[m.e]);
    if (B) {
      tell(A, B, m, "Rinaldi's");
      return;
    }
  }
}
export function storyStep(dt) {
  const f = fl(),
    t = G.tom;
  if (!f.arrived) {
    f.arrived = 1;
    act('arrive');
  }
  clock();
  workStep(dt);
  lads(dt);
  ambient(dt);
  tick += dt;
  if (tick < 0.4) return;
  tick = 0;
  marks();
  comebacks();
  proximity();
  recover();
  const h = hour();
  const spent =
    h >= REST.deadOnHisFeetFromHour && h < REST.deadOnHisFeetUntilHour && G.story.lastSleepDay < day();
  if (spent && !G.paused && !F.on && !G.story.arrest?.st) {
    G.story.lastSleepDay = day();
    collapse();
  }
  if (
    day() >= REST.weekEndsUnansweredOnDayIndex &&
    h >= REST.weekEndsUnansweredAtHour &&
    !G.story.ended &&
    !G.paused
  ) {
    sub('You never went in. Sheila locked the door and went home. That is an answer as well.', '', 'over', 6);
    endWeek('silent');
  }
}
async function collapse() {
  const t = G.tom;
  await pausedWhile('dead on his feet: to bed', async () => {
    await fade(true, 'You are dead on your feet.\nYou get as far as your bed.');
    if (t.inCar) t.inCar = false;
    if (G.hooks.enterRoom) G.hooks.enterRoom('boarding', true);
    advanceTo(day() * 1440 + REST.wakesAfterCollapseAtHour * 60);
    t.hurt = Math.max(0, t.hurt - REST.collapseHealsHurtBy);
    await fade(false);
  });
  if (G.hooks.save) G.hooks.save();
}
export function initStory() {
  Object.assign(G.hooks, {
    matters: mattersFor,
    pending,
    yielded,
    fightOver,
    beaten,
    arrestNow,
    clock,
    ellisTalk,
    bought: (P, p) => (P.id === 'ron' ? ronEyes() : P.id === 'darren' ? darrenHeard(p) : null),
    demandFor: (P) => (G.debts[P.id] && G.debts[P.id].st === 'open' ? { type: 'debt' } : null),
    killed: (P) => {
      news('MAN FOUND DEAD ON THE HOOK', 'Police appeal for witnesses');
      G.story.lastNews = 'MURDER INQUIRY: QUAY STREET SEALED';
    },
  });
}
