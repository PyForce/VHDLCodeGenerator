#
#   PROJECT:   VHDL Code Generator
#   NAME:      Class System
#
#   LICENSE:   GNU-GPL V3
#

__author__ = "BlakeTeam"

# TODO: Comment system (Comments & Doc are different things)

from Class import *
from main import *

class System:
    def __init__(self,name,input_vector,output_vector):
        """ Structure that handles an abstract system

        :String name:           Name of the system (Name of the project)
        :Int[] input_vector:    List with the size of the input ports of the system
        :Int[] output_vector:   List with the size of the output ports of the system
        """
        self.name = name        # The name of the system

        self.block_name = set() # The name of all blocks on the system
        self.conn_name = set()  # The name of all connections on the system

        self.block = []
        self.connections = []
        self.system_input = Block((),input_vector,self)
        self.system_input.setName("SystemInput")
        self.system_output = Block(output_vector,(),self)
        self.system_output.setName("SystemOutput")

        self.input_vector = input_vector
        self.input_names = ["in" + str(i) for i in range(len(input_vector))]
        self.output_vector = output_vector
        self.output_names = ["out" + str(i) for i in range(len(output_vector))]

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

    def get_name(self,obj):
        """ Give a valid name for the current object.

        :T obj: (Where T is Connection/Block) is the recommended name by the system
        """
        if isinstance(obj,Block):
            ind = 0
            while True:
                name = "block" + str(ind)
                if not name in self.block_name:
                    self.block_name.add(name)
                    return name
                else:
                    ind += 1
        elif isinstance(obj,Connection):
            ind = 0
            while True:
                name = "conn" + str(ind)
                if not name in self.conn_name:
                    self.conn_name.add(name)
                    return name
                else:
                    ind += 1

    def connect(self,output_block,ind_output,input_block,ind_input):
        """

        :param output_block:
        :param ind_output:
        :param input_block:
        :param ind_input:
        """
        # TODO: Documentation for this function, it is short but UGLY & it is 3:21am
        conn = Connection(output_block,ind_output,input_block,ind_input,self)
        output_block.output_ports[ind_output].connection.append(conn)
        input_block.input_ports[ind_input] = conn
        self.connections.append(conn)