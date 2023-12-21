from typing import List
from collections import Counter
from queue import Queue

from PyQt6.QtWidgets import QFrame ,QGraphicsScene , QProgressDialog, QWidget,QHBoxLayout, QVBoxLayout, QGraphicsView, QLabel, QPushButton, QSpinBox
from PyQt6.QtGui import QBrush, QColor
from PyQt6.QtCore import QObject, Qt, QThreadPool, pyqtSignal
from PyQt6.QtGui import QBrush, QColor

import models.settings as settings
from models.file_tile import FileTile, FileTileCreatorWorker
from view.ouput_widgets.tag_table_widget import TagTableRow, TagTableWidget
from controller.output.file_tile_display_controller import FileTileGridController

class FileTileGridView(QWidget):

    view = None
    scene = None
    def __init__(self, parent,tag_table_widget:TagTableWidget):
        super().__init__()
        self.controller = FileTileGridController(self, tag_table_widget, parent)
        
        self.parent_widget = parent
        self.tag_table_widget = tag_table_widget
        
        if settings.get_output_splitter_tiles_geometry():
            self.restoreGeometry(settings.get_output_splitter_tiles_geometry())
        filegrid_layout = QVBoxLayout()
        self.setLayout(filegrid_layout)
        
        view = QGraphicsView()
        self.view = view
        view.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.BoundingRectViewportUpdate)
        view.setInteractive(True)
        filegrid_layout.addWidget(view)
        

        scene = QGraphicsScene()
        self.scene = scene
        scene.setBackgroundBrush(QBrush(QColor(230, 230, 230)))
        view.setScene(scene)
        view.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        
        self.update()
        
        
    
