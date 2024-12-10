from src.interface.tek_scope import TektronixTDS3014C
# Test de la connexion
def main():
    osc_ip = "10.192.79.62"
    scope = TektronixTDS3014C(osc_ip)

    try:
        scope.connect()
        idn = scope.oscilloscope.query("*IDN?")
        print(f"Identifiant de l'oscilloscope : {idn}")
    except Exception as e:
        print(f"Erreur : {e}")
    finally:
        scope.disconnect()

if __name__ == "__main__":
    main()