# fichier de gestion de l'interface utilisateur

import wx

class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='FilterAnalyzer', size=(400, 400))
        
        # Création d'un panneau
        panel = wx.Panel(self)

        # Titre : Frequency
        freq_title = wx.StaticText(panel, label='Frequency :', pos=(20, 20))
        font = freq_title.GetFont()
        font.SetPointSize(11)
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        freq_title.SetFont(font)

        # Texte statique : Min frequency
        min_freq_label = wx.StaticText(panel, label='Min frequency', pos=(40, 50))
        self.min_freq_ctrl = wx.TextCtrl(panel, pos=(130, 50), size=(100, -1))
        min_freq_unit = wx.StaticText(panel, label='[Hz]', pos=(233, 52))   

        # Texte statique : Max frequency
        max_freq_label = wx.StaticText(panel, label='Max frequency', pos=(40, 80))
        self.max_freq_ctrl = wx.TextCtrl(panel, pos=(130, 80), size=(100, -1))
        max_freq_unit = wx.StaticText(panel, label='[Hz]', pos=(233, 82))

        # Titre : Input amplitude
        input_amp_title = wx.StaticText(panel, label='Input amplitude :', pos=(20, 110))
        font = input_amp_title.GetFont()
        font.SetPointSize(11)
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        input_amp_title.SetFont(font)

        # Entrée texte amplitude
        self.amplitude_ctrl = wx.TextCtrl(panel, pos=(130, 140), size=(100, -1))
        input_amp_unit = wx.StaticText(panel, label='[V]', pos=(233, 142))

        # ---- Choix entre USB ou Ethernet ----
        # Titre : Connection
        connection_title = wx.StaticText(panel, label='Connection :', pos=(20, 170))
        font = connection_title.GetFont()
        font.SetPointSize(11)
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        connection_title.SetFont(font)

        # Choix entre USB ou Ethernet (radio button)
        self.radio_box = wx.RadioBox(panel, label='USB/Eth.', pos=(130, 190), choices=['USB', 'Ethernet'], majorDimension=1, style=wx.RA_SPECIFY_COLS)
        self.radio_box.Bind(wx.EVT_RADIOBOX, self.on_radio_selection)

        # Section USB Configuration
        self.usb_label = wx.StaticText(panel, label='USB ID:', pos=(40, 250))
        self.usb_ctrl = wx.TextCtrl(panel, pos=(130, 248), size=(100, -1))

        # Section Ethernet Configuration
        self.ip_label = wx.StaticText(panel, label='IP Address:', pos=(40, 250))
        self.ip_ctrl = wx.TextCtrl(panel, pos=(130, 248), size=(100, -1))

        self.port_label = wx.StaticText(panel, label='Port:', pos=(40, 280))
        self.port_ctrl = wx.TextCtrl(panel, pos=(130, 278), size=(100, -1))

        # Cacher les champs au démarrage
        self.show_usb_fields()

        # Affichage de la fenêtre
        self.Show()

    def on_radio_selection(self, event):
        selection = self.radio_box.GetStringSelection()
        if selection == 'USB':
            self.show_usb_fields()
        elif selection == 'Ethernet':
            self.show_ethernet_fields()

    def show_usb_fields(self):
        # Afficher les champs USB et cacher les champs Ethernet
        self.usb_label.Show()
        self.usb_ctrl.Show()

        self.ip_label.Hide()
        self.ip_ctrl.Hide()
        self.port_label.Hide()
        self.port_ctrl.Hide()

    def show_ethernet_fields(self):
        # Afficher les champs Ethernet et cacher les champs USB
        self.usb_label.Hide()
        self.usb_ctrl.Hide()

        self.ip_label.Show()
        self.ip_ctrl.Show()
        self.port_label.Show()
        self.port_ctrl.Show()

if __name__ == '__main__':
    app = wx.App(False)  # L'objet principal de l'application
    frame = MainFrame()  # Création de la fenêtre principale
    app.MainLoop()       # Lancement de la boucle principale
