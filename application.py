"""Main application function to be called
"""
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QSplitter

from view import input_view, output_view

#origin source
# https://upload.wikimedia.org/wikipedia/commons/7/74/%22I_Got_an_Idea%5E_If_it%27s_Good...I%27ll_Cash_In%22_-_NARA_-_514560_-_retouched.jpg
# https://commons.wikimedia.org/wiki/Category:Large_images 



# from PIL import Image

# image = Image.open("origin.jpg")

# # Compress and save the image

# image.save("pil_origin.jpg", optimize=True, quality=85)

#hydrus key c87559638ca2aaebe9ec109248d290d7b96be20d4cbc5479cc7ee555289fa5dd
# http://localhost:45869/
# will be diff per user
import intercontroller_comm

class MainApp(QMainWindow):
    """Primary class, uses QT as a base

    Args:
        QMainWindow (_type_): needed to be a QT application
    """
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Hydrus Compressor")
        self.setGeometry(100, 100, 800, 400)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        left_pane = input_view.InputWindow()
        right_pane = output_view.OutputWindow()

        intercontroller_comm.connect_input_output_controllers(
                left_pane.input_controller,
                right_pane.output_controller)

        splitter.addWidget(left_pane)
        splitter.addWidget(right_pane)        
        splitter.setStretchFactor(0, 1) 
        splitter.setStretchFactor(1, 50)  

        self.setCentralWidget(splitter)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
