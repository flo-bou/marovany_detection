from os import scandir, listdir

from PyQt6.QtWidgets import (QWidget, QSizePolicy, QFileDialog,
                             QBoxLayout, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton)
from PyQt6.QtCore import QSize
import pretty_midi

from FileAnalysisWidget import FileAnalysisWidget
from analysis import *

class MainContainer(QWidget):

    def __init__(self):
        super().__init__()
        self.dir_path = ""
        self.init_midi_vars()
        self.note_list = create_note_list()
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.v_box = QVBoxLayout()
        # self.v_box.setSpacing(2)
        self.add_header_widget()
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
    
    
    def add_header_widget(self):
        # TODO : keep that widget and add button for midi
        self.welcoming_label = QLabel("Use the menu buttons ‘File > Import directory’ to start the analysis.")
        self.header_box = QHBoxLayout()
        self.header_box.addWidget(self.welcoming_label)
        
        self.header_widget = QWidget()
        self.header_widget.setLayout(self.header_box)
        # generate_multitrack_midi_and_add_plot() -> btn
        # self.welcoming_widget.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        self.header_widget.adjustSize()
        print(id(self.header_widget), "header_widget size:", self.header_widget.size())
        self.v_box.addWidget(self.header_widget)
    
    
    def update_header_widget(self):
        print("welcoming_widget deletion")
        self.header_box.removeWidget(self.welcoming_label)
        for child in self.header_box.children():
            child.deleteLater()
        
        self.midi_btn = QPushButton("Generate multitrack midi")
        self.midi_btn.clicked.connect(self.generate_multitrack_midi_file_and_add_plot)
        self.analysis_btn = QPushButton("Analyze all")
        self.analysis_btn.clicked.connect(self.add_plots_to_fileAnalysisWidgets)

        self.header_box.addWidget(self.midi_btn)
        self.header_box.addWidget(self.analysis_btn)
        # self.header_box.adjustSize()
        self.header_widget.adjustSize()

    
    def add_plots_to_fileAnalysisWidgets(self):
        pass
    
    
    def generate_multitrack_midi_file_and_add_plot(self):
        print(len(self.children())) # 15 (1 layout + 1 header + 13 analysis )
        # add_notes_to_instru_from_decal() for each analisyswidget
        analysisWidgets = list(filter(
            lambda child: not (child is self.v_box or child is self.header_widget), 
            self.children()
        ))
        print(len(analysisWidgets))
        for analysisWidget in analysisWidgets: # parcours des enfants des enfants ?
            if not analysisWidget.is_analysis_done:
                analysisWidget.generate_analysis()
            analysisWidget.add_notes_to_instru_from_decal()
        self.midi_fname = self.dir_path + "/multitrack.mid"
        self.pmidi.write(self.midi_fname)
        print("midi written")
        # self.midi_fig = get_multitrack_fig(fname=self.midi_fname, y=, samp_rate=)
    
    
    def add_multiple_analysis_widget(self, file_paths: list):
        self.update_header_widget()
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

    
    def open_dir(self):
        # Only files with the .wav extensions will be used
        self.dir_path = QFileDialog.getExistingDirectory(parent=None, caption="Choose a directory containing wav files to analyse.", directory="", options=QFileDialog.Option.ShowDirsOnly)
        print(str(self.dir_path))
        dir_content = listdir(self.dir_path)
        print("dir_content", dir_content)
        file_paths = list(map(lambda file_name: self.dir_path + "/" + file_name, dir_content))
        print("file_paths", file_paths)
        wav_file_paths = list(filter(lambda file_path: file_path.split(".")[-1]=="wav", file_paths))
        print("wav_files", wav_file_paths)
        if len(wav_file_paths)>0:
            self.add_multiple_analysis_widget(file_paths=wav_file_paths)
        else:
            print("No .wav files found in ", self.dir_path)
