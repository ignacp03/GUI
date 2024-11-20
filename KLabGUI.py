import sys
from os.path import basename, dirname, abspath
from os import chdir
from time import sleep, time

from PyQt5.QtWidgets import (
    QMainWindow, QApplication,QStatusBar, QVBoxLayout, QWidget, QHBoxLayout, QMessageBox 
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal, QThread

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from Widgets.Toolbar import ToolbarWidget
from Widgets.Helpers import Color
from Widgets.ImageVisualization import ImageDisplayWidget
from Widgets.MainPlot import MainPlot
from Widgets.LogConsole import ConsoleWidget
from Widgets.AuxiliarPlots import AuxPlots

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
        self.defaultFolder = "\\\\files.ad.icfo.net\\groups\\QGE\\Potassium\\Personal folders\\Ignacio\\code\\GUI" #! MODIFY WITH THE DEFAULT DIRECTORY WITH ALL PLOTS #########

        self.running = False
        self.data = None
        self.selected_file = None
        self.meas = "BEC"
        self.pixelSize = 7.5e-6
        self.mode = "Auto"
        self.magnification = 1.2
        self.DataFileName = "processedData.db"
        self.file_watcher = FileWatcher(self.defaultFolder, self.DataFileName)
        self.file_watcher.path_changed.connect(self.update_gui)
        self.analysisWatcher = AnalysisWatcher(self.defaultFolder,self.DataFileName,  self.meas, self.magnification, self.pixelSize)
        self.varyingVariables = []
        self.console = ConsoleWidget()




        ###############################

        self.setWindowTitle("K Lab Experiment GUI")
        self.setGeometry(100, 100, 1500, 800)  
        self.setWindowIcon(QIcon(r"images\\icon.ico"))      

        self.toolbar = ToolbarWidget(self)
        self.addToolBar(self.toolbar)

        self.setStatusBar(QStatusBar(self))
        self.statusBar().showMessage("Application started. Mode: Auto. Measurement: BEC", 5000)

        ### Set two top widgets ###

        RowLayout = QVBoxLayout()
        Column1Layout = QHBoxLayout()
        Column2Layout = QHBoxLayout()

        RowLayout.setContentsMargins(10,10,10,10)
        RowLayout.setSpacing(10)

        self.Raw_Image_widget = ImageDisplayWidget(title = "Raw Pictures", parent = self)
        self.MainPlot_widget = MainPlot(title= "Main Plot", parent = self)

        Column1Layout.addWidget(self.Raw_Image_widget, stretch = 1)
        Column1Layout.addWidget(self.MainPlot_widget, stretch = 1)
        RowLayout.addLayout( Column1Layout, stretch = 2)

        #### Set tow bottom widgets ###

        self.AuxPLot_Widget = AuxPlots(title= "Auxiliar Plots", parent = self)

        Column2Layout.addWidget(self.AuxPLot_Widget , stretch = 1)
        Column2Layout.addWidget(self.console, stretch = 1)
        RowLayout.addLayout( Column2Layout,  stretch = 1 )

        # Redirect stdout to the console widget
        sys.stdout = self.console
        Qw = QWidget()


        Qw.setLayout(RowLayout)
        Qw.setStyleSheet("background-color: #CED3DC;")

        self.setCentralWidget(Qw)
        self.load_default_settings()
        self.analysisWatcher.start()
        self.showMaximized()
        print("GUI ready")


    def load_default_settings(self):
        #Launching with mode auto and BEC
        self.toolbar.button_mode_auto.setChecked(True)
        self.toolbar.mode = "auto" 
        
        self.toolbar.button_meas_BEC.setChecked(True)
        self.toolbar.meas = "BEC"

    def update_gui(self, new_path, openFolder = False):
        """Slot to Update gui."""
        try:
            self.data = LoadData(new_path, load_all=True) #Loads all the existent data
            #Here the function is prepared for loading the whole set only when a new folder is found.
            #However, we sometimes send new sequences with the same name than previous, being therefore stored 
            #in the same folder. Then, to always have the latest data, we opted for loading all the data.

            if new_path != self.selected_file: #checks if the path is new
                self.selected_file = new_path #Saves new path
                print(f"Updated path to: {self.selected_file}")
                print("Loading plots")
                self.varyingVariables = [] #Reset the varying parameter
                self.MainPlot_widget.UpdateGroupBy() 
                self.AuxPLot_Widget.UpdateCustomPlot()

            if openFolder:
                self.varyingVariables = []
                self.setVaryingVariables2()
            else:
                self.setVaryingVariables()

            self.Raw_Image_widget.load_image()
            print("Last shot displayed")
            self.MainPlot_widget.load_plot()
            print("Atom Number plot updated")
            self.AuxPLot_Widget.selectPlot()
            print("Auxiliar plot displayed")
            sleep(1)

        except Exception as e:
            QMessageBox.information(self, "Couldn't load data", "\nError details: " + str(e))



    def setVaryingVariables(self):
        """Find the varying variables of the last shot compared to the one before"""
        if len(self.data)<2:
            changedVariables = []
        else: 
            changedVariables = [variable for variable in self.data[-1]["Variables"] if variable in self.data[-2]["Variables"] 
                            and self.data[-1]["Variables"][variable] != self.data[-2]["Variables"][variable]]
        if 'CreationTime' in changedVariables:
            changedVariables.remove('CreationTime')
        for changedVariable in changedVariables:
            if changedVariable not in self.varyingVariables:
                 self.varyingVariables.append(changedVariable)
        self.MainPlot_widget.UpdateGroupBy()
        self.AuxPLot_Widget.UpdateCustomPlot()

    def setVaryingVariables2(self):
        """Find the varying variables of the last shot compared to the one before"""
        for index in range(len(self.data)-1): #for every image saved
            for variable in self.data[index]["Variables"]: #we check every variable
                if variable in self.data[index+1]["Variables"] and self.data[index]["Variables"][variable] != self.data[index+1]["Variables"][variable]: #and if it is different than the next image
                    if variable not in self.varyingVariables: #and is not aleady stored
                        self.varyingVariables.append(variable) #store it
        
        if 'CreationTime' in self.varyingVariables:
            self.varyingVariables.remove('CreationTime') #Delete Creation Time
        self.MainPlot_widget.UpdateGroupBy()
        self.AuxPLot_Widget.UpdateCustomPlot()

    
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
        self.last_event_time = 0 
        self.debounce_interval = 10



    def _should_emit_signal(self):
        """Check if enough time has passed since the last signal."""
        ## Windows sends several modification signals for the same file. 
        ## Therefore, we keep the first and block the rest. 
        current_time = time()
        if current_time - self.last_event_time > self.debounce_interval:
            self.last_event_time = current_time
            return True
        return False

    def on_created(self, event):
        if not event.is_directory and basename(event.src_path) == self.file_name:
            sleep(1.5)
            if self._should_emit_signal():
                self.signal.emit(event.src_path)
    def on_modified(self, event):
        """Called when a file or directory is modified."""
        if not event.is_directory and basename(event.src_path) == self.file_name:
            sleep(1.5)
            if self._should_emit_signal():
                self.signal.emit(event.src_path)

class FileWatcher(QThread):
    path_changed = pyqtSignal(str)

    def __init__(self, directory_to_watch, file_name):
        super().__init__()
        self.directory_to_watch = directory_to_watch
        self.file_name = file_name
        self.event_handler = FileWatcherHandler(self.path_changed, self.file_name)
        self.observer = Observer(timeout=5) 
        self.running = False

    def run(self):
        print("Data loader watcher started")
        self.observer = Observer(timeout=5) 
        self.observer.schedule(self.event_handler, self.directory_to_watch, recursive=True)
        self.observer.start()
        self.running = True
        self.exec_()


    def stop(self):
        print("Data loader watcher stopped")
        
        if self.observer:
            self.observer.stop()
            self.running = False
            self.observer.join()

class AnalysisWatcher(QThread):
    def __init__(self, directory_to_watch,saveFile, meas, magnification, pixelSize = None):
        super().__init__()
        self.directory_to_watch = directory_to_watch
        self.savefile = saveFile
        self.meas = meas
        self.magnification = magnification 
        self.pixelSize = pixelSize
            
    def run(self):
        print("Analysis observer started")
        self.event_SetHandler = ImageSetHandler(self.directory_to_watch,self.savefile,self.meas, self.magnification, self.pixelSize)
        self.observer_run_SetHandler = Observer()
        self.observer_run_SetHandler.schedule(self.event_SetHandler, self.directory_to_watch, recursive=True)
        self.observer_run_SetHandler.start()
        self.exec_()

    def stop(self):
        if self.observer_run_SetHandler:
            print("Stopping Analysis observer")
            self.observer_run_SetHandler.stop()
            self.observer_run_SetHandler.join()

    def log_message(self, message):
        print(message)




if __name__=="__main__":
    chdir(dirname(abspath(sys.argv[0])))
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(r"images\\icon.ico"))
    w = MainWindow()
    w.show()
    app.exec()