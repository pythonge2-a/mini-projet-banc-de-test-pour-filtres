import pyvisa
import logging

# Configuration de la journalisation
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

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
            self.oscilloscope.timeout = 5000  # Timeout de 5 secondes
            logging.info("Connexion établie avec l'oscilloscope.")
        except Exception as e:
            logging.error(f"Erreur de connexion : {e}")
            raise ConnectionError(f"Erreur de connexion : {e}")

    def disconnect(self):
        """Ferme la connexion avec l'oscilloscope."""
        if self.oscilloscope:
            self.oscilloscope.close()
            self.resource_manager.close()
            logging.info("Connexion fermée.")

    def get_id(self):
        """Retourne l'identifiant de l'oscilloscope."""
        idn = self.oscilloscope.query("*IDN?")
        logging.info(f"Identifiant de l'oscilloscope : {idn.strip()}")
        return idn.strip()

    def set_channel_scale(self, channel, scale):
        """Configure l'échelle d'une voie."""
        if channel not in range(1, 5):
            raise ValueError("Le canal doit être entre 1 et 4.")
        if not (0.001 <= scale <= 10):
            raise ValueError("L'échelle doit être entre 0.001 et 10.")
        self.oscilloscope.write(f"CH{channel}:SCALE {scale}")
        logging.info(f"Échelle du canal {channel} configurée à {scale} V/div.")

    def get_channel_scale(self, channel):
        """Lit l'échelle d'une voie."""
        if channel not in range(1, 5):
            raise ValueError("Le canal doit être entre 1 et 4.")
        scale = self.oscilloscope.query(f"CH{channel}:SCALE?")
        logging.info(f"Échelle actuelle du canal {channel} : {scale.strip()} V/div.")
        return float(scale.strip())

    def set_trigger(self, source, slope="POSITIVE"):
        """Configure le déclenchement."""
        if source not in [f"CH{i}" for i in range(1, 5)]:
            raise ValueError("La source doit être l'un des canaux CH1, CH2, CH3 ou CH4.")
        if slope not in ["POSITIVE", "NEGATIVE"]:
            raise ValueError("La pente doit être 'POSITIVE' ou 'NEGATIVE'.")
        self.oscilloscope.write(f"TRIGGER:EDGE:SOURCE {source}")
        self.oscilloscope.write(f"TRIGGER:EDGE:SLOPE {slope}")
        logging.info(f"Déclenchement configuré sur {source} avec une pente {slope}.")

    def capture_waveform(self, channel):
        """Capture et retourne les données de la courbe d'un canal."""
        if channel not in range(1, 5):
            raise ValueError("Le canal doit être entre 1 et 4.")
        self.oscilloscope.write(f"DATA:SOURCE CH{channel}")
        self.oscilloscope.write("DATA:WIDTH 1")
        self.oscilloscope.write("DATA:ENC RPB")
        raw_data = self.oscilloscope.query_binary_values("CURVE?", datatype="B", container=list)
        logging.info(f"{len(raw_data)} points capturés sur le canal {channel}.")
        return raw_data

    def __enter__(self):
        """Support du gestionnaire de contexte."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Nettoyage lors de la sortie du contexte."""
        self.disconnect()