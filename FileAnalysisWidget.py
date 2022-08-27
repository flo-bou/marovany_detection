from time import time

from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QSizePolicy)
from PyQt6.QtCore import Qt
from librosa import load as librosa_load
# from pretty_midi import Instrument

from FigureWidget import FigureWidget
from analysis import *


class FileAnalysisWidget(QWidget):
    """Widget containing analysis of wav files, its figures and buttons to run them
    """
    def __init__(self, fpath: str, note_list: list, instru: pretty_midi.Instrument):
        super().__init__()
        self.file_path = fpath
        self.note_list = note_list
        self.instru = instru
        self.init_var()
        # self.generate_analysis()
        
        self.time_series_btn = QPushButton("Plot times series")
        self.time_series_btn.clicked.connect(self.add_time_series_figure)
        self.note_detection_btn = QPushButton("Plot note detection")
        self.note_detection_btn.clicked.connect(self.add_played_string_detection_figure)
        self.params_btn = QPushButton("Params")
        # self.params_btn.clicked.connect(self.openDialog)

        self.header_box = QHBoxLayout()
        self.header_box.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.header_box.addWidget(self.time_series_btn)
        self.header_box.addWidget(self.note_detection_btn)
        self.header_box.addWidget(self.params_btn)
        self.header_box.addWidget(QLabel(fpath))
        
        self.figure_box = QVBoxLayout() # box where figures will be added

        self.main_box = QVBoxLayout()
        self.main_box.addLayout(self.header_box)
        self.main_box.addLayout(self.figure_box)

        self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        self.setLayout(self.main_box)
        # print(id(self), "AnalysisWidget size:", str(self.size()))
        print(id(self), "AnalysisWidget sizeHint:", str(self.sizeHint()))
        self.adjustSize()
        print(id(self), "AnalysisWidget size:", str(self.size()))


    def init_var(self):
        # self.do_plot = True
        # self.verbose = True
        self.midi_note = get_note_guessed_from_fname(note_list=self.note_list, fname=self.file_path)
        print("Guessed note :", self.midi_note)
        ## Some user parameters 
        self.duration_for_analysis = 20 # duration of each wav that is analyzed
        self.filter_timescale = 80 # parameter for note segmentation : median filter lenghth, the larger the smoother the signal envelop
        self.threshold = 0.15 # parameter for note segmentation : energy level above which a note occurrence is detected
        self.min_duration = 0.03 # parameter for note segmentation : minimal duration below which a note occurrence is discarded 
        # self.wav_list = glob.glob('capteurs/*wav')
        # Create a PrettyMIDI object
        self.decal = None
    
    
    def generate_analysis(self):
        # if verbose:
        #     print('\n Now processing file', wav_file)
        # audio data loading
        # print("Start of analysis")
        start = time()
        self.y, self.sr = librosa_load(self.file_path, offset=0, duration=self.duration_for_analysis)
        self.amplitude_envelope = get_amplitude_envelope(y=self.y, filter_timescale=self.filter_timescale)
        self.decal = get_decal(y=self.y, amplitude_envelope=self.amplitude_envelope, threshold=self.threshold)
        end = time()
        print("Duration of generate_analysis() :", str(end-start))


    def add_time_series_figure(self):
        if not self.decal: # TODO ValueError: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()
            self.generate_analysis()
        self.time_series_figure_widget = FigureWidget(
            figure=get_time_series_fig(y=self.y, samp_rate=self.sr)
        )
        # parent = self.time_series_figure_widget.parentWidget()
        # print(id(widget), type(widget).__name__, parent.id(), type(parent).__name__)
        if self.time_series_figure_widget.parent() is not self.figure_box:
            self.figure_box.addWidget(self.time_series_figure_widget)
        self.adjustSize()
        # self.figure_box.update()

    
    def add_played_string_detection_figure(self):
        if not self.decal:
            self.generate_analysis()
        self.played_string_detection_figure_widget = FigureWidget(
            figure=get_pitch_detection_fig_and_add_note_to_instru(
                ampl_envel=self.amplitude_envelope, 
                threshold=self.threshold, 
                min_duration=self.min_duration, 
                instru=self.instru, 
                decal=self.decal, 
                midi_note=self.midi_note, 
                sample_rate=self.sr
            )
        )
        if self.played_string_detection_figure_widget.parent() is not self.figure_box:
            self.figure_box.addWidget(self.played_string_detection_figure_widget)
        self.adjustSize()
