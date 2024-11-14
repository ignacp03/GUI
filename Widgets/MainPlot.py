from PyQt5.QtWidgets import QWidget, QVBoxLayout, QComboBox, QLabel, QHBoxLayout, QSpacerItem, QCompleter, QSizePolicy, QLineEdit, QPushButton, QMessageBox
import matplotlib.pyplot as plt
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from numpy import arange, array, std
from collections import defaultdict


class MainPlot(QWidget):
    def __init__(self, title="Main Plot", parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)

        #Create the main layout
        layout = QVBoxLayout()
        self.figure, self.ax = plt.subplots(figsize=(6*1.5, 4*1.5), facecolor='#CED3DC')
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas, stretch = 3)
       


        # Group by
        Control_layout = QHBoxLayout()
        Control_layout.setSpacing(0)
        Control_layout.setAlignment(Qt.AlignCenter)

        GroupBy_label = QLabel("Group by:")
        GroupBy_label.setFixedWidth(60)
        Control_layout.addWidget(GroupBy_label)
        self.selectParam_combo = QComboBox(self)
        self.selectParam_combo.setFixedWidth(250)
        self.selectParam_combo.setFixedHeight(25)
        self.selectParam_combo.setStyleSheet("QComboBox { background-color: #FCF7F8; }")
        self.selectParam_combo.textActivated.connect(self.GroupBy)
        Control_layout.addWidget(self.selectParam_combo)

        spacer1 = QSpacerItem(30, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        Control_layout.addItem(spacer1)

        ## Select Plot
        selectPlot = QLabel("Plot:")
        Control_layout.addWidget(selectPlot)
        selectPlot.setFixedWidth(30)

        self.selectPlot_combo = QComboBox(self)
        self.selectPlot_combo.setFixedWidth(150)
        self.selectPlot_combo.setFixedHeight(25)
        self.selectPlot_combo.addItems(['Fitted Atom Number', 'Integrated Atom Number'])
        self.selectPlot_combo.setStyleSheet("QComboBox { background-color: #FCF7F8; }")
        self.selectPlot_combo.textActivated.connect(self.selectPlot)
        Control_layout.addWidget(self.selectPlot_combo)

        spacer2 = QSpacerItem(30, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        Control_layout.addItem(spacer2)

        ## Select scale
        selectScale = QLabel("Unit:")
        Control_layout.addWidget(selectScale)
        selectScale.setFixedWidth(30)

        self.selectScale_combo = QComboBox(self)
        self.selectScale_combo.setFixedWidth(40)
        self.selectScale_combo.addItems(["#", "k", "M"])
        self.selectScale_combo.setStyleSheet("QComboBox { background-color: #FCF7F8; }")
        self.selectScale_combo.textActivated.connect(self.selectScale)
        Control_layout.addWidget(self.selectScale_combo)

        layout.addLayout(Control_layout)


        ##Control 2
        Control_layout2 = QHBoxLayout()
        Control_layout2.setSpacing(0)
        Control_layout2.setAlignment(Qt.AlignCenter)
        spacer_width = 20


        ### YMIN
        Ymin_label = QLabel("Ymin:")
        Ymin_label.setFixedWidth(35)
        Control_layout2.addWidget(Ymin_label)

        self.ymin_Line =  QLineEdit()
        self.ymin_Line.setStyleSheet("QLineEdit { background-color: #FCF7F8; }")
        self.ymin_Line.setFixedWidth(50)
        Control_layout2.addWidget(self.ymin_Line)

        spacer3 = QSpacerItem(spacer_width, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        Control_layout2.addItem(spacer3)     

        ### YMAX
        Ymax_label = QLabel("Ymax:")
        Ymax_label.setFixedWidth(35)
        Control_layout2.addWidget(Ymax_label)

        self.ymax_Line =  QLineEdit()
        self.ymax_Line.setStyleSheet("QLineEdit { background-color: #FCF7F8; }")
        self.ymax_Line.setFixedWidth(50)
        Control_layout2.addWidget(self.ymax_Line)


        spacer4 = QSpacerItem(spacer_width, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        Control_layout2.addItem(spacer4)


        ### XMin
        Xmin_label = QLabel("Xmin:")
        Xmin_label.setFixedWidth(35)
        Control_layout2.addWidget(Xmin_label)

        self.xmin_Line =  QLineEdit()
        self.xmin_Line.setStyleSheet("QLineEdit { background-color: #FCF7F8; }")
        self.xmin_Line.setFixedWidth(50)
        Control_layout2.addWidget(self.xmin_Line)

        spacer5 = QSpacerItem(spacer_width, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        Control_layout2.addItem(spacer5)

        ### XMAX
        Xmax_label = QLabel("Xmax:")
        Xmax_label.setFixedWidth(35)
        Control_layout2.addWidget(Xmax_label)

        self.xmax_Line =  QLineEdit()
        self.xmax_Line.setStyleSheet("QLineEdit { background-color: #FCF7F8; }")
        self.xmax_Line.setFixedWidth(50)
        Control_layout2.addWidget(self.xmax_Line)

        spacer6 = QSpacerItem(spacer_width, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        Control_layout2.addItem(spacer6)


        ### Save Limits
        self.save_button = QPushButton("Save limits")
        self.save_button.setFixedWidth(60)
        self.save_button.clicked.connect(self.saveButton)
        Control_layout2.addWidget(self.save_button)

        spacer7 = QSpacerItem(spacer_width, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        Control_layout2.addItem(spacer7)

        ### Standard deviation display
        self.stdLabel = QLabel("Std: --")
        self.stdLabel.setFixedWidth(100)
        Control_layout2.addWidget(self.stdLabel)


        layout.addLayout(Control_layout2)

        self.setLayout(layout)


    def saveButton(self):
        xMax = self.xmax_Line.text()
        xMin = self.xmin_Line.text()
        yMax = self.ymax_Line.text()
        yMin = self.ymin_Line.text()

        self.ax.autoscale() #Resetting axis

        if xMax: xMax = float(xMax)
        else: 
            xMax = self.ax.get_xlim()[-1]

        if xMin: xMin = float(xMin)
        else: xMin = self.ax.get_xlim()[0]

        if yMax: yMax = float(yMax)
        else: yMax = self.ax.get_ylim()[-1]

        if yMin: yMin = float(yMin)
        else: yMin = self.ax.get_ylim()[0]


        try: 
            self.ax.set_ylim([yMin, yMax])
            self.ax.set_xlim([xMin, xMax])
            self.canvas.draw()

        except Exception as e:
            QMessageBox.information(self, "Invalid Limits", "Please select valid limits.\nError details: " + str(e))


    def selectScale(self):
        self.make_plot()

    def selectPlot(self):
        self.make_plot()

    def load_plot(self): 
        main_window = self.get_main_window()  # Get the MainWindow instance

    
        if main_window is None:
            raise RuntimeError("Main window not found in parent hierarchy.")
        
        data = main_window.data
        self.IntAtomNum = []
        self.FitAtomNum = []
        self.variables = []
        for image in data:
            if image["fitStatus"] == 0:
                self.FitAtomNum.append(image["Results"]['Fitted Atom Number'])
                self.IntAtomNum.append(image["Results"]['Integrated Atom Number'])
                self.variables.append(image["Variables"])
        self.make_plot()
        

    def make_plot(self):
        Param = self.selectParam_combo.currentText()
        Plot = self.selectPlot_combo.currentText()
        units = self.selectScale_combo.currentText()
        if units == "#": unit = 1
        elif units == "k": unit = 1000
        elif units == "M": unit = 1e6

        try: #Checks whether there is already data processed
            if Plot == 'Fitted Atom Number':
                y = self.FitAtomNum
            elif Plot == 'Integrated Atom Number':
                y = self.IntAtomNum
        except:
            return 0 #Returns 0 if there is no data yet
        
        
        if Param == "Iteration":  #If no parameter it displays the iteration
            x = arange(0,len(self.IntAtomNum))
            std_y = std(array(y)/unit)
            self.ax.clear()
            self.ax.plot(x, array(y)/unit, 'o--', color = 'steelblue')  
            self.ax.set_xlabel("Iteration")
            self.ax.set_ylabel(Plot+" ["+units+"]")
            self.ax.grid(True)
            self.canvas.draw()
            self.stdLabel.setText(f"Std: {round(std_y, 2)}")

        elif Param in self.variables[-1]: #If parameter selected 
            grouped_data = defaultdict(list)
            for value, param_dict in zip(y, self.variables):
                if Param in param_dict:
                    grouped_data[param_dict[Param]].append(value)
            
            averages = []
            stds = []
            for item in grouped_data.items():
                averages.append(sum(item[-1])/ len(item[-1]))
                stds.append(std(item[-1]))
            x = list(grouped_data.keys())
            self.ax.clear()
            self.ax.errorbar(x, array(averages)/unit, array(stds)/unit, fmt = 'o--', color = 'steelblue',capsize=3, capthick=1.5, ecolor="#799fbf")
            self.ax.set_xlabel(Param)
            self.ax.set_ylabel(Plot+" ["+units+"]")
            self.ax.grid(True)
            self.canvas.draw()
            self.stdLabel.setText("Std: --")


        
    def UpdateGroupBy(self):
        """Updates the Group By content"""
        main_window = self.get_main_window()  # Get the MainWindow instance
    
        if main_window is None:
            raise RuntimeError("Main window not found in parent hierarchy.")
        variables = main_window.varyingVariables ###! For list of all variables. sorted(list(data["Variables"].keys()))
        self.varyingVariables = variables.copy()
        self.selectParam_combo.clear() #Clears previous options
        self.selectParam_combo.addItems(variables+["Iteration"]) #Add new options
        self.selectParam_combo.setEditable(True)
        completer = QCompleter(variables+["Iteration"], self) #Set a completer to allow searching a specific parameter
        completer.setCaseSensitivity(False) 
        self.selectParam_combo.setCompleter(completer)


    def UpdateGroup(self):
        self.load_plot()

    def GroupBy(self):
        self.load_plot()


    def get_main_window(self):
        parent = self.parent()
        while parent is not None:
            # Check the type name without direct import
            if type(parent).__name__ == 'MainWindow':
                return parent
            parent = parent.parent()
        return None
    
    