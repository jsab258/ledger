#!/usr/bin/env python3
"""The weekend approval page, 26 September: the rebuilt faces and the faster voice.

    python tools/weekend_page.py            # writes production/approvals/2026-09-26-weekend/index.html and files.json
    python tools/weekend_page.py --selftest

WHY. Jafar's sitting: rebuild Sheila, Ron and Darren from northern European
presets to their casting sheets, four or five candidates each, judged in the
street's daylight; and cut the six seconds between his line and a character
speaking, with Pocket TTS put blind beside the current voice, each with its
measured delay. "One page for the weekend with the faces and the voices."

The page keeps the 25 September casting page's format (tools/candidate_page.py,
whose look it borrows): each candidate's front, profile and speaking pictures,
one pick and a note, stored on the page (verdicts/face-<person>,
verdicts/voice-<person>). Only what passed the gate is on it
(production/approvals/2026-09-26-weekend/gate.json names each candidate and
voice and both checks). Which voice letter is which engine is in
production/casting/voice-key-2026-09-26.json, never on the page.
"""
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
DATE = "2026-09-26-weekend"
OUT = os.path.join("production", "approvals", DATE)
CAND = "production/casting/candidates-2026-09-26"
VOICES = "production/casting/voices-2026-09-26"
KEY = "production/casting/voice-key-2026-09-26.json"
PEOPLE = [("sheila-dunn", "Sheila Dunn", "her"), ("ron-kirby", "Ron Kirby", "him"), ("darren-milner", "Darren Milner", "him")]


def rel_exists(rel):
    return os.path.exists(os.path.join(REPO, rel))


def gather():
    files = {}
    gate = json.load(open(os.path.join(REPO, OUT, "gate.json"), encoding="utf-8"))
    idx_path = os.path.join(REPO, CAND, "index.json")
    index = json.load(open(idx_path, encoding="utf-8")) if os.path.exists(idx_path) else {}
    key = json.load(open(os.path.join(REPO, KEY), encoding="utf-8")) if rel_exists(KEY) else {}
    people = []
    for slug, name, pron in PEOPLE:
        passed = set(gate.get("faces", {}).get(slug, {}).get("passed", []))
        cands = []
        for e in index.get(slug, []):
            if e["take"] not in passed:
                continue
            c = {"take": e["take"]}
            for shot in ("front", "profile"):
                if e.get(shot):
                    pub = "cand/" + e[shot]
                    files[pub] = CAND + "/" + e[shot]
                    c[shot] = pub
            if e.get("speak"):
                pub = "cand/" + e["speak"]["file"]
                files[pub] = CAND + "/" + e["speak"]["file"]
                c["speak"] = dict(e["speak"], file=pub)
            cands.append(c)
        # the line the speaking face was animated from, for those on the page
        line = VOICES + "/%s/speaking-line.wav" % slug
        if cands and rel_exists(line):
            files["line/%s.wav" % slug] = line
        voices = []
        vk = key.get(slug, {})
        for letter in sorted(vk.get("letters", {})):
            if letter not in gate.get("voices", {}).get(slug, {}).get("passed", []):
                continue
            lines = []
            texts = sheet_lines(slug)
            for entry in vk["letters"][letter].get("lines", []):
                rel = entry["file"]
                if rel_exists(rel):
                    pub = "voice/%s/%s" % (slug, rel.split("/")[-1])
                    files[pub] = rel
                    lines.append({"src": pub, "text": texts[entry["sheetLine"] - 1]})
            voices.append({"letter": letter, "lines": lines, "delay": vk["letters"][letter].get("delay", "")})
        people.append({"slug": slug, "name": name, "pron": pron, "audio": "line/%s.wav" % slug if "line/%s.wav" % slug in files else "",
                       "candidates": cands, "voices": voices, "voiceNote": gate.get("voices", {}).get(slug, {}).get("note", ""),
                       "faceNote": gate.get("faces", {}).get(slug, {}).get("note", ""), "sheetLines": sheet_lines(slug)})
    return people, files, gate


def sheet_lines(slug):
    import re
    text = open(os.path.join(REPO, "production", "casting", slug, "SHEET.md"), encoding="utf-8-sig").read()
    return re.findall(r'^\d\.\s+"(.+)"\s*$', text, re.M)[:3]


def style():
    import candidate_page
    page = candidate_page.PAGE
    return page[page.index("<link rel=\"preconnect\""):page.index("</style>") + len("</style>")]


BODY = r"""
<div class="wrap">
  <header>
    <div class="kicker">LEDGER · approval page · 26 September, for the weekend</div>
    <h1>Three faces rebuilt to their sheets, and a quicker voice</h1>
    <p class="how">__HOW_FACES__</p>
    <p class="how">__HOW_VOICES__</p>
    <div class="tally" id="tally">Loading your earlier picks…</div>
  </header>
  <main class="wrap" id="people"></main>
  <footer>__FOOT__</footer>
</div>
<script>
const PEOPLE = __DATA__;
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
  for (const p of PEOPLE) {
    const sec = el("section", {class:"person", id:p.slug});
    sec.append(el("div", {}, el("h2", {text:p.name})));
    if (p.candidates.length) {
      const fk = "face-" + p.slug, fs = state[fk] || {};
      total++; if (fs.pick) judged++;
      const grid = el("div", {class:"cands"});
      for (const c of p.candidates.concat([{take:"none"}])) {
        const box = el("div", {class:"cand" + (fs.pick === c.take ? " picked" : "")});
        if (c.take !== "none") {
          box.append(el("div", {class:"take", text:c.take}));
          box.append(el("div", {class:"pair"},
            c.front ? el("img", {src:c.front, alt:p.name + " " + c.take + ", front", loading:"lazy"}) : el("div", {class:"speak"}),
            c.profile ? el("img", {src:c.profile, alt:p.name + " " + c.take + ", profile", loading:"lazy"}) : el("div", {class:"speak"})));
          if (c.speak && p.audio) {
            const s = spriteBox(c.speak);
            const b = el("button", {type:"button", text:"Play the line"});
            b.addEventListener("click", () => play(p.audio, b, s.at));
            box.append(s.box, el("div", {class:"row"}, b));
          }
        } else {
          box.append(el("div", {class:"take", text:"None of these"}));
        }
        const id = "pick-" + fk + "-" + c.take;
        const radio = el("input", {type:"radio", name:"pick-" + fk, id, value:c.take});
        if (fs.pick === c.take) radio.checked = true;
        radio.addEventListener("change", () => save(fk, {pick:c.take}));
        box.append(el("label", {class:"pick", for:id}, radio, document.createTextNode(c.take === "none" ? "None is " + p.pron : "This is " + p.pron)));
        grid.append(box);
      }
      sec.append(el("h3", {text:"Faces"}));
      if (p.faceNote) sec.append(el("p", {class:"was", text:p.faceNote}));
      sec.append(grid, note(fk, fs), el("span", {class:"saved", text: fs.at ? "Saved " + new Date(fs.at).toLocaleString() : ""}));
    } else if (p.faceNote) {
      sec.append(el("h3", {text:"Faces"}), el("p", {class:"was", text:p.faceNote}));
    }
    const ac = el("div", {class:"acting"});
    if (p.voices.length || p.voiceNote) ac.append(el("h3", {text:"Voices"}));
    if (p.voiceNote) ac.append(el("p", {class:"was", text:p.voiceNote}));
    if (p.voices.length) {
      const vk = "voice-" + p.slug, vs = state[vk] || {};
      total++; if (vs.pick) judged++;
      for (const v of p.voices) {
        const row = el("div", {class:"row"});
        v.lines.forEach((ln, i) => {
          const b = el("button", {type:"button", text:"Line " + (i + 1)});
          b.addEventListener("click", () => play(ln.src, b));
          row.append(b);
        });
        ac.append(el("div", {class:"feel"}, el("div", {class:"label", text:"Voice " + v.letter}), el("div", {class:"was", text:v.delay}), row));
      }
      const lines = el("div", {class:"was"});
      p.voices[0].lines.forEach((ln, i) => lines.append(el("div", {text:(i + 1) + ". “" + ln.text + "”"})));
      ac.append(lines, picks(vk, p.voices.map(v => [v.letter, "Voice " + v.letter + " is " + p.pron]).concat([["none", "Neither"]]), vs.pick), note(vk, vs));
    }
    sec.append(ac);
    root.append(sec);
  }
  document.getElementById("tally").innerHTML = "<b>" + judged + " of " + total + "</b> picked" + (db ? "" : " · picks are not being stored on this view");
}
render();
(async () => {
  try { db = window.claude && window.claude.use ? await window.claude.use("db") : null; } catch (e) { db = null; }
  if (!db) { render(); return; }
  for (const p of PEOPLE) for (const k of ["face-" + p.slug, "voice-" + p.slug]) {
    try { const s = await db.doc("verdicts/" + k).get(); if (s.exists) state[k] = Object.assign({}, s.data()); } catch (e) {}
  }
  render();
})();
</script>
"""


def build():
    people, files, gate = gather()
    out_dir = os.path.join(REPO, OUT)
    page = "<title>Faces and a Quicker Voice</title>\n" + style() + BODY
    for k in ("HOW_FACES", "HOW_VOICES", "FOOT"):
        page = page.replace("__%s__" % k, gate.get("page", {}).get(k.lower(), ""))
    page = page.replace("__DATA__", json.dumps(people, ensure_ascii=False).replace("</", "<\\/"))
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(page)
    with open(os.path.join(out_dir, "files.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(files, fh, indent=1)
    size = sum(os.path.getsize(os.path.join(REPO, v)) for v in files.values() if rel_exists(v)) / 1e6
    print("weekend_page: %d people, %d faces, %d voices, %d files, %.1f MB" % (
        len(people), sum(len(p["candidates"]) for p in people), sum(len(p["voices"]) for p in people), len(files), size))


def selftest():
    ok = bad = 0

    def check(name, cond):
        nonlocal ok, bad
        if cond:
            ok += 1
        else:
            bad += 1
            print("weekend_page selftest FAIL " + name)
    s = style()
    check("the casting page's look is borrowed", s.startswith("<link") and s.endswith("</style>") and "--ground" in s)
    check("every person has a sheet with three lines", all(len(sheet_lines(slug)) == 3 for slug, _, _ in PEOPLE))
    check("no engine name on the page's own text", all(w not in BODY.lower() for w in ("pocket", "chatterbox", "kyutai")))
    print("weekend_page selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else build())
