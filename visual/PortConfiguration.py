#-------------------------------------------------------------------------------
#   PROJECT:   VHDL Code Generator
#   NAME:      Block visual
#
#   LICENSE:   GNU-GPL V3
#-------------------------------------------------------------------------------

__author__ = "BlakeTeam"

__author__ = 'BlakeTeam'

import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic

class PortWidget(QWidget):
    def __init__(self,defaultName,total = 1,parent = None):
        super().__init__(parent)
        self.defaultName = defaultName
        self.total = total  # Total of ports on the screen

        self.lineEdit = [] # Name of the ports on memory
        self.spinBox = []  # Size of the ports on memory

        self.widgetLayout = QVBoxLayout()

        for i in range(total):
            widget = self.generateWidget(i)
            self.widgetLayout.addWidget(widget)

        self.setLayout(self.widgetLayout)

    def getInfo(self):
        return [(self.lineEdit[i].text(),self.spinBox[i].value()) for i in range(self.total)]

    def updateName(self,index,name):
        self.nameValue[index] = name

    def updatePortSize(self,index,size):
        self.portValue[index] = size

    def generateWidget(self,index):
        label = QLabel()
        label.setText("Port %d:"%(index))

        lineEdit = QLineEdit()
        lineEdit.setText("%s_%d"%(self.defaultName,index))
        self.lineEdit.append(lineEdit)

        spinBox = QSpinBox()
        spinBox.setMinimum(1)
        spinBox.setValue(1)
        self.spinBox.append(spinBox)

        curWidget = QWidget()
        portLayout = QHBoxLayout()
        portLayout.addWidget(label)
        portLayout.addWidget(lineEdit)
        portLayout.addWidget(spinBox)
        curWidget.setLayout(portLayout)

        return curWidget