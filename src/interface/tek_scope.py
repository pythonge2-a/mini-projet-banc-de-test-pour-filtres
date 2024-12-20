import pyvisa

ip = '10.192.79.30'

try:
    # Initialisation du gestionnaire de ressources
    rm = pyvisa.ResourceManager()

    # Connexion à l'oscilloscope
    scope = rm.open_resource(f'TCPIP::{ip}::INSTR')

    # Envoi d'une commande SCPI
    print("Connected to:", scope.query('*IDN?'))


    # Default setup
    scope.write('*RST')
    scope.write('AUTOSCALE')
except pyvisa.VisaIOError as e:
    print(f"Failed to connect to the oscilloscope: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")