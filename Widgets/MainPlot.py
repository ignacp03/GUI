from PyQt5.QtWidgets import QWidget, QVBoxLayout, QComboBox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from processing.SaverLoader import LoadData

class MainPlot(QWidget):
    def __init__(self, title="Main Plot", parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        #Create the main layout

        layout = QVBoxLayout()
        self.figure, self.ax = plt.subplots(figsize=(6*1.5, 4*1.5), facecolor='#CED3DC')
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas, stretch = 3)


        ##Plot control layout

        self.Group_combo = QComboBox(self)
        self.Group_combo.setFixedWidth(80)
        self.Group_combo.setStyleSheet("QComboBox { background-color: #FCF7F8; }")
        self.Group_combo.addItems(["None"])
        self.Group_combo.textActivated.connect(self.UpdateGroup)



    def get_main_window(self):
        parent = self.parent()
        while parent is not None:
            # Check the type name without direct import
            if type(parent).__name__ == 'MainWindow':
                return parent
            parent = parent.parent()
        return None
    
    def load_plot(self, folder_path = ""): ###! REMOVE =""
        main_window = self.get_main_window()  # Get the MainWindow instance
    
        if main_window is None:
            raise RuntimeError("Main window not found in parent hierarchy.")
        
        data = LoadData(folder_path)
        

    def UpdateGroup(self):
        self.load_plot()
