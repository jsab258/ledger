"""bicycle: the preview crop of photograph P1 (the roadster leaning on a wall)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import sd_family as SF
if __name__ == "__main__":
    SF.previews_main(HERE, "bicycle", [dict(gid="2932507", key="P1", crop=(210, 40, 640, 380), name="p1-ruin-roadster-leaning.jpg")])
