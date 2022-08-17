import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QTabWidget
from PyQt6.QtGui import QPalette, QColor, QAction

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")

        menu = self.menuBar()

        file_menu = menu.addMenu("&File")
        file_menu.addAction(QAction("test 1", self))

        layout_g = QGridLayout()
        layout_g.addWidget(Color('red'), 0, 0)
        layout_g.addWidget(Color('green'), 1, 0)
        layout_g.addWidget(Color('blue'), 1, 1)
        layout_g.addWidget(Color('purple'), 2, 1)
        
        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.TabPosition.West)
        tabs.setMovable(True)
        for i, color in enumerate(["red", "green", "blue", "yellow"]):
            tabs.addTab(Color(color), color)
        
        layout_h = QHBoxLayout()
        # layout_h.addWidget(tabs)
        layout_h.addWidget(Color('red'))
        layout_h.addWidget(Color('green'))
        layout_h.addLayout(layout_g)
        
        layout_v = QVBoxLayout()
        layout_v.setContentsMargins(10, 10, 10, 10)
        layout_v.setSpacing(5)
        layout_v.addLayout(layout_h)
        layout_v.addWidget(Color('blue'))

        container = QWidget()
        container.setLayout(layout_v)
        self.setCentralWidget(container)

class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()