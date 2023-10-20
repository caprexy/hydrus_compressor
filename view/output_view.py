"""Right panel where the output/found files should be displayed
"""
    
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QScrollArea, QPushButton

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
        self.setLayout(output_layout)

        self.file_grid = QWidget()
        self.grid_layout = QGridLayout()
        self.file_grid.setLayout(self.grid_layout)
        
        file_grid_widget = QScrollArea()
        file_grid_widget.setWidgetResizable(True)
        file_grid_widget.setWidget(self.file_grid)
        output_layout.addWidget(file_grid_widget)
        file_grid_widget.show()
        
        
        compress_button = QPushButton("Compress selected files")
        # compress_button.clicked.connect()
        output_layout.addWidget(compress_button)
        
        self.output_controller = OutputController(
            self.grid_layout
        )
