#!/usr/bin/env python3
"""THE AI TESTER, played by Claude Code itself (Jafar, 29 September).

    python tools/ai-tester/play.py start [--editor] [--force] [--wait 60]
    python tools/ai-tester/play.py shot
    python tools/ai-tester/play.py walk forward|back|left|right SECONDS [--run]
    python tools/ai-tester/play.py turn DEGREES          (negative left, positive right)
    python tools/ai-tester/play.py press E|T|Esc|Q
    python tools/ai-tester/play.py say "WORDS"
    python tools/ai-tester/play.py wait SECONDS
    python tools/ai-tester/play.py note SEVERITY "WHAT"   (5 unplayable .. 1 cosmetic)
    python tools/ai-tester/play.py finish "SUMMARY"
    python tools/ai-tester/play.py --selftest

WHY THIS SHAPE, 29 September. Jafar: "nothing in development calls the
Anthropic API directly ... The AI tester: you play the game yourselves,
looking at its screenshots and sending the keys, instead of a script calling
the API per screenshot." He pays for Max and not for API calls on top. Until
then this script asked the conversation model for one action per screenshot
on the game's key. Now the player is the Claude Code session running it: each
command does one action with real key presses and mouse moves sent to the
game window, the way a hand would, then saves a picture of the window and
prints its path, which the session looks at before choosing the next command.
Nothing here calls a model, and no key is read or passed on: the game's own
talk runs as its stand-in (-TalkFake).

WHAT HE ASKED FOR, 24 September: "it plays the packaged slice through the
screen and keyboard as a person would, runs the encounter and wanders freely,
and writes what broke into FOR-JAFAR.md, worst first. It is not a gate." The
playbook `start` prints is what to do.

WHAT IT WRITES: production/playtest/ai-tester/<time>/ with each step's
picture, report.md (every note, worst first, each with the picture it was
looking at, and the log) and for-jafar.md, the short block the day's summary
links. The run's state between commands is in F:/LedgerTools/tmp/ai-tester.

NOT WHILE THE BUILD MACHINE PLAYS, 29 September: its test steps start the game
too; a second game could take the keys meant for this one. `start` waits, up
to --wait minutes (default 60), until the machine runs no game or Unreal of
its own.

IT TAKES THE KEYBOARD AND MOUSE while it runs, so nobody should be using the
PC at the time: `start` refuses when the PC was used in the last two minutes,
unless --force.
"""
import ctypes
import ctypes.wintypes as wt
import datetime
import json
import os
import subprocess
import sys
import tempfile
import time

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PACKAGED = r"F:\LedgerTools\played-game\Windows\LedgerProbe.exe"   # 26 September: moved out of the old copy ledger-migrate
EDITOR = r"C:\Program Files\Epic Games\UE_5.8\Engine\Binaries\Win64\UnrealEditor.exe"
PROJECT = os.path.join(REPO, "ue-probe", "LedgerProbe.uproject")
HELPER = os.path.join(REPO, "ledger", "TalkHelper", "bin", "Release", "net8.0", "TalkHelper.exe")
STATE_DIR = r"F:\LedgerTools\tmp\ai-tester"
STATE = os.path.join(STATE_DIR, "state.json")
RES = (1280, 720)

SCAN = {"w": 0x11, "a": 0x1E, "s": 0x1F, "d": 0x20, "e": 0x12, "t": 0x14, "shift": 0x2A, "esc": 0x01, "q": 0x10}
WALK_KEY = {"forward": "w", "back": "s", "left": "a", "right": "d"}
PIXELS_PER_DEGREE = 5.7                  # a first guess; the player sees the result and corrects

PLAYBOOK = """THE PLAYBOOK (what the tester does, as before):
The game: a street in a British port town, about 1990. You are the man in the grey tracksuit, seen from behind. Walk with W A S D (walk), turn with the mouse (turn), E does the act in front of you. To talk, stand near someone and use say: it presses T, types the words and presses Enter; the talk runs as its stand-in, so judge that the talk works, not what is said. Yellow and white lines are the game telling you things and people speaking.
1. Play the encounter: walk to the shop window by Mickey's (the minicab office with the dark blue front) and press E beside it to break it. Someone will shout. Then go round through the yard behind the parade if you can find it. After a while the game says it is later that week and tells you where Darren is; find him and talk to him; answer him once or twice. Talk to Sheila and Ron too if you find them.
2. Then wander freely: walk the street, look at the buildings and the people, try the edges, try walking into things.
Note anything broken or wrong as soon as you see it (stuck or through the world, a person floating, half in the ground or in an odd pose, flicker, something missing, garbled text, a key ignored, talk that makes no sense), and anything showing or mentioning alcohol, betting or children. Severity: 5 unplayable or crashed, 4 a feature does not work, 3 clearly wrong and noticeable, 2 minor, 1 cosmetic. Not the same thing twice. Walk a second or two at a time, then look. Finish with a two-sentence summary."""

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




def runner_busy():
    """Whether the build machine runs a game or Unreal of its own (its processes live under actions-runner-ledger)."""
    try:
        out = subprocess.run(["powershell", "-NoProfile", "-Command",
                              "@(Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match 'actions-runner-ledger' -and "
                              "($_.Name -like 'LedgerProbe*' -or $_.Name -like 'UnrealEditor*' -or $_.Name -like 'UnrealBuildTool*') }).Count"],
                             capture_output=True, text=True, timeout=60).stdout.strip()
        return int(out or "0") > 0
    except Exception:
        return False


def wait_for_runner(minutes):
    t0 = time.time()
    while runner_busy():
        if time.time() - t0 > minutes * 60:
            return False
        time.sleep(30)
    return True




# ---------------------------------------------------------------- the run's state between commands
def load_state():
    try:
        return json.load(open(STATE, encoding="utf-8"))
    except Exception:
        return None


def save_state(st):
    os.makedirs(STATE_DIR, exist_ok=True)
    tmp = STATE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(st, f, indent=1)
    os.replace(tmp, STATE)


def pid_alive(pid):
    h = ctypes.windll.kernel32.OpenProcess(0x1000, False, int(pid))   # PROCESS_QUERY_LIMITED_INFORMATION
    if not h:
        return False
    code = wt.DWORD()
    ctypes.windll.kernel32.GetExitCodeProcess(h, ctypes.byref(code))
    ctypes.windll.kernel32.CloseHandle(h)
    return code.value == 259                                           # STILL_ACTIVE


def running_state():
    st = load_state()
    if not st or st.get("finished"):
        print("aiTester status=NO-RUN (start one first)")
        return None
    if not pid_alive(st["pid"]) or not user32.IsWindow(st["hwnd"]):
        print("aiTester status=GAME-GONE (the game has closed; finish the run to write its report)")
        return None
    return st


def picture(st, label):
    """Brings the game to the front, saves its picture as the next step and prints the path."""
    hwnd = st["hwnd"]
    focus(hwnd)
    if not game_in_front(hwnd):
        print("aiTester status=NOT-IN-FRONT front=%s" % front_title()[:60])
        return None
    try:
        im = screenshot(hwnd)
    except RuntimeError as e:
        print("aiTester status=NO-PICTURE (%s)" % e)
        return None
    st["step"] += 1
    pic = "step-%03d.jpg" % st["step"]
    im.save(os.path.join(REPO, st["folder"], pic), quality=80)
    st["picture"] = pic
    st["log"].append("%d. %s" % (st["step"], label))
    save_state(st)
    print("aiTester step=%d did=%s picture=%s" % (st["step"], label, os.path.join(REPO, st["folder"], pic)))
    return pic


# ---------------------------------------------------------------- the commands
def start(args):
    if user32 is None:
        print("aiTester status=NOT-WINDOWS")
        return 1
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        pass
    st = load_state()
    if st and not st.get("finished") and pid_alive(st["pid"]):
        print("aiTester status=ALREADY-RUNNING folder=%s (finish it first)" % st["folder"])
        return 2
    # AN EDITOR ON THIS PC BLOCKS THE BUILD MACHINE'S BUILD (24 September), so
    # the editor form refuses while the build machine has a job running; the
    # packaged game, the default, never takes that lock.
    if args.get("editor"):
        jobs = subprocess.run(["tasklist", "/FI", "IMAGENAME eq Runner.Worker.exe"], capture_output=True, text=True).stdout
        if "Runner.Worker.exe" in jobs:
            print("aiTester status=BUILD-MACHINE-BUSY (an editor now would block its build; run without --editor, or later)")
            return 2
    idle = seconds_since_input()
    if idle < 120 and not args.get("force"):
        print("aiTester status=PC-IN-USE secondsSinceInput=%.0f (it takes the keyboard and mouse; run it when nobody is at the PC, or --force)" % idle)
        return 2
    # NO KEY, EVER (29 September): the game's talk runs as its stand-in, and
    # the game's environment carries no key it could pass on.
    env = dict(os.environ)
    env.pop("ANTHROPIC_API_KEY", None)
    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    folder = os.path.join("production", "playtest", "ai-tester", datetime.datetime.now().strftime("%Y-%m-%d-%H%M"))
    os.makedirs(os.path.join(REPO, folder), exist_ok=True)
    save = tempfile.mkdtemp(prefix="ledger-ai-tester-save-")
    # THE PACKAGED GAME AS A PLAYER GETS IT (24 September, Jafar's rule: the
    # tester walks the packaged release build with the real cast, dialogue,
    # light and sound). A package that carries its own run-time files is run
    # ALONE, so a missing file shows as a fault here; an older one gets the
    # old props, and the report says which.
    pack_root = os.path.join(os.path.dirname(PACKAGED), "LedgerProbe")
    self_contained = (not args.get("editor")) and os.path.isfile(os.path.join(
        pack_root, "Content", "LedgerData", "production", "assets", "street", "quay-street.json"))
    shipping = os.path.isfile(os.path.join(pack_root, "Binaries", "Win64", "LedgerProbe-Win64-Shipping.exe"))
    game_args = ["-LedgerSlice", "-LedgerCrime", "-Encounter=live", "-LiveFresh", "-TalkHelper=" + HELPER, "-TalkFake",
                 "-EncounterSave=" + save, "-windowed", "-ResX=%d" % RES[0], "-ResY=%d" % RES[1], "-nosplash",
                 "-dpcvars=Slate.ForceRawInputSimulation=1", "-ini:Engine:[Audio]:UnfocusedVolumeMultiplier=1.0"]
    if not self_contained:
        game_args.append("-LedgerRepo=" + REPO)
        import shutil
        stage = pack_root if not args.get("editor") else os.path.join(REPO, "ue-probe")
        if os.path.isdir(stage):
            shutil.copyfile(os.path.join(REPO, "production", "specs", "vignette-pieces.json"), os.path.join(stage, "vignette-pieces.json"))
            shutil.copyfile(os.path.join(REPO, "content", "dialogue", "crime-witness-v1.json"), os.path.join(stage, "crime-witness-v1.json"))
    game_args += [x for x in args.get("extra", []) if x.startswith("-") and " " not in x]
    build = "editor" if args.get("editor") else "packaged"
    print("aiTester build=%s selfContained=%s config=%s" % (build, "yes" if self_contained else "no", "Shipping" if shipping else "Development"))
    cmd = ([EDITOR, PROJECT, "-game"] if args.get("editor") else [PACKAGED]) + game_args
    subprocess.run(["dotnet", "build", os.path.join(REPO, "ledger", "TalkHelper"), "-c", "Release", "-nologo", "-v", "q"],
                   capture_output=True)
    if not wait_for_runner(float(args.get("wait", 60))):
        print("aiTester status=RUNNER-BUSY: the build machine's game or Unreal was still running")
        return 1
    game = subprocess.Popen(cmd, env=env)
    hwnd = None
    t0 = time.time()
    while time.time() - t0 < 180 and hwnd is None:
        time.sleep(2)
        hwnd = find_window("LedgerProbe")
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
    st = {"pid": game.pid, "hwnd": int(hwnd), "folder": folder.replace("\\", "/"), "stamp": stamp, "started": time.time(),
          "build": build, "selfContained": self_contained, "step": 0, "log": [], "notes": [], "picture": None, "finished": False}
    save_state(st)
    print(PLAYBOOK)
    picture(st, "started")
    return 0


def act(verb, rest):
    st = running_state()
    if st is None:
        return 1
    hwnd = st["hwnd"]
    focus(hwnd)
    if not game_in_front(hwnd):
        print("aiTester status=NOT-IN-FRONT (no keys sent) front=%s" % front_title()[:60])
        return 1
    if verb == "walk":
        direction = rest[0] if rest else "forward"
        seconds = min(4.0, max(0.2, float(rest[1]) if len(rest) > 1 else 1.0))
        running = "--run" in rest
        hold(WALK_KEY.get(direction, "w"), seconds, running)
        label = "walked %s for %.1f s%s" % (direction, seconds, " running" if running else "")
    elif verb == "turn":
        degrees = max(-180.0, min(180.0, float(rest[0]) if rest else 0.0))
        mouse_move(degrees * PIXELS_PER_DEGREE)
        label = "turned %+.0f degrees" % degrees
    elif verb == "press":
        k = (rest[0] if rest else "E").upper()
        # ESC AND Q, 29 September: the pause (Esc) and quitting from it (Q).
        tap({"E": "e", "T": "t", "ESC": "esc", "Q": "q"}.get(k, "t"))
        label = "pressed %s" % k
    elif verb == "say":
        words = " ".join(rest)[:200]
        tap("t")
        time.sleep(0.6)
        type_text(words)
        time.sleep(0.2)
        enter()
        label = "said: %s" % words
    elif verb == "wait":
        seconds = min(15.0, max(0.5, float(rest[0]) if rest else 2.0))
        time.sleep(seconds)
        label = "waited %.0f s" % seconds
    else:
        print("aiTester status=UNKNOWN-COMMAND %s" % verb)
        return 2
    time.sleep(0.4)                                  # the frame after the action
    return 0 if picture(st, label) else 1


def note(rest):
    st = load_state()
    if not st or st.get("finished"):
        print("aiTester status=NO-RUN")
        return 1
    severity = max(1, min(5, int(rest[0]))) if rest else 2
    what = " ".join(rest[1:]).strip()
    st["notes"].append({"severity": severity, "what": what, "step": st["step"], "picture": st.get("picture") or "none"})
    st["log"].append("%d. NOTED (%d): %s" % (st["step"], severity, what))
    save_state(st)
    print("aiTester noted severity=%d at step %d" % (severity, st["step"]))
    return 0


def report_lines(notes, steps, minutes, summary, stamp, build):
    worst = sorted(notes, key=lambda n: -n["severity"])
    out = ["# AI tester, %s" % stamp, "",
           "%d steps in %.1f minutes, the %s game, played by Claude Code on Jafar's subscription: no API calls." % (steps, minutes, build), "",
           "Its summary: " + (summary or "none; it did not finish by itself."), "", "## What broke, worst first", ""]
    if not worst:
        out.append("Nothing reported.")
    for n in worst:
        out.append("- **%d** %s (step %d, %s)" % (n["severity"], n["what"].strip(), n["step"], n["picture"]))
    return out, worst


def for_jafar_block(worst, steps, minutes, stamp, folder_rel):
    lines = ["", "### AI tester, %s" % stamp, "",
             "%d steps, %.0f minutes, played by Claude Code (no API cost). Not a gate. Worst first:" % (steps, minutes)]
    for n in worst[:6]:
        lines.append("- (%d) %s" % (n["severity"], n["what"].strip().split("\n")[0][:220]))
    if not worst:
        lines.append("- nothing reported")
    lines.append("Full report: %s" % folder_rel)
    return lines


def finish(rest):
    st = load_state()
    if not st or st.get("finished"):
        print("aiTester status=NO-RUN")
        return 1
    summary = " ".join(rest).strip() or None
    if pid_alive(st["pid"]) and user32.IsWindow(st["hwnd"]):
        user32.PostMessageW(st["hwnd"], 0x0010, 0, 0)   # WM_CLOSE: the game's own window, closed as a person would
        t0 = time.time()
        while pid_alive(st["pid"]) and time.time() - t0 < 60:
            time.sleep(1)
        if pid_alive(st["pid"]):
            subprocess.run(["taskkill", "/PID", str(st["pid"]), "/F"], capture_output=True)
    minutes = (time.time() - st["started"]) / 60.0
    lines, worst = report_lines(st["notes"], st["step"], minutes, summary, st["stamp"], st["build"])
    lines += ["", "## Its log", ""] + ["- " + l for l in st["log"]]
    folder = os.path.join(REPO, st["folder"])
    with open(os.path.join(folder, "report.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    rel = st["folder"] + "/report.md"
    with open(os.path.join(folder, "for-jafar.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(for_jafar_block(worst, st["step"], minutes, st["stamp"], rel)) + "\n")
    st["finished"] = True
    save_state(st)
    print("aiTester status=RAN steps=%d minutes=%.1f notes=%d report=%s" % (st["step"], minutes, len(st["notes"]), rel))
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
    notes = [{"severity": 2, "what": "a", "step": 3, "picture": "p"}, {"severity": 5, "what": "b", "step": 9, "picture": "q"}]
    lines, worst = report_lines(notes, 10, 4.0, "s", "x", "packaged")
    check("worst first", worst[0]["severity"] == 5)
    check("the report says no API calls", any("no API calls" in l for l in lines))
    block = for_jafar_block(worst, 10, 4.0, "x", "r.md")
    check("the block for Jafar is worst first and short", block[4].startswith("- (5)") and len(block) <= 12)
    check("the keys the commands send exist", all(v in SCAN for v in WALK_KEY.values()) and "e" in SCAN and "t" in SCAN)
    src = open(os.path.abspath(__file__), encoding="utf-8").read()
    check("nothing here calls the API or reads a key",
          ("api." + "anthropic.com") not in src and ("anthropic" + "_api_key") not in src and ("x-" + "api-key") not in src)
    check("the game's talk is the stand-in", '"-TalkFake"' in src)
    check("its save is never the player's", '"-EncounterSave=" + save' in src)
    print("ai-tester selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    argv = sys.argv[1:]
    if "--selftest" in argv:
        sys.exit(selftest())
    verb = argv[0] if argv else ""
    rest = argv[1:]
    if verb == "start":
        a = {"editor": "--editor" in rest, "force": "--force" in rest}
        if "--wait" in rest:
            a["wait"] = rest[rest.index("--wait") + 1]
        # --game-arg X, repeatable: one more argument for the game, such as a
        # trial exposure (-PlayNightPin=2.0) while the evening is tuned in play.
        a["extra"] = [rest[k + 1] for k, x in enumerate(rest) if x == "--game-arg" and k + 1 < len(rest)]
        sys.exit(start(a))
    if verb == "shot":
        s = running_state()
        sys.exit(0 if s and picture(s, "looked") else 1)
    if verb in ("walk", "turn", "press", "say", "wait"):
        sys.exit(act(verb, rest))
    if verb == "note":
        sys.exit(note(rest))
    if verb == "finish":
        sys.exit(finish(rest))
    print(__doc__)
    sys.exit(2)
