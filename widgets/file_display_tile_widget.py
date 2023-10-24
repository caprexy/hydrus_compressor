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
    
    tile_background_color = QColor(192, 255, 192)
    selected_background_color = QColor(255, 255, 255)
    highlight_tile = False
    
    def __init__(self, input_file: FileModel, tile_width: int, tile_height: int, ordered_sibling_tiles:list[QGraphicsItem]):
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
        self.ordered_sibling_tiles = ordered_sibling_tiles
        
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
        new_pivot = None
        for item in self.scene().items():
            if isinstance(item, FileDisplayTile):
                if modifier == Qt.KeyboardModifier.ShiftModifier:
                    # look for pivots for shift multiple select
                    if item.isSelected():
                        new_pivot = item
                    if item.pivot_tile is True:
                        found_pivot = item
                elif modifier == Qt.KeyboardModifier.NoModifier:
                    #unhighlight all other tiles
                    item.setSelected(False)
                    item.highlight_tile = False
                    item.pivot_tile = False
                    item.update()
                elif modifier == Qt.KeyboardModifier.ControlModifier:
                    if item.pivot_tile is True:
                        item.pivot_tile = False
        self.setSelected(True)
        self.update()
        
        if modifier == Qt.KeyboardModifier.ControlModifier:
            self.pivot_tile = True
            self.highlight_tile = True
        
        if modifier == Qt.KeyboardModifier.ShiftModifier:
            if found_pivot:
                new_pivot = found_pivot
            else:
                new_pivot.pivot_tile = True
            self.select_multiple_tiles(new_pivot)
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
    