from collections import Counter

from PyQt6.QtCore import QObject, Qt, QThreadPool, pyqtSignal
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView,QHBoxLayout, QVBoxLayout, QGraphicsView, QLabel, QPushButton, QSpinBox


class TagTableRow(QTableWidgetItem):
    pass

class TagTableWidget(QTableWidget):
    build_table_emitter = pyqtSignal()
    
    def __init__(self, parent):
        super().__init__(parent)
        self.horizontalHeader().setHidden(True)
        self.verticalHeader().setHidden(True)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        self.itemSelectionChanged.connect(self.on_selection_change)
        self.itemDoubleClicked.connect(self.item_double_clicked)
        
        self.related_tag_counter = Counter()

    def pass_tag_info(self, tag_counter:Counter, filetile_tag_pairlist:[]):
        self.tag_counter = tag_counter
        self.filetile_tag_pairlist = filetile_tag_pairlist
        
    
    def build_tag_table(self, tag_counter):
        i = 0
        self.setRowCount(len(tag_counter))  # Set number of rows
        self.setColumnCount(2)
        for tag in tag_counter.keys():
            tag_sentence = TagTableRow(f"{tag}({tag_counter[tag]})")
            tag_sentence.set_tag_n_count(tag, tag_counter[tag])
            self.setItem(i, 0, tag_sentence)
            tag_count = TagTableRow(str(tag_counter[tag]))
            self.setItem(i, 1, tag_count)
            i += 1
        self.setColumnHidden(1, True)
        self.sortItems(1, Qt.SortOrder.DescendingOrder)
        
    def item_double_clicked(self, row_item:QTableWidgetItem):
        row = row_item.row()
        
        tag_row = self.takeItem(row, 0)
        selected_tag = tag_row.tag 
        self.related_tag_counter = Counter()
        # now build related_tag_counter for new display
        for tile, tags in self.filetile_tag_pairlist:
            tile.hide()
            if selected_tag in tags:
                tile.show()
                for tag in tags:
                    self.related_tag_counter[tag] += 1
                
        self.build_tag_table(self.related_tag_counter)
        
        self.build_table_emitter.emit()
    
    def on_selection_change(self):
        selected = self.selectedIndexes()
        
        if not selected:
            # if nothing selected then reset all tiles and tag rows
            self.build_tag_table(self.tag_counter)
            for tile, tags in self.filetile_tag_pairlist:
                tile.show()
class TagTableRow(QTableWidgetItem):
    def __init__(self, text):
        super().__init__()
        self.setText(text)
        self.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsUserCheckable)
    
        self.setToolTip("Double click me to select all files with my tag, click elsewhere to get back to normal")
    def set_tag_n_count(self, tag, count):
        self.tag = tag
        self.count = count
        