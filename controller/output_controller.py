"""Is the right side of the primary screen, should deal with calculating everything needed to setup the table for the view
"""
from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QWidget
from PyQt6.QtGui import QBrush, QColor

from models.file_model import FileModel
from models.file_display_tile import FileDisplayTile

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
        
    def set_file_options(self, 
        size_type_in: str,
    ):
        """Set needed file options/information so we can display nicely

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
        
    def build_file_table(self):
        """Builds the file table based off of the file_list, so can be called any time
            Calculates where to put the file tiles
        """
        if self.file_list is None:
            return
        self.file_grid_scene.clear()
        
        available_width = self.parent_widget.width() - 40
        
        tile_width = 200
        tile_height = 200
        
        num_cols = max(1, available_width // tile_width)
        
        row = col = 0
    
        # NEED TO BUILD THE GRID OF TILES AND THEN LIMIT THE SIZE OF THE SCENE SO THE
        # SCENE WILL START IN THE TOP LEFT OF THE VIEW
        # OTHERWISE VIEW DOES STUFF IDK
        for file in self.file_list:
            if col % 2 == 0:
                background_rect = QGraphicsRectItem(col * tile_width, row * tile_height, tile_width, tile_height)
                background_rect.setBrush(QBrush(QColor(192, 192, 192)))
                self.file_grid_scene.addItem(background_rect)
            else:
                background_rect = QGraphicsRectItem(col * tile_width, row * tile_height, tile_width, tile_height)
                background_rect.setBrush(QBrush(QColor(192, 255, 192)))
                self.file_grid_scene.addItem(background_rect)
            tile = FileDisplayTile(file, tile_width)
            # offset = int((cell_size-tile.boundingRect().width())/2)
            tile.setPos(col * tile_width, row * tile_height)
            self.file_grid_scene.addItem(tile)
            background_rect = QGraphicsRectItem(0,0,50,50)
            background_rect.setBrush(QBrush(QColor(255, 192, 192)))
            background_rect.setPos(col * tile_width, row * tile_height)
            # self.file_grid_scene.addItem(background_rect)
            
            
            col += 1
            if col == num_cols:
                col = 0
                row += 1
           
    
    # def handle_click(self, event):
    #     """Beginnings of an handle click event

    #     Args:
    #         event (_type_): _description_
    #     """
    #     # Get the position of the click in scene coordinates
    #     scene_pos = self.file_grid_view.mapToScene(event.pos())

    #     # Find the item at the click position
    #     clicked_item = self.file_grid_scene.itemAt(scene_pos, self.file_grid_view.transform())

    #     if clicked_item:
    #         print(f"Clicked on item: {clicked_item}")
    #     else:
    #         print("Clicked on an empty area")