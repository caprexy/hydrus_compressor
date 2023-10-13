
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QSplitter, QWidget, QVBoxLayout, QLineEdit, QListWidget, QPushButton
from PyQt6.QtWidgets import QLabel, QApplication, QMainWindow, QPushButton, QDialog, QVBoxLayout

import controller.input_controller as input_controller

class InputWindow(QWidget):
    output_window = None
    def __init__(self):
        super().__init__()
        
        input_layout = QVBoxLayout()
        self.setLayout(input_layout)

        
        self.input_box = QLineEdit()
        add_button = QPushButton("Add Item")

        add_button.clicked.connect(self.add_item)

        input_layout.addWidget(self.input_box)
        input_layout.addWidget(add_button)
        
        config_button = QPushButton("Open config")
        config_button.clicked.connect(input_controller.open_config_menu)
        input_layout.addWidget(config_button)
    
    def add_item(self):
        text = self.input_box.text()
        if text:
            self.output_window.addItem(text)
            self.input_box.clear()

    def pass_output_window(self, output_window: QWidget):
        self.output_window = output_window