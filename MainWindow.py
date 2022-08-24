from os import scandir, listdir
# from os.path import split, isfile

from PyQt6.QtWidgets import QScrollArea, QVBoxLayout, QMainWindow, QFileDialog
from PyQt6.QtCore import Qt

from AnalysisWidget import AnalysisWidget
from MainContainer import MainContainer


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.get_screen_size()
        
        self.v_box = QVBoxLayout()
        analysis_1 = AnalysisWidget("ex1-int.jpg")
        # analysis_2 = AnalysisWidget("ex1-spec.jpg")
        self.v_box.addWidget(analysis_1, 0)
        # self.v_box.addStretch()
        # size_policy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        # size_policy.setHorizontalStretch(0)
        # size_policy.setVerticalStretch(0)
        # self.v_box.setSizePolicy(size_policy)
        self.v_box.update()

        self.main_container = MainContainer()
        self.main_container.setLayout(self.v_box)
        print(id(self.main_container), "main_container sizeHint:", str(self.main_container.sizeHint()))
        self.main_container.adjustSize()
        print(id(self.main_container), "main_container size:", str(self.main_container.size()))
        # self.main_container.update()
        # print("v_box geometry:", str(self.v_box.geometry()))

        # scroll_area is the centralWidget
        # scroll_area contains the main_container
        self.scroll_area = QScrollArea()
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        # self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.main_container)
        width = int(self.screen_available_size.width() * 0.85)
        height = int(self.screen_available_size.height() * 0.85)
        self.scroll_area.setFixedSize(width, height)
        print("scroll_area size:", str(self.scroll_area.size()))
        
        self.create_menu()

        self.setCentralWidget(self.scroll_area)
        # self.setGeometry(100, 100, 1200, 800)
        self.adjustSize()
        # print("devicePixelRatio", self.devicePixelRatio())
        self.setWindowTitle('Scroll Area Demo')
        # print("main_window size:", str(self.size()))
        # print("main_window geometry:", str(self.geometry()))
    
    
    def get_screen_size(self):
        screen = self.screen()
        self.device_pixel_ratio = screen.devicePixelRatio()
        print("device_pixel_ratio", self.device_pixel_ratio)
        self.screen_available_size = screen.availableSize()
        print("screen_available_size", self.screen_available_size)


    def create_menu(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        open_dir_action = file_menu.addAction("Open directory", self.do_smth_using_dir)
        add_analysis_action = file_menu.addAction("Add analysis", self.add_analysis_widget)
        edit_menu = menu_bar.addMenu("&Edit")
    
    
    def do_smth_using_dir(self):
        dir_path = self.get_dir_using_dialog()
        dir_content = listdir(dir_path)
        print("dir_content", dir_content)
        file_paths = list(map(lambda file_name: dir_path + file_name, dir_content))
        print("file_paths", file_paths)
        wav_files = filter(lambda file_path: file_path.split(".")[-1]=="wav", file_paths)
        print("wav_files", list(wav_files))
    
    
    def get_dir_using_dialog(self):
        dir_path = QFileDialog.getExistingDirectory(parent=None, caption="Choose a directory containing wav files to analyse.", directory="", options=QFileDialog.Option.ShowDirsOnly)
        print(str(dir_path))
        return dir_path
    
    
    def add_analysis_widget(self):
        a = AnalysisWidget("ex1-spec.jpg")
        print("AnalysisWidget sizeHint:", str(a.sizeHint()))
        self.v_box.addStretch()
        self.v_box.addWidget(a, 0)
        # self.v_box.update()
        print("main_container sizeHint:", str(self.main_container.sizeHint()))
        self.main_container.adjustSize()
        self.main_container.update()
        l = self.main_container.children()
        for child in l:
            print(id(child), type(child).__name__, "main_container child geometry:", str(child.geometry()))
        print("main_container:", str(self.main_container.size()))
