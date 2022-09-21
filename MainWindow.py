from os import scandir, listdir
# from os.path import split, isfile

from PyQt6.QtWidgets import QScrollArea, QMainWindow, QFileDialog
from PyQt6.QtCore import Qt

from MainContainer import MainContainer


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.scroll_area = QScrollArea()
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        # self.scroll_area.setWidgetResizable(True)
        app_size = self.get_app_size()
        self.scroll_area.setFixedSize(*app_size)
        self.main_container = MainContainer(app_size=app_size)
        self.scroll_area.setWidget(self.main_container)
        print("scroll_area size:", str(self.scroll_area.size()))
        self.create_menu()
        
        self.setCentralWidget(self.scroll_area)
        self.adjustSize()
        self.setWindowTitle('Marovany')
    
    
    def get_app_size(self):
        screen = self.screen()
        self.device_pixel_ratio = screen.devicePixelRatio()
        print("device_pixel_ratio", self.device_pixel_ratio)
        self.screen_available_size = screen.availableSize()
        print("screen_available_size", self.screen_available_size)
        width = int(self.screen_available_size.width() * 0.85)
        height = int(self.screen_available_size.height() * 0.85)
        print("app_size", width, height)
        return width, height
    
    
    def create_menu(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        import_dir_action = file_menu.addAction("Import a directory", self.main_container.import_dir)
        import_file_action = file_menu.addAction("Import a single file", self.main_container.import_file)
        # add_analysis_action = file_menu.addAction("Add analysis", self.main_container.add_file_analysis_widget())
        # edit_menu = menu_bar.addMenu("Edit")
    
    
    def get_dir_using_dialog(self):
        dir_path = QFileDialog.getExistingDirectory(parent=None, caption="Choose a directory containing wav files to analyse.", directory="", options=QFileDialog.Option.ShowDirsOnly)
        print(str(dir_path))
        return dir_path
