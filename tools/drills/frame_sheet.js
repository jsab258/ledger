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
