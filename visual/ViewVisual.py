# from data.MainWindow import MainWindow

__author__ = 'GVF'

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import visual.BlockVisual
import data.constants

class QView(QGraphicsView):
    def __init__(self, parent = None):
        super().__init__(parent)
        # self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.drawConn = False       # True if connection is drawing
        self.currentLine = None     # Active line
        self.mode = data.constants.DEFAULT_MODE

        self.lineSource = ()        # Source coordinates
        self.currentItem = None     # Source item

    def beginLine(self):
        print("BEGIN LINE")
        self.drawConn = True
        x,y = self.currentItem.x1,self.currentItem.y1
        self.currentLine = QGraphicsLineItem(x, y, x+1, y+1)
        self.scene().addItem(self.currentLine)

    def endLine(self,item):
        if isinstance(item,visual.BlockVisual.QPin):
            print("YEES")

        self.scene().removeItem(self.currentLine)
        self.drawConn = False
        self.currentLine = None

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        item = self.scene().itemAt(self.mapToScene(event.pos()))

        if isinstance(item,visual.BlockVisual.QPin):
            self.setCursor(Qt.CrossCursor)
            print("Dime algo")
        else:
            self.setCursor(Qt.ArrowCursor)

        if self.drawConn:
            coord = self.mapToScene(event.pos().x(), event.pos().y())
            x2 = coord.x()
            y2 = coord.y()
            self.currentLine.setLine(self.currentItem.x1, self.currentItem.y1, x2, y2)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        print("Estoy aqui!!!!!!!!!")
        item = self.itemAt(event.pos())
        if isinstance(item,visual.BlockVisual.QPin) and self.mode == data.constants.DEFAULT_MODE:
            print(item.block)
            print(item.index)
            print(item.mode)
            print("Im a QPin")
            # coord = self.mapToScene(event.pos().x(), event.pos().y())
            # self.beginLine(coord.x(), coord.y())
            self.currentItem = item
            # self.lineSource = item.x1,item.y1
            # self.beginLine(item.x1,item.y1)
            self.beginLine()
            self.setDragMode(self.NoDrag)


    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if self.drawConn:
            coord = self.mapToScene(event.pos().x(), event.pos().y())

            self.endLine(self.itemAt(coord.toPoint()))
            self.setDragMode(self.ScrollHandDrag)

            item = self.itemAt(event.pos())
            print("Item size:%d\nItem2 Size:%d"%(item.getSize(),self.currentItem.getSize()))

            if isinstance(item, visual.BlockVisual.QPin) and item.mode != self.currentItem.mode and item.getSize() == self.currentItem.getSize():
                if item.mode == data.constants.IN:
                    inputItem = item
                    outputItem = self.currentItem
                else:
                    inputItem = self.currentItem
                    outputItem = item
                if inputItem.getPort().connection == None:
                    print("ESTABLISHING CONNECTION BETWEEN %s & %s"%(str(inputItem),str(outputItem)))
                    # TODO: Establish full connection (Abstract and visual)
                    # ABSTRACT CONNECTION

                    # VISUAL CONNECTION
                    x1,y1 = self.currentItem.x1,self.currentItem.y1
                    x2,y2 = item.x1, item.y1
                    self.scene().addItem(QGraphicsLineItem(x1,y1,x2,y2))

            self.currentItem = None

    def wheelEvent(self, event):
        if event.delta() > 0:
            self.scale(1.25,1.25)
        else:
            self.scale(0.8,0.8)