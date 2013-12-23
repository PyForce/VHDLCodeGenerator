#-------------------------------------------------------------------------------
#   PROJECT:   VHDL Code Generator
#   NAME:      Main Window
#
#   LICENSE:   GNU-GPL V3
#-------------------------------------------------------------------------------

__author__ = "BlakeTeam"

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic

from lib.System import System as _System
from lib.Block import *
from lib.Connection import *

from visual.SystemVisual import *

WIDTH = 200
HEIGHT = 200

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initializeUI()

        self.projects = {}              # All projects {string dirName: IProject project }
        self.dynamicProjectTable = {}   # All projects opened (on tabs) {int tabIndex: IProject project }
        self.currentProject = None      # Project that is being used on each moment

    def initializeUI(self):
        """ Initialize all graphics components of the Main Window.
        """
        self.ui = uic.loadUi('mainWindow.ui', self)

        # Toggling dock widgets on closing
        self.ui.BlockBox.closeEvent = lambda event: self.ui.action_Block_Box.toggle()

        self.ui.action_New_System.triggered.connect(self.create)
        self.ui.tabWidget.tabCloseRequested.connect(self.ui.tabWidget.removeTab)
        self.ui.tabWidget.currentChanged.connect(self.changeTab)

    def changeTab(self,tab):
        """ Action that is executed when the tab is changed.
            Current project should be changed.
        """
        # TODO: This is a test code, here is when we set the new current project
        try:
            print(tab)
            # self.currentView = self.tabWidget.widget(self.tabWidget.currentIndex()).layout().itemAt(0).widget()   # Current View
            # system = _System("main",(2,3),(5,))
            # self.currentView.scene().addItem(QSystem(system))
        except AttributeError:
            pass

    def create(self):
        """ Create a new Project, generating a new TabWidget and initializing it components.
        """
        #TODO: We have to allow that the user can set the name of the current project.
        #TODO: Two projects with the same name are not allowed

        widget = QWidget()  # Widget on the TabWidget
        self.ui.tabWidget.insertTab(self.ui.tabWidget.count(),widget,"new")
        view = QGraphicsView()
        layout = QHBoxLayout()
        widget.setLayout(layout)
        layout.addWidget(view)
        # self.initializeView(view)