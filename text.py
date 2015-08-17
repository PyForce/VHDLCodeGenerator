__author__ = 'FarSeer'

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys

app = QApplication(sys.argv)
win = QTextEdit()
win.setText("VHDL Code Generator")
win.show()

win2 = QTextEdit()
win2.setText("VHDL Code Generator2")
win2.show()
app.exec_()