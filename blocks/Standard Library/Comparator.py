#-------------------------------------------------------------------------------
#   PROJECT:   VHDL Code Generator
#   NAME:      Dynamic Decoder
#
#   LICENSE:   GNU-GPL V3
#-------------------------------------------------------------------------------

__isBlock__ = True
__className__ = "Comparator"
__win__ = "CompWindow"

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic

from lib.Block import *

class Comparator(Block):
	""" COMPARATOR

		PORTS SPECIFICATIONS
	"""
	# TODO: Specifications of comparator (Documentation)
	def __init__(self,system,sizeInput,numInput=2,defineOutput='0'):
		"""

		:param name:
		:param sizeInput:    Size of binary words to compare
		:param system:
		:stdLogic defineOutput: It only can be 0/1
		
		"""
		if defineOutput=='0':
			self.defecto='1'
		else:
			self.defecto='0'
		self.numInput=numInput
		self.sizeInput=sizeInput
		self.defineOutput=defineOutput
		self.name='Comparator'
		 
		input_vector=[self.sizeInput]*self.numInput
		output_vector=[1]*2
		super().__init__(input_vector,output_vector,system,self.name)

		#Setting Port names
		self.setInputName("P_"+str(self.sizeInput)+"bits",0)
		self.setInputName("Q_"+str(self.sizeInput)+"bits",1)
		self.setOutputName("P_equals_Q_o" if self.defineOutput=='0' else "P_equals_Q",0)
		self.setOutputName("P_greater_than_Q_o" if self.defineOutput=='0' else "P_greater_than_Q",1)
		
		#self.variables=[(enablerActiveSymbol,sizeInput)]
	def generate(self):
		filetext=""
		filetext+="%s <= %s when(%s=%s) else %s;\n"%(self.getOutputSignalName(0),"'"+self.defineOutput+"'",self.getInputSignalName(0),self.getInputSignalName(1),"'"+self.defecto+"'")
		filetext+="%s <= %s when(%s>%s) else %s;\n"%(self.getOutputSignalName(1),"'"+self.defineOutput+"'",self.getInputSignalName(0),self.getInputSignalName(1),"'"+self.defecto+"'")
		return filetext



class CompWindow(QWidget):
	accept=pyqtSignal(list)

	def __init__(self,parent=None):
		super().__init__()
		self.ui=uic.loadUi("blocks\\Standard Library\\Comparator.ui",self)
		self.ui.acceptButton.clicked.connect(self.accepted)

	def accepted(self):
		numInput=2
		sizeInput=self.ui.sizeInput.value()
		defineOutput='0' if self.ui.defOut0.isChecked() else '1'
		self.accept.emit([sizeInput,numInput, defineOutput])
		self.close()