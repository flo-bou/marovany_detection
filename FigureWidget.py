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
        
        if figure != None:
            self.figure = figure # fig_size = [12, 3] means [1200px, 300px]
            print(id(self.figure), "figure", self.figure)
            # print(id(self.figure2), "figure2", self.figure)
            self.canvas = FigureCanvasQTAgg(self.figure)
            # static_canvas = FigureCanvas(self.figure)
            print(id(self), "canvas sizeHint:", str(self.canvas.sizeHint()))
            print(id(self), "canvas size:", str(self.canvas.size()))
            self.nav_toolbar = NavigationToolbar2QT(self.canvas, self, coordinates=False)
            
            layout = QVBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)
            layout.addWidget(self.canvas, 0)
            layout.addWidget(self.nav_toolbar, 0)
            
            self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
            self.setStyleSheet("border: 0px solid")
            self.setLayout(layout)
        print(id(self), "FigureWidget sizeHint:", str(self.sizeHint()))
        # self.adjustSize() # default size max is 1280px
        self.setFixedSize(self.sizeHint())
        # self.update()
        print(id(self), "FigureWidget size:", str(self.size()))
