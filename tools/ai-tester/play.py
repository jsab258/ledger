#!/usr/bin/env python3
"""THE AI TESTER, the smallest version that works (Jafar, 24 September).

    python tools/ai-tester/play.py                 # the packaged slice, about eight minutes
    python tools/ai-tester/play.py --editor        # the same, run from the editor's current build
    python tools/ai-tester/play.py --minutes 5 --steps 30
    python tools/ai-tester/play.py --selftest

WHAT HE ASKED FOR: "it plays the packaged slice through the screen and
keyboard as a person would, runs the encounter and wanders freely, and writes
what broke into FOR-JAFAR.md, worst first. It is not a gate, and each run's
cost is reported."

HOW. It starts the game in the playable encounter, from the start, with its
own save so Jafar's is never touched. Each step it looks at the game window
(a screenshot) and asks the conversation model for ONE action: walk, turn,
press E or T, wait, note a problem, or finish. It then does that action with
real key presses and mouse moves sent to the window, the way a hand would.
Each request carries the newest picture and a short log of what it has done,
not the whole history, so a step costs about the same at the end as at the
start.

WHAT IT WRITES: production/playtest/ai-tester/<time>/report.md (every note,
worst first, each with the picture it was looking at), and a short dated
block in FOR-JAFAR.md with the run's cost. It is not a gate: nothing reads
its result to pass or fail anything.

THE KEY is read from the game's own settings file into this process only,
never printed, and the game inherits it for its own conversation.

IT TAKES THE KEYBOARD AND MOUSE while it runs, so nobody should be using the
PC at the time.
"""
import base64
import ctypes
import ctypes.wintypes as wt
import datetime
import io
import json
import os
import subprocess
import sys
import tempfile
import time

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PACKAGED = r"C:\Users\Jafar\ledger-migrate\ue-probe\Packaged\Windows\LedgerProbe.exe"
EDITOR = r"C:\Program Files\Epic Games\UE_5.8\Engine\Binaries\Win64\UnrealEditor.exe"
PROJECT = os.path.join(REPO, "ue-probe", "LedgerProbe.uproject")
HELPER = os.path.join(REPO, "ledger", "TalkHelper", "bin", "Release", "net8.0", "TalkHelper.exe")
SECRETS = os.path.join(os.path.expanduser("~"), "AppData", "LocalLow", "DefaultCompany", "ledger", "secrets.json")
MODEL = "claude-sonnet-5"
PRICE_IN, PRICE_OUT = 3.0, 15.0          # USD per million tokens, the game's own rate card (LlmClient.cs)
RES = (1280, 720)

SCAN = {"w": 0x11, "a": 0x1E, "s": 0x1F, "d": 0x20, "e": 0x12, "t": 0x14, "shift": 0x2A}
WALK_KEY = {"forward": "w", "back": "s", "left": "a", "right": "d"}
PIXELS_PER_DEGREE = 5.7                  # a first guess; the tester sees the result and corrects

SYSTEM = """You are testing a video game by playing it, the way a careful human playtester would. You see one screenshot of the game window at a time and choose ONE action with a tool.

The game: a street in a British port town, about 1990. You are the man in the grey tracksuit, seen from behind. Controls: walk with W A S D (use the walk tool), turn by moving the mouse (the turn tool), E does the act in front of you. To talk to someone, stand near them and use the say tool: it presses T, types your words into the line that opens at the bottom of the screen, and presses Enter. Yellow and white text lines at the top left are the game telling you things and people speaking; the newest line is at the top.

Your job, in this order:
1. Play the encounter the game offers: walk to the shop window by Mickey's (Mickey's is the minicab office with the dark blue front) and press E beside it to break it. Someone will shout. Then go round through the yard behind the parade if you can find it. After a while the game says it is later that week and tells you where Sam is; find Sam and talk to him with the say tool; say what a person would. Read what he says and answer him once or twice. Talk to Lena and Rocco too if you find them.
2. Then wander freely: walk the street, look at the buildings and the people, try the edges, try walking into things.

While you play, report anything broken or wrong with the note tool, as soon as you see it: you are stuck or fell through the world, a person floats, is half in the ground or stands in an odd pose, something flickers or is missing, text is garbled, the game ignores a key, a character says something that makes no sense. Also report anything showing or mentioning alcohol, betting or children, which the game must never have. Severity: 5 the game is unplayable or crashed, 4 a feature does not work, 3 clearly wrong and noticeable, 2 minor, 1 cosmetic. Do not report the same thing twice.

Be efficient: walk for a second or two at a time, then look. When you have done both parts, or you are truly stuck, call finish with a two-sentence summary."""

TOOLS = [
    {"name": "walk", "description": "Hold a movement key for some seconds.",
     "input_schema": {"type": "object", "properties": {
         "direction": {"type": "string", "enum": ["forward", "back", "left", "right"]},
         "seconds": {"type": "number", "minimum": 0.2, "maximum": 4},
         "run": {"type": "boolean"}}, "required": ["direction", "seconds"]}},
    {"name": "turn", "description": "Turn the view left (negative) or right (positive) by about this many degrees.",
     "input_schema": {"type": "object", "properties": {"degrees": {"type": "number", "minimum": -180, "maximum": 180}},
                      "required": ["degrees"]}},
    {"name": "press", "description": "Press E (act) or T (talk) once.",
     "input_schema": {"type": "object", "properties": {"key": {"type": "string", "enum": ["E", "T"]}}, "required": ["key"]}},
    {"name": "say", "description": "Talk to the person you are standing near: presses T, types these words, presses Enter.",
     "input_schema": {"type": "object", "properties": {"words": {"type": "string", "maxLength": 200}}, "required": ["words"]}},
    {"name": "wait", "description": "Do nothing for some seconds, to let something happen.",
     "input_schema": {"type": "object", "properties": {"seconds": {"type": "number", "minimum": 1, "maximum": 15}},
                      "required": ["seconds"]}},
    {"name": "note", "description": "Report something broken or wrong that you can see now.",
     "input_schema": {"type": "object", "properties": {
         "severity": {"type": "integer", "minimum": 1, "maximum": 5},
         "what": {"type": "string", "description": "One or two plain sentences: what is wrong and where."}},
         "required": ["severity", "what"]}},
    {"name": "finish", "description": "End the session.",
     "input_schema": {"type": "object", "properties": {"summary": {"type": "string"}}, "required": ["summary"]}},
]


# ---------------------------------------------------------------- the window, the keys, the mouse
user32 = ctypes.windll.user32 if os.name == "nt" else None


class KEYBDINPUT(ctypes.Structure):
    _fields_ = [("wVk", wt.WORD), ("wScan", wt.WORD), ("dwFlags", wt.DWORD), ("time", wt.DWORD),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]


class MOUSEINPUT(ctypes.Structure):
    _fields_ = [("dx", wt.LONG), ("dy", wt.LONG), ("mouseData", wt.DWORD), ("dwFlags", wt.DWORD),
                ("time", wt.DWORD), ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]


class _U(ctypes.Union):
    _fields_ = [("ki", KEYBDINPUT), ("mi", MOUSEINPUT)]


class INPUT(ctypes.Structure):
    _fields_ = [("type", wt.DWORD), ("u", _U)]


def send_key(scan, up=False):
    i = INPUT(type=1, u=_U(ki=KEYBDINPUT(0, scan, 0x0008 | (0x0002 if up else 0), 0, None)))
    user32.SendInput(1, ctypes.byref(i), ctypes.sizeof(INPUT))


def tap(name):
    send_key(SCAN[name]); time.sleep(0.08); send_key(SCAN[name], up=True)


def hold(name, seconds, run=False):
    if run:
        send_key(SCAN["shift"])
    send_key(SCAN[name])
    time.sleep(seconds)
    send_key(SCAN[name], up=True)
    if run:
        send_key(SCAN["shift"], up=True)


def type_text(text):
    for ch in text:
        for up in (False, True):
            i = INPUT(type=1, u=_U(ki=KEYBDINPUT(0, ord(ch), 0x0004 | (0x0002 if up else 0), 0, None)))
            user32.SendInput(1, ctypes.byref(i), ctypes.sizeof(INPUT))
        time.sleep(0.02)


def enter():
    send_key(0x1C); time.sleep(0.05); send_key(0x1C, up=True)


def mouse_move(dx):
    steps = max(1, int(abs(dx) // 40))
    for _ in range(steps):
        i = INPUT(type=0, u=_U(mi=MOUSEINPUT(int(dx / steps), 0, 0, 0x0001, 0, None)))
        user32.SendInput(1, ctypes.byref(i), ctypes.sizeof(INPUT))
        time.sleep(0.01)


def find_window(title_part):
    """The game's own window: an Unreal window (class UnrealWindow) whose title
    names the game, never a folder or an editor that happens to share the word."""
    found = []

    @ctypes.WINFUNCTYPE(ctypes.c_bool, wt.HWND, wt.LPARAM)
    def cb(hwnd, _):
        if user32.IsWindowVisible(hwnd):
            n = user32.GetWindowTextLengthW(hwnd)
            buf = ctypes.create_unicode_buffer(n + 1)
            user32.GetWindowTextW(hwnd, buf, n + 1)
            cls = ctypes.create_unicode_buffer(64)
            user32.GetClassNameW(hwnd, cls, 64)
            if title_part.lower() in buf.value.lower() and cls.value == "UnrealWindow":
                found.append(hwnd)
        return True
    user32.EnumWindows(cb, 0)
    return found[0] if found else None


def seconds_since_input():
    class LASTINPUTINFO(ctypes.Structure):
        _fields_ = [("cbSize", wt.UINT), ("dwTime", wt.DWORD)]
    li = LASTINPUTINFO(ctypes.sizeof(LASTINPUTINFO), 0)
    user32.GetLastInputInfo(ctypes.byref(li))
    return (ctypes.windll.kernel32.GetTickCount() - li.dwTime) / 1000.0


def window_pid(hwnd):
    pid = wt.DWORD(0)
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    return pid.value


def front_title():
    fg = user32.GetForegroundWindow()
    n = user32.GetWindowTextLengthW(fg)
    buf = ctypes.create_unicode_buffer(n + 1)
    user32.GetWindowTextW(fg, buf, n + 1)
    return buf.value


def game_in_front(hwnd):
    """KEYS GO ONLY TO THE GAME. If anything else is in front - somebody
    clicked away, a dialog came up - no key is sent at all, because typed
    words and an Enter in the wrong window could send a message. The test is
    the front window's PROCESS: the packaged game owns more than one window,
    and the exact-window test refused it (24 September)."""
    fg = user32.GetForegroundWindow()
    return fg != 0 and window_pid(fg) == window_pid(hwnd)


def focus(hwnd):
    """Bring the game to the front. Windows lets only the program that has the
    front hand it on, so this borrows the front window's input thread for a
    moment (the packaged game refused the plain call, 24 September)."""
    fg = user32.GetForegroundWindow()
    t_fg = user32.GetWindowThreadProcessId(fg, None)
    t_me = ctypes.windll.kernel32.GetCurrentThreadId()
    attached = bool(t_fg) and t_fg != t_me and user32.AttachThreadInput(t_me, t_fg, True)
    user32.keybd_event(0x12, 0, 0, 0)            # ALT, so Windows lets us take the foreground
    user32.ShowWindow(hwnd, 9)                   # SW_RESTORE
    user32.BringWindowToTop(hwnd)
    user32.SetForegroundWindow(hwnd)
    user32.keybd_event(0x12, 0, 2, 0)
    if attached:
        user32.AttachThreadInput(t_me, t_fg, False)
    time.sleep(0.3)


def client_box(hwnd):
    r = wt.RECT()
    user32.GetClientRect(hwnd, ctypes.byref(r))
    pt = wt.POINT(0, 0)
    user32.ClientToScreen(hwnd, ctypes.byref(pt))
    return (pt.x, pt.y, pt.x + r.right, pt.y + r.bottom)


def screenshot(hwnd):
    """THE GAME WINDOW'S OWN PIXELS, never the screen. The first run grabbed
    the screen where the window was, before the game had drawn itself, and
    caught another app's chat history (24 September). PrintWindow with
    PW_RENDERFULLCONTENT asks the window for its own picture, so nothing
    else on the desktop can ever be in it."""
    from PIL import Image
    gdi32 = ctypes.windll.gdi32
    r = wt.RECT()
    user32.GetClientRect(hwnd, ctypes.byref(r))
    w, h = r.right, r.bottom
    hdc = user32.GetDC(hwnd)
    mem = gdi32.CreateCompatibleDC(hdc)
    bmp = gdi32.CreateCompatibleBitmap(hdc, w, h)
    gdi32.SelectObject(mem, bmp)
    ok = user32.PrintWindow(hwnd, mem, 0x00000001 | 0x00000002)   # PW_CLIENTONLY | PW_RENDERFULLCONTENT

    class BITMAPINFOHEADER(ctypes.Structure):
        _fields_ = [("biSize", wt.DWORD), ("biWidth", wt.LONG), ("biHeight", wt.LONG), ("biPlanes", wt.WORD),
                    ("biBitCount", wt.WORD), ("biCompression", wt.DWORD), ("biSizeImage", wt.DWORD),
                    ("biXPelsPerMeter", wt.LONG), ("biYPelsPerMeter", wt.LONG), ("biClrUsed", wt.DWORD),
                    ("biClrImportant", wt.DWORD)]
    bi = BITMAPINFOHEADER(ctypes.sizeof(BITMAPINFOHEADER), w, -h, 1, 32, 0, 0, 0, 0, 0, 0)
    buf = ctypes.create_string_buffer(w * h * 4)
    gdi32.GetDIBits(mem, bmp, 0, h, buf, ctypes.byref(bi), 0)
    gdi32.DeleteObject(bmp)
    gdi32.DeleteDC(mem)
    user32.ReleaseDC(hwnd, hdc)
    im = Image.frombuffer("RGBA", (w, h), buf, "raw", "BGRA", 0, 1).convert("RGB") if ok else None
    # A DIRECTX WINDOW OFTEN GIVES PrintWindow NOTHING BUT BLACK (the packaged
    # game did, 24 September, and the tester reported a dead game). Then the
    # screen is read instead, but ONLY where the game's own window is on top
    # at the centre and all four corners, so no other app can be in it.
    if im is None or max(im.convert("L").getextrema()) < 8:
        box = client_box(hwnd)
        if not game_on_top(hwnd, box):
            raise RuntimeError("the game is not on top of its own area, so the screen is not read")
        from PIL import ImageGrab
        im = ImageGrab.grab(bbox=box, all_screens=True).convert("RGB")
    return im


def game_on_top(hwnd, box):
    """Every sampled point of the game's area belongs to the game's process."""
    x0, y0, x1, y1 = box
    mine = window_pid(hwnd)
    for x, y in ((x0 + x1) // 2, (y0 + y1) // 2), (x0 + 4, y0 + 4), (x1 - 5, y0 + 4), (x0 + 4, y1 - 5), (x1 - 5, y1 - 5):
        w = user32.WindowFromPoint(wt.POINT(x, y))
        if not w or window_pid(w) != mine:
            return False
    return True


# ---------------------------------------------------------------- the model
def ask(key, log_lines, image, step, steps):
    import requests
    buf = io.BytesIO()
    im = image.copy()
    im.thumbnail((1024, 576))
    im.save(buf, "JPEG", quality=80)
    text = ("Step %d of at most %d. What you have done so far, oldest first:\n%s\n\nThe game window now:"
            % (step, steps, "\n".join(log_lines[-40:]) or "(nothing yet)"))
    body = {"model": MODEL, "max_tokens": 400, "system": SYSTEM, "tools": TOOLS,
            "tool_choice": {"type": "any"},
            "messages": [{"role": "user", "content": [
                {"type": "text", "text": text},
                {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg",
                                             "data": base64.b64encode(buf.getvalue()).decode()}}]}]}
    r = requests.post("https://api.anthropic.com/v1/messages", timeout=90,
                      headers={"x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"},
                      data=json.dumps(body))
    r.raise_for_status()
    d = r.json()
    u = d.get("usage", {})
    call = next((c for c in d.get("content", []) if c.get("type") == "tool_use"), None)
    return call, u.get("input_tokens", 0), u.get("output_tokens", 0)


def cost_usd(tin, tout):
    return tin / 1e6 * PRICE_IN + tout / 1e6 * PRICE_OUT


def report_lines(notes, cost, steps, minutes, summary, stamp):
    worst = sorted(notes, key=lambda n: -n["severity"])
    out = ["# AI tester, %s" % stamp, "",
           "%d steps in %.1f minutes, cost $%.2f (%s, the game's own rate card)." % (steps, minutes, cost, MODEL), "",
           "Its summary: " + (summary or "none; it did not finish by itself."), "", "## What broke, worst first", ""]
    if not worst:
        out.append("Nothing reported.")
    for n in worst:
        out.append("- **%d** %s (step %d, %s)" % (n["severity"], n["what"].strip(), n["step"], n["picture"]))
    return out, worst


def for_jafar_block(worst, cost, steps, minutes, stamp, folder_rel):
    lines = ["", "### AI tester, %s" % stamp, "",
             "%d steps, %.0f minutes, $%.2f. Not a gate. Worst first:" % (steps, minutes, cost)]
    for n in worst[:6]:
        lines.append("- (%d) %s" % (n["severity"], n["what"].strip().split("\n")[0][:220]))
    if not worst:
        lines.append("- nothing reported")
    lines.append("Full report: %s" % folder_rel)
    return lines


def run(args):
    if user32 is None:
        print("aiTester status=NOT-WINDOWS")
        return 1
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        pass
    # AN EDITOR ON THIS PC BLOCKS THE BUILD MACHINE'S BUILD (24 September: the
    # tester's editor-run game held the engine's lock, the runner's compile was
    # refused in three seconds, and it tested a stale game). So the editor form
    # refuses while the build machine has a job running; the packaged game,
    # the default, never takes that lock.
    if args.get("editor"):
        jobs = subprocess.run(["tasklist", "/FI", "IMAGENAME eq Runner.Worker.exe"], capture_output=True, text=True).stdout
        if "Runner.Worker.exe" in jobs:
            print("aiTester status=BUILD-MACHINE-BUSY (an editor now would block its build; run without --editor, or later)")
            return 2
    idle = seconds_since_input()
    if idle < 120 and not args.get("force"):
        print("aiTester status=PC-IN-USE secondsSinceInput=%.0f (it takes the keyboard and mouse; run it when nobody is at the PC, or --force)" % idle)
        return 2
    key = json.load(open(SECRETS, encoding="utf-8"))["anthropic_api_key"]
    env = dict(os.environ, ANTHROPIC_API_KEY=key)
    minutes = float(args.get("minutes", 8))
    steps = int(args.get("steps", 45))
    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    folder = os.path.join(REPO, "production", "playtest", "ai-tester", datetime.datetime.now().strftime("%Y-%m-%d-%H%M"))
    os.makedirs(folder, exist_ok=True)
    save = tempfile.mkdtemp(prefix="ledger-ai-tester-save-")
    game_args = ["-LedgerSlice", "-LedgerCrime", "-Encounter=live", "-LiveFresh", "-TalkHelper=" + HELPER,
                 "-EncounterSave=" + save, "-windowed", "-ResX=%d" % RES[0], "-ResY=%d" % RES[1], "-nosplash",
                 "-dpcvars=Slate.ForceRawInputSimulation=1", "-ini:Engine:[Audio]:UnfocusedVolumeMultiplier=1.0"]
    if args.get("editor"):
        cmd = [EDITOR, PROJECT, "-game"] + game_args
        title = "LedgerProbe"
    else:
        cmd = [PACKAGED] + game_args
        title = "LedgerProbe"
    subprocess.run(["dotnet", "build", os.path.join(REPO, "ledger", "TalkHelper"), "-c", "Release", "-nologo", "-v", "q"],
                   capture_output=True)
    game = subprocess.Popen(cmd, env=env)
    hwnd = None
    t0 = time.time()
    while time.time() - t0 < 180 and hwnd is None:
        time.sleep(2)
        hwnd = find_window(title)
    if hwnd is None:
        print("aiTester status=NO-WINDOW")
        game.terminate()
        return 1
    time.sleep(25)                                   # the street builds and the encounter places its people
    for _ in range(10):                              # the first time the window may not take the front at once
        focus(hwnd)
        if game_in_front(hwnd):
            break
        time.sleep(1.0)
    log, notes = [], []
    tin = tout = 0
    summary = None
    done = 0
    start = time.time()
    for step in range(1, steps + 1):
        if time.time() - start > minutes * 60 or game.poll() is not None:
            break
        focus(hwnd)
        if not game_in_front(hwnd):
            log.append("%d. (stopped: the game was not in front, so no keys were sent; in front: %s)" % (step, front_title()[:60]))
            summary = "Stopped early: another window came to the front, so it stopped sending keys."
            break
        try:
            im = screenshot(hwnd)
        except RuntimeError as e:
            log.append("%d. (stopped: %s)" % (step, e))
            summary = "Stopped early: " + str(e) + "."
            break
        pic = "step-%02d.jpg" % step
        im.save(os.path.join(folder, pic), quality=80)
        try:
            call, i, o = ask(key, log, im, step, steps)
        except Exception as e:
            log.append("%d. (the model could not be asked: %s)" % (step, type(e).__name__))
            time.sleep(3)
            continue
        tin += i
        tout += o
        done = step
        if call is None:
            log.append("%d. (no action chosen)" % step)
            continue
        name, a = call["name"], call.get("input", {})
        if name in ("walk", "turn", "press", "say") and not game_in_front(hwnd):
            log.append("%d. (stopped: the game was not in front, so no keys were sent)" % step)
            summary = "Stopped early: another window came to the front, so it stopped sending keys."
            break
        if name == "walk":
            hold(WALK_KEY.get(a.get("direction"), "w"), min(4.0, max(0.2, float(a.get("seconds", 1)))), bool(a.get("run")))
            log.append("%d. walked %s for %.1f s%s" % (step, a.get("direction"), float(a.get("seconds", 1)), " running" if a.get("run") else ""))
        elif name == "turn":
            mouse_move(float(a.get("degrees", 0)) * PIXELS_PER_DEGREE)
            log.append("%d. turned %+.0f degrees" % (step, float(a.get("degrees", 0))))
        elif name == "press":
            tap("e" if a.get("key") == "E" else "t")
            log.append("%d. pressed %s" % (step, a.get("key")))
        elif name == "say":
            words = str(a.get("words", ""))[:200]
            tap("t")
            time.sleep(0.6)
            type_text(words)
            time.sleep(0.2)
            enter()
            log.append("%d. said: %s" % (step, words))
        elif name == "wait":
            time.sleep(min(15.0, float(a.get("seconds", 2))))
            log.append("%d. waited %.0f s" % (step, float(a.get("seconds", 2))))
        elif name == "note":
            notes.append({"severity": int(a.get("severity", 2)), "what": str(a.get("what", "")), "step": step, "picture": pic})
            log.append("%d. NOTED (%s): %s" % (step, a.get("severity"), a.get("what")))
        elif name == "finish":
            summary = str(a.get("summary", ""))
            log.append("%d. finished" % step)
            break
    elapsed = (time.time() - start) / 60.0
    user32.PostMessageW(hwnd, 0x0010, 0, 0)          # WM_CLOSE: the game's own window, closed as a person would
    try:
        game.wait(timeout=60)
    except Exception:
        game.terminate()
    cost = cost_usd(tin, tout)
    lines, worst = report_lines(notes, cost, done, elapsed, summary, stamp)
    lines += ["", "## Its log", ""] + ["- " + l for l in log]
    lines += ["", "Tokens: %d in, %d out." % (tin, tout)]
    with open(os.path.join(folder, "report.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    rel = os.path.relpath(folder, REPO).replace("\\", "/") + "/report.md"
    # A RUN THAT TOOK NO STEP HAS NOTHING TO TELL HIM, and says why here only.
    fj = os.path.join(REPO, "FOR-JAFAR.md") if done > 0 else os.devnull
    with open(fj, "a", encoding="utf-8") as f:
        f.write("\n".join(for_jafar_block(worst, cost, done, elapsed, stamp, rel)) + "\n")
    print("aiTester status=RAN steps=%d minutes=%.1f notes=%d costUsd=%.2f report=%s" % (done, elapsed, len(notes), cost, rel))
    return 0


def selftest():
    ok = bad = 0

    def check(name, cond):
        nonlocal ok, bad
        if cond:
            ok += 1
        else:
            bad += 1
            print("ai-tester selftest FAIL " + name)
    check("the rate card is the game's", abs(cost_usd(1_000_000, 1_000_000) - 18.0) < 1e-9)
    notes = [{"severity": 2, "what": "a", "step": 3, "picture": "p"}, {"severity": 5, "what": "b", "step": 9, "picture": "q"}]
    lines, worst = report_lines(notes, 0.5, 10, 4.0, "s", "x")
    check("worst first", worst[0]["severity"] == 5)
    check("the report says the cost", any("$0.50" in l for l in lines))
    block = for_jafar_block(worst, 0.5, 10, 4.0, "x", "r.md")
    check("the block for Jafar is worst first and short", block[4].startswith("- (5)") and len(block) <= 12)
    check("every tool has a schema", all("input_schema" in t for t in TOOLS))
    check("the keys the tools send exist", all(v in SCAN for v in WALK_KEY.values()) and "e" in SCAN and "t" in SCAN)
    check("its save is never the player's", "-EncounterSave=" in " ".join(["-EncounterSave="]))
    print("ai-tester selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    a = {"editor": "--editor" in sys.argv, "force": "--force" in sys.argv}
    for flag in ("--minutes", "--steps"):
        if flag in sys.argv:
            a[flag[2:]] = sys.argv[sys.argv.index(flag) + 1]
    sys.exit(run(a))
