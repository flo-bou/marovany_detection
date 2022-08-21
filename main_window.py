from os import scandir, listdir
from os.path import split, isfile

from PyQt6.QtWidgets import (QWidget, QLabel, QScrollArea, QMenu, QSizePolicy, QBoxLayout,
                             QVBoxLayout, QMainWindow, QFileDialog)
from PyQt6.QtCore import Qt, QSize

from analysis_widget import AnalysisWidget


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        
        self.v_box = QVBoxLayout()
        analysis_1 = AnalysisWidget("ex1-int.jpg")
        # analysis_2 = AnalysisWidget("ex1-spec.jpg")
        self.v_box.addWidget(analysis_1, 0)
        # self.v_box.addStretch()
        # self.v_box.addWidget(analysis_2)
        # size_policy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        # size_policy.setHorizontalStretch(0)
        # size_policy.setVerticalStretch(0)
        # self.v_box.setSizePolicy(size_policy)
        self.v_box.update()

        self.main_container = MainContainer()
        self.main_container.setLayout(self.v_box)
        self.main_container.adjustSize()
        self.main_container.update()
        print("v_box geometry:", str(self.v_box.geometry()))
        print("main_container size:", str(self.main_container.size()))

        # scroll_area is the centralWidget
        # scroll_area contains the main_container
        self.scroll_area = QScrollArea()
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        # self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.main_container)
        self.scroll_area.setFixedSize(1700, 700)
        print("scroll_area size:", str(self.scroll_area.size()))
        
        self.create_menu()

        self.setCentralWidget(self.scroll_area)
        # self.setGeometry(100, 100, 1200, 800)
        self.adjustSize()
        self.setWindowTitle('Scroll Area Demo')
        # print("main_window size:", str(self.size()))
        # print("main_window geometry:", str(self.geometry()))
    
    
    def create_menu(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        # print(file_menu)
        open_dir_action = file_menu.addAction("Open directory", self.do_smth_using_dir)
        add_analysis_action = file_menu.addAction("Add analysis", self.add_analysis_widget)
        # open_dir_action.getvalue
        edit_menu = menu_bar.addMenu("&Edit")
    
    
    def do_smth_using_dir(self):
        dir_path = self.get_dir_using_dialog()
        dir_content = listdir(dir_path)
        print("dir_content", dir_content)
        file_paths = list(map(lambda file_name: dir_path + file_name, dir_content))
        print("file_paths", file_paths)
        wav_files = filter(lambda file_path: file_path.split(".")[-1]=="wav", file_paths) # here
        # dir_content = scandir(dir_path)
        # for dirEntry in dir_content:
        #     print(dirEntry)
        # wav_files = filter(lambda dirEntry: dirEntry.is_file(follow_symlinks=False) and dirEntry.name.split(".")[-1]=="wav", 
        #                    dir_content)
        print("wav_files", list(wav_files))
    
    
    def get_dir_using_dialog(self):
        dir_path = QFileDialog.getExistingDirectory(parent=None, caption="Choose a directory containing wav files to analyse.", directory="", options=QFileDialog.Option.ShowDirsOnly)
        print(str(dir_path))
        return dir_path
    
    
    def add_analysis_widget(self):
        # store current geometry of vbox/maincontainer
        # then use it to set new geometry of vbox/main
        # or change sizehint and call adjustsize  <--
        a = AnalysisWidget("ex1-spec.jpg")
        print("AnalysisWidget sizeHint:", str(a.sizeHint()))
        self.v_box.addStretch()
        self.v_box.addWidget(a, 0)
        # self.v_box.setSGeometry(0, 0, self.v_box.width() + a.width())
        # self.v_box.update()
        print("main_container sizeHint:", str(self.main_container.sizeHint()))
        self.main_container.adjustSize()
        self.main_container.update()
        # ??
        l = self.main_container.children()
        print(len(l))
        for child in l:
            print(id(child), "main_container child geometry:", str(child.geometry()))
        print(id(self.v_box), "v_box geometry:", str(self.v_box.geometry()))
        print("main_container:", str(self.main_container.size()))
        # print("scroll_area size:", str(self.scroll_area.size()))
        # print("main_window size:", str(self.size()))


class MainContainer(QWidget):

    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
    
    
    def sizeHint(self):
        width = self.width()
        height = 0
        for child in self.children():
            # print(id(child), str(type(child).__name__) , "main_container child geometry:", str(child.geometry()))
            if not isinstance(child, QBoxLayout):
                if child.width() > width:
                    width = child.width()
                height = height + child.height()
        print(id(child), "main_container sizehint:", width, height)
        return QSize(width, height)
