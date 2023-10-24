"""This is the model that represents a file as a tile. These tiles can then be arranged to become a grid.
    Has all file information and grid painting info.
"""
from PyQt6 import QtCore, QtGui
from PyQt6.QtWidgets import  QGraphicsSceneMouseEvent, QGraphicsWidget, QGraphicsRectItem, QGraphicsItem
from PyQt6.QtCore import  Qt, QRectF, QEvent
from PyQt6.QtGui import  QColor, QBrush, QPainterPath

from models.file_model import FileModel
from widgets.center_text_box_widget import CenterTextBox

class FileDisplayTile(QGraphicsItem):
    """Custom widget to reprsent a tile in the grid of images.

    Args:
        QGraphicsWidget (QGraphicsWidget): inheritence
    """
    
    tile_background_color = QColor(167, 164, 163)
    selected_background_color = QColor(179, 236, 248)
    highlight_tile = False
    ordered_sibling_tiles = None
    file_obj = None
    
    def __init__(self, input_file: FileModel, tile_width: int, tile_height: int):
        """Creates a new tile to display the file and all file information

        Args:
            input_file (FileModel): file object to use
            tile_width (int) : width of tile
            tile_height (int): heeight of tile
        """
        super().__init__()
        
        self.file_obj = input_file
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.pivot_tile = False
        self.highlight_tile = False
        
        self.setFlag(QGraphicsWidget.GraphicsItemFlag.ItemIsSelectable)
        
        # split tile into image and label according to hard coded ratios here
        self.image_height = int(self.tile_height * .9)
        self.text_height = int(self.tile_height * .1)
        
        # build textbox child widget
        # calculate text to say
        size = input_file.size_bytes
        if input_file.size_type == "GB":
            size = size / (1024**3)
        if input_file.size_type == "MB":
            size = size / (1024**2)
        size = round(size, 2)
        self.child_text_box = CenterTextBox(str(size) +" "+ input_file.size_type, 
                    self.tile_width, self.text_height)
        self.child_text_box.setParentItem(self)
        self.child_text_box.setPos(0, self.tile_height-self.text_height)

        
    def paint(self, painter, option, widget=None):
        """Overloading of the QGraphicsWidget paint string. See original
        """
        
        # paint background
        if self.isSelected() or self.highlight_tile:
            color = self.selected_background_color
        else:
            color = self.tile_background_color
        painter.setBrush(QBrush(color))
        painter.drawRect(0, 0, self.tile_width, self.tile_height)
        
        # build the image and scale it
        pixmap = self.file_obj.pixmap
        width_factor = self.tile_width / pixmap.width()
        height_factor = self.image_height / pixmap.height()
        scaling_factor = min(width_factor, height_factor)
        scaled_pixmap = pixmap.scaled(
            int(pixmap.width() * scaling_factor),
            int(pixmap.height() * scaling_factor),
            Qt.AspectRatioMode.KeepAspectRatio
        )
        x = (self.tile_width - scaled_pixmap.width()) / 2 # center of image at center of tile
        painter.drawPixmap(int(x), 1, scaled_pixmap)
   
    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        """Overload original
        """
        modifier = event.modifiers()
        found_pivot = None
        last_clicked_tile = None
        for tile in self.ordered_sibling_tiles:
            if modifier == Qt.KeyboardModifier.ShiftModifier:
                if tile.isSelected():  #find last clicked tile
                    last_clicked_tile = tile
                if tile.pivot_tile is True: # finds the prexisting pivot
                    found_pivot = tile
            elif modifier == Qt.KeyboardModifier.NoModifier:
                #unhighlight all other tiles
                tile.highlight_tile = False
                tile.pivot_tile = False
                tile.update()
            elif modifier == Qt.KeyboardModifier.ControlModifier:
                if tile.pivot_tile is True: #clears any prexisting pivot since 
                    # we are becoming the new one
                    tile.pivot_tile = False
            if tile.isSelected():
                tile.setSelected(False)
        self.setSelected(True)
        self.update()
        
        if modifier == Qt.KeyboardModifier.ControlModifier:
            self.pivot_tile = True
            self.highlight_tile = True
        
        if modifier == Qt.KeyboardModifier.ShiftModifier:
            if found_pivot and last_clicked_tile is not None:
                # changing an existing selection so need to erase previous selection
                last_clicked_tile = self.ordered_sibling_tiles.index(last_clicked_tile)
                pivot_tile_index = self.ordered_sibling_tiles.index(found_pivot)
                first_index = last_clicked_tile if last_clicked_tile < pivot_tile_index else pivot_tile_index
                second_index = pivot_tile_index if first_index == last_clicked_tile else last_clicked_tile
        
                for i,tile in enumerate(self.ordered_sibling_tiles):
                    if first_index <= i <= second_index:
                        tile.highlight_tile = False
                        tile.update()
            if found_pivot is None:
                found_pivot = last_clicked_tile
                last_clicked_tile.pivot_tile = True
            self.select_multiple_tiles(found_pivot)
        return super().mousePressEvent(event)
    
    def select_multiple_tiles(self, pivot_tile):
        """From the pivot, select every tile inbetween pivot and self

        Args:
            pivot_tile (FileDisplayTile): pivot tile or one of the ends of a selected set of continous tiles
        """
        cur_tile_index = self.ordered_sibling_tiles.index(self)
        pivot_tile_index = self.ordered_sibling_tiles.index(pivot_tile)
        
        first_index = cur_tile_index if cur_tile_index < pivot_tile_index else pivot_tile_index
        second_index = pivot_tile_index if first_index == cur_tile_index else cur_tile_index
        
        for i,tile in enumerate(self.ordered_sibling_tiles):
            if first_index <= i <= second_index:
                tile.highlight_tile = True
            tile.update()
        
    
    def boundingRect(self):
        """Overloaded define bounding rect
        """
        return QRectF(0, 0, self.tile_width, self.tile_height) 
    
    def set_ordered_sibling_tiles(self, tiles:list[QGraphicsItem]):
        self.ordered_sibling_tiles = tiles