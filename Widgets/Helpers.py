from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPalette, QColor



class Color(QWidget):

    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.window, QColor(color))
        self.setPalette(palette)