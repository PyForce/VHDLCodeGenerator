#-------------------------------------------------------------------------------
#   PROJECT:   VHDL Code Generator
#   NAME:      Connection visual
#
#   LICENSE:   GNU-GPL V3
#-------------------------------------------------------------------------------

__author__ = "BlakeTeam"

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class QConnection(QGraphicsItem):
    def __init__(self,parent = None):
        super().__init__(parent)