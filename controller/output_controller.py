"""Is the right side of the primary screen, should deal with calculating everything needed to setup the table for the view
"""
from PyQt6.QtCore import QObject, Qt
from PyQt6.QtWidgets import QGridLayout, QWidget, QVBoxLayout, QLabel
from models.file_model import FileModel
class OutputController(QObject):
    """Calculates anything needed for the output/right view

    Args:
        QObject (_type_): of type qobj so we can borrow the signials and slots mechanisms to pass data between controllers
    """
    file_grid = None
    
    def __init__(self,
        file_grid_in: QGridLayout):
        super().__init__()
        self.file_grid = file_grid_in
        
    def set_file_options(self, 
        max_file_size_in: int,
        size_type_in: str,
    ):
        self.max_file_size = int(max_file_size_in)
        self.size_type = size_type_in
        
        
    def build_file_table(self, file_list:list[FileModel]):
        for file in file_list:
            file_widget = QWidget()
            file_widget_layout = QVBoxLayout()
            file_widget.setLayout(file_widget_layout)
            
            image = QLabel()
            image.setPixmap(file.pixmap)
            image.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            text = QLabel(str(file.size_bytes) + " " + file.file_type)
            text.setAlignment(Qt.AlignmentFlag.AlignCenter)

            file_widget_layout.addWidget(image)
            file_widget_layout.addWidget(text)
            
            self.file_grid.addWidget(file_widget)