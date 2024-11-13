from PyQt5.QtWidgets import QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
import datetime


class ConsoleWidget(QTextEdit):
    append_text_signal = pyqtSignal(str)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setStyleSheet("background-color: black; color: white;")
        self.append_text_signal.connect(self.write)
        self.current_message = ""
        self.current_index = 0
        self.typing_timer = QTimer(self)
        self.typing_timer.timeout.connect(self._type_next_character)

    def write(self, message):
        if message.strip():
            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.current_message = f"[{date}] {message.strip()}"
            self.current_index = 0
            self.typing_timer.start(15)  # Adjust the interval for typing speed (milliseconds)

    def _type_next_character(self):
        if self.current_index < len(self.current_message):
            self.moveCursor(self.textCursor().End)
            self.insertPlainText(self.current_message[self.current_index])
            self.current_index += 1
        else:
            self.typing_timer.stop()
            self.append("")  # Move to a new line after completing the message

    def flush(self):
        pass


class WorkerThread(QThread):
    text_to_print = pyqtSignal(str)

    def run(self):
        # Simulate background work
        import time
        self.text_to_print.emit(f"GUI succesfully launched!")