#-------------------------------------------------------------------------------
#   PROJECT:   VHDL Code Generator
#   NAME:      Connection
#
#   LICENSE:   GNU-GPL V3
#-------------------------------------------------------------------------------

__author__ = "BlakeTeam"

from lib import *

class Connection:
    def __init__(self, out_block, ind_output, in_block, ind_input, system):
        """ Structure that handles the links between two Blocks(Ports)
            Each Connection has a name(string) that is given by default.

        :Block out_block:   Output block
        :Int ind_output:    Port index in the output block
        :Block in_block:    Input block
        :Int ind_input:     Port index in the input block
        :System system:     Global system where the connection was created
        """
        if  out_block.output_ports[ind_output].size != in_block.input_ports[ind_input].size:
            # The size of both ports must be equal.
            raise InvalidConnection("Size of ports doesn't match")

        self.out_block = out_block
        self.ind_output = ind_output
        self.in_block = in_block
        self.ind_input = ind_input
        self.system = system

        self.size = out_block.output_ports[ind_output].size

        self.name = self.get_name(self)

    def get_name(self):
        """ Return a valid name for the block.
            A name that is not in the list of names in the current system.
        """
        ind = 0
        while True:
            name = "conn" + str(ind)
            if not name in self.conn_name:
                self.conn_name.add(name)
                return name
            else:
                ind += 1

    def setName(self,name):
        """ Set the name of the current connection.
            It is safely change the name using this method.

        :String name:      The new name of this connection.
        """
        # Check that the new name do not already exist
        if name in self.system.conn_name:
            raise ValueError("This name already exist")

        self.system.conn_name.remove(self.name)
        self.system.conn_name.add(name)
        self.name = name

class InvalidConnection(BaseException):
    pass