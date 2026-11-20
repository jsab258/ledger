// LEDGER, the whole game: side stories (DESIGN section 4: found on foot, no markers, light or grey against the main
// story, three to five steps, each ending in something the town knows). Six to begin with. A step is a spot on the
// street, sometimes with hours; nothing announces it but a prompt when he is there.
import { X, emit } from './core.js';
import { G, day, hour } from '../state.js';
import { RULES } from '../rules.js';
import { say, choose, scene } from '../ui.js';
import { act } from '../events.js';
import { note } from '../ledger.js';
import { pay } from '../money.js';
import { clamp } from '../util.js';

const T = RULES.game.life.stories;
const regard = (id, by) => {
  const P = G.people[id];
  if (P && P.mind) P.mind.regard = clamp(P.mind.regard + by, -1, 1);
};
const night = () => hour() >= 20 || hour() < 5;
const notSunday = () => day() % 7 !== 6;
// Each step: { x, z, prompt, when?: () => bool, run: async (st) => next step number | { end, kind, what, line, fact } | null (nothing yet) }
export const STORIES = [
  {
    id: 'bench',
    name: 'The plate off the bench',
    steps: [
      {
        x: -6.2, z: -62.6, prompt: 'Look at the bench',
        run: async () => {
          await say('', 'The memorial bench by the chapel gate. Four screw holes and a clean oblong where a brass plate was. Somebody has pencilled the words back from memory: TO THE MEN OF THE HOOK LOST AT SEA.');
          note('The brass plate is gone off the memorial bench by the chapel. Brass goes for scrap.', 'story', 'st_bench', { how: 'Saw it' });
          return 1;
        },
      },
      {
        x: -6.0, z: 0, prompt: 'Ask in the doorway about brass', when: () => notSunday() && hour() >= 8.5 && hour() < 17.5,
        run: async () => {
          await say('', 'The ironmonger does not look up from the till. "A lad brought a brass plate in Monday wanting it weighed. I do not buy off benches. I sent him to Iveson\'s, who does."');
          return 2;
        },
      },
      {
        x: -99, z: 44, prompt: 'Look through the brass by the gate', when: () => hour() >= 7.5 && hour() < 21,
        run: async (st) => {
          const i = await choose('', 'A tea chest of taps, door knockers and stair rods inside Iveson\'s gate. Near the top, face down, a plate with four holes. The yard hand is watching.', ['Pay him the scrap price (£1.20)', 'Tell him whose it is, and take it', 'Leave it']);
          if (i === 2 || i < 0) return null;
          if (i === 0 && !pay(120, false, 'scrap price for the bench plate')) {
            await say('', 'He has not got one pound twenty to spare.');
            return null;
          }
          st.paid = i === 0;
          await say('', i === 0 ? 'The yard hand pockets it and shrugs. Brass is brass.' : '"It is off the chapel bench, and you know it is." The yard hand finds something to do elsewhere.');
          G.tom.items['brass plate'] = 1;
          return 3;
        },
      },
      {
        x: -6.2, z: -62.6, prompt: 'Screw the plate back on',
        run: async () => {
          await say('', 'Father Walsh comes out with a screwdriver and holds the plate straight while Tom turns the screws. "I will not ask where it was. I will say who put it back, if anybody asks. And somebody always asks."');
          delete G.tom.items['brass plate'];
          regard('walsh', 0.3);
          return { end: 'returned', kind: 'story_end', what: 'found the brass plate off the chapel bench and screwed it back on', told: ['walsh'], line: 'The plate is back on the memorial bench. Father Walsh knows who put it there.', fact: 'bench' };
        },
      },
    ],
  },
  {
    id: 'nets',
    name: 'The man in the net store',
    steps: [
      {
        x: -68, z: 43.6, prompt: 'The door banging on the net store', when: night,
        run: async (st) => {
          const i = await choose('', 'The net store door is banging in the wind. Inside, by matchlight: a man asleep on the nets under a tarpaulin, his boots set neatly beside him.', ['Wake him', 'Pull the door to and leave him']);
          if (i !== 0) {
            st.did = 'left';
            st.day = day();
            return 1;
          }
          const j = await choose('', '"Deckhand. The Marguerite, laid up since June. I have nowhere till Thursday and I have touched nothing." He has not.', ['Give him the price of a dinner (£1.80)', '"The Harbour Office will hear of this."', 'Leave him be']);
          st.did = j === 0 && pay(180, false, 'a dinner for the deckhand in the net store') ? 'fed' : j === 1 ? 'told' : 'left';
          st.day = day();
          await say('', st.did === 'fed' ? 'He counts it twice. "I will not forget the face."' : st.did === 'told' ? 'He starts pulling his boots on without a word.' : 'He lies back down. The door bangs.');
          return 1;
        },
      },
      {
        x: -6.2, z: -29, prompt: "A word at Rinaldi's door", when: () => hour() >= 7 && hour() < 17.5,
        ready: (st) => day() > st.day,
        run: async (st) => {
          if (st.did === 'fed') {
            await say('grace', 'That feller off the Marguerite was in at seven asking for work, and said who sent him. I have him washing pots. He has hands like shovels and he has not broken one yet.');
            regard('grace', 0.2);
            st.end = { end: 'fed', kind: 'story_end', what: 'fed a laid-up deckhand who was sleeping in the net store', told: ['grace'], line: 'The deckhand from the net store washes pots at Rinaldi\'s now. He will not forget the face.', fact: 'deckhand' };
            return 2;
          }
          if (st.did === 'told') {
            await say('grace', 'The Board had a padlock on the net store by eight. Some poor soul off the boats was sleeping in it. Somebody told on him. This street will work out who.');
            st.end = { end: 'told', kind: 'looked_away', what: 'had a homeless deckhand turned out of the net store', told: ['grace'], line: 'The Harbour Board padlocked the net store. The street is working out who told.', fact: null };
            return 2;
          }
          await say('grace', 'Brenda says there is a man sleeping in the net store. Saw his boots at dawn. Nobody has done a thing about it, one way or the other.');
          st.end = { end: 'left', kind: null, line: 'A laid-up deckhand is sleeping in the net store, and the street knows.', fact: null };
          return 2;
        },
      },
      {
        x: -68, z: 43.6, prompt: 'Look in at the net store',
        run: async (st) => {
          await say('', st.did === 'fed' ? 'The nets are folded square and the tarpaulin with them. On the top one, in chalk: TA.' : st.did === 'told' ? 'A new padlock on the net store door, and a Harbour Board notice. A pair of boots has been left on the step.' : 'The door is wedged shut from inside with a fish box. Somebody is making the best of it.');
          return st.end;
        },
      },
    ],
  },
  {
    id: 'piano',
    name: 'The piano for the hall',
    steps: [
      {
        x: -7, z: -66, prompt: 'The man measuring the gate', when: () => notSunday() && hour() >= 14.5 && hour() < 16.5,
        run: async () => {
          const i = await choose('danby', 'It will go through by an inch. There is a piano in the yard of the Ship, under a sheet, and the owners say the hall can have it if somebody will shift it. It is on castors. Two men could do it.', ['"Now is as good as any."', '"Another day."']);
          if (i !== 0) return null;
          await say('danby', 'Then I will fetch the hall key. The yard gate is round the side of the Ship, tied with wire.');
          return 1;
        },
      },
      {
        x: -6.2, z: -84, prompt: 'Untwist the wire on the yard gate',
        run: async () => {
          await say('', 'Behind the gate of the boarded Ship, a shape under a tarpaulin gone green with a summer of rain. Under it an upright piano, walnut, two keys missing like teeth. It rolls.');
          return 2;
        },
      },
      {
        x: -7, z: -66, prompt: 'Roll the piano up to the hall',
        run: async () => {
          await say('', 'Sixty yards of pavement with a piano between them, every castor finding every crack. A woman at the bus stop calls the kerbs. Doors open to watch. At the chapel gate it goes through by an inch.');
          await say('danby', 'It wants tuning, and so do I. Thank you. I mean that more than it sounds.');
          regard('danby', 0.3);
          regard('walsh', 0.2);
          const c = X('life').calls;
          c.danby.push({ honest: true, cool: false, t: Math.round(G.t), how: 'the piano' });
          return { end: 'moved', kind: 'story_end', what: 'helped Philip Danby roll a piano up Quay Street to the chapel hall', told: ['danby', 'walsh'], line: 'The chapel hall has a piano. Half Quay Street watched it go up the pavement.', fact: 'piano' };
        },
      },
    ],
  },
  {
    id: 'wreath',
    name: 'The wreath',
    steps: [
      {
        x: -5.8, z: 22.6, prompt: 'The woman waving from the bus stop', when: () => day() >= 21 && day() <= 26 && hour() >= 8 && hour() < 13,
        run: async () => {
          const i = await choose('nora', 'Ah, it is yourself. The wreath for Sunday is ordered at the flower stall on the market and my legs will not do that bridge twice. It is paid for. Would you?', ['"I will fetch it."', '"Not today."']);
          return i === 0 ? 1 : null;
        },
      },
      {
        x: -34, z: -146, prompt: 'Ask at the flower stall', when: () => hour() >= 8 && hour() < 16,
        run: async () => {
          await say('', 'A ring of poppies and laurel in tissue paper, with a card in a careful hand: THE MEN OF THE HOOK. "For the chapel? Mind the wire, it is sharp."');
          G.tom.items.wreath = 1;
          return 2;
        },
      },
      {
        x: -13, z: -70, prompt: 'Lay the wreath by the stone',
        run: async () => {
          await say('', 'He sets it against the stone where the others will go on Sunday. Forty names, and six of them Suddaby.');
          delete G.tom.items.wreath;
          regard('nora', 0.3);
          regard('walsh', 0.15);
          return { end: 'laid', kind: 'story_end', what: 'fetched the Remembrance wreath from the market and laid it at the chapel stone', told: ['nora'], line: 'The wreath is at the stone for Sunday. Six of the forty names are Suddaby.', fact: 'wreath' };
        },
      },
    ],
  },
  {
    id: 'ladder',
    name: "Shaun's ladder",
    steps: [
      {
        x: 6.2, z: 3.4, prompt: 'The painter looking up at nothing', when: () => notSunday() && hour() >= 8 && hour() < 16.5,
        run: async () => {
          await say('shaun', 'Some beggar has walked off with my ladder. Double extension, red tape on the third rung. I turned my back to mix a tin. I cannot do a fascia off a chair.');
          note('Shaun Hewson, the sign painter, has had his ladder taken: a double extension with red tape on the third rung.', 'story', 'st_ladder', { who: 'shaun', how: 'Shaun says' });
          return 1;
        },
      },
      {
        x: 30.2, z: 2, prompt: 'The ladder on the garage roofs',
        run: async () => {
          const i = await choose('', 'Flat on the garage roofs off the back lane, a double extension ladder. Red tape on the third rung. Whoever used it to get over the yards did not need it to get back.', ['Take it down', 'Leave it']);
          if (i !== 0) return null;
          note('Shaun\'s ladder was on the garage roofs off the back lane. Somebody went over the yards with it.', 'story', 'st_ladder2', { how: 'Saw it' });
          return 2;
        },
      },
      {
        x: 6.2, z: 3.4, prompt: 'Give Shaun his ladder',
        run: async () => {
          await say('shaun', 'On the garages? Over the yards, then. Well. I owe you one, and I pay in paint. Anything you want a different colour, you say.');
          regard('shaun', 0.35);
          return { end: 'returned', kind: 'story_end', what: 'found Shaun Hewson\'s ladder on the garage roofs and brought it back', told: ['shaun'], line: 'Shaun Hewson owes a favour, and pays in paint.', fact: 'shaun' };
        },
      },
    ],
  },
  {
    id: 'keys',
    name: 'The keys on the bollard',
    steps: [
      {
        x: -30, z: 51.6, prompt: 'The keys on the bollard',
        run: async () => {
          const i = await choose('', 'A bunch of keys hung on the bollard by the phone box, where a man might put them down to find his change. A brass tag: No. 3.', ['Take them', 'Leave them']);
          if (i !== 0) return null;
          G.tom.items['keys: No. 3'] = 1;
          return 1;
        },
      },
      {
        x: -28.5, z: 43.2, prompt: 'Ask at the Harbour Office whose No. 3 is', when: () => notSunday() && hour() >= 8 && hour() < 22,
        run: async () => {
          await say('', 'The clerk reads the tag without touching it. "No. 3 is let to Jensen and Son. Their watchman is Dent. He comes on at ten and sits by a brazier on the row. He will be missing those."');
          note('The keys with the brass tag are for warehouse No. 3, let to Jensen and Son. The watchman, Dent, comes on at ten.', 'story', 'st_keys', { how: 'Told at the Harbour Office' });
          return 2;
        },
      },
      {
        x: 70, z: 43.4, prompt: "The watchman's brazier on the row", when: night,
        run: async () => {
          const i = await choose('', 'Norman Dent, the night watchman, is turning out his pockets by the brazier for the third time.', ['Hand him the keys', 'Say nothing and walk on']);
          if (i === 0) {
            await say('norman', 'Oh, thank God. Oh. I thought that was my job gone. I never saw you. But I will know you, if you take my meaning.');
            delete G.tom.items['keys: No. 3'];
            regard('norman', 0.45);
            return { end: 'returned', kind: 'story_end', what: 'handed the watchman of the warehouse row his lost keys', told: ['norman'], line: 'Norman Dent, the watchman on the row, has his keys back and knows who to thank.', fact: 'norman' };
          }
          return { end: 'kept', kind: 'story_grey', what: 'kept the keys of warehouse No. 3 off the quay', silent: true, line: 'The keys of No. 3 are in his pocket. Norman Dent is asking along the row for them.', fact: 'keys3' };
        },
      },
    ],
  },
];
const byId = Object.fromEntries(STORIES.map((s) => [s.id, s]));
const stOf = (id) => {
  const x = X('life').stories;
  return x[id] || (x[id] = { step: 0, done: false });
};
function open(s) {
  const st = stOf(s.id);
  if (st.done) return null;
  const step = s.steps[st.step];
  if (!step) return null;
  if (step.when && !step.when()) return null;
  if (step.ready && !step.ready(st)) return null;
  return step;
}
// what is waiting to be found now, for "always something to do"
export function storyThings() {
  return STORIES.map((s) => {
    const step = open(s);
    return step ? { id: s.id, x: step.x, z: step.z, step: stOf(s.id).step } : null;
  }).filter(Boolean);
}
async function runStep(s) {
  const st = stOf(s.id),
    step = s.steps[st.step];
  let r = null;
  await scene(async () => {
    r = await step.run(st);
  });
  if (r == null) return;
  if (typeof r === 'number') {
    st.step = r;
    st.t = Math.round(G.t);
  } else {
    st.done = true;
    st.outcome = r.end;
    st.t = Math.round(G.t);
    let E = null;
    if (r.kind) E = act(r.kind, { what: r.what, told: r.told || [], silent: !!r.silent });
    if (r.line) note(r.line, 'story', 'st_' + s.id + '_end', { how: 'Was there', ev: E && E.id });
    if (r.fact) X('life').favours[r.fact] = day();
    emit('story:end', { id: s.id, outcome: r.end });
  }
  if (G.hooks.save) G.hooks.save();
}
export function storyHotspots(out) {
  const t = G.tom;
  if (t.space !== 'street' || t.inCar) return;
  for (const s of STORIES) {
    const step = open(s);
    if (!step || Math.hypot(t.x - step.x, t.z - step.z) > T.foundWithinMetres) continue;
    out.push({ k: 'E', t: step.prompt, run: () => runStep(s) });
    return;
  }
}
export const storyHook = {
  stories: () => STORIES.map((s) => ({ id: s.id, name: s.name, steps: s.steps.map((p) => ({ x: p.x, z: p.z, prompt: p.prompt, hours: !!p.when })), state: Object.assign({}, stOf(s.id)) })),
  storyOpen: (id) => {
    const p = open(byId[id]);
    return p ? { x: p.x, z: p.z, prompt: p.prompt } : null;
  },
  storyRun: (id) => runStep(byId[id]),
};
