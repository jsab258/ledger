"""Records the RDR2 window Jafar already has open, for his drill (advisor 361, 24 Nov 2026).

Never starts the game, never sends a key or click, never reads or writes the game's files.
Run in the background when he types 'RDR2 drill starting':
    python tools/drills/rdr2_record.py start
and stop it when he types 'RDR2 drill done':
    python tools/drills/rdr2_record.py stop
Frames: 5 a second, half size, JPEG, kept in memory with their high-resolution clock time and
written to F:/LedgerTools/game-inputs/footage/rdr2-drill-<stamp>/ every 60 s and at the end, with
frames.jsonl (file, seconds since start, wall time). A frame is taken only while the game's own
window covers its area (centre and four corners belong to its process), so no other app or chat
can be in a picture; skipped frames are counted. The window is found by its title.
"""
import ctypes, ctypes.wintypes as wt, io, json, os, sys, threading, time
from datetime import datetime

ROOT = "F:/LedgerTools/game-inputs/footage"
STOP = os.path.join(ROOT, "rdr2-drill.stop")
TITLE = "Red Dead Redemption 2"
FPS, SCALE, QUALITY = 5, 0.5, 80
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()


def find_window():
    found = []
    @ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
    def cb(h, _):
        n = user32.GetWindowTextLengthW(h)
        if n and user32.IsWindowVisible(h):
            b = ctypes.create_unicode_buffer(n + 1)
            user32.GetWindowTextW(h, b, n + 1)
            if b.value.startswith(TITLE):
                found.append(h)
        return True
    user32.EnumWindows(cb, 0)
    return found[0] if found else None


def client_box(h):
    r = wt.RECT(); user32.GetClientRect(h, ctypes.byref(r))
    p = wt.POINT(0, 0); user32.ClientToScreen(h, ctypes.byref(p))
    return (p.x, p.y, p.x + r.right, p.y + r.bottom)


def pid_of(h):
    p = wt.DWORD(); user32.GetWindowThreadProcessId(h, ctypes.byref(p)); return p.value


def on_top(h, box):
    want = pid_of(h); x0, y0, x1, y1 = box
    for x, y in [((x0 + x1) // 2, (y0 + y1) // 2), (x0 + 4, y0 + 4), (x1 - 5, y0 + 4), (x0 + 4, y1 - 5), (x1 - 5, y1 - 5)]:
        w = user32.WindowFromPoint(wt.POINT(x, y))
        if not w or pid_of(user32.GetAncestor(w, 2)) != want:
            return False
    return True


def record():
    from PIL import ImageGrab
    h = find_window()
    if not h:
        print("rdr2_record: no window titled", TITLE, "- nothing recorded"); return 2
    if os.path.exists(STOP):
        os.remove(STOP)
    out = os.path.join(ROOT, "rdr2-drill-" + datetime.now().strftime("%Y%m%d-%H%M"))
    os.makedirs(out, exist_ok=True)
    pending, lock, kept, skipped = [], threading.Lock(), 0, 0
    t0 = time.perf_counter()

    def flush():
        with lock:
            batch = pending[:]; pending.clear()
        with open(os.path.join(out, "frames.jsonl"), "a", encoding="utf-8") as idx:
            for name, data, t, wall in batch:
                open(os.path.join(out, name), "wb").write(data)
                idx.write(json.dumps({"file": name, "t": round(t, 3), "wall": wall}) + "\n")

    last_flush, n = time.perf_counter(), 0
    while not os.path.exists(STOP):
        tick = time.perf_counter()
        if not user32.IsWindow(h):
            print("rdr2_record: the window closed"); break
        box = client_box(h)
        if box[2] > box[0] and on_top(h, box):
            im = ImageGrab.grab(bbox=box, all_screens=True).convert("RGB")
            im = im.resize((int(im.width * SCALE), int(im.height * SCALE)))
            b = io.BytesIO(); im.save(b, "JPEG", quality=QUALITY)
            with lock:
                pending.append((f"{n:06d}.jpg", b.getvalue(), tick - t0, datetime.now().isoformat(timespec="milliseconds")))
            n += 1; kept += 1
        else:
            skipped += 1
        if tick - last_flush > 60:
            threading.Thread(target=flush).start(); last_flush = tick
        time.sleep(max(0, 1 / FPS - (time.perf_counter() - tick)))
    flush()
    if os.path.exists(STOP):
        os.remove(STOP)
    print(f"rdr2_record: kept={kept} skipped_not_on_top={skipped} seconds={time.perf_counter() - t0:.0f} out={out}")
    return 0


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "start":
        sys.exit(record())
    elif cmd == "stop":
        open(STOP, "w").close(); print("rdr2_record: stop asked")
    else:
        print(__doc__)
