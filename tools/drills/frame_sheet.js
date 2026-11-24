// Contact sheet for footage studies in the built-in browser pane (24 Nov 2026).
// Paste into a YouTube watch page (javascript_tool) after each navigation (a page load drops it);
// set the pane's viewport to 1600x900 before the screenshot (the pane drops it when its width
// changes). sheet([t1..t12]) seeks to each time, waits for the frame, draws it into a 4 x 3
// grid (400 px cells) labelled with the video time in yellow, and returns
// [videoWidth, videoHeight, centre pixel sums] (a sum of 0 = a black or empty cell).
// Use a coarse sheet (every 30 s) to find an event, then a fine one (every 1 to 4 s).
// Known faults: a screenshot taken while the sheet still draws shows fewer cells; vertical
// shorts overflow the cells (cropped to 300 px tall).
window.sheet = async (ts) => {
  const v = document.querySelector('video'); v.muted = true; v.pause();
  let c = document.getElementById('lsheet');
  if (!c) { c = document.createElement('canvas'); c.id = 'lsheet'; document.documentElement.appendChild(c); }
  c.width = 1600; c.height = 900;
  c.style.cssText = 'position:fixed;left:0;top:0;width:1600px;z-index:2147483647;background:#000';
  const g = c.getContext('2d'); g.fillStyle = '#000'; g.fillRect(0, 0, 1600, 900);
  const res = [];
  for (let i = 0; i < ts.length; i++) {
    v.currentTime = ts[i];
    await new Promise((r) => v.addEventListener('seeked', r, { once: true }));
    for (let k = 0; k < 40 && v.readyState < 4; k++) await new Promise((r) => setTimeout(r, 200));
    await new Promise((r) => setTimeout(r, 900));
    const x = (i % 4) * 400, y = Math.floor(i / 4) * 300;
    const h = Math.min(300, 400 * v.videoHeight / v.videoWidth);
    g.drawImage(v, x, y, 400, h);
    g.fillStyle = '#ff0'; g.font = 'bold 20px sans-serif'; g.fillText(v.currentTime.toFixed(1), x + 4, y + 20);
    const d = g.getImageData(x + 200, y + Math.floor(h / 2), 1, 1).data; res.push(d[0] + d[1] + d[2]);
  }
  return [v.videoWidth, v.videoHeight, res];
};

// SAVED EVIDENCE (24 Nov 2026, after the RDR2 review failed five readings with nothing saved): the pane refuses a
// page's request to a local receiver ("Unsafe attempt to load URL http://127.0.0.1"), so pictures cannot be posted
// from the page. The pane's own screenshots are kept as files in the session's tool-results folder: draw the frame
// with its time label (one(t) above, or a canvas the pane's width), take a screenshot at scale 0.4, and copy that
// file to F:/LedgerTools/game-inputs/footage/<video id>/<t>-<label>.jpg with an index.json. The screenshot lags one
// draw: name each file by the yellow label in it, never by the call order. First used on KvZfR0IU9ms 1,102-1,293 s.

// RED SCAN (24 Nov 2026, 18:05): scanRed(t0, t1, step) runs in the background (call without await, then poll
// window.scan.rows / window.scan.done in calls under 40 s): each row [time, red pixels, white pixels] in the flag
// region (top-right 30% by 10.5%; red = R>170, G<70, B<70). Any row over 15 red is looked at with flags([...]),
// which draws the flag region itself at 2 x: the ammo counter turning red at zero gives about 100 red pixels too.
window.scanRed = async (t0, t1, step) => {
  const v = document.querySelector('video'); v.muted = true; v.pause();
  const c = document.createElement('canvas'); const W = v.videoWidth, H = v.videoHeight;
  const cw = Math.round(W * 0.30), ch = Math.round(H * 0.105); c.width = cw; c.height = ch;
  const g = c.getContext('2d', { willReadFrequently: true });
  window.scan = { done: false, rows: [] };
  for (let t = t0; t <= t1; t += step) {
    if (document.querySelector('.ad-showing')) { await new Promise((r) => setTimeout(r, 2000)); t -= step; continue; }
    v.currentTime = t;
    await Promise.race([new Promise((r) => v.addEventListener('seeked', r, { once: true })), new Promise((r) => setTimeout(r, 6000))]);
    for (let k = 0; k < 30 && v.readyState < 3; k++) await new Promise((r) => setTimeout(r, 200));
    await new Promise((r) => setTimeout(r, 250));
    g.drawImage(v, W - cw, 0, cw, ch, 0, 0, cw, ch);
    const d = g.getImageData(0, 0, cw, ch).data; let red = 0, wh = 0;
    for (let i = 0; i < d.length; i += 4) { if (d[i] > 170 && d[i + 1] < 70 && d[i + 2] < 70) red++; if (d[i] > 230 && d[i + 1] > 230 && d[i + 2] > 230) wh++; }
    window.scan.rows.push([Math.round(v.currentTime), red, wh]);
  }
  window.scan.done = true;
};
window.flags = async (ts) => {
  const v = document.querySelector('video'); v.muted = true; v.pause();
  let c = document.getElementById('lsheet');
  if (!c) { c = document.createElement('canvas'); c.id = 'lsheet'; document.documentElement.appendChild(c); }
  const W = v.videoWidth, H = v.videoHeight, cw = Math.round(W * 0.30), ch = Math.round(H * 0.105);
  c.width = 800; c.height = 100 * Math.ceil(ts.length / 2);
  c.style.cssText = 'position:fixed;left:0;top:0;width:800px;z-index:2147483647;background:#000';
  const g = c.getContext('2d'); g.fillStyle = '#000'; g.fillRect(0, 0, c.width, c.height);
  for (let i = 0; i < ts.length; i++) {
    v.currentTime = ts[i];
    await Promise.race([new Promise((r) => v.addEventListener('seeked', r, { once: true })), new Promise((r) => setTimeout(r, 6000))]);
    for (let k = 0; k < 30 && v.readyState < 3; k++) await new Promise((r) => setTimeout(r, 200));
    await new Promise((r) => setTimeout(r, 400));
    const x = (i % 2) * 400, y = Math.floor(i / 2) * 100;
    g.drawImage(v, W - cw, 0, cw, ch, x, y, 396, 96);
    g.fillStyle = '#ff0'; g.font = 'bold 16px sans-serif'; g.fillText(v.currentTime.toFixed(1), x + 4, y + 90);
  }
  return 'ok';
};

// HARE SCAN for KCD2 (24 Nov 2026, 18:50, first try, unvalidated): scanHare(t0, t1, step) counts red, orange, yellow
// and white pixels in the top-centre strip (42-58% wide, top 14%) where KCD2's behaviour indicator (the hare) sits;
// rows [time, red, orange, yellow, white] in window.hscan. First run on sLU3UQlw62o (88 h PS5 Pro longplay) at 30 s:
// orange hits at 1,350-1,500, 6,150, 6,330, 9,480 s, none looked at yet. Validate the colours on one hit before trusting.
window.scanHare = async (t0, t1, step) => {
  const v = document.querySelector('video'); v.muted = true; v.pause();
  const c = document.createElement('canvas'); const W = v.videoWidth, H = v.videoHeight;
  const x0 = Math.round(W * 0.42), cw = Math.round(W * 0.16), ch = Math.round(H * 0.14); c.width = cw; c.height = ch;
  const g = c.getContext('2d', { willReadFrequently: true });
  window.hscan = { done: false, rows: [] };
  for (let t = t0; t <= t1; t += step) {
    if (document.querySelector('.ad-showing')) { await new Promise((r) => setTimeout(r, 2000)); t -= step; continue; }
    v.currentTime = t;
    await Promise.race([new Promise((r) => v.addEventListener('seeked', r, { once: true })), new Promise((r) => setTimeout(r, 6000))]);
    for (let k = 0; k < 30 && v.readyState < 3; k++) await new Promise((r) => setTimeout(r, 200));
    await new Promise((r) => setTimeout(r, 200));
    g.drawImage(v, x0, 0, cw, ch, 0, 0, cw, ch);
    const d = g.getImageData(0, 0, cw, ch).data; let red = 0, orange = 0, yellow = 0, white = 0;
    for (let i = 0; i < d.length; i += 4) { const r = d[i], gg = d[i + 1], b = d[i + 2];
      if (r > 180 && gg < 70 && b < 70) red++; else if (r > 200 && gg > 100 && gg < 170 && b < 70) orange++;
      else if (r > 200 && gg > 180 && b < 90) yellow++; else if (r > 235 && gg > 235 && b > 235) white++; }
    window.hscan.rows.push([Math.round(v.currentTime), red, orange, yellow, white]);
  }
  window.hscan.done = true;
};

// MENU FILTER (24 Nov 2026, 23:20): KCD2 menus fill the frame's centre with parchment; share of beige pixels
// (R>150, G>130, B>90, 20<R-B<90, sampled every 4th pixel) in x 40-80%, y 30-70% reads 17-62% on menus, 0-6% in play;
// drop hare hits above 12% before looking (q6qsCaxOciw: 75 of 75 hits were menus).
// HARE BOX SCAN (KCD2, 24 Nov 2026, 20:30): scanHare(t0, t1, step) like scanRed, but counts pixels in the
// behaviour indicator's own box (top centre: x 42-58%, y 0-14%): yellow (R>170, G>130, B<90, R-G<70),
// orange (R>180, 70<=G<=130, B<70), red (R>170, G<70, B<70), white (all >215; the sky fills it, so unused).
// Rows [time, yellow, orange, red, white] in window.hs.rows; window.scanStop = true ends it. Calibrated on
// vyA2Nm1BHyw 1,000-1,064 s at 2 s against the by-eye reading: yellow 8-26 at the first notice (1,014-1,016),
// red 260 at the alarm (1,022), orange 87 (1,024), yellow 46-75 searching (1,028-1,048), red 109-149 once the
// guard has him (1,050+). Hit: yellow > 15, orange > 30 or red > 60; menus and adverts can hit too, so look
// at every hit's frame before reading it. Re-query the video each step (the player swaps it; a hidden pane
// unloads it: kick it with movie_player.seekTo(t, true) and playVideo()).
window.scanHare = async (t0, t1, step) => {
  window.scanStop = false; const c = document.createElement('canvas'); const g = c.getContext('2d', { willReadFrequently: true });
  window.hs = { done: false, rows: [] };
  for (let t = t0; t <= t1 && !window.scanStop; t += step) {
    try {
      const v = document.querySelector('video');
      if (!v || document.querySelector('.ad-showing') || !(v.duration > 0)) { await new Promise((r) => setTimeout(r, 2000)); t -= step; continue; }
      v.muted = true; v.pause(); v.currentTime = t;
      await Promise.race([new Promise((r) => v.addEventListener('seeked', r, { once: true })), new Promise((r) => setTimeout(r, 5000))]);
      for (let k = 0; k < 30 && v.readyState < 2; k++) await new Promise((r) => setTimeout(r, 150));
      const W = v.videoWidth, H = v.videoHeight, x0 = Math.round(W * 0.42), bw = Math.round(W * 0.16), bh = Math.round(H * 0.14);
      c.width = bw; c.height = bh; g.drawImage(v, x0, 0, bw, bh, 0, 0, bw, bh);
      const d = g.getImageData(0, 0, bw, bh).data; let y = 0, r = 0, o = 0, w = 0;
      for (let i = 0; i < d.length; i += 4) { const R = d[i], G = d[i + 1], B = d[i + 2];
        if (R > 170 && G > 130 && B < 90 && R - G < 70) y++; else if (R > 170 && G < 70 && B < 70) r++;
        else if (R > 180 && G >= 70 && G <= 130 && B < 70) o++; else if (R > 215 && G > 215 && B > 215) w++; }
      window.hs.rows.push([Math.round(v.currentTime), y, o, r, w]);
    } catch (e) { await new Promise((r) => setTimeout(r, 1000)); }
  }
  window.hs.done = true;
};
