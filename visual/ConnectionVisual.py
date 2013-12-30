#-------------------------------------------------------------------------------
#   PROJECT:   VHDL Code Generator
#   NAME:      Connection visual
#
#   LICENSE:   GNU-GPL V3
#-------------------------------------------------------------------------------

__author__ = "BlakeTeam"

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class QConnection(QGraphicsItem):
    def __init__(self,connection,parent = None):
        super().__init__(parent)
        self.conn = connection
        self.node1 = None
        self.node2 = None
        self.getCoords()

    def getCoords(self):
        self.node1 = self.conn.in_block.getCoords(1,self.conn.ind_input)
        self.node2 = self.conn.out_block.getCoords(0,self.conn.ind_output)

    def refresh(self):
        self.getCoords()
        self.update()

    def boundingRect(self):
        x1,x2 = sorted(self.node1[0],self.node2[0])
        y1,y2 = sorted(self.node1[1],self.node2[1])
        return QRectF(0,0,x2 - x1,y2 - y1).adjusted(0.5,0.5,0.5,0.5)

    def shape(self):
        path = QPainterPath()
        path.addRect(self.rect)
        return path

    def paint(self,painter,styleOptionGraphicsItem,widget):
        x = min(self.node1[0],self.node2[0])
        y = min(self.node1[1],self.node2[1])
        painter.drawLine(self.node1[0] - x,self.node1[1] - y,self.node2[0] - x,self.node2[1] - y)
