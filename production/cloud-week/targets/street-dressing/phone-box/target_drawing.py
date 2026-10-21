"""phone-box: draws the target from target.json alone: elevations, plan and sections as filled polygons in millimetres
(target_drawing.json) and, with a folder on the command line, as pictures. Usage: python target_drawing.py [PICTURE_DIR]"""
import os
import sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import sd_lib as L

if __name__ == "__main__":
    L.drawing_main(HERE, sys.argv[1:])
