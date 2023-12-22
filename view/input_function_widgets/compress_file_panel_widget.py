import typing
from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCloseEvent, QResizeEvent
from PyQt6.QtWidgets import QCheckBox, QWidget, QVBoxLayout, QPushButton
from PyQt6.QtWidgets import QLabel, QComboBox, QSpinBox, QHBoxLayout, QSizePolicy
from PyQt6.QtWidgets import QWidget, QSizePolicy, QComboBox, QGridLayout, QStackedWidget ,QButtonGroup,QSizePolicy , QHBoxLayout, QVBoxLayout, QCheckBox, QLabel, QRadioButton , QSpinBox

from controller.utilities import file_compressor
import models.settings as settings

class CompressingFilePanel(QWidget):
    """Qwidget object to define the panel that contains all compression file options

    Args:
        QWidget (_type_): standard input for the qwidget
    """
    
    def __init__(self):
        super().__init__()
        
        panel_layout = QVBoxLayout()
        self.setLayout(panel_layout)
        
        self.compression_settings = CompressionSettingsWidget()
        panel_layout.addWidget(self.compression_settings)
        
        compress_button = QPushButton("Compress selected files")
        panel_layout.addWidget(compress_button)
        compress_button.clicked.connect(self.compress_selected_files)
        
    def close_save(self):
        settings.set_input_window_geometry(self.saveGeometry())
        
    
    def set_file_grid_view_controller(self, file_grid_view_controller):
        self.file_grid_view_controller = file_grid_view_controller
        
    def compress_selected_files(self):
        """Called when pressing the compress selected files button
        """
        selected_file_tiles = self.file_grid_view_controller.get_selected_tiles()
        if selected_file_tiles == [] or selected_file_tiles is None:
            return
        file_compressor.FileCompresser(selected_file_tiles, self.compression_settings)
        
class PercentageWidget(QWidget):
    pass
class PixelsWidget(QWidget):
    pass

class CompressionSettingsWidget(QWidget):
    
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
        
        retain_size_when_hidden_policy = QSizePolicy()
        retain_size_when_hidden_policy.setRetainSizeWhenHidden(True)
        parent_resize_widget.setSizePolicy(retain_size_when_hidden_policy)
        
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
        self.button_group = button_group
        pixels_button = QRadioButton("Resize by Pixels")
        self.percentage_button = QRadioButton("Resize by Percentage")
        button_group.addButton(pixels_button, 0)
        per_or_pix_layout.addWidget(pixels_button)
        button_group.addButton(self.percentage_button, 1)
        per_or_pix_layout.addWidget(self.percentage_button)
        resize_layout.addLayout(per_or_pix_layout)
        
        self.percentage_button.setChecked(settings.should_resize_by_percentage)
        pixels_button.setChecked(not settings.should_resize_by_percentage)

        # resize by pixels widget
        pixels_widget = PixelsWidget()
        self.pixels_widget = pixels_widget
        resize_layout.addWidget(pixels_widget)
        pixels_widget.setSizePolicy(retain_size_when_hidden_policy)
        
        # resize by percentage widget
        percentage_widget = PercentageWidget()
        self.percentage_widget = percentage_widget
        resize_layout.addWidget(percentage_widget)
        percentage_widget.setSizePolicy(retain_size_when_hidden_policy)
        
        # setup radio group show/hide
        radio_stacked_widget = QStackedWidget(self)
        radio_stacked_widget.addWidget(pixels_widget)
        radio_stacked_widget.addWidget(percentage_widget)
        resize_layout.addWidget(radio_stacked_widget)
        def on_button_clicked(index=0):
            # Show the corresponding widget in the QStackedWidget when a button is clicked
            radio_stacked_widget.setCurrentIndex(index)
        button_group.idClicked.connect(on_button_clicked)
        radio_stacked_widget.setCurrentIndex(settings.should_resize_by_percentage)
        
        layout.addWidget(parent_resize_widget)
        
    
    def get_settings(self):
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
        
        self.height_spinbox = height_spinbox
        self.width_spinbox = width_spinbox
        self.res_combobox = res_combobox