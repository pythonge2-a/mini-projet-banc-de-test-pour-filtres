import pyvisa


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
            self.multimeter.timeout = 5000  # Define timeout to 5000 ms (5 seconds)
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
            print("Connexion terminée avec le multimetre.")

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

    def VdcChangeMode(self):
        """Check if multimeter is ready."""
        if not self.isconnected:
            raise ConnectionError("Pas de connexion établie.")

        # makes sure the multimeter is in vac mode
        try:
            self.get_measure_v_dc()
        except pyvisa.errors.VisaIOError as e:
            _ = e  # timeout is a known error, this is an easy fix
            pass

        self.get_measure_v_dc()

        return self.get_id()

    def VacChangeMode(self):
        """Check if multimeter is ready."""
        if not self.isconnected:
            raise ConnectionError("Pas de connexion établie.")

        # makes sure the multimeter is in vdc mode
        try:
            self.get_measure_v_ac()
        except pyvisa.errors.VisaIOError as e:
            _ = e  # timeout is a known error, this is an easy fix
            pass

        self.get_measure_v_ac()

        return self.get_id()
