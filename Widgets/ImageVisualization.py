from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QSizePolicy, QSpacerItem,QLineEdit
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtCore import Qt, pyqtSignal
from processing.SaverLoader import LoadData

from os.path import join

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
from os.path import basename

class ImageDisplayWidget(QWidget):
    def __init__(self, title="Image Display", parent=None):
        super().__init__(parent)


        self.setWindowTitle(title)
  
        #Create the main layout

        layout = QVBoxLayout()
        # Create title label
        #title_label = QLabel(title)
        #title_label.setAlignment(Qt.AlignCenter)
        #layout.addWidget(title_label)

        layout_plot = QHBoxLayout()
        layout_plot.setContentsMargins(0, 0, 0, 0)
        layout_plot.setSpacing(0)
        self.figure, self.ax = plt.subplots(figsize=(6*1.5, 4*1.5), facecolor='#CED3DC') 
        self.canvas = FigureCanvas(self.figure)
        layout_plot.addWidget(self.canvas, stretch = 3)

        layout_results = QVBoxLayout()
        self.IAN_label = QLabel("Integrated #Atom: ")
        layout_results.addWidget(self.IAN_label)
        self.FAN_label = QLabel("Fitted #Atom: ")
        layout_results.addWidget(self.FAN_label)
        self.Temp_label = QLabel("Temperature: ")
        layout_results.addWidget(self.Temp_label)

        layout_plot.addLayout(layout_results)

        layout.addLayout(layout_plot, stretch=1)



        # Add controls for colormap, normalization, etc.
        control_layout = QHBoxLayout()
        control_layout.setContentsMargins(0, 0, 0, 0) 
        control_layout.setSpacing(0)
        control_layout.setAlignment(Qt.AlignLeft)

        # Colormap selection (ComboBox)
        self.colormap_combo = QComboBox(self)
        self.colormap_combo.setFixedWidth(80)
        self.colormap_combo.setStyleSheet("QComboBox { background-color: #FCF7F8; }")
        self.colormap_combo.addItems(["Blues", "Greys", "coolwarm", "cool", "viridis"])
        self.colormap_combo.textActivated.connect(self.UpdateColorMap)
        colormap_label = QLabel("Colormap:")
        colormap_label.setFixedWidth(65)
        control_layout.addWidget(colormap_label)
        control_layout.addWidget(self.colormap_combo)

        spacer1 = QSpacerItem(30, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        control_layout.addItem(spacer1)

        # Normalization 
        self.norm_Line =  QLineEdit()
        self.norm_Line.setStyleSheet("QLineEdit { background-color: #FCF7F8; }")
        self.norm_Line.setFixedWidth(80)
        self.norm_Line.setMaxLength(3)
        self.norm_Line.setText("30")  # Default normalization value
        norm_label = QLabel("Normalization:")
        norm_label.setFixedWidth(80)
        control_layout.addWidget(norm_label)
        control_layout.addWidget(self.norm_Line)
        self.norm_Line.returnPressed.connect(self.UpdateNorm)


        spacer2 = QSpacerItem(30, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        control_layout.addItem(spacer2)

        # Select image
        
        selectImage_label = QLabel("Image:")
        selectImage_label.setFixedWidth(50)
        control_layout.addWidget(selectImage_label)
        self.selectImage_combo = QComboBox(self)
        self.selectImage_combo.setFixedWidth(80)
        self.selectImage_combo.setStyleSheet("QComboBox { background-color: #FCF7F8; }")
        self.selectImage_combo.addItems(["ROI","Atoms", "Dark", "Bright", "OD"])
        self.selectImage_combo.textActivated.connect(self.UpdateDisplayedImage)

        control_layout.addWidget(self.selectImage_combo)

        layout.addLayout(control_layout)

        self.setLayout(layout)

    def load_image(self): 
        # Load the image and display it

        main_window = self.get_main_window()  # Get the MainWindow instance
    
        if main_window is None:
            raise RuntimeError("Main window not found in parent hierarchy.")
        
        
        data = main_window.data

        imageSelected = self.selectImage_combo.currentText()
        if imageSelected == "Atoms":
            image_path = data[-1]["Paths"]["Atoms"]
            image = plt.imread(image_path)
            self.figure.suptitle(basename(image_path))
            
        elif imageSelected == "Bright":
            image_path = data[-1]["Paths"]["Bright"]
            image = plt.imread(image_path)
            self.figure.suptitle(basename(image_path))
        elif imageSelected == "Dark":
            image_path = data[-1]["Paths"]["Dark"]
            image = plt.imread(image_path)
            self.figure.suptitle(basename(image_path))
        elif imageSelected == "OD":
            image = data[-1]["Other"]["OpDen"]
            self.figure.suptitle("Optical Density")

        elif imageSelected == "ROI":
            image = data[-1]["ROI"]
            self.figure.suptitle("Optical Density")

        self.ax.clear()
        IAN = data[-1]["Results"]["Integrated Atom Number"]
        FAN = data[-1]["Results"]["Fitted Atom Number"]
        Temp = data[-1]["Results"]["Temperature"]
        colormap = self.colormap_combo.currentText()
        norm_value = float(self.norm_Line.text())/1000

        self.ax.imshow(image/np.max(image), cmap=colormap, vmin = 0, vmax = norm_value)

        if main_window.meas == "MagTrap" or main_window .meas == "HybridTrap":
            self.IAN_label.setText(f"Integrated #Atom: {np.round(IAN/1e6,3)} million.")
            self.FAN_label.setText(f"Fitted #Atom: {np.round(FAN/1e6,3)} million.")
            self.Temp_label.setText(f"Temperature: {np.round(Temp*1e6,3)} uK.")
        elif main_window.meas == "BEC":
            self.IAN_label.setText(f"Integrated #Atom: {np.round(IAN/1e3,3)} k.")
            self.FAN_label.setText(f"Fitted #Atom: {np.round(FAN/1e3,3)} k.")
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.canvas.draw()



    def UpdateColorMap(self, cmap):
        self.load_image()

    def UpdateNorm(self):
        self.load_image()

    def UpdateDisplayedImage(self):
        self.load_image()

    def get_main_window(self):
        parent = self.parent()
        while parent is not None:
            # Check the type name without direct import
            if type(parent).__name__ == 'MainWindow':
                return parent
            parent = parent.parent()
        return None