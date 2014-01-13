#-------------------------------------------------------------------------------
#   PROJECT:   VHDL Code Generator
#   NAME:      Dynamic NOT Gate
#
#   LICENSE:   GNU-GPL V3
#-------------------------------------------------------------------------------

__isBlock__ = True
__className__ = "NOTGate"
__win__ = "NOTGateWindow"

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic

from lib.Block import *

class NOTGate(Block):
    """ NOT Gate

        PORTS SPECIFICATIONS
    """
    # TODO: Specifications of NOT Gate (Documentation)
    def __init__(self,system,sizeInput):
        """

        :param name:
        :param numInput:    Number of input
        :param size:        Size of each input
        :param system:
        """
        self.name = "NOT_GATE"
        self.sizeInput = sizeInput


        input_vector = [sizeInput]
        output_vector = [sizeInput]
        super().__init__(input_vector,output_vector,system,self.name)

    def generate(self):
        filetext = ""
        if self.getOutputSignalSize(0) == 1:
            filetext += "%s <= not %s"%(self.getOutputSignalName(0),self.getInputSignalName(0))

        else:
            filetext += "%s <= "%self.getOutputSignalName(0)
            for i in range (self.sizeInput):
                filetext += "not %s[%d]"%(self.getInputSignalName(0),self.sizeInput-i-1)
                if i != self.sizeInput - 1:
                    filetext += " & "
        filetext += ";\n"
        return filetext

class NOTGateWindow(QWidget):
    accept = pyqtSignal(list)

    def __init__(self,parent = None):
        super().__init__()
        self.ui = uic.loadUi("blocks\\Standard Library\\GATE NOT.ui",self)
        self.ui.acceptButton.clicked.connect(self.accepted)
        self.ui.setWindowTitle("NOT GATE")

    def accepted(self):
        sizeInput = self.ui.sizeInput.value()

        self.accept.emit([sizeInput])
        self.close()


