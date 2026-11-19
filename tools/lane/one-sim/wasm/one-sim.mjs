// ONE SIMULATION IN THE BROWSER: the loader (first slice, 19 November 2026).
//
// Loads one-sim.wasm (the game's own C++ town rules, compiled for the browser) and
// gives JavaScript a plain object to call. It runs the same in a web page, in a Web
// Worker and under Node, and it needs no library: the handful of system calls the C
// library asks for are answered here, in about thirty lines.
//
//   import { loadOneSim } from './one-sim.mjs';
//   const sim = await loadOneSim(await (await fetch('one-sim.wasm')).arrayBuffer());
//   sim.newTown(castJsonText);            // production/specs/hook-cast.json, as text
//   const row = sim.hour(0, 19, 'mickeys');   // one game hour, in the game's own order
//
// What the module may ask of the outside world is listed in sim.asksOutside, and the
// answers below are fixed: no clock, no random numbers, no files. The same calls in
// the same order therefore always give the same town (the tests check this).

const ENOSYS = 52, EBADF = 8, ESPIPE = 70;

export async function loadOneSim(wasm, { print = (text) => console.log(text) } = {}) {
  const mod = wasm instanceof WebAssembly.Module ? wasm : await WebAssembly.compile(wasm);
  let memory;
  const dec = new TextDecoder(), enc = new TextEncoder();
  const u8 = () => new Uint8Array(memory.buffer);
  const dv = () => new DataView(memory.buffer);
  let pending = '';

  const system = {
    // Printing (the C library's stdout and stderr): handed to `print`, whole lines.
    fd_write(fd, iovs, count, written) {
      let n = 0;
      for (let i = 0; i < count; i++) {
        const p = dv().getUint32(iovs + 8 * i, true), len = dv().getUint32(iovs + 8 * i + 4, true);
        pending += dec.decode(u8().subarray(p, p + len));
        n += len;
      }
      const cut = pending.lastIndexOf('\n');
      if (cut >= 0) { print(pending.slice(0, cut)); pending = pending.slice(cut + 1); }
      dv().setUint32(written, n, true);
      return 0;
    },
    fd_close: () => 0,
    fd_seek: () => ESPIPE,
    fd_fdstat_get(fd, buf) { u8().fill(0, buf, buf + 24); dv().setUint8(buf, 2); return 0; },   // a plain character stream
    fd_prestat_get: () => EBADF,            // no folders: the page has no files
    fd_prestat_dir_name: () => EBADF,
    environ_sizes_get(count, size) { dv().setUint32(count, 0, true); dv().setUint32(size, 0, true); return 0; },
    environ_get: () => 0,
    clock_time_get(id, precision, out) { dv().setBigUint64(out, 0n, true); return 0; },   // the town's time is the game's clock, never the computer's
    random_get(buf, len) { u8().fill(0, buf, buf + len); return 0; },                     // the town's chance is seeded by the rules, never by the computer
    proc_exit(code) { throw new Error('one-sim: the module asked to stop with code ' + code); },
  };

  const asksOutside = [];
  const imports = {};
  for (const imp of WebAssembly.Module.imports(mod)) {
    asksOutside.push(imp.module + '.' + imp.name);
    (imports[imp.module] ??= {})[imp.name] = system[imp.name] ?? (() => ENOSYS);
  }

  const { exports: x } = await WebAssembly.instantiate(mod, imports);
  memory = x.memory;
  if (x._initialize) x._initialize();

  const put = (text) => {
    const bytes = enc.encode(String(text));
    const p = x.os_alloc(bytes.length + 1);
    u8().set(bytes, p);
    u8()[p + bytes.length] = 0;
    return p;
  };
  const read = (p) => {
    const m = u8();
    let e = p;
    while (m[e]) e++;
    return dec.decode(m.subarray(p, e));
  };
  // Call an export; JavaScript strings are copied in and freed after the call.
  const call = (name, ...args) => {
    const held = [];
    const real = args.map((a) => (typeof a === 'string' ? (held.push(put(a)), held[held.length - 1]) : a));
    try { return x[name](...real); } finally { for (const p of held) x.os_free(p); }
  };
  const text = (name, ...args) => read(call(name, ...args));

  const sim = {
    asksOutside,
    version: () => text('os_version'),

    // The town: from a cast file's text. Throws with the reason if the cast cannot be read.
    newTown(castJson) { if (!call('os_town_new', castJson)) throw new Error(text('os_error')); },
    people: () => text('os_people').split(',').filter(Boolean),
    // Routines: where a person is at an hour of a day (day 0 is the first Monday).
    placeOf: (person, day, hour) => text('os_place_of', person, day, hour),
    age: (day, hour, minute = 0) => call('os_age', day, hour, minute),
    // One game hour, the scheduled steps in the game's order. Returns thirteen fields joined by '|'.
    hour: (day, hour, area) => text('os_hour', day, hour, area),

    // What the player does, between the hours.
    roundsTo: (day, hour, minute) => call('os_rounds_to', day, hour, minute),
    deed: (day, hour, minute, area, thing, said, witnesses, storyFact, storySaid, certainty = 1.0) =>
      call('os_deed', day, hour, minute, area, thing, said, witnesses, storyFact, storySaid, certainty),
    answerAsk: (askDay, what, day, hour, minute) => call('os_answer_ask', askDay, what, day, hour, minute) === 1,
    asksOn: (day) => call('os_asks_on', day) === 1,
    askDelivered: (day) => call('os_ask_delivered', day) === 1,
    teaDay: () => call('os_tea_day'),
    teaWithHer: (day, hour, minute) => call('os_tea_with_her', day, hour, minute),
    weekDay: () => call('os_week_day'),
    weekAsksNow: (day, hour, minute, atOffice = true) => call('os_week_asks_now', day, hour, minute, atOffice ? 1 : 0) === 1,
    weekAsk: (day, hour, minute) => call('os_week_ask', day, hour, minute) === 1,
    weekGive: (answer, day, hour, minute) => call('os_week_give', answer, day, hour, minute) === 1,
    policeReport: (who, topic, offence, rung, day) => call('os_police_report', who, topic, offence, rung, day) === 1,
    takeIn: (topic, day, hour, minute) => call('os_take_in', topic, day, hour, minute) === 1,

    // Reading the town back.
    state: () => text('os_state'),          // the week's pieces as the game's own save writes them (JSON text)
    stories: () => text('os_stories'),      // who holds which story, one line a person
    // The Ledger's facts: who knows what, and how. A list of { who, topic, value, saw, hops, from, rung, names, sure, private, said }.
    knows: () => JSON.parse(text('os_knows')),

    // The proof, in the check build only: any row of the C# Core's golden table.
    check: x.os_check_row
      ? { castFile: (name, body) => call('os_check_cast_file', name, body), row: (line) => text('os_check_row', line) }
      : null,
  };
  return sim;
}

// The numbers the bridge takes, named (they are the port's own enum orders).
export const NightAnswer = { Did: 0, Refused: 1, NoShow: 2, Undelivered: 3 };
export const WeekAnswer = { None: 0, WindDown: 1, TakeOver: 2, WontSay: 3 };
export const Offence = { Suspicious: 0, Damage: 1, Assault: 2, Wounding: 3, Robbery: 4, Killing: 5 };
