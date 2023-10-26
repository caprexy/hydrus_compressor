"""View for the left side of the panel. Should be where the user makes all their inputs
"""
from PyQt6.QtWidgets import QCheckBox, QWidget, QVBoxLayout, QPushButton
from PyQt6.QtWidgets import QLabel, QComboBox, QSpinBox, QHBoxLayout

from controller.input_controller import InputController

class InputWindow(QWidget):
    """Qwidget object to define the input window frame

    Args:
        QWidget (_type_): standard input for the qwidget
    """
    input_controller = None
    
    def __init__(self):
        super().__init__()
        
        self.input_controller = InputController()
        
        input_layout = QVBoxLayout()
        self.setLayout(input_layout)

        
        get_files_metadata_button = QPushButton("Get all files following the conditions below")
        input_layout.addWidget(get_files_metadata_button)
        
        conditions_layout = QHBoxLayout()
        file_size_explain_label = QLabel("Get if greater than: ")
        conditions_layout.addWidget(file_size_explain_label)
        file_number_box = QSpinBox()
        file_number_box.setValue(10)
        conditions_layout.addWidget(file_number_box)
        size_type_box = QComboBox()
        size_type_box.addItem("MB")
        size_type_box.addItem("GB")
        conditions_layout.addWidget(size_type_box)
        input_layout.addLayout(conditions_layout)

        checkbox_layout = QHBoxLayout()
        file_size_explain_label = QLabel("Get if greater than: ")
        img_checkbox = QCheckBox('Images')
        img_checkbox.setChecked(True)
        checkbox_layout.addWidget(img_checkbox)
        vid_checkbox = QCheckBox('Videos')
        vid_checkbox.setChecked(False)
        checkbox_layout.addWidget(vid_checkbox)
        archive_checkbox = QCheckBox('Archive')
        archive_checkbox.setChecked(True)
        checkbox_layout.addWidget(archive_checkbox)
        inbox_checkbox = QCheckBox('Inbox')
        inbox_checkbox.setChecked(False)
        checkbox_layout.addWidget(inbox_checkbox)
        input_layout.addLayout(checkbox_layout)
        
        get_files_metadata_button.clicked.connect( lambda:
            self.input_controller.get_files_metadata(
                file_number_box.value(),
                size_type_box.currentText(),
                img_checkbox.isChecked(),
                vid_checkbox.isChecked(),
                archive_checkbox.isChecked(),
                inbox_checkbox.isChecked()
            ))

        
        config_button = QPushButton("Open config")
        config_button.clicked.connect(self.input_controller.open_config_menu)
        input_layout.addWidget(config_button)
