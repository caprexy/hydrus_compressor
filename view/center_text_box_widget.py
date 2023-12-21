"""Creates a rectangle/box with some text inside that is center justified. Auto finds a text size
"""
from PyQt6.QtWidgets import QGraphicsWidget
from PyQt6.QtGui import QColor, QFont

class CenterTextBox(QGraphicsWidget):
    """Widget that paints a rectangle and words inside the center of that rectangle

    Args:
        QGraphicsWidget (_type_): inherited class
    """
    def __init__(self, text, box_width, box_height):
        super().__init__()

        self.text = text
        self.box_width = box_width
        self.box_height = box_height

    def calculateFontSize(self, painter) -> int:
        """Determines what font size to use by checking if the font + box text is larger than avalible space
        Args:
            painter (_type_): _description_
        Returns:
            int: font size
        """
        font_size = 30

        while font_size > 0:
            
            # Using font + text, determine how big of a rectangle needed to contain
            # if too big, then decrease font
            font = QFont("Arial", font_size)
            painter.setFont(font)
            text_rect = painter.boundingRect(0, 0, self.box_width, self.box_height, 0, self.text)

            if text_rect.width() <= self.box_width and text_rect.height() <= self.box_height:
                return font_size

            font_size -= 1  # Decrease the font size

        return 0  # Font size is too small; text doesn't fit

    def paint(self, painter, option, widget=None):
        """Overloading of the QGraphicsWidget paint string. See original
        """
        box_x = 0
        box_y = 0
        
        # draw rectangle with colors
        painter.setPen(QColor(0, 0, 0))  
        painter.setBrush(QColor(236, 236, 236 ))
        rect_w = self.box_width
        rect_h = self.box_height
        painter.drawRect(box_x, box_y, rect_w, rect_h)
        
        # draw the text
        painter.setPen(QColor(0, 0, 0))  # Set the pen color (outline color)
        painter.setBrush(QColor(255, 0, 0))  # Set the brush color (fill color)
        font_size = self.calculateFontSize(painter)
        if font_size > 0:
            font = QFont("Arial", font_size)
            painter.setFont(font)

            # Calculate the text's position to center it in the rectangle
            text_rect = painter.boundingRect(0, 0, self.box_width, self.box_height, 0, self.text)
            text_x = int(box_x + (self.box_width - text_rect.width()) / 2)
            text_y = int(box_y + (self.box_height - text_rect.height()) / 2 + text_rect.height())

            painter.drawText(text_x, text_y, self.text)
        else:
            painter.drawText(box_x, box_y, "Text doesn't fit")
