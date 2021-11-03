from .azlyrics import AzlyricsProxy
from .elyrics import ElyricsProxy
import config

ProxyLyricsFactory = {
    config.AZLYRICS_PROXY.lower(): AzlyricsProxy(),
    config.ELYRICS_PROXY.lower(): ElyricsProxy(),
}