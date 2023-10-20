"""Is the right side of the primary screen, should deal with calculating everything needed to setup the table for the view
"""
from PyQt6.QtCore import QObject, Qt
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QWidget, QGraphicsPixmapItem
from PyQt6.QtGui import QBrush, QColor

from models.file_model import FileModel
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
        """
        if self.file_list is None:
            return
        self.file_grid_scene.clear()
        
        available_width = self.parent_widget.width() - 40
        
        cell_size = 200
        
        num_cols = max(1, available_width // cell_size)
        
        row = col = 0
    
        for file in self.file_list:
            if col % 2 == 0:
                background_rect = QGraphicsRectItem(col * cell_size, row * cell_size, cell_size, cell_size)
                background_rect.setBrush(QBrush(QColor(192, 192, 192)))
                self.file_grid_scene.addItem(background_rect)
                
            image = self.file_to_objs(file, cell_size)
            offset = int((cell_size-image.boundingRect().width())/2)
            image.setPos(col * cell_size + offset, row * cell_size)
            self.file_grid_scene.addItem(image)
            
            col += 1
            if col == num_cols:
                col = 0
                row += 1
            
    
    def file_to_objs(self, file: FileModel, cell_size: int):
        """Turns a file into all of the objects to display

        Args:
            file (FileModel): file to turn into objects
            cell_size (int): cell size of the working space so we can confine objects to cell

        Returns:
            _type_: QGraphicsPixmapItem image
        """
        
        pixmap = file.pixmap
        width_factor = cell_size / pixmap.width()
        height_factor = cell_size / pixmap.height()
        
        scaling_factor = min(width_factor, height_factor)

        scaled_pixmap = pixmap.scaled(
            int(pixmap.width() * scaling_factor),
            int(pixmap.height() * scaling_factor),
            Qt.AspectRatioMode.KeepAspectRatio
        )
        
        image = QGraphicsPixmapItem(scaled_pixmap)
        
        return image
    
    def handle_click(self, event):
        """Beginnings of an handle click event

        Args:
            event (_type_): _description_
        """
        # Get the position of the click in scene coordinates
        scene_pos = self.file_grid_view.mapToScene(event.pos())

        # Find the item at the click position
        clicked_item = self.file_grid_scene.itemAt(scene_pos, self.file_grid_view.transform())

        if clicked_item:
            print(f"Clicked on item: {clicked_item}")
        else:
            print("Clicked on an empty area")