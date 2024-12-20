# fichier de gestion de l'interface utilisateur

import wx

class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='FilterAnalyzer', size=(400, 550))
        
        # Création d'un panneau
        panel = wx.Panel(self)

        # ---- Configuration de la fréquence ----
        freq_title = wx.StaticText(panel, label='Frequency Configuration:', pos=(20, 10))
        font = freq_title.GetFont()
        font.SetPointSize(11)
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        freq_title.SetFont(font)

        # Min frequency
        wx.StaticText(panel, label='Min frequency [Hz]:', pos=(20, 40))
        self.min_freq_ctrl = wx.TextCtrl(panel, pos=(180, 38), size=(100, -1))

        # Max frequency
        wx.StaticText(panel, label='Max frequency [Hz]:', pos=(20, 70))
        self.max_freq_ctrl = wx.TextCtrl(panel, pos=(180, 68), size=(100, -1))

        # ---- Configuration de l'amplitude ----
        amp_title = wx.StaticText(panel, label='Amplitude Configuration:', pos=(20, 110))
        font = amp_title.GetFont()
        font.SetPointSize(11)
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        amp_title.SetFont(font)

        # Amplitude
        wx.StaticText(panel, label='Amplitude [V]:', pos=(20, 140))
        self.amp_ctrl = wx.TextCtrl(panel, pos=(180, 138), size=(100, -1))

        # ---- Configuration Ethernet pour les appareils ----
        connection_title = wx.StaticText(panel, label='Ethernet Configuration:', pos=(20, 180))
        font = connection_title.GetFont()
        font.SetPointSize(11)
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        connection_title.SetFont(font)

        # Champs IP pour Oscilloscope et Générateur de fonction
        self.devices = ['Oscilloscope', 'Générateur de fonction']
        self.ip_controls = {}
        y_pos = 210

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
        return min_freq, max_freq

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
        if not self.validate_inputs():
            wx.MessageBox('Please specify all configuration values.', 'Error', wx.OK | wx.ICON_ERROR)
        else:
            min_freq, max_freq = self.get_frequency_config()
            amplitude = self.get_amplitude()
            ip_addresses = self.get_ip_addresses()

            # Afficher les configurations dans la console
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
    
    # fonction de la page de résultats de test lancée apres pression du bouton (avec bare de chargement et affichage des résultats) 
    def test_results(self):
        """Afficher la page de résultats de test."""
        # Créer une nouvelle fenêtre
        result_frame = wx.Frame(parent=None, title='Test Results', size=(400, 550))
        panel = wx.Panel(result_frame)

        # Barre de chargement
        gauge = wx.Gauge(panel, range=100, pos=(20, 20), size=(360, 25))
        gauge.SetValue(50)

        # Afficher les résultats
        result_text = wx.StaticText(panel, label='Test Results:', pos=(20, 60))
        font = result_text.GetFont()
        font.SetPointSize(11)
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        result_text.SetFont(font)

        # Afficher les résultats dans un texte
        results = "Results will be displayed here."
        results_text = wx.TextCtrl(panel, value=results, pos=(20, 90), size=(360, 400), style=wx.TE_MULTILINE | wx.TE_READONLY)

        # Afficher la fenêtre
        result_frame.Show()

if __name__ == '__main__':
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()
