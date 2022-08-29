import random

from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QSizePolicy
# from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qtagg import FigureCanvas, FigureCanvasQTAgg, NavigationToolbar2QT
import matplotlib.figure as fig
# import matplotlib.pyplot as plt

class FigureWidget(QWidget):
    """Generic figure widget. Made for several figure types.

    Args:
        QWidget (QWidget): Qt all-around widget
    """
    # (figwidth=16, figheight=4)
    def __init__(self, figure: fig.Figure):
        """_summary_

        Args:
            fig_size (list[w, h]): size of the figure in mpl usuals units (it will be 100 times more in Qt pixels)
        """
        super().__init__()
        
        # self.fig_size = [28, 14]
        fig_size = [12, 3] # 12, 3 mean 1200px, 300px
        self.figure = figure
        # self.figure.set(figwidth=fig_size[0], figheight=fig_size[1]) # 10 = 1000px
        print(id(self.figure), "figure", self.figure)
        # print(id(self.figure2), "figure2", self.figure)
        
        self.canvas = FigureCanvasQTAgg(self.figure)
        # static_canvas = FigureCanvas(self.figure)
        print(id(self), "canvas sizeHint:", str(self.canvas.sizeHint()))
        print(id(self), "canvas size:", str(self.canvas.size()))
        self.nav_toolbar = NavigationToolbar2QT(self.canvas, self, coordinates=False)
        print(id(self), "nav_toolbar sizeHint:", str(self.nav_toolbar.sizeHint()))
        print(id(self), "nav_toolbar size:", str(self.nav_toolbar.size()))
        # self.button = QPushButton('Plot')
        # self.button.clicked.connect(self.plot)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.nav_toolbar)
        # layout.addWidget(self.button)

        # self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        self.setLayout(layout)
        # print(id(self), "plot widget size:", str(self.size()))
        print(id(self), "FigureWidget sizeHint:", str(self.sizeHint()))
        # self.adjustSize() # default size max is 1280px
        self.setFixedSize(self.sizeHint())
        # self.update()
        print(id(self), "FigureWidget size:", str(self.size()))

    # action called by the push button
    def plot(self):
        data = [random.random() for i in range(20)] # random data
        self.figure.clear() # clearing old figure
        ax = self.figure.add_subplot(111)
        ax.plot(data, '*-')
        self.canvas.draw() # refresh canvas

    # def sizeHint(self):
    #     return self.size()
