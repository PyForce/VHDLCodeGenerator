#-------------------------------------------------------------------------------
#   PROJECT:   VHDL Code Generator
#   NAME:      Block visual
#
#   LICENSE:   GNU-GPL V3
#-------------------------------------------------------------------------------
from PyQt4.QtCore import QRectF

__author__ = "BlakeTeam"

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import data.constants
import visual.ViewVisual
from lib import *
from visual import *

class QBlock(QGraphicsItem):
    DX = 10 # Distance between ports
    PORT_SIZE = DX/2
    COLOR = 0,100,0,100 # Red, Green, Blue, Alpha
    WIDTH = 10
    ADJUST = 5

    def __init__(self, block, view = None):
        """ QGraphicsItem that represent the Blocks of VHDL Code.
        """
        super().__init__()
        self.block = block
        self.setPos(*block.screenPos)
        self.height = QBlock.DX*(max(len(self.block.input_ports), len(self.block.output_ports))+1)
        # self.width = self.height/

        x0,y0 = block.screenPos
        self.inputPort = []
        self.outputPort = []


        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setCursor(Qt.OpenHandCursor)

        di = self.height/(len(self.block.input_ports) + 1)
        do = self.height/(len(self.block.output_ports) + 1)

        scene = view.scene()
        self.scene = scene

        self.name_label = QGraphicsTextItem(str(self.block.__class__).split("'")[1].split(".")[-1], self)
        self.name_label.setPos(0, self.height - QBlock.ADJUST + 1)
        font = self.name_label.font()
        font.setPixelSize(QBlock.DX)

        self.in_labels = []
        self.out_labels = []

        in_width = 0
        out_width = 0
        # Drawing input ports

        for i, port in enumerate(self.block.input_ports):
            yi = di * (i + 1)
            pin = QPin(x0,y0,i,IN,di,self)
            # self.inputPort.addPin(pin)
            self.inputPort.append(pin)
            scene.addItem(pin)
            self.block.input_ports[i].pin = pin

            txt = QGraphicsTextItem(port.name, self)
            font = txt.font()                        #
            font.setPixelSize(QBlock.DX)                # adjusting label font
            txt.setFont(font)                        #
            point = pin.mapToItem(self,QPointF(pin.x2 ,pin.y1 - pin.dy)) # aligning label to pin
            txt.setPos(QBlock.PORT_SIZE, yi - di)                                         #
            in_width = max(in_width, txt.boundingRect().width())
            self.in_labels.append(txt)


        # Drawing output ports
        for i, port in enumerate(self.block.output_ports):

            txt = QGraphicsTextItem(port.name, self)
            font = txt.font()                        #
            font.setPixelSize(QBlock.DX)             # adjusting label font
            txt.setFont(font)                        #
            out_width = max(out_width, txt.boundingRect().width())
            self.out_labels.append(txt)

        self.width = in_width + QBlock.WIDTH + out_width
        self.rect = QRectF(0,0,self.width,self.height)


        for i, txt in enumerate(self.out_labels):
            yi = do * (i + 1)
            txt.setPos(self.width - txt.boundingRect().width(), yi - do)

            pin = QPin(x0,y0,i,OUT,do,self)
            # self.outputPort.addPin(pin)
            self.outputPort.append(pin)
            scene.addItem(pin)
            self.block.output_ports[i].pin = pin


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
        #painter.fillRect(0,0,self.width,self.height,QColor(*QBlock.COLOR))
        #painter.drawRoundedRect(0,0,self.width,self.height)
        painter.setBrush(QBrush(QColor(*QBlock.COLOR)))
        painter.drawRoundedRect(self.rect, QBlock.ADJUST, QBlock.ADJUST)




class ExternalBlock(QBlock):
    def __init__(self,block,view = None):
        super().__init__(block,view)

class EventFilter(QObject):
    def __init__(self):
        super().__init__()

    def sceneEventFilter(self, watched, event):
        pass


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
        self.diagonal = QLineF()

        self.size_label = QGraphicsTextItem(str(self.getSize()), self.parentItem())
        parent.scene.addItem(self.size_label)

        #def f(this):
        #    x = self.pos().x()
        #    y = self.pos().y() - QBlock.DX/2
        #    return QRectF(x,y,QBlock.PORT_SIZE, QBlock.DX)
        #
        #self.size_label.boundingRect = f
        #self.size_label.hide()
        font = self.size_label.font()
        font.setPixelSize(QBlock.DX/2)
        font.setStyleHint(QFont.Monospace)
        self.setZValue(10)
        self.size_label.setFont(font)
        self.size_label.setZValue(1)
        #self.size_label.stackBefore(self)
        #self.size_label.setFlag(QGraphicsItem.ItemStacksBehindParent)
        self.size_label.installEventFilter(EventFilter())
        self.myUpdate()
        self.rect = QRectF(min(self.x1, self.x2), min(self.y1, self.y2)-2, abs(self.x1 - self.x2), 4)
        self.setCursor(Qt.CrossCursor)



        self._shape = QPainterPath()
        self._shape.addRect(self.rect)
        self.setToolTip(str(self.getSize()))
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
        self.x = point.x()
        self.y = point.y()

        # Calculating coordinates of the pin
        # x1,y1 is the out node in both cases.
        if self.mode == IN:
            self.x1 = -QBlock.PORT_SIZE + self.x
            self.y1 = self.dy * (self.index + 1) + self.y
            self.x2 = self.x
            self.y2 = self.y1
            #self.size_label.setPos((self.x1+self.x2)/2 - QBlock.PORT_SIZE, self.y1 - self.dy)
        else:
            self.x1 = self.block.width + QBlock.PORT_SIZE + self.x
            self.y1 = self.dy*(self.index + 1) + self.y
            self.x2 = self.block.width + self.x
            self.y2 = self.y1
            #self.size_label.setPos((self.x1+self.x2)/2 - QBlock.PORT_SIZE, self.y1 - self.dy)
        #dx, dy = QBlock.PORT_SIZE/4,

        self.rect = QRectF(min(self.x1, self.x2), min(self.y1, self.y2)-2-self.dy/4, abs(self.x1 - self.x2), self.dy)
        self._shape = QPainterPath()
        self._shape.addRect(self.rect)

        self.size_label.setPos((self.x1+self.x2)/2 - QBlock.PORT_SIZE, self.y1 - self.dy)
        self.setLine(self.x1,self.y1,self.x2,self.y2)

        # if the port size is great than zero paint a diagonal line over the pin
        #if self.getSize()-1:
        #    xc,yc = (self.x1+self.x2)/2, self.y1
        #    dx, dy = QBlock.PORT_SIZE/4, self.dy/4
        #    self.diagonal.setLine(xc-dx, yc-dy, xc+dx, yc+dy)

        # Update Connection
        port = self.getPort()
        if port.mode == data.constants.IN:
            if port.connection != None:
                connLine = self.getAbstractBlock().system.connections[port.connection]
                otherPin = port.connection.out_block.output_ports[port.connection.ind_output].pin
                QView.paintConnection(self,otherPin,connLine)
                connLine.update()
        else:
            for i in port.connection:
                connLine = self.getAbstractBlock().system.connections[i]
                otherPin = i.in_block.input_ports[i.ind_input].pin
                QView.paintConnection(otherPin,self,connLine)
                connLine.update()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.pos() in self.rect:
            print(self.parentWidget(), self)

    def paint(self,painter:QPainter,styleOptionGraphicsItem,widget):
        super().paint(painter,styleOptionGraphicsItem,widget)
        self.myUpdate()
        #painter.drawRect(self.size_label.mapRectToItem(self,self.size_label.boundingRect()))
        #painter.drawRect(self.boundingRect())
        #painter.drawText(self.x1, self.y1 -QBlock.DX/2, 20,QBlock.DX, ,str(self.getSize()))
        #painter.drawRect(self.rect.adjusted(2,2,-2,-2)) # testing bounding box

        #painter.drawLine(self.diagonal)
        #painter.drawRect(QRectF(self.x2,self.y1-self.dy/4, QBlock.PORT_SIZE, self.dy/2))
        #if self.getPort().mode == IN:
        #    painter.drawText(QRectF(self.x1, self.y1 -QBlock.DX/2, 20,QBlock.DX), Qt.AlignRight, str(self.getSize()))
        #else:
        #    painter.drawText(QRectF(self.x1, self.y1 -QBlock.DX/2, 20,QBlock.DX), Qt.AlignLeft, str(self.getSize()))