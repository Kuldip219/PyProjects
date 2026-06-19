from kivy.lang import Builder
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

Builder.load_file('music_player.kv')

class MusicPlayer(BoxLayout):
    pass


class MusicApp(App):
    def build(self):
        return MusicPlayer()
    

MusicApp().run()