import requests
from config import ELYRICS_SEARCH_URL
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import re

from .lyrics import LyricsRetriverProxy

# Helpers function
def _locate_string_value(soup, string_value):

    search_string = string_value.split(' ')[0]

    try:
        return soup.find("b",string=re.compile(search_string)).parent['href']
    except:
        pass
    return None


def _post_form(url, payload):
    r = requests.post(url, data=payload)
    if r.status_code != 200:
        return None
    return r.text

def _retrive_url(url:str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.text
class ElyricsProxy(LyricsRetriverProxy):
    def __init__(self):
        super().__init__()
        self._name = "ELyrics"

    def get_artist_page(self, artist:str):
        r = _post_form(ELYRICS_SEARCH_URL,{'q':artist})
        if not r:
            return None


        soup = bs(r, "html.parser")
        a_string = _locate_string_value(soup, artist.upper())
        if not a_string:
            return None

        return urljoin("https://elyrics.net",a_string)

    def get_lyrics_url(self, artist_page_url:str, song_name:str):
        r = _retrive_url(artist_page_url)
        if not r:
            return None

        soup = bs(r, "html.parser")

        song_label = soup.find(string=re.compile(f" {song_name.title()}"))
        if not song_label:
            return None
        
        song_relative_url = song_label.parent['href']
        song_url = urljoin(artist_page_url,song_relative_url)

        return song_url

    def retrive_lyrics(self, lyrics_url:str):
        return _retrive_url(lyrics_url)

    def to_txt(self, lyrics):
        soup = bs(lyrics, "html.parser")
        div_lyrics = soup.find(attrs={"id":"inlyr"})
        return div_lyrics.text
