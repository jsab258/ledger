"""A named person's street lines, as a page to read (U2, 30 September).

    python tools/own_lines_md.py rocco      # writes production/casting/ron-kirby/STREET-LINES.md

Reads ledger/Assets/Scripts/Core/OwnLines.cs, which the game uses, so what
Jafar reads is what the street says; groups the lines by when they are said, in
plain words. --check compares instead of writing (the file must match the code).
"""
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(REPO, "ledger", "Assets", "Scripts", "Core", "OwnLines.cs")
FOLDERS = {"rocco": ("ron-kirby", "Ron Kirby")}

# When each bank is said, in plain words, in the order a reader meets them.
WHEN = [
    ("recognition/ordinary", "To Tom as he passes"),
    ("recognition/arrival-saw", "To Tom, the first time, having seen him arrive"),
    ("recognition/arrival-heard", "To Tom, the first time, having heard he'd come"),
    ("recognition/sensitive", "To Tom, while talk about him is going round"),
    ("recognition/confronts", "To Tom, when Ron wants it out with him"),
    ("recognition/refuses", "To Tom, when Ron won't help him"),
    ("recognition/avoids", "To Tom, when Ron would rather not stop"),
    ("recognition/taken-saw", "To Tom, having seen the police take him"),
    ("recognition/taken-heard", "To Tom, having heard the police took him"),
    ("recognition/police-asked", "To Tom, after the detective asked Ron about him"),
    ("recognition/police-heard", "To Tom, having heard the police are asking"),
    ("recognition/threat-told", "To Tom, after Tom threatened him"),
    ("recognition/threat-heard", "To Tom, having heard he threatened someone"),
    ("recognition/outfit-did", "To Tom, having heard he did Mickey's run"),
    ("recognition/outfit-refused", "To Tom, having heard he told the outfit no"),
    ("recognition/outfit-wounddown", "To Tom, once Mickey's arrangement is wound down"),
    ("recognition/outfit-noshow", "To Tom, having heard he left the outfit waiting"),
    ("recognition/week-winddown", "To Tom, having heard he's winding Mickey's down"),
    ("recognition/week-takeover", "To Tom, having heard he's taking it all on"),
    ("recognition/week-wontsay", "To Tom, having heard he won't tell Sheila"),
    ("faint", "Half a word to whoever is beside him, once Tom is past"),
    ("ambient/open/ordinary", "Starting a word with a neighbour, in the day"),
    ("ambient/reply/ordinary", "Answering a neighbour, in the day"),
    ("ambient/open/night", "Starting a word at night"),
    ("ambient/reply/night", "Answering at night"),
    ("ambient/open/slump", "Starting a word when trade is dead"),
    ("ambient/reply/slump", "Answering when trade is dead"),
    ("ambient/open/prices", "Starting a word when prices are up"),
    ("ambient/reply/prices", "Answering when prices are up"),
    ("ambient/open/injured", "Starting a word when he's hurt"),
    ("ambient/reply/injured", "Answering somebody who's hurt"),
    ("ambient/open/feud", "To somebody he's fallen out with"),
    ("ambient/reply/feud", "Answering somebody he's fallen out with"),
    ("ambient/open/justnow/glass", "Just after glass breaks"),
    ("ambient/open/justnow/shout", "Just after a shout"),
    ("ambient/open/justnow/crash", "Just after a crash"),
    ("ambient/open/justnow/noise", "Just after a noise"),
    ("ambient/reply/justnow", "Answering, just after"),
    ("ambient/open/settling", "Once it's gone quiet again"),
    ("ambient/reply/settling", "Answering, once it's gone quiet"),
]


def parse(text):
    """speaker id -> bank -> lines, from OwnLines.cs."""
    out = {}
    for m in re.finditer(r'\["(\w+)"\] = new Dictionary<string, string\[\]>\s*\{(.*?)\n            \},', text, re.S):
        banks = {}
        for b in re.finditer(r'\["([a-z/\-]+)"\] = new\[\]\s*\{(.*?)\}', m.group(2), re.S):
            banks[b.group(1)] = [s.encode().decode("unicode_escape") if "\\" in s else s
                                 for s in re.findall(r'"((?:[^"\\]|\\.)*)"', b.group(2))]
        out[m.group(1)] = banks
    return out


def page(who, banks):
    folder, name = FOLDERS[who]
    n = sum(len(v) for v in banks.values())
    lines = ["# %s's own street lines" % name, "",
             "What %s says on the street, written ahead in his own voice: %d lines. The game takes "
             "these before the street's shared lines, and never says one twice until he has said them all. "
             "Made from ledger/Assets/Scripts/Core/OwnLines.cs by tools/own_lines_md.py; the sample before "
             "anybody else's are written." % (name.split()[0], n), ""]
    known = [b for b, _ in WHEN]
    for bank, when in WHEN + [(b, b) for b in sorted(banks) if b not in known]:
        if bank not in banks:
            continue
        lines.append("## " + when)
        lines.append("")
        for l in banks[bank]:
            lines.append("- " + l)
        lines.append("")
    return os.path.join(REPO, "production", "casting", folder, "STREET-LINES.md"), "\n".join(lines)


def main(argv):
    who = next((a for a in argv[1:] if not a.startswith("--")), "rocco")
    with open(SOURCE, encoding="utf-8") as fh:
        banks = parse(fh.read()).get(who)
    if not banks:
        print("no own lines for", who)
        return 1
    path, text = page(who, banks)
    if "--check" in argv:
        try:
            with open(path, encoding="utf-8") as fh:
                same = fh.read() == text
        except OSError:
            same = False
        print("own_lines_md: " + ("matches the code" if same else "OUT OF DATE: run tools/own_lines_md.py " + who))
        return 0 if same else 1
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    print("wrote", os.path.relpath(path, REPO), sum(len(v) for v in banks.values()), "lines")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
