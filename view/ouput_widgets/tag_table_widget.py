from collections import Counter

from PyQt6.QtCore import QObject, Qt, QThreadPool, pyqtSignal
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView,QHBoxLayout, QVBoxLayout, QGraphicsView, QLabel, QPushButton, QSpinBox

from controller.output.tag_table_controller import TagTableController
class TagTableRow(QTableWidgetItem):
    pass

class TagTableWidget(QTableWidget):
    build_file_grid_emitter = pyqtSignal()
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.tag_table_controller = TagTableController(self)
        
        self.horizontalHeader().setHidden(True)
        self.verticalHeader().setHidden(True)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        self.itemSelectionChanged.connect(self.tag_table_controller.on_selection_change)
        self.itemDoubleClicked.connect(self.tag_table_controller.item_double_clicked)
        
        self.related_tag_counter = Counter()
        
    def update_tags(self, tag_counter:Counter, filetile_tag_pairlist:[]):
            self.tag_table_controller.update_tags(tag_counter, filetile_tag_pairlist)
            
    def create_tag_table_row(self, string_val:str):
        new_row = TagTableRow(string_val)
        return new_row
    
    
class TagTableRow(QTableWidgetItem):
    def __init__(self, tag_string):
        super().__init__()
        self.setText(tag_string)
        self.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsUserCheckable)
    
        self.setToolTip("Double click me to select all files with my tag, click elsewhere to get back to normal")
    
    def set_tag_n_count(self, tag, count):
        self.tag = tag
        self.count = count
        