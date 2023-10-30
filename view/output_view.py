"""Right panel where the output/found files should be displayed
"""
    
from PyQt6.QtWidgets import QHBoxLayout, QWidget, QVBoxLayout, QGraphicsView, QLabel, QPushButton, QSpinBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush, QColor
from controller.output_controller import OutputController

from controller.widgets.file_display_scene_widget import FileDisplayScene
from controller.widgets.file_grid_view_widget import FileGridView

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
        file_grid_view.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.BoundingRectViewportUpdate)
        file_grid_view.setInteractive(True)
        output_layout.addWidget(file_grid_view)

        file_grid_scene = FileDisplayScene()
        file_grid_scene.setBackgroundBrush(QBrush(QColor(230, 230, 230)))
        file_grid_view.setScene(file_grid_scene)
        file_grid_view.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        
        saving_opts_layout = QHBoxLayout()
        quality_label = QLabel("Compressed Image quality: ")
        saving_opts_layout.addWidget(quality_label)
        quality_input = QSpinBox()
        quality_input.setMinimum(0)
        quality_input.setMaximum(95)
        quality_input.setValue(85)
        saving_opts_layout.addWidget(quality_input)
        output_layout.addLayout(saving_opts_layout)
        
        compress_button = QPushButton("Compress selected files")
        output_layout.addWidget(compress_button)

        self.output_controller = OutputController(
            self,
            file_grid_scene,
            file_grid_view,
            quality_input
        )
        compress_button.clicked.connect(self.output_controller.compress_selected_files)

    def resizeEvent(self, event):
        """Should overload the existing resize event, tells us to rebuild the file table
        """
        self.output_controller.build_file_table()
        event.accept()
        