// The town's eyes setting (testing only): off by default, and what switching it on shows.
import puppeteer from 'puppeteer-core';
import http from 'http'; import fs from 'fs'; import path from 'path';
const srv = http.createServer((q, r) => { const f = path.join(path.resolve('dist'), decodeURIComponent(q.url.split('?')[0])); fs.readFile(f, (e, d) => { if (e) { r.writeHead(404); r.end(); } else { r.writeHead(200, { 'content-type': f.endsWith('.js') ? 'text/javascript' : f.endsWith('.html') ? 'text/html' : 'application/octet-stream' }); r.end(d); } }); }).listen(8784);
const b = await puppeteer.launch({ executablePath: '/usr/bin/google-chrome', headless: 'new', args: ['--no-sandbox', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--window-size=1000,600'] });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
for (const eyes of [false, true]) {
  const p = await b.newPage(); await p.setViewport({ width: 1000, height: 600 }); const errs = []; p.on('pageerror', (e) => errs.push(String(e.stack || e).slice(0, 300)));
  await p.evaluateOnNewDocument((eyes) => { localStorage.setItem('ledger.settings', JSON.stringify(Object.assign({ quality: 'low', autoRes: false, vol: 0 }, eyes ? { eyes: true } : {}))); }, eyes);
  await p.goto('http://localhost:8784/index.html'); await p.waitForFunction('window.LEDGER && document.getElementById("load").classList.contains("hidden")', { timeout: 180000 });
  const has = await p.evaluate(() => { document.querySelector('#tmenu [data-act="titlesettings"]').click(); const el = document.querySelector('[data-set="eyes"]'); const r = el ? [el.checked, el.closest('label').textContent.trim()] : null; document.querySelector('#book [data-act="back"]').click(); return r; });
  await p.click('[data-act="new"]'); await sleep(3500); await p.mouse.click(500, 300); await sleep(1500); await p.mouse.click(500, 310); await sleep(2500);
  await p.evaluate(() => { const G = LEDGER.G; G.people.ron.mark = '!'; G.tom.x = 6.2; G.tom.z = 33; }); await sleep(4000);
  console.log('eyes', eyes, '| setting:', JSON.stringify(has), '| slip shown:', await p.evaluate(() => !document.getElementById('expo').classList.contains('hidden')), '| under the sign:', JSON.stringify(await p.evaluate(() => document.getElementById('called').textContent)), '| marks over heads:', await p.evaluate(() => document.querySelectorAll('#bubbles .mark, #bubbles .eye').length), '| secs counted:', await p.evaluate(() => (LEDGER.G.stats.eyesSecs || 0).toFixed(1)), '| report:', (await p.evaluate(() => LEDGER.reportText())).split('\n').find((l) => l.startsWith('Town')), '| errors', errs.length, errs[0] || '');
  await p.close();
}
await b.close(); srv.close();
