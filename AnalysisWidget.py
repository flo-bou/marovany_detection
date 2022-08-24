from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from PlotWidget import PlotWidget

class AnalysisWidget(QWidget):
    
    def __init__(self, path):
        super().__init__()
        # print("devicePixelRatio", self.devicePixelRatio())
        
        self.button_box = QVBoxLayout()
        self.button_box.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.button_box.addWidget(QPushButton("Hi !"))
        self.button_box.addWidget(QPushButton("Hi too !"))
        
        self.plot_box = QVBoxLayout()
        # self.left_box.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)
        self.plot_box.addWidget(QLabel("Very long text indeed."))
        # self.left_box.addWidget(self.create_img_label(path))
        self.plot_box.addWidget(PlotWidget())

        self.main_box = QHBoxLayout()
        self.main_box.addLayout(self.button_box)
        self.main_box.addLayout(self.plot_box)
        # print(id(self), "main_box geometry:", str(self.main_box.geometry()))

        self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        self.setLayout(self.main_box)
        # print(id(self), "AnalysisWidget size:", str(self.size()))
        print(id(self), "AnalysisWidget sizeHint:", str(self.sizeHint()))
        self.adjustSize()
        # print(id(self), "left_box sizehint:", str(self.left_box.sizeHint()))
        # print(id(self), "left_box geometry:", str(self.left_box.geometry()))
        # print(id(self), "right_box sizehint:", str(self.right_box.sizeHint()))
        # print(id(self), "right_box geometry:", str(self.right_box.geometry()))
        print(id(self), "AnalysisWidget size:", str(self.size()))
        # print(id(self), "AnalysisWidget sizePolicy:", self.sizePolicy().horizontalStretch(), self.sizePolicy().verticalStretch())

    
    def create_img_label(self, path):
        img = QPixmap()
        if not img.load(path):
            print(id(self), "img loading failed")
        print(id(self), "img size:", str(img.size()))
        img_label = QLabel()
        # print(id(self), "img_label sizeHint:", str(img_label.sizeHint()))
        img_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        # print("label sizeHint:", str(img_label.sizeHint()))
        img_label.setPixmap(img)
        print(id(self), "img_label sizeHint:", str(img_label.sizeHint()))
        img_label.adjustSize()
        # img_label.setGeometry()
        print(id(self), "img_label size:", str(img_label.size()))
        return img_label
    
    # def sizeHint(self):
    #     # size is fixed
    #     width = 1400
    #     height = 400
    #     return QSize(width, height)
