#!/usr/bin/env python3
"""The town session's approval page: the casting sheets, the story outline, and
the canon questions they raise, judged in minutes on a phone.

    python tools/town_page.py 2026-09-28      # writes production/approvals/2026-09-28-town/index.html
    python tools/town_page.py --selftest

WHY, 28 September. Jafar's town list: casting sheets for the eleven principals
who had none, text only, with "one approval page for the sheets", and a story
outline "for my approval". The rules: one page a day, each item with one pick
and a note, stored on the page itself (the artifact's db, at verdicts/<key>),
read back the next day and turned into approval files beside what they approve
(tools/approvals.py). Text only today: faces and voice samples are the
builder's, made to the sheets once they are approved.
"""
import html
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CASTING = os.path.join(REPO, "production", "casting")
OUTLINE = os.path.join(REPO, "game-design", "story-outline-2026-09-28.md")
SLUGS = ("tom-nowak", "carol-ellis", "geoffrey-agar", "maureen-jensen", "danny-cammack", "ada",
         "june", "father-emil", "alison-sedman", "philip-danby", "the-fixer")
FIELDS = ("Age", "Origin", "Occupation", "Build", "Face", "Hair", "Clothes, 1990", "How he moves",
          "How she moves", "Voice")

# The canon questions the sheets and the outline raise: one multiple-choice
# question each, the recommendation first and marked, as the rules ask.
QUESTIONS = [
    ("q-emil", "Father Emil's name",
     [("emil", "Keep Emil: the priest of the town's Polish community, who knew Tom's father (recommended: it ties Tom to the parish, and keeps the name the game already uses)"),
      ("walsh", "Father Brendan Walsh, an Irish-born parish priest (the casting research's other offer)")]),
    ("q-fixer", "The Fixer's name",
     [("garbutt", "Keith Garbutt, the casting research's proposal (recommended)"),
      ("none", "No name: he stays \"the Fixer\" to everyone")]),
    ("q-june", "June's surname",
     [("suddaby", "Suddaby, her father's (recommended)"),
      ("married", "A married name you give")]),
    ("q-tom", "Tom's life before the Hook",
     [("unsaid", "Left unsaid: nobody in the game asks and he never tells (recommended: the player fills it)"),
      ("decide", "Decided now, in a line you give")]),
    ("q-ada", "Ada as a retired teacher (the prototype's card)",
     [("out", "Leave it out (recommended: her years of teaching cannot be spoken of without children)"),
      ("in", "Put it back, as a fact she never talks about")]),
    ("q-spine", "The story's spine as the baseline: Tom, the three acts, the three rivals and the empire roster (canon's open question 2)",
     [("yes", "Yes, as outlined (recommended)"),
      ("changes", "Yes, with the changes in your note"),
      ("other", "A different story")]),
]


def read_sheet(slug):
    path = os.path.join(CASTING, slug, "SHEET.md")
    with open(path, encoding="utf-8-sig") as fh:
        text = fh.read()
    name = re.search(r"^#\s+(.+)$", text, re.M).group(1).strip()
    intro = text.split("\n| |", 1)[0].split("\n", 1)[1].strip()
    fields = []
    for m in re.finditer(r"^\|\s*\*\*(.+?)\*\*\s*\|\s*(.+?)\s*\|\s*$", text, re.M):
        if m.group(1) in FIELDS:
            fields.append((m.group(1), m.group(2)))
    lines = re.findall(r'^\d\.\s+"(.+)"\s*$', text, re.M)
    return {"slug": slug, "name": name, "intro": " ".join(intro.split()), "fields": fields, "lines": lines[:3]}


def inline(md):
    """Bold and emphasis, after escaping."""
    s = html.escape(md)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    return s


def outline_html(path=None):
    with open(path or OUTLINE, encoding="utf-8") as fh:
        text = fh.read()
    out, para, items = [], [], []

    def flush():
        if para:
            out.append("<p>" + inline(" ".join(para)) + "</p>")
            para.clear()
        if items:
            out.append("<ul>" + "".join("<li>" + inline(i) + "</li>" for i in items) + "</ul>")
            items.clear()
    for raw in text.split("\n"):
        line = raw.rstrip()
        if line.startswith("# "):
            flush()
            continue  # the page carries its own heading
        if line.startswith("## "):
            flush()
            out.append("<h3>" + inline(line[3:]) + "</h3>")
        elif re.match(r"^(- |\d\. )", line):
            if para:
                flush()
            items.append(re.sub(r"^(- |\d\. )", "", line))
        elif line.startswith("  ") and items:
            items[-1] += " " + line.strip()
        elif not line.strip():
            flush()
        else:
            if items:
                flush()
            para.append(line.strip())
    flush()
    return "\n".join(out)


STYLE = """
:root{--bg:#eef0ee;--card:#fbfcfb;--ink:#1d2326;--soft:#56646a;--line:#cdd4d2;--amber:#a7650f;--amber-bg:#f6e8d3;--flag:#8d2f22;
 --ok:#2f6b45;color-scheme:light}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#141819;--card:#1c2123;--ink:#e3e7e5;--soft:#9aa8ad;--line:#33403f;--amber:#e3a454;--amber-bg:#2f2517;--flag:#e58a78;--ok:#7cc497;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#141819;--card:#1c2123;--ink:#e3e7e5;--soft:#9aa8ad;--line:#33403f;--amber:#e3a454;--amber-bg:#2f2517;--flag:#e58a78;--ok:#7cc497;color-scheme:dark}
body{background:var(--bg);color:var(--ink);font:16px/1.5 "Public Sans",system-ui,sans-serif;margin:0}
.wrap{max-width:46rem;margin:0 auto;padding-inline:16px;padding-block:24px 64px;display:grid;gap:28px}
h1,h2,h3{font-family:"Newsreader",Georgia,serif;font-weight:600;text-wrap:balance;margin:0}
h1{font-size:2rem;line-height:1.15}h2{font-size:1.45rem}h3{font-size:1.1rem;margin-top:14px}
.lede{color:var(--soft);margin:6px 0 0}
.eyebrow{font-size:.75rem;letter-spacing:.08em;text-transform:uppercase;color:var(--soft);margin:0 0 4px}
section{display:grid;gap:14px}
.card{background:var(--card);border:1px solid var(--line);border-radius:6px;padding:16px;display:grid;gap:10px}
.intro{color:var(--soft);font-size:.92rem;margin:0}
dl{display:grid;grid-template-columns:8.5rem 1fr;gap:6px 14px;margin:0;font-size:.95rem}
dt{color:var(--soft);font-weight:600}dd{margin:0}
@media (max-width:520px){dl{grid-template-columns:1fr}dt{margin-top:6px}}
.voice{background:var(--amber-bg);border-radius:4px;padding:8px 10px;font-size:.95rem}
.voice strong{color:var(--flag)}
blockquote{margin:0;padding-left:12px;border-left:3px solid var(--line);font-family:"Newsreader",Georgia,serif;font-size:1.05rem}
.lines{display:grid;gap:6px}
.row{display:flex;flex-wrap:wrap;gap:8px}
.pick{display:flex;gap:8px;align-items:flex-start;border:1px solid var(--line);border-radius:4px;padding:8px 10px;cursor:pointer;flex:1 1 14rem}
.pick input{margin-top:4px}
.pick:has(input:checked){border-color:var(--amber);background:var(--amber-bg)}
textarea{width:100%;box-sizing:border-box;min-height:3.2rem;font:inherit;padding:8px;border:1px solid var(--line);border-radius:4px;background:var(--bg);color:var(--ink)}
.status{font-size:.85rem;color:var(--soft)}
.saved{color:var(--ok)}
.outline p,.outline li{max-width:65ch}
.outline ul{padding-left:1.2rem;margin:4px 0}
:focus-visible{outline:2px solid var(--amber);outline-offset:2px}
img{max-width:100%;height:auto;cursor:zoom-in}
.full{position:fixed;inset:0;background:rgba(0,0,0,.92);display:flex;align-items:center;justify-content:center;z-index:10;cursor:zoom-out}
.full img{max-width:100vw;max-height:100vh;width:auto;height:auto;object-fit:contain;cursor:zoom-out}
"""


def build(date):
    sheets = [read_sheet(s) for s in SLUGS if os.path.exists(os.path.join(CASTING, s, "SHEET.md"))]
    esc = html.escape
    parts = ['<title>Town Sheets and Story</title>',
             '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
             '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,500;6..72,600&family=Public+Sans:wght@400;600&display=swap">',
             "<style>" + STYLE + "</style>", '<main class="wrap">',
             '<header><p class="eyebrow">LEDGER · the town session · ' + esc(date) + '</p>',
             '<h1>Casting sheets and the story</h1>',
             '<p class="lede">Eleven principals on paper, text only, and the story in two pages. '
             'Pick on each, add a note if something is wrong. Faces and voices come after, from the builder, made to what you approve.</p></header>',
             '<section><h2>Your calls first</h2><p class="intro">Canon questions the sheets and the story raise. The first choice in each is my recommendation.</p>']
    for key, title, options in QUESTIONS:
        parts.append(f'<div class="card" data-key="{key}"><h3>{esc(title)}</h3><div class="row">')
        for v, label in options:
            parts.append(f'<label class="pick"><input type="radio" name="{key}" id="{key}-{v}" value="{v}"><span>{esc(label)}</span></label>')
        parts.append(f'</div><textarea id="{key}-note" placeholder="A note, if you want one"></textarea><p class="status" id="{key}-status"></p></div>')
    parts.append('</section><section><h2>The eleven sheets</h2>'
                 '<p class="intro">Each passed two checks: mine against canon and the casting and dress research, and a reviewer\'s who had not seen them made. '
                 'Where a voice is flagged, the approved voice does not fit the age or accent and a new one is needed.</p>')
    for s in sheets:
        key = "sheet-" + s["slug"]
        parts.append(f'<article class="card" data-key="{key}"><h3>{esc(s["name"])}</h3><p class="intro">{inline(s["intro"])}</p><dl>')
        voice = ""
        for k, v in s["fields"]:
            if k == "Voice":
                voice = v
                continue
            parts.append(f"<dt>{esc(k)}</dt><dd>{inline(v)}</dd>")
        parts.append("</dl>")
        if voice:
            parts.append(f'<div class="voice"><span class="eyebrow">Voice</span><br>{inline(voice)}</div>')
        if s["lines"]:
            parts.append('<div class="lines">' + "".join(f"<blockquote>{esc(l)}</blockquote>" for l in s["lines"]) + "</div>")
        parts.append(f'<div class="row"><label class="pick"><input type="radio" name="{key}" id="{key}-approve" value="approve"><span>Approve this sheet</span></label>'
                     f'<label class="pick"><input type="radio" name="{key}" id="{key}-redo" value="redo"><span>Redo it (say what in the note)</span></label></div>'
                     f'<textarea id="{key}-note" placeholder="What is right or wrong, in a few words"></textarea><p class="status" id="{key}-status"></p></article>')
    parts.append('</section><section><h2>The story, in outline</h2><article class="card outline" data-key="story">')
    parts.append(outline_html())
    parts.append('<div class="row"><label class="pick"><input type="radio" name="story" id="story-approve" value="approve"><span>Approve the outline</span></label>'
                 '<label class="pick"><input type="radio" name="story" id="story-redo" value="redo"><span>Redo it (say what in the note)</span></label></div>'
                 '<textarea id="story-note" placeholder="What to change"></textarea><p class="status" id="story-status"></p></article></section>')
    parts.append('<p class="status" id="store-status"></p></main>')
    parts.append(SCRIPT)
    return "\n".join(parts)


SCRIPT = """<script>
// EVERY PICTURE OPENS AT FULL SIZE WHEN TAPPED (Jafar, 30 September); tap again to close.
document.addEventListener("click", e => {
  const open = document.querySelector(".full");
  if (open) { open.remove(); return; }
  const img = e.target.closest && e.target.closest("img");
  if (!img) return;
  const d = document.createElement("div"); d.className = "full";
  const big = document.createElement("img"); big.src = img.currentSrc || img.src; big.alt = img.alt || "";
  d.appendChild(big); document.body.appendChild(d);
});
document.addEventListener("keydown", e => { if (e.key === "Escape") { const o = document.querySelector(".full"); if (o) o.remove(); } });
let db = null, canWrite = true;
const state = {};
function status(key, text, ok){const s=document.getElementById(key+"-status"); if(s){s.textContent=text; s.className="status"+(ok?" saved":"");}}
function save(key){
  const card=document.querySelector('[data-key="'+key+'"]');
  const picked=card.querySelector('input[type=radio]:checked');
  const note=document.getElementById(key+"-note").value;
  state[key]={pick:picked?picked.value:null,note:note,at:new Date().toISOString()};
  if(!db){status(key,"Not saved: this view cannot store your answer.");return;}
  if(!canWrite){status(key,"Not saved: you can read this page but not answer on it.");return;}
  status(key,"Saving...");
  db.doc("verdicts/"+key).set(state[key]).then(()=>status(key,"Saved",true)).catch(e=>{
    if(e&&(e.code==="not_granted"||e.code==="permission_denied"||e.code==="invalid_argument")) canWrite=false;
    status(key,"Not saved: "+(e&&e.message?e.message:"the store refused it")+".");});
}
for(const card of document.querySelectorAll("[data-key]")){
  const key=card.dataset.key;
  card.querySelectorAll("input[type=radio]").forEach(r=>r.addEventListener("change",()=>save(key)));
  const t=document.getElementById(key+"-note"); if(t) t.addEventListener("change",()=>save(key));
}
(async()=>{
  try{ db = await window.claude?.use?.("db"); }catch(e){ db=null; }
  const g=document.getElementById("store-status");
  if(!db){ g.textContent="Answers cannot be stored in this view."; return; }
  for(const card of document.querySelectorAll("[data-key]")){
    const key=card.dataset.key;
    try{
      const snap=await db.doc("verdicts/"+key).get();
      const v=snap&&(snap.data?snap.data():snap);
      if(v&&v.pick){const r=document.getElementById(key+"-"+v.pick); if(r) r.checked=true;}
      if(v&&v.note){document.getElementById(key+"-note").value=v.note;}
      if(v&&(v.pick||v.note)) status(key,"Saved",true);
    }catch(e){}
  }
})();
</script>"""


def selftest():
    s = read_sheet("tom-nowak")
    assert s["name"] == "Tom Nowak" and any(k == "Voice" for k, _ in s["fields"]), s
    page = build("2026-09-28")
    assert page.count('data-key="sheet-') == len(SLUGS), page.count('data-key="sheet-')
    assert "<title>" in page[:8000] and 'data-key="story"' in page
    assert "<script" not in outline_html()
    print("town_page selftest: ok,", len(SLUGS), "sheets,", len(QUESTIONS), "questions")
    return 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    date = argv[1] if len(argv) > 1 else "2026-09-28"
    out_dir = os.path.join(REPO, "production", "approvals", date + "-town")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "index.html")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(build(date))
    print("wrote", os.path.relpath(path, REPO))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
