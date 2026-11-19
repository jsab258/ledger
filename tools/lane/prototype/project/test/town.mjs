// The town's harder turns, through the test hook, pass or fail. It checks what the first round's logic script
// only printed: being seen; the ladder stopping at a threat for the priest; the police coming next day and
// custody; Ada's invitation and tea; the second ask and Iveson's yard; DS Ellis asking the street; the lads
// setting on Tom at night and where he wakes; saving and loading; the run report.
// It moves Tom and the clock about by hand to reach each turn; the turns themselves run by the game's rules.
import { launch } from './harness.mjs';
import { driver } from './week_bot.mjs';

const h = await launch({ port: 8896, seed: +(process.env.SEED || 1990) }); // a fixed seed: the same turns every run
const { L, clear } = driver(h, { log: () => {} });
let bad = 0;
const check = (name, ok, extra = '') => { if (!ok) bad++; console.log(`${ok ? 'ok  ' : 'FAIL'} ${name}${extra ? ' | ' + String(extra).slice(0, 260) : ''}`); };
const put = (x, z, ang = 0) => L((x, z, ang) => { const t = LEDGER.G.tom; if (t.space !== 'street') LEDGER.leaveRoom(); t.inCar = false; t.x = x; t.z = z; t.ang = ang; LEDGER.cam.yaw = ang; }, x, z, ang);
const beside = (id, d = 1.6) => L((id, d) => { const G = LEDGER.G, P = G.people[id], t = G.tom; if (t.space !== 'street') LEDGER.leaveRoom(); t.inCar = false; t.x = P.x; t.z = P.z + d; t.ang = Math.PI; LEDGER.cam.yaw = Math.PI; return [P.space, !!P.gone]; }, id, d);
const pass = async (t) => { await L((t) => LEDGER.passTime(t), t); await clear(); };
const press = async (k, secs = 0.4) => { await L((k) => LEDGER.press(k), k); await h.step(secs); };
const F = () => L(() => ({ on: LEDGER.F.on, rung: LEDGER.F.rung, foes: LEDGER.F.foes.map((f) => f.P.id + ':' + f.st) }));
const flags = () => L(() => Object.assign({}, LEDGER.G.story.flags));
const stepUntil = async (test, secs = 3, max = 40) => { for (let i = 0; i < max; i++) { if (await L(test)) return true; await h.step(secs); } return L(test); };
try {
  await h.newWeek();
  await clear();
  await L(() => { const G = LEDGER.G, f = G.story.flags; f.tour = 1; G.car.keys = true; f.metRon = f.metDarren = f.metPauline = f.metJune = 1; for (const id of ['sheila', 'ron', 'darren', 'pauline']) { G.ledger.met[id] = 1; G.people[id].mind.fam = 0.85; } });

  // seen: the ferry landing late on Monday
  await pass(22.75 * 60); await h.step(1); await put(-47, 57.2, 3.14); await h.step(2);
  const w = await L(() => LEDGER.read().watching.map((x) => `${x.personId}:${x.takesHimFor}:${x.clarityZeroToOne}`));
  check('someone has Tom in sight on the landing at night', w.length > 0, w.join(' '));

  // the ladder and the priest: it stops at a threat, in front of people
  await pass(1440 + 11.2 * 60); await h.step(0.5);
  const at = await beside('walsh');
  await L(() => { const G = LEDGER.G; G.ledger.met.walsh = 1; G.story.flags.metWalsh = 1; G.people.walsh.mind.fam = 0.8; G.people.walsh.mind.regard = -0.3; });
  await h.step(0.3);
  await press('Q'); await press('R'); await press('R'); await press('R', 0.5);
  const lad = await F();
  const kinds = await L(() => LEDGER.G.events.slice(-3).map((e) => e.kind + '[' + e.wit.length + ' saw]'));
  check('fronting up to Father Walsh climbs to a threat', lad.on && lad.rung === 3, `walsh ${at} | rung ${lad.rung} | ${kinds.join(' ')}`);
  await press('R', 0.6);
  check('and no further: Tom does not lay hands on the priest', (await F()).rung === 3, 'rung ' + (await F()).rung);
  await press('X', 1); await clear();
  check('X walks away from it', !(await F()).on);

  // the police: somebody gave a statement, the constable comes the next day, custody takes hours
  await pass(2 * 1440 + 8.9 * 60); await h.step(0.5);
  const due = await L(() => LEDGER.read().story.policeComing);
  check('a statement was given: the police are due', !!due, JSON.stringify(due));
  await L(() => { LEDGER.G.story.flags.alison = 1; });
  await put(6.2, 20, 3.14);
  const t0 = await L(() => LEDGER.G.t);
  await stepUntil(() => LEDGER.ui.modal === 'dialog', 3, 60);
  const came = await L(() => LEDGER.ui.modal === 'dialog');
  await clear({ choice: 0 }); await h.sleep(2500); await h.step(1); await clear();
  const after = await L(() => ({ coming: LEDGER.read().story.policeComing, hoursGone: Math.round((LEDGER.G.t - 0) / 6) / 10, place: LEDGER.read().tom.place, paused: LEDGER.read().paused }));
  check('the constable came for him', came);
  check('custody took time and let him go', !after.coming && after.hoursGone * 60 - t0 > 60 && !after.paused, JSON.stringify(after) + ' from minute ' + Math.round(t0));

  // Ada: the invitation from her window on Wednesday
  await L(() => { LEDGER.G.t = 2 * 1440 + 14 * 60; }); await h.step(1); await put(-6.5, 32, -1.57); await h.step(1.5); await clear();
  check('Ada asks him to tea from her window', !!(await flags()).teaInvited, await L(() => { const P = LEDGER.G.people.ada; return [P.space, P.atWindow, P.awake].join(','); }));

  // the second ask, and yes
  await L(() => { LEDGER.G.t = 2 * 1440 + 16.6 * 60; }); await h.step(3); await clear();
  const via = (await flags()).ask1 === 'yes' ? 'ron' : 'darren';
  await L((id) => LEDGER.talk.open(id), via); await h.step(0.4);
  await clear({ answer: 'yes', proposal: 0 });
  check('the second ask is put and taken', (await flags()).ask2 === 'yes', 'through ' + via + ', ask2 ' + (await flags()).ask2);

  // Iveson's yard: front up, the yard lad steps in, it comes to blows and ends
  await pass(2 * 1440 + 19.05 * 60); await h.step(3); await clear(); // seven in the evening: Iveson is at his yard, and so is his lad
  await beside('dennis', 1.7); await h.step(0.4);
  await L(() => LEDGER.talk.open('dennis')); await h.step(0.4);
  await clear({ choice: 0, answer: 'yes' }); await h.sleep(200); await h.step(0.5);
  const y0 = await F();
  for (let i = 0; i < 5 && (await F()).rung < 5; i++) await press('R', 0.7);
  const y1 = await F();
  check('at the yard the ladder starts and climbs', y0.on || y1.on, `first ${JSON.stringify(y0)} then ${JSON.stringify(y1)}`);
  let blows = false;
  for (let i = 0; i < 60 && (await F()).on; i++) { await press(i % 4 === 3 ? 'Space' : 'J', 0.5); blows = blows || (await L(() => LEDGER.G.tom.hurt > 0 || (LEDGER.G.people.yardlad.hurt || 0) > 0)); }
  await h.sleep(2500); await h.step(1); await clear(); await h.sleep(1500); await h.step(1); await clear();
  const y2 = await L(() => ({ on: LEDGER.F.on, tomHurt: +LEDGER.G.tom.hurt.toFixed(2), yardLadHurt: +(LEDGER.G.people.yardlad.hurt || 0).toFixed(2), job3: LEDGER.G.story.flags.job3 || null, debt: LEDGER.G.debts.dennis, place: LEDGER.read().tom.place, paused: LEDGER.read().paused }));
  check('it came to blows with the yard lad, and it ended', blows && !y2.on && !y2.paused, JSON.stringify(y2));
  check('and the debt at the yard is settled by it', y2.job3 === 'done' && y2.debt.st !== 'open', `job ${y2.job3}, debt ${y2.debt.st}`);

  // tea at Ada's, late and bruised
  await L(() => { const G = LEDGER.G; if (G.tom.space !== 'street') LEDGER.leaveRoom(); G.t = 2 * 1440 + 20.3 * 60; G.tom.hurt = 0.3; }); await h.step(1);
  await put(-7.2, 30.6, -1.57); await h.step(0.5); await press('E', 0.5); await clear({ choice: 0 });
  check('he knocks at Ada\'s and tea is taken', ['late', 'yes'].includes((await flags()).tea), 'tea ' + (await flags()).tea);

  // DS Ellis on Thursday
  await pass(3 * 1440 + 9.9 * 60); await h.step(1);
  await L(() => { const G = LEDGER.G; G.story.arrest = null; G.story.flags.forceEllis = 1; for (const P of G.named) for (const m of P.mind.mem) m.heat = Math.max(m.heat, 0.7); });
  await put(6.2, 10, 3.14);
  await stepUntil(() => LEDGER.ui.modal === 'dialog', 3, 80);
  const ellis = await L(() => !!LEDGER.G.story.ellis);
  await clear({ choice: 2 });
  await stepUntil(() => LEDGER.G.named.filter((p) => p.mind.mem.some((m) => LEDGER.G.ev[m.e].kind === 'ellis_asked')).length >= 3, 3, 40);
  const asked = await L(() => LEDGER.G.named.filter((p) => p.mind.mem.some((m) => LEDGER.G.ev[m.e].kind === 'ellis_asked')).map((p) => p.id));
  check('DS Ellis comes, and word that he is asking gets about', ellis && asked.length >= 3, asked.join(','));

  // the lads at night on Copper Row
  await pass(3 * 1440 + 20.5 * 60);
  await L(() => { LEDGER.G.tom.hurt = 0; LEDGER.G.story.flags.ask1 = 'no'; LEDGER.G.story.flags.ladsDone = 0; }); await h.step(4);
  await put(5.6, -154.4, 0);
  let setOn = false;
  for (let i = 0; i < 20 && !setOn; i++) { await h.step(1); if (await L(() => LEDGER.read().paused && !LEDGER.F.on)) await clear(); setOn = await L(() => !!LEDGER.G.story.flags.ladsDone); }
  check('the lads set on him', setOn, await L(() => LEDGER.G.crowd.filter((p) => p.lad).map((p) => [p.gone, !!p.down, Math.round(p.x), Math.round(p.z)].join('/')).join(' ') + ' | ' + JSON.stringify({ ladder: LEDGER.F.on, paused: LEDGER.G.paused, space: LEDGER.G.tom.space, clock: LEDGER.read().clock, box: LEDGER.read().boxOpen, tom: [Math.round(LEDGER.G.tom.x), Math.round(LEDGER.G.tom.z)] })));
  for (let i = 0; i < 50 && (await F()).on; i++) await h.step(1);
  await h.sleep(2500); await h.step(1); await clear(); await h.sleep(1200); await h.step(1); await clear();
  const beat = await L(() => ({ place: LEDGER.read().tom.place, hurt: +LEDGER.G.tom.hurt.toFixed(2), note: (LEDGER.G.ledger.notes.slice(-1)[0] || {}).text, paused: LEDGER.read().paused }));
  check('beaten, he comes round at Rinaldi\'s, and the game goes on', /Rinaldi/.test(beat.place + ' ' + beat.note) && !beat.paused, JSON.stringify(beat));

  // saving and loading
  const rt = await L(() => { const G = LEDGER.G, before = [Math.round(G.t), G.events.length, Object.keys(G.minds).length, G.money.clean, LEDGER.ledger.book().length]; const ok = LEDGER.restore(LEDGER.saveText()); const G2 = LEDGER.G; return { ok, before, after: [Math.round(G2.t), G2.events.length, Object.keys(G2.minds).length, G2.money.clean, LEDGER.ledger.book().length] }; });
  check('a save loads back the same week', rt.ok !== false && JSON.stringify(rt.before) === JSON.stringify(rt.after), JSON.stringify(rt));
  check('the run report is written', (await L(() => LEDGER.reportText().length)) > 1000);
  check('no pause was left hanging', (await L(() => LEDGER.pauseFaults())) === 0);
} catch (e) { bad++; console.log('TEST FAIL', String(e.stack || e).slice(0, 700)); }
if (h.errors.length) { bad++; console.log(' errors', [...new Set(h.errors)].slice(0, 4).join('\n  ')); }
await h.close();
console.log(bad ? 'FAIL' : 'PASS');
process.exit(bad ? 1 : 0);
