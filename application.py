"""Main application function to be called
"""
import sys
import os
import copy
from PyQt6.QtGui import QCloseEvent

from PyQt6.QtCore import Qt, QByteArray, pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow, QSplitter, QFrame,QSizePolicy

from view import input_view, output_view
import controller.intercontroller_comm as intercontroller_comm
import models.settings as settings

class MainApp(QMainWindow):
    """Primary class, uses QT as a base

    Args:
        QMainWindow (_type_): needed to be a QT application
    """
    app_closing = pyqtSignal()
    
    def __init__(self):
        super().__init__()

        # random startup stuff
        folder_path = 'temp-images'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)    
        settings.read_user_json()
        self.setWindowTitle("Hydrus Compressor")
        self.restoreGeometry(settings.get_main_window_geometry())
        
        # build primary splitter and it's widgets
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.main_splitter = main_splitter
        self.setCentralWidget(main_splitter)
        
        # set up panes
        input_pane = input_view.InputWindow()
        output_pane = output_view.OutputWindow()
        intercontroller_comm.connect_input_output(
                input_pane.input_controller,
                output_pane.output_controller,
                output_pane.file_grid_view)
        # letting the sub widgets know we are closing
        self.app_closing.connect(input_pane.close_save)
        self.app_closing.connect(output_pane.close_save)

        # add widgets to splitter and position if needed
        main_splitter.addWidget(input_pane)
        main_splitter.addWidget(output_pane)   
        if settings.get_input_window_geometry() is None:
            main_splitter.setStretchFactor(0, 1) 
            main_splitter.setStretchFactor(1, 50)  
        else:
            input_pane.restoreGeometry(settings.get_input_window_geometry())
            output_pane.restoreGeometry(settings.get_output_window_geometry())
            
            
        # build frame for the widget
        separator_frame = QFrame()
        separator_frame.setFrameShape(QFrame.Shape.VLine) 
        separator_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum) 
        separator_frame.setFixedWidth(1)
        main_splitter.insertWidget(1, separator_frame)
        
    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.app_closing.emit()
        super().closeEvent(a0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
