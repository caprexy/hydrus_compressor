"""Is the right side of the primary screen, should deal with calculating everything needed to setup the table for the view
"""
from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QWidget
from PyQt6.QtGui import QBrush, QColor

from models.file_model import FileModel
from widgets.file_display_tile_widget import FileDisplayTile
from controller.helpers.file_compressor import compress_file_tiles

class OutputController(QObject):
    """Calculates anything needed for the output/right view

    Args:
        QObject (_type_): of type qobj so we can borrow the signials and slots mechanisms to pass data between controllers
    """
    file_grid_scene = None
    file_list = None
    
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
        if self.file_list is None:
            return
        self.file_grid_scene.clear()
        
        tile_width = 200
        tile_height = 200
        width_pad = 10
        height_pad = 10
        
        available_width = self.parent_widget.width() - 40
        num_cols = max(1, available_width // tile_width)
        
        # build the tiles and sort them and 
        # then let them know their siblings and place on scene
        row = col = 0
        tiles = []
        for file in self.file_list:
            file.size_type = self.size_type
            tile = FileDisplayTile(file, tile_width, tile_height)
            tiles.append(tile)
        self.ordered_tiles = sorted(tiles, 
                               key=lambda tile: tile.file_obj.size_bytes, 
                               reverse=True)
        
        for tile in self.ordered_tiles:
            tile.set_ordered_sibling_tiles(self.ordered_tiles)
            tile.setPos(col * (tile_width) + (col+1)*width_pad, 
                        row * (tile_height) + (row+1)*height_pad)
            self.file_grid_scene.addItem(tile)
            col += 1
            if col == num_cols:
                col = 0
                row += 1
        
        # resize the scene to eliminate empty space
        self.file_grid_scene.setSceneRect(0, 0, 
                self.file_grid_scene.width(), 
                tile.mapToScene(0, 0).y()+tile_height+height_pad+10)
    
    def compress_selected_files(self):
        """Called when pressing the compress selected files button
        """
        # if self.file_grid_scene is None or self.ordered_tiles == []:
        #     return
        self.build_file_table()
        compress_file_tiles(self.ordered_tiles)
        
    
    def set_file_options(self, 
        size_type_in: str,
    ):
        """Set needed file options/information so we can display the newly set files nicely

        Args:
            size_type_in (str): Should be if GB, MB, etc
        """
        self.size_type = size_type_in
        
    def set_files(self, files:list[FileModel]):
        """Sets the files list

        Args:
            files (list[FileModel]): list of file objects that have been cleaned/parsed
        """
        self.file_list = files