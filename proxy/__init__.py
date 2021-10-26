from .azlyrics import AzlyricsProxy
from .elyrics import ElyricsProxy

class ProxyLyricsFactory():
    def create_proxy(self, typ:str):
        targetclass = f"{typ.capitalize()}Proxy"
        return globals()[targetclass]()
