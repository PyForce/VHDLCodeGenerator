#
#   PROJECT:   VHDL Code Generator
#   NAME:      main
#
#   DATE: 12/10/13
#   TIME: 19:12 PM
#

# TODO: FIX IMPORTS
# TODO: Change default templates. Remove Date&Time and Add License&Authors(BlakeTeam)

import sys
from Class import *
from Visual import *

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()
    sys.exit(app.exec_())