import pyvisa
from pyvisa import VisaIOError

ip = '10.192.79.62'
rm = pyvisa.ResourceManager('@py')

try:
    scope = rm.open_resource(f'TCPIP::{ip}:INSTR')
    print(scope.query('*IDN?'))
except VisaIOError as e:
    print(f"Failed to connect to the device: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")