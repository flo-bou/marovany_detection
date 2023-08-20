import os

from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, 
                             QHBoxLayout, QLabel, QSizePolicy, 
                             QVBoxLayout, QSlider, QLCDNumber)
from PyQt6.QtCore import (Qt, QUrl, QTimer, 
                          QTime)
from PyQt6.QtGui import QIcon
from PyQt6.QtMultimedia import QMediaPlayer
import librosa
# from scipy.io import wavfile
import sounddevice as sd


class AudioPlayer(QWidget):
    def __init__(self,parent: QWidget,fname: str,file_path:str):
        super().__init__()
        self.file_path=file_path
        self.fname=fname
        """
        self.window_width, self.window_height = 800, 120
        self.setMinimumSize(self.window_width, self.window_height)
        """
        self.title_label = QLabel("Playing File : " + self.fname + " ;")
        self.title_label.adjustSize()

        
        

        play_btn = QPushButton('Play')
        play_btn.clicked.connect(self.playAudioFile)
        play_btn.adjustSize()

        pause_btn = QPushButton('Pause')
        pause_btn.clicked.connect(self.Pause_Audifile)
        pause_btn.adjustSize()

        stop_btn = QPushButton('Stop')
        stop_btn.clicked.connect(self.Stop_Audiofile)
        stop_btn.adjustSize()

        self.audio_box=QHBoxLayout()
        self.audio_box.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.audio_box.addWidget(self.title_label)

        self.audio_box.addWidget(play_btn)
        
        self.audio_box.addWidget(pause_btn)
        self.audio_box.addWidget(stop_btn)
        
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        self.setLayout(self.audio_box)
        self.adjustSize()


        self.time_elapsed = QLCDNumber()
        self.total_duration = QLCDNumber()

 

        self.player = QMediaPlayer()
        #self.player.durationChanged.connect(self.set_duration)
        #self.player.positionChanged.connect(self.update_position)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_duration)

        self.current_position = 0

    def Pause_Audifile(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.current_position = self.player.position()
            self.player.pause()

    def Stop_Audiofile(self):
        self.player.stop()
        self.slider.setValue(0)
        self.time_elapsed.display("00:00")

    def playAudioFile(self):
        if not self.player.isAvailable():
            full_file_path = os.path.join(os.getcwd(),self.file_path)
            y, sr = librosa.load(full_file_path, sr=None)
            # sr, y = wavfile.read(self.file_path)
            sd.play(y, sr)
            sd.wait()

        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
        else:
            self.player.setPosition(self.current_position)
            self.player.play()

    def set_duration(self, duration):
        self.slider.setRange(0, duration)
        self.slider.setSingleStep(1)  # Step de 1 milliseconde
        total_duration_msecs = duration
        total_mins = total_duration_msecs // 60000
        total_secs = (total_duration_msecs % 60000) // 1000
        self.total_duration.display(f"{total_mins:02}:{total_secs:02}")

    def set_position(self, position):
        self.current_position = position
        elapsed_mins = position // 60000
        elapsed_secs = (position % 60000) // 1000
        self.time_elapsed.display(f"{elapsed_mins:02}:{elapsed_secs:02}")

    def slider_pressed(self):
        # Jump to the position indicated by the slider when clicked
        position = self.slider.value()
        self.player.setPosition(position)

    def update_position(self, position):
        self.slider.setValue(position)

        elapsed_mins = position // 60000
        elapsed_secs = (position % 60000) // 1000
        self.time_elapsed.display(f"{elapsed_mins:02}:{elapsed_secs:02}")

    def update_duration(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            position = self.player.position()
            self.update_position(position)
        else:
            self.timer.stop()
"""
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget {
            font-size: 30px;
        }
    ''')
    
    myApp = MyApp()
    myApp.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')
"""

class FileAnalysis(QWidget):
    # ... (le reste de la classe FileAnalysis)

    def init_player_ui(self):
        # Éléments de l'interface pour le lecteur audio
        self.play_label = QLabel("Time: 0:00 / 0:00")
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.play_button = QPushButton("Play")
        self.stop_button = QPushButton("Stop")
        # ...

        # Connecter les boutons aux méthodes correspondantes
        self.play_button.clicked.connect(self.play_audio)
        self.stop_button.clicked.connect(self.stop_audio)
        # ...

        # Ajouter les éléments à l'interface graphique
        # ...

        # Initialiser un minuteur pour mettre à jour l'étiquette du temps écoulé
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_play_time)

        # Initialiser un QTime pour suivre le temps écoulé
        self.elapsed_time = QTime(0, 0, 0)

        # Déterminer la durée totale de l'audio
        self.total_duration = librosa.get_duration(self.y, self.sr)

    def play_audio(self):
        # Démarrer le minuteur pour mettre à jour l'étiquette du temps écoulé
        self.timer.start(100)  # Mettre à jour toutes les 100 millisecondes (ajuster selon vos besoins)

        # Lire l'audio avec sounddevice
        sd.play(self.y, self.sr)
        sd.wait()

        # Arrêter le minuteur une fois que la lecture est terminée
        self.timer.stop()

    def stop_audio(self):
        # Arrêter la lecture audio avec sounddevice
        sd.stop()

        # Arrêter le minuteur
        self.timer.stop()

        # Réinitialiser le temps écoulé
        self.elapsed_time = QTime(0, 0, 0)

    def update_play_time(self):
        # Mettre à jour l'étiquette du temps écoulé avec le temps actuel
        self.elapsed_time = self.elapsed_time.addMSecs(100)
        time_str = self.elapsed_time.toString("m:ss")  # Format: minutes:secondes
        self.play_label.setText(f"Time: {time_str} / {self.total_duration:.2f} s")

        # Mettre à jour la barre de progression en fonction du temps écoulé
        progress = (self.elapsed_time.msecs() / 1000) / self.total_duration * 100
        self.progress_bar.setValue(progress)

    # ... (le reste de la classe FileAnalysis)
