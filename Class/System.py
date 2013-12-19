#
#   PROJECT:   VHDL Code Generator
#   NAME:      Class System
#
#   DATE: 12/10/13
#   TIME: 5:18 PM
#

from Class import *

class System:
    def __init__(self,name,input_vector,output_vector):
        self.name = name

        self.block_name = set()
        self.conn_name = set()

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
        conn = Connection(output_block,ind_output,input_block,ind_input,self)
        output_block.output_ports[ind_output].connection.append(conn)
        input_block.input_ports[ind_input] = conn
        self.connections.append(conn)

def tester():
    # s = object.__new__(System)
    # s.name = "mySystem"
    # s.input_vector = (1,8)
    # s.output_vector = (2,2,3)

    s = System("mySystem",(1,8),(2,2,3))
    b1 = Block((4,),(2,2),s)
    b2 = Block((2,),(4,2),s)

    s.connect(b1,1,b2,0)


if __name__ == "__main__":
    tester()