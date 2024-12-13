from testbench.interface.siglentmultimeter import siglentmultimeter

ip_test_lab_multimeter = "10.192.79.36"

multimeter = siglentmultimeter.SiglentSDM3065X(ip_test_lab_multimeter)

multimeter.connect()