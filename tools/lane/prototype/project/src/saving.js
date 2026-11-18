// Saving the week. To the viewer's Claude account when the page can (so it follows them between devices), and to this browser as well.
import { G, VERSION, setPaused } from './state.js';

const KEYS = [
  'v',
  't',
  'played',
  'weather',
  'tom',
  'car',
  'minds',
  'events',
  'sightIdx',
  'transfers',
  'nextE',
  'ledger',
  'log',
  'money',
  'debts',
  'story',
  'stats',
  'measures', // the Ledger screen test's measures (a save from before them has none)
];
const LS = 'ledger.save.v' + VERSION,
  CH = 150000;
const S = { db: null, uid: null, ready: false, busy: false, queued: null, last: 0 };
export async function initSave() {
  try {
    if (window.claude && window.claude.use) {
      const [db, user] = await Promise.all([window.claude.use('db'), window.claude.use('user')]);
      if (db && user) {
        const id = await user.id();
        if (id) {
          S.db = db;
          S.uid = id;
        }
      }
    }
  } catch (e) {
    /* no account storage here */
  }
  S.ready = true;
}
export function serialize() {
  const o = {};
  for (const k of KEYS) o[k] = G[k];
  o.minds = {};
  for (const id in G.minds) {
    const m = G.minds[id];
    const c = Object.assign({}, m);
    delete c.by;
    c.attn = 0;
    c.look = 0;
    o.minds[id] = c;
  }
  o.story = Object.assign({}, G.story, { fare: null, ellis: null, phase: 'play' });
  if (o.story.arrest && o.story.arrest.st)
    o.story.arrest = Object.assign({}, o.story.arrest, { st: undefined });
  o.at = Date.now();
  return JSON.stringify(o);
}
export function restore(json) {
  const o = JSON.parse(json);
  if (o.v !== VERSION) return false;
  for (const k of KEYS) if (o[k] !== undefined) G[k] = o[k];
  if (o.measures === undefined) G.measures = null; // an older save: the measures start from here
  G.ev = {};
  for (const E of G.events) G.ev[E.id] = E;
  G.tom.inCar = false;
  G.tom.armed = false;
  setPaused(false, 'a saved week was loaded');
  G.fast = 1;
  G.watch = [];
  return true;
}
function local() {
  try {
    return localStorage.getItem(LS);
  } catch (e) {
    return null;
  }
}
const doc = (name) => S.db.doc('data/users/' + S.uid + '/' + name);
async function remote() {
  if (!S.db) return null;
  try {
    const m = await doc('ledger_meta').get();
    if (!m.exists) return null;
    const d = m.data();
    let s = '';
    for (let i = 0; i < d.n; i++) {
      const c = await doc('ledger_' + i).get();
      if (!c.exists) return null;
      s += c.data().s;
    }
    return s;
  } catch (e) {
    return null;
  }
}
// The newer of the two saves, by wall clock.
export async function findSave() {
  const a = local(),
    b = await remote();
  const at = (s) => {
    try {
      return JSON.parse(s).at || 0;
    } catch (e) {
      return -1;
    }
  };
  const best = a && b ? (at(b) > at(a) ? b : a) : a || b;
  if (!best) return null;
  try {
    const o = JSON.parse(best);
    if (o.v !== VERSION || !o.story || o.story.phase === 'title') return null;
    return { json: best, t: o.t, played: o.played, ended: o.story.ended };
  } catch (e) {
    return null;
  }
}
async function pushRemote(json) {
  if (!S.db) return;
  if (S.busy) {
    S.queued = json;
    return;
  }
  S.busy = true;
  try {
    const n = Math.ceil(json.length / CH);
    for (let i = 0; i < n; i++) await doc('ledger_' + i).set({ s: json.slice(i * CH, (i + 1) * CH) });
    await doc('ledger_meta').set({ n, at: Date.now(), t: G.t, played: G.played });
    S.last = Date.now();
  } catch (e) {
    /* keep the local copy */
  }
  S.busy = false;
  if (S.queued) {
    const q = S.queued;
    S.queued = null;
    pushRemote(q);
  }
}
export function saveNow(remoteToo = true) {
  if (G.story.phase !== 'play' && G.story.phase !== 'end') return false;
  const json = serialize();
  let ok = false;
  try {
    localStorage.setItem(LS, json);
    ok = true;
  } catch (e) {
    /* storage unavailable */
  }
  if (remoteToo && S.db) {
    pushRemote(json);
    ok = true;
  }
  return ok;
}
export const saveWhere = () => (S.db ? 'your Claude account and this browser' : 'this browser');
