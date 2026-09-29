#!/usr/bin/env python3
"""One piece of street clutter made live in Blender by a Claude Code helper, timed, then its gate pictures.

    python tools/blender-live/live_piece.py --id pillar-box --brief F:/LedgerTools/tmp/clutter/pillar-box/brief.md
        [--attempt 1] [--minutes 25]

WHY, 29 September (the builder's list, item 10: "Street clutter, live in
Blender: ten pieces ... with the time each took against the script route's
times"). The Blender connection (the official Blender Lab MCP server,
production/research/blender-mcp) loads only when a Claude Code session starts,
so the session that runs the list cannot use it; a helper started here with
Claude Code's non-interactive mode can, on Jafar's subscription (his rule of
29 September: no API calls in development; the helper's own record says
apiKeySource none, and any ANTHROPIC_API_KEY is taken out of its environment).
The helper gets the piece's brief (what the research found: the real thing's
type, size, colours and parts, and its reference photographs as links), builds
it in the live Blender (tools/blender-live/start-blender-live.ps1 starts it),
looks at it as it goes, and exports it; then tools/meshgen/blender/
clutter_sheet.py makes the same three gate pictures the script route's pieces
get. Writes timing.json beside them: the helper's minutes, turns and result.
"""
import json
import os
import subprocess
import sys
import time

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WORK = r"F:\LedgerTools\tmp\clutter"
BLENDER45 = r"C:\LedgerTools\blender\4.5.13\blender-4.5.13-windows-x64\blender.exe"

PROMPT = """You are making one piece of street clutter for a video game set in a northern English town in 1990, working live in the Blender that is open, through the blender tools only.

The piece: {id}. Its brief, from the project's research (the real thing's type, size, colours and parts, and photographs of it):

{brief}

Build it at real-world scale in metres, standing on the ground at z = 0, centred on x = 0, y = 0, its front facing -y. Start by deleting everything in the scene. Use modelled geometry for the shapes that give it its silhouette and the parts a person would recognise it by; plain materials (Principled BSDF, base colour, roughness, metallic) in the real thing's colours; no textures from outside. Keep it game-ready: under 5,000 triangles, no hidden or duplicate objects. Look at it as you go (the screenshot tools) and compare it with the brief's sizes and parts; fix what is wrong.

When it is done, run Python in Blender that applies all transforms and exports the whole scene as glTF binary to {glb} and saves the .blend to {blend}. Then reply with two short lines: what you made, and anything in the brief you could not match."""


def run(pid, brief_path, attempt, minutes):
    d = os.path.join(WORK, pid)
    os.makedirs(d, exist_ok=True)
    brief = open(brief_path, encoding="utf-8").read()
    glb = os.path.join(d, "live-%d.glb" % attempt).replace("\\", "/")
    blend = os.path.join(d, "live-%d.blend" % attempt).replace("\\", "/")
    env = dict(os.environ)
    env.pop("ANTHROPIC_API_KEY", None)          # never a key: the helper runs on his subscription
    t0 = time.time()
    # THE PROMPT ON STANDARD INPUT: through the Windows shell a prompt of many
    # lines in the arguments was cut at its first line break (the first live
    # attempt, 29 September, ran 1.3 minutes on half a sentence).
    p = subprocess.run(["claude", "-p", "--allowedTools", "mcp__blender", "--output-format", "json"],
                       input=PROMPT.format(id=pid, brief=brief, glb=glb, blend=blend),
                       cwd=REPO, env=env, capture_output=True, text=True, encoding="utf-8",
                       timeout=minutes * 60, shell=(os.name == "nt"))
    took = (time.time() - t0) / 60.0
    try:
        res = json.loads(p.stdout[p.stdout.index("{"):])
    except Exception:
        res = {"raw": p.stdout[-800:], "stderr": p.stderr[-400:]}
    timing = {"id": pid, "attempt": attempt, "route": "live", "minutes": round(took, 1),
              "turns": res.get("num_turns"), "result": str(res.get("result", res.get("raw", "")))[:600],
              "stderr": p.stderr[-300:], "glb": glb,
              "made": os.path.isfile(glb)}
    if timing["made"]:
        sheet = os.path.join(d, "live-%d-sheet" % attempt)
        subprocess.run([BLENDER45, "--background", "--factory-startup", "--python",
                        os.path.join(REPO, "tools", "meshgen", "blender", "clutter_sheet.py"), "--", "--piece", glb, "--out", sheet],
                       capture_output=True, text=True)
        timing["sheet"] = sheet
        try:
            timing["dims"] = json.load(open(os.path.join(sheet, "dims.json")))
        except Exception:
            timing["dims"] = None
    json.dump(timing, open(os.path.join(d, "live-%d-timing.json" % attempt), "w", encoding="utf-8"), indent=1)
    print(json.dumps(timing, indent=1))
    return 0 if timing["made"] else 1


if __name__ == "__main__":
    a = sys.argv[1:]
    get = lambda k, dflt=None: a[a.index(k) + 1] if k in a else dflt
    sys.exit(run(get("--id"), get("--brief"), int(get("--attempt", "1")), float(get("--minutes", "25"))))
