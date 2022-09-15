from os import scandir, listdir
# from os.path import split, isfile

from PyQt6.QtWidgets import QScrollArea, QMainWindow, QFileDialog
from PyQt6.QtCore import Qt

from MainContainer import MainContainer


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.get_screen_size()
        
        self.main_container = MainContainer()
        self.scroll_area = QScrollArea()
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        # self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.main_container)
        width = int(self.screen_available_size.width() * 0.85)
        height = int(self.screen_available_size.height() * 0.85)
        self.scroll_area.setFixedSize(width, height)
        print("scroll_area size:", str(self.scroll_area.size()))
        # signal slot to send scroll area size
        self.create_menu()
        
        self.setCentralWidget(self.scroll_area)
        # self.setGeometry(100, 100, 1200, 800)
        self.adjustSize()
        # print("devicePixelRatio", self.devicePixelRatio())
        self.setWindowTitle('Marovany')
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
        open_dir_action = file_menu.addAction("Import directory", self.main_container.open_dir)
        # add_analysis_action = file_menu.addAction("Add analysis", self.main_container.add_file_analysis_widget())
        # edit_menu = menu_bar.addMenu("Edit")
    
    
    # def open_dir(self):
    #     # Only files with the .wav extensions will be used
    #     self.dir_path = QFileDialog.getExistingDirectory(parent=None, caption="Choose a directory containing wav files to analyse.", directory="", options=QFileDialog.Option.ShowDirsOnly)
    #     print(str(self.dir_path))
    #     dir_content = listdir(self.dir_path)
    #     print("dir_content", dir_content)
    #     file_paths = list(map(lambda file_name: self.dir_path + "/" + file_name, dir_content))
    #     print("file_paths", file_paths)
    #     wav_file_paths = list(filter(lambda file_path: file_path.split(".")[-1]=="wav", file_paths))
    #     print("wav_files", wav_file_paths)
    #     if len(wav_file_paths)>0:
    #         self.main_container.add_multiple_analysis_widget(file_paths=wav_file_paths)
    #     else:
    #         print("No .wav files found in ", self.dir_path)
    
    
    def get_dir_using_dialog(self):
        dir_path = QFileDialog.getExistingDirectory(parent=None, caption="Choose a directory containing wav files to analyse.", directory="", options=QFileDialog.Option.ShowDirsOnly)
        print(str(dir_path))
        return dir_path
    

