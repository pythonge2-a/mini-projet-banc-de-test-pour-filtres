import pyvisa

class TektronixTDS3014C:
    def __init__(self, ip_address):
        """Initialise la connexion avec l'oscilloscope."""
        self.resource_manager = pyvisa.ResourceManager()
        self.resource_string = f"TCPIP::{ip_address}::INSTR"
        self.oscilloscope = None

    def connect(self):
        """Établit la connexion avec l'oscilloscope."""
        try:
            self.oscilloscope = self.resource_manager.open_resource(self.resource_string)
            print("Connexion établie avec l'oscilloscope.")
        except Exception as e:
            raise ConnectionError(f"Erreur de connexion : {e}")

    def disconnect(self):
        """Ferme la connexion avec l'oscilloscope."""
        if self.oscilloscope:
            self.oscilloscope.close()
            self.resource_manager.close()
            print("Connexion fermée.")

    def get_id(self):
        """Retourne l'identifiant de l'oscilloscope."""
        return self.oscilloscope.query("*IDN?")

    def set_channel_scale(self, channel, scale):
        """Configure l'échelle d'une voie."""
        self.oscilloscope.write(f"CH{channel}:SCALE {scale}")

    def get_channel_scale(self, channel):
        """Lit l'échelle d'une voie."""
        return self.oscilloscope.query(f"CH{channel}:SCALE?")

    def set_trigger(self, source, slope="POSITIVE"):
        """Configure le déclenchement."""
        self.oscilloscope.write(f"TRIGGER:EDGE:SOURCE {source}")
        self.oscilloscope.write(f"TRIGGER:EDGE:SLOPE {slope}")

    def capture_waveform(self, channel):
        """Capture et retourne les données de la courbe d'un canal."""
        self.oscilloscope.write(f"DATA:SOURCE CH{channel}")
        self.oscilloscope.write("DATA:WIDTH 1")
        self.oscilloscope.write("DATA:ENC RPB")
        return self.oscilloscope.query_binary_values("CURVE?", datatype='B', container=list)
