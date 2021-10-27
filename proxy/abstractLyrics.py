from abc import ABCMeta, abstractmethod
import os

from config import OUTPUT_FORMAT

class AbstractLyricsRetriverProxy(metaclass=ABCMeta):
    def __init__(self):
        self.outputs={
            'txt': self.to_txt
        }
    
    
    def provided_by(func):
        def inner(*args, **kwargs):
            t = func(*args, **kwargs) 
            t += f"\nProvided by {args[0].name}"
            return t
        return inner

    @provided_by
    def get_lyrics(self, artist: str, song_name:str, out_format:str=OUTPUT_FORMAT)->str:
        artist_page_url = self.get_artist_page_url(artist)
        if not artist_page_url:
            raise ValueError(f"Artist {artist} not found")

        lyrics_url = self.get_lyrics_url(artist_page_url, song_name)
        if not lyrics_url:
            raise ValueError(f"Url Lyrics for {song_name} by {artist} not found")

        lyrics = self.fetch_lyric_content(lyrics_url)
        if not lyrics:
            raise ValueError(f"Lyrics for {song_name} by {artist} not found")

        return self.__format_result(lyrics, out_format)
        
    
    @property
    def name(self):
        return getattr(self,"_name","undefined")
    
    def __format_result(self, lyrics:str, out_typ:str)->str:
        outf = self.outputs[out_typ]
        if not outf:
            raise ValueError(f"Unknown output type {out_typ}")

        return outf(lyrics)

    @abstractmethod
    def get_artist_page_url(self, artist:str)->str:
        raise NotImplementedError # pragma: no cover

    @abstractmethod
    def get_lyrics_url(self, artist_page_url:str, song_name:str)->str:
        raise NotImplementedError # pragma: no cover

    @abstractmethod
    def fetch_lyric_content(self, lyrics_url:str)->str:
        raise NotImplementedError # pragma: no cover

    @abstractmethod
    def to_txt(self, lyrics:str):
        raise NotImplementedError # pragma: no cover
