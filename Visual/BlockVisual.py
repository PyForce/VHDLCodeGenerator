#
#   PROJECT:   VHDL Code Generator
#   NAME:      Block Visual
#
#   DATE: 12/10/13
#   TIME: 7:14 PM
#

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic

class QBlock(QGraphicsItem):
    DX = 10 # Distance between ports
    PORT_SIZE = DX/2
    COLOR = 0,100,0,100 # Red, Green, Blue, Alpha

    def __init__(self, block, parent = None):
        """ QGraphicsItem that represent the Blocks of VHDL Code.
        """
        super().__init__(parent)
        self.block = block
        self.height = QBlock.DX*(max(len(self.block.input_ports), len(self.block.output_ports))+1)
        # self.width = self.height/
        self.width = 40

        self.rect = QRectF(-QBlock.PORT_SIZE,0,2*QBlock.PORT_SIZE + self.width,self.height).adjusted(0.5,0.5,0.5,0.5)
        # self.rectf = QRectF(-QBlock.PORT_SIZE,0,QBlock.PORT_SIZE+self.width,self.height).adjusted(0.1,0.1,0.1,0.1)

        self.setFlag(QGraphicsItem.ItemIsMovable)

    def boundingRect(self):
        return self.rect

    def shape(self):
        path = QPainterPath()
        path.addRect(self.rect)
        return path

    def paint(self,painter,styleOptionGraphicsItem,widget):
        painter.fillRect(0,0,self.width,self.height,QColor(*QBlock.COLOR))
        painter.drawRect(0,0,self.width,self.height)

        di = self.height/(len(self.block.input_ports) + 1)
        do = self.height/(len(self.block.output_ports) + 1)

        # Drawing input ports
        for i in range(len(self.block.input_ports)):
            painter.drawLine(-QBlock.PORT_SIZE,di*(i + 1),0,di*(i + 1))

        # Drawing output ports
        for i in range(len(self.block.output_ports)):
            painter.drawLine(self.width ,do*(i + 1),self.width+ QBlock.PORT_SIZE,do*(i + 1))