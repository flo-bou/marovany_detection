from PyQt6.QtWidgets import (QWidget, QLabel, QScrollArea,
                            QVBoxLayout, QMainWindow)
from PyQt6.QtCore import Qt, QSize

from analysis_widget import AnalysisWidget


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        
        self.v_box = QVBoxLayout()
        self.v_box.addWidget(AnalysisWidget())

        # for i in range(50):
        #     label = QLabel("TextLabel " + str(i))
        #     self.v_box.addWidget(label)

        self.main_container = QWidget()
        self.main_container.setLayout(self.v_box)

        self.scroll_area = QScrollArea() # Scroll Area which contains the widgets, set as the centralWidget
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.main_container)

        self.setCentralWidget(self.scroll_area)
        # self.setGeometry(300, 100, 1200, 800)
        self.setWindowTitle('Scroll Area Demo')