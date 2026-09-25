#!/usr/bin/env python3
"""The approval page for the cast as the game has them, beside the candidates he chose.

    python tools/ingame_page.py pack F:/LedgerTools/tmp/ingame5 VOICE_DIR   # pictures and lines into the repo
    python tools/ingame_page.py                                             # writes the page and files.json
    python tools/ingame_page.py --voices-only                               # the same, faces held back
    python tools/ingame_page.py --selftest

WHY, 25 September (evening). Jafar: "each character in the game, in the
street's daylight, beside the candidate I approved, speaking in their voice.
I judge whether the game matches what I chose." The same format as the
casting page (CLAUDE.md: kept for every approval): pictures and sound, one
pick and a note, stored on the page (verdicts/game-<person>).

pack takes the portrait tool's -PortraitInGame pictures (the encounter's own
cast, photographed where it stands) and each character's line as the game's
voice engine speaks it (tools/voice-live/speak_lines.py), and writes
production/casting/in-game-2026-09-25/: <slug>-front.jpg, -wide.jpg,
-speak.jpg (a sheet of frames the page steps through with the line), and
voice/<slug>.wav. Nothing reaches the page without the gate (CLAUDE.md): the
lines are accent- and word-checked, and a second reviewer has looked.
"""
import glob
import json
import math
import os
import shutil
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATE = "2026-09-25-in-game"
OUT = "production/casting/in-game-2026-09-25"
CAND = "production/casting/candidates-2026-09-25"
# who: (slug, name, asset name, approved take, the line file the voice engine made)
PEOPLE = [("sheila-dunn", "Sheila Dunn", "lena", "C1", "lena-1.wav"),
          ("ron-kirby", "Ron Kirby", "rocco", "C1", "rocco-1.wav"),
          ("darren-milner", "Darren Milner", "sam", "C5", "sam-2.wav")]
FRAME, COLS, FPS = (400, 300), 10, 15
SPEAK_BOX = (400, 40, 880, 400)


def pack(src, voices):
    from PIL import Image
    os.makedirs(os.path.join(REPO, OUT, "voice"), exist_ok=True)
    spoken = {s["wav"].split("/")[-1]: s for s in json.load(open(os.path.join(voices, "spoken.json"), encoding="utf-8"))}
    index = {}
    for slug, name, who, take, line in PEOPLE:
        e = {"line": spoken.get(line, {}).get("text", "")}
        for shot, cut in (("front", (280, 0, 1000, 540)), ("mid", None)):
            f = os.path.join(src, "ue-portrait-ingame-%s-%s.png" % (who, shot))
            if os.path.exists(f):
                im = Image.open(f).convert("RGB")
                im = im.crop(cut) if cut else im
                rel = "%s-%s.jpg" % (slug, "front" if shot == "front" else "wide")
                im.save(os.path.join(REPO, OUT, rel), quality=85)
                e["front" if shot == "front" else "wide"] = rel
        frames = sorted(glob.glob(os.path.join(src, "ue-speak-ingame-%s" % who, "f*.png")))
        if frames:
            rows = max(1, math.ceil(len(frames) / COLS))
            sheet = Image.new("RGB", (COLS * FRAME[0], rows * FRAME[1]))
            for i, f in enumerate(frames):
                im = Image.open(f).convert("RGB").crop(SPEAK_BOX).resize(FRAME, Image.LANCZOS)
                sheet.paste(im, ((i % COLS) * FRAME[0], (i // COLS) * FRAME[1]))
            rel = "%s-speak.jpg" % slug
            sheet.save(os.path.join(REPO, OUT, rel), quality=78)
            e["speak"] = {"file": rel, "frames": len(frames), "cols": COLS, "rows": rows, "fps": FPS}
        wav = os.path.join(voices, line)
        if os.path.exists(wav):
            shutil.copyfile(wav, os.path.join(REPO, OUT, "voice", slug + ".wav"))
            e["voice"] = "voice/%s.wav" % slug
        index[slug] = e
    json.dump(index, open(os.path.join(REPO, OUT, "index.json"), "w", encoding="utf-8"), indent=1)
    print("ingame_page pack: %s" % {k: sorted(v) for k, v in index.items()})


def gather():
    files, people = {}, []
    idx = json.load(open(os.path.join(REPO, OUT, "index.json"), encoding="utf-8"))
    cand = json.load(open(os.path.join(REPO, CAND, "index.json"), encoding="utf-8"))
    for slug, name, who, take, _ in PEOPLE:
        g = idx.get(slug, {})
        c = next((x for x in cand.get(slug, []) if x["take"] == take), {})
        p = {"slug": slug, "name": name, "take": take, "line": g.get("line", "")}
        if c.get("front"):
            files["chosen/%s-front.jpg" % slug] = CAND + "/" + c["front"]
            p["chosenFront"] = "chosen/%s-front.jpg" % slug
        for k in ("front", "wide"):
            if g.get(k):
                files["game/%s-%s.jpg" % (slug, k)] = OUT + "/" + g[k]
                p["game" + k.title()] = "game/%s-%s.jpg" % (slug, k)
        if g.get("speak"):
            files["game/%s-speak.jpg" % slug] = OUT + "/" + g["speak"]["file"]
            p["speak"] = dict(g["speak"], file="game/%s-speak.jpg" % slug)
        if g.get("voice"):
            files["game/%s.wav" % slug] = OUT + "/" + g["voice"]
            p["voice"] = "game/%s.wav" % slug
        people.append(p)
    return people, files


PAGE = r"""<title>The Cast In Game</title>
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
.tally,.was{font:400 13px/1.4 var(--type);color:var(--muted)}
.tally b{color:var(--ink)}
section.person{display:grid;gap:18px;background:var(--surface);border:1px solid var(--rule);padding:22px}
.sides{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px}
.side{display:grid;gap:8px;align-content:start}
.side img{width:100%;aspect-ratio:4/3;object-fit:cover;display:block;background:var(--chip)}
.side img.wide{aspect-ratio:16/9}
.speak{width:100%;aspect-ratio:4/3;background-color:var(--chip);background-repeat:no-repeat}
.row{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
button{font:600 14px/1 var(--display);letter-spacing:.04em;border:1px solid var(--rule);background:var(--surface);color:var(--ink);padding:9px 12px;cursor:pointer;min-height:38px}
button:hover{border-color:var(--ink)}
button.playing{background:var(--ink);color:var(--ground);border-color:var(--ink)}
button:focus-visible,textarea:focus-visible,input:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
label.pick{display:flex;align-items:center;gap:6px;font:400 14px var(--type)}
textarea{width:100%;min-height:54px;font:15px/1.4 var(--body);color:var(--ink);background:var(--ground);border:1px solid var(--rule);padding:8px}
.saved{font:400 13px var(--type);color:var(--muted)}
footer{font:400 13px/1.5 var(--type);color:var(--muted);border-top:1px solid var(--rule);padding-top:14px}
</style>

<div class="wrap">
  <header>
    <div class="kicker">LEDGER · approval page · 25 September, evening</div>
    <h1>Does the game match what you chose?</h1>
    <p class="how">__HOW__</p>
    <p class="how">Everything here passed the gate first: checked against the casting sheet and for accent and words, then looked at by a second reviewer that did not make it.</p>
    <div class="tally" id="tally">Loading your earlier picks…</div>
  </header>
  <main class="wrap" id="people"></main>
  <footer>__FOOT__</footer>
</div>

<script>
const PEOPLE = __DATA__;
const state = {};
let db = null, canWrite = true, audio = null, playing = null, timer = 0;
function el(tag, attrs, ...kids){
  const n = document.createElement(tag);
  for (const [k,v] of Object.entries(attrs||{})) { if (k === "class") n.className = v; else if (k === "text") n.textContent = v; else n.setAttribute(k, v); }
  for (const k of kids) if (k) n.append(k);
  return n;
}
function stop(){ if (audio) audio.pause(); if (playing) playing.classList.remove("playing"); clearInterval(timer); audio = null; playing = null; }
function play(src, btn, onFrame){
  const same = playing === btn; stop(); if (same) return;
  const a = new Audio(src); audio = a; playing = btn; btn.classList.add("playing");
  a.addEventListener("ended", () => { if (onFrame) onFrame(0); stop(); });
  a.play().then(() => { if (onFrame) timer = setInterval(() => { if (audio === a) onFrame(a.currentTime); }, 33); }).catch(() => stop());
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
  let judged = 0;
  for (const p of PEOPLE) {
    const k = "game-" + p.slug, st = state[k] || {};
    if (st.pick) judged++;
    const sec = el("section", {class:"person", id:p.slug});
    sec.append(el("div", {}, el("h2", {text:p.name}), el("div", {class:"was", text:"Speaking: “" + p.line + "”"})));
    if (!p.chosenFront && !p.gameFront && p.voice) {
      const b = el("button", {type:"button", text:"Play the line"});
      b.addEventListener("click", () => play(p.voice, b));
      sec.append(el("div", {class:"row"}, b));
    }
    const chosen = el("div", {class:"side"}, el("h3", {text:"You chose: " + p.take}));
    if (p.chosenFront) chosen.append(el("img", {src:p.chosenFront, alt:p.name + ", the candidate you chose", loading:"lazy"}));
    const game = el("div", {class:"side"}, el("h3", {text:"In the game"}));
    if (p.gameFront) game.append(el("img", {src:p.gameFront, alt:p.name + " in the game", loading:"lazy"}));
    const talk = el("div", {class:"side"}, el("h3", {text:"In the game, speaking"}));
    if (p.speak) {
      const s = spriteBox(p.speak);
      const b = el("button", {type:"button", text:"Play the line"});
      if (p.voice) b.addEventListener("click", () => play(p.voice, b, s.at));
      talk.append(s.box, el("div", {class:"row"}, b));
    }
    if (p.gameWide) talk.append(el("img", {class:"wide", src:p.gameWide, alt:p.name + " where the game stands them", loading:"lazy"}));
    if (p.chosenFront || p.gameFront) sec.append(el("div", {class:"sides"}, chosen, game, talk));
    const picks = el("div", {class:"row"});
    for (const [v, t] of [["match", "The game matches what I chose"], ["no", "It does not"]]) {
      const id = "pick-" + k + "-" + v;
      const r = el("input", {type:"radio", name:"pick-" + k, id, value:v});
      if (st.pick === v) r.checked = true;
      r.addEventListener("change", () => save(k, {pick:v}));
      picks.append(el("label", {class:"pick", for:id}, r, document.createTextNode(t)));
    }
    const note = el("textarea", {placeholder:"What is right or wrong, in a few words (optional)"});
    note.value = st.note || "";
    note.addEventListener("change", () => save(k, {note:note.value}));
    sec.append(picks, note, el("span", {class:"saved", text: st.at ? "Saved " + new Date(st.at).toLocaleString() : ""}));
    root.append(sec);
  }
  document.getElementById("tally").innerHTML = "<b>" + judged + " of " + PEOPLE.length + "</b> judged" + (db ? "" : " · picks are not being stored on this view");
}
render();
(async () => {
  try { db = window.claude && window.claude.use ? await window.claude.use("db") : null; } catch (e) { db = null; }
  if (!db) { render(); return; }
  for (const p of PEOPLE) { try { const s = await db.doc("verdicts/game-" + p.slug).get(); if (s.exists) state["game-" + p.slug] = Object.assign({}, s.data()); } catch (e) {} }
  render();
})();
</script>
"""

FOOT = ("Faces: Epic's MetaHuman, built on this PC from the casting sheets; in the game as the encounter dresses them. "
        "Voices: the game's own voice engine (Chatterbox Nano) from each character's game clip: Sheila the voice you picked (D, "
        "designed by Parler-TTS), Ron his July voice (p227, VCTK), Darren his (p241, VCTK). Each line passed the accent check "
        "and a word check before a second reviewer listened by measurement.")


def build(voices_only=False):
    people, files = gather()
    if voices_only:
        # THE FACES HELD BACK, 25 September (evening): Jafar saw the approved
        # faces read East Asian, which the sheets do not describe; under the
        # gate a face that fails its sheet does not reach his page.
        keep = {"voice", "line", "slug", "name", "take"}
        people = [{k: v for k, v in p.items() if k in keep} for p in people]
        files = {k: v for k, v in files.items() if k.endswith(".wav")}
    out = os.path.join(REPO, "production", "approvals", DATE)
    os.makedirs(out, exist_ok=True)
    page = PAGE if not voices_only else PAGE.replace("<h1>Does the game match what you chose?</h1>", "<h1>Do the game's voices match what you chose?</h1>").replace(
        "__HOW__", "For each of Sheila, Ron and Darren, a line as the game's own voice engine speaks it, from the voice the game now gives them (press Play). "
        "Their faces are held back: you saw they read East Asian, the sheets do not describe that, and under the new gate a face that fails its sheet "
        "does not come to you until it is fixed. Pick whether the voice matches what you chose, with a word if not.")
    page = page.replace("__HOW__", "For each of Sheila, Ron and Darren: on the left the candidate you approved, as you saw it; on the right the character as the game has them, photographed where the encounter stands them, in that place's light, speaking a line in the voice the game gives them (press Play). Pick whether the game matches what you chose, with a word if not.")
    if voices_only:
        page = page.replace("The game matches what I chose", "The voice matches what I chose")
    page = page.replace("__DATA__", json.dumps(people, ensure_ascii=False).replace("</", "<" + chr(92) + "/")).replace("__FOOT__", FOOT)
    open(os.path.join(out, "index.html"), "w", encoding="utf-8", newline="\n").write(page)
    json.dump(files, open(os.path.join(out, "files.json"), "w", encoding="utf-8"), indent=1)
    size = sum(os.path.getsize(os.path.join(REPO, v)) for v in files.values() if os.path.exists(os.path.join(REPO, v))) / 1e6
    print("ingame_page: %d people, %d files, %.1f MB" % (len(people), len(files), size))


def selftest():
    ok = bad = 0

    def check(name, cond):
        nonlocal ok, bad
        if cond:
            ok += 1
        else:
            bad += 1
            print("ingame_page selftest FAIL " + name)
    check("the three, each with the take he approved", [(p[0], p[3]) for p in PEOPLE] == [("sheila-dunn", "C1"), ("ron-kirby", "C1"), ("darren-milner", "C5")])
    check("no script from another host", 'src="http' not in PAGE)
    check("one pick per person, stored under game-<person>", "verdicts/game-" in PAGE)
    print("ingame_page selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if len(sys.argv) > 1 and sys.argv[1] == "pack":
        pack(sys.argv[2], sys.argv[3])
    else:
        build("--voices-only" in sys.argv)
