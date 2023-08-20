import os 
import random

from PyQt6.QtWidgets import (QWidget, QSizePolicy, QFileDialog,
                             QBoxLayout, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton,QMessageBox)
from PyQt6.QtCore import Qt, QSize
import pretty_midi
import pandas as pd 

from ChooseFileDialog import ChooseFileDialog
from FileAnalysis import FileAnalysis
from FigureWidget import FigureWidget
from old.analysis import *
from Fonctions import *

class MainContainer(QWidget):

    def __init__(self, app_size: tuple):
        print("MainContainer")
        super().__init__()
        dir_path = ""
        self.app_size = app_size
        self.init_midi_vars()
        self.note_list = Create_Note_list()
        self.main_dir_path = ""
        
        self.add_notes_to_midi=False

        self.generate_header_widget()
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

        self.analysis_widget=None
        self.choose_file=None
        self.add_note=False
        self.delete_note=False
        self.edit_note=False
        self.add_audio=False
        self.save=False
    
    #------Widgets----------#
    def generate_header_widget(self):
        print("generate_header_widget")
        # TODO : keep that widget and add button for midi
        self.welcoming_label = QLabel("Use the menu buttons ‘File’ then ‘Import directory’ to start the analysis.")
        self.header_box = QHBoxLayout()
        self.header_box.addWidget(self.welcoming_label)
        # self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        self.header_box.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        self.header_widget = QWidget()
        # header_widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.header_widget.setLayout(self.header_box)
        # generate_multitrack_midi_and_add_plot() -> btn
        # self.welcoming_widget.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        self.header_widget.adjustSize()
        print(id(self.header_widget), "header_widget size:", self.header_widget.size())
    

    def add_btn_to_header_widget(self):
        
        print("add_btn_to_header_widget")
        if not hasattr(self, 'midi_btn'):
            print("welcoming_widget deletion")
            self.header_box.removeWidget(self.welcoming_label)
            self.welcoming_label.deleteLater()
            # for child in self.header_box.children():
            #     child.deleteLater()
            self.analysis_btn = QPushButton("Plot all")
            self.analysis_btn.clicked.connect(self.add_plots_to_every_FileAnalysis)
            self.midi_btn = QPushButton("Generate multitrack midi file")
            self.midi_btn.clicked.connect(self.generate_multitrack_midi_file)
            self.reset_midi_btn = QPushButton("Reset midi note")
            self.reset_midi_btn.clicked.connect(self.Clear_Midi_Notes)
            self.header_box.addWidget(self.analysis_btn)
            
            self.header_box.addWidget(self.midi_btn)
            self.header_box.addWidget(self.reset_midi_btn)
            self.header_widget.adjustSize()
            self.header_widget.update()
            # self.adjustSize()
            # self.update()
        else:
            print("midi btn already exists")

    def get_ana_widget(self):
        if self.analysis_widget is not None:
            analysisWidgets = list(filter(
            lambda child: not (child is self.v_box or child is self.header_widget), 
            self.children()
        ))  
        return analysisWidgets
    
    def add_midi_figure_to_header_widget(self):
        print("add_midi_figure_to_header_widget")
        # TODO
        # read multitrack.midi to get datas
        fig = get_multitrack_fig(
            # fname=, 
            # y=, 
            sample_rate=self.sr
        )
        fig.set(figwidth=self.fig_size[0], figheight=self.fig_size[1]) # 10 = 1000px
        self.multitrack_midi_figure = FigureWidget(parent=self, figure=fig)
        # if self.played_string_detection_figure_widget.parent() is not self.figure_box:
        # self.figure = self.played_string_detection_figure_widget
        self.header_box.addWidget(self.multi_midi_plot) # ,0
        self.header_widget.adjustSize()
        self.header_widget.update()
        self.adjustSize()
        self.update()
    
    
    def add_plots_to_every_FileAnalysis(self):
        print("add_plots_to_every_FileAnalysis")
        analysisWidgets = list(filter(
            lambda child: not (child is self.v_box or child is self.header_widget), 
            self.children()
        ))
        print("number of analysis widgets : ", len(analysisWidgets))
        for aw in analysisWidgets:
            aw.add_played_string_detection_figure()
    def add_multiple_analysis_widget(self, file_paths: list):
        print("add_multiple_analysis_widget")
        self.add_btn_to_header_widget()
        for file_path in file_paths:
            self.add_single_analysis_widget(fpath=file_path)
        print(id(self), "main_container size:", str(self.size()))
    
   
    def add_single_analysis_widget(self, fpath: str):
        print("add_single_analysis_widget")
        self.analysis_widget = FileAnalysis(
            fpath=fpath, 
            note_list=self.note_list, 
            instru=self.pmidi_instru,
            app_size=self.app_size
        )
       
        self.v_box.addWidget(self.analysis_widget, 0) # + param ,0
    
    #---- Choose file-----#
    def call_ChooseFileDialog_Edit(self):
        self.edit_note=True
        self.choose_file=ChooseFileDialog(self)
        result_code=self.choose_file.exec()
        print("result code = ", result_code)

    def call_ChooseFileDialog_Add(self):
        self.add_note=True
        self.choose_file=ChooseFileDialog(self)
        result_code=self.choose_file.exec()
        print("result code = ", result_code)

    def call_ChooseFileDialog_Delete(self):
        self.delete_note=True
        self.choose_file=ChooseFileDialog(self)
        result_code=self.choose_file.exec()
        print("result code = ", result_code)

    def call_ChooseFileDialog_Add_audio(self):
        self.add_audio=True
        self.choose_file=ChooseFileDialog(self)
        result_code=self.choose_file.exec()
        print("result code = ", result_code)

    def call_ChooseFileDialog_save_file(self):
        self.save=True
        self.choose_file=ChooseFileDialog(self)
        result_code=self.choose_file.exec()
    
    def Choose_File_Edition(self,children):
        if self.analysis_widget is not None:
            analysisWidgets = list(filter(
            lambda child: not (child is self.v_box or child is self.header_widget), 
            self.children()
        ))  
        if self.choose_file is not None:
            for aw in analysisWidgets:
                name_file=os.path.basename(aw.file_path)
                if self.edit_note:
                    if self.choose_file.chosen_option==name_file[0:2]:
                        aw.header.Edit_note(aw)
                        self.edit_note=False
                if self.add_note:
                    if self.choose_file.chosen_option==name_file[0:2]:
                        aw.header.Add_Note_func(aw)
                        self.add_note=False
                if self.delete_note:
                    if self.choose_file.chosen_option==name_file[0:2]:
                        aw.header.Delete_Note_func(aw)
                        self.delete_note=False
                if self.add_audio:
                    if self.choose_file.chosen_option==name_file[0:2]:
                        aw.header.Audio_player_btn(aw)
                        self.add_audio=False
                if self.save:
                    if self.choose_file.chosen_option==name_file[0:2]:
                        aw.header.Add_notes_to_midi_instrument(aw)
                        self.midi_notes=self.pmidi_instru.notes
                        self.save_notes_to_excel()
                        self.save=False


    #--------Menu Add---------#                
    
    def Add_audio_player(self):
        if self.analysis_widget is not None:
            analysisWidgets = list(filter(
            lambda child: not (child is self.v_box or child is self.header_widget), 
            self.children()
        ))
        print("number of analysis widgets : ", len(analysisWidgets))
        for aw in analysisWidgets:
            aw.header.Audio_player_btn(aw)

    def Add_Note(self):
        
        if self.analysis_widget is not None:
            analysisWidgets = list(filter(
            lambda child: not (child is self.v_box or child is self.header_widget), 
            self.children()
        ))  
            for aw in analysisWidgets:
                aw.header.Add_Note_func(aw)

    #--------Menu Edit--------#
    def Note_edition(self):
        if self.analysis_widget is not None:
            analysisWidgets = list(filter(
            lambda child: not (child is self.v_box or child is self.header_widget), 
            self.children()
        ))
        print("number of analysis widgets : ", len(analysisWidgets))
        for aw in analysisWidgets:
            aw.header.Edit_note(aw)
            
    def Delete_Note(self):
        
        if self.analysis_widget is not None:
            analysisWidgets = list(filter(
            lambda child: not (child is self.v_box or child is self.header_widget), 
            self.children()
        ))  
            for aw in analysisWidgets:
                aw.header.Delete_Note_func(aw)
 
    #--------MIDI File--------#
    def init_midi_vars(self):
        print("init_midi_vars")
        self.pmidi = pretty_midi.PrettyMIDI()
        # Create an Instrument instance for a banjo instrument
        self.pmidi_program = pretty_midi.instrument_name_to_program('Acoustic Grand Piano')
        self.pmidi_instru = pretty_midi.Instrument(program=self.pmidi_program)
        # Add the banjo instrument to the PrettyMIDI object
        self.pmidi.instruments.append(self.pmidi_instru)

    def generate_multitrack_midi_file(self):
        #Genration d'un chiffre aleatoire pour le nom du fichier 
        liste = random.sample(range(10), 4)

        # Convertissez la liste en un nombre entier (code à 4 chiffres)
        random_code = int(''.join(map(str, liste)))
        try:
        
            # add_notes_to_midi_instrument() for each analisyswidget
            analysisWidgets = list(filter(
                lambda child: not (child is self.v_box or child is self.header_widget), 
                self.children()
            ))
            print("number of analysis widgets : ", len(analysisWidgets))
            for aw in analysisWidgets:
                aw.header.Add_notes_to_midi_instrument(aw)
            self.add_notes_to_midi=True
            if self.main_dir_path[-1]!="/":
                self.main_dir_path = self.main_dir_path + "/"
            self.midi_fname = self.main_dir_path + "multitrack"+str(random_code)+".mid"
            
            
            self.pmidi.write(self.midi_fname) # error
            QMessageBox.information(self, "Midi file", "Midi file successfully written.")
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while writting midi file: {e}")
        
            
        
        # TODO then add figure of multitrack midi to header_box
        # self.midi_fig = get_multitrack_fig(fname=self.midi_fname, y=, samp_rate=)

    def Clear_Midi_Notes(self,parent):
        
        self.init_midi_vars()
        analysisWidgets = list(filter(
            lambda child: not (child is self.v_box or child is self.header_widget), 
            self.children()
        ))
        print("number of analysis widgets : ", len(analysisWidgets))
        for aw in analysisWidgets:
            aw.is_analysis_done = False

    #-------Import-------#
    
    def import_dir(self):
        print("import_dir")
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
        if len(self.main_dir_path)!=0:
            if self.main_dir_path[-1]!="/":
                self.main_dir_path = self.main_dir_path + "/"
            try:
                dir_content = os.listdir(dir_path)
                file_paths = list(map(lambda file_name: dir_path + "/" + file_name, dir_content))
                wav_file_paths = list(filter(lambda file_path: file_path.split(".")[-1]=="wav", file_paths))
                print("wav_files", wav_file_paths)
                if len(wav_file_paths)>0:
                    self.add_multiple_analysis_widget(file_paths=wav_file_paths)
                else:
                    print("No .wav files found in ", dir_path)
                self.adjustSize()
                self.update()
            except Exception as e:
             QMessageBox.critical(self, "Error", f"An error occurred while importing file: {e}")
        
        
    def import_file(self):
        print("import_file")
        # called by the menu button "File" -> "Import file"
        # Only files with the .wav extensions will be used
        try:
            file_path, filter = QFileDialog.getOpenFileName(
                    parent=None, 
                    caption="Select a wav file to add.", 
                    # directory="", 
                    filter="Audio file (*.wav)"
                    # initialFilter=
                    # options=QFileDialog.Option
            )
            try:
                if self.main_dir_path=="":
                    fname = file_path.split("/")[-1]
                    self.main_dir_path = file_path[:-len(fname)] # has the final "/"
                if len(file_path)>0:
                    self.add_multiple_analysis_widget(file_paths=[file_path])
            except Exception as e:
             QMessageBox.critical(self, "Error", f"No .wav file selected")

        except Exception as e:
             QMessageBox.critical(self, "Error", f"An error occurred while importing file: {e}")
        self.adjustSize()
        self.update()
    
    
    def remove_FileAnalysis(self, fileAnalysis_id: int):
        print("remove_FileAnalysis called")
        for child in self.children():
            if id(child)==fileAnalysis_id:
                self.v_box.removeWidget(child)
                child.deleteLater()
                break
        self.adjustSize()
        self.update()
        # self.parent().adjustSize()
        # self.parent().update()

    #----Sauvegarde-------#
    def save_notes(self):
        self.save_all=True
        self.save=False
        self.save_notes_to_excel()
    
    def save_notes_to_excel(self):
        if self.save :
            midi_notes = self.midi_notes
        else : 
            midi_notes = self.get_all_midi_notes()  
        data = {
            'Start Time': [note.start for note in midi_notes],
            'End Time': [note.end for note in midi_notes],
            'Pitch': [note.pitch for note in midi_notes],
            'Velocity': [note.velocity for note in midi_notes],
        }
        df = pd.DataFrame(data) # here
        file_path, _ = QFileDialog.getSaveFileName(parent=None, 
                                                   caption="Save MIDI notes to Excel", 
                                                   directory="", 
                                                   filter="Excel Files (*.xlsx)")
        if file_path:
            df.to_excel(file_path, index=False)
            print('file written')

    def get_all_midi_notes(self):
        if not self.add_notes_to_midi:
            analysisWidgets = list(filter(
            lambda child: not (child is self.v_box or child is self.header_widget), 
            self.children()
        ))
        print("number of analysis widgets : ", len(analysisWidgets))
        for aw in analysisWidgets:
            aw.header.Add_notes_to_midi_instrument(aw)
        
        return self.pmidi_instru.notes
    
    def get_data_to_save(self):
        data = {
            "main_dir_path": self.main_dir_path,
            "analysis_widgets_data": [aw.get_data_to_save() for aw in self.get_ana_widget()]

        }
        return data
    
    #----Open Projet----#
    def load_data_from_project(self, project_data):
        self.add_btn_to_header_widget()
        analysis_data_list = project_data.get("analysis_widgets_data", [])
        self.main_dir_path=project_data.get("main_dir_path","")
        for aw_data in analysis_data_list:
            self.add_single_analysis_widget(fpath=aw_data["file_path"])
            analysis_widget = self.analysis_widget
            if analysis_widget:
                analysis_widget.load_data_from_project(self,aw_data)
            
            self.adjustSize()
            self.update()