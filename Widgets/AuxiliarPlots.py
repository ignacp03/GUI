from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QSpacerItem, QSizePolicy, QCheckBox
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np


class AuxPlots(QWidget):
    def __init__(self, title="Aux Plot", parent=None):
        super().__init__(parent)

        self.CustomVariables = []

        self.setWindowTitle(title)
        self.mainWindow = self.get_main_window()


        layout = QVBoxLayout()
        self.figure, self.ax = plt.subplots(figsize=(6*1.5, 4), facecolor='#CED3DC')
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas, stretch = 3)


        ### Control Layout
        Control_layout = QHBoxLayout()
        Control_layout.setSpacing(0)
        Control_layout.setAlignment(Qt.AlignLeft)
        spacer_width = 20

        ### Plot Selection
        Plot_label = QLabel("Plot selection:")
        Plot_label.setFixedWidth(80)
        Control_layout.addWidget(Plot_label)
        self.plot_combo = QComboBox(self)
        self.plot_combo.setFixedWidth(150)
        self.plot_combo.setFixedHeight(25)
        self.plot_combo.setStyleSheet("QComboBox { background-color: #FCF7F8; }")
        self.plot_combo.addItems(["Fit", "Center of the cloud", "Temperature", "Custom"])
        self.plot_combo.textActivated.connect(self.selectPlot)
        Control_layout.addWidget(self.plot_combo)

        spacer1 = QSpacerItem(spacer_width, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        Control_layout.addItem(spacer1)

        ### Custom plot X
        CustomPlotX_label = QLabel("X-axis")
        CustomPlotX_label.setFixedWidth(40)
        Control_layout.addWidget(CustomPlotX_label)

        self.CustomPlotX_combo = QComboBox(self)
        self.CustomPlotX_combo.setFixedWidth(150)
        self.CustomPlotX_combo.setFixedHeight(25)
        self.CustomPlotX_combo.setStyleSheet("QComboBox { background-color: #FCF7F8; }")
        self.CustomPlotX_combo.setEnabled(False)
        Control_layout.addWidget(self.CustomPlotX_combo)

        spacer2 = QSpacerItem(spacer_width, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        Control_layout.addItem(spacer2)

        ### Custom plot Y
        CustomPlotY_label = QLabel("Y-axis")
        CustomPlotY_label.setFixedWidth(40)
        Control_layout.addWidget(CustomPlotY_label)

        self.CustomPlotY_combo = QComboBox(self)
        self.CustomPlotY_combo.setFixedWidth(150)
        self.CustomPlotY_combo.setFixedHeight(25)
        self.CustomPlotY_combo.setStyleSheet("QComboBox { background-color: #FCF7F8; }")
        self.CustomPlotY_combo.setEnabled(False)
        Control_layout.addWidget(self.CustomPlotY_combo)

        spacer3 = QSpacerItem(spacer_width, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        Control_layout.addItem(spacer3)


        ###Custom plot load

        self.CustomPlot_button = QPushButton("Plot")
        self.CustomPlot_button.setFixedWidth(60)
        self.CustomPlot_button.clicked.connect(self.CustomPlot)
        self.CustomPlot_button.setEnabled(False)
        Control_layout.addWidget(self.CustomPlot_button)

        spacer4 = QSpacerItem(spacer_width, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        Control_layout.addItem(spacer4)

        #### Checkbox Show x

        ShowX_label = QLabel("Display X")
        ShowX_label.setFixedWidth(50)
        Control_layout.addWidget(ShowX_label)

        self.ShowX_box = QCheckBox()
        self.ShowX_box.setCheckState(True)
        self.ShowX_box.stateChanged.connect(self.selectPlot)
        self.ShowX_box.setTristate(False)
        Control_layout.addWidget(self.ShowX_box)

        spacer5 = QSpacerItem(spacer_width, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        Control_layout.addItem(spacer5)

        #### Checkbox Show x

        ShowY_label = QLabel("Display Y")
        ShowY_label.setFixedWidth(50)
        Control_layout.addWidget(ShowY_label)

        self.ShowY_box = QCheckBox()
        self.ShowY_box.setCheckState(True)
        self.ShowY_box.stateChanged.connect(self.selectPlot)
        self.ShowY_box.setTristate(False)
        Control_layout.addWidget(self.ShowY_box)

        layout.addLayout(Control_layout)

        self.setLayout(layout)





    def selectPlot(self):
        plot = self.plot_combo.currentText()
        if plot == "Custom":
            self.CustomPlotX_combo.setEnabled(True)
            self.CustomPlotY_combo.setEnabled(True)
            self.CustomPlot_button.setEnabled(True)
        else:
            self.CustomPlotX_combo.setEnabled(False)
            self.CustomPlotY_combo.setEnabled(False)
            self.CustomPlot_button.setEnabled(False)
            if plot == "Fit":
                self.PlotFit()
            elif plot == "Center of the cloud":
                self.PlotCenter()
            elif plot == "Temperature":
                self.PlotTemperature()


    def PlotFit(self):
        """Displays the fit of the last image"""
        if self.mainWindow.data == None:
            return 0
        image = self.mainWindow.data[-1]
        center = image["Other"]["New Center"]
        fittedImage = image["Fitted_Image"]
        RoiImage = image["ROI"]
        #Cut ROI slice
        xROI = RoiImage[center[1], :]
        yROI = RoiImage[:, center[0]]
        #Cut Fit slice
        xFit = fittedImage[center[1], :]
        yFit = fittedImage[:, center[0]]

        self.ax.clear()
        if self.ShowX_box.checkState() == 2:
            self.ax.plot(xROI/np.max(xROI), 'o', color = 'steelblue', zorder = 2, label = "Raw along X")
            self.ax.plot(xFit/np.max(xROI), '--', color = 'lightblue', zorder = 1, label = "Fit along X")
        
        if self.ShowY_box.checkState() == 2:
            self.ax.plot(yROI/np.max(yROI), 'o', color = 'darkorange', zorder = 2, label = "Raw along Y")
            self.ax.plot(yFit/np.max(yROI), '--', color = 'navajowhite', zorder = 1, label = "Fit along Y")
        
        self.ax.set_xlabel("Pixel")
        self.ax.set_ylabel("Normalized intensity")
        self.ax.legend()
        self.canvas.draw()


    def PlotCenter(self):
        "Displays the center of the cloud"
        if self.mainWindow.data == None:
            return 0
        centersX= []
        centersY = []
        for image in self.mainWindow.data:
            centersX.append(image["Other"]["Center"][0])
            centersY.append(image["Other"]["Center"][1])
        
        self.ax.clear()
        if self.ShowX_box.checkState() == 2:
            self.ax.plot(centersX, 'o', color = 'steelblue', zorder = 2, label = "Center X")
        
        if self.ShowY_box.checkState() == 2:
            self.ax.plot(centersY, 'o', color = 'darkorange', zorder = 2, label = "Center Y")
        
        self.ax.set_xlabel("Iteration")
        self.ax.set_ylabel("Position of the center [pixel]")
        self.ax.legend()
        self.canvas.draw()

    def PlotTemperature(self):
        self.ax.clear()
        if self.mainWindow.data == None:
            return 0
        Temperature = [image["Results"]["Temperature"]*1e6 for image in self.mainWindow.data]
        self.ax.plot(Temperature, 'o', color = 'steelblue', zorder = 2)
        self.ax.set_xlabel("Iteration")
        self.ax.set_ylabel("Temperature [uK]")
        self.canvas.draw()


    def get_main_window(self):
        parent = self.parent()
        while parent is not None:
            # Check the type name without direct import
            if type(parent).__name__ == 'MainWindow':
                return parent
            parent = parent.parent()
        return None
    

    def CustomPlot(self):

        x = None
        y = None
        if self.mainWindow.data == None:
            return 0
        xlabel = self.CustomPlotX_combo.currentText() 
        ylabel = self.CustomPlotX_combo.currentText() 

        if xlabel[:-2] == "Center":
            if xlabel[-1] =="x":
                x = [image["Other"]["Center"][0] for image in self.mainWindow.data if image["fitStatus"] == 0]
            elif xlabel[-1] == "y":
                x = [image["Other"]["Center"][1] for image in self.mainWindow.data if image["fitStatus"] == 0]

        if ylabel[:-2] == "Center":
            if ylabel[-1] == "x":
                y = [image["Other"]["Center"][0] for image in self.mainWindow.data if image["fitStatus"] == 0]
            if ylabel[-1] == "y":
                y = [image["Other"]["Center"][1] for image in self.mainWindow.data if image["fitStatus"] == 0]

        if xlabel in ["Temperature", "Fitted Atom Number", "Integrated Atom Number"]:
            x = [image["Results"][xlabel] for image in self.mainWindow.data if image["fitStatus"] == 0]
        if ylabel in ["Temperature", "Fitted Atom Number", "Integrated Atom Number"]:
            y = [image["Results"][ylabel] for image in self.mainWindow.data if image["fitStatus"] == 0]

        if xlabel in self.CustomVariables:
            x = [image["Variables"][xlabel] for image in self.mainWindow.data if image["fitStatus"] == 0]

        if ylabel in self.CustomVariables:
            y = [image["Variables"][ylabel] for image in self.mainWindow.data if image["fitStatus"] == 0]

        if xlabel == "":
            xtot = sum(1 for image in self.mainWindow.data if image["fitStatus"]==0)
            x = np.arange(xtot)
            xlabel = "Iteration"

        if ylabel == "":
            ytot = sum(1 for image in self.mainWindow.data if image["fitStatus"]==0)
            y = np.arange(ytot)
            ylabel = "Iteration"
        self.ax.clear()
        if x is not None and y is not None: 
            self.ax.plot(x,y, 'o', color = 'steelblue', zorder = 2)
            self.ax.set_xlabel(xlabel)
            self.ax.set_ylabel(ylabel)
        else: 
            print("Plot could not be displayed")
        self.canvas.draw()
        


    def UpdateCustomPlot(self):
        """Updates the X and Y custom plot data"""
        data = self.mainWindow.data[-1]
        other = ["", "Center x","Center y", "Temperature", "Fitted Atom Number", "Integrated Atom Number"]
        variables = sorted(list(data["Variables"].keys()))
        self.CustomVariables = variables

        self.CustomPlotX_combo.clear() #Clears previous options
        self.CustomPlotX_combo.addItems(other+variables) #Add new options
        self.CustomPlotX_combo.setEditable(True)

        self.CustomPlotY_combo.clear() #Clears previous options
        self.CustomPlotY_combo.addItems(other+variables) #Add new options
        self.CustomPlotY_combo.setEditable(True)




    