"""milk-crates: the masked preview crop of photograph P1."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import sd_family as SF
if __name__ == "__main__":
    SF.previews_main(HERE, "milk-crates", [dict(gid="6898849", key="P1", crop=(430, 560, 780, 940), fill=[(520, 755, 730, 840)], blur=[(480, 625, 690, 760)], radius=5, name="p1-pavement-two-crates-stacked.jpg")])
