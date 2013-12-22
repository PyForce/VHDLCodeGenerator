#
#   PROJECT:   VHDL Code Generator
#   NAME:      Main Window
#
#   LICENSE:   GNU-GPL V3
#

__author__ = "BlakeTeam"

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic

from Class import *
from Visual import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initializeUI()

        # Current info related to the project that the user is working
        self.currentView = None

    def initializeUI(self):
        """ Initialize all graphics components of the Main Window.
        """
        self.ui = uic.loadUi('circuits.ui', self)
        self.initializeActions()
        self.ui.BlockBox.closeEvent = lambda event: self.ui.action_Block_Box.toggle()

    def initializeView(self,view):
        """ Initialize all QGraphicsView components.
        """
        scene = QGraphicsScene()
        view.setScene(scene)

        def view_wheelEvent(event):
            if event.delta() > 0:
                self.currentView.scale(1.25,1.25)
            else:
                self.currentView.scale(0.8,0.8)

        view.setSceneRect(-WIDTH/2,-HEIGHT/2,WIDTH,HEIGHT)
        view.wheelEvent = view_wheelEvent

    def initializeActions(self):
        """  Connect all action with the signals.
        """
        self.initializeTabWidget()
        self.ui.action_New_System.triggered.connect(self.create)

    def initializeTabWidget(self):
        """ Initialize the actions on the TabWidget
        """
        self.ui.tabWidget.tabCloseRequested.connect(self.ui.tabWidget.removeTab)
        self.ui.tabWidget.currentChanged.connect(self.changeTab)

    def changeTab(self,tab):
        """ Action that is executed when the
        """
        # TODO: This is a test code, here is when we set the new current project
        try:
            self.currentView = self.tabWidget.widget(self.tabWidget.currentIndex()).layout().itemAt(0).widget()   # Current View
            system = System("main",(2,3),(5,))
            self.currentView.scene().addItem(QSystem(system))
        except AttributeError:
            pass

    def create(self):
        """ Create a new Project, generating a new TabWidget and initializing it components.
        """
        #TODO: We have to allow that the user can set the name of the current project.

        widget = QWidget()  # Widget on the TabWidget
        self.ui.tabWidget.insertTab(self.ui.tabWidget.count(),widget,"new")
        view = QGraphicsView()
        layout = QHBoxLayout()
        widget.setLayout(layout)
        layout.addWidget(view)
        self.initializeView(view)