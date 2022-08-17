from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton)
from PyQt6.QtCore import Qt, QSize


class AnalysisWidget(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.left_box = QVBoxLayout()
        self.left_box.addWidget(QLabel("Very long text indeed."))
        self.left_box.addWidget(QLabel("Very long text indeed."))
        
        self.right_box = QVBoxLayout()
        self.right_box.addWidget(QPushButton("Hi !"))
        self.right_box.addWidget(QPushButton("Hi too !"))
        
        self.h_box = QHBoxLayout()
        self.h_box.addLayout(self.left_box)
        self.h_box.addLayout(self.right_box)

        self.setLayout(self.h_box)