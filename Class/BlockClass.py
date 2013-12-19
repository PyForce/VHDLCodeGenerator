#
#   PROJECT:   VHDL Code Generator
#   NAME:      Class Blocks
#
#   DATE: 12/10/13
#   TIME: 5:33 PM
#

from Class import *

class Block:
    def __init__(self, input_vector, output_vector, system):
        self.input_ports = [Port("in"+str(i),input_vector[i],IN) for i in range(len(input_vector))]
        self.output_ports = [Port("out"+str(i),output_vector[i],OUT) for i in range(len(output_vector))]

        self.system = system
        self.name = system.get_name(self)

    def __getitem__(self, name):
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
        self.system.block_name.remove(self.name)
        self.system.block_name.add(name)
        self.name = name

class Port:
    def __init__(self,name,size,mode):
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


def main():
    a = BlockClass((2,8),(1,2),None)
    print(a["in0"])

if __name__ == "__main__":
    main()