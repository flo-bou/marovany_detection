# importing various libraries
import sys

from PyQt6.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
import matplotlib.pyplot as plt
import random

# main window
class Window(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        # a figure instance to plot on
        self.figure = plt.figure()
        # this is the Canvas Widget that displays the 'figure'it takes the 'figure' instance as a parameter to __init__
        self.canvas = FigureCanvasQTAgg(self.figure)
        # this is the Navigation widget, it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        # Just some button connected to 'plot' method
        self.button = QPushButton('Plot')
        # adding action to the button
        self.button.clicked.connect(self.plot)
        # creating a Vertical Box layout
        layout = QVBoxLayout()
        # adding tool bar to the layout
        layout.addWidget(self.toolbar)
        # adding canvas to the layout
        layout.addWidget(self.canvas)
        # adding push button to the layout
        layout.addWidget(self.button)
        # setting layout to the main window
        self.setLayout(layout)

    # action called by the push button
    def plot(self):
        # random data
        data = [random.random() for i in range(10)]
        # clearing old figure
        self.figure.clear()
        # create an axis
        ax = self.figure.add_subplot(111)
        # plot data
        ax.plot(data, '*-')
        # refresh canvas
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Window()
    main.show()
    sys.exit(app.exec())