"""The photographs this target measured (Geograph, CC BY-SA 2.0), their crops and masks, and how to fetch them again.
Photographs are for measuring and for the reviewers only: never placed in the game, never traced into a texture, never fed to an image model.
Every crop below drops people and real firms' names by cropping; what a crop would still show is masked flat grey (GREY) and read back from
the written JPEG by self_check.py."""
import json
import os
import re
import sys
import time
import urllib.request

sys.dont_write_bytecode = True
UA = "ledger-cloud-research (production reference measuring)"
GREY = (120, 120, 120)

# id: geograph id, author, title as on the page, taken (as on the page), licence read on the page, local file stem, what it shows
PHOTOS = {
    "P1": {"gid": "3380884", "author": "Bernard Sharp", "title": "John Street, Kingston upon Hull", "taken": "5 March 1985", "place": "hull-john-street",
           "shows": "a port town's 1850s terrace seen along the street at 10 to 35 degrees: white-painted 1/1 and 2/2 sashes and dark-brown ones, white voile nets in the lower sash, stone-painted sills and heads",
           "period": "the period itself (1985)",
           "crop": (330, 370, 700, 545), "scale": 3.0, "masks": []},
    "P2": {"gid": "3462979", "author": "Bernard Sharp", "title": "Durham Street, Kingston upon Hull", "taken": "17 August 1986", "place": "hull-durham-street",
           "shows": "a brick terrace with each house's frames painted its own colour (white, blue, olive, cream render), lower-sash voile nets with the upper sash clear, a louvre blind in one ground window",
           "period": "the period itself (1986)",
           "crop": (0, 240, 1000, 440), "scale": 1.15, "masks": [{"what": "street-name sign", "shape": "rect", "box": [735, 322, 775, 345]}]},
    "P3": {"gid": "2738668", "author": "Chris Andrews", "title": "Penchwintan Terrace, Bangor", "taken": "29 May 1988", "place": "bangor-penchwintan-terrace",
           "shows": "a stone terrace with 2/2 and 1/1 sashes in white, cream and red-brown, lace and voile nets, a bare ground window with a dark room, seen from 30 degrees to square on",
           "period": "the period itself (1988)",
           "crop": (440, 265, 1024, 535), "scale": 2.0, "masks": []},
    "P4": {"gid": "566077", "author": "Dr Neil Clifton", "title": "Oswald Street, Rochdale, Lancashire", "taken": "15 September 1979", "place": "rochdale-oswald-street",
           "shows": "black-and-white: a brick terrace's sashes seen at 20 to 40 degrees: full white nets, a half net, a bare ground window with the room black and a pot plant",
           "period": "the period itself (1979)",
           "crop": (380, 60, 640, 480), "scale": 3.0, "masks": []},
    "P5": {"gid": "566265", "author": "Dr Neil Clifton", "title": "Tanfield Road, Croydon - North side", "taken": "14 October 1979", "place": "croydon-tanfield-road",
           "shows": "black-and-white: a Victorian terrace's bay and upper sashes at 15 to 40 degrees, white nets, dark glass",
           "period": "the period itself (1979)",
           "crop": (270, 110, 640, 390), "scale": 2.6, "masks": []},
    "P6": {"gid": "2321423", "author": "Anthony Parkes", "title": "Terraced House - Ratcliffe Street, Levenshulme", "taken": "10 June 1994", "place": "levenshulme-ratcliffe-street",
           "shows": "a terrace front square on: a replacement upper window (white, a top light across and two lower lights, the transom at 0.66 of the height), a ground bay with a full net and a side light with lace",
           "period": "the period itself (1994); the upper window is a replacement",
           "crop": (270, 60, 658, 575), "scale": 1.6, "masks": []},
    "P7": {"gid": "689253", "author": "Dr Neil Clifton", "title": "Nos. 34, 32 and 30, Frederick Street, Barnoldswick", "taken": "10 April 1990", "place": "barnoldswick-frederick-street",
           "shows": "black-and-white: stone terrace 'mostly modernised with double glazing' (the page): white replacement frames with a top light, half-height and full nets",
           "period": "the period itself (1990)",
           "crop": (195, 195, 640, 440), "scale": 2.4, "masks": [{"what": "street-name plate", "shape": "rect", "box": [198, 262, 230, 274]},
                                                  {"what": "small plate on the dark door (a house number's place)", "shape": "rect", "box": [389, 400, 407, 413]}]},
    "P8": {"gid": "3499732", "author": "Christopher Hilton", "title": "Back of terraced houses, Sunningwell Road, Oxford, 1987", "taken": "30 June 1987", "place": "oxford-sunningwell-road-rear",
           "shows": "the back of a Victorian terrace seen nearly square on from below: two 2/2 sashes, white frames, the panes dark blue-grey (sky over a dark room), a net at the right of one",
           "period": "the period itself (1987); the sashes are original (the page: Victorian)",
           "crop": (280, 270, 680, 470), "scale": 3.0, "masks": []},
    "P9": {"gid": "3466378", "author": "Christopher Hilton", "title": "Boundary Street Estate, 1989", "taken": "4 June 1989", "place": "shoreditch-boundary-street",
           "shows": "tall arched sashes of a brick estate at 25 to 40 degrees, sunlit and shaded faces: panes pale, frames white, the bars as dark lines",
           "period": "the period itself (1989)",
           "crop": (280, 30, 560, 430), "scale": 2.5, "masks": []},
    "P10": {"gid": "361082", "author": "Tom Jolliffe", "title": "Copenhagen Street, Islington", "taken": "October 1983", "place": "islington-copenhagen-street",
            "shows": "a Georgian terrace: 6/6 sashes seen at 20 to 35 degrees with pale blue panes, boarded windows beside them",
            "period": "the period itself (1983)",
            "crop": (0, 0, 640, 442), "scale": 1.8, "masks": []},
    "P11": {"gid": "2876894", "author": "Kevin Hall", "title": "Newburn Council Houses", "taken": "1 August 1989", "place": "newburn-council-houses",
            "shows": "1960s council houses in 1989: white casement windows, a fixed light and a top-hung light, net and vertical drapes; the council replacement kind",
            "period": "the period itself (1989)",
            "crop": (0, 370, 700, 690), "scale": 1.6, "masks": []},
    "P12": {"gid": "2238747", "author": "P L Chadwick", "title": "Terraced housing in Railway Street", "taken": "9 August 1987", "place": "railway-street-terrace",
            "shows": "a stone terrace with white and olive-green sashes, lower-sash voile nets, an open curtain, leaded top lights",
            "period": "the period itself (1987)",
            "crop": (80, 100, 800, 400), "scale": 1.6,
            "masks": [{"what": "street-name plate", "shape": "rect", "box": [220, 283, 268, 294]}, {"what": "notice board on a post", "shape": "rect", "box": [424, 262, 484, 332]},
                       {"what": "oval plate on the white door (a house number's place)", "shape": "rect", "box": [765, 297, 792, 318]}]},
    "P13": {"gid": "3379651", "author": "Bernard Sharp", "title": "Prince Street, Kingston upon Hull", "taken": "25 July 1982", "place": "hull-prince-street",
            "shows": "a narrow street: the windows of the right-hand wall seen at under 10 degrees read as a white slit beside a dark void (the 1a finding), boarded and blank windows opposite",
            "period": "the period itself (1982)",
            "crop": (600, 0, 766, 620), "scale": 1.5, "masks": []},
    "P14": {"gid": "674344", "author": "Dr Neil Clifton", "title": "Derelict council houses, Milan Avenue, Burnley, Lancashire", "taken": "29 July 1988", "place": "burnley-milan-avenue",
            "shows": "empty houses of 1988: windows boarded with plywood, broken lights, no nets",
            "period": "the period itself (1988)",
            "crop": (330, 100, 640, 360), "scale": 2.2, "masks": []},
}


def local_path(photo_dir, pid):
    return os.path.join(photo_dir, "%s.jpg" % PHOTOS[pid]["gid"])


def fetch(photo_dir, pid, size_order=("_1024x1024.jpg", "_800x800.jpg", "_640x640.jpg", ".jpg")):
    """Fetch one photograph by Geograph id: the photo page (a browser user agent) names the file; the largest size that exists is taken."""
    os.makedirs(photo_dir, exist_ok=True)
    p = local_path(photo_dir, pid)
    if os.path.exists(p):
        return p
    gid = PHOTOS[pid]["gid"]
    ua = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36 ledger-cloud-research"
    html = urllib.request.urlopen(urllib.request.Request("https://www.geograph.org.uk/photo/%s" % gid, headers={"User-Agent": ua}), timeout=60).read().decode("utf8", "ignore")
    m = re.search(r"(https://s\d\.geograph\.org\.uk/(?:geo)?photos/[^\"' ]*?/%s_[0-9a-f]{8})" % gid, html)
    if not m:
        raise RuntimeError("photograph %s: no image path on its page" % gid)
    base = m.group(1)
    for suf in size_order:
        try:
            data = urllib.request.urlopen(urllib.request.Request(base + suf, headers={"User-Agent": UA}), timeout=60).read()
            open(p, "wb").write(data)
            time.sleep(0.5)
            return p
        except Exception:
            continue
    raise RuntimeError("no size of %s could be fetched" % gid)
