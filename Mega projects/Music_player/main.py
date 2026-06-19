import os


from kivy.app import App
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout


Builder.load_file('music_player.kv')


class MusicPlayer(BoxLayout):
    songs = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        songs_folder = "songs"

        if os.path.exists(songs_folder):
            self.songs = [
                file for file in os.listdir(songs_folder) 
                if file.endswith(".mp3")
            ]


class MusicApp(App):
    def build(self):
        return MusicPlayer()
    

MusicApp().run()