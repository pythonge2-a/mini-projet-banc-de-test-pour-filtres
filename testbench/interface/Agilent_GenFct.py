import pyvisa

class Agilent33220A:
    def __init__(self, ip_address):
        """Initialise la connexion avec le générateur de fonctions."""
        self.resourceManager = pyvisa.ResourceManager()
        self.resourceString = f"TCPIP::{ip_address}::INSTR"
        self.functionGenerator = None
    # CONNECTION
    def connect(self):
        """Établit la connexion avec le générateur de fonctions."""
        try:
            self.functionGenerator = self.resourceManager.open_resource(self.resourceString)
            print("Connexion établie avec le générateur de fonctions.")
        except Exception as e:
            raise ConnectionError(f"Erreur de connexion : {e}")
        
    def disconnect(self):
        """Ferme la connexion avec le générateur de fonctions."""
        if self.functionGenerator:
            self.functionGenerator.close()
            self.resourceManager.close()
            print("Connexion fermée.")
            
    def get_id(self):
        """Retourne l'identifiant du générateur de fonctions."""
        return self.functionGenerator.query("*IDN?")
    
    # OUTPUT
    def ActiveOutput(self):
        """Active la sortie du générateur de fonctions."""
        self.functionGenerator.write("OUTPUT ON")

    def DeactiveOutput(self):
        """Désactive la sortie du générateur de fonctions."""
        self.functionGenerator.write("OUTPUT OFF")

    def get_output_status(self):
        """Lit l'état de la sortie du générateur de fonctions."""
        return self.functionGenerator.query("OUTPUT?")
    
    # SIGNAL CONFIGURATION
    def set_frequency(self, frequency):
        """Configure la fréquence du signal."""
        self.functionGenerator.write(f"FREQUENCY {frequency}")

    def get_frequency(self):
        """Lit la fréquence du signal."""
        return self.functionGenerator.query("FREQUENCY?")
    
    def set_amplitude(self, amplitude):
        """Configure l'amplitude du signal."""
        self.functionGenerator.write(f"VOLTAGE {amplitude}")

    def get_amplitude(self):
        """Lit l'amplitude du signal."""
        return self.functionGenerator.query("VOLTAGE?")
    
    def set_waveform(self, waveform):
        """Configure la forme d'onde du signal."""
        self.functionGenerator.write(f"FUNCTION {waveform}")
    
    def get_waveform(self):
        """Lit la forme d'onde du signal."""
        return self.functionGenerator.query("FUNCTION?")
    
    # def set_DutyCycle(self, DutyCycle):
    #      """Configure le cycle de travail du signal."""
    #      self.functionGenerator.write(f"DUTY_CYCLE {DutyCycle}")

    # def get_DutyCycle(self):
    #      """Lit le cycle de travail du signal."""
    #      return self.functionGenerator.query("DUTY_CYCLE?") 

Genfct = Agilent33220A("10.192.79.15")
Genfct.connect()
print(Genfct.get_id())
Genfct.set_amplitude(1)
Genfct.set_frequency(20000)
Genfct.set_waveform("SQUARE")
#Genfct.set_DutyCycle(10)
Genfct.DeactiveOutput()
print(Genfct.get_amplitude())
print(Genfct.get_frequency())
print(Genfct.get_waveform())
#print(Genfct.get_DutyCycle())
print(Genfct.get_output_status())


