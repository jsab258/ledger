// The talk slip, the subtitles and the Noted line must never cover one another. Checked at four window sizes,
// with the slip folded and unfolded, by reading the boxes off the page.
import { launch, sleep } from './harness.mjs';
const sizes = [[1280, 720], [1920, 1080], [1000, 600], [620, 820]];
let bad = 0;
for (const [W, H] of sizes) {
  const h = await launch({ port: 8801, width: W, height: H });
  try {
    await h.newWeek();
    await h.ev(() => { const f = LEDGER.G.story.flags; Object.assign(f, { tour: 1, metRon: 1, metDarren: 1 }); LEDGER.G.settings.slipOpen = false; });
    const boxes = () => h.ev(() => {
      const r = (el) => { if (!el || el.classList.contains('hidden') || !el.offsetParent && getComputedStyle(el).position !== 'fixed') return null; const b = el.getBoundingClientRect(); return b.width && b.height ? { l: Math.round(b.left), t: Math.round(b.top), r: Math.round(b.right), b: Math.round(b.bottom) } : null; };
      const hit = (a, b) => a && b && a.l < b.r && b.l < a.r && a.t < b.b && b.t < a.b;
      const subs = [...document.querySelectorAll('#subs .s')].map(r).filter(Boolean), slip = r(document.getElementById('tslip')), talk = r(document.getElementById('talk')), typing = r(document.querySelector('#talk .typing')), noted = document.getElementById('noted').classList.contains('on') ? r(document.getElementById('noted')) : null;
      return { subs: subs.length, slip, typing, slipFolded: document.getElementById('tslip').classList.contains('folded'), slipOverSubs: subs.some((s) => hit(s, slip)), talkOverSubs: subs.some((s) => hit(s, talk)), notedOverSubs: subs.some((s) => hit(s, noted)), slipBesideTyping: !!(slip && typing && (slip.r <= typing.l + 2 || slip.b <= typing.t + 2)), slipInsideTalk: !!(slip && talk && slip.l >= talk.l && slip.r <= talk.r && slip.b <= talk.b) };
    });
    // three subtitles on screen, then a talk
    await h.ev(() => { LEDGER.talk.open('ron', { free: true }); });
    await h.ev(() => { const P = LEDGER.G.people.darren; LEDGER.G.hooks.sfx && 0; });
    await h.ev(() => { const el = (t, w) => { const d = document.createElement('div'); d.className = 's'; d.innerHTML = '<b>' + w + '</b>' + t; document.getElementById('subs').appendChild(d); LEDGER.ui.subs.push({ el: d, t: 60 }); }; el('One suitcase. I saw you get off the bus, Nowak.', 'DARREN MILNER'); el('Heavier than it looks. Something is sewn in the hem.', ''); el('Boss. A word, when you have a minute.', 'RON KIRBY'); });
    await sleep(900);
    const folded = await boxes();
    if (W === 1280) await h.shot(`out/layout_${W}_folded.png`, 700);
    await h.ev(() => LEDGER.talk.key('F2')); await sleep(600);
    const open = await boxes();
    if (W === 1280) await h.shot(`out/layout_${W}_unfolded.png`, 700);
    // the Ledger opens over the talk with L once the suggested lines have the keys, and gives the talk back
    await h.ev(() => LEDGER.talk.key('Tab')); await h.key('KeyL'); await sleep(300);
    const led = await h.ev(() => [LEDGER.ui.modal, LEDGER.read().pausedBecause]);
    await h.key('KeyL'); await sleep(300);
    const back = await h.ev(() => [LEDGER.ui.modal, LEDGER.talk.state().open]);
    await h.ev(() => LEDGER.talk.key('F2'));
    const ok = folded.subs >= 3 && !folded.slipOverSubs && !folded.talkOverSubs && folded.slipFolded && !open.slipOverSubs && !open.talkOverSubs && !open.slipFolded && open.slipBesideTyping && open.slipInsideTalk && led[0] === 'ledger' && back[0] === 'talk' && back[1];
    if (!ok) bad++;
    console.log(`${W}x${H}: ${ok ? 'ok' : 'FAIL'} | folded: ${JSON.stringify({ subs: folded.subs, slipOverSubs: folded.slipOverSubs, talkOverSubs: folded.talkOverSubs, folded: folded.slipFolded })} | unfolded: ${JSON.stringify({ slipOverSubs: open.slipOverSubs, talkOverSubs: open.talkOverSubs, besideTyping: open.slipBesideTyping, insideTalk: open.slipInsideTalk, slip: open.slip, typing: open.typing })} | L over the talk: ${led.join(' / ')} -> ${back.join(' / ')}`);
  } catch (e) { bad++; console.log(`${W}x${H}: TEST FAIL`, String(e.stack || e).slice(0, 400)); }
  if (h.errors.length) { bad++; console.log(' errors', h.errors.slice(0, 3)); }
  await h.close();
}
console.log(bad ? 'FAIL' : 'PASS');
