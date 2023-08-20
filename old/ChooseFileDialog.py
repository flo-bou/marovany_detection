import os 

from PyQt6.QtWidgets import (QLabel, QPushButton,
                             QDialog, QLabel, QComboBox,
                             QHBoxLayout, QGridLayout)
from PyQt6.QtCore import Qt


class ChooseFileDialog(QDialog):

    def __init__(self, parent):
        super().__init__()
        #self.aw = parent.analysisWidgets
        self.parent = parent
        self.chosen_option=None
        layout = QGridLayout()
        self.label = QLabel("Cliquez ci-dessous pour afficher les choix")
        layout.addWidget(self.label)

        #layout.setSpacing(10)
        self.combo_box = QComboBox()
        self.AddItem(parent)
        
        layout.addWidget(self.combo_box)
        cancel_button = QPushButton(text="Cancel")
        cancel_button.setMaximumWidth(70)
        cancel_button.adjustSize()
        cancel_button.clicked.connect(self.reject)
        ok_button = QPushButton(text="Ok")
        ok_button.setMaximumWidth(70)
        ok_button.adjustSize()
        ok_button.clicked.connect(self.accept)
        footer_box = QHBoxLayout()
        footer_box.addSpacing(10)
        footer_box.addWidget(cancel_button)
        footer_box.addWidget(ok_button)
        footer_box.setAlignment(Qt.AlignmentFlag.AlignRight)
    
        
        layout.addLayout(footer_box, 4, 0, 1, 5)
        
        self.accepted.connect(self.file_choosed)
        self.setLayout(layout)

        self.setWindowTitle("Change params")
        self.setLayout(layout)
    
    def AddItem(self,parent):
        analysisWidgets=parent.get_ana_widget()
        for aw in analysisWidgets:
            name_file=os.path.basename(aw.file_path)
            self.combo_box.addItem(str(name_file[0:2]))
        self.combo_box.activated.connect(self.handle_choice)
    
    def file_choosed(self):
        pass

    def handle_choice(self, index):
        self.chosen_option = self.combo_box.itemText(index)
        self.label.setText(f"Vous avez choisi : {self.chosen_option}")
        self.parent.Choose_File_Edition(self.chosen_option)
        
    