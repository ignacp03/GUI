import sys
from PyQt5.QtWidgets import (
    QMainWindow, QApplication,
    QLabel,QStatusBar, QVBoxLayout, QWidget
)


from Widgets.Toolbar import ToolbarWidget
from PyQt5.QtCore import Qt, QSize
from Widgets.Helpers import Color



class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("K Lab Experiment GUI")
        self.setGeometry(100, 100, 1500, 800)
        label = QLabel("Hello!")
        label.setAlignment(Qt.AlignCenter)

        

        self.toolbar = ToolbarWidget(self)
        self.addToolBar(self.toolbar)

        self.setStatusBar(QStatusBar(self))


        layout = QVBoxLayout()

        #layout.addWidget(Color('red'))
        #layout.addWidget(Color('green'))
        #layout.addWidget(Color('blue'))

        #widget = QWidget()
        #widget.setLayout(layout)
        self.setCentralWidget(label)

app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()