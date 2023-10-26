"""Is the right side of the primary screen, should deal with calculating everything needed to setup the table for the view
"""
from PyQt6.QtCore import QObject, QRunnable, QThreadPool, pyqtSignal
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QWidget, QProgressDialog 
from PyQt6.QtGui import QBrush, QColor
from queue import Queue

# from models.file_model import FileModel
from widgets.file_tile_widget import FileTile, FileTileCreatorWorker
from controller.helpers.file_compressor import compress_file_tiles

class OutputController(QObject):
    """Calculates anything needed for the output/right view

    Args:
        QObject (_type_): of type qobj so we can borrow the signials and slots mechanisms to pass data between controllers
    """
    file_grid_scene = None
    file_tile_list = []
        
    tile_width = 200
    tile_height = 200
    
    
    def __init__(self,
        parent_widget : QWidget,
        file_grid_scene_in: QGraphicsScene,
        file_grid_view: QGraphicsView):
        super().__init__()
        self.file_grid_scene = file_grid_scene_in
        self.parent_widget = parent_widget
        self.file_grid_view = file_grid_view
        
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
        total_items = len(self.file_tile_list)
        num_rows = (total_items + num_cols - 1) // num_cols
        
        
        for item in self.file_grid_scene.items():
            self.file_grid_scene.removeItem(item)
        
        row = col = 0
        
        for tile in self.file_tile_list:
            tile.set_ordered_sibling_tiles(self.file_tile_list)
            tile.setPos(col * (self.tile_width) + (col+1)*width_pad, 
                        row * (self.tile_height) + (row+1)*height_pad)
            self.file_grid_scene.addItem(tile)
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
        if self.file_grid_scene is None or self.ordered_tiles == []:
            return
        compress_file_tiles(self.ordered_tiles)
        
    
    def set_file_options(self, 
        size_type_in: str,
    ):
        """Set needed file options/information so we can display the newly set files nicely

        Args:
            size_type_in (str): Should be if GB, MB, etc
        """
        self.size_type = size_type_in
        
    def process_api_files_metadata(self, files_metadata:[])->[FileTile]:
        """ turns file_metadata into filetiles

        Args:
            files_metadata ([]): List of metadata for files, now need to process and turn into file_tiles
        """
        thread_pool = QThreadPool()
        
        # dialogue popup setup
        progress_dialog = QProgressDialog(
            "Getting files from hydrus",
            "Cancel",
            0,
            len(files_metadata)
        )
        progress_dialog.setValue(0)
        def progress_callback():
            progress_dialog.setValue(progress_dialog.value()+1)
        
        # create workers and make popup
        file_queue = Queue()
        for file_metadata in files_metadata:
            file_tile_worker = FileTileCreatorWorker(
                file_metadata, self.tile_width, self.tile_height, file_queue, self.size_type
            )
            file_tile_worker.signals.finished.connect(progress_callback)
            thread_pool.start(file_tile_worker)
        progress_dialog.exec()
        
        thread_pool.waitForDone()
        
        # empty out our filequeue and sort
        self.file_tile_list = []
        while not file_queue.empty():
            item = file_queue.get()
            self.file_tile_list.append(item)
        self.file_tile_list = sorted(self.file_tile_list, 
                               key=lambda tile: tile.size_bytes, 
                               reverse=True)
    
        self.build_file_table()
