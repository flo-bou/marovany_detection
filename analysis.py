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
