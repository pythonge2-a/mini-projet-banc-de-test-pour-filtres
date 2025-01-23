# fichier de gestion de l'interface utilisateur

import wx
import matplotlib
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import time

import tek_scope
import Agilent_GenFct
import siglentmultimeter
import pyvisa
import filtermathRDG

class MainFrame(wx.Frame):
    def __init__(self):

        # Créer une fenêtre principale
        super().__init__(parent=None, title='FilterAnalyzer', size=(380, 600)) 
        # cengtre la fenetre
        self.Centre()
        
        # Création d'un panneau
        panel = wx.Panel(self)

        # enlève le bouton d'agrangissement de la fenêtre
        self.SetWindowStyle(self.GetWindowStyle() & ~wx.MAXIMIZE_BOX)

        # ---- Configuration de la fréquence ----
        freq_title = wx.StaticText(panel, label='Frequency Configuration:', pos=(20, 10))
        font = freq_title.GetFont()
        font.SetPointSize(11)
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        freq_title.SetFont(font)

        # Min frequency
        wx.StaticText(panel, label='Min frequency [Hz]:', pos=(20, 40))
        self.min_freq_ctrl = wx.TextCtrl(panel, pos=(180, 38), size=(100, -1))
        # unités, kilo, mega, giga pour la fréquence
        self.unitMinF = wx.ComboBox(panel, pos=(300, 38), choices=['Hz', 'kHz', 'MHz', 'GHz'], style=wx.CB_READONLY)
        self.unitMinF.SetSelection(0)

        # Max frequency
        wx.StaticText(panel, label='Max frequency [Hz]:', pos=(20, 70))
        self.max_freq_ctrl = wx.TextCtrl(panel, pos=(180, 68), size=(100, -1))
        # unités, kilo, mega, giga pour la fréquence
        self.unitMaxF = wx.ComboBox(panel, pos=(300, 68), choices=['Hz', 'kHz', 'MHz', 'GHz'], style=wx.CB_READONLY)
        self.unitMaxF.SetSelection(0)

        # ---- Configuration du nombre de points ----
        points_title = wx.StaticText(panel, label='Number of Points Configuration:', pos=(20, 110))
        font = points_title.GetFont()
        font.SetPointSize(11)
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        points_title.SetFont(font)

        # Number of points
        wx.StaticText(panel, label='Number of Points:', pos=(20, 140))
        self.points_ctrl = wx.TextCtrl(panel, pos=(180, 138), size=(100, -1))
        # unités, kilo, mega, giga pour le nombre de points
        self.unitPoint = wx.ComboBox(panel, pos=(300, 138), choices=['-', 'k', 'M', 'G'], style=wx.CB_READONLY)
        self.unitPoint.SetSelection(0)

        # ---- Configuration de l'amplitude ----
        amp_title = wx.StaticText(panel, label='Amplitude Configuration:', pos=(20, 180))
        font = amp_title.GetFont()
        font.SetPointSize(11)
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        amp_title.SetFont(font)

        # Amplitude
        wx.StaticText(panel, label='Amplitude [V]:', pos=(20, 208))
        self.amp_ctrl = wx.TextCtrl(panel, pos=(180, 208), size=(100, -1))

        # ---- Configuration Ethernet pour les appareils ----
        connection_title = wx.StaticText(panel, label='Ethernet Configuration:', pos=(20, 250))
        font = connection_title.GetFont()
        font.SetPointSize(11)
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        connection_title.SetFont(font)

        # Champs IP pour Oscilloscope et Générateur de fonction
        self.devices = ['Oscilloscope', 'Générateur de fonction']
        self.ip_controls = {}
        y_pos = 280

        for device in self.devices:
            wx.StaticText(panel, label=f'{device} IP Address:', pos=(20, y_pos))
            self.ip_controls[device] = wx.TextCtrl(panel, pos=(20, y_pos + 20), size=(260, -1))
            y_pos += 60

        # Checkbox pour sélectionner le multimètre
        self.use_multimeter = wx.CheckBox(panel, label='Use Multimeter', pos=(20, y_pos))
        self.use_multimeter.Bind(wx.EVT_CHECKBOX, self.on_multimeter_checkbox)

        # Champ IP pour le Multimètre (initialement caché)
        self.multimeter_ip_label = wx.StaticText(panel, label='Multimeter IP Address:', pos=(20, y_pos + 30))
        self.multimeter_ip_ctrl = wx.TextCtrl(panel, pos=(20, y_pos + 50), size=(260, -1))
        self.multimeter_ip_label.Hide()
        self.multimeter_ip_ctrl.Hide()

        # Bouton : Start test
        button = wx.Button(panel, label='Start Test', pos=(130, y_pos + 90), size=(140, 40))
        button.Bind(wx.EVT_BUTTON, self.on_button_click)

        # Affichage de la fenêtre
        self.Show()

    def on_multimeter_checkbox(self, event):
        """Afficher ou masquer le champ IP du multimètre selon l'état de la checkbox."""
        if self.use_multimeter.IsChecked():
            self.multimeter_ip_label.Show()
            self.multimeter_ip_ctrl.Show()
        else:
            self.multimeter_ip_label.Hide()
            self.multimeter_ip_ctrl.Hide()

    def get_frequency_config(self):
        """Récupérer les valeurs de fréquence."""
        min_freq = self.min_freq_ctrl.GetValue()
        max_freq = self.max_freq_ctrl.GetValue()

        # Convertir les unités de fréquence
        unitMinF = self.unitMinF.GetValue()
        unitMaxF = self.unitMaxF.GetValue()

        if unitMinF == 'kHz':
            min_freq = float(min_freq) * 1e3
        elif unitMinF == 'MHz':
            min_freq = float(min_freq) * 1e6
        elif unitMinF == 'GHz':
            min_freq = float(min_freq) * 1e9

        if unitMaxF == 'kHz':
            max_freq = float(max_freq) * 1e3
        elif unitMaxF == 'MHz':
            max_freq = float(max_freq) * 1e6
        elif unitMaxF == 'GHz':
            max_freq = float(max_freq) * 1e9

        return min_freq, max_freq
    
    def get_points_config(self):
        """Récupérer les valeurs de points."""
        points = self.points_ctrl.GetValue()

        # Convertir les unités de points
        unitPoint = self.unitPoint.GetValue()

        if unitPoint == 'k':
            points = float(points) * 1e3
        elif unitPoint == 'M':
            points = float(points) * 1e6
        elif unitPoint == 'G':
            points = float(points) * 1e9

        return points

    def get_amplitude(self):
        """Récupérer la valeur de l'amplitude."""
        return self.amp_ctrl.GetValue()

    def get_ip_addresses(self):
        """Récupérer les adresses IP des appareils."""
        ip_addresses = {device: ctrl.GetValue() for device, ctrl in self.ip_controls.items()}
        if self.use_multimeter.IsChecked():
            ip_addresses['Multimètre'] = self.multimeter_ip_ctrl.GetValue()
        return ip_addresses

    def validate_inputs(self):
        """Vérifier si toutes les valeurs sont spécifiées."""
        min_freq, max_freq = self.get_frequency_config()
        amplitude = self.get_amplitude()
        ip_addresses = self.get_ip_addresses()

        # Vérifier les valeurs vides
        if not min_freq or not max_freq or not amplitude:
            return False
        for ip in ip_addresses.values():
            if not ip:
                return False
        return True

    def on_button_click(self, event):
        """Récupérer et afficher les configurations si toutes les valeurs sont spécifiées."""

        # Vérifier si les valeurs entrées sont entre 0 et 9 et . pour les champs min et max fréquence
        if not self.min_freq_ctrl.GetValue().replace('.','').isdigit() or not self.max_freq_ctrl.GetValue().replace('.','').isdigit():
            wx.MessageBox('Please enter only numbers for frequency.', 'Error', wx.OK | wx.ICON_ERROR)
            return

        # Vérifier si les valeurs entrées sont entre 0 et 9 et . pour lee champ nombre de points
        if not self.points_ctrl.GetValue().replace('.','').isdigit():
            wx.MessageBox('Please enter only numbers for number of points.', 'Error', wx.OK | wx.ICON_ERROR)
            return

        # Vérifier si les valeurs entrées sont entre 0 et 9 et . pour le champ amplitude
        if not self.amp_ctrl.GetValue().replace('.','').isdigit():
            wx.MessageBox('Please enter only numbers for amplitude.', 'Error', wx.OK | wx.ICON_ERROR)
            return

        # Vérifier si les valeurs entrées sont entre 0 et 9 et . pour les champs IP
        for device, ctrl in self.ip_controls.items():
            if not ctrl.GetValue().replace('.','').isdigit():
                wx.MessageBox('Please enter only numbers for IP addresses.', 'Error', wx.OK | wx.ICON_ERROR)
                return   

        if not self.validate_inputs():
            wx.MessageBox('Please specify all configuration values.', 'Error', wx.OK | wx.ICON_ERROR)
        else:
            min_freq, max_freq = self.get_frequency_config()
            amplitude = self.get_amplitude()
            ip_addresses = self.get_ip_addresses()

            # Afficher les configurations dans la console fois les unités converties
            print("Configuration Summary:")
            print(f"Min Frequency: {min_freq} Hz")
            print(f"Max Frequency: {max_freq} Hz")
            print(f"Amplitude: {amplitude} V")
            print("\nEthernet Configuration:")
            for device, ip in ip_addresses.items():
                print(f"{device}: {ip}")

            # Lancer la page de résultats de test
            self.test_results()

        # retourner les valeurs de configuration
        return min_freq, max_freq, amplitude, ip_addresses

    # fonction pour la mise à jour de la barre de chargement
    def update_progress(self, progress):
        """Mettre à jour la barre de progression."""
        gauge = self.FindWindowById(1)
        gauge.SetValue(progress)
    
    def test_results(self):
        # Créer une nouvelle fenêtre pour les résultats
        result_frame = wx.Frame(parent=None, title='Test Results', size=(1000, 800))
        panel = wx.Panel(result_frame)

        # Barre de chargement
        gauge = wx.Gauge(panel, range=100, pos=(20, 20), size=(360, 25))
        gauge.SetValue(10)

        # ------------ Séquence de test ------------

        pk2pk = float(self.get_amplitude())
        min_freq, max_freq = self.get_frequency_config()
        min_freq = float(min_freq)
        max_freq = float(max_freq)
        points = int(self.get_points_config())
        ip = self.get_ip_addresses()

        gain_x, gain_y, phase_x, phase_y = [], [], [], []

        try:
            # Connexion aux instruments
            function_gen = Agilent_GenFct.Agilent33220A(ip['Générateur de fonction'])
            function_gen.connect()
            function_gen.set_amplitude(pk2pk)
            function_gen.set_waveform('SIN')
            function_gen.ActiveOutput()

            scope = tek_scope.Tektronix_scope(ip['Oscilloscope'])

            # Check if multimeter is used
            if self.use_multimeter.IsChecked():
                multimeter = siglentmultimeter.SiglentMultimeter(ip['Multimètre'])
                multimeter.connect()
            
            # Premier point
            freq = min_freq
            function_gen.set_frequency(freq)
            time.sleep(2)

            scope.rescale_channels(frequence=freq)
            time.sleep(2)

            # Mesures initiales
            freq_mes = scope.mesure_frequence()
            phase = scope.mesure_phase()

            # Check if multimeter is used
            if self.use_multimeter.IsChecked():
                multimeter.VacChangeMode()
                vOut = multimeter.mesure_v_ac()
                gain = filtermathRDG.get_gainDb(scope.mesure_VrmsCH1, vOut)
            else:
                gain = scope.mesure_gain()
        
            # Acquisition des données
            for i in range(0, points):
                freq = min_freq * (max_freq / min_freq) ** (i / (points - 1))
                function_gen.set_frequency(freq)
                time.sleep(0.1)

                scope.rescale_channels(frequence=freq)
                time.sleep(0.1)

                freq_mes = scope.mesure_frequence()
                phase = scope.mesure_phase()

                #si la fréquence dépasse 10^15, on suprime la valeur en question ainsi que le gain et la phase
                if freq_mes > 1e15:
                    freq_mes = None
                    gain = None
                    phase = None

                # Check if multimeter is used
                if self.use_multimeter.IsChecked():
                    multimeter.VacChangeMode()
                    vOut = multimeter.mesure_v_ac()
                    gain = filtermathRDG.get_gainDb(scope.mesure_VrmsCH1, vOut)

                else:
                    gain = scope.mesure_gain()

                if freq_mes is not None and gain is not None and phase is not None:
                    gain_x.append(freq_mes)
                    gain_y.append(gain)
                    phase_x.append(freq_mes)
                    phase_y.append(phase)
                else:
                    print(f"⚠ Erreur de mesure à {freq:.2f} Hz, valeurs ignorées.")

            # Fermeture propre des instruments
            scope.deconnecter()
            function_gen.DeactiveOutput()
            function_gen.disconnect()

            # affiche gain_x, gain_y, phase_x, phase_y séparément
            print(f"Gain X: {gain_x}")
            print(f"Gain Y: {gain_y}")
            print(f"Phase X: {phase_x}")
            print(f"Phase Y: {phase_y}")

            #supression des valeurs abérrantes de phase (supérieur à 90° et inférieur à -90°) et de la fréquence apartenant à la phase
            for i in range(len(phase_y)):
                if phase_y[i] > 90 or phase_y[i] < -90:
                    phase_y[i] = None
                    gain_y[i] = None
                    gain_x[i] = None

        except Exception as e:
            print(f"Erreur lors de la connexion ou de l'acquisition : {e}")
            wx.MessageBox(f"Erreur lors de la connexion ou de l'acquisition : {e}", 'Error', wx.OK | wx.ICON_ERROR)
            return

        # ------------ Résultats calculés ------------

        # dictionnaire de données (gain_x, et gain_y) 
        data = dict(zip(gain_x, gain_y))

        results = {
            'frequence_coupure': [filtermathRDG.get_cutoff_frequency(data)],  # Exemple statique, ajustez selon vos calculs
            'facteur_qualite': filtermathRDG.get_quality_factor(data),
            'ordre': filtermathRDG.get_order(data)
        }

        # ------------ Affichage des résultats ------------

        # Créer un graphique matplotlib
        figure = Figure(figsize=(6, 4))
        ax1 = figure.add_subplot(211)
        ax2 = figure.add_subplot(212)
        figure.subplots_adjust(hspace=0.5)

        # Tracer le graphique logarithmique pour le gain, la fréquence vas de 10^3 en 10^3
        ax1.set_xscale('log')
        ax1.plot(gain_x, gain_y, marker='o', color='blue', label='Amplitude')
        ax1.set_title('Amplitude (Log-Log)')
        ax1.set_xlabel('Frequency (Hz)')
        ax1.set_ylabel('Amplitude')
        ax1.legend()
        ax1.grid(True, which='both', linestyle='--')
        # trace une ligne à la fréquence de coupure
        ax1.axvline(x=results['frequence_coupure'][0], color='red', linestyle='--', label='Fréquence de coupure')
        ax1.legend()

        # Tracer le graphique logarithmique pour la phase, la fréquence vas de 10^3 en 10^3
        ax2.set_xscale('log')
        ax2.plot(phase_x, phase_y, marker='s', color='green', label='Phase')
        ax2.set_title('Phase (Semi-Log)')
        ax2.set_xlabel('Frequency (Hz)')
        ax2.set_ylabel('Phase (degrees)')
        ax2.legend()
        ax2.grid(True, which='both', linestyle='--')

        # Intégrer matplotlib dans wxPython
        canvas = FigureCanvas(panel, -1, figure)

        # Ajouter les résultats sous forme de texte
        results_text = (
            f"Fréquences de coupure : {', '.join([f'{fc} Hz' for fc in results['frequence_coupure']])}\n"
            f"Facteur de qualité (Q) : {results['facteur_qualite']}\n"
            f"Ordre du filtre : {results['ordre']}\n"
            f"Nombre de points : {self.get_points_config()}"
        )
        results_label = wx.StaticText(panel, label=results_text, pos=(20, 40))

        # Appliquer un style au texte
        font = wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        results_label.SetFont(font)

        # ------------ Bouton de redémarrage ------------

        restart_button = wx.Button(panel, label='Restart Test', size=(180, 40))
        button_font = wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        restart_button.SetFont(button_font)
        restart_button.Bind(wx.EVT_BUTTON, self.restart_test)

        # ------------ Mise en page ------------

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(gauge, 0, wx.ALL | wx.EXPAND, 10)
        sizer.Add(canvas, 1, wx.ALL | wx.EXPAND, 10)
        sizer.Add(results_label, 0, wx.ALL | wx.EXPAND, 10)
        sizer.Add(restart_button, 0, wx.ALL | wx.CENTER, 10)
        panel.SetSizer(sizer)

        # Afficher la fenêtre
        result_frame.Show()


    def restart_test(self, event):
        """Redémarrer le test en fermant la fenêtre actuelle et rouvrant la configuration principale."""
        # Fermer toutes les fenêtres ouvertes (page de résultats)
        for child in wx.GetTopLevelWindows():
            if isinstance(child, wx.Frame) and child.GetTitle() == 'Test Results':
                    child.Destroy()

        # Rouvrir la fenêtre principale (optionnel, selon besoin)
        self.Show()


if __name__ == '__main__':
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()
