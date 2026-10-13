"""skip: the preview crop (turned copy, the stencil painted out) and the target-on-photo overlay."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import sd_family as SF
if __name__ == "__main__":
    SF.previews_main(HERE, "skip", [dict(gid="6875634", key="P1", path="P1rot.jpg", crop=(500, 150, 950, 370), fill=[(610, 218, 860, 305)], name="p1-grass-skip-side-elevation.jpg",
                                         overlay_name="p1-grass-skip-target-on-photo.jpg", photo_id="P1")])
