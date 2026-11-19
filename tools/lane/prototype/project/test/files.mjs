// The files published beside the page: the game lists them, shows any of them as text, gathers them as one
// zip that unpacks into a folder that builds, and the measures export falls back to text where the host has
// no save door. Needs site/ (npm run publish-set).
import { launch, sleep } from './harness.mjs';
import fs from 'fs';
import { execSync } from 'child_process';
import crypto from 'crypto';
import os from 'os';
import path from 'path';
const SITE = process.env.SITE || 'site'; // the published set, written by tools/publish_set.mjs
let bad = 0;
const check = (name, ok, extra = '') => { if (!ok) bad++; console.log(`${ok ? 'ok  ' : 'FAIL'} ${name}${extra ? ' | ' + extra : ''}`); };

// 1. no save door (as in a plain browser tab)
let h = await launch({ port: 8821, dist: SITE });
await sleep(600);
await h.page.click('[data-act="titlefiles"]'); await sleep(900);
const list = await h.ev(() => ({ links: document.querySelectorAll('table.files button.link').length, rows: document.querySelectorAll('table.files tr').length, zipHidden: document.getElementById('fzip').classList.contains('hidden'), modal: LEDGER.ui.modal, paused: LEDGER.read().paused }));
check('the list opens from the title', list.modal === 'files' && list.links > 60 && list.rows > 80, JSON.stringify(list));
check('no save door: the zip button stays hidden', list.zipHidden);
await h.page.click('button.link[data-arg="source/src/seeing.js"]'); await sleep(700);
const one = await h.ev(() => ({ modal: LEDGER.ui.modal, text: document.getElementById('ftext').textContent.length, hasWitness: document.getElementById('ftext').textContent.includes('export function witness'), saveHidden: document.getElementById('fsave').classList.contains('hidden') }));
check('a source file is shown as text', one.modal === 'file' && one.hasWitness && one.text > 3000 && one.saveHidden, JSON.stringify(one));
await h.page.click('[data-act="files"]'); await sleep(500);
check('Back to the files gives the list again', (await h.ev(() => LEDGER.ui.modal)) === 'files');
await h.page.click('button.link[data-arg="NOT_DONE.md"]'); await sleep(600);
check('a document is shown as text', await h.ev(() => document.getElementById('ftext').textContent.includes('What could not be done')));
await h.page.click('[data-act="files"]'); await sleep(400); await h.page.click('[data-act="back"]'); await sleep(400);
check('Back gives the title again', await h.ev(() => !document.getElementById('title').classList.contains('hidden') && !LEDGER.ui.modal));
// the zip, built in the page, unpacked here and compared file by file
const b64 = await h.ev(async () => { const blob = await LEDGER.files.zip(); const u = new Uint8Array(await blob.arrayBuffer()); let s = ''; for (let i = 0; i < u.length; i += 32768) s += String.fromCharCode.apply(null, u.subarray(i, i + 32768)); return btoa(s); });
const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'ledger-zip-'));
fs.writeFileSync(dir + '/ledger-source.zip', Buffer.from(b64, 'base64'));
let unzip = '';
try { unzip = execSync(`cd ${dir} && unzip -q ledger-source.zip && unzip -l ledger-source.zip | tail -1`).toString().trim(); } catch (e) { unzip = 'unzip failed: ' + e.message.slice(0, 200); }
const sha = (f) => crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex');
const pairs = [['src/seeing.js', 'src/seeing.js'], ['src/render/town.js', 'src/render/town.js'], ['package.json', 'package.json'], ['tools/build.mjs', 'tools/build.mjs'], ['assets/people.jpg', 'assets/people.jpg'], ['dist/ledger.js', 'dist/ledger.js'], ['.prettierrc.json', '.prettierrc.json'], ['CHANGELOG.md', 'CHANGELOG.md']];
const same = pairs.filter(([a, b]) => fs.existsSync(`${dir}/ledger/${a}`) && sha(`${dir}/ledger/${a}`) === sha(b)).length;
check('the zip unpacks and its files are the repository\'s', same === pairs.length, `${unzip} | ${same} of ${pairs.length} compared the same | ${dir}`);
// the measures export with no door: the JSON is shown to copy
await h.newWeek();
await h.ev(() => LEDGER.ui.hooks.measures()); await sleep(500);
const m = await h.ev(() => { const t = document.getElementById('mjson'); let ok = false; try { ok = JSON.parse(t.value).about.includes('LEDGER'); } catch (e) { ok = false; } return { exportHidden: document.getElementById('mexport').classList.contains('hidden'), textShown: !t.classList.contains('hidden'), json: ok, said: document.getElementById('mmsg').textContent }; });
check('no save door: the measures JSON is shown to copy', m.exportHidden && m.textShown && m.json && /copy/.test(m.said), JSON.stringify(m));
if (h.errors.length) { bad++; console.log(' errors', h.errors.slice(0, 3)); }
await h.close();

// 2. with a stand-in for the host's save door
h = await launch({ port: 8822, dist: SITE, before: () => { window.__saved = []; window.claude = { use: async (n) => (n === 'downloads' ? { save: async (r) => { if (window.__decline) { const e = new Error('no'); e.code = 'declined'; throw e; } window.__saved.push({ filename: r.filename, bytes: r.data.size != null ? r.data.size : r.data.length }); return { status: 'saved' }; } } : null) }; } });
await sleep(600);
await h.page.click('[data-act="titlefiles"]'); await sleep(900);
check('with a save door the zip button shows', await h.ev(() => !document.getElementById('fzip').classList.contains('hidden')));
await h.page.click('#fzip');
await h.page.waitForFunction('window.__saved.length > 0', { timeout: 60000 }); await sleep(200);
const z = await h.ev(() => ({ saved: window.__saved[0], said: document.getElementById('fmsg').textContent }));
check('the zip goes through the save door', z.saved.filename === 'ledger-source.zip' && z.saved.bytes > 3e6 && /Saved/.test(z.said), JSON.stringify(z));
await h.page.click('button.link[data-arg="source/src/rules.js"]'); await sleep(700);
await h.page.click('#fsave'); await sleep(400);
const f1 = await h.ev(() => ({ saved: window.__saved[1], said: document.getElementById('fmsg').textContent }));
check('one file saves with a name the host takes', f1.saved && f1.saved.filename === 'rules.js.txt' && /Saved/.test(f1.said), JSON.stringify(f1));
await h.ev(() => { window.__decline = true; }); await h.page.click('#fsave'); await sleep(400);
check('a declined save says so', /declined/.test(await h.ev(() => document.getElementById('fmsg').textContent)));
await h.ev(() => { window.__decline = false; });
await h.page.click('[data-act="files"]'); await sleep(400); await h.page.click('[data-act="back"]'); await sleep(400);
await h.newWeek();
// in play: pause menu, Source and files, a file, and Esc steps back to the list
await h.ev(() => LEDGER.ui.hooks.files()); await sleep(600);
await h.ev(() => LEDGER.ui.hooks.file('README.md')); await sleep(600); // the mouse is held by the game here, so not a click
await h.key('Escape'); await sleep(500);
check('in play, Esc on a file goes back to the list', (await h.ev(() => LEDGER.ui.modal)) === 'files');
await h.key('Escape'); await sleep(300);
await h.ev(() => LEDGER.ui.hooks.measures()); await sleep(500);
await h.ev(() => document.getElementById('mexport').click()); await sleep(500); // the mouse is held by the game here
const m2 = await h.ev(() => ({ saved: window.__saved[window.__saved.length - 1], said: document.getElementById('mmsg').textContent }));
check('the measures export goes through the save door as one JSON file', m2.saved.filename === 'ledger-measures.json' && m2.saved.bytes > 200 && /Saved/.test(m2.said), JSON.stringify(m2));
if (h.errors.length) { bad++; console.log(' errors', h.errors.slice(0, 3)); }
await h.close();
console.log(bad ? 'FAIL' : 'PASS');
