#-------------------------------------------------------------------------------
#   PROJECT:   VHDL Code Generator
#   NAME:      main
#
#   LICENSE:   GNU-GPL V3
#-------------------------------------------------------------------------------

# .vcgp -> VHDL Code Generator Project

__author__ = "BlakeTeam"

import sys
import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *

data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))
lib_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'lib'))
visual_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'visual'))

sys.path.append(lib_dir)
sys.path.append(visual_dir)
sys.path.append(data_dir)

from MainWindow import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()

    window.showMaximized()
    sys.exit(app.exec_())

# TODO: ->	Guardar y cargar proyectos
# TODO: ->	Incluir los labels necesarios a los bloques para mostrar su información
# TODO: ->	Hacer el parametrizador y habilitar los bloques paramétricos
# TODO: ->	Hacer el guardador de bloques estáticos (exportar)
# TODO: ->  Prohibir el uso de "__" en los nombres de bloques y puertos y sistemas