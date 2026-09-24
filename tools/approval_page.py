#!/usr/bin/env python3
"""The sitting's approval page: pictures and sound, judged in minutes.

    python tools/approval_page.py 2026-09-25           # writes production/approvals/2026-09-25/index.html and files.json
    python tools/approval_page.py --selftest

WHY, 24 September. Jafar: "Approvals reach me as one page per sitting,
pictures and sound, judged in minutes, linked at the top of the closing
summary." The page shows each principal's sheet (age, trade, face, body,
hair, clothes), the three concept portraits, and the three lines spoken by
every voice candidate, blind (letters only; ../voice-key.json says which is
which). He approves a sheet whole or sends it back with a note, and picks a
voice. His verdicts are stored by the page itself (the artifact's db, at
verdicts/<slug>); the next sitting reads them and writes the approval file
beside the sheet (tools/approvals.py --record).

files.json maps each published path to its repo file, for publishing the page
with its pictures and sound beside it.
"""
import html
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CASTING = os.path.join(REPO, "production", "casting")
ORDER = ("sheila-dunn", "ron-kirby", "darren-milner")
FIELDS = ("Age", "Occupation", "Face", "Body", "Hair", "Clothes, 1990", "Voice")


def read_sheet(slug):
    """The sheet's name, its table fields and its three lines."""
    path = os.path.join(CASTING, slug, "SHEET.md")
    with open(path, encoding="utf-8-sig") as fh:
        text = fh.read()
    name = re.search(r"^#\s+(.+)$", text, re.M).group(1).strip()
    fields = {}
    for m in re.finditer(r"^\|\s*\*\*(.+?)\*\*\s*\|\s*(.+?)\s*\|\s*$", text, re.M):
        fields[m.group(1)] = m.group(2)
    lines = re.findall(r'^\d\.\s+"(.+)"\s*$', text, re.M)
    return {"slug": slug, "name": name, "fields": {k: fields.get(k, "") for k in FIELDS}, "lines": lines[:3]}


def voices(slug, names):
    """Letters with their files, from names like <slug>-B-line2.mp3 and <slug>-B-reference.mp3."""
    out = {}
    for n in names:
        m = re.match(re.escape(slug) + r"-([A-Z])-(line[123]|reference)\.(mp3|wav)$", n)
        if m:
            out.setdefault(m.group(1), {})[m.group(2)] = n
    return [{"letter": k, **{p: v[p] for p in v}} for k, v in sorted(out.items())]


def gather():
    people, files = [], {}
    for slug in ORDER:
        if not os.path.exists(os.path.join(CASTING, slug, "SHEET.md")):
            continue
        p = read_sheet(slug)
        p["pictures"] = {}
        # IN THE GAME TONIGHT, beside the concept: the stand-in MetaHuman as
        # the street lights it (the audit: "watch that person talk and move in
        # street lighting"), until one is built to the approved portrait.
        p["ingame"] = {}
        for shot in ("close", "mid"):
            rel = "production/casting/%s/ingame-%s.jpg" % (slug, shot)
            if os.path.exists(os.path.join(REPO, rel)):
                pub = "%s/ingame-%s.jpg" % (slug, shot)
                p["ingame"][shot] = pub
                files[pub] = rel
        for shot in ("front", "profile", "full"):
            rel = "production/casting/%s/%s.jpg" % (slug, shot)
            if os.path.exists(os.path.join(REPO, rel)):
                pub = "%s/%s.jpg" % (slug, shot)
                p["pictures"][shot] = pub
                files[pub] = rel
        vdir = os.path.join(CASTING, slug, "voices")
        names = sorted(os.listdir(vdir)) if os.path.isdir(vdir) else []
        p["voices"] = voices(slug, names)
        for v in p["voices"]:
            for k in ("line1", "line2", "line3", "reference"):
                if k in v:
                    pub = "%s/voices/%s" % (slug, v[k])
                    files[pub] = "production/casting/%s/voices/%s" % (slug, v[k])
                    v[k] = pub
        people.append(p)
    return people, files


# THINGS TO APPROVE THAT ARE NOT A PERSON, 25 September: the clothing item's
# proof of manufacture. Each is judged on its own, stored at verdicts/<slug>.
PROOFS = [{
    "slug": "donkey-jacket",
    "name": "The donkey jacket",
    "was": "A proof that a garment can be made, fitted and worn, not the finished jacket",
    "text": ("Made by script in Blender from MetaHuman's own template body (no money, no new licence), in two sizes, "
             "and worn in the game over the cast's clothes, following each man's body as he idles. Ron takes the large, "
             "Darren the regular. What it is not yet: cloth that hangs and moves, a proper collar and pockets, and a yoke "
             "that sits over the shoulders; the template body is a woman's, and a trace of that shows. Approve the method "
             "and it becomes the way garments are made; Redo with a word on what matters most."),
    "pictures": [("production/casting/ron-kirby/jacket-mid.jpg", "Ron, the large, in the street"),
                 ("production/casting/darren-milner/jacket-mid.jpg", "Darren, the regular, in the street"),
                 ("production/casting/ron-kirby/jacket-close.jpg", "Ron, close"),
                 ("production/casting/ron-kirby/jacket-made.jpg", "As made, on the template body")],
}]


def gather_proofs(files):
    out = []
    for pr in PROOFS:
        pics = []
        for rel, cap in pr["pictures"]:
            if os.path.exists(os.path.join(REPO, rel)):
                pub = "proofs/" + pr["slug"] + "/" + os.path.basename(os.path.dirname(rel)) + "-" + os.path.basename(rel)
                files[pub] = rel
                pics.append({"src": pub, "caption": cap})
        if pics:
            out.append({"slug": pr["slug"], "name": pr["name"], "was": pr["was"], "text": pr["text"], "pictures": pics})
    return out


PAGE = r"""<title>Casting Approvals</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo+Narrow:wght@500;600;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&family=Courier+Prime:wght@400;700&display=swap">
<style>
:root{
  --ground:#e9ecea; --surface:#f6f7f6; --ink:#1b2224; --muted:#56636a; --rule:#c9d0d0;
  --accent:#9a3e2b; --ok:#2e6a48; --redo:#9a5a12; --chip:#dde2e1;
  --display:"Archivo Narrow","Arial Narrow",Arial,sans-serif;
  --body:"Source Serif 4",Georgia,"Times New Roman",serif;
  --type:"Courier Prime","Courier New",Courier,monospace;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --ground:#121617; --surface:#1a2022; --ink:#e3e8e7; --muted:#98a4a7; --rule:#2d3639;
    --accent:#d27352; --ok:#63b384; --redo:#d59c4c; --chip:#242c2e; color-scheme:dark;
  }
}
:root[data-theme="dark"]{
  --ground:#121617; --surface:#1a2022; --ink:#e3e8e7; --muted:#98a4a7; --rule:#2d3639;
  --accent:#d27352; --ok:#63b384; --redo:#d59c4c; --chip:#242c2e; color-scheme:dark;
}
*{box-sizing:border-box}
body{background:var(--ground);color:var(--ink);font:16px/1.5 var(--body);padding-inline:16px;padding-block:28px 64px}
.wrap{max-width:1100px;margin:0 auto;display:grid;gap:40px}
header{display:grid;gap:10px;border-bottom:2px solid var(--ink);padding-bottom:18px}
.kicker{font:700 12px/1 var(--type);letter-spacing:.12em;text-transform:uppercase;color:var(--accent)}
h1{font:700 clamp(30px,5vw,46px)/1.02 var(--display);letter-spacing:.01em;margin:0;text-wrap:balance}
.how{margin:0;max-width:68ch;color:var(--muted)}
.tally{font:400 14px/1.4 var(--type);color:var(--muted)}
.tally b{color:var(--ink)}
section.person{display:grid;gap:22px;background:var(--surface);border:1px solid var(--rule);padding:22px}
.head{display:flex;flex-wrap:wrap;align-items:baseline;gap:6px 16px;justify-content:space-between}
h2{font:700 clamp(26px,4vw,34px)/1 var(--display);margin:0;text-wrap:balance}
.was{font:400 13px/1.2 var(--type);color:var(--muted)}
.state{font:700 12px/1 var(--type);letter-spacing:.08em;text-transform:uppercase;padding:6px 9px;border:1px solid currentColor}
.state.none{color:var(--muted)} .state.approve{color:var(--ok)} .state.redo{color:var(--redo)}
.shots{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}
.shots figure{margin:0;display:grid;gap:6px}
.shots img{width:100%;aspect-ratio:3/4;object-fit:cover;background:var(--chip);display:block}
.shots figure:last-child img{object-position:center top}
.shots figcaption{font:400 12px/1 var(--type);letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.ingame{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
.ingame figure{margin:0;display:grid;gap:6px}
.ingame img{width:100%;aspect-ratio:16/9;object-fit:cover;background:var(--chip);display:block}
.ingame figcaption,.ingame-note{font:400 12px/1.4 var(--type);letter-spacing:.04em;color:var(--muted)}
.missing{aspect-ratio:3/4;display:grid;place-items:center;background:var(--chip);color:var(--muted);font:400 13px var(--type);text-align:center;padding:10px}
.cols{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:28px}
dl{margin:0;display:grid;grid-template-columns:max-content 1fr;gap:8px 16px}
dt{font:700 12px/1.9 var(--type);letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
dd{margin:0}
.lines{margin:0;padding-left:1.3em;display:grid;gap:6px;font-style:italic}
h3{font:600 15px/1 var(--display);letter-spacing:.06em;text-transform:uppercase;margin:0 0 10px}
.voices{display:grid;gap:8px}
.voice{display:grid;grid-template-columns:auto 1fr auto;align-items:center;gap:10px;padding:8px 10px;border:1px solid var(--rule)}
.voice.picked{border-color:var(--accent);box-shadow:inset 3px 0 0 var(--accent)}
.letter{font:700 22px/1 var(--display);width:1.4em;text-align:center}
.plays{display:flex;flex-wrap:wrap;gap:6px}
button{font:600 14px/1 var(--display);letter-spacing:.04em;border:1px solid var(--rule);background:var(--ground);color:var(--ink);padding:9px 12px;cursor:pointer;min-height:38px}
button:hover{border-color:var(--ink)}
button:focus-visible,textarea:focus-visible,input:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
button.playing{background:var(--ink);color:var(--ground);border-color:var(--ink)}
.pick{display:flex;align-items:center;gap:6px;font:400 13px var(--type);white-space:nowrap}
.verdict{display:grid;gap:10px;border-top:1px solid var(--rule);padding-top:16px}
.verdict .row{display:flex;flex-wrap:wrap;gap:10px;align-items:center}
button.approve{border-color:var(--ok);color:var(--ok)} button.approve.on{background:var(--ok);color:var(--surface)}
button.redo{border-color:var(--redo);color:var(--redo)} button.redo.on{background:var(--redo);color:var(--surface)}
textarea{width:100%;min-height:64px;font:15px/1.4 var(--body);color:var(--ink);background:var(--ground);border:1px solid var(--rule);padding:8px}
.saved{font:400 13px var(--type);color:var(--muted)}
.note-off{font:400 13px var(--type);color:var(--redo)}
footer{font:400 13px/1.5 var(--type);color:var(--muted);border-top:1px solid var(--rule);padding-top:14px}
@media (max-width:760px){ .cols{grid-template-columns:1fr} .shots{gap:6px} dl{grid-template-columns:1fr} dt{line-height:1.2} }
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
</style>

<div class="wrap">
  <header>
    <div class="kicker">LEDGER · approval page · __DATE__</div>
    <h1>Sheila, Ron and Darren, and a jacket, for your yes</h1>
    <p class="how">Each person is approved whole: face, clothes and voice together. Look at the three pictures, play the three lines in each voice (the letters are blind; your approved voice is one of them), pick the voice that is the person, then Approve, or Redo with a word on what is wrong. The jacket, at the end, is judged on its own.</p>
    <div class="tally" id="tally">Loading your earlier verdicts…</div>
  </header>
  <main class="wrap" id="people" style="gap:40px"></main>
  <footer id="foot">Portraits: the local image model (Z-Image-Turbo, Apache-2.0), invented people not based on anyone. Voices: the game's voice engine (Chatterbox) speaking from each reference; the references are his approved clips, voices designed from a written description, and two northern English volunteer recordings per sex. The portraits and voices go into the game only once you approve them; the "in the game tonight" pictures show the stand-ins it uses meanwhile.</footer>
</div>

<script>
const PEOPLE = __DATA__;
const PROOFS = __PROOFS__;
const state = {};           // slug -> {verdict, voice, note}
let db = null, canWrite = true;
let audio = null, playingBtn = null;

function el(tag, attrs, ...kids){
  const n = document.createElement(tag);
  for (const [k,v] of Object.entries(attrs||{})) {
    if (k === "class") n.className = v; else if (k === "text") n.textContent = v; else n.setAttribute(k, v);
  }
  for (const k of kids) if (k) n.append(k);
  return n;
}

function play(src, btn){
  if (audio) { audio.pause(); }
  if (playingBtn) { playingBtn.classList.remove("playing"); }
  if (playingBtn === btn) { playingBtn = null; audio = null; return; }
  audio = new Audio(src); playingBtn = btn; btn.classList.add("playing");
  audio.addEventListener("ended", () => { btn.classList.remove("playing"); if (playingBtn === btn) playingBtn = null; });
  audio.play().catch(() => { btn.classList.remove("playing"); playingBtn = null; });
}

function render(){
  const root = document.getElementById("people");
  root.replaceChildren();
  for (const p of PEOPLE) {
    const s = state[p.slug] || {};
    const sec = el("section", {class:"person", id:p.slug});
    const st = el("span", {class:"state " + (s.verdict || "none"), text: s.verdict === "approve" ? "Approved" : s.verdict === "redo" ? "Redo" : "Not judged"});
    sec.append(el("div", {class:"head"}, el("div", {}, el("h2", {text:p.name}), el("div", {class:"was", text:p.fields["Age"]})), st));

    const shots = el("div", {class:"shots"});
    for (const [shot, label] of [["front","Front"],["profile","Profile"],["full","Full length"]]) {
      const src = p.pictures[shot];
      shots.append(el("figure", {}, src ? el("img", {src, alt: p.name + ", " + label.toLowerCase(), loading:"lazy"}) : el("div", {class:"missing", text:"not made yet"}), el("figcaption", {text:label})));
    }
    sec.append(shots);
    if (p.ingame && (p.ingame.close || p.ingame.mid)) {
      const g = el("div", {class:"ingame"});
      for (const [shot, label] of [["close","In the game tonight, close"],["mid","In the game tonight, mid"]]) {
        if (p.ingame[shot]) g.append(el("figure", {}, el("img", {src:p.ingame[shot], alt:p.name + " in the game, " + shot, loading:"lazy"}), el("figcaption", {text:label})));
      }
      sec.append(el("div", {class:"ingame-note", text:"The stand-in the game uses tonight, in Epic's plain clothes, lit by the street. It is rebuilt to the portraits above once you approve them."}), g);
    }

    const dl = el("dl");
    for (const k of ["Occupation","Face","Body","Hair","Clothes, 1990"]) { dl.append(el("dt", {text:k.replace(", 1990","")}), el("dd", {text:p.fields[k] || ""})); }
    const ol = el("ol", {class:"lines"}); p.lines.forEach(l => ol.append(el("li", {text:"“" + l + "”"})));
    const left = el("div", {}, dl, el("div", {style:"height:14px"}), el("h3", {text:"The three lines"}), ol);

    const vs = el("div", {class:"voices"});
    if (!p.voices.length) vs.append(el("div", {class:"saved", text:"Voices not made yet."}));
    for (const v of p.voices) {
      const plays = el("div", {class:"plays"});
      [["line1","1"],["line2","2"],["line3","3"]].forEach(([k,t]) => { if (v[k]) { const b = el("button", {type:"button", "aria-label": "Voice " + v.letter + ", line " + t, text:"Line " + t}); b.addEventListener("click", () => play(v[k], b)); plays.append(b); } });
      const id = "pick-" + p.slug + "-" + v.letter;
      const radio = el("input", {type:"radio", name:"pick-" + p.slug, id, value:v.letter});
      if (s.voice === v.letter) radio.checked = true;
      radio.addEventListener("change", () => save(p.slug, {voice: v.letter}));
      const row = el("div", {class:"voice" + (s.voice === v.letter ? " picked" : "")}, el("div", {class:"letter", text:v.letter}), plays, el("label", {class:"pick", for:id}, radio, document.createTextNode("This voice")));
      vs.append(row);
    }
    sec.append(el("div", {class:"cols"}, left, el("div", {}, el("h3", {text:"Voices, blind"}), vs)));

    const note = el("textarea", {id:"note-" + p.slug, placeholder:"What is wrong, in a few words (for Redo)"});
    note.value = s.note || "";
    const ok = el("button", {type:"button", class:"approve" + (s.verdict === "approve" ? " on" : ""), text:"Approve " + p.name.split(" ")[0]});
    const redo = el("button", {type:"button", class:"redo" + (s.verdict === "redo" ? " on" : ""), text:"Redo"});
    const saved = el("span", {class:"saved", id:"saved-" + p.slug, text: s.at ? "Saved " + new Date(s.at).toLocaleString() : ""});
    ok.addEventListener("click", () => save(p.slug, {verdict:"approve", note: note.value}));
    redo.addEventListener("click", () => save(p.slug, {verdict:"redo", note: note.value}));
    sec.append(el("div", {class:"verdict"}, note, el("div", {class:"row"}, ok, redo, saved), canWrite ? null : el("div", {class:"note-off", text:"Verdicts cannot be saved from this view."})));
    root.append(sec);
  }
  for (const p of PROOFS) {
    const s = state[p.slug] || {};
    const sec = el("section", {class:"person", id:p.slug});
    const st = el("span", {class:"state " + (s.verdict || "none"), text: s.verdict === "approve" ? "Approved" : s.verdict === "redo" ? "Redo" : "Not judged"});
    sec.append(el("div", {class:"head"}, el("div", {}, el("h2", {text:p.name}), el("div", {class:"was", text:p.was})), st));
    sec.append(el("p", {class:"how", text:p.text}));
    const g = el("div", {class:"ingame"});
    for (const pic of p.pictures) g.append(el("figure", {}, el("img", {src:pic.src, alt:p.name + ": " + pic.caption, loading:"lazy"}), el("figcaption", {text:pic.caption})));
    sec.append(g);
    const note = el("textarea", {id:"note-" + p.slug, placeholder:"What is wrong, in a few words (for Redo)"});
    note.value = s.note || "";
    const ok = el("button", {type:"button", class:"approve" + (s.verdict === "approve" ? " on" : ""), text:"Approve the method"});
    const redo = el("button", {type:"button", class:"redo" + (s.verdict === "redo" ? " on" : ""), text:"Redo"});
    const saved = el("span", {class:"saved", id:"saved-" + p.slug, text: s.at ? "Saved " + new Date(s.at).toLocaleString() : ""});
    ok.addEventListener("click", () => save(p.slug, {verdict:"approve", note: note.value}));
    redo.addEventListener("click", () => save(p.slug, {verdict:"redo", note: note.value}));
    sec.append(el("div", {class:"verdict"}, note, el("div", {class:"row"}, ok, redo, saved), canWrite ? null : el("div", {class:"note-off", text:"Verdicts cannot be saved from this view."})));
    root.append(sec);
  }
  const all = PEOPLE.concat(PROOFS);
  const judged = all.filter(p => state[p.slug] && state[p.slug].verdict).length;
  document.getElementById("tally").innerHTML = "<b>" + judged + " of " + all.length + "</b> judged" + (db ? "" : " · verdicts are not being stored on this view");
}

let writing = Promise.resolve();
function save(slug, patch){
  state[slug] = Object.assign({}, state[slug] || {}, patch, {at: new Date().toISOString()});
  render();
  if (!db || !canWrite) return;
  const body = Object.assign({}, state[slug]);
  writing = writing.then(() => db.doc("verdicts/" + slug).set(body)).catch(e => {
    if (e && e.code === "invalid_argument") { canWrite = false; render(); }
  });
}

render();
(async () => {
  try { db = window.claude && window.claude.use ? await window.claude.use("db") : null; } catch (e) { db = null; }
  if (!db) { render(); return; }
  for (const p of PEOPLE.concat(PROOFS)) {
    try {
      const snap = await db.doc("verdicts/" + p.slug).get();
      if (snap.exists) state[p.slug] = Object.assign({}, snap.data());
    } catch (e) { /* render without it */ }
  }
  render();
})();
</script>
"""


def build(date):
    people, files = gather()
    proofs = gather_proofs(files)
    out_dir = os.path.join(REPO, "production", "approvals", date)
    os.makedirs(out_dir, exist_ok=True)
    data = json.dumps(people, ensure_ascii=False).replace("</", "<\\/")
    pdata = json.dumps(proofs, ensure_ascii=False).replace("</", "<\\/")
    page = PAGE.replace("__DATA__", data).replace("__PROOFS__", pdata).replace("__DATE__", html.escape(date))
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(page)
    with open(os.path.join(out_dir, "files.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(files, fh, indent=1)
    pics = sum(len(p["pictures"]) for p in people)
    vox = sum(len(p["voices"]) for p in people)
    print("approval_page: %d people, %d pictures, %d voice candidates, %d files -> production/approvals/%s/index.html"
          % (len(people), pics, vox, len(files), date))


def selftest():
    ok = bad = 0

    def check(name, cond):
        nonlocal ok, bad
        if cond:
            ok += 1
        else:
            bad += 1
            print("approval_page selftest FAIL " + name)
    v = voices("ron-kirby", ["ron-kirby-B-line1.mp3", "ron-kirby-B-line2.mp3", "ron-kirby-A-reference.mp3", "notes.txt", "sheila-dunn-A-line1.mp3"])
    check("voices are grouped by letter, in order", [x["letter"] for x in v] == ["A", "B"])
    check("a letter carries its lines", v[1].get("line1") == "ron-kirby-B-line1.mp3" and v[1].get("line2") == "ron-kirby-B-line2.mp3")
    check("another person's files are not taken", all("sheila" not in json.dumps(x) for x in v))
    if os.path.exists(os.path.join(CASTING, "sheila-dunn", "SHEET.md")):
        s = read_sheet("sheila-dunn")
        check("the sheet's name is read", s["name"] == "Sheila Dunn")
        check("the sheet's age is read", s["fields"]["Age"].startswith("53"))
        check("the sheet's three lines are read", len(s["lines"]) == 3)
    check("the page carries no script from another host", "src=\"http" not in PAGE)
    print("approval_page selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    build(sys.argv[1] if len(sys.argv) > 1 else "latest")
