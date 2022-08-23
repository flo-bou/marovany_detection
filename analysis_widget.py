from PyQt6.QtWidgets import (QWidget, QLabel, QLayout, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy)
# from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


class AnalysisWidget(QWidget):
    
    def __init__(self, path):
        super().__init__()
        # print("devicePixelRatio", self.devicePixelRatio())
        
        self.left_box = QVBoxLayout()
        # self.left_box.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)
        self.left_box.addWidget(QLabel("Very long text indeed."))
        self.left_box.addWidget(self.create_img_label(path))
        
        self.right_box = QVBoxLayout()
        self.right_box.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.right_box.addWidget(QPushButton("Hi !"))
        self.right_box.addWidget(QPushButton("Hi too !"))
        
        self.main_box = QHBoxLayout()
        self.main_box.addLayout(self.left_box)
        self.main_box.addLayout(self.right_box)

        size_policy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        self.setSizePolicy(size_policy)
        self.setLayout(self.main_box)
        self.adjustSize()
        # print(id(self), "left_box sizehint:", str(self.left_box.sizeHint()))
        # print(id(self), "left_box geometry:", str(self.left_box.geometry()))
        # print(id(self), "right_box sizehint:", str(self.right_box.sizeHint()))
        # print(id(self), "right_box geometry:", str(self.right_box.geometry()))
        print(id(self), "AnalysisWidget size:", str(self.size()))
        print(id(self), "AnalysisWidget sizePolicy:", self.sizePolicy().horizontalStretch(), self.sizePolicy().verticalStretch())

        
    def create_img_label(self, path):
        img = QPixmap()
        if not img.load(path):
            print(id(self), "img loading failed")
        print(id(self), "img size:", str(img.size()))
        img_label = QLabel()
        # print(id(self), "img_label sizeHint:", str(img_label.sizeHint()))
        img_label.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred))
        # print("label sizeHint:", str(img_label.sizeHint()))
        img_label.setPixmap(img)
        print(id(self), "img_label sizeHint:", str(img_label.sizeHint()))
        img_label.adjustSize()
        # img_label.setGeometry()
        print(id(self), "img_label size:", str(img_label.size()))
        return img_label
    
    def sizeHint(self):
        return self.size()