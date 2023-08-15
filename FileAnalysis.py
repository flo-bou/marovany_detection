from time import time

from PyQt6.QtWidgets import (QWidget, QBoxLayout, QVBoxLayout, 
                             QSizePolicy, QMessageBox)
from PyQt6.QtCore import QSize
from matplotlib.widgets import Cursor
import sounddevice as sd
import librosa
# from scipy.io import wavfile
# from pretty_midi import Instrument

from ParamDialog import ParamDialog
from FigureWidget import FigureWidget
from FileAnalysisHeader import FileAnalysisHeader
from analysis import *
from Fonctions import * 


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

        
        self.onsets_lines=None
        self.offsets_lines=None
        self.threshold_on_lines=None
        self.threshold_off_lines=None

        self.xdata=None
        self.xlim=None
        self.onset_initial=None
        self.offset_initial =None
        self.add_note_initial=None

        self.figures_visible = False
        self.finish=False
        self.onset_edit=False
        self.offset_edit=False
        self.Add_note_edit=False

        self.cursor_onset=None
        self.cursor_offset=None
        self.cursor_add_note=None

      
        self.zoom_button_bool=False
        self.audio_load=False
        self.onsets=[]
        self.offsets=[]
        self.notes=[]

        self.fig, self.ax =None,None
        self.audio,self.sr=None,None
        self.header = FileAnalysisHeader(fname=self.fname, note=self.params["note_name"], parent=self)
        self.main_box = QVBoxLayout()
        self.main_box.setContentsMargins(0, 0, 0, 0)
        self.main_box.setSpacing(5)
        self.main_box.addWidget(self.header, 0)
        
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.setLayout(self.main_box)
        self.adjustSize()
    

    def init_params(self):
        print("init_params")
        print("file path : ", self.file_path)
        self.fname = self.file_path.split("/")[-1]
        note_name, midi_note = get_note_guessed_from_fname(note_list=self.note_list, fname=self.fname)
        
        self.params = {
            "note_name": note_name,
            "midi_note": midi_note,
            "note_list": self.note_list,
            "duration_for_analysis": 10, # duration of each wav that is analyzed
            "filter_timescale": 80, # parameter for note segmentation : median filter lenght, the larger the smoother the signal envelop
            "Onsets threshold":0, # parameter for note segmentation : energy level above which a note occurrence is detected
            "Offsets threshold": 0,
            "min_note_duration": 0.1 # parameter for note segmentation : minimal duration below which a note occurrence is discarded
        }
        print("Guessed note :", self.params["note_name"])
        self.fig_size: list = self.get_figure_size()
        self.is_analysis_done = False
    

    def Zoom(self, event):
        if event.xdata is not None and event.ydata is not None:
            if event.button == 1:  # Vérifier si le bouton relâché est le bouton gauche de la souris (zoom effectué)
                # Récupérer les limites de l'axe x après le zoom
                self.xlim = event.inaxes.get_xlim()
                self.xdata = event.xdata
                if len(self.audio)!=0:
                    accueil=len(self.audio)/self.sr
                    # Show the button when zoom is performed
                    if not self.zoom_button_bool and (self.xlim[1]-self.xlim[0])<accueil:
                        self.header.Zoom_Analysis_btn(self)
                        self.zoom_button_bool=True
                        
    #--------analysis widget--------#
    def sizeHint(self):
        print("sizeHint FileAnalysis")
        width = 0
        height = 0
        for child in self.children():
            if not isinstance(child, QBoxLayout):
                if child.width() > width:
                    width = child.width()
                height = height + child.height() + 5
        print(id(self), "FileAnalysis sizeHint :", width, height)
        return QSize(width, height)
    
    
    #--------Analysis--------#  
    def generate_analysis(self):
        start = time()
        self.audio_load=True
        # self.sr, self.audio = wavfile.read(self.file_path)
        self.audio, self.sr = librosa.load(self.file_path, sr=None)
        self.audio =np.real(Denoise(self.audio,self.sr))

        #Normaliser l'audio 
        self.norm_signal= normalize_audio(self.audio)
        self.amplitude_envelope=get_amplitude_envelope(self.norm_signal,filter_timescale=self.params["filter_timescale"])
       
        threshold_on=np.max(self.amplitude_envelope)*0.2
        
        self.params["Onsets threshold"]=threshold_on
        self.params["Offsets threshold"]=threshold_on-threshold_on*0.7

        #print("Duration of librosa.load() :", str(time()-start)) # long : 4 to 5 seconds when resampling
       
        #self.decal = get_decal(y=self.y, amplitude_envelope=self.amplitude_envelope, threshold=self.params["threshold"])
        
        #print("Duration of generate_analysis() :", str(time()-start))
        self.generate_analysis_linda()
        self.is_analysis_done = True


    def generate_analysis_linda(self):
        threshold_on=self.params["Onsets threshold"]
        threshold_off=self.params["Offsets threshold"]
        self.fenetre_retard=2000
        
        onset_times,offset_times=Calcul_onsets_offsets(self.amplitude_envelope,self.sr, threshold_on,threshold_off,self.params["min_note_duration"],self.fenetre_retard)

        if len(onset_times)==len(offset_times):
            for on,off in zip (onset_times,offset_times):
                if on not in (self.onsets) and off not in (self.offsets):
                    self.onsets.append(on)
                    self.offsets.append(off)


    def generate_zoom_analysis(self):
        self.zoom_button_bool=True
        x0,x1=int(self.xlim[0]*self.sr),int(self.xlim[1]*self.sr)
        
        if x0 < x1:
            threshold_on = np.max(self.amplitude_envelope[x0:x1])*0.2
            threshold_off = threshold_on-threshold_on*0.7
            self.params["Onsets threshold"]=threshold_on
            self.params["Offsets threshold"]=threshold_off
            onset_times, offset_times = Calcul_onsets_offsets(self.amplitude_envelope, self.sr, threshold_on, threshold_off, self.params["min_note_duration"],self.fenetre_retard)

            # Filter the onset_times and offset_times within the xlim range
            onset_times= [time for time in onset_times if self.xlim[0]-self.params["min_note_duration"] <= time <= self.xlim[1]]
            offset_times = [time for time in offset_times if self.xlim[0]<= time <= self.xlim[1]+self.params["min_note_duration"]]

            if len(onset_times)==len(offset_times):
                for on,off in zip (onset_times,offset_times):
                    if on not in (self.onsets) and off not in (self.offsets):
                        self.onsets.append(on)
                        self.offsets.append(off)
            else: 
                onset_times,offset_times=Clean_note(onset_times,offset_times)
                for on,off in zip (onset_times,offset_times):
                    if on not in (self.onsets) and off not in (self.offsets):
                        self.onsets.append(on)
                        self.offsets.append(off)

            self.Affichage()
            self.fig.canvas.draw()

    #------Plots------#
    def Affichage(self):
        if self.onsets_lines is not None:
            self.onsets_lines.remove()
        if self.offsets_lines is not None:
            self.offsets_lines.remove()
        if self.threshold_on_lines is not None:
            self.threshold_on_lines.remove()
        if self.threshold_off_lines is not None:
            self.threshold_off_lines.remove()
        
        self.onsets_lines = self.ax.vlines(self.onsets, 0, 1, color='g', label="onsets")
        self.offsets_lines=self.ax.vlines(self.offsets, 0, 1, color='r',label="offsets")
        self.threshold_on_lines=self.ax.axhline(y=self.params["Onsets threshold"], color='y', linestyle='--', label='threshold_on',linewidth=0.5)
        self.threshold_off_lines=self.ax.axhline(y=self.params["Offsets threshold"], color='grey', linestyle='--', label='threshold_off',linewidth=0.5)   
        

       
    

    def get_pitch_detection_fig(self):
        self.figures_visible=True
        self.fig, self.ax = subplots()
        self.fig.set(tight_layout=True)

        x = np.linspace(0, len(self.amplitude_envelope)/self.sr, len(self.amplitude_envelope))
        self.ax.plot(x, self.amplitude_envelope, 'b', linewidth=0.8)

        self.Affichage()
        
        self.fig.canvas.mpl_connect('button_release_event', self.Zoom)

    
    def add_time_series_figure(self):
        print("add_time_series_figure")
        start = time()
        if not self.is_analysis_done:
            self.generate_analysis()
        self.y_normalized=normalize_audio(self.audio)
        fig = get_time_series_fig(y=self.y_normalized, samp_rate=self.sr)
        fig.set(figwidth=self.fig_size[0], figheight=self.fig_size[1]) # 10 = 1000px
        self.time_series_figure_widget = FigureWidget(parent=self, figure=fig)
        # self.figure = self.time_series_figure_widget
        self.main_box.addWidget(self.time_series_figure_widget, 0)
        
        #print("Duration of add_time_series_figure() :", str(time()-start))
        self.adjustSize()
        self.update()
        self.parent().adjustSize()
        self.parent().update()
    
    def add_played_string_detection_figure(self):
        start = time()
        if not self.is_analysis_done:
            self.generate_analysis()
        self.get_pitch_detection_fig()
        self.fig.set(figwidth=self.fig_size[0], figheight=self.fig_size[1]) # 10 = 1000px
        self.played_string_detection_figure_widget = FigureWidget(parent=self, figure=self.fig)
        # if self.played_string_detection_figure_widget.parent() is not self.figure_box:
        # self.figure = self.played_string_detection_figure_widget
        self.main_box.addWidget(self.played_string_detection_figure_widget, 0)
        #print("Duration of add_played_string_detection_figure() :", str(time()-start))
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

    def get_figure_size(self):
        # retrieve size of scroll_area widget
        app_width, app_height = self.app_size
        # app_width = 1579
        # app_height = 918
        duration = self.params["duration_for_analysis"]
        if duration < 20:
            resize=3
        if duration>20:
            resize=1
        fig_width = app_width / 30 * duration*resize/ 100 # Default width is 1 full width = 30 secs
        fig_height = app_height * 0.4 / 100 # Default height is 1/3 of app height. / 100 to convert to matplotlib's size
        fig_width = max(fig_width, app_width / 2 / 100) # half of window’s width as min
        fig_width = min(fig_width, 40) # 3400px max
       
        return [fig_width, fig_height] 


   #------Midi-----#
    def add_notes_to_midi_instrument(self):
        if not self.is_analysis_done:
            self.generate_analysis()
        try :

            if self.params["midi_note"] != None:
                print("on",self.onsets)
                print("off",self.offsets)
                for start, end in zip(self.onsets, self.offsets):
                    start_ind = start * self.sr
                    end_ind = end * self.sr
                    if (end_ind - start_ind)> self.params["min_note_duration"]:
                        print("end_ind - start_ind :",(end_ind - start_ind))
                        # Create a Note instance for each note
                        note = pretty_midi.Note(
                            velocity=100,
                            pitch=round(self.params["midi_note"]),
                            start=start_ind / self.sr,
                            end=end_ind / self.sr
                        )
                        self.instru.notes.append(note)
                print("1 :" , self.instru.notes)
                        
                end_audio=len(self.amplitude_envelope)/self.sr
                
                if len(self.offsets)!=0:
                    print("aaaoo")
                    ecart=end_audio-self.offsets[-1]
                    note = pretty_midi.Note(
                        velocity=0,
                        pitch=0,
                        start=self.offsets[-1],
                        end=end_audio)

                    self.instru.notes.append(note)  
                    print("2 :" , self.instru.notes)
               
        except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred while adding notes: {e}")
    

    #------Params dialog-------#
    def call_ParamDialog(self):
        print("call_ParamDialog")
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
        self.is_analysis_done = False
        try :
            self.Redo_generate_analysis()
        except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred while the analysis try again: {e}")
        self.is_analysis_done = True
        self.params = new_params

    def Redo_generate_analysis(self):
        self.onsets=[]
        self.offsets=[]
        threshold_on=self.params["Onsets threshold"]
        threshold_off=self.params["Offsets threshold"]
        self.fenetre_retard=2000
        
        onset_times,offset_times=Calcul_onsets_offsets(self.amplitude_envelope,self.sr, threshold_on,threshold_off,self.params["min_note_duration"],self.fenetre_retard)

        if len(onset_times)==len(offset_times):
            for on,off in zip (onset_times,offset_times):
                    self.onsets.append(on)
                    self.offsets.append(off)

        self.Affichage()
        self.fig.canvas.draw()

  
    #---------Add Menu------#
    def play_audio(self):
        # sr, y = wavfile.read(self.file_path)
        y, sr = librosa.load(self.file_path, sr=None)
        sd.play(y, sr)

    def Add_Note(self, event):
        if not self.finish and self.Add_note_edit:
            if self.xdata is not None and not self.onset_edit and not self.offset_edit:
                if self.add_note_initial is None:
                    self.onset_note = self.xdata
                    self.add_note_initial = 1
                else:
                    self.add_note_initial = None
                    offset_note = self.xdata
                    self.onsets.append(self.onset_note)
                    self.offsets.append(offset_note)

                    
                    if self.onsets_lines is not None:
                        self.onsets_lines.remove()
                    if self.offsets_lines is not None:
                        self.offsets_lines.remove()

                    self.onsets_lines = self.ax.vlines(self.onsets, 0, 1, color='g', label="onsets")
                    self.offsets_lines = self.ax.vlines(self.offsets, 0, 1, color='r', label="offsets")
                    self.ax.autoscale(enable=True, axis='x', tight=True)
                    self.fig.canvas.draw()

   #---------Curseur---------#
    def Add_Note_Cursor(self):
        self.Add_note_edit=True
        self.header.Finish_btn.setVisible(True)
        
        if self.cursor_add_note==None:
         self.cursor_add_note = Cursor(self.ax,horizOn=False,vertOn=True,color='black',label="cursor add note",linewidth=2.0)
        self.fig.canvas.mpl_connect('button_release_event',self.Add_Note)
        
    def Edit_Onsets_Cursor(self):
        self.onset_edit=True
        self.header.Finish_btn.setVisible(True)
        if self.cursor_onset==None:
         self.cursor_onset = Cursor(self.ax,horizOn=False,vertOn=True,color='grey',label="cursor offsets",linewidth=2.0)
        self.fig.canvas.mpl_connect('button_release_event',self.Edit_Onsets)
    
    def Edit_Offsets_Cursor(self):
        self.offset_edit=True
        self.header.Finish_btn.setVisible(True)
        if self.cursor_offset==None:
         self.cursor_offset = Cursor(self.ax,horizOn=False,vertOn=True,color='orange',label="cursor offsets",linewidth=2.0)
        self.fig.canvas.mpl_connect('button_release_event',self.Edit_Offsets)
    
    #---------Edit Menu--------#
    def Edit_Onsets(self,event):
       if not self.finish and self.onset_edit:
        if len(self.onsets)!=0 and self.xdata is not None and not self.offset_edit and not self.Add_note_edit:
            onsets = np.asarray(self.onsets)
            idx = (np.abs(onsets - self.xdata)).argmin()
            if self.onset_initial is None:
                print("aaa",self.onsets[idx])
                self.onset_initial=self.onsets[idx]
            else : 
                self.onset_initial=None
                onset_final=self.xdata
                self.onsets[idx]=onset_final
                
                if self.onsets_lines is not None:
                    self.onsets_lines.remove()

                self.onsets_lines = self.ax.vlines(self.onsets, 0, 1, color='g', label="onsets")
                self.ax.autoscale(enable=True, axis='x', tight=True)
                self.fig.canvas.draw()


    def Edit_Offsets(self,event):
       
       if not self.finish and self.offset_edit:
        if len(self.offsets)!=0 and self.xdata is not None and not self.onset_edit and not self.Add_note_edit:
            offsets = np.asarray(self.offsets)
            idx = (np.abs(offsets - self.xdata)).argmin()
            if self.offset_initial is None:
                print("ooo",self.offsets[idx])
                self.offset_initial=self.offsets[idx]
            else : 
                self.offset_initial=None
                offset_final=self.xdata
                self.offsets[idx]=offset_final
                
                if self.offsets_lines is not None:
                    self.offsets_lines.remove()

                self.offsets_lines = self.ax.vlines(self.offsets, 0, 1, color='r', label="offsets")
                self.ax.autoscale(enable=True, axis='x', tight=True)
                self.fig.canvas.draw()

    def Delete_note(self):
        if self.xlim is not None:
            if len(self.onsets)!=0 and len(self.onsets)==len(self.offsets):
                for i, (on,off) in enumerate(zip(self.onsets,self.offsets)):
                    if self.xlim[0] <= on <= self.xlim[1] and self.xlim[0] <= off <= self.xlim[1]:
                        self.onsets.remove(self.onsets[i])
                        self.offsets.remove(self.offsets[i])

            if len(self.offsets)>len(self.onsets):
                for i, off in enumerate(self.offsets):
                    if self.xlim[0] <= off <= self.xlim[1] and self.xlim[0] <= off <= self.xlim[1]:
                        self.onsets.remove(self.offsets[i])

            if len(self.onsets)>len(self.offsets):
                for i, on in enumerate(self.onsets):
                    if self.xlim[0] <= on <= self.xlim[1] and self.xlim[0] <= on <= self.xlim[1]:
                        self.onsets.remove(self.onsets[i])

            self.Affichage()
            self.fig.canvas.draw()


    #-------Remove, Reset, Finish et Cancel--------#
    def Cancel(self):
        self.Cancel_button_bool=False
        self.cursor_onset=None
        self.cursor_offset=None
        self.cursor_add_note=None
        self.finish=False
        self.onset_edit=False
        self.offset_edit=False
        self.Add_note_edit=False

    def Cancel1(self):
        self.Cancel_button_bool=True
        self.header.Edit_onsets_btn.setVisible(False)
        self.header.Edit_offsets_btn.setVisible(False)
        self.header.Finish_btn.setVisible(False)
        self.header.Cancel_btn.setVisible(False)
        self.Cancel()

    def Cancel2(self):
        self.Cancel_button_bool=True
        self.header.Finish_btn.setVisible(False)
        self.header.Cancel_btn2.setVisible(False)
        self.header.Add_note_btn.setVisible(False)
        self.Cancel()

    def Cancel3(self):
        self.Cancel_button_bool=True
        self.header.Cancel_btn3.setVisible(False)
        self.header.Delete_note_btn.setVisible(False)
        self.Cancel()

    def Cancel4(self):
        self.Cancel_button_bool=True
        self.header.zoom_btn.setVisible(False)
        self.header.Cancel_btn4.setVisible(False)
        self.zoom_button_bool=None
        self.Cancel()
    

    def Done_fonction(self):
        if self.onset_edit==True:
            self.cursor_onset.disconnect_events()
            self.cursor_onset=None
            self.fig.canvas.mpl_disconnect(self.Edit_Onsets)
            self.onset_edit=False
            self.finish=False
            self.Affichage()
            return
        
        if self.offset_edit==True:
            self.cursor_offset.disconnect_events()
            self.cursor_offset=None
            self.fig.canvas.mpl_disconnect(self.Edit_Offsets)
            self.offset_edit=False
            self.finish=False
            self.Affichage()
            return 
    
        if self.Add_note_edit==True:
            self.cursor_add_note.disconnect_events()
            self.cursor_add_note=None
            self.fig.canvas.mpl_disconnect(self.Add_Note)
            self.Add_note_edit=False
            self.finish=False
            self.Affichage()
            return 
        
    def Finish(self):
        self.finish = False
        self.Done_fonction()
        self.header.Finish_btn.setVisible(False)
    
    def Reset_plot(self):
       
        try : 
            self.Reset_button_bool=True
            # Supprimer les lignes du plot
            if len(self.onsets)==0 and len(self.offsets)==0 :
                pass
            else :
                if self.onsets_lines is not None:
                        self.onsets_lines.remove()
                if self.offsets_lines is not None:
                        self.offsets_lines.remove()
            # Supprimer la légende
            if self.ax.legend() is not None:
                self.ax.legend().remove()
            self.onsets=[]
            self.offsets=[]
            # Redessiner le plot sans les lignes supprimées
            self.fig.canvas.draw()
            
            self.onsets_lines=None
            self.offsets_lines=None
            self.is_analysis_done=False
        except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred while resetting the figure: {e}")
    

    def remove_self(self):
        self.parent().remove_FileAnalysis(fileAnalysis_id=id(self))
    
    def remove_FigureWidget(self, figure_id: int):
        for child in self.children():
            if id(child)==figure_id:
                self.main_box.removeWidget(child)
                child.deleteLater()
                break
        self.adjustSize()
        self.update()
        self.parent().adjustSize()
        self.parent().update()

    #----------Sauvegarde-------#
    def get_data_to_save(self):
        if self.audio_load:
           
            data = {
                "file_path": self.file_path,
                "onsets": self.onsets,
                "offsets": self.offsets,
                "amplitude_envelope": self.amplitude_envelope.tolist(), 
                "parameters": self.params,
                #"midi_data":self.instru.notes,
                "figures_visible": self.figures_visible,
                "analysis_is_done": self.is_analysis_done,
                "audio_load":self.audio_load,
              
            }
            return data
        
    #----------Open File--------#
    def load_data_from_project(self,parent, aw_data):
        
        # Load the data from the project 
        self.onsets = aw_data.get("onsets", [])
        self.offsets = aw_data.get("offsets", [])
        self.file_path=aw_data.get("file_path",None)
        self.audio,self.sr = librosa.load(self.file_path, sr=None)
        # self.sr, self.audio = wavfile.read(self.file_path)
        self.amplitude_envelope = np.array(aw_data.get("amplitude_envelope",0))
        print('len ampli env',len(self.amplitude_envelope))
        print('type: ',type(self.amplitude_envelope))
        self.params = aw_data.get("parameters", {})
        self.figures_visible = aw_data.get("figures_visible",False)
        self.is_analysis_done=aw_data.get("analysis_is_done",False)
        self.audio_load=aw_data.get("audio_load",False)
        











    
       
                