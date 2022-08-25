import glob
import os
import time

import numpy as np
from scipy.signal import hilbert
from scipy.ndimage import median_filter
import matplotlib.pyplot as plt
# import mpld3
# from mpld3 import plugins
import librosa
import librosa.display
import pretty_midi
import pypianoroll


def create_note_list():
    note_letters = ['E','D','B','G']
    note_numbers = range(10)
    note_commas = ['', '#']
    note_names = []
    for nl in note_letters:
        for nn in note_numbers:
            for nc in note_commas:
                note_names.append(nl + str(nn) + nc)
    return note_names

def get_note_guessed_from_fname(note_list: list, fname: str):
    """Extract MIDI note name based on wav filename. 
    Note name should be in the filename

    Args:
        note_list (list[str]): List of every possible notes as strings
        fname (str): name of wav file

    Returns:
        int or None: note number in midi format or None if note name was not in file name
    """
    midi_note = None
    for note_candidate in note_list:
        if note_candidate in fname:
            midi_note = pretty_midi.note_name_to_number(note_candidate)
            break
    return midi_note

def get_amplitude_envelope(y: np.ndarray, filter_timescale: int):
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
    return amplitude_envelope

def get_decal(amplitude_envelope: np.ndarray, threshold: float):
    """
    Args:
        amplitude_envelope (np.ndarray): _description_
        threshold (float): _description_
    Returns:
        np.ndarray: decal
    """
    new_binary = np.zeros(len(y))
    new_binary[amplitude_envelope > threshold] = 1
    decal = new_binary[1:] - new_binary[0:-1]
    return decal

def get_time_series_fig(fig_size: list, y: np.ndarray, samp_rate):
    # plt.rcParams['figure.figsize'] = fig_size
    fig, ax = plt.subplots()
    fig.set(figwidth=fig_size[0], figheight=fig_size[1],tight_layout=True)
    ax.plot(np.linspace(0, len(y)/samp_rate, len(y)), y)
    ax.autoscale(enable=True, axis='x', tight=True)
    return fig


def get_pitch_detection_fig(fig_size: list, ampl_envel: np.ndarray, threshold:float, min_duration: float, instru: pretty_midi.Instrument, decal: np.ndarray, midi_note: int):
    # plt.rcParams['figure.figsize'] = fig_size
    fig, ax = plt.subplots()
    fig.set(figwidth=fig_size[0], figheight=fig_size[1], tight_layout=True)
    x = np.linspace(0, len(ampl_envel)/sr, len(ampl_envel))
    ax.plot(x, ampl_envel, 'b', linewidth=0.8)
    ax.plot(x, np.linspace(threshold, threshold, len(ampl_envel)), 'k--',linewidth=0.8)

    # loop over events
    for start_ind, end_ind in zip(np.where(decal==1)[0], np.where(decal==-1)[0]):
        if (end_ind - start_ind)/sr > min_duration:
            ax.plot(np.linspace(start_ind, start_ind, 100)/sr, 
                    np.linspace(0, 1, 100), 'g-')
            ax.plot(np.linspace(end_ind, end_ind, 100)/sr, 
                    np.linspace(0, 1, 100), 'r-')
                # Create a Note instance for each note
            note = pretty_midi.Note(velocity=100, pitch=round(midi_note), start=start_ind/sr, end=end_ind/sr)
            add_note_to_instru(note, instru)

    return fig

def add_note_to_instru(note: pretty_midi.Note, instru: pretty_midi.Instrument):
    instru.notes.append(note)

def write_midi_file(midi: pretty_midi.PrettyMIDI, fname: str):
    midi.write(fname)
    
def get_multitrack_plot(fname: str):
    multitrack = pypianoroll.read(fname)
    multitrack_plot = multitrack.plot()


def rest():
    start = time.time()

    do_plot = True
    verbose = True

    ## Some user parameters 
    duration_for_analysis = 20 # duration of each wav that is analyzed
    filter_timescale = 80 # parameter for note segmentation : median filter lenghth, the larger the smoother the signal envelop
    threshold = 0.15 # parameter for note segmentation : energy level above which a note occurrence is detected
    min_duration = 0.03 # parameter for note segmentation : minimal duration below which a note occurrence is discarded 

    wav_list = glob.glob('capteurs/*wav')

    ## Create a PrettyMIDI object
    banjo_MIDI = pretty_midi.PrettyMIDI()
    # Create an Instrument instance for a banjo instrument
    banjo_program = pretty_midi.instrument_name_to_program('Banjo')
    banjo_instru = pretty_midi.Instrument(program=banjo_program)
    # Add the banjo instrument to the PrettyMIDI object
    banjo_MIDI.instruments.append(banjo_instru)

    ## Instatiate Marovany note dictionary
    note_list = create_note_list()
    fig_size = [28, 14]

    ## Start audio analysis
    for wav_file in wav_list:
        if verbose:
            print('\n Now processing file', wav_file)
        # audio data loading
        y, sr = librosa.load(wav_file, offset=0, duration=duration_for_analysis)
        amplitude_envelope = get_amplitude_envelope(y=y, filter_timescale=filter_timescale)
        decal = get_decal(amplitude_envelope, threshold)
        midi_note = get_note_guessed_from_fname(note_list=note_list, fname=wav_file)
        print("Guessed note :", midi_note)
        
        time_series_fig = get_time_series_fig(fig_size=fig_size, y=y, samp_rate=sr)
        pitch_detection_fig = get_pitch_detection_fig(fig_size=fig_size, ampl_envel=amplitude_envelope, threshold=threshold, min_duration=min_duration, instru=banjo_instru, decal=decal, midi_note=midi_note)

    plt.show()

    write_midi_file(banjo_MIDI, 'marovany.mid')
    get_multitrack_plot("marovany.mid")

    end = time.time()
    print('time of analysis:', end-start)
