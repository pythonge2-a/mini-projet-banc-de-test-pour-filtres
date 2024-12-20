import numpy as np
from matplotlib import pyplot as plt

def get_gainDb(vin, vout):
    """Retourne le gain en dB."""
    return 20 * np.log10(vout / vin)

def gain_for_each_frequency(freqs, gainsDb):
    """Return a dictionary conaining the gains indexed by frequency."""
    return dict(zip(freqs, gainsDb))

def formulate_data_multiple_Vin(freqs, vs_in, vs_out):
    """Format data in a dictionary."""
    gainsDb = [get_gainDb(vin, vout) for vin, vout in zip(vs_in, vs_out)]
    return gain_for_each_frequency(freqs, gainsDb)

def formulate_data_single_Vin(freqs, vin, vs_out):
    """Format data in a dictionary."""
    gainsDb = [get_gainDb(vin, vout) for vout in vs_out]
    return gain_for_each_frequency(freqs, gainsDb)

def get_cutoff_frequency(data):
    """Return cut off frequency (-3 dB) from dictionary."""
    for freq, gain in data.items():
        if gain < -3:
            return freq
    for freq, gain in data.items():
        if round(gain, 3) < -3:
            return freq
    return None

def plot_gain(data):
    """Plot response of the filter."""
    plt.plot(data.keys(), data.values())
    plt.xscale("log")
    plt.xlabel("Fréquence [Hz]")
    plt.ylabel("Gain [dB]")
    plt.grid()
    plt.show()
