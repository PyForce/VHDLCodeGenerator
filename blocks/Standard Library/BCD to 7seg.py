#-------------------------------------------------------------------------------
#   PROJECT:   VHDL Code Generator
#   NAME:      Dynamic BCD to 7 seg
#
#   LICENSE:   GNU-GPL V3
#-------------------------------------------------------------------------------

__isBlock__ = True
__className__ = "BCD27seg"
__win__ = "BCD27segwin"

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic

from lib.Block import *

class BCD27seg(Block):

    def __init__(self,system, type):

        self.type = type
        self.name = "BCDTo7Segments"

        input_vector = [4]
        output_vector = [7]
        super().__init__(input_vector,output_vector,system,self.name)

        # Settings port names
        self.setInputName("BCD",0)

        self.setOutputName("7seg",0)
        self.variables = [("segBuffer",7)]

    def generate(self):
        filetext = ""

        filetext += "%s <= "%(self.getVariableSignalName(0))
        filetext += """"1111110"  when {0}="0000" else  --0
"0110000"  when {0}="0001"  else   --1
"1101101"  when {0}="0010"  else   --2
"1111001"  when {0}="0011"  else   --3
"0110011"  when {0}="0100"  else   --4
"1011011"  when {0}="0101"  else   --5
"1011111"  when {0}="0110"  else   --6
"1110001"  when {0}="0111"  else   --7
"1111111"  when {0}="1000"  else   --8
"1111011"  when {0}="1001"  else   --9
"1110111"  when {0}="1010"  else   --A
"0011111"  when {0}="1011"  else   --B
"1001110"  when {0}="1100"  else   --C
"0111101"  when {0}="1101"  else   --D
"1001111"  when {0}="1110"  else   --E
"1000111"  when {0}="1111";            --F

{1} <= {2}{3};
""".format(self.getInputSignalName(0),self.getOutputSignalName(0),"not " if self.type == "common_anode" else "",self.getVariableSignalName(0))

        return filetext


class BCD27segwin(QWidget):
    accept = pyqtSignal(list)

    def __init__(self,parent = None):
        super().__init__()
        self.ui = uic.loadUi("blocks\\Standard Library\\BCD to 7seg.ui",self)
        self.ui.acceptButton.clicked.connect(self.accepted)

    def accepted(self):
        display_type = "common_anode" if self.ui.comanod.isChecked() else "common_cathode"

        self.accept.emit([display_type])
        self.close()


