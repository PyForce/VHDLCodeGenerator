#-------------------------------------------------------------------------------
# Name:       Port Configuration
# Project:    QTester
# Purpose:     
#
# Created:     <22/12/13-12:10>
#-------------------------------------------------------------------------------

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

        self.nameValue = [defaultName + "_" + str(i) for i in range(total)] # Name of the ports on memory
        self.portValue = [1 for i in range(total)]  # Size of the ports on memory

        for i in range(total):
            widget = self.generateWidget(i)
            self.widgetLayout.addWidget(widget)

        self.setLayout(self.widgetLayout)

    def getInfo(self):
        return [(self.nameValue[i],self.portValue[i]) for i in range(self.total)]

    def updateName(self,index,name):
        self.nameValue[index] = name

    def updatePortSize(self,index,size):
        self.portValue[index] = size

    def generateWidget(self,index):
        label = QLabel()
        label.setText("Port %d:"%(index))
        lineEdit = QLineEdit()
        lineEdit.setText(self.nameValue[index])
        spinBox = QSpinBox()
        spinBox.setMinimum(1)
        spinBox.setValue(1)

        curWidget = QWidget()
        portLayout = QHBoxLayout()
        portLayout.addWidget(label)
        portLayout.addWidget(lineEdit)
        portLayout.addWidget(spinBox)
        curWidget.setLayout(portLayout)

        return curWidget