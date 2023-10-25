
import sys
import typing
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import QThread, QThreadPool, Qt, QEvent
from PyQt6.QtGui import QTextDocument, QResizeEvent, QColorConstants, QBrush, QTextCursor, QTextCharFormat
from PyQt6.QtWidgets import QScrollArea, QSizePolicy, QVBoxLayout,  QSizePolicy, QGridLayout, QTextEdit, QDialog,QFrame, QLabel, QWidget, QStackedLayout


from widgets.file_display_tile_widget import FileDisplayTile

class FileCompressingProgressWindow(QDialog):
    def __init__(self, file_tile_list:list[FileDisplayTile]):
        super().__init__()
        self.setWindowTitle("File Compressing Progress Window")
        self.setGeometry(100, 100, 300, 300)
        
        # Set a layout for this widget
        layout = QVBoxLayout(self)
        self.setLayout(layout)
        
        primary_widget = QScrollArea(self)
        primary_widget.setWidgetResizable(True)
        layout.addWidget(primary_widget)

        # build file display grid
        grid_layout = QGridLayout(primary_widget) 
        grid_layout.addWidget(
            QLabel("File ID"), 0,0 
        )
        grid_layout.addWidget(
            QLabel("File size"), 0,1 
        )
        grid_layout.addWidget(
            QLabel("Steps to do"), 0,2 
        )
        
        for row_index, file_tile in enumerate(file_tile_list):
            row_index = row_index+1
            grid_layout.addWidget(
                QLabel(str(file_tile.file_obj.file_id)),
                row_index, 0
            )

            grid_layout.addWidget(
                QLabel(str(file_tile.calculated_size)+file_tile.file_obj.size_type),
                row_index, 1
            )
            progressWordBox = ProgressWordBox()
            grid_layout.addWidget(
                progressWordBox,
                row_index, 2
            )

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

        
        
    
# class CompressingFileRow(QWidget):
#     def __init__(self,
#             file_id: str,
#             file_size: str,
#                  ) -> None:
#         super().__init__()
        
# class CompressingFileThreadWorker(QThread):
#     def __init__(self) -> None:
#         super().__init__()