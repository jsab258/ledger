// LEDGER: a week on Quay Street. Boot, the frame loop, menus.
import { installHook } from './hook.js';
import { syncOpen } from './ledger.js';
import { visitStart, visitEnd, notedShown, activeAsk, askTick, measures } from './measures.js';
import { THREE } from './render/core.js';
import { initRenderer, frame, resize, setQuality, setInside, fx, benchmark } from './render/effects.js';
import { buildTown } from './render/town.js';
import { buildRooms, rooms } from './render/rooms.js';
import { G, resetState, day, hour, setPaused, PAUSE } from './state.js';
import { initEnv, simStep } from './clock.js';
import { initPeople, placeAll } from './routines.js';
import { townLevel } from './gossip.js';
import { ROOMS } from './map.js';
import { buildActors, syncActors } from './render/sync.js';
import { loadPeople, peopleInfo, buildCharR, poseCharR, poseClip } from './render/rig.js';
import {
  ui,
  initUI,
  hud,
  dialogTick,
  show,
  panel,
  closePanel,
  noted,
  titleMenu,
  loaded,
  loadMsg,
  fade,
  settingsHTML,
  bindSettings,
  sub,
  $,
  saveSettings,
  tickTimers,
} from './ui.js';
import { believedLine, ledgerHTML, drawMap, ledgerInput, ledgerClick, LS, PARTS } from './ledger_screen.js';
import { endHTML, reportText, playtestHTML, measuresHTML } from './end_screen.js';
import { pauseHTML, howHTML, creditsHTML, notesHTML, introLetter } from './design_notes.js';
import {
  FILES,
  hostDownloads,
  loadFileList,
  filesHTML,
  fileHTML,
  readFile,
  entryOf,
  saveName,
  saveFault,
  sourceZip,
} from './files_panel.js';
import {
  initPlayer,
  stepPlayer,
  stepCamera,
  titleCamera,
  cam,
  enterRoom,
  leaveRoom,
  snapCam,
  unlock,
  onKey,
  keys,
  pad,
} from './player.js';
import {
  initTraffic,
  stepTraffic,
  clearTraffic,
  spawnBusLeaving,
  exitPoint,
  cabFeel,
  footClear,
  streetThings,
} from './drive.js';
import { step as fightStep, F, block as fightBlock } from './fight.js';
import { RULES } from './rules.js';
import { initStory, newWeek, storyStep, endWeek } from './scenes.js';
import { passTime } from './work.js';
import { initTalk, checkTalk, talkLines, talkState, startTalk } from './talk.js';
import { initAudio, audioStep, sfx } from './audio.js';
import { initSave, saveNow, findSave, restore, saveWhere } from './saving.js';

let scene,
  camera,
  last = 0,
  time = 0,
  autoT = 0,
  saveInfo = null,
  bloods = [],
  bi = 0,
  prevPanel = null;
const cv = document.getElementById('c');

async function boot() {
  loadMsg('lettering the fascias');
  try {
    await Promise.race([
      Promise.all(
        [
          '700 20px Oswald',
          '400 20px "Alfa Slab One"',
          '900 20px "Playfair Display"',
          '600 20px Fredoka',
          '400 20px Yellowtail',
          '700 20px "Courier Prime"',
          '400 16px "Patrick Hand"',
        ].map((f) => document.fonts.load(f)),
      ),
      new Promise((r) => setTimeout(r, 2800)),
    ]);
  } catch (e) {
    /* fall back to system faces */
  }
  ({ scene, camera } = initRenderer(cv));
  loadMsg('laying the setts');
  await new Promise((r) => setTimeout(r, 30));
  buildTown(scene);
  buildRooms(scene);
  initEnv(() => cam.yaw);
  resetState();
  G.story.phase = 'title';
  G.t = 17.55 * 60;
  G.tom.space = 'away';
  G.tom.carry = null;
  G.weather.next = 1e9;
  loadMsg('waking the street');
  try {
    await Promise.race([
      loadPeople(G.settings.quality === 'low'),
      new Promise((_, rej) => setTimeout(() => rej(new Error('timed out')), 25000)),
    ]);
  } catch (e) {
    console.warn('People models unavailable, using the simple figures:', e && e.message);
  }
  initPeople();
  buildActors(scene);
  initTraffic(scene);
  initUI(camera);
  initPlayer(cv, camera);
  initStory();
  const bm = new THREE.MeshBasicMaterial({
    color: '#3a0606',
    transparent: true,
    opacity: 0.85,
    depthWrite: false,
    polygonOffset: true,
    polygonOffsetFactor: -6,
    polygonOffsetUnits: -6,
  });
  for (let i = 0; i < 26; i++) {
    const m = new THREE.Mesh(
      new THREE.CircleGeometry(0.16 + Math.random() * 0.22, 9).rotateX(-Math.PI / 2),
      bm,
    );
    m.visible = false;
    m.layers.set(1);
    scene.add(m);
    bloods.push(m);
  }
  Object.assign(G.hooks, {
    sfx,
    shake: (v) => {
      cam.shake = Math.max(cam.shake, v);
    },
    blood: (x, z) => {
      const m = bloods[bi++ % bloods.length];
      m.position.set(x + (Math.random() - 0.5) * 0.6, 0.14, z + (Math.random() - 0.5) * 0.6);
      m.visible = true;
    },
    save: () => saveNow(true),
    end: showEnd,
    enterRoom,
    leaveRoom,
    townLevel,
    doorOpen: () => {
      if (rooms.lockDoor) rooms.lockDoor.visible = false;
    },
    ambience: () => {},
    believed,
  });
  $('lbook').addEventListener('click', (e) => {
    const r = ledgerClick(e.target, G.settings.touch ? 'touch' : 'keyboard');
    if (r === 'close') closeLedger();
    else if (r) drawLedger();
  });
  Object.assign(ui.hooks, {
    sfx,
    pause: () => {
      prevPanel = null;
      panel(pauseHTML(), 'pause');
    },
    ledger: (device) => {
      if (ui.modal === 'ledger') return closeLedger();
      if (ui.modal === 'pause') closePanel();
      openLedger(typeof device === 'string' && device ? device : 'keyboard');
    },
    ledgerKey,
    measures: openMeasures,
    files: openFiles,
    titlefiles: openFiles,
    file: openFile,
    filecopy: copyFile,
    filesave: saveFile,
    fileszip: saveZip,
    notedShown: (n) => notedShown(n),
    back,
    settings: () => {
      panel(settingsHTML(), 'settings');
      bindSettings(onSetting);
    },
    how: () => panel(howHTML(), 'how'),
    playtest: () => {
      panel(playtestHTML(), 'playtest');
      bindPlaytest();
    },
    notes: () => {
      prevPanel = ui.modal === 'end' ? 'end' : null;
      panel(notesHTML(), 'notes');
    },
    credits: () => panel(creditsHTML(), 'credits'),
    save: () => {
      const ok = saveNow(true);
      const el = $('saved');
      if (el) el.textContent = ok ? 'Saved to ' + saveWhere() + '.' : 'Could not save here.';
    },
    skip: async (arg, b) => {
      if (!sure(b, arg === 'friday' ? 'jump to Friday' : 'jump to tomorrow morning')) return;
      closePanel();
      await passTime(
        arg === 'friday'
          ? Math.max(G.t + 5, 4 * 1440 + 16 * 60)
          : (hour() < 5 ? day() : day() + 1) * 1440 + 7.5 * 60,
        'Time passes.',
      );
    },
    finish: async (arg, b) => {
      if (!sure(b, 'end the week now')) return;
      closePanel();
      await endWeek(G.story.flags.choice || 'silent');
    },
    bench: () => {
      const el = $('bench');
      if (!el) return;
      el.textContent = 'Measuring...';
      setTimeout(() => {
        const r = benchmark();
        el.textContent = `${r.ms.toFixed(1)} ms a frame (${Math.round(1000 / r.ms)} a second) at ${r.w} by ${r.h} on ${G.settings.quality}: ${r.calls} draw calls, ${Math.round(r.tris / 1000)} thousand triangles. ${r.gpu.replace(/ANGLE \(|\)$/g, '').slice(0, 90)}`;
      }, 60);
    },
    talkcheck: () =>
      checkTalk((st, msg) => {
        const el = $('talkcheck');
        if (el) {
          el.textContent = msg;
          el.style.fontWeight = st === 'on' ? '700' : '400';
        }
      }),
    totitle: () => {
      saveNow(true);
      toTitle();
    },
    new: (arg, b) => {
      if (saveInfo && !sure(b, 'a new week replaces the saved one')) return;
      startNew();
    },
    cont: continueWeek,
    copy: copyReport,
    titlehow: () => {
      panel(howHTML(), 'how');
    },
    titlenotes: () => panel(notesHTML(), 'notes'),
    titlecredits: () => panel(creditsHTML(), 'credits'),
    titlesettings: () => {
      panel(settingsHTML(), 'settings');
      bindSettings(onSetting);
    },
  });
  addEventListener('resize', () => resize(false));
  initTalk();
  initSave().then(async () => {
    saveInfo = await findSave();
    if (G.story.phase === 'title') showTitle();
  });
  try {
    saveInfo = await findSave();
  } catch (e) {
    saveInfo = null;
  }
  showTitle();
  loaded();
  last = performance.now();
  requestAnimationFrame(loop);
  installHook({
    logic,
    files: { list: loadFileList, read: readFile, zip: sourceZip, open: openFiles, state: FILES },
    benchmark,
    rig: { peopleInfo, buildCharR, poseCharR, poseClip },
    scene,
    camera,
    THREE,
    cam,
    F,
    startNew,
    simStep,
    endWeek,
    passTime,
    reportText,
    saveNow,
    loadWeek,
    snapCam,
    openLedger,
    closeLedger,
    ledgerKey,
    padStep, // round 6: read the pad now (a test that steps the game by hand has no frames to do it)
    cabFeel,
    footClear,
    exitPoint,
    streetThings,
  });
}
// Round 6 (ER-SAVE-02, ER-CORE-03): no choice that cannot be undone is one press from Carry on. The first press
// only asks; the second, on the same button, does it.
function sure(b, what) {
  if (!b || !b.dataset || b.dataset.sure) return true;
  b.dataset.sure = '1';
  b.textContent = 'Sure? Press again to ' + what;
  return false;
}
// Tom comes to believe something new: one short line, low at the left
function believed(E, P, b) {
  if (G.story.phase !== 'play') return;
  const txt = believedLine(E, P, b);
  if (!txt) return;
  noted(txt);
  G.stats.noted = (G.stats.noted || 0) + 1;
  if (!G.ledger.hintL) {
    G.ledger.hintL = 1;
    sub('L opens the Ledger: what you believe the street knows.', '', 'over', 6);
  }
}
function back() {
  if (ui.modal === 'file') return openFiles();
  if (prevPanel === 'end') {
    prevPanel = null;
    return showEnd();
  }
  if (G.story.phase === 'title') {
    closePanel();
    show('title', true);
    setPaused(false, 'back at the title');
    return;
  }
  if (ui.modal === 'pause') return closePanel();
  if (G.story.phase === 'end') return showEnd();
  panel(pauseHTML(), 'pause');
}
function onSetting(k) {
  if (k === 'quality') setQuality(G.settings.quality);
  if (k === 'touch') show('touch', G.settings.touch && G.story.phase === 'play');
}
// ---------- the Ledger screen ----------
// Opens anywhere with L and closes with L or Esc. It pauses the game, or the talk or written line under it,
// and gives that back when it closes. It opens on the part last used.
let ledgerUnder = null;
function drawLedger() {
  const el = $('lbook');
  el.innerHTML = ledgerHTML();
  const cv = document.getElementById('lmap');
  if (cv) drawMap(cv);
  const cur = el.querySelector('.le.cur'),
    main = document.getElementById('lmain');
  if (cur && main) {
    const top = cur.offsetTop - main.offsetTop;
    if (top < main.scrollTop || top + cur.offsetHeight > main.scrollTop + main.clientHeight)
      main.scrollTop = Math.max(0, top - main.clientHeight / 3);
  }
  const page = el.querySelector('.lpg.on');
  if (page && page.scrollIntoView) page.scrollIntoView({ block: 'nearest' });
}
function openLedger(device = 'keyboard', part) {
  if (G.story.phase !== 'play' || ui.modal === 'ledger') return false;
  if (ui.modal && ui.modal !== 'talk' && ui.modal !== 'dialog') return false; // another panel is up
  if (PAUSE.busy > 0) return false; // mid-fade: time is passing
  ledgerUnder = ui.modal;
  G.ledgerNew = 0;
  G.stats.ledgerOpens = (G.stats.ledgerOpens || 0) + 1;
  if (PARTS.includes(part)) LS.part = part;
  else if (PARTS.includes(G.settings.ledgerPart)) LS.part = G.settings.ledgerPart;
  LS.cur = 0;
  LS.said = '';
  LS.jump = false;
  if (document.activeElement && document.activeElement.blur) document.activeElement.blur();
  unlock();
  ui.modal = 'ledger';
  setPaused(true, 'the Ledger is open');
  visitStart(device, ledgerUnder || 'play', LS.part);
  show('ledgerp', true);
  drawLedger();
  sfx('paper');
  return true;
}
function closeLedger() {
  if (ui.modal !== 'ledger') return;
  show('ledgerp', false);
  visitEnd();
  if (G.settings.ledgerPart !== LS.part) {
    G.settings.ledgerPart = LS.part;
    saveSettings();
  }
  ui.modal = ledgerUnder;
  ledgerUnder = null;
  setPaused(!!ui.modal || !!ui.inScene, 'the Ledger is closed');
  if (ui.modal === 'talk' && !G.settings.touch && !talkState().open) $('tin').focus();
  showAsk();
}
function ledgerKey(code, device) {
  if (ui.modal !== 'ledger') return;
  const r = ledgerInput(code, device);
  if (r === 'close') closeLedger();
  else if (r) drawLedger();
}
// The playtest ask slip on the play screen.
function showAsk() {
  const a = activeAsk(),
    el = $('ask');
  show('ask', !!a && G.story.phase === 'play');
  if (!a) return;
  el.classList.toggle('low', !!G.settings.eyes);
  el.innerHTML = `<b>PLAYTEST ASK</b>${a.question}<br>Open the Ledger [L] and mark the entry.`;
}
// Round 6 (the gate, ER-INPUT-03): a pad reaches the same verbs as the keys. The sticks and triggers are analogue
// and go to player.js; every button comes through onKey, the road the keyboard takes, so a pad can never do what a
// key cannot. In the Ledger it works as before: View opens and closes it, B closes, LB and RB change part, the
// D-pad moves, A marks, X strikes out.
//   on foot   left stick walk, right stick look, right trigger run, A use or talk (E), X the second thing (T),
//             Y the cab (F), B the coat (C), LB front up (Q), RB pick up (G), D-pad up take the fare (Y),
//             D-pad down held pass the time (Z)
//   the cab   left stick steer, right trigger drive, left trigger brake and reverse, A handbrake, Y get out,
//             D-pad up take the fare
//   a fight   X light blow (J), Y heavy blow (U), B held block (K), A dodge (Space), RB grab (G), LB step it up (R),
//             D-pad down back down (X), right stick pressed finish (V)
//   a written line: A reads on; D-pad up and down move along the choices, A takes the one in hand
//   a talk: Y suggested lines (Tab), D-pad up and down choose, A says it (Enter), B leaves (Esc)
//   Menu pauses and carries on; B closes any other box
const padWas = { block: false, wait: false };
const PAD_FOOT = { 0: 'KeyE', 2: 'KeyT', 3: 'KeyF', 1: 'KeyC', 4: 'KeyQ', 5: 'KeyG', 12: 'KeyY' },
  PAD_CAB = { 3: 'KeyF', 12: 'KeyY' },
  PAD_FIGHT = { 2: 'KeyJ', 3: 'KeyU', 0: 'Space', 5: 'KeyG', 4: 'KeyR', 13: 'KeyX', 11: 'KeyV' },
  PAD_FRONT = { 4: 'KeyR', 13: 'KeyX', 1: 'KeyX' },
  PAD_TALK = { 3: 'Tab', 12: 'ArrowUp', 13: 'ArrowDown', 0: 'Enter', 1: 'Escape' };
function padStep() {
  const pads = navigator.getGamepads ? navigator.getGamepads() : [];
  let seen = false;
  for (const gp of pads) {
    if (!gp || !gp.connected) continue;
    const held = (i) => !!(gp.buttons[i] && gp.buttons[i].pressed),
      value = (i) => (gp.buttons[i] ? gp.buttons[i].value || (gp.buttons[i].pressed ? 1 : 0) : 0),
      hit = (i) => {
        const down = held(i),
          k = gp.index + ':' + i,
          edge = down && !padWas[k];
        padWas[k] = down;
        return edge;
      };
    if (!seen) {
      // the sticks and triggers of the first pad, with a dead zone so a resting stick is still
      seen = true;
      const dz = (v, z) => (Math.abs(v || 0) < z ? 0 : (Math.sign(v) * (Math.abs(v) - z)) / (1 - z)),
        Z = RULES.pad;
      pad.x = dz(gp.axes[0], Z.stickDeadZone);
      pad.y = -dz(gp.axes[1], Z.stickDeadZone);
      pad.cx = dz(gp.axes[2], Z.stickDeadZone);
      pad.cy = dz(gp.axes[3], Z.stickDeadZone);
      pad.gas = dz(value(7), Z.triggerDeadZone);
      pad.brake = dz(value(6), Z.triggerDeadZone);
      pad.hb = G.tom.inCar && held(0);
      const any = pad.x || pad.y || pad.cx || pad.cy || pad.gas || pad.brake || gp.buttons.some((b) => b && b.pressed);
      if (any && !ui.pad) {
        ui.pad = true; // the prompts are drawn again with the pad's own button names (a key press turns them back)
        ui.pk = null;
      }
      // held things: B blocks in a fight, D-pad down passes the time on foot
      const fightOn = F.on && F.rung >= RULES.ladder.strikeRung;
      if (padWas.block !== (fightOn && held(1))) fightBlock((padWas.block = fightOn && held(1)));
      const waits = !ui.modal && !F.on && !G.tom.inCar && held(13);
      if (padWas.wait !== waits) keys.KeyZ = padWas.wait = waits;
    }
    const press = {};
    for (let i = 0; i < 16; i++) press[i] = hit(i);
    if (G.story.phase !== 'play') continue;
    if (ui.modal === 'ledger') {
      if (press[8] || press[1]) ledgerKey('KeyL', 'pad');
      else if (press[4]) ledgerKey('KeyQ', 'pad');
      else if (press[5]) ledgerKey('KeyE', 'pad');
      else if (press[12]) ledgerKey('ArrowUp', 'pad');
      else if (press[13]) ledgerKey('ArrowDown', 'pad');
      else if (press[14]) ledgerKey('ArrowLeft', 'pad');
      else if (press[15]) ledgerKey('ArrowRight', 'pad');
      else if (press[0]) ledgerKey('Enter', 'pad');
      else if (press[2]) ledgerKey('Backspace', 'pad');
      continue;
    }
    if (press[8]) {
      openLedger('pad');
      continue;
    }
    if (ui.modal === 'dialog') {
      // a written line: A reads on; with choices up, the D-pad moves along them and A takes the one in hand
      const opts = [...document.querySelectorAll('#dopts .opt')];
      let cur = opts.findIndex((o) => o.classList.contains('on'));
      if (opts.length && (press[12] || press[13] || cur < 0)) {
        cur = cur < 0 ? 0 : (cur + (press[13] ? 1 : opts.length - 1)) % opts.length;
        opts.forEach((o, i) => o.classList.toggle('on', i === cur));
      } else if (press[0]) onKey(opts.length ? 'Digit' + (cur + 1) : 'KeyE');
      continue;
    }
    if (ui.modal === 'talk') {
      for (const i in PAD_TALK) if (press[i]) onKey(PAD_TALK[i]);
      continue;
    }
    if (ui.modal) {
      if (press[1] || press[9]) onKey('Escape');
      continue;
    }
    if (press[9]) {
      onKey('Escape');
      continue;
    }
    const map = G.tom.inCar
      ? PAD_CAB
      : F.on
        ? F.rung >= RULES.ladder.strikeRung
          ? PAD_FIGHT
          : PAD_FRONT
        : PAD_FOOT;
    for (const i in map) if (press[i]) onKey(map[i]);
  }
  if (!seen && (pad.x || pad.y || pad.cx || pad.cy || pad.gas || pad.brake || pad.hb)) {
    // the pad has gone: nothing is held
    pad.x = pad.y = pad.cx = pad.cy = pad.gas = pad.brake = 0;
    pad.hb = false;
  }
}
// ---------- the measures screen ----------
function openMeasures() {
  prevPanel = ui.modal === 'end' ? 'end' : null;
  panel(measuresHTML(), 'measures');
  const out = document.getElementById('mjson'),
    exp = document.getElementById('mexport'),
    cp = document.getElementById('mcopy'),
    say = (t) => {
      const m = document.getElementById('mmsg');
      if (m) m.textContent = t;
    },
    showText = () => {
      out.value = JSON.stringify(measures(), null, 2);
      out.classList.remove('hidden');
      return out.value;
    };
  // A page here may not start a download itself: the host's save door is asked for, and the text can always be copied.
  hostDownloads().then((door) => {
    if (door || ui.modal !== 'measures' || !exp.isConnected) return;
    exp.classList.add('hidden');
    showText();
    say('This view cannot save a file. The JSON is below: copy it.');
  });
  exp.onclick = async () => {
    const text = showText(),
      door = await hostDownloads();
    if (!door) return say('This view cannot save a file. The JSON is below: copy it.');
    try {
      await door.save({ filename: 'ledger-measures.json', data: text });
      say('Saved as ledger-measures.json.');
    } catch (e) {
      say(saveFault(e) + ' The JSON is below.');
    }
  };
  cp.onclick = () => {
    const text = showText();
    out.select();
    copyText(text).then((ok) => say(ok ? 'Copied.' : 'Select the text below and copy it.'));
  };
}
// Copy from a click. True when the browser took it.
async function copyText(text) {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch (e) {
    return false;
  }
}

// ---------- the files published beside the page ----------
const fileSay = (t) => {
  const m = document.getElementById('fmsg');
  if (m) m.textContent = t;
};
async function openFiles() {
  if (ui.modal !== 'files' && ui.modal !== 'file') prevPanel = ui.modal === 'end' ? 'end' : null;
  panel(filesHTML(), 'files');
  await loadFileList();
  if (ui.modal !== 'files') return;
  panel(filesHTML(), 'files');
  const door = await hostDownloads(),
    zip = document.getElementById('fzip');
  if (door && zip && ui.modal === 'files') zip.classList.remove('hidden');
}
async function openFile(path) {
  fileSay('Reading ' + path + '...');
  try {
    const text = await readFile(path);
    if (ui.modal !== 'files' && ui.modal !== 'file') return;
    panel(fileHTML(path, text), 'file');
    const door = await hostDownloads(),
      save = document.getElementById('fsave');
    if (door && save) save.classList.remove('hidden');
  } catch (e) {
    fileSay('Could not read it here: ' + (e.message || e));
  }
}
function copyFile() {
  copyText(FILES.text).then((ok) => {
    if (!ok) {
      const pre = document.getElementById('ftext');
      if (pre) getSelection().selectAllChildren(pre);
    }
    fileSay(ok ? 'Copied.' : 'The text is selected: copy it with your own keys.');
  });
}
async function saveFile() {
  const door = await hostDownloads(),
    f = entryOf(FILES.shown);
  if (!door || !f) return fileSay('Saving is not available in this view. Copy the text instead.');
  try {
    const name = saveName(f.as);
    await door.save({ filename: name, data: FILES.text });
    fileSay('Saved as ' + name + '.');
  } catch (e) {
    fileSay(saveFault(e));
  }
}
async function saveZip() {
  const door = await hostDownloads();
  if (!door) return fileSay('Saving is not available in this view. Read or copy the files one at a time.');
  try {
    const zip = await sourceZip((i, n) => fileSay(`Gathering the files: ${i} of ${n}`));
    fileSay('Ready. Confirm the save.');
    await door.save({ filename: 'ledger-source.zip', data: zip });
    fileSay('Saved as ledger-source.zip.');
  } catch (e) {
    fileSay(e && e.code ? saveFault(e) : 'Could not gather the files: ' + ((e && e.message) || e));
  }
}
function bindPlaytest() {
  document.querySelectorAll('[data-pt]').forEach((el) => {
    el.oninput = () => {
      G.story.playtest = G.story.playtest || [];
      G.story.playtest[+el.dataset.pt] = el.value;
    };
    el.onchange = () => saveNow(false);
  });
}
async function copyReport() {
  const txt = reportText(),
    ta = $('report'),
    msg = $('copied');
  if (ta) {
    ta.classList.remove('hidden');
    ta.value = txt;
    ta.style.minHeight = '160px';
    ta.focus();
    ta.select();
  }
  try {
    await navigator.clipboard.writeText(txt);
    if (msg) msg.textContent = 'Copied. Paste it back into the chat.';
  } catch (e) {
    if (msg) msg.textContent = 'Select all in the box above and copy it by hand.';
  }
}
function showTitle() {
  const items = [];
  if (saveInfo)
    items.push({
      t: saveInfo.ended
        ? 'See how the week ended'
        : `Continue: ${['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'][Math.floor(saveInfo.t / 1440)] || 'the week'}`,
      act: 'cont',
    });
  items.push(
    { t: 'New week', act: 'new', alt: !!saveInfo },
    { t: 'How the town watches', act: 'titlehow', alt: 1 },
    { t: 'Settings', act: 'titlesettings', alt: 1 },
    { t: 'Design notes', act: 'titlenotes', alt: 1 },
    { t: 'Source and files', act: 'titlefiles', alt: 1 },
    { t: 'Credits', act: 'titlecredits', alt: 1 },
  );
  titleMenu(items, true);
}
function toTitle() {
  unlock();
  closePanel();
  G.story.phase = 'title';
  show('hud', false);
  show('touch', false);
  setInside(null);
  ui.roomName = null;
  clearTraffic();
  G.tom.space = 'away';
  G.tom.inCar = false;
  G.t = 17.55 * 60;
  G.weather.next = 1e9;
  setPaused(false, 'the title screen');
  placeAll();
  findSave().then((s) => {
    saveInfo = s;
    showTitle();
  });
  showTitle();
}
function waitClick(ms) {
  return new Promise((res) => {
    let done = false;
    const fin = () => {
      if (done) return;
      done = true;
      removeEventListener('pointerdown', fin);
      removeEventListener('keydown', fin);
      res();
    };
    setTimeout(() => {
      addEventListener('pointerdown', fin);
      addEventListener('keydown', fin);
    }, 600);
    setTimeout(fin, ms);
  });
}
async function startNew() {
  initAudio();
  titleMenu([], false);
  closePanel();
  setPaused(true, 'starting a new week');
  await fade(true, introLetter);
  await waitClick(15000);
  clearTraffic();
  newWeek();
  if (rooms.lockDoor) rooms.lockDoor.visible = true;
  bloods.forEach((b) => {
    b.visible = false;
  });
  const t = G.tom;
  t.x = -5.4;
  t.z = 27.5;
  t.ang = 0.6;
  t.space = 'street';
  setInside(null);
  ui.roomName = null;
  cam.yaw = 0.6;
  cam.pitch = 0.24;
  cam.dist = 5.4;
  snapCam();
  spawnBusLeaving();
  show('hud', true);
  show('touch', G.settings.touch);
  setPaused(false, 'the new week has started');
  await fade(false);
  sub('Quay Street. One suitcase. The bus does not wait.', '', 'over', 5);
}
// Put a saved week back: the state, then the people rebuilt around their restored memories (each mind gets its
// index again), then the room and the camera. Continue and the test hook both come through here.
function loadWeek(json) {
  clearTraffic();
  if (!restore(json)) return false;
  initPeople();
  G.story.phase = 'play';
  const t = G.tom,
    r = ROOMS[t.space];
  if (r) {
    setInside(r);
    ui.roomName = r.name;
    cam.yaw = Math.PI;
    cam.pitch = 0.62;
    cam.dist = 6.4;
  } else {
    t.space = 'street';
    setInside(null);
    ui.roomName = null;
    // Round 6 (ER-SAVE-02, ER-CORE-01): a week saved at the wheel comes back with Tom on his feet (a save holds no
    // fare and no traffic). He is put at the cab's door, not inside its body where no step would get him out.
    const c = G.car;
    if (Math.hypot(t.x - c.x, t.z - c.z) < RULES.tom.cabBodyRadiusMetres) {
      const [ex, ez] = exitPoint();
      t.x = ex;
      t.z = ez;
    }
  }
  snapCam();
  if (rooms.lockDoor) rooms.lockDoor.visible = !G.story.ended;
  show('hud', true);
  show('touch', G.settings.touch);
  return true;
}
async function continueWeek() {
  if (!saveInfo) return;
  initAudio();
  titleMenu([], false);
  setPaused(true, 'loading a saved week');
  await fade(true);
  if (!loadWeek(saveInfo.json)) {
    await fade(false);
    return showTitle();
  }
  setPaused(false, 'the saved week is loaded');
  await fade(false);
  if (G.story.ended) showEnd();
}
function showEnd() {
  unlock();
  G.story.phase = 'end';
  panel(endHTML(), 'end');
  bindPlaytest();
  fade(false);
}

let slowT = 0;
function logic(dt) {
  const ph = G.story.phase;
  tickTimers(dt); // fades and goodbyes: timed by the game's steps, so they end in a hidden tab and in a stepped test

  if (ph === 'title') {
    simStep(dt);
    stepTraffic(dt);
    return;
  }
  dialogTick(dt);
  if (!G.paused && ph === 'play') {
    G.played += dt;
    slowT += dt;
    if (slowT > 1) {
      // once a second: the Open part is brought up to date, and the next playtest ask is put when its moment comes
      slowT = 0;
      syncOpen();
      if (askTick(!ui.modal && !F.on && !G.tom.inCar && !G.story.fare)) showAsk();
    }
    stepPlayer(dt);
    const n = G.fast > 1 ? 4 : 1,
      sdt = (dt * G.fast) / n;
    for (let i = 0; i < n; i++) {
      simStep(sdt);
      storyStep(sdt);
      if (G.paused) break;
    }
    fightStep(dt);
    stepTraffic(dt * Math.min(G.fast, 3));
    autoT += dt;
    if (autoT > 75 && !F.on) {
      autoT = 0;
      saveNow(false);
    }
  }
}
function loop(now) {
  requestAnimationFrame(loop);
  const dt = Math.min(0.05, Math.max(0.001, (now - last) / 1000));
  last = now;
  time += dt;
  const ph = G.story.phase;
  if (!window.LEDGER_MANUAL) logic(dt);
  if (window.LEDGER_NORENDER) {
    // a test has switched the picture off: the words on screen still run
    if (ph !== 'title') hud(dt);
    padStep();
    return;
  }
  if (ph === 'title') titleCamera(time);
  else stepCamera(dt);
  if (window.LEDGER_CAM) {
    const k = window.LEDGER_CAM;
    camera.position.set(k[0], k[1], k[2]);
    camera.lookAt(k[3], k[4], k[5]);
    if (k[6]) {
      camera.fov = k[6];
      camera.updateProjectionMatrix();
    }
  }
  {
    const want =
      ph === 'play' && !G.tom.inCar ? Math.min(1, Math.max(0, G.tom.light == null ? 1 : G.tom.light)) : 0.8;
    fx.light += (want - fx.light) * Math.min(1, dt * 2.2);
  } // the corners lift in light and close in in shadow
  fx.hurt = ph === 'play' ? Math.max(0, G.tom.hurt - 0.25) * (0.75 + Math.sin(time * 5) * 0.25) : 0;
  syncActors(dt, camera);
  if (ph !== 'title') hud(dt);
  padStep();
  // A pause that nothing is holding (no box open, no scene running, no time passing) is a fault: it is logged
  // and the game goes on. See LEDGER.pauses().
  if (
    G.paused &&
    ph === 'play' &&
    !ui.modal &&
    !ui.inScene &&
    PAUSE.busy === 0 &&
    performance.now() - PAUSE.since > 3000
  ) {
    PAUSE.faults++;
    setPaused(false, 'FAULT: a pause nothing was holding (' + G.pauseWhy + ')');
  }
  audioStep(dt);
  frame(dt, time);
}
boot().catch((e) => {
  loadMsg('Could not start: ' + (e && e.message ? e.message : e));
  console.error(e);
});
