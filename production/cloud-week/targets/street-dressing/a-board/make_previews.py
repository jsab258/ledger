"""a-board: the preview crops (P1 turned, its lettering blurred beyond reading; P2 enlarged 4 times with the card's print blurred) and the target-on-photo overlay."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import sd_family as SF
import sd_lib as L
from PIL import Image

if __name__ == "__main__":
    scr = SF.scratch("a-board")
    pg, path = L.sampled_photo("6913397", "P2", scr)
    im = Image.open(path).convert("RGB")
    im.resize((im.width * 4, im.height * 4), Image.BICUBIC).save(os.path.join(scr, "P2x4.jpg"), quality=95)
    SF.previews_main(HERE, "a-board", [
        dict(gid="3671864", key="P1", path="P1rot.jpg", crop=(40, 20, 480, 640), blur=[(76, 48, 432, 595)], radius=16, name="p1-village-board-front-leaf.jpg",
             overlay_name="p1-village-board-target-on-photo.jpg", photo_id="P1"),
        dict(gid="6913397", key="P2", path="P2x4.jpg", crop=(440 * 4, 436 * 4, 600 * 4, 590 * 4), blur=[(492 * 4, 474 * 4, 552 * 4, 556 * 4)], radius=20, name="p2-1978-notice-board.jpg"),
    ])
