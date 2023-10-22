from PyQt6.QtWidgets import  QGraphicsLinearLayout, QGraphicsRectItem, QGraphicsProxyWidget , QGraphicsSimpleTextItem, QGraphicsWidget
from PyQt6.QtCore import  Qt, QMarginsF 
from PyQt6.QtGui import QBrush, QColor

from models.file_model import FileModel
class FileDisplayTile(QGraphicsWidget):
    
    def __init__(self, input_file: FileModel, cell_size: int):
        """Creates a new tile to display the file and all file information

        Args:
            width (int): width of the tile, usually cell size
            height (int): height of the tile, usually cell size
            input_file (FileModel): file object to use
            cell_size (int): cell size
        """
        super().__init__()
        
        self.file_obj = input_file
        self.parent_cell_size = cell_size
        
        layout = QGraphicsLinearLayout(Qt.Orientation.Vertical, self)
        
        layout.setContentsMargins(0,0,0,0)
        self.setContentsMargins(0,0,0,0)
        
        class CustomGraphicsWidget(QGraphicsWidget):
            def paint(self, painter, option, widget):
                rect = self.rect()
                painter.setBrush(QBrush(QColor(255, 0, 0)))  # Set the color of the rectangle
                # Calculate the position to center the rectangle
                rect_width = rect.width()
                rect_height = rect.height()
                x = (cell_size - rect_width) / 2
                y = (cell_size - rect_height) / 2
                painter.drawRect(x, y, rect_width, rect_height)
        
        
        widget = CustomGraphicsWidget()
        widget.setPos(0,0)
        layout.addItem(widget)
        layout.setAlignment(widget,Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)

        
        
        # print(self.geometry().x())
        ## build the image
        # pixmap = self.file_obj.pixmap
        # width_factor = cell_size / pixmap.width()
        # height_factor = cell_size / pixmap.height()
        
        # scaling_factor = min(width_factor, height_factor)

        # scaled_pixmap = pixmap.scaled(
        #     int(pixmap.width() * scaling_factor),
        #     int(pixmap.height() * scaling_factor),
        #     Qt.AspectRatioMode.KeepAspectRatio
        # )
        
        # img = QLabel()
        # pixmap = QPixmap(scaled_pixmap)
        # img.setPixmap(pixmap)
        # proxy_widget = QGraphicsProxyWidget()
        # proxy_widget.setWidget(img)
        # proxy_widget.setPos(0,0)
        # layout.addItem(proxy_widget)
        # layout.setAlignment(proxy_widget, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)