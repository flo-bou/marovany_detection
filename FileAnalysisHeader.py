from time import time

from PyQt6.QtWidgets import (QWidget, QLabel, 
                             QBoxLayout, QHBoxLayout, 
                             QPushButton, QSizePolicy)
from PyQt6.QtCore import Qt, QSize


class FileAnalysisHeader(QWidget):
    """Widget containing header of analysis widget, name of file and buttons
    """
    def __init__(self, fname: str, note: str, parent: QWidget):
        super().__init__()
        self.title_label = QLabel("File : " + fname + " ;")
        self.title_label.adjustSize()
        self.note_label = QLabel("Note : " + str(note))
        self.note_label.adjustSize()
        self.plot_btn = QPushButton("Plot")
        self.plot_btn.clicked.connect(parent.add_time_series_figure)
        self.plot_btn.adjustSize()
        self.params_btn = QPushButton("Params")
        self.params_btn.clicked.connect(parent.call_ParamDialog)
        self.params_btn.adjustSize()
        # self.options_btn = QPushButton("Options")
        # self.options_btn.clicked.connect(parent.delete_FileAnalysis)
        # self.options_btn.adjustSize()
        
        self.header_box = QHBoxLayout()
        self.header_box.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.header_box.addWidget(self.title_label)
        self.header_box.addWidget(self.note_label)
        self.header_box.addWidget(self.plot_btn)
        self.header_box.addWidget(self.params_btn)
        # self.header_box.addWidget(self.options_btn)

        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        self.setLayout(self.header_box)
        self.adjustSize()

    
    def sizeHint(self):
        width = 0
        height = 0
        for child in self.children():
            if not isinstance(child, QBoxLayout):
                width = width + child.width()
                if child.height() > height:
                    height = child.height()
        # print(id(self), "FileAnalysisHeader sizeHint :", width, height)
        return QSize(width, height)