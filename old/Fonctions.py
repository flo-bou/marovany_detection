import numpy as np
# import librosa.display
import librosa
import scipy.signal as sig
import librosa
# from scipy.io import wavfile
import matplotlib.pyplot as plt
# from IPython.display import display, Audio
from scipy.signal import hilbert
from scipy.ndimage import median_filter
import torch
import torchyin


#Fonction pour calculer l'enveloppe du signal creer par M. Boutonnet
def get_amplitude_envelope(y: np.ndarray, filter_timescale=160):
    """ Extract signal envelop, median filter it and normalize by max

    Args:
        y (_type_): _description_

    Returns:
        np.ndarray: amplitude_envelope
    """
    analytic_signal = hilbert(y)
    amplitude_envelope = np.abs(analytic_signal)
    amplitude_envelope = median_filter(amplitude_envelope, filter_timescale)
    amplitude_envelope = amplitude_envelope / max(amplitude_envelope)
    return np.array(amplitude_envelope)

def get_time_series_fig(y: np.ndarray, samp_rate):
    print("get_time_series_fig")
    # plt.rcParams['figure.figsize'] = fig_size
    fig, ax = plt.subplots()
    # fig.set(figwidth=fig_size[0], figheight=fig_size[1])
    fig.set(tight_layout=True)
    x = np.linspace(0, len(y)/samp_rate, len(y))
    ax.plot(x, y)
    ax.autoscale(enable=True, axis='x', tight=True)
    return fig

def Sup_retard(onset_times, signal, fs, fenetre, seuil_amplitude):
    new_onset_times = []
    cpt=0
    for i, onset_time in enumerate(onset_times):
        i=i-cpt
        echantillon_actuel = int(onset_time * fs)
        echantillon_max = np.argmax(signal[max(0, echantillon_actuel - fenetre):echantillon_actuel])
       
        if np.any(signal[echantillon_max:echantillon_actuel])< seuil_amplitude:
          while np.any(signal[echantillon_max:echantillon_actuel])< seuil_amplitude:
            fenetre-=200
            echantillon_max = np.argmax(signal[max(0, echantillon_actuel - fenetre):echantillon_actuel])

        temps_attaque = (echantillon_actuel - fenetre + echantillon_max) / fs
   
        if  signal[echantillon_actuel - fenetre + echantillon_max] >= seuil_amplitude :
            new_onset_times.append(temps_attaque)
        else:
            new_onset_times.append(onset_time)

    return new_onset_times

def filtre(amplitude_envelope,fs,onsets,min_note_duration,threshold):

  new_onsets=[]

  for on in (onsets):

    index = int(on * fs)
    min_time = int((on + 0.08) * fs)
    if min_time>len(amplitude_envelope):
       min_time=len(amplitude_envelope)-5
    min_time_ampli=amplitude_envelope[min_time]

    if index >= len(amplitude_envelope):
      index=len(amplitude_envelope)-1

    amplitude = amplitude_envelope[index]
    if amplitude> threshold:
      new_onsets.append(on)

    if amplitude> threshold and min_time_ampli>threshold*0.3:
        new_onsets.append(on)

  return new_onsets


def detect_offsets(onset_times, min_note_duration, audio_signal, fs, offset_threshold):
    offset_times = []
    last_onset_index = 0

    for onset_time in onset_times:
        offset_sample = int((onset_time + min_note_duration) * fs)
        if offset_sample>len(audio_signal):
          offset_sample=len(audio_signal)
        else:
          offset_amplitude = audio_signal[offset_sample]

        if offset_amplitude <= offset_threshold+offset_threshold*0.3:
            offset_times.append(onset_time + min_note_duration)
        else:
           
            for i in range(offset_sample, len(audio_signal)):
                if i >= len(audio_signal) - 1 or audio_signal[i] < offset_threshold:
                    offset_times.append(i / fs)
                    break
                elif audio_signal[i] >= offset_threshold and audio_signal[i + 1] < offset_threshold:
                    offset_times.append(i / fs)
                    break

    return offset_times

def remove_duplicate_onsets(onset_times, offset_times):
    valid_onset_times = []
    seen_offsets = []
    if len(onset_times)>len(offset_times):
      tab=offset_times
    else:
      tab=onset_times
    for i in range(len(tab)):
        current_onset = onset_times[i]
        current_offset = offset_times[i]
        if i>0:
          if current_offset not in seen_offsets and current_onset>offset_times[i-1]:
              valid_onset_times.append(current_onset)
              seen_offsets.append(current_offset)
        else:
          if current_offset not in seen_offsets:
            valid_onset_times.append(current_onset)
            seen_offsets.append(current_offset)

    return valid_onset_times,seen_offsets


def get_pitch(y, fs,pitch_min=100,pitch_max=1000):
  π = np.pi

  #Estimation des pitch avec Yin
  p = torchyin.estimate(y, sample_rate=fs,pitch_min=pitch_min, pitch_max=pitch_max)

  #Générez une séquence de pitches pour couvrir toute la durée du signal
  f = np.repeat(p, -(-len(y) // len(p)))
  #Générez un signal sinusoïdal basé sur les pitches détectés
  y_p = np.sin(2 * π * (np.cumsum(f / fs) % 1.0))[:len(y)]

  # display(Audio(y_p,rate=fs)) # removed during ipython deletion

  freqs=p.numpy()#conversion de tenseur pytorch vers numpy

  t = np.linspace(0, len(y)/fs, len(y))
  plt.figure()
  plt.plot(t,y_p)
  plt.title("Instant des pitches")
  plt.show()

  return freqs


def get_frequency(note_name):
    # Dictionnaire contenant les correspondances note-fréquence
    """
    note_frequency = {
        'C-1': 16.35, 'C#-1': 17.32, 'Db-1': 17.32, 'D-1': 18.35, 'D#-1': 19.45, 'Eb-1': 19.45, 'E-1': 20.60,
        'F-1': 21.83, 'F#-1': 23.12, 'Gb-1': 23.12, 'G-1': 24.50, 'G#-1': 25.96, 'Ab-1': 25.96, 'A-1': 27.50,
        'A#-1': 29.14, 'Bb-1': 29.14, 'B-1': 30.87, 'C0': 32.70, 'C#0': 34.65, 'Db0': 34.65, 'D0': 36.71,
        'D#0': 38.89, 'Eb0': 38.89, 'E0': 41.20, 'F0': 43.65, 'F#0': 46.25, 'Gb0': 46.25, 'G0': 49.00,
        'G#0': 51.91, 'Ab0': 51.91, 'A0': 55.00, 'A#0': 58.27, 'Bb0': 58.27, 'B0': 61.74, 'C1': 65.41,
        'C#1': 69.30, 'Db1': 69.30, 'D1': 73.42, 'D#1': 77.78, 'Eb1': 77.78, 'E1': 82.41, 'F1': 87.31,
        'F#1': 92.50, 'Gb1': 92.50, 'G1': 98.00, 'G#1': 103.83, 'Ab1': 103.83, 'A1': 110.00, 'A#1': 116.54,
        'Bb1': 116.54, 'B1': 123.47, 'C2': 130.81, 'C#2': 138.59, 'Db2': 138.59, 'D2': 146.83, 'D#2': 155.56,
        'Eb2': 155.56, 'E2': 164.81, 'F2': 174.61, 'F#2': 185.00, 'Gb2': 185.00, 'G2': 196.00, 'G#2': 207.65,
        'Ab2': 207.65, 'A2': 220.00, 'A#2': 233.08, 'Bb2': 233.08, 'B2': 246.94, 'C3': 261.63, 'C#3': 277.18,
        'Db3': 277.18, 'D3': 293.66, 'D#3': 311.13, 'Eb3': 311.13, 'E3': 329.63, 'F3': 349.23, 'F#3': 369.99,
        'Gb3': 369.99, 'G3': 392.00, 'G#3': 415.30, 'Ab3': 415.30, 'A3': 440.00, 'A#3': 466.16, 'Bb3': 466.16,
        'B3': 493.88, 'C4': 523.25, 'C#4': 554.37, 'Db4': 554.37, 'D4': 587.33, 'D#4': 622.25, 'Eb4': 622.25,
        'E4': 659.25, 'F4': 698.46, 'F#4': 739.99, 'Gb4': 739.99, 'G4': 783.99, 'G#4': 830.61, 'Ab4': 830.61,
        'A4': 880.00, 'A#4': 932.33, 'Bb4': 932.33, 'B4': 987.77, 'C5': 1046.50, 'C#5': 1108.73, 'Db5': 1108.73,
        'D5': 1174.66, 'D#5': 1244.51, 'Eb5': 1244.51, 'E5': 1318.51, 'F5': 1396.91, 'F#5': 1479.98, 'Gb5': 1479.98,
        'G5': 1567.98, 'G#5': 1661.22, 'Ab5': 1661.22, 'A5': 1760.00, 'A#5': 1864.66, 'Bb5': 1864.66, 'B5': 1975.53,
        'C6': 2093.00, 'C#6': 2217.46, 'Db6': 2217.46, 'D6': 2349.32, 'D#6': 2489.02, 'Eb6': 2489.02, 'E6': 2637.02,
        'F6': 2793.83, 'F#6': 2959.96, 'Gb6': 2959.96, 'G6': 3135.96, 'G#6': 3322.44, 'Ab6': 3322.44, 'A6': 3520.00,
        'A#6': 3729.31, 'Bb6': 3729.31, 'B6': 3951.07, 'C7': 4186.01
    }"""

    note_frequency = {
    'C-1': 8.18, 'C#-1': 8.66, 'Db-1': 8.66, 'D-1': 9.18, 'D#-1': 9.72, 'Eb-1': 9.72, 'E-1': 10.30,
    'F-1': 10.91, 'F#-1': 11.56, 'Gb-1': 11.56, 'G-1': 12.25, 'G#-1': 12.98, 'Ab-1': 12.98, 'A-1': 13.75,
    'A#-1': 14.57, 'Bb-1': 14.57, 'B-1': 15.43, 'C0': 16.35, 'C#0': 17.32, 'Db0': 17.32, 'D0': 18.35,
    'D#0': 19.45, 'Eb0': 19.45, 'E0': 20.60, 'F0': 21.83, 'F#0': 23.12, 'Gb0': 23.12, 'G0': 24.50,
    'G#0': 25.96, 'Ab0': 25.96, 'A0': 27.50, 'A#0': 29.14, 'Bb0': 29.14, 'B0': 30.87, 'C1': 32.70,
    'C#1': 34.65, 'Db1': 34.65, 'D1': 36.71, 'D#1': 38.89, 'Eb1': 38.89, 'E1': 41.20, 'F1': 43.65,
    'F#1': 46.25, 'Gb1': 46.25, 'G1': 49.00, 'G#1': 51.91, 'Ab1': 51.91, 'A1': 55.00, 'A#1': 58.27,
    'Bb1': 58.27, 'B1': 61.74, 'C2': 65.41, 'C#2': 69.30, 'Db2': 69.30, 'D2': 73.42, 'D#2': 77.78,
    'Eb2': 77.78, 'E2': 82.41, 'F2': 87.31, 'F#2': 92.50, 'Gb2': 92.50, 'G2': 98.00, 'G#2': 103.83,
    'Ab2': 103.83, 'A2': 110.00, 'A#2': 116.54, 'Bb2': 116.54, 'B2': 123.47, 'C3': 130.81, 'C#3': 138.59,
    'Db3': 138.59, 'D3': 146.83, 'D#3': 155.56, 'Eb3': 155.56, 'E3': 164.81, 'F3': 174.61, 'F#3': 185.00,
    'Gb3': 185.00, 'G3': 196.00, 'G#3': 207.65, 'Ab3': 207.65, 'A3': 220.00, 'A#3': 233.08, 'Bb3': 233.08,
    'B3': 246.94, 'C4': 261.63, 'C#4': 277.18, 'Db4': 277.18, 'D4': 293.66, 'D#4': 311.13, 'Eb4': 311.13,
    'E4': 329.63, 'F4': 349.23, 'F#4': 369.99, 'Gb4': 369.99, 'G4': 392.00, 'G#4': 415.30, 'Ab4': 415.30,
    'A4': 440.00, 'A#4': 466.16, 'Bb4': 466.16, 'B4': 493.88, 'C5': 523.25, 'C#5': 554.37, 'Db5': 554.37,
    'D5': 587.33, 'D#5': 622.25, 'Eb5': 622.25, 'E5': 659.25, 'F5': 698.46, 'F#5': 739.99, 'Gb5': 739.99,
    'G5': 783.99, 'G#5': 830.61, 'Ab5': 830.61, 'A5': 880.00, 'A#5': 932.33, 'Bb5': 932.33, 'B5': 987.77,
    'C6': 1046.50, 'C#6': 1108.73, 'Db6': 1108.73, 'D6': 1174.66, 'D#6': 1244.51, 'Eb6': 1244.51, 'E6': 1318.51,
    'F6': 1396.91, 'F#6': 1479.98, 'Gb6': 1479.98, 'G6': 1567.98, 'G#6': 1661.22, 'Ab6': 1661.22, 'A6': 1760.00,
    'A#6': 1864.66, 'Bb6': 1864.66, 'B6': 1975.53, 'C7': 2093.00
    }

    # Vérification si la note existe dans le dictionnaire
    if note_name in note_frequency:
        return note_frequency[note_name]
    else:
        return None

def Create_Note_list():
    frequency_note = {
      8.18: 'C-1', 8.66: 'C#-1', 9.18: 'D-1', 9.72: 'D#-1', 10.3: 'E-1', 10.91: 'F-1', 11.56: 'F#-1',
      12.25: 'G-1', 12.98: 'G#-1', 13.75: 'A-1', 14.57: 'A#-1', 15.43: 'B-1', 16.35: 'C0', 17.32: 'C#0',
      18.35: 'D0', 19.45: 'D#0', 20.6: 'E0', 21.83: 'F0', 23.12: 'F#0', 24.5: 'G0', 25.96: 'G#0',
      27.5: 'A0', 29.14: 'A#0', 30.87: 'B0', 32.7: 'C1', 34.65: 'C#1', 36.71: 'D1', 38.89: 'D#1',
      41.2: 'E1', 43.65: 'F1', 46.25: 'F#1', 49.0: 'G1', 51.91: 'G#1', 55.0: 'A1', 58.27: 'A#1',
      61.74: 'B1', 65.41: 'C2', 69.3: 'C#2', 73.42: 'D2', 77.78: 'D#2', 82.41: 'E2', 87.31: 'F2',
      92.5: 'F#2', 98.0: 'G2', 103.83: 'G#2', 110.0: 'A2', 116.54: 'A#2', 123.47: 'B2', 130.81: 'C3',
      138.59: 'C#3', 146.83: 'D3', 155.56: 'D#3', 164.81: 'E3', 174.61: 'F3', 185.0: 'F#3', 196.0: 'G3',
      207.65: 'G#3', 220.0: 'A3', 233.08: 'A#3', 246.94: 'B3', 261.63: 'C4', 277.18: 'C#4', 293.66: 'D4',
      311.13: 'D#4', 329.63: 'E4', 349.23: 'F4', 369.99: 'F#4', 392.0: 'G4', 415.3: 'G#4', 440.0: 'A4',
      466.16: 'A#4', 493.88: 'B4', 523.25: 'C5', 554.37: 'C#5', 587.33: 'D5', 622.25: 'D#5', 659.25: 'E5',
      698.46: 'F5', 739.99: 'F#5', 783.99: 'G5', 830.61: 'G#5', 880.0: 'A5', 932.33: 'A#5', 987.77: 'B5',
      1046.5: 'C6', 1108.73: 'C#6', 1174.66: 'D6', 1244.51: 'D#6', 1318.51: 'E6', 1396.91: 'F6',
      1479.98: 'F#6', 1567.98: 'G6', 1661.22: 'G#6', 1760.0: 'A6', 1864.66: 'A#6', 1975.53: 'B6',
      2093.0: 'C7'
  }
  
    liste_notes = [valeur for valeur in frequency_note.values()]
    return liste_notes

def get_Note(frequency):
  """
  frequency_note = {
      16.35: 'C-1', 17.32: 'C#-1', 18.35: 'D-1', 19.45: 'D#-1', 20.6: 'E-1', 21.83: 'F-1', 23.12: 'F#-1', 24.5: 'G-1',
      25.96: 'G#-1', 27.5: 'A-1', 29.14: 'A#-1', 30.87: 'B-1', 32.7: 'C0', 34.65: 'C#0', 36.71: 'D0', 38.89: 'D#0',
      41.2: 'E0', 43.65: 'F0', 46.25: 'F#0', 49.0: 'G0', 51.91: 'G#0', 55.0: 'A0', 58.27: 'A#0', 61.74: 'B0', 65.41: 'C1',
      69.3: 'C#1', 73.42: 'D1', 77.78: 'D#1', 82.41: 'E1', 87.31: 'F1', 92.5: 'F#1', 98.0: 'G1', 103.83: 'G#1', 110.0: 'A1',
      116.54: 'A#1', 123.47: 'B1', 130.81: 'C2', 138.59: 'C#2', 146.83: 'D2', 155.56: 'D#2', 164.81: 'E2', 174.61: 'F2',
      185.0: 'F#2', 196.0: 'G2', 207.65: 'G#2', 220.0: 'A2', 233.08: 'A#2', 246.94: 'B2', 261.63: 'C3', 277.18: 'C#3',
      293.66: 'D3', 311.13: 'D#3', 329.63: 'E3', 349.23: 'F3', 369.99: 'F#3', 392.0: 'G3', 415.3: 'G#3', 440.0: 'A3',
      466.16: 'A#3', 493.88: 'B3', 523.25: 'C4', 554.37: 'C#4', 587.33: 'D4', 622.25: 'D#4', 659.25: 'E4', 698.46: 'F4',
      739.99: 'F#4', 783.99: 'G4', 830.61: 'G#4', 880.0: 'A4', 932.33: 'A#4', 987.77: 'B4', 1046.5: 'C5', 1108.73: 'C#5',
      1174.66: 'D5', 1244.51: 'D#5', 1318.51: 'E5', 1396.91: 'F5', 1479.98: 'F#5', 1567.98: 'G5', 1661.22: 'G#5',
      1760.0: 'A5', 1864.66: 'A#5', 1975.53: 'B5', 2093.0: 'C6', 2217.46: 'C#6', 2349.32: 'D6', 2489.02: 'D#6',
      2637.02: 'E6', 2793.83: 'F6', 2959.96: 'F#6', 3135.96: 'G6', 3322.44: 'G#6', 3520.0: 'A6', 3729.31: 'A#6',
      3951.07: 'B6', 4186.01: 'C7'
       }"""
  frequency_note = {
      8.18: 'C-1', 8.66: 'C#-1', 9.18: 'D-1', 9.72: 'D#-1', 10.3: 'E-1', 10.91: 'F-1', 11.56: 'F#-1',
      12.25: 'G-1', 12.98: 'G#-1', 13.75: 'A-1', 14.57: 'A#-1', 15.43: 'B-1', 16.35: 'C0', 17.32: 'C#0',
      18.35: 'D0', 19.45: 'D#0', 20.6: 'E0', 21.83: 'F0', 23.12: 'F#0', 24.5: 'G0', 25.96: 'G#0',
      27.5: 'A0', 29.14: 'A#0', 30.87: 'B0', 32.7: 'C1', 34.65: 'C#1', 36.71: 'D1', 38.89: 'D#1',
      41.2: 'E1', 43.65: 'F1', 46.25: 'F#1', 49.0: 'G1', 51.91: 'G#1', 55.0: 'A1', 58.27: 'A#1',
      61.74: 'B1', 65.41: 'C2', 69.3: 'C#2', 73.42: 'D2', 77.78: 'D#2', 82.41: 'E2', 87.31: 'F2',
      92.5: 'F#2', 98.0: 'G2', 103.83: 'G#2', 110.0: 'A2', 116.54: 'A#2', 123.47: 'B2', 130.81: 'C3',
      138.59: 'C#3', 146.83: 'D3', 155.56: 'D#3', 164.81: 'E3', 174.61: 'F3', 185.0: 'F#3', 196.0: 'G3',
      207.65: 'G#3', 220.0: 'A3', 233.08: 'A#3', 246.94: 'B3', 261.63: 'C4', 277.18: 'C#4', 293.66: 'D4',
      311.13: 'D#4', 329.63: 'E4', 349.23: 'F4', 369.99: 'F#4', 392.0: 'G4', 415.3: 'G#4', 440.0: 'A4',
      466.16: 'A#4', 493.88: 'B4', 523.25: 'C5', 554.37: 'C#5', 587.33: 'D5', 622.25: 'D#5', 659.25: 'E5',
      698.46: 'F5', 739.99: 'F#5', 783.99: 'G5', 830.61: 'G#5', 880.0: 'A5', 932.33: 'A#5', 987.77: 'B5',
      1046.5: 'C6', 1108.73: 'C#6', 1174.66: 'D6', 1244.51: 'D#6', 1318.51: 'E6', 1396.91: 'F6',
      1479.98: 'F#6', 1567.98: 'G6', 1661.22: 'G#6', 1760.0: 'A6', 1864.66: 'A#6', 1975.53: 'B6',
      2093.0: 'C7'
  }


  min_note=[]
  # Parcours du dictionnaire frequency_note
  for f in frequency:
    min=8
    for freq, note in frequency_note.items():
        diff=abs(f - freq)
        if diff <= min:
          min=diff
          min_note.append(note)
  if len(min_note)!=0:
    return min_note

  return None  # Aucune correspondance trouvée


def most_frequent_note(notes):
    compteur = {}

    # Compter les occurrences de chaque note dans le tableau
    for note in notes:
        if note in compteur:
            compteur[note] += 1
        else:
            compteur[note] = 1

    # Trouver la note la plus fréquente
    note_plus_frequente = max(compteur, key=compteur.get)

    return note_plus_frequente


def get_equivalence_table(file_path, equivalence_table):

    if file_path[0]=='0':
      num_corde=int(file_path[1])
    else :
      num_corde=int(file_path[:2])

    y, fs = librosa.load(file_path, sr=None)
    # fs, y = wavfile.read(file_path)

    pitchs=get_pitch(y, fs)
    print(pitchs)
    notes= get_Note(pitchs)
    if notes!=None:
      note = most_frequent_note(notes)

      equivalence_table[num_corde]=note

    return equivalence_table



def Is_corde_played(y,fs,num_corde,equivalence_table):

    note_played=False
    """
    if file_path[0]=='0':
      num_corde=int(file_path[1])
    else :
      num_corde=int(file_path[0:2])
    print(num_corde) y,fs = librosa.load(file_path)
    """


    pitchs=get_pitch(y, fs)

    notes= get_Note(pitchs)

    print("EQ",equivalence_table[num_corde])
    if notes!=None:
      note = most_frequent_note(notes)
      print("NOTE",note)
      if equivalence_table[num_corde]==note:
        note_played=True

      else :
          note_played=False
    else :
      note_played=False

    return note_played


def supprimer_notes_courtes(onsets, offsets, min_time_duration):
    indices_a_supprimer = []
    for i in range(len(onsets)):
        durée_note = offsets[i] - onsets[i]
        print(f"durée_note = {offsets[i]} - {onsets[i]}={durée_note}")
        if durée_note < min_time_duration:
            indices_a_supprimer.append(i)

    # Supprimer les notes dans l'ordre inverse pour éviter les décalages d'indices
    for indice in reversed(indices_a_supprimer):
        del onsets[indice]
        del offsets[indice]


def normalize_audio(audio):
    # Normalisation
    normalized_audio = audio / np.max(np.abs(audio))

    return normalized_audio

#fonction tfct adapté à itfct
def tfct1(signal,sample_rate, Nwin, Nhop, Nfft):
    
    #fenêtre hamming 
    window = sig.hamming(Nwin)
    #nombre de trams
    num_frames = int(np.ceil((len(signal) - Nwin) / Nhop)) + 1
    #0 padding
    pad_length = (num_frames - 1) * Nhop + Nwin - len(signal)
    signal = np.pad(signal, (0, int(pad_length)), mode='constant', constant_values=0)
    #initialise xmat
    xmat = np.zeros((Nfft, num_frames),dtype=np.complex_)
    for i in range(num_frames):
        start = i * Nhop
        end = start + Nwin
        frame = signal[int(start):int(end)]
        frame_hamm = window*frame
        xmat[:, i] = np.fft.fft(frame_hamm, Nfft)[:Nfft]#symétrie hemitienne 
#     freqs = np.fft.fftfreq(Nfft, 1/sample_rate)[Nfft//2+1:]# freq en Hz 
    freqs = np.arange(Nfft) * sample_rate / (Nfft)# freq en Hz 
    times = np.arange(num_frames) * Nhop / sample_rate #temps en seconds
    return xmat, freqs, times

def itfct(xmat, Nwin, Nhop,Fs):
    # Préallocation de mémoire pour le signal reconstruit y
    Nfft,ntrames = xmat.shape
    n = (ntrames - 1) * Nhop + Nwin
    y = np.zeros((n),dtype=np.complex_)
    
    #Etape 2 : reconstruire chaque trame fenêtrée
    for i in range(ntrames):
        yl = np.fft.ifft(xmat[:, i])
    #Etape 3 : décaler la lè trame yl, de (l − 1) trames
    #Etape 4 : sommer les trames décalées yl[n − (l − 1)Nhop]
        y[i*Nhop:i*Nhop+Nwin] = y[i*Nhop:i*Nhop+Nwin] + yl[:Nwin]
    
    # Normalisation de y, valeur de K
    K = np.sum(np.hamming(Nwin)/Nhop)
    y = y/K
    
    # Vecteur temporel pour l'affichage
    t = np.arange(0, n) / float(n-1)
    
    return y, t

def Denoise(audio,fs):
  Nwin = 2048
  xmat, freqs, times = tfct1(audio,fs, Nwin, Nwin//2,Nwin)
  num_frames_to_avg = 20
  frames_to_avg = np.zeros((num_frames_to_avg, Nwin))
  for i in range(num_frames_to_avg):
      frame_idx = i 
      frames_to_avg[i,:] = np.abs(xmat[:,i])

  mean_frame = np.mean(frames_to_avg, axis=0)
  xmat_clean = np.zeros((xmat.shape))
  num_frames = xmat.shape[1]

  for i in range(num_frames):
      xmat_clean[:, i] = np.abs(xmat[:, i]) - np.abs(mean_frame)#supprimer le module du bruit

  xmat_clean = np.maximum(xmat_clean,0)#valeurs négatives à 0
  xmat_clean_phase = xmat_clean*np.exp(1j*np.angle(xmat))
  y2, t = itfct(xmat_clean_phase, Nwin, Nwin//2,fs)

  return y2


def create_notes_array(onsets, offsets):
    notes = []
    for on,off in zip(onsets,offsets):
        note = [on, off]
        notes.append(note)
    return notes

def remove_duplicate_offsets(offset_times):
     # Utilisons un dictionnaire pour marquer les valeurs uniques
    occurences = {}
    for off in offset_times:
        occurences[off] = 1

    # Créons un nouveau tableau pour stocker les éléments uniques
    resultat = list(occurences.keys())

    return resultat

def Calcul_onsets(audio,fs, threshold_on,min_note_duration,fenetre_retard):
 
  onset_frames= librosa.onset.onset_detect(y=audio, sr=fs, units='time') 
  onsets=filtre(audio,fs,onset_frames,min_note_duration,threshold_on)
  onsets=Sup_retard(onsets, audio, fs, fenetre_retard, threshold_on)
  
  return onsets

def Calcul_offsets(audio,fs,onsets,threshold_on,threshold_off,min_note_duration):
 
  offsets=detect_offsets(onsets, min_note_duration, audio, fs, threshold_off)
  onsets,offsets=remove_duplicate_onsets(onsets, offsets)
  offsets=remove_duplicate_offsets(offsets)
  
  return offsets,onsets

def Calcul_onsets_offsets(audio,fs, threshold_on,threshold_off,min_note_duration,fenetre_retard):
    
    onset_frames= librosa.onset.onset_detect(y=audio, sr=fs, units='time')
    onsets=filtre(audio,fs,onset_frames,min_note_duration,threshold_on)
    onsets=Sup_retard(onsets, audio, fs, fenetre_retard, threshold_on)
    offsets=detect_offsets(onsets, min_note_duration, audio, fs, threshold_off)
    onsets,offsets=remove_duplicate_onsets(onsets, offsets)
    offsets=remove_duplicate_offsets(offsets)
   
    return onsets,offsets

def Clean_note(onsets,offsets):
  valid_onsets=[]
  valid_offsets=[]
  if len(onsets)>len(offsets):
    for i in range(len(offsets)):
      valid_onsets.append(onsets[i])
      valid_offsets.append(offsets[i])
  else :
      for i in range(len(onsets)):
        valid_onsets.append(onsets[i])
        valid_offsets.append(offsets[i])
  return valid_onsets,valid_offsets
