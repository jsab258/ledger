#!/usr/bin/env python3
"""Fetch the CC0 sources for Quay Street's sound (unit 10, cloud week 42) and record where each came from.

    python fetch_sources.py             # fetch what is missing, check each page's licence, write sources.json
    python fetch_sources.py --verify    # no network: check the files on disk against the md5 sums in sources.json

sources.json lists every source with the fields that decide its use (id, host, page, what it is used for). This
script reads each source's own page and refuses the source unless the page states CC0, then fills in what the
page says (author, title, licence exactly as printed, date uploaded, the original's format and length, the
description), the download address, the file's md5 and size, and the date it was read.

Where the files go: SOUND_SOURCES (default /home/user/ledger-scratch/sound-sources), outside the repository.

  - Freesound: the sound page, read without signing in. The original WAV needs a free login, so the file is the
    page's public high-quality preview (the page's `data-mp3` address with -lq changed to -hq: about 190 kbps
    MP3 at the original's rate, 44.1 or 48 kHz). The 30 September footsteps research took the same route.
  - BigSoundBank: the sound page's own download list; the FLAC where the page offers one, else the BWF (WAV),
    both lossless, no account.

Freesound's CDN answers 403 when several downloads run at once, so downloads here go one at a time, with a
pause between and a growing wait on a refusal.
"""
import datetime
import hashlib
import html
import json
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCES_JSON = os.path.join(HERE, "sources.json")
DEST = os.environ.get("SOUND_SOURCES", "/home/user/ledger-scratch/sound-sources")
UA = "Mozilla/5.0 (LedgerSoundFetch; CC0 sources only)"
CC0_URL = "creativecommons.org/publicdomain/zero/1.0"


def curl(url, out=None, tries=6, pause=3.0):
    """GET url; returns the body text (out=None) or the saved path. Retries 403, 429 and 5xx with a growing wait."""
    for k in range(tries):
        cmd = ["curl", "-sS", "-L", "-m", "300", "-A", UA, "-w", "\n%{http_code}", url]
        if out:
            cmd = ["curl", "-sS", "-L", "-m", "300", "-A", UA, "-o", out, "-w", "%{http_code}", url]
        r = subprocess.run(cmd, capture_output=True)
        txt = r.stdout.decode("utf8", "replace")
        if out:
            code, body = txt.strip(), None
        else:
            body, _, code = txt.rpartition("\n")
        if code == "200":
            return out if out else body
        if out and os.path.exists(out):
            os.remove(out)
        if code in ("404", "410"):
            raise SystemExit("fetch_sources: %s is %s" % (url, code))
        time.sleep(pause * (2 ** k))
    raise SystemExit("fetch_sources: gave up on %s (last status %s)" % (url, code))


def plain(h):
    h = re.sub(r"<script.*?</script>|<style.*?</style>", "", h, flags=re.S)
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h)))


def md5(path):
    m = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            m.update(chunk)
    return m.hexdigest()


def read_freesound(src):
    for k in range(5):
        h = curl(src["page_url"])
        if "data-mp3=" in h and "<title>Freesound - " in h:
            break
        time.sleep(5 * (k + 1))  # a throttled answer is a 200 page without the sound on it
    else:
        raise SystemExit("fetch_sources: %s: the page never showed the sound; not used" % src["id"])
    t = plain(h)
    title_by = re.search(r"<title>Freesound - (.*?)</title>", h, re.S)
    title_by = html.unescape(title_by.group(1)).strip()
    author = title_by.rsplit(" by ", 1)[1].strip()  # the page's own title line: "Freesound - TITLE by AUTHOR"
    title = html.unescape(re.search(r'data-title="([^"]*)"', h).group(1))
    lic = re.search(r'title="Go to the full license text" href="([^"]+)"[^>]*>([^<]+)</a>', h)
    if not lic:
        raise SystemExit("fetch_sources: %s: no licence on the page; not used" % src["id"])
    lic_url, lic_text = lic.group(1), html.unescape(lic.group(2)).strip()
    if lic_text != "Creative Commons 0" or CC0_URL not in lic_url:
        raise SystemExit("fetch_sources: %s: the page says %r (%s), not CC0; not used" % (src["id"], lic_text, lic_url))
    mp3 = re.search(r'data-mp3="([^"]+)"', h).group(1)
    # the date follows the author's name, usually "AUTHOR July 4th, 2024 Follow"; the first build's pattern needed " Follow" straight
    # after it and missed one page (fs_744592), so take the first date within 60 characters of the name
    date = re.search(re.escape(author) + r"\W{0,3}.{0,60}?([A-Z][a-z]+ \d+(?:st|nd|rd|th), \d{4})", t)
    if not date:
        print("fetch_sources: %s: the page gives no upload date after the author's name; uploaded is left empty (check_sound.py fails a Freesound source without one)" % src["id"])
    follow = t.find(" Follow ")
    info = {}
    for key, pat in (("original_duration", r"Duration (\d+:\d+(?:\.\d+)?)"), ("original_sample_rate", r"Sample rate ([\d.]+ kHz)"),
                     ("original_bit_depth", r"Bit depth (\d+ bit)"), ("original_channels", r"Channels (Stereo|Mono)")):
        m = re.search(pat, t)
        info[key] = m.group(1) if m else None
    desc = t[follow + 8:t.find("Sound illegal or offensive?")].strip() if follow > 0 else ""
    return dict(
        title=title, author=author, page_title=title_by, licence=lic_text, licence_url=lic_url,
        uploaded=date.group(1) if date else None, description_on_page=desc[:600], **info,
        download_url=mp3.replace("-lq.", "-hq."), download_kind="Freesound high-quality preview (MP3, about 190 kbps)",
        file="fs_%d.mp3" % src["freesound_id"])


def read_bsb(src):
    h = curl(src["page_url"])
    t = plain(h)
    if "License CC0 (public domain)" not in t:
        raise SystemExit("fetch_sources: %s: the page does not say CC0 (public domain); not used" % src["id"])
    title = re.search(r"<h1[^>]*>(.*?)</h1>", h, re.S)
    title = html.unescape(re.sub(r"<[^>]+>", "", title.group(1))).strip() if title else None
    tech = t[t.find("Technical details"):t.find("FAQ about this sound")]
    g = lambda pat: (re.search(pat, tech).group(1).strip() if re.search(pat, tech) else None)
    opts = re.findall(r"<option value='([^']*)'", h)
    n = "%04d" % src["bsb_number"]
    kind = "flac" if "flac" in opts else "bwf"
    ext = "flac" if kind == "flac" else "wav"
    return dict(
        title=title, author=g(r"Author : (.*?) Sound number"), page_title=None, licence="CC0 (public domain)",
        licence_url="https://creativecommons.org/publicdomain/zero/1.0/",
        uploaded=None, description_on_page=(re.search(r"Donations or merchandise purchases are appreciated\. (.*?) Listen", t).group(1)[:600]
                                            if re.search(r"Donations or merchandise purchases are appreciated\. (.*?) Listen", t) else None),
        original_duration=g(r"Length : (\S+)"),
        original_sample_rate=g(r"Sampling Rate : ([\d,]+ Hz)"), original_bit_depth=g(r"Bit Depth : (\d+ bits)"),
        original_channels=g(r"Channels : (\w+)"),
        download_url="https://bigsoundbank.com/UPLOAD/%s/%s.%s" % (kind, n, ext),
        download_kind="BigSoundBank %s, lossless" % ("FLAC" if kind == "flac" else "BWF WAV"),
        file="bsb_%d.%s" % (src["bsb_number"], ext))


def fetch_all():
    os.makedirs(DEST, exist_ok=True)
    with open(SOURCES_JSON, encoding="utf8") as f:
        data = json.load(f)
    today = datetime.date.today().isoformat()
    for src in data["sources"]:
        have = src.get("file") and os.path.exists(os.path.join(DEST, src["file"])) and src.get("md5") == md5(os.path.join(DEST, src["file"]))
        if have:
            print("have   %s" % src["id"])
            continue
        meta = read_freesound(src) if src["host"] == "freesound" else read_bsb(src)
        src.update(meta)
        path = os.path.join(DEST, src["file"])
        time.sleep(1.5)
        curl(src["download_url"], out=path)
        src["md5"] = md5(path)
        src["bytes"] = os.path.getsize(path)
        src["date_read"] = today
        print("fetched %s  %s  %d bytes  %s" % (src["id"], src["licence"], src["bytes"], src["md5"]))
        with open(SOURCES_JSON, "w", encoding="utf8") as f:
            json.dump(data, f, indent=1, ensure_ascii=False)
            f.write("\n")
        time.sleep(2.0)
    return data


def verify():
    with open(SOURCES_JSON, encoding="utf8") as f:
        data = json.load(f)
    bad = 0
    for src in data["sources"]:
        path = os.path.join(DEST, src.get("file", "?"))
        if not os.path.exists(path):
            print("MISSING %s" % src["id"])
            bad += 1
        elif md5(path) != src.get("md5"):
            print("CHANGED %s (md5 differs from sources.json)" % src["id"])
            bad += 1
    print("%d of %d sources present and unchanged" % (len(data["sources"]) - bad, len(data["sources"])))
    return 1 if bad else 0


if __name__ == "__main__":
    if "--verify" in sys.argv:
        sys.exit(verify())
    fetch_all()
    sys.exit(verify())
