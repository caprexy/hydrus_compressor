from models.file_model import FileModel
from PyQt6.QtGui import QImage
from PyQt6.QtCore import QBuffer, QIODevice, QByteArray
from PyQt6.QtWidgets import QDialog, QGridLayout, QLabel

from PIL import Image
from io import BytesIO

from widgets.file_display_tile_widget import FileDisplayTile
from widgets.file_compressing_display_widget import FileCompressingProgressWindow
from controller.helpers.api_file_processor import get_full_image

def compress_file_tiles(file_tile_list:list[FileDisplayTile]):
    # for file_tile in file_tile_list:
    #     if file_tile.highlight_tile is True:
    #         get_full_image(file_tile.file_obj.file_id)
    file_compress_window = FileCompressingProgressWindow(file_tile_list)
    file_compress_window.exec()