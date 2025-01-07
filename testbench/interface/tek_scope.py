import pyvisa
from pyvisa import VisaIOError

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
        # Mesure the gain between Ch1 and Ch2
        if not self.scope:
            print("Oscilloscope non connecté.")
            return None

        try:
            # Configuration des mesures sur les canaux
            self.scope.write('MEASUrement:MEAS1:SOURCE CH1')
            self.scope.write('MEASUrement:MEAS1:TYPE PK2pk')
            self.scope.write('MEASUrement:MEAS1:STATE ON')

            self.scope.write('MEASUrement:MEAS2:SOURCE CH2')
            self.scope.write('MEASUrement:MEAS2:TYPE PK2pk')
            self.scope.write('MEASUrement:MEAS2:STATE ON')

            # Autoscale pour ajuster l'affichage
            self.scope.write('AUTOSCALE')

            # Récupération des valeurs crête-à-crête
            pik1 = float(self.scope.query('MEASUrement:MEAS1:VALue?'))
            pik2 = float(self.scope.query('MEASUrement:MEAS2:VALue?'))

            # Delete the measure
            self.scope.write('MEASUrement:MEAS1:STATE OFF')
            self.scope.write('MEASUrement:MEAS2:STATE OFF')
                             
            # Calcul du gain
            if pik1 == 0:
                print("Valeur du canal 1 invalide (0).")
                return None
            gain = pik2 / pik1
            return gain
        except VisaIOError as e:
            print(f"Erreur lors de la mesure du gain : {e}")
            return None

    def mesure_phase(self):
        # Mesure the phase between Ch1 and Ch2
        if not self.scope:
            print("Oscilloscope non connecté.")
            return None

        try:
            # Configuration de la mesure de phase
            self.scope.write('MEASUrement:MEAS3:SOURCE1 CH1')
            self.scope.write('MEASUrement:MEAS3:SOURCE2 CH2')
            self.scope.write('MEASUrement:MEAS3:TYPE PHASE')
            self.scope.write('MEASUrement:MEAS3:STATE ON')

            # Autoscale pour ajuster l'affichage
            self.scope.write('AUTOSCALE')

            # Récupération de la valeur de phase
            phase = float(self.scope.query('MEASUrement:MEAS3:VALue?'))

            # Suppression de la mesure
            self.scope.write('MEASUrement:MEAS3:STATE OFF')

            return phase
        except VisaIOError as e:
            print(f"Erreur lors de la mesure de phase : {e}")
            return None
    
    def mesure_frequence(self):
        # Mesure the frequency of the signal on Ch1
        if not self.scope:
            print("Oscilloscope non connecté.")
            return None

        try:
            # Configuration de la mesure de fréquence
            self.scope.write('MEASUrement:MEAS4:SOURCE CH1')
            self.scope.write('MEASUrement:MEAS4:TYPE FREQuency')
            self.scope.write('MEASUrement:MEAS4:STATE ON')

            # Autoscale pour ajuster l'affichage
            self.scope.write('AUTOSCALE')

            # Récupération de la valeur de fréquence
            freq = float(self.scope.query('MEASUrement:MEAS4:VALue?'))

            # Suppression de la mesure
            self.scope.write('MEASUrement:MEAS4:STATE OFF')

            return freq
        except VisaIOError as e:
            print(f"Erreur lors de la mesure de fréquence : {e}")

    def deconnecter(self):
        # Close the connection
        if self.scope:
            self.scope.close()
            print("Connexion fermée.")
        else:
            print("Aucune connexion à fermer.")
