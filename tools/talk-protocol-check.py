#!/usr/bin/env python3
"""THE TALK PROGRAM'S PROTOCOL, KEPT TRUE (town list 6av).

production/specs/talk-protocol.md says every field the talk program reads
from the game and writes back. This reads ledger/TalkHelper/Program.cs, finds
every field it reads (TryGetProperty, Bool, Str) and every field it writes
(the anonymous objects it serialises), and fails naming each one the page
does not mention, so the page cannot quietly fall behind the program.

    python tools/talk-protocol-check.py
    python tools/talk-protocol-check.py --selftest
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROGRAM = os.path.join(ROOT, "ledger", "TalkHelper", "Program.cs")
SPEC = os.path.join(ROOT, "production", "specs", "talk-protocol.md")


def program_body(src):
    """The program without its self-test, which builds requests for itself."""
    cut = src.find("static async Task<int> SelfTest(")
    return src if cut < 0 else src[:cut] + src[src.find("\n    static", cut + 10):] if src.find("\n    static", cut + 10) > 0 else src[:cut]


def read_fields(src):
    names = set(re.findall(r'TryGetProperty\("([A-Za-z]+)"', src))
    names |= set(re.findall(r'\b(?:Bool|Str|Int|Num)\(\w+, "([A-Za-z]+)"\)', src))
    return names


def split_top(s):
    parts, depth, cur, quote = [], 0, [], None
    i = 0
    while i < len(s):
        c = s[i]
        if quote:
            cur.append(c)
            if c == "\\" and i + 1 < len(s):
                cur.append(s[i + 1]); i += 2; continue
            if c == quote:
                quote = None
        elif c in "\"'":
            quote = c; cur.append(c)
        elif c in "({[":
            depth += 1; cur.append(c)
        elif c in ")}]":
            depth -= 1; cur.append(c)
        elif c == "," and depth == 0:
            parts.append("".join(cur)); cur = []
        else:
            cur.append(c)
        i += 1
    if "".join(cur).strip():
        parts.append("".join(cur))
    return parts


def members(body):
    """The member names of an anonymous object's body, nested ones too."""
    out = set()
    for part in split_top(body):
        p = part.strip()
        m = re.match(r'^@?([A-Za-z_]\w*)\s*=(?!=)\s*(.*)$', p, re.S)
        if m:
            out.add(m.group(1))
            value = m.group(2)
        else:
            ident = re.findall(r'@?([A-Za-z_]\w*)\s*$', p)
            if ident:
                out.add(ident[-1])
            value = p
        for nested in re.finditer(r'new\s*\{', value):
            start = nested.end()
            depth, j = 1, start
            while j < len(value) and depth:
                if value[j] == "{": depth += 1
                elif value[j] == "}": depth -= 1
                j += 1
            out |= members(value[start:j - 1])
    return out


def written_fields(src):
    names = set()
    for m in re.finditer(r'Serialize\(new\s*\{', src):
        start = m.end()
        depth, j = 1, start
        while j < len(src) and depth:
            if src[j] == "{": depth += 1
            elif src[j] == "}": depth -= 1
            j += 1
        names |= members(src[start:j - 1])
    return names


def missing(spec, names):
    return sorted(n for n in names if not re.search(r'[`"]' + re.escape(n) + r'[`"]', spec))


def main(argv):
    if "--selftest" in argv:
        assert members('id, to, reply = brush, ms = 0L, why = a ?? b.Latest(), notice = new { title = T, text = X.Y(z) }, @unchecked, helper.Online') == \
            {"id", "to", "reply", "ms", "why", "notice", "title", "text", "unchecked", "Online"}
        assert read_fields('r.TryGetProperty("deed", out var d); Bool(a, "held")') == {"deed", "held"}
        assert missing("| `id` | x |\n\"to\"", {"id", "to", "reply"}) == ["reply"]
        print("talk-protocol-check selftest: ok")
        return 0
    src = open(PROGRAM, encoding="utf-8").read()
    body = program_body(src)
    spec = open(SPEC, encoding="utf-8").read()
    reads, writes = read_fields(body), written_fields(body)
    gone_r, gone_w = missing(spec, reads), missing(spec, writes)
    for n in gone_r:
        print(f"  read, not on the page: {n}")
    for n in gone_w:
        print(f"  written, not on the page: {n}")
    ok = not gone_r and not gone_w and reads and writes
    print(f"talk-protocol-check: {'ok' if ok else 'FAILED'} - {len(reads)} fields read, {len(writes)} written, {len(gone_r) + len(gone_w)} not on the page")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
