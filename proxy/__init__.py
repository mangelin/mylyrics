from .abstractLyrics import (
    ArtistNotFoundException,
    LyricNotFoundException,
    OutputTypeNotFound
)
from .azlyrics import AzlyricsProxy
from .elyrics import ElyricsProxy
import config

class ProxyLyricsFactory():
    @staticmethod
    def create_proxy(typ:str):
        providers = config.providers()

        if (typ.lower()) not in providers:
            raise ValueError(f"Error: unkown provider {typ}\nvalid value are {','.join(providers)}")

        targetclass = f"{typ.capitalize()}Proxy"
        return globals()[targetclass]()