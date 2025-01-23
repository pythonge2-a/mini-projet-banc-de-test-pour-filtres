from testbench.siglentmultimeter import SiglentSDM3065X

ip_test_lab_multimeter = "192.168.137.221"

print("Test du multimètre Siglent SDM3065X")

multimeter = SiglentSDM3065X(ip_test_lab_multimeter)
multimeter.connect()

print("ID du multimètre :")
print(multimeter.get_id())

if multimeter.VdcChangeMode() is not None:
    print("DC ready, measures :")

    print(multimeter.get_measure_v_dc())
    print(multimeter.get_measure_v_dc())
    print(multimeter.get_measure_v_dc())
    print(multimeter.get_measure_v_dc())
    print(multimeter.get_measure_v_dc())
else:
    print("DC not ready")

if multimeter.VacChangeMode() is not None:
    print("AC ready, measures :")

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
else:
    print("AC not ready")


multimeter.disconnect()
