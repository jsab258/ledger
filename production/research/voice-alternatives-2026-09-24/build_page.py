"""The listening page, from page.json and vctk-inventory.json, written beside
the rendered clips (VOICEDIR/listen.html) for publishing as an artifact.

    python build_page.py VOICEDIR"""
import html, json, pathlib, sys
HERE = pathlib.Path(__file__).parent
V = pathlib.Path(sys.argv[1])
page = json.loads((HERE / "page.json").read_text(encoding="utf-8"))
inv = json.loads((HERE / "vctk-inventory.json").read_text(encoding="utf-8"))["speakers"]
ACC = {"NorthernIrish": "Northern Irish", "Unknown": "not given"}

def who(s):
    v = inv[s]
    acc = ACC.get(v["accent"], v["accent"])
    reg = v["region"].strip()
    where = "%s, %s" % (acc, reg) if reg and reg != "nan" else acc
    return "%s, %s" % ({"M": "man", "F": "woman"}.get(v["gender"], v["gender"]), v["age"]), where

cards = []
for c in page["characters"]:
    rows = []
    for s in [c["current"]] + c["alternatives"]:
        g, where = who(s)
        tag = '<span class="tag now">cast 14 Aug, never approved</span>' if s == c["current"] else '<span class="tag alt">alternative</span>'
        rows.append(f'''
      <div class="row{' is-now' if s == c['current'] else ''}">
        <div class="spk"><span class="id">{s}</span>{tag}<span class="meta">{html.escape(g)} · {html.escape(where)}</span></div>
        <div class="clip"><span class="lbl">As {html.escape(c['name'].split()[0])}</span><audio controls preload="none" src="line_{c['id']}_{s}.wav"></audio></div>
        <div class="clip"><span class="lbl">Their own recording</span><audio controls preload="none" src="own_{s}.wav"></audio></div>
      </div>''')
    cards.append(f'''
    <section class="char" id="{c['id']}">
      <header>
        <h2>{html.escape(c['name'])}</h2>
        <p class="brief">{html.escape(c['who'])}</p>
        <p class="line">“{html.escape(c['line'])}”</p>
      </header>
      <div class="rows">{''.join(rows)}
      </div>
    </section>''')

doc = f'''<title>Four Voices to Pick</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600&family=Source+Sans+3:wght@400;600&family=IBM+Plex+Mono:wght@500&display=swap">
<style>
:root {{
  --ground: #edf0eb; --surface: #f8f9f6; --ink: #1d241f; --muted: #58625b; --rule: #c8cfc6;
  --accent: #a3372a; --accent-soft: #f3e1dd; --alt: #2f5563; --alt-soft: #dde8ec;
  --display: "Barlow Condensed", "Arial Narrow", sans-serif;
  --body: "Source Sans 3", "Segoe UI", system-ui, sans-serif;
  --mono: "IBM Plex Mono", ui-monospace, Consolas, monospace;
}}
@media (prefers-color-scheme: dark) {{
  :root:not([data-theme="light"]) {{
    color-scheme: dark;
    --ground: #141816; --surface: #1c211e; --ink: #e3e8e2; --muted: #9aa59d; --rule: #323a35;
    --accent: #e0786a; --accent-soft: #3a211d; --alt: #8fbccb; --alt-soft: #1c2d33;
  }}
}}
:root[data-theme="dark"] {{
  color-scheme: dark;
  --ground: #141816; --surface: #1c211e; --ink: #e3e8e2; --muted: #9aa59d; --rule: #323a35;
  --accent: #e0786a; --accent-soft: #3a211d; --alt: #8fbccb; --alt-soft: #1c2d33;
}}
body {{ background: var(--ground); color: var(--ink); font: 16px/1.5 var(--body); }}
.wrap {{ max-width: 980px; margin: 0 auto; padding-inline: 16px; padding-block: 28px 56px; display: grid; gap: 28px; }}
.top h1 {{ font: 600 clamp(30px, 5vw, 44px)/1.05 var(--display); letter-spacing: .01em; margin: 0 0 10px; text-wrap: balance; }}
.top p {{ margin: 0 0 8px; max-width: 68ch; color: var(--muted); }}
.top p strong {{ color: var(--ink); font-weight: 600; }}
nav {{ display: flex; flex-wrap: wrap; gap: 8px; }}
nav a {{ font: 500 15px var(--display); letter-spacing: .06em; text-transform: uppercase; color: var(--ink); text-decoration: none; border: 1px solid var(--rule); padding: 4px 10px; border-radius: 3px; }}
nav a:hover, nav a:focus-visible {{ border-color: var(--accent); color: var(--accent); outline: none; }}
.char {{ background: var(--surface); border: 1px solid var(--rule); border-radius: 4px; padding: 20px; display: grid; gap: 16px; }}
.char h2 {{ font: 600 30px/1 var(--display); margin: 0; letter-spacing: .01em; }}
.brief {{ margin: 4px 0 0; color: var(--muted); }}
.line {{ margin: 10px 0 0; font-style: italic; max-width: 65ch; }}
.rows {{ display: grid; gap: 0; }}
.row {{ display: grid; grid-template-columns: minmax(220px, 1.1fr) 1fr 1fr; gap: 12px 16px; align-items: center; padding: 12px 0; border-top: 1px solid var(--rule); }}
.row.is-now {{ background: linear-gradient(90deg, var(--accent-soft), transparent 70%); margin-inline: -20px; padding-inline: 20px; }}
.spk {{ display: flex; flex-wrap: wrap; align-items: baseline; gap: 4px 10px; }}
.id {{ font: 500 15px var(--mono); }}
.meta {{ flex-basis: 100%; color: var(--muted); font-size: 14px; }}
.tag {{ font: 600 12px var(--display); letter-spacing: .08em; text-transform: uppercase; padding: 1px 6px; border-radius: 2px; }}
.tag.now {{ color: var(--accent); border: 1px solid var(--accent); }}
.tag.alt {{ color: var(--alt); background: var(--alt-soft); }}
.clip {{ display: grid; gap: 4px; }}
.lbl {{ font: 500 13px var(--display); letter-spacing: .08em; text-transform: uppercase; color: var(--muted); }}
audio {{ width: 100%; max-width: 100%; height: 36px; }}
.foot {{ color: var(--muted); font-size: 14px; max-width: 72ch; display: grid; gap: 6px; }}
.foot p {{ margin: 0; }}
@media (max-width: 720px) {{
  .row {{ grid-template-columns: 1fr; }}
}}
</style>
<div class="wrap">
  <div class="top">
    <h1>Four voices to pick</h1>
    <p><strong>Aldous, Danny, June and Zlata</strong> were cast on 14 August without your yes. Each is shown here beside three other speakers from the same Edinburgh recordings (VCTK), none of whom voices anyone else in the game. Tell me one pick per character, and nothing is cast until you do.</p>
    <p>“As …” is the character's line in that voice, made by Nano, the small version of the game's voice engine, on this PC. “Their own recording” is the speaker reading the same sentence every speaker in the collection reads, so you can compare like with like.</p>
    <p>The speakers in these recordings are all 18 to 38. None is as old as Aldous (61) or Zlata (43), so age has to come from the engine's settings, not the voice.</p>
  </div>
  <nav aria-label="Characters">{''.join(f'<a href="#{c["id"]}">{html.escape(c["name"])}</a>' for c in page["characters"])}</nav>
  {''.join(cards)}
  <div class="foot">
    <p>Recordings: CSTR VCTK Corpus, Centre for Speech Technology Research, University of Edinburgh, CC BY 4.0. Using its recordings to clone game characters is a risk you accepted on the record on 24 September.</p>
    <p>Picked by accent and sex from the speakers nobody else in the cast uses: {html.escape(", ".join(s for c in page["characters"] for s in c["alternatives"]))}.</p>
  </div>
</div>
'''
(V / "listen.html").write_text(doc, encoding="utf-8")
print("wrote", V / "listen.html")
