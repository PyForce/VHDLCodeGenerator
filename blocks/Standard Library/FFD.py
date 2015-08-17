#-------------------------------------------------------------------------------
#   PROJECT:   VHDL Code Generator
#   NAME:      Dynamic Decoder
#
#   LICENSE:   GNU-GPL V3
#-------------------------------------------------------------------------------

__isBlock__ = True
__className__ = "FFD"
__win__ = "FFDWindow"

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic

from lib.Block import *

class FFD(Block):
	""" FFD

		PORTS SPECIFICATIONS
	"""
	# TODO: Specifications of flip flop D (Documentation)
	def __init__(self,system,enablePreset=True,enablePresetActiveSymbol='0',definePreset='Asynchronous',enableClear=True,enableClearActiveSymbol='0',defineClear='Asynchronous',defineEdge='Negative'):
		"""

		:param name:
		:param Preset:    type of preset, synchronous or asynchronous
		:param Clear: 	  type of clear, synchronous or asynchronous
		:param Edge:	  clock triggering edge, negative or positive
		"""
		#setting flags
		self.one,self.both,self.Asynchronous_clear,self.Asynchronous_preset,self.clearflag,self.presetflag,self.ninguno=False,False,False,False,False,False,False
		if ((enablePreset and enableClear) and (definePreset=='Asynchronous' and defineClear=='Asynchronous')):
			self.both=True
		if ((enablePreset or enableClear) and (definePreset=='Asynchronous' or defineClear=='Asynchronous')):
			self.one=True
		if not self.both and self.one and defineClear=='Asynchronous':
			self.Asynchronous_clear=True
		if not self.both and self.one and definePreset=='Asynchronous':
			self.Asynchronous_preset=True
		if enablePreset and definePreset=='Synchronous':
			self.presetflag=True
		if enableClear and defineClear =='Synchronous':
			self.clearflag=True
		if not enablePreset and not enableClear:
			self.ninguno=True
		self.defineEdge=defineEdge
		self.enablePreset=enablePreset
		self.enablePresetActiveSymbol=enablePresetActiveSymbol
		self.definePreset=definePreset
		self.enableClear=enableClear
		self.enableClearActiveSymbol=enableClearActiveSymbol
		self.defineClear=defineClear
		self.name='FFD'

		input_vector=[1]*2 + ([1] if enablePreset else []) + ([1] if enableClear else [])
		output_vector=[1]*2
		super().__init__(input_vector,output_vector,system,self.name)

		#Setting Port names
		self.setInputName("D",0)
		if enablePreset and enableClear:
			self.setInputName("o_Pr" if enablePresetActiveSymbol=='0' else "Pr",3)
			self.setInputName("o_Cl" if enableClearActiveSymbol=='0' else "Cl",2)
		elif not enablePreset and enableClear:
			self.setInputName("o_Cl" if enableClearActiveSymbol=='0' else "Cl",2)
		elif enablePreset and not enableClear:
			self.setInputName("o_Pr" if enablePresetActiveSymbol=='0' else "Pr",2)

		self.setInputName("o_CLOCK" if self.defineEdge=='Negative' else "CLOCK",1)
		self.setOutputName("Q",0)
		self.setOutputName("Q_o",1)
		

	def generate(self):


		filetext=""
		filetext+="PROCESS ("+self.getInputSignalName(1)
		if self.Asynchronous_clear:
			filetext+=","+self.getInputSignalName(2)
		if self.both:
			filetext+=","+self.getInputSignalName(2)+","+self.getInputSignalName(3)  
		if self.Asynchronous_preset and not self.enableClear:
			filetext+=","+self.getInputSignalName(2)
		if self.Asynchronous_preset and self.clearflag:
			filetext+=","+self.getInputSignalName(3)
		filetext+=")\n"
	
		filetext+="BEGIN \n"
		if self.both:
			filetext+="if "+self.getInputSignalName(2)+" = '"+self.enableClearActiveSymbol+"' then "+self.getOutputSignalName(0)+" <= '0' ; "+self.getOutputSignalName(1)+" <= '1'; \nelsif "+self.getInputSignalName(3)+" = '"+self.enablePresetActiveSymbol+"' then "+self.getOutputSignalName(0)+" <= '1' ; "+self.getOutputSignalName(1)+" <= '0'; \nelsif "
		elif self.Asynchronous_clear:
			filetext+="if "+self.getInputSignalName(2)+" = '"+self.enableClearActiveSymbol+"' then "+self.getOutputSignalName(0)+" <= '0' ; "+self.getOutputSignalName(1)+" <= '1'; \nelsif "
		elif self.Asynchronous_preset and self.enableClear:
			filetext+="if "+self.getInputSignalName(3)+" = '"+self.enablePresetActiveSymbol+"' then "+self.getOutputSignalName(0)+" <= '1' ; "+self.getOutputSignalName(1)+" <= '0'; \nelsif "
		elif self.Asynchronous_preset and not self.enableClear:
			filetext+="if "+self.getInputSignalName(2)+" = '"+self.enablePresetActiveSymbol+"' then "+self.getOutputSignalName(0)+" <= '1' ; "+self.getOutputSignalName(1)+" <= '0'; \nelsif "
		elif not self.one:
			filetext+="if "
		filetext+="Falling_edge(" if self.defineEdge=='Negative' else "Rising_edge("
		filetext+=self.getInputSignalName(1)+") then "
		if self.both or self.ninguno:
			filetext+=self.getOutputSignalName(0)+" <= "+self.getInputSignalName(0)+" ; "+self.getOutputSignalName(1)+" <= not("+self.getInputSignalName(0)+") ;\n"
			filetext+="else "+self.getOutputSignalName(0)+" <= "+self.getOutputSignalName(0)+" ; "+self.getOutputSignalName(1)+" <= "+self.getOutputSignalName(1)+";\n"
			filetext+="END if;\nEND PROCESS;\n"
		elif not self.one and self.clearflag or self.presetflag :
			if self.clearflag:
				filetext+="\nif "+self.getInputSignalName(2)+" = '"+self.enableClearActiveSymbol+"' then "+self.getOutputSignalName(0)+" <= '0' ; "+self.getOutputSignalName(1)+" <= '1' ; \n"
				if self.presetflag:
					filetext+="elsif "+self.getInputSignalName(3)+" = '"+self.enablePresetActiveSymbol+"' then "+self.getOutputSignalName(0)+" <= '1' ; "+self.getOutputSignalName(1)+" <= '0' ; \nelse "
				else:
					filetext+="else "
			else:
				filetext+="\nif "+self.getInputSignalName(3)+" = '"+self.enablePresetActiveSymbol+"' then "+self.getOutputSignalName(0)+" <= '1' ; "+self.getOutputSignalName(1)+" <= '0' ; \nelse "
			filetext+=self.getOutputSignalName(0)+" <= "+self.getInputSignalName(0)+" ; "+self.getOutputSignalName(1)+" <= not("+self.getInputSignalName(0)+") ;\n"
			filetext+="END if ;\nEND if ;" if self.clearflag or self.presetflag else "END if ;"	
			filetext+="\nEND PROCESS ;"
		elif self.one and self.clearflag or self.presetflag:
			if self.clearflag:
				filetext+="\nif "+self.getInputSignalName(2)+" = '"+self.enableClearActiveSymbol+"' then "+self.getOutputSignalName(0)+" <= '0' ; "+self.getOutputSignalName(1)+" <= '1' ; \nelse "
			else:
				filetext+="\nif "+self.getInputSignalName(3)+" = '"+self.enablePresetActiveSymbol+"' then "+self.getOutputSignalName(0)+" <= '1' ; "+self.getOutputSignalName(1)+" <= '0' ; \nelse "
			filetext+=self.getOutputSignalName(0)+" <= "+self.getInputSignalName(0)+" ; "+self.getOutputSignalName(1)+" <= not("+self.getInputSignalName(0)+") ;\n"
			filetext+="END if ;\nEND if ;\nEND PROCESS ;"  	
		elif self.one:
			filetext+=self.getOutputSignalName(0)+" <= "+self.getInputSignalName(0)+" ; "+self.getOutputSignalName(1)+" <= not("+self.getInputSignalName(0)+") ;\n"
			filetext+="else "+self.getOutputSignalName(0)+" <= "+self.getOutputSignalName(0)+" ; "+self.getOutputSignalName(1)+" <= "+self.getOutputSignalName(1)+";\n"
			filetext+="END if ;\nEND PROCESS ;" 

		
		return filetext

class FFDWindow(QWidget):
	accept=pyqtSignal(list)

	def __init__(self,parent=None):
		super().__init__()
		self.ui=uic.loadUi("blocks\\Standard Library\\FFD.ui",self)
		self.ui.acceptButton.clicked.connect(self.accepted)

	def accepted(self):
		
		 
		includeEnablePreset=self.ui.preset.isChecked()
		if includeEnablePreset:
			presetactiveSymbol='0' if self.ui.presetsymb0.isChecked() else '1'
			presettype='Asynchronous' if self.ui.presettype0.isChecked() else 'Synchronous'
		else:
			presetactiveSymbol=None
			presettype=None
		includeEnableClear=self.ui.clear.isChecked()
		if includeEnableClear:
			clearactiveSymbol='0' if self.ui.clearsymb0.isChecked() else '1'
			cleartype='Asynchronous' if self.ui.cleartype0.isChecked() else 'Synchronous'
		else:
			clearactiveSymbol=None
			cleartype=None
		edge='Negative' if self.ui.defedge0.isChecked() else 'Positive'

		self.accept.emit([includeEnablePreset,presetactiveSymbol,presettype,includeEnableClear,clearactiveSymbol,cleartype,edge])
		self.close()

		   