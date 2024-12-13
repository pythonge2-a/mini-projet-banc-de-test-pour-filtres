import pyvisa

#ip_test_lab_multimeter = "10.192.79.36"

class SiglentSDM3065X:
    def __init__(self, ip_address):
        """Initialise la connexion avec le multimètre."""
        self.resourceManager = pyvisa.ResourceManager()
        self.resourceString = f"TCPIP::{ip_address}::INSTR"
        self.multimeter = None

    def connect(self):
        """Établit la connexion avec le multimètre."""
        try:
            self.multimeter = self.resourceManager.open_resource(self.resourceString)
            print("Connexion établie avec le multimètre.")
        except Exception as e:
            raise ConnectionError(f"Erreur de connexion : {e}")
    
    def disconnect(self):
        """Ferme la connexion avec le multimètre."""
        if self.multimeter:
            self.multimeter.close()
            self.resourceManager.close()
            print("Connexion terminée.")
    
    def get_id(self):
        """Retourne l'identifiant du multimètre."""
        return self.multimeter.query("*IDN?")
    
    def get_measure(self):
        """Lit la mesure du multimètre."""
        return self.multimeter.query("MEASURE?")
    
