from time import time

import numpy as np
from scipy.signal import hilbert
from scipy.ndimage import median_filter
# import matplotlib.pyplot as plt
from matplotlib.pyplot import subplots
import pretty_midi
from pypianoroll import read as pianorollread


def get_amplitude_envelope(y: np.ndarray, filter_timescale: int):
    print("get_amplitude_envelope")
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


def get_time_series_fig(y: np.ndarray, samp_rate):
    print("get_time_series_fig")
    # plt.rcParams['figure.figsize'] = fig_size
    fig, ax = subplots()
    # fig.set(figwidth=fig_size[0], figheight=fig_size[1])
    fig.set(tight_layout=True)
    x = np.linspace(0, len(y)/samp_rate, len(y))
    ax.plot(x, y)
    ax.autoscale(enable=True, axis='x', tight=True)
    return fig


def get_note_guessed_from_fname(note_list: list, fname: str):
    """Extract MIDI note name based on wav filename. 
    Note name should be in the filename

    Args:
        note_list (list[str]): List of possible notes as strings
        fname (str): name of wav file

    Returns:
        A tuple containing :
            str or None : the note name
            int or None : the note number in pretty_midi format or None if note name was not in file name
    """
    midi_note = None
    note_name = None
    for note_candidate in note_list:
        if note_candidate in fname:
            note_name = note_candidate
            midi_note = pretty_midi.note_name_to_number(note_candidate)
            break
    return note_name, midi_note


def verify_note_proposition(note_list: list, note_name: str):
    """Verify a note name proposal (by the user)
    Args:
        note_list (list[str]): List of possible notes as strings
        note_name (str): name of note
    Returns:
        A tuple containing :
            str : the note name
            int or None : the note number in pretty_midi format or None if note_name was not in note_list
    """
    midi_note = None
    if note_name in note_list:
        midi_note = pretty_midi.note_name_to_number(note_name)
    return note_name, midi_note


def get_amplitude_envelope(y: np.ndarray, filter_timescale: int):
    """ Extract signal envelop, median filter it and normalize by max
    Args:
        y (_type_): _description_
    Returns:
        np.ndarray: amplitude_envelope
    """
    # very long : 40 sec/40Mo
    start = time()
    analytic_signal = hilbert(y) # long : 20 sec
    print("Duration of hilbert() :", str(time()-start))
    amplitude_envelope = np.abs(analytic_signal)  
    print("Duration of hilbert() + np.abs() :", str(time()-start))
    amplitude_envelope = median_filter(amplitude_envelope, filter_timescale) # long : 20 sec
    print("Duration of hilbert() + np.abs() + median_filter() :", str(time()-start))
    amplitude_envelope = amplitude_envelope / max(amplitude_envelope)
    print("Duration of get_amplitude_envelope() :", str(time()-start))
    return amplitude_envelope


def get_decal(y: np.ndarray, amplitude_envelope: np.ndarray, threshold: float):
    """
    Args:
        y (np.ndarray): time series
        amplitude_envelope (np.ndarray):
        threshold (float):
    Returns:
        np.ndarray:
    """
    start = time()
    new_binary = np.zeros(len(y))
    print("Duration of np.zeros() :", str(time()-start))
    new_binary[amplitude_envelope > threshold] = 1
    print("Duration of np.zeros() + new_binary :", str(time()-start))
    decal = new_binary[1:] - new_binary[0:-1]
    print("Duration of get_decal() :", str(time()-start)) # very short
    return decal


def get_time_series_fig(y: np.ndarray, samp_rate):
    """Generate a matplotlib figure from time series data

    Args:
        y (np.ndarray): 
        samp_rate (_type_): 

    Returns:
        matplotlib.figure.Figure: The generated figure
    """    
    # plt.rcParams['figure.figsize'] = fig_size
    fig, ax = subplots()
    # fig.set(figwidth=fig_size[0], figheight=fig_size[1])
    fig.set(tight_layout=True)
    x = np.linspace(0, len(y)/samp_rate, len(y))
    ax.plot(x, y)
    ax.autoscale(enable=True, axis='x', tight=True)
    return fig


def get_pitch_detection_fig(
        ampl_envel: np.ndarray, 
        threshold: float, 
        min_duration: float, 
        # instru: pretty_midi.Instrument, 
        decal: np.ndarray,
        # midi_note: int | None, 
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
            # note = pretty_midi.Note(velocity=100, pitch=round(midi_note), start=start_ind/sample_rate, end=end_ind/sample_rate)
            # instru.notes.append(note)
    ax.autoscale(enable=True, axis='x', tight=True)
    return fig


# def add_notes_to_midi_instrument(
#         instru: pretty_midi.Instrument, 
#         min_duration: float, 
#         decal: np.ndarray, 
#         midi_note: int | None, 
#         sample_rate
#     ):
#     if midi_note != None:
#         for start_ind, end_ind in zip(np.where(decal==1)[0], np.where(decal==-1)[0]):
#             if (end_ind - start_ind)/sample_rate > min_duration:
#                 # Create a Note instance for each note
#                 note = pretty_midi.Note(velocity=100, pitch=round(midi_note), start=start_ind/sample_rate, end=end_ind/sample_rate)
#                 instru.notes.append(note)
#     else:
#         print("ERROR : Note not identified. No note added to instrument")


def get_multitrack_fig(fname: str, y: np.ndarray, samp_rate):
    # TODO
    multitrack = pianorollread(fname)
    multitrack_plot: np.ndarray = multitrack.plot()
    print(multitrack_plot)
    # fig, ax = subplots()
    # fig.set(tight_layout=True)
    # x = np.linspace(0, len(y)/samp_rate, len(y))
    # # x = np.linspace(0, len(ampl_envel)/sample_rate, len(ampl_envel))
    # ax.plot(x, multitrack_plot)
    # # ax.plot(x, ampl_envel, 'b', linewidth=0.8)
    # # ax.plot(x, np.linspace(threshold, threshold, len(ampl_envel)), 'k--', linewidth=0.8)
    # ax.autoscale(enable=True, axis='x', tight=True)
    # return fig
