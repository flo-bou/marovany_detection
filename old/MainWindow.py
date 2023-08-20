import json

from MainContainer import MainContainer

class MainWindow(QMainWindow):
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
