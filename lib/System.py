#-------------------------------------------------------------------------------
#   PROJECT:   VHDL Code Generator
#   NAME:      System
#
#   LICENSE:   GNU-GPL V3
#-------------------------------------------------------------------------------

__author__ = "BlakeTeam"

def signature():
    import random
    authors = "Gustavo Viera López,Danilo Gómez Gómez,Marcelo Fornet Fornés".split(',')
    sign =  "-- This code was automatically generated using VHDL Code Generator.\n"
    sign += "-- Courtesy of BlakeTeam:\n"
    for i in random.sample(range(3),3):
        sign += "--\t%s\n"%authors[i]
    sign += "--\tManuel Madrigal Casals\n"
    sign += "--\tCesar Hernández Hernández\n"
    sign += "---------------------------------:)\n\n"
    return sign

print(signature())

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
        self.connections = {}   # Connection dictionary of the system <Abstract Connection: QGraphicsLineItem>
        self.system_input = _Block((),[size for name,size in input_info],self)
        # Setting names to input ports
        for i in range(len(input_info)):
            self.system_input.output_ports[i].name = input_info[i][0]

        self.system_input.screenPos = (-50,0)
        self.system_input.setName("SystemInput")
        self.system_output = _Block([size for name,size in output_info],(),self)

        # Setting names to input ports
        for i in range(len(output_info)):
            self.system_output.input_ports[i].name = output_info[i][0]

        self.system_output.screenPos = (50,0)
        self.system_output.setName("SystemOutput")

        self.input_info = input_info
        self.output_info = output_info
        self.input_names = [name for name,size in input_info]
        self.output_names = [name for name,size in output_info]
        self.includedLibrary = ["IEEE.std_logic_1164.all"]

    def buildVHDLCode(self):
        """ Building the code that will be generated.
        """
        fileText = signature()

        # Including libraries
        fileText += "-- Including libraries\nlibrary IEEE;\n"

        for i in self.includedLibrary:
            fileText += "use %s;\n"%i

        fileText += "\n"
        fileText += "entity %s is\n"%self.name

        fileText += "-- Generating ports\n"
        fileText += "port (\n"

        # Generating input ports
        for i in self.system_input.output_ports:
            fileText += "%s : in std_logic%s;\n"%(i.name,"" if i.size == 1 else "_vector(%d downto 0)"%(i.size - 1))

        # Generating output ports
        for i in self.system_output.input_ports:
            fileText += "%s : out std_logic%s;\n"%(i.name,"" if i.size == 1 else "_vector(%d downto 0)"%(i.size - 1))

        fileText = fileText[:-2]
        fileText += ");\n"
        fileText += "end %s;\n"%self.name

        # Architecture Implementation
        fileText += "\n-- Architecture Implementation\n"
        fileText += "architecture Arq_%s of %s is\n"%(self.name,self.name)
        fileText += "begin\n"

        # Port declaration
        fileText += "-- Port declaration\n"

        # TODO: Overrated RAM
        for i in self.block:
            fileText += "\n-- Declaring %s ports & temporary signals\n"%(i.name)
            signals = i.getSignals()
            inputSig = []
            outputSig = []
            tempSig = []
            for name,size,mode in signals:
                if mode == IN:
                    inputSig.append((name,size))
                elif mode == OUT:
                    outputSig.append((name,size))
                else:
                    tempSig.append((name,size))

            fileText += "-- Input ports\n"
            for name,size in inputSig:
                fileText += "signal %s__%s : std_logic%s;\n"%(i.name, name,"" if size == 1 else "_vector(%d downto 0)"%(size - 1))

            fileText += "\n-- Output ports\n"
            for name,size in outputSig:
                fileText += "signal %s__%s : std_logic%s;\n"%(i.name, name,"" if size == 1 else "_vector(%d downto 0)"%(size - 1))

            fileText += "\n-- Temporary signals\n"
            for name,size in tempSig:
                fileText += "signal %s__%s : std_logic%s;\n"%(i.name, name,"" if size == 1 else "_vector(%d downto 0)"%(size - 1))

        # Defining connections
        fileText += "\n-- Defining connections\n"

        for i in self.block:
            for port_inp in i.input_ports:
                receiver = i.name + "__" + port_inp.name
                if self.system_input == port_inp.connection.out_block:
                    sender = port_inp.connection.out_block.output_ports[port_inp.connection.ind_output].name
                else:
                    sender = port_inp.connection.out_block.name + "__" + port_inp.connection.out_block.output_ports[port_inp.connection.ind_output].name
                fileText += "%s <= %s;\n"%(receiver, sender)
            fileText += "\n"

        # Block implementations
        fileText += "\n-- Blocks implementation\n"

        for i in self.block:
            fileText += "-- Implementation of %s block\n"%i.name
            fileText += i.generate()
            fileText += "\n"

        # Connecting outputs
        fileText += "-- Connecting outputs\n"
        for i in self.system_output.input_ports:
            fileText += "%s <= %s__%s;\n"%(i.name,i.connection.out_block.name,i.connection.out_block.output_ports[i.connection.ind_output].name)

        fileText += "end Arq_%s;\n"%self.name

        # print("\nGENERATED CODE\n")
        # print(fileText)
        return fileText


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

    def connect(self,output_block,ind_output,input_block,ind_input,visualConnection = None):
        """
        :param output_block:
        :param ind_output:
        :param input_block:
        :param ind_input:
        """
        conn = _Connection(output_block,ind_output,input_block,ind_input,self)  # Creating the connection between 2 blocks
        output_block.output_ports[ind_output].connection.append(conn)  # Linking the connection with the output block
        input_block.input_ports[ind_input].connection = conn           # Linking the connection with the input block
        self.connections.update({conn:visualConnection})   # Adding the connection to the connection list (on the system)
        return conn