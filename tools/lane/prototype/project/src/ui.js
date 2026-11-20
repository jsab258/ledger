// The interface: carbon dockets, a street nameplate, typewritten slips. HUD, dialogue, talk panel, menus.
import { RULES } from './rules.js';
import { G, day, hour, setPaused, PAUSE } from './state.js';
import { money, hhmm, DAYS3, esc, cap, clamp } from './util.js';
import { NAMES } from './kinds.js';
import { townLevel } from './gossip.js';
import { heardCall, knownNames, hearName, learnName, heardNames } from './ledger.js';

import { lightWord } from './light.js';
import { toScreen } from './render/sync.js';
import { groundY } from './map.js';

const $ = (id) => document.getElementById(id);
export const ui = {
  modal: null,
  subs: [],
  bubs: [],
  hooks: {},
  camera: null,
  hudT: 0,
  wait: false,
  notes: [],
};
export const noted = (text) => {
  if (ui.notes.length < 40) ui.notes.push(text);
};
export const tomName = (P) => (P.anon ? cap(P.def.desc) : knownNames()[P.id] ? P.def.name : cap(P.def.desc));
const DATE = (d) => `${DAYS3[d % 7].toUpperCase()} ${15 + d} OCT 1990`;

export function initUI(camera) {
  ui.camera = camera;
  $('book').addEventListener('click', (e) => {
    const b = e.target.closest('[data-act]');
    if (b && ui.hooks[b.dataset.act]) ui.hooks[b.dataset.act](b.dataset.arg, b);
  });
  $('tmenu').addEventListener('click', (e) => {
    const b = e.target.closest('[data-act]');
    if (b && ui.hooks[b.dataset.act]) ui.hooks[b.dataset.act](b.dataset.arg, b);
  });
  $('dialog').addEventListener('click', (e) => {
    if (!e.target.closest('.opt')) advance();
  });
  try {
    Object.assign(G.settings, JSON.parse(localStorage.getItem('ledger.settings') || '{}'));
  } catch (e) {
    /* no storage */
  }
}
export function saveSettings() {
  try {
    localStorage.setItem('ledger.settings', JSON.stringify(G.settings));
  } catch (e) {
    /* no storage */
  }
}
export const show = (id, on) => $(id).classList.toggle('hidden', !on);

// ---------- HUD ----------
export function hud(dt) {
  // bubbles follow heads every frame
  const cam = ui.camera,
    box = $('bubbles');
  let html = '';
  if (!ui.modal || ui.modal === 'dialog') {
    const list = ui.bubs.slice();
    const eyes = !!G.settings.eyes;
    if (eyes)
      for (const P of G.named)
        if (P.mark && !P.gone && P.space === G.tom.space) list.push({ P, text: P.mark, cls: 'mark', t: 1 });
    if (eyes)
      for (const w of G.watch)
        if (w.noticed && !w.P.gone && w.P.space !== 'home')
          list.push({
            P: w.P,
            text: w.who === 'tom' ? '◉' : w.who === 'owner' ? '◐' : '○',
            cls: 'eye',
            t: 1,
            low: 1,
          });
    for (const b of list) {
      const P = b.P;
      if (P && (P.gone || (P.space !== G.tom.space && P.space !== 'home'))) continue;
      if (P && !b.cls && !inEarshot(P)) continue;
      const home = P && P.space === 'home' && P.win,
        x = P ? (home ? P.win.x : P.x) : b.x,
        z = P ? (home ? P.win.z : P.z) : b.z,
        y = P
          ? home
            ? P.win.y + 0.9
            : groundY(x, z) + (P.def.look ? P.def.look.h : 1.75) + (b.low ? 0.18 : 0.42)
          : b.y;
      const s = toScreen(x, y, z, cam);
      if (!s || s[0] < -50 || s[0] > innerWidth + 50) continue;
      html += `<div class="bub ${b.cls || ''}" style="left:${s[0].toFixed(0)}px;top:${s[1].toFixed(0)}px">${esc(b.text)}</div>`;
    }
  }
  box.innerHTML = html;
  for (let i = ui.subs.length - 1; i >= 0; i--) {
    const s = ui.subs[i]; // a subtitle's time runs down with the game's steps: see tickTimers
    // the one-shot (the smoke run's fault): a subtitle never outstays its time by more than a few seconds, whatever holds the game
    if (s.t <= 0 || performance.now() - s.born > (s.secs + RULES.game.feel.subtitleClearsAfterRealSecondsAtMost) * 1000) {
      s.el.remove();
      ui.subs.splice(i, 1);
    }
  }
  // the one-shot (the smoke run's fault): prompts never sit over subtitles: they stand clear above the lowest lines
  {
    const subs = $('subs'),
      pr = $('prompt');
    if (subs && pr) {
      const need = ui.subs.length ? subs.offsetHeight + (parseFloat(getComputedStyle(subs).bottom) || 0) + PROMPT_CLEARS_SUBTITLES_PX : 0;
      const want = need > PROMPT_BOTTOM_PX ? need + 'px' : '';
      if (pr.style.bottom !== want) pr.style.bottom = want;
    }
  }
  ui.hudT -= dt;
  if (ui.hudT > 0) return;
  ui.hudT = 0.2;
  const t = G.tom,
    h = hour(),
    w = G.weather;
  $('dday').textContent = DATE(day());
  $('dtime').textContent = hhmm(h);
  $('dwx').textContent =
    w.rain > 0.8
      ? 'heavy rain'
      : w.rain > 0.45
        ? 'rain'
        : w.rain > 0.15
          ? 'drizzle'
          : w.mist > 0.6
            ? 'mist'
            : 'overcast';
  $('dclean').textContent = money(G.money.clean);
  $('ddirty').textContent = money(G.money.dirty);
  $('zone').textContent = t.space !== 'street' && ui.roomName ? ui.roomName : t.zone;
  const lv = townLevel(),
    ey = !!G.settings.eyes;
  show('expo', ey);
  {
    const now = performance.now();
    if (ey && ui.eyeAt) G.stats.eyesSecs = (G.stats.eyesSecs || 0) + Math.min(5, (now - ui.eyeAt) / 1000);
    ui.eyeAt = ey ? now : 0;
  }
  $('called').innerHTML = ey
    ? lv
      ? `The street calls you <b>${NAMES[lv]}</b>`
      : 'The street does not know you yet'
    : t.inCar
      ? 'in the cab'
      : t.coat
        ? 'the coat is on'
        : '';
  // The Noted line: never over the subtitles and never while one shows; about four seconds; one in ten seconds
  // at most; when more than one thing is waiting they are said as a count.
  if (ui.notes.length && !ui.modal && !ui.subs.length && G.played >= (ui.noteHold || 0)) {
    const n = ui.notes.length,
      text = n > 1 ? `Noted in the Ledger: ${n} things` : ui.notes[0],
      el = $('noted'),
      ob = $('obj');
    ui.notes.length = 0;
    el.textContent = text;
    el.style.bottom = (ob && !ob.classList.contains('hidden') ? ob.offsetHeight : 0) + 34 + 'px';
    el.classList.add('on');
    const shown = (ui.noteN = (ui.noteN || 0) + 1);
    after(NOTED.notedLineShowsRealSeconds, () => {
      if (ui.noteN === shown) el.classList.remove('on');
    });
    ui.noteHold = G.played + NOTED.notedLineAtMostEveryRealSeconds; // seconds of play: the game is stopped while a box is open
    if (ui.hooks.notedShown) ui.hooks.notedShown(n, text);
  }
  if (ui.subs.length && $('noted').classList.contains('on')) $('noted').classList.remove('on'); // a subtitle has come up: the line gives way
  // subtitles ride above the talk box and the written line, so nothing in them is ever covered
  {
    const box = ui.modal === 'talk' ? $('talk') : ui.modal === 'dialog' ? $('dialog') : null,
      lift = box ? box.offsetHeight + 14 + 'px' : '0px';
    if (ui.lift !== lift) document.documentElement.style.setProperty('--lift', (ui.lift = lift));
  }
  const L = t.light || 0;
  $('mlight').style.width = (L * 100).toFixed(0) + '%';
  $('vlight').textContent = lightWord(L).toLowerCase();
  const nr = t.noiseR || 0;
  $('mnoise').style.width = clamp(nr / 30, 0, 1) * 100 + '%';
  $('vnoise').textContent = nr < 1.5 ? 'silent' : 'carries ' + nr.toFixed(0) + ' m';
  $('coatst').textContent = t.inCar ? 'IN THE CAB' : t.coat ? 'COAT ON' : t.hasCoat ? 'coat off' : '';
  const seen = G.watch
    .filter((x) => x.noticed)
    .sort((a, b) => b.c - a.c)
    .slice(0, 5);
  $('eyes').innerHTML = seen.length
    ? seen
        .map(
          (x) =>
            `<div class="e"><span>${esc(tomName(x.P))}</span><span class="k">${x.who === 'tom' ? 'knows you' : x.who === 'owner' ? "thinks it's you" : x.who === 'cab' ? 'sees the cab' : x.who === 'coat' ? 'sees a coat' : 'sees a stranger'}</span></div>`,
        )
        .join('')
    : '<div class="e"><span>nobody you can see</span></div>';
  show('hp', G.settings.healthBar);
  if (G.settings.healthBar) $('hp').firstElementChild.style.width = (1 - t.hurt) * 100 + '%';
  $('obj').innerHTML = G.story.objective
    ? `<b>${DAYS3[day() % 7].toUpperCase()} · TO DO</b>${esc(G.story.objective)}`
    : '';
  show('obj', !!G.story.objective && ui.modal !== 'talk');
  show('waitbar', ui.wait);
  if (ui.wait) $('waitbar').textContent = 'Passing the time. ' + hhmm(h);
}
// Round 6 (the gate): while a pad is in the hands the prompts name its buttons, not the keys.
const PAD_NAMES = { E: 'A', T: 'X', F: 'Y', C: 'B', Q: 'LB', G: 'RB', Y: 'D-pad up' };
const PROMPT_BOTTOM_PX = 168, // where the prompts stand by the page's own layout
  PROMPT_CLEARS_SUBTITLES_PX = 10;
export function setPrompts(list) {
  const k = list.map((p) => p.k + p.t).join('|');
  if (k === ui.pk) return;
  ui.pk = k;
  $('prompt').innerHTML = list
    .map((p) => `<div><kbd>${ui.pad ? PAD_NAMES[p.k] || p.k : p.k}</kbd>${esc(p.t)}</div>`)
    .join('');
}
// A line heard on the street. cls: 'face' when it is said to him about him, 'over' when overheard.
export function sub(text, who, cls = '', secs) {
  const el = document.createElement('div');
  el.className = 's ' + cls;
  el.innerHTML = (who ? `<b>${esc(who)}</b>` : '') + esc(text);
  $('subs').appendChild(el);
  const lasts = secs || clamp(2.2 + text.length * 0.055, 3, 9);
  ui.subs.push({ el, t: lasts, secs: lasts, born: performance.now() });
  while (ui.subs.length > 3) {
    ui.subs[0].el.remove();
    ui.subs.shift();
  }
}
const TALK_RULES = RULES.talk;
export function bubble(P, text, secs = 3.5) {
  // no empty bubbles; the same line from a second person within a few seconds stays unsaid
  if (!text || !String(text).replace(/[\s.…“”"']/g, '')) return;
  const now = Date.now(),
    seen = (ui.saidAt || (ui.saidAt = new Map())).get(text);
  if (seen && seen.P !== P && now - seen.at < TALK_RULES.sameBubbleQuietRealSeconds * 1000) return;
  ui.saidAt.set(text, { P, at: now });
  ui.bubs = ui.bubs.filter((b) => b.P !== P);
  ui.bubs.push({ P, text, t: secs });
}
// a bubble shows only for someone Tom could see and hear: in range and not behind a wall
function inEarshot(P) {
  const t = G.tom,
    home = P.space === 'home' && P.win,
    x = home ? P.win.x : P.x,
    z = home ? P.win.z : P.z,
    tx = t.inCar && G.car ? G.car.x : t.x,
    tz = t.inCar && G.car ? G.car.z : t.z;
  if (Math.hypot(x - tx, z - tz) > TALK_RULES.bubbleHeardWithinMetres) return false;
  return G.tom.space !== 'street' || !G.env || !G.env.los || G.env.los(tx, tz, x, z);
}
export function news(headline, sb = '') {
  const el = $('news');
  el.innerHTML = `<div class="m">Meridian Evening Mail</div><div class="d">${DATE(day())} · Late Final · 20p</div><div class="hl">${esc(headline)}</div>${sb ? `<div class="sb">${esc(sb)}</div>` : ''}`;
  el.classList.remove('hidden');
  el.style.opacity = 1;
  clearTimeout(ui.newsT);
  ui.newsT = setTimeout(() => {
    el.style.opacity = 0;
    setTimeout(() => el.classList.add('hidden'), 700);
  }, 5200);
  if (ui.hooks.sfx) ui.hooks.sfx('stamp');
}
export function fade(on, text = '') {
  const f = $('fade');
  f.textContent = text;
  f.style.opacity = on ? 1 : 0;
  return new Promise((r) => after(FADE_REAL_SECONDS, r));
}

const NOTED = RULES.ledger;

// ---------- the game's own timers ----------
// Anything the game's flow waits on (a fade, a goodbye before the talk box shuts) is timed by the game's own
// steps and not by the browser's timers. A browser holds its timers back in a tab that is not showing, by as much
// as a minute, which left the game paused. These run the same in a showing tab, a hidden one and a stepped test.
const FADE_REAL_SECONDS = 0.75;
const timers = [];
export function after(realSeconds, fn) {
  const t = { left: realSeconds, fn, done: false };
  timers.push(t);
  // The browser's own timer stands behind it, for a test that waits without stepping the game. Whichever comes
  // first runs it, once.
  setTimeout(() => fire(t), realSeconds * 1000 + 60);
}
function fire(t) {
  if (t.done) return;
  t.done = true;
  const i = timers.indexOf(t);
  if (i >= 0) timers.splice(i, 1);
  t.fn();
}
export function tickTimers(dt) {
  // the one-shot (the consequence checker's finding): a speech bubble's time runs with the game's own steps, as the
  // other timers here do, so it ends in a stepped test and in a hidden tab too, and never hangs over a head for hours
  for (let i = ui.bubs.length - 1; i >= 0; i--) {
    const b = ui.bubs[i];
    b.t -= dt;
    if (b.t <= 0) ui.bubs.splice(i, 1);
  }
  for (const s of ui.subs) s.t -= dt;
  for (const t of timers.slice()) {
    t.left -= dt;
    if (t.left <= 0) fire(t);
  }
}

// ---------- dialogue ----------
let dlg = null;
PAUSE.stillHeld = () => !!ui.modal || !!ui.inScene;
export const dialogNow = () => dlg;
function showLine(who, text, opts, res) {
  const P = G.people[who];
  if (P) {
    P.talking = true;
    heardCall(P);
  }
  $('dwho').textContent = P ? tomName(P) : who || '';
  $('dcall').textContent = '';
  if (P) {
    hearName(P, text);
    if (heardNames()[P.id]) learnName(P.id);
  }
  dlg = { who, P, text, i: 0, opts, res, done: false, t: 0 };
  $('dtxt').textContent = '';
  $('dopts').innerHTML = '';
  $('dmore').style.visibility = 'hidden';
  show('dialog', true);
  ui.modal = 'dialog';
  setPaused(true, 'a written line: ' + (who || 'narration'));
  if (ui.hooks.sfx) ui.hooks.sfx('paper');
}
export function dialogTick(dt) {
  if (!dlg || dlg.done) return;
  dlg.t += dt;
  const n = Math.min(dlg.text.length, Math.floor(dlg.t * 70));
  if (n !== dlg.i) {
    dlg.i = n;
    $('dtxt').textContent = dlg.text.slice(0, n);
    if (ui.hooks.sfx && n % 3 === 0) ui.hooks.sfx('tick');
  }
  if (n >= dlg.text.length) finishLine();
}
function finishLine() {
  dlg.done = true;
  $('dtxt').textContent = dlg.text;
  if (dlg.opts)
    $('dopts').innerHTML = dlg.opts
      .map((o, i) => `<button class="opt" data-i="${i}"><kbd>${i + 1}</kbd>${esc(o)}</button>`)
      .join('');
  else $('dmore').style.visibility = 'visible';
  $('dopts').onclick = (e) => {
    const b = e.target.closest('.opt');
    if (b) pickOpt(+b.dataset.i);
  };
}
export function pickOpt(i) {
  if (!dlg || !dlg.opts || i >= dlg.opts.length) return;
  const d = dlg;
  dlg = null;
  if (d.P) d.P.talking = false;
  d.res(i);
  afterLine();
}
export function advance() {
  if (!dlg) return;
  if (!dlg.done) return finishLine();
  if (dlg.opts) return;
  const d = dlg;
  dlg = null;
  if (d.P) d.P.talking = false;
  d.res();
  afterLine();
}
// A line said outside a written scene has nobody to close its box. Once it is answered, and nothing has followed
// it by the next moment, the box closes and the game goes on.
function afterLine() {
  after(0.05, () => {
    if (dlg || ui.inScene || ui.modal !== 'dialog') return;
    show('dialog', false);
    ui.modal = null;
    setPaused(false, 'a line outside a scene was answered');
  });
}
export const say = (who, text) => new Promise((res) => showLine(who, text, null, res));
export const choose = (who, text, opts) => new Promise((res) => showLine(who, text, opts, res));
// Run a scripted exchange with the world paused.
export async function scene(fn) {
  if (ui.inScene) return fn();
  ui.inScene = true;
  setPaused(true, 'a written scene');
  let r;
  try {
    r = await fn();
  } finally {
    ui.inScene = false;
    ui.sceneEndedAt = G.played; // the use key rests a moment after a scene (player.js)
    if (ui.modal === 'dialog') {
      show('dialog', false);
      ui.modal = null;
    }
    setPaused(!!ui.modal, 'the scene is over');
  }
  return r;
}

// ---------- talk panel ----------
export function openTalk(P, o) {
  $('twho').textContent = tomName(P);
  $('tcall').textContent = '';
  $('tlog').innerHTML = '';
  $('tai').textContent = o.note || '';
  show('talk', true);
  ui.modal = 'talk';
  setPaused(true, 'a talk with ' + P.id);
  P.talking = true;
  ui.talkP = P;
  $('tsend').onclick = () => {
    const v = $('tin').value.trim();
    if (ui.hooks.talkKey && ui.hooks.talkKey('Enter', v)) return;
    if (v) {
      $('tin').value = '';
      o.onSay(v);
    }
  };
  $('tbye').onclick = () => o.onBye();
  $('tlines').onclick = (e) => {
    const b = e.target.closest('.opt');
    if (b && ui.hooks.talkPick) ui.hooks.talkPick(+b.dataset.i);
  };
  $('tslip').onclick = () => ui.hooks.talkKey && ui.hooks.talkKey('F2');
  $('thint').textContent = G.settings.touch ? '' : 'Tab: suggested lines';
  setTalkLines([], false, 0);
  setTimeout(() => {
    try {
      $('tin').focus();
    } catch (e) {
      /* */
    }
  }, 50);
}
// Tom's suggested lines: his exact words, three at most, the one in hand marked
export function setTalkLines(lines, open, sel) {
  const el = $('tlines');
  el.innerHTML = open
    ? lines
        .map((l, i) => `<button class="opt${i === sel ? ' on' : ''}" data-i="${i}">${esc(l.text)}</button>`)
        .join('')
    : '';
  el.classList.toggle('hidden', !open || !lines.length);
  if (!G.settings.touch) {
    $('thint').textContent = open
      ? 'Up, Down: choose. Enter: say it. Tab: your own words. L: the Ledger'
      : 'Tab: suggested lines';
    if (ui.modal === 'talk') {
      if (open) $('tin').blur();
      else $('tin').focus();
    }
  }
}
export function setTalkSlip(html, on) {
  // on: unfolded. Folded, the slip is its heading and nothing more.
  const el = $('tslip');
  el.innerHTML = html;
  el.classList.toggle('hidden', !html);
  el.classList.toggle('folded', !on);
}
export const talkHead = () => {
  if (ui.talkP) $('twho').textContent = tomName(ui.talkP);
};
export function setTalkActs() {
  /* the chips are gone: suggested lines and decision lines replace them */
}
export function talkLine(cls, text) {
  const p = document.createElement('p');
  p.className = cls;
  p.textContent = text;
  $('tlog').appendChild(p);
  $('tlog').scrollTop = 1e6;
  return p;
}
export function talkBusy(on) {
  $('tsend').disabled = on;
  $('tin').disabled = on;
  if (!on)
    try {
      $('tin').focus();
    } catch (e) {
      /* */
    }
}
export function closeTalk() {
  show('talk', false);
  if (ui.talkP) ui.talkP.talking = false;
  ui.talkP = null;
  ui.modal = null;
  setPaused(!!ui.inScene, 'the talk is over');
}

// ---------- panels ----------
export function panel(html, name = 'panel') {
  $('book').innerHTML = html;
  $('book').scrollTop = 0;
  show('panel', true);
  ui.modal = name;
  setPaused(true, 'a panel is open: ' + name);
  if (G.story.phase === 'title') show('title', false);
}
export function closePanel() {
  show('panel', false);
  ui.modal = null;
  setPaused(!!ui.inScene, 'the panel is closed');
}
export function key(code) {
  // returns true when the interface used the key
  if (ui.modal === 'ledger') {
    if (ui.hooks.ledgerKey) ui.hooks.ledgerKey(code, 'keyboard');
    return true;
  }
  if (ui.modal === 'dialog') {
    if (code === 'KeyL' && ui.hooks.ledger) ui.hooks.ledger('keyboard');
    else if (code === 'KeyE' || code === 'Space' || code === 'Enter') advance();
    else if (/^Digit[1-9]$/.test(code)) pickOpt(+code.slice(5) - 1);
    return true;
  }
  if (ui.modal === 'talk') {
    if (code === 'Enter') $('tsend').click();
    else if (code === 'Escape') $('tbye').click();
    else if (code === 'KeyL' && document.activeElement !== $('tin') && ui.hooks.ledger)
      ui.hooks.ledger('keyboard');
    else if (ui.hooks.talkKey) ui.hooks.talkKey(code);
    return true;
  }
  if (ui.modal) {
    // the one-shot (the smoke run's fault): every panel, the pause menu first, can be worked by keys alone.
    // Up and down (or W and S, or Tab) move between its buttons; Enter, Space or E presses the one in hand.
    const book = $('book');
    const items = book ? [...book.querySelectorAll('button, [data-act], input, select')].filter((e) => !e.disabled && e.offsetParent !== null) : [];
    if (items.length && ui.modal !== 'file') {
      const at = items.indexOf(document.activeElement);
      const typing = document.activeElement && /^(INPUT|SELECT|TEXTAREA)$/.test(document.activeElement.tagName) && document.activeElement.type !== 'checkbox';
      if (code === 'ArrowDown' || code === 'Tab' || (code === 'KeyS' && !typing)) {
        items[(at + 1) % items.length].focus();
        return true;
      }
      if (code === 'ArrowUp' || (code === 'KeyW' && !typing)) {
        items[(at - 1 + items.length) % items.length].focus();
        return true;
      }
      if ((code === 'Enter' || ((code === 'Space' || code === 'KeyE') && !typing)) && at >= 0) {
        items[at].click();
        return true;
      }
    }
    // the hands-on run's fault: the key that opened the paper map or the standing page puts it away again
    if ((ui.modal === 'map' && code === 'Comma') || (ui.modal === 'reading' && code === 'Period')) {
      closePanel();
      return true;
    }
    if (code === 'Escape') {
      if (ui.modal !== 'end') {
        if ((G.story.phase === 'title' || ui.modal === 'file') && ui.hooks.back) ui.hooks.back();
        else closePanel();
      }
    }
    return true;
  }
  return false;
}
export function titleMenu(items, on) {
  show('title', on);
  if (on)
    $('tmenu').innerHTML = items
      .map(
        (i) =>
          `<button class="btn ${i.alt ? 'alt' : ''}" data-act="${i.act}" data-arg="${i.arg || ''}">${esc(i.t)}</button>`,
      )
      .join('');
}
export const loaded = () => show('load', false);
export const loadMsg = (t) => {
  $('loadmsg').textContent = t;
};

export function settingsHTML() {
  const s = G.settings,
    sel = (k, opts) =>
      `<select data-set="${k}">${opts.map((o) => `<option ${s[k] === o ? 'selected' : ''}>${o}</option>`).join('')}</select>`,
    chk = (k) => `<input type="checkbox" data-set="${k}" ${s[k] ? 'checked' : ''}>`,
    rng = (k, a, b) =>
      `<input type="range" data-set="${k}" min="${a}" max="${b}" step="0.05" value="${s[k]}">`;
  return `<h1>Settings</h1><h2>Picture</h2><label>Graphics quality ${sel('quality', ['low', 'medium', 'high'])}</label><label>Hold the frame rate by lowering resolution ${chk('autoRes')}</label><label>Bloom on lamps and windows ${chk('bloom')}</label><div class="row"><button class="btn alt" data-act="bench">Measure the frame time</button></div><p id="bench" style="font-size:13px;min-height:1.3em"></p>
  <h2>Play</h2><label>Show a small health bar ${chk('healthBar')}</label><label>Mouse sensitivity ${rng('sens', 0.3, 2.5)}</label><label>Invert vertical look ${chk('invertY')}</label><label>Touch controls ${chk('touch')}</label><label>Show the town's eyes (testing only) ${chk('eyes')}</label><label>Playtest asks: find a fact in the Ledger at set moments ${chk('asks')}</label><label>End screen: show the truth beside the Ledger (playtest view) ${chk('truthView')}</label>
  <h2>Live talk</h2><label>Let Claude voice what people say when you talk freely ${chk('liveTalk')}</label><p style="font-size:13px;margin:6px 0">The game always decides what happens. With this off, people answer in their written lines.</p><div class="row"><button class="btn alt" data-act="talkcheck">Check the live voices</button></div><p id="talkcheck" style="font-size:13px;min-height:1.3em"></p>
  <h2>Sound</h2><label>Volume ${rng('vol', 0, 1)}</label><label>Score ${rng('music', 0, 1)}</label><div class="row"><button class="btn" data-act="back">Back</button></div>`;
}
export function bindSettings(onChange) {
  $('book')
    .querySelectorAll('[data-set]')
    .forEach((el) => {
      el.onchange = el.oninput = () => {
        const k = el.dataset.set;
        G.settings[k] = el.type === 'checkbox' ? el.checked : el.type === 'range' ? +el.value : el.value;
        saveSettings();
        onChange(k);
      };
    });
}
export { $, DATE };
