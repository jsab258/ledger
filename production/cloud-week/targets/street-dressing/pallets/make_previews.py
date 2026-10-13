"""pallets: the preview crop of photograph P1 (the leaning pallets; the fish boxes lie outside the crop)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import sd_family as SF
if __name__ == "__main__":
    SF.previews_main(HERE, "pallets", [dict(gid="2660949", key="P1", crop=(0, 150, 400, 580), name="p1-maiden-street-pallets-leaning.jpg")])
