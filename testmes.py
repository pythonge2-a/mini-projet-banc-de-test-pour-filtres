import testbench.interface.tek_scope as tek_scope
import testbench.interface.Agilent_GenFct as Agilent_GenFct
import time

### Fait les mesure et avance le chargement de la barre de progression selon les mesures
function_gen = Agilent_GenFct.Agilent33220A('10.192.79.15')  # Use the correct class name here
function_gen.connect()
function_gen.set_amplitude(5)
function_gen.set_waveform('SIN')
function_gen.ActiveOutput()

scope = tek_scope.Tektronix_scope('10.192.79.78')

min_freq = 10
max_freq = 100
points = 6
amp_x, amp_y, phase_x, phase_y = [], [], [], []

for i in range(points):
    freq = min_freq + (max_freq - min_freq) * i / (points - 1)
    function_gen.set_frequency(freq)
    time.sleep(0.1)
    scope.rescale_channels()
    freq_mes = scope.mesure_frequence()
    amp_x.append(freq_mes)
    amp_y.append(scope.mesure_gain())
    phase_x.append(freq_mes)
    phase_y.append(scope.mesure_phase())