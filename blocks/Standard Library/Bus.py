#-------------------------------------------------------------------------------
#   PROJECT:   VHDL Code Generator
#   NAME:      Dynamic Bus
#
#   LICENSE:   GNU-GPL V3
#-------------------------------------------------------------------------------

__isBlock__ = True
__className__ = "Bus"
__win__ = "BusWindow"

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic

from lib.Block import *

class Bus(Block):
    """ MULTIPLEXER

        PORTS SPECIFICATIONS
    """
    # TODO: Specifications of multiplexer (Documentation)
    def __init__(self,system,numbits,mode):
        """

        # Document
        """

        self.numbits = numbits
        self.mode = mode
        self.name = "Bus_" + mode

        if self.mode == "Splitter":
            input_vector = [self.numbits]
            output_vector = [1]*self.numbits
        else:
            input_vector = [1]*self.numbits
            output_vector = [self.numbits]

        super().__init__(input_vector,output_vector,system,self.name)

        if self.mode == "Splitter":
            for i in range (self.numbits):
                self.setOutputName("bit_"+str(self.numbits-1-i),i)
            self.setInputName("input_vector",0)
        else:
            for i in range (self.numbits):
                self.setInputName("bit_"+str(self.numbits-1-i),i)
            self.setOutputName("output_vector",0)



    def generate(self):
        filetext = ""
        if self.mode == "Splitter":
            for i in range(self.numbits):
                filetext += "%s <= %s"%(self.getOutputSignalName(i),self.getInputSignalName(0)+"["+str(self.numbits -1 -i)+"];\n")
        else:
            filetext += "%s <= "%self.getOutputSignalName(0)
            for i in range(self.numbits):
                filetext += "%s"%(self.getInputSignalName(i))
                if i != (self.numbits - 1):
                    filetext += " & "
            filetext += ";"
        return filetext


class BusWindow(QWidget):
    accept = pyqtSignal(list)

    def __init__(self,parent = None):
        super().__init__()
        self.ui = uic.loadUi("blocks\\Standard Library\\Bus.ui",self)
        self.ui.acceptButton.clicked.connect(self.accepted)

    def accepted(self):
        size = self.ui.size.value()
        mode = "Splitter" if self.ui.symb0.isChecked() else "Joiner"
        self.accept.emit([size,mode])
        self.close()


