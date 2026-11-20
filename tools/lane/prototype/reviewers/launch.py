"""Fill a player type's or a breaker's brief for one session (lane task 4t, pieces 2 and 3).

Found on the first smoke run (20 Nov): filling the briefs by plain text replacement turned LEDGER_PLAY_PORT into
LEDGER_PLAY_8771 and wrote the launcher's own note into the brief. This fills each placeholder only as a whole word.

    python launch.py player  --card 1 --minutes 60 --port 8771 --playdir DIR  > brief.txt
    python launch.py breaker --card A --minutes 30 --port 8772 --playdir DIR  > brief.txt
"""
import argparse, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))

def section(text, head):
    m = re.search(r"^## %s.*?(?=^## |\Z)" % re.escape(head), text, re.S | re.M)
    if not m:
        raise SystemExit("no card %r" % head)
    return m.group(0).strip()

def fill(brief, card, minutes, port, playdir, name="..."):
    card = re.sub(r" ?\((?:[A-Z]{1,2}\d+(?:, ?)?)+\)", "", card)   # design codes such as (X4) mean nothing to a blind player
    brief = brief.replace("in the shape at the end of PLAYER-TYPES.md (copied here)", "in this shape")
    brief = re.sub(r'"type": "[^".]+"', '"type": "%s"' % name, brief)
    card = re.sub(r'"type": "[^".]+"', '"type": "%s"' % name, card)
    for k, v in (("CARD", card), ("MINUTES", str(minutes)), ("PLAYDIR", playdir)):
        brief = re.sub(r"(?<![A-Za-z_])%s(?![A-Za-z_])" % k, lambda m: v, brief)
    brief = re.sub(r"(?<![A-Za-z])PORT(?![A-Za-z_])", str(port), brief)   # LEDGER_PLAY_PORT keeps its name
    brief = brief.replace("LEDGER_PLAY_%s=" % port, "LEDGER_PLAY_PORT=")
    left = [k for k in ("CARD", "MINUTES", "PLAYDIR") if re.search(r"(?<![A-Za-z_])%s(?![A-Za-z_])" % k, brief)]
    if left or "LEDGER_PLAY_PORT=%s" % port not in brief:
        raise SystemExit("brief not filled: %s" % (left or "port"))
    return brief

def main(argv=None):
    a = argparse.ArgumentParser()
    a.add_argument("kind", choices=["player", "breaker"])
    a.add_argument("--card", required=True)
    a.add_argument("--minutes", type=int, required=True)
    a.add_argument("--port", type=int, required=True)
    a.add_argument("--playdir", required=True)
    o = a.parse_args(argv)
    if o.kind == "player":
        prompt = open(os.path.join(HERE, "players", "PLAY-PROMPT.md"), encoding="utf-8").read().split("\n---\n", 1)[1]
        cards = open(os.path.join(HERE, "players", "PLAYER-TYPES.md"), encoding="utf-8").read()
        card = section(cards, o.card + ".")
        name = card.splitlines()[0].split(". ", 1)[1].strip()
    else:
        prompt = open(os.path.join(HERE, "breakers", "BREAK-PROMPT.md"), encoding="utf-8").read().split("\n---\n", 1)[1]
        cards = open(os.path.join(HERE, "breakers", "BREAKERS.md"), encoding="utf-8").read()
        card = section(cards, o.card + ".") + "\n\n" + section(cards, "What each breaker returns")
        name = card.splitlines()[0].split(". ", 1)[1].strip().lower().replace("the ", "", 1)
    sys.stdout.write(fill(prompt, card, o.minutes, o.port, o.playdir, name).strip() + "\n")

if __name__ == "__main__":
    main()
