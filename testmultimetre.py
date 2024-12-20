from testbench.interface.siglentmultimeter import SiglentSDM3065X

ip_test_lab_multimeter = "10.192.79.36"


multimeter= SiglentSDM3065X(ip_test_lab_multimeter)
multimeter.connect()
print(multimeter.get_id())
print(multimeter.get_measure())