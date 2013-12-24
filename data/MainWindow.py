#-------------------------------------------------------------------------------
#   PROJECT:   VHDL Code Generator
#   NAME:      Main Window
#
#   LICENSE:   GNU-GPL V3
#-------------------------------------------------------------------------------

__author__ = "BlakeTeam"

import os
import pickle

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic

from lib.System import System as _System
from lib.Block import *
from lib.Connection import *

from visual.SystemVisual import *
from data.NewProject import *
from lib.ProjectInterface import *

WIDTH = 200
HEIGHT = 200

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initializeUI()

        self.projects = {}                  # All projects {string dirName: IProject project }
        self.dynamicProjectTable = [None]   # All projects opened (on tabs) {int tabIndex: IProject project }
        self.currentProject = None          # Project that is being used on each moment

        self.defaultDirectory = os.getenv("USERPROFILE") + r"\VHDL Code Generator\Projects"

    def initializeUI(self):
        """ Initialize all graphics components of the Main Window.
        """
        self.ui = uic.loadUi('mainWindow.ui', self)

        # Toggling dock widgets on closing
        self.ui.BlockBox.closeEvent = lambda event: self.ui.action_Block_Box.toggle()
        self.ui.Explorer.closeEvent = lambda event: self.ui.actionExplorer.toggle()

        self.ui.action_New_System.triggered.connect(self.create)
        self.ui.tabExplorer.tabCloseRequested.connect(self.removeTab)
        self.ui.tabExplorer.currentChanged.connect(self.changeTab)

        # Tree Widget
        self.ui.explorerTree.setHeaderLabels(["Project Explorer"])
        self.ui.explorerTree.itemDoubleClicked.connect(self.projectSelected)

    def projectSelected(self,item,column):
        project = self.projects[item.text(0)]
        try:
            index = self.dynamicProjectTable.index(project)
            #TODO: I DON'T KNOW HOW TO SET FOCUS TO THE GIVEN TAB
            self.ui.tabExplorer.setTabEnabled(index,True)
        except ValueError:
            self.dynamicProjectTable.append(project.view)
            self.ui.tabExplorer.addTab(project.view,project.name.split('.')[0])

    def removeTab(self,tab):
        if tab != 0:    # Tab 0 is not closable
            print("REMOVING TAB %d"%tab)
            self.dynamicProjectTable.remove(self.dynamicProjectTable[tab])
            self.ui.tabExplorer.removeTab(tab)

    def changeTab(self,tab):
        """ Action that is executed when the tab is changed.
            Current project should be changed.
        """
        print("CURRENT PROJECT: ",end = "")
        try:
            self.currentProject = self.dynamicProjectTable[tab]
            print(str(self.currentProject.name))
        except AttributeError:
            self.currentProject = None
            print("None")

    def create(self):
        """ Call the Project Creator Window.
        """
        projectCreator = NProjectWindow(self)
        projectCreator.show()

    def createProject(self,name,input_info,output_info):
        directory = self.defaultDirectory + "\\" + name + ".vcgp"
        project = IProject(directory,input_info,output_info)
        project.save()

        self.dynamicProjectTable.append(project)
        self.projects[name] = project
        self.currentProject = project

        self.ui.tabExplorer.addTab(project.view,name)

        # Creating element in the explorer Tree
        item = QTreeWidgetItem()
        item.setText(0,name)
        self.ui.explorerTree.addTopLevelItem(item)

