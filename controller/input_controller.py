""" Controller for input plane where user chooses their settings and such
"""
import json
import requests

# pylint: disable=E0611
from PyQt6.QtWidgets import QLabel, QLineEdit, QHBoxLayout, QPushButton, QDialog, QVBoxLayout

from models.user_model import UserInfo
import constants

userInfo = UserInfo()

def warning(reason:str):
    """Creates a warning popup with given reason

    Args:
        reason (str): Text to be put into warning box
    """
    warning_window = QDialog()
    warning_window.setWindowTitle("Warning!!!!!")
    warning_window_layout = QVBoxLayout()
    warning_window.setLayout(warning_window_layout)


    hydrus_key_label = QLabel(reason)
    warning_window_layout.addWidget(hydrus_key_label)

    close_button = QPushButton('Close', warning_window)
    close_button.clicked.connect(warning_window.accept)
    warning_window_layout.addWidget(close_button)
    
    warning_window.exec()

def get_files(
        max_file_size: int,
        size_type: str,
        get_imgs: bool,
        get_vids: bool,
        get_inbox : bool, 
        get_archive : bool,
):
    """ Once all inputs are given, the get files button is clicked and we pass in all information

    Args:
        max_file_size (int): number for max file size
        size_type (str): descriptor for max file size number
        get_imgs (bool): to get imgs or not
        get_vids (bool): to get vids or not
        get_inbox (bool): if should get inbox stuff
        get_archive (bool): if should get archive stuff
    """
    hydrus_key, api_port = userInfo.get_user_info()
    print(hydrus_key, api_port)
    if hydrus_key is None or api_port is None:
        warning("Missing either api port or hydrus key!")
        return    

    tags_list = [
            "system:filesize > "+str(max_file_size) + " "+ size_type,
            ]
    
    if get_imgs:
        tags_list.append("system:filetype is image")
    if get_vids:
        tags_list.append("system:filetype is video")
    if not get_imgs and not get_vids:
        warning("Did not select any media to get")
        return
    if not get_inbox and not get_archive:
        warning("Did not select inbox or archive")
        return

    res = requests.get(
        url=constants.LOCALHOST+str(api_port)+"/get_files/search_files",
        headers={
            constants.HYDRUS_APIKEY_PARAM : hydrus_key,
        },
        params={
            "tags" : json.dumps(tags_list)
        },
        timeout= 10
    )
    print(res.json())

def open_config_menu():
    config_window = QDialog()
    config_window.setWindowTitle("Set user information")
    config_window_layout = QVBoxLayout()
    config_window.setLayout(config_window_layout)


    hydrus_key_label = QLabel("Enter the Hydrus API key")
    config_window_layout.addWidget(hydrus_key_label)
    hydrus_key_input = QLineEdit()
    config_window_layout.addWidget(hydrus_key_input)

    api_label = QLabel("Enter the API port")
    config_window_layout.addWidget(api_label)
    api_input = QLineEdit()
    config_window_layout.addWidget(api_input)
    

    status_label = QLabel("")
    status_label_basic_styling = "text-align: center; padding: 10px;"
    config_window_layout.addWidget(status_label)

    button_layout = QHBoxLayout()

    remember_button = QPushButton("Remember these values")
    button_layout.addWidget(remember_button)
    def memorize_values():
        hydrus_key = hydrus_key_input.text().strip()
        api_port = api_input.text().strip()
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
        sucess = userInfo.set_user_info(hydrus_key=hydrus_key, api_port=api_port)

        if sucess:
            status_label.setText("Values set!")
            status_label.setStyleSheet(status_label_basic_styling+"background-color: lightgreen")
            return
        status_label.setText("Somehow failed")
        status_label.setStyleSheet(status_label_basic_styling+"background-color: red")
    remember_button.clicked.connect(memorize_values)

    close_button = QPushButton('Close', config_window)
    close_button.clicked.connect(config_window.accept)
    button_layout.addWidget(close_button)

    config_window_layout.addLayout(button_layout)

    config_window.exec()
    