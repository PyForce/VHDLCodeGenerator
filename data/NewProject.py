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

from data.PortConfigurationWindow import *

class NProjectWindow(QWidget):
    def __init__(self, main):
        super().__init__()
        self.initializeUI()
        self.main = main
        self.valid = False

    def initializeUI(self):
        """ Initialize all graphics components of the New Project Window
        """
        self.ui = uic.loadUi('newProject.ui',self)
        self.ui.name.textChanged.connect(self.textChanged)
        self.ui.acceptButton.clicked.connect(self.accept)
        self.ui.cancelButton.clicked.connect(self.cancel)
        # self.ui.inputPorts.valueChanged.connect(self.inputPortsUpdate)
        # self.ui.outputPorts.valueChanged.connect(self.outputPortsUpdate)

    def accept(self):
        if self.valid:
            pcWin = PortConfigurationWindow(self.ui.name.text(),self.ui.inputPorts.value(),self.ui.outputPorts.value(),self.main,self)
            pcWin.show()
            self.hide()

    def cancel(self):
        self.close()

    def textChanged(self,text):
        if self.validateName(text):
            self.ui.statusBar.setText("New name available")
            self.valid = True
        else:
            self.ui.statusBar.setText("New name NOT available !!!")
            self.valid = False

    def validateName(self,text):
        """ Check that the current name selected is available
        """
        return  not (text == "" or text in self.main.projects)

