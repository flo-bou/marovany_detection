import glob
# import os
# import time

import numpy as np
from scipy.signal import hilbert
from scipy.ndimage import median_filter
# import matplotlib.pyplot as plt
from matplotlib.pyplot import subplots
# import mpld3
# from mpld3 import plugins
# import librosa
# import librosa.display
import pretty_midi
from pypianoroll import read as pianorollread


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
    for note_candidate in note_list: # attention, A est reconnus même quand la note est A#
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


def get_decal(y: np.ndarray, amplitude_envelope: np.ndarray, threshold: float):
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


def get_time_series_fig(y: np.ndarray, samp_rate):
    # plt.rcParams['figure.figsize'] = fig_size
    fig, ax = subplots()
    # fig.set(figwidth=fig_size[0], figheight=fig_size[1])
    fig.set(tight_layout=True)
    ax.plot(np.linspace(0, len(y)/samp_rate, len(y)), y)
    ax.autoscale(enable=True, axis='x', tight=True)
    return fig


def get_pitch_detection_fig_and_add_note_to_instru(
        ampl_envel: np.ndarray, 
        threshold: float, 
        min_duration: float, 
        instru: pretty_midi.Instrument, 
        decal: np.ndarray,
        midi_note: int, 
        sample_rate
    ):
    # plt.rcParams['figure.figsize'] = fig_size
    fig, ax = subplots()
    fig.set(tight_layout=True)
    x = np.linspace(0, len(ampl_envel)/sample_rate, len(ampl_envel))
    ax.plot(x, ampl_envel, 'b', linewidth=0.8)
    ax.plot(x, np.linspace(threshold, threshold, len(ampl_envel)), 'k--', linewidth=0.8)

    # loop over events
    for start_ind, end_ind in zip(np.where(decal==1)[0], np.where(decal==-1)[0]):
        if (end_ind - start_ind)/sample_rate > min_duration:
            ax.plot(np.linspace(start_ind, start_ind, 100)/sample_rate, 
                    np.linspace(0, 1, 100), 'g-')
            ax.plot(np.linspace(end_ind, end_ind, 100)/sample_rate, 
                    np.linspace(0, 1, 100), 'r-')
            # Create a Note instance for each note
            note = pretty_midi.Note(velocity=100, pitch=round(midi_note), start=start_ind/sample_rate, end=end_ind/sample_rate)
            instru.notes.append(note)
    ax.autoscale(enable=True, axis='x', tight=True)
    return fig


def add_notes_to_instru_from_decal(
        instru: pretty_midi.Instrument, 
        min_duration: float, 
        decal: np.ndarray, 
        midi_note: int, 
        sample_rate
    ):
    for start_ind, end_ind in zip(np.where(decal==1)[0], np.where(decal==-1)[0]):
        if (end_ind - start_ind)/sample_rate > min_duration:
            # Create a Note instance for each note
            note = pretty_midi.Note(velocity=100, pitch=round(midi_note), start=start_ind/sample_rate, end=end_ind/sample_rate)
            instru.notes.append(note)


def write_midi_file(midi: pretty_midi.PrettyMIDI, fname: str):
    midi.write(fname)


def get_multitrack_fig(fname: str):
    multitrack = pianorollread(fname)
    multitrack_plot: np.ndarray = multitrack.plot()
    # fig, ax = subplots()
    # fig.set(tight_layout=True)
    # x = np.linspace(0, len(ampl_envel)/sample_rate, len(ampl_envel))
    # ax.plot(x, ampl_envel, 'b', linewidth=0.8)
    # ax.plot(x, np.linspace(threshold, threshold, len(ampl_envel)), 'k--', linewidth=0.8)
    return multitrack_plot


def rest():
    # start = time.time()

    do_plot = True
    verbose = True

    wav_list = glob.glob('capteurs/*wav')

    ## Instatiate Marovany note dictionary
    note_list = create_note_list()
    fig_size = [28, 14]

    ## Start audio analysis
    for wav_file in wav_list:
        if verbose:
            print('\n Now processing file', wav_file)
        # audio data loading
        # y, sr = librosa.load(wav_file, offset=0, duration=duration_for_analysis)
        # amplitude_envelope = get_amplitude_envelope(y=y, filter_timescale=filter_timescale)
        # decal = get_decal(amplitude_envelope, threshold)
        # midi_note = get_note_guessed_from_fname(note_list=note_list, fname=wav_file)
        # print("Guessed note :", midi_note)
        
        # time_series_fig = get_time_series_fig(fig_size=fig_size, y=y, samp_rate=sr)
        # pitch_detection_fig = get_pitch_detection_fig(fig_size=fig_size, ampl_envel=amplitude_envelope, threshold=threshold, min_duration=min_duration, instru=banjo_instru, decal=decal, midi_note=midi_note, sample_rate=sr)

    # plt.show()

    # write_midi_file(banjo_MIDI, 'marovany.mid')
    # get_multitrack_plot("marovany.mid")

    # end = time.time()
    # print('time of analysis:', end-start)
