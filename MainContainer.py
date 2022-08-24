from PyQt6.QtWidgets import QWidget, QSizePolicy, QBoxLayout
from PyQt6.QtCore import QSize


class MainContainer(QWidget):

    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    
    
    def sizeHint(self):
        width = self.width()
        height = 0
        for child in self.children():
            # print(id(child), str(type(child).__name__) , "main_container child geometry:", str(child.geometry()))
            if not isinstance(child, QBoxLayout):
                if child.width() > width:
                    width = child.width()
                height = height + child.height()
        print(id(child), "main_container child sizehint:", width, height)
        return QSize(width, height)