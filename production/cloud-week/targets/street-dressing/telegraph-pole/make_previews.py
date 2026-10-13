"""telegraph-pole: the preview crop of photograph P1 (the pole's upper part; the cars are below the crop)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import sd_family as SF
if __name__ == "__main__":
    SF.previews_main(HERE, "telegraph-pole", [dict(gid="2630310", key="P1", crop=(290, 0, 560, 310), name="p1-wilmott-close-pole-top.jpg")])
