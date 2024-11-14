from PyQt5.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QLineEdit
import datetime

class ConsoleWidget2(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setStyleSheet("background-color: black; color: white;")

    def write(self, message):
        # Check if the message is only a newline or empty string
        if message.strip():
            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            message = f"[{date}] {message.strip()}"
            self.append(message)

    def flush(self):
        pass



class ConsoleWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
            
        # Layout to hold the text display and input line
        layout = QVBoxLayout()
        layout.setSpacing(0)
            
        # Console display area
        self.console_output = QTextEdit()
        self.console_output.setReadOnly(True)
        self.console_output.setStyleSheet("background-color: black; color: white; font-size: 12px; line-height: 2")
            
        # Input line for user interaction
        self.console_input = QLineEdit()
        self.console_input.setStyleSheet("background-color: black; color: white; font-size: 12px")
        self.console_input.setText(">>")
        self.console_input.returnPressed.connect(self.handle_input)

        # Add widgets to the layout
        layout.addWidget(self.console_output)
        layout.addWidget(self.console_input)
            
        # Set layout to the main widget
        self.setLayout(layout)

    def write(self, message, color="white", strip = True):
        if strip is True:
            if message.strip():
                date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                formatted_message = f'<span style="color:{color};">[{date}] {message.strip()}</span>'
                self.console_output.append(formatted_message)
        elif strip is False:
            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            formatted_message = f'<span style="color:{color};">[{date}] {message}</span>'
            self.console_output.append(formatted_message)

    def flush(self):
        pass
        
    def handle_input(self):
        # Get input from the console input line
        user_input = self.console_input.text().strip()
            
        # Display the input as if it was a command entered
        
        self.write(f"{user_input}", color="green")
        
            
        # Clear the input line after pressing enter
        self.console_input.clear()
        self.console_input.setText(">>")
        user_input = user_input[2:]
        if user_input.lower() == "help":
            self.write("Available commands:\n - help: Show available commands\n - clear: Clear the console", strip = False)
        elif user_input.lower() == "clear":
            self.console_output.clear()
        else:
            self.write("Unknown command. Type 'help' for a list of available commands.")

            ####### Add more usefull commands
