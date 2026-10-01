"""PICTURES JUDGED ON THE PAGE ITSELF, on every approval page (Jafar, 30
September: Wednesday's pictures were too small to judge; and 1 October: "tap a
picture and it opens full-screen at its full resolution, pinch to zoom, swipe
to the next, close to return. No separate links."; CLAUDE.md, "PICTURES AT
FULL SIZE").

Every picture shown for judging is as wide as the page's column, one to a
row, never cropped. A tap opens the viewer: the picture full-screen at its own
full resolution, fitted to the screen first; pinch (or the mouse wheel) zooms
up to well past its own pixels, one finger (or the mouse) drags it about, a
double tap goes between the whole picture and its pixels one to one; a swipe
(or the arrow keys, or the side arrows) goes to the next or the one before,
through every picture on the page in order; Close (or Esc) returns to the page
where it was. A filmed face (an element with data-film-sprite, as
tools/day_page.py's speaking films are) opens the same way and plays with its
own sound. Nothing opens a link or a new tab.

Every page tool applies it to its template once:

    import page_pictures
    PAGE = page_pictures.apply(PAGE)

    python tools/page_pictures.py --selftest
"""
import sys

MARK = "PICTURES JUDGED ON THE PAGE (tools/page_pictures.py"

CSS = """
/* PICTURES JUDGED ON THE PAGE (tools/page_pictures.py, Jafar 30 September and 1 October) */
.capgrid,.cands,.pair{grid-template-columns:1fr!important}
.capgrid img,.pair img,.cands img,figure img{width:100%!important;height:auto!important;aspect-ratio:auto!important;object-fit:contain!important}
main img,section img,[data-film-sprite]{cursor:zoom-in}
.pv{position:fixed;inset:0;z-index:2147483000;background:#000;display:none;touch-action:none;overscroll-behavior:contain;-webkit-user-select:none;user-select:none}
.pv.on{display:block}
.pv .pv-stage{position:absolute;inset:0;overflow:hidden}
.pv .pv-hold{position:absolute;left:0;top:0;transform-origin:0 0;will-change:transform}
.pv .pv-hold img{display:block;max-width:none!important;width:auto!important;height:auto!important;-webkit-user-drag:none;pointer-events:none}
.pv .pv-film{background-repeat:no-repeat;pointer-events:none}
.pv .pv-bar{position:absolute;left:0;right:0;top:0;display:flex;align-items:center;justify-content:space-between;gap:12px;
  padding:calc(10px + env(safe-area-inset-top, 0px)) 12px 10px;background:linear-gradient(rgba(0,0,0,.75),rgba(0,0,0,0));color:#fff;font:600 14px/1.2 system-ui,sans-serif;pointer-events:none}
.pv .pv-bar *{pointer-events:auto}
.pv .pv-count{opacity:.85;font-variant-numeric:tabular-nums}
.pv .pv-close{min-width:88px;min-height:44px;border:1px solid rgba(255,255,255,.6);background:rgba(0,0,0,.55);color:#fff;font:700 15px/1 system-ui,sans-serif;border-radius:22px;cursor:pointer}
.pv .pv-cap{position:absolute;left:0;right:0;bottom:0;padding:10px 14px calc(12px + env(safe-area-inset-bottom, 0px));background:linear-gradient(rgba(0,0,0,0),rgba(0,0,0,.75));color:#fff;font:14px/1.35 system-ui,sans-serif;pointer-events:none}
.pv .pv-nav{position:absolute;top:50%;transform:translateY(-50%);width:48px;height:72px;border:0;background:rgba(0,0,0,.35);color:#fff;font:700 30px/1 system-ui,sans-serif;cursor:pointer}
.pv .pv-prev{left:0;border-radius:0 8px 8px 0}.pv .pv-next{right:0;border-radius:8px 0 0 8px}
.pv .pv-play{position:absolute;left:50%;bottom:calc(64px + env(safe-area-inset-bottom, 0px));transform:translateX(-50%);min-height:44px;padding:0 18px;border:1px solid rgba(255,255,255,.6);background:rgba(0,0,0,.55);color:#fff;font:700 15px/1 system-ui,sans-serif;border-radius:22px;display:none;cursor:pointer}
.pv.film .pv-play{display:block}
@media (hover:none){.pv .pv-nav{display:none}}
"""

JS = r"""
// PICTURES JUDGED ON THE PAGE (tools/page_pictures.py): a tap opens a picture
// full-screen at its own resolution; pinch or wheel to zoom, drag to look
// about, double tap for its pixels one to one, swipe or arrows for the next,
// Close or Esc to return. Filmed faces play with their own sound.
(function(){
  if (window.__pvReady) return; window.__pvReady = true;
  const mk = (tag, cls, text) => { const n = document.createElement(tag); if (cls) n.className = cls; if (text) n.textContent = text; return n; };
  const view = mk("div", "pv"); view.setAttribute("role", "dialog"); view.setAttribute("aria-label", "Picture, full screen");
  const stage = mk("div", "pv-stage"), hold = mk("div", "pv-hold");
  const bar = mk("div", "pv-bar"), count = mk("span", "pv-count"), close = mk("button", "pv-close", "Close");
  const cap = mk("div", "pv-cap"), prev = mk("button", "pv-nav pv-prev", "‹"), next = mk("button", "pv-nav pv-next", "›");
  const play = mk("button", "pv-play", "Play again");
  close.type = prev.type = next.type = play.type = "button";
  prev.setAttribute("aria-label", "The picture before"); next.setAttribute("aria-label", "The next picture");
  stage.append(hold); bar.append(count, close); view.append(stage, bar, cap, prev, next, play);
  (document.body || document.documentElement).append(view);

  let items = [], idx = 0, W = 1, H = 1, fit = 1, sc = 1, tx = 0, ty = 0, audio = null, raf = 0, film = null;
  const pts = new Map(); let pinch = null, drag = null, swipe = null, lastTap = 0;

  function collect(){
    return Array.from(document.querySelectorAll("img, [data-film-sprite]")).filter(e => !view.contains(e) && (e.tagName !== "IMG" || (e.currentSrc || e.src)));
  }
  function apply(){ hold.style.transform = "translate(" + tx + "px," + ty + "px) scale(" + sc + ")"; }
  function clampPan(){
    const vw = stage.clientWidth, vh = stage.clientHeight, w = W * sc, h = H * sc;
    tx = w <= vw ? (vw - w) / 2 : Math.min(0, Math.max(vw - w, tx));
    ty = h <= vh ? (vh - h) / 2 : Math.min(0, Math.max(vh - h, ty));
  }
  function fitNow(){ const vw = stage.clientWidth, vh = stage.clientHeight; fit = Math.min(vw / W, vh / H); sc = fit; tx = (vw - W * sc) / 2; ty = (vh - H * sc) / 2; apply(); }
  function zoomAt(s, cx, cy){
    const max = Math.max(fit * 8, 4), ns = Math.min(max, Math.max(fit, s));
    tx = cx - (cx - tx) * ns / sc; ty = cy - (cy - ty) * ns / sc; sc = ns; clampPan(); apply();
  }
  function stopFilm(){ if (audio) { audio.pause(); audio = null; } clearInterval(raf); film = null; }
  function frameOf(sp, i){
    i = Math.max(0, Math.min(sp.frames - 1, i)); const c = i % sp.cols, r = Math.floor(i / sp.cols);
    return (sp.cols > 1 ? c / (sp.cols - 1) * 100 : 0) + "% " + (sp.rows > 1 ? r / (sp.rows - 1) * 100 : 0) + "%";
  }
  function runFilm(){
    if (!film) return; stopAudioOnly();
    const sp = film.sp; audio = film.audio ? new Audio(film.audio) : null;
    const box = film.box; box.style.backgroundPosition = frameOf(sp, 0);
    // THE FILM'S CLOCK IS ITS SOUND; when the sound cannot play (no sound
    // device, or the browser refuses), its own timer, so the face still moves.
    const t0 = performance.now(), len = sp.frames / (sp.fps || 10);
    let silent = !audio;
    const now = () => silent ? (performance.now() - t0) / 1000 : audio.currentTime;
    const over = () => silent ? now() >= len : audio.ended;
    if (audio) { audio.play().catch(() => { silent = true; }); }
    // A plain timer, as the page's own player uses: animation frames stop in a hidden view.
    raf = setInterval(() => { if (film === null || film.box !== box) { clearInterval(raf); return; }
      if (over()) { clearInterval(raf); box.style.backgroundPosition = frameOf(sp, 0); return; }
      box.style.backgroundPosition = frameOf(sp, Math.floor(now() * sp.fps)); }, 33);
  }
  function stopAudioOnly(){ if (audio) { audio.pause(); audio = null; } clearInterval(raf); }
  function show(i){
    stopFilm(); idx = (i + items.length) % items.length; const el = items[idx];
    hold.replaceChildren(); view.classList.remove("film");
    count.textContent = (idx + 1) + " / " + items.length;
    cap.textContent = el.getAttribute("data-caption") || el.alt || el.getAttribute("aria-label") || "";
    if (el.tagName === "IMG") {
      const im = new Image(); im.alt = el.alt || ""; im.decoding = "async";
      im.onload = () => { W = im.naturalWidth || 1; H = im.naturalHeight || 1; fitNow(); };
      im.src = el.getAttribute("data-full") || el.currentSrc || el.src;
      hold.append(im); W = el.naturalWidth || 1; H = el.naturalHeight || 1; fitNow();
    } else {
      let sp = {}; try { sp = JSON.parse(el.getAttribute("data-film-sprite")); } catch (e) {}
      const box = mk("div", "pv-film"); const probe = new Image();
      box.style.backgroundImage = "url(" + sp.file + ")"; box.style.backgroundSize = (sp.cols * 100) + "% " + (sp.rows * 100) + "%";
      hold.append(box); view.classList.add("film");
      film = { sp, box, audio: el.getAttribute("data-film-audio") };
      probe.onload = () => { W = Math.round(probe.naturalWidth / sp.cols); H = Math.round(probe.naturalHeight / sp.rows);
        box.style.width = W + "px"; box.style.height = H + "px"; fitNow(); runFilm(); };
      probe.src = sp.file;
    }
  }
  function open(el){ items = collect(); const i = items.indexOf(el); if (i < 0) return;
    view.classList.add("on"); document.documentElement.style.overflow = "hidden"; show(i); close.focus({preventScroll:true}); }
  function shut(){ stopFilm(); view.classList.remove("on"); hold.replaceChildren(); document.documentElement.style.overflow = ""; }

  document.addEventListener("click", (e) => {
    if (view.contains(e.target)) return;
    const el = e.target.closest ? e.target.closest("img, [data-film-sprite]") : null;
    if (!el || (el.tagName === "IMG" && !(el.currentSrc || el.src))) return;
    if (el.closest("a")) e.preventDefault();
    open(el);
  }, true);
  close.addEventListener("click", shut);
  prev.addEventListener("click", () => show(idx - 1));
  next.addEventListener("click", () => show(idx + 1));
  play.addEventListener("click", runFilm);
  document.addEventListener("keydown", (e) => {
    if (!view.classList.contains("on")) return;
    if (e.key === "Escape") shut(); else if (e.key === "ArrowRight") show(idx + 1); else if (e.key === "ArrowLeft") show(idx - 1);
    else if (e.key === "+" || e.key === "=") zoomAt(sc * 1.5, stage.clientWidth / 2, stage.clientHeight / 2);
    else if (e.key === "-") zoomAt(sc / 1.5, stage.clientWidth / 2, stage.clientHeight / 2);
    else return; e.preventDefault();
  });
  stage.addEventListener("wheel", (e) => { e.preventDefault(); const r = stage.getBoundingClientRect(); zoomAt(sc * Math.exp(-e.deltaY * 0.0015), e.clientX - r.left, e.clientY - r.top); }, {passive:false});
  stage.addEventListener("pointerdown", (e) => {
    try { stage.setPointerCapture(e.pointerId); } catch (err) {}   // some browsers refuse; the pinch must not depend on it
    const r = stage.getBoundingClientRect(); pts.set(e.pointerId, {x: e.clientX - r.left, y: e.clientY - r.top});
    if (pts.size === 2) { const [a, b] = [...pts.values()]; pinch = {d: Math.hypot(a.x - b.x, a.y - b.y), s: sc}; drag = swipe = null; }
    else if (pts.size === 1) { const p = pts.get(e.pointerId); drag = {x: p.x, y: p.y, tx, ty}; swipe = {x: p.x, y: p.y, t: Date.now()}; }
  });
  stage.addEventListener("pointermove", (e) => {
    if (!pts.has(e.pointerId)) return; const r = stage.getBoundingClientRect(); pts.set(e.pointerId, {x: e.clientX - r.left, y: e.clientY - r.top});
    if (pinch && pts.size >= 2) { const [a, b] = [...pts.values()]; zoomAt(pinch.s * Math.hypot(a.x - b.x, a.y - b.y) / (pinch.d || 1), (a.x + b.x) / 2, (a.y + b.y) / 2); }
    else if (drag && sc > fit * 1.02) { const p = pts.get(e.pointerId); tx = drag.tx + p.x - drag.x; ty = drag.ty + p.y - drag.y; clampPan(); apply(); }
  });
  function lift(e){
    const p = pts.get(e.pointerId); pts.delete(e.pointerId);
    if (pts.size < 2) pinch = null;
    if (!p || pts.size) return;
    if (swipe && sc <= fit * 1.02) {
      const dx = p.x - swipe.x, dy = p.y - swipe.y, dt = Date.now() - swipe.t;
      if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.5 && dt < 800) { show(idx + (dx < 0 ? 1 : -1)); swipe = drag = null; return; }
    }
    if (swipe && Math.hypot(p.x - swipe.x, p.y - swipe.y) < 10) {
      const now = Date.now();
      if (now - lastTap < 320) { lastTap = 0; if (sc > fit * 1.02) fitNow(); else zoomAt(Math.max(1, fit * 2.5), p.x, p.y); }
      else lastTap = now;
    }
    swipe = drag = null;
  }
  stage.addEventListener("pointerup", lift); stage.addEventListener("pointercancel", lift);
  window.addEventListener("resize", () => { if (view.classList.contains("on")) fitNow(); });
})();
"""


def apply(page):
    """The template with the viewer: the styles before the first </style>,
    the script before the last </script>. Applied twice, once; a page built
    with the earlier full-size view gets this one in its place."""
    css_mark, js_mark = "/* " + MARK, "// " + MARK
    if css_mark in page and js_mark in page:
        return page
    old_css = page.find("/* PICTURES AT FULL SIZE (tools/page_pictures.py")
    if old_css >= 0:
        end = page.find(".fullsize .fullhint", old_css)
        end = page.find("}", end) + 1 if end >= 0 else -1
        if end > 0:
            page = page[:old_css] + page[end:]
    old_js = page.find("// PICTURES AT FULL SIZE (tools/page_pictures.py)")
    if old_js >= 0:
        end = page.find("})();", old_js)
        if end > 0:
            page = page[:old_js] + page[end + len("})();"):]
    # EACH HALF ON ITS OWN: a page that borrows another page's styles has the
    # viewer's styles already and still needs its script (the day page had
    # the styles and no script, so a tap did nothing; 1 October).
    if css_mark not in page:
        s = page.find("</style>")
        page = (page[:s] + CSS + page[s:]) if s >= 0 else ("<style>" + CSS + "</style>\n" + page)
    if js_mark not in page:
        e = page.rfind("</script>")
        page = (page[:e] + JS + page[e:]) if e >= 0 else (page + "\n<script>" + JS + "</script>\n")
    return page


def selftest():
    ok = bad = 0

    def check(name, cond):
        nonlocal ok, bad
        if cond:
            ok += 1
        else:
            bad += 1
            print("page_pictures selftest FAIL " + name)
    t = "<style>a{}</style><main></main><script>let x=1;</script>"
    out = apply(t)
    check("the styles go inside the style block", out.index(".pv{") < out.index("</style>"))
    check("the script goes inside the last script block", out.index("function show(i)") < out.rindex("</script>"))
    check("applied twice is applied once", apply(out) == out)
    check("pinch, swipe, wheel, double tap, keys and close are all there",
          all(k in JS for k in ("pinch", "swipe", "wheel", "lastTap", "Escape", "ArrowRight", "shut()")))
    check("nothing opens a link or a new tab", "window.open" not in JS and "target=" not in JS and "location" not in JS)
    old = ("<style>a{}\n/* PICTURES AT FULL SIZE (tools/page_pictures.py, Jafar 30 September) */\n.fullsize{x}\n"
           ".fullsize .fullhint{y}\n</style><script>let x=1;\n// PICTURES AT FULL SIZE (tools/page_pictures.py): a\n(function(){ z })();\n</script>")
    up = apply(old)
    check("a page with the earlier view gets this one in its place", ".fullsize" not in up and up.count(MARK) == 2)
    borrowed = "<style>a{}" + CSS + "</style><main></main><script>let x=1;</script>"
    got = apply(borrowed)
    check("a page that borrowed the styles still gets the script, and the styles once",
          "function show(i)" in got and got.count("/* " + MARK) == 1)
    print("page_pictures selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else 0)
