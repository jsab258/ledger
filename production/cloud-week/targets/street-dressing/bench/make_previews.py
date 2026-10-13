"""bench: preview crop and the target-on-photo overlay."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import sd_family as SF
if __name__ == "__main__":
    SF.previews_main(HERE, "bench", [dict(gid="2693537", key="P1", crop=(120, 140, 540, 400), name="p1-poole-bench-back.jpg", overlay_name="p1-poole-bench-target-on-photo.jpg", photo_id="P1")])
