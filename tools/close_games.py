#!/usr/bin/env python3
"""CLOSE ANY GAME WINDOW LEFT OPEN, BEFORE A NIGHT JOB STARTS (Jafar, 7 October).

    python tools/close_games.py              # close them, say which
    python tools/close_games.py --dry-run    # say which it would close
    python tools/close_games.py --selftest

WHY. On the night of 6 October the session closed at about 00:30 in the middle of the packaged P1
measurement, which left three copies of the game running. At 02:30 the nightly walk could not start
its game, and at 05:15 the morning pictures ran past their time. Jafar: "make the nightly jobs close
any game windows left open before they start." tools/nightly_walk.py and tools/morning_pictures.py
call close_games() first.

WHAT COUNTS AS A GAME WINDOW: the packaged game (LedgerProbe.exe, the launcher and the real binary)
and the editor playing the game (UnrealEditor.exe with -game on its command line). An editor without
-game is a build, an import or a face being made, and is left alone; so is everything else.
"""
import json
import subprocess
import sys


def is_game(name, cmd):
    name = (name or "").lower()
    cmd = (cmd or "").lower()
    if name == "ledgerprobe.exe":
        return True
    return name == "unrealeditor.exe" and " -game" in (" " + cmd)


def running():
    """[(pid, name, command line)] of the processes that could be a game window."""
    ps = ("Get-CimInstance Win32_Process -Filter \"Name='LedgerProbe.exe' or Name='UnrealEditor.exe'\" | "
          "Select-Object ProcessId, Name, CommandLine | ConvertTo-Json -Compress")
    r = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True)
    out = (r.stdout or "").strip()
    if not out:
        return []
    rows = json.loads(out)
    if isinstance(rows, dict):
        rows = [rows]
    return [(row["ProcessId"], row["Name"], row.get("CommandLine") or "") for row in rows]


def close_games(dry=False, log=print):
    games = [(pid, name, cmd) for pid, name, cmd in running() if is_game(name, cmd)]
    for pid, name, cmd in games:
        log("closeGames %s pid=%d %s" % ("would-close" if dry else "closing", pid, name))
        if not dry:
            subprocess.run(["taskkill", "/PID", str(pid), "/F", "/T"], capture_output=True)
    if not games:
        log("closeGames none-open")
    return len(games)


def selftest():
    ok = bad = 0

    def check(name, cond):
        nonlocal ok, bad
        ok, bad = (ok + 1, bad) if cond else (ok, bad + 1)
        if not cond:
            print("close_games selftest FAIL " + name)
    check("the packaged game is a game window", is_game("LedgerProbe.exe", '"F:\\x\\LedgerProbe.exe" LedgerProbe -LedgerSlice'))
    check("the editor playing the game is one", is_game("UnrealEditor.exe", '"UnrealEditor.exe" "x.uproject" -game -LedgerSlice'))
    check("an editor building or importing is left alone", not is_game("UnrealEditor.exe", '"UnrealEditor.exe" "MHAssemble.uproject" -unattended'))
    check("an editor commandlet is left alone", not is_game("UnrealEditor-Cmd.exe", '"UnrealEditor-Cmd.exe" x -run=pythonscript'))
    check("nothing else is", not is_game("python.exe", "python tools/nightly_walk.py -game"))
    print("close_games selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    close_games(dry="--dry-run" in sys.argv)
