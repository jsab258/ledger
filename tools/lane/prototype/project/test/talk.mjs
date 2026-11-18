// Live talk with a stand-in for the page's Claude: the Settings check, the on/off switch, and a real street conversation with streaming.
import puppeteer from 'puppeteer-core';
import http from 'http'; import fs from 'fs'; import path from 'path';
const root = path.resolve('dist');
const srv = http.createServer((q, r) => { const f = path.join(root, decodeURIComponent(q.url.split('?')[0])); fs.readFile(f, (e, d) => { if (e) { r.writeHead(404); r.end(); } else { r.writeHead(200, { 'content-type': f.endsWith('.js') ? 'text/javascript' : 'text/html' }); r.end(d); } }); }).listen(8769);
const b = await puppeteer.launch({ executablePath: '/usr/bin/google-chrome', headless: 'new', args: ['--no-sandbox', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--window-size=900,600'] });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const log = (...a) => console.log(...a);
async function run(mode) {
  const p = await b.newPage(); await p.setViewport({ width: 900, height: 600 });
  const errs = []; p.on('console', (m) => { const t = m.text(); if ((m.type() === 'error' || m.type() === 'warning') && !/404|GPU stall|fonts.g|ERR_|Automatic fallback|GroupMarker/.test(t)) errs.push(t.slice(0, 500)); }); p.on('pageerror', (e) => errs.push('PAGEERR ' + String(e.stack || e).slice(0, 900)));
  await p.evaluateOnNewDocument((mode) => {
    localStorage.setItem('ledger.settings', JSON.stringify({ quality: 'low', autoRes: false, vol: 0 })); window.LEDGER_NORENDER = true; window.CALLS = [];
    if (mode === 'none') return;
    const wait = (ms) => new Promise((r) => setTimeout(r, ms));
    const sample = async (input, opts = {}) => {
      window.CALLS.push({ kind: 'text', len: input.length, opts: Object.keys(opts).sort().join(','), head: input.slice(0, 60), hasRules: /ABSOLUTE CONTENT RULES/.test(input), hasChar: /CHARACTER: /.test(input) });
      if (mode === 'refuse') { const e = new Error('no'); e.code = 'not_granted'; throw e; }
      const full = mode === 'banned' ? 'Come down the boozer for a pint and we will talk.' : 'Nowt you need telling yet — keep the fare book straight. "Kettle is on".';
      for (let i = 12; i < full.length; i += 14) { await wait(15); if (opts.onText) opts.onText({ text: full.slice(0, i), delta: '' }); }
      return { text: full, truncated: false };
    };
    window.SUG = { follow: 'What makes you say that?', personal: 'How long have you worked the rank?' };
    sample.json = async (input, opts = {}) => { if (/"follow"/.test(input)) { window.CALLS.push({ kind: 'suggest', len: input.length, leak: /SECRET|CHARACTER:|regard|fear|memor/i.test(input), name: /Nowak|\bTom\b/.test(input.split('ABSOLUTE CONTENT RULES')[0] + (input.split('He knows ONLY')[1] || '')), who: (input.match(/as he knows them: (.*)\./) || [])[1] }); if (window.SUGWAIT) await wait(window.SUGWAIT); return window.SUG; }
      window.CALLS.push({ kind: 'json', len: input.length, opts: Object.keys(opts).sort().join(',') }); if (mode === 'refuse') { const e = new Error('no'); e.code = 'not_granted'; throw e; } await wait(10); return { intent: /quid|£/.test(input.split('Player typed:')[1] || '') ? 'bribe' : 'ask', topic: 'other', amount: 0, denies: false }; };
    window.claude = { use: async (n) => (n === 'sample' ? sample : null) };
  }, mode);
  await p.goto('http://localhost:8769/index.html');
  const ev = (fn, ...a) => p.evaluate(fn, ...a);
  await p.waitForFunction('window.LEDGER && document.getElementById("load").classList.contains("hidden")', { timeout: 120000 });
  // 1) Settings check from the title menu
  await ev(() => { document.querySelector('#tmenu [data-act="titlesettings"]').click(); }); await sleep(200);
  const has = await ev(() => !!document.querySelector('[data-act="talkcheck"]') && !!document.querySelector('[data-set="liveTalk"]'));
  await ev(() => document.querySelector('[data-act="talkcheck"]').click()); await sleep(900);
  log(mode, 'title check:', has, JSON.stringify(await ev(() => document.getElementById('talkcheck').textContent)));
  if (mode === 'ok') {   // switch off, check, switch on
    await ev(() => { const c = document.querySelector('[data-set="liveTalk"]'); c.checked = false; c.onchange(); document.querySelector('[data-act="talkcheck"]').click(); }); await sleep(300);
    log(mode, 'switched off:', JSON.stringify(await ev(() => document.getElementById('talkcheck').textContent)));
    await ev(() => { const c = document.querySelector('[data-set="liveTalk"]'); c.checked = true; c.onchange(); });
  }
  await ev(() => document.querySelector('#book [data-act="back"]').click()); await sleep(100);
  // 2) a street conversation
  await ev(() => { window.LEDGER_MANUAL = true; LEDGER.startNew(); }); await sleep(2600); await ev(() => dispatchEvent(new Event('pointerdown'))); await sleep(2200);
  await ev(() => LEDGER.step(1));
  await ev(() => { const G = LEDGER.G; G.story.flags.tour = 1; G.story.flags.metRon = 1; G.ledger.met.ron = 1; G.people.ron.mind.fam = 0.85; const P = G.people.ron, t = G.tom; t.x = P.x; t.z = P.z + 1.5; t.ang = Math.PI; LEDGER.cam.yaw = Math.PI; LEDGER.step(0.3); });
  await ev(() => { dispatchEvent(new KeyboardEvent('keydown', { code: 'KeyE' })); dispatchEvent(new KeyboardEvent('keyup', { code: 'KeyE' })); }); await sleep(200); await ev(() => LEDGER.step(0.2));
  const modal = await ev(() => LEDGER.ui.modal);
  if (modal === 'dialog') { for (let i = 0; i < 30 && (await ev(() => LEDGER.ui.modal)) === 'dialog'; i++) { await ev(() => { dispatchEvent(new KeyboardEvent('keydown', { code: 'KeyE' })); dispatchEvent(new KeyboardEvent('keyup', { code: 'KeyE' })); LEDGER.step(0.2); }); await sleep(40); }
    await ev(() => { dispatchEvent(new KeyboardEvent('keydown', { code: 'KeyE' })); dispatchEvent(new KeyboardEvent('keyup', { code: 'KeyE' })); }); await sleep(200); }
  log(mode, 'modal:', await ev(() => LEDGER.ui.modal), '| note:', JSON.stringify(await ev(() => (document.getElementById('tai') || {}).textContent || '')));
  const send = async (text) => { await ev((text) => { const i = document.getElementById('tin'); i.value = text; document.getElementById('tsend').click(); }, text); const seen = new Set(); for (let k = 0; k < 40; k++) { await sleep(25); const last = await ev(() => { const ps = document.querySelectorAll('#tlog p.npc'); return ps.length ? ps[ps.length - 1].textContent : ''; }); seen.add(last); if (!(await ev(() => document.getElementById('tin').disabled))) break; } return [...seen]; };
  const s1 = await send('What do people round here do of an evening?');
  log(mode, 'stream states:', s1.length, '| final:', JSON.stringify(s1[s1.length - 1]));
  const s2 = await send('Here is five quid for your trouble.');
  log(mode, 'second final:', JSON.stringify(s2[s2.length - 1]));
  if (mode === 'ok') {       // the follow-up call of its own, and the checks on what comes back
    await ev(() => { dispatchEvent(new KeyboardEvent('keydown', { code: 'Escape' })); LEDGER.step(0.2); LEDGER.talk.start('albert'); }); await sleep(200); log(mode, 'head before:', await ev(() => document.getElementById('twho').textContent), '| lines:', await ev(() => { dispatchEvent(new KeyboardEvent('keydown', { code: 'Tab' })); return LEDGER.talk.lines().map((l) => `[${l.job}] ${l.text}`).join(' / '); }));
    await ev(() => dispatchEvent(new KeyboardEvent('keydown', { code: 'Enter' }))); await sleep(400); log(mode, 'head after the greeting:', await ev(() => document.getElementById('twho').textContent));
    const lines = async () => { for (let k = 0; k < 50; k++) { await sleep(40); if (!(await ev(() => LEDGER.talk.state().busy))) break; } await sleep(250); return ev(() => LEDGER.talk.lines().map((l) => `[${l.job}${l.model ? ', model' : ''}] ${l.text}`).join(' / ')); };
    log(mode, 'lines after a reply:', await lines());
    const tryS = async (label, sug, wait) => { await ev((sug, wait) => { window.SUG = sug; window.SUGWAIT = wait || 0; }, sug, wait); await send('And what else is there to know?'); if (wait) await sleep(wait > 6000 ? 6600 : wait + 200); log(mode, 'check', label + ':', await lines()); };
    await tryS('too long', { follow: 'What exactly do you mean by that and who told you and when did they say it?', personal: '' });
    await tryS('his name', { follow: 'Why would they talk about Tom Nowak?', personal: 'Nowak is a Polish name, you know.' });
    await tryS('unheard name', { follow: 'Does Brenda Laverack say the same?', personal: 'Is Old Barker still about?' });
    await tryS('content rule', { follow: 'Fancy a pint down the pub after?', personal: '' });
    await tryS('decides a deal', { follow: 'Deal. I\'ll take it for forty quid.', personal: 'Tell them no from me.' });
    await tryS('good', { follow: 'Who was it told you that?', personal: 'Is the rank always this quiet?' });
    await tryS('seven seconds late', { follow: 'Is that how Mickey did it?', personal: '' }, 7000);
    log(mode, 'suggest calls:', JSON.stringify(await ev(() => window.CALLS.filter((c) => c.kind === 'suggest').slice(0, 2))), 'dropped', await ev(() => LEDGER.G.stats.sugDropped), 'kept', await ev(() => LEDGER.G.stats.sugLive));
  }
  log(mode, 'log:', JSON.stringify(await ev(() => [...document.querySelectorAll('#tlog p')].map((x) => x.className + ': ' + x.textContent.slice(0, 90)))));
  log(mode, 'stats:', JSON.stringify(await ev(() => ({ live: LEDGER.G.stats.live, fb: LEDGER.G.stats.fallback, talks: LEDGER.G.stats.talks }))), '| calls:', JSON.stringify(await ev(() => window.CALLS)));
  log(mode, 'errors:', errs.length ? errs : 'none');
  await p.close();
}
try { for (const m of ['ok', 'none', 'refuse', 'banned']) await run(m); } catch (e) { console.log('FAILED', e); }
await b.close(); srv.close();
