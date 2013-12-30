#-------------------------------------------------------------------------------
#   PROJECT:   VHDL Code Generator
#   NAME:      Main Window
#
#   LICENSE:   GNU-GPL V3
#-------------------------------------------------------------------------------

__author__ = "BlakeTeam"

import os
import importlib
import pickle
import _pickle

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic

from visual import *
from lib import *

STATIC_BLOCK = 0
PARAMETRIC_BLOCK = 1
DYNAMIC_BLOCK = 2

DEFAULT_MODE = 0    # MOVE & CONNECT MODE
BLOCK_INSERTION = 1

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.projects = {}                  # All projects {string dirName: IProject project }
        self.dynamicProjectTable = [None]   # All projects opened (on tabs) {int tabIndex: IProject project }
        self.currentProject = None          # Project that is being used on each moment

        self.defaultDirectory = os.getenv("USERPROFILE") + r"\VHDL Code Generator\Projects"

        self.blocks = []    # Reference to the blocks to be loaded. <QItem:Path,Type>

        self.state = DEFAULT_MODE

        self.dynamicBlock = None    # Current loaded dynamic block
        self.parameters = None      # Parameters that receive the current loaded dynamic block

        self.initializeUI()

    def initializeUI(self):
        """ Initialize all graphics components of the Main Window.
        """
        self.ui = uic.loadUi('mainWindow.ui', self)

        self.loadIcons()
        # self.initializeToolBar()

        # Toggling dock widgets on closing
        self.ui.BlockBox.closeEvent = lambda event: self.ui.action_Block_Box.toggle()
        self.ui.Explorer.closeEvent = lambda event: self.ui.actionExplorer.toggle()

        self.ui.action_New_System.triggered.connect(self.create)
        self.ui.action_Load.triggered.connect(self.loadProject)
        self.ui.actionDefault.triggered.connect(self.setDefaultMode)
        self.ui.tabExplorer.tabCloseRequested.connect(self.removeTab)
        self.ui.tabExplorer.currentChanged.connect(self.changeTab)

        ### Tree Widget ###

        # Blocks
        self.ui.blockTree.setHeaderLabels(["Blocks"])
        self.ui.blockTree.itemDoubleClicked.connect(self.blockSelected)
        self.loadBlocks()
        print(self.blocks)

        # Explorer
        self.ui.explorerTree.setHeaderLabels(["Project Explorer"])
        self.ui.explorerTree.itemDoubleClicked.connect(self.projectSelected)

    # def initializeToolBar(self):
    #     toolBar = QToolBar(self)
    #     toolBar.setAllowedAreas(Qt.TopToolBarArea)
    #     self.layout().addWidget(toolBar)

    def setDefaultMode(self):
        self.state = DEFAULT_MODE
        self.ui.actionDefault.setChecked(True)

    def blockSelected(self,item,column):
        if self.currentProject == None:
            message = QMessageBox(self)
            message.setWindowTitle("WARNING")
            message.setIcon(QMessageBox.Warning)
            message.setText("There is no selected project")
            message.exec()

        else:
            founded = False
            for _item,path,type,mod in self.blocks:
                if item == _item:
                    founded = True
                    print("LOADING",path)
                    self.loadBlock(path,type,mod)
                    break
            if not founded:
                print("NO ITEM SELECTED")

    def loadBlock(self,path,type,mod = None):
        """ Loading selected block to the current system
        """
        print(path,type)

        if type == STATIC_BLOCK:
            pass
        elif type == PARAMETRIC_BLOCK:
            pass
        elif type == DYNAMIC_BLOCK:
            self.loadDynamicBlock(mod)

    def loadDynamicBlock(self,mod):
        print("Loading Dynamic Block")
        self.dynamicBlock = mod.__getattribute__(mod.__className__)
        win = mod.__getattribute__(mod.__win__)()
        win.show()
        win.accept.connect(self.loadParameters)

    def loadParameters(self,args):
        self.parameters = args
        self.state = BLOCK_INSERTION
        self.ui.actionDefault.setChecked(False)

    def loadIcons(self):
        self.standardIco = QIcon("resources\\standard.ico")
        self.parameterIco = QIcon("resources\\parameter.ico")
        self.dynamicIco = QIcon("resources\\dynamic.ico")
        self.folderIco = QIcon("resources\\folder.ico")
        self.projectIco = QIcon("resources\\project.png")

    @staticmethod
    def isParameterBlock(path):
        """ Check if the file refers to a Parameter block
        """
        return os.path.splitext(path)[1] == ".pvb"

    @staticmethod
    def isStandardBlock(path):
        """ Check if the file refers to a standard block
        """
        return os.path.splitext(path)[1] == ".svb"

    @staticmethod
    def isDynamicBlock(path):
        """ Check if the file refers to a dynamic block
            It returns the module if it is a dynamic block
        """
        if os.path.splitext(path)[1] == ".py":
            name = os.path.splitext(os.path.split(path)[1])[0]
            mod = importlib.__import__(name)
            try:
                if mod.__isBlock__:
                    return mod
            except:
                return False
        return False

    def __loadBlockFromDir__(self,item,path):
        files = False   # Return true if is a file, or is a directory with files inside
        dirItems = []
        fileItems = []
        for i in os.listdir():
            curPath = os.path.join(path,i)
            if os.path.isdir(i):
                os.chdir(i)
                child = QTreeWidgetItem([i])
                child.setIcon(0,self.folderIco)
                child.path = None
                if self.__loadBlockFromDir__(child,os.path.join(path,i)):
                    dirItems.append(child)
                    # item.addChild(child)
                    files = True
                os.chdir("..")
            else:
                name = os.path.splitext(i)[0]
                child = QTreeWidgetItem([name])
                #Standard Block
                if self.isStandardBlock(curPath):
                    fileItems.append((child,self.standardIco))
                    self.blocks.append((child,curPath,STATIC_BLOCK,None))
                    files = True
                # Parametric Block
                elif self.isParameterBlock(curPath):
                    fileItems.append((child,self.parameterIco))
                    self.blocks.append((child,curPath,PARAMETRIC_BLOCK,None))
                    files = True
                else:
                    mod = self.isDynamicBlock(curPath)
                    # Dynamic Block
                    if mod:
                        fileItems.append((child,self.dynamicIco))
                        self.blocks.append((child,curPath,DYNAMIC_BLOCK,mod))
                        files = True
        for i in dirItems:
            item.addChild(i)
        for i,j in fileItems:
            item.addChild(i)
            i.setIcon(0,j)
        return files

    def loadBlocks(self):

        os.chdir("blocks")

        path = os.getcwd()
        for i in os.listdir():
            if os.path.isdir(i):
                os.chdir(i)
                item = QTreeWidgetItem([i])
                item.setIcon(0,self.folderIco)
                item.path = None
                if self.__loadBlockFromDir__(item,os.path.join(path,i)):
                    self.ui.blockTree.addTopLevelItem(item)
                os.chdir("..")

        os.chdir("..")

    def loadProject(self):
        if os.path.exists(self.defaultDirectory):
            dialog = QFileDialog(self,"Loading...",self.defaultDirectory)
        else:
            dialog = QFileDialog(self,"Loading",os.getenv("USERPROFILE"))
        dialog.show()
        dialog.fileSelected.connect(self.loadFile)

    def loadFile(self,file):
        try:
            project = IProject.load(file)
            # TODO: ES AQUI
            project.scene.mousePressEvent = self.viewPressEvent
            if project.name in self.projects:
                print("YA EXISTE")
            else:
                name = project.name.split('.')[0]
                self.dynamicProjectTable.append(project)
                self.projects[name] = project
                self.currentProject = project

                self.ui.tabExplorer.addTab(project.view,name)
                self.ui.tabExplorer.setCurrentWidget(project.view)

                # Creating element in the explorer Tree
                item = QTreeWidgetItem()
                item.setText(0,name)
                item.setIcon(0,self.projectIco)
                self.ui.explorerTree.addTopLevelItem(item)

        except _pickle.UnpicklingError:
            message = QMessageBox(self)
            message.setText("The file format is not correct.\n"+file)
            message.exec()

    def projectSelected(self,item,column):
        project = self.projects[item.text(0)]
        try:
            index = self.dynamicProjectTable.index(project)
            self.ui.tabExplorer.setCurrentIndex(index)
        except ValueError:
            self.dynamicProjectTable.append(project)
            self.ui.tabExplorer.addTab(project.view,project.name.split('.')[0])
            self.ui.tabExplorer.setCurrentWidget(project.view)

    def removeTab(self,tab):
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
        project.scene.mousePressEvent = self.viewPressEvent

        self.dynamicProjectTable.append(project)
        self.projects[name] = project
        self.currentProject = project

        self.ui.tabExplorer.addTab(project.view,name)
        self.ui.tabExplorer.setCurrentWidget(project.view)

        # Creating element in the explorer Tree
        item = QTreeWidgetItem()
        item.setText(0,name)
        item.setIcon(0,self.projectIco)
        self.ui.explorerTree.addTopLevelItem(item)
        # # Drawing project
        # self.drawProject(project)

    def viewPressEvent(self,event):
        super(GraphicsScene,self.currentProject.scene).mousePressEvent(event)
        # TODO: Check everything is ok without mousePressEvent
        # super().mousePressEvent(event)
        pos = event.scenePos()
        x = int(pos.x())
        y = int(pos.y())
        if self.state == BLOCK_INSERTION:
            block = self.dynamicBlock(self.currentProject.system,*self.parameters)
            block.screenPos = x,y
            visualBlock = QBlock(block)
            self.currentProject.scene.addItem(visualBlock)