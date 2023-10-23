"""This is the model that represents a file as a tile. These tiles can then be arranged to become a grid.
    Has all file information and grid painting info.
"""
from PyQt6.QtWidgets import  QGraphicsWidget
from PyQt6.QtCore import  Qt, QRectF
from PyQt6.QtGui import  QColor,  QFontMetrics

from models.file_model import FileModel

class FileDisplayTile(QGraphicsWidget):
    """Custom widget to reprsent a tile in the grid of images.

    Args:
        QGraphicsWidget (QGraphicsWidget): inheritence
    """
    
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
        
        self.setContentsMargins(0,0,0,0)
        
        # split tile into image and label according to hard coded ratios here
        self.image_height = int(self.tile_height * .9)
        self.text_height = int(self.tile_height * .1)

        
    def paint(self, painter, option, widget=None):
        """Overloading of the QGraphicsWidget paint string. See original
        """
        super().paint(painter, option, widget)
        
        #build a background and outline for the tile
        painter.setPen(QColor(0, 0, 0))  # Set the pen color (outline color)
        painter.setBrush(QColor(255, 0, 0))  # Set the brush color (fill color)
        rect_x = 0
        rect_y = self.tile_height-self.text_height
        rect_w = self.tile_width-1
        rect_h = self.text_height
        painter.drawRect(rect_x, rect_y, rect_w, rect_h)
        
        
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


        # Create a label below the image
        painter.setPen(QColor(0, 0, 0))
        text = "Centered Text"
        font_metrics = QFontMetrics(painter.font()) #need complicated calculations for box shes
        text_rect = font_metrics.boundingRect(text)
        text_width = text_rect.width()
        text_height = text_rect.height()
        text_x = int(rect_x + (rect_w - text_width) / 2)
        text_y = int(rect_y + (rect_h - text_height) / 2 + text_height)
        painter.drawText(text_x, text_y, text)
        
    def boundingRect(self):
        """Overloaded define bounding rect
        """
        return QRectF(0, 0, self.tile_width, self.tile_height) 

    def setGeometry(self, rect):
        """ Overloaded set geometry but nothing really different
        """
        self.prepareGeometryChange()
        self.rect = rect