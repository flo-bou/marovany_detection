from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import pretty_midi

from FigureWidget import FigureWidget
from analysis import *

class FileAnalysisWidget(QWidget):
    """Widget containing analysis of wav files, its figures and buttons to run them
    """
    
    banjo_MIDI = pretty_midi.PrettyMIDI()
    # Create an Instrument instance for a banjo instrument
    banjo_program = pretty_midi.instrument_name_to_program('Banjo')
    banjo_instru = pretty_midi.Instrument(program=banjo_program)
    # Add the banjo instrument to the PrettyMIDI object
    banjo_MIDI.instruments.append(banjo_instru)
    
    def __init__(self, path):
        super().__init__()
        self.init_var()
        self.analyse()
        # print("devicePixelRatio", self.devicePixelRatio())

        self.button_box = QVBoxLayout()
        self.button_box.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.button_box.addWidget(QPushButton("Hi !"))
        self.button_box.addWidget(QPushButton("Hi too !"))
        
        self.plot_box = QVBoxLayout()
        # self.left_box.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)
        self.plot_box.addWidget(QLabel("Very long text indeed."))
        # self.left_box.addWidget(self.create_img_label(path))
        self.plot_box.addWidget(FigureWidget(figure=get_time_series_fig(fig_size=self.fig_size, y=self.y, samp_rate=self.sr)))

        self.main_box = QHBoxLayout()
        self.main_box.addLayout(self.button_box)
        self.main_box.addLayout(self.plot_box)
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
    
    def create_img_label(self, path):
        img = QPixmap()
        if not img.load(path):
            print(id(self), "img loading failed")
        print(id(self), "img size:", str(img.size()))
        img_label = QLabel()
        # print(id(self), "img_label sizeHint:", str(img_label.sizeHint()))
        img_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        # print("label sizeHint:", str(img_label.sizeHint()))
        img_label.setPixmap(img)
        print(id(self), "img_label sizeHint:", str(img_label.sizeHint()))
        img_label.adjustSize()
        # img_label.setGeometry()
        print(id(self), "img_label size:", str(img_label.size()))
        return img_label
    
    # def sizeHint(self):
    #     # size is fixed
    #     width = 1400
    #     height = 400
    #     return QSize(width, height)
    

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
        
    def analyse(self):
        # if verbose:
        #     print('\n Now processing file', wav_file)
        # audio data loading
        self.y, self.sr = librosa.load(wav_file, offset=0, duration=self.duration_for_analysis)
        self.amplitude_envelope = get_amplitude_envelope(y=self.y, filter_timescale=self.filter_timescale)
        self.decal = get_decal(self.amplitude_envelope, self.threshold)
        self.midi_note = get_note_guessed_from_fname(note_list=self.note_list, fname=wav_file)
        print("Guessed note :", midi_note)