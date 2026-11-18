// LEDGER. The test hook: window.LEDGER.
// Everything a test needs without a key press, by the same roads the keyboard takes, and with every number
// readable: plain names with their units (Pence, GameMinutes, Metres, RealSeconds, ZeroToOne).
//
//   LEDGER.rules                 every rule's number, in one named table
//   LEDGER.read()                the game now: time, Tom, the cab, money, debts, weather, who is watching
//   LEDGER.person(id)            one person: where, doing what, what they know and feel
//   LEDGER.places                named places with their positions in metres
//   LEDGER.goTo(place)           put Tom at a named place (test only)
//   LEDGER.prompts()             the key prompts on offer now;  LEDGER.press('E') takes one, as the key does
//   LEDGER.written               a written scene: read() the line and its choices, next(), choose(n)
//   LEDGER.talk                  a talk: open(id), lines(), say(which), type(text), answer('yes'|'no'|'keep'), leave()
//   LEDGER.cab, LEDGER.fare      the cab and the radio fare: call(), accept(), pickUp(), dropOff()
//   LEDGER.job                   the night job: read(), goToPickUp(), goToDrop()
//   LEDGER.ledger                the Ledger screen: open(part), rows(), key(code), mark(row), close(), book()
//   LEDGER.measures()            the Ledger screen test's measures (the same object the JSON export holds)
//   LEDGER.pauses()              every pause and resume, with the game time and its reason
//   LEDGER.check                 arrivals() and nights(): see checks.js
//   LEDGER.step(realSeconds)     run the game forward by hand (set window.LEDGER_MANUAL = true first)
//   LEDGER.restore(text)         load a saved week exactly as Continue does;  LEDGER.saveText() gives one
import { G, day, hour, PAUSE, TALLY } from './state.js';
import { RULES } from './rules.js';
import { act } from './events.js';
import { clockText, dateText, DAYS, hyp } from './util.js';
import { KINDS } from './kinds.js';
import { SPOTS, DESTS, ROOMS, INSIDE, roomPos, zoneAt, blocked as mapBlocked } from './map.js';
import { ui, tomName, dialogNow, advance, pickOpt } from './ui.js';
import { buildPrompts, onKey, enterRoom, leaveRoom, talkTo } from './player.js';
import { startTalk, endTalk, talkLines, talkState, talkPick, talkType, talkKeyPress } from './talk.js';
import { fareOffer, fareAccept, farePlaces } from './fares.js';
import { JOBS } from './jobs.js';
import { washCap } from './money.js';
import { callName } from './gossip.js';
import { book, bookFaults, knownNames, openNow, moneyNow, syncOpen, ledgerSeen } from './ledger.js';
import { LS, PARTS, ledgerRows, peoplePages } from './ledger_screen.js';
import { measures, activeAsk } from './measures.js';
import { serialize } from './saving.js';
import { makeChecks } from './checks.js';
import { frontUp as fightFrontUp, setOn as fightSetOn, input as fightInput, block as fightBlock, climb as fightClimb, end as fightEnd } from './fight.js';

const r2 = (v) => Math.round(v * 100) / 100;
const r1 = (v) => Math.round(v * 10) / 10;
const wait = (ms) => new Promise((res) => setTimeout(res, ms));
const settle = () => wait(0);

// ---------- named places ----------
function places() {
  const out = {};
  const put = (name, x, z, kind) => {
    out[name] = { xMetres: r1(x), zMetres: r1(z), kind };
  };
  put('the rank', SPOTS.rank[0], SPOTS.rank[1], 'street');
  put("Mickey's door", SPOTS.door[0], SPOTS.door[1], 'door');
  for (const id in ROOMS)
    if (ROOMS[id].street)
      put(ROOMS[id].name + ' (street door)', ROOMS[id].street[0], ROOMS[id].street[1], 'door');
  for (const n in JOBS) {
    const J = JOBS[n];
    put(J.fromZ + ' (' + J.name + ': pick-up)', SPOTS[J.from][0], SPOTS[J.from][1], 'night job');
    put(J.toZ + ' (' + J.name + ': drop door)', SPOTS[J.to][0], SPOTS[J.to][1], 'night job');
  }
  for (const p of farePlaces().pickUps) put(p.name + ' (fare pick-up)', p.xMetres, p.zMetres, 'fare pick-up');
  for (const d of farePlaces().destinations)
    put(d.name + ' (fare destination)', d.xMetres, d.zMetres, 'fare destination');
  return out;
}

// ---------- reading the game ----------
function shown(P) {
  return tomName(P);
}
function read() {
  const t = G.tom,
    m = G.money,
    c = G.car,
    st = G.story,
    room = ROOMS[t.space];
  const debts = {};
  for (const id in G.debts)
    debts[G.people[id] ? G.people[id].def.name : id] = {
      personId: id,
      owedPence: G.debts[id].owed,
      state: G.debts[id].st,
    };
  return {
    gameMinute: r1(G.t),
    dayIndex: day(),
    day: DAYS[day() % 7],
    date: dateText(G.t),
    clock: clockText(G.t),
    hour: r2(hour()),
    realSecondsPlayed: r1(G.played),
    phase: st.phase,
    weekEnded: !!st.ended,
    paused: !!G.paused,
    pausedBecause: G.pauseWhy || null,
    boxOpen: ui.modal || null,
    inAWrittenScene: !!ui.inScene,
    toDo: st.objective || null,
    tom: {
      xMetres: r2(t.x),
      zMetres: r2(t.z),
      facingRadians: r2(t.ang),
      place: room ? room.name : zoneAt(t.inCar ? c.x : t.x, t.inCar ? c.z : t.z),
      indoorsRoomId: room ? t.space : null,
      inTheCab: !!t.inCar,
      hasTheCoat: !!t.hasCoat,
      coatOn: !!t.coat,
      carrying: t.carry || null,
      weapon: t.weapon || null,
      lightZeroToOne: r2(t.light == null ? 1 : t.light),
      noiseCarriesMetres: r1(t.noiseR || 0),
      hurtZeroToOne: r2(t.hurt || 0),
      speedMetresPerSecond: r2(t.v || 0),
    },
    cab: { xMetres: r2(c.x), zMetres: r2(c.z), speedMetresPerSecond: r2(c.v), tomHasTheKeys: !!c.keys },
    money: {
      pocketPence: m.clean,
      tinPence: m.dirty,
      faresTakenPence: m.fares,
      faresCount: m.fareCount,
      putThroughTheBookPence: m.washed,
      moreThanTheBookCanHidePence: m.booksOff,
      theBookWouldHideNowPence: washCap(),
      earnedCleanPence: m.earnedClean,
      earnedDirtyPence: m.earnedDirty,
      spentPence: m.spent,
    },
    debts,
    weather: {
      kind: G.weather.kind,
      rainZeroToOne: r2(G.weather.rain),
      mistZeroToOne: r2(G.weather.mist),
      streetWetZeroToOne: r2(G.weather.wet),
    },
    story: {
      flags: Object.assign({}, st.flags),
      nightJob: jobRead(),
      fare: fareRead(),
      policeComing: st.arrest ? { state: st.arrest.st || 'due', dueGameMinute: st.arrest.due } : null,
    },
    watching: (G.watch || []).map((w) => ({
      personId: w.P.id,
      shownAs: shown(w.P),
      clarityZeroToOne: r2(w.c),
      takesHimFor: w.who,
      tomHasNoticedThem: !!w.noticed,
    })),
  };
}

const SRC = { saw: 'saw it', told: 'was told', heard: 'heard it', self: 'was part of it' };
function person(id) {
  const P = G.people[id];
  if (!P) return null;
  const m = P.mind,
    room = ROOMS[P.space];
  return {
    personId: P.id,
    name: P.def.name,
    shownAs: shown(P),
    nameKnownToTom: !!knownNames()[P.id],
    xMetres: r2(P.x),
    zMetres: r2(P.z),
    place: room ? room.name : P.space === 'home' ? 'at home' : P.space === 'off' ? 'away' : zoneAt(P.x, P.z),
    awake: !!P.awake,
    atTheWindow: !!P.atWindow,
    walking: !!P.moving,
    goingTo: P.route && P.route.g ? goalName(P.route.g) : null,
    doing: P.state || null,
    pausedInWalkRealSeconds: r2(Math.max(0, P.pauseT || 0)),
    familiarityZeroToOne: r2(m.fam),
    regardMinusOneToOne: r2(m.regard),
    fearZeroToOne: r2(m.fear),
    callsTom: callName(P) || null,
    memories: m.mem.map((r) => ({
      eventId: r.e,
      what: KINDS[G.ev[r.e].kind].truth(G.ev[r.e]),
      howTheyKnow: SRC[r.src] || r.src,
      heardFromPersonId: r.from || null,
      takesHimFor: r.who,
      sureZeroToOne: r2(r.sure),
      heatZeroToOne: r2(r.heat),
      sinceGameMinute: r1(r.t),
      saidToHisFace: !!r.said,
    })),
  };
}
export function goalName(g) {
  if (!g) return null;
  if (g.kind === 'room') return ROOMS[g.room] ? ROOMS[g.room].name : g.room;
  if (g.kind === 'home') return 'home';
  if (g.kind === 'off') return 'away from the Hook';
  return zoneAt(g.x, g.z) + ` (${Math.round(g.x)}, ${Math.round(g.z)})`;
}

// ---------- the night job and the fare ----------
function jobRead() {
  const j = G.story.job;
  if (!j) return null;
  const J = JOBS[j.n];
  return {
    name: J.name,
    state: j.st === 'pickup' ? 'to pick up' : j.st === 'carry' ? 'carrying' : j.st,
    pickUpPlace: J.fromZ,
    pickUp: { xMetres: SPOTS[J.from][0], zMetres: SPOTS[J.from][1] },
    dropPlace: J.toZ,
    drop: { xMetres: SPOTS[J.to][0], zMetres: SPOTS[J.to][1] },
    payPence: J.pay,
    doorsOpenFromHour: J.after,
    doorsShutAtHour: RULES.jobs.doorsShutAtHour,
    // round 2: the constable on his beat during the carry (null before the pick-up or on old saves)
    watch: j.watch
      ? {
          state: j.watch.st,
          how: j.watch.how || null,
          constable: { xMetres: r1(G.people.pc.x), zMetres: r1(G.people.pc.z) },
          metresAway: r1(hyp(G.people.pc.x, G.people.pc.z, G.tom.x, G.tom.z)),
        }
      : null,
  };
}
function fareRead() {
  const f = G.story.fare;
  if (!f) return null;
  const D = DESTS[f.dest];
  return {
    state: f.st === 'offer' ? 'offered on the radio' : f.st === 'pickup' ? 'to pick up' : 'carrying',
    fromPlace: f.from,
    pickUp: { xMetres: r1(f.sx), zMetres: r1(f.sz) },
    toPlace: D.n,
    dropOff: { xMetres: D.p[0], zMetres: D.p[1] },
    farePence: f.pay,
    offerEndsInRealSeconds: f.st === 'offer' ? r1(f.t) : null,
    passengerPersonId: f.pid || f.who || null,
  };
}

export function installHook(x) {
  // x: what only the main file has (the stepping function, starting and loading a week, the Ledger's open and close)
  const stepBy = (secs) => {
    for (let i = 0; i < secs / 0.05; i++) x.logic(0.05);
  };
  const putTom = (px, pz) => {
    const t = G.tom;
    if (t.inCar) {
      G.car.x = px;
      G.car.z = pz;
      G.car.v = 0;
    } else {
      if (t.space !== 'street') leaveRoom();
      t.x = px;
      t.z = pz;
      t.v = 0;
    }
    x.snapCam();
    return read().tom;
  };

  const written = {
    // the written line on screen: who says it (as Tom knows them), the words, and the choices if it asks
    read() {
      const d = dialogNow();
      if (ui.modal !== 'dialog' || !d) return { open: false };
      return {
        open: true,
        speakerPersonId: d.P ? d.P.id : null,
        speaker: d.P ? shown(d.P) : d.who || null,
        text: d.text,
        choices: d.opts ? d.opts.slice() : null,
        waitsForAChoice: !!d.opts,
      };
    },
    // E: finish the line and go on. Resolves with the next line (or { open: false } when the scene is over).
    async next() {
      const d = dialogNow();
      if (!d) return written.read();
      if (!d.done) advance();
      if (!d.opts) advance();
      await settle();
      await settle();
      return written.read();
    },
    // pick choice n (0 is the first), as the number keys do
    async choose(n) {
      const d = dialogNow();
      if (!d || !d.opts) return written.read();
      if (!d.done) advance();
      pickOpt(n);
      await settle();
      await settle();
      return written.read();
    },
  };

  const talk = {
    state() {
      const s = talkState(),
        P = s.who ? G.people[s.who] : null;
      return {
        open: ui.modal === 'talk' && !!s.on,
        personId: s.who,
        shownAs: P ? shown(P) : null,
        waitingForTheReply: !!s.busy,
        suggestedLinesOpen: !!s.open,
        deciding: s.dec,
        plainQuestionPut: s.q != null,
        slipUnfolded: !!s.slip,
      };
    },
    lines: () =>
      talkLines().map((l, i) => ({ line: i, job: l.job, text: l.text, writtenByTheModel: !!l.model })),
    // the old name, kept for the earlier tests: open a talk with this person at once, where they both stand
    start: (id) => startTalk(G.people[id]),
    // Go up to someone and press E, wherever they are (Tom is put beside them). If a written scene is waiting
    // with them (a first meeting, a job offered) it runs, exactly as in play: read it with LEDGER.written.
    // Otherwise a talk opens. free: true skips any waiting scene and opens a talk.
    open(id, o = {}) {
      const P = G.people[id];
      if (!P || ui.modal || P.gone || P.space === 'home' || P.space === 'off')
        return Object.assign(talk.state(), { written: written.read() });
      const t = G.tom;
      if (t.inCar) t.inCar = false;
      if (P.space !== t.space) {
        if (ROOMS[P.space]) enterRoom(P.space, true);
        else if (t.space !== 'street') leaveRoom();
      }
      t.x = P.x + Math.sin(P.ang) * 1.5;
      t.z = P.z + Math.cos(P.ang) * 1.5;
      if (o.free) startTalk(P);
      else talkTo(P);
      return Object.assign(talk.state(), { written: written.read() });
    },
    // wait until the other person has answered
    async idle() {
      for (let i = 0; i < 400 && talkState().busy; i++) {
        await wait(25);
        if (window.LEDGER_MANUAL) x.logic(0.05);
      }
      await settle();
      return talk.state();
    },
    // say a suggested line: by its number, or by its job ('greet', 'follow', 'personal', 'leave', 'yes', 'no', 'keep', 'prop')
    async say(which, nth = 0) {
      await talk.idle();
      if (ui.modal !== 'talk') return null;
      if (!talkState().open) talkKeyPress('Tab');
      const L = talkLines();
      let i = typeof which === 'number' ? which : -1;
      if (i < 0) {
        const same = L.map((l, k) => (l.job === which ? k : -1)).filter((k) => k >= 0);
        i = same.length ? same[Math.min(nth, same.length - 1)] : -1;
      }
      if (i < 0 || i >= L.length) {
        talkKeyPress('Tab');
        return null;
      }
      const said = L[i];
      talkPick(i);
      await wait(20);
      await talk.idle();
      if (said.job === 'leave') {
        for (let k = 0; k < 120 && ui.modal === 'talk'; k++) await wait(25);
      }
      return { said: said.text, job: said.job, state: talk.state() };
    },
    async type(text) {
      await talk.idle();
      if (ui.modal !== 'talk') return null;
      talkType(text);
      await wait(20);
      return talk.idle();
    },
    // answer what is being decided. 'yes' takes it (proposing first if the plain question has not been put),
    // 'no' and 'keep' decide nothing. proposal: which thing to propose when there is more than one.
    async answer(what, proposal = 0) {
      await talk.idle();
      if (ui.modal !== 'talk' || !talkState().dec)
        return { answered: false, why: 'nothing is being decided', state: talk.state() };
      const said = [];
      if (what === 'yes' && talkState().q == null) {
        const r = await talk.say('prop', proposal);
        if (r) said.push(r.said);
      }
      if (ui.modal === 'talk' && talkState().dec) {
        const r = await talk.say(what);
        if (r) said.push(r.said);
      }
      await wait(30);
      return { answered: said.length > 0, said, state: talk.state() };
    },
    // a key in the talk box: 'Tab' (suggested lines), 'F2' (fold or unfold the slip), 'ArrowDown', 'ArrowUp'
    key(code) {
      talkKeyPress(code);
      return talk.state();
    },
    async leave() {
      if (ui.modal === 'talk') endTalk();
      await settle();
      return talk.state();
    },
  };

  const cab = {
    read: () => read().cab,
    // F at the cab door (Tom is put beside it)
    getIn() {
      const t = G.tom;
      if (t.inCar) return true;
      if (t.space !== 'street') leaveRoom();
      t.x = G.car.x + 1.6;
      t.z = G.car.z;
      onKey('KeyF');
      return !!t.inCar;
    },
    getOut() {
      G.car.v = 0;
      if (G.tom.inCar) onKey('KeyF');
      return !G.tom.inCar;
    },
    driveTo(px, pz) {
      G.car.x = px;
      G.car.z = pz;
      G.car.v = 0;
      return read().cab;
    },
  };
  const fare = {
    read: fareRead,
    places: farePlaces,
    // have Pauline call a fare now, instead of waiting for the radio (Tom must be in the cab with the keys)
    call() {
      if (!G.story.fare) fareOffer();
      for (let i = 0; i < 40 && !G.story.fare; i++) fareOffer(); // a run too short to be worth a fare is not offered
      return fareRead();
    },
    accept() {
      fareAccept(); // the same call the Y key makes
      return fareRead();
    },
    // pull in beside the passenger and stop
    pickUp() {
      const f = G.story.fare;
      if (!f || f.st !== 'pickup') return fareRead();
      cab.driveTo(f.sx + 1.5, f.sz);
      stepBy(0.5);
      return fareRead();
    },
    // pull in at the destination and stop. Resolves when the fare is settled (a written scene may follow).
    async dropOff() {
      const f = G.story.fare;
      if (!f || f.st !== 'carry') return { settled: false, fare: fareRead() };
      const before = G.money.clean,
        D = DESTS[f.dest];
      cab.driveTo(D.p[0], D.p[1] + 1.5);
      stepBy(0.5);
      await settle();
      return {
        settled: !G.story.fare,
        paidPence: G.money.clean - before,
        fare: fareRead(),
        boxOpen: ui.modal || null,
      };
    },
  };
  const job = {
    read: jobRead,
    goToPickUp() {
      const j = jobRead();
      return j ? putTom(j.pickUp.xMetres, j.pickUp.zMetres) : null;
    },
    goToDrop() {
      const j = jobRead();
      return j ? putTom(j.drop.xMetres, j.drop.zMetres) : null;
    },
  };

  const ledger = {
    open(part, device = 'hook') {
      x.openLedger(device, part);
      return ledger.read();
    },
    close() {
      x.closeLedger();
      return ui.modal !== 'ledger';
    },
    read: () => ({
      open: ui.modal === 'ledger',
      said: LS.said || null, // the one line the book says back ("Jump to which letter?", "Not that one.")
      part: LS.part,
      parts: PARTS.slice(),
      person: LS.person,
      dayIndex: LS.dayIdx,
      cursorRow: LS.cur,
      rows: ledgerRows(),
      ask: activeAsk() ? activeAsk().question : null,
    }),
    rows: ledgerRows,
    pages: () =>
      peoplePages().map((id) => ({
        personId: id,
        heading: id === 'anon' ? 'Passers-by' : tomName(G.people[id]),
        nameKnown: !!knownNames()[id],
      })),
    // a key or pad button, as the Ledger takes it: 'KeyQ', 'KeyE', 'ArrowDown', 'ArrowRight', 'KeyB', 'Enter', 'KeyL'
    key(code, device = 'hook') {
      x.ledgerKey(code, device);
      return ledger.read();
    },
    // put the cursor on a row and mark it (Enter): this is how a find-the-fact ask is answered
    mark(row, device = 'hook') {
      LS.cur = row;
      x.ledgerKey('Enter', device);
      return { said: LS.said, ask: activeAsk() ? activeAsk().question : null };
    },
    // every entry in the book, whatever part it shows in
    book: () => {
      syncOpen();
      return book().entries.map((e) => Object.assign({}, e, { when: dateText(e.t) + ', ' + clockText(e.t) }));
    },
    // As if Tom had just learned that this person knows of that act (he saw them see it, or they said so): the
    // game's own way of writing a belief, so a test can make a watcher turn up when it wants one.
    learn(eventId, personId, basis = 'said') {
      const E = G.ev[eventId],
        P = G.people[personId];
      if (!E || !P) return false;
      ledgerSeen(E, P, basis);
      return true;
    },
    // As if Tom had just done this, where he stands: the game's own act(), with its witnesses and its entry.
    // For a test that needs an act at a moment of its choosing. Returns the event's id.
    act(kind, o = {}) {
      const E = act(kind, o);
      return E ? E.id : null;
    },
    // the acts still waiting to see whether anybody saw them ("Nobody saw" is written only after the wait)
    waiting: () => (book().waiting || []).map((w) => ({ eventId: w.ev, sinceGameMinute: w.t })),
    openItems: openNow, // what is waiting on him now, as the game computes it
    moneySums: moneyNow, // the sums Tom knows, in pence
    faults: bookFaults,
  };

  const hook = {
    // kept from earlier rounds
    benchmark: x.benchmark,
    rig: x.rig,
    scene: x.scene,
    camera: x.camera,
    THREE: x.THREE,
    G,
    ui,
    cam: x.cam,
    F: x.F,
    tick: (dt) => x.logic(dt), // one game step of dt real seconds (round 3: the drills step at 1/60 s)
    isBlocked: (px, pz) => mapBlocked(px, pz), // round 3: the wall drill looks for a wall
    fight: { frontUp: fightFrontUp, setOn: fightSetOn, input: fightInput, block: fightBlock, climb: fightClimb, end: fightEnd }, // round 3: the melee drills drive the fight directly
    startNew: x.startNew,
    simStep: x.simStep,
    enterRoom,
    leaveRoom,
    endWeek: x.endWeek,
    passTime: x.passTime,
    reportText: x.reportText,
    saveNow: x.saveNow,
    step: stepBy,
    restore: x.loadWeek,
    // readable
    rules: RULES,
    read,
    person,
    people: () => G.named.map((P) => ({ personId: P.id, name: P.def.name, shownAs: shown(P) })),
    places: places(),
    goTo(place) {
      const p = typeof place === 'string' ? hook.places[place] : place;
      if (!p) return null;
      return putTom(p.xMetres, p.zMetres);
    },
    // things inside rooms, by name: the coat hook, the cot, the bed, the counters
    insidePlaces: Object.fromEntries(
      Object.values(INSIDE).map((h) => [
        h.name,
        {
          roomId: h.room,
          room: ROOMS[h.room].name,
          xMetresInRoom: h.x,
          zMetresInRoom: h.z,
          withinMetres: h.within,
        },
      ]),
    ),
    // put Tom inside a room, at a named thing in it (or just inside the door when only the room is given)
    goInside(name) {
      const h = Object.values(INSIDE).find((q) => q.name === name),
        room = h ? h.room : Object.keys(ROOMS).find((id) => id === name || ROOMS[id].name === name);
      if (!room) return null;
      if (G.tom.inCar) G.tom.inCar = false;
      if (G.tom.space !== room) enterRoom(room, true);
      if (h) {
        const [px, pz] = roomPos(h.room, h.x, h.z);
        G.tom.x = px;
        G.tom.z = pz;
      }
      x.snapCam();
      return read().tom;
    },
    goOutside() {
      if (G.tom.space !== 'street') leaveRoom();
      return read().tom;
    },
    prompts: () => buildPrompts().map((p) => ({ key: p.k, text: p.t })),
    // press a key as the keyboard does: 'E', 'T', 'F', 'C', 'Y', 'G', 'L', or a full code such as 'KeyE'
    press(key) {
      onKey(/^[A-Z]$/.test(key) ? 'Key' + key : key);
      return { prompts: hook.prompts(), boxOpen: ui.modal || null, paused: !!G.paused };
    },
    written,
    talk,
    cab,
    fare,
    job,
    ledger,
    measures,
    measuresJSON: () => JSON.stringify(measures(), null, 2),
    // The gossip table: per day, sightings, stories passed on, how far the furthest story travelled (in tellings),
    // and which named people stood within talking distance. Counted since this week was started or loaded.
    gossip() {
      const days = [];
      for (let d = 0; d <= day(); d++) {
        const row = TALLY.days[d] || { sightings: 0, heard: 0, met: {} };
        let far = 0;
        for (const id in G.minds)
          for (const r of G.minds[id].mem || [])
            if (Math.floor(r.t / 1440) === d && (r.hop || 0) > far) far = r.hop;
        days.push({
          dayIndex: d,
          date: dateText(d * 1440),
          sightings: row.sightings,
          heardOnly: row.heard,
          storiesPassedOn: G.transfers.filter((t) => Math.floor(t.t / 1440) === d).length,
          furthestStoryTellings: far,
          pairsWhoMet: Object.keys(row.met).sort(),
        });
      }
      return days;
    },
    // the files published beside the page: list them, read one as text, gather them all as one zip (a Blob)
    files: x.files,
    pauses: () =>
      PAUSE.log.map((p) =>
        Object.assign({ clock: dateText(p.gameMinute) + ', ' + clockText(p.gameMinute) }, p),
      ),
    pauseFaults: () => PAUSE.faults,
    saveText: serialize,
    wait,
  };
  hook.check = makeChecks(hook, x);
  window.LEDGER = hook;
  return hook;
}
