from PyQt6.QtWidgets import (QWidget, QLabel, QBoxLayout, 
                             QHBoxLayout, QPushButton, QSizePolicy)
from PyQt6.QtCore import Qt, QSize


class FileAnalysisHeader(QWidget):
    """Widget containing header of analysis widget, name of file and buttons
    """
    def __init__(self, fname: str, note: str, parent: QWidget):
        super().__init__()
        self.title_label = QLabel("File : " + fname + " ;")
        self.title_label.adjustSize()
        self.note_label = QLabel("Note : " + str(note))
        self.note_label.adjustSize()

        self.plot_time_series_btn = QPushButton("Plot signal")
        self.plot_time_series_btn.clicked.connect(parent.add_time_series_figure)
        self.plot_time_series_btn.adjustSize()
        self.plot_note_tracking_btn = QPushButton("Plot notes")
        self.plot_note_tracking_btn.clicked.connect(parent.add_played_string_detection_figure)
        self.plot_note_tracking_btn.adjustSize()
        
        self.params_btn = QPushButton("Params")
        self.params_btn.clicked.connect(parent.call_ParamDialog)
        self.params_btn.adjustSize()

        self.remove_btn = QPushButton("Remove File")
        self.remove_btn.clicked.connect(parent.remove_self)
        self.remove_btn.adjustSize()
        
        self.reset_plot_btn = QPushButton("Reset plot") # QComboBox instead
        self.reset_plot_btn.clicked.connect(parent.Reset_plot)
        self.reset_plot_btn.adjustSize()
        
        self.header_box = QHBoxLayout()
        self.header_box.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.header_box.addWidget(self.title_label)
        self.header_box.addWidget(self.note_label)
        
        self.header_box.addWidget(self.plot_time_series_btn)
        self.header_box.addWidget(self.plot_note_tracking_btn)
        self.header_box.addWidget(self.reset_plot_btn)
        self.header_box.addWidget(self.params_btn)
        self.header_box.addWidget(self.remove_btn)
        # self.header_box.addWidget(self.options_btn)

        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        self.setLayout(self.header_box)
        self.adjustSize()


    def Audio_player_btn(self,parent):

        self.play_button = QPushButton("Play audio")
        self.play_button.setVisible(True)
        self.play_button.clicked.connect(parent.play_audio)
        self.play_button.adjustSize()
        self.header_box.addWidget(self.play_button)
        self.adjustSize()
        

    def Zoom_Analysis_btn(self,parent):
        self.zoom_btn=QPushButton("Zoom analysis")
        self.zoom_btn.setVisible(True)
        self.zoom_btn.clicked.connect(parent.generate_zoom_analysis)
        self.zoom_btn.adjustSize()

        self.Cancel_btn4=QPushButton("Back")
        self.Cancel_btn4.setVisible(True)
        
        self.Cancel_btn4.clicked.connect(parent.Cancel4)
        self.Cancel_btn4.adjustSize()

        self.header_box.addWidget(self.zoom_btn)
        self.header_box.addWidget(self.Cancel_btn4)
        self.adjustSize()

    def Delete_Note_func(self,parent):
        self.Delete_note_btn=QPushButton("Delete Note")
        self.Delete_note_btn.setVisible(True)
        self.Delete_note_btn.clicked.connect(parent.Delete_note)
        self.Delete_note_btn.adjustSize()

        self.Cancel_btn3=QPushButton("Back")
        self.Cancel_btn3.setVisible(True)
        self.Cancel_btn3.clicked.connect(parent.Cancel3)
        self.Cancel_btn3.adjustSize()

        self.header_box.addWidget(self.Delete_note_btn)
        self.header_box.addWidget(self.Cancel_btn3)
        self.adjustSize()

    def Add_Note_func(self,parent):
        self.Add_note_btn=QPushButton("Add Note")
        self.Add_note_btn.setVisible(True)
        self.Add_note_btn.clicked.connect(parent.Add_Note_Cursor)
        self.Add_note_btn.adjustSize()

        self.Cancel_btn2=QPushButton("Back")
        self.Cancel_btn2.setVisible(True)
        
        self.Cancel_btn2.clicked.connect(parent.Cancel2)
        self.Cancel_btn2.adjustSize()

        self.Finish_btn= QPushButton("Finish")
        self.Finish_btn.setVisible(False)
        self.Finish_btn.clicked.connect(parent.Finish)
        self.Finish_btn.adjustSize()

        self.header_box.addWidget(self.Add_note_btn)
        self.header_box.addWidget(self.Finish_btn)
        self.header_box.addWidget(self.Cancel_btn2)
        self.adjustSize()
        
    def Edit_note(self,parent):
        # on rend les autre bouton invisible car pas besoin 
        self.Edit_Note_button_bool=True

        self.Edit_onsets_btn=QPushButton("Edit Onsets")
        self.Edit_onsets_btn.setVisible(True)
        self.Edit_onsets_btn.clicked.connect(parent.Edit_Onsets_Cursor)
        self.Edit_onsets_btn.adjustSize()

        self.Edit_offsets_btn= QPushButton("Edit Offset")
        self.Edit_offsets_btn.setVisible(True)
        self.Edit_offsets_btn.clicked.connect(parent.Edit_Offsets_Cursor)
        self.Edit_offsets_btn.adjustSize()

        self.Cancel_btn=QPushButton("Back")
        self.Cancel_btn.setVisible(True)
        
        self.Cancel_btn.clicked.connect(parent.Cancel1)
        self.Cancel_btn.adjustSize()

        self.Finish_btn= QPushButton("Finish")
        self.Finish_btn.setVisible(False)
        self.Finish_btn.clicked.connect(parent.Finish)
        self.Finish_btn.adjustSize()

        self.header_box.addWidget(self.Edit_onsets_btn)
        self.header_box.addWidget(self.Edit_offsets_btn)
        self.header_box.addWidget(self.Finish_btn)
        self.header_box.addWidget(self.Cancel_btn)
        self.adjustSize()
    
    def Add_notes_to_midi_instrument(self,parent):
        parent.add_notes_to_midi_instrument()

    def sizeHint(self):
        width = 0
        height = 0
        for child in self.children():
            if not isinstance(child, QBoxLayout):
                width = width + child.width()
                if child.height() > height:
                    height = child.height()
        # print(id(self), "FileAnalysisHeader sizeHint :", width, height)
        return QSize(width, height)