#-------------------------------------------------------------------------------
#   PROJECT:   VHDL Code Generator
#   NAME:      Dynamic Coder
#
#   LICENSE:   GNU-GPL V3
#-------------------------------------------------------------------------------

__isBlock__ = True
__className__ = "Coder"
__win__ = "CodWindow"

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic

from lib.Block import *

class Coder(Block):
	""" CODER

		PORTS SPECIFICATIONS
	"""
	# TODO: Specifications of coder (Documentation)
	def __init__(self,system,numInput,priority='MSB',sizeInput='1',defineOutput='0',defineInput='0',enabler=True,enablerActiveSymbol='0'):
		"""

		:param name:
		:param codInput:    Total of input bits to code
		:param system:
		:stdLogic defineOutput: It only can be 0/1
		:stdLogic defineInput: It only can be 0/1
		:param enabler:
		:bit enablerActiveSymbol: It only can be 0/1. No hi Z available
		"""
		
		if defineOutput=='0':
			self.defectoOut='1'
		else:
			self.defectoOut='0'

		self.defineOutput =defineOutput
		self.defineInput=defineInput
		self.enablerActiveSymbol=enablerActiveSymbol
		self.enabler=enabler
		self.numCodIn=numInput
		self.priority=priority
		self.name='Coder'
		 
		input_vector=[sizeInput]*self.numCodIn + ([1] if enabler else [])
		output_vector=[len(bin(numInput)) - 2 ]
		super().__init__(input_vector,output_vector,system,self.name)

		#Setting Port names 
		

		if self.enabler==True:
			self.setInputName("o_EN",self.numCodIn) if self.enablerActiveSymbol=='0' else self.setInputName("EN",self.numCodIn)
		if defineOutput=="0":
			self.setOutputName("out0_o",0)
		else:
			self.setOutputName("out0  ",0)
		for i in range(self.numCodIn):
			if defineInput=='0':
				self.setInputName("o_"+"in"+str(i+1) ,i)
				if (i==self.numCodIn-1 and self.priority=='LSB'):
					self.setInputName("o_in1_High",0)
					self.setInputName("o_in"+str(i+1)+"_Low",i) 
					self.flag=1
				elif (i==self.numCodIn-1 and self.priority=='MSB'):
					self.setInputName("o_in"+str(i+1)+"_High",i)
					self.setInputName("o_in1_Low",0)
					self.flag=0
			else:
				self.setInputName("in"+str(i+1),i)
				if (i==self.numCodIn-1 and self.priority=='LSB'):
					self.setInputName("in1_High",0) 
					self.setInputName("in"+str(i+1)+"_Low",i)
					self.flag=1
				elif (i==self.numCodIn-1 and self.priority=='MSB'):
					self.setInputName("in"+str(i+1)+"_High",i)
					self.setInputName("in1_Low",0)
					self.flag=0
		#self.variables=[(enablerActiveSymbol,sizeInput)]

	def generate(self):
		filetext=''
		filetext+=self.getOutputSignalName(0)+" <="
		if self.flag:
			for i in range(self.numCodIn):
				binary=bin(i+1)[2:]
				a='0'*(len(bin(self.numCodIn)[2:])-len(binary))
				binary=a+binary
				binary=self.invert(binary) if self.defineOutput=='0' else binary
				if self.enabler==False:
					if i==0:
						filetext+=" %s when (%s=%s) else \n"%('"'+binary+'"',self.getInputSignalName(i), "'"+self.defineInput+"'")
					else:
						filetext+="                %s when (%s=%s) else \n"%('"'+binary+'"',self.getInputSignalName(i), "'"+self.defineInput+"'")
				else:
					if i==0:
						filetext+=" %s when (%s=%s and %s=%s) else \n"%('"'+binary+'"',self.getInputSignalName(i), "'"+self.defineInput+"'",self.getInputSignalName(self.numCodIn),"'"+self.enablerActiveSymbol+"'")
					else:
						filetext+="                %s when (%s=%s and %s=%s) else \n"%('"'+binary+'"',self.getInputSignalName(i), "'"+self.defineInput+"'",self.getInputSignalName(self.numCodIn),"'"+self.enablerActiveSymbol+"'")
		else:
			for i in range (self.numCodIn-1,-1,-1):
				binary=bin(i+1)[2:]
				a='0'*(len(bin(self.numCodIn)[2:])-len(binary))
				binary=a+binary
				binary=self.invert(binary) if self.defineOutput=='0' else binary
				if self.enabler==False:
					if i==self.numCodIn-1:
						filetext+=" %s when (%s=%s) else \n"%('"'+binary+'"',self.getInputSignalName(i), "'"+self.defineInput+"'")
					else:
						filetext+="                %s when (%s=%s) else \n"%('"'+binary+'"',self.getInputSignalName(i), "'"+self.defineInput+"'")
				else:
					if i==self.numCodIn-1:
						filetext+=" %s when (%s=%s and %s=%s) else \n"%('"'+binary+'"',self.getInputSignalName(i), "'"+self.defineInput+"'",self.getInputSignalName(self.numCodIn),"'"+self.enablerActiveSymbol+"'")
					else:
						filetext+="                %s when (%s=%s and %s=%s) else \n"%('"'+binary+'"',self.getInputSignalName(i), "'"+self.defineInput+"'",self.getInputSignalName(self.numCodIn),"'"+self.enablerActiveSymbol+"'")
		
			
		nothing=self.defectoOut*(len(bin(self.numCodIn)[2:]))
		filetext+='                "'+nothing+'"'+';'
		return filetext

	def invert(self,binary):
		b=''
		for i in binary:
			if i =='0':
				b+='1'
			else:
				b+='0'
		return b


class CodWindow(QWidget):
	accept=pyqtSignal(list)

	def __init__(self,parent=None):
		super().__init__()
		self.ui=uic.loadUi("blocks\\Standard Library\\Coder.ui",self)
		self.ui.acceptButton.clicked.connect(self.accepted)

	def accepted(self):
		sizeInput=1
		numInput=self.ui.numInput.value()
		includeEnabler=self.ui.enabler.isChecked()
		if includeEnabler:
			activeSymbol='0' if self.ui.symb0.isChecked() else '1'
		else:
			activeSymbol=None
		defineOutput='0' if self.ui.defOut0.isChecked() else '1'
		defineInput='0' if self.ui.defIn0.isChecked() else '1'
		priority='MSB' if self.ui.msb.isChecked() else 'LSB'
		self.accept.emit([numInput,priority,sizeInput,defineOutput,defineInput,includeEnabler,activeSymbol])
		self.close()

 