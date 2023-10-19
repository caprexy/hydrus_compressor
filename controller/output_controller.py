"""Is the right side of the primary screen, should deal with calculating everything needed to setup the table for the view
"""
from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
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
        
        
    def build_file_table(self, file_list:list[FileModel]):
        """Takes the file list or file objects from input controller's calls and turns it into a list

        Args:
            file_list (list[FileModel]): given file objects
        """
        print("displaying" , file_list)
        
        # logic to build the  table
        self.file_table.setRowCount(2)
        self.file_table.setColumnCount(2)
        for row_num, file in enumerate(file_list):
            file_id = QTableWidgetItem(str(file.file_id))
            file_type = QTableWidgetItem(file.file_type)
            extension = QTableWidgetItem(file.extension)
            size_bytes = QTableWidgetItem(file.size_bytes)
            display_tags = QTableWidgetItem(str(file.display_tags))
            print(file_id.text())
            self.file_table.setItem(row_num, 0, file_id)
            self.file_table.setItem(row_num, 1, file_type)
        
        self.file_table.show()