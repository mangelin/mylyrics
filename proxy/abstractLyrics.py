import os
from abc import ABCMeta, abstractmethod

from config import OUTPUT_FORMAT

from .excpetion import (ArtistNotFoundException, LyricNotFoundException,
                        OutputTypeNotFound)


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

    """
    Implements proxy bahviour.

    Args:
        artist:     artist name
        song_name:  song name
        out_format: output file format
    
    Return:
        The lyrics formatted in the output format or None

    Raises:
        Value error in unable to find artist, song or content
    """
    @provided_by
    def get_lyrics(self, artist: str, song_name:str, out_format:str=OUTPUT_FORMAT)->str:
        artist_page_url = self.get_artist_page_url(artist)
        if not artist_page_url:
            raise ArtistNotFoundException(f"Artist {artist} not found")

        lyrics_url = self.get_lyrics_url(artist_page_url, song_name)
        if not lyrics_url:
            raise LyricNotFoundException(f"Url Lyrics for {song_name} by {artist} not found")

        lyrics = self.fetch_lyric_content(lyrics_url)
        if not lyrics:
            raise LyricNotFoundException(f"Lyrics for {song_name} by {artist} not found")

        return self._format_result(lyrics, out_format)
        
    
    @property
    def name(self):
        return getattr(self,"_name","undefined")
    
    def _format_result(self, lyrics:str, out_typ:str)->str:
        outf = self.outputs.get(out_typ)
        if not outf:
            raise OutputTypeNotFound(f"Unknown output type {out_typ}")

        return outf(lyrics)

    """
    Return the absolute url for the artist page
    Args:
        artist:  name of the artist
    
    Return:
        a string apresenting a url
    """
    @abstractmethod
    def get_artist_page_url(self, artist:str)->str:
        raise NotImplementedError # pragma: no cover

    """
    Return the absolute url for the song song_name
    Args:
        artist_page_url:  a string rapresenting the artist url page
        song_name:        the song name
    
    Return:
        a string apresenting a url
    """
    @abstractmethod
    def get_lyrics_url(self, artist_page_url:str, song_name:str)->str:
        raise NotImplementedError # pragma: no cover

    """
        retrun the content of the lyrics_url
        Args:
            lyrics_url:  a string, the url to retrive the song
        Return:
            lyrics content
    """
    @abstractmethod
    def fetch_lyric_content(self, lyrics_url:str)->object:
        raise NotImplementedError # pragma: no cover

    """
        Tranform the lyrics in txt
        Args:
            lyrics:  some encoded object rapresenting the lyrics

        Return:
            the lyrics in txt format
    """
    @abstractmethod
    def to_txt(self, lyrics:str):
        raise NotImplementedError # pragma: no cover
