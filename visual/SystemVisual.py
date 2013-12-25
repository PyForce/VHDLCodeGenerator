#-------------------------------------------------------------------------------
#   PROJECT:   VHDL Code Generator
#   NAME:      System visual
#
#   LICENSE:   GNU-GPL V3
#-------------------------------------------------------------------------------

__author__ = "BlakeTeam"

from PyQt4.QtCore import *

from data import *
# from data.MainWindow import *

class QSystem(QGraphicsItem):
    COLOR = 0,0,100,100 # Red, Green, Blue, Alpha
    PORTLEN = 20

    def __init__(self, system, parent = None):
        """ QGraphicsItem that represent the system of the current project.
            Each QSystem has an array of input ports, an array of output ports,
            & a rectangle that enclose the area (pure esthetically)
        """
        super().__init__(parent)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setCursor(Qt.OpenHandCursor)
        self.system = system
        self.rect = QRectF(-4*WIDTH/10,-4*HEIGHT/10,4*WIDTH/5,4*HEIGHT/5)

    def boundingRect(self):
        return self.rect.adjusted(-QSystem.PORTLEN-1,1,QSystem.PORTLEN+2,2)

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
        self.system.screenPos = (self.pos().x(), self.pos().y())

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
            line = QLine(-4*WIDTH/10.0 - pl, di*(i + 1) - HEIGHT/2.0, -4*WIDTH/10.0, di*(i + 1) - HEIGHT/2.0)
            painter.drawLine(line)
            print("caca1")

        # Drawing output ports
        for i in range(len(OutputBlock.output_ports)):
            print("caca2")
            painter.drawLine(4*WIDTH/10.0 ,do*(i + 1) - HEIGHT / 2.0, 4*WIDTH/10.0 + pl, do*(i + 1) - HEIGHT / 2.0)