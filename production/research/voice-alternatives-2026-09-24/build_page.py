"""The listening page, from page.json and vctk-inventory.json, written beside
the rendered clips (VOICEDIR/listen.html) for publishing as an artifact.

    python build_page.py VOICEDIR

REBUILT 24 September on Jafar's word: the first version only played clips,
with "no way to select and save a choice", and "the previous page for the a/b
test was much better". So, like that page: play buttons, one pick per
character saved as he goes into the page's own store (collection "picks", one
document per character, holding the speaker id), and the voices blind -
lettered in a fixed shuffle, the current one not marked - with who's who shown
only once all four are picked."""
import json, pathlib, random, sys

HERE = pathlib.Path(__file__).parent
V = pathlib.Path(sys.argv[1])
page = json.loads((HERE / "page.json").read_text(encoding="utf-8"))
inv = json.loads((HERE / "vctk-inventory.json").read_text(encoding="utf-8"))["speakers"]
ACC = {"NorthernIrish": "Northern Irish", "Unknown": "accent not given"}


def about(s):
    v = inv[s]
    reg = v["region"].strip()
    acc = ACC.get(v["accent"], v["accent"])
    sex = {"M": "man", "F": "woman"}[v["gender"]]
    return "%s %s, %s%s" % (sex, v["age"], acc, (", " + reg) if reg and reg != "nan" else "")


chars = []
for c in page["characters"]:
    order = [c["current"]] + c["alternatives"]
    random.Random("ledger-" + c["id"]).shuffle(order)
    chars.append({"id": c["id"], "name": c["name"], "first": c["name"].split()[0], "who": c["who"],
                  "line": c["line"],
                  "voices": [{"letter": "ABCD"[i], "speaker": s, "now": s == c["current"], "about": about(s)}
                             for i, s in enumerate(order)]})

TEMPLATE = (HERE / "listen-template.html").read_text(encoding="utf-8")
(V / "listen.html").write_text(TEMPLATE.replace("__DATA__", json.dumps(chars, ensure_ascii=False)), encoding="utf-8")
print("wrote", V / "listen.html")
for c in chars:
    print(c["id"], " ".join("%s=%s%s" % (v["letter"], v["speaker"], "*" if v["now"] else "") for v in c["voices"]))
