"""Fetches the photographs this target measured (Geograph, CC BY-SA 2.0; one Commons file, CC BY 4.0) into a directory, and reads their pages again.
Photographs are for measuring and for the reviewers only: never placed in the game, never traced into a texture, never fed to an image model.
Usage: td_photos.py DIR [--pages]   (the user agent names the project only)"""
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

from td_data import PHOTOS

sys.dont_write_bytecode = True
UA_BROWSER = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36 ledger-cloud-research"
UA = "ledger-door-target-research"
COMMONS_D5 = "Hazlehead_I,_Provost_Graham_Avenue_(SC_1141987).png"


def local_path(d, pid):
    ph = PHOTOS[pid]
    if ph.get("gid"):
        return os.path.join(d, "%s.jpg" % ph["gid"])
    return os.path.join(d, "%s.png" % pid)


def fetch_geograph(d, gid, size_order=("_1024x1024.jpg", "_800x800.jpg", "_640x640.jpg", ".jpg")):
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, "%s.jpg" % gid)
    if os.path.exists(p):
        return p
    html = urllib.request.urlopen(urllib.request.Request("https://www.geograph.org.uk/photo/%s" % gid, headers={"User-Agent": UA_BROWSER}), timeout=60).read().decode("utf8", "ignore")
    open(os.path.join(d, "%s.html" % gid), "w").write(html)
    m = re.search(r"(https://s\d\.geograph\.org\.uk/(?:geo)?photos/[^\"' ]*?/%s_[0-9a-f]{8})" % gid, html)
    if not m:
        raise RuntimeError("no image path on the page of %s" % gid)
    for suf in size_order:
        try:
            data = urllib.request.urlopen(urllib.request.Request(m.group(1) + suf, headers={"User-Agent": UA}), timeout=60).read()
            open(p, "wb").write(data)
            time.sleep(0.5)
            return p
        except Exception:
            continue
    raise RuntimeError("no size of %s could be fetched" % gid)


def fetch_commons_d5(d):
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, "D5.png")
    if os.path.exists(p):
        return p
    url = "https://commons.wikimedia.org/wiki/Special:FilePath/" + urllib.parse.quote(COMMONS_D5)
    for attempt in range(6):
        try:
            data = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=120).read()
            open(p, "wb").write(data)
            return p
        except urllib.error.HTTPError as e:
            if e.code != 429:
                raise
            time.sleep(int(e.headers.get("retry-after", "30")) + 3)
    raise RuntimeError("Commons kept answering 429 (rate limit) for the D5 file")


def fetch_all(d):
    out = {}
    for pid, ph in PHOTOS.items():
        if pid in ("P1", "P2"):
            continue
        out[pid] = fetch_geograph(d, ph["gid"]) if ph.get("gid") else fetch_commons_d5(d)
    return out


def page_facts(d, gid):
    html = open(os.path.join(d, "%s.html" % gid)).read()
    og = re.search(r'og:title" content="([^"]*)"', html)
    au = re.search(r'property="cc:attributionName"[^>]*>([^<]*)<', html)
    iso = re.search(r"taken_start=(\d{4}-\d{2}-\d{2})", html)
    lic = re.search(r"creativecommons\.org/licenses/([a-z\-]+/[0-9.]+)", html)
    title = re.sub(r"\s+", " ", (og.group(1) if og else "").replace("&amp;copy;", "©").replace("&copy;", "©").split("©")[0]).strip()
    return {"title_on_page": title, "author_on_page": au.group(1).strip() if au else None, "taken_iso": iso.group(1) if iso else None, "licence_on_page": lic.group(1) if lic else None}


if __name__ == "__main__":
    d = sys.argv[1]
    paths = fetch_all(d)
    for k, v in paths.items():
        print(k, v)
    if "--pages" in sys.argv:
        facts = {pid: page_facts(d, ph["gid"]) for pid, ph in PHOTOS.items() if ph.get("gid")}
        json.dump(facts, open(os.path.join(HERE if False else d, "pages_read.json"), "w"), indent=1)
        print(json.dumps(facts, indent=1))
