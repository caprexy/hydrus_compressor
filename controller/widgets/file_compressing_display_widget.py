"""This file describes the window/dialog that opens when compressing files,
also describes the workers needed to execute the work for compression
"""
import os

from PyQt6.QtCore import QRunnable, QThreadPool, QObject, QEvent, pyqtSignal
from PyQt6.QtGui import QScreen, QResizeEvent, QColorConstants, QBrush, QTextCursor, QTextCharFormat
from PyQt6.QtWidgets import QScrollArea, QSpinBox, QVBoxLayout,  QSizePolicy, QGridLayout, QTextEdit, QDialog,QFrame, QLabel, QWidget, QStackedLayout

from controller.widgets.file_tile_widget import FileTile
from controller.helpers.api_file_processor import get_full_image
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
        self.setGeometry(1000, 500, 300, 300)
        self.setSizeGripEnabled(True)
        self.quality_input_spinbox = quality_input_spinbox
        
        layout = QVBoxLayout(self)
        self.setLayout(layout)
        primary_widget = QScrollArea(self)
        primary_widget.setWidgetResizable(True)
        layout.addWidget(primary_widget)

        self.thread_pool = QThreadPool()
        self.total_files = len(file_tile_list)
        # build file display grid and horizontal labels
        grid_widget = QWidget()
        primary_widget.setWidget(grid_widget)
        grid_layout = QGridLayout(grid_widget) 
        grid_layout.setSpacing(10)
        grid_layout.addWidget(
            QLabel("File ID"), 0,0 
        )
        grid_layout.addWidget(
            QLabel("File size"), 0,1 
        )
        grid_layout.addWidget(
            QLabel("Steps to do"), 0,2 
        )
        
        compression_value = self.quality_input_spinbox.value()
        for row_index, file_tile in enumerate(file_tile_list):
            row_index = row_index+1
            grid_layout.addWidget(
                QLabel(str(file_tile.file_id)),
                row_index, 0
            )

            grid_layout.addWidget(
                QLabel(str(file_tile.calculated_size)+file_tile.size_type),
                row_index, 1
            )
            progressWordBox = ProgressWordBox()
            grid_layout.addWidget(
                progressWordBox,
                row_index, 2
            )
            grid_layout.setRowMinimumHeight(row_index, progressWordBox.y())
            line = QFrame()
            line.setFrameStyle(QFrame.Shape.HLine)
            line.setLineWidth(1)
            row_index += 1
            
            # run compresssor for file_tile
            compressor_worker = CompressingFileThreadWorker(file_tile, compression_value, progressWordBox)
            compressor_worker.workerSingals.finished.connect(self.if_done)
            self.thread_pool.start(compressor_worker)
        grid_layout.setColumnStretch(0, 0)
        grid_layout.setColumnStretch(1, 0)
        grid_layout.setColumnStretch(2, 0)
        self.exec()
        
    def if_done(self):
        """Checks if we are done compressing everything and if so, what to do next
        """
        self.done_count += 1
        if self.done_count != self.total_files:
            return
        print("done")

class ProgressWordBox(QLabel):
    steps =[
        "Querying Hydrus API",
        "Compressing",
        "Sending to Hydrus",
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
            self.setStyleSheet("color: green;")
        else:
            self.setText(self.steps[self.working_step])
            self.setStyleSheet("color: orange;")
        
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
        image = get_full_image(self.file_tile.file_id)
        self.progress_box.step_forward()
        with image as open_image:
            file_path = constants.LOCAL_TEMP_IMAGE_LOCATION+str(self.file_tile.file_id)+\
                "."+open_image.format.lower()
            open_image.save(fp=file_path,
                    quality=self.compression_value,
                    optimize=True,
                    format=open_image.format)
            self.progress_box.step_forward()
        os.remove(file_path)
        self.workerSingals.finished.emit()