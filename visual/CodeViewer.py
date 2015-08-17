__author__ = 'FarSeer'

from PyQt4.QtGui import QTextEdit, QDockWidget
from PyQt4.QtCore import Qt
from pygments import highlight
from pygments.lexers import VhdlLexer
from pygments.formatters import HtmlFormatter
#import  webbrowser


CODE_WIDTH = 400

class CodeViewer(QDockWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowTitle("Code")
        self.setMinimumWidth(CODE_WIDTH)
        self.setAllowedAreas(Qt.AllDockWidgetAreas)
        self.textBrowser = QTextEdit(self)
        self.setWidget(self.textBrowser)
        self.lexer = VhdlLexer()
        self.formatter = HtmlFormatter(noclass=True, full=True)

    def showCode(self, code, name):
        html = highlight(code, self.lexer, self.formatter)
        css = self.formatter.get_style_defs(".highlight")

        # header = "<link rel=\"stylesheet\" ref=\"style.css\">\n"
        # h = open(name + ".html", "wt")
        # h.write(header)
        # h.write(html)
        # h.close()
        #
        # c = open("style.css", "wt")
        # c.write(css)
        # c.close()
        #
        # webbrowser.open(name + ".html")

        self.textBrowser.setStyleSheet(css)
        self.textBrowser.setText(html)