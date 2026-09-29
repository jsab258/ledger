#!/usr/bin/env python3
"""The day's approval page: faces, looks and voices, in the 25 September casting page's format.

    python tools/day_page.py production/approvals/<date>/page.json     # writes index.html and files.json beside it
    python tools/day_page.py --selftest

WHY, 28 September. Jafar: one approval page a day, linked first in the day's
summary, "pictures and sound, judged in minutes", keeping the 25 September
casting page's format (each item's pictures and sound, one pick and a note,
stored on the page), and "anything I have not judged carries onto the next
page". tools/weekend_page.py made one page for one weekend; this makes any
day's from a page.json that lists its sections. Only items that passed the
gate (CLAUDE.md) are listed there.

page.json:
  {"title": "...", "kicker": "...", "how": ["paragraph", ...], "foot": "...",
   "sections": [
     {"kind": "faces", "key": "face-sheila-dunn", "name": "Sheila Dunn", "pron": "her", "note": "...",
      "audio": "repo path of the line the speaking face follows",
      "candidates": [{"take": "Q1", "front": "repo path", "profile": "repo path",
                      "speak": {"file": "repo path", "frames": 90, "cols": 10, "rows": 9, "fps": 15}}]},
     {"kind": "look", "key": "look-talk-light", "name": "...", "note": "...", "pictures": [{"src": "repo path", "alt": "..."}],
      "options": [["yes", "Keep it"], ["no", "Not like this"]]},
     {"kind": "voice", "key": "game-sheila-dunn", "name": "...", "note": "...", "line": "...", "audio": "repo path",
      "options": [["yes", "This is her"], ["no", "Not her"]]},
     {"kind": "pair", "key": "act-ron-kirby-threat", "name": "...", "note": "...", "line": "...",
      "takes": [{"label": "A", "audio": "repo path"}, {"label": "B", "audio": "repo path"}],
      "options": [["A", "A"], ["B", "B"], ["neither", "Neither"]]}]}
A pair is heard blind: which take is which engine is kept in a key file, never on the page.
Picks are stored as verdicts/<key>.
"""
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))


def style():
    import candidate_page
    page = candidate_page.PAGE
    return page[page.index("<link rel=\"preconnect\""):page.index("</style>") + len("</style>")]


def publishable(spec):
    """The page's data with every repo path replaced by a published name, and the files map."""
    files = {}

    def pub(rel, prefix):
        name = prefix + "/" + rel.replace("\\", "/").split("/")[-1]
        base, ext = os.path.splitext(name)
        k = 1
        while name in files and files[name] != rel:
            k += 1
            name = "%s-%d%s" % (base, k, ext)
        files[name] = rel
        return name

    out = dict(spec)
    secs = []
    for s in spec["sections"]:
        s = json.loads(json.dumps(s))
        tag = s["key"]
        if s.get("audio"):
            s["audio"] = pub(s["audio"], tag)
        for c in s.get("candidates", []):
            for shot in ("front", "profile"):
                if c.get(shot):
                    c[shot] = pub(c[shot], tag)
            if c.get("speak"):
                c["speak"]["file"] = pub(c["speak"]["file"], tag)
        for p in s.get("pictures", []):
            p["src"] = pub(p["src"], tag)
        for t in s.get("takes", []):
            t["audio"] = pub(t["audio"], tag)
        secs.append(s)
    out["sections"] = secs
    return out, files


BODY = r"""
<div class="wrap">
  <header>
    <div class="kicker" id="kicker"></div>
    <h1 id="title"></h1>
    <div id="how"></div>
    <div class="tally" id="tally">Loading your earlier picks…</div>
  </header>
  <main class="wrap" id="people"></main>
  <footer id="foot"></footer>
</div>
<script>
const PAGE = __DATA__;
const state = {};
let db = null, canWrite = true, audio = null, playing = null, raf = 0;
function el(tag, attrs, ...kids){
  const n = document.createElement(tag);
  for (const [k,v] of Object.entries(attrs||{})) { if (k === "class") n.className = v; else if (k === "text") n.textContent = v; else n.setAttribute(k, v); }
  for (const k of kids) if (k) n.append(k);
  return n;
}
function stop(){ if (audio) audio.pause(); if (playing) playing.classList.remove("playing"); clearInterval(raf); audio = null; playing = null; }
function play(src, btn, onFrame){
  const same = playing === btn; stop(); if (same) return;
  const a = new Audio(src); audio = a; playing = btn; btn.classList.add("playing");
  a.addEventListener("ended", () => { if (onFrame) onFrame(0); stop(); });
  a.play().then(() => { if (onFrame) raf = setInterval(() => { if (audio === a) onFrame(a.currentTime); }, 33); }).catch(() => stop());
}
function spriteBox(sp){
  const box = el("div", {class:"speak", role:"img", "aria-label":"speaking"});
  box.style.backgroundImage = "url(" + sp.file + ")";
  box.style.backgroundSize = (sp.cols * 100) + "% " + (sp.rows * 100) + "%";
  const show = i => {
    i = Math.max(0, Math.min(sp.frames - 1, i));
    const c = i % sp.cols, r = Math.floor(i / sp.cols);
    box.style.backgroundPosition = (sp.cols > 1 ? c / (sp.cols - 1) * 100 : 0) + "% " + (sp.rows > 1 ? r / (sp.rows - 1) * 100 : 0) + "%";
  };
  show(0);
  return {box, at: t => show(Math.floor(t * sp.fps))};
}
function save(key, patch){
  state[key] = Object.assign({}, state[key] || {}, patch, {at: new Date().toISOString()});
  render();
  if (!db || !canWrite) return;
  db.doc("verdicts/" + key).set(Object.assign({}, state[key])).catch(e => { if (e && e.code === "invalid_argument") { canWrite = false; render(); } });
}
function picks(key, options, cur){
  const row = el("div", {class:"row"});
  for (const [v, t] of options) {
    const id = "pick-" + key + "-" + v;
    const r = el("input", {type:"radio", name:"pick-" + key, id, value:v});
    if (cur === v) r.checked = true;
    r.addEventListener("change", () => save(key, {pick:v}));
    row.append(el("label", {class:"pick", for:id}, r, document.createTextNode(t)));
  }
  return row;
}
function note(key, st){
  const t = el("textarea", {placeholder:"What is right or wrong, in a few words (optional)"});
  t.value = st.note || "";
  t.addEventListener("change", () => save(key, {note:t.value}));
  return t;
}
function render(){
  const root = document.getElementById("people");
  root.replaceChildren();
  let judged = 0, total = 0;
  for (const s of PAGE.sections) {
    const st = state[s.key] || {};
    total++; if (st.pick) judged++;
    const sec = el("section", {class:"person", id:s.key});
    sec.append(el("div", {}, el("h2", {text:s.name})));
    if (s.note) sec.append(el("p", {class:"was", text:s.note}));
    if (s.kind === "faces") {
      const grid = el("div", {class:"cands"});
      for (const c of s.candidates.concat([{take:"none"}])) {
        const box = el("div", {class:"cand" + (st.pick === c.take ? " picked" : "")});
        if (c.take !== "none") {
          box.append(el("div", {class:"take", text:c.take}));
          box.append(el("div", {class:"pair"},
            c.front ? el("img", {src:c.front, alt:s.name + " " + c.take + ", front", loading:"lazy"}) : el("div", {class:"speak"}),
            c.profile ? el("img", {src:c.profile, alt:s.name + " " + c.take + ", profile", loading:"lazy"}) : el("div", {class:"speak"})));
          if (c.speak && s.audio) {
            const sp = spriteBox(c.speak);
            const b = el("button", {type:"button", text:"Play the line"});
            b.addEventListener("click", () => play(s.audio, b, sp.at));
            box.append(sp.box, el("div", {class:"row"}, b));
          }
        } else {
          box.append(el("div", {class:"take", text:"None of these"}));
        }
        const id = "pick-" + s.key + "-" + c.take;
        const radio = el("input", {type:"radio", name:"pick-" + s.key, id, value:c.take});
        if (st.pick === c.take) radio.checked = true;
        radio.addEventListener("change", () => save(s.key, {pick:c.take}));
        box.append(el("label", {class:"pick", for:id}, radio, document.createTextNode(c.take === "none" ? "None is " + s.pron : "This is " + s.pron)));
        grid.append(box);
      }
      sec.append(grid);
    } else if (s.kind === "look") {
      const g = el("div", {class:"capgrid"});
      for (const p of s.pictures) g.append(el("figure", {}, el("img", {src:p.src, alt:p.alt, loading:"lazy"}), el("figcaption", {class:"was", text:p.alt})));
      sec.append(g, picks(s.key, s.options, st.pick));
    } else if (s.kind === "pair") {
      const row = el("div", {class:"row"});
      for (const t of s.takes) {
        const b = el("button", {type:"button", text:"Play " + t.label});
        b.addEventListener("click", () => play(t.audio, b));
        row.append(b);
      }
      sec.append(row, el("div", {class:"row"}, el("q", {text:s.line})), picks(s.key, s.options, st.pick));
    } else if (s.kind === "voice") {
      const b = el("button", {type:"button", text:"Play"});
      b.addEventListener("click", () => play(s.audio, b));
      sec.append(el("div", {class:"row"}, b, el("q", {text:s.line})), picks(s.key, s.options, st.pick));
    }
    sec.append(note(s.key, st), el("span", {class:"saved", text: st.at ? "Saved " + new Date(st.at).toLocaleString() : ""}));
    root.append(sec);
  }
  document.getElementById("tally").innerHTML = "<b>" + judged + " of " + total + "</b> picked" + (db ? "" : " · picks are not being stored on this view");
}
document.getElementById("kicker").textContent = PAGE.kicker;
document.getElementById("title").textContent = PAGE.title;
for (const h of PAGE.how) document.getElementById("how").append(el("p", {class:"how", text:h}));
document.getElementById("foot").textContent = PAGE.foot || "";
render();
(async () => {
  try { db = window.claude && window.claude.use ? await window.claude.use("db") : null; } catch (e) { db = null; }
  if (!db) { render(); return; }
  for (const s of PAGE.sections) {
    try { const d = await db.doc("verdicts/" + s.key).get(); if (d.exists) state[s.key] = Object.assign({}, d.data()); } catch (e) {}
  }
  render();
})();
</script>
"""


def build(spec_path):
    spec = json.load(open(spec_path, encoding="utf-8"))
    data, files = publishable(spec)
    missing = [v for v in files.values() if not os.path.exists(os.path.join(REPO, v))]
    if missing:
        print("day_page: missing files: " + ", ".join(missing))
        return 1
    out_dir = os.path.dirname(os.path.abspath(spec_path))
    page = "<title>" + spec.get("tab", "The Day's Page") + "</title>\n" + style() + BODY.replace(
        "__DATA__", json.dumps(data, ensure_ascii=False).replace("</", "<\\/"))
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(page)
    with open(os.path.join(out_dir, "files.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(files, fh, indent=1)
    size = sum(os.path.getsize(os.path.join(REPO, v)) for v in files.values()) / 1e6
    print("day_page: %d sections, %d files, %.1f MB" % (len(data["sections"]), len(files), size))
    return 0


def selftest():
    ok = bad = 0

    def check(name, cond):
        nonlocal ok, bad
        if cond:
            ok += 1
        else:
            bad += 1
            print("day_page selftest FAIL " + name)
    spec = {"sections": [{"kind": "faces", "key": "face-x", "audio": "a/line.wav",
                          "candidates": [{"take": "Q1", "front": "c/x/Q1-front.jpg", "profile": "c/x/Q1-profile.jpg",
                                          "speak": {"file": "c/x/Q1-speak.jpg"}},
                                         {"take": "Q2", "front": "c/y/Q1-front.jpg"}]}]}
    data, files = publishable(spec)
    names = list(files)
    check("every file gets one published name", len(files) == 5 and len(set(names)) == 5)
    check("two files of the same name stay apart", files[data["sections"][0]["candidates"][1]["front"]] == "c/y/Q1-front.jpg")
    s = style()
    check("the casting page's look is borrowed", s.startswith("<link") and s.endswith("</style>"))
    print("day_page selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else build(sys.argv[1]))
