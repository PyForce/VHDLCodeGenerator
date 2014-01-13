
# Import REGION
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic

from lib.Block import *

# Change this to True when you want to able the block
__isBlock__ = False

# The name of the dynamic block class
__className__ = "DynamicBlockModel"

# The name of the window to build class
__win__ = "WindowModel"

class DynamicBlockModel(Block):
    """ Dynamic Block Documentation
    """
    def __init__(self,system,*args):
        """

        :param system:  The system where the block is created
        :param args:    All the parameters you need to build the block
        """

        # Set the name of the block here
        # If another block with the same name already exists it will be renamed
        # with the same name and an index at the end. Ex: "BlockName_2"
        name = "BlockName"

        # Array of int that indicates the size of each port in the block
        input_ports = []
        output_ports = []

        # CODE HERE
        # to build the input & output ports

        super().__init__(input_ports,output_ports,system,name)

        # Port has default names. We recommend you to change it.
        # For inputs ports: using self.setInputName(name,index) EX: self.setInputName("MyInputName",0)
        # For outputs ports: using self.setOutputName(name,index) EX: self.setOutputName("MyOutputName",0)

        # Variables declaration
        # If you need to use variables you just need the name and the size in bits
        # Mode: self.addVariable(name,size)  Ex: self.addVariable("MyVar",size)

        # WARNING
        # Variable's name can't be the same than other variables or port name.
        # Variables are going to be used as signals in VHDL


    # This function returns the string were the statements of the block are declared.
    # No need of signal declaration.
    # You have access to name and size of each port and variable using these method:

        # getVariableSignalName(self,index)
        # getOutputSignalName(self,index)
        # getInputSignalName(self,index)

        # getVariableSignalSize(self,index)
        # getOutputSignalSize(self,index)
        # getInputSignalSize(self,index)
    def generate(self):
        return ""

#
class WindowModel(QWidget):
    # QtSignal that will be emitted with a list of parameters to generate a block using the dynamic model
    accept = pyqtSignal(list)

    def __init__(self,parent = None):
        super().__init__()
        # Reference to the path where the .ui that should be loaded is created.
        PATH = "blocks\\DynamicModel\\Model.ui"
        self.ui = uic.loadUi(PATH,self)

    # When the parameters are caught, it should be passed as list in args
    def accepted(self,args):
        self.accept.emit(args)
        self.close()

