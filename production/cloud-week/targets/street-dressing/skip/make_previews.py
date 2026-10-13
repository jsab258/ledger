"""skip: the preview crop (turned copy, the stencil painted out) and the target-on-photo overlay."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import subprocess
import sd_family as SF
import sd_lib as L
import sd_photo as P


def schedule_1_preview():
    """S8's Schedule 1 (print page 5686 of the made SI 1984/1933, an Open Government Licence statutory page): cropped to the diagram and notes."""
    from PIL import Image
    scr = SF.scratch("skip")
    pdf = os.path.join(scr, "si1984-1933.pdf")
    if not os.path.exists(pdf) or os.path.getsize(pdf) < 5000:
        subprocess.run(["curl", "-sS", "-m", "90", "-A", L.UA_API, "https://www.legislation.gov.uk/uksi/1984/1933/pdfs/uksi_19841933_en.pdf", "-o", pdf], check=True)
    subprocess.run(["pdftoppm", "-r", "130", "-f", "3", "-l", "3", "-png", pdf, os.path.join(scr, "si-p")], check=True)
    png = [f for f in os.listdir(scr) if f.startswith("si-p") and f.endswith(".png")][0]
    im = Image.open(os.path.join(scr, png)).convert("RGB")
    s = im.width / 909.0                      # the 110 dpi look-through's width
    crop = im.crop((int(190 * s), int(120 * s), int(730 * s), int(800 * s)))
    print("s8", P.save_limited(crop, os.path.join(L.PREVIEWS, "skip", "s8-si1984-1933-schedule-1.jpg")))


if __name__ == "__main__":
    SF.previews_main(HERE, "skip", [dict(gid="6875634", key="P1", path="P1rot.jpg", crop=(500, 150, 950, 370), fill=[(610, 218, 860, 305)], name="p1-grass-skip-side-elevation.jpg",
                                         overlay_name="p1-grass-skip-target-on-photo.jpg", photo_id="P1")])
    schedule_1_preview()
