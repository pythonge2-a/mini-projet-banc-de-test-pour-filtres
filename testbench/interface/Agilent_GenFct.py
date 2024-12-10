import pyvisa

class Agilent33220A:
    def __init__(self, ip_address):
        """Initialise la connexion avec le générateur de fonctions."""
        self.resourceManager = pyvisa.ResourceManager()
        self.resourceString = f"TCPIP::{ip_address}::INSTR"
        self.functionGenerator = None
    
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
    
