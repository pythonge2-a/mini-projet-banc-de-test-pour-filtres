import pyvisa
from pyvisa import VisaIOError
import time

class Tektronix_scope:
    def __init__(self, ip):
        self.ip = ip
        self.rm = pyvisa.ResourceManager()

        try:
            self.scope = self.rm.open_resource(f'TCPIP::{ip}::INSTR')
            print("Connecté à :", self.scope.query('*IDN?'))
            self.scope.write('*RST')  # Réinitialise l'oscilloscope
            time.sleep(1)

            # Activation des canaux CH1 et CH2
            self.scope.write('SELect:CH1 ON')
            self.scope.write('SELect:CH2 ON')

            # Acquisition en cours
            self.scope.write('ACQuire:STATE RUN')

        except VisaIOError as e:
            print(f"Erreur de connexion à l'oscilloscope : {e}")
            self.scope = None

    def rescale_channels(self, frequence, pk2pk):
        try:
            # Calcul de l'échelle à partir de pk2pk
            scale_value = pk2pk / 4  # Appliquer 1/4 de la valeur de crête-à-crête

            # Ajuster les échelles des canaux en fonction de pk2pk
            self.scope.write(f'CH1:SCAle {scale_value}')
            self.scope.write(f'CH2:SCAle {scale_value}')

            print(f"Canaux rescalés : Échelle définie à {scale_value} V/div pour pk2pk = {pk2pk} V")

            # Ajuster l'échelle de temps en fonction de la fréquence
            self.scope.write(f'TIMEBASE:SCAle {1 / frequence}')  # Par exemple, pour une fréquence de 1 Hz, l'échelle de temps est 1 seconde/div
            print(f"Fréquence mise à jour : {frequence} Hz")

            time.sleep(1)  # Attente après l'ajustement

        except VisaIOError as e:
            print(f"Erreur lors du rescale des canaux : {e}")

    def mesure_gain(self):
        if not self.scope:
            print("Oscilloscope non connecté.")
            return None

        try:
            self.scope.write('MEASUrement:IMMed:TYPe CRMS')
            self.scope.write('MEASUrement:IMMed:SOUrce1 CH1')
            time.sleep(1)
            rms1 = float(self.scope.query('MEASUrement:IMMed:VALue?'))

            self.scope.write('MEASUrement:IMMed:SOUrce1 CH2')
            time.sleep(1)
            rms2 = float(self.scope.query('MEASUrement:IMMed:VALue?'))

            # Check if the rms1 is not null
            if rms1 == 0:
                print("Erreur : le gain ne peut pas être calculé si la valeur de référence est nulle.")
                return None

            gain = rms2 / rms1
            return gain

        except VisaIOError as e:
            print(f"Erreur lors de la mesure du gain : {e}")
            return None

    def mesure_phase(self):
        if not self.scope:
            print("Oscilloscope non connecté.")
            return None

        try:
            self.scope.write('MEASUrement:IMMed:TYPe PHASE')
            self.scope.write('MEASUrement:IMMed:SOUrce1 CH1')
            self.scope.write('MEASUrement:IMMed:SOUrce2 CH2')
            time.sleep(2)

            phase = float(self.scope.query('MEASUrement:IMMed:VALue?'))
            return phase

        except VisaIOError as e:
            print(f"Erreur lors de la mesure de phase : {e}")
            return None

    def mesure_frequence(self):
        if not self.scope:
            print("Oscilloscope non connecté.")
            return None

        try:
            self.scope.write('MEASUrement:IMMed:TYPe FREQuency')
            self.scope.write('MEASUrement:IMMed:SOUrce1 CH1')
            time.sleep(2)

            freq = float(self.scope.query('MEASUrement:IMMed:VALue?'))
            return freq

        except VisaIOError as e:
            print(f"Erreur lors de la mesure de fréquence : {e}")
            return None

    def deconnecter(self):
        if self.scope:
            self.scope.close()
            print("Connexion fermée.")
        else:
            print("Aucune connexion à fermer.")

# Exemple d'utilisation
if __name__ == '__main__':
    ip = '10.192.79.8'

    # Connect to the oscilloscope
    mesure = Tektronix_scope(ip)

    # Compteur the time of the measurement
    start = time.time()

    # Rescale the channels
    mesure.rescale_channels()

    # Measure gain, phase and frequency
    gain = mesure.mesure_gain()
    if gain is not None:
        print(f"Gain : {gain}")

    phase = mesure.mesure_phase()
    if phase is not None:
        print(f"Phase : {phase}")

    freq = mesure.mesure_frequence()
    if freq is not None:
        print(f"Fréquence : {freq} Hz")

    # Print the time of the measurement
    print(f"Temps de mesure : {time.time() - start} s")
    
    # Disconnect from the oscilloscope
    mesure.deconnecter()
