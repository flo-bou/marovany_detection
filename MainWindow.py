import json

from PyQt6.QtWidgets import (QScrollArea, QMainWindow, QFileDialog, 
                             QMenuBar, QMenu, QMessageBox)
from PyQt6.QtCore import Qt

from MainContainer import MainContainer


class MainWindow(QMainWindow):

    def __init__(self):
        print("Classe MainWindow")
        super().__init__()
        self.scroll_area = QScrollArea()
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        #self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
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
        print("get_app_size")
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
        print("create_menu")
        menu_bar = self.menuBar()
        
        # --------------------------------- File Menu -------------------------------- #
        file_menu = menu_bar.addMenu("File")
        
        import_dir_action = file_menu.addAction("Import a directory", self.main_container.import_dir)
        
        import_file_action = file_menu.addAction("Import a single file", self.main_container.import_file)
        
        save_project_action = file_menu.addAction("Save project", self.save_project)
        
        save_note_menu = file_menu.addMenu("Save to excel")
        save_note_menu.addAction("Choose file",self.main_container.call_ChooseFileDialog_save_file)
        save_note_menu.addAction("Save All",self.main_container.save_notes)
        
        load_project_action = file_menu.addAction("Open Project", self.load_project)

        # --------------------------------- Edit Menu -------------------------------- #
        edit_menu = menu_bar.addMenu('Edit')
        
        edit_note_menu = edit_menu.addMenu('Edit Note')
        edit_note_menu.addAction('Choose file',self.main_container.call_ChooseFileDialog_Edit)
        edit_note_menu.addAction('All file',self.main_container.Note_edition)

        delete_note_menu = edit_menu.addMenu('Delete Note')
        delete_note_menu.addAction('Choose file',self.main_container.call_ChooseFileDialog_Delete)
        delete_note_menu.addAction('All files',self.main_container.Delete_Note)

        # --------------------------------- Add Menu --------------------------------- #
        add_menu = menu_bar.addMenu('Add')
        
        add_audio_menu = add_menu.addMenu('Add audio player')
        add_audio_menu.addAction('Choose file',self.main_container.call_ChooseFileDialog_Add_audio)
        add_audio_menu.addAction('All files',self.main_container.Add_audio_player)
        
        add_note_menu = add_menu.addMenu('Add Note')
        add_note_menu.addAction('Choose file',self.main_container.call_ChooseFileDialog_Add)
        add_note_menu.addAction('All files',self.main_container.Add_Note)
    
    
    def save_project(self):
        project_data = {
            "main_container_data": self.main_container.get_data_to_save(), 
        }
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Project", "", "Project Files (*.json)")
        if file_path:
            try:
                with open(file_path, "w") as file:
                    json.dump(project_data, file)
                QMessageBox.information(self, "Save Project", "Project saved successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred while saving the project: {e}")
            
    def load_project(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Load Project", "", "Project Files (*.json)")
        if file_path:
            try:
                with open(file_path, "r") as file:
                    project_data = json.load(file)
                self.main_container.load_data_from_project(project_data["main_container_data"])
                QMessageBox.information(self, "Load Project", "Project loaded successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred while loading the project: {e}")
    

    def get_dir_using_dialog(self):
        print("create_menu")
        dir_path = QFileDialog.getExistingDirectory(parent=None, caption="Choose a directory containing wav files to analyse.", directory="", options=QFileDialog.Option.ShowDirsOnly)
        print(str(dir_path))
        return dir_path
