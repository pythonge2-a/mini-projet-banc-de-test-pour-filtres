import pyvisa

ip = '10.192.79.62'
port = 5025  # Port par défaut pour SCPI
backend = '@py'  # Utiliser pyvisa-py explicitement

try:
    # Initialisation du gestionnaire de ressources
    rm = pyvisa.ResourceManager(backend)
    print("Available resources:", rm.list_resources())

    # Connexion à l'oscilloscope
    scope = rm.open_resource(f'TCPIP::{ip}::{port}::SOCKET')
    scope.timeout = 5000  # Timeout de 5 secondes
    scope.read_termination = '\n'  # Terminaison pour les commandes SCPI

    # Envoi d'une commande SCPI
    print("Connected to:", scope.query('*IDN?'))
except pyvisa.VisaIOError as e:
    print(f"Failed to connect to the oscilloscope: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
