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
from controller.widgets.output_settings_widget import OutputSettingsDialog
from controller.widgets.tag_table_widget import TagTableRow, TagTableWidget
from models.file_compressor import FileCompresser

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
    
    def __init__(self,
            parent_widget : QWidget,
            file_grid_scene_in: QGraphicsScene,
            file_grid_view: QGraphicsView,
            settings_dialog: OutputSettingsDialog,
            tag_table: TagTableWidget,
        ):
        super().__init__()
        self.file_grid_scene = file_grid_scene_in
        self.parent_widget = parent_widget
        self.file_grid_view = file_grid_view
        self.settings_dialog = settings_dialog
        self.tag_table_widget = tag_table
        self.tag_table_widget.build_table_emitter.connect(self.build_file_table)
        self.tag_counter = Counter()
        
    def build_file_table(self):
        """Builds the file table based off of the file_list, so can be called any time
            Calculates where to put the file tiles
        """
        if len(self.file_tile_list) == 0:
            return
        
        width_pad = 10
        height_pad = 10
        
        available_width = self.parent_widget.width() - 70
        num_cols = max(1, available_width // self.tile_width)
        
        row = col = 0
        
        # place tiles and add to scene
        for tile in self.file_tile_list:
            if tile.isVisible() is  False: #dont paint hidden tiles
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
        self.file_grid_scene.setSceneRect(0, 0, 
                num_cols * self.tile_width + (num_cols + 1) * width_pad, 
                (row+1)*self.tile_height+(row+2)*height_pad)

    def compress_selected_files(self):
        """Called when pressing the compress selected files button
        """
        if self.file_grid_scene is None or self.file_tile_list == []:
            return
        
        selected_file_tiles = [tile for tile in self.file_tile_list if tile.highlight_tile is True]
        if selected_file_tiles == []:
            return
        FileCompresser(selected_file_tiles, self.settings_dialog)
        
    def process_api_files_metadata(self, files_metadata:[])->[FileTile]:
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
                file_metadata, self.tile_width, self.tile_height, file_tile_queue, self.size_type
            )
            file_tile_worker.signals.finished.connect(progress_callback)
            thread_pool.start(file_tile_worker)
            
        # setup waiting part
        progress_dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        progress_dialog.show()
        thread_pool.waitForDone()
        
        # clean  previous items
        for item in self.file_grid_scene.items():
            self.file_grid_scene.removeItem(item)
            
        # sort the file_tiles and then rebuild the table
        self.tag_counter = Counter()
        self.filetile_tag_pairlist = []
        self.file_tile_list = []
        while not file_tile_queue.empty():
            tile = file_tile_queue.get()
            self.file_tile_list.append(tile)
            self.file_grid_scene.addItem(tile)
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
        self.tag_table_widget.pass_tag_info(self.tag_counter, self.filetile_tag_pairlist)
        self.tag_table_widget.build_tag_table(self.tag_counter)
        
        self.build_file_table()