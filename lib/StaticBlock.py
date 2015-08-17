#
#   PROJECT:   VHDL Code Generator
#   NAME:      Static blocks
#

import lib.Block
import data.constants
import pickle

class StaticBlock(lib.Block):
    def __init__(self,name,signals,code,system = None):
        self.input_signals   =  [signal[1] for signal in signals if signal[2] == data.constants.IN]
        self.output_signals  =  [signal[1] for signal in signals if signal[2] == data.constants.OUT]

        self.variables = [(signal[0],signal[1],2) for signal in signals]
        self.code = code
        self.name = name
        super().__init__(self.input_signals,self.output_signals,system,name)

    def generate(self):
        return self.code%{"name":self.name}

    @staticmethod
    def load(path):
        file = open(path,"rb")
        arguments = pickle.load(file)
        file.close()
        return arguments

    @staticmethod
    def save(name,signals,code):
        file = open("blocks\\My Static Blocks\\" + name + ".svb","wb")
        pickle.dump((name, signals,code),file)
        file.close()
