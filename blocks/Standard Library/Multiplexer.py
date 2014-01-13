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
    # TODO: Specifications of multiplexer (Documentation)
    def __init__(self,system,numInput,sizeInput,defaultOutput='Z',enabler=True,enablerActiveSymbol = '0'):
        """

        :param name:
        :param muxInput:    Total of multiplexed input
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
        self.numMuxIn = numInput
        self.selBits = len(bin(numInput - 1)) - 2    # Binary Input Selector
        self.name = "Multiplexer"
        self.HiZ = "Z"*sizeInput


        input_vector = [sizeInput]*self.numMuxIn + [self.selBits] + ([1] if enabler else [])
        output_vector = [sizeInput]
        super().__init__(input_vector,output_vector,system,self.name)

        # Settings port names
        self.setInputName("SELECT",self.numMuxIn)

        if self.enabler == True:
            self.setInputName("EN",self.numMuxIn + 1)

        self.setOutputName("out",0)
        self.variables = [("CHOSEN",sizeInput)]

    def generate(self):
        filetext = ""
        if self.enabler == False:
            filetext += "%s <= "%(self.getOutputSignalName(0))
            for i in range(self.numMuxIn):
                selbinary = bin(i)[2:]
                filetext += "%s when (%s = %s) else\n"%(self.getInputSignalName(i),self.getInputSignalName(self.numMuxIn),"'"+selbinary+"'" if self.getInputSignalSize(self.numMuxIn) == 1 else '"'+selbinary+'"')
            filetext += "%s when others;\n"%(("'"+self.defaultOutput+"'") if (len(self.defaultOutput) == 1) else ('"'+self.defaultOutput+'"'))
        else:
            filetext += "%s <= "%(self.name + "__" + self.variables[0][0])
            for i in range(self.numMuxIn):
                selbinary = bin(i)[2:]
                filetext += "%s when (%s = %s) else\n"%(self.getInputSignalName(i),self.getInputSignalName(self.numMuxIn),"'"+selbinary+"'" if self.getInputSignalSize(self.numMuxIn) == 1 else '"'+selbinary+'"')
            filetext += "%s when others;\n"%("'"+self.defaultOutput+"'" if len(self.defaultOutput) == 1 else '"'+self.defaultOutput+'"')
            filetext += "%s <= %s when %s = %s else\n"%(self.getOutputSignalName(0),self.getVariableSignalName(0),self.getInputSignalName(self.numMuxIn + 1),"'"+self.enablerActiveSymbol+"'")
            filetext += "%s when others;\n"%(("'"+self.HiZ+"'") if (len(self.HiZ) == 1) else ('"'+self.HiZ+'"'))
        return filetext


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
        self.close()


