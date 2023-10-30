"""Custom redfine of the scene widget
"""
from PyQt6.QtWidgets import QGraphicsScene

from controller.widgets.file_tile_widget import FileTile

class FileDisplayScene(QGraphicsScene):
    """Redefines the scene used for the file display

    Args:
        QGraphicsScene (QGraphicsScene): inherited type
    """
    def mousePressEvent(self, event):
        """Intercept mouse press event for overriding

        Args:
            event (_type_): standard input event

        Returns:
            _type_: standard output event
        """
        items_at_click = self.items(event.scenePos())

        if len(items_at_click) == 0:
            for item in self.items():
                if isinstance(item, FileTile):
                    item.highlight_tile = False
                    item.setSelected(False)
                    item.update()
            
        return super().mousePressEvent(event)
    
    