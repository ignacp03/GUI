from PyQt5.QtWidgets import QToolBar, QAction, QFileDialog, QMessageBox, QMenu, QToolButton, QActionGroup
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt


class ToolbarWidget(QToolBar):
    def __init__(self, parent=None):
        super().__init__("Toolbar", parent)
 

        button_play = QAction(QIcon("images\\control.png"),"Run", self)
        button_play.setStatusTip("Run watcher")
        button_play.triggered.connect(self.RunWatcher)
        self.addAction(button_play)

        self.addSeparator()

        button_pause = QAction(QIcon("images\\control-pause.png"), "Pause", self)
        button_pause.setStatusTip("Pause watcher")
        button_pause.triggered.connect(self.StopWatcher)
        self.addAction(button_pause)

        self.addSeparator()

        button_folder = QAction(QIcon("images\\folder.png"), "Open Path", self)
        button_folder.triggered.connect(self.OpenFolder)
        self.addAction(button_folder)

        self.addSeparator()
        
        """
        ### MENU MODE ###
        """

        self.menu_button = QToolButton(self)
        self.menu_button.setIcon(QIcon("images\\dashboard.png"))
        self.menu_button.setText("Mode")
        #self.menu_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.menu_button.setPopupMode(QToolButton.InstantPopup)

        self.menu_mode = QMenu(self.menu_button)

        #Define action group
        action_group_mode = QActionGroup(self)
        action_group_mode.setExclusive(True)

        ## Define mode auto
        self.button_mode_auto = QAction(QIcon("images\\arrow-circle-double.png"), "Auto", self)
        self.button_mode_auto.triggered.connect(lambda: self.mode_auto_triggered("Mode Auto"))
        self.button_mode_auto.setCheckable(True) 
        action_group_mode.addAction(self.button_mode_auto)
        self.menu_mode.addAction(self.button_mode_auto)

        ##Define measurement
        self.button_mode_analysis = QAction(QIcon("images\\drive.png"), "Analysis", self) 
        self.button_mode_analysis.triggered.connect(lambda: self.mode_analysis_triggered("Mode Analysis"))
        self.button_mode_analysis.setCheckable(True) 
        action_group_mode.addAction(self.button_mode_analysis)
        self.menu_mode.addAction(self.button_mode_analysis)


        self.menu_button.setMenu(self.menu_mode)
        self.addWidget(self.menu_button)

        """
        MENU Measurement
        """

        self.menu_button_meas = QToolButton(self)
        self.menu_button_meas.setIcon(QIcon("images\\dashboard.png"))
        self.menu_button_meas.setText("Measurement")
        #self.menu_button_meas.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.menu_button_meas.setPopupMode(QToolButton.InstantPopup)


        self.menu_meas = QMenu(self.menu_button_meas)

        #Define action group
        action_group_meas = QActionGroup(self)
        action_group_meas.setExclusive(True)


        ## Define meas MagTrap
        self.button_meas_MagTrap = QAction(QIcon("images\\magnet.png"), "MagTrap", self)
        self.button_meas_MagTrap.triggered.connect(lambda: self.meas_MagTrap_triggered("MagTrap"))
        self.button_meas_MagTrap.setCheckable(True) 
        action_group_meas.addAction(self.button_meas_MagTrap)
        self.menu_meas.addAction(self.button_meas_MagTrap)


        ## Define meas HybridTrap
        self.button_meas_HybridTrap = QAction(QIcon("images\\arrow-circle-double.png"), "HybridTrap", self)
        self.button_meas_HybridTrap.triggered.connect(lambda: self.meas_HybridTrap_triggered("HybridTrap"))
        self.button_meas_HybridTrap.setCheckable(True) 
        action_group_meas.addAction(self.button_meas_HybridTrap)
        self.menu_meas.addAction(self.button_meas_HybridTrap)

        ## Define meas BEC
        self.button_meas_BEC = QAction(QIcon("images\\asterisk.png"), "BEC", self)
        self.button_meas_BEC.triggered.connect(lambda: self.meas_BEC_triggered("BEC"))
        self.button_meas_BEC.setCheckable(True) 
        action_group_meas.addAction(self.button_meas_BEC)
        self.menu_meas.addAction(self.button_meas_BEC)

        self.menu_button_meas.setMenu(self.menu_meas)
        self.addWidget(self.menu_button_meas)





        
    def mode_auto_triggered(self, option_name):
        QMessageBox.information(self, "Menu Action Triggered", f"You selected: {option_name}")
        self.mode = "Auto"

    def mode_analysis_triggered(self, option_name):
        QMessageBox.information(self, "Menu Action Triggered", f"You selected: {option_name}")
        self.mode = "Analysis"


    def RunWatcher(self, s):
        print("Running Watcher")

    def StopWatcher(self,s):
        print("Watcher Stopped")

    def OpenFolder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder", "")
        
        if folder_path:  # Check if a folder was selected
            QMessageBox.information(self, "Folder Selected", f"Selected Folder: {folder_path}")
            # You can add any logic here to use the selected folder path, e.g., processing files
            self.selected_folder = folder_path  # Store the path in an instance variable for later use
            if self.parent():
                self.parent().selected_folder = folder_path
        else:
            QMessageBox.warning(self, "No Folder Selected", "Please select a folder.")

    def meas_MagTrap_triggered(self, option_name):
        QMessageBox.information(self, "Menu Action Triggered", f"You selected: {option_name}")
        self.meas = "MagTrap"

    def meas_HybridTrap_triggered(self, option_name):
        QMessageBox.information(self, "Menu Action Triggered", f"You selected: {option_name}")
        self.meas = "HybridTrap"

    def meas_BEC_triggered(self, option_name):
        QMessageBox.information(self, "Menu Action Triggered", f"You selected: {option_name}")
        self.meas = "BEC"