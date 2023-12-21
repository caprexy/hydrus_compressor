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

class FileTileGridController(QWidget):

    parent_file_tile_grid_view = None
    grandfather_output_widget = None
    
    file_tile_list: List[FileTile] = []
    
    tile_width = 200
    tile_height = 200
    tag_table_widget = None
    
    def __init__(self, 
                 parent_file_tile_grid_view:QWidget, 
                 tag_table_widget:TagTableWidget,
                 grandfather_output_widget:QWidget):
        super().__init__()
        self.parent_file_tile_grid_view = parent_file_tile_grid_view
        self.tag_table_widget = tag_table_widget
        self.grandfather_output_widget = grandfather_output_widget
        
    def build_file_table(self):
        """Builds the file table based off of the file_list, so can be called any time
            Calculates where to put the file tiles
        """
        if len(self.file_tile_list) == 0:
            return
        
        width_pad = 10
        height_pad = 10
        
        available_width = self.grandfather_output_widget.width() - 70
        num_cols = max(1, available_width // self.tile_width)
        
        row = col = 0
        
        # place tiles and add to scene
        for tile in self.file_tile_list:
            if tile.isVisible() is  False: #dont paint hidden tiles
                print("invis")
                continue
            tile.set_ordered_tiles(self.file_tile_list)
            tile.setPos(col * (self.tile_width) + (col+1)*width_pad, 
                        row * (self.tile_height) + (row+1)*height_pad)
            tile.update()
            col += 1
            if col == num_cols:
                col = 0
                row += 1
        
        # resize the scene to eliminate empty space
        self.parent_file_tile_grid_view.scene.setSceneRect(0, 0, 
                num_cols * self.tile_width + (num_cols + 1) * width_pad, 
                (row+1)*self.tile_height+(row+2)*height_pad)
        
    
    def get_selected_tiles(self):
        if self.parent_file_tile_grid_view.scene is None or self.file_tile_list == []:
            return
        
        selected_file_tiles = [tile for tile in self.file_tile_list if tile.highlight_tile is True]
        if selected_file_tiles == []:
            return
        return selected_file_tiles
    
    
    def process_api_files_metadata(self, files_metadata:[], size_type:str)->[FileTile]:
        """ turns given file_metadata into filetiles for display

        Args:
            files_metadata ([]): List of metadata for files, given from hydrus_api
        """
        if files_metadata == [] or files_metadata is None:
            return None
        thread_pool = QThreadPool()
        
        # dialogue popup setup
        progress_dialog = QProgressDialog(
            "Getting files from hydrus",
            "Cancel",
            0,
            len(files_metadata)
        )
        progress_dialog.setWindowTitle("Requesting from hydrus")
        progress_dialog.setValue(0)
        def progress_callback():
            progress_dialog.setValue(progress_dialog.value()+1)
        
        # create workers and connect to popup
        file_tile_queue = Queue()
        
        for file_metadata in files_metadata:
            file_tile_worker = FileTileCreatorWorker(
                file_metadata, self.tile_width, self.tile_height, file_tile_queue, size_type
            )
            file_tile_worker.signals.finished.connect(progress_callback)
            thread_pool.start(file_tile_worker)
            
        # setup waiting part
        progress_dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        progress_dialog.show()
        thread_pool.waitForDone()
        
        # clean  previous items
        for item in self.parent_file_tile_grid_view.scene.items():
            self.parent_file_tile_grid_view.scene.removeItem(item)
            
        # sort the file_tiles and then rebuild the table
        self.tag_counter = Counter()
        self.filetile_tag_pairlist = []
        self.file_tile_list = []
        while not file_tile_queue.empty():
            tile = file_tile_queue.get()
            self.file_tile_list.append(tile)
            self.parent_file_tile_grid_view.scene.addItem(tile)
            # add data to tag window:
            for service in tile.tags:
                if tile.tags[service]['type_pretty'] == "virtual combined tag service":
                    tile_tags = tile.tags[service]['storage_tags']["0"]
                    for tag in tile_tags:
                        self.tag_counter[tag] += 1
                    self.filetile_tag_pairlist.append((tile, tile_tags))
        self.file_tile_list = sorted(self.file_tile_list, 
                        key=lambda tile_list_ele: tile_list_ele.size_bytes, 
                        reverse=True)
        
        # build tag window
        self.tag_table_widget.update_tags(self.tag_counter, self.filetile_tag_pairlist)
        
        self.build_file_table()