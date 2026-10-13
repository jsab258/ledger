"""bicycle: draws the target from target.json alone (target_drawing.json; pictures into the folder on the command line)."""
import os
import sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import sd_family as SF

if __name__ == "__main__":
    SF.drawing_main(HERE, sys.argv[1:])
