"""Main application function to be called
"""
import sys
import os

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QSplitter

from view import input_view, output_view
import controller.intercontroller_comm as intercontroller_comm

class MainApp(QMainWindow):
    """Primary class, uses QT as a base

    Args:
        QMainWindow (_type_): needed to be a QT application
    """
    def __init__(self):
        super().__init__()

        folder_path = 'temp-images'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            
        self.setWindowTitle("Hydrus Compressor")
        self.setGeometry(1000, 500, 800, 400)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        left_pane = input_view.InputWindow()
        right_pane = output_view.OutputWindow()

        intercontroller_comm.connect_input_output_controllers(
                left_pane.input_controller,
                right_pane.output_controller)

        splitter.addWidget(left_pane)
        splitter.addWidget(right_pane)        
        splitter.setStretchFactor(0, 1) 
        splitter.setStretchFactor(1, 50)  

        self.setCentralWidget(splitter)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
