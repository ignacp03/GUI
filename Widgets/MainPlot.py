from PyQt5.QtWidgets import QWidget, QVBoxLayout, QComboBox, QLabel, QHBoxLayout, QSpacerItem, QCompleter, QSizePolicy
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
        Control_layout.setAlignment(Qt.AlignLeft)

        GroupBy_label = QLabel("Group by:")
        GroupBy_label.setFixedWidth(60)
        Control_layout.addWidget(GroupBy_label)
        self.selectParam_combo = QComboBox(self)
        self.selectParam_combo.setFixedWidth(250)
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

        self.setLayout(layout)

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
        
        if Param == "":  #If no parameter it displays the iteration
            x = arange(0,len(self.IntAtomNum))
            self.ax.clear()
            self.ax.plot(x, array(y)/unit, 'o--', color = 'steelblue')  
            self.ax.set_xlabel("Iteration")
            self.ax.set_ylabel(Plot+" ["+units+"]")
            self.ax.grid(True)
            self.canvas.draw()
            #! Display the std somewhere

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


        
    def UpdateGroupBy(self):
        """Updates the Group By content"""
        main_window = self.get_main_window()  # Get the MainWindow instance
    
        if main_window is None:
            raise RuntimeError("Main window not found in parent hierarchy.")
        data = main_window.data[-1]
        variables = sorted(list(data["Variables"].keys()))
        self.selectParam_combo.clear() #Clears previous options
        self.selectParam_combo.addItems([""]+variables) #Add new options
        self.selectParam_combo.setEditable(True)
        completer = QCompleter(variables, self) #Set a completer to allow searching a specific parameter
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