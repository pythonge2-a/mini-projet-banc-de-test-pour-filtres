from testbench.interface.siglentmultimeter import SiglentSDM3065X

ip_test_lab_multimeter = "10.192.79.36"

print("Test du multimètre Siglent SDM3065X")

multimeter = SiglentSDM3065X(ip_test_lab_multimeter)
multimeter.connect()

print("ID du multimètre :")
print(multimeter.get_id())
print("measure",multimeter.get_measure())
print("measure v dc", multimeter.get_measure_v_dc())

print("measures v ac")
print(multimeter.get_measure_v_ac())
print(multimeter.get_measure_v_ac())
print(multimeter.get_measure_v_ac())
print(multimeter.get_measure_v_ac())
print(multimeter.get_measure_v_ac())
print(multimeter.get_measure_v_ac())
print(multimeter.get_measure_v_ac())
print(multimeter.get_measure_v_ac())
print(multimeter.get_measure_v_ac())
print(multimeter.get_measure_v_ac())
print(multimeter.get_measure_v_ac())


multimeter.disconnect()