#
#   PROJECT:   VHDL Code Generator
#   NAME:      Class Blocks
#
#   LICENSE:   GNU-GPL V3
#

__author__ = "BlakeTeam"

from Class import *
from main import *

class Block:
    def __init__(self, input_vector, output_vector, system):
        """ Structure that handles an abstract Block.
            Each block has a name(string) that is given by default for the system.

        :Int[] input_vector:      Size of the inner ports of the block.
        :Int[] output_vector:     Size of the outer ports of the block.
        :System system:           Reference to the system where this block belong.
        """
        # Comprehension list that generates list of ports initialized by default
        self.input_ports = [Port("in"+str(i),input_vector[i],IN) for i in range(len(input_vector))]
        self.output_ports = [Port("out"+str(i),output_vector[i],OUT) for i in range(len(output_vector))]

        self.system = system
        self.name = system.get_name(self)

    def __getitem__(self, name):
        """ Find a port for his name.
            This function starts for input ports.
            If the port exist it returns the reference to the port & mode(IN/OUT)
            Else it returns -1

        :String name: The name of the wanted port/
        """
        try:
            pos = self.input_ports.index(name)
            return pos,IN
        except ValueError:
            try:
                pos = self.output_ports.index(name)
                return pos,OUT
            except ValueError:
                return -1

    def setName(self,name):
        """ Set the name of the current block.
            It is safely change the name using this method.

        :String name:      The new name of this block.
        """
        # TODO: Validate the new name (there is no another object with the same name) in the system.
        self.system.block_name.remove(self.name)
        self.system.block_name.add(name)
        self.name = name

class Port:
    def __init__(self,name,size,mode):
        """ Structure that handles an abstract port.
            Each Port has a connection property,
            If the mode is IN:
                connection property is a reference to other port of mode OUT.
            If the mode is OUT:
                connection property is an array of Ports of mode IN.
            connection is the one who keep the links between blocks.

        :String name:   Name of the port.
        :Int size:      The total of bits that the port handles.
        :IN/OUT mode:   Mode of the port.
        """
        self.name = name
        self.size = size
        self.mode = mode

        if self.mode == IN:
            self.connection = None
        else:
            self.connection = []

    def __eq__(self, other):
        if isinstance(other,str):
            return other == self.name