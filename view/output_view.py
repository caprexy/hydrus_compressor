"""Right panel where the output/found files should be displayed.
"""
    
from PyQt6.QtWidgets import QTableWidget, QSplitter, QWidget,QHBoxLayout, QVBoxLayout, QGraphicsView, QLabel, QPushButton, QSpinBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush, QColor
from controller.output_controller import OutputController

from controller.widgets.file_display_scene_widget import FileDisplayScene
from controller.widgets.output_settings_widget import OutputSettingsDialog
from controller.widgets.tag_table_widget import TagTableWidget

class OutputWindow(QWidget):
    """Primary class for the right panel

    Args:
        QWidget (_type_): For qwidget import, standard
    """
    input_window = None
    output_controller = None
    table = None

    def __init__(self):
        super().__init__()
        
        output_layout = QHBoxLayout()
        self.setLayout(output_layout)
        main_splitter = QSplitter()
        output_layout.addWidget(main_splitter)

        # build file grid and buttons
        file_grid_widget = QWidget()
        filegrid_layout = QVBoxLayout()
        file_grid_view = QGraphicsView()
        file_grid_view.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.BoundingRectViewportUpdate)
        file_grid_view.setInteractive(True)
        filegrid_layout.addWidget(file_grid_view)

        file_grid_scene = FileDisplayScene()
        file_grid_scene.setBackgroundBrush(QBrush(QColor(230, 230, 230)))
        file_grid_view.setScene(file_grid_scene)
        file_grid_view.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        
        open_settings = QPushButton("Open image compression settings")
        filegrid_layout.addWidget(open_settings)
        settings_dialog = OutputSettingsDialog()
        def open_settings_widget():
            settings_dialog.show()
        open_settings.clicked.connect(open_settings_widget)
        
        compress_button = QPushButton("Compress selected files")
        filegrid_layout.addWidget(compress_button)
        file_grid_widget.setLayout(filegrid_layout)
        main_splitter.addWidget(file_grid_widget)

        #tag table
        tag_table = TagTableWidget(self)
        main_splitter.addWidget(tag_table)
        # tag_table.hide()
        

        self.output_controller = OutputController(
            self,
            file_grid_scene,
            file_grid_view,
            settings_dialog,
            tag_table
        )
        compress_button.clicked.connect(self.output_controller.compress_selected_files)



    def resizeEvent(self, event):
        """Should overload the existing resize event, tells us to rebuild the file table
        """
        self.output_controller.build_file_table()
        event.accept()
        