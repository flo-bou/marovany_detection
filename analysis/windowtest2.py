import sys
import time

import numpy as np
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure

from PyQt6.QtWidgets import QVBoxLayout, QMainWindow, QWidget


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        fig = Figure()
        fig.set(figwidth=10, figheight=5)
        ax = fig.subplots()
        x = np.linspace(0, 10, 20)
        ax.plot(x, x, label='linear')
        ax.plot(x, x**2, label='quadratic')
        ax.plot(x, x**3, label='cubic')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title('Aardvark lengths')
        ax.legend()
        ax.axis([0, 10, 0, 100]) # set min/max of axes : 55 to 175 for x and 0 to .03 for y

        self.canvas = FigureCanvasQTAgg(fig)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)

        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    # def _update_canvas(self):
    #     t = np.linspace(0, 10, 101)
    #     # Shift the sinusoid as a function of time.
    #     self._line.set_data(t, np.sin(t + time.time()))
    #     self._line.figure.canvas.draw()


if __name__ == "__main__":
    # Check whether there is already a running QApplication (e.g., if running
    # from an IDE).
    qapp = QtWidgets.QApplication.instance()
    if not qapp:
        qapp = QtWidgets.QApplication(sys.argv)

    app = AppWindow()
    app.show()
    # app.activateWindow()
    app.raise_()
    qapp.exec()