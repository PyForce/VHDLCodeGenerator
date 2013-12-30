#-------------------------------------------------------------------------------
#   PROJECT:   VHDL Code Generator
#   NAME:      System
#
#   LICENSE:   GNU-GPL V3
#-------------------------------------------------------------------------------

__author__ = "BlakeTeam"

# from lib import *
from .Block import Block as _Block
from lib.Connection import Connection as _Connection

IN = 1
OUT = 0

class System:
    def __init__(self,name,input_info,output_info):
        """ Structure that handles an abstract system

        :String name:           Name of the system (Name of the project)
        :Int[] input_info:      List with the name & size of the input ports of the system
        :Int[] output_info:     List with the name & size of the output ports of the system
        """
        self.name = name        # The name of the system

        self.block_name = set() # The name of all blocks on the system
        self.conn_name = set()  # The name of all connections on the system

        self.block = []         # Block list of the system
        self.connections = []   # Connection list of the system
        self.system_input = _Block([size for name,size in input_info],(),self)
        self.system_input.setName("SystemInput")
        self.system_output = _Block((),[size for name,size in output_info],self)
        self.system_output.setName("SystemOutput")

        self.input_info = input_info
        self.output_info = output_info
        self.input_names = [name for name,size in input_info]
        self.output_names = [name for name,size in output_info]
        self.includedLibrary = ["IEEE.std_logic_1164.all"]

    def buildVHDLCode(self):
        """ Building the code that will be generated.
        """
        fileText = """
        library IEEE;
        """
        # Including libraries
        fileText += "-- Including libraries"
        for i in self.includedLibrary:
            fileText += "use %s;\n"%i

        fileText += "\n"
        fileText += "entity %s is\n"%self.name





    def __getitem__(self, name):
        """ Find a port for his name.
            This function starts for input ports.
            If the port exist it returns the reference to the port & mode(IN/OUT)
            Else it returns -1

        :String name: The name of the wanted port/
        """
        try:
            pos = self.input_names.index(name)
            return pos,IN
        except ValueError:
            try:
                pos = self.output_names.index(name)
                return pos,OUT
            except ValueError:
                return -1

    def connect(self,output_block,ind_output,input_block,ind_input):
        """
        :param output_block:
        :param ind_output:
        :param input_block:
        :param ind_input:
        """
        conn = _Connection(output_block,ind_output,input_block,ind_input,self)  # Creating the connection between 2 blocks
        output_block.output_ports[ind_output].connection.append(conn)  # Linking the connection with the output block
        input_block.input_ports[ind_input] = conn                      # Linking the connection with the input block
        self.connections.append(conn)   # Adding the connection to the connection list (on the system)