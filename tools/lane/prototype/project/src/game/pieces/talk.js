// LEDGER rule piece: talk. What Tom's typed words are taken to mean; the decision rule (a yes, a no and a line that
// keeps talking; only a plain yes is taken; what cannot be undone asks twice; Leave is always offered); the claim
// check (a character says only what the simulation knows); the memory of lines (nobody says the same line twice in
// a day, no shared line twice in a week on one street); the slow-reply rule. DESIGN section 11; ER-TALK-01 to 07.
// Pure: plain data in, plain data out. The live model never decides anything here (canon: LLMs classify, never
// adjudicate): these rules are the game's own.
import { RULES } from '../../rules.js';
const OLD = RULES.talk;
export const TABLE = Object.assign({}, OLD, RULES.game.econ.talk);

// ---------- what his words are taken to mean ----------
const OFFER = /(for your trouble|make it worth|something for you|take this|here'?s (a|some|the) (little )?(something|money|fiver|tenner|quid)|buy your|i'?ll (give|pay) you|there'?s .{0,12} in it for you|keep the change)/;
const DEMAND = /(you owe|owe (me|the book|mickey)|i'?ve come for|i want (it|the|my|that)|pay (up|me|it)|hand it over|where'?s (my|the) money|on the book|the debt|it'?s the |what'?s owed|how much|fare|rent|cost|price|worth|wages?)/;
const YES = /^(yes|aye|all right|alright|ok|okay|i'?ll do it|fine|agreed|deal|go on then|i will|count me in)\b/;
const NO = /^(no\b|not me|never\b|i won'?t|i'?m not|forget it|leave it|not a chance)/;
// A sum of money alone is not an offer of money: "it's the twenty-two pounds, I want it paid" is a demand, and
// "how much is the rent" is a question. He offers money only when he says he is giving it.
export function intent(text, T = TABLE) {
  const s = String(text || '').toLowerCase().trim();
  let amount = 0;
  const m = s.match(/£\s*(\d+)/) || s.match(/(\d+)\s*(quid|pounds?|nicker)/);
  if (m) amount = +m[1];
  else if (/fiver/.test(s)) amount = T.fiverPounds;
  else if (/tenner/.test(s)) amount = T.tennerPounds;
  const offers = OFFER.test(s),
    demands = DEMAND.test(s),
    asks = /\?$|^(what|who|where|when|why|how|did|do|does|is|are|have|has|can|could|tell me|any)\b/.test(s);
  let kind = 'smalltalk',
    denies = false;
  if (offers && !(demands && !/(for your trouble|make it worth|in it for you|i'?ll (give|pay) you)/.test(s))) kind = 'bribe';
  else if (/(or else|break your|hurt you|you'?ll regret|last warning|i know where you|keep your mouth shut|or i'?ll|watch your back|shut your|i'?ll have you|be a shame if)/.test(s)) kind = 'threaten';
  else if (/(wasn'?t me|i was (at|in) |i was asleep|never (went|left|touched|saw|been)|i didn'?t|not true|you'?re mistaken|must have been someone)/.test(s)) {
    kind = 'lie';
    denies = true;
  } else if (YES.test(s)) kind = 'agree';
  else if (NO.test(s)) kind = 'refuse';
  else if (/(you look|lovely|good job|best .* in|i like your|respect you|kind of you|you'?re a (good|grand|fine))/.test(s)) kind = 'flatter';
  else if (asks) kind = 'ask';
  let topic = 'other';
  if (/(about me|say about|saying about|heard about me|they call me|call me|think of me|know about me|seen me|saw me)/.test(s)) topic = 'me';
  else if (/(fire|warehouse|no\.? ?4|number four|burn)/.test(s)) topic = 'fire';
  else if (/(mickey|my uncle|suddaby)/.test(s)) topic = 'mickey';
  else if (/(agar|widow|jensen|cammack|garbutt|fixer)/.test(s)) topic = 'rivals';
  else if (/(owe|debt|the book|pay up|what'?s owed|slate)/.test(s)) topic = 'debt';
  return { intent: kind, topic, amount: kind === 'bribe' ? amount : 0, sumSpoken: amount, denies };
}

// ---------- the decision rule ----------
// Is this a plain yes? Only then is anything taken. "Yes, but", "yes?" and "yes if" are not plain.
export function plainYes(text) {
  const s = String(text || '').toLowerCase().trim();
  if (!YES.test(s)) return false;
  if (/\?\s*$/.test(s)) return false;
  if (/\b(but|if|unless|maybe|perhaps|depends|not sure|suppose|might|when|once|after|before|except|though)\b/.test(s)) return false;
  if (/\b(no|not|never|won'?t|don'?t|can'?t)\b/.test(s)) return false;
  return true;
}
export function plainNo(text) {
  return NO.test(String(text || '').toLowerCase().trim());
}
// A decision as plain data. spec: { direct, opts: [{ agree, refuse, asksTwice (it has a plain question q before it
// is taken), undoable: false marks what cannot be undone }] }.
// State: { q: index of the option whose plain question stands, or null; asked: how often that question was put }.
// Input: { job: 'prop' (an option's own line was picked), 'yes', 'no', 'keep' (the line that keeps talking),
//          'leave', or 'typed' with text }.
// Output: the new state, the option taken (or null), what the person does next, and whether Leave is offered (always).
export function decisionStart(spec) {
  return { q: spec.direct ? 0 : null, asked: spec.direct ? 1 : 0, done: false };
}
export function decisionStep(spec, state, input) {
  const out = { state: { q: state.q, asked: state.asked, done: state.done }, taken: null, does: 'waits', leaveOffered: true };
  if (state.done) return Object.assign(out, { does: 'nothing: it is decided' });
  let job = input.job,
    idx = input.idx;
  if (job === 'typed') {
    if (state.q != null) job = plainYes(input.text) ? 'yes' : plainNo(input.text) ? 'no' : 'talk';
    else {
      idx = plainYes(input.text) ? spec.opts.findIndex((o) => o.agree) : plainNo(input.text) ? spec.opts.findIndex((o) => o.refuse) : -1;
      job = idx >= 0 ? 'prop' : 'talk';
    }
  }
  if (job === 'leave') return Object.assign(out, { does: 'he leaves: nothing is decided' });
  if (job === 'talk' || job === 'keep') return Object.assign(out, { does: state.q != null ? 'answers, and puts the plain question again' : 'answers' });
  if (job === 'prop') {
    const o = spec.opts[idx];
    if (!o) return Object.assign(out, { does: 'answers' });
    const twice = o.asksTwice || o.undoable === false;
    if (twice) {
      out.state.q = idx;
      out.state.asked = 1;
      return Object.assign(out, { does: 'puts the plain question' });
    }
    out.state.done = true;
    return Object.assign(out, { taken: idx, does: 'takes it' });
  }
  if (job === 'yes') {
    if (state.q == null) return Object.assign(out, { does: 'answers' });
    out.state.done = true;
    out.state.q = null;
    return Object.assign(out, { taken: state.q, does: 'takes it' });
  }
  if (job === 'no') {
    out.state.q = null;
    out.state.asked = 0;
    if (spec.direct) out.state.done = true;
    return Object.assign(out, { does: spec.direct ? 'drops the matter' : 'lets it stand: a no decides nothing' });
  }
  return Object.assign(out, { does: 'answers' });
}
// Is a decision's data sound? Every option that cannot be undone asks twice; there is a way to say no; nothing is
// taken by a single press unless it can be undone.
export function decisionSound(spec) {
  const faults = [];
  if (!spec.opts || !spec.opts.length) faults.push('no options');
  (spec.opts || []).forEach((o, i) => {
    if (o.undoable === false && !o.asksTwice) faults.push('option ' + i + ' cannot be undone and does not ask twice');
  });
  return { ok: !faults.length, faults };
}

// ---------- the claim check ----------
// A reply may name only people the speaker knows, may accuse Tom only of what the speaker holds a memory of, and
// may use no word the content rule or the year forbids. known: { people: [names the speaker may say],
// allNames: [every name in the town], deeds: [words for what the speaker holds about Tom], holdsAnything: bool }.
const FORBIDDEN = /\b(beer|lager|pint|pints|whisky|whiskey|vodka|gin|drunk|drunken|booze|pub crawl|bet|bets|betting|bookie|bookies|bookmaker|gamble|gambling|casino|kid|kids|child|children|schoolboy|schoolgirl|toddler|baby|mobile phone|smartphone|internet|website|email|e-mail|text message|texted|google|online|wifi|cctv app|selfie|euro|euros)\b/i;
const ACCUSE = /\b(i saw you|saw you|seen you|you were (seen|at|in|on|by)|i heard you|they say you|everyone knows you|i know what you did|you did|you hit|you took|you broke|you carried|you ran)\b/i;
export function claimCheck(reply, known) {
  const text = String(reply || '');
  const bad = text.match(FORBIDDEN);
  if (bad) return { ok: false, why: 'a word the content rule or the year forbids: ' + bad[0].toLowerCase() };
  const may = new Set((known.people || []).map((n) => n.toLowerCase()));
  for (const name of known.allNames || []) {
    const first = name.split(' ')[0],
      last = name.split(' ').slice(-1)[0];
    for (const n of [name, first, last]) {
      if (n.length < 3) continue; // never match on a scrap of a name
      if (new RegExp('\\b' + n.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '\\b', 'i').test(text) && !may.has(name.toLowerCase())) return { ok: false, why: 'names somebody the speaker does not know: ' + name };
    }
  }
  if (ACCUSE.test(text)) {
    if (!known.holdsAnything) return { ok: false, why: 'says something of Tom the speaker holds no memory of' };
    const deeds = (known.deeds || []).map((d) => d.toLowerCase());
    const verb = (text.match(/\byou (hit|took|broke|carried|ran)\b/i) || [])[1];
    if (verb && deeds.length && !deeds.some((d) => d.includes(verb.toLowerCase()))) return { ok: false, why: 'accuses him of a deed the speaker does not hold: ' + verb.toLowerCase() };
  }
  return { ok: true, why: '' };
}

// ---------- the memory of lines ----------
// heard: { own: { personId: { line: dayIndex } }, st: { street: { line: dayIndex } } }.
export function lineAllowed(heard, line, personId, street, dayIndex, shared, T = TABLE) {
  if (shared) {
    const last = ((heard.st || {})[street] || {})[line];
    return last == null || dayIndex - last >= T.sharedLineAgainAfterDays;
  }
  const last = ((heard.own || {})[personId] || {})[line];
  return last == null || dayIndex - last >= T.ownLineAgainAfterDays;
}
export function lineSaid(heard, line, personId, street, dayIndex, shared) {
  const h = { own: Object.assign({}, heard.own), st: Object.assign({}, heard.st) };
  if (shared) h.st[street] = Object.assign({}, h.st[street], { [line]: dayIndex });
  else h.own[personId] = Object.assign({}, h.own[personId], { [line]: dayIndex });
  return h;
}
// The first line of a list that may be said now, or null: then the person closes the talk in their own voice.
export function nextLine(heard, lines, personId, street, dayIndex, shared, T = TABLE) {
  for (const l of lines) if (lineAllowed(heard, l, personId, street, dayIndex, shared, T)) return l;
  return null;
}

// ---------- slow replies, long scenes, reports ----------
// ER-TALK-01: a live reply that has begun within two seconds is heard; later than that the written line plays; a
// reply that has begun but is not whole after eight seconds is dropped with an in-character brush-off.
export function replyRule(beganAfterSeconds, wholeAfterSeconds, T = TABLE) {
  if (beganAfterSeconds == null || beganAfterSeconds > T.liveReplyHeardWithinRealSeconds) return { plays: 'written', sign: true };
  if (wholeAfterSeconds == null || wholeAfterSeconds > T.liveReplyDroppedAfterRealSeconds) return { plays: 'brush-off', sign: true };
  return { plays: 'live', sign: false };
}
// ER-TALK-06: no talk scene runs sixty seconds without a choice or control.
export function sceneTooLong(secondsSinceChoiceOrControl, T = TABLE) {
  return secondsSinceChoiceOrControl > T.sceneWithoutChoiceRealSecondsAtMost;
}
// ER-TALK-07: a report of a line. Returns the list with the report added (the newest kept, the oldest dropped).
export function report(list, r, T = TABLE) {
  if (!r || !r.line || !String(r.line).trim()) return { list, ok: false, why: 'no line to report' };
  const row = { line: String(r.line).slice(0, 400), who: r.who || 'someone', minute: Math.round(r.minute || 0), from: r.from === 'pause' ? 'pause' : 'talk', live: !!r.live, why: String(r.why || '').slice(0, 200) };
  return { list: (list || []).concat([row]).slice(-T.reportKeepsLines), ok: true, why: '' };
}
// ER-SPEAK-01: can this talk state be played through by a pad alone? There must be a line to pick or Leave.
export function padCanAct(lines, leaveOffered) {
  return (lines || []).length > 0 || !!leaveOffered;
}

export const PIECE = {
  name: 'talk',
  fns: { intent, plainYes, plainNo, decisionStart, decisionStep, decisionSound, claimCheck, lineAllowed, lineSaid, nextLine, replyRule, sceneTooLong, report, padCanAct },
};
