#-------------------------------------------------------------------------------
#   PROJECT:   VHDL Code Generator
#   NAME:      Dynamic NOR Gate
#
#   LICENSE:   GNU-GPL V3
#-------------------------------------------------------------------------------

__isBlock__ = True
__className__ = "NORGate"
__win__ = "NORGateWindow"

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic

from lib.Block import *

class NORGate(Block):
    """ NOR Gate

        PORTS SPECIFICATIONS
    """
    # TODO: Specifications of NOR Gate (Documentation)
    def __init__(self,system,numInput,sizeInput):
        """

        :param name:
        :param numInput:    Number of input
        :param size:        Size of each input
        :param system:
        """
        self.numInput = numInput
        self.name = "NOR_GATE"
        self.sizeInput = sizeInput


        input_vector = [sizeInput]*self.numInput
        output_vector = [sizeInput]
        super().__init__(input_vector,output_vector,system,self.name)

    def generate(self):
        filetext = ""
        if self.getOutputSignalSize(0) == 1:
            filetext += "%s <= %s"%(self.getOutputSignalName(0),self.getInputSignalName(0))
            for i in range(1,self.numInput):
                filetext += " nor %s"%(self.getInputSignalName(i))
        else:
            filetext += "%s <= "%self.getOutputSignalName(0)
            for i in range (self.sizeInput):
                filetext += "%s[%d]"%(self.getInputSignalName(0),self.sizeInput-i-1)
                for j in range(1,self.numInput):
                    filetext += " nor %s[%d]"%(self.getInputSignalName(j),self.sizeInput-i-1)
                if i != self.sizeInput - 1:
                    filetext += " & "
        filetext += ";\n"
        return filetext

class NORGateWindow(QWidget):
    accept = pyqtSignal(list)

    def __init__(self,parent = None):
        super().__init__()
        self.ui = uic.loadUi("blocks\\Standard Library\\Gate.ui",self)
        self.ui.acceptButton.clicked.connect(self.accepted)
        self.ui.setWindowTitle("NOR GATE")

    def accepted(self):
        numInput = self.ui.numInput.value()
        sizeInput = self.ui.sizeInput.value()

        self.accept.emit([numInput,sizeInput])
        self.close()


