from testbench.interface.siglentmultimeter import SiglentSDM3065X

ip_test_lab_multimeter = "10.192.79.36"

print("Test du multimètre Siglent SDM3065X")

multimeter = SiglentSDM3065X(ip_test_lab_multimeter)
multimeter.connect()
print(multimeter.get_id())
print(multimeter.get_measure())
print(multimeter.get_measure_v_dc())
print(multimeter.get_measure_v_ac())
multimeter.disconnect()