from collections import Counter

from PyQt6.QtCore import QObject, Qt, QThreadPool, pyqtSignal
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView,QHBoxLayout, QVBoxLayout, QGraphicsView, QLabel, QPushButton, QSpinBox


class TagTableController():
    related_tag_counter = None
    mechanical_selection_change = False
    def __init__(self, parent_tag_table_widget) -> None:
        super().__init__()
        self.parent_tag_table_widget = parent_tag_table_widget
    
    def update_tags(self, tag_counter: Counter,
                           filetile_tag_pairlist:[]):
        self.all_files_tag_counter = tag_counter
        self.filetile_tag_pairlist = filetile_tag_pairlist
        self.build_tag_table(self.all_files_tag_counter)

    
    def build_tag_table(self, tag_counter, selected_tag=None):
        self.mechanical_selection_change = True
        i = 0
        self.parent_tag_table_widget.clear()
        self.parent_tag_table_widget.setRowCount(len(tag_counter))  # Set number of rows
        self.parent_tag_table_widget.setColumnCount(2)
        self.parent_tag_table_widget.setColumnHidden(1, True)
        for tag in tag_counter.keys():
            # idk a better way to avoid a circulur import
            tag_sentence = self.parent_tag_table_widget.create_tag_table_row(f"{tag}({tag_counter[tag]})")
            tag_sentence.set_tag_n_count(tag, tag_counter[tag])
            self.parent_tag_table_widget.setItem(i, 0, tag_sentence)
            tag_count = self.parent_tag_table_widget.create_tag_table_row(str(tag_counter[tag]))
            self.parent_tag_table_widget.setItem(i, 1, tag_count)
            if tag is selected_tag:
                tag_sentence.setSelected(True)
            else:
                tag_sentence.setSelected(False)
            i += 1
        self.parent_tag_table_widget.sortItems(1, Qt.SortOrder.DescendingOrder)
        self.parent_tag_table_widget.update()
        
    def item_double_clicked(self, row_item:QTableWidgetItem):
        row = row_item.row()
        
        tag_row = self.parent_tag_table_widget.takeItem(row, 0)
        selected_tag = tag_row.tag 
        
        self.related_tag_counter = Counter()
        # now build related_tag_counter for new display
        for tile, tags in self.filetile_tag_pairlist:
            tile.hide()
            if selected_tag in tags:
                tile.show()
                for tag in tags:
                    self.related_tag_counter[tag] += 1
        
        self.build_tag_table(self.related_tag_counter, selected_tag)
        
        self.parent_tag_table_widget.build_file_grid_emitter.emit()
    
    def on_selection_change(self):
        if self.mechanical_selection_change:
            self.mechanical_selection_change = False
            return
        
        selected = self.parent_tag_table_widget.selectedIndexes()
        
        if not selected:
            # if nothing selected then reset all tiles and tag rows
            self.build_tag_table(self.all_files_tag_counter)
            for tile, tags in self.filetile_tag_pairlist:
                tile.show()