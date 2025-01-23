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
    gains_db = np.array([data[f] for f in frequences])

    # Vérifier les valeurs invalides dans les données
    if not np.all(np.isfinite(gains_db)):
        raise ValueError(
            "Les gains contiennent des valeurs non finies (NaN ou Inf). Vérifiez les données."
        )

    # Parcourir les fréquences pour détecter une chute de -3 dB par décades
    for i in range(1, len(frequences)):
        # Vérifier si les points appartiennent à une nouvelle décade
        if np.log10(frequences[i]) - np.log10(frequences[i - 1]) >= 1:
            # Calcul de la différence de gain entre les deux points
            gain_diff = gains_db[i] - gains_db[i - 1]
            if abs(gain_diff) >= 3:  # Si la chute est de -3 dB ou plus
                return frequences[i]

    # Si aucune fréquence de coupure n'est trouvée
    return None


def get_quality_factor(data):
    """Return quality factor from dictionary."""
    # Trier les données par fréquence croissante
    frequences = np.array(sorted(data.keys()))
    gains = np.array([data[f] for f in frequences])

    # Trouver la fréquence centrale (f0) où le gain est maximal
    gain_max = max(gains)
    indice_max = np.argmax(gains)
    f0 = frequences[indice_max]

    # Calculer le niveau de -3 dB
    seuil_coupure = gain_max / np.sqrt(2)

    # Trouver f1 et f2 (fréquences où le gain est égal au seuil -3 dB)
    f1, f2 = None, None
    for i in range(1, len(gains)):
        if gains[i - 1] >= seuil_coupure > gains[i]:
            # Interpolation linéaire pour f1
            f1 = frequences[i - 1] + (seuil_coupure - gains[i - 1]) * (
                frequences[i] - frequences[i - 1]
            ) / (gains[i] - gains[i - 1])
        if gains[i - 1] <= seuil_coupure < gains[i]:
            # Interpolation linéaire pour f2
            f2 = frequences[i - 1] + (seuil_coupure - gains[i - 1]) * (
                frequences[i] - frequences[i - 1]
            ) / (gains[i] - gains[i - 1])

    # Vérifier si f1 et f2 ont été trouvés
    if f1 is not None and f2 is not None and f2 > f1:
        # Calculer le facteur de qualité
        Q = f0 / (f2 - f1)
        return Q

    # Retourner None si Q ne peut pas être calculé
    return None


def get_order(data):
    """Return order of the filter."""
    # Trier les données par fréquence croissante
    frequences = np.array(sorted(data.keys()))
    gains = np.array([data[f] for f in frequences])

    # Vérifier si les gains sont en dB, sinon les convertir
    if max(gains) > 0:
        gains = 20 * np.log10(gains)

    # Trouver la fréquence de coupure (-3 dB)
    gain_max = max(gains)
    seuil_coupure = gain_max - 3

    # Trouver l'indice correspondant à la fréquence de coupure
    indice_coupure = None
    for i in range(1, len(gains)):
        if gains[i - 1] >= seuil_coupure > gains[i]:
            indice_coupure = i
            break

    if indice_coupure is None:
        return None  # Impossible de déterminer l'ordre sans fréquence de coupure

    # Calculer la pente autour de la fréquence de coupure (zone linéaire)
    pente = (gains[indice_coupure] - gains[indice_coupure + 1]) / (
        np.log10(frequences[indice_coupure]) - np.log10(frequences[indice_coupure + 1])
    )

    # La pente en dB/décade est proportionnelle à l'ordre
    ordre = abs(pente / 20)  # Diviser par 20 car un ordre donne -20 dB/décade
    return round(ordre)


def plot_gain(data):
    """Plot response of the filter."""
    plt.plot(data.keys(), data.values())
    plt.xscale("log")
    plt.xlabel("Fréquence [Hz]")
    plt.ylabel("Gain [dB]")
    plt.grid()
    plt.show()
