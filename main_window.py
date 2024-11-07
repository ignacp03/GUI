from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QSizePolicy, QComboBox, QListWidget, QLineEdit, QCompleter, QListView
from PyQt5.QtCore import Qt
import sys
#from image_panel import ImagePanel
#from info_panel import InfoPanel
#from control_panel import ControlPanel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()


        #Set window properties

        self.setWindowTitle("K Lab Experiment GUI")
        self.setGeometry(100, 100, 1500, 800)

        # Create a central widget and set layout
        #central_widget = QWidget()
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.dropdown = QComboBox()
        self.dropdown.setEditable(True)
        options = [f"Option {i}" for i in range(1, 101)]  # 100 options for demonstration
        self.dropdown.addItems(options)
        self.dropdown.textActivated.connect( self.text_changed )
        #a = self.dropdown.currentTextChanged.connect(self.text_changed)

        completer = QCompleter(options, self)
        completer.setFilterMode(Qt.MatchContains)  # Allow matching by any part of the string
        completer.setCaseSensitivity(False)  # Case-insensitive
        self.dropdown.setCompleter(completer)


        list_view = QListView()
        list_view.setMaximumHeight(120)  # Adjust to show only a few items at a time
        self.dropdown.setView(list_view)

        layout.addWidget(self.dropdown)





        # Alignments (optional, adjust as needed)
        #image_label.setAlignment(Qt.AlignCenter)
        #image_label2.setAlignment(Qt.AlignCenter)
        #info_label.setAlignment(Qt.AlignCenter)


    def text_changed(self, s): # s is a str
        print(s)
        return s