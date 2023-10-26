"""This is the model that represents a file as a tile. These tiles can then be arranged to become a grid.
    Has all file information and grid painting info. This is effectively a file.
"""
from PyQt6 import QtCore, QtGui
from PyQt6.QtWidgets import  QGraphicsSceneMouseEvent, QGraphicsWidget, QGraphicsRectItem, QGraphicsItem
from PyQt6.QtCore import  Qt, QRectF, QEvent, QRunnable, pyqtSignal, QObject
from PyQt6.QtGui import  QColor, QBrush, QPainterPath
from queue import Queue

from controller.helpers import api_file_processor

from widgets.center_text_box_widget import CenterTextBox

class FileTile(QGraphicsItem):
    """Custom widget to reprsent a tile in the grid of images.

    Args:
        QGraphicsWidget (QGraphicsWidget): inheritence
    """
    
    tile_background_color = QColor(210, 210, 210)
    selected_background_color = QColor(179, 236, 248)
    highlight_tile = False
    ordered_sibling_tiles = None
    
    def __init__(self, file_metadata: {}, tile_width: int, tile_height: int, size_type: str):
        """Creates a new tile to display the file and all file information

        Args:
            file_metadata ({}}): file metadata to parse
            tile_width (int) : width of tile
            tile_height (int): heeight of tile
        """
        super().__init__()
        self.process_metadata(file_metadata)
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.size_type = size_type
        self.pivot_tile = False
        self.highlight_tile = False
        
        self.setFlag(QGraphicsWidget.GraphicsItemFlag.ItemIsSelectable)
        
        # split tile into image and label according to hard coded ratios here
        self.image_height = int(self.tile_height * .9)
        self.text_height = int(self.tile_height * .1)
        
        # build textbox child widget
        # calculate text to say
        size = self.size_bytes
        if self.size_type == "GB":
            size = size / (1024**3)
        if self.size_type == "MB":
            size = size / (1024**2)
        size = round(size, 2)
        self.calculated_size = size
        self.child_text_box = CenterTextBox(str(size) +" "+ self.size_type, 
                    self.tile_width, self.text_height)
        self.child_text_box.setParentItem(self)
        self.child_text_box.setPos(0, self.tile_height-self.text_height)

        
    def paint(self, painter, option, widget=None):
        """Overloading of the QGraphicsWidget paint string. See original
        """
        
        # paint background
        if self.highlight_tile:
            color = self.selected_background_color
        else:
            color = self.tile_background_color
        painter.setBrush(QBrush(color))
        painter.drawRect(0, 0, self.tile_width, self.tile_height)
        
        # paint textbox again
        self.child_text_box.setParentItem(self)
        self.child_text_box.setPos(0, self.tile_height-self.text_height)
        
        # get the thumbnail and build it
        pixmap = api_file_processor.get_file_thumbnail(self.file_id)
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
        pivot_tile = None
        last_clicked_tile = None
        for tile in self.ordered_sibling_tiles:
            if modifier == Qt.KeyboardModifier.ShiftModifier:
                if tile.isSelected():  #find last clicked tile
                    pivot_index = self.ordered_sibling_tiles.index(tile)
                    last_clicked_tile = tile
                if tile.pivot_tile is True: # finds the prexisting pivot
                    pivot_tile = tile
                    pivot_index = self.ordered_sibling_tiles.index(tile)
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
        if pivot_tile is None:
            self.pivot_tile = True
        
        # handle control click for self
        if modifier == Qt.KeyboardModifier.ControlModifier and self.highlight_tile is True:
            self.highlight_tile = False
        elif modifier == Qt.KeyboardModifier.ControlModifier and self.highlight_tile is False:
            self.highlight_tile = True
            self.pivot_tile = True
        else:
            self.highlight_tile = True
            
        # handle shift click
        if modifier == Qt.KeyboardModifier.ShiftModifier and pivot_tile:
            pivot_index = self.ordered_sibling_tiles.index(pivot_tile)
            self_index = self.ordered_sibling_tiles.index(self)
            # if last_clicked_tile wasn't pivot, then we must dehighlight other tiles
            if pivot_tile is not last_clicked_tile and last_clicked_tile is not None:
                last_clicked_index = self.ordered_sibling_tiles.index(last_clicked_tile)
                for index, tile in enumerate(self.ordered_sibling_tiles):
                    if last_clicked_index <= index <= pivot_index or pivot_index <= index <= last_clicked_index:
                        tile.highlight_tile = False
                        tile.update()
            # highlight all new tiles from pivot to self 
            for index, tile in enumerate(self.ordered_sibling_tiles):
                if self_index <= index <= pivot_index or pivot_index <= index <= self_index:
                    tile.highlight_tile = True
                    tile.update()
        
        return super().mousePressEvent(event)
    
    
    def boundingRect(self):
        """Overloaded define bounding rect
        """
        return QRectF(0, 0, self.tile_width, self.tile_height) 
    
    def set_ordered_sibling_tiles(self, tiles:list[QGraphicsItem]):
        self.ordered_sibling_tiles = tiles
        
    def process_metadata(self, file_metadata):
        self.file_id = file_metadata["file_id"]
        self.file_type, self.extension = file_metadata["mime"].split("/")
        self.size_bytes = file_metadata["size"]
        self.display_tags = file_metadata["tags"]["616c6c206b6e6f776e2074616773"] 
        


class WorkerSignals(QObject):
    finished = pyqtSignal()
    
class FileTileCreatorWorker(QRunnable):
    """FileTile worker to create filetiles without slowing applicaiton too much
    Args:
        QRunnable (_type_): overriden thread type
    """
    def __init__(self, 
            file_metadata:{}, 
            tile_width:int, 
            tile_height:int, 
            file_queue:Queue,  
            size_type:str) -> None:
        """Worker to thread the creation of file_tiles

        Args:
            file_metadata ({}): json metadata in dict format
            self.tile_width (int): width of the display tile
            self.tile_height (int): height of the display tile
            file_queue (file_queue): thread safe queue to put our complete objs in
            size_type (str): pass in size type from input
        """
        super().__init__()
        self.file_metadata = file_metadata
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.file_queue = file_queue
        self.size_type = size_type
        self.signals = WorkerSignals()
        
    def run(self) -> None:
        """Overwrites thread run to instead put an filetile object with the given data
        """
        self.file_queue.put(
            FileTile(self.file_metadata, 
                     self.tile_width, 
                     self.tile_height,  
                     self.size_type))
        self.signals.finished.emit()
    