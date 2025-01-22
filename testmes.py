import testbench.tek_scope as tek_scope
import testbench.Agilent_GenFct as Agilent_GenFct
import time
import numpy as np
import matplotlib.pyplot as plt

### Paramètres
pk2pk = 5
min_freq = 10
max_freq = 1000
points = 5

### Connexion aux instruments
try:
    function_gen = Agilent_GenFct.Agilent33220A('10.192.79.15')
    function_gen.connect()
    function_gen.set_amplitude(pk2pk)
    function_gen.set_waveform('SIN')
    function_gen.ActiveOutput()
except Exception as e:
    print(f"Erreur de connexion au générateur de fonction : {e}")
    exit(1)

try:
    scope = tek_scope.Tektronix_scope('10.192.79.63')
except Exception as e:
    print(f"Erreur de connexion à l'oscilloscope : {e}")
    function_gen.DeactivateOutput()
    function_gen.disconnect()
    exit(1)

### Acquisition des données
amp_x, amp_y, phase_x, phase_y = [], [], [], []

# Init
function_gen.set_frequency(min_freq)
scope.rescale_channels(frequence=min_freq, pk2pk=pk2pk)
time.sleep(1)
freq_mes = scope.mesure_frequence()
gain = scope.mesure_gain()
phase = scope.mesure_phase()

for i in range(0, points):
    freq = min_freq * (max_freq / min_freq) ** (i / (points - 1))
    function_gen.set_frequency(freq)
    time.sleep(0.2)

    scope.rescale_channels(frequence=freq, pk2pk=pk2pk)
    time.sleep(0.2)
    freq_mes = scope.mesure_frequence()
    gain = scope.mesure_gain()
    phase = scope.mesure_phase()

    if freq_mes is not None and gain is not None and phase is not None:
        amp_x.append(freq_mes)
        amp_y.append(gain)
        phase_x.append(freq_mes)
        phase_y.append(phase)
    else:
        print(f"⚠ Erreur de mesure à {freq:.2f} Hz, valeurs ignorées.")

### Fermeture propre des instruments
scope.deconnecter()

# Print the mesure in console
for i in range(len(amp_x)):
    print(f"Fréquence : {amp_x[i]} Hz, Gain : {amp_y[i]}, Phase : {phase_y[i]}")
