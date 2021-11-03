import re
from urllib.parse import urljoin

import config
import requests
from bs4 import BeautifulSoup as bs

from .abstractLyrics import AbstractLyricsRetriverProxy
from .helpers import helper_retrive_url


# Helpers function
def _locate_anchor(soup, value):
    res = soup.find(string=re.compile(value, re.IGNORECASE))
    if not res:
        return None
    anchor = res.findParent("a")

    if not anchor:
        return None
    return anchor.get("href")


# AZLyrics concrete proxy
class AzlyricsProxy(AbstractLyricsRetriverProxy):
    def __init__(self):
        super().__init__()

        self._name = config.AZLYRICS_PROXY
        self._az_search_url = config.AZLYRICS_SEARCH_URL

    def get_artist_page_url(self, artist:str)->str:
        r = helper_retrive_url(f"{self._az_search_url}{artist}")
        if not r:
            return None

        soup = bs(r, "html.parser")
        a_string = soup.find(string=re.compile("Artist result"))
        if not a_string:
            return None

        t = a_string.findNext("table")
        if not t:
            return None

        return _locate_anchor(t, artist)

    def get_lyrics_url(self, artist_page_url:str, song_name:str)->str:
        r = helper_retrive_url(artist_page_url)
        if not r:
            return None

        soup = bs(r, "html.parser")

        song_relative_url = _locate_anchor(soup, song_name)
        if not song_relative_url:
            return None

        song_url = urljoin(artist_page_url,song_relative_url)

        return song_url

    def fetch_lyric_content(self, lyrics_url:str)->str:
        return helper_retrive_url(lyrics_url) # pragma: no cover

    def to_txt(self, lyrics):
        soup = bs(lyrics, "html.parser")
        div_ringtone = soup.find(attrs={"class":"ringtone"})
        div_lyrics = div_ringtone.findNext("div")
        return div_lyrics.text
