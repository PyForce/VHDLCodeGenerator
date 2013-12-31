#-------------------------------------------------------------------------------
#   PROJECT:   VHDL Code Generator
#   NAME:      Block visual
#
#   LICENSE:   GNU-GPL V3
#-------------------------------------------------------------------------------

__author__ = "BlakeTeam"

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from lib import *
from visual import *

class QBlock(QGraphicsItem):
    DX = 10 # Distance between ports
    PORT_SIZE = DX/2
    COLOR = 0,100,0,100 # Red, Green, Blue, Alpha
    WIDTH = 40

    def __init__(self, block, parent = None):
        """ QGraphicsItem that represent the Blocks of VHDL Code.
        """
        super().__init__()
        self.block = block
        self.setPos(*block.screenPos)
        self.height = QBlock.DX*(max(len(self.block.input_ports), len(self.block.output_ports))+1)
        # self.width = self.height/
        self.width = WIDTH

        self.inputPort = QPort(parent, self)
        self.inputPort.setPos(*block.screenPos)

        self.outputPort = QPort(parent, self)
        self.outputPort.setPos(*block.screenPos)

        self.rect = QRectF(-QBlock.PORT_SIZE,0,2*QBlock.PORT_SIZE + self.width,self.height).adjusted(0.5,0.5,0.5,0.5)
        # self.rectf = QRectF(-QBlock.PORT_SIZE,0,QBlock.PORT_SIZE+self.width,self.height).adjusted(0.1,0.1,0.1,0.1)

        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setCursor(Qt.OpenHandCursor)

        x0,y0 = block.screenPos

        di = self.height/(len(self.block.input_ports) + 1)
        do = self.height/(len(self.block.output_ports) + 1)

        # Drawing input ports
        for i in range(len(self.block.input_ports)):
            self.inputPort.addPin(QPin(-QBlock.PORT_SIZE +x0,di*(i + 1) +y0,0 +x0,di*(i + 1) +y0, self.inputPort))

        # Drawing output ports
        for i in range(len(self.block.output_ports)):
            self.outputPort.addPin(QPin(self.width  +x0,do*(i + 1) +y0,self.width+ QBlock.PORT_SIZE +x0,do*(i + 1) +y0, self.outputPort))

    def boundingRect(self):
        return self.rect

    def shape(self):
        path = QPainterPath()
        path.addRect(self.rect)
        return path

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.setCursor(Qt.ClosedHandCursor)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.setCursor(Qt.OpenHandCursor)
        self.block.screenPos = (self.pos().x(), self.pos().y())

    def paint(self,painter,styleOptionGraphicsItem,widget):
        painter.fillRect(0,0,self.width,self.height,QColor(*QBlock.COLOR))
        painter.drawRect(0,0,self.width,self.height)

        di = self.height/(len(self.block.input_ports) + 1)
        do = self.height/(len(self.block.output_ports) + 1)

class QPort(QGraphicsItemGroup):
    def __init__(self, view, parent=None):
        super().__init__(parent)
        self._parent = parent
        self.view = view
        self.pins = []

    def addPin(self, pin):
        self.addToGroup(pin)
        self.pins.append(pin)


class QPin(QGraphicsLineItem):
    def __init__(self,x0, y0, x1, y1, parent=None):
        super().__init__(x0, y0, x1, y1)
        self._parent = parent
        self.setCursor(Qt.CrossCursor)
    #     self.rect = super().boundingRect().adjusted(.1, 1, .1, 1)
    #
    # def boundingRect(self):
    #     return self.rect



