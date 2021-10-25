from abc import ABCMeta, abstractmethod

class LyricsRetriverProxy(metaclass=ABCMeta):
    @abstractmethod
    def get_song(artist: str, song:str):
        raise NotImplementedError # pragma: no cover
    

class AzlyricsProxy(LyricsRetriverProxy):
    def get_song(artist: str, song:str):
        return f"AZLyrics get {song} of {artist}"


class ElyricsProxy(LyricsRetriverProxy):
    def get_song(artist: str, song:str):
        return f"ELyrics get {song} of {artist}"

class ProxyLyricsFactory():
    def create_proxy(self, typ:str):
        targetclass = f"{typ.capitalize()}Proxy"
        return globals()[targetclass]