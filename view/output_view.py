
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QSplitter, QWidget, QVBoxLayout, QLineEdit, QListWidget, QPushButton

class OutputWindow(QWidget):
    input_window = None

    def __init__(self):
        super().__init__()
        
        output_layout = QVBoxLayout()
        self.output_list = QListWidget()

        self.setLayout(output_layout)

        output_layout.addWidget(self.output_list)
