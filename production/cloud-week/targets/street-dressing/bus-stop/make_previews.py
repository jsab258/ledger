"""bus-stop: preview crops (card print blurred) and the target-on-photo overlay."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import sd_family as SF
if __name__ == "__main__":
    SF.previews_main(HERE, "bus-stop", [dict(gid="5668101", key="P1", crop=(430, 40, 660, 480), blur=[(528, 292, 575, 366)], name="p1-fulbrook-stop-flag-and-case.jpg",
                                             overlay_name="p1-fulbrook-stop-target-on-photo.jpg", photo_id="P1", radius=4)])
