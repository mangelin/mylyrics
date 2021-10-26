from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import requests, re

from config import AZLYRICS_SEARCH_URL

from .lyrics import LyricsRetriverProxy

# Helpers function
def _locate_string_value(soup, string_value):
    return soup.find(string=re.compile(string_value))

def _locate_table(soup):
    return soup.findNext("table")

def _locate_anchor(soup, value):
    res = soup.find(string=re.compile(value))
    if not res:
        return None
    return res.findParent("a")

def _retrive_url(url:str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.text

# AzLyrics.com proxy
class AzlyricsProxy(LyricsRetriverProxy):
    def __init__(self):
        super().__init__()

        self._name = "AZLyrics"
        self._az_search_url = AZLYRICS_SEARCH_URL

    def get_artist_page(self, artist:str):
        r = _retrive_url(f"{self._az_search_url}{artist}")
        if not r:
            return None

        soup = bs(r, "html.parser")
        a_string = _locate_string_value(soup, "Artist result")
        if not a_string:
            return None

        t = _locate_table(a_string)
        if not t:
            return None

        anchor = _locate_anchor(t, artist)
        if not anchor:
            return None

        return anchor.get("href")

    def get_lyrics_url(self, artist_page_url:str, song_name:str):
        r = _retrive_url(artist_page_url)
        if not r:
            return None

        soup = bs(r, "html.parser")

        anchor = _locate_anchor(soup, song_name)
        if not anchor:
            return None

        song_relative_url = anchor.get("href")
        song_url = urljoin(artist_page_url,song_relative_url)

        return song_url

    def retrive_lyrics(self, lyrics_url:str):
        return _retrive_url(lyrics_url)

    def to_txt(self, lyrics):
        soup = bs(lyrics, "html.parser")
        div_ringtone = soup.find(attrs={"class":"ringtone"})
        div_lyrics = div_ringtone.findNext("div")
        return div_lyrics.text
