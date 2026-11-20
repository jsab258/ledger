// The hands-on run's blocker (20 Nov): he walks up from the ferry and may come late. Sheila sits on at her desk on
// the first day until she has looked him over, so the keys can always be had; the to-do line says where she is.
import { start } from './lib.mjs';
const t = await start({ port: 8876, atLanding: true });
const clear = () => t.ev(async () => { for (let i = 0; i < 30; i++) { const w = LEDGER.written.read(); if (!w.open) break; if (w.choices && w.choices.length) await LEDGER.written.choose(0); else await LEDGER.written.next(); } });
const at = async (hour) => { for (let k = 0; k < 60; k++) { const done = await t.ev((h) => { for (let i = 0; i < 20 && LEDGER.G.t < h * 60; i++) LEDGER.step(1); return LEDGER.G.t >= h * 60; }, hour); await clear(); if (done) break; } return t.ev(() => { const S = LEDGER.G.people.sheila; return { space: S.space, gone: !!S.gone, hour: (LEDGER.G.t / 60) % 24, keys: !!LEDGER.G.car.keys, tour: !!LEDGER.G.story.flags.tour }; }); };
const a = await at(19.5);
t.ok(a.space === 'mickeys' && !a.gone && !a.tour, 'at half past seven on the first evening Sheila is still at her desk', a);
const b = await at(23.2);
t.ok(b.space === 'mickeys' && !b.gone, 'and at ten past eleven', b);
await t.ev(() => { LEDGER.goTo({ xMetres: LEDGER.G.car.x + 1.6, zMetres: LEDGER.G.car.z }); LEDGER.G.car.keys = false; });
let p = null;
for (let k = 0; k < 6; k++) { await t.ev(() => { for (let i = 0; i < 30; i++) LEDGER.tick(1 / 60); }); await clear(); p = await t.ev(() => ({ p: LEDGER.prompts().map((x) => x.text), paused: LEDGER.G.paused, modal: LEDGER.ui.modal })); if (p.p.length) break; }
t.ok(p.p.some((x) => /locked/.test(x)), 'the cab without its keys says it is locked, at the cab', p);
await t.done();
