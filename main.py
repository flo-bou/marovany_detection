from sys import argv as sys_argv, exit as sys_exit
from time import time

from PyQt6.QtWidgets import QApplication

from Widgets.MainWindow import MainWindow


if __name__ == '__main__':
    start = time()
    app = QApplication(sys_argv)
    window = MainWindow()
    window.show()
    end = time()
    print("App creation: ", str(end-start), " sec")

    sys_exit(app.exec())