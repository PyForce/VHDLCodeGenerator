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

    def __init__(self, block, view = None):
        """ QGraphicsItem that represent the Blocks of VHDL Code.
        """
        super().__init__()
        self.block = block
        self.setPos(*block.screenPos)
        self.height = QBlock.DX*(max(len(self.block.input_ports), len(self.block.output_ports))+1)
        # self.width = self.height/
        self.width = QBlock.WIDTH

        x0,y0 = block.screenPos
        print(x0,y0)
        self.inputPort = []
        self.outputPort = []
        # self.inputPort = QPort()
        # self.inputPort.setPos(*block.screenPos)
        #
        # self.outputPort = QPort()
        # self.outputPort.setPos(*block.screenPos)

        # self.rect = QRectF(-QBlock.PORT_SIZE,0,2*QBlock.PORT_SIZE + self.width,self.height).adjusted(0.5,0.5,0.5,0.5)
        self.rect = QRectF(0,0,self.width,self.height)
        # self.rectf = QRectF(-QBlock.PORT_SIZE,0,QBlock.PORT_SIZE+self.width,self.height).adjusted(0.1,0.1,0.1,0.1)

        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setCursor(Qt.OpenHandCursor)

        di = self.height/(len(self.block.input_ports) + 1)
        do = self.height/(len(self.block.output_ports) + 1)

        scene = view.scene()
        self.scene = scene

        # Drawing input ports
        for i in range(len(self.block.input_ports)):
            pin = QPin(x0,y0,i,IN,di,self)
            # self.inputPort.addPin(pin)
            self.inputPort.append(pin)
            scene.addItem(pin)

        # Drawing output ports
        for i in range(len(self.block.output_ports)):
            pin = QPin(x0,y0,i,OUT,do,self)
            # self.outputPort.addPin(pin)
            self.outputPort.append(pin)
            scene.addItem(pin)

    def updatePorts(self):
        for i in self.inputPort:
            i.myUpdate()
        for i in self.outputPort:
            i.myUpdate()

    def mouseMoveEvent(self,event):
        super().mouseMoveEvent(event)
        self.updatePorts()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.setCursor(Qt.ClosedHandCursor)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.setCursor(Qt.OpenHandCursor)
        self.block.screenPos = (self.pos().x(), self.pos().y())
        self.updatePorts()

    def boundingRect(self):
        return self.rect

    def shape(self):
        path = QPainterPath()
        path.addRect(self.rect)
        return path

    def paint(self,painter,styleOptionGraphicsItem,widget):
        painter.fillRect(0,0,self.width,self.height,QColor(*QBlock.COLOR))
        painter.drawRect(0,0,self.width,self.height)
        # di = self.height/(len(self.block.input_ports) + 1)
        # do = self.height/(len(self.block.output_ports) + 1)

class QPin(QGraphicsLineItem):
    # selected = pyqtSignal(QPin)

    def __init__(self, x, y, index, mode, dy, parent):
        """

        :int x:         x coordinate of the block that inherit
        :int y:         y coordinate of the block that inherit
        :int index:     position of the pin in the block
        :1/0 mode:      IN/OUT
        :float dy:      distance between two pins
        :param parent:  Block of the pin
        """
        super().__init__()
        self.dy = dy
        self.index = index
        self.mode = mode
        self.block = parent
        self.setCursor(Qt.CrossCursor)
        self.myUpdate()
        print("AQUI ESTA SELF.X1")
        print(self.x1)
        self.rect = QRectF(min(self.x1, self.x2), min(self.y1, self.y2)-2, abs(self.x1 - self.x2), 4)
        self._shape = QPainterPath()
        self._shape.addRect(self.rect)
        # parent.scene.addItem(QGraphicsRectItem(self.rect))

    def boundingRect(self):
        self.myUpdate()
        return self.rect

    def shape(self):
        self.myUpdate()
        return self._shape

    def getPort(self):
        if self.mode == IN:
            return self.getAbstractBlock().input_ports[self.index]
        else:
            return self.getAbstractBlock().output_ports[self.index]

    def getSize(self):
        return self.getPort().size

    def getAbstractBlock(self):
        return self.block.block

    def myUpdate(self):
        point = self.block.scenePos()
        # print(point)
        self.x = point.x()
        self.y = point.y()
        # print(self.x,self.y)

        # Calculating coordinates of the pin
        # x1,y1 is the out node in both cases.
        if self.mode == IN:
            self.x1 = -QBlock.PORT_SIZE + self.x
            self.y1 = self.dy * (self.index + 1) + self.y
            self.x2 = self.x
            self.y2 = self.y1
        else:
            self.x1 = QBlock.WIDTH + QBlock.PORT_SIZE + self.x
            self.y1 = self.dy*(self.index + 1) + self.y
            self.x2 = QBlock.WIDTH + self.x
            self.y2 = self.y1

        self.rect = QRectF(min(self.x1, self.x2), min(self.y1, self.y2)-2, abs(self.x1 - self.x2), 4)
        self._shape = QPainterPath()
        self._shape.addRect(self.rect)

        self.setLine(self.x1,self.y1,self.x2,self.y2)


    def paint(self,painter,styleOptionGraphicsItem,widget):
        # print(self.rect, self.rect.width(), self.rect.height())
        super().paint(painter,styleOptionGraphicsItem,widget)

        #painter.drawRect(self.rect)

    # def mousePressEvent(self,event):
    #     super().mousePressEvent(event)
    #     print("I was selected")
    #     print(self.x1,self.y1)
    #     self.selected.emit(self)
