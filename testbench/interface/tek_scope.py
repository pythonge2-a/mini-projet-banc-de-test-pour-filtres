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
            time.sleep(2)

            # Activation des canaux CH1 et CH2
            self.scope.write('SELect:CH1 ON')
            self.scope.write('SELect:CH2 ON')

            # Acquisition en cours
            self.scope.write('ACQuire:STATE RUN')
            time.sleep(1)

        except VisaIOError as e:
            print(f"Erreur de connexion à l'oscilloscope : {e}")
            self.scope = None

    def rescale_channels(self):
        """ Ajuste automatiquement l'échelle des canaux CH1 et CH2 """
        try:
            self.scope.write('MEASUrement:IMMed:TYPe PK2pk')  # Peak-to-peak
            self.scope.write('MEASUrement:IMMed:SOUrce1 CH1')
            time.sleep(1)
            pk2pk1 = float(self.scope.query('MEASUrement:IMMed:VALue?'))

            self.scope.write('MEASUrement:IMMed:SOUrce1 CH2')
            time.sleep(1)
            pk2pk2 = float(self.scope.query('MEASUrement:IMMed:VALue?'))

            # Définition de l'échelle (1/4 de la valeur peak-to-peak pour un bon affichage)
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
            self.rescale_channels()  # Ajustement de l'échelle avant la mesure

            self.scope.write('MEASUrement:IMMed:TYPe CRMS')
            self.scope.write('MEASUrement:IMMed:SOUrce1 CH1')
            time.sleep(2)
            rms1 = float(self.scope.query('MEASUrement:IMMed:VALue?'))

            self.scope.write('MEASUrement:IMMed:SOUrce1 CH2')
            time.sleep(2)
            rms2 = float(self.scope.query('MEASUrement:IMMed:VALue?'))

            if rms1 <= 0:
                print("Valeur RMS de CH1 invalide (0 ou négative), impossible de calculer le gain.")
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
            self.rescale_channels()  # Ajustement de l'échelle avant la mesure

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
            self.rescale_channels()  # Ajustement de l'échelle avant la mesure

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

    mesure = Mesure(ip)

    gain = mesure.mesure_gain()
    if gain is not None:
        print(f"Gain : {gain}")

    phase = mesure.mesure_phase()
    if phase is not None:
        print(f"Phase : {phase}")

    freq = mesure.mesure_frequence()
    if freq is not None:
        print(f"Fréquence : {freq} Hz")

    mesure.deconnecter()
