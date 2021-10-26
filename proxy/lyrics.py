from abc import ABCMeta, abstractmethod
from slugify import slugify

from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin

class LyricsRetriverProxy(metaclass=ABCMeta):
    def get_song(self, artist: str, song_name:str):
        artist_page_url = self.get_artist_page(artist)
        if not artist_page_url:
            raise ValueError(f"Artist {artist} not found")

        lyrics = self.get_lyrics(artist_page_url, song_name)
        if not lyrics:
            raise ValueError(f"Lyrics for {song_name} by {artist} not found")

        return self.to_txt(lyrics)
    
    def save(self, artist:str, song_name:str, lyrics:str):
        file_name = f"./{slugify(artist)}/{slugify(song_name)}.txt"
        with open(file_name,"w") as f:
            f.write(lyrics)
    
    @property
    def name(self):
        return getattr(self,"_name","undefined")
    
    @abstractmethod
    def get_artist_page(self, artist:str):
        raise NotImplementedError # pragma: no cover

    @abstractmethod
    def get_lyrics(self, artist_page_url:str, song_name:str):
        raise NotImplementedError # pragma: no cover

    @abstractmethod
    def to_txt(self, lyrics:str):
        raise NotImplementedError # pragma: no cover


    def to_txt(self, lyrics):
        soup = bs(lyrics, "html.parser")
        div_ringtone = soup.find(attrs={"class":"ringtone"})
        div_lyrics = div_ringtone.findNext("div")
        return div_lyrics.text