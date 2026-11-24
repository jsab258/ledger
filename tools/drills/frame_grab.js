// Frame grabber for footage studies in the built-in browser pane (24 Nov 2026).
// Paste into the page (javascript_tool) on a YouTube watch page, with the pane's viewport
// set to 1600x900. one(t) seeks to t seconds, waits for the frame, draws it full size on a
// canvas over the page with the video time in yellow, and returns [time, readyState, centre
// pixel sum] (sum 0 = a black draw: repeat). Then take a screenshot.
// Known faults: (1) a screenshot can show the previous draw; trust the yellow label, never
// the call order. (2) The earlier multi-frame version (play/pause between seeks) drew black
// cells; seek-and-wait only. (3) The video is whatever quality YouTube streams (720p seen).
window.one = async (t) => {
  const v = document.querySelector('video');
  v.pause();
  v.currentTime = t;
  await new Promise((r) => v.addEventListener('seeked', r, { once: true }));
  for (let k = 0; k < 40 && v.readyState < 4; k++) await new Promise((r) => setTimeout(r, 250));
  await new Promise((r) => setTimeout(r, 1500));
  let c = document.getElementById('lsheet');
  if (!c) { c = document.createElement('canvas'); c.id = 'lsheet'; document.documentElement.appendChild(c); }
  c.width = 1600; c.height = 900;
  c.style.cssText = 'position:fixed;left:0;top:0;width:1600px;z-index:2147483647;background:#000';
  const g = c.getContext('2d');
  g.drawImage(v, 0, 0, 1600, 900);
  g.fillStyle = '#ff0'; g.font = 'bold 22px sans-serif';
  g.fillText(Math.floor(v.currentTime / 60) + ':' + String(Math.floor(v.currentTime % 60)).padStart(2, '0'), 8, 26);
  const d = g.getImageData(800, 450, 1, 1).data;
  return [v.currentTime, v.readyState, d[0] + d[1] + d[2]];
};
