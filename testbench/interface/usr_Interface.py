# fichier de gestion de l'inteface utilisateur

import wx

class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='FilterAnalyzer', size=(400, 300))
        
        # Création d'un panneau
        panel = wx.Panel(self)
        
        # texte statique parametrage fréquence
        text = wx.StaticText(panel, label='Input frequency', pos=(20, 20))

        # zone de texte parametrage fréquence
        self.text_ctrl = wx.TextCtrl(panel, pos=(150, 20))
        
        # texte statique parametrage amplitude
        text = wx.StaticText(panel, label='Input amplitude', pos=(20, 50))

        # zone de texte parametrage amplitude
        self.text_ctrl = wx.TextCtrl(panel, pos=(150, 50))

        # texte statique parametrage forme d'onde
        text = wx.StaticText(panel, label='Input waveform', pos=(20, 80))

        # boutons parametrage forme d'onde
        self.radio1 = wx.RadioButton(panel, label='Sinus', pos=(150, 80))
        self.radio2 = wx.RadioButton(panel, label='Square', pos=(150, 100))
        self.radio3 = wx.RadioButton(panel, label='Triangle', pos=(150, 120))
        self.radio4 = wx.RadioButton(panel, label='Sawtooth', pos=(150, 140))                       

        # Création d'un bouton
        button = wx.Button(panel, label='Launch test', pos=(150, 200))
        button.Bind(wx.EVT_BUTTON, self.on_button_click)
        
        # Affichage de la fenêtre
        self.Show()

    def on_button_click(self, event):
        wx.MessageBox('Le bouton a été cliqué !', 'Information', wx.OK | wx.ICON_INFORMATION)

if __name__ == '__main__':
    app = wx.App(False)  # L'objet principal de l'application
    frame = MainFrame()  # Création de la fenêtre principale
    app.MainLoop()       # Lancement de la boucle principale


