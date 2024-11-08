import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from main_window import MainWindow

def main():
    #Creation of the application object
    app = QApplication(sys.argv)

    # Instantiate and show the main window
    MW = MainWindow()
    MW.show()
    # Execute the application's main loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()