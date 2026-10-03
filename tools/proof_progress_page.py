"""The proof view's progress page: one picture of the hook frame after each finished step,
for Jafar's eyes only, nothing to decide (his rule of 3 October).

    python tools/proof_progress_page.py --out DIR      # writes DIR/index.html and DIR/pictures/
    python tools/proof_progress_page.py --selftest

WHY A PAGE AND NOT GIT. The overview (FOR-JAFAR.md) is text in git, and since 3 October only
text and small files go into git; so the pictures sit on this one private page, linked from the
overview's first lines, and the page is published again (same address) after each step. The
frame comes to his approval page only when it stands beside the Hook sheet; this page asks
nothing. Since the evening of 3 October each step's frame also has a reduced preview in git
for outside reviewers (its "preview" in steps.json, made by tools/make_preview.py).

WHAT IT SHOWS, from production/proof-view/steps.json (text, in git): the Hook sheet as the bar
(flipped to canon's sides, as tools/hook-pair.py compares it), then, newest first, each finished
step: its number and name, one line of what changed, the reviewer's verdict in a phrase, and the
frame at 2560 by 1440 from F:/LedgerTools/renders/proof-<step>/ (each picture opens full-screen
in the shared viewer, tools/page_pictures.py).
"""
import html
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STEPS = os.path.join(ROOT, "production", "proof-view", "steps.json")
SHEET = os.path.join(ROOT, "production", "reference", "hook-sheet.png")

PAGE = """<title>Proof View</title>
<style>
:root{--bg:#f4f1ea;--fg:#1d1c1a;--muted:#6b665c;--rule:#d9d3c6;--accent:#8a3b22;--card:#fbf9f4}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#171614;--fg:#ece8df;--muted:#a39d90;--rule:#36332e;--accent:#d98a62;--card:#1f1d1a;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#171614;--fg:#ece8df;--muted:#a39d90;--rule:#36332e;--accent:#d98a62;--card:#1f1d1a;color-scheme:dark}
body{background:var(--bg);color:var(--fg);font:16px/1.5 Georgia,"Times New Roman",serif}
main{max-width:1100px;margin:0 auto;padding-inline:16px;padding-block:20px 48px;display:grid;gap:28px}
h1{font-size:1.5rem;margin:0;text-wrap:balance}
.lede{color:var(--muted);margin:4px 0 0;font-size:.95rem}
section{display:grid;gap:8px;min-width:0}
h2{font-size:1.1rem;margin:0}
h2 .n{color:var(--accent);font-variant-numeric:tabular-nums;letter-spacing:.04em}
p{margin:0}
.verdict{color:var(--muted);font-size:.9rem}
figure{margin:0;display:grid;gap:6px}
figure img{width:100%;height:auto;display:block;border-radius:3px}
figcaption{color:var(--muted);font-size:.85rem}
hr{border:0;border-top:1px solid var(--rule);margin:0}
</style>
<main>
<header><h1>The proof view, step by step</h1>
<p class="lede">For your eyes only: one frame after each finished step of the list's item 2, nothing to decide. The frame comes to your page when it stands beside the Hook sheet. Tap a picture to see it full size.</p></header>
%(steps)s
<hr>
<section><h2>The bar: the Hook sheet</h2>
<figure><img src="pictures/hook-sheet-flipped.jpg" alt="The Hook sheet's street, flipped to canon's sides"><figcaption>The approved Hook sheet, flipped so Mickey's stands on the right as canon has it.</figcaption></figure></section>
</main>
"""


def picture_name(s):
    """Each step's frame under its own name: every step's file is ue-vign_hook_day.png."""
    return "step-%s.jpg" % s["step"]


def step_html(s):
    return ("<section><h2><span class=\"n\">%s</span> %s</h2><p>%s</p><p class=\"verdict\">%s</p>"
            "<figure><img src=\"pictures/%s\" alt=\"The hook frame after step %s\"><figcaption>%s</figcaption></figure></section>"
            % (html.escape(s["step"]), html.escape(s["name"]), html.escape(s["changed"]),
               html.escape(s.get("verdict", "")), html.escape(picture_name(s)),
               html.escape(s["step"]), html.escape(s.get("caption", "The game's own camera and light, 2560 by 1440."))))


def build(out_dir):
    from PIL import Image
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import page_pictures
    steps = json.load(open(STEPS, encoding="utf-8"))["steps"]
    pics = os.path.join(out_dir, "pictures")
    os.makedirs(pics, exist_ok=True)
    sheet = Image.open(SHEET).convert("RGB").crop((0, 0, 2048, 1088)).transpose(Image.FLIP_LEFT_RIGHT)
    sheet.save(os.path.join(pics, "hook-sheet-flipped.jpg"), quality=90)
    for s in steps:
        Image.open(s["picture"]).convert("RGB").save(os.path.join(pics, picture_name(s)), quality=90)
    body = "\n".join(step_html(s) for s in reversed(steps)) or "<p>No step finished yet.</p>"
    page = page_pictures.apply(PAGE.replace("%(steps)s", body))   # the CSS has its own percent signs
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(page)
    return os.path.join(out_dir, "index.html")


def selftest():
    s = {"step": "2.1", "name": "Composition", "changed": "a <b>", "verdict": "pass", "picture": "F:/x/ue-vign_hook_day.png"}
    h = step_html(s)
    two = step_html(dict(s, step="2.2"))
    ok = ["&lt;b&gt;" in h, "pictures/step-2.1.jpg" in h, "pictures/step-2.2.jpg" in two, "<title>" in PAGE[:200]]
    print("proof_progress_page selftest: passed=%d/%d failed=%d" % (sum(ok), len(ok), len(ok) - sum(ok)))
    return 0 if all(ok) else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    out = sys.argv[sys.argv.index("--out") + 1]
    print(build(out))
