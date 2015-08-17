#-------------------------------------------------------------------------------
#   PROJECT:   VHDL Code Generator
#   NAME:      Main Window
#
#   LICENSE:   GNU-GPL V3
#-------------------------------------------------------------------------------
from data.constants import STATIC_BLOCK

__author__ = "BlakeTeam"

import os
import importlib
import pickle
import _pickle
import data.constants
import data.NewProject
import plugin.parametrizer
import lib.StaticBlock
import visual.CodeViewer

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic

from visual import *
from lib import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.projects = {}                  # All projects {string dirName: IProject project }
        self.dynamicProjectTable = [None]   # All projects opened (on tabs) {int tabIndex: IProject project }
        self.currentProject = None          # Project that is being used on each moment

        self.defaultDirectory = os.getenv("USERPROFILE") + r"\VHDL Code Generator\Projects"

        self.blocks = []    # Reference to the blocks to be loaded. <QItem:Path,Type,Mod>
        self.tempBlocks = []

        self.state = data.constants.DEFAULT_MODE

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


        self.ui.actionBlock_Parametrizer.triggered.connect(plugin.parametrizer.exec)
        self.ui.action_Save.triggered.connect(self.save)
        self.ui.action_New_System.triggered.connect(self.create)
        self.ui.action_Load.triggered.connect(self.loadProject)
        self.ui.action_Export.triggered.connect(self.exportStaticBlock)
        self.ui.tabExplorer.tabCloseRequested.connect(self.removeTab)
        self.ui.tabExplorer.currentChanged.connect(self.changeTab)

        self.ui.action_Set_Default_Mode.triggered.connect(self.setDefaultMode)
        self.ui.toolBar.addAction(self.ui.action_Set_Default_Mode)
        self.ui.action_Set_Default_Mode.setIcon(QIcon("resources/cursor.png"))

        self.ui.action_Generate_Code.triggered.connect(self.buildVHDLCode)
        self.ui.toolBar.addAction(self.ui.action_Generate_Code)
        self.ui.action_Generate_Code.setIcon(QIcon("resources/build.png"))

        self.ui.actionExport_VHDL_Code.triggered.connect(self.exportVhdl)
        self.ui.toolBar.addAction(self.ui.actionExport_VHDL_Code)
        self.ui.actionExport_VHDL_Code.setIcon(QIcon("resources/export.png"))
        self.ui.newProjectLink.clicked.connect(self.create)

        #self.ui.tabExplorer.currentWidget().setBackgroundRole(QPalette.Dark)

        self.ui.actionSave_All.triggered.connect(lambda: QMessageBox.warning(self, "Warning", "Operation not available yet", QMessageBox.Ok))


        ### Tree Widget ###

        # Blocks
        self.ui.blockTree.setHeaderLabels(["Blocks"])
        self.ui.blockTree.itemDoubleClicked.connect(self.blockSelected)
        self.loadBlocks()
        self.refreshBlocks()
        print(self.blocks)

        # Explorer
        self.ui.explorerTree.setHeaderLabels(["Project Explorer"])
        self.ui.explorerTree.itemDoubleClicked.connect(self.projectSelected)

        # Generated Code
        self.codeViewer = None

    def exportStaticBlock(self):
        if self.currentProject == None:
            self.WARNSelectProject()

        else:
            name = self.currentProject.name
            code = self.currentProject.system.exportVHDLCode()
            print("THE CODE")
            print(code)
            print("END THE CODE")

            signals = []

            for i in self.currentProject.system.block:
                blockSignals = i.getSignals()
                for sign in blockSignals:
                    signals.append((i.name + "__" + sign[0],sign[1],data.constants.TEMP))

            for i in self.currentProject.system.system_input.output_ports:
                signals.append((i.name,i.size,data.constants.IN))

            for i in self.currentProject.system.system_output.input_ports:
                signals.append((i.name,i.size,data.constants.OUT))

            lib.StaticBlock.StaticBlock.save(os.path.splitext(name)[0],signals,code)
            #staticBlock = lib.StaticBlock.StaticBlock(name,signals,code)
            #staticBlock.save()

        self.refreshBlocks()

    def parametrizer(self):
        plugin.parametrizer.exec()
        self.refreshBlocks()
        print("QUE VOLA")

    def refreshBlocks(self):
        print("REFRESHING")
        print(len(self.blocks))
        self.ui.blockTree.clear()
        self.loadBlocks()
        print(len(self.blocks))

    def buildVHDLCode(self):
        #print("Showing code")
        if self.currentProject == None:
            self.WARNSelectProject()
            return

        if self.codeViewer:
            self.codeViewer.destroy()
        self.codeViewer = visual.CodeViewer.CodeViewer(self)
        self.addDockWidget(Qt.RightDockWidgetArea, self.codeViewer)
        self.codeViewer.showCode(self.currentProject.system.buildVHDLCode(), ".".join(self.currentProject.name.split(".")[:-1]))
        self.codeViewer.show()

    def save(self):
        QMessageBox.warning(self, "Warning", "Operation not available yet", QMessageBox.Ok)
        return
        try:
            print("IT WILL SAVE")
            self.currentProject.save()
        except AttributeError:
            print("There is no project selected")

    def setDefaultMode(self):

        if self.currentProject == None:
            self.ui.action_Set_Default_Mode.setChecked(False)
            message = QMessageBox(self)
            message.setWindowTitle("WARNING")
            message.setIcon(QMessageBox.Warning)
            message.setText("There is no selected project")
            message.exec()
        else:
            self.state = data.constants.DEFAULT_MODE
            self.ui.action_Set_Default_Mode.setChecked(True)
            #self.currentProject.view.mode = self.state

    def WARNSelectProject(self):
        message = QMessageBox(self)
        message.setWindowTitle("WARNING")
        message.setIcon(QMessageBox.Warning)
        message.setText("There is no selected project")
        message.exec()


    def blockSelected(self,item,column):
        if self.currentProject == None:
            self.WARNSelectProject()
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

        if type == data.constants.STATIC_BLOCK:
            self.loadStaticBlock(path)
        elif type == data.constants.PARAMETRIC_BLOCK:
            self.loadParametricBlock(path,mod)
        elif type == data.constants.DYNAMIC_BLOCK:
            self.loadDynamicBlock(mod)

        # TODO: Set state to Block insertion if static and parametric mode, the view of the curProject too

    def loadStaticBlock(self,path):
        print("Loading Static Block")
        self.state = data.constants.BLOCK_INSERTION
        self.ui.action_Set_Default_Mode.setChecked(False)
        self.type = data.constants.STATIC_BLOCK
        self.path = path

    def loadParametricBlock(self,path,mod):
        print("Load Parametric Block")
        print(path,mod)
        self.dynamicBlock = mod.__getattribute__(mod.__className__)
        self.parameters = self.parameterData(path)[1]
        self.state = data.constants.BLOCK_INSERTION
        self.ui.action_Set_Default_Mode.setChecked(False)
        self.type = data.constants.PARAMETRIC_BLOCK

    def loadDynamicBlock(self,mod):
        print("Loading Dynamic Block")
        self.dynamicBlock = mod.__getattribute__(mod.__className__)
        win = mod.__getattribute__(mod.__win__)()
        win.show()
        win.accept.connect(self.loadParameters)
        self.type = data.constants.DYNAMIC_BLOCK

    def loadParameters(self,args):
        if args != None:
            self.parameters = args
            self.state = data.constants.BLOCK_INSERTION
            #self.currentProject.view.mode = self.state
            self.ui.action_Set_Default_Mode.setChecked(False)

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
    def isStaticBlock(path):
        """ Check if the file refers to a static block
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
                print(curPath)
                if self.isStaticBlock(curPath):
                    fileItems.append((child,self.standardIco))
                    self.tempBlocks.append((child,curPath,data.constants.STATIC_BLOCK,None))
                    files = True

                # Parametric Block
                elif self.isParameterBlock(curPath):
                    # Loading the name of the class of the dynamic block that build it
                    dynamicBlockName = self.parameterName(curPath)
                    mod = self.findModule(dynamicBlockName)

                    if mod != None:
                        fileItems.append((child,self.parameterIco))
                        self.tempBlocks.append((child,curPath,data.constants.PARAMETRIC_BLOCK,mod))
                        files = True
                else:
                    mod = self.isDynamicBlock(curPath)
                    # Dynamic Block
                    if mod:
                        fileItems.append((child,self.dynamicIco))
                        self.tempBlocks.append((child,curPath,data.constants.DYNAMIC_BLOCK,mod))
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

        self.blocks = self.tempBlocks
        self.tempBlocks = []

    def findModule(self,name):
        """ Find a dynamic block with the given name and return the loaded module
            of it.
        """
        for child,path,_type,mod in self.blocks:
            try:
                if name == mod.__className__:
                    print(path)
                    return mod
            except:
                print("YO NO TENGO CLASS NAME")
                print(path)
                continue
        return None

    def parameterData(self,path):
        """ Get the name and arguments of the dynamic block that build the parametric block chosen
        """
        file = open(path,'rb')
        name,args = pickle.load(file)
        return name,args

    def parameterName(self,path):
        """ Get the name of the dynamic block that build the parametric block chosen
        """
        return self.parameterData(path)[0]

    def loadProject(self):
        QMessageBox.warning(self, "Warning", "Not yet available", QMessageBox.Ok)
        return
        if os.path.exists(self.defaultDirectory):
            dialog = QFileDialog(self,"Load Project",self.defaultDirectory)
        else:
            dialog = QFileDialog(self,"Load Project",os.getenv("USERPROFILE"))
        dialog.show()
        dialog.fileSelected.connect(self.loadFile)


    def exportVhdl(self):
        path = self.defaultDirectory if os.path.exists(self.defaultDirectory) else os.getenv("USERPROFILE")
        fileName = QFileDialog.getSaveFileName(self, "Save File",
                            path,
                            "VHDL file (*.vhd)")

        file = open(fileName, 'w')
        file.write(self.currentProject.system.buildVHDLCode())
        file.close()


    def loadFile(self,file):
        try:
            project = IProject.load(file)
            project.mainWindow = self
            project.scene.mousePressEvent = self.scenePressEvent
            if project.name in self.projects:
                print("Already exists")
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
            self.setDefaultMode()
            self.currentProject = self.dynamicProjectTable[tab]
            print(str(self.currentProject.name))
        except AttributeError:
            self.currentProject = None
            print("None")

    def create(self):
        """ Call the Project Creator Window.
        """
        projectCreator = data.NewProject.NProjectWindow(self)
        projectCreator.show()

    def createProject(self,name,input_info,output_info):
        directory = self.defaultDirectory + "\\" + name + ".vcgp"
        project = IProject(directory,input_info,output_info,self)
        project.save()
        project.scene.mousePressEvent = self.scenePressEvent

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

    def scenePressEvent(self,event):
        curScene = self.currentProject.scene
        super(GraphicsScene,curScene).mousePressEvent(event)

        pos = event.scenePos()
        x = int(pos.x())
        y = int(pos.y())
        elements = curScene.itemAt(x,y)

        if self.state == data.constants.BLOCK_INSERTION:
            if self.type == data.constants.STATIC_BLOCK:
                name,signals,code = lib.StaticBlock.StaticBlock.load(self.path)
                block = lib.StaticBlock.StaticBlock(name,signals,code,self.currentProject.system)
            else:
                print(self.dynamicBlock)
                print(self.parameters)
                block = self.dynamicBlock(self.currentProject.system,*self.parameters)

            self.currentProject.system.block.append(block)
            block.screenPos = x,y
            visualBlock = QBlock(block, self.currentProject.view)
            self.currentProject.scene.addItem(visualBlock)
            visualBlock.setPos(x,y)
            self.setDefaultMode()

        elif self.state == data.constants.DEFAULT_MODE:
            pass