#!/usr/bin/env python3
"""The approval page for the MetaHuman candidates and the acting test.

    python tools/candidate_page.py            # writes production/approvals/2026-09-25-casting/index.html and files.json
    python tools/candidate_page.py --selftest

WHY, 25 September. Jafar's rulings: faces are cast in MetaHuman first, five
candidates each, shown front, profile and speaking in the street's light, the
one he approves becoming the concept; and the voices tested calm against
acted references, blind, each feeling judged on its own. One page per
sitting. His picks are stored by the page (verdicts/cand-<person> and
verdicts/act-<person>-<feeling>); which letter is which take stays in
production/casting/acting-key.json, never on the page. The sitting's third
item, the first garment (FreeSewing's flat cap, worn in the street), is at the
foot for a look (verdicts/cap-flat-cap).
"""
import html
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATE = "2026-09-25-casting"
CAND = "production/casting/candidates-2026-09-25"
ACTING_KEY = "production/casting/acting-key.json"
CAP = "production/art/clothing/flat-cap-2026-09-25"
CAP_PICTURES = [("worn-front", "Ron wearing the cap, front"), ("worn-profile", "Ron wearing the cap, side"),
                ("worn-street", "Ron in the cap, in the street"), ("draped-in-blender", "The cap draped in Blender, four sides"),
                ("pattern-panels", "The pattern's pieces, cut flat")]
PEOPLE = [("sheila-dunn", "Sheila Dunn", "her", "D"), ("ron-kirby", "Ron Kirby", "him", "A"), ("darren-milner", "Darren Milner", "him", "A")]
FEELINGS = [("threat", "Threat"), ("warmth", "Warmth"), ("embarrassment", "Embarrassment"), ("humour", "Humour")]


def sheet_line(slug):
    import re
    text = open(os.path.join(REPO, "production", "casting", slug, "SHEET.md"), encoding="utf-8-sig").read()
    lines = re.findall(r'^\d\.\s+"(.+)"\s*$', text, re.M)
    return lines[0] if lines else ""


def gather():
    files = {}
    idx_path = os.path.join(REPO, CAND, "index.json")
    index = json.load(open(idx_path, encoding="utf-8")) if os.path.exists(idx_path) else {}
    key = json.load(open(os.path.join(REPO, ACTING_KEY), encoding="utf-8")) if os.path.exists(os.path.join(REPO, ACTING_KEY)) else {}
    people = []
    for slug, name, pron, letter in PEOPLE:
        line_rel = "production/casting/%s/voices/%s-%s-line1.mp3" % (slug, slug, letter)
        files["line/%s.mp3" % slug] = line_rel
        cands = []
        for e in index.get(slug, []):
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
        acting = []
        ch = key.get("characters", {}).get(slug, {})
        for feeling, label in FEELINGS:
            ln = ch.get("lines", {}).get(feeling)
            if not ln:
                continue
            takes = []
            for L in sorted(ln["letters"]):
                pub = "act/%s/%s-%s.mp3" % (slug, feeling, L)
                files[pub] = ln["letters"][L]["file"]
                takes.append({"letter": L, "src": pub})
            acting.append({"feeling": feeling, "label": label, "line": ln["line"], "takes": takes})
        people.append({"slug": slug, "name": name, "pron": pron, "line": sheet_line(slug), "audio": "line/%s.mp3" % slug,
                       "candidates": cands, "acting": acting})
    cap = []
    for stem, alt in CAP_PICTURES:
        rel = "%s/%s.jpg" % (CAP, stem)
        if os.path.exists(os.path.join(REPO, rel)):
            files["cap/%s.jpg" % stem] = rel
            cap.append({"src": "cap/%s.jpg" % stem, "alt": alt})
    return people, files, cap


PAGE = r"""<title>Faces and Voices</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo+Narrow:wght@500;600;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&family=Courier+Prime:wght@400;700&display=swap">
<style>
:root{
  --ground:#e9ecea; --surface:#f6f7f6; --ink:#1b2224; --muted:#56636a; --rule:#c9d0d0;
  --accent:#9a3e2b; --ok:#2e6a48; --chip:#dde2e1;
  --display:"Archivo Narrow","Arial Narrow",Arial,sans-serif;
  --body:"Source Serif 4",Georgia,"Times New Roman",serif;
  --type:"Courier Prime","Courier New",Courier,monospace;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --ground:#121617; --surface:#1a2022; --ink:#e3e8e7; --muted:#98a4a7; --rule:#2d3639;
    --accent:#d27352; --ok:#63b384; --chip:#242c2e; color-scheme:dark;
  }
}
:root[data-theme="dark"]{
  --ground:#121617; --surface:#1a2022; --ink:#e3e8e7; --muted:#98a4a7; --rule:#2d3639;
  --accent:#d27352; --ok:#63b384; --chip:#242c2e; color-scheme:dark;
}
*{box-sizing:border-box}
body{background:var(--ground);color:var(--ink);font:16px/1.5 var(--body);padding-inline:16px;padding-block:28px 64px}
.wrap{max-width:1180px;margin:0 auto;display:grid;gap:40px}
header{display:grid;gap:10px;border-bottom:2px solid var(--ink);padding-bottom:18px}
.kicker{font:700 12px/1 var(--type);letter-spacing:.12em;text-transform:uppercase;color:var(--accent)}
h1{font:700 clamp(30px,5vw,46px)/1.02 var(--display);margin:0;text-wrap:balance}
h2{font:700 clamp(26px,4vw,34px)/1 var(--display);margin:0;text-wrap:balance}
h3{font:600 15px/1 var(--display);letter-spacing:.06em;text-transform:uppercase;margin:0}
.how{margin:0;max-width:70ch;color:var(--muted)}
.tally,.was,.cap{font:400 13px/1.4 var(--type);color:var(--muted)}
.tally b{color:var(--ink)}
section.person{display:grid;gap:22px;background:var(--surface);border:1px solid var(--rule);padding:22px}
.capgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:10px}
.capgrid img{width:100%;display:block;background:var(--chip)}
.cands{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px}
.cand{display:grid;gap:8px;border:1px solid var(--rule);padding:10px;background:var(--ground)}
.cand.picked{border-color:var(--accent);box-shadow:inset 0 3px 0 var(--accent)}
.pair{display:grid;grid-template-columns:1fr 1fr;gap:6px}
.pair img{width:100%;aspect-ratio:4/3;object-fit:cover;display:block;background:var(--chip)}
.speak{width:100%;aspect-ratio:4/3;background-color:var(--chip);background-repeat:no-repeat}
.row{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
button{font:600 14px/1 var(--display);letter-spacing:.04em;border:1px solid var(--rule);background:var(--surface);color:var(--ink);padding:9px 12px;cursor:pointer;min-height:38px}
button:hover{border-color:var(--ink)}
button.playing{background:var(--ink);color:var(--ground);border-color:var(--ink)}
button:focus-visible,textarea:focus-visible,input:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
label.pick{display:flex;align-items:center;gap:6px;font:400 14px var(--type)}
.take{font:700 20px/1 var(--display)}
.acting{display:grid;gap:14px}
.feel{display:grid;gap:8px;border-top:1px solid var(--rule);padding-top:12px}
.feel .label{font:700 12px/1 var(--type);letter-spacing:.1em;text-transform:uppercase;color:var(--accent)}
.feel q{font-style:italic}
textarea{width:100%;min-height:54px;font:15px/1.4 var(--body);color:var(--ink);background:var(--ground);border:1px solid var(--rule);padding:8px}
.saved{font:400 13px var(--type);color:var(--muted)}
footer{font:400 13px/1.5 var(--type);color:var(--muted);border-top:1px solid var(--rule);padding-top:14px}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
</style>

<div class="wrap">
  <header>
    <div class="kicker">LEDGER · approval page · 25 September, afternoon</div>
    <h1>Five faces for each, and whether acting helps the voices</h1>
    <p class="how">Faces first: for Sheila, Ron and Darren, five MetaHumans each, built from the casting sheet, in plain clothes, in the street's daylight. Each shows front, profile, and speaking the sheet's first line in the voice you picked (press Play). Pick the one that is the person, or None, with a word on what is wrong. The one you pick becomes the concept.</p>
    <p class="how">Then the voices: each person says four lines, one for threat, warmth, embarrassment and humour. Each line is made four ways with the same voice, words and settings; the letters are shuffled per line. Pick the take that sounds most like a person meaning it, or None.</p>
    <div class="tally" id="tally">Loading your earlier picks…</div>
  </header>
  <main class="wrap" id="people"></main>
  <footer>Faces: Epic's MetaHuman, built on this PC, the speaking faces animated from the line's audio by Epic's MetaHuman Animator; plain clothes from Epic's free Fab garments. Voices: Chatterbox (the original model, MIT), from the voice you picked on the last page. How each take was made is recorded apart from this page, so the choice stays blind. The cap: FreeSewing's Florent pattern (MIT), sewn by this project's own Blender script.</footer>
</div>

<script>
const PEOPLE = __DATA__;
const CAP = __CAP__;
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
  // A timer, not animation frames: those pause in a tab the viewer is not
  // looking at, and the face would stop while the voice went on.
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
function render(){
  const root = document.getElementById("people");
  root.replaceChildren();
  let judged = 0, total = 0;
  for (const p of PEOPLE) {
    const sec = el("section", {class:"person", id:p.slug});
    const ck = "cand-" + p.slug, cs = state[ck] || {};
    total++; if (cs.pick) judged++;
    sec.append(el("div", {}, el("h2", {text:p.name}), el("div", {class:"was", text:"Speaking: “" + p.line + "”"})));
    const grid = el("div", {class:"cands"});
    for (const c of p.candidates.concat([{take:"none"}])) {
      const box = el("div", {class:"cand" + (cs.pick === c.take ? " picked" : "")});
      if (c.take !== "none") {
        box.append(el("div", {class:"take", text:c.take}));
        box.append(el("div", {class:"pair"},
          c.front ? el("img", {src:c.front, alt:p.name + " " + c.take + ", front", loading:"lazy"}) : el("div", {class:"speak"}),
          c.profile ? el("img", {src:c.profile, alt:p.name + " " + c.take + ", profile", loading:"lazy"}) : el("div", {class:"speak"})));
        if (c.speak) {
          const s = spriteBox(c.speak);
          const b = el("button", {type:"button", text:"Play the line"});
          b.addEventListener("click", () => play(p.audio, b, s.at));
          box.append(s.box, el("div", {class:"row"}, b));
        }
      } else {
        box.append(el("div", {class:"take", text:"None of these"}));
      }
      const id = "pick-" + ck + "-" + c.take;
      const radio = el("input", {type:"radio", name:"pick-" + ck, id, value:c.take});
      if (cs.pick === c.take) radio.checked = true;
      radio.addEventListener("change", () => save(ck, {pick:c.take}));
      box.append(el("label", {class:"pick", for:id}, radio, document.createTextNode(c.take === "none" ? "None is " + p.pron : "This is " + p.pron)));
      grid.append(box);
    }
    const note = el("textarea", {placeholder:"What is right or wrong, in a few words (optional)"});
    note.value = cs.note || "";
    note.addEventListener("change", () => save(ck, {note:note.value}));
    sec.append(el("h3", {text:"Faces"}), grid, note, el("span", {class:"saved", text: cs.at ? "Saved " + new Date(cs.at).toLocaleString() : ""}));
    if (p.acting.length) {
      const ac = el("div", {class:"acting"}, el("h3", {text:"Voices: which take means it"}));
      for (const f of p.acting) {
        const ak = "act-" + p.slug + "-" + f.feeling, as = state[ak] || {};
        total++; if (as.pick) judged++;
        const row = el("div", {class:"row"});
        for (const t of f.takes) {
          const b = el("button", {type:"button", text:"Take " + t.letter});
          b.addEventListener("click", () => play(t.src, b));
          row.append(b);
        }
        const picks = el("div", {class:"row"});
        for (const L of f.takes.map(t => t.letter).concat(["none"])) {
          const id = "pick-" + ak + "-" + L;
          const r = el("input", {type:"radio", name:"pick-" + ak, id, value:L});
          if (as.pick === L) r.checked = true;
          r.addEventListener("change", () => save(ak, {pick:L}));
          picks.append(el("label", {class:"pick", for:id}, r, document.createTextNode(L === "none" ? "None" : L)));
        }
        ac.append(el("div", {class:"feel"}, el("div", {class:"label", text:f.label}), el("q", {text:f.line}), row, picks));
      }
      sec.append(ac);
    }
    root.append(sec);
  }
  if (CAP.length) {
    const k = "cap-flat-cap", st = state[k] || {};
    total++; if (st.pick) judged++;
    const sec = el("section", {class:"person", id:"cap"});
    sec.append(el("div", {}, el("h2", {text:"The first garment: a flat cap"}),
      el("p", {class:"how", text:"FreeSewing's flat cap pattern, cut for a 57 cm head, sewn and draped in Blender, then worn by Ron (candidate 5, only to show it) in the street. About an hour from pattern to worn. Not finished: rounder than a true flat cap, and plain dark wool with no tweed weave yet. Only a look: is this way of making clothes worth going on with?"})));
    const g = el("div", {class:"capgrid"});
    for (const c of CAP) g.append(el("img", {src:c.src, alt:c.alt, loading:"lazy"}));
    const picks = el("div", {class:"row"});
    for (const [v, t] of [["go", "Good start, go on this way"], ["no", "Not like this"]]) {
      const id = "pick-" + k + "-" + v;
      const r = el("input", {type:"radio", name:"pick-" + k, id, value:v});
      if (st.pick === v) r.checked = true;
      r.addEventListener("change", () => save(k, {pick:v}));
      picks.append(el("label", {class:"pick", for:id}, r, document.createTextNode(t)));
    }
    const note = el("textarea", {placeholder:"What is right or wrong, in a few words (optional)"});
    note.value = st.note || "";
    note.addEventListener("change", () => save(k, {note:note.value}));
    sec.append(g, picks, note);
    root.append(sec);
  }
  document.getElementById("tally").innerHTML = "<b>" + judged + " of " + total + "</b> picked" + (db ? "" : " · picks are not being stored on this view");
}
render();
(async () => {
  try { db = window.claude && window.claude.use ? await window.claude.use("db") : null; } catch (e) { db = null; }
  if (!db) { render(); return; }
  const keys = [];
  for (const p of PEOPLE) { keys.push("cand-" + p.slug); for (const f of p.acting) keys.push("act-" + p.slug + "-" + f.feeling); }
  if (CAP.length) keys.push("cap-flat-cap");
  for (const k of keys) { try { const s = await db.doc("verdicts/" + k).get(); if (s.exists) state[k] = Object.assign({}, s.data()); } catch (e) {} }
  render();
})();
</script>
"""


def build():
    people, files, cap = gather()
    out_dir = os.path.join(REPO, "production", "approvals", DATE)
    os.makedirs(out_dir, exist_ok=True)
    page = PAGE.replace("__DATA__", json.dumps(people, ensure_ascii=False).replace("</", "<\\/"))
    page = page.replace("__CAP__", json.dumps(cap, ensure_ascii=False).replace("</", "<\\/"))
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(page)
    with open(os.path.join(out_dir, "files.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(files, fh, indent=1)
    size = sum(os.path.getsize(os.path.join(REPO, v)) for v in files.values() if os.path.exists(os.path.join(REPO, v))) / 1e6
    print("candidate_page: %d people, %d candidates, %d acting lines, %d cap pictures, %d files, %.1f MB" % (
        len(people), sum(len(p["candidates"]) for p in people), sum(len(p["acting"]) for p in people), len(cap), len(files), size))


def selftest():
    ok = bad = 0

    def check(name, cond):
        nonlocal ok, bad
        if cond:
            ok += 1
        else:
            bad += 1
            print("candidate_page selftest FAIL " + name)
    check("the page never names a take's reference or settings", "calm" not in PAGE.split("<script>")[1] and "drama" not in PAGE)
    check("the three people, with the voice letter each picked", [p[0] for p in PEOPLE] == ["sheila-dunn", "ron-kirby", "darren-milner"])
    check("the four feelings", [f for f, _ in FEELINGS] == ["threat", "warmth", "embarrassment", "humour"])
    check("each sheet's first line is read", all(sheet_line(p[0]) for p in PEOPLE))
    check("no script from another host", 'src="http' not in PAGE)
    check("the cap's pictures are named", len(CAP_PICTURES) == 5 and all(s for s, _ in CAP_PICTURES))
    print("candidate_page selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    build()
