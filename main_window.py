from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout
#from image_panel import ImagePanel
#from info_panel import InfoPanel
#from control_panel import ControlPanel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()


        #Set window properties

        self.setWindowTitle("K Lab Experiment GUI")
        self.setGeometry(100, 100, 800, 600)

        #Initialize main layout container

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)        

        # Instantiate and add each panel to the layout

        
        #self.image_panel = ImagePanel()
        #self.info_panel = InfoPanel()
        #self.control_panel = ControlPanel()
        
        #layout.addWidget(self.image_panel)
        #layout.addWidget(self.info_panel)
        #layout.addWidget(self.control_panel)