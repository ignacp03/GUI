import sys
from PyQt5.QtWidgets import (
    QMainWindow, QApplication,
    QLabel,QStatusBar, QVBoxLayout, QWidget, QHBoxLayout, QGroupBox
)

from os.path import basename, dirname, join
from time import sleep
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from Widgets.Toolbar import ToolbarWidget
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from Widgets.Helpers import Color
from Widgets.ImageVisualization import ImageDisplayWidget
from Widgets.MainPlot import MainPlot

from processing.Watcher import ImageSetHandler
from processing.SaverLoader import LoadData


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
        self.data = None
        self.defaultFolder = "\\\\files.ad.icfo.net\\groups\\QGE\\Potassium\\Personal folders\\Ignacio\\code\\GUI" #! MODIFY WITH THE DEFAULT DIRECTORY WITH ALL PLOTS #########
        self.selected_file = None
        self.meas = "BEC"
        self.mode = "Auto"
        self.magnification = 1.2
        self.DataFileName = "processedData.pkl"
        self.file_watcher = FileWatcher(self.defaultFolder, self.DataFileName)
        self.file_watcher.path_changed.connect(self.update_gui)
        self.analysisWatcher = AnalysisWatcher(self.defaultFolder, self.meas, self.magnification)
        
        




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

        self.Raw_Image_widget = ImageDisplayWidget(title = "Raw Pictures", parent = self)
        #Raw_Image_widget.setStyleSheet(style)

        self.MainPlot_widget = MainPlot(title= "Main Plot", parent = self)
        #self.MainPlot_widget.setStyleSheet(style)

        Column1Layout.addWidget(self.Raw_Image_widget, stretch = 1)
        #self.Raw_Image_widget.load_image()
        
        Column1Layout.addWidget(self.MainPlot_widget, stretch = 1)#! Dis-comment
        #self.MainPlot_widget.load_plot()#! Dis-comment
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
        self.analysisWatcher.start()


    def load_default_settings(self):
        #Launching with mode auto
        self.toolbar.button_mode_auto.setChecked(True)
        self.toolbar.mode = "auto" 
        
        self.toolbar.button_meas_BEC.setChecked(True)
        self.toolbar.meas = "BEC"

    def update_gui(self, new_path):
        """Slot to handle updated gui."""
        self.data = LoadData(new_path) 
        if new_path != self.selected_file:
            self.selected_file = new_path
            print(f"Updated path to: {self.selected_file}")
            self.MainPlot_widget.UpdateGroupBy()
        self.Raw_Image_widget.load_image()
        self.MainPlot_widget.load_plot()

    
    def closeEvent(self, event):
        """Ensure the file watcher stops when the application closes."""
        if self.running:
            self.file_watcher.stop()
        self.analysisWatcher.stop()

        super().closeEvent(event)



class FileWatcherHandler(FileSystemEventHandler):
    """A handler for monitoring file system changes."""
    def __init__(self, signal, file_name):
        super().__init__()
        self.signal = signal
        self.file_name = file_name

    def on_created(self, event):
        if not event.is_directory and basename(event.src_path) == "processedData.pkl":
            print(f"Creation detected: {event.src_path}")
            self.signal.emit(event.src_path)
            sleep(1)

    def on_modified(self, event):
        """Called when a file or directory is modified."""
        if not event.is_directory and basename(event.src_path) == self.file_name:
            print(f"Modification detected: {event.src_path}")
            self.signal.emit(event.src_path)
            sleep(1)

class FileWatcher(QThread):
    path_changed = pyqtSignal(str)

    def __init__(self, directory_to_watch, file_name):
        super().__init__()
        self.directory_to_watch = directory_to_watch
        self.file_name = file_name
        self.event_handler = FileWatcherHandler(self.path_changed, self.file_name)


    def run(self):
        print("Data loader watcher started")
        self.observer = Observer()
        self.observer.schedule(self.event_handler, self.directory_to_watch, recursive=True)
        self.observer.start()
        self.exec_()


    def stop(self):
        print("Data loader watcher stopped")
        if self.observer:
            self.observer.stop()
            self.observer.join()

class AnalysisWatcher(QThread):
    def __init__(self, directory_to_watch,meas, magnification):
        super().__init__()
        self.directory_to_watch = directory_to_watch
        self.meas = meas
        self.magnification = magnification 
            
    def run(self):
        print("Analysis observer start")
        self.event_SetHandler = ImageSetHandler(self.directory_to_watch, self.meas, self.magnification)
        self.observer_run_SetHandler = Observer()
        self.observer_run_SetHandler.schedule(self.event_SetHandler, self.directory_to_watch, recursive=True)
        self.observer_run_SetHandler.start()
        self.exec_()

    def stop(self):
        if self.observer_run_SetHandler:
            print("Stopping Analysis observer")
            self.observer_run_SetHandler.stop()
            self.observer_run_SetHandler.join()





app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()