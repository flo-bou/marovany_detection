import sys

from PyQt6.QtWidgets import (QWidget, QSlider, QLineEdit, QLabel, QPushButton, QScrollArea,QApplication,
                            QHBoxLayout, QVBoxLayout, QMainWindow)
from PyQt6.QtCore import Qt, QSize
from PyQt6 import QtWidgets, uic


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.scroll_area = QScrollArea() # Scroll Area which contains the widgets, set as the centralWidget
        self.widget = QWidget() # Widget that contains the collection of Vertical Box
        self.v_layout = QVBoxLayout() # The Vertical Box that contains the Horizontal Boxes of  labels and buttons

        for i in range(1,50):
            label = QLabel("TextLabel " + str(i))
            self.v_layout.addWidget(label)

        self.widget.setLayout(self.v_layout)

        #Scroll Area Properties
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.widget)

        self.setCentralWidget(self.scroll_area)

        self.setGeometry(300, 100, 1200, 800)
        self.setWindowTitle('Scroll Area Demonstration')
        self.show()

        return

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    sys.exit(app.exec())