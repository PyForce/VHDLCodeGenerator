from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic

import pickle
import os

class Parametrizer(QWidget):
    def __init__(self):
        super().__init__()

        self.name = None
        self.ui = uic.loadUi(r'plugin\parametrizer.ui',self)
        self.setWindowTitle("Parametrizer")

        self.ui.accept.clicked.connect(self.ok)
        self.ui.blockTree.setHeaderLabel("")
        self.loadIcons()
        self.loadBlocks()

    def loadIcons(self):
        self.dynamicIco = QIcon("resources\\dynamic.ico")
        self.folderIco = QIcon("resources\\folder.ico")

    def __loadBlockFromDir__(self,item,path):
        files = False   # Return true if is a file, or is a directory with files inside
        dirItems = []
        fileItems = []
        for i in os.listdir():
            curPath = os.path.join(path,i)
            if os.path.isdir(i):
                os.chdir(i)
                child = QTreeWidgetItem([i])
                child.path = None
                if self.__loadBlockFromDir__(child,os.path.join(path,i)):
                    dirItems.append(child)
                    files = True
                os.chdir("..")
            else:
                name = os.path.splitext(i)[0]
                child = QTreeWidgetItem([name])

                mod = self.isDynamicBlock(curPath)
                if mod:
                    fileItems.append((child,self.dynamicIco,mod))
                    # self.blocks.append((child,curPath,data.constants.DYNAMIC_BLOCK,mod))
                    files = True

        for i in dirItems:
            item.addChild(i)
        for i,j,mod in fileItems:
            i.mod = mod
            item.addChild(i)
            i.setIcon(0,j)
        return files

    @staticmethod
    def isDynamicBlock(path):
        """ Check if the file refers to a dynamic block
            It returns the module if it is a dynamic block
        """
        if os.path.splitext(path)[1] == ".py":
            name = os.path.splitext(os.path.split(path)[1])[0]
            mod = __import__(name)
            try:
                if mod.__isBlock__:
                    return mod
            except:
                return False
        return False

    def loadBlocks(self):
        os.chdir("blocks")
        path = os.getcwd()
        for i in os.listdir():
            if os.path.isdir(i):
                os.chdir(i)
                item = QTreeWidgetItem([i])
                # item.setIcon(0,self.folderIco)
                item.path = None
                if self.__loadBlockFromDir__(item,os.path.join(path,i)):
                    self.ui.blockTree.addTopLevelItem(item)
                os.chdir("..")
        os.chdir("..")

    @staticmethod
    def validate(path):
        # TODO: It can't be two equal names.
        return True

    def ok(self):
        try:
            item = self.ui.blockTree.selectedItems()[0]
            self.mod = item.mod
            print(self.mod.__className__)

            self.name = self.ui.lineEdit.text()
            if Parametrizer.validate(self.name):
                win = self.mod.__getattribute__(self.mod.__win__)()
                win.show()
                win.accept.connect(self.save)
        except:
            print("INVALID ACCEPT")

    def save(self,args):
        f = open('blocks\\Parametric Library\\' + self.name + '.pvb','wb')
        name = self.mod.__className__
        pickle.dump((name,args),f)
        f.close()

def exec():
    param = Parametrizer()
    param.show()