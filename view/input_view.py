"""View for the left side of the panel. Should be where the user makes all their inputs then gives inputs to input_controller when button pressed
"""
import typing
from PyQt6 import QtGui
from PyQt6.QtGui import QCloseEvent, QResizeEvent
from PyQt6.QtWidgets import QCheckBox, QWidget, QVBoxLayout, QPushButton
from PyQt6.QtWidgets import QLabel, QComboBox, QSpinBox, QHBoxLayout, QGroupBox, QStackedWidget, QFrame

from view.input_function_widgets.compress_file_panel_widget import CompressingFilePanel
from controller.input_controller import InputController
from controller.utilities import file_compressor
import models.settings as settings

class InputWindow(QWidget):
    """Qwidget object to define the input window frame

    Args:
        QWidget (_type_): standard input for the qwidget
    """
    input_controller = None
    output_controller = None
    
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
        file_number_box.setMinimum(0)
        conditions_layout.addWidget(file_number_box)
        size_type_box = QComboBox()
        size_type_box.addItem("MB")
        size_type_box.addItem("GB")
        conditions_layout.addWidget(size_type_box)
        input_layout.addLayout(conditions_layout)


        
        checkbox_layout = QHBoxLayout()
        img_checkbox = QCheckBox('Images')
        img_checkbox.setChecked(True)
        # checkbox_layout.addWidget(img_checkbox)
        vid_checkbox = QCheckBox('Videos')
        vid_checkbox.setChecked(False)
        # checkbox_layout.addWidget(vid_checkbox)
        archive_checkbox = QCheckBox('Archive')
        archive_checkbox.setChecked(True)
        checkbox_layout.addWidget(archive_checkbox)
        inbox_checkbox = QCheckBox('Inbox')
        inbox_checkbox.setChecked(False)
        checkbox_layout.addWidget(inbox_checkbox)
        input_layout.addLayout(checkbox_layout)
                
        get_files_metadata_button.clicked.connect( lambda:
            self.input_controller.get_files_onclick(
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
        

        ##### panel to dynamically change for different settings
        panels_frame = QGroupBox("Operation inputs", self)
        input_layout.addWidget(panels_frame)
        panels_layout = QVBoxLayout()
        panels_frame.setLayout(panels_layout)
        
        panels_dropdown = QComboBox(self)
        self.panels_dropdown = panels_dropdown
        panels_layout.addWidget(panels_dropdown)
        panels_title = [
            "File compression settings",
            "test"
        ]
        panels_dropdown.addItems(panels_title)
        
        horizontal_line = QFrame(self)
        horizontal_line.setFrameShape(QFrame.Shape.HLine)  # Set frame shape to a horizontal line
        horizontal_line.setFrameShadow(QFrame.Shadow.Sunken)  # Set line style
        horizontal_line.setLineWidth(2)
        panels_layout.addWidget(horizontal_line)
        
        panels_stack_widget = QStackedWidget(self)
        self.panels_stack_widget = panels_stack_widget
        panels_layout.addWidget(panels_stack_widget)
        
        def panels_dropdown_changed(index=0):
            panels_stack_widget.setCurrentIndex(index)
        panels_dropdown.currentIndexChanged.connect(panels_dropdown_changed)
        
        self.compress_file_panel = CompressingFilePanel()
        self.input_controller.set_compress_file_panel_widget(self.compress_file_panel)
        panels_stack_widget.addWidget(self.compress_file_panel)
        panels_stack_widget.addWidget(QLabel("ooga"))
        
        panels_stack_widget.setCurrentIndex(-1)
        
    def close_save(self):
        settings.set_input_window_geometry(self.saveGeometry())