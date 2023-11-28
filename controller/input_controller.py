""" Controller for input plane, processes user input and then calls the relevant api model. 
    Finally calls the output_controller for display
"""
# pylint: disable=E0611
import typing
from PyQt6 import QtCore
from PyQt6.QtCore import QObject, pyqtSignal, Qt
from PyQt6.QtWidgets import QLabel, QLineEdit, QHBoxLayout, QPushButton, QDialog, QVBoxLayout, QWidget

import models.settings as settings
from models import hydrus_api

class InputController(QObject):
    """Class to define functions for the controller and to be used to be passed to the intercontroller comms
    """
    
    get_files_onclick_complete = pyqtSignal()
    api_file_objects = []

    def __init__(self) -> None:
        super().__init__()
        try:
            settings.get_api_info()
        except ValueError as e:
            self.warning(f"Couldnt get your info, check settings: {e}")
        
    def warning(self, reason:str):
        """Creates a warning popup with given reason

        Args:
            reason (str): Text to be put into warning box
        """
        warning_window = QDialog()
        warning_window.setWindowTitle("Warning!!!!!")
        warning_window_layout = QVBoxLayout()
        warning_window.setLayout(warning_window_layout)


        reason_label = QLabel(reason)
        warning_window_layout.addWidget(reason_label)

        close_button = QPushButton('Close', warning_window)
        close_button.clicked.connect(warning_window.accept)
        warning_window_layout.addWidget(close_button)
        
        warning_window.exec()
        return warning_window

    def get_files_onclick(self, 
            max_file_size: int,
            size_type: str,
            get_imgs: bool,
            get_vids: bool,
            get_archive : bool,
            get_inbox : bool, 
    ):
        """ Process chosen settings and make the api call. 
            Finally pass to output controller for output display
        Args:
            max_file_size (int): number for max file size
            size_type (str): descriptor for max file size number
            get_imgs (bool): to get imgs or not
            get_vids (bool): to get vids or not
            get_inbox (bool): if should get inbox stuff
            get_archive (bool): if should get archive stuff
        """
        self.max_file_size = max_file_size
        self.size_type = size_type
        self.get_imgs = get_imgs
        self.get_vids = get_vids
        self.get_inbox = get_inbox
        self.get_archive = get_archive

        tags_list = [
                "system:filesize > "+str(max_file_size) + " "+ size_type,
                ]
        
        try:
            hydrus_key, api_port = settings.get_api_info()
        except ValueError as e:
            self.warning(str(e))
            return
        
        if get_imgs:
            tags_list.append("system:filetype is image")
        if get_vids:
            tags_list.append("system:filetype is video")
        if get_archive and get_inbox:
            tags_list.append("system:everything")
        elif get_inbox:
            tags_list.append("system:inbox")
        elif get_archive:
            tags_list.append("system:archive")
        if not get_imgs and not get_vids:
            self.warning("Did not select any media to get")
            return
        if not get_inbox and not get_archive:
            self.warning("Did not select inbox or archive")
            return

        # sets the file_metadata and emits signal for intercontroller_comm to pass to output controller
        self.api_files_metadata = hydrus_api.get_filtered_files_metadata_from_api(tags_list)
        self.get_files_onclick_complete.emit()
        
    def open_config_menu(self):
        """Function to be called when making a popup for the config menu
        """
        UserConfigWindow().show()

class UserConfigWindow(QDialog):
    """ Defines a window for display when open config menu is clicked

    Args:
        QDialog (_type_): inhereited parent
    """
    def __init__(self) -> None:
        super().__init__()
        self.setModal(True)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setWindowTitle("Set user information")
        config_window_layout = QVBoxLayout()
        self.setLayout(config_window_layout)


        hydrus_key_label = QLabel("Enter the Hydrus API key")
        config_window_layout.addWidget(hydrus_key_label)
        self.hydrus_key_input = QLineEdit()
        config_window_layout.addWidget(self.hydrus_key_input)

        api_label = QLabel("Enter the API port")
        config_window_layout.addWidget(api_label)
        self.api_input = QLineEdit()
        config_window_layout.addWidget(self.api_input)
        

        status_label = QLabel("")
        self.status_label = status_label
        status_label_basic_styling = "text-align: center; padding: 10px;"
        config_window_layout.addWidget(status_label)

        button_layout = QHBoxLayout()
        
        # tries to get existing values
        hydrus_key, api_port = None, None
        try:
            hydrus_key, api_port = settings.get_api_info()
            if hydrus_key is not None: 
                self.hydrus_key_input.setText(hydrus_key)
            if api_port is not None:
                self.api_input.setText(str(api_port))
        except ValueError as e:
            pass

        remember_button = QPushButton("Remember these values")
        self.remember_button = remember_button
        button_layout.addWidget(remember_button)
        def memorize_values():
            """Attempts to memorize the values and error handling for when it goes wrong
            """
            hydrus_key = self.hydrus_key_input.text().strip()
            api_port = self.api_input.text().strip()
            if hydrus_key == "" and api_port == "":
                status_label.setText("No values set")
                status_label.setStyleSheet(status_label_basic_styling+"background-color: orange")
                return
            if hydrus_key == "":
                status_label.setText("Missing hydrus key")
                status_label.setStyleSheet(status_label_basic_styling+"background-color: red")
                return
            if api_port == "":
                status_label.setText("Missing api port")
                status_label.setStyleSheet(status_label_basic_styling+"background-color: red")
                return
            
            try: 
                api_port = int(api_port)
            except ValueError:
                status_label.setText("Need numeric value for port")
                status_label.setStyleSheet(status_label_basic_styling+"background-color: red")
                return
            try:
                settings.set_api_info(hydrus_key_in=hydrus_key, api_port_in=api_port)
                status_label.setText("Values set!")
                status_label.setStyleSheet(status_label_basic_styling+"background-color: lightgreen")
                return
            except ValueError as error:
                status_label.setText(error.args[0])
                status_label.setStyleSheet(status_label_basic_styling+"background-color: red")
                return
        remember_button.clicked.connect(memorize_values)

        close_button = QPushButton('Close', self)
        self.close_button = close_button
        close_button.clicked.connect(self.accept)
        button_layout.addWidget(close_button)

        config_window_layout.addLayout(button_layout)
