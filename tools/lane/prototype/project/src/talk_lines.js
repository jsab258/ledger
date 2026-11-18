// Written lines. What people say to Tom's face when a story reaches them, and what they fall back on when the live talk is unavailable.
// {n} what they call him, {src} who told them, {t} the other party, {z} place, {d} day, {w} weapon.
import { pick, DAYS, cap, R } from './util.js';
import { G, hour, day } from './state.js';
import { KINDS } from './kinds.js';
import { nameLevel } from './gossip.js';
import { attached } from './seeing.js';
import { RULES } from './rules.js';
const TALKING = RULES.talk;

export const SAY = {
  night_out: {
    saw: [
      'Funny hours you keep.',
      'You were about late. I was up.',
      "Saw you on {z} gone midnight. Couldn't sleep either?",
    ],
    told: ['They say you keep funny hours.', '{src} says you were out on {z} in the small hours.'],
  },
  coat_day: {
    saw: ["That's Mickey's coat. I'd know it across the river.", 'Bit much for daylight, that coat.'],
    told: ["I hear you've been walking about in Mickey's coat."],
  },
  ran: {
    saw: ['You were in a hurry last night.'],
    told: ["Heard you were seen running. Nobody runs round here unless it's from something."],
  },
  parcel: {
    saw: ['That was a heavy bag for a short walk.', "I saw the bag. I'm only saying I saw it."],
    told: [
      'Word is you were carrying for somebody {d} night.',
      "{src} says there was a bag. {src} doesn't get bags wrong.",
    ],
  },
  pickup: {
    saw: ['I saw what you picked up at {z}.'],
    told: ["They're saying something was left at {z} and went away with you."],
  },
  drop: {
    saw: ["A caller at {z}, at that hour. I've eyes."],
    told: ['I hear there was a caller at {z}, late on.'],
  },
  cab_drive: {
    saw: ['Driving yourself now? Mickey never did, after the first year.'],
    told: ["They say you're on the cabs yourself. Folk like that."],
  },
  cab_night: {
    saw: ['One of your cars was out late on {z}.'],
    told: ["A Mickey's car on {z} gone midnight. That's what I heard."],
  },
  fare: { saw: [], told: ["{src} says you drove them and didn't take the long way round."] },
  free_ride: {
    saw: [],
    told: ["Heard you wouldn't take {t}'s fare money. That gets round, a thing like that."],
  },
  job_yes: {
    saw: [],
    told: ["So you're carrying on where Mickey left off. That's what I hear.", 'Heard you said yes to them.'],
  },
  job_no: { saw: [], told: ['Heard you told them no.', "They say you sent Garbutt's errand back unopened."] },
  no_show: { saw: [], told: ['Heard they waited on you and you never came.'] },
  tea: {
    saw: ["Saw you go in at Ada's. She doesn't ask everyone."],
    told: ["You had your tea at Ada's, I hear. That counts for something on this street."],
  },
  tea_late: { saw: [], told: ["Late to Ada's, they say, and with your knuckles skinned."] },
  tea_snub: { saw: [], told: ['Ada had the good cups out, I heard. And sat on her own.'] },
  chapel: {
    saw: ['Saw you in the chapel. Your uncle sat at the back and all.'],
    told: ["They say you've been in the chapel."],
  },
  talk_ellis: {
    saw: ['You and that detective had plenty to say.'],
    told: ["Word is you've been talking to Ellis. People notice who a man talks to."],
  },
  talk_press: {
    saw: ['That reporter had her notebook out with you.'],
    told: ["I hear you've been talking to the paper."],
  },
  asked_fire: {
    saw: [],
    told: ["You've been asking about the fire. Folk who ask about that fire get asked back."],
  },
  stare: { saw: ['I saw you front {t} up.'], told: ['They say you stared {t} out on {z}.'] },
  squareup: { saw: ['I saw you square up to {t}.'], told: ['They say you squared up to {t}.'] },
  threat: {
    saw: ['I heard what you said to {t}. Half the street did.'],
    told: ['Heard you threatened {t}.', '{src} says you leaned on {t}.'],
  },
  shove: { saw: ['You put your hands on {t}. I saw.'], told: ['They say you laid hands on {t}.'] },
  strike: {
    saw: ["I watched you hit {t}. I'll not forget it."],
    told: ["It's all down the street. You hit {t}."],
  },
  weapon_out: {
    saw: ['I saw what you had in your hand.'],
    told: ['They say you pulled a {w} on {t}. They say it quietly.'],
  },
  weapon_used: {
    saw: ['I saw you use that {w}. I saw the blood.'],
    told: ['They say you used a {w} on {t}. Nobody says it loud.'],
  },
  kill: {
    saw: ["I saw what you did to {t}. God forgive you, because this street won't."],
    told: ['Everyone knows about {t}. Nobody says it. Everyone knows.'],
  },
  set_on: {
    saw: ["Saw them set about you. You stayed on your feet, I'll give you that."],
    told: ['Heard some lads tried it on with you.'],
  },
  beaten: { saw: ['You took a hiding. I saw them leave you.'], told: ['Heard you took a beating.'] },
  patched: {
    saw: ["You look better than you did on Grace's kitchen floor."],
    told: ["Grace says she's had you bleeding in her kitchen."],
  },
  debt_paid: { saw: [], told: ['Heard {t} paid up. Wonders never cease.'] },
  debt_forgive: {
    saw: [],
    told: ["Is it right you struck {t} out of Mickey's book? Mickey never struck anybody out."],
  },
  paid_info: { saw: [], told: ['I hear you pay for what you want to know. I know a few things myself.'] },
  bribe_try: { saw: [], told: ["They say you tried to put money in {t}'s hand."] },
  lied: { saw: [], told: ['{t} says you looked them in the eye and lied.'] },
  good_word: {
    saw: [],
    told: ["Darren Milner says you're all right. Mind, Darren says that about whoever's paying."],
  },
  arrested: { saw: ['I saw them walk you to the car.'], told: ['Heard the police had you.'] },
  ran_police: {
    saw: ['You ran from a policeman. On this street.'],
    told: ['They say you legged it from the police.'],
  },
  bag_taken: {
    saw: ["I saw the constable take that bag off you. Under the lamp, an' all."],
    told: ['Word is the police had a bag off you. Whose was it, love?'],
  },
  ellis_asked: {
    saw: ['That detective stopped me about you.'],
    told: ['Word is Ellis was down the street after you.'],
  },
  rent_paid: { saw: [], told: ['Sylvia says you paid on the Friday. She says it like a reference.'] },
  rent_late: { saw: [], told: ['Sylvia says you were short with the rent.'] },
  knocked: {
    saw: ['You had {t} over with that car.'],
    told: ['They say you knocked {t} down with the cab.'],
  },
  crash: { saw: ["You'll have that wing to pay for."], told: ["Heard you bent Mickey's car."] },
  choice_wind: { saw: [], told: ["So you're winding it down. Mickey's. I never thought I'd see it."] },
  choice_take: { saw: [], told: ["So it's you now. In Mickey's chair, doing Mickey's business."] },
  choice_silent: {
    saw: [],
    told: ["Sheila asked you straight and you wouldn't say. That's what they're telling."],
  },
  arrive: {
    saw: ['One suitcase. I saw you get off the bus.'],
    told: ['They say you came with one suitcase.'],
  },
};
const GRUDGE = {
  stare: "You stood and stared me out. I've not forgotten.",
  squareup: 'You squared up to me. I remember a thing like that.',
  threat: "You threatened me. I've not said who to. Yet.",
  shove: 'You put your hands on me. I remember.',
  strike: 'You hit me. This street has a long memory and so have I.',
  weapon_out: 'You pulled a weapon on me. Think on that when you want something.',
  weapon_used: "I've the stitches to remember you by.",
  bribe_try: "I've still not taken your money.",
  lied: "You lied to my face. I let it go. I didn't forget it.",
  knocked: 'You put me on the road with that car.',
};
// A few lines in a principal's own mouth.
const OWN = {
  sheila: {
    night_out: 'You were out late. Three people told me before I had my coat off.',
    parcel: "The bag got where it was going, I hear. I didn't hear it from you.",
    job_no: 'You told them no. Mickey never managed that in thirty years.',
    strike: "You hit {t}. I do the books. I don't do bail.",
    cab_drive: 'You took fares yourself. The book likes that.',
    tea: "Tea at Ada's. She'll have got more out of you than I have.",
    arrested: 'They had you in. I told Pauline to say you were at the dentist.',
  },
  ron: {
    night_out: "Boss. You were seen late. I'd have told you who was looking, for the right money.",
    job_no: "You told them no. I passed it on. They didn't like it, but they heard it.",
    strike: 'Boss. You hit {t}. Tidy, was it? Folk are saying tidy.',
    tea: "Tea at Ada's. Clever. She's worth ten of me for seeing.",
  },
  darren: {
    parcel: "So listen. Somebody saw the bag. I'm not saying who, I'm saying somebody.",
    job_yes: 'So listen, I heard you said yes. Good. Good for everyone, that.',
    threat: "So listen, you leaned on {t}, yeah? Everybody knows. I didn't say nothing.",
  },
  ada: {
    night_out: 'Funny hours you keep. I was sat here.',
    parcel: 'I saw the bag. Coat or no coat, I know a walk.',
    coat_day: "That's Mickey's coat. You've not his shoulders for it.",
    strike: 'I saw you hit {t}. Your uncle hit people. It never mended anything.',
  },
};
const dayOf = (t) => DAYS[Math.floor((t - TALKING.smallHoursBelongToTheDayBeforeUntilGameMinute) / 1440) % 7]; // the small hours belong to the night before
export function vocative(P) {
  if (P.id === 'sheila') return G.story.flags.sheilaNamed ? 'Tom' : 'new management';
  const l = nameLevel(P);
  if (l < 2) return '';
  if (l === 2) return P.def.upright || P.def.voice === 'official' ? 'Mr Nowak' : 'Nowak';
  return l === 3 ? 'Tom' : 'Tommy';
}
function fill(s, P, m, E) {
  const src =
    m && m.from && m.from !== 'someone' && G.people[m.from]
      ? G.people[m.from].def.name.split(' ')[0]
      : 'Somebody';
  const tgt = E && E.target === P.id ? 'me' : (E && E.name) || 'them';
  return s
    .replace(/\{src\}/g, src)
    .replace(/\{t\}/g, tgt)
    .replace(/\{z\}/g, (E && E.zone) || 'the street')
    .replace(/\{d\}/g, E ? dayOf(E.t) : '')
    .replace(/\{w\}/g, (E && E.weapon) || 'blade')
    .replace(/\{n\}/g, vocative(P));
}
// The line someone says to his face for a memory they hold.
export function comebackLine(P, m) {
  const E = G.ev[m.e],
    kind = E.kind;
  let s;
  if (m.src === 'self' && GRUDGE[kind]) s = GRUDGE[kind];
  else if (OWN[P.id] && OWN[P.id][kind]) s = OWN[P.id][kind];
  else {
    const bank = SAY[kind] || { saw: [], told: [] };
    const list = m.src === 'told' ? bank.told : bank.saw;
    s = list.length
      ? pick(list)
      : bank.told[0] || bank.saw[0] || "I heard something about you. I'll not say what.";
  }
  s = fill(s, P, m, E);
  if (m.who === 'owner' && m.src !== 'self')
    s = pick(["I'm not saying it was you. ", 'Might have been you, might not. ', 'Somebody your size. ']) + s;
  const v = vocative(P);
  if (v && !/boss|new management|listen/i.test(s) && Math.random() < TALKING.addressWordChance)
    s = s.replace(/[.?]$/, (c) => ', ' + v + c);
  return s;
}

// ---------- fallbacks for free talk ----------
export const GREET = {
  sheila: ['New management.', 'Yes?'],
  ron: ['Boss.', 'Now then, boss.'],
  darren: ["So listen. I was hoping I'd see you.", 'Alright, chief.'],
  ada: ['I saw you coming. I see everybody coming.', 'Well. Come where I can see you.'],
  june: ['Mr Nowak.', "I haven't changed my mind, if that's what you're here for."],
  ellis: ['Mr Nowak.'],
  alison: ['Mr Nowak. Have you a minute? Everybody has a minute.'],
  walsh: ["God be with you. You're welcome here, whatever brings you."],
  pauline: ['Hello, love. Hang on. Car two, where are you? Go on, love.'],
  kevin: ["Now then. You'll be wanting the keys or a moan, and I've only the moan."],
  terry: ['Evening.'],
  rita: ["I'll look at it. Looking costs you nothing."],
  wayne: ['Alright. Buying or selling?'],
  brenda: ['Now then, love. Filleted, or do you want to wrestle it yourself?'],
  lee: ['Alright.'],
  grace: ["Sit down before you fall down. Tea's on."],
  peter: ['Ten minutes for anything hot.'],
  lily: ['Hello. What can I get you?'],
  hal: ["We're between stock."],
  susan: ['Anything to declare?'],
  nora: ["Ah, it's yourself."],
  albert: ["Now then, young 'un."],
  sylvia: ['Feet. Mat. Thank you.'],
  dennis: ["If it's about the eighty quid, I'm out."],
  norman: ["I couldn't say. Sorry. What was it?"],
  julie: ['Hiya.'],
  shaun: ['Mind the ladder.'],
  pc: ['Sir.'],
};
export const FB = {
  nothing: [
    "Nothing you'd mind. Yet.",
    "I've heard nowt worth repeating.",
    'Nobody tells me anything, and I tell them less.',
  ],
  wont: [
    "I don't carry tales to them they're about.",
    'Ask somebody who likes you better.',
    "I've nothing to say on that.",
  ],
  fire: [
    'The fire? I only know what the paper printed. No. 4 went up in the night, five weeks back, and nobody was hurt.',
    'Ask the paper. Or ask that detective, she never stops.',
  ],
  mickey: [
    'Mickey was Mickey. Paid what he owed, most weeks.',
    "He'd have liked the turnout. He'd have counted it.",
  ],
  rivals: [
    "There's Agar with the deeds, the Widow with the dock and Cammack with the noise. I keep clear of all three.",
    "Names like that I don't say on the pavement.",
  ],
  small: [
    "It's been wet since August.",
    'Same as ever. Less of it.',
    'You get used to the quiet. You never get to like it.',
    'Aye, well. There it is.',
  ],
  scared: ['All right. All right. I never saw anything.', "There's no call for that. I'll say nothing."],
  defiant: [
    "You'll have to do better than that.",
    "Don't you speak to me like that.",
    'Is that supposed to frighten me?',
  ],
  take: ['Go on, then. I never saw this.', "That'll do nicely."],
  notake: ['Put that away.', "I don't want your money. I want you to think about why you offered it."],
  flat: ['Save it.', 'Is that right.'],
  flatok: ["Well. That's nice of you to say.", 'Go on with you.'],
  caught: ["I was stood there. Don't tell me what I saw.", "That's a lie, and not a good one."],
  believed: ['If you say so.', "Well, that's as may be."],
  ok: ['Right you are.', 'Fair enough.'],
  no: ['Suit yourself.', "Then that's that."],
  bye: ['Mind how you go.', 'Aye.', 'Ta-ra.'],
  busy: ['Not now.', "I'm busy."],
};
const FBOWN = {
  sheila: {
    nothing: ["If I'd heard it I'd have written it down."],
    small: ["The weather isn't in the book. I only discuss what's in the book."],
    defiant: ["Thirty-one years. I've been threatened by better."],
    notake: ["I count money. I don't take it."],
    flat: ['Save it for the fares.'],
    mickey: ["He was careful. Then he wasn't. That's all there is."],
    fire: ["The fare book shows nothing for that night. I've looked."],
    wont: ['Not yet.'],
  },
  ron: {
    nothing: ["Quiet so far, boss. Quiet's cheap."],
    small: ["Thirty years on the dock, I never minded rain. It's the standing still."],
    defiant: ["Boss. Don't. You'll only hurt your hand."],
    take: ["Now you're talking my language."],
    fire: ['I was on the rank till midnight. The row was dark by one.'],
    rivals: [
      "The Widow pays on the day. Agar never comes down himself. Cammack's lot wear shell suits. That's all you need.",
    ],
  },
  darren: {
    nothing: ["So listen, there's talk, but it's only talk, yeah?"],
    small: ['So listen, you got a minute? No? No. Fair enough.'],
    scared: ['Alright! Alright. I never said nothing to nobody.'],
    take: ["Sound. You won't regret it. Well. You might, but not much."],
    flatok: ["You're alright, you are. I've said so."],
  },
  ada: {
    nothing: ["I see more than I hear. Ask me what I've seen."],
    small: ["Sit a day at this window and you'll not need the wireless."],
    defiant: ["I buried a husband off this street. You don't frighten me, young man."],
    notake: ["Put your money away. I'm not that sort of window."],
    mickey: ['Forty years I knew him. Good to his crew, hard on himself.'],
    fire: ['I saw the sky go orange at two. And a car come down after, no lights.'],
  },
  norman: { fire: ["I was at the far end. I've said. I was at the far end."] },
  albert: {
    fire: ['I smelled paraffin on the wind that night. Before the glow.'],
    mickey: ['Your uncle could find fish in a bath.'],
  },
  alison: {
    fire: ["The insurance on No. 4 went up a month before it burned. That's in print. The rest isn't, yet."],
  },
  susan: { fire: ["There were goods under bond in there. The paperwork doesn't match what burned."] },
  grace: { fire: ['I fed the firemen till four. One of them said it burned too clean.'] },
  peter: { fire: ['We were still up. I rang 999 from the phone box.'] },
  shaun: { fire: ['I painted the 4 on that door. Somebody had it repainted a fortnight before. Not me.'] },
  dennis: { fire: ["I bought iron out of that ruin. Cheap. I don't ask why things are cheap."] },
  terry: { fire: ["I'd a fare to the ferry at one. The other car was out. It wasn't me on the row."] },
  walsh: {
    wont: ["That's not mine to tell."],
    defiant: ["I'll pray for you. I do that for everyone, so don't take it as a remark."],
    notake: ["There's a box by the door for the roof. Not my pocket."],
  },
  ellis: {
    defiant: ["I'll note that you said that."],
    notake: ["I'll note that you offered that."],
    wont: ["I ask the questions, Mr Nowak. It's tidier."],
  },
  pc: { defiant: ["That's an offence, sir."], notake: ["That's an offence, sir."] },
};
// Within one talk nobody says the same line twice; a shared line (FB) is said by one person a day at most and used once a talk;
// when nothing fitting is left, the person closes the talk in their own voice (talk.js then offers only a Leave).
const CLOSE = {
  sheila: "That's all I have for you. The book's waiting.",
  ron: "Right, boss. I'd best watch the rank.",
  darren: "So listen, I've got to be somewhere. See you about, yeah?",
  ada: "That's enough for one sitting. Off you go.",
  june: "I've said what I'm going to say, Mr Nowak.",
  ellis: "That'll be all for now, Mr Nowak.",
  alison: "I've a deadline. Another time.",
  walsh: 'Go in peace. I have the roof to worry about.',
  pauline: "Hang on, love, the radio's going. We'll talk after.",
  kevin: "I've a car in bits. Go on.",
  terry: "That's me, then. I've a fare waiting.",
  rita: "Looking's done. Buy something or let me shut.",
  wayne: "That's me done. Places to be.",
  brenda: "I've fish to see to, love.",
  lee: 'Right. See you.',
  grace: "Drink your tea and let me get on.",
  peter: "Ten minutes is up. Next.",
  lily: "I'd best see to the counter.",
  hal: 'Nothing more in stock, that included.',
  susan: "Nothing further to declare, then.",
  nora: "Away with you now. I've things on.",
  albert: "That's me talked out, young 'un.",
  sylvia: 'Feet. Mat. Door. Thank you.',
  dennis: "That's me. I've iron to shift.",
  norman: "I couldn't say more. Sorry.",
  julie: 'Anyway. See you.',
  shaun: "I'd best get back up the ladder.",
  pc: "I'll be on my way, sir.",
};
const SHARED = new Set(Object.values(FB).flat());
export const FBT = { used: new Set(), shared: false, closed: false, day: -1, sharedBy: new Map() };
export function fbReset() {
  FBT.used = new Set();
  FBT.shared = false;
  FBT.closed = false;
}
export function fbNote(line) {
  if (line) FBT.used.add(line);
}
export function fb(P, key) {
  const o = FBOWN[P.id],
    r = R.f(); // one draw, as before, so the seeded week keeps its course
  const d = day();
  if (FBT.day !== d) {
    FBT.day = d;
    FBT.sharedBy = new Map();
  }
  const own = (o && o[key] ? o[key] : []).filter((x) => !FBT.used.has(x));
  let line = null;
  if (own.length) line = own[Math.floor(r * own.length) % own.length];
  else if (!FBT.shared) {
    const pool = (FB[key] || FB.ok).filter((x) => {
      const by = FBT.sharedBy.get(x);
      return !FBT.used.has(x) && (!by || by === P.id);
    });
    if (pool.length) {
      line = pool[Math.floor(r * pool.length) % pool.length];
      FBT.shared = true;
      FBT.sharedBy.set(line, P.id);
    }
  }
  if (!line) {
    line = CLOSE[P.id] || (P.def.sex === 'f' ? "Anyway, love. I'd best get on." : "Anyway. I'd best get on.");
    FBT.closed = true;
  }
  FBT.used.add(line);
  return line;
}
export const isSharedLine = (x) => SHARED.has(x);
// Greetings follow the hour: a "Morning." at night or an "Evening." at breakfast is put right.
function timely(s) {
  const h = hour(),
    w =
      h >= TALKING.eveningGreetingUntilHour && h < TALKING.morningUntilHour
        ? 'Morning'
        : h >= TALKING.morningUntilHour && h < TALKING.afternoonUntilHour
          ? 'Afternoon'
          : 'Evening';
  return s.replace(/\b(Morning|Afternoon|Evening)\b/g, w);
}
export function greet(P) {
  return timely(pick(GREET[P.id] || ['Aye?']));
}

// Things overheard when two people are talking and it is not about Tom. key marks the Ledger note.
export const OVERHEARD = [
  {
    k: 'agar',
    s: "Agar's clerk was round about the lease again. Never the man himself.",
    n: 'Geoffrey Agar, solicitor and alderman, holds the lease on the parade. He sends a clerk. Nobody sees him.',
  },
  {
    k: 'agar2',
    s: 'Alderman Agar opened the new car park. Had his picture took.',
    n: 'Agar is an alderman. He likes his name read out.',
  },
  {
    k: 'widow',
    s: "The Widow paid out on the day, I'll say that for her.",
    n: 'Maureen Jensen, "the Widow", runs the fish dock. She pays on the day.',
  },
  {
    k: 'widow2',
    s: "Maureen Jensen's put the ice up again. Who's going to tell her no?",
    n: 'The Widow sets the price of ice on the dock and nobody argues.',
  },
  {
    k: 'cammack',
    s: "Cammack's lot had a stereo going on Copper Row till one. Nobody rang anybody.",
    n: "Danny Cammack's crew are loud on Copper Row at night, outside the video shop. Nobody complains.",
  },
  {
    k: 'cammack2',
    s: "Danny Cammack was buying breakfasts for lads who've never done a day's work.",
    n: 'Cammack is buying young lads. Breakfasts first.',
  },
  {
    k: 'garbutt',
    s: 'Garbutt was in. Sat with his back to the wall like always.',
    n: 'Keith Garbutt, "the Fixer", carries messages between the three. Mickey\'s arrangement was his.',
  },
  {
    k: 'fire',
    s: "Five weeks and they still haven't boarded No. 4.",
    n: 'No. 4 on the warehouse row burned five weeks ago. It still stands open.',
  },
  { k: 'docks', s: 'Forty went from our gang in one morning. One morning.', n: null },
  { k: 'docks2', s: "He's not worked since the scheme went. Sits in that caff nursing one tea.", n: null },
  { k: 'm1', s: "I'll have a bit of haddock if it's today's.", n: null },
  { k: 'm2', s: 'She never did. She did!', n: null },
  { k: 'm3', s: 'Bus was twenty minutes late and then two come at once.', n: null },
  { k: 'm4', s: "They've let the old laundry go to ruin. Shame.", n: null },
  { k: 'm5', s: "Rent's up again. I said to him, where's it to come from?", n: null },
  { k: 'm6', s: "Our lass says there's work at the frozen pea place, if you'll do nights.", n: null },
];
export const HEADLINES = [
  'WAREHOUSE FIRE: POLICE FILE "STILL OPEN"',
  'FERRY TIMES TO CHANGE FROM NOVEMBER',
  'DOCK JOBS: NO NEW SCHEME, SAYS BOARD',
  'ALDERMAN AGAR OPENS COPPER ROW CAR PARK',
  'WET WEEK AHEAD FOR HUMBER BANK',
];
export const capSay = cap;
export function describeMem(P, m) {
  // one plain sentence of what this person holds, for the talk prompt and the end screen
  const E = G.ev[m.e],
    k = KINDS[E.kind];
  const how =
    m.src === 'saw'
      ? 'saw it'
      : m.src === 'self'
        ? 'was there'
        : m.src === 'heard'
          ? 'heard a noise'
          : 'was told by ' + (m.from && G.people[m.from] ? G.people[m.from].def.name : 'someone');
  const who = attached(m)
    ? m.who === 'tom'
      ? ''
      : ' (thinks it was the new owner, not certain)'
    : ' (does not know it was Tom: saw only ' +
      ({ coat: 'a man in a long dark coat', man: 'a man', cab: "one of Mickey's cars" }[m.who] || 'a man') +
      ')';
  return `${k.truth(E)}, ${dayOf(E.t)}${who}. [${how}, ${m.sure > TALKING.soundsSureAboveSureness ? 'sure' : m.sure > TALKING.soundsFairlySureAboveSureness ? 'fairly sure' : 'not sure'}]`;
}
