"""This file describes the window/dialog that opens when compressing files,
also describes the workers needed to execute the work for compression
"""
import os
import pathlib
import datetime
import cv2
import uuid
import sys

from PyQt6.QtCore import QRunnable, QThreadPool, QObject, Qt, pyqtSignal
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor, QTextCharFormat
from PyQt6.QtWidgets import QTableWidget , QSpinBox, QVBoxLayout,  QTableWidgetItem, QSizePolicy, QAbstractScrollArea, QHeaderView, QDialog,QFrame, QLabel, QWidget, QStackedLayout

from models.file_tile import FileTile
from models import hydrus_api
from controller import constants
from controller.widgets.output_settings_widget import OutputSettingsDialog

class FileCompresser(QDialog):
    """Compresses the files and displays all files being compressed and status information
    """
    done_count = total_files = 0
    def __init__(self, 
                 file_tile_list:list[FileTile],
                 settings_dialog:OutputSettingsDialog):
        """Get all things neede for file compression

        Args:
            file_tile_list (list[FileTile]): list of file tiles to compress
            quality_input_spinbox (QSpinBox): spinbox to find the value from to compress to
        """
        super().__init__()
        self.setWindowTitle("File Compressing Progress Window")
        self.setSizeGripEnabled(True)
        self.settings_dialog = settings_dialog
        
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        self.thread_pool = QThreadPool()
        self.total_files = len(file_tile_list)
        # build file display grid and horizontal labels
        table = QTableWidget()
        table.setColumnCount(4)
        table.setRowCount(len(file_tile_list))
        table.setHorizontalHeaderLabels(['File id', 'Original Size', 'Compression Progress', 'New Size'])
        # table.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        for row_index, file_tile in enumerate(file_tile_list):
            
            file_progressWordBox = ProgressWordBox()
            table.setItem(
                row_index, 0,
                QTableWidgetItem(str(file_tile.file_id))
            )
            table.setItem(
                row_index, 1,
                QTableWidgetItem(str(file_tile.calculated_size)+file_tile.size_type),
            )
            table.setItem(
                row_index, 2,
                file_progressWordBox
            )
            size_label = QTableWidgetItem("..")
            table.setItem(
                row_index, 3,
                size_label
            )
            
            # grab compressor settings
            compression_level, use_percentage, resize_percentage, max_width, max_height = self.settings_dialog.get_settings()
            
            # run compresssor for file_tile
            compressor_worker = CompressingFileThreadWorker(file_tile, file_progressWordBox, size_label, 
                compression_level, use_percentage, resize_percentage, max_width, max_height)
            compressor_worker.workerSingals.finished.connect(self.if_done)
            
            self.thread_pool.start(compressor_worker)
        #resizer
        layout.addWidget(table)
        tableSize = table.sizeHint()
        dialogSize = self.size()
        dialogSize.setWidth(tableSize.width())
        self.resize(dialogSize)
        self.exec()
        
    def if_done(self):
        """Checks if we are done compressing everything and if so, what to do next
        """
        self.done_count += 1
        if self.done_count != self.total_files:
            return

class ProgressWordBox(QTableWidgetItem):
    def __init__(self):
        super().__init__()
        self.set_progress_text("Querying Hydrus API for image")
    
    def set_progress_text(self, text:str, done=False):
        self.setText(text)
        if done:
            self.setForeground(QBrush(QColor("green")))
        else:
            self.setForeground(QBrush(QColor("orange")))
    
    def set_text_and_color(self, text:str, color:str):
        self.setText(text)
        self.setForeground(QBrush(QColor(color)))
    
class WorkerSignals(QObject):
    """Miniclass to allow signalling
    """
    finished = pyqtSignal()
    
class CompressingFileThreadWorker(QRunnable):
    def __init__(self, 
                file_tile:FileTile, 
                progress_box:ProgressWordBox,
                size_label: QLabel,
                compression_value:int,
                use_percentage:bool,
                resize_percentage=None,
                max_width=None,
                max_height=None)-> None:
        super().__init__()
        self.workerSingals = WorkerSignals()
        self.compression_value = compression_value
        self.file_tile = file_tile
        self.progress_box = progress_box
        self.size_label = size_label
        
        self.use_percentage = use_percentage
        if use_percentage:
            self.resize_percentage = resize_percentage
        else:
            self.max_width = max_width
            self.max_height = max_height
            
    def run(self) -> None:
        """Given a fileTile, pull out the data and compress it
        """
        #get from hydrus
        image = hydrus_api.get_full_image(self.file_tile.file_id)
        self.progress_box.set_progress_text("Compressing original image")

        # Calculate the new width and height while maintaining the aspect ratio
        height, width = image.shape[:2]
        aspect_ratio = width / height
        new_width = new_height = -1
        if self.use_percentage:
            new_height = int(height * self.resize_percentage/100)
            new_width = int(width * self.resize_percentage/100)
            self.compression_value = 100
        else:
            if width > self.max_width:
                    new_width = self.max_width
                    new_height = int(new_width / aspect_ratio)
            elif height > self.max_height:
                    new_height = self.max_height
                    new_width = int(new_height * aspect_ratio)
            else:
                    new_width = width
                    new_height = height
        resized_image = cv2.resize(image, (new_width, new_height))
        # build the image and save
        file_path = str(pathlib.Path().resolve())
        output_image_path = file_path+"\\temp-images\\"+f"{self.file_tile.file_id}.jpeg"
        cv2.imwrite(output_image_path, resized_image, 
                    [cv2.IMWRITE_JPEG_QUALITY, self.compression_value, 
                     cv2.IMWRITE_JPEG_OPTIMIZE, 1])

        img_size = os.stat(output_image_path).st_size
        if self.file_tile.size_type == "MB":
            img_size = img_size / (1024 ** 2)
            self.size_label.setText(f"{img_size:.2f} MB")
        if self.file_tile.size_type == "GB":
            img_size = img_size / (1024 ** 3)
            self.size_label.setText(f"{img_size:.2f} GB")
            
        # Set the modified time of the file
        modified_time = datetime.datetime.utcfromtimestamp(self.file_tile.unix_modified_time)
        os.utime(output_image_path, (modified_time.timestamp(), modified_time.timestamp()))
        self.progress_box.set_progress_text("Sending new file to hydrus")
            
        # send file to hydrus
        res = hydrus_api.send_to_hydrus(output_image_path)
        if "error" in res:
            raise ConnectionAbortedError("Somethihng went wrong when sending to hydrus, got error back")
        status = res["status"]
        new_hash = res["hash"]
        if status == 1:
            self.progress_box.set_text_and_color("Sucessful file import", "orange")
        if status == 2:
            self.progress_box.set_text_and_color("File was already in database somehow", "red")
        if status == 3:
            self.progress_box.set_text_and_color("File was already deleted somehow", "red")
        if status >= 4:
            self.progress_box.set_text_and_color("File failed to import", "red")
        os.remove(output_image_path)
        
        # stop if broken, else progress
        if status != 1:
            return
        self.progress_box.set_progress_text("Duplicating tags to new file")
        hydrus_api.add_tags_hash(new_hash, self.file_tile.storage_tags)
        self.progress_box.set_progress_text("Duplicating ratings to new file")
        hydrus_api.add_ratings(new_hash, self.file_tile.ratings)
        self.progress_box.set_progress_text("Duplicating notes to new file")
        hydrus_api.add_notes(new_hash, self.file_tile.notes)
        self.progress_box.set_progress_text("Sending old file to hydrus trash")
        hydrus_api.delete_file(self.file_tile.file_id)
        self.progress_box.set_progress_text("Progress complete!!", done=True)
        
        # if sucess, we can add tags
        self.workerSingals.finished.emit()