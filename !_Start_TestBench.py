import subprocess

# Activer l'environnement virtuel Poetry
subprocess.run(["poetry", "shell"], check=True)

# Exécuter le script Python dans l'environnement virtuel
subprocess.run(["poetry", "run", "python", "testbench/usr_Interface.py"], check=True)