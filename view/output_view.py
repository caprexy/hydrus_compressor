"""Right panel where the output/found files should be displayed
"""
    
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton

# import controller.output_controller as output_controller

class OutputWindow(QWidget):
    """Primary class for the right panel

    Args:
        QWidget (_type_): For qwidget import, standard
    """
    input_window = None

    def __init__(self):
        super().__init__()
        
        output_layout = QVBoxLayout()
        self.output_list = QListWidget()

        self.setLayout(output_layout)

        output_layout.addWidget(self.output_list)

        
        compress_button = QPushButton("Compress selected files")
        # compress_button.clicked.connect()
        output_layout.addWidget(compress_button)
