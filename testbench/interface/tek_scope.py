import pyvisa
from pyvisa import VisaIOError
import time

class Mesure:
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

    def rescale_channels(self):
        # Rescale the channels to 1/4 of the peak-to-peak value for a better display
        try:
            self.scope.write('MEASUrement:IMMed:TYPe PK2pk')  # Peak-to-peak
            self.scope.write('MEASUrement:IMMed:SOUrce1 CH1')
            time.sleep(1)
            pk2pk1 = float(self.scope.query('MEASUrement:IMMed:VALue?'))

            self.scope.write('MEASUrement:IMMed:SOUrce1 CH2')
            time.sleep(1)
            pk2pk2 = float(self.scope.query('MEASUrement:IMMed:VALue?'))

            # Define the scale of the channels
            if pk2pk1 > 0:
                self.scope.write(f'CH1:SCAle {pk2pk1 / 4}')
            if pk2pk2 > 0:
                self.scope.write(f'CH2:SCAle {pk2pk2 / 4}')

            print("Canaux rescalés")
            time.sleep(1)  # Attente après le rescale

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
    mesure = Mesure(ip)

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
