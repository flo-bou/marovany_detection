from os import listdir

from PyQt6.QtWidgets import (QWidget, QSizePolicy, QFileDialog,
                             QBoxLayout, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton)
from PyQt6.QtCore import Qt, QSize
import pretty_midi

from FileAnalysis import FileAnalysis
from analysis import *

class MainContainer(QWidget):

    def __init__(self, app_size: tuple):
        super().__init__()
        dir_path = ""
        self.app_size = app_size
        self.init_midi_vars()
        self.note_list = create_note_list()
        self.main_dir_path = ""
        
        self.header_widget = self.get_header_widget()
        self.v_box = QVBoxLayout()
        self.v_box.addWidget(self.header_widget, 0)
        self.v_box.setContentsMargins(10, 0, 0, 0)
        self.v_box.setSpacing(1)
        # self.v_box.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        # self.setStyleSheet("FileAnalysis {border: 1px solid}")
        self.setLayout(self.v_box)
        # self.setStyleSheet("FileAnalysis {border: 1px solid}")
        self.adjustSize()
        self.update()
        print(id(self), "main_container size:", str(self.size()))
        # self.update()
    
    
    def sizeHint(self):
        width = self.width()
        height = 0
        for child in self.children():
            if not isinstance(child, QBoxLayout):
                if child.width() > width:
                    width = child.width()
                height = height + child.height() + 10
        print(id(self), "MainContainer sizeHint :", width, height)
        return QSize(width, height)
    
    
    def get_header_widget(self):
        # TODO : keep that widget and add button for midi
        self.welcoming_label = QLabel("Use the menu buttons ‘File’ then ‘Import directory’ to start the analysis.")
        self.header_box = QHBoxLayout()
        self.header_box.addWidget(self.welcoming_label)
        # self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        self.header_box.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        header_widget = QWidget()
        # header_widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        header_widget.setLayout(self.header_box)
        # generate_multitrack_midi_and_add_plot() -> btn
        # self.welcoming_widget.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        header_widget.adjustSize()
        print(id(header_widget), "header_widget size:", header_widget.size())
        return header_widget
    
    
    def update_header_widget(self):
        if not hasattr(self, 'midi_btn'):
            print("welcoming_widget deletion")
            self.header_box.removeWidget(self.welcoming_label)
            self.welcoming_label.deleteLater()
            # for child in self.header_box.children():
            #     child.deleteLater()
            self.midi_btn = QPushButton("Generate multitrack midi")
            self.midi_btn.clicked.connect(self.generate_multitrack_midi_file_and_add_plot)
            self.analysis_btn = QPushButton("Analyze all")
            self.analysis_btn.clicked.connect(self.add_plots_to_FileAnalysiss)
            
            self.header_box.addWidget(self.midi_btn)
            self.header_box.addWidget(self.analysis_btn)
            # self.header_box.adjustSize()
            self.header_widget.adjustSize()
            self.header_widget.update()
            # self.adjustSize()
            # self.update()
        else:
            print("midi btn already exists")
    
    
    def add_plots_to_FileAnalysiss(self):
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
        if self.main_dir_path[-1]!="/":
            self.main_dir_path = self.main_dir_path + "/"
        self.midi_fname = self.main_dir_path + "multitrack.mid"
        self.pmidi.write(self.midi_fname) # error
        print("midi written")
        # self.midi_fig = get_multitrack_fig(fname=self.midi_fname, y=, samp_rate=)
    
    
    def init_midi_vars(self):
        self.pmidi = pretty_midi.PrettyMIDI()
        # Create an Instrument instance for a banjo instrument
        self.pmidi_program = pretty_midi.instrument_name_to_program('Banjo')
        self.pmidi_instru = pretty_midi.Instrument(program=self.pmidi_program)
        # Add the banjo instrument to the PrettyMIDI object
        self.pmidi.instruments.append(self.pmidi_instru)
    
    
    def import_dir(self):
        # called by the menu button "File" -> "Import directory"
        # Only files with the .wav extensions will be used
        dir_path = QFileDialog.getExistingDirectory(
                parent=None, 
                caption="Select the directory containing wav files to analyse.", 
                # directory="", 
                options=QFileDialog.Option.ShowDirsOnly
        )
        if self.main_dir_path=="":
            self.main_dir_path = dir_path
        if self.main_dir_path[-1]!="/":
            self.main_dir_path = self.main_dir_path + "/"
        dir_content = listdir(dir_path)
        file_paths = list(map(lambda file_name: dir_path + "/" + file_name, dir_content))
        wav_file_paths = list(filter(lambda file_path: file_path.split(".")[-1]=="wav", file_paths))
        print("wav_files", wav_file_paths)
        if len(wav_file_paths)>0:
            self.add_multiple_analysis_widget(file_paths=wav_file_paths)
        else:
            print("No .wav files found in ", dir_path)
        self.adjustSize()
        self.update()
        
        
    def import_file(self):
        # called by the menu button "File" -> "Import file"
        # Only files with the .wav extensions will be used
        file_path, filter = QFileDialog.getOpenFileName(
                parent=None, 
                caption="Select a wav file to add.", 
                # directory="", 
                filter="Audio file (*.wav)"
                # initialFilter=
                # options=QFileDialog.Option
        )
        if self.main_dir_path=="":
            fname = file_path.split("/")[-1]
            self.main_dir_path = file_path[:-len(fname)] # has the final "/"
        if len(file_path)>0:
            self.add_multiple_analysis_widget(file_paths=[file_path])
        else:
            print("No .wav file selected")
        self.adjustSize()
        self.update()
    
    
    def add_multiple_analysis_widget(self, file_paths: list):
        self.update_header_widget()
        for file_path in file_paths:
            self.add_single_analysis_widget(fpath=file_path)
        print(id(self), "main_container size:", str(self.size()))
    
    
    def add_single_analysis_widget(self, fpath: str):
        analysis_widget = FileAnalysis(
            fpath=fpath, 
            note_list=self.note_list, 
            instru=self.pmidi_instru,
            app_size=self.app_size
        )
        self.v_box.addWidget(analysis_widget, 0) # + param ,0
