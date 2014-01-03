#-------------------------------------------------------------------------------
#   PROJECT:   VHDL Code Generator
#   NAME:      Project Interface
#
#   LICENSE:   GNU-GPL V3
#-------------------------------------------------------------------------------

__author__ = "BlakeTeam"

import os.path
import pickle

from data import *
from visual.ViewVisual import *


from .System import System as _System
from visual.SystemVisual import QSystem

import visual.BlockVisual

class GraphicsScene(QGraphicsScene):
    def __init__(self):
        super().__init__()

class IProject:
    def __init__(self,path,input_vector,output_vector,mainWindow = None):
        """ Interface to handle each project.

        :string path:           Directory (name included of the current project)
        :Int[] input_vector:    List with the size of the input ports of the system
        :Int[] output_vector:   List with the size of the output ports of the system
        """
        self.dir, self.name = os.path.split(path)
        realName = self.name.split('.')[0]  # The name of the project without the extension
        self.system = _System(realName,input_vector,output_vector)
        self.scene = GraphicsScene()
        self.view = QView(self)
        self.view.setScene(self.scene)
        self.initializeView(self.view)

        self.mainWindow = mainWindow

    @classmethod
    def load(cls,path):
        dir, name = os.path.split(path)
        file = open(dir + "\\" + name,"rb")
        system = pickle.load(file)
        file.close()
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
        inp = visual.BlockVisual.ExternalBlock(self.system.system_input,view)
        out = visual.BlockVisual.ExternalBlock(self.system.system_output,view)

        self.scene.addItem(inp)
        self.scene.addItem(out)

        # self.visualSystem = QSystem(self.system)
        # self.scene.addItem(self.visualSystem)

        # Loading blocks
        for b in self.system.block:
            self.scene.addItem(QBlock(b, view))

        # TODO: Load Connections
        # Loading Connections
