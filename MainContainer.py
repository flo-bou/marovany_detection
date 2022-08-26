from PyQt6.QtWidgets import (QWidget, QSizePolicy, QBoxLayout, QVBoxLayout, QLabel)
from PyQt6.QtCore import QSize
import pretty_midi

from FileAnalysisWidget import FileAnalysisWidget
from analysis import get_note_guessed_from_fname

class MainContainer(QWidget):

    def __init__(self):
        super().__init__()
        self.dir_path = ""
        # self.dir_path = "C:/Users/admin/Project/MIDIconversion_marovany/capteurs/"
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.v_box = QVBoxLayout()
        # add default widget (no Analysis)
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
            print(id(child), str(type(child).__name__) , "main_container child geometry:", str(child.geometry()))
            if not isinstance(child, QBoxLayout):
                if child.width() > width:
                    width = child.width()
                height = height + child.height()
        print(id(child), "main_container child sizehint:", width, height)
        return QSize(width, height)
    
    
    def add_welcoming_widget(self):
        self.welcoming_widget = QLabel("Use « File » > « Import directory » to start the analysis.")
        self.welcoming_widget.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        self.v_box.addWidget(self.welcoming_widget)

    def add_multiple_analysis_widget(self, file_paths: list):
        del self.welcoming_widget # TODO
        for file_path in file_paths:
            self.add_single_analysis_widget(fpath=file_path)
        self.adjustSize()
        self.update()
    
    def add_single_analysis_widget(self, fpath: str):
        analysis_widget = FileAnalysisWidget(fpath=fpath)
        print("AnalysisWidget sizeHint:", str(analysis_widget.sizeHint()))
        self.v_box.addStretch()
        self.v_box.addWidget(analysis_widget, 0)
        # self.v_box.update()
        print("main_container sizeHint:", str(self.sizeHint()))
        self.adjustSize()
        # self.main_container.update()
        # children = self.children()
        # for child in children:
        #     print(id(child), type(child).__name__, "main_container child geometry:", str(child.geometry()))
        print("main_container:", str(self.size()))
    
    
    def get_midi_widget(self):
        banjo_MIDI = pretty_midi.PrettyMIDI()
        # Create an Instrument instance for a banjo instrument
        banjo_program = pretty_midi.instrument_name_to_program('Banjo')
        banjo_instru = pretty_midi.Instrument(program=banjo_program)
        # Add the banjo instrument to the PrettyMIDI object
        banjo_MIDI.instruments.append(banjo_instru)
        
        self.midi_note = get_note_guessed_from_fname(note_list=self.note_list, fname=self.file_path)
        print("Guessed note :", self.midi_note)
