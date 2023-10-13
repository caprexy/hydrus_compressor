from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QLineEdit, QHBoxLayout, QPushButton, QDialog, QVBoxLayout

from models.user_model import UserInfo

userInfo = UserInfo()

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

    