import pyvisa
import pyvisa

ip = '10.192.79.62'
rm = pyvisa.ResourceManager()

try:
    scope = rm.open_resource(f'TCPIP::{ip}::INSTR')
    print(scope.query('*IDN?'))
except pyvisa.VisaIOError as e:
    print(f"Failed to connect to the device: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")