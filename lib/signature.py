import data.constants

def signature():
    import random
    authors = "Gustavo Viera López,Danilo Gómez Gómez,Marcelo Fornet Fornés".split(',')

    sign =  "-- Generated with VHDL Code Generator %s.\n"%data.constants.VERSION
    sign += "-- Courtesy of BlakeTeam:\n"
    for i in random.sample(range(3),3):
        sign += "--\t%s\n"%authors[i]
    sign += "---------------------------------:)\n\n"
    return sign