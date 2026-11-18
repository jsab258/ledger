// Live talk. The model only voices the line and names the intent; the game's rules decide what happens.
import { tabPressed, talkEnded } from './measures.js';
import { G, hour, day } from './state.js';
import { clamp, hhmm, DAYS, money } from './util.js';
import { KINDS } from './kinds.js';
import { act, logLine } from './events.js';
import { attached } from './seeing.js';
import { comeback, markSaid, menaceTo, callName } from './gossip.js';
import { meet, heardCall, ledgerSeen, note, knownNames, heardNames, hearName } from './ledger.js';
import { comebackLine, describeMem, greet, fb, vocative, fbReset, FBT } from './talk_lines.js';
import { NAME_ONLY } from './cast.js';
import {
  openTalk,
  closeTalk,
  talkLine,
  talkBusy,
  setTalkLines,
  setTalkSlip,
  talkHead,
  tomName,
  ui,
  saveSettings,
  after,
} from './ui.js';
import { slipHTML, tomKnows } from './ledger_screen.js';
import { RULES as NUMBERS } from './rules.js';
const TALKING = NUMBERS.talk;

const T = {
  sample: null,
  ready: false,
  consent: false,
  P: null,
  hist: [],
  busy: false,
  ctl: null,
  lines: [],
  used: new Set(),
  sug: { seq: 0 },
  raised: new Set(),
};
export const RULES = `ABSOLUTE CONTENT RULES for everything you write:
- No alcohol and no gambling, ever: never shown, served, drunk or mentioned. A pub is only a building.
- Tobacco is fine.
- No children at all: never mention children, pupils, babies or anyone under 18. Everyone in this town is an adult.
- No sexual content. Mild seaside-postcard innuendo at most.
- Drugs are never named, shown or offered.
- Period swearing is fine. No slurs of any kind. No racism or sectarianism voiced.
- Religion is part of life and never mocked.
- Violence may be spoken of plainly, never dwelt on as spectacle.
- Every brand, product and business is fictional. No real people.
- It is October 1990 in northern England: landlines, phone boxes, pagers, cash and paper. No mobile phones, no internet, nothing from the 1950s or 1970s, nothing American.`;
const INTENTS = ['ask', 'smalltalk', 'threaten', 'bribe', 'flatter', 'lie', 'refuse', 'agree'];
const BANNED =
  /\b(pint|beer|lager|whisky|whiskey|vodka|brandy|wine|booze|boozer|drunk|hangover|betting|bookie|bookies|gamble|gambling|the horses|casino|child|children|kiddies|toddler|baby|babies|schoolboy|schoolgirl|pupil|heroin|cocaine|cannabis|internet|mobile phone|email)\b/i;

export async function initTalk() {
  ui.hooks.talkKey = talkKey;
  ui.hooks.talkPick = pick;
  G.hooks.nameLearned = () => talkHead();
  try {
    if (window.claude && window.claude.use) {
      T.sample = await window.claude.use('sample');
    }
  } catch (e) {
    T.sample = null;
  }
  T.ready = true;
}
export const talkAvailable = () => !!T.sample && !T.dead && G.settings.liveTalk !== false;
function timed(fn, ms) {
  // a call that falls back rather than stall the game
  const ctl = new AbortController();
  T.ctl = ctl;
  let to = null;
  const p = fn(ctl.signal);
  if (ms) to = setTimeout(() => ctl.abort(), ms);
  return p.finally(() => clearTimeout(to));
}
function localIntent(text) {
  const s = text.toLowerCase().trim();
  let amount = 0;
  const m = s.match(/£\s*(\d+)/) || s.match(/(\d+)\s*(quid|pounds?|nicker)/);
  if (m) amount = +m[1];
  else if (/fiver/.test(s)) amount = TALKING.fiverPounds;
  else if (/tenner/.test(s)) amount = TALKING.tennerPounds;
  let intent = 'smalltalk',
    denies = false;
  if (
    amount ||
    /(for your trouble|make it worth|something for you|take this|here'?s (a|some) (little )?(something|money)|buy your)/.test(
      s,
    )
  )
    intent = 'bribe';
  else if (
    /(or else|break your|hurt you|you'?ll regret|last warning|i know where you|keep your mouth shut|or i'?ll|watch your back|shut your|i'?ll have you|be a shame if)/.test(
      s,
    )
  )
    intent = 'threaten';
  else if (
    /(wasn'?t me|i was (at|in) |i was asleep|never (went|left|touched|saw|been)|i didn'?t|not true|you'?re mistaken|must have been someone)/.test(
      s,
    )
  ) {
    intent = 'lie';
    denies = true;
  } else if (
    /^(yes|aye|all right|alright|ok|okay|i'?ll do it|fine|agreed|deal|go on then|i will|count me in)\b/.test(
      s,
    )
  )
    intent = 'agree';
  else if (/^(no\b|not me|never\b|i won'?t|i'?m not|forget it|leave it|not a chance)/.test(s))
    intent = 'refuse';
  else if (
    /(you look|lovely|good job|best .* in|i like your|respect you|kind of you|you'?re a (good|grand|fine))/.test(
      s,
    )
  )
    intent = 'flatter';
  else if (/\?$|^(what|who|where|when|why|how|did|do|does|is|are|have|has|can|could|tell me|any)\b/.test(s))
    intent = 'ask';
  let topic = 'other';
  if (
    /(about me|say about|saying about|heard about me|they call me|call me|think of me|know about me|seen me|saw me)/.test(
      s,
    )
  )
    topic = 'me';
  else if (/(fire|warehouse|no\.? ?4|number four|burn)/.test(s)) topic = 'fire';
  else if (/(mickey|my uncle|suddaby)/.test(s)) topic = 'mickey';
  else if (/(agar|widow|jensen|cammack|garbutt|fixer)/.test(s)) topic = 'rivals';
  else if (/(owe|debt|the book|pay up|what'?s owed|slate)/.test(s)) topic = 'debt';
  return { intent, topic, amount, denies };
}
async function classify(P, text, pending) {
  const loc = localIntent(text);
  if (!talkAvailable()) return loc;
  const prompt = `Classify one line a player typed to a character in a text-driven crime game set in England in 1990. The player is Tom, a cab office owner.
Reply with only JSON like {"intent":"ask","topic":"me","amount":0,"denies":false}.
intent is exactly one of: ask (asks a question), smalltalk (greeting or chat), threaten (menaces the character), bribe (offers money or a favour for something), flatter (praise meant to please), lie (denies or gives an account of his own actions, such as an alibi), refuse (says no to what was asked of him), agree (says yes to what was asked of him).
topic is one of: me (what people know, say or call Tom), fire (the warehouse fire), mickey (his dead uncle Mickey), rivals (Agar, the Widow Jensen, Cammack, Garbutt), debt (money owed), person (asks about another named person), other.
amount is the number of pounds he offers, or 0. denies is true if he denies having done something.
${pending ? 'The character has just asked him: "' + pending + '"\n' : ''}Player typed: ${JSON.stringify(text)}`;
  try {
    const r = await timed(
      (signal) => T.sample.json(prompt, { modelTier: 'quick', signal }),
      T.consent ? TALKING.sortingWaitsRealMilliseconds : 0,
    );
    T.consent = true;
    if (r && INTENTS.includes(r.intent))
      return {
        live: true,
        intent: r.intent,
        topic: ['me', 'fire', 'mickey', 'rivals', 'debt', 'person', 'other'].includes(r.topic)
          ? r.topic
          : loc.topic,
        amount: Math.max(0, Math.min(TALKING.offerAtMostPounds, +r.amount || loc.amount || 0)),
        denies: !!r.denies,
      };
  } catch (e) {
    noteFail(e);
  }
  return loc;
}
function noteFail(e) {
  const c = e && e.code;
  if (
    [
      'not_granted',
      'sampling_disabled',
      'not_declared',
      'capability_disabled',
      'capability_removed',
      'session_expired',
    ].includes(c)
  ) {
    T.dead = true;
    T.why = c;
    if (T.P)
      talkLine('sys', 'The live voices are not available here. People will answer in their written lines.');
  } else if (c === 'rate_limited') {
    T.cool = Date.now() + TALKING.liveVoiceRestsAfterLimitRealMilliseconds;
  }
}

function feeling(P) {
  const m = P.mind,
    a = [];
  a.push(
    m.regard > TALKING.feelsWarmAboveRegard
      ? 'You have warmed to him.'
      : m.regard > TALKING.feelsAllRightAboveRegard
        ? 'You think he might be all right.'
        : m.regard < -TALKING.feelsDistrustBelowMinusRegard
          ? 'You dislike and distrust him.'
          : m.regard < -TALKING.feelsCoolBelowMinusRegard
            ? 'You have cooled on him and are wary.'
            : 'You have not made your mind up about him.',
  );
  if (m.fear > TALKING.frightenedAboveFear) a.push('He frightens you.');
  else if (m.fear > TALKING.uneasyAboveFear) a.push('He makes you uneasy.');
  return a.join(' ');
}
function prompt(P, directive, text) {
  const c = P.def.card,
    mems = P.mind.mem
      .filter((m) => G.ev[m.e].kind !== 'inherit')
      .sort((a, b) => b.heat - a.heat)
      .slice(0, TALKING.remembersForATalkAtMost);
  const name = callName(P),
    v = vocative(P);
  const facts = mems.length
    ? mems.map((m) => '- ' + describeMem(P, m)).join('\n')
    : '- Nothing in particular.';
  const hist = T.hist
    .slice(-TALKING.pastTurnsGivenToTheVoice)
    .map((h) => (h.role === 'user' ? 'Tom: ' : P.def.name + ': ') + h.content)
    .join('\n');
  return `You are voicing one character in LEDGER, a grounded British noir game set in Meridian, a fictional port town on the Humber, in October 1990. The docks are dying and nobody has money. Reply with ONLY the words the character says aloud: one to three short spoken sentences. No narration, no stage directions, no quotation marks, no asterisks, no dashes, no lists. Dry northern English understatement, never American.

${RULES}

CHARACTER: ${P.def.name}, ${P.def.age}. ${c.who}
HOW THEY SPEAK: ${c.speak} Lines they have said: ${c.lines.map((l) => '"' + l + '"').join(' ')}
THEIR LIFE: ${c.life}
WHAT THEY KNOW OF THE WAREHOUSE FIRE: ${c.fire}
WHAT THEY KNOW OF THE NAMES IN TOWN: ${c.rivals} (${Object.values(NAME_ONLY).join('; ')}.)
${c.secret ? 'WHAT THEY KNOW BUT WILL NOT TELL HIM: ' + c.secret + '\n' : ''}
WHO THEY ARE TALKING TO: Tom Nowak, 32, nephew of the late Mickey Suddaby, who has inherited Mickey's Cars, the minicab office on Quay Street. Nobody knows anything of his life before and nobody asks.
${!P.mind.inh && P.mind.fam < TALKING.strangerBelowFamiliarity ? 'They do not know who he is yet: to them he is a stranger.' : `They ${name ? 'call him "' + name + '"' : 'do not use a name for him yet'}${v ? ' and may address him as "' + v + '"' : ''}.`}
${feeling(P)}
NOW: ${DAYS[day() % 7]}, ${hhmm(hour())}, ${G.weather.rain > TALKING.saysRainingAboveRain ? 'raining' : G.weather.rain > TALKING.saysDrizzleAboveRain ? 'drizzle' : 'dry and overcast'}, at ${G.tom.space === 'street' ? G.tom.zone : ui.roomName || 'indoors'}.

ALL THEY KNOW ABOUT TOM'S DOINGS (nothing else has happened; they must never invent events about him; asked about anything not listed, they say in character that they do not know):
${facts}

THE GAME HAS ALREADY DECIDED WHAT HAPPENS IN THIS LINE. Voice exactly this outcome: ${directive}
${hist ? '\nSo far:\n' + hist + '\n' : ''}
Tom says: ${JSON.stringify(text)}
${P.def.name} replies:`;
}
function clean(s) {
  s = String(s || '')
    .replace(/[*_"“”]/g, '')
    .replace(/\s*[—–]\s*/g, ', ')
    .replace(/\([^)]*\)/g, '')
    .replace(/^\s*[\w .']{2,24}:\s*/, '')
    .replace(/\s+/g, ' ')
    .trim();
  const parts = s.match(/[^.!?]+[.!?]+/g);
  if (parts && parts.length > TALKING.replySentencesAtMost)
    s = parts.slice(0, TALKING.replySentencesAtMost).join('').trim();
  return s.slice(0, TALKING.replyCharactersAtMost);
}
// One spoken line from the model, cleaned. Null if it broke a content rule.
async function sampleLine(P, directive, text, onText) {
  const r = await timed(
    (signal) =>
      T.sample(prompt(P, directive, text), {
        modelTier: 'quick',
        cache: false,
        signal,
        onText: ({ text: tx }) => {
          const c = clean(tx);
          onText(BANNED.test(c) ? '' : c);
        },
      }),
    T.consent ? TALKING.replyWaitsRealMilliseconds : 0,
  );
  T.consent = true;
  const out = clean(r && r.text);
  return out && !BANNED.test(out) ? out : null;
}
async function voice(P, res, text) {
  const cool = T.cool && Date.now() < T.cool;
  if (talkAvailable() && !cool) {
    const p = talkLine('npc', '...');
    try {
      const out = await sampleLine(P, res.directive, text, (tx) => {
        p.textContent = tx || '...';
      });
      if (out) {
        p.textContent = out;
        G.stats.live++;
        return out;
      }
    } catch (e) {
      noteFail(e);
    }
    p.remove();
  }
  G.stats.fallback++;
  const line = res.say || fb(P, res.fb || 'ok');
  talkLine('npc', line);
  return line;
}
// Settings: ask one real question through the same road as a street conversation, and say plainly whether it worked.
export async function checkTalk(show) {
  if (T.busy || T.P) return;
  T.busy = true;
  try {
    if (!T.sample && window.claude && window.claude.use) {
      try {
        T.sample = await window.claude.use('sample');
      } catch (e) {
        T.sample = null;
      }
    }
    if (!T.sample)
      return show(
        'off',
        'Not available in this view. People answer in their written lines; everything else in the game works the same.',
      );
    if (G.settings.liveTalk === false)
      return show('off', 'Switched off above. People answer in their written lines.');
    const P = G.people.sheila,
      text = 'Morning. Is there anything I ought to know about this street?';
    T.dead = false;
    T.why = null;
    T.cool = 0;
    show('wait', 'Asking Sheila Dunn one question. The first time, Claude may ask your permission.');
    const it = await classify(P, text, null);
    if (T.dead)
      return show(
        'off',
        'Claude was not allowed to answer here (' + T.why + '). People answer in their written lines.',
      );
    const out = await sampleLine(
      P,
      'Answer briefly from your own life and knowledge given above. If you do not know, say so in character.',
      text,
      (tx) => {
        if (tx) show('wait', 'Sheila Dunn: ' + tx);
      },
    );
    if (out)
      return show(
        'on',
        'Working. Your line was read as "' +
          it.intent +
          '"' +
          (it.live ? '' : ' (by the built-in rules, the reader did not answer)') +
          '. Sheila Dunn: ' +
          out,
      );
    show(
      'off',
      'An answer came back but broke a content rule and was thrown away. In play a written line is used instead. Try once more.',
    );
  } catch (e) {
    noteFail(e);
    const c = e && e.code;
    show(
      'off',
      c === 'rate_limited'
        ? 'Claude is busy just now. Try again in a minute; written lines are used meanwhile.'
        : c === 'not_granted'
          ? 'Permission was not given, so people answer in their written lines. Press the button again to be asked once more.'
          : 'No answer came back' + (c ? ' (' + c + ')' : '') + '. People answer in their written lines.',
    );
  } finally {
    T.busy = false;
    T.ctl = null;
  }
}

// ---------- the rules ----------
function spend(pence) {
  // dirty money first, then pocket
  const m = G.money;
  if (m.clean + m.dirty < pence) return false;
  const d = Math.min(m.dirty, pence);
  m.dirty -= d;
  m.clean -= pence - d;
  m.spent += pence;
  return true;
}
function bestMem(P, pred) {
  let b = null;
  for (const m of P.mind.mem) {
    if (!attached(m) || G.ev[m.e].kind === 'inherit' || KINDS[G.ev[m.e].kind].priv) continue;
    if (pred && !pred(m)) continue;
    if (!b || m.heat > b.heat) b = m;
  }
  return b;
}
function decide(P, it, text) {
  const m = P.mind,
    d = P.def;
  const hook = G.hooks.pending && G.hooks.pending(P, it, text);
  if (hook) return hook;
  switch (it.intent) {
    case 'ask': {
      if (it.topic === 'me') {
        if (
          m.regard > -TALKING.tellsAboutHimAboveMinusRegard ||
          m.fear > TALKING.tellsAboutHimAboveFear ||
          m.bought
        ) {
          const mm = bestMem(P);
          if (mm) {
            const E = G.ev[mm.e],
              line = comebackLine(P, mm),
              tellSrc =
                mm.src === 'told' &&
                mm.from &&
                mm.from !== 'someone' &&
                (m.regard > TALKING.namesTheSourceAboveRegard || m.bought);
            mm.said = true;
            ledgerSeen(E, P, 'asked', tellSrc ? mm.from : null);
            return {
              say: line,
              directive: `Tell him plainly the one thing you know about him: ${describeMem(P, mm)} ${tellSrc ? 'You may say it was ' + G.people[mm.from].def.name + ' who told you.' : 'Do not say who told you.'}`,
            };
          }
          return {
            fb: 'nothing',
            directive: 'You have heard nothing about him worth repeating, and say so in character.',
          };
        }
        return {
          fb: 'wont',
          directive: 'You will not carry tales to the man they are about. Refuse, in character.',
        };
      }
      if (it.topic === 'fire') {
        if (!m.askedFire) {
          m.askedFire = 1;
          act('asked_fire', { target: P.id });
          note(`On the fire: ${d.card.fire}`, 'fire', 'fire:' + P.id, { who: P.id, how: sayer(P) });
        }
        return {
          fb: 'fire',
          directive: 'Answer from what you know of the warehouse fire, given above, and nothing beyond it.',
        };
      }
      if (it.topic === 'mickey')
        return {
          fb: 'mickey',
          directive:
            'Say something true to your character about Mickey Suddaby, from your own life given above.',
        };
      if (it.topic === 'rivals') {
        note(`On the names: ${d.card.rivals}`, 'rival', 'riv:' + P.id, { who: P.id, how: sayer(P) });
        return {
          fb: 'rivals',
          directive:
            'Answer from what you know of the names in town, given above. Be guarded; these are dangerous people to discuss.',
        };
      }
      if (it.topic === 'debt' && G.debts[P.id] && G.debts[P.id].st === 'open')
        return {
          fb: 'no',
          directive: `You owe Mickey's book ${money(G.debts[P.id].owed)}. You cannot or will not pay today. Deflect, in character.`,
        };
      return {
        fb: 'small',
        directive:
          'Answer briefly from your own life and knowledge given above. If you do not know, say so in character.',
      };
    }
    case 'threaten': {
      if (d.police) {
        G.story.flags.threatPolice = (G.story.flags.threatPolice || 0) + 1;
        return {
          fb: 'defiant',
          directive: 'He has threatened a police officer. You note it, coldly and exactly.',
        };
      }
      act('threat', { target: P.id, noiseR: TALKING.spokenThreatNoiseCarriesMetres });
      const pressure =
        TALKING.spokenThreatPressure +
        menaceTo(P) +
        (G.tom.armed ? TALKING.spokenThreatPressureAddedWhenArmed : 0);
      if (pressure > d.nerve) {
        m.fear = clamp(m.fear + TALKING.fearAddedWhenAThreatWorks, 0, 1);
        m.regard = clamp(m.regard - TALKING.regardLostWhenAThreatWorks, -1, 1);
        return {
          fb: 'scared',
          directive:
            'This threat frightens you. You back down. You will say nothing to the police, though you cannot promise what the street says.',
        };
      }
      m.regard = clamp(m.regard - TALKING.regardLostWhenAThreatFails, -1, 1);
      m.fear = clamp(m.fear + TALKING.fearAddedWhenAThreatFails, 0, 1);
      return {
        fb: 'defiant',
        directive: 'You are not frightened by this threat. Answer with contempt or cold calm, in character.',
      };
    }
    case 'bribe': {
      const p = Math.round((it.amount || TALKING.bribeAssumedPounds) * 100);
      if (G.money.clean + G.money.dirty < p)
        return {
          fb: 'flat',
          directive: 'He offers money he plainly has not got on him. React, in character.',
        };
      if ((d.venal ?? TALKING.venalAssumed) >= TALKING.takesMoneyFromVenal && !d.police) {
        spend(p);
        m.regard = clamp(m.regard + TALKING.regardAddedWhenBought, -1, 1);
        m.bought = true;
        act('paid_info', { target: P.id });
        const extra = G.hooks.bought ? G.hooks.bought(P, p) : null;
        return {
          fb: 'take',
          say: extra,
          directive:
            'You take his money. You are better disposed to him now and will keep quiet with the police.' +
            (extra ? ' Then tell him this, in your own words: ' + extra : ''),
        };
      }
      m.regard = clamp(m.regard - TALKING.regardLostWhenABribeIsRefused, -1, 1);
      act('bribe_try', { target: P.id });
      if (d.police) G.story.flags.bribePolice = 1;
      return {
        fb: 'notake',
        directive: 'You refuse his money. You are offended, or coldly amused, according to your character.',
      };
    }
    case 'flatter': {
      const soft =
        (d.talk ?? TALKING.talkativeAssumed) > TALKING.flatteryWorksAboveTalkative &&
        d.voice !== 'dry' &&
        d.voice !== 'official';
      if (soft) m.regard = clamp(m.regard + TALKING.regardAddedByFlattery, -1, 1);
      return {
        fb: soft ? 'flatok' : 'flat',
        directive: soft
          ? 'You are a little pleased by the compliment, and show it in character.'
          : 'Flattery does not work on you. Brush it off drily.',
      };
    }
    case 'lie': {
      const mm = bestMem(P, (x) => KINDS[G.ev[x.e].kind].val < 0);
      if (mm && (mm.src === 'saw' || mm.src === 'self') && mm.sure > TALKING.knowsALieAboveSureness) {
        m.regard = clamp(m.regard - TALKING.regardLostWhenCaughtLying, -1, 1);
        act('lied', { target: P.id, silent: true });
        return {
          fb: 'caught',
          directive: `You saw this yourself: ${describeMem(P, mm)} You know he is lying to your face, and you say so.`,
        };
      }
      if (mm) {
        mm.sure *= TALKING.denialCutsSurenessTimes;
        mm.heat *= TALKING.denialCutsHeatTimes;
        return {
          fb: 'believed',
          directive: 'You only had it second hand. You half accept what he says, without warmth.',
        };
      }
      return {
        fb: 'believed',
        directive: 'You have no reason to doubt him and no great interest. Accept it lightly.',
      };
    }
    case 'agree':
      return { fb: 'ok', directive: 'He has agreed with you. Acknowledge it briefly, in character.' };
    case 'refuse':
      return { fb: 'no', directive: 'He has said no. Acknowledge it briefly, in character.' };
    default: {
      if ((m.chatDay || -1) !== day()) {
        m.chatDay = day();
        m.fam = clamp(m.fam + TALKING.familiarityAddedPerDayOfTalk, 0, 1);
        m.regard = clamp(m.regard + TALKING.regardAddedPerDayOfTalk, -1, 1);
      }
      return { fb: 'small', directive: 'Make brief small talk, in character.' };
    }
  }
}

// ---------- Tom's suggested lines, and the game's decisions ----------
// His exact words, three at most, always in the same order of jobs: about what was just said, something personal, a line that leaves.
// Hellos, goodbyes and every line that decides something are the game's own. The follow-up is the model's only, written in a call
// of its own that sees what Tom knows and nothing else; it is left out when live voices are off, slow or wrong.
// "Ron says", or "He says" while Tom has no name for him
const sayer = (P) =>
  (knownNames()[P.id] ? P.def.name.split(' ')[0] : P.def.sex === 'f' ? 'She' : 'He') + ' says';
const GREETS = [
  'Hello. Have you got a minute?',
  'Sorry to bother you.',
  'All right? Can I have a word?',
  'Hello there.',
  'Mind if I stop a minute?',
  'Hello. Is now a good time?',
];
const LEAVES = [
  "I'll let you get on.",
  "I won't keep you.",
  "Right. I'd best be off.",
  "I'll leave you to it.",
  'Another time, then.',
  "I won't stop, then.",
  "I'll not hold you up.",
];
const PERSONAL = [
  'Have you always lived round here?',
  'What was Mickey like?',
  "Where's good for a cup of tea round here?",
  'What do you make of the street these days?',
  "I'm still finding my feet here.",
  "It's all new to me, this.",
  'What do people do round here of a Sunday?',
  'Who should I get to know round here?',
  'Do you get many strangers down here?',
  "What's the best thing about this street?",
];
const BYES = [
  'Right you are.',
  'Mind how you go.',
  'Aye. Go on, then.',
  'Ta-ra, then.',
  'See you about.',
  'Go careful.',
];
const SHY = { wayne: 1, lee: 1, dennis: 1, rita: 1 }; // these keep their names to themselves the first time
const DEAL =
  /(\bi'?ll (do|take|pay|carry|fetch|see him|have)\b|\bi will\b|\bcount me\b|\bdeal\b|\bagreed\b|\bhere'?s\b|£|\b\d+\s*(quid|pounds?|pence|p)\b|\bfiver\b|\btenner\b|\bpay you\b|\bstrike it\b|\bwind it\b|\btak(e|ing) it (on|over)\b|\btell them\b)/i;
const st = (n) => {
  G.stats[n] = (G.stats[n] || 0) + 1;
};
function reset(P) {
  T.P = P;
  fbReset();
  T.hist = [];
  T.used = new Set();
  T.lines = [];
  T.open = false;
  T.sel = 0;
  T.said = 0;
  T.turn = 0;
  T.dec = null;
  T.first = null;
  T.news = false;
  T.raised = new Set();
  T.sug = { seq: (T.sug ? T.sug.seq : 0) + 1, follow: null, personal: null };
  T.slip = !!G.settings.slipOpen; // starts folded to its heading; F2 unfolds it, and the last choice is remembered
  T.slipSeen = T.slip;
  P.sugN = (P.sugN || 0) + 1;
}
const unused = (arr, off = 0) => {
  for (let k = 0; k < arr.length; k++) {
    const x = arr[(k + off) % arr.length];
    if (!T.used.has(x)) return x;
  }
  return null;
};
function buildLines() {
  const P = T.P;
  if (!P) return;
  const L = [],
    D = T.dec,
    n = (P.sugN || 0) * 3 + [...P.id].reduce((x, c) => x + c.charCodeAt(0), 0); // each person, and each visit, starts the written lines at a different place
  if (D) {
    if (D.q != null) {
      const o = D.opts[D.q];
      for (const job of ['yes', 'no', 'keep']) {
        const x = o[job] && unused(o[job]);
        if (x) L.push({ job, text: x });
      }
    } else {
      D.opts.forEach((o, i) => {
        if (L.length < TALKING.suggestedLinesAtMost && o.say) {
          const x = unused(o.say);
          if (x) L.push({ job: 'prop', i, text: x });
        }
      });
      if (L.length < TALKING.suggestedLinesAtMost && D.keep) {
        const x = unused(D.keep);
        if (x) L.push({ job: 'keep', text: x });
      }
      if (!D.resolve) {
        // a street matter never takes away the way out: Leave is always last
        const lv = unused(LEAVES, n + T.turn);
        if (lv) L.splice(Math.min(L.length, TALKING.suggestedLinesAtMost - 1), L.length, { job: 'leave', text: lv });
      }
    }
  }
  if (D && !D.resolve && L.every((l) => l.job === 'leave') && !(D.q != null)) {
    // a street decision with nothing left to say on it never leaves the talk dead: it lapses and the ordinary lines return
    T.dec = null;
    return buildLines();
  }
  if (D) {
    // the decision's lines stand
  } else if (FBT.closed) {
    // they have closed the talk in their own voice: only a way to leave is offered
    L.push({ job: 'leave', text: unused(LEAVES, n + T.turn) || 'Right. Bye, then.' });
  } else {
    if (!T.said) {
      const x = unused(GREETS, n);
      if (x) L.push({ job: 'greet', text: x });
    } else if (T.sug.follow && !T.used.has(T.sug.follow))
      L.push({ job: 'follow', text: T.sug.follow, model: 1 });
    const pm = T.sug.personal && !T.used.has(T.sug.personal) ? T.sug.personal : null,
      pw = unused(PERSONAL, n + T.turn);
    if (pm) L.push({ job: 'personal', text: pm, model: 1 });
    else if (pw) L.push({ job: 'personal', text: pw });
    const lv = unused(LEAVES, n + T.turn);
    if (lv) L.push({ job: 'leave', text: lv });
  }
  T.lines = L;
  if (T.sel >= L.length) T.sel = 0;
  const open = T.open || !!G.settings.touch;
  setTalkLines(L, open, T.sel);
  if (open && L.length) {
    const k = L.map((l) => l.text).join(' | ');
    if (k !== T.shown) {
      T.shown = k;
      logLine(
        `Lines offered with ${tomName(P)}: ${L.map((l) => `[${l.job}${l.model ? ', model' : ''}] ${l.text}`).join(' / ')}`,
        'lines',
      );
    }
  }
}
export const talkLines = () => T.lines.map((l) => ({ job: l.job, text: l.text, model: !!l.model }));
export const talkState = () => ({
  on: !!T.P,
  who: T.P ? T.P.id : null,
  busy: !!T.busy,
  open: !!T.open,
  sel: T.sel,
  dec: T.dec ? T.dec.key || 'scene' : null,
  q: T.dec ? T.dec.q : null,
  slip: !!T.slip,
});
export const talkStub = (fn) => {
  T.sample = fn;
  T.ready = true;
  T.consent = true;
  T.dead = false;
};
function slip() {
  if (T.P) setTalkSlip(slipHTML(T.P, T.slip), T.slip);
}
function npc(P, text) {
  const p = talkLine('npc', text);
  T.hist.push({ role: 'assistant', content: text });
  heard(P, text);
  return p;
}
function heard(P, text) {
  hearName(P, text);
  talkHead();
  slip();
}
function talkKey(code, typed) {
  // Tab opens his lines, Up and Down choose, Enter says the one in hand, Tab goes back to his own words
  if (!T.P) return false;
  if (code === 'Tab') {
    T.open = !T.open;
    T.sel = 0;
    if (T.open) {
      st('linesOpened');
      tabPressed();
    }
    buildLines();
    return true;
  }
  if (code === 'F2') {
    T.slip = !T.slip;
    if (T.slip) {
      st('slipOpened');
      T.slipSeen = true;
    }
    G.settings.slipOpen = T.slip;
    saveSettings();
    slip();
    return true;
  }
  if (!T.open || !T.lines.length) return false;
  if (code === 'ArrowDown') {
    T.sel = (T.sel + 1) % T.lines.length;
    buildLines();
    return true;
  }
  if (code === 'ArrowUp') {
    T.sel = (T.sel + T.lines.length - 1) % T.lines.length;
    buildLines();
    return true;
  }
  if (code === 'Enter' && !typed) {
    pick(T.sel);
    return true;
  }
  return false;
}
function pick(i) {
  const l = T.lines[i];
  if (l && !T.busy) say(l.text, l);
}
// for the test hook: say suggested line i, or say typed words, by the same road as the keyboard
export const talkPick = (i) => pick(i);
export const talkType = (text) => say(text, null);
export const talkKeyPress = (code) => talkKey(code);
export function startTalk(P, opening) {
  if (T.P) return;
  reset(P);
  meet(P);
  let first = opening || (G.hooks.greet && G.hooks.greet(P)),
    news = !!first;
  if (!first) {
    const m = comeback(P);
    if (m) {
      first = comebackLine(P, m);
      markSaid(P, m);
      logLine(`${P.def.name} said it to his face: ${first}`, 'face');
      news = true;
    }
  }
  heardCall(P);
  openTalk(P, {
    onSay: (v) => say(v, null),
    onBye: endTalk,
    note: talkAvailable()
      ? 'Answers are voiced live by an AI. The game decides what happens.'
      : 'Live voices unavailable here: written lines only.',
  });
  if (!G.story.talkNotice) {
    G.story.talkNotice = true;
    talkLine(
      'sys',
      'A note, once: when you talk freely, the town answers in words written by an AI. What people know, and what your words do, is decided by the game.',
    );
  }
  if (news) {
    T.said = 1;
    npc(P, first);
    afterReply(P, true);
  } // they had something to say to his face, so they say it first
  else T.first = greet(P); // otherwise he opens, and they answer as they always do
  if (G.hooks.onTalkOpen) G.hooks.onTalkOpen(P);
  G.stats.talks++;
  st('slipShown');
  slip();
  buildLines();
}
function intro(P) {
  // a first meeting: most people give their name once he has spoken to them
  if (P.anon || knownNames()[P.id] || !P.def.name) return;
  if (SHY[P.id]) {
    P.shyN = (P.shyN || 0) + 1;
    if (P.shyN < 2) return;
  }
  const [f, ...l] = P.def.name.split(' '),
    last = l.join(' ');
  npc(
    P,
    [`${f} ${last}.`, `${f}. ${f} ${last}.`, `I'm ${f} ${last}.`, `${last}. ${f} ${last}.`][
      (P.def.name.length + (P.def.age || 0)) % 4
    ],
  );
}
async function afterReply(P, firstTurn) {
  if (T.P !== P) return;
  if (firstTurn) intro(P);
  const ms = G.hooks.matters ? G.hooks.matters(P) : [],
    m = ms.find((x) => !T.raised.has(x.key));
  if (m && !T.dec) {
    T.raised.add(m.key);
    if (m.raise) npc(P, m.raise);
    T.dec = Object.assign({}, m, { q: m.direct ? 0 : null, free: true });
  }
  if (!T.dec) suggest(P);
  buildLines();
}
async function say(text, line) {
  if (T.busy || !T.P || !text) return;
  const P = T.P;
  T.busy = true;
  talkBusy(true);
  T.open = false;
  setTalkLines([], false, 0);
  T.used.add(text);
  talkLine('me', text);
  st(line ? 'linesSaid' : 'typed');
  T.hist.push({ role: 'user', content: text });
  T.sug.seq++;
  try {
    if (T.dec) await decStep(P, text, line);
    else await freeStep(P, text, line);
  } catch (e) {
    console.warn('talk:', e);
  } finally {
    T.busy = false;
    talkBusy(false);
    if (T.P === P) {
      T.turn++;
      buildLines();
    }
  }
}
async function freeStep(P, text, line) {
  const firstTurn = !T.said;
  T.said++;
  if (line && line.job === 'leave') {
    npc(P, BYES[(P.def.name || P.id).length % BYES.length]);
    logLine(`Left ${tomName(P)} with: ${text}`, 'talk');
    after(TALKING.goodbyeAfterRealSeconds, () => {
      if (T.P === P) endTalk();
    });
    return;
  }
  if (line && line.job === 'greet' && T.first) {
    npc(P, T.first);
    T.first = null;
    logLine(`Greeted ${tomName(P)}: ${text}`, 'talk');
  } else {
    const it = await classify(P, text, null);
    if (T.P !== P) return;
    const res = decide(P, it, text);
    logLine(
      `Said to ${P.def.name} [${it.intent}${it.topic !== 'other' ? ':' + it.topic : ''}]: ${text.slice(0, 80)}`,
      'talk',
    );
    const out = await voice(P, res, text);
    if (T.P !== P) return;
    T.hist.push({ role: 'assistant', content: out });
    heard(P, out);
    T.first = null;
    if (res.after) await res.after();
    if (res.close && T.P === P) {
      after(TALKING.closesAfterRealSeconds, () => {
        if (T.P === P) endTalk();
      });
      return;
    }
  }
  heardCall(P);
  G.t += TALKING.turnTakesGameMinutes;
  await afterReply(P, firstTurn);
}
// A decision: the yes and the no are both the game's lines, with a third that keeps talking. Only a yes is taken.
async function decStep(P, text, line) {
  const D = T.dec;
  let job = line && line.job,
    idx = line ? line.i : -1;
  T.said++;
  if (!line) {
    const it = await classify(P, text, D.ask || (D.q != null ? D.opts[D.q].q : null) || 'a decision');
    if (T.P !== P || T.dec !== D) return;
    if (D.q != null) job = it.intent === 'agree' ? 'yes' : it.intent === 'refuse' ? 'no' : 'talk';
    else {
      idx =
        it.intent === 'agree'
          ? D.opts.findIndex((o) => o.agree)
          : it.intent === 'refuse'
            ? D.opts.findIndex((o) => o.refuse)
            : -1;
      job = idx >= 0 ? 'prop' : 'talk';
    }
    if (job === 'talk') {
      const res = decide(P, it, text),
        out = await voice(P, res, text);
      if (T.P !== P) return;
      T.hist.push({ role: 'assistant', content: out });
      heard(P, out);
      if (T.dec === D && D.resolve && D.q != null && D.opts[D.q].q) npc(P, D.opts[D.q].q);
      return;
    } // inside a scene the plain question is put again; in the street it simply stands
  }
  logLine(`Decision with ${tomName(P)} [${job}]: ${text.slice(0, 80)}`, 'talk');
  if (job === 'prop') {
    const o = D.opts[idx];
    if (o.q) {
      D.q = idx;
      npc(P, o.q);
    } else await take(P, D, idx);
    return;
  }
  if (job === 'yes') return take(P, D, D.q);
  if (job === 'keep') {
    const o = D.q != null ? D.opts[D.q] : null;
    npc(P, (o && o.keepSay) || D.keepSay || "That's as much as I can tell you.");
    if (o && o.keepDid) o.keepDid(); // what that answer told him, if it told him anything
    return;
  }
  if (job === 'no') {
    // a no decides nothing
    npc(
      P,
      (D.q != null && D.opts[D.q].noSay) ||
        D.noSay ||
        ["Right. It'll keep.", 'As you like.', 'Then we leave it there.'][T.turn % 3],
    );
    if (D.direct) {
      if (D.resolve) return finish(D, D.noIdx == null ? -1 : D.noIdx);
      T.dec = null;
      suggest(P);
    } else if (D.q == null) {
      // a no to the matter itself: it is dropped, and the ordinary lines and Leave come back
      T.dec = null;
      suggest(P);
    } else D.q = null;
  }
}
async function take(P, D, idx) {
  if (D.resolve) return finish(D, idx);
  T.dec = null;
  const o = D.opts[idx],
    out = o.take ? await o.take() : null;
  if (T.P === P) {
    if (typeof out === 'string') npc(P, out);
    suggest(P);
  }
}
function finish(D, idx) {
  T.dec = null;
  T.P = null;
  T.busy = false;
  closeTalk();
  D.resolve(idx);
}
// A decision put inside a scene: the person's line, then Tom's lines. Resolves with the option taken, or the one that stands for walking away.
export function decision(who, text, spec) {
  return new Promise((resolve) => {
    const P = G.people[who];
    if (T.P) endTalk();
    reset(P);
    T.said = 1;
    heardCall(P);
    openTalk(P, { onSay: (v) => say(v, null), onBye: endTalk, note: '' });
    npc(P, text);
    T.dec = Object.assign({ leaveIdx: -1 }, spec, { q: spec.direct ? 0 : null, resolve });
    st('slipShown');
    slip();
    buildLines();
  });
}
// The follow-up and the personal line: a call of its own, given only what Tom knows.
async function suggest(P) {
  const seq = ++T.sug.seq;
  T.sug.follow = null;
  T.sug.personal = null;
  if (!talkAvailable() || !T.consent || !T.hist.length) return;
  let late = false;
  const ctl = new AbortController(),
    to = setTimeout(() => {
      late = true;
      st('sugDropped');
      try {
        ctl.abort();
      } catch (e) {
        /* */
      }
    }, TALKING.liveVoiceWaitsRealMilliseconds); // six seconds, then the written lines stand
  try {
    const r = await T.sample.json(sugPrompt(P), { modelTier: 'quick', cache: false, signal: ctl.signal });
    if (late || seq !== T.sug.seq || T.P !== P || T.dec) return;
    T.sug.follow = okLine(r && r.follow);
    T.sug.personal = okLine(r && r.personal);
    if (T.sug.follow) st('sugLive');
    else st('sugDropped');
    logLine(
      `Model lines with ${tomName(P)}: follow ${T.sug.follow ? 'kept' : 'dropped'}${r && r.follow && !T.sug.follow ? ' (' + String(r.follow).slice(0, 70) + ')' : ''}, personal ${T.sug.personal ? 'kept' : r && r.personal ? 'dropped (' + String(r.personal).slice(0, 70) + ')' : 'none'}`,
      'lines',
    );
    buildLines();
  } catch (e) {
    if (!late) st('sugDropped');
  } finally {
    clearTimeout(to);
  }
}
// words that may carry a capital inside one of his lines without being somebody he has not heard of
const PLAIN = new Set(
  'I Mickey Suddaby Meridian Humber Quay Street Chapel Lane Hook Regent House Monday Tuesday Wednesday Thursday Friday Saturday Sunday October God Lord Christ Mr Mrs Miss Father Hull Evening Mail Dock Road Ferry Fish Row Customs'.split(
    ' ',
  ),
);
function okLine(x) {
  // too long, a name he has not heard, his own name, the content rule, or a deal: any of these and the line is dropped
  if (typeof x !== 'string') return null;
  x = clean(x)
    .replace(/^["'“]+|["'”]+$/g, '')
    .trim();
  if (
    !x ||
    x.split(/\s+/).length > TALKING.followUpWordsAtMost ||
    x.length > TALKING.followUpCharactersAtMost ||
    T.used.has(x)
  )
    return null;
  if (BANNED.test(x) || /\b(tom|tommy|thomas|nowak)\b/i.test(x) || DEAL.test(x)) return null;
  const kn = knownNames(),
    hd = heardNames(),
    ok = new Set(PLAIN);
  for (const Q of G.named) {
    const mine = kn[Q.id] || hd[Q.id];
    for (const w of Q.def.name.split(' ')) {
      if (mine) ok.add(w);
      else if (w.length > 2 && new RegExp('\\b' + w + '\\b').test(x)) return null;
    }
  }
  const words = x.split(/\s+/);
  for (let i = 1; i < words.length; i++) {
    const w = words[i].replace(/[^A-Za-z']/g, '').replace(/'s$/, '');
    if (/^[A-Z][a-z]/.test(w) && !/[.?!]$/.test(words[i - 1]) && !ok.has(w)) return null;
  } // any other capital mid-sentence is a name he was never given
  return x;
}
function sugPrompt(P) {
  const k = tomKnows(P),
    talk = T.hist
      .slice(-TALKING.pastTurnsGivenForFollowUps)
      .map((h) => `${h.role === 'user' ? 'He said' : 'They said'}: ${h.content}`)
      .join('\n');
  return `You write short spoken lines for one man, in his own plain words: a newcomer of 32 who has just inherited a minicab office on Quay Street in the port town of Meridian, on the Humber, in October 1990. Northern English, dry, few words, period speech.
${RULES}
He knows ONLY what is written here. Use nothing else.
Who he is talking to, as he knows them: ${tomName(P)}.
His own notebook about them:
${k.length ? k.map((x) => '- ' + x).join('\n') : '- Nothing yet.'}
The talk so far:
${talk}
Write what he might say next, as his exact words, in JSON with two keys:
"follow": one line that asks about, or picks up, what the other person JUST said. Twelve words at most.
"personal": one line off the subject, about them or the street. Twelve words at most, or an empty string.
Never give his own name. Never name anyone who is not named above. Never agree to, refuse, offer, promise or pay for anything. No stage directions, no quotation marks.`;
}
export function refreshActs() {
  slip();
  buildLines();
}
export function endTalk() {
  if (!T.P) return;
  const P = T.P,
    D = T.dec;
  if (T.ctl)
    try {
      T.ctl.abort();
    } catch (e) {
      /* */
    }
  if (D && D.resolve) return finish(D, D.leaveIdx); // walking away from a decision decides nothing more than it says
  talkEnded(!!T.slipSeen); // measured: the share of talks in which the slip was unfolded
  T.P = null;
  T.dec = null;
  T.busy = false;
  T.sug.seq++;
  closeTalk();
  if (G.hooks.onTalkClose) G.hooks.onTalkClose(P);
}
export function talkSay(cls, text) {
  return talkLine(cls, text);
}
export const talking = () => T.P;
