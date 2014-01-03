#-------------------------------------------------------------------------------
#   PROJECT:   VHDL Code Generator
#   NAME:      System visual
#
#   LICENSE:   GNU-GPL V3
#-------------------------------------------------------------------------------

__author__ = "BlakeTeam"

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from data import *
from data.MainWindow import *

# Todo: Change system form(paint)
WIDTH = 100
HEIGHT = 50

class QSystem(QGraphicsItem):
    COLOR = 0,200,30,20 # Red, Green, Blue, Alpha
    PORTLEN = 20

    def __init__(self, system, parent = None):
        """ QGraphicsItem that represent the system of the current project.
            Each QSystem has an array of input ports, an array of output ports,
            & a rectangle that enclose the area (pure esthetically)
        """
        super().__init__(parent)
        self.system = system
        self.rect = QRectF(-WIDTH/2.0, -HEIGHT/2.0, WIDTH, HEIGHT)

    def boundingRect(self):
        return self.rect.adjusted(-QSystem.PORTLEN-1,1,QSystem.PORTLEN+2,2)

    def shape(self):
        path = QPainterPath()
        path.addRect(self.rect)
        return path

    def mousePressEvent(self, event):
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)

    def paint(self,painter,styleOptionGraphicsItem,widget):
        InputBlock = self.system.system_input
        OutputBlock = self.system.system_output

        di = HEIGHT/(len(InputBlock.input_ports) + 1)
        do = HEIGHT/(len(OutputBlock.output_ports) + 1)
        pl = QSystem.PORTLEN

        painter.drawRect(self.rect)
        painter.fillRect(self.rect, QColor(*QSystem.COLOR))

        # Drawing input ports

        for i in range(len(InputBlock.input_ports)):
            painter.drawLine(-WIDTH/2.0 - pl, di*(i + 1) - HEIGHT/2.0, -WIDTH/2.0, di*(i + 1) - HEIGHT/2.0)
            if InputBlock.input_ports[i].size > 1:
                painter.drawLine(-WIDTH/2.0 - pl/4.0, di*(i + 1) - HEIGHT/2.0 - di/4.0, -WIDTH/2.0 - 3*pl/4.0, di*(i + 1) - HEIGHT/2.0 + di/4.0)
                #painter.drawRect(-WIDTH/2.0 - pl/4.0, di*(i + 1) - HEIGHT/2.0 - di/2.0,4, 4)
                #painter.drawRect(-WIDTH/2.0 - pl/4.0, di*(i + 1) - HEIGHT/2.0 - 3*di/4.0, -WIDTH/2.0, di*(i + 1) - HEIGHT/2.0 - di/2)
                #painter.drawText(QRectF(-WIDTH/2.0 - pl/4.0, di*(i + 1) - HEIGHT/2.0 - 3*di/4.0, -WIDTH/2.0, di*(i + 1) - HEIGHT/2.0 - di/2), Qt.AlignRight, str(InputBlock.input_ports[i].size))

        # Drawing output ports
        for i in range(len(OutputBlock.output_ports)):
            painter.drawLine(WIDTH/2.0, do*(i + 1) - HEIGHT/2.0, WIDTH/2.0 + pl, do*(i + 1) - HEIGHT/2.0)
            if OutputBlock.output_ports[i].size > 1:
                painter.drawLine(WIDTH/2.0 + 3*pl/4, do*(i + 1) - HEIGHT/2.0 - do/4.0, WIDTH/2.0 + pl/4, do*(i + 1) - HEIGHT/2.0 + do/4.0)
                #painter.drawText(QRectF(), Qt.AlignLeft, str(OutputBlock.output_ports[i].size))