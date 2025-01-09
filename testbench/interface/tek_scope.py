import pyvisa
from pyvisa import VisaIOError
import time

# Classe Mesure pour l'oscilloscope
class Mesure:
    def __init__(self, ip):
        # Init the ip and the resource manager
        self.ip = ip
        self.rm = pyvisa.ResourceManager()

        try:
            self.scope = self.rm.open_resource(f'TCPIP::{ip}::INSTR')
            print("Connecté à :", self.scope.query('*IDN?'))
            self.scope.write('*RST')  # Réinitialise l'oscilloscope
        except VisaIOError as e:
            print(f"Erreur de connexion à l'oscilloscope : {e}")
            self.scope = None

    def mesure_gain(self):
        # Mesure le gain entre CH1 et CH2
        if not self.scope:
            print("Oscilloscope non connecté.")
            return None

        try:
            self.scope.write('MEASUrement:IMMed:TYPe PK2pk')
            
            # Configuration et lecture pour CH1
            self.scope.write('MEASUrement:IMMed:SOUrce1 CH1')
            time.sleep(2)  # Attente pour stabilisation
            pik1 = float(self.scope.query('MEASUrement:IMMed:VALue?'))

            # Configuration et lecture pour CH2
            self.scope.write('MEASUrement:IMMed:SOUrce1 CH2')
            time.sleep(2)
            pik2 = float(self.scope.query('MEASUrement:IMMed:VALue?'))

            if pik1 <= 0:
                print("Valeur du canal 1 invalide (0 ou négative).")
                return None

            gain = pik2 / pik1
            return gain
        except VisaIOError as e:
            print(f"Erreur lors de la mesure du gain : {e}")
            return None

    def mesure_phase(self):
        # Mesure la phase entre CH1 et CH2
        if not self.scope:
            print("Oscilloscope non connecté.")
            return None

        try:
            self.scope.write('MEASUrement:IMMed:TYPe PHASE')
            self.scope.write('MEASUrement:IMMed:SOUrce1 CH1')
            self.scope.write('MEASUrement:IMMed:SOUrce2 CH2')
            time.sleep(2)  # Attente pour stabilisation

            phase = float(self.scope.query('MEASUrement:IMMed:VALue?'))
            return phase
        except VisaIOError as e:
            print(f"Erreur lors de la mesure de phase : {e}")
            return None

    def mesure_frequence(self):
        # Mesure la fréquence du signal sur CH1
        if not self.scope:
            print("Oscilloscope non connecté.")
            return None

        try:
            self.scope.write('MEASUrement:IMMed:TYPe FREQuency')
            self.scope.write('MEASUrement:IMMed:SOUrce1 CH1')
            time.sleep(2)  # Attente pour stabilisation

            freq = float(self.scope.query('MEASUrement:IMMed:VALue?'))
            return freq
        except VisaIOError as e:
            print(f"Erreur lors de la mesure de fréquence : {e}")
            return None

    def deconnecter(self):
        # Fermeture de la connexion
        if self.scope:
            self.scope.close()
            print("Connexion fermée.")
        else:
            print("Aucune connexion à fermer.")

# Exemple d'utilisation
if __name__ == '__main__':
    ip = '10.192.79.79'

    # Création de l'objet Mesure
    mesure = Mesure(ip)

    # Mesure du gain
    gain = mesure.mesure_gain()
    if gain is not None:
        print(f"Gain : {gain}")

    # Mesure de la phase
    phase = mesure.mesure_phase()
    if phase is not None:
        print(f"Phase : {phase}")

    # Mesure de la fréquence
    freq = mesure.mesure_frequence()
    if freq is not None:
        print(f"Fréquence : {freq} Hz")

    # Déconnexion
    mesure.deconnecter()
