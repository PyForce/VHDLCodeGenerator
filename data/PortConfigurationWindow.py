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

from visual.PortConfiguration import *

class PortConfigurationWindow(QWidget):
    def __init__(self, name, tot_input, tot_output, main, parent):
        """ Window to configure name and size of all ports (input/output)

        :string name:       Name of the project
        :int tot_input:     Amount of input ports
        :param tot_output:  Amount of output ports
        :MainWindow main:   Reference to the mainWindow
        :NewProject parent: Reference to newProjectWindow
        """
        super().__init__()
        self.main = main
        self.totInputPorts = tot_input
        self.totOutputPorts = tot_output
        self.name = name
        self.parent = parent
        self.initializeUI()

        self.text = "There can't be more than one port with the same name"

    def initializeUI(self):
        """ Initialize all graphics components of the New Project Window
        """
        self.ui = uic.loadUi('PortConfiguration.ui',self)
        self.setWindowTitle(self.name)
        self.ui.input.setText(str(self.totInputPorts))
        self.ui.output.setText(str(self.totOutputPorts))

        self.inputWidget = PortWidget("input",self.totInputPorts)
        self.outputWidget = PortWidget("output",self.totOutputPorts)

        self.ui.inputScroll.setWidget(self.inputWidget)
        self.ui.outputScroll.setWidget(self.outputWidget)

        self.ui.acceptButton.clicked.connect(self.accept)
        self.ui.cancelButton.clicked.connect(self.cancel)

    def validate(self):
        """ Check if all names are valid, they doesn't match between them

        :return:    True/False
        """
        validNames = set()
        _in = self.inputWidget.lineEdit
        _out = self.outputWidget.lineEdit

        for i in range(len(_in)):
            curText = _in[i].text()
            if curText in validNames:
                return False
            validNames.add(curText)

        for i in range(len(_out)):
            curText = _out[i].text()
            if curText in validNames:
                return False
            validNames.add(curText)

        return True

    def cancel(self):
        self.parent.show()
        self.close()

    def accept(self):
        self.text += "!"
        if self.validate():
            self.main.createProject(self.name,self.inputWidget.getInfo(),self.outputWidget.getInfo())
            self.parent.close()
            self.close()
        else:
            self.ui.statusBar.setText(self.text)
