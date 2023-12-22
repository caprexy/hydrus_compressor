"""Is the right side of the primary screen, should deal with calculating everything needed to display the table for the view.
"""
from typing import List
from queue import Queue
import json
from collections import Counter

from PyQt6.QtCore import QObject, Qt, QThreadPool, pyqtSignal
from PyQt6.QtWidgets import QGraphicsView, QTableWidgetItem, QGraphicsScene, QTableWidget, QWidget, QProgressDialog 
from PyQt6.QtGui import QBrush, QColor

from models.file_tile import FileTile, FileTileCreatorWorker
from view.input_function_widgets.file_compression_widgets import CompressionSettingsWidget
from view.ouput_widgets.tag_table_widget import TagTableRow, TagTableWidget
from view.ouput_widgets.file_tile_display_widget import FileTileGridView
from controller.utilities.file_compressor import FileCompresser
from view.ouput_widgets.tag_table_widget import TagTableRow, TagTableWidget

class OutputController(QObject):
    """Calculates anything needed for the output/right view

    Args:
        QObject (_type_): of type qobj so we can borrow the signials and slots mechanisms to pass data between controllers
    """
    file_grid_scene = None
    file_tile_list: List[FileTile] = []
        
    tile_width = 200
    tile_height = 200
    
    size_type = None
    
    input_controller = None
    def __init__(self,
            tag_table : TagTableWidget,
            file_grid_view : FileTileGridView
        ):
        super().__init__()
        self.file_grid_view = file_grid_view
        tag_table.build_file_grid_emitter.connect(file_grid_view.controller.build_file_table)
        
    def return_file_tile_grid_view(self):
        return self.file_grid_view
