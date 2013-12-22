#-------------------------------------------------------------------------------
#   PROJECT:   VHDL Code Generator
#   NAME:      Project Interface
#
#   LICENSE:   GNU-GPL V3
#-------------------------------------------------------------------------------

__author__ = "BlakeTeam"

import os.path

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from Class import System as _System
from Visual.MainWindow import *

class IProject:
    def __init__(self,path,input_vector,output_vector):
        """ Interface to handle each project.

        :string path:           Directory (name included of the current project)
        :Int[] input_vector:    List with the size of the input ports of the system
        :Int[] output_vector:   List with the size of the output ports of the system
        """
        self.dir,self.name = os.path.split(path)
        realName = self.name.split('.')[0]  # The name of the project without the extension
        self.system = _System(realName,input_vector,output_vector)
        self.scene = QGraphicsScene()
        self.view = QGraphicsView()
        self.view.setScene(self.scene)
        self.initializeView(self.view) #TODO: Test the view initializer(wheel event)

    def initializeView(self,view):
        """ Initialize all QGraphicsView components.
        """
        scene = QGraphicsScene()
        view.setScene(scene)

        def view_wheelEvent(event):
            if event.delta() > 0:
                view.scale(1.25,1.25)
                print("Scaling up")
            else:
                view.scale(0.8,0.8)
                print("Scaling down")

        view.setSceneRect(-WIDTH/2,-HEIGHT/2,WIDTH,HEIGHT)
        view.wheelEvent = view_wheelEvent