#-------------------------------------------------------------------------------
#   PROJECT:   VHDL Code Generator
#   NAME:      New Project Window
#
#   LICENSE:   GNU-GPL V3
#-------------------------------------------------------------------------------

__author__ = "BlakeTeam"

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic

class NProjectWindow(QWidget):
    def __init__(self, main):
        super().__init__()
        self.initializeUI()
        self.main = main
        self.totInputPorts = 1
        self.totOutputPorts = 1

    def initializeUI(self):
        """ Initialize all graphics components of the New Project Window
        """
        self.ui = uic.loadUi('newProject.ui',self)
        self.ui.lineEdit.textChanged.connect(self.textChanged)
        self.ui.inputPorts.valueChanged(self.inputPortsUpdate)
        self.ui.outputPorts.valueChanged(self.outputPortsUpdate)

    # Functions to change the total of spin bar
    def inputPortsUpdate(self,value):
        pass

    def outputPortsUpdate(self,value):
        pass

    def textChanged(self,text):
        if self.validateName(text):
            self.ui.statusBar.setText("New name available")
        else:
            self.ui.statusBar.setText("New name NOT available !!!")

    def validateName(self,text):
        """ Check that the current name selected is available
        """
        return  not (text == "" or text in self.main.projects)

