// The files published beside the game's page: the source this page is built from, the build command,
// the changelog, the measures from one full week, and what could not be done.
// They are listed from files.json (written by tools/publish_set.mjs), read by fetch and shown as text,
// so they can be read from the game's own link. Where the host allows saving, all of them go in one zip.
import { esc } from './util.js';

export const FILES = { list: null, error: null, save: null, shown: null, text: '' };

// the host's "save a file" door, or null where this view has none
export async function hostDownloads() {
  if (FILES.save !== null) return FILES.save || null;
  let d = null;
  try {
    if (window.claude && window.claude.use) d = await window.claude.use('downloads');
  } catch (e) {
    d = null;
  }
  FILES.save = d || false;
  return d;
}

export async function loadFileList() {
  if (FILES.list) return FILES.list;
  try {
    const r = await fetch('files.json');
    if (!r.ok) throw new Error('files.json: ' + r.status);
    FILES.list = await r.json();
    FILES.error = null;
  } catch (e) {
    FILES.error = String(e.message || e);
  }
  return FILES.list;
}

const kb = (bytes) => (bytes < 1024 ? bytes + ' bytes' : Math.round(bytes / 1024) + ' KB');

export function filesHTML() {
  const L = FILES.list;
  if (!L)
    return `<h1>Source and files</h1><p>${
      FILES.error
        ? 'The list of files could not be read here (' + esc(FILES.error) + ').'
        : 'Reading the list of files...'
    }</p><div class="row"><button class="btn" data-act="back">Back</button></div>`;
  const groups = L.groups
    .map(
      (g) =>
        `<h2>${esc(g.name)}</h2>${g.note ? `<p>${esc(g.note)}</p>` : ''}<table class="files">${g.files
          .map(
            (f) =>
              `<tr><td>${
                f.text
                  ? `<button class="link" data-act="file" data-arg="${esc(f.path)}">${esc(f.as)}</button>`
                  : esc(f.as)
              }</td><td>${esc(f.what || '')}</td><td>${kb(f.bytes)}</td></tr>`,
          )
          .join('')}</table>`,
    )
    .join('');
  return `<h1>Source and files</h1>
  <p>Published beside this page on ${esc(L.published)}. This page is what the source below builds: <b>${esc(L.buildCommand)}</b> gives a ledger.js with the checksum ${esc(L.ledgerJsSha256.slice(0, 16))}... (the whole of it is in BUILD.md). Choose a file to read it here.</p>
  <div class="row"><button class="btn hidden" id="fzip" data-act="fileszip">Save all of it as one zip</button><button class="btn alt" data-act="back">Back</button></div><p id="fmsg" style="font-size:12px"></p>
  ${groups}
  <div class="row"><button class="btn alt" data-act="back">Back</button></div>`;
}

export function fileHTML(path, text) {
  const f = entryOf(path);
  return `<h1>${esc(f ? f.as : path)}</h1><p>${esc((f && f.what) || '')}</p>
  <div class="row"><button class="btn" data-act="files">Back to the files</button><button class="btn alt" data-act="filecopy">Copy this file</button><button class="btn alt hidden" id="fsave" data-act="filesave">Save this file</button></div><p id="fmsg" style="font-size:12px"></p>
  <pre class="src" id="ftext">${esc(text)}</pre>
  <div class="row"><button class="btn" data-act="files">Back to the files</button></div>`;
}

export function entryOf(path) {
  if (!FILES.list) return null;
  for (const g of FILES.list.groups) for (const f of g.files) if (f.path === path) return f;
  return null;
}
export const allFiles = () => (FILES.list ? FILES.list.groups.flatMap((g) => g.files) : []);

export async function readFile(path) {
  if (!entryOf(path)) throw new Error('not one of the published files');
  const r = await fetch(path);
  if (!r.ok) throw new Error(path + ': ' + r.status);
  FILES.shown = path;
  FILES.text = await r.text();
  return FILES.text;
}

// A file name the host will take: it saves txt, json, md, html and zip, so a .js or .mjs file gets .txt added.
export const saveName = (as) => {
  const base = as.split('/').pop();
  return /\.(txt|json|md|html)$/.test(base) ? base : base + '.txt';
};

// What to tell the player when a save does not happen.
export function saveFault(e) {
  const c = e && e.code;
  if (c === 'declined') return 'Not saved: the save was declined.';
  if (c === 'rate_limited') return 'Another save is still open. Try again in a moment.';
  if (c === 'rejected_extension' || c === 'extension_not_enabled')
    return 'This view does not save that kind of file. Copy the text instead.';
  if (c === 'too_large') return 'Too large to save from here.';
  return 'Saving is not available in this view. Copy the text instead.';
}

// ---------- one zip of everything, built in the page ----------
const CRC = (() => {
  const t = new Uint32Array(256);
  for (let n = 0; n < 256; n++) {
    let c = n;
    for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
    t[n] = c >>> 0;
  }
  return t;
})();
const crc32 = (u8) => {
  let c = 0xffffffff;
  for (let i = 0; i < u8.length; i++) c = CRC[(c ^ u8[i]) & 255] ^ (c >>> 8);
  return (c ^ 0xffffffff) >>> 0;
};
// files: [{ name, data: Uint8Array }]. Stored, not squeezed: every unzip reads it.
export function zipStore(files, when = new Date()) {
  const enc = new TextEncoder(),
    parts = [],
    central = [],
    time = (when.getHours() << 11) | (when.getMinutes() << 5) | (when.getSeconds() >> 1),
    date = ((when.getFullYear() - 1980) << 9) | ((when.getMonth() + 1) << 5) | when.getDate();
  let offset = 0;
  for (const f of files) {
    const name = enc.encode(f.name),
      crc = crc32(f.data),
      n = f.data.length,
      h = new DataView(new ArrayBuffer(30)),
      c = new DataView(new ArrayBuffer(46));
    h.setUint32(0, 0x04034b50, true);
    h.setUint16(4, 20, true);
    h.setUint16(6, 0x0800, true);
    h.setUint16(10, time, true);
    h.setUint16(12, date, true);
    h.setUint32(14, crc, true);
    h.setUint32(18, n, true);
    h.setUint32(22, n, true);
    h.setUint16(26, name.length, true);
    parts.push(new Uint8Array(h.buffer), name, f.data);
    c.setUint32(0, 0x02014b50, true);
    c.setUint16(4, 20, true);
    c.setUint16(6, 20, true);
    c.setUint16(8, 0x0800, true);
    c.setUint16(12, time, true);
    c.setUint16(14, date, true);
    c.setUint32(16, crc, true);
    c.setUint32(20, n, true);
    c.setUint32(24, n, true);
    c.setUint16(28, name.length, true);
    c.setUint32(42, offset, true);
    central.push(new Uint8Array(c.buffer), name);
    offset += 30 + name.length + n;
  }
  const centralBytes = central.reduce((a, b) => a + b.length, 0),
    end = new DataView(new ArrayBuffer(22));
  end.setUint32(0, 0x06054b50, true);
  end.setUint16(8, files.length, true);
  end.setUint16(10, files.length, true);
  end.setUint32(12, centralBytes, true);
  end.setUint32(16, offset, true);
  return new Blob([...parts, ...central, new Uint8Array(end.buffer)], { type: 'application/zip' });
}

// Every published file, fetched and laid out as the repository has it (the art goes back under assets/).
export async function sourceZip(onStep) {
  const out = [],
    all = allFiles();
  for (let i = 0; i < all.length; i++) {
    const f = all[i],
      r = await fetch(f.path);
    if (!r.ok) throw new Error(f.path + ': ' + r.status);
    out.push({ name: 'ledger/' + f.as, data: new Uint8Array(await r.arrayBuffer()) });
    if (onStep) onStep(i + 1, all.length);
  }
  return zipStore(out);
}
