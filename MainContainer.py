from PyQt6.QtWidgets import (QWidget, QSizePolicy, QBoxLayout, QVBoxLayout, QLabel)
from PyQt6.QtCore import QObject, QSize
import pretty_midi

from FileAnalysisWidget import FileAnalysisWidget
from analysis import get_note_guessed_from_fname, create_note_list

class MainContainer(QWidget):

    def __init__(self):
        super().__init__()
        self.dir_path = ""
        self.init_midi_vars()
        self.note_list = create_note_list()
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.v_box = QVBoxLayout()
        # self.v_box.setSpacing(2)
        self.add_welcoming_widget()
        self.setLayout(self.v_box)
        print(id(self), "main_container sizeHint:", str(self.sizeHint()))
        self.adjustSize()
        print(id(self), "main_container size:", str(self.size()))
        # self.update()
        # print("v_box geometry:", str(self.v_box.geometry()))
    
    
    def sizeHint(self):
        width = self.width()
        height = 0
        for child in self.children():
            if not isinstance(child, QBoxLayout):
                # print(id(child), str(type(child).__name__) , "main_container child size:", str(child.size()))
                if child.width() > width:
                    width = child.width()
                height = height + child.height()
        return QSize(width, height)
    
    
    def add_welcoming_widget(self):
        self.welcoming_widget = QLabel("Use « File » > « Import directory » to start the analysis.")
        # self.welcoming_widget.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        self.welcoming_widget.adjustSize()
        print(id(self.welcoming_widget), "welcoming_widget size:", self.welcoming_widget.size())
        self.v_box.addWidget(self.welcoming_widget)
    
    
    def add_multiple_analysis_widget(self, file_paths: list):
        # if self.welcoming_widget.parent() is QObject:
        print("welcoming_widget deletion")
        self.v_box.removeWidget(self.welcoming_widget)
        self.welcoming_widget.deleteLater()
        # self.welcoming_widget = None
        for file_path in file_paths:
            self.add_single_analysis_widget(fpath=file_path)
        print(id(self), "main_container sizeHint:", str(self.sizeHint()))
        self.adjustSize()
        print(id(self), "main_container size:", str(self.size()))
        # self.update()
    
    
    def add_single_analysis_widget(self, fpath: str):
        analysis_widget = FileAnalysisWidget(
            fpath=fpath, 
            note_list=self.note_list, 
            instru=self.pmidi_instru
        )
        # print("AnalysisWidget sizeHint:", str(analysis_widget.sizeHint()))
        self.v_box.addWidget(analysis_widget) # + param ,0
    
    
    def init_midi_vars(self):
        self.pmidi = pretty_midi.PrettyMIDI()
        # Create an Instrument instance for a banjo instrument
        self.pmidi_program = pretty_midi.instrument_name_to_program('Banjo')
        self.pmidi_instru = pretty_midi.Instrument(program=self.pmidi_program)
        # Add the banjo instrument to the PrettyMIDI object
        self.pmidi.instruments.append(self.pmidi_instru)
