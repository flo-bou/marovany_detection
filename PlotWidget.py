import random

from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QSizePolicy
# from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qtagg import FigureCanvas, FigureCanvasQTAgg, NavigationToolbar2QT
import matplotlib.figure as fig
# import matplotlib.pyplot as plt

class PlotWidget(QWidget):

    def __init__(self):
        super().__init__()
        
        # self.figure = plt.figure() # a figure instance to plot on
        self.figure = fig.Figure()
        self.figure.set(figwidth=16, figheight=4) # 10 = 1000px
        # self.figure.
        print(id(self.figure), "figure", self.figure)
        # print(id(self.figure2), "figure2", self.figure)
        
        self.canvas = FigureCanvasQTAgg(self.figure)
        # static_canvas = FigureCanvas(self.figure)
        print(id(self), "canvas sizeHint:", str(self.canvas.sizeHint()))
        print(id(self), "canvas size:", str(self.canvas.size()))
        self.nav_toolbar = NavigationToolbar2QT(self.canvas, self)
        print(id(self), "nav_toolbar sizeHint:", str(self.nav_toolbar.sizeHint()))
        print(id(self), "nav_toolbar size:", str(self.nav_toolbar.size()))
        self.button = QPushButton('Plot')
        self.button.clicked.connect(self.plot)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.nav_toolbar)
        layout.addWidget(self.button)

        # self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        self.setLayout(layout)
        # print(id(self), "plot widget size:", str(self.size()))
        print(id(self), "plot widget sizeHint:", str(self.sizeHint()))
        # self.adjustSize() # default size max is 1280px
        self.setFixedSize(self.sizeHint())
        # self.update()
        print(id(self), "plot widget size:", str(self.size()))

    # action called by the push button
    def plot(self):
        data = [random.random() for i in range(20)] # random data
        self.figure.clear() # clearing old figure
        ax = self.figure.add_subplot(111)
        ax.plot(data, '*-')
        self.canvas.draw() # refresh canvas
        
    # def sizeHint(self):
    #     return self.size()

