import sys
from PyQt5.QtWidgets import (
    QMainWindow, QApplication,
    QLabel,QStatusBar, QVBoxLayout, QWidget, QHBoxLayout, QGroupBox
)


from Widgets.Toolbar import ToolbarWidget
from PyQt5.QtCore import Qt, QSize
from Widgets.Helpers import Color
from Widgets.ImageVisualization import ImageDisplayWidget


style = """
    background-color: #CED3DC;
    border: 1.5px solid #000000;
    border-radius: 15px;
    padding: 5px;
"""


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()


        ### INITIATE SOME ATRIBUTES ###
        self.running = False
        self.selected_folder = "Default" #! MODIFY WITH THE DEFAULT DIRECTORY #########
        self.meas = "BEC"
        self.mode = "Auto"


        ###############################

        self.setWindowTitle("K Lab Experiment GUI")
        self.setGeometry(100, 100, 1500, 800)
        #label = QLabel("Hello!")
        #label.setAlignment(Qt.AlignCenter)

        widget = Color('#CED3DC')

        

        self.toolbar = ToolbarWidget(self)
        self.addToolBar(self.toolbar)

        self.setStatusBar(QStatusBar(self))
        self.statusBar().showMessage("Application starte. Mode: Auto. Measurement: BEC", 5000)


        RowLayout = QVBoxLayout()
        Column1Layout = QHBoxLayout()
        Column2Layout = QHBoxLayout()

        RowLayout.setContentsMargins(10,10,10,10)
        RowLayout.setSpacing(10)

        Raw_Image_widget = ImageDisplayWidget(title = "Raw Pictures", parent = self)
        #Raw_Image_widget.setStyleSheet(style)
        label12 = QLabel("Atom Number Widget")
        label12.setAlignment(Qt.AlignCenter)
        label12.setStyleSheet(style)

        Column1Layout.addWidget(Raw_Image_widget, stretch = 1)
        Raw_Image_widget.load_image()
        Column1Layout.addWidget(label12, stretch = 1)
        RowLayout.addLayout( Column1Layout, stretch = 2)

        label21 = QLabel("Auxiliar plot (fits)")
        label21.setAlignment(Qt.AlignCenter)
        label21.setStyleSheet(style)
        label22 = QLabel("Dialog Box")
        label22.setAlignment(Qt.AlignCenter)
        label22.setStyleSheet(style)

        Column2Layout.addWidget(label21 , stretch = 1)
        Column2Layout.addWidget(label22, stretch = 1)
        RowLayout.addLayout( Column2Layout,  stretch = 1 )

        #Qw = QWidget(Color('#CED3DC'))
        Qw = QWidget()
        Qw.setLayout(RowLayout)
        Qw.setStyleSheet("background-color: #CED3DC;")

        self.setCentralWidget(Qw)
        self.load_default_settings()


    def load_default_settings(self):
        #Launching with mode auto
        self.toolbar.button_mode_auto.setChecked(True)
        self.toolbar.mode = "auto" 
        
        self.toolbar.button_meas_BEC.setChecked(True)
        self.toolbar.meas = "BEC"

app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()