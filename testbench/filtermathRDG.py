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
     # Trier les données par fréquence croissante
    frequences = np.array(sorted(data.keys()))
    gains = np.array([data[f] for f in frequences])

    # Trouver le gain maximal
    gain_max = max(gains)

    # Calculer le niveau de -3 dB
    seuil_coupure = gain_max / np.sqrt(2)

    # Trouver la fréquence la plus proche du seuil de -3 dB
    for i in range(1, len(gains)):
        if gains[i] <= seuil_coupure:
            # Interpolation linéaire pour une meilleure précision
            f1, f2 = frequences[i - 1], frequences[i]
            g1, g2 = gains[i - 1], gains[i]
            frequence_coupure = f1 + (seuil_coupure - g1) * (f2 - f1) / (g2 - g1)
            return frequence_coupure
    
    # Si aucune fréquence de coupure n'est trouvée
    return None


def get_quality_factor(data):
    """Return quality factor from dictionary."""
    if not isinstance(data, dict):
        raise TypeError("Data must be a dictionary")

    cutfreq = get_cutoff_frequency(data)

    if cutfreq is None:
        raise ValueError("Cutoff frequency is not found")

    cutfreq = round(cutfreq, 0)

    if data[cutfreq / 10] < 5:
        return cutfreq / (2 * (data[cutfreq] + 3))
    else:
        return cutfreq / (2 * (data[cutfreq / 10] + 3))


def get_order(data):
    """Return order of the filter."""

    if not isinstance(data, dict):
        raise TypeError("Data must be a dictionary")

    if data == None:
        raise ValueError("No data found")

    cutfreq = get_cutoff_frequency(data)

    if cutfreq is None:
        raise ValueError("Cutoff frequency is not found")

    cutfreq = round(cutfreq, 0)

    if data[cutfreq / 10] < 5:
        if -19 > data[10 * cutfreq] > -25:
            return 1
        elif -39 > data[10 * cutfreq] > -45:
            return 2
        elif -58 > data[10 * cutfreq] > -65:
            return 3
        else:
            return None
    else:
        if -19 > data[cutfreq / 10] > -25:
            return 1
        elif -39 > data[cutfreq / 10] > -45:
            return 2
        elif -58 > data[cutfreq / 10] > -65:
            return 3
        else:
            return None


def plot_gain(data):
    """Plot response of the filter."""
    plt.plot(data.keys(), data.values())
    plt.xscale("log")
    plt.xlabel("Fréquence [Hz]")
    plt.ylabel("Gain [dB]")
    plt.grid()
    plt.show()
