// The system "law" played by the game's own rules in Node (law_headless.mjs: no browser, no drawing): the witness's
// walk and stopping it, the crowd after a deed, the four stages and their signs, the beat constable's challenge,
// search and chase, custody by the deed, the office searched, bought men, finding an unseen deed, the missing, the
// dial's police, and the real town's hour. It needs no browser, so it runs however busy the machine is. The rules' numbers
// are in src/game/tune/law.js; the pure rules have their cases in test/cases/.
import { boot } from './law_headless.mjs';

const h = await boot({ seed: 1990 });
const L = async (fn, ...a) => fn(...a);
const clear = h.clear;
let bad = 0;
const check = (name, ok, extra = '') => { if (!ok) bad++; console.log(`${ok ? 'ok  ' : 'FAIL'} ${name}${extra ? ' | ' + String(typeof extra === 'string' ? extra : JSON.stringify(extra)).slice(0, 300) : ''}`); };
const put = (x, z, ang = 0) => L((x, z, ang) => { const t = LEDGER.G.tom; if (t.space !== 'street') LEDGER.leaveRoom(); t.inCar = false; t.x = x; t.z = z; t.ang = ang; t.run = false; LEDGER.cam.yaw = ang; }, x, z, ang);
const pass = h.pass;
const stepUntil = async (test, secs = 1, max = 60, ...a) => { for (let i = 0; i < max; i++) { if (await L(test, ...a)) return true; await h.step(secs); } return L(test, ...a); };
const nextAt = (hr) => L((hr) => { const t = LEDGER.G.t, d = Math.floor(t / 1440); return d * 1440 + hr * 60 > t + 1 ? d * 1440 + hr * 60 : (d + 1) * 1440 + hr * 60; }, hr);
const law = () => L(() => JSON.parse(JSON.stringify(LEDGER.game.law.state())));
// a deed nobody else sees, then one person made its plain witness by hand, as if she had stood and watched
const deed = (kind, who, o = {}) => L((kind, who, o) => {
  const G = LEDGER.G, id = LEDGER.act(kind, Object.assign({ silent: true }, o)), E = G.ev[id];
  Object.assign(E, o.set || {});
  if (who) { const P = G.people[who]; P.mind.regard = -0.4; P.mind.fear = 0; P.mind.bought = false; LEDGER.game.law.plantWitness(id, who); }
  return id;
}, kind, who, o);
try {
  await L(() => { const G = LEDGER.G, f = G.story.flags; f.tour = 1; G.car.keys = true; f.metRon = f.metDarren = f.metPauline = f.metJune = 1; });
  await pass(1440 + 10.5 * 60); await h.step(1);
  await L(() => LEDGER.game.law.beat.force(false));

  // ---- 2.5.1, 1.4.5: the walk. Nothing is on record until it ends; in his sight it lasts at least 30 real seconds
  const who = await L(() => { const G = LEDGER.G; const P = G.named.find((p) => p.space === 'street' && !p.gone && p.awake && !p.def.nostmt && !p.def.police && !p.keeper && !['sheila', 'ron', 'pauline', 'kevin', 'terry', 'darren'].includes(p.id)); return P ? { id: P.id, x: P.x, z: P.z } : null; });
  check('a witness is on the street to walk', !!who, who);
  await put(who.x + 2.5, who.z + 2, Math.atan2(-2.5, -2));
  const e1 = await deed('shove', who.id);
  const w0 = await L((id, e) => LEDGER.game.law.wouldState(id, e), who.id, e1);
  check('she saw it plainly and means to tell', w0.goes, w0);
  await L((id, e) => LEDGER.game.law.startWalk(id, e), who.id, e1);
  await h.step(6);
  let x = await law();
  const w1 = x.walks.find((w) => w.e === e1);
  check('she sets off, and is seen to go', w1 && w1.st === 'walking' && w1.inSight && w1.said === 1, w1);
  check('ER-EYES-04: a walk begun in his sight is given at least 30 real seconds', w1 && w1.realLeft > 20 && w1.realLeft <= 30, w1 && w1.realLeft);
  check('until the walk ends nothing is on record', !(await L((e) => (LEDGER.G.ev[e].stmt || []).length, e1)) && !(await L(() => LEDGER.G.story.arrest)));
  const m0 = await L((id) => { const P = LEDGER.G.people[id]; return { moving: !!P.moving, to: P.override && P.override.where, x: P.x, z: P.z }; }, who.id);
  check('she walks to the phone box, the station or a friend', m0.to === 'phone' || m0.to === 'station' || w1.to === 'friend', m0);
  // ---- 2.5.2: stopping her. Each answer's effect
  const talk = await L((id) => { const P = LEDGER.G.people[id]; return LEDGER.G.hooks.matters(P).map((m) => ({ key: m.key, opts: m.opts.length, raise: m.raise })); }, who.id);
  check('reached first, she can be talked round, paid, threatened or helped (a talk decision)', talk.some((m) => /^lawwalk/.test(m.key) && m.opts === 4), talk);
  const r1 = await L((id) => { const G = LEDGER.G; G.people[id].def.nerve = 0.4; const before = G.people[id].mind.by; return LEDGER.game.law.stopWalk(id, 'threat'); }, who.id);
  x = await law();
  check('a threat stops the report to the police', r1 && r1.police === false && x.walks.find((w) => w.e === e1).st === 'stopped', r1);
  check('and never the street: she still holds what she saw', r1.street === true && (await L((id, e) => !!LEDGER.G.people[id].mind.by[e], who.id, e1)));
  check('she will give no statement now', !(await L((id, e) => LEDGER.game.law.wouldState(id, e).goes, who.id, e1)));
  // paid: the money goes, she keeps quiet
  const e2 = await deed('shove', who.id);
  await L((id, e) => { const G = LEDGER.G, P = G.people[id]; P.mind.fear = 0; P.def.venal = 0.6; G.x.law.turned = {}; G.money.clean = 5000; LEDGER.game.law.startWalk(id, e); }, who.id, e2);
  await h.step(6);
  const r2 = await L((id) => ({ r: LEDGER.game.law.stopWalk(id, 'pay'), clean: LEDGER.G.money.clean, bought: LEDGER.G.people[id].mind.bought }), who.id);
  check('paid: ten pounds for a shove, out of his pocket, and no report', r2.r.police === false && r2.r.cost === 1000 && r2.clean === 4000 && r2.bought === true, r2);
  // let go: the walk ends and it is on record
  const e3 = await deed('shove', who.id);
  await L((id, e) => { const G = LEDGER.G, P = G.people[id]; P.mind.fear = 0; P.mind.bought = false; P.mind.regard = -0.4; G.x.law.turned = {}; LEDGER.game.law.startWalk(id, e); for (const w of G.x.law.walks) if (w.e !== e && (w.st === 'pending' || w.st === 'walking')) w.st = 'dropped'; G.story.arrest = null; }, who.id, e3);
  await h.step(0.5);
  await L((e) => { const G = LEDGER.G; for (const w of G.x.law.walks) if (w.e !== e && (w.st === 'pending' || w.st === 'walking')) w.st = 'dropped'; }, e3);
  await h.step(6);
  await put(60, 80); // out of her way
  const landed = await stepUntil((e) => (LEDGER.G.ev[e].stmt || []).length > 0, 5, 80, e3);
  x = await law();
  const w3 = x.walks.find((w) => w.e === e3);
  check('let go, she gets there and it is on record', landed && w3.st === 'landed', w3);
  const arr = await L(() => LEDGER.G.story.arrest);
  check('a named statement brings the constable at nine next morning (ER-POL-01)', arr && arr.e === e3 && arr.by.includes(who.id) && arr.cls === 'window' && arr.due === 2 * 1440 + 9 * 60, arr);
  check('the first statement moves the police to asking round, one stage at a time', (await law()).stage >= 1 && (await law()).stage <= 2, (await law()).stage);

  // ---- 2.5.3: after a seen deed, people look, one comes nearer and drifts back, witnesses talk quieter
  const near = await L(() => { const G = LEDGER.G; const P = G.named.concat(G.crowd).filter((p) => p.space === 'street' && !p.gone && p.awake && !p.def.police); return P.length; });
  await L((id) => { const G = LEDGER.G, P = G.people[id], t = G.tom; t.x = P.x + 2; t.z = P.z + 2; let n = 0; for (const Q of G.named.concat(G.crowd)) { if (Q === P || Q.def.police || Q.dead || Q.keeper || n >= 3) continue; if (Q.space !== 'street' || Q.gone || !Q.awake) continue; Q.x = P.x + 5 + n * 2; Q.z = P.z + 4; Q.route = null; n++; } }, who.id);
  const e4 = await deed('shove', who.id);
  const re = await L((e) => { const r = LEDGER.game.law.reaction(e); return { looked: r.looked.length, gathered: r.gathered, quiet: LEDGER.game.law.talksQuieter(LEDGER.G.ev[e].wit[0]) }; }, e4);
  check('ER-EYES-09: people near a seen deed look, one gathers, the witness talks quieter', re.looked >= 1 && !!re.gathered && re.quiet, Object.assign(re, { onStreet: near }));
  await h.step(12);
  check('and the one who came nearer drifts back', (await law()).gatherers.length === 0);

  // ---- 2.6.4: custody as hours by the deed; never twice for one deed; under two real minutes
  await L(() => { LEDGER.G.story.flags.alison = 1; });
  await pass(2 * 1440 + 8.95 * 60); await h.step(0.5);
  await put(6.2, 20, 3.14);
  const t0 = await L(() => LEDGER.G.t);
  const played0 = await L(() => LEDGER.G.played);
  const came = await stepUntil(() => LEDGER.ui.modal === 'dialog', 3, 60);
  check('the constable comes to him and says what the statement was (an officer at his door)', came);
  await clear({ choice: 2 }); await h.sleep(2500); await h.step(1); await clear();
  x = await law();
  const la = x.lastArrest;
  check('owning up to the least deed: two hours and a caution', la && la.hours === 2 && la.outcome === 'cautioned' && la.cls === 'window', la);
  const t1 = await L(() => LEDGER.G.t);
  check('custody cost its hours and let him go (ER-POL-03)', Math.abs(t1 - la.fromT - 120) < 20 && !(await L(() => LEDGER.G.story.arrest)) && !(await L(() => LEDGER.read().paused)), { minutes: t1 - t0 });
  check('and under two real minutes of play', (await L(() => LEDGER.G.played)) - played0 < 120, (await L(() => LEDGER.G.played)) - played0);
  check('the duty solicitor is free: no bill', !(await L(() => LEDGER.G.story.flags.oweAgar)) && (await L(() => LEDGER.G.money.clean)) === 4000);
  const again = await L((id, e) => { LEDGER.game.law.plantStatement(e, id); return LEDGER.G.story.arrest; }, who.id, e3);
  check('never twice for one deed', !again, again);
  // a robbery: twelve hours, charged and bailed, and the charge joins the case
  const e5 = await deed('strike', who.id, { set: { lawClass: 'robbery' } });
  await L((id, e) => LEDGER.game.law.plantStatement(e, id), who.id, e5);
  const a5 = await L(() => LEDGER.G.story.arrest);
  check('a witnessed robbery is on record and an arrest is due', a5 && a5.e === e5 && a5.cls === 'robbery', a5);
  await pass(a5.due - 3); await h.step(0.5); await put(6.2, 20, 3.14);
  const t2 = await L(() => LEDGER.G.t);
  await stepUntil(() => LEDGER.ui.modal === 'dialog', 3, 60);
  await clear({ choice: 0 }); await h.sleep(2500); await h.step(1); await clear();
  x = await law();
  check('a robbery costs twelve hours, a charge and bail', x.lastArrest.hours === 12 && x.lastArrest.outcome === 'charged' && Math.abs((await L(() => LEDGER.G.t)) - x.lastArrest.fromT - 720) < 20, x.lastArrest);
  check('the charge joins DS Ellis\'s case, for the endings to read', x.case.charges.length === 1 && x.case.charges[0].cls === 'robbery' && x.case.strength >= 3, x.case);

  // ---- 2.6.5: four stages, each with its sign; none skipped; a manhunt's sign an hour before its arrest
  await L(() => { const x = LEDGER.G.x.law; x.stage = 0; x.signs = []; x.reported = {}; x.ellisAsked = 0; x.ran = 0; LEDGER.G.story.arrest = null; LEDGER.game.law.setStage(3); });
  const seenStages = [];
  let arrestAt = null, sign3 = null;
  for (let i = 0; i < 260 && arrestAt == null; i++) {
    await h.step(1.5);
    const s = await L(() => { const x = LEDGER.G.x.law; return { stage: x.stage, signs: x.signs.map((g) => [g.stage, g.t, g.shown]), t: LEDGER.G.t, arrest: !!LEDGER.G.story.arrest }; });
    if (seenStages[seenStages.length - 1] !== s.stage) seenStages.push(s.stage);
    const g3 = s.signs.find((g) => g[0] === 3 && g[2]);
    if (g3 && sign3 == null) sign3 = g3[1];
    if (s.arrest) arrestAt = s.t;
  }
  check('ER-POL-05: the stages come one at a time, 1 then 2 then 3', seenStages.join(',').replace(/^0,/, '') === '1,2,3', seenStages.join(','));
  x = await law();
  const shown = x.signs.filter((g) => g.shown).map((g) => g.stage);
  check('each stage showed its sign before the next began', shown.join(',') === '1,2,3' && x.signs[1].t - x.signs[0].t >= 30 && x.signs[2].t - x.signs[1].t >= 30, x.signs);
  check("a manhunt's sign is up a game hour before its arrest can land", arrestAt != null && sign3 != null && arrestAt - sign3 >= 60, { sign3, arrestAt });
  await L(() => { const x = LEDGER.G.x.law; LEDGER.G.story.arrest = null; x.hunted = 0; x.stage = 0; x.signs = []; });

  // ---- 2.6.1, 2.6.2: the beat constable. Heard 3 s before he can challenge; he calls out before he acts; a search
  // finds exactly what is carried and he keeps it
  await pass(await nextAt(23)); await h.step(0.5); await clear();
  await put(4.5, 10, 3.14);
  await L(() => { const G = LEDGER.G; G.x.crime = G.x.crime || {}; G.x.crime.carried = [{ name: 'the envelope', hand: true }, 'a crowbar']; G.tom.carry = null; G.tom.weapon = 'cosh'; LEDGER.game.law.beat.place(6); });
  let calledAt = null, heardAtCall = null;
  for (let i = 0; i < 80 && calledAt == null; i++) {
    await h.step(0.25);
    const b = await L(() => ({ st: LEDGER.G.x.law.beat.st, heard: LEDGER.G.x.law.beat.heard, said: LEDGER.G.x.law.beat.said }));
    if (b.st === 'called') { calledAt = i * 0.25; heardAtCall = b.heard; }
  }
  check('ER-POL-02: he is heard for 3 s before he calls out, and he calls out before he acts', calledAt != null && heardAtCall >= 3 && calledAt >= 2.75, { calledAt, heardAtCall });
  const dlg = await stepUntil(() => LEDGER.ui.modal === 'dialog', 0.5, 80);
  check('standing, he walks up and puts it to him', dlg);
  await clear({ choice: 0 });
  x = await law();
  const found = x.beat.lastSearch && x.beat.lastSearch.found;
  check('the search finds exactly what he carries, and the constable keeps it (ER-POCKET-01)', found && found.join('|') === 'the envelope|a crowbar|a cosh' && (await L(() => LEDGER.G.x.crime.carried.length === 0 && LEDGER.G.tom.weapon === null)), found);
  // the chase: run, and it ends lost inside 90 s; then he looks round where he last saw him
  await L(() => { const G = LEDGER.G; G.x.crime.carried = [{ name: 'a holdall', big: true }]; G.tom.x = 4.5; G.tom.z = 10; LEDGER.game.law.beat.place(6); });
  await stepUntil(() => LEDGER.G.x.law.beat.st === 'called', 0.25, 80);
  await L(() => { LEDGER.G.tom.x += 9; LEDGER.G.tom.z += 4; });
  await h.step(0.3);
  check('moving off after he has called out starts a chase', (await law()).beat.st === 'chase', (await law()).beat.st);
  let secs = 0;
  for (; secs < 100; secs += 2) { await L(() => { const t = LEDGER.G.tom; t.x = 120; t.z = 40; }); await h.step(2); if ((await law()).beat.st !== 'chase') break; }
  x = await law();
  check('ER-POL-04: the chase ends, lost, inside 90 real seconds, by breaking sight or distance', x.beat.st === 'look' && secs < 90 && x.beat.chases[x.beat.chases.length - 1].end === 'lost', { secs, st: x.beat.st });
  check('A3: having lost him he goes to where he last saw him and looks round', x.beat.lookLeft > 0 && x.beat.lookLeft <= 30);
  // a word, and a note. An honest constable: a note offered is a crime he saw
  await L(() => { const G = LEDGER.G; G.x.crime.carried = [{ name: 'a holdall', big: true }]; G.tom.x = 4.5; G.tom.z = 10; G.money.clean = 6000; LEDGER.game.law.beat.force(null); LEDGER.game.law.beat.place(6); });
  const officer = await L(() => LEDGER.G.x.law.beat.officer);
  await stepUntil(() => LEDGER.ui.modal === 'dialog', 0.5, 120);
  const metNote = await clear({ choice: 2 });
  x = await law();
  const a6 = await L(() => LEDGER.G.story.arrest);
  if (officer === 'pc') check('A13: a note offered to an honest constable is a crime he saw himself', x.beat.lastWord === 'arrest' && a6 && LEDGER_ok(a6), { word: x.beat.lastWord, a6 });
  else check('A13: PC Pashby takes the note and looks away, once a night', x.beat.lastWord === 'looks away' && x.bought.pashby.used === 1 && !a6, { word: x.beat.lastWord, b: x.bought, metNote, beat: LEDGER.G.x.law.beat, cause: LEDGER.game.law.beat.cause(), paused: LEDGER.G.paused, modal: LEDGER.ui.modal, hour: (LEDGER.G.t % 1440) / 60 });
  await L(() => { LEDGER.G.story.arrest = null; LEDGER.game.law.beat.force(false); });
  await h.step(1);

  // ---- 2.6.8: bought men. Each does only what his limit says (ER-BOUGHT-01)
  const e7 = await deed('shove', who.id);
  await L((id, e) => { const G = LEDGER.G; G.x.law.turned = {}; G.people[id].mind.bought = false; G.people[id].mind.fear = 0; G.people[id].mind.regard = -0.4; G.x.law.bought.thwaite.used = 0; G.money.clean = 9000; LEDGER.game.law.plantStatement(e, id); }, who.id, e7);
  const b1 = await L(() => ({ pending: !!LEDGER.G.story.arrest, matter: LEDGER.G.hooks.matters(LEDGER.G.people.thwaite).some((m) => m.key === 'lawthwaite') }));
  check('with a statement on his desk the sergeant offers to lose it', b1.pending && b1.matter, b1);
  const b2 = await L(() => ({ r: LEDGER.game.law.buyOfficer('thwaite', 'statement'), arrest: LEDGER.G.story.arrest, clean: LEDGER.G.money.clean }));
  check('Sergeant Thwaite loses the statement for fifty pounds: no constable comes', b2.r.does && !b2.arrest && b2.clean === 4000, b2);
  check('the witness whose statement was lost is not asked again for it', !(await L((id, e) => LEDGER.game.law.wouldState(id, e).goes, who.id, e7)));
  const b3 = await L(() => LEDGER.game.law.buyOfficer('thwaite', 'statement'));
  check('once: he will not do it a second time', !b3.does && !b3.crime, b3);
  const b4 = await L(() => LEDGER.game.law.buyOfficer('thwaite', 'car'));
  check('and he does nothing outside his limit', !b4.does, b4);
  const b5 = await L(() => ({ r: LEDGER.game.law.buyOfficer('pc', 'car'), arrest: LEDGER.G.story.arrest }));
  check('the rest of the station is unchanged: PC Ibbotson is offered a note and books it', b5.r.crime && b5.arrest && b5.arrest.cls === 'window', b5);
  await L(() => { LEDGER.G.story.arrest = null; });

  // ---- 2.6.9: the office searched, never without the sign the evening before (ER-SEARCHED-01)
  await L(() => { LEDGER.G.x.crime.office = ['a sawn-off bat', { name: 'the fare book', hot: false }, { name: 'the tin of night money' }]; });
  const s0 = await L(() => LEDGER.game.law.searchOffice());
  check('no search without notice', s0 === null);
  await L(() => { const x = LEDGER.G.x.law; x.office = { noticeT: null, done: false, found: [], wanted: 1 }; });
  await pass(await nextAt(18.1)); await h.step(2); await clear();
  x = await law();
  check('at investigating, notice is given at six the evening before, and he is told', x.office.noticeT != null && x.office.said === 1 && !x.office.done, x.office);
  await pass(await nextAt(9.1)); await h.step(2); await clear();
  x = await law();
  check('next morning the office is searched once and finds what is stored there', x.office.done && x.office.found.join('|') === 'a sawn-off bat|the tin of night money' && x.case.officeFinds === 2, x.office);
  check('what is not incriminating is left', (await L(() => LEDGER.G.x.crime.office.length)) === 1);

  // ---- 2.5.5 (A38): an unseen deed is found by the first routine that passes; the finder holds only the aftermath
  await pass(await nextAt(11)); await h.step(1); await clear();
  const spotP = await L(() => { const G = LEDGER.G; const P = G.named.find((p) => p.space === 'street' && !p.gone && p.awake && !p.def.police && !p.dead); return { id: P.id, x: P.x, z: P.z }; });
  await put(spotP.x + 3, spotP.z + 1);
  const e8 = await deed('shove', null, { set: { trace: true, what: 'a window put in' } });
  await h.step(0.3);
  await L(() => { const t = LEDGER.G.tom; t.x = 100; t.z = 60; });
  // her routine brings her past it (staged: she is stood two metres from what was left)
  await L((id, e) => { const G = LEDGER.G, P = G.people[id], E = G.ev[e]; P.x = E.x + 2; P.z = E.z + 0.5; P.route = null; P.hold = true; }, spotP.id, e8);
  await h.step(3); await pass(LEDGER.G.t + 3); await h.step(3);
  x = await law();
  const tr = x.traces.find((t) => t.e === e8);
  check('the first person whose routine passes the trace finds it', tr && tr.found && !!tr.found.who, [tr, (() => { const P = LEDGER.G.people[spotP.id]; return [P.id, P.x, P.z, P.space, P.gone, P.awake, P.dead, LEDGER.G.env.los(P.x, P.z, tr.x, tr.z)]; })()]);
  const fm = await L((who) => { const G = LEDGER.G, P = G.people[who]; const A = G.events.filter((E) => E.kind === 'law_found').pop(); const m = P.mind.by[A.id]; return { who: m && m.who, src: m && m.src, deed: !!P.mind.by[A.about] }; }, tr.found.who);
  check('the finder holds only the aftermath: what was left, never who did it', fm.who === 'man' && fm.src === 'saw' && !fm.deed, fm);
  check('found damage brings an officer to its spot, and no arrest without a name (ER-POL-01)', x.spots.some((s) => s.e === e8) && !(await L(() => LEDGER.G.story.arrest)));
  check('A36: the spot is watched ground until morning', x.spots.find((s) => s.e === e8).until === ((await L(() => Math.floor(LEDGER.G.t / 1440))) + 1) * 1440 + 6 * 60, x.spots.find((s) => s.e === e8));
  // a hidden or sunk body is never found; the missing man becomes the town's question; a body never cools
  const victim = await L(() => { const G = LEDGER.G; const P = G.named.find((p) => !p.def.police && !p.dead && (p.def.close || []).length && !['sheila', 'ron', 'darren', 'ada', 'pauline', 'hal'].includes(p.id)); return P.id; });
  const e9 = await L((v) => { const G = LEDGER.G; const id = LEDGER.act('kill', { silent: true, target: v }); G.people[v].dead = true; return id; }, victim);
  await h.step(0.5);
  await L((v) => LEDGER.game.law.bodyMoved(v, 'sunk'), victim);
  await L(() => { const t = LEDGER.G.tom; t.x = 100; t.z = 60; });
  await pass((await L(() => LEDGER.G.t)) + 26 * 60); await h.step(2); await clear();
  x = await law();
  const body = x.bodies.find((b) => b.id === victim);
  check('a sunk body is never found, whoever passes', body && body.sunk && !body.found && !x.traces.find((t) => t.e === e9).found, body);
  check('the man who stopped keeping his routine becomes the town\'s question within a day or so', x.missing[victim] && x.missing[victim].asked >= 1 && (await L(() => LEDGER.G.events.some((E) => E.kind === 'law_missing'))), x.missing[victim]);
  check('ER-POL-01 holds for a killing nobody can name: no arrest', !(await L(() => LEDGER.G.story.arrest)));

  // ---- 2.6.6: the dial's police
  const e10 = await deed('shove', null);
  const g0 = await L((e) => { LEDGER.G.x.dial = { state: 1 }; LEDGER.game.law.gunCall(e); return LEDGER.G.x.law.armed.calls; }, e10);
  const g2 = await L((e) => { LEDGER.G.x.dial = { state: 2 }; LEDGER.game.law.gunCall(e); const x = LEDGER.G.x.law; return { calls: x.armed.calls, lead: x.spots.filter((s) => s.armed).pop().from - Math.round(LEDGER.G.t) }; }, e10);
  check('no armed police until a shot has been fired in the town; then they come for gun calls, slowly', g0 === 0 && g2.calls === 1 && g2.lead === 25, { g0, g2 });
  await pass(await nextAt(11)); await h.step(0.5); await clear(); await put(4.5, 10, 3.14);
  await L(() => { const G = LEDGER.G; G.x.dial = { state: 3 }; G.x.law.armed.lastStopT = -1e9; G.tom.x = 4.5; G.tom.z = 10; G.x.crime.carried = ['a parcel']; LEDGER.game.law.beat.force(null); });
  await h.step(2);
  x = await law();
  check('at War there is stop and search on the street by day', x.armed.stops === 1 && (x.beat.stopSearch === 1 || x.beat.st !== 'off'), { stops: x.armed.stops, beat: x.beat.st });
  await L(() => { const G = LEDGER.G; G.x.dial = { state: 0 }; G.x.law.beat.stopSearch = 0; LEDGER.game.law.beat.force(false); });
  await h.step(1); await clear();

  // ---- the real town's hour comes down the same road
  const e11 = await deed('shove', null);
  await L(() => { const x = LEDGER.G.x.law; x.stage = 0; x.signs = []; LEDGER.G.story.arrest = null; LEDGER.G.x.town = { live: true }; });
  await h.step(0.3);
  check('once the real town runs, its cast is the town\'s to decide: the prototype rule stands back', (await L((e) => { LEDGER.game.law.plantWitness(e, 'hal'); LEDGER.G.people.hal.mind.regard = -0.5; return LEDGER.game.law.wouldState('hal', e); }, e11)).goes === false);
  const th = await L((e) => { LEDGER.game.emit('town:hour', { went: ['hal'], ellis: null, taken: null, found: [] }); return { stmt: LEDGER.G.ev[e].stmt, arrest: LEDGER.G.story.arrest }; }, e11);
  check("'town:hour' went: the statement is on record and the arrest is due, by the one road", th.stmt && th.stmt.includes('hal') && th.arrest && th.arrest.e === e11, th);
  const tk = await L(() => { LEDGER.game.emit('town:hour', { went: [], taken: 'Cautioned' }); const a = LEDGER.G.story.arrest; return { due: a.due <= LEDGER.G.t, outcome: a.outcome }; });
  check("'town:hour' taken: the constable comes now and the town's ending is used", tk.due && tk.outcome === 'cautioned', tk);
  await L(() => { LEDGER.G.story.arrest = null; LEDGER.G.x.town = { live: false }; });

  // ---- 2.5.4 (A37): three seen deeds on one street set it on edge; one does not
  const ed = await L((id) => {
    const G = LEDGER.G, x = G.x.law; x.deeds = {}; x.edge = {};
    const P = G.people[id]; P.dead = false;
    const mk = () => { const e = LEDGER.act('shove', { silent: true }); const E = G.ev[e]; E.zone = 'Quay Street'; E.wit.push(id); return e; };
    mk(); return 1;
  }, who.id);
  await h.step(0.5);
  const ed1 = await L(() => Object.keys(LEDGER.G.x.law.edge).length);
  await L((id) => { const G = LEDGER.G; for (let i = 0; i < 2; i++) { const e = LEDGER.act('shove', { silent: true }); G.ev[e].zone = 'Quay Street'; G.ev[e].wit.push(id); } }, who.id);
  await h.step(0.5);
  x = await law();
  check('one seen deed alone does not set a street on edge; three within two days do', ed1 === 0 && !!x.edge['Quay Street'], { ed1, edge: x.edge });
  await L(() => { LEDGER.G.x.law.walks.forEach((w) => { if (w.st === 'pending' || w.st === 'walking') w.st = 'dropped'; }); });

  const faults = await L(() => LEDGER.game.faults.slice());
  check('no fault in any system', faults.length === 0, faults.join(' || '));
  check('no page errors', h.errors.length === 0, h.errors.join(' || '));
} catch (e) {
  bad++;
  console.log('TEST FAIL ' + (e && e.stack || e));
}
function LEDGER_ok(a) { return a && a.cls === 'window' && a.officerSaw !== false; }
await h.close();
console.log(bad ? `FAIL: ${bad} checks failed` : 'PASS');
process.exit(bad ? 1 : 0);
