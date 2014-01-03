import data.constants

def signature():
    import random
    authors = "Gustavo Viera López,Danilo Gómez Gómez,Marcelo Fornet Fornés".split(',')

    sign =  "-- This code was automatically generated using VHDL Code Generator %s.\n"%data.constants.VERSION
    sign += "-- Courtesy of BlakeTeam:\n"
    for i in random.sample(range(3),3):
        sign += "--\t%s\n"%authors[i]
    sign += "--\tManuel Madrigal Casals\n"
    sign += "--\tCesar Hernández Hernández\n"
    sign += "---------------------------------:)\n\n"
    return sign