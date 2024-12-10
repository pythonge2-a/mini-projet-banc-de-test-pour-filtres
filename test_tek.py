from src.interface.tek_scope import TektronixTDS3014C

def main():
    # Adresse IP de l'oscilloscope
    osc_ip = "10.193.64.62"

    # Instancier la classe
    scope = TektronixTDS3014C(osc_ip)

    try:
        # Connexion à l'oscilloscope
        scope.connect()

        # Obtenir l'identifiant
        idn = scope.get_id()
        print(f"Identifiant : {idn}")

        # Configurer le canal 1
        scope.set_channel_scale(channel=1, scale=0.01)
        scale = scope.get_channel_scale(channel=1)
        print(f"Échelle actuelle du canal 1 : {scale}")

        # Configurer le déclenchement
        scope.set_trigger(source="CH1", slope="POSITIVE")

        # Capturer les données de la courbe
        waveform = scope.capture_waveform(channel=1)
        print(f"Nombre de points capturés : {len(waveform)}")

    except Exception as e:
        print(f"Erreur : {e}")
    finally:
        # Déconnexion de l'oscilloscope
        scope.disconnect()

if __name__ == "__main__":
    main()
