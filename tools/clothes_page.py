#!/usr/bin/env python3
"""The clothing session's page for Jafar's tap: one phone screen, at most three one-line decisions, detail folded.

    python tools/clothes_page.py 2026-10-02     # writes production/approvals/2026-10-02-clothes/index.html

WHY, 2 October. The Marvelous Designer jacket proof failed its blind review in the game on the cut and the lapel
(production/art/clothing/md-suit-jacket/review-1-ingame-ron.md). By Jafar's ruling of 1 October that makes tailored
clothes a blocked capability in Needs you, with research in a different direction; how to go on costs money, so it
is his to choose, with a tap (CLAUDE.md: every page fits one phone screen; pictures judged on the page itself,
tools/page_pictures.py). His picks are stored on the page (the artifact's db, verdicts/<key>), read before every
summary.
"""
import html
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import page_pictures  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DAY = sys.argv[1] if len(sys.argv) > 1 else "2026-10-02"
OUT = os.path.join(REPO, "production", "approvals", DAY + "-clothes")
FRAMES = "F:/LedgerTools/renders/md-jacket-2026-10-02"
PICTURES = [("ron-portrait.jpg", FRAMES + "/ron-stand/ue-portrait-rocco-p2-mid.png",
             "Ron in the jacket, in the game's light: his right lapel collapsed, the front a sack"),
            ("ron-side.jpg", FRAMES + "/ron-stand/ue-motion-rocco-p2-v90/f0001.png",
             "From the side: the side view reads best of all")]

# 2 October, evening: both questions settled by his message (DECISIONS.md, the free-garments entries): free CLO
# patterns are tested in the Marvelous trial first, and the month is bought only if one passes, so the trial runs
# to 15 October. The page stays, its questions withdrawn, so the link never shows a settled question.
ASKS = []
SETTLED = ("Settled by your message of 2 October evening: the free CLO patterns are tested first in the Marvelous "
           "trial, and you buy the month only if one passes. Nothing to tap here.")

CSS = """<title>Tailored clothes</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,500;1,6..72,500&family=Public+Sans:wght@400;600&display=swap">
<style>
:root{--bg:#eef0ee;--card:#fbfcfb;--ink:#1d2326;--soft:#56646a;--line:#cdd4d2;--amber:#a7650f;--amber-bg:#f6e8d3;--ok:#2f6b45}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#141819;--card:#1c2123;--ink:#e3e7e5;--soft:#9aa8ad;--line:#33403f;--amber:#e3a454;--amber-bg:#2f2517;--ok:#7cc497;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#141819;--card:#1c2123;--ink:#e3e7e5;--soft:#9aa8ad;--line:#33403f;--amber:#e3a454;--amber-bg:#2f2517;--ok:#7cc497;color-scheme:dark}
body{background:var(--bg);color:var(--ink);font:15px/1.45 "Public Sans",system-ui,sans-serif;margin:0}
.wrap{max-width:30rem;margin:0 auto;padding-inline:16px;padding-block:18px 28px;display:grid;gap:14px}
.eyebrow{font-size:.72rem;letter-spacing:.08em;text-transform:uppercase;color:var(--soft);margin:0}
h1{font:600 1.35rem/1.2 "Newsreader",Georgia,serif;margin:2px 0 0;text-wrap:balance}
figure{margin:0;display:grid;gap:4px}
figure img{width:100%;height:auto;display:block;border:1px solid var(--line)}
figcaption{font-size:.78rem;color:var(--soft)}
.ask{background:var(--card);border:1px solid var(--line);border-radius:6px;padding:12px;display:grid;gap:10px}
.ask p{margin:0;font-weight:600}
.row{display:flex;gap:8px;flex-wrap:wrap}
.row button{flex:1 1 6rem;font:inherit;padding:10px 8px;border:1px solid var(--line);border-radius:5px;background:var(--bg);color:var(--ink);cursor:pointer}
.row button.rec{border-color:var(--amber)}
.row button[aria-pressed="true"]{background:var(--amber-bg);border-color:var(--amber);font-weight:600}
.row button:focus-visible,summary:focus-visible,textarea:focus-visible{outline:2px solid var(--amber);outline-offset:2px}
.status{font-size:.8rem;color:var(--soft);margin:0;min-height:1.1em}
.status.saved{color:var(--ok)}
details{font-size:.86rem;color:var(--soft)}
summary{cursor:pointer}
details p{margin:6px 0 0;font-weight:400}
textarea{width:100%;box-sizing:border-box;min-height:2.6rem;margin-top:6px;font:inherit;padding:6px 8px;border:1px solid var(--line);border-radius:4px;background:var(--bg);color:var(--ink)}
</style>
"""

SCRIPT = """<script>
let db = null, canWrite = true;
const picks = {};
function status(key, t, ok) { const s = document.getElementById(key + "-status"); s.textContent = t; s.className = "status" + (ok ? " saved" : ""); }
function show(key, p) { document.querySelectorAll('[data-key="' + key + '"] [data-pick]').forEach(b => b.setAttribute("aria-pressed", String(b.dataset.pick === p))); }
function save(key) {
  const note = document.getElementById(key + "-note").value;
  if (!db) { status(key, "Not saved: this view cannot store your answer."); return; }
  if (!canWrite) { status(key, "Not saved: you can read this page but not answer on it."); return; }
  status(key, "Saving...");
  db.doc("verdicts/" + key).set({ pick: picks[key] || null, note, at: new Date().toISOString() })
    .then(() => status(key, "Saved", true))
    .catch(e => { if (e && (e.code === "not_granted" || e.code === "permission_denied")) canWrite = false; status(key, "Not saved: " + (e && e.message ? e.message : "the store refused it") + "."); });
}
document.querySelectorAll("[data-key]").forEach(card => {
  const key = card.dataset.key;
  card.querySelectorAll("[data-pick]").forEach(b => b.addEventListener("click", () => { picks[key] = b.dataset.pick; show(key, picks[key]); save(key); }));
  document.getElementById(key + "-note").addEventListener("change", () => save(key));
});
(async () => {
  try { db = await window.claude?.use?.("db"); } catch (e) { db = null; }
  if (!db) return;
  for (const card of document.querySelectorAll("[data-key]")) {
    const key = card.dataset.key;
    try {
      const snap = await db.doc("verdicts/" + key).get();
      const v = snap && (snap.data ? snap.data() : snap);
      if (v && v.pick) { picks[key] = v.pick; show(key, v.pick); status(key, "Saved", true); }
      if (v && v.note) document.getElementById(key + "-note").value = v.note;
    } catch (e) {}
  }
})();
</script>
"""


def build():
    from PIL import Image
    os.makedirs(OUT, exist_ok=True)
    e = html.escape
    parts = [CSS, '<main class="wrap">',
             '<header><p class="eyebrow">LEDGER · clothes · %s</p><h1>Tailored clothes</h1></header>' % DAY]
    for name, src, cap in PICTURES:
        im = Image.open(src).convert("RGB")
        im.save(os.path.join(OUT, name), quality=92)            # full size, as filmed (2560 by 1440)
        parts.append('<figure><img src="%s" alt="%s" width="%d" height="%d"><figcaption>%s</figcaption></figure>'
                     % (name, e(cap), im.width, im.height, e(cap)))
    parts.append('<section class="ask"><p>%s</p></section>' % e(SETTLED))
    for key, q, opts, more in ASKS:
        btns = "\n".join('<button type="button"%s id="%s-%s" data-pick="%s" aria-pressed="false">%s</button>'
                         % (' class="rec"' if rec else "", key, v, v, e(label)) for v, label, rec in opts)
        parts.append('<section class="ask" data-key="%s"><p>%s</p><div class="row" role="group" aria-label="%s">\n%s\n</div>'
                     '<p class="status" id="%s-status"></p><details><summary>More</summary>%s'
                     '<label for="%s-note">A word, if any</label><textarea id="%s-note"></textarea></details></section>'
                     % (key, e(q), e(q), btns, key, "".join("<p>%s</p>" % m for m in more), key, key))
    parts.append("</main>")
    parts.append(SCRIPT)
    page = page_pictures.apply("\n".join(parts))
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(page)
    print("PAGE", os.path.join(OUT, "index.html"), sorted(os.listdir(OUT)))


if __name__ == "__main__":
    build()
