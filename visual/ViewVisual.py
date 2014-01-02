__author__ = 'GVF'

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import visual.BlockVisual

class QView(QGraphicsView):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.drawConn = False       # True if connection is drawing
        self.currentLine = None     # Active line
        self.lineSource = ()        # Source coordinates

    def beginLine(self, x, y):
        self.drawConn = True
        self.lineSource = (x, y)
        self.currentLine = QGraphicsLineItem(x, y, x+1, y+1)
        self.scene().addItem(self.currentLine)

    def endLine(self,item):
        if isinstance(item,visual.BlockVisual.QPin):
            print("YEES")

        self.scene().removeItem(self.currentLine)
        self.drawConn = False
        self.currentLine = None
        self.lineSource = ()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        item = self.scene().itemAt(self.mapToScene(event.pos()))

        if isinstance(item,visual.BlockVisual.QPin):
            self.setCursor(Qt.CrossCursor)
            print("Dime algo")
        else:
            self.setCursor(Qt.ArrowCursor)
            print(".",end = "")

        if self.drawConn:
            x1,y1 = self.lineSource
            coord = self.mapToScene(event.pos().x(), event.pos().y())
            x2 = coord.x()
            y2 = coord.y()
            self.currentLine.setLine(x1, y1, x2, y2)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        print("Estoy aqui!!!!!!!!!")
        item = self.itemAt(event.pos())
        if isinstance(item,visual.BlockVisual.QPin):
            print(item.block)
            print(item.index)
            print(item.mode)
            print("Im a QPin")
            # coord = self.mapToScene(event.pos().x(), event.pos().y())
            # self.beginLine(coord.x(), coord.y())
            self.lineSource = item.x1,item.y1
            self.beginLine(item.x1,item.y1)
            self.setDragMode(self.NoDrag)


    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if self.drawConn:
            coord = self.mapToScene(event.pos().x(), event.pos().y())

            self.endLine(self.itemAt(coord.toPoint()))
            self.setDragMode(self.ScrollHandDrag)

            item = self.itemAt(event.pos())
            if isinstance(item, visual.BlockVisual.QPin):
                x1,y1 = self.lineSource
                x2,y2 = item.x2, item.y2
                print("add line",x1,y1,x2,y2)
                self.scene().addItem(QGraphicsLineItem(x1,y1,x2,y2))

    def wheelEvent(self, event):
        if event.delta() > 0:
            self.scale(1.25,1.25)
        else:
            self.scale(0.8,0.8)