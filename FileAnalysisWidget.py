from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QSizePolicy)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from FigureWidget import FigureWidget
from analysis import *

class FileAnalysisWidget(QWidget):
    """Widget containing analysis of wav files, its figures and buttons to run them
    """
    
    def __init__(self, fpath: str):
        super().__init__()
        self.file_path = fpath
        self.init_var()
        self.generate_analysis()
        # print("devicePixelRatio", self.devicePixelRatio())

        self.title_box = QHBoxLayout()
        self.title_box.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.title_box.addWidget(QPushButton("Plot times series"))
        self.title_box.addWidget(QPushButton("Plot note detection"))
        self.title_box.addWidget(QPushButton("Params"))
        self.title_box.addWidget(QLabel(fpath))
        
        self.plot_box = QVBoxLayout()
        self.time_series_figure_widget = FigureWidget(
            figure=get_time_series_fig(y=self.y, samp_rate=self.sr)
        )
        # self.pitch_detection_figure_widget = FigureWidget(
        #     figure=get_pitch_detection_fig(fig_size=self.fig_size, ampl_envel=self.amplitude_envelope, threshold=self.threshold,min_duration=self.min_duration, instru=, decal=self.decal, midi_note=, sample_rate=self.sr)
        # )
        self.plot_box.addWidget(self.time_series_figure_widget)
        # self.plot_box.addWidget(self.pitch_detection_figure_widget)

        self.main_box = QVBoxLayout()
        self.main_box.addLayout(self.title_box)
        self.main_box.addLayout(self.plot_box)
        # self.main_box.addLayout(self.plot_box)
        # print(id(self), "main_box geometry:", str(self.main_box.geometry()))

        self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        self.setLayout(self.main_box)
        # print(id(self), "AnalysisWidget size:", str(self.size()))
        print(id(self), "AnalysisWidget sizeHint:", str(self.sizeHint()))
        self.adjustSize()
        # print(id(self), "left_box sizehint:", str(self.left_box.sizeHint()))
        # print(id(self), "left_box geometry:", str(self.left_box.geometry()))
        # print(id(self), "right_box sizehint:", str(self.right_box.sizeHint()))
        # print(id(self), "right_box geometry:", str(self.right_box.geometry()))
        print(id(self), "AnalysisWidget size:", str(self.size()))
        # print(id(self), "AnalysisWidget sizePolicy:", self.sizePolicy().horizontalStretch(), self.sizePolicy().verticalStretch())

    
    def create_note_list(self):
        note_letters = ['E','D','B','G']
        note_numbers = range(10)
        note_commas = ['', '#']
        note_names = []
        for nl in note_letters:
            for nn in note_numbers:
                for nc in note_commas:
                    note_names.append(nl + str(nn) + nc)
        return note_names
    

    def init_var(self):
        # self.do_plot = True
        # self.verbose = True
        self.note_list = self.create_note_list()
        ## Some user parameters 
        self.duration_for_analysis = 20 # duration of each wav that is analyzed
        self.filter_timescale = 80 # parameter for note segmentation : median filter lenghth, the larger the smoother the signal envelop
        self.threshold = 0.15 # parameter for note segmentation : energy level above which a note occurrence is detected
        self.min_duration = 0.03 # parameter for note segmentation : minimal duration below which a note occurrence is discarded 
        # self.wav_list = glob.glob('capteurs/*wav')
        # Create a PrettyMIDI object
    
    
    def generate_analysis(self):
        # if verbose:
        #     print('\n Now processing file', wav_file)
        # audio data loading
        print("Start of analysis")
        self.y, self.sr = librosa.load(self.file_path, offset=0, duration=self.duration_for_analysis)
        self.amplitude_envelope = get_amplitude_envelope(y=self.y, filter_timescale=self.filter_timescale)
        self.decal = get_decal(y=self.y ,amplitude_envelope=self.amplitude_envelope, threshold=self.threshold)
