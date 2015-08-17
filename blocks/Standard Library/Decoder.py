#-------------------------------------------------------------------------------
#   PROJECT:   VHDL Code Generator
#   NAME:      Dynamic Decoder
#
#   LICENSE:   GNU-GPL V3
#-------------------------------------------------------------------------------

__isBlock__ = True
__className__ = "Decoder"
__win__ = "DecWindow"

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic

from lib.Block import *

class Decoder(Block):
	""" DECODER

		PORTS SPECIFICATIONS
	"""
	# TODO: Specifications of decoder (Documentation)
	def __init__(self,system,sizeInput,numInput=1,defineOutput='0',enabler=True,enablerActiveSymbol='0'):
		"""

		:param name:
		:param decInput:    Total of input bits to decode
		:param system:
		:stdLogic defineOutput: It only can be 0/1
		:param enabler:
		:bit enablerActiveSymbol: It only can be 0/1. No hi Z available
		"""
		if defineOutput=='0':
			self.defecto='1'
		else:
			self.defecto='0'
		self.activity=defineOutput
		self.enablerActiveSymbol=enablerActiveSymbol
		self.enabler=enabler
		self.numDecodIn=sizeInput
		self.name='Decoder'
		 
		input_vector=[self.numDecodIn] + ([1] if enabler else [])
		output_vector=[numInput]*(2**sizeInput)
		super().__init__(input_vector,output_vector,system,self.name)

		#Setting Port names 
		

		if self.enabler==True:
			self.setInputName("o_EN",1) if self.enablerActiveSymbol=='0' else self.setInputName("EN",1)
		for i in range(2**sizeInput):
			if defineOutput=="0":
				self.setOutputName("out"+str(i)+"_o",i)
			else:
				self.setOutputName("out"+str(i),i)
		#self.variables=[(enablerActiveSymbol,sizeInput)]

	def generate(self):
		filetext=""
		
		for i in range(2**self.numDecodIn):
			binary=bin(i)[2:]
			a='0'*(len(bin((2**self.numDecodIn)-1)[2:])-len(binary))
			binary=a+binary
			if self.enabler==False:
				filetext+="%s <= %s when (%s=%s) else %s;\n"%(self.getOutputSignalName(i),"'"+ self.activity+"'",self.getInputSignalName(0),"'"+binary+"'" if self.numDecodIn ==1  else '"'+binary+'"',"'"+self.defecto+"'")
			else:
				filetext+="%s <= %s when (%s=%s and %s=%s) else %s;\n"%(self.getOutputSignalName(i),"'"+ self.activity+"'",self.getInputSignalName(0),"'"+binary+"'" if self.numDecodIn ==1  else '"'+binary+'"',self.getInputSignalName(1),"'"+self.enablerActiveSymbol+"'","'"+self.defecto+"'")
		return filetext

	
		
		

class DecWindow(QWidget):
	accept=pyqtSignal(list)

	def __init__(self,parent=None):
		super().__init__()
		self.ui=uic.loadUi("blocks\\Standard Library\\Decoder.ui",self)
		self.ui.acceptButton.clicked.connect(self.accepted)

	def accepted(self):
		numInput=1
		sizeInput=self.ui.sizeInput.value()
		includeEnabler=self.ui.enabler.isChecked()
		if includeEnabler:
			activeSymbol='0' if self.ui.symb0.isChecked() else '1'
		else:
			activeSymbol=None
		defineOutput='0' if self.ui.defOut0.isChecked() else '1'

		self.accept.emit([sizeInput,numInput,defineOutput,includeEnabler,activeSymbol])
		self.close()


		 

 