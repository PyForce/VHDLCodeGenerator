#-------------------------------------------------------------------------------
#   PROJECT:   VHDL Code Generator
#   NAME:      Dynamic Multiplexer
#
#   LICENSE:   GNU-GPL V3
#-------------------------------------------------------------------------------

__isBlock__ = True
__className__ = "Multiplexer"
__win__ = "MuxWindow"

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic

from lib.Block import *

class Multiplexer(Block):
    """ MULTIPLEXER

        PORTS SPECIFICATIONS
    """
    # TODO: Specifications of multiplexer
    def __init__(self,system,name,numInput,sizeInput,defaultOutput='Z',enabler=True,enablerActiveSymbol = '0'):
        """

        :param name:
        :param muxInput:    Number of input
        :param size:        Size of each input
        :param system:
        :stdLogic defaultOutput: It only can be 0/1/Z
        :param enabler:
        :bit enablerActiveSymbol: It only can be 0/1. No hi Z available
        """
        self.defaultOutput = defaultOutput*sizeInput
        self.defaultOutput = self.defaultOutput.upper()
        self.enablerActiveSymbol = enablerActiveSymbol
        self.enabler = enabler
        self.selBits = len(bin(numInput)) - 2    # Binary Input Selector

        input_vector = [sizeInput]*numInput + [self.selBits] + ([1] if enabler else [])
        super().__init__(input_vector,[sizeInput],system,name)
        self.variables = [("CHOSEN",sizeInput)]

    def generate(self):
        pass

    @staticmethod
    def initializer(main):
        win = MuxWindow()
        win.show()

class MuxWindow(QWidget):
    accept = pyqtSignal(list)

    def __init__(self,parent = None):
        super().__init__()
        self.ui = uic.loadUi("blocks\\Standard Library\\Multiplexer.ui",self)
        self.ui.acceptButton.clicked.connect(self.accepted)

    def accepted(self):
        numInput = self.ui.numInput.value()
        sizeInput = self.ui.sizeInput.value()
        includeEnabler = self.ui.enabler.isChecked()
        if includeEnabler:
            activeSymbol = '0' if self.ui.symb0.isChecked() else '1'
        else:
            activeSymbol = None
        defaultOutput = '0' if self.ui.defOut0.isChecked() else ('1' if self.ui.defOut1.isChecked() else 'Z')

        self.accept.emit([numInput,sizeInput,defaultOutput,includeEnabler,activeSymbol])


if __name__ == "__main__":
    a = Multiplexer(5,8,False,None)