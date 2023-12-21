"""Right panel where the output/found files should be displayed.
"""
    
from PyQt6.QtWidgets import QFrame ,QGraphicsScene , QSplitter, QWidget,QHBoxLayout, QVBoxLayout, QGraphicsView, QLabel, QPushButton, QSpinBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush, QColor
from controller.output_controller import OutputController

from view.input_function_widgets.file_compression_widgets import CompressionSettingsDialog
from view.ouput_widgets.tag_table_widget import TagTableWidget
from view.ouput_widgets.file_tile_display_widget import FileTileGridView
import models.settings as settings

class OutputWindow(QWidget):
    """Primary class for the right panel, the right panel should display and select images. And also to filter those images by tags

    Args:
        QWidget (_type_): For qwidget import, standard
    """
    input_window = None
    output_controller = None
    table = None

    file_grid_view = None
    def __init__(self):
        super().__init__()
        
        output_layout = QHBoxLayout()
        self.setLayout(output_layout)
        
        main_splitter = QSplitter()
        self.main_splitter = main_splitter
        output_layout.addWidget(main_splitter)
        
        #tag table
        self.tag_table = TagTableWidget(self)
        self.file_grid_view = FileTileGridView(self, self.tag_table)
        main_splitter.addWidget(self.file_grid_view)
        main_splitter.addWidget(self.tag_table)
        if settings.get_output_splitter_tags_geometry():
            self.tag_table.restoreGeometry(settings.get_output_splitter_tags_geometry())
        # tag_table.hide()
        
        self.output_controller = OutputController(
            self.tag_table,
            self.file_grid_view
        )


    def close_save(self):
        settings.set_output_window_geometry(self.saveGeometry())
        settings.set_output_splitter_tiles_geometry(self.file_grid_view.saveGeometry())
        settings.set_output_splitter_tags_geometry(self.tag_table.saveGeometry())

    def resizeEvent(self, event):
        """Should overload the existing resize event, tells us to rebuild the file table
        """
        self.file_grid_view.controller.build_file_table()
        event.accept()
        