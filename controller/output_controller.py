"""Is the right side of the primary screen, should deal with calculating everything needed to setup the table for the view
"""
from PyQt6.QtCore import QObject, Qt
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QSizePolicy, QAbstractScrollArea
from models.file_model import FileModel
class OutputController(QObject):
    """Calculates anything needed for the output/right view

    Args:
        QObject (_type_): of type qobj so we can borrow the signials and slots mechanisms to pass data between controllers
    """
    file_table = None
    
    def __init__(self,
        file_table_in: QTableWidget):
        super().__init__()
        self.file_table = file_table_in
        
    def set_file_options(self, 
        max_file_size_in: int,
        size_type_in: str,
    ):
        self.max_file_size = int(max_file_size_in)
        self.size_type = size_type_in
        
        
    def build_file_table(self, file_list:list[FileModel]):
        """Takes the file list or file objects from input controller's calls and turns it into a list

        Args:
            file_list (list[FileModel]): given file objects
        """
        print("displaying" , file_list)
        
        # logic to build the  table
        self.file_table.setSortingEnabled(True)
            
        self.file_table.setRowCount(len(file_list))
        self.file_table.setColumnCount(4)

        self.file_table.setHorizontalHeaderLabels(
            ["file id", "file type", "file extension", "file size"])
        
        # if want no horizontal scroll, might need to manually calculate sizes for cols
        for row_num, file in enumerate(file_list):
            file_id_item = QTableWidgetItem(str(file.file_id))
            file_type_item = QTableWidgetItem(file.file_type)
            extension_item = QTableWidgetItem(file.extension)
            
            size = 0
            #calculate MB or GB
            if self.size_type == "MB":
                size = file.size_bytes/1048576
            if self.size_type == "GB":
                size = file.size_bytes/1073741824
            size = round(size,2)
            size_item = QTableWidgetItem(str(size) + " " + self.size_type)
            
            self.file_table.setItem(row_num, 0, file_id_item)
            self.file_table.setItem(row_num, 1, file_type_item)
            self.file_table.setItem(row_num, 2, extension_item)
            self.file_table.setItem(row_num, 3, size_item)
        
        self.file_table.show()