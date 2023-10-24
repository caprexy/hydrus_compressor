"""Right panel where the output/found files should be displayed
"""
    
from PyQt6.QtWidgets import QSizePolicy, QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene, QPushButton, QGraphicsRectItem
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush, QColor
from controller.output_controller import OutputController

from widgets.file_display_scene_widget import FileDisplayScene

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

        file_grid_view = QGraphicsView()
        file_grid_view.setInteractive(True)
        output_layout.addWidget(file_grid_view)

        file_grid_scene = FileDisplayScene()
        file_grid_scene.setBackgroundBrush(QBrush(QColor(167, 164, 163)))
        file_grid_view.setScene(file_grid_scene)
        file_grid_view.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        
        compress_button = QPushButton("Compress selected files")
        # compress_button.clicked.connect()
        output_layout.addWidget(compress_button)

        self.output_controller = OutputController(
            self,
            file_grid_scene,
            file_grid_view
        )
        # file_grid_view.mousePressEvent = self.output_controller.handle_click

    def resizeEvent(self, event):
        """Should overload the existing resize event, tells us to rebuild the file table
        """
        self.output_controller.build_file_table()
        event.accept()
        