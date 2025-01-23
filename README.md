# Projet banc de test pour filtres
## Membres du groupe

- Nicolas Zaco
- Rémy Di Giovanni
- Julien Vullioud
- Martin Luthi

# Objectif du projet

L'objectif de ce projet est de développer un programme en Python permettant de tester un filtre de type quelconque. Le programme interagira avec un générateur de signaux et un oscilloscope afin de générer et d'analyser un diagramme de Bode.

## Description
Ce projet consiste à :

- Interfacer un oscilloscope et un générateur de fonctions avec un PC, afin de réaliser des mesures sur un filtre d'ordre n.

- Utiliser le générateur de fonctions pour produire des signaux sinusoïdaux à fréquence variable, servant d'entrée pour le filtre à tester.

- Mesurer la réponse du filtre avec l'oscilloscope, qui enregistrera l'amplitude et la phase de la sortie du filtre pour différentes fréquences.

- Récupérer les données mesurées par l'oscilloscope via le PC, pour les traiter et caractériser le filtre (gain, réponse en fréquence, etc.).

- Afficher les résultats via une interface graphique, permettant de visualiser les caractéristiques du filtre sous forme de diagramme de Bode.

- Permettre la configuration du test via l'interface graphique : l'utilisateur pourra paramétrer les conditions du test (fréquences, types de signaux, etc.) et lancer le test.

## Diagramme
![Diagramme](doc/image/diagramme.png)

## Appareils de mesures

### Oscilloscope :
![Oscilloscope_f](doc/image/Oscilloscope_f.jpg)
![Oscilloscope_b](doc/image/Oscilloscope_b.jpg)

### Générateur de fonctions :
![gene_f](doc/image/gene_f.jpg)
![gene_b](doc/image/gene_b.jpg)

### Multimètre digital :
![gene_f](doc/image/multim_f.jpg)
![gene_b](doc/image/multim_b.jpg)

# Liste des tâches par personnes
![Liste_taches](doc/image/Liste_taches.png)

# Fonctionnement de la mesure
![Diagramme_Code_Mesure](doc/image/Diagramme_Code_Mesure.png)

- Envois des paramètres de fréquence et amplitude au générateur de fonctions
- attente de la stabilisation de la sortie du générateur (soit temp d'attente, soit validation par le générateur)
- Mesure de l'amplitude et de la phase par l'oscilloscope (exemple: CH1: (fréquence ; amplitude) CH2: (fréquence ; amplitude) Phase (fréquence ; phase))
  - fréquence: fréquence mesurée par l'oscillo (on ne fait pas confiance au générateur)
  - amplitude: amplitude mesurée par l'oscillo, CH1 entrée filtre, CH2 sortie filtre
  - phase: phase mesurée par l'oscillo par mesure auto ou par delta T.
- mesure de l'amplitude de sortie du filtre (exemple: Uout(fréquence ; amplitude) )
  - fréquence: fréquence mesurée par l'oscilloscope
  - amplutide: amplitude de la sortie du filtre mesurée par le multimètre

# (OPTIONNEL) mode rapide FFT, bruit en entrée 

- Mesure : 
  - Le bruit blanc est appliqué à l'entrée du filtre, et le signal de sortie est capturé.
- Gain et phase : 
  - La FFT permet d'extraire le gain et le déphasage du filtre pour chaque fréquence.
- Rapide et efficace : 
  - Cette méthode caractérise le comportement du filtre en une seule mesure sur toute la bande passante.
- Applications : 
  - Utilisée en électronique, audio, et télécommunications pour évaluer les filtres passe-bas, passe-haut, et autres.