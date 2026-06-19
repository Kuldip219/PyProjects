from kivy.app import App
from kivy.uix.boxlayout import BoxLayout


class MusicPlayer(BoxLayout):
    pass


class MusicApp(App):
    def build(self):
        return MusicPlayer()
    

MusicApp().run()