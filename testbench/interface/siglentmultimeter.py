import pyvisa

#ip_test_lab_multimeter = "10.192.79.36"

class SiglentSDM3065X:
    def __init__(self, ip_address):
        """Initialise multimeter class."""
        self.resourceManager = pyvisa.ResourceManager()
        self.resourceString = f"TCPIP::{ip_address}::INSTR"
        self.multimeter = None
        self.isconnected = False

    def connect(self):
        """Connect to multimeter."""
        if self.isconnected:
            raise ConnectionError("Connexion déjà établie.")
        
        try:
            self.multimeter = self.resourceManager.open_resource(self.resourceString)
            self.isconnected = True
            print("Connexion établie avec le multimètre.")
        except Exception as e:
            raise ConnectionError(f"Erreur de connexion : {e}")
    
    def disconnect(self):
        """Ferme la connexion avec le multimètre."""
        if not self.isconnected:
            raise ConnectionError("Pas de connexion établie.")
        
        if self.multimeter:
            self.multimeter.close()
            self.resourceManager.close()
            self.isconnected = False
            print("Connexion terminée.")

    
    def get_id(self):
        """Return multimeter ID."""
        if not self.isconnected:
            raise ConnectionError("Pas de connexion établie.")
        
        return self.multimeter.query("*IDN?")
    
    def get_measure(self):
        if not self.isconnected:
            raise ConnectionError("Pas de connexion établie.")
        
        """Read multimeter."""
        return self.multimeter.query("MEASURE?")
    
    def get_measure_v_dc(self):
        """Read DC voltage from multimeter."""

        if not self.isconnected:
            raise ConnectionError("Pas de connexion établie.")
        
        return self.multimeter.query("MEASURE:VOLTAGE:DC?")

    def get_measure_v_ac(self):
        """Read ac voltage from multimeter."""
        if not self.isconnected:
            raise ConnectionError("Pas de connexion établie.")
        
        return self.multimeter.query("MEASURE:VOLTAGE:AC?")

    def append_vac_in_csv(self, filename):
        """Save measure in csv."""
        if not self.isconnected:
            raise ConnectionError("Pas de connexion établie.")
        
        measure = self.get_measure_v_ac()
        with open(filename, "a") as file:
            file.write(measure)

    def append_vdc_in_csv(self, filename):
        if not self.isconnected:
            raise ConnectionError("Pas de connexion établie.")
        
        """Save measure in csv."""
        measure = self.get_measure_v_dc()
        with open(filename, "a") as file:
            file.write(measure)
    
    def append_multmeter_measure_in_csv(self, mode, filename):
        """Save measure in csv."""
        if not self.isconnected:
            raise ConnectionError("Pas de connexion établie.")
        
        if mode == "VDC":
            measure = self.get_measure_v_dc()
        elif mode == "VAC":
            measure = self.get_measure_v_ac()
        with open(filename, "a") as file:
            file.writerows(measure)
            
    
