#
#   PROJECT:   VHDL Code Generator
#   NAME:      main
#
#   LICENSE:   GNU-GPL V3
#

__author__ = "BlakeTeam"

# TODO: FIX IMPORTS

import sys
import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Class'))
visual_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Visual'))

sys.path.append(class_dir)
sys.path.append(visual_dir)

from MainWindow import MainWindow

IN = 1
OUT = 0

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()
    sys.exit(app.exec_())