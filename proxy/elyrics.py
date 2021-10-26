from .lyrics import LyricsRetriverProxy
class ElyricsProxy(LyricsRetriverProxy):
    def __init__(self):
        super().__init__()
        self._name = "ELyrics"

    def get_artist_page(self, artist:str):
        pass

    def get_lyrics_url(self, artist_page_url:str, song_name:str):
        pass

    def retrive_lyrics(self, lyrics):
        pass

    def to_txt(self, lyrics):
        pass