from PyQt6.QtWidgets import QLabel, QLineEdit, QHBoxLayout, QPushButton, QDialog, QVBoxLayout, QWidget

def warning(reason:str):
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

def working(reason:str):
    """Creates a working popup with given reason. Uses open so less stop heavy

    Args:
        reason (str): Text to be put into warning box
    """
    working_window = QDialog()
    working_window.setWindowTitle("Working!!!!!")
    warning_window_layout = QVBoxLayout()
    working_window.setLayout(warning_window_layout)


    reason_label = QLabel(reason)
    warning_window_layout.addWidget(reason_label)

    close_button = QPushButton('Close', working_window)
    close_button.clicked.connect(working_window.accept)
    warning_window_layout.addWidget(close_button)
    
    working_window.open()
    return working_window