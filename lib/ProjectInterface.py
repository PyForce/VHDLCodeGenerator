#-------------------------------------------------------------------------------
#   PROJECT:   VHDL Code Generator
#   NAME:      Project Interface
#
#   LICENSE:   GNU-GPL V3
#-------------------------------------------------------------------------------

__author__ = "BlakeTeam"

import os.path
import pickle

from lib.System import System as _System
from data.MainWindow import *
from data import *

class IProject:
    def __init__(self,path,input_vector,output_vector):
        """ Interface to handle each project.

        :string path:           Directory (name included of the current project)
        :Int[] input_vector:    List with the size of the input ports of the system
        :Int[] output_vector:   List with the size of the output ports of the system
        """
        self.dir, self.name = os.path.split(path)
        realName = self.name.split('.')[0]  # The name of the project without the extension
        self.system = _System(realName,input_vector,output_vector)
        self.scene = QGraphicsScene()
        self.view = QGraphicsView()
        self.view.setScene(self.scene)
        self.initializeView(self.view) #TODO: Test the view initializer(wheel event)

    @classmethod
    def load(cls,path):
        dir, name = os.path.split(path)###########################
        file = open(dir + "\\" + name,"rb")#######################
        system = pickle.load(file)################################
        file.close()##############################################
        return IProject(path,system.input_info,system.output_info)

    def save(self):
        # Saving file
        vhdlDir,proj = os.path.split(self.dir)

        try:os.mkdir(vhdlDir)
        except:pass
        try:os.mkdir(vhdlDir+"\\"+proj)
        except:pass
        f = open(self.dir + "\\" + self.name,"wb")
        pickle.dump(self.system,f)
        f.close()

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