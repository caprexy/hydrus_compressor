"""Right panel where the output/found files should be displayed
"""
    
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QPushButton

from controller.output_controller import OutputController

class OutputWindow(QWidget):
    """Primary class for the right panel

    Args:
        QWidget (_type_): For qwidget import, standard
    """
    input_window = None
    output_controller = None
    table = None

    def __init__(self):
        super().__init__()
        
        
        output_layout = QVBoxLayout()
        self.file_table = QTableWidget()

        self.setLayout(output_layout)

        output_layout.addWidget(self.file_table)

        
        compress_button = QPushButton("Compress selected files")
        # compress_button.clicked.connect()
        output_layout.addWidget(compress_button)
        
        self.output_controller = OutputController(
            self.file_table
        )
