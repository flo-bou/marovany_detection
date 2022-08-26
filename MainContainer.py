from PyQt6.QtWidgets import (QWidget, QSizePolicy, QBoxLayout, QVBoxLayout)
from PyQt6.QtCore import QSize
import pretty_midi

from FileAnalysisWidget import FileAnalysisWidget
from analysis import get_note_guessed_from_fname

class MainContainer(QWidget):

    def __init__(self):
        super().__init__()
        self.dir_path = "C:/Users/admin/Project/MIDIconversion_marovany/capteurs/"
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.v_box = QVBoxLayout()
        # add default widget (no Analysis)
        analysis_1 = FileAnalysisWidget(fpath=self.dir_path + "05-G5-140709_1628.wav")
        # analysis_2 = AnalysisWidget("ex1-spec.jpg")
        self.v_box.addWidget(analysis_1, 0)
        # self.v_box.addStretch()
        # size_policy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        # size_policy.setHorizontalStretch(0)
        # size_policy.setVerticalStretch(0)
        # self.v_box.setSizePolicy(size_policy)
        # self.v_box.update()

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
            # print(id(child), str(type(child).__name__) , "main_container child geometry:", str(child.geometry()))
            if not isinstance(child, QBoxLayout):
                if child.width() > width:
                    width = child.width()
                height = height + child.height()
        print(id(child), "main_container child sizehint:", width, height)
        return QSize(width, height)
    
    
    def add_file_analysis_widget(self):
        # add path as entry
        a = FileAnalysisWidget(self.dir_path)
        print("AnalysisWidget sizeHint:", str(a.sizeHint()))
        self.v_box.addStretch()
        self.v_box.addWidget(a, 0)
        # self.v_box.update()
        print("main_container sizeHint:", str(self.sizeHint()))
        self.adjustSize()
        # self.main_container.update()
        l = self.children()
        for child in l:
            print(id(child), type(child).__name__, "main_container child geometry:", str(child.geometry()))
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
