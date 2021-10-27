import requests
from config import ELYRICS_SEARCH_URL
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import re

from .abstractLyrics import AbstractLyricsRetriverProxy
from .helpers import helper_post_form, helper_retrive_url

# Helpers function
def _locate_string_value(soup, string_value):

    search_string = string_value.split(' ')[0]

    try:
        return soup.find("b",string=re.compile(search_string)).parent['href']
    except:
        pass
    return None


class ElyricsProxy(AbstractLyricsRetriverProxy):
    def __init__(self):
        super().__init__()
        self._name = "ELyrics"

    def get_artist_page_url(self, artist:str)->str:
        r = helper_post_form(ELYRICS_SEARCH_URL,{'q':artist})
        if not r:
            return None


        soup = bs(r, "html.parser")
        a_string = _locate_string_value(soup, artist.upper())
        if not a_string:
            return None

        return urljoin("https://elyrics.net",a_string)

    def get_lyrics_url(self, artist_page_url:str, song_name:str)->str:
        r = helper_retrive_url(artist_page_url)
        if not r:
            return None

        soup = bs(r, "html.parser")

        song_label = soup.find(string=re.compile(f" {song_name.title()}"))
        if not song_label:
            return None
        
        song_relative_url = song_label.parent['href']
        song_url = urljoin(artist_page_url,song_relative_url)

        return song_url

    def fetch_lyric_content(self, lyrics_url:str)->str:
        return helper_retrive_url(lyrics_url)

    def to_txt(self, lyrics):
        soup = bs(lyrics, "html.parser")
        div_lyrics = soup.find(attrs={"id":"inlyr"})
        return div_lyrics.text
