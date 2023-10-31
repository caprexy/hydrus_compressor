"""This file describes the window/dialog that opens when compressing files,
also describes the workers needed to execute the work for compression
"""
import os
import pathlib

from PyQt6.QtCore import QRunnable, QThreadPool, QObject, QEvent, pyqtSignal
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor, QTextCharFormat
from PyQt6.QtWidgets import QTableWidget , QSpinBox, QVBoxLayout,  QTableWidgetItem, QSizePolicy, QAbstractScrollArea, QHeaderView, QDialog,QFrame, QLabel, QWidget, QStackedLayout

from controller.widgets.file_tile_widget import FileTile
import controller.helpers.api_file_processor as api_file_processor
from controller import constants
class FileCompressingProgressWindow(QDialog):
    """Displays all files being compressed and status information
    """
    done_count = total_files = 0
    def __init__(self, 
                 file_tile_list:list[FileTile],
                 quality_input_spinbox:QSpinBox):
        """Get all things neede for file compression

        Args:
            file_tile_list (list[FileTile]): list of file tiles to compress
            quality_input_spinbox (QSpinBox): spinbox to find the value from to compress to
        """
        super().__init__()
        self.setWindowTitle("File Compressing Progress Window")
        self.setSizeGripEnabled(True)
        self.quality_input_spinbox = quality_input_spinbox
        
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        self.thread_pool = QThreadPool()
        self.total_files = len(file_tile_list)
        # build file display grid and horizontal labels
        table = QTableWidget()
        table.setColumnCount(3)
        table.setRowCount(len(file_tile_list))
        table.setHorizontalHeaderLabels(['File id', 'Size', 'Compression Progress'])
        table.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        # table.horizontalHeader().setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        # table.horizontalHeader().setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        table.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        compression_value = self.quality_input_spinbox.value()
        for row_index, file_tile in enumerate(file_tile_list):
            
            progressWordBox = ProgressWordBox()
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
                progressWordBox
            )
            
            # run compresssor for file_tile
            compressor_worker = CompressingFileThreadWorker(file_tile, compression_value, progressWordBox)
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
    steps =[
        "Querying Hydrus API",
        "Compressing",
        "Sending to Hydrus",
        "Sending previous file tags to hydrus",
        "Sending preivous ratings to hydrus",
        "Sending previous notes to hydrus",
        "Deleting previous non compressed hydrus file",
        "Complete!"
    ]
    working_step = -1
            
    def __init__(self):
        super().__init__()
        self.step_forward()
        
    def step_forward(self):
        self.working_step += 1
        if self.working_step >= len(self.steps):
            # if done
            self.setText(self.steps[len(self.steps)-1])
            self.setForeground(QBrush(QColor("green")))
        else:
            self.setText(self.steps[self.working_step])
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
                 compression_value:int,
                 progress_box:ProgressWordBox) -> None:
        super().__init__()
        self.workerSingals = WorkerSignals()
        self.compression_value = compression_value
        self.file_tile = file_tile
        self.progress_box = progress_box
    def run(self) -> None:
        """Given a fileTile, pull out the data and compress it
        """
        #get from hydrus
        image = api_file_processor.get_full_image(self.file_tile.file_id)
        self.progress_box.step_forward()
        
        with image as open_image:
            # open as image and save/optmize the image\
            file_path = str(pathlib.Path().resolve()) +  "\\temp-images\\"
            file_path = file_path+str(self.file_tile.file_id)+\
                "."+open_image.format.lower()
            open_image.save(fp=file_path,
                    quality=self.compression_value,
                    optimize=True,
                    format=open_image.format)
            self.progress_box.step_forward()
            
            # send file to hydrus
            res = api_file_processor.send_to_hydrus(file_path)
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
        os.remove(file_path)
        
        # stop if broken, else progress
        if status != 1:
            return
        self.progress_box.step_forward()
        api_file_processor.add_tags_hash(new_hash, self.file_tile.storage_tags)
        self.progress_box.step_forward()
        api_file_processor.add_ratings(new_hash, self.file_tile.ratings)
        self.progress_box.step_forward()
        api_file_processor.add_notes(new_hash, self.file_tile.notes)
        self.progress_box.step_forward()
        
        # api_file_processor.delete_file(self.file_tile.file_id)
        # self.progress_box.step_forward()
        
        # if sucess, we can add tags
        self.workerSingals.finished.emit()