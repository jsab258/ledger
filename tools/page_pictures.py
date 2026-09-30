"""PICTURES AT FULL SIZE on every approval page (Jafar, 30 September:
Wednesday's pictures were too small to judge; CLAUDE.md, "PICTURES AT FULL
SIZE"). Every picture shown for judging is as wide as the page's column,
one to a row, never cropped; a tap opens it at its own full resolution in a
view that scrolls and zooms, and a tap closes it.

Any page tool applies it to its template once:

    import page_pictures
    PAGE = page_pictures.apply(PAGE)

    python tools/page_pictures.py --selftest
"""
import sys

CSS = """
/* PICTURES AT FULL SIZE (tools/page_pictures.py, Jafar 30 September) */
.capgrid,.cands,.pair{grid-template-columns:1fr!important}
.capgrid img,.pair img,.cands img,figure img{width:100%!important;height:auto!important;aspect-ratio:auto!important;object-fit:contain!important}
main img,section img{cursor:zoom-in}
.fullsize{position:fixed;inset:0;z-index:1000;background:#000;overflow:auto;display:none;-webkit-overflow-scrolling:touch;cursor:zoom-out}
.fullsize.on{display:block}
.fullsize img{max-width:none!important;width:auto!important;height:auto!important;display:block;margin:0 auto}
.fullsize .fullhint{position:fixed;top:calc(8px + env(safe-area-inset-top, 0px));right:12px;font:600 13px/1 sans-serif;color:#fff;background:rgba(0,0,0,.6);padding:8px 10px}
"""

JS = """
// PICTURES AT FULL SIZE (tools/page_pictures.py): a tap on a picture opens it
// at its own resolution; a tap anywhere on that view closes it.
(function(){
  const view = document.createElement("div");
  view.className = "fullsize";
  const big = document.createElement("img");
  const hint = document.createElement("div");
  hint.className = "fullhint";
  hint.textContent = "Full size. Tap to close.";
  view.append(big, hint);
  document.body.append(view);
  view.addEventListener("click", () => { view.classList.remove("on"); big.removeAttribute("src"); });
  document.addEventListener("click", (e) => {
    const t = e.target;
    if (!(t instanceof HTMLImageElement) || view.contains(t)) return;
    big.src = t.currentSrc || t.src;
    big.alt = t.alt || "";
    view.scrollTo(0, 0);
    view.classList.add("on");
  });
})();
"""


def apply(page):
    """The template with the full-size rule: the styles before the first
    </style>, the script before the last </script>. Applied twice, once."""
    if "PICTURES AT FULL SIZE (tools/page_pictures.py" in page:
        return page
    s = page.find("</style>")
    e = page.rfind("</script>")
    if s < 0 or e < 0:
        raise ValueError("page_pictures: the template needs a <style> and a <script>")
    page = page[:s] + CSS + page[s:]
    e = page.rfind("</script>")
    return page[:e] + JS + page[e:]


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
    check("the styles go inside the style block", out.index(".fullsize{") < out.index("</style>"))
    check("the script goes inside the last script block", out.index("classList.add(\"on\")") < out.rindex("</script>"))
    check("applied twice is applied once", apply(out) == out)
    check("pictures are one to a row", "grid-template-columns:1fr" in CSS)
    check("no picture is cropped", "object-fit:contain" in CSS and "aspect-ratio:auto" in CSS)
    check("the full view keeps the picture's own size", "max-width:none" in CSS)
    try:
        apply("<p>no style</p>")
        check("a template without style or script is refused", False)
    except ValueError:
        check("a template without style or script is refused", True)
    print("page_pictures selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else 0)
