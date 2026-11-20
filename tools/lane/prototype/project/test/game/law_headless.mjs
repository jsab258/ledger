// The game's rules run in Node, with no browser and no drawing: the clock, the people and their routines, seeing,
// gossip, the story's steps, the police and every system of game/, stepped by hand. Written by the law builder
// on 20 Nov when nine builders' browsers could not share the machine's memory; any system's test may use it.
// What is not here: the player's own walking and camera (Tom is put where a test needs him), drawing, sound,
// the talk box (a test reads a person's matters and calls their take). Written scenes run: clear() reads on and
// takes choices, as the browser tests' clear() does.
//   const h = await boot();  h.LEDGER.G ...;  await h.step(2);  await h.clear({ choice: 0 });  await h.pass(t);
const el = () => new Proxy(function () {}, {
  get: (t, k) => (k === 'classList' ? { add() {}, remove() {}, toggle() {}, contains: () => true } : k === 'style' || k === 'dataset' ? {} : k === 'children' || k === 'childNodes' ? [] : k === 'getContext' ? () => null : typeof k === 'symbol' ? undefined : k === 'then' ? undefined : el()),
  set: () => true,
  apply: () => el(),
});
globalThis.document = { getElementById: () => el(), createElement: () => el(), querySelector: () => el(), querySelectorAll: () => [], addEventListener() {}, body: el(), fonts: { load: async () => {} }, documentElement: el() };
globalThis.window = globalThis;
globalThis.addEventListener = () => {};
globalThis.localStorage = { getItem: () => null, setItem() {} };
globalThis.requestAnimationFrame = () => 0;

export async function boot(o = {}) {
  const util = await import('../../src/util.js');
  // the game's random numbers from a seed, so a run is the same every time
  let s = (o.seed || 1990) >>> 0;
  util.R.f = () => {
    s = (s + 0x6d2b79f5) | 0;
    let t = Math.imul(s ^ (s >>> 15), 1 | s);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
  const S = await import('../../src/state.js');
  const scenes = await import('../../src/scenes.js');
  const game = await import('../../src/game/index.js');
  const clock = await import('../../src/clock.js');
  const UI = await import('../../src/ui.js');
  const events = await import('../../src/events.js');
  const work = await import('../../src/work.js');
  const fight = await import('../../src/fight.js');
  const G = S.G;
  clock.initEnv(() => G.tom.ang);
  scenes.initStory();
  scenes.newWeek();
  game.gameLoaded();
  G.tom.x = -5.4;
  G.tom.z = 27.5;
  G.tom.space = 'street';
  const micro = () => new Promise((r) => setImmediate(r));
  // one step of the game, as main.js logic() runs it, without the player's own walking
  function logic(dt) {
    UI.tickTimers(dt);
    UI.dialogTick(dt);
    if (!G.paused && G.story.phase === 'play') {
      G.played += dt;
      clock.simStep(dt);
      scenes.storyStep(dt);
      game.gameStep(dt);
      fight.step(dt);
    }
  }
  async function step(secs) {
    const n = Math.max(1, Math.round(secs / 0.05));
    for (let i = 0; i < n; i++) {
      logic(0.05);
      if (i % 4 === 3) await micro();
    }
    await micro();
  }
  // read written lines on and take choice n until the game runs again
  async function clear(c = {}) {
    const met = [];
    for (let i = 0; i < 400; i++) {
      await step(0.1);
      const d = UI.dialogNow();
      if (d) {
        if (!d.done) UI.advance();
        if (d.opts) {
          met.push(d.who + ': ' + d.text.slice(0, 60) + ' [' + d.opts.join(' | ') + ']');
          UI.pickOpt(Math.min(c.choice || 0, d.opts.length - 1));
        } else {
          met.push(d.who + ': ' + d.text.slice(0, 60));
          UI.advance();
        }
        await micro();
      } else if (!G.paused && !UI.ui.modal && !UI.ui.inScene) {
        await step(0.2);
        if (!G.paused && !UI.dialogNow()) return met;
      }
    }
    return met;
  }
  const LEDGER = {
    G,
    ui: UI.ui,
    F: fight.F,
    game: game.gameHook(),
    act: (kind, x = {}) => events.act(kind, x).id,
    passTime: (t) => work.passTime(t),
    leaveRoom() {
      G.tom.space = 'street';
    },
    cam: { yaw: 0 },
    read: () => ({ paused: !!G.paused, boxOpen: UI.ui.modal || null }),
  };
  globalThis.LEDGER = LEDGER;
  const pass = async (t) => {
    const p = work.passTime(t);
    await clear();
    await p;
    await clear();
  };
  return { LEDGER, G, step, clear, pass, sleep: (ms) => step(Math.max(0.05, ms / 1000)), errors: game.FAULTS, close: async () => {} };
}
