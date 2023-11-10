import typing
from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget, QComboBox, QGridLayout, QDialog ,QButtonGroup, QHBoxLayout, QVBoxLayout, QCheckBox, QLabel, QRadioButton , QSpinBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush, QColor

import models.settings as settings

class PercentageWidget(QWidget):
    pass
class PixelsWidget(QWidget):
    pass

class OutputSettingsDialog(QDialog):
    
    def __init__(self) -> None:
        super().__init__()
        
        # get the user_model and grab options from there
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # quality setting
        quality_layout = QHBoxLayout()
        quality_label = QLabel("Compressed Image quality: ")
        quality_layout.addWidget(quality_label)
        quality_input = QSpinBox()
        quality_input.setMinimum(0)
        quality_input.setMaximum(95)
        quality_input.setValue(settings.compressed_img_quality)
        def update_img_quality(new_val):
            settings.compressed_img_quality = new_val
        quality_input.valueChanged.connect(update_img_quality)
        quality_layout.addWidget(quality_input)
        self.quality_input = quality_input
        layout.addLayout(quality_layout)
        
        # resize checkbox
        resize_checkbox = QCheckBox("Resize?")
        resize_checkbox.setChecked(settings.should_resize)
        def update_should_resize(new_val):
            settings.should_resize = new_val
        resize_checkbox.stateChanged.connect(update_should_resize)
        layout.addWidget(resize_checkbox)
        
        parent_resize_widget = QWidget()
        resize_layout = QVBoxLayout()
        parent_resize_widget.setLayout(resize_layout)
        def resize_visiblility(should):
            if should == False:
                parent_resize_widget.hide()
                return
            parent_resize_widget.show()
        resize_visiblility(settings.should_resize)
        resize_checkbox.stateChanged.connect(resize_visiblility)
                
        # in percentage or pixels radio group
        per_or_pix_layout = QHBoxLayout()
        button_group = QButtonGroup()
        pixels_button = QRadioButton("Resize by Pixels")
        percentage_button = QRadioButton("Resize by Percentage")
        button_group.addButton(pixels_button, 1)
        button_group.addButton(percentage_button, 2)
        def percentage_button_clicked():
            settings.should_resize_by_percentage = True
        def pixel_button_clicked():
            settings.should_resize_by_percentage = False
        percentage_button.clicked.connect(percentage_button_clicked)
        pixels_button.clicked.connect(pixel_button_clicked)
        percentage_button.setChecked(settings.should_resize_by_percentage)
        pixels_button.setChecked(not settings.should_resize_by_percentage)
        self.percentage_button = percentage_button
        
        per_or_pix_layout.addWidget(pixels_button)
        per_or_pix_layout.addWidget(percentage_button)
        resize_layout.addLayout(per_or_pix_layout)

        # resize by pixels widget
        pixels_widget = PixelsWidget()
        self.pixels_widget = pixels_widget
        resize_layout.addWidget(pixels_widget)
        
        # resize by percentage widget
        percentage_widget = PercentageWidget()
        self.percentage_widget = percentage_widget
        resize_layout.addWidget(percentage_widget)
        
        # add functionality to radio buttons of hide or show
        def toggle_pixels(checked):
            if checked:
                pixels_widget.show()
                percentage_widget.hide()
                return
            pixels_widget.hide()
            percentage_widget.show()
        pixels_button.toggled.connect(toggle_pixels)
        toggle_pixels(not settings.should_resize_by_percentage)
        
        layout.addWidget(parent_resize_widget)
        
    def settings(self):
        compression_level = self.quality_input.value()
        use_percentage = self.percentage_button.isChecked()
        resize_percentage = self.percentage_widget.percentage_spinbox.value()
        max_height = self.pixels_widget.height_spinbox.value()
        max_width = self.pixels_widget.width_spinbox.value()
        
        return compression_level, use_percentage, resize_percentage, max_width, max_height

class PercentageWidget(QWidget):
    """This widget will hold all the options if resizing by percentage
    """
    def __init__(self) -> None:
        super().__init__()
        
        percentage_layout = QVBoxLayout(self)
        
        # spin box for percent selection
        percentage_spin_layout = QHBoxLayout()
        percentagle_label = QLabel("Resize height and width by: ")
        percentage_spin_layout.addWidget(percentagle_label)
        percentage_spinbox = QSpinBox()
        percentage_spinbox.setMinimum(1)
        percentage_spinbox.setMaximum(1000)
        percentage_spinbox.setValue(settings.resize_by_percentage)
        def update_resize_percentage(new_val):
            settings.resize_by_percentage = new_val
        percentage_spinbox.valueChanged.connect(update_resize_percentage)
        percentage_spin_layout.addWidget(percentage_spinbox)
        percentagle_label = QLabel("%")
        percentage_spin_layout.addWidget(percentagle_label)
        
        percentage_layout.addLayout(percentage_spin_layout)
        
        self.percentage_spinbox = percentage_spinbox

class PixelsWidget(QWidget):
    """If resizing by pixels, then here are the possible options
    """
    def __init__(self) -> None:
        super().__init__()
        pixels_layout = QGridLayout(self)
        
        row = 0
        height_label = QLabel("Max possible height: ")
        pixels_layout.addWidget(height_label, row, 0)
        
        height_spinbox = QSpinBox()
        height_spinbox.setMinimum(1)
        height_spinbox.setMaximum(10000)
        height_spinbox.setValue(int(settings.resize_by_pixel_height))
        def update_resize_pixel_height(new_val):
            settings.resize_by_pixel_height = new_val
        height_spinbox.valueChanged.connect(update_resize_pixel_height)
        pixels_layout.addWidget(height_spinbox, row, 1)
        self.height_spinbox = height_spinbox
        
        row += 1
        width_label = QLabel("Max possible width: ")
        pixels_layout.addWidget(width_label, row, 0)
        
        width_spinbox = QSpinBox()
        width_spinbox.setMinimum(1)
        width_spinbox.setMaximum(10000)
        width_spinbox.setValue(int(settings.resize_by_pixel_width))
        def update_resize_pixel_width(new_val):
            settings.resize_by_pixel_width = new_val
        height_spinbox.valueChanged.connect(update_resize_pixel_width)
        pixels_layout.addWidget(width_spinbox, row, 1)
        self.width_spinbox = width_spinbox
        
        row += 1
        res_combobox = QComboBox()
        res_combobox.addItems([
                "<Use a standard size(WxH)>",
                "1980 x 1080",
                "2560 x 1440", 
                "3840 x 2160"
            ])
        
        def res(chosen_text):
            if chosen_text[0] == "<":
                return
            w,h = chosen_text.split(" x ")
            h = int(h)
            w = int(w)
            update_resize_pixel_height(h)
            height_spinbox.setValue(h)
            update_resize_pixel_width(w)
            width_spinbox.setValue(w)
        res_combobox.textActivated.connect(res)
        pixels_layout.addWidget(res_combobox, row, 0, 2,  1, Qt.AlignmentFlag.AlignCenter)
        self.hide()
        
        self.height_spinbox = height_spinbox
        self.width_spinbox = width_spinbox
        self.res_combobox = res_combobox