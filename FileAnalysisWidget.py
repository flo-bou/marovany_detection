from time import time

from PyQt6.QtWidgets import (QWidget, QLabel, QBoxLayout, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QSizePolicy)
from PyQt6.QtCore import Qt, QSize
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
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        # self.generate_analysis()
        
        self.time_series_btn = QPushButton("Plot times series")
        self.time_series_btn.clicked.connect(self.add_time_series_figure)
        self.time_series_btn.adjustSize()
        self.note_detection_btn = QPushButton("Plot note detection")
        self.note_detection_btn.clicked.connect(self.add_played_string_detection_figure)
        self.note_detection_btn.adjustSize()
        self.params_btn = QPushButton("Params")
        self.params_btn.adjustSize()
        self.title_label = QLabel(fpath)
        self.title_label.adjustSize()
        # self.params_btn.clicked.connect(self.openDialog)

        self.header_box = QHBoxLayout()
        # self.header_box.setSpacing(2)
        self.header_box.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.header_box.addWidget(self.time_series_btn)
        self.header_box.addWidget(self.note_detection_btn)
        self.header_box.addWidget(self.params_btn)
        self.header_box.addWidget(self.title_label)
        
        self.figure_box = QVBoxLayout() # box where figures will be added

        self.main_box = QVBoxLayout()
        # self.main_box.setSpacing(5)
        self.main_box.addLayout(self.header_box)
        self.main_box.addLayout(self.figure_box)

        self.setLayout(self.main_box)
        # print(id(self), "AnalysisWidget size:", str(self.size()))
        print(id(self), "FileAnalysisWidget sizeHint at init:", str(self.sizeHint()))
        # print("header_box.spacing():", self.main_box.spacing())
        # print("figure_box.spacing():", self.main_box.spacing())
        # print("main_box.spacing():", self.main_box.spacing())
        self.adjustSize()
        print(id(self), "FileAnalysisWidget size at init:", str(self.size()))


    def sizeHint(self):
        width = self.width()
        height = 0
        print("FileAnalysisWidget children numbers", len(self.children()))
        for child in self.children():
            if not isinstance(child, QBoxLayout):
                # print(id(child), str(type(child).__name__) , "FileAnalysisWidget child size:", str(child.size()))
                if child.width() > width:
                    width = child.width()
                height = height + child.height()
            else:
                print(id(child), str(type(child).__name__) , "FileAnalysisWidget child")
        return QSize(width, height)
    

    def init_var(self):
        # self.do_plot = True
        # self.verbose = True
        self.midi_note = get_note_guessed_from_fname(note_list=self.note_list, fname=self.file_path)
        print("Guessed note :", self.midi_note)
        ## Some user parameters 
        self.duration_for_analysis = 10 # duration of each wav that is analyzed
        self.filter_timescale = 80 # parameter for note segmentation : median filter lenght, the larger the smoother the signal envelop
        self.threshold = 0.15 # parameter for note segmentation : energy level above which a note occurrence is detected
        self.min_duration = 0.03 # parameter for note segmentation : minimal duration below which a note occurrence is discarded
        self.fig_size: list = self.get_figure_size()
        self.is_analysis_done = False
    
    
    def generate_analysis(self):
        # if verbose:
        #     print('\n Now processing file', wav_file)
        # audio data loading
        # print("Start of analysis")
        start = time()
        self.y, self.sr = librosa_load(self.file_path, offset=0, duration=self.duration_for_analysis, sr=None)
        print("Duration of librosa.load() :", str(time()-start)) # long : 4 to 5 seconds
        self.amplitude_envelope = get_amplitude_envelope(y=self.y, filter_timescale=self.filter_timescale)
        self.decal = get_decal(y=self.y, amplitude_envelope=self.amplitude_envelope, threshold=self.threshold)
        self.is_analysis_done = True
        print("Duration of generate_analysis() :", str(time()-start))

    
    def add_time_series_figure(self):
        start = time()
        if not self.is_analysis_done:
            self.generate_analysis()
        fig = get_time_series_fig(y=self.y, samp_rate=self.sr)
        fig.set(figwidth=self.fig_size[0], figheight=self.fig_size[1]) # 10 = 1000px
        self.time_series_figure_widget = FigureWidget(
            figure=fig
        )
        # parent = self.time_series_figure_widget.parentWidget()
        # print(id(widget), type(widget).__name__, parent.id(), type(parent).__name__)
        # test if time_series_figure_widget was already in figure box (it has been generated previously)
        # if self.time_series_figure_widget.parent() is not self.figure_box:
        self.figure_box.addWidget(self.time_series_figure_widget)
        
        print("Duration of add_time_series_figure() :", str(time()-start))
        print(id(self), "AnalysisWidget sizeHint:", str(self.sizeHint()))
        self.adjustSize()
        print(id(self), "AnalysisWidget size:", str(self.size()))
        
        print("FileAnalysis parent :", self.parent()) # MainContainer
        print(id(self.parent()), "AnalysisWidget parent sizeHint:", str(self.parent().sizeHint()))
        self.parent().adjustSize()
        print(id(self.parent()), "AnalysisWidget parent size:", str(self.parent().size()))
        # self.figure_box.update()

    
    def add_played_string_detection_figure(self):
        start = time()
        if not self.is_analysis_done:
            self.generate_analysis()
        fig = get_pitch_detection_fig_and_add_note_to_instru(
            ampl_envel=self.amplitude_envelope, 
            threshold=self.threshold, 
            min_duration=self.min_duration, 
            instru=self.instru, 
            decal=self.decal, 
            midi_note=self.midi_note, 
            sample_rate=self.sr
        )
        fig.set(figwidth=self.fig_size[0], figheight=self.fig_size[1]) # 10 = 1000px
        self.played_string_detection_figure_widget = FigureWidget(
            figure=fig
        )
        # if self.played_string_detection_figure_widget.parent() is not self.figure_box:
        self.figure_box.addWidget(self.played_string_detection_figure_widget)
        
        print("Duration of add_time_series_figure() :", str(time()-start))
        print(id(self), "AnalysisWidget sizeHint:", str(self.sizeHint()))
        self.adjustSize()
        print(id(self), "AnalysisWidget size:", str(self.size()))
        
        print("FileAnalysis parent :", self.parent()) # MainContainer
        print(id(self.parent()), "AnalysisWidget parent sizeHint:", str(self.parent().sizeHint()))
        self.parent().adjustSize()
        print(id(self.parent()), "AnalysisWidget parent size:", str(self.parent().size()))
        
        # write_midi_file(banjo_MIDI, 'marovany.mid')
        # get_multitrack_plot("marovany.mid")
    
    
    def get_figure_size(self):
        screen_width = 1579
        screen_height = 918
        duration = self.duration_for_analysis
        # Default width is 1 full width = 30 secs
        fig_width = screen_width / 30 * duration / 100
        # Default height is 1/3 of full width. / 100 to convert to matplotlib's size
        fig_height = screen_height * 0.3 / 100
        fig_width = max(fig_width, screen_width / 2 / 100) # half of window’s width as min
        fig_width = min(fig_width, 40) # 3400px max
        print("fig size is", fig_width, fig_height)
        return [fig_width, fig_height]
