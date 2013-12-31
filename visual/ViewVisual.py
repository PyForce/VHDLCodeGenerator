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

    def endLine(self):
        self.drawConn = False
        self.currentLine = None
        self.scene().removeItem(self.currentLine)
        self.lineSource = ()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if self.drawConn:
            x,y = self.lineSource
            coord = self.mapToScene(event.pos().x(), event.pos().y())
            self.currentLine.setLine(x, y, coord.x(), coord.y())

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        # print("press")
        # item = self.itemAt(event.pos())
        # if isinstance(item,visual.BlockVisual.QPin):
        #     print("Im a QPin")
        # coord = self.mapToScene(event.pos().x(), event.pos().y())
        # self.beginLine(coord.x(), coord.y())

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if self.drawConn:
            self.endLine()

    def wheelEvent(self, event):
        if event.delta() > 0:
            self.scale(1.25,1.25)
        else:
            self.scale(0.8,0.8)