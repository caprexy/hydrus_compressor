import typing
from PyQt6 import QtGui
from PyQt6.QtCore import Qt, QSize, QEvent
from PyQt6.QtWidgets import QAbstractSlider, QScrollBar, QWidget, QVBoxLayout, QGraphicsView

class FileGridView(QGraphicsView):
    widget_list = []
    widget_bounding_box_list = []
    old_widgets = []
    
    # def __init__(self):
    #     super().__init__()
    #     scroll_bar = self.verticalScrollBar()
    #     scroll_bar.valueChanged.connect(self.updateVisibleWidgets)
        

    # def updateVisibleWidgets(self):
    #     if self.widget_list is []:
    #         return
        
    #     for item in self.old_widgets:
    #         self.scene().removeItem(item)
            
    #     self.old_widgets = []    
    #     cur_rect = self.mapToScene(self.viewport().rect()).boundingRect()
    #     for index, bounding_box in enumerate(self.widget_bounding_box_list):
    #         if cur_rect.intersects(bounding_box) and self.widget_list[index].scene() is None:
    #             self.scene().addItem(self.widget_list[index])
    #             self.old_widgets.append(self.widget_list[index])

    # def resizeEvent(self, a0) -> None:
    #     self.updateVisibleWidgets()
    #     return super().resizeEvent(a0)
