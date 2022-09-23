from time import time

from PyQt6.QtWidgets import (QWidget,
                             QBoxLayout, QVBoxLayout, 
                             QSizePolicy)
from PyQt6.QtCore import QSize
from librosa import load as librosa_load
# from pretty_midi import Instrument

from FileAnalysisHeader import FileAnalysisHeader
from FigureWidget import FigureWidget
from ParamDialog import ParamDialog
from analysis import *


class FileAnalysis(QWidget):
    """Widget containing analysis of wav files, its figures and buttons to run them
    """
    def __init__(self, fpath: str, note_list: list, instru: pretty_midi.Instrument, app_size: tuple):
        super().__init__()
        self.file_path = fpath
        self.note_list = note_list
        self.instru = instru
        self.app_size = app_size
        self.init_params()

        self.header = FileAnalysisHeader(fname=self.fname, note=self.params["note_name"], parent=self)
        self.main_box = QVBoxLayout()
        self.main_box.setContentsMargins(0, 0, 0, 0)
        self.main_box.setSpacing(5)
        self.main_box.addWidget(self.header, 0)
        
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.setLayout(self.main_box)
        self.adjustSize()
    

    def sizeHint(self):
        width = 0
        height = 0
        for child in self.children():
            if not isinstance(child, QBoxLayout):
                if child.width() > width:
                    width = child.width()
                height = height + child.height() + 5
        print(id(self), "FileAnalysis sizeHint :", width, height)
        return QSize(width, height)
    
    
    def init_params(self):
        print("file path : ", self.file_path)
        self.fname = self.file_path.split("/")[-1]
        note_name, midi_note = get_note_guessed_from_fname(note_list=self.note_list, fname=self.fname)
        # print("Guessed note :", self.params["note_name"])
        self.params = {
            "note_name": note_name,
            "midi_note": midi_note,
            "note_list": self.note_list,
            "duration_for_analysis": 60, # duration of each wav that is analyzed
            "filter_timescale": 80, # parameter for note segmentation : median filter lenght, the larger the smoother the signal envelop
            "threshold": 0.15, # parameter for note segmentation : energy level above which a note occurrence is detected
            "min_note_duration": 0.03 # parameter for note segmentation : minimal duration below which a note occurrence is discarded
        }
        self.fig_size: list = self.get_figure_size()
        self.is_analysis_done = False
    
    
    def generate_analysis(self):
        start = time()
        self.y, self.sr = librosa_load(
            self.file_path, 
            offset=0, 
            duration=self.params["duration_for_analysis"], 
            sr=None)
        print("Duration of librosa.load() :", str(time()-start)) # long : 4 to 5 seconds when resampling
        self.amplitude_envelope = get_amplitude_envelope(y=self.y, filter_timescale=self.params["filter_timescale"])
        self.decal = get_decal(y=self.y, amplitude_envelope=self.amplitude_envelope, threshold=self.params["threshold"])
        self.is_analysis_done = True
        print("Duration of generate_analysis() :", str(time()-start))

    
    def add_time_series_figure(self):
        start = time()
        if not self.is_analysis_done:
            self.generate_analysis()
        fig = get_time_series_fig(y=self.y, samp_rate=self.sr)
        fig.set(figwidth=self.fig_size[0], figheight=self.fig_size[1]) # 10 = 1000px
        self.time_series_figure_widget = FigureWidget(parent=self, figure=fig)
        # self.figure = self.time_series_figure_widget
        self.main_box.addWidget(self.time_series_figure_widget, 0)
        
        print("Duration of add_time_series_figure() :", str(time()-start))
        self.adjustSize()
        self.update()
        self.parent().adjustSize()
        self.parent().update()

    
    def add_played_string_detection_figure(self):
        start = time()
        if not self.is_analysis_done:
            self.generate_analysis()
        fig = get_pitch_detection_fig(
            ampl_envel=self.amplitude_envelope, 
            threshold=self.params["threshold"], 
            min_duration=self.params["min_note_duration"], 
            # instru=self.instru, 
            decal=self.decal, 
            # midi_note=self.params["midi_note"], 
            sample_rate=self.sr
        )
        fig.set(figwidth=self.fig_size[0], figheight=self.fig_size[1]) # 10 = 1000px
        self.played_string_detection_figure_widget = FigureWidget(parent=self, figure=fig)
        # if self.played_string_detection_figure_widget.parent() is not self.figure_box:
        # self.figure = self.played_string_detection_figure_widget
        self.main_box.addWidget(self.played_string_detection_figure_widget, 0)
        print("Duration of add_played_string_detection_figure() :", str(time()-start))
        self.adjustSize()
        self.update()
        self.parent().adjustSize()
        self.parent().update()
        # write_midi_file(banjo_MIDI, 'marovany.mid')
        # get_multitrack_plot("marovany.mid")
    
    
    def add_figures(self):
        self.add_time_series_figure()
        self.add_played_string_detection_figure()
        self.adjustSize()
        self.update()
        self.parent().adjustSize()
        self.parent().update()
        self.add_notes_to_midi_instrument()


    def add_notes_to_midi_instrument(self):
        if not self.is_analysis_done:
            self.generate_analysis()
        if self.params["midi_note"] != None:
            for start_ind, end_ind in zip(np.where(self.decal==1)[0], np.where(self.decal==-1)[0]):
                if (end_ind - start_ind)/self.sr > self.params["min_note_duration"]:
                    # Create a Note instance for each note
                    note = pretty_midi.Note(
                        velocity=100, 
                        pitch=round(self.params["midi_note"]), 
                        start=start_ind/self.sr, 
                        end=end_ind/self.sr
                    )
                    self.instru.notes.append(note)
        else:
            print("ERROR : Note not identified. No note added to instrument")
    
    
    def get_figure_size(self):
        # retrieve size of scroll_area widget
        app_width, app_height = self.app_size
        # app_width = 1579
        # app_height = 918
        duration = self.params["duration_for_analysis"]
        fig_width = app_width / 30 * duration / 100 # Default width is 1 full width = 30 secs
        fig_height = app_height * 0.3 / 100 # Default height is 1/3 of app height. / 100 to convert to matplotlib's size
        fig_width = max(fig_width, app_width / 2 / 100) # half of window’s width as min
        fig_width = min(fig_width, 40) # 3400px max
        print("fig size is", fig_width, fig_height)
        return [fig_width, fig_height]


    def remove_self(self):
        self.parent().remove_FileAnalysis(fileAnalysis_id=id(self))
    
    
    def remove_FigureWidget(self, figure_id: int):
        print("remove_FigureWidget called")
        for child in self.children():
            if id(child)==figure_id:
                self.main_box.removeWidget(child)
                child.deleteLater()
                break
        self.adjustSize()
        self.update()
        self.parent().adjustSize()
        self.parent().update()


    def call_ParamDialog(self):
        param_dialog = ParamDialog(self)
        result_code = param_dialog.exec()
        print("result code = ", result_code)
        if result_code==1:
            print("New params :")
            for k, v in self.params.items():
                print(k, v)


    def store_new_params(self, new_params: dict):
        # called by ParamDialog when params are changed by the user
        print("store_new_params called")
        self.params = new_params
        self.is_analysis_done = False
