import pyvisa

ip = '10.192.79.79'

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

    # Set automatique mesure the pk-pk value to Ch1 and Ch2
    scope.write('MEASUrement:MEAS1:SOURCE CH1')
    scope.write('MEASUrement:MEAS1:TYPe PK2pk')
    scope.write('MEASUrement:MEAS1:STATE ON')
    scope.write('MEASUrement:MEAS2:SOURCE CH1')
    scope.write('MEASUrement:MEAS2:TYPe PK2pk')
    scope.write('MEASUrement:MEAS2:STATE ON')
    
    # Get the pk-pk value of Ch1 and Ch2
    pik1 = scope.query('MEASUrement:MEAS1:VALue?')
    pik2 = scope.query('MEASUrement:MEAS2:VALue?')

    # print pik
    print(pik1)
    print(pik2)

    # print pik
    print(scope.query('MEASUrement:MEAS1:VALue?'))


except pyvisa.VisaIOError as e:
    print(f"Failed to connect to the oscilloscope: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")